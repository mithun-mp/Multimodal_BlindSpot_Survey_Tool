"""
Behavioral Fingerprinting for Audited Text Classifiers.
Constructs descriptive multi-dimensional profiles characterizing robustness, calibration, and failure tendencies.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any
import numpy as np

from blindspot.core.types import ModelProbeEvaluation, FailureCategory


@dataclass
class ModelBehavioralFingerprint:
    """
    Descriptive behavioral fingerprint summarizing a single model's responses to linguistic probes.
    Purely observational; does not compute normative ranks.
    """
    model_id: str
    total_probes: int
    flip_rate: float
    ece: float
    satisfaction_rate: float
    mean_confidence_shift_pts: float
    category_flip_rates: Dict[str, float] = field(default_factory=dict)
    failure_counts: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "total_probes": self.total_probes,
            "flip_rate": self.flip_rate,
            "ece": self.ece,
            "satisfaction_rate": self.satisfaction_rate,
            "mean_confidence_shift_pts": self.mean_confidence_shift_pts,
            "category_flip_rates": self.category_flip_rates,
            "failure_counts": self.failure_counts,
        }


def compute_model_fingerprint(
    model_id: str,
    evaluations: List[ModelProbeEvaluation],
    failures: List[Dict[str, Any]],
    ece: float = 0.0,
) -> ModelBehavioralFingerprint:
    """
    Computes behavioral fingerprint metrics from probe evaluations and failure records.
    """
    if not evaluations:
        return ModelBehavioralFingerprint(
            model_id=model_id,
            total_probes=0,
            flip_rate=0.0,
            ece=0.0,
            satisfaction_rate=1.0,
            mean_confidence_shift_pts=0.0,
            category_flip_rates={},
            failure_counts={c.value: 0 for c in FailureCategory},
        )

    total_probes = len(evaluations)
    flips = sum(1 for e in evaluations if (e.get("is_flipped", False) if isinstance(e, dict) else getattr(e, "is_flipped", False)))
    flip_rate = float(flips / total_probes)

    satisfactions = sum(1 for e in evaluations if (e.get("expectation_satisfied", False) if isinstance(e, dict) else getattr(e, "expectation_satisfied", False)))
    satisfaction_rate = float(satisfactions / total_probes)

    mean_shift = float(np.mean([
        float(e.get("confidence_delta_pts", 0.0) if isinstance(e, dict) else getattr(e, "confidence_delta_pts", 0.0))
        for e in evaluations
    ]))

    # Category-specific flip rates
    cat_probes: Dict[str, List[bool]] = {}
    for e in evaluations:
        ptype = str(e.get("perturbation_type", e.get("category", "")) if isinstance(e, dict) else getattr(e, "perturbation_type", ""))
        if ptype not in cat_probes:
            cat_probes[ptype] = []
        is_flip = bool(e.get("is_flipped", False) if isinstance(e, dict) else getattr(e, "is_flipped", False))
        cat_probes[ptype].append(is_flip)

    category_flip_rates = {
        cat: float(sum(flips_list) / len(flips_list))
        for cat, flips_list in cat_probes.items()
    }

    # Failure counts
    failure_counts = {c.value: 0 for c in FailureCategory}
    for f in failures:
        cat_val = f.get("category")
        if cat_val in failure_counts:
            failure_counts[cat_val] += 1
        elif isinstance(cat_val, FailureCategory):
            failure_counts[cat_val.value] += 1
        else:
            failure_counts[FailureCategory.UNDETERMINED.value] += 1

    return ModelBehavioralFingerprint(
        model_id=model_id,
        total_probes=total_probes,
        flip_rate=flip_rate,
        ece=ece,
        satisfaction_rate=satisfaction_rate,
        mean_confidence_shift_pts=mean_shift,
        category_flip_rates=category_flip_rates,
        failure_counts=failure_counts,
    )
