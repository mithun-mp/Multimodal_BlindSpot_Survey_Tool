"""
Model Registry and Verification Service for BlindSpot.
Maintains curated presets, validates model identifiers, and probes configuration metadata.
"""
from typing import Dict, List, Optional, Any
import logging

from blindspot.core.types import ModelMetadata
from blindspot.models.huggingface_wrapper import normalize_label_name

logger = logging.getLogger(__name__)


from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Union
import logging

from blindspot.core.types import ModelMetadata
from blindspot.models.huggingface_wrapper import normalize_label_name

logger = logging.getLogger(__name__)


@dataclass
class ModelSpec:
    """Canonical model specification with explicit task, label space, and architecture."""
    model_id: str
    name: str
    task: str  # e.g., "SENTIMENT", "AI_TEXT_DETECTION", "OTHER"
    num_classes: int
    labels: List[str]
    architecture: str
    source: str = "HuggingFace"
    domain: str = "General"
    parameters_millions: Optional[float] = None
    default: bool = False
    description: str = ""
    license: str = "Unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "name": self.name,
            "task": self.task,
            "num_classes": self.num_classes,
            "label_names": list(self.labels),
            "architecture": self.architecture,
            "source": self.source,
            "domain": self.domain,
            "parameters_millions": self.parameters_millions,
            "default": self.default,
            "description": self.description,
            "license": self.license,
            "metadata": self.metadata,
        }


class ModelRegistry:
    """
    Central registry for verified models, task compatibility validation,
    and custom model registration.
    """
    # Curated, verified presets with explicit tasks
    PRESETS: Dict[str, Dict[str, Any]] = {
        # Model 1: DistilBERT (compact binary sentiment baseline)
        "distilbert-base-uncased-finetuned-sst-2-english": {
            "model_id": "distilbert-base-uncased-finetuned-sst-2-english",
            "name": "DistilBERT SST-2",
            "task": "SENTIMENT",
            "num_classes": 2,
            "label_names": ["NEGATIVE", "POSITIVE"],
            "architecture": "DistilBertForSequenceClassification",
            "parameters_millions": 66.96,
            "default": True,
            "source": "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
            "domain": "Movie Reviews (SST-2)",
            "license": "Apache-2.0",
            "description": "Compact BERT-family binary sentiment baseline fine-tuned on Stanford Sentiment Treebank.",
        },
        # Model 2: ALBERT (cross-layer parameter sharing, 2-class binary)
        "textattack/albert-base-v2-SST-2": {
            "model_id": "textattack/albert-base-v2-SST-2",
            "name": "ALBERT Base SST-2",
            "task": "SENTIMENT",
            "num_classes": 2,
            "label_names": ["NEGATIVE", "POSITIVE"],
            "architecture": "AlbertForSequenceClassification",
            "parameters_millions": 11.68,
            "default": True,
            "source": "textattack/albert-base-v2-SST-2",
            "domain": "Movie Reviews (SST-2)",
            "license": "Apache-2.0",
            "description": "A Lite BERT (ALBERT) architecture with cross-layer parameter sharing fine-tuned on SST-2 binary sentiment.",
        },
        # Model 3: Twitter RoBERTa Latest (3-class social sentiment)
        "cardiffnlp/twitter-roberta-base-sentiment-latest": {
            "model_id": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "name": "Twitter RoBERTa Latest (3-Class)",
            "task": "SENTIMENT",
            "num_classes": 3,
            "label_names": ["NEGATIVE", "NEUTRAL", "POSITIVE"],
            "architecture": "RobertaForSequenceClassification",
            "parameters_millions": 124.65,
            "default": True,
            "source": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "domain": "Social Media (Tweets)",
            "license": "MIT",
            "description": "RoBERTa fine-tuned on ~124M tweets with 3-class sentiment (negative, neutral, positive).",
        },
        # Model 4: BERT Base SST-2 (standard BERT architecture, binary)
        "textattack/bert-base-uncased-SST-2": {
            "model_id": "textattack/bert-base-uncased-SST-2",
            "name": "BERT Base SST-2",
            "task": "SENTIMENT",
            "num_classes": 2,
            "label_names": ["NEGATIVE", "POSITIVE"],
            "architecture": "BertForSequenceClassification",
            "parameters_millions": 109.48,
            "default": True,
            "source": "textattack/bert-base-uncased-SST-2",
            "domain": "Movie Reviews (SST-2)",
            "license": "Apache-2.0",
            "description": "Full BERT Base architecture fine-tuned on SST-2 binary sentiment.",
        },
        # Model 5: Twitter RoBERTa Base (3-class social sentiment, distinct checkpoint)
        "cardiffnlp/twitter-roberta-base-sentiment": {
            "model_id": "cardiffnlp/twitter-roberta-base-sentiment",
            "name": "Twitter RoBERTa Base (3-Class)",
            "task": "SENTIMENT",
            "num_classes": 3,
            "label_names": ["NEGATIVE", "NEUTRAL", "POSITIVE"],
            "architecture": "RobertaForSequenceClassification",
            "parameters_millions": 124.65,
            "default": True,
            "source": "cardiffnlp/twitter-roberta-base-sentiment",
            "domain": "Social Media (Tweets)",
            "license": "MIT",
            "description": "RoBERTa Base trained on tweet sentiment analysis (negative, neutral, positive).",
        },
        # NON-SENTIMENT MODEL: AI Text Detector (strictly task: AI_TEXT_DETECTION)
        # Must NEVER participate in SENTIMENT_ROBUSTNESS experiments
        "roberta-base-openai-detector": {
            "model_id": "roberta-base-openai-detector",
            "name": "RoBERTa OpenAI Detector",
            "task": "AI_TEXT_DETECTION",
            "num_classes": 2,
            "label_names": ["Fake", "Real"],
            "architecture": "RobertaForSequenceClassification",
            "parameters_millions": 124.65,
            "default": False,
            "source": "openai/roberta-base-openai-detector",
            "domain": "Synthetic Text Detection",
            "license": "MIT",
            "description": "RoBERTa model detecting synthetic AI text (Outputs: Fake, Real). INELIGIBLE FOR SENTIMENT BENCHMARKS.",
        },
    }

    def __init__(self):
        self._custom_models: Dict[str, Dict[str, Any]] = {}

    def list_presets(self, task: Optional[str] = "SENTIMENT") -> List[Dict[str, Any]]:
        """
        Returns list of curated preset specifications.
        If task is specified, filters models strictly by task compatibility.
        """
        all_models = list(self.PRESETS.values()) + list(self._custom_models.values())
        if not task:
            return all_models
        target_task = task.strip().upper()
        return [m for m in all_models if m.get("task", "").upper() == target_task]

    def list_sentiment_models(self) -> List[Dict[str, Any]]:
        """Returns only validated sentiment models."""
        return self.list_presets(task="SENTIMENT")

    def get_preset(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Returns preset configuration by model_id if available."""
        return self.PRESETS.get(model_id) or self._custom_models.get(model_id)

    def register_custom(
        self,
        model_id: str,
        name: Optional[str] = None,
        task: str = "SENTIMENT",
        num_classes: int = 2,
        label_names: Optional[List[str]] = None,
        architecture: str = "CustomSequenceClassification",
        description: str = "",
    ) -> Dict[str, Any]:
        """Registers a custom model specification with explicit task."""
        labels = label_names or [f"CLASS_{i}" for i in range(num_classes)]
        entry = {
            "model_id": model_id,
            "name": name or model_id.split("/")[-1],
            "task": task.strip().upper(),
            "num_classes": num_classes,
            "label_names": labels,
            "architecture": architecture,
            "parameters_millions": None,
            "default": False,
            "description": description or f"Custom registered model {model_id} (task: {task})",
        }
        self._custom_models[model_id] = entry
        return entry

    def validate_model_for_sentiment(
        self, model_id_or_spec: Union[str, Dict[str, Any], ModelSpec]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Model Validation Gate (Section 3).
        Every model must pass registration validation gate before being available for an experiment.
        Required:
            - task == SENTIMENT
            - num_labels >= 2
            - id2label exists
            - label2id exists or can be derived
            - logits are available
            - probability distribution is available
            - predicted label is derived from model output
            - confidence is derived from probability
            - label semantics are documented

        Returns:
            (is_valid: bool, reason: str, details: Dict[str, Any])
        """
        if isinstance(model_id_or_spec, ModelSpec):
            spec_dict = model_id_or_spec.to_dict()
            model_id = model_id_or_spec.model_id
        elif isinstance(model_id_or_spec, dict):
            spec_dict = model_id_or_spec
            model_id = model_id_or_spec.get("model_id", "")
        else:
            model_id = str(model_id_or_spec)
            spec_dict = self.get_preset(model_id) or {}

        task = spec_dict.get("task", "").upper() if spec_dict else ""

        # Gate 1: Task Compatibility
        if task and task != "SENTIMENT":
            return (
                False,
                f"Model '{model_id}' has incompatible task '{task}'. Only task 'SENTIMENT' is permitted for sentiment experiments.",
                {"task": task, "expected_task": "SENTIMENT"},
            )

        # Gate 2: Known non-sentiment models
        if "openai-detector" in model_id.lower() or "ai-detector" in model_id.lower():
            return (
                False,
                f"Model '{model_id}' is an AI text detector, not a sentiment classifier. Rejected from sentiment experiments.",
                {"task": "AI_TEXT_DETECTION", "expected_task": "SENTIMENT"},
            )

        # Gate 3: Label check
        labels = spec_dict.get("label_names") or []
        upper_labels = [l.upper() for l in labels]
        if any(l in {"FAKE", "REAL"} for l in upper_labels):
            return (
                False,
                f"Model '{model_id}' outputs detection labels {labels} ('FAKE'/'REAL'). Cannot silently reinterpret as sentiment.",
                {"labels": labels},
            )

        # Gate 4: Inspect config
        try:
            from transformers import AutoConfig

            cfg = AutoConfig.from_pretrained(model_id)
            num_classes = getattr(cfg, "num_labels", len(labels) if labels else 2)
            if num_classes < 2:
                return False, f"Model has num_labels={num_classes} < 2.", {"num_classes": num_classes}

            id2label = getattr(cfg, "id2label", None)
            if not id2label and not labels:
                return False, "Neither id2label nor preset label_names exists.", {}

            raw_labels = list(id2label.values()) if id2label else labels
            raw_upper = [str(l).strip().upper() for l in raw_labels]

            # Reject if raw labels are non-sentiment
            if any(l in {"FAKE", "REAL"} for l in raw_upper):
                return (
                    False,
                    f"Model config contains non-sentiment labels: {raw_labels}. Rejected.",
                    {"id2label": id2label},
                )

            architecture = cfg.architectures[0] if getattr(cfg, "architectures", None) else "transformer"

            return (
                True,
                "Model passed sentiment registration validation gate.",
                {
                    "model_id": model_id,
                    "task": "SENTIMENT",
                    "num_classes": num_classes,
                    "architecture": architecture,
                    "id2label": id2label,
                    "labels": [normalize_label_name(l, num_classes) for l in raw_labels],
                },
            )

        except Exception as err:
            # If offline but preset exists and task is SENTIMENT
            if spec_dict and spec_dict.get("task") == "SENTIMENT":
                return (
                    True,
                    f"Verified against preset metadata (offline/cached): {spec_dict.get('description', '')}",
                    spec_dict,
                )
            return False, f"Model verification failed: {err}", {"error": str(err)}

    def verify_model(self, model_id: str) -> Dict[str, Any]:
        """
        Verifies model availability, task compatibility, and retrieves metadata.
        """
        preset = self.get_preset(model_id)
        is_valid, reason, details = self.validate_model_for_sentiment(model_id)

        if not is_valid and preset and preset.get("task") != "SENTIMENT":
            return {
                "model_id": model_id,
                "verified": False,
                "error": reason,
                "task": preset.get("task", "OTHER"),
                "num_classes": preset.get("num_classes", 2),
                "label_names": preset.get("label_names", []),
                "architecture": preset.get("architecture", "Unknown"),
                "description": preset.get("description", ""),
            }

        try:
            from transformers import AutoConfig

            config = AutoConfig.from_pretrained(model_id)
            num_classes = getattr(config, "num_labels", 2)
            id2label = getattr(config, "id2label", None)
            if id2label:
                label_names = [
                    normalize_label_name(id2label[i], num_classes)
                    for i in sorted(id2label.keys())
                ]
            else:
                label_names = preset.get("label_names", [f"CLASS_{i}" for i in range(num_classes)]) if preset else [f"CLASS_{i}" for i in range(num_classes)]

            architecture = config.architectures[0] if getattr(config, "architectures", None) else "transformer"

            return {
                "model_id": model_id,
                "verified": is_valid,
                "error": None if is_valid else reason,
                "task": preset.get("task", "SENTIMENT") if preset else "SENTIMENT",
                "num_classes": num_classes,
                "label_names": label_names,
                "architecture": architecture,
                "description": preset.get("description", "") if preset else f"Model {model_id}",
            }
        except Exception as e:
            if preset:
                return {
                    "model_id": model_id,
                    "verified": is_valid,
                    "error": None if is_valid else reason,
                    "task": preset.get("task", "SENTIMENT"),
                    "num_classes": preset["num_classes"],
                    "label_names": preset["label_names"],
                    "architecture": preset["architecture"],
                    "description": preset["description"],
                }
            return {
                "model_id": model_id,
                "verified": False,
                "error": str(e),
                "task": "UNKNOWN",
                "num_classes": 2,
                "label_names": ["NEGATIVE", "POSITIVE"],
                "architecture": "Unknown",
                "description": f"Verification failed: {e}",
            }

    def get_cache_overview(self) -> List[Dict[str, Any]]:
        """
        Returns combined metadata and cache telemetry for all presets.
        Provides disk footprint, snapshot presence, and RAM residency.
        """
        from blindspot.models.cache import ModelCache
        cache = ModelCache.get_shared_cache()
        presets = self.list_presets(task=None)
        status_list = cache.get_disk_cache_status([p["model_id"] for p in presets])
        status_by_id = {s["model_id"]: s for s in status_list}

        overview = []
        for p in presets:
            m_id = p["model_id"]
            st = status_by_id.get(m_id, {})
            merged = {
                **p,
                "cached_on_disk": st.get("cached_on_disk", False),
                "disk_size_mb": st.get("disk_size_mb", 0.0),
                "revision_hash": st.get("revision_hash"),
                "is_resident_in_ram": st.get("is_resident_in_ram", False),
                "disk_path": st.get("disk_path"),
            }
            overview.append(merged)
        return overview

