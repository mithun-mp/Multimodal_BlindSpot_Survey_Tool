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
    SemanticPolarity,
    ExpectationType,
    BehavioralRelation,
    ProbeExpectation,
    is_raw_label_flip,
    is_polarity_flip,
    is_semantic_state_change,
    resolve_expected_behavioral_relation,
    determine_observed_behavioral_relation,
)
from .metrics import (
    compute_flip_rate,
    compute_observed_flip_rate,
    compute_expected_flip_rate,
    compute_expected_flip_compliance,
    compute_preserve_rate,
    compute_behavioral_consistency,
    compute_raw_label_flip_rate,
    compute_polarity_flip_rate,
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
    original_polarity: Optional[SemanticPolarity] = None,
    probe_polarity: Optional[SemanticPolarity] = None,
    expectation: Optional[ProbeExpectation] = None,
) -> Tuple[BehavioralOutcome, FailureCategory, Dict[str, Any], str]:
    """
    Pure deterministic classifier for behavioral auditing (Phases 6, 7, 8).
    Evaluates expected vs observed predictions, multiclass transitions, and confidence movements.
    Distinguishes:
        - raw_label_flip: index/string change
        - polarity_flip: POSITIVE <-> NEGATIVE reversal
        - semantic_state_change: state change including transitions to/from NEUTRAL
    Classifies into Primary Behavioral Outcome and Secondary Failure Taxonomy.
    Does NOT depend on model names, UI state, or Streamlit.

    Returns:
        (behavioral_outcome, failure_type, evidence_dict, rationale_str)
    """
    # 1. Validation & Undetermined Check
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

    orig_lbl = str(original_label).strip()
    prb_lbl = str(probe_label).strip()
    orig_conf = float(original_confidence)
    prb_conf = float(probe_confidence)

    # 2. Canonical Semantic Polarity resolution
    orig_pol = original_polarity or SemanticPolarity.from_str(orig_lbl)
    prb_pol = probe_polarity or SemanticPolarity.from_str(prb_lbl)

    # 3. Flips and Transitions
    raw_flipped = is_raw_label_flip(orig_lbl, prb_lbl)
    polarity_flipped = is_polarity_flip(orig_pol, prb_pol)
    state_changed = is_semantic_state_change(orig_pol, prb_pol)
    confidence_delta_pp = (prb_conf - orig_conf) * 100.0
    transition_str = f"{orig_lbl} ({orig_pol.value}) → {prb_lbl} ({prb_pol.value})"

    observed_rel = determine_observed_behavioral_relation(
        orig_pol, prb_pol, orig_conf, prb_conf, delta_threshold_pp=confidence_delta_threshold_pp
    )

    norm_effect = str(expected_effect or "").strip().upper()
    norm_intent = str(semantic_intent or "").strip().upper()
    norm_conf_rel = str(expected_confidence_relation or "").strip().upper()

    # 4. Resolve expectation
    if expectation is not None:
        exp_rel = expectation.expected_semantic_relation
        exp_type = expectation.expectation_type
    else:
        exp_type = ExpectationType.UNKNOWN
        if norm_intent == "REVERSE_POLARITY" or norm_effect in ("EXPECTED_FLIP", "INVERT"):
            exp_type = ExpectationType.REVERSE_POLARITY
        elif norm_intent in ("PRESERVE_POLARITY", "PRESERVE_MEANING") or norm_effect in ("EXPECTED_PRESERVE", "PRESERVE"):
            exp_type = ExpectationType.PRESERVE_POLARITY
        elif norm_intent == "ADD_NEGATION":
            # For ADD_NEGATION, if baseline polarity was neutral, negation does not reverse sentiment
            if orig_pol == SemanticPolarity.NEUTRAL:
                exp_type = ExpectationType.PRESERVE_POLARITY
            else:
                exp_type = ExpectationType.REVERSE_POLARITY
        elif norm_intent in ("STRENGTHEN_POLARITY", "INTENSIFY"):
            exp_type = ExpectationType.INTENSIFY
        elif norm_intent in ("WEAKEN_POLARITY", "DOWNTONE"):
            exp_type = ExpectationType.DOWNTONE
        elif norm_intent == "SHIFT_CONTRAST" or norm_effect == "CONCESSION":
            exp_type = ExpectationType.CONTRAST_SHIFT
        elif norm_intent in ("UNCERTAIN", "OTHER") or norm_effect in ("UNCERTAIN", "OTHER"):
            exp_type = ExpectationType.UNKNOWN

        exp_rel = resolve_expected_behavioral_relation(exp_type, orig_pol)

    evidence: Dict[str, Any] = {
        "original_label": orig_lbl,
        "probe_label": prb_lbl,
        "original_confidence": orig_conf,
        "probe_confidence": prb_conf,
        "confidence_delta_pp": confidence_delta_pp,
        "label_transition": transition_str,
        "raw_label_flip": raw_flipped,
        "polarity_flip": polarity_flipped,
        "semantic_state_change": state_changed,
        "is_prediction_flip": polarity_flipped if orig_pol in (SemanticPolarity.POSITIVE, SemanticPolarity.NEGATIVE) else raw_flipped,
        "original_polarity": orig_pol.value,
        "probe_polarity": prb_pol.value,
        "expected_relation": exp_rel.value if hasattr(exp_rel, "value") else str(exp_rel),
        "observed_relation": observed_rel.value if hasattr(observed_rel, "value") else str(observed_rel),
        "expected_effect": norm_effect,
        "semantic_intent": norm_intent,
        "threshold_pp": confidence_delta_threshold_pp,
    }

    # 5. Diagnostic Taxonomy Classification
    is_binary = bool(original_distribution and len(original_distribution) == 2)
    if is_binary and (orig_pol == SemanticPolarity.NEUTRAL or prb_pol == SemanticPolarity.NEUTRAL):
        evidence["is_unrepresentable_neutral"] = True
        evidence["semantic_compatibility"] = "NOT_DIRECTLY_REPRESENTABLE"
        # Capability-aware evaluation: binary model cannot output NEUTRAL
        if exp_type in (ExpectationType.PRESERVE_POLARITY, ExpectationType.UNKNOWN) and not raw_flipped:
            evidence["expectation_match"] = True
            evidence["preservation"] = True
            rationale = (
                f"Binary model forced-polarity output preserved ({transition_str}) "
                f"under neutral reference (neutral is unrepresentable in 2-class label space)."
            )
            return (
                BehavioralOutcome.EXPECTED_PRESERVE,
                FailureCategory.NONE,
                evidence,
                rationale,
            )
        elif exp_type == ExpectationType.PRESERVE_POLARITY and raw_flipped:
            evidence["expectation_match"] = False
            evidence["preservation"] = False
            rationale = (
                f"Binary model flipped prediction ({transition_str}) under neutral meaning-preserving perturbation."
            )
            return (
                BehavioralOutcome.UNEXPECTED_FLIP,
                FailureCategory.SPURIOUS,
                evidence,
                rationale,
            )

    if exp_type == ExpectationType.UNKNOWN or exp_rel == BehavioralRelation.UNKNOWN:
        evidence["expectation_match"] = False
        evidence["preservation"] = not polarity_flipped
        return (
            BehavioralOutcome.UNDETERMINED,
            FailureCategory.UNDETERMINED,
            evidence,
            "Undetermined probe expectation contract.",
        )

    # Check for explicit DIFFERENT_LABEL contract
    if expected_label_relation == "DIFFERENT_LABEL":
        if raw_flipped:
            evidence["is_prediction_flip"] = True
            evidence["expectation_match"] = True
            evidence["preservation"] = False
            rationale = f"Model correctly flipped and changed label ({transition_str}) under DIFFERENT_LABEL expectation."
            return BehavioralOutcome.EXPECTED_FLIP, FailureCategory.NONE, evidence, rationale

    # REVERSE POLARITY EXPECTATION
    if exp_rel == BehavioralRelation.POLARITY_REVERSED:
        if observed_rel == BehavioralRelation.POLARITY_REVERSED:
            evidence["expectation_match"] = True
            evidence["preservation"] = False
            rationale = f"Model correctly flipped and reversed polarity ({transition_str}) under polarity-altering probe."
            return BehavioralOutcome.EXPECTED_FLIP, FailureCategory.NONE, evidence, rationale

        elif orig_pol != SemanticPolarity.NEUTRAL and prb_pol == SemanticPolarity.NEUTRAL:
            evidence["expectation_match"] = False
            evidence["preservation"] = False
            rationale = (
                f"Probe demanded polarity reversal, but model neutralized sentiment ({transition_str}), "
                f"indicating partial sensitivity or attenuation."
            )
            return BehavioralOutcome.UNEXPECTED_CHANGE, FailureCategory.MISWEIGHTED, evidence, rationale

        else:
            # Model preserved polarity despite reversal probe -> BLIND
            evidence["expectation_match"] = False
            evidence["preservation"] = True
            rationale = (
                f"Probe introduces a polarity reversal ({norm_intent or 'REVERSE_POLARITY'}), "
                f"but model retained the same predicted class and polarity ({transition_str})."
            )
            return BehavioralOutcome.MISSING_FLIP, FailureCategory.BLIND, evidence, rationale

    # PRESERVE POLARITY EXPECTATION
    elif exp_rel == BehavioralRelation.SAME_POLARITY:
        if not polarity_flipped and not state_changed:
            # Polarity was preserved. Check for disproportionate confidence movements.
            if norm_intent in ("STRENGTHEN_POLARITY", "INTENSIFY") or norm_conf_rel == "INCREASE":
                if confidence_delta_pp < -confidence_delta_threshold_pp:
                    evidence["expectation_match"] = False
                    evidence["preservation"] = True
                    rationale = (
                        f"Expected polarity strengthening, but confidence dropped by "
                        f"{abs(confidence_delta_pp):.2f} percentage points ({orig_conf:.2f} → {prb_conf:.2f})."
                    )
                    return BehavioralOutcome.EXPECTED_PRESERVE, FailureCategory.MISWEIGHTED, evidence, rationale

            elif norm_intent in ("WEAKEN_POLARITY", "DOWNTONE") or norm_conf_rel == "DECREASE":
                if confidence_delta_pp > confidence_delta_threshold_pp:
                    evidence["expectation_match"] = False
                    evidence["preservation"] = True
                    rationale = (
                        f"Expected polarity downtoning, but confidence increased by "
                        f"{confidence_delta_pp:.2f} percentage points ({orig_conf:.2f} → {prb_conf:.2f})."
                    )
                    return BehavioralOutcome.EXPECTED_PRESERVE, FailureCategory.MISWEIGHTED, evidence, rationale

            elif confidence_delta_pp < -confidence_delta_threshold_pp:
                evidence["expectation_match"] = False
                evidence["preservation"] = True
                rationale = (
                    f"Polarity preserved, but confidence collapsed by {abs(confidence_delta_pp):.2f} percentage points "
                    f"under meaning-preserving perturbation."
                )
                return BehavioralOutcome.EXPECTED_PRESERVE, FailureCategory.MISWEIGHTED, evidence, rationale

            evidence["expectation_match"] = True
            evidence["preservation"] = True
            rationale = f"Model correctly preserved prediction ({transition_str}) under meaning-preserving probe."
            return BehavioralOutcome.EXPECTED_PRESERVE, FailureCategory.NONE, evidence, rationale

        else:
            # Polarity or state changed unexpectedly
            evidence["expectation_match"] = False
            evidence["preservation"] = False
            if norm_intent in ("STRENGTHEN_POLARITY", "WEAKEN_POLARITY", "INTENSIFY", "DOWNTONE"):
                rationale = (
                    f"Model inverted/altered prediction ({transition_str}) when presented with a degree modifier ({norm_intent}), "
                    f"indicating disproportionately skewed feature weighting."
                )
                return BehavioralOutcome.UNEXPECTED_FLIP, FailureCategory.MISWEIGHTED, evidence, rationale
            else:
                rationale = (
                    f"The perturbation is meaning-preserving ({norm_intent or 'PRESERVE_POLARITY'}), "
                    f"but model unexpectedly changed its predicted class and altered its predicted state ({transition_str})."
                )
                outcome = BehavioralOutcome.UNEXPECTED_FLIP if polarity_flipped else BehavioralOutcome.UNEXPECTED_CHANGE
                return outcome, FailureCategory.SPURIOUS, evidence, rationale

    # INTENSIFY EXPECTATION
    elif exp_type == ExpectationType.INTENSIFY:
        if observed_rel in (BehavioralRelation.SAME_POLARITY, BehavioralRelation.POLARITY_STRENGTHENED, BehavioralRelation.POLARITY_WEAKENED):
            if confidence_delta_pp < -confidence_delta_threshold_pp:
                evidence["expectation_match"] = False
                evidence["preservation"] = True
                rationale = f"Intensifier caused confidence to drop: dropped by {abs(confidence_delta_pp):.2f} percentage points ({transition_str})."
                return BehavioralOutcome.EXPECTED_PRESERVE, FailureCategory.MISWEIGHTED, evidence, rationale
            evidence["expectation_match"] = True
            evidence["preservation"] = True
            return BehavioralOutcome.EXPECTED_PRESERVE, FailureCategory.NONE, evidence, "Intensifier preserved polarity."
        else:
            evidence["expectation_match"] = False
            evidence["preservation"] = False
            return BehavioralOutcome.UNEXPECTED_FLIP, FailureCategory.MISWEIGHTED, evidence, f"Intensifier inverted polarity ({transition_str})."

    # DOWNTONE EXPECTATION
    elif exp_type == ExpectationType.DOWNTONE:
        if polarity_flipped:
            evidence["expectation_match"] = False
            evidence["preservation"] = False
            return BehavioralOutcome.UNEXPECTED_FLIP, FailureCategory.MISWEIGHTED, evidence, f"Downtoner inverted polarity ({transition_str})."
        elif confidence_delta_pp > confidence_delta_threshold_pp:
            evidence["expectation_match"] = False
            evidence["preservation"] = True
            return BehavioralOutcome.EXPECTED_PRESERVE, FailureCategory.MISWEIGHTED, evidence, f"Downtoner caused confidence to surge: confidence increased by {confidence_delta_pp:.2f} percentage points ({transition_str})."
        evidence["expectation_match"] = True
        evidence["preservation"] = True
        return BehavioralOutcome.EXPECTED_PRESERVE, FailureCategory.NONE, evidence, f"Downtoner preserved polarity ({transition_str})."

    evidence["expectation_match"] = False
    evidence["preservation"] = not polarity_flipped
    return BehavioralOutcome.UNDETERMINED, FailureCategory.UNDETERMINED, evidence, "Indeterminate behavioral transition."


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
            base_eval = BaselineEvaluation(
                model_id=self.model.model_name,
                seed_text=seed,
                sentence_type=stype,
                prediction=pred,
                latency_ms=pred.latency_ms,
            )
            # Evaluate baseline against semantic reference if present
            if hasattr(probe_set, "semantic_reference_set") and probe_set.semantic_reference_set:
                base_annot = probe_set.semantic_reference_set.baseline_annotation
                pred.evaluate_semantic_compatibility(base_annot.final_semantic_polarity)
                base_eval.semantic_reference = base_annot.to_dict()
                base_eval.semantic_compatibility = pred.semantic_compatibility
            baselines[seed] = base_eval

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

            base_eval = baselines.get(probe.seed_text)
            base_id = base_eval.baseline_id if base_eval else ""

            # Check for probe semantic reference
            sem_ref_data = getattr(probe, "semantic_reference", None)
            base_annot = None
            p_annot = None
            if hasattr(probe_set, "semantic_reference_set") and probe_set.semantic_reference_set:
                base_annot = getattr(probe_set.semantic_reference_set, "baseline_annotation", None)
                p_annot = probe_set.semantic_reference_set.probe_annotations.get(probe.probe_id)
                if p_annot:
                    sem_ref_data = p_annot.to_dict()
                    if base_annot:
                        sem_ref_data["baseline_semantic_polarity"] = base_annot.final_semantic_polarity.value
                    pert_pred.evaluate_semantic_compatibility(p_annot.final_semantic_polarity)

            # Derive expected behavioral contract from Semantic Ground Truth
            exp_effect = probe.expected_semantic_effect
            e_flip = probe.expected_flip
            exp_intent = getattr(probe, "semantic_intent", "")
            exp_label_rel = getattr(
                probe, "expected_label_relation", "DIFFERENT_LABEL" if e_flip else "SAME_LABEL"
            )

            if p_annot:
                sem_rel = p_annot.semantic_relation_to_baseline
                rel_str = sem_rel.value if hasattr(sem_rel, "value") else str(sem_rel)
                if rel_str in ("REVERSE", "REVERSE_POLARITY"):
                    e_flip = True
                    exp_effect = "EXPECTED_FLIP"
                    exp_intent = "REVERSE_POLARITY"
                    exp_label_rel = "DIFFERENT_LABEL"
                elif rel_str in ("PRESERVE", "PRESERVE_POLARITY"):
                    e_flip = False
                    exp_effect = "EXPECTED_PRESERVE"
                    exp_intent = "PRESERVE_POLARITY"
                    exp_label_rel = "SAME_LABEL"
                elif rel_str == "SHIFT_TO_NEUTRAL":
                    base_pol_str = base_annot.final_semantic_polarity.value if base_annot else "UNKNOWN"
                    e_flip = False
                    exp_effect = "SHIFT_TO_NEUTRAL"
                    exp_intent = "SHIFT_TO_NEUTRAL"
                    exp_label_rel = "DIFFERENT_LABEL" if base_pol_str != "NEUTRAL" else "SAME_LABEL"
                elif rel_str == "SHIFT_FROM_NEUTRAL":
                    e_flip = False
                    exp_effect = "SHIFT_FROM_NEUTRAL"
                    exp_intent = "SHIFT_FROM_NEUTRAL"
                    exp_label_rel = "UNCONSTRAINED"
                elif rel_str in ("UNCERTAIN", "OTHER"):
                    e_flip = False
                    exp_effect = "UNCERTAIN"
                    exp_intent = "UNCERTAIN"
                    exp_label_rel = "UNCONSTRAINED"

            # Pure deterministic classification with SemanticPolarity & ProbeExpectation
            outcome, failure_type, evidence, rationale = classify_behavior(
                original_label=orig_pred.label,
                probe_label=pert_pred.label,
                original_confidence=orig_pred.confidence,
                probe_confidence=pert_pred.confidence,
                expected_effect=exp_effect,
                semantic_intent=exp_intent,
                expected_label_relation=exp_label_rel,
                expected_confidence_relation=getattr(probe, "expected_confidence_relation", "UNCONSTRAINED"),
                original_distribution=orig_pred.probabilities,
                probe_distribution=pert_pred.probabilities,
                probe_metadata=probe.metadata,
                original_polarity=orig_pred.semantic_polarity,
                probe_polarity=pert_pred.semantic_polarity,
                expectation=getattr(probe, "expectation", None),
            )

            is_flipped = evidence["polarity_flip"] if orig_pred.semantic_polarity in (SemanticPolarity.POSITIVE, SemanticPolarity.NEGATIVE) else evidence["raw_label_flip"]
            delta = pert_pred.confidence - orig_pred.confidence
            delta_pts = delta * 100.0
            expectation_satisfied = evidence["expectation_match"]

            # Build backward-compatible ModelProbeEvaluation
            eval_item = ModelProbeEvaluation(
                model_id=self.model.model_name,
                probe_id=probe.probe_id,
                seed_text=probe.seed_text,
                perturbed_text=probe.perturbed_text,
                perturbation_type=probe.perturbation_type,
                expected_flip=e_flip,
                expected_semantic_effect=exp_effect,
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
                baseline_id=base_id,
                raw_label_flip=evidence["raw_label_flip"],
                polarity_flip=evidence["polarity_flip"],
                semantic_state_change=evidence["semantic_state_change"],
                expected_relation=evidence["expected_relation"],
                observed_relation=evidence["observed_relation"],
                expectation_match=evidence["expectation_match"],
                preservation=evidence["preservation"],
                semantic_reference=sem_ref_data,
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
                baseline_id=base_id,
                raw_label_flip=evidence["raw_label_flip"],
                polarity_flip=evidence["polarity_flip"],
                semantic_state_change=evidence["semantic_state_change"],
                expected_relation=evidence["expected_relation"],
                observed_relation=evidence["observed_relation"],
                expectation_match=evidence["expectation_match"],
                preservation=evidence["preservation"],
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
        suite_expected_flip_rate = float(sum(1 for e in evaluations if bool(getattr(e, "expected_flip", False))) / max(1, total_probes))
        expected_flip_compliance = compute_expected_flip_compliance(evaluations)
        preserve_rate = compute_preserve_rate(evaluations)
        behavioral_consistency = compute_behavioral_consistency(evaluations)
        raw_label_flip_rate = compute_raw_label_flip_rate(evaluations)
        polarity_flip_rate = compute_polarity_flip_rate(evaluations)
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
            "suite_expected_flip_rate": suite_expected_flip_rate,
            "expected_flip_rate": suite_expected_flip_rate,
            "expected_flip_compliance": expected_flip_compliance,
            "observed_expected_reversal_rate": expected_flip_compliance,
            "preserve_rate": preserve_rate,
            "behavioral_consistency": behavioral_consistency,
            "satisfaction_rate": behavioral_consistency,
            "raw_label_flip_rate": raw_label_flip_rate,
            "polarity_flip_rate": polarity_flip_rate,
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
