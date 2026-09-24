"""
Execution and Experiment Configuration for BlindSpot.
Defines resource profiles, performance modes, and experiment specifications.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class PerformanceMode(str, Enum):
    SAFE = "safe"
    BALANCED = "balanced"
    PERFORMANCE = "performance"
    CUSTOM = "custom"
    # Backward-compatible aliases:
    DEFAULT = "default"
    HIGH_THROUGHPUT = "high_throughput"
    LOW_MEMORY = "low_memory"
    FAST_DEBUG = "fast_debug"

    @classmethod
    def from_str(cls, value: str) -> "PerformanceMode":
        v = str(value).strip().lower()
        if v == "safe":
            return cls.SAFE
        if v == "low_memory":
            return cls.LOW_MEMORY
        if v == "performance":
            return cls.PERFORMANCE
        if v == "high_throughput":
            return cls.HIGH_THROUGHPUT
        if v == "custom":
            return cls.CUSTOM
        if v == "fast_debug":
            return cls.FAST_DEBUG
        if v == "balanced":
            return cls.BALANCED
        if v == "default":
            return cls.DEFAULT
        try:
            return cls(v)
        except ValueError:
            return cls.BALANCED


@dataclass
class ResourceConfig:
    """Hardware resource limits and execution tunings."""
    mode: PerformanceMode = PerformanceMode.DEFAULT
    max_workers: int = 2
    batch_size: int = 16
    model_cache_size: int = 5
    device: str = "cpu"
    memory_reserve_gb: float = 1.0
    explanation_sample_size: int = 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode.value,
            "max_workers": self.max_workers,
            "batch_size": self.batch_size,
            "model_cache_size": self.model_cache_size,
            "device": self.device,
            "memory_reserve_gb": self.memory_reserve_gb,
            "explanation_sample_size": self.explanation_sample_size,
        }


@dataclass
class ExperimentConfig:
    """Full configuration specification for an auditing experiment."""
    experiment_name: str = "Multimodel Audit"
    model_ids: List[str] = field(default_factory=lambda: ["distilbert-base-uncased-finetuned-sst-2-english"])
    seed_texts: List[str] = field(default_factory=lambda: ["The movie was great and the acting was top notch."])
    perturbation_types: List[str] = field(
        default_factory=lambda: ["negation", "double_negation", "connective", "synonym_substitution"]
    )
    explainer_type: str = "lime"  # lime, shap, both, none
    performance_mode: PerformanceMode = PerformanceMode.DEFAULT
    batch_size: Optional[int] = None
    random_seed: int = 42
    confidence_threshold: float = 0.65
    selected_probe_set: Optional[Any] = None
    sentence_types: Dict[str, str] = field(default_factory=dict)
    confidence_sensitivity_threshold_pts: float = 20.0
    output_dir: str = "runs"

    def __init__(
        self,
        experiment_name: str = "Multimodel Audit",
        model_ids: Optional[List[str]] = None,
        seed_texts: Optional[List[str]] = None,
        input_sentences: Optional[List[str]] = None,  # Backward-compatible alias
        perturbation_types: Optional[List[str]] = None,
        explainer_type: str = "lime",
        performance_mode: PerformanceMode = PerformanceMode.DEFAULT,
        batch_size: Optional[int] = None,
        random_seed: int = 42,
        confidence_threshold: float = 0.65,
        output_dir: str = "runs",
        selected_probe_set: Optional[Any] = None,
        selected_probe_ids: Optional[List[str]] = None,
        sentence_types: Optional[Dict[str, str]] = None,
        confidence_sensitivity_threshold_pts: float = 20.0,
    ):
        self.experiment_name = experiment_name
        self.model_ids = model_ids if model_ids is not None else ["distilbert-base-uncased-finetuned-sst-2-english"]
        if seed_texts is not None:
            self.seed_texts = seed_texts
        elif input_sentences is not None:
            self.seed_texts = input_sentences
        else:
            self.seed_texts = ["The movie was great and the acting was top notch."]
        self.perturbation_types = perturbation_types if perturbation_types is not None else [
            "negation", "double_negation", "connective", "synonym_substitution"
        ]
        self.explainer_type = explainer_type
        if isinstance(performance_mode, str):
            self.performance_mode = PerformanceMode.from_str(performance_mode)
        else:
            self.performance_mode = performance_mode
        self.batch_size = batch_size
        self.random_seed = random_seed
        self.confidence_threshold = confidence_threshold
        self.output_dir = output_dir
        self.selected_probe_set = selected_probe_set
        self.selected_probe_ids = selected_probe_ids or []
        self.sentence_types = sentence_types or {}
        self.confidence_sensitivity_threshold_pts = confidence_sensitivity_threshold_pts

    @property
    def input_sentences(self) -> List[str]:
        return self.seed_texts

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_name": self.experiment_name,
            "model_ids": self.model_ids,
            "seed_texts": self.seed_texts,
            "sentence_types": self.sentence_types,
            "perturbation_types": self.perturbation_types,
            "explainer_type": self.explainer_type,
            "performance_mode": self.performance_mode.value,
            "batch_size": self.batch_size,
            "random_seed": self.random_seed,
            "confidence_threshold": self.confidence_threshold,
            "confidence_sensitivity_threshold_pts": self.confidence_sensitivity_threshold_pts,
            "output_dir": self.output_dir,
            "has_selected_probes": self.selected_probe_set is not None,
            "selected_probe_ids": self.selected_probe_ids,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ExperimentConfig":
        perf_mode = d.get("performance_mode", "default")
        if isinstance(perf_mode, str):
            perf_mode = PerformanceMode.from_str(perf_mode)
        return cls(
            experiment_name=d.get("experiment_name", "Multimodel Audit"),
            model_ids=d.get("model_ids"),
            seed_texts=d.get("seed_texts") or d.get("input_sentences"),
            perturbation_types=d.get("perturbation_types"),
            explainer_type=d.get("explainer_type", "lime"),
            performance_mode=perf_mode,
            batch_size=d.get("batch_size"),
            random_seed=int(d.get("random_seed", 42)),
            confidence_threshold=float(d.get("confidence_threshold", 0.65)),
            output_dir=d.get("output_dir", "runs"),
            selected_probe_ids=d.get("selected_probe_ids"),
            sentence_types=d.get("sentence_types"),
            confidence_sensitivity_threshold_pts=float(d.get("confidence_sensitivity_threshold_pts", 20.0)),
        )



