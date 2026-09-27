"""
Behavioral and Statistical Metrics for Text Classifier Auditing (Phase 13).
Includes Multiclass ECE, Directional Transitions, Behavioral Alignment,
and Capability-Aware Neutral Handling.
"""
from typing import List, Dict, Any, Optional, Union
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


def compute_observed_label_flip(original_label: str, probe_label: str) -> int:
    """
    Phase 13 Metric A: observed_label_flip
    1 if model output label changed between original and probe, 0 otherwise.
    """
    return 1 if str(original_label).strip() != str(probe_label).strip() else 0


def compute_expected_semantic_change(semantic_relation: Any) -> Optional[int]:
    """
    Phase 13 Metric B: expected_semantic_change
    1 if verified semantic relation indicates a polarity-affecting change.
    0 if relation indicates preservation.
    None (NA) if uncertain/not applicable.
    """
    rel = str(semantic_relation or "").strip().upper()
    if rel in ("REVERSE", "REVERSE_POLARITY", "INVERT", "SHIFT_FROM_NEUTRAL", "SHIFT_TO_NEUTRAL", "CONTRAST_SHIFT"):
        return 1
    elif rel in ("PRESERVE", "PRESERVE_POLARITY", "PRESERVE_MEANING", "SAME_LABEL"):
        return 0
    elif rel in ("UNCERTAIN", "OTHER", "UNKNOWN"):
        return None
    return None


def compute_behavioral_alignment(
    observed_label_flipped: bool,
    expected_change: Optional[int],
    is_unrepresentable_neutral: bool = False,
) -> Optional[int]:
    """
    Phase 13 Metric C: behavioral_alignment
    1 if observed behavior is consistent with verified semantic contract.
    0 if inconsistent.
    None (NA) if relation is uncertain or incompatible with model label space.
    """
    if is_unrepresentable_neutral:
        return None
    if expected_change is None:
        return None

    obs_flip = 1 if observed_label_flipped else 0
    return 1 if obs_flip == expected_change else 0


def classify_directional_transition(orig_label: str, probe_label: str) -> str:
    """
    Phase 13 Metric D: directional_transition
    Categorical transitions without inventing a numeric polarity ordering:
    NEG_TO_POS, POS_TO_NEG, POS_TO_NEU, NEU_TO_POS, NEG_TO_NEU, NEU_TO_NEG, SAME_LABEL.
    """
    def _norm(lbl: str) -> str:
        s = str(lbl or "").strip().upper()
        if "POS" in s:
            return "POS"
        if "NEG" in s:
            return "NEG"
        if "NEU" in s:
            return "NEU"
        return s

    src = _norm(orig_label)
    dst = _norm(probe_label)

    if src == dst:
        return "SAME_LABEL"
    elif src == "POS" and dst == "NEG":
        return "POS_TO_NEG"
    elif src == "NEG" and dst == "POS":
        return "NEG_TO_POS"
    elif src == "POS" and dst == "NEU":
        return "POS_TO_NEU"
    elif src == "NEU" and dst == "POS":
        return "NEU_TO_POS"
    elif src == "NEG" and dst == "NEU":
        return "NEG_TO_NEU"
    elif src == "NEU" and dst == "NEG":
        return "NEU_TO_NEG"
    else:
        return f"{src}_TO_{dst}"


def compute_confidence_delta_pp(orig_conf: float, probe_conf: float) -> float:
    """
    Phase 13 Metric E: confidence_delta_pp
    probe confidence - baseline confidence in percentage points.
    """
    return float(probe_conf - orig_conf) * 100.0


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
    Computes fraction of all executed probes where a prediction/polarity flip was observed.
    observed_flip_rate = observed_flips / total_applicable_probes
    """
    if not evaluations:
        return 0.0
    flips = 0
    for e in evaluations:
        if isinstance(e, dict):
            if e.get("polarity_flip", False) or e.get("is_prediction_flip", False) or e.get("is_flipped", False):
                flips += 1
        else:
            if getattr(e, "polarity_flip", False) or getattr(e, "is_prediction_flip", False) or getattr(e, "is_flipped", False):
                flips += 1
    return float(flips / len(evaluations))


def compute_expected_flip_rate(evaluations: List[Any]) -> float:
    """
    Computes fraction of applicable probes where a flip was expected under the verified semantic contract.
    """
    if not evaluations:
        return 0.0

    has_is_flipped = any((isinstance(e, dict) and "is_flipped" in e) or (not isinstance(e, dict) and hasattr(e, "is_flipped")) for e in evaluations)
    if has_is_flipped:
        return compute_expected_flip_compliance(evaluations)

    expected_count = 0
    for e in evaluations:
        val = e.get("expected_flip") if isinstance(e, dict) else getattr(e, "expected_flip", None)
        if val is None:
            rel = e.get("expected_relation") if isinstance(e, dict) else getattr(e, "expected_relation", "")
            val = rel in ("REVERSE", "REVERSE_POLARITY", "POLARITY_REVERSED")
        if bool(val):
            expected_count += 1
    return float(expected_count / len(evaluations))


def compute_expected_flip_compliance(evaluations: List[Any]) -> float:
    """
    Computes fraction of probes expecting a flip that actually flipped.
    expected_flip_compliance = observed_flips_where_expected / total_probes_expecting_flip
    """
    targets = []
    for e in evaluations:
        val = e.get("expected_flip") if isinstance(e, dict) else getattr(e, "expected_flip", None)
        if val is None:
            rel = e.get("expected_relation") if isinstance(e, dict) else getattr(e, "expected_relation", "")
            val = rel in ("REVERSE", "REVERSE_POLARITY", "POLARITY_REVERSED")
        if bool(val):
            targets.append(e)

    if not targets:
        return 0.0

    flips = 0
    for e in targets:
        if isinstance(e, dict):
            if e.get("polarity_flip", False) or e.get("is_prediction_flip", False) or e.get("is_flipped", False):
                flips += 1
        else:
            if getattr(e, "polarity_flip", False) or getattr(e, "is_prediction_flip", False) or getattr(e, "is_flipped", False):
                flips += 1
    return float(flips / len(targets))


def compute_preserve_rate(evaluations: List[Any]) -> float:
    """
    Computes fraction of probes expecting preservation that preserved their polarity/prediction.
    preserve_rate = observed_preserves_where_expected / total_probes_expecting_preservation
    """
    targets = []
    for e in evaluations:
        val = e.get("expected_flip") if isinstance(e, dict) else getattr(e, "expected_flip", None)
        if val is None:
            rel = e.get("expected_relation") if isinstance(e, dict) else getattr(e, "expected_relation", "")
            val = rel in ("REVERSE", "REVERSE_POLARITY", "POLARITY_REVERSED")
        if not bool(val):
            targets.append(e)

    if not targets:
        return 0.0

    preserves = 0
    for e in targets:
        is_flip = False
        if isinstance(e, dict):
            is_flip = e.get("polarity_flip", False) or e.get("is_prediction_flip", False) or e.get("is_flipped", False)
        else:
            is_flip = getattr(e, "polarity_flip", False) or getattr(e, "is_prediction_flip", False) or getattr(e, "is_flipped", False)
        if not is_flip:
            preserves += 1
    return float(preserves / len(targets))


def compute_behavioral_consistency(evaluations: List[Any]) -> float:
    """
    Computes fraction of applicable probes that satisfied their behavioral expectation:
    consistency = expectation_matches / total_applicable_probes
    """
    if not evaluations:
        return 1.0
    satisfied = 0
    applicable = 0
    for e in evaluations:
        # Exclude unrepresentable neutral
        if (isinstance(e, dict) and e.get("semantic_compatibility") == "NOT_DIRECTLY_REPRESENTABLE") or \
           (not isinstance(e, dict) and getattr(e, "semantic_compatibility", "") == "NOT_DIRECTLY_REPRESENTABLE"):
            continue
        applicable += 1
        match = False
        if isinstance(e, dict):
            match = e.get("expectation_match", e.get("expectation_satisfied", False))
        else:
            match = getattr(e, "expectation_match", getattr(e, "expectation_satisfied", False))
        if bool(match):
            satisfied += 1
    return float(satisfied / applicable) if applicable > 0 else 1.0


def compute_raw_label_flip_rate(evaluations: List[Any]) -> float:
    """
    Computes fraction of probes where raw model class label changed.
    raw_label_flip_rate = raw_label_flips / total_applicable_probes
    """
    if not evaluations:
        return 0.0
    flips = 0
    for e in evaluations:
        if isinstance(e, dict):
            if e.get("raw_label_flip", e.get("is_flipped", False)):
                flips += 1
        else:
            if getattr(e, "raw_label_flip", getattr(e, "is_flipped", False)):
                flips += 1
    return float(flips / len(evaluations))


def compute_polarity_flip_rate(evaluations: List[Any]) -> float:
    """
    Computes fraction of probes where canonical semantic polarity reversed.
    polarity_flip_rate = polarity_flips / total_applicable_probes
    """
    if not evaluations:
        return 0.0
    flips = 0
    for e in evaluations:
        if isinstance(e, dict):
            if e.get("polarity_flip", e.get("is_flipped", False)):
                flips += 1
        else:
            if getattr(e, "polarity_flip", getattr(e, "is_flipped", False)):
                flips += 1
    return float(flips / len(evaluations))


def compute_confidence_flip_rate(evaluations: List[Any], threshold_pts: float = 15.0) -> float:
    """
    Computes fraction of probes where confidence dropped by more than threshold_pts percentage points.
    """
    if not evaluations:
        return 0.0
    sensitive = 0
    for e in evaluations:
        delta_pts = getattr(e, "confidence_delta_pts", None)
        if delta_pts is None and isinstance(e, dict):
            delta_pts = e.get("confidence_delta_pts", e.get("confidence_delta_pp", None))
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
