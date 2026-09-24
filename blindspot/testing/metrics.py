"""
Behavioral and Statistical Metrics for Text Classifier Auditing.
Includes Multiclass ECE, Transition Matrices, Confidence Shifts, and Agreement Metrics.
"""
from typing import List, Dict, Any, Optional
import numpy as np


def compute_ece(
    confidences: np.ndarray,
    predictions: np.ndarray,
    labels: np.ndarray,
    n_bins: int = 10,
) -> float:
    """
    Computes Expected Calibration Error (ECE) for binary and multiclass models.
    confidences: max probability predicted for each sample in [0.0, 1.0]
    predictions: predicted class index or class string
    labels: ground truth / expected class index or class string
    """
    if len(confidences) == 0:
        return 0.0

    confidences = np.asarray(confidences, dtype=np.float64)
    predictions = np.asarray(predictions)
    labels = np.asarray(labels)

    # Convert to equal matches
    is_correct = (predictions == labels).astype(np.float64)

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    total_samples = len(confidences)

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]

        # Samples falling into the bin
        if i == 0:
            in_bin = (confidences >= bin_lower) & (confidences <= bin_upper)
        else:
            in_bin = (confidences > bin_lower) & (confidences <= bin_upper)

        bin_count = int(np.sum(in_bin))
        if bin_count > 0:
            accuracy_in_bin = float(np.mean(is_correct[in_bin]))
            avg_confidence_in_bin = float(np.mean(confidences[in_bin]))
            bin_weight = bin_count / total_samples
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * bin_weight

    return float(ece)


def compute_flip_rate(original_label: str, perturbed_labels: List[str]) -> float:
    """
    Computes fraction of perturbed instances that flip away from original prediction label.
    Backward-compatible helper.
    """
    if not perturbed_labels:
        return 0.0
    flips = sum(1 for label in perturbed_labels if label != original_label)
    return float(flips / len(perturbed_labels))


def compute_observed_flip_rate(evaluations: List[Any]) -> float:
    """
    Computes fraction of all executed probes where a prediction flip was observed.
    observed_flip_rate = flips / total_executed_probes
    """
    if not evaluations:
        return 0.0
    flips = sum(
        1 for e in evaluations
        if getattr(e, "is_flipped", False) or (isinstance(e, dict) and e.get("is_flipped", False))
    )
    return float(flips / len(evaluations))


def compute_expected_flip_rate(evaluations: List[Any]) -> float:
    """
    Computes fraction of probes where expected_flip is True that actually flipped.
    expected_flip_rate = flips_on_expected / count(expected_flip == True)
    """
    targets = [
        e for e in evaluations
        if (getattr(e, "expected_flip", False) if not isinstance(e, dict) else e.get("expected_flip", False))
    ]
    if not targets:
        return 0.0
    flips = sum(
        1 for e in targets
        if getattr(e, "is_flipped", False) or (isinstance(e, dict) and e.get("is_flipped", False))
    )
    return float(flips / len(targets))


def compute_preserve_rate(evaluations: List[Any]) -> float:
    """
    Computes fraction of probes where expected_flip is False that preserved their prediction label.
    preserve_rate = preserves_on_expected / count(expected_flip == False)
    """
    targets = [
        e for e in evaluations
        if not (getattr(e, "expected_flip", False) if not isinstance(e, dict) else e.get("expected_flip", False))
    ]
    if not targets:
        return 0.0
    preserves = sum(
        1 for e in targets
        if not (getattr(e, "is_flipped", False) or (isinstance(e, dict) and e.get("is_flipped", False)))
    )
    return float(preserves / len(targets))


def compute_behavioral_consistency(evaluations: List[Any]) -> float:
    """
    Computes fraction of all probes that satisfied their behavioral expectation:
    consistency = (expected_flips + expected_preserves) / total_evaluable_probes
    """
    if not evaluations:
        return 1.0
    satisfied = sum(
        1 for e in evaluations
        if (getattr(e, "expectation_satisfied", False) if not isinstance(e, dict) else e.get("expectation_satisfied", False))
    )
    return float(satisfied / len(evaluations))


def compute_confidence_flip_rate(evaluations: List[Any], threshold_pts: float = 20.0) -> float:
    """
    Computes fraction of probes where confidence dropped by more than threshold_pts percentage points.
    """
    if not evaluations:
        return 0.0
    sensitive = 0
    for e in evaluations:
        delta_pts = getattr(e, "confidence_delta_pts", None)
        if delta_pts is None and isinstance(e, dict):
            delta_pts = e.get("confidence_delta_pts", 0.0)
        if delta_pts is None:
            delta = getattr(e, "confidence_delta", 0.0) if not isinstance(e, dict) else e.get("confidence_delta", 0.0)
            delta_pts = delta * 100.0
        if delta_pts <= -abs(threshold_pts):
            sensitive += 1
    return float(sensitive / len(evaluations))



def compute_transition_matrix(
    original_labels: List[str],
    perturbed_labels: List[str],
    label_order: Optional[List[str]] = None,
) -> Dict[str, Dict[str, int]]:
    """
    Computes label transition matrix {from_label: {to_label: count}}.
    """
    all_labels = label_order or sorted(list(set(original_labels + perturbed_labels)))
    matrix = {src: {dst: 0 for dst in all_labels} for src in all_labels}

    for src, dst in zip(original_labels, perturbed_labels):
        if src in matrix and dst in matrix[src]:
            matrix[src][dst] += 1

    return matrix


def compute_confidence_shifts(
    original_confidences: List[float],
    perturbed_confidences: List[float],
) -> Dict[str, float]:
    """
    Computes signed confidence shifts in percentage points.
    E.g. delta_pts = (pert_conf - orig_conf) * 100.
    """
    if not original_confidences or not perturbed_confidences:
        return {
            "mean_delta_pts": 0.0,
            "median_delta_pts": 0.0,
            "max_drop_pts": 0.0,
            "max_gain_pts": 0.0,
        }

    deltas_pts = [
        (p - o) * 100.0
        for o, p in zip(original_confidences, perturbed_confidences)
    ]

    arr = np.array(deltas_pts, dtype=np.float64)
    drops = [d for d in deltas_pts if d < 0]
    gains = [d for d in deltas_pts if d > 0]
    unchanged = [d for d in deltas_pts if d == 0]

    return {
        "mean_delta_pts": float(np.mean(arr)),
        "median_delta_pts": float(np.median(arr)),
        "max_drop_pts": float(abs(min(drops))) if drops else 0.0,
        "max_gain_pts": float(max(gains)) if gains else 0.0,
        "num_increased": len(gains),
        "num_decreased": len(drops),
        "num_unchanged": len(unchanged),
    }


def compute_prediction_agreement(preds_a: List[str], preds_b: List[str]) -> float:
    """
    Computes fraction of samples where two models produce identical prediction labels.
    """
    if not preds_a or not preds_b or len(preds_a) != len(preds_b):
        return 0.0
    matches = sum(1 for a, b in zip(preds_a, preds_b) if a == b)
    return float(matches / len(preds_a))
