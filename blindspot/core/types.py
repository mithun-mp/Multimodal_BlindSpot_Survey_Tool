"""
Core Domain Types and Data Contracts for BlindSpot.
Unified, strongly-typed contracts for multimodel auditing, normalized inference,
shared probe protocols, explainability provenance, and failure diagnoses.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple, Iterator, Mapping
import time
import hashlib
import json


class FailureCategory(str, Enum):
    """
    Standardized 4-way Failure Taxonomy (Secondary Diagnostic Layer).
    Every diagnosis must be backed by traceable evidence.
    """
    BLIND = "Blind"
    SPURIOUS = "Spurious"
    MISWEIGHTED = "Misweighted"
    UNDETERMINED = "Undetermined"
    NONE = "None"


class BehavioralOutcome(str, Enum):
    """
    Primary Research-Centered Behavioral Outcome Classification.
    Evaluates whether the observed prediction transition matches the expected semantic effect.
    """
    EXPECTED_FLIP = "EXPECTED_FLIP"
    MISSING_FLIP = "MISSING_FLIP"
    UNEXPECTED_FLIP = "UNEXPECTED_FLIP"
    EXPECTED_PRESERVE = "EXPECTED_PRESERVE"
    UNEXPECTED_CHANGE = "UNEXPECTED_CHANGE"
    UNDETERMINED = "UNDETERMINED"


class ExpectedEffect(str, Enum):
    """Canonical behavioral expectations under perturbation."""
    EXPECTED_FLIP = "EXPECTED_FLIP"
    EXPECTED_PRESERVE = "EXPECTED_PRESERVE"
    EXPECTED_CONFIDENCE_INCREASE = "EXPECTED_CONFIDENCE_INCREASE"
    EXPECTED_CONFIDENCE_DECREASE = "EXPECTED_CONFIDENCE_DECREASE"
    EXPECTED_DIRECTIONAL_CHANGE = "EXPECTED_DIRECTIONAL_CHANGE"
    UNDETERMINED = "UNDETERMINED"


class ProbeStatus(str, Enum):
    """Lifecycle and verification status of a probe."""
    GENERATED = "GENERATED"
    VERIFIED = "VERIFIED"
    USER_EDITED = "USER_EDITED"
    CUSTOM = "CUSTOM"
    UNVERIFIED = "UNVERIFIED"


class SemanticIntent(str, Enum):
    """Explicit linguistic/semantic intention of a perturbation."""
    REVERSE_POLARITY = "REVERSE_POLARITY"
    PRESERVE_MEANING = "PRESERVE_MEANING"
    STRENGTHEN_POLARITY = "STRENGTHEN_POLARITY"
    WEAKEN_POLARITY = "WEAKEN_POLARITY"
    SHIFT_CONTRAST = "SHIFT_CONTRAST"
    REMOVE_NEGATION = "REMOVE_NEGATION"
    ADD_NEGATION = "ADD_NEGATION"
    CHANGE_SCOPE = "CHANGE_SCOPE"
    NEUTRAL_DRIFT = "NEUTRAL_DRIFT"
    OTHER = "OTHER"


class SentenceType(str, Enum):
    """Classification of seed sentence semantics/pragmatics."""
    LITERAL = "literal"
    PROVERB = "proverb"
    IDIOM = "idiom"
    FIGURATIVE = "figurative"
    SARCASTIC = "sarcastic"
    IRONIC = "ironic"
    UNKNOWN = "unknown"


class ExpectedLabelRelation(str, Enum):
    """Expected relationship between original and perturbed prediction labels."""
    SAME_LABEL = "SAME_LABEL"
    DIFFERENT_LABEL = "DIFFERENT_LABEL"
    SPECIFIED_LABEL = "SPECIFIED_LABEL"


class ExpectedConfidenceRelation(str, Enum):
    """Expected directional shift in prediction confidence."""
    INCREASE = "INCREASE"
    DECREASE = "DECREASE"
    PRESERVE = "PRESERVE"
    UNCONSTRAINED = "UNCONSTRAINED"


class PerturbationCategory(str, Enum):
    """Canonical high-level linguistic perturbation categories."""
    NEGATION = "negation"
    DOUBLE_NEGATION = "double_negation"
    CONNECTIVE = "connective"
    SYNONYM_SUBSTITUTION = "synonym_substitution"
    INTENSITY = "intensity"
    STRUCTURE = "structure"
    CONTRAST_POSITIVE = "contrast_positive"
    CUSTOM = "custom"


class RunStatus(str, Enum):
    """Canonical execution run statuses distinguishing failed/incomplete runs."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    INCOMPLETE = "INCOMPLETE"
    FAILED = "FAILED"


class AnalysisStatus(str, Enum):
    """
    Canonical behavioral analysis status per Section 10.
    Distinguishes genuine zero failures from failed or unexecuted runs.
    """
    NO_FAILURES_OBSERVED = "NO_FAILURES_OBSERVED"
    NO_VALID_ANALYSIS = "NO_VALID_ANALYSIS"
    RUN_FAILED = "RUN_FAILED"
    UNDETERMINED = "UNDETERMINED"


class ModelStatus(str, Enum):
    """Model-level execution state machine per Section 7."""
    QUEUED = "QUEUED"
    LOADING = "LOADING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class ModelExecutionTiming:
    """Detailed latency and runtime profiling for model lifecycle per Section 15."""
    model_id: str
    cache_lookup_ms: float = 0.0
    model_load_ms: float = 0.0
    tokenizer_load_ms: float = 0.0
    baseline_inference_ms: float = 0.0
    probe_inference_ms: float = 0.0
    total_inference_ms: float = 0.0
    analysis_ms: float = 0.0
    report_ms: float = 0.0
    persistence_ms: float = 0.0
    total_duration_sec: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "cache_lookup_ms": round(self.cache_lookup_ms, 2),
            "model_load_ms": round(self.model_load_ms, 2),
            "tokenizer_load_ms": round(self.tokenizer_load_ms, 2),
            "baseline_inference_ms": round(self.baseline_inference_ms, 2),
            "probe_inference_ms": round(self.probe_inference_ms, 2),
            "total_inference_ms": round(self.total_inference_ms, 2),
            "analysis_ms": round(self.analysis_ms, 2),
            "report_ms": round(self.report_ms, 2),
            "persistence_ms": round(self.persistence_ms, 2),
            "total_duration_sec": round(self.total_duration_sec, 3),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ModelExecutionTiming":
        return cls(
            model_id=d.get("model_id", ""),
            cache_lookup_ms=float(d.get("cache_lookup_ms", 0.0)),
            model_load_ms=float(d.get("model_load_ms", 0.0)),
            tokenizer_load_ms=float(d.get("tokenizer_load_ms", 0.0)),
            baseline_inference_ms=float(d.get("baseline_inference_ms", 0.0)),
            probe_inference_ms=float(d.get("probe_inference_ms", 0.0)),
            total_inference_ms=float(d.get("total_inference_ms", 0.0)),
            analysis_ms=float(d.get("analysis_ms", 0.0)),
            report_ms=float(d.get("report_ms", 0.0)),
            persistence_ms=float(d.get("persistence_ms", 0.0)),
            total_duration_sec=float(d.get("total_duration_sec", 0.0)),
        )


@dataclass
class ModelRunState:
    """Individual model execution state tracking per Section 7 & 10."""
    model_id: str
    status: ModelStatus = ModelStatus.QUEUED
    probes_done: int = 0
    total_probes: int = 0
    error: Optional[str] = None
    timing: Optional[ModelExecutionTiming] = None
    completed_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "status": self.status.value if isinstance(self.status, ModelStatus) else str(self.status),
            "probes_done": self.probes_done,
            "total_probes": self.total_probes,
            "error": self.error,
            "timing": self.timing.to_dict() if self.timing else None,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ModelRunState":
        st_val = d.get("status", "QUEUED")
        try:
            status_enum = ModelStatus(st_val)
        except Exception:
            status_enum = ModelStatus.QUEUED
        timing_data = d.get("timing")
        timing = ModelExecutionTiming.from_dict(timing_data) if timing_data else None
        return cls(
            model_id=d.get("model_id", ""),
            status=status_enum,
            probes_done=int(d.get("probes_done", 0)),
            total_probes=int(d.get("total_probes", 0)),
            error=d.get("error"),
            timing=timing,
            completed_at=d.get("completed_at"),
        )


@dataclass
class ModelPrediction:
    """
    [DEPRECATED] Legacy model prediction container.
    Superseded by PredictionResult. Maintained for backwards compatibility.
    """
    model_id: str
    predicted_label: str
    predicted_label_id: int
    confidence: float
    probabilities: Dict[str, float]
    raw_logits: List[float] = field(default_factory=list)
    raw_labels: List[str] = field(default_factory=list)
    label_mapping: Dict[str, str] = field(default_factory=dict)
    latency_ms: float = 0.0

    def to_prediction_result(self) -> "PredictionResult":
        return PredictionResult(
            label=self.predicted_label,
            confidence=self.confidence,
            probabilities=self.probabilities,
            raw_logits=self.raw_logits,
            latency_ms=self.latency_ms,
            model_id=self.model_id,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "predicted_label": self.predicted_label,
            "predicted_label_id": self.predicted_label_id,
            "confidence": self.confidence,
            "probabilities": self.probabilities,
            "raw_logits": self.raw_logits,
            "raw_labels": self.raw_labels,
            "label_mapping": self.label_mapping,
            "latency_ms": self.latency_ms,
            "deprecated": True,
        }



def is_prediction_flip(original_label: str, perturbed_label: str) -> bool:
    """
    Canonical definition of prediction flip:
    True iff perturbed label differs from original label.
    Does NOT assume binary classification.
    """
    if not original_label or not perturbed_label:
        return False
    return str(original_label).strip().upper() != str(perturbed_label).strip().upper()


def classify_behavioral_outcome(
    original_label: str,
    perturbed_label: str,
    expected_flip: bool,
    expected_semantic_effect: str = "invert",
) -> BehavioralOutcome:
    """
    Classifies the observed transition against the expected semantic effect into
    the canonical primary behavioral outcomes.
    """
    flipped = is_prediction_flip(original_label, perturbed_label)
    if expected_flip:
        if flipped:
            return BehavioralOutcome.EXPECTED_FLIP
        else:
            return BehavioralOutcome.MISSING_FLIP
    else:
        if not flipped:
            return BehavioralOutcome.EXPECTED_PRESERVE
        else:
            return BehavioralOutcome.UNEXPECTED_FLIP


@dataclass
class ModelMetadata:
    """Metadata describing an evaluated text classification model."""
    model_id: str
    architecture: str = "transformer"
    task: str = "text-classification"
    num_classes: int = 2
    label_names: List[str] = field(default_factory=lambda: ["NEGATIVE", "POSITIVE"])
    device: str = "cpu"
    max_seq_len: int = 512
    parameters_millions: Optional[float] = None
    verified: bool = False
    loaded: bool = False
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "architecture": self.architecture,
            "task": self.task,
            "num_classes": self.num_classes,
            "label_names": self.label_names,
            "device": self.device,
            "max_seq_len": self.max_seq_len,
            "parameters_millions": self.parameters_millions,
            "verified": self.verified,
            "loaded": self.loaded,
            "description": self.description,
        }


@dataclass
class PredictionResult:
    """
    Normalized prediction output for any model (binary or multiclass).
    Provides consistent confidence formatting (e.g. 98.73%).
    """
    label: str
    confidence: float  # [0.0, 1.0]
    probabilities: Dict[str, float] = field(default_factory=dict)
    raw_logits: Optional[List[float]] = None
    latency_ms: float = 0.0
    model_id: str = ""
    device: str = "cpu"
    model_status: str = "READY"

    @property
    def formatted_confidence(self) -> str:
        """Percentage format with exactly 2 decimal places."""
        return f"{self.confidence * 100:.2f}%"

    @property
    def formatted_probabilities(self) -> Dict[str, str]:
        """Dictionary of class probabilities formatted as percentages."""
        return {k: f"{v * 100:.2f}%" for k, v in self.probabilities.items()}

    @property
    def formatted_distribution_ascii(self) -> str:
        """
        Formats probability distribution with dense meters, e.g.:
        POSITIVE     [====================] 98.73%
        NEGATIVE     [                    ]  1.27%
        """
        lines = []
        max_label_len = max([len(str(k)) for k in self.probabilities.keys()] or [8])
        for cls_name, prob in self.probabilities.items():
            pct = prob * 100.0
            filled_chars = int(round(prob * 20))
            bar = "=" * filled_chars
            bar_padded = bar.ljust(20)
            lines.append(f"{cls_name.ljust(max_label_len + 2)} [{bar_padded}] {pct:6.2f}%")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "confidence": self.confidence,
            "formatted_confidence": self.formatted_confidence,
            "probabilities": self.probabilities,
            "formatted_probabilities": self.formatted_probabilities,
            "formatted_distribution_ascii": self.formatted_distribution_ascii,
            "raw_logits": self.raw_logits,
            "latency_ms": self.latency_ms,
            "model_id": self.model_id,
            "device": self.device,
            "model_status": self.model_status,
        }


@dataclass
class LinguisticProbe:
    """
    Controlled linguistic perturbation probe with stable identity, semantic intent,
    and expected behavioral effect.
    """
    probe_id: str
    seed_text: str
    perturbed_text: str
    perturbation_type: str  # negation, double_negation, connective, synonym_substitution, intensity, structure
    description: str
    expected_semantic_effect: str  # invert, preserve, weaken, strengthen, concession, refutation, neutral_drift
    expected_flip: bool
    subtype: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    name: str = ""
    semantic_intent: str = "REVERSE_POLARITY"
    status: str = "GENERATED"  # GENERATED, VERIFIED, USER_EDITED, CUSTOM
    transformation: str = ""
    version: int = 1
    expected_label_relation: str = "DIFFERENT_LABEL"  # DIFFERENT_LABEL, SAME_LABEL, SPECIFIED_LABEL
    expected_confidence_relation: str = "UNCONSTRAINED"  # INCREASE, DECREASE, PRESERVE, UNCONSTRAINED
    sentence_type: str = "literal"
    rationale: str = ""
    probe_set_id: str = ""

    @property
    def original_text(self) -> str:
        return self.seed_text

    @property
    def expected_effect(self) -> str:
        return self.expected_semantic_effect

    @property
    def category(self) -> str:
        return self.perturbation_type

    @classmethod
    def create(
        cls,
        seed_text: str,
        perturbed_text: str,
        perturbation_type: str,
        description: str = "",
        expected_semantic_effect: str = "preserve",
        expected_flip: bool = False,
        subtype: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        name: str = "",
        semantic_intent: str = "",
        status: str = "GENERATED",
        transformation: str = "",
        version: int = 1,
        category: Optional[str] = None,
        **kwargs,
    ) -> "LinguisticProbe":


        # Deterministic SHA-256 ID based on content
        raw = f"{seed_text}|{perturbed_text}|{perturbation_type}|{expected_semantic_effect}"
        probe_id = f"prb_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:12]}"
        
        if not semantic_intent:
            if expected_flip:
                semantic_intent = "REVERSE_POLARITY"
            elif expected_semantic_effect == "strengthen":
                semantic_intent = "STRENGTHEN_POLARITY"
            elif expected_semantic_effect == "weaken":
                semantic_intent = "WEAKEN_POLARITY"
            else:
                semantic_intent = "PRESERVE_MEANING"

        expected_label_rel = kwargs.get("expected_label_relation") or ("DIFFERENT_LABEL" if expected_flip else "SAME_LABEL")
        expected_conf_rel = kwargs.get("expected_confidence_relation")
        if not expected_conf_rel:
            if expected_semantic_effect == "strengthen":
                expected_conf_rel = "INCREASE"
            elif expected_semantic_effect == "weaken":
                expected_conf_rel = "DECREASE"
            elif expected_semantic_effect == "preserve":
                expected_conf_rel = "PRESERVE"
            else:
                expected_conf_rel = "UNCONSTRAINED"

        return cls(
            probe_id=probe_id,
            seed_text=seed_text,
            perturbed_text=perturbed_text,
            perturbation_type=perturbation_type,
            description=description,
            expected_semantic_effect=expected_semantic_effect,
            expected_flip=expected_flip,
            subtype=subtype,
            metadata=metadata or {},
            name=name or f"{perturbation_type.replace('_', ' ').title()} Probe",
            semantic_intent=semantic_intent,
            status=status,
            transformation=transformation or subtype or description,
            version=version,
            expected_label_relation=expected_label_rel,
            expected_confidence_relation=expected_conf_rel,
            sentence_type=kwargs.get("sentence_type", "literal"),
            rationale=kwargs.get("rationale") or description or f"Controlled {perturbation_type} perturbation.",
            probe_set_id=kwargs.get("probe_set_id", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "probe_id": self.probe_id,
            "seed_text": self.seed_text,
            "original_text": self.seed_text,
            "perturbed_text": self.perturbed_text,
            "perturbation_type": self.perturbation_type,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "expected_semantic_effect": self.expected_semantic_effect,
            "expected_effect": self.expected_semantic_effect,
            "expected_flip": self.expected_flip,
            "semantic_intent": self.semantic_intent,
            "status": self.status,
            "transformation": self.transformation,
            "subtype": self.subtype,
            "version": self.version,
            "metadata": self.metadata,
            "expected_label_relation": self.expected_label_relation,
            "expected_confidence_relation": self.expected_confidence_relation,
            "sentence_type": self.sentence_type,
            "rationale": self.rationale,
            "probe_set_id": self.probe_set_id,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "LinguisticProbe":
        seed = d.get("seed_text") or d.get("original_text", "")
        ptype = d.get("perturbation_type") or d.get("category", "unknown")
        effect = d.get("expected_semantic_effect") or d.get("expected_effect", "invert")
        flipped = bool(d.get("expected_flip", False))
        desc = d.get("description", "")
        rat = d.get("rationale") or desc or f"Controlled {ptype} perturbation."
        return cls(
            probe_id=d.get("probe_id", ""),
            seed_text=seed,
            perturbed_text=d.get("perturbed_text", ""),
            perturbation_type=ptype,
            description=desc,
            expected_semantic_effect=effect,
            expected_flip=flipped,
            subtype=d.get("subtype"),
            metadata=d.get("metadata", {}),
            name=d.get("name", ""),
            semantic_intent=d.get("semantic_intent", "PRESERVE_MEANING"),
            status=d.get("status", "GENERATED"),
            transformation=d.get("transformation", ""),
            version=int(d.get("version", 1)),
            expected_label_relation=d.get("expected_label_relation", "DIFFERENT_LABEL" if flipped else "SAME_LABEL"),
            expected_confidence_relation=d.get("expected_confidence_relation", "UNCONSTRAINED"),
            sentence_type=d.get("sentence_type", "literal"),
            rationale=rat,
            probe_set_id=d.get("probe_set_id", ""),
        )

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validates individual probe contract integrity per Section 13:
        - original_text != perturbed_text
        - probe_id exists
        - category exists
        - expected_effect exists
        - semantic_intent exists
        - text is non-empty
        - probe rationale exists
        - expected behavior is internally consistent
        """
        errors = []
        if not self.probe_id or not self.probe_id.strip():
            errors.append(f"Probe {self.probe_id or 'unknown'}: missing probe_id.")
        if not self.seed_text or not self.seed_text.strip():
            errors.append(f"Probe {self.probe_id}: Original text is missing or empty.")
        if not self.perturbed_text or not self.perturbed_text.strip():
            errors.append(f"Probe {self.probe_id}: Perturbed text is missing or empty.")
        if self.seed_text.strip().lower() == self.perturbed_text.strip().lower():
            errors.append(f"Probe {self.probe_id}: Perturbed text is identical to original seed text.")
        if not self.perturbation_type or not self.perturbation_type.strip():
            errors.append(f"Probe {self.probe_id}: Perturbation category is missing.")
        if not self.expected_semantic_effect or not self.expected_semantic_effect.strip():
            errors.append(f"Probe {self.probe_id}: Expected semantic effect is missing.")
        if not self.semantic_intent or not self.semantic_intent.strip():
            errors.append(f"Probe {self.probe_id}: Semantic intent is missing.")
        if not self.rationale or not self.rationale.strip():
            if not self.description:
                errors.append(f"Probe {self.probe_id}: Linguistic rationale is missing.")

        # Internal consistency check
        if self.semantic_intent == "PRESERVE_MEANING" and self.expected_label_relation == "DIFFERENT_LABEL":
            errors.append(f"Probe {self.probe_id}: Internal inconsistency: PRESERVE_MEANING cannot require DIFFERENT_LABEL.")
        if self.semantic_intent == "REVERSE_POLARITY" and self.expected_label_relation == "SAME_LABEL":
            errors.append(f"Probe {self.probe_id}: Internal inconsistency: REVERSE_POLARITY cannot require SAME_LABEL.")

        return len(errors) == 0, errors


@dataclass
class SharedProbeSet:
    """
    Collection of shared probes generated from seed sentences to evaluate across models.
    Ensures identical stimuli across heterogeneous models.
    """
    probe_set_id: str
    seed_texts: List[str]
    probes: List[LinguisticProbe]
    created_at: float = field(default_factory=time.time)
    probe_set_version: int = 1
    generator_version: str = "2.2.0"
    sentence_types: Dict[str, str] = field(default_factory=dict)

    def get_selected(self, probe_ids: Any) -> "SharedProbeSet":
        """Returns a new SharedProbeSet containing only probes matching the specified IDs."""
        id_set = set(probe_ids)
        selected_probes = [p for p in self.probes if p.probe_id in id_set]
        return SharedProbeSet(
            probe_set_id=f"{self.probe_set_id}_sel",
            seed_texts=self.seed_texts,
            probes=selected_probes,
            created_at=time.time(),
            probe_set_version=self.probe_set_version,
            generator_version=self.generator_version,
            sentence_types=dict(self.sentence_types),
        )

    def find_by_id(self, probe_id: str) -> Optional[LinguisticProbe]:
        for p in self.probes:
            if p.probe_id == probe_id:
                return p
        return None

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validates the probe set integrity before execution per Section 13.
        Invalid probes must BLOCK execution.
        Returns (is_valid, list_of_warnings_or_errors).
        """
        errors = []
        seen_ids = set()
        seen_pairs = set()

        for idx, p in enumerate(self.probes):
            is_valid, p_errors = p.validate()
            if not is_valid:
                errors.extend(p_errors)

            if p.probe_id:
                if p.probe_id in seen_ids:
                    errors.append(f"Duplicate probe_id detected: {p.probe_id}")
                seen_ids.add(p.probe_id)

            # Duplicate perturbation content detection
            pair = (p.seed_text.strip(), p.perturbed_text.strip())
            if pair in seen_pairs:
                errors.append(f"Duplicate perturbation content: '{p.perturbed_text}'")
            seen_pairs.add(pair)

        return len(errors) == 0, errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "probe_set_id": self.probe_set_id,
            "probe_set_version": self.probe_set_version,
            "generator_version": self.generator_version,
            "seed_texts": self.seed_texts,
            "sentence_types": self.sentence_types,
            "num_probes": len(self.probes),
            "probes": [p.to_dict() for p in self.probes],
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SharedProbeSet":
        probes_raw = d.get("probes", [])
        probes = [LinguisticProbe.from_dict(p) if isinstance(p, dict) else p for p in probes_raw]
        return cls(
            probe_set_id=d.get("probe_set_id", "pset_unknown"),
            seed_texts=d.get("seed_texts", []),
            probes=probes,
            created_at=d.get("created_at", time.time()),
            probe_set_version=int(d.get("probe_set_version", 1)),
            generator_version=d.get("generator_version", "2.2.0"),
            sentence_types=d.get("sentence_types", {}),
        )


@dataclass
class BaselineEvaluation:
    """Dedicated standalone evaluation record for the original seed sentence baseline."""
    model_id: str
    seed_text: str
    sentence_type: str
    prediction: PredictionResult
    latency_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "seed_text": self.seed_text,
            "sentence_type": self.sentence_type,
            "prediction": self.prediction.to_dict(),
            "latency_ms": self.latency_ms,
        }


@dataclass
class ModelProbeEvaluation:
    """Evaluation result for one model evaluated against one probe."""
    model_id: str
    probe_id: str
    seed_text: str
    perturbed_text: str
    perturbation_type: str
    expected_flip: bool
    expected_semantic_effect: str
    original_prediction: PredictionResult
    perturbed_prediction: PredictionResult
    is_flipped: bool
    confidence_delta: float  # signed in [-1.0, 1.0]
    confidence_delta_pts: float  # signed percentage points
    expectation_satisfied: bool
    behavioral_outcome: str = "EXPECTED_FLIP"
    semantic_intent: str = ""
    failure_type: str = "None"
    rationale: str = ""
    latency_ms: float = 0.0
    original_label: str = ""
    original_confidence: float = 0.0
    perturbed_label: str = ""
    perturbed_confidence: float = 0.0

    def __post_init__(self):
        # Ensure original_label and original_confidence are reliably initialized
        if not self.original_label and self.original_prediction:
            if hasattr(self.original_prediction, "label"):
                self.original_label = str(self.original_prediction.label)
                self.original_confidence = float(getattr(self.original_prediction, "confidence", 0.0))
            elif isinstance(self.original_prediction, dict):
                self.original_label = str(self.original_prediction.get("label", "Unknown"))
                self.original_confidence = float(self.original_prediction.get("confidence", 0.0))
        # Ensure perturbed_label and perturbed_confidence are reliably initialized
        if not self.perturbed_label and self.perturbed_prediction:
            if hasattr(self.perturbed_prediction, "label"):
                self.perturbed_label = str(self.perturbed_prediction.label)
                self.perturbed_confidence = float(getattr(self.perturbed_prediction, "confidence", 0.0))
            elif isinstance(self.perturbed_prediction, dict):
                self.perturbed_label = str(self.perturbed_prediction.get("label", "Unknown"))
                self.perturbed_confidence = float(self.perturbed_prediction.get("confidence", 0.0))

    def get(self, key: str, default: Any = None) -> Any:
        """Enables dict-like .get() access on ModelProbeEvaluation instances."""
        return getattr(self, key, default)

    def __getitem__(self, key: str) -> Any:
        """Enables dict-like indexing on ModelProbeEvaluation instances."""
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    @property
    def formatted_confidence_delta(self) -> str:
        sign = "+" if self.confidence_delta_pts > 0 else ""
        return f"{sign}{self.confidence_delta_pts:.2f} percentage points"



    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "probe_id": self.probe_id,
            "seed_text": self.seed_text,
            "perturbed_text": self.perturbed_text,
            "perturbation_type": self.perturbation_type,
            "category": self.perturbation_type,
            "expected_flip": self.expected_flip,
            "expected_semantic_effect": self.expected_semantic_effect,
            "original_prediction": self.original_prediction.to_dict(),
            "perturbed_prediction": self.perturbed_prediction.to_dict(),
            "original_label": self.original_label,
            "original_confidence": self.original_confidence,
            "perturbed_label": self.perturbed_label,
            "perturbed_confidence": self.perturbed_confidence,
            "is_flipped": self.is_flipped,
            "confidence_delta": self.confidence_delta,
            "confidence_delta_pts": self.confidence_delta_pts,
            "formatted_confidence_delta": self.formatted_confidence_delta,
            "expectation_satisfied": self.expectation_satisfied,
            "behavioral_outcome": self.behavioral_outcome,
            "failure_type": self.failure_type,
            "rationale": self.rationale,
            "semantic_intent": self.semantic_intent,
            "latency_ms": self.latency_ms,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ModelProbeEvaluation":
        orig_pred = d.get("original_prediction", {})
        if isinstance(orig_pred, dict):
            orig_pred = PredictionResult(
                label=orig_pred.get("label", ""),
                confidence=float(orig_pred.get("confidence", 0.0)),
                probabilities=orig_pred.get("probabilities", {}),
                latency_ms=float(orig_pred.get("latency_ms", 0.0)),
                model_id=orig_pred.get("model_id", ""),
            )
        pert_pred = d.get("perturbed_prediction", {})
        if isinstance(pert_pred, dict):
            pert_pred = PredictionResult(
                label=pert_pred.get("label", ""),
                confidence=float(pert_pred.get("confidence", 0.0)),
                probabilities=pert_pred.get("probabilities", {}),
                latency_ms=float(pert_pred.get("latency_ms", 0.0)),
                model_id=pert_pred.get("model_id", ""),
            )
        return cls(
            model_id=d.get("model_id", ""),
            probe_id=d.get("probe_id", ""),
            seed_text=d.get("seed_text", ""),
            perturbed_text=d.get("perturbed_text", ""),
            perturbation_type=d.get("perturbation_type", d.get("category", "")),
            expected_flip=bool(d.get("expected_flip", False)),
            expected_semantic_effect=d.get("expected_semantic_effect", ""),
            original_prediction=orig_pred,
            perturbed_prediction=pert_pred,
            is_flipped=bool(d.get("is_flipped", False)),
            confidence_delta=float(d.get("confidence_delta", 0.0)),
            confidence_delta_pts=float(d.get("confidence_delta_pts", 0.0)),
            expectation_satisfied=bool(d.get("expectation_satisfied", False)),
            behavioral_outcome=d.get("behavioral_outcome", "EXPECTED_FLIP"),
            semantic_intent=d.get("semantic_intent", ""),
            failure_type=d.get("failure_type", "None"),
            rationale=d.get("rationale", ""),
            latency_ms=float(d.get("latency_ms", 0.0)),
            original_label=d.get("original_label", ""),
            original_confidence=float(d.get("original_confidence", 0.0)),
            perturbed_label=d.get("perturbed_label", ""),
            perturbed_confidence=float(d.get("perturbed_confidence", 0.0)),
        )


@dataclass
class RunPlan:
    """
    Immutable execution specification consumed by Live Run per Section 32.
    Ensures identical stimulus set and strict integrity without regeneration.
    """
    experiment_id: str
    model_ids: List[str]
    probe_set_id: str
    probe_set_version: int
    selected_probe_ids: List[str]
    probe_versions: Dict[str, int]
    original_text: str
    created_at: float = field(default_factory=time.time)
    sentence_type: str = "literal"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "model_ids": self.model_ids,
            "probe_set_id": self.probe_set_id,
            "probe_set_version": self.probe_set_version,
            "selected_probe_ids": self.selected_probe_ids,
            "probe_versions": self.probe_versions,
            "original_text": self.original_text,
            "created_at": self.created_at,
            "sentence_type": self.sentence_type,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RunPlan":
        return cls(
            experiment_id=d.get("experiment_id", ""),
            model_ids=d.get("model_ids", []),
            probe_set_id=d.get("probe_set_id", ""),
            probe_set_version=int(d.get("probe_set_version", 1)),
            selected_probe_ids=d.get("selected_probe_ids", []),
            probe_versions=d.get("probe_versions", {}),
            original_text=d.get("original_text", ""),
            created_at=float(d.get("created_at", time.time())),
            sentence_type=d.get("sentence_type", "literal"),
            metadata=d.get("metadata", {}),
        )

    def validate_execution(self, executed_probe_ids: List[str]) -> Tuple[bool, str]:
        """
        Validates that all planned probes were executed exactly once without drops or unexpected probes.
        """
        selected_set = set(self.selected_probe_ids)
        executed_set = set(executed_probe_ids)
        if selected_set == executed_set:
            return True, f"All {len(selected_set)} planned probes executed successfully."
        missing = selected_set - executed_set
        unexpected = executed_set - selected_set
        err_parts = []
        if missing:
            err_parts.append(f"Missing {len(missing)} planned probe(s): {sorted(list(missing))[:5]}")
        if unexpected:
            err_parts.append(f"Unexpected {len(unexpected)} probe(s): {sorted(list(unexpected))[:5]}")
        return False, "; ".join(err_parts)


@dataclass
class BehavioralProbeResult:
    """
    Canonical probe evaluation and behavioral audit record per Section 18.
    Stores comprehensive baseline vs probe evidence, transitions, outcome, and failure taxonomy.
    """
    experiment_id: str
    run_id: str
    model_id: str
    probe_id: str
    probe_version: int
    original_text: str
    perturbed_text: str
    original_label: str
    probe_label: str
    original_confidence: float
    probe_confidence: float
    original_distribution: Dict[str, float]
    probe_distribution: Dict[str, float]
    label_transition: str
    is_prediction_flip: bool
    confidence_delta_pp: float
    expected_effect: str
    semantic_intent: str
    expected_label_relation: str
    expected_confidence_relation: str
    behavioral_outcome: str
    failure_type: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    timestamp: float = field(default_factory=time.time)
    category: str = ""
    transformation: str = ""
    latency_ms: float = 0.0

    @property
    def seed_text(self) -> str:
        return self.original_text

    @property
    def perturbed_label(self) -> str:
        return self.probe_label

    @property
    def is_flipped(self) -> bool:
        return self.is_prediction_flip

    @property
    def confidence_delta(self) -> float:
        return self.confidence_delta_pp / 100.0

    @property
    def confidence_delta_pts(self) -> float:
        return self.confidence_delta_pp

    @property
    def formatted_confidence_delta(self) -> str:
        sign = "+" if self.confidence_delta_pp > 0 else ""
        return f"{sign}{self.confidence_delta_pp:.2f} percentage points"

    @property
    def perturbation_type(self) -> str:
        return self.category

    @property
    def expected_flip(self) -> bool:
        return self.expected_label_relation == "DIFFERENT_LABEL" or self.expected_effect in ("invert", "EXPECTED_FLIP")

    @property
    def expected_semantic_effect(self) -> str:
        return self.expected_effect

    @property
    def expectation_satisfied(self) -> bool:
        return self.is_prediction_flip == self.expected_flip

    @property
    def original_prediction(self) -> PredictionResult:
        return PredictionResult(
            label=self.original_label,
            confidence=self.original_confidence,
            probabilities=self.original_distribution,
            model_id=self.model_id,
        )

    @property
    def perturbed_prediction(self) -> PredictionResult:
        return PredictionResult(
            label=self.probe_label,
            confidence=self.probe_confidence,
            probabilities=self.probe_distribution,
            model_id=self.model_id,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "run_id": self.run_id,
            "model_id": self.model_id,
            "probe_id": self.probe_id,
            "probe_version": self.probe_version,
            "original_text": self.original_text,
            "seed_text": self.original_text,
            "perturbed_text": self.perturbed_text,
            "original_label": self.original_label,
            "probe_label": self.probe_label,
            "perturbed_label": self.probe_label,
            "original_confidence": self.original_confidence,
            "probe_confidence": self.probe_confidence,
            "perturbed_confidence": self.probe_confidence,
            "original_distribution": self.original_distribution,
            "probe_distribution": self.probe_distribution,
            "label_transition": self.label_transition,
            "is_prediction_flip": self.is_prediction_flip,
            "is_flipped": self.is_prediction_flip,
            "confidence_delta_pp": self.confidence_delta_pp,
            "confidence_delta_pts": self.confidence_delta_pp,
            "confidence_delta": self.confidence_delta,
            "formatted_confidence_delta": self.formatted_confidence_delta,
            "expected_effect": self.expected_effect,
            "expected_semantic_effect": self.expected_effect,
            "expected_flip": self.expected_flip,
            "semantic_intent": self.semantic_intent,
            "expected_label_relation": self.expected_label_relation,
            "expected_confidence_relation": self.expected_confidence_relation,
            "behavioral_outcome": self.behavioral_outcome,
            "failure_type": self.failure_type,
            "evidence": self.evidence,
            "rationale": self.rationale,
            "timestamp": self.timestamp,
            "category": self.category,
            "perturbation_type": self.category,
            "transformation": self.transformation,
            "expectation_satisfied": self.expectation_satisfied,
            "latency_ms": self.latency_ms,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "BehavioralProbeResult":
        return cls(
            experiment_id=d.get("experiment_id", ""),
            run_id=d.get("run_id", ""),
            model_id=d.get("model_id", ""),
            probe_id=d.get("probe_id", ""),
            probe_version=int(d.get("probe_version", 1)),
            original_text=d.get("original_text") or d.get("seed_text", ""),
            perturbed_text=d.get("perturbed_text", ""),
            original_label=d.get("original_label", ""),
            probe_label=d.get("probe_label") or d.get("perturbed_label", ""),
            original_confidence=float(d.get("original_confidence", 0.0)),
            probe_confidence=float(d.get("probe_confidence") or d.get("perturbed_confidence", 0.0)),
            original_distribution=d.get("original_distribution", {}),
            probe_distribution=d.get("probe_distribution", {}),
            label_transition=d.get("label_transition", ""),
            is_prediction_flip=bool(d.get("is_prediction_flip", d.get("is_flipped", False))),
            confidence_delta_pp=float(d.get("confidence_delta_pp", d.get("confidence_delta_pts", 0.0))),
            expected_effect=d.get("expected_effect") or d.get("expected_semantic_effect", "EXPECTED_FLIP"),
            semantic_intent=d.get("semantic_intent", "REVERSE_POLARITY"),
            expected_label_relation=d.get("expected_label_relation", "DIFFERENT_LABEL"),
            expected_confidence_relation=d.get("expected_confidence_relation", "UNCONSTRAINED"),
            behavioral_outcome=d.get("behavioral_outcome", "EXPECTED_FLIP"),
            failure_type=d.get("failure_type", "None"),
            evidence=d.get("evidence", {}),
            rationale=d.get("rationale", ""),
            timestamp=float(d.get("timestamp", time.time())),
            category=d.get("category") or d.get("perturbation_type", ""),
            transformation=d.get("transformation", ""),
            latency_ms=float(d.get("latency_ms", 0.0)),
        )


class ExplanationResult(dict):
    """
    Model-specific explanation result with full provenance.
    Inherits from dict for complete backwards compatibility across all consumers.
    """
    def __init__(
        self,
        token_weights: Dict[str, float],
        token_attributions: Optional[List[Any]] = None,
        model_id: str = "",
        text: str = "",
        explainer_requested: str = "lime",
        explainer_used: str = "lime",
        fallback_used: bool = False,
        fallback_reason: Optional[str] = None,
        runtime_ms: float = 0.0,
        random_seed: int = 42,
    ):
        super().__init__(token_weights)
        self.token_weights = token_weights
        self.token_attributions = token_attributions or [
            {"token": k, "attribution": v, "position": i + 1}
            for i, (k, v) in enumerate(token_weights.items())
        ]
        self.model_id = model_id
        self.text = text
        self.explainer_requested = explainer_requested
        self.explainer_used = explainer_used
        self.fallback_used = fallback_used
        self.fallback_reason = fallback_reason
        self.runtime_ms = runtime_ms
        self.random_seed = random_seed

    def get_token_attributions(self) -> List[Any]:
        return self.token_attributions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "token_weights": self.token_weights,
            "token_attributions": self.token_attributions,
            "model_id": self.model_id,
            "text": self.text,
            "explainer_requested": self.explainer_requested,
            "explainer_used": self.explainer_used,
            "fallback_used": self.fallback_used,
            "fallback_reason": self.fallback_reason,
            "runtime_ms": self.runtime_ms,
            "random_seed": self.random_seed,
        }


@dataclass
class FailureDiagnosis:
    """
    Evidence-backed failure diagnosis adhering to the 4-way taxonomy.
    """
    failure_id: str
    model_id: str
    probe_id: str
    category: FailureCategory
    severity: str  # high, medium, low
    evidence: Dict[str, Any]
    traceable_narrative: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "failure_id": self.failure_id,
            "model_id": self.model_id,
            "probe_id": self.probe_id,
            "category": self.category.value,
            "severity": self.severity,
            "evidence": self.evidence,
            "traceable_narrative": self.traceable_narrative,
            "timestamp": self.timestamp,
        }
