"""
Unit and Integration Test Suite for BlindSpot Scientific Repairs.
Validates the 25 core scientific integrity invariants defined in the audit:
- Canonical semantic polarity representations
- Accurate 3-class vs binary model mappings
- Rejection of non-sentiment models
- Deterministic baseline ID anchoring
- Disambiguation of raw label flips vs semantic polarity flips vs state changes
- Deterministic failure taxonomy diagnoses (Blind, Spurious, Misweighted, Undetermined, None)
- Correct metric calculations (observed, expected, compliance, consistency)
- ProbeValidator criteria
- RunPlan staging and execution fidelity
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from blindspot.core.types import (
    SemanticPolarity,
    ExpectationType,
    BehavioralRelation,
    ProbeExpectation,
    PredictionResult,
    BaselineEvaluation,
    ModelProbeEvaluation,
    LinguisticProbe,
    SharedProbeSet,
    RunPlan,
    FailureCategory,
    BehavioralOutcome,
    is_raw_label_flip,
    is_polarity_flip,
    is_semantic_state_change,
)
from blindspot.models.huggingface_wrapper import map_raw_label_to_semantic_polarity
from blindspot.models.registry import ModelRegistry
from blindspot.testing.behavioral import classify_behavior
from blindspot.testing.metrics import (
    compute_observed_flip_rate,
    compute_expected_flip_rate,
    compute_expected_flip_compliance,
    compute_preserve_rate,
    compute_behavioral_consistency,
    compute_raw_label_flip_rate,
    compute_polarity_flip_rate,
)
from blindspot.perturbations.shared import ProbeValidator


class TestScientificRepairs(unittest.TestCase):

    # 1. Binary model prediction label mapping
    def test_case_01_binary_label_mapping(self):
        lbl0, pol0 = map_raw_label_to_semantic_polarity("LABEL_0", raw_id=0, num_classes=2)
        lbl1, pol1 = map_raw_label_to_semantic_polarity("LABEL_1", raw_id=1, num_classes=2)
        self.assertEqual(lbl0, "NEGATIVE")
        self.assertEqual(pol0, SemanticPolarity.NEGATIVE)
        self.assertEqual(lbl1, "POSITIVE")
        self.assertEqual(pol1, SemanticPolarity.POSITIVE)

    # 2. 3-Class model prediction label mapping
    def test_case_02_three_class_label_mapping(self):
        lbl0, pol0 = map_raw_label_to_semantic_polarity("LABEL_0", raw_id=0, num_classes=3)
        lbl1, pol1 = map_raw_label_to_semantic_polarity("LABEL_1", raw_id=1, num_classes=3)
        lbl2, pol2 = map_raw_label_to_semantic_polarity("LABEL_2", raw_id=2, num_classes=3)
        self.assertEqual(lbl0, "NEGATIVE")
        self.assertEqual(pol0, SemanticPolarity.NEGATIVE)
        self.assertEqual(lbl1, "NEUTRAL")
        self.assertEqual(pol1, SemanticPolarity.NEUTRAL)
        self.assertEqual(lbl2, "POSITIVE")
        self.assertEqual(pol2, SemanticPolarity.POSITIVE)

    # 3. Binary model SST-2 string label mapping
    def test_case_03_sst2_string_label_mapping(self):
        lbl_neg, pol_neg = map_raw_label_to_semantic_polarity("NEGATIVE", raw_id=0, num_classes=2)
        lbl_pos, pol_pos = map_raw_label_to_semantic_polarity("POSITIVE", raw_id=1, num_classes=2)
        self.assertEqual(lbl_neg, "NEGATIVE")
        self.assertEqual(pol_neg, SemanticPolarity.NEGATIVE)
        self.assertEqual(lbl_pos, "POSITIVE")
        self.assertEqual(pol_pos, SemanticPolarity.POSITIVE)

    # 4. 3-Class Twitter RoBERTa string label mapping
    def test_case_04_twitter_roberta_string_label_mapping(self):
        lbl0, pol0 = map_raw_label_to_semantic_polarity("Negative", raw_id=0, num_classes=3)
        lbl1, pol1 = map_raw_label_to_semantic_polarity("Neutral", raw_id=1, num_classes=3)
        lbl2, pol2 = map_raw_label_to_semantic_polarity("Positive", raw_id=2, num_classes=3)
        self.assertEqual(lbl0, "NEGATIVE")
        self.assertEqual(pol0, SemanticPolarity.NEGATIVE)
        self.assertEqual(lbl1, "NEUTRAL")
        self.assertEqual(pol1, SemanticPolarity.NEUTRAL)
        self.assertEqual(lbl2, "POSITIVE")
        self.assertEqual(pol2, SemanticPolarity.POSITIVE)

    # 5. Non-sentiment model rejection
    def test_case_05_non_sentiment_rejection(self):
        reg = ModelRegistry()
        is_valid, reason, _ = reg.validate_model_for_sentiment("roberta-base-openai-detector")
        self.assertFalse(is_valid)
        self.assertIn("AI_TEXT_DETECTION", reason)

    # 6. Immutable baseline ID computation (deterministic SHA-256)
    def test_case_06_baseline_id_determinism(self):
        b1 = BaselineEvaluation.compute_baseline_id("model_A", "The movie was fantastic.")
        b2 = BaselineEvaluation.compute_baseline_id("model_A", "The movie was fantastic.")
        b3 = BaselineEvaluation.compute_baseline_id("model_B", "The movie was fantastic.")
        self.assertEqual(b1, b2)
        self.assertNotEqual(b1, b3)
        self.assertTrue(b1.startswith("base_"))

    # 7. Single baseline evaluation per (model, seed)
    def test_case_07_single_baseline_per_model_seed(self):
        pred = PredictionResult(label="POSITIVE", confidence=0.98, semantic_polarity=SemanticPolarity.POSITIVE)
        base = BaselineEvaluation(
            model_id="distilbert-base-uncased-finetuned-sst-2-english",
            seed_text="The movie was fantastic.",
            prediction=pred,
        )
        self.assertTrue(base.baseline_id.startswith("base_"))
        self.assertEqual(base.semantic_polarity, SemanticPolarity.POSITIVE)
        self.assertEqual(base.confidence, 0.98)

    # 8. Distinct flip definitions (raw label flip vs polarity flip vs state change)
    def test_case_08_flip_definitions_distinction(self):
        # Case A: POSITIVE -> NEUTRAL
        self.assertTrue(is_raw_label_flip("POSITIVE", "NEUTRAL"))
        self.assertFalse(is_polarity_flip(SemanticPolarity.POSITIVE, SemanticPolarity.NEUTRAL))
        self.assertTrue(is_semantic_state_change(SemanticPolarity.POSITIVE, SemanticPolarity.NEUTRAL))

        # Case B: POSITIVE -> NEGATIVE
        self.assertTrue(is_raw_label_flip("POSITIVE", "NEGATIVE"))
        self.assertTrue(is_polarity_flip(SemanticPolarity.POSITIVE, SemanticPolarity.NEGATIVE))
        self.assertTrue(is_semantic_state_change(SemanticPolarity.POSITIVE, SemanticPolarity.NEGATIVE))

        # Case C: POSITIVE -> POSITIVE
        self.assertFalse(is_raw_label_flip("POSITIVE", "POSITIVE"))
        self.assertFalse(is_polarity_flip(SemanticPolarity.POSITIVE, SemanticPolarity.POSITIVE))
        self.assertFalse(is_semantic_state_change(SemanticPolarity.POSITIVE, SemanticPolarity.POSITIVE))

    # 9. Transition POSITIVE -> NEGATIVE under REVERSE_POLARITY -> EXPECTED_FLIP, Failure NONE
    def test_case_09_expected_flip_reversal(self):
        exp = ProbeExpectation(ExpectationType.REVERSE_POLARITY, BehavioralRelation.POLARITY_REVERSED)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "NEGATIVE", 0.95, 0.90,
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.NEGATIVE,
            expectation=exp,
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_FLIP)
        self.assertEqual(failure, FailureCategory.NONE)
        self.assertTrue(ev["expectation_match"])
        self.assertFalse(ev["preservation"])

    # 10. Transition POSITIVE -> POSITIVE under REVERSE_POLARITY -> MISSING_FLIP, Failure BLIND
    def test_case_10_missing_flip_blind(self):
        exp = ProbeExpectation(ExpectationType.REVERSE_POLARITY, BehavioralRelation.POLARITY_REVERSED)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "POSITIVE", 0.95, 0.92,
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
            expectation=exp,
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)
        self.assertEqual(failure, FailureCategory.BLIND)
        self.assertFalse(ev["expectation_match"])

    # 11. Transition POSITIVE -> NEUTRAL under REVERSE_POLARITY -> UNEXPECTED_CHANGE, Failure MISWEIGHTED
    def test_case_11_neutralization_under_reversal(self):
        exp = ProbeExpectation(ExpectationType.REVERSE_POLARITY, BehavioralRelation.POLARITY_REVERSED)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "NEUTRAL", 0.95, 0.60,
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.NEUTRAL,
            expectation=exp,
        )
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_CHANGE)
        self.assertEqual(failure, FailureCategory.MISWEIGHTED)
        self.assertFalse(ev["expectation_match"])

    # 12. Transition POSITIVE -> POSITIVE under PRESERVE_POLARITY (stable confidence) -> EXPECTED_PRESERVE, Failure NONE
    def test_case_12_expected_preserve_none(self):
        exp = ProbeExpectation(ExpectationType.PRESERVE_POLARITY, BehavioralRelation.SAME_POLARITY)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "POSITIVE", 0.95, 0.93,
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
            expectation=exp,
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)
        self.assertEqual(failure, FailureCategory.NONE)
        self.assertTrue(ev["expectation_match"])
        self.assertTrue(ev["preservation"])

    # 13. Transition POSITIVE -> POSITIVE under PRESERVE_POLARITY with >15pp confidence drop -> Failure MISWEIGHTED
    def test_case_13_expected_preserve_confidence_drop(self):
        exp = ProbeExpectation(ExpectationType.PRESERVE_POLARITY, BehavioralRelation.SAME_POLARITY)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "POSITIVE", 0.95, 0.70,  # 25pp drop
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
            expectation=exp,
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)
        self.assertEqual(failure, FailureCategory.MISWEIGHTED)
        self.assertFalse(ev["expectation_match"])

    # 14. Transition POSITIVE -> NEGATIVE under PRESERVE_POLARITY -> UNEXPECTED_FLIP, Failure SPURIOUS
    def test_case_14_unexpected_flip_spurious(self):
        exp = ProbeExpectation(ExpectationType.PRESERVE_POLARITY, BehavioralRelation.SAME_POLARITY)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "NEGATIVE", 0.95, 0.90,
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.NEGATIVE,
            expectation=exp,
        )
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_FLIP)
        self.assertEqual(failure, FailureCategory.SPURIOUS)
        self.assertFalse(ev["expectation_match"])

    # 15. Transition POSITIVE -> NEUTRAL under PRESERVE_POLARITY -> UNEXPECTED_CHANGE, Failure SPURIOUS
    def test_case_15_unexpected_neutral_shift_spurious(self):
        exp = ProbeExpectation(ExpectationType.PRESERVE_POLARITY, BehavioralRelation.SAME_POLARITY)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "NEUTRAL", 0.95, 0.65,
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.NEUTRAL,
            expectation=exp,
        )
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_CHANGE)
        self.assertEqual(failure, FailureCategory.SPURIOUS)
        self.assertFalse(ev["expectation_match"])

    # 16. Degree intensifier causing confidence drop > 15pp -> Failure MISWEIGHTED
    def test_case_16_intensifier_drop_misweighted(self):
        exp = ProbeExpectation(ExpectationType.INTENSIFY, BehavioralRelation.POLARITY_STRENGTHENED)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "POSITIVE", 0.95, 0.70,
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
            expectation=exp,
            semantic_intent="INTENSIFY",
        )
        self.assertEqual(failure, FailureCategory.MISWEIGHTED)

    # 17. Degree downtoner causing confidence increase > 15pp -> Failure MISWEIGHTED
    def test_case_17_downtoner_increase_misweighted(self):
        exp = ProbeExpectation(ExpectationType.DOWNTONE, BehavioralRelation.POLARITY_WEAKENED)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "POSITIVE", 0.60, 0.95,
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
            expectation=exp,
            semantic_intent="DOWNTONE",
        )
        self.assertEqual(failure, FailureCategory.MISWEIGHTED)

    # 18. Undetermined expectation -> Failure UNDETERMINED
    def test_case_18_undetermined_expectation(self):
        exp = ProbeExpectation(ExpectationType.UNKNOWN, BehavioralRelation.UNKNOWN)
        outcome, failure, ev, _ = classify_behavior(
            "POSITIVE", "POSITIVE", 0.90, 0.90,
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
            expectation=exp,
        )
        self.assertEqual(outcome, BehavioralOutcome.UNDETERMINED)
        self.assertEqual(failure, FailureCategory.UNDETERMINED)

    # 19. Missing label / confidence -> Failure UNDETERMINED
    def test_case_19_missing_labels_undetermined(self):
        outcome1, failure1, _, _ = classify_behavior(None, "POSITIVE", 0.90, 0.90)
        self.assertEqual(failure1, FailureCategory.UNDETERMINED)
        outcome2, failure2, _, _ = classify_behavior("POSITIVE", "POSITIVE", None, 0.90)
        self.assertEqual(failure2, FailureCategory.UNDETERMINED)

    # 20. Observed flip rate metric
    def test_case_20_observed_flip_rate_metric(self):
        evals = [
            {"polarity_flip": True},
            {"polarity_flip": False},
            {"polarity_flip": True},
            {"polarity_flip": False},
        ]
        self.assertAlmostEqual(compute_observed_flip_rate(evals), 0.50)

    # 21. Expected flip rate metric (fraction of probe suite expecting a flip)
    def test_case_21_expected_flip_rate_metric(self):
        evals = [
            {"expected_flip": True},
            {"expected_flip": False},
            {"expected_flip": False},
            {"expected_flip": False},
        ]
        self.assertAlmostEqual(compute_expected_flip_rate(evals), 0.25)

    # 22. Expected flip compliance metric (fraction of expected flips that actually flipped)
    def test_case_22_expected_flip_compliance_metric(self):
        evals = [
            {"expected_flip": True, "polarity_flip": True},
            {"expected_flip": True, "polarity_flip": False},
            {"expected_flip": False, "polarity_flip": False},
        ]
        # 1 flip observed out of 2 expected flips = 0.50 compliance
        self.assertAlmostEqual(compute_expected_flip_compliance(evals), 0.50)

    # 23. Behavioral consistency metric (matches / total)
    def test_case_23_behavioral_consistency_metric(self):
        evals = [
            {"expectation_match": True},
            {"expectation_match": True},
            {"expectation_match": False},
            {"expectation_match": True},
        ]
        self.assertAlmostEqual(compute_behavioral_consistency(evals), 0.75)

    # 24. ProbeValidator checking text existence, difference, and validity
    def test_case_24_probe_validator(self):
        # Empty text
        p_empty = LinguisticProbe.create(seed_text="", perturbed_text="abc", perturbation_type="negation")
        ok, reason = ProbeValidator.validate_probe(p_empty)
        self.assertFalse(ok)

        # Identical text (no mutation)
        p_same = LinguisticProbe.create(seed_text="Good film.", perturbed_text="Good film.", perturbation_type="negation")
        ok, reason = ProbeValidator.validate_probe(p_same)
        self.assertFalse(ok)
        self.assertIn("identical", reason.lower())

        # Valid probe
        p_valid = LinguisticProbe.create(seed_text="Good film.", perturbed_text="Bad film.", perturbation_type="negation", expected_flip=True)
        ok, reason = ProbeValidator.validate_probe(p_valid)
        self.assertTrue(ok)

    # 25. RunPlan validation (staged probe IDs == executed probe IDs)
    def test_case_25_run_plan_validation(self):
        plan = RunPlan(
            experiment_id="exp_01",
            model_ids=["model_1"],
            probe_set_id="pset_01",
            selected_probe_ids=["prb_1", "prb_2", "prb_3"],
        )
        # Valid execution
        ok, msg = plan.validate_execution(["prb_1", "prb_2", "prb_3"])
        self.assertTrue(ok)

        # Missing a probe
        ok_miss, msg_miss = plan.validate_execution(["prb_1", "prb_2"])
        self.assertFalse(ok_miss)
        self.assertIn("Missing", msg_miss)

        # Unexpected extra probe
        ok_extra, msg_extra = plan.validate_execution(["prb_1", "prb_2", "prb_3", "prb_4"])
        self.assertFalse(ok_extra)
        self.assertIn("Unexpected", msg_extra)


if __name__ == "__main__":
    unittest.main()
