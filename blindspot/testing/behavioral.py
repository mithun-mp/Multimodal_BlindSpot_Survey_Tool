"""
Behavioral Testing Engine for Text Classifiers.
Evaluates single models and shared probe sets with expectation checks, transition tracking,
and deterministic failure diagnosis adhering to the 4-way behavioral failure taxonomy.
"""
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import time
import uuid

from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.core.types import (
    SharedProbeSet,
    LinguisticProbe,
    PredictionResult,
    ModelProbeEvaluation,
    BaselineEvaluation,
    SentenceType,
    FailureCategory,
    BehavioralOutcome,
    ExpectedEffect,
    ExpectedLabelRelation,
    ExpectedConfidenceRelation,
    BehavioralProbeResult,
    is_prediction_flip,
)
from .metrics import (
    compute_flip_rate,
    compute_observed_flip_rate,
    compute_expected_flip_rate,
    compute_preserve_rate,
    compute_behavioral_consistency,
    compute_confidence_flip_rate,
    compute_ece,
    compute_transition_matrix,
    compute_confidence_shifts,
)


def classify_behavior(
    original_label: Optional[str],
    probe_label: Optional[str],
    original_confidence: Optional[float],
    probe_confidence: Optional[float],
    expected_effect: str = "EXPECTED_FLIP",
    semantic_intent: str = "REVERSE_POLARITY",
    expected_label_relation: Optional[str] = None,
    expected_confidence_relation: str = "UNCONSTRAINED",
    original_distribution: Optional[Dict[str, float]] = None,
    probe_distribution: Optional[Dict[str, float]] = None,
    probe_metadata: Optional[Dict[str, Any]] = None,
    confidence_delta_threshold_pp: float = 15.0,
) -> Tuple[BehavioralOutcome, FailureCategory, Dict[str, Any], str]:
    """
    Pure deterministic classifier for behavioral auditing per Section 19.
    Evaluates expected vs observed predictions, multiclass transitions, and confidence movements.
    Classifies into Primary Behavioral Outcome and Secondary Failure Taxonomy.
    Does NOT depend on model names, UI state, or Streamlit.

    Returns:
        (behavioral_outcome, failure_type, evidence_dict, rationale_str)
    """
    # 1. Validation & Undetermined Check (Case 8)
    if (
        original_label is None
        or probe_label is None
        or str(original_label).strip() == ""
        or str(probe_label).strip() == ""
    ):
        evidence = {
            "error": "missing_prediction_labels",
            "original_label": original_label,
            "probe_label": probe_label,
        }
        return (
            BehavioralOutcome.UNDETERMINED,
            FailureCategory.UNDETERMINED,
            evidence,
            "Missing model prediction output labels.",
        )

    if original_confidence is None or probe_confidence is None:
        evidence = {
            "error": "missing_confidence_values",
            "original_confidence": original_confidence,
            "probe_confidence": probe_confidence,
        }
        return (
            BehavioralOutcome.UNDETERMINED,
            FailureCategory.UNDETERMINED,
            evidence,
            "Missing model prediction confidence values.",
        )

    orig_lbl = str(original_label).strip().upper()
    prb_lbl = str(probe_label).strip().upper()
    orig_conf = float(original_confidence)
    prb_conf = float(probe_confidence)

    # 2. Pure Prediction Flip Definition (works for binary and multiclass)
    flipped = is_prediction_flip(orig_lbl, prb_lbl)
    confidence_delta_pp = (prb_conf - orig_conf) * 100.0
    transition_str = f"{orig_lbl} → {prb_lbl}"

    norm_effect = str(expected_effect or "").strip().upper()
    norm_intent = str(semantic_intent or "").strip().upper()
    
    if expected_label_relation is not None and str(expected_label_relation).strip():
        norm_label_rel = str(expected_label_relation).strip().upper()
    else:
        # Deduce from intent/effect
        if norm_intent in ("PRESERVE_MEANING", "STRENGTHEN_POLARITY", "WEAKEN_POLARITY") or norm_effect in ("PRESERVE", "EXPECTED_PRESERVE", "STRENGTHEN", "WEAKEN"):
            norm_label_rel = "SAME_LABEL"
        elif norm_intent in ("REVERSE_POLARITY", "ADD_NEGATION", "REMOVE_NEGATION", "SHIFT_CONTRAST") or norm_effect in ("INVERT", "EXPECTED_FLIP", "CONCESSION"):
            norm_label_rel = "DIFFERENT_LABEL"
        else:
            norm_label_rel = ""
    norm_conf_rel = str(expected_confidence_relation or "").strip().upper()

    evidence: Dict[str, Any] = {
        "original_label": orig_lbl,
        "probe_label": prb_lbl,
        "original_confidence": orig_conf,
        "probe_confidence": prb_conf,
        "confidence_delta_pp": confidence_delta_pp,
        "label_transition": transition_str,
        "is_prediction_flip": flipped,
        "expected_effect": norm_effect,
        "semantic_intent": norm_intent,
        "expected_label_relation": norm_label_rel,
        "expected_confidence_relation": norm_conf_rel,
        "threshold_pp": confidence_delta_threshold_pp,
    }

    if norm_effect in ("UNDETERMINED", "UNKNOWN") and not norm_label_rel:
        return (
            BehavioralOutcome.UNDETERMINED,
            FailureCategory.UNDETERMINED,
            evidence,
            "Undetermined probe contract expectation.",
        )

    # 3. Determine if a prediction flip is expected under the probe contract
    is_expected_flip = (
        norm_label_rel == "DIFFERENT_LABEL"
        or norm_effect in ("EXPECTED_FLIP", "INVERT", "CONCESSION")
        or norm_intent in ("REVERSE_POLARITY", "ADD_NEGATION", "REMOVE_NEGATION", "SHIFT_CONTRAST")
    )

    # 4. Behavioral Outcome Classification (Empirical Observation)
    if is_expected_flip:
        if flipped:
            outcome = BehavioralOutcome.EXPECTED_FLIP
        else:
            outcome = BehavioralOutcome.MISSING_FLIP
    else:
        if not flipped:
            outcome = BehavioralOutcome.EXPECTED_PRESERVE
        else:
            outcome = BehavioralOutcome.UNEXPECTED_FLIP

    # 5. Secondary Failure Taxonomy Classification (Diagnostic Interpretation)
    # Case 1 & Case 5: Correct Expected Flip / Multiclass Flip
    if is_expected_flip and flipped:
        rationale = f"Model correctly flipped prediction from {transition_str} under {norm_intent or 'expected change'}."
        return outcome, FailureCategory.NONE, evidence, rationale

    # Case 2: Missing Flip -> BLIND
    if is_expected_flip and not flipped:
        rationale = (
            f"The verified probe introduces a polarity-altering change ({norm_intent or 'REVERSE_POLARITY'}), "
            f"but the model retained the same predicted class ({transition_str})."
        )
        return outcome, FailureCategory.BLIND, evidence, rationale

    # Case 3 & Case 7: Expected Preserve (Label did not change)
    if not is_expected_flip and not flipped:
        # Check for MISWEIGHTED on degree strengthening or downtoning
        if norm_intent == "STRENGTHEN_POLARITY" or norm_conf_rel == "INCREASE":
            if confidence_delta_pp < -confidence_delta_threshold_pp:
                rationale = (
                    f"Expected polarity strengthening, but model prediction confidence dropped by "
                    f"{abs(confidence_delta_pp):.2f} percentage points ({orig_conf:.2f} → {prb_conf:.2f})."
                )
                return outcome, FailureCategory.MISWEIGHTED, evidence, rationale
        elif norm_intent == "WEAKEN_POLARITY" or norm_conf_rel == "DECREASE":
            if confidence_delta_pp > confidence_delta_threshold_pp:
                rationale = (
                    f"Expected polarity weakening/downtoning, but model prediction confidence increased by "
                    f"{confidence_delta_pp:.2f} percentage points ({orig_conf:.2f} → {prb_conf:.2f})."
                )
                return outcome, FailureCategory.MISWEIGHTED, evidence, rationale

        rationale = f"Model correctly preserved prediction class ({transition_str}) under meaning-preserving perturbation."
        return outcome, FailureCategory.NONE, evidence, rationale

    # Case 4 & Case 7: Unexpected Flip on Meaning-Preserving Probe
    if not is_expected_flip and flipped:
        if norm_intent in ("STRENGTHEN_POLARITY", "WEAKEN_POLARITY"):
            rationale = (
                f"Model inverted prediction ({transition_str}) when presented with a degree modifier ({norm_intent}), "
                f"indicating disproportionately skewed feature weighting."
            )
            return outcome, FailureCategory.MISWEIGHTED, evidence, rationale
        else:
            rationale = (
                f"The verified perturbation is meaning-preserving ({norm_intent or 'PRESERVE_MEANING'}), "
                f"but the model unexpectedly changed its predicted class ({transition_str})."
            )
            return outcome, FailureCategory.SPURIOUS, evidence, rationale

    return outcome, FailureCategory.UNDETERMINED, evidence, "Indeterminate behavioral transition."


def classify_behavioral_outcome(
    original_label: str,
    perturbed_label: str,
    expected_flip: bool,
    expected_semantic_effect: str = "invert",
) -> BehavioralOutcome:
    """Backward-compatible helper mapping transition to BehavioralOutcome."""
    outcome, _, _, _ = classify_behavior(
        original_label=original_label,
        probe_label=perturbed_label,
        original_confidence=1.0,
        probe_confidence=1.0,
        expected_effect="EXPECTED_FLIP" if expected_flip else "EXPECTED_PRESERVE",
    )
    return outcome


class BehavioralTester:
    """
    Evaluates target black-box classifier on original vs perturbed input variants.
    Supports single-sentence backward compatibility and batched SharedProbeSet audits.
    """
    def __init__(self, model_wrapper: HuggingFaceWrapper):
        self.model = model_wrapper

    def evaluate_probe(self, original_text: str, perturbed_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Runs inference on original text and all perturbed variants.
        Backward-compatible method for single model audits.
        """
        orig_res = self.model.predict_result(original_text)
        orig_label = orig_res.label
        orig_conf = orig_res.confidence
        orig_probas = [orig_res.probabilities.get(lbl, 0.0) for lbl in self.model.labels]

        probe_results = []
        perturbed_labels = []
        confidences = []
        pred_indices = []
        expected_indices = []

        pert_texts = [item["perturbed"] for item in perturbed_items]
        pert_results = self.model.predict_results_batch(pert_texts) if pert_texts else []

        for item, pert_res in zip(perturbed_items, pert_results):
            pert_text = item["perturbed"]
            pert_label = pert_res.label
            pert_conf = pert_res.confidence
            pert_probas = [pert_res.probabilities.get(lbl, 0.0) for lbl in self.model.labels]

            is_flipped = (pert_label != orig_label)
            conf_delta = pert_conf - orig_conf
            conf_delta_pts = conf_delta * 100.0

            p_type = item.get("type", "unknown")
            raw_expected = item.get("expected_flip")
            if raw_expected is not None:
                expected_flip = bool(raw_expected)
            elif "negation" in p_type and "double" not in p_type:
                expected_flip = True
            elif "contrast_negative" in p_type or "concession" in p_type:
                expected_flip = True
            else:
                expected_flip = False

            unexpected_behavior = (is_flipped != expected_flip)

            res_entry = {
                "original": original_text,
                "perturbed": pert_text,
                "type": p_type,
                "description": item.get("description", ""),
                "original_label": orig_label,
                "original_confidence": orig_conf,
                "perturbed_label": pert_label,
                "perturbed_confidence": pert_conf,
                "is_flipped": is_flipped,
                "expected_flip": expected_flip,
                "unexpected_behavior": unexpected_behavior,
                "confidence_delta": conf_delta,
                "confidence_delta_pts": conf_delta_pts,
                "original_probas": orig_probas,
                "perturbed_probas": pert_probas,
            }
            probe_results.append(res_entry)
            perturbed_labels.append(pert_label)
            confidences.append(pert_conf)

            pred_idx = self.model.labels.index(pert_label) if pert_label in self.model.labels else 0
            pred_indices.append(pred_idx)

            expectation_satisfied = (is_flipped == expected_flip)
            if expectation_satisfied:
                exp_idx = pred_idx
            else:
                exp_idx = (pred_idx + 1) % max(2, len(self.model.labels))
            expected_indices.append(exp_idx)

        flip_rate = compute_flip_rate(orig_label, perturbed_labels)
        ece = compute_ece(np.array(confidences), np.array(pred_indices), np.array(expected_indices))

        return {
            "original_sentence": original_text,
            "original_prediction": orig_label,
            "original_confidence": orig_conf,
            "total_perturbations": len(perturbed_items),
            "flip_rate": flip_rate,
            "ece": ece,
            "probe_details": probe_results,
        }

    def evaluate_shared_probes(self, probe_set: SharedProbeSet) -> Dict[str, Any]:
        """
        Evaluates the model against a SharedProbeSet using batched execution.
        Returns detailed probe evaluations, baseline evaluations, canonical BehavioralProbeResults,
        failure taxonomy diagnoses, and stratified research metrics.
        """
        evaluations: List[ModelProbeEvaluation] = []
        canonical_probe_results: List[BehavioralProbeResult] = []
        failures: List[Dict[str, Any]] = []
        seed_predictions: Dict[str, PredictionResult] = {}
        baselines: Dict[str, BaselineEvaluation] = {}

        # 1. Evaluate baseline exactly once per unique seed sentence
        for seed in probe_set.seed_texts:
            pred = self.model.predict_result(seed)
            seed_predictions[seed] = pred
            stype = probe_set.sentence_types.get(seed, SentenceType.LITERAL.value)
            baselines[seed] = BaselineEvaluation(
                model_id=self.model.model_name,
                seed_text=seed,
                sentence_type=stype,
                prediction=pred,
                latency_ms=pred.latency_ms,
            )

        # 2. Batch predict all perturbed probe texts
        pert_texts = [p.perturbed_text for p in probe_set.probes]
        batch_results = self.model.predict_results_batch(pert_texts, batch_size=16)

        orig_labels = []
        pert_labels = []
        orig_confs = []
        pert_confs = []
        confidences = []
        pred_indices = []
        expected_indices = []

        for probe, pert_pred in zip(probe_set.probes, batch_results):
            orig_pred = seed_predictions.get(probe.seed_text)
            if not orig_pred:
                orig_pred = self.model.predict_result(probe.seed_text)
                seed_predictions[probe.seed_text] = orig_pred

            is_flipped = is_prediction_flip(orig_pred.label, pert_pred.label)
            delta = pert_pred.confidence - orig_pred.confidence
            delta_pts = delta * 100.0

            # Pure deterministic classification
            outcome, failure_type, evidence, rationale = classify_behavior(
                original_label=orig_pred.label,
                probe_label=pert_pred.label,
                original_confidence=orig_pred.confidence,
                probe_confidence=pert_pred.confidence,
                expected_effect=probe.expected_semantic_effect,
                semantic_intent=getattr(probe, "semantic_intent", ""),
                expected_label_relation=getattr(
                    probe, "expected_label_relation", "DIFFERENT_LABEL" if probe.expected_flip else "SAME_LABEL"
                ),
                expected_confidence_relation=getattr(probe, "expected_confidence_relation", "UNCONSTRAINED"),
                original_distribution=orig_pred.probabilities,
                probe_distribution=pert_pred.probabilities,
                probe_metadata=probe.metadata,
            )

            expectation_satisfied = (is_flipped == probe.expected_flip)

            # Build backward-compatible ModelProbeEvaluation
            eval_item = ModelProbeEvaluation(
                model_id=self.model.model_name,
                probe_id=probe.probe_id,
                seed_text=probe.seed_text,
                perturbed_text=probe.perturbed_text,
                perturbation_type=probe.perturbation_type,
                expected_flip=probe.expected_flip,
                expected_semantic_effect=probe.expected_semantic_effect,
                original_prediction=orig_pred,
                perturbed_prediction=pert_pred,
                is_flipped=is_flipped,
                confidence_delta=delta,
                confidence_delta_pts=delta_pts,
                expectation_satisfied=expectation_satisfied,
                behavioral_outcome=outcome.value,
                failure_type=failure_type.value,
                rationale=rationale,
                semantic_intent=getattr(probe, "semantic_intent", ""),
                latency_ms=pert_pred.latency_ms,
            )
            evaluations.append(eval_item)

            # Build canonical BehavioralProbeResult per Section 18
            canon_res = BehavioralProbeResult(
                experiment_id="",
                run_id="",
                model_id=self.model.model_name,
                probe_id=probe.probe_id,
                probe_version=getattr(probe, "version", 1),
                original_text=probe.seed_text,
                perturbed_text=probe.perturbed_text,
                original_label=orig_pred.label,
                probe_label=pert_pred.label,
                original_confidence=orig_pred.confidence,
                probe_confidence=pert_pred.confidence,
                original_distribution=orig_pred.probabilities,
                probe_distribution=pert_pred.probabilities,
                label_transition=f"{orig_pred.label} → {pert_pred.label}",
                is_prediction_flip=is_flipped,
                confidence_delta_pp=delta_pts,
                expected_effect=probe.expected_semantic_effect,
                semantic_intent=getattr(probe, "semantic_intent", ""),
                expected_label_relation=getattr(
                    probe, "expected_label_relation", "DIFFERENT_LABEL" if probe.expected_flip else "SAME_LABEL"
                ),
                expected_confidence_relation=getattr(probe, "expected_confidence_relation", "UNCONSTRAINED"),
                behavioral_outcome=outcome.value,
                failure_type=failure_type.value,
                evidence=evidence,
                rationale=rationale,
                category=probe.perturbation_type,
                transformation=probe.transformation,
                latency_ms=pert_pred.latency_ms,
            )
            canonical_probe_results.append(canon_res)

            # If diagnosed as a behavioral failure, record failure diagnosis
            if failure_type not in (FailureCategory.NONE, "None", "NONE"):
                severity = "high" if failure_type in (FailureCategory.BLIND, FailureCategory.SPURIOUS) else "medium"
                fail_item = {
                    "failure_id": f"fail_{uuid.uuid4().hex[:8]}",
                    "model_id": self.model.model_name,
                    "probe_id": probe.probe_id,
                    "category": failure_type.value,
                    "severity": severity,
                    "reason": rationale,
                    "details": evidence.get("description", rationale) if isinstance(evidence, dict) else str(evidence or rationale),
                    "recommendation": f"Augment training data and regularize behavior against {probe.perturbation_type} perturbations to fix {failure_type.value} failures.",
                    "evidence": evidence,
                    "traceable_narrative": rationale,
                    "original_sentence": probe.seed_text,
                    "perturbed_sentence": probe.perturbed_text,
                    "original_label": orig_pred.label,
                    "perturbed_label": pert_pred.label,
                    "original_confidence": orig_pred.confidence,
                    "perturbed_confidence": pert_pred.confidence,
                    "confidence_delta_pts": delta_pts,
                    "is_flipped": is_flipped,
                    "expected_flip": probe.expected_flip,
                    "behavioral_outcome": outcome.value,
                }
                failures.append(fail_item)

            orig_labels.append(orig_pred.label)
            pert_labels.append(pert_pred.label)
            orig_confs.append(orig_pred.confidence)
            pert_confs.append(pert_pred.confidence)
            confidences.append(pert_pred.confidence)

            # ECE indices
            p_idx = self.model.labels.index(pert_pred.label) if pert_pred.label in self.model.labels else 0
            pred_indices.append(p_idx)
            if expectation_satisfied:
                exp_idx = p_idx
            else:
                exp_idx = (p_idx + 1) % max(2, len(self.model.labels))
            expected_indices.append(exp_idx)

        total_probes = len(evaluations)
        observed_flip_rate = compute_observed_flip_rate(evaluations)
        expected_flip_rate = compute_expected_flip_rate(evaluations)
        preserve_rate = compute_preserve_rate(evaluations)
        behavioral_consistency = compute_behavioral_consistency(evaluations)
        confidence_flip_rate = compute_confidence_flip_rate(evaluations)

        ece = compute_ece(np.array(confidences), np.array(pred_indices), np.array(expected_indices))
        transition_matrix = compute_transition_matrix(orig_labels, pert_labels, self.model.labels)
        confidence_shifts = compute_confidence_shifts(orig_confs, pert_confs)

        failure_counts = {
            "Blind": sum(1 for f in failures if f.get("category") == "Blind"),
            "Spurious": sum(1 for f in failures if f.get("category") == "Spurious"),
            "Misweighted": sum(1 for f in failures if f.get("category") == "Misweighted"),
            "Undetermined": sum(1 for f in failures if f.get("category") == "Undetermined"),
        }

        return {
            "model_id": self.model.model_name,
            "baselines": {k: v.to_dict() for k, v in baselines.items()},
            "total_probes": total_probes,
            "flip_rate": observed_flip_rate,
            "observed_flip_rate": observed_flip_rate,
            "expected_flip_rate": expected_flip_rate,
            "preserve_rate": preserve_rate,
            "behavioral_consistency": behavioral_consistency,
            "satisfaction_rate": behavioral_consistency,
            "confidence_flip_rate": confidence_flip_rate,
            "ece": ece,
            "transition_matrix": transition_matrix,
            "confidence_shifts": confidence_shifts,
            "evaluations": evaluations,
            "probe_results": [pr.to_dict() for pr in canonical_probe_results],
            "canonical_results": canonical_probe_results,
            "failures": failures,
            "failure_counts": failure_counts,
        }
