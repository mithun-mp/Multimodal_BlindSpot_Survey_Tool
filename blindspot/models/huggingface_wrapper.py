import time
import numpy as np
from typing import List, Dict, Union, Optional, Any
import logging
import warnings

# Suppress noisy Hugging Face, PyTorch, and Transformers deprecation/warning messages
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

from blindspot.core.types import PredictionResult, ModelMetadata


def normalize_label_name(label: str, num_classes: int = 2) -> str:
    """
    Standardizes label strings across different model architectures and datasets.
    E.g. 'LABEL_0' -> 'NEGATIVE' in 2-class, 'LABEL_1' -> 'POSITIVE'.
    """
    cleaned = str(label).strip()
    upper = cleaned.upper()

    if num_classes == 2:
        if upper in {"LABEL_0", "0", "NEG", "NEGATIVE"}:
            return "NEGATIVE"
        if upper in {"LABEL_1", "1", "POS", "POSITIVE"}:
            return "POSITIVE"
    elif num_classes == 3:
        if upper in {"LABEL_0", "0", "NEG", "NEGATIVE"}:
            return "NEGATIVE"
        if upper in {"LABEL_1", "1", "NEU", "NEUTRAL"}:
            return "NEUTRAL"
        if upper in {"LABEL_2", "2", "POS", "POSITIVE"}:
            return "POSITIVE"

    return upper


class HuggingFaceWrapper:
    """
    Model-agnostic wrapper for Hugging Face sequence classification models.
    Provides standardized probability predictions compatible with LIME, SHAP,
    multiclass evaluations, and behavioral evaluation routines.
    """
    def __init__(
        self,
        model_name_or_path: str = "distilbert-base-uncased-finetuned-sst-2-english",
        device: Optional[str] = None,
        allow_fallback: bool = False,
    ):
        self.model_name = model_name_or_path
        self.pipeline = None
        self.device = device or ("cuda" if self._has_cuda() else "cpu")
        self.allow_fallback = allow_fallback
        self.load_error: Optional[str] = None
        self.labels: List[str] = ["NEGATIVE", "POSITIVE"]
        self.raw_id2label: Dict[int, str] = {0: "NEGATIVE", 1: "POSITIVE"}
        self.num_classes: int = 2
        self.parameters_millions: Optional[float] = None
        self.architecture: str = "transformer"
        self._load_model()

    @staticmethod
    def _has_cuda() -> bool:
        try:
            import torch
            return torch.cuda.is_available()
        except Exception:
            return False

    def _load_model(self):
        try:
            from transformers import pipeline, AutoConfig, AutoModelForSequenceClassification

            logger.info(f"Loading Hugging Face pipeline for: {self.model_name} on {self.device}")
            device_arg = 0 if self.device == "cuda" else -1

            try:
                self.pipeline = pipeline(
                    "text-classification",
                    model=self.model_name,
                    device=device_arg,
                    use_fast=True,
                    top_k=None,
                )
            except Exception:
                try:
                    self.pipeline = pipeline(
                        "text-classification",
                        model=self.model_name,
                        device=device_arg,
                        use_fast=True,
                        return_all_scores=True,
                    )
                except Exception:
                    self.pipeline = pipeline(
                        "text-classification",
                        model=self.model_name,
                        device=device_arg,
                        use_fast=False,
                        return_all_scores=True,
                    )

            # Extract model configuration & class counts
            if hasattr(self.pipeline.model, "config"):
                cfg = self.pipeline.model.config
                if hasattr(cfg, "id2label") and cfg.id2label:
                    self.raw_id2label = cfg.id2label
                    self.num_classes = len(self.raw_id2label)
                    # Normalize labels
                    self.labels = [
                        normalize_label_name(self.raw_id2label[i], self.num_classes)
                        for i in sorted(self.raw_id2label.keys())
                    ]
                if hasattr(cfg, "architectures") and cfg.architectures:
                    self.architecture = cfg.architectures[0]

            # Estimate model parameters
            if hasattr(self.pipeline.model, "parameters"):
                num_params = sum(p.numel() for p in self.pipeline.model.parameters())
                self.parameters_millions = round(num_params / 1e6, 2)

        except Exception as e:
            self.load_error = str(e)
            if not self.allow_fallback:
                logger.error(f"Failed to load real HF pipeline for {self.model_name}: {e}")
                self.pipeline = None
            else:
                logger.warning(f"Could not load real HF pipeline ({e}). Initializing fallback rule-based classifier.")
                self.pipeline = None
                self.labels = ["NEGATIVE", "POSITIVE"]
                self.num_classes = 2

    def get_metadata(self) -> ModelMetadata:
        """Returns structured ModelMetadata."""
        return ModelMetadata(
            model_id=self.model_name,
            architecture=self.architecture,
            task="text-classification",
            num_classes=self.num_classes,
            label_names=list(self.labels),
            device=self.device,
            parameters_millions=self.parameters_millions,
            verified=True,
            loaded=self.pipeline is not None,
            description=f"Model {self.model_name} with {self.num_classes} classes: {', '.join(self.labels)}",
        )

    def predict_proba(
        self,
        texts: Union[str, List[str], np.ndarray],
        batch_size: int = 32,
    ) -> np.ndarray:
        """
        Returns prediction probabilities array of shape (N, num_classes).
        Guarantees input sanitization for string types across third-party callers.
        Uses batched pipeline inference for high performance.
        """
        if isinstance(texts, np.ndarray):
            texts = texts.tolist()
        elif isinstance(texts, str):
            texts = [texts]
        elif not isinstance(texts, (list, tuple)):
            texts = [str(texts)]

        clean_texts = [str(t) for t in texts]
        if not clean_texts:
            return np.empty((0, len(self.labels)))

        if self.pipeline is not None:
            try:
                bs = min(len(clean_texts), max(1, batch_size))
                try:
                    results = self.pipeline(clean_texts, top_k=None, batch_size=bs)
                except Exception:
                    try:
                        results = self.pipeline(clean_texts, return_all_scores=True, batch_size=bs)
                    except Exception:
                        results = self.pipeline(clean_texts, batch_size=bs)

                # Normalize return structures across transformer pipeline versions
                if isinstance(results, dict):
                    results = [[results]]
                elif isinstance(results, list) and results and isinstance(results[0], dict):
                    results = [results]

                probas = []
                for res in results:
                    res_dict = {}
                    if isinstance(res, list):
                        for item in res:
                            if isinstance(item, dict) and 'label' in item:
                                norm_lbl = normalize_label_name(item['label'], self.num_classes)
                                res_dict[norm_lbl] = item['score']
                    elif isinstance(res, dict) and 'label' in res:
                        norm_lbl = normalize_label_name(res['label'], self.num_classes)
                        res_dict[norm_lbl] = res['score']

                    row = [float(res_dict.get(lbl, 0.0)) for lbl in self.labels]
                    s = sum(row)
                    if s > 0:
                        row = [x / s for x in row]
                    else:
                        row = [1.0 / len(self.labels)] * len(self.labels)
                    probas.append(row)

                return np.array(probas, dtype=np.float64)
            except Exception as e:
                # Check for CUDA OOM
                if "CUDA out of memory" in str(e) or "OutOfMemoryError" in type(e).__name__:
                    logger.warning("CUDA OOM detected! Falling back to CPU.")
                    self._recover_from_oom()
                    return self.predict_proba(clean_texts)
                if not self.allow_fallback:
                    raise RuntimeError(f"Inference error with HF pipeline for {self.model_name}: {e}") from e
                logger.warning(f"Inference error with HF pipeline ({e}). Falling back to heuristic probabilities.")
        else:
            if not self.allow_fallback:
                raise RuntimeError(
                    f"Model '{self.model_name}' pipeline is not loaded (load error: {self.load_error}) and allow_fallback=False."
                )

        # Fallback keyword/heuristic probabilistic classifier for testing when offline/unloaded
        probas = []
        positive_words = {"great", "good", "excellent", "awesome", "fantastic", "amazing", "love", "wonderful", "like"}
        negative_words = {"bad", "terrible", "awful", "horrible", "poor", "hate", "dislike", "worst", "boring"}

        for text in clean_texts:
            words = set(text.lower().split())
            pos_score = sum(1 for w in words if w in positive_words)
            neg_score = sum(1 for w in words if w in negative_words)

            if "not" in words or "n't" in words or "never" in words:
                pos_score, neg_score = neg_score, pos_score

            total = pos_score + neg_score
            if total == 0:
                p_pos = 0.5
            else:
                p_pos = (pos_score + 0.1) / (total + 0.2)
            p_neg = 1.0 - p_pos

            if self.num_classes == 2:
                probas.append([p_neg, p_pos])
            elif self.num_classes == 3:
                # Negative, Neutral, Positive
                p_neu = 0.2
                p_pos = p_pos * 0.8
                p_neg = p_neg * 0.8
                probas.append([p_neg, p_neu, p_pos])
            else:
                row = [p_neg, p_pos] + [0.0] * (self.num_classes - 2)
                probas.append(row)

        return np.array(probas, dtype=np.float64)

    def _recover_from_oom(self):
        """Clean up GPU memory and fallback to CPU."""
        try:
            import torch
            torch.cuda.empty_cache()
            self.device = "cpu"
            self._load_model()
        except Exception:
            pass

    def predict(self, texts: Union[str, List[str], np.ndarray]) -> List[str]:
        """Returns top predicted string labels for texts."""
        probas = self.predict_proba(texts)
        top_indices = np.argmax(probas, axis=1)
        return [self.labels[idx] for idx in top_indices]

    def predict_result(self, text: str) -> PredictionResult:
        """Runs inference on a single text and returns strongly typed PredictionResult."""
        t0 = time.perf_counter()
        proba_matrix = self.predict_proba([text])
        latency_ms = (time.perf_counter() - t0) * 1000.0

        probs_row = proba_matrix[0]
        top_idx = int(np.argmax(probs_row))
        confidence = float(probs_row[top_idx])
        label = self.labels[top_idx]
        probabilities = {self.labels[i]: float(probs_row[i]) for i in range(len(self.labels))}

        return PredictionResult(
            label=label,
            confidence=confidence,
            probabilities=probabilities,
            latency_ms=latency_ms,
            model_id=self.model_name,
            device=self.device,
            model_status="READY" if self.pipeline is not None else "HEURISTIC_FALLBACK",
        )

    def predict_results_batch(self, texts: List[str], batch_size: int = 16) -> List[PredictionResult]:
        """Runs batched inference across texts returning List[PredictionResult]."""
        if not texts:
            return []

        results: List[PredictionResult] = []
        for i in range(0, len(texts), batch_size):
            chunk = texts[i:i + batch_size]
            t0 = time.perf_counter()
            probs_matrix = self.predict_proba(chunk)
            chunk_latency = (time.perf_counter() - t0) * 1000.0
            per_item_latency = chunk_latency / max(1, len(chunk))

            for j, text in enumerate(chunk):
                row = probs_matrix[j]
                top_idx = int(np.argmax(row))
                confidence = float(row[top_idx])
                label = self.labels[top_idx]
                probabilities = {self.labels[k]: float(row[k]) for k in range(len(self.labels))}
                results.append(
                    PredictionResult(
                        label=label,
                        confidence=confidence,
                        probabilities=probabilities,
                        latency_ms=per_item_latency,
                        model_id=self.model_name,
                        device=self.device,
                        model_status="READY" if self.pipeline is not None else "HEURISTIC_FALLBACK",
                    )
                )

        return results
