import numpy as np
import time
from typing import List, Dict, Any, Union, Optional
import logging
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.core.types import ExplanationResult

logger = logging.getLogger(__name__)


class ShapExplainerWrapper:
    """
    Extracts SHAP (Shapley Additive exPlanations) token-level attributions.
    Provides robust multi-dimensional array handling, provenance tracking, and zero-dependency fallbacks.
    """
    def __init__(self, model_wrapper: HuggingFaceWrapper):
        self.model = model_wrapper
        self.explainer = None
        self._init_explainer()

    def _predict_fn(self, texts: Union[np.ndarray, List[str], str]) -> np.ndarray:
        """
        Adapter function ensuring text inputs are passed as List[str] to model wrapper.
        Uses batched pipeline prediction.
        """
        if isinstance(texts, np.ndarray):
            texts = texts.tolist()
        elif isinstance(texts, str):
            texts = [texts]

        clean_texts = [str(t) for t in texts]
        return self.model.predict_proba(clean_texts, batch_size=32)

    def _init_explainer(self):
        try:
            import shap
            self.explainer = shap.Explainer(self._predict_fn, masker=shap.maskers.Text())
        except Exception as e:
            logger.warning(f"SHAP package not available or initialization failed ({e}). Using Shapley LOO fallback.")
            self.explainer = None

    def explain(self, text: str, max_evals: int = 50) -> ExplanationResult:
        """
        Returns ExplanationResult with token SHAP value attributions for the top predicted class.
        Uses bounded max_evals and batched inference for speed.
        """
        t0 = time.perf_counter()

        if not text or not text.strip():
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="shap",
                explainer_used="none",
                runtime_ms=0.0,
            )

        fallback_reason = None
        if self.explainer is not None:
            try:
                try:
                    shap_values = self.explainer([text], max_evals=max_evals)
                except TypeError:
                    shap_values = self.explainer([text])
                probas = self._predict_fn([text])[0]
                top_class_idx = int(np.argmax(probas))

                tokens = shap_values.data[0]
                vals = shap_values.values

                if vals.ndim == 3:
                    vals_sample = vals[0]
                elif vals.ndim == 2:
                    vals_sample = vals
                else:
                    vals_sample = np.atleast_2d(vals)

                if vals_sample.ndim == 2:
                    if top_class_idx < vals_sample.shape[1]:
                        token_weights = vals_sample[:, top_class_idx]
                    else:
                        token_weights = vals_sample[:, 0]
                else:
                    token_weights = np.ravel(vals_sample)

                token_records = []
                result = {}
                for idx, (tok, val) in enumerate(zip(tokens, token_weights)):
                    tok_str = str(tok).strip()
                    if tok_str:
                        score = float(val)
                        token_records.append({
                            "token": tok_str,
                            "position": idx + 1,
                            "attribution": score
                        })
                        if tok_str not in result:
                            result[tok_str] = score

                runtime_ms = (time.perf_counter() - t0) * 1000.0
                return ExplanationResult(
                    token_weights=result,
                    token_attributions=token_records,
                    model_id=self.model.model_name,
                    text=text,
                    explainer_requested="shap",
                    explainer_used="shap",
                    fallback_used=False,
                    fallback_reason=None,
                    runtime_ms=runtime_ms,
                )
            except Exception as e:
                fallback_reason = str(e)
                logger.warning(f"SHAP explanation computation encountered ({e}). Falling back to Shapley LOO.")
        else:
            fallback_reason = "SHAP explainer initialization failed or unavailable"

        # Fallback Leave-One-Out (LOO) Shapley estimation
        exp_res = self._leave_one_out_explain(text)
        runtime_ms = (time.perf_counter() - t0) * 1000.0
        exp_res.runtime_ms = runtime_ms
        exp_res.fallback_used = True
        exp_res.fallback_reason = fallback_reason
        return exp_res

    def _leave_one_out_explain(self, text: str) -> ExplanationResult:
        """
        Robust Leave-One-Out Shapley feature importance estimator.
        """
        words = text.split()
        if not words:
            return ExplanationResult(
                token_weights={},
                token_attributions=[],
                model_id=self.model.model_name,
                text=text,
                explainer_requested="shap",
                explainer_used="loo_fallback",
                fallback_used=True,
            )

        orig_probas = self._predict_fn([text])[0]
        top_idx = int(np.argmax(orig_probas))
        orig_score = float(orig_probas[top_idx])

        token_records = []
        attributions = {}
        for i, word in enumerate(words):
            masked_words = [w for j, w in enumerate(words) if j != i]
            masked_text = " ".join(masked_words)
            if not masked_text.strip():
                masked_score = 0.5
            else:
                masked_score = float(self._predict_fn([masked_text])[0][top_idx])

            score = float(orig_score - masked_score)
            token_records.append({
                "token": word,
                "position": i + 1,
                "attribution": score
            })
            if word not in attributions:
                attributions[word] = score

        return ExplanationResult(
            token_weights=attributions,
            token_attributions=token_records,
            model_id=self.model.model_name,
            text=text,
            explainer_requested="shap",
            explainer_used="loo_fallback",
            fallback_used=True,
        )
