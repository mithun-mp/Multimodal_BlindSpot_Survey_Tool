import numpy as np
import re
import time
from typing import List, Dict, Any, Tuple, Optional
import logging
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.core.types import ExplanationResult

logger = logging.getLogger(__name__)


class LimeExplainerWrapper:
    """
    Extracts LIME local word-level attributions for black-box text classifiers.
    Provides safe label index resolution, provenance tracking, and zero-dependency fallbacks.
    """
    def __init__(self, model_wrapper: HuggingFaceWrapper, random_seed: int = 42):
        self.model = model_wrapper
        self.random_seed = random_seed
        self.explainer = None
        self._init_explainer()

    def _init_explainer(self):
        try:
            from lime.lime_text import LimeTextExplainer
            self.explainer = LimeTextExplainer(
                class_names=self.model.labels,
                split_expression=r'\W+',
                random_state=self.random_seed
            )
        except Exception as e:
            logger.warning(f"LIME package not available or initialization failed ({e}). Using heuristic explainer fallback.")
            self.explainer = None

    def explain(
        self,
        text: str,
        num_features: int = 10,
        num_samples: int = 50,
    ) -> ExplanationResult:
        """
        Returns ExplanationResult mapping words to attribution scores for top predicted class.
        Uses batched inference and bounded sample count for fast CPU/GPU evaluation.
        """
        t0 = time.perf_counter()

        if not text or not text.strip():
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="lime",
                explainer_used="none",
                runtime_ms=0.0,
                random_seed=self.random_seed,
            )

        fallback_reason = None
        if self.explainer is not None:
            try:
                # Reset random states before explanation to guarantee reproducibility across calls
                if self.random_seed is not None:
                    from sklearn.utils import check_random_state
                    rng = check_random_state(self.random_seed)
                    self.explainer.random_state = rng
                    if hasattr(self.explainer, "base"):
                        self.explainer.base.random_state = rng

                exp = self.explainer.explain_instance(
                    text,
                    lambda texts: self.model.predict_proba(texts, batch_size=32),
                    num_features=num_features,
                    num_samples=num_samples,
                )
                probas = self.model.predict_proba([text])[0]
                top_class_idx = int(np.argmax(probas))

                avail_labels = exp.available_labels() if hasattr(exp, "available_labels") else []
                if top_class_idx in avail_labels:
                    target_label = top_class_idx
                elif avail_labels:
                    target_label = avail_labels[0]
                else:
                    target_label = top_class_idx

                try:
                    list_weights = exp.as_list(label=target_label)
                except Exception:
                    list_weights = exp.as_list()

                weight_map = {word: float(weight) for word, weight in list_weights}
                words = re.findall(r'\b\w+\b', text)
                token_records = []
                for i, word in enumerate(words):
                    w_val = weight_map.get(word, weight_map.get(word.lower(), 0.0))
                    token_records.append({
                        "token": word,
                        "position": i + 1,
                        "attribution": w_val
                    })

                runtime_ms = (time.perf_counter() - t0) * 1000.0
                return ExplanationResult(
                    token_weights=weight_map,
                    token_attributions=token_records,
                    model_id=self.model.model_name,
                    text=text,
                    explainer_requested="lime",
                    explainer_used="lime",
                    fallback_used=False,
                    fallback_reason=None,
                    runtime_ms=runtime_ms,
                    random_seed=self.random_seed,
                )
            except Exception as e:
                fallback_reason = str(e)
                logger.warning(f"LIME explanation failed ({e}). Falling back to word-level perturbation estimator.")
        else:
            fallback_reason = "LIME package unavailable"

        # Fallback word-level perturbation estimator
        exp_res = self._leave_one_out_explain(text)
        runtime_ms = (time.perf_counter() - t0) * 1000.0
        exp_res.runtime_ms = runtime_ms
        exp_res.fallback_used = True
        exp_res.fallback_reason = fallback_reason
        return exp_res

    def _leave_one_out_explain(self, text: str) -> ExplanationResult:
        """
        Word-level Leave-One-Out importance estimator.
        """
        words = text.split()
        if not words:
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="lime",
                explainer_used="loo_fallback",
                fallback_used=True,
                random_seed=self.random_seed,
            )

        orig_probas = self.model.predict_proba([text])[0]
        top_idx = int(np.argmax(orig_probas))
        orig_score = float(orig_probas[top_idx])

        token_records = []
        weight_map = {}
        for i, word in enumerate(words):
            masked_words = [w for j, w in enumerate(words) if j != i]
            masked_text = " ".join(masked_words)
            if not masked_text.strip():
                masked_score = 0.5
            else:
                masked_score = float(self.model.predict_proba([masked_text])[0][top_idx])

            score = float(orig_score - masked_score)
            token_records.append({
                "token": word,
                "position": i + 1,
                "attribution": score
            })
            if word not in weight_map:
                weight_map[word] = score

        return ExplanationResult(
            token_weights=weight_map,
            token_attributions=token_records,
            model_id=self.model.model_name,
            text=text,
            explainer_requested="lime",
            explainer_used="loo_fallback",
            fallback_used=True,
            random_seed=self.random_seed,
        )
