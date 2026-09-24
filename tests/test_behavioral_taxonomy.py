"""
Synthetic Behavioral Taxonomy Calibration Test Suite.
Verifies the isolated, deterministic classify_behavior function against the canonical
diagnostic behavior classes: BLIND, SPURIOUS, MISWEIGHTED, UNDETERMINED, and NONE.
Strictly adheres to Sections 6, 7, 19, 20, 22 of the Research-Integrity Specification.
"""
import unittest

from blindspot.core.types import (
    FailureCategory,
    BehavioralOutcome,
    ExpectedLabelRelation,
    ExpectedConfidenceRelation,
    SemanticIntent,
)
from blindspot.testing.behavioral import classify_behavior


class TestBehavioralTaxonomyCalibration(unittest.TestCase):
    """
    Controlled synthetic tests where model predictions and probe expectations
    are explicitly configured to test taxonomy reachability and precision.
    """

    # ----------------------------------------------------------------------
    # CASE 1 — EXPECTED FLIP
    # ----------------------------------------------------------------------
    def test_case1_expected_flip(self):
        """
        Original: POSITIVE
        Probe: NEGATIVE
        Expected: REVERSE_POLARITY
        Result: EXPECTED_FLIP, failure = NONE
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.92,
            probe_confidence=0.88,
            expected_effect="invert",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_FLIP)
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertTrue(evidence["is_prediction_flip"])
        self.assertIn("correctly flipped", rationale)

    # ----------------------------------------------------------------------
    # CASE 2 — BLIND
    # ----------------------------------------------------------------------
    def test_case2_blind(self):
        """
        Original: POSITIVE
        Probe: POSITIVE
        Expected: REVERSE_POLARITY
        Result: MISSING_FLIP, failure = BLIND
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.91,
            probe_confidence=0.89,
            expected_effect="invert",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)
        self.assertEqual(failure_type, FailureCategory.BLIND)
        self.assertFalse(evidence["is_prediction_flip"])
        self.assertIn("retained the same predicted class", rationale.lower())

    # ----------------------------------------------------------------------
    # CASE 3 — EXPECTED PRESERVE
    # ----------------------------------------------------------------------
    def test_case3_expected_preserve(self):
        """
        Original: POSITIVE
        Probe: POSITIVE
        Expected: PRESERVE_MEANING
        Result: EXPECTED_PRESERVE, failure = NONE
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.94,
            probe_confidence=0.93,
            expected_effect="preserve",
            semantic_intent="PRESERVE_MEANING",
            expected_label_relation="SAME_LABEL",
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertFalse(evidence["is_prediction_flip"])
        self.assertIn("correctly preserved", rationale)

    # ----------------------------------------------------------------------
    # CASE 4 — SPURIOUS
    # ----------------------------------------------------------------------
    def test_case4_spurious(self):
        """
        Original: POSITIVE
        Probe: NEGATIVE
        Expected: PRESERVE_MEANING
        Result: UNEXPECTED_FLIP, failure = SPURIOUS
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.95,
            probe_confidence=0.80,
            expected_effect="preserve",
            semantic_intent="PRESERVE_MEANING",
            expected_label_relation="SAME_LABEL",
        )
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_FLIP)
        self.assertEqual(failure_type, FailureCategory.SPURIOUS)
        self.assertTrue(evidence["is_prediction_flip"])
        self.assertIn("unexpectedly changed its predicted class", rationale.lower())

    # ----------------------------------------------------------------------
    # CASE 5 — MULTICLASS FLIP
    # ----------------------------------------------------------------------
    def test_case5_multiclass_flip(self):
        """
        Original: POSITIVE
        Probe: NEUTRAL
        Expected: REVERSE_POLARITY
        Result: is_prediction_flip = TRUE, EXPECTED_FLIP, failure = NONE
        Does NOT require NEGATIVE specifically.
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEUTRAL",
            original_confidence=0.85,
            probe_confidence=0.72,
            expected_effect="invert",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
        )
        self.assertTrue(evidence["is_prediction_flip"])
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_FLIP)
        self.assertEqual(failure_type, FailureCategory.NONE)

    # ----------------------------------------------------------------------
    # CASE 6 — MULTICLASS NO FLIP
    # ----------------------------------------------------------------------
    def test_case6_multiclass_no_flip(self):
        """
        Original: POSITIVE
        Probe: POSITIVE
        Result: is_prediction_flip = FALSE
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.88,
            probe_confidence=0.87,
            expected_effect="preserve",
            semantic_intent="PRESERVE_MEANING",
            expected_label_relation="SAME_LABEL",
        )
        self.assertFalse(evidence["is_prediction_flip"])
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)

    # ----------------------------------------------------------------------
    # CASE 7 — MISWEIGHTED (Directional Confidence Inversion)
    # ----------------------------------------------------------------------
    def test_case7_misweighted_degree_drop(self):
        """
        Original: POSITIVE (0.90)
        Probe: POSITIVE (0.45) -> delta = -45.0 pp (exceeds threshold 15.0 pp)
        Expected: STRENGTHEN_POLARITY with INCREASE
        Result: MISWEIGHTED
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.45,
            expected_effect="strengthen",
            semantic_intent="STRENGTHEN_POLARITY",
            expected_label_relation="SAME_LABEL",
            expected_confidence_relation="INCREASE",
            confidence_delta_threshold_pp=15.0,
        )
        self.assertEqual(failure_type, FailureCategory.MISWEIGHTED)
        self.assertIn("dropped by 45.00 percentage points", rationale)
        self.assertAlmostEqual(evidence["confidence_delta_pp"], -45.0)

    def test_case7_misweighted_degree_surge_on_downtoning(self):
        """
        Original: POSITIVE (0.60)
        Probe: POSITIVE (0.95) -> delta = +35.0 pp (exceeds threshold 15.0 pp)
        Expected: WEAKEN_POLARITY with DECREASE
        Result: MISWEIGHTED
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.60,
            probe_confidence=0.95,
            expected_effect="weaken",
            semantic_intent="WEAKEN_POLARITY",
            expected_label_relation="SAME_LABEL",
            expected_confidence_relation="DECREASE",
            confidence_delta_threshold_pp=15.0,
        )
        self.assertEqual(failure_type, FailureCategory.MISWEIGHTED)
        self.assertIn("confidence increased by 35.00 percentage points", rationale)

    def test_case7_misweighted_strengthening_flipped_label(self):
        """
        Original: POSITIVE (0.85)
        Probe: NEGATIVE (0.80)
        Expected: STRENGTHEN_POLARITY
        Result: MISWEIGHTED (strengthening should not invert sentiment)
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.85,
            probe_confidence=0.80,
            expected_effect="strengthen",
            semantic_intent="STRENGTHEN_POLARITY",
            expected_label_relation="SAME_LABEL",
        )
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_FLIP)
        self.assertEqual(failure_type, FailureCategory.MISWEIGHTED)

    # ----------------------------------------------------------------------
    # CASE 8 — UNDETERMINED
    # ----------------------------------------------------------------------
    def test_case8_undetermined_missing_labels(self):
        """
        Missing original or probe label outputs.
        Result: UNDETERMINED
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.90,
        )
        self.assertEqual(outcome, BehavioralOutcome.UNDETERMINED)
        self.assertEqual(failure_type, FailureCategory.UNDETERMINED)

    def test_case8_undetermined_missing_confidence(self):
        """
        Missing confidence values.
        Result: UNDETERMINED
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=None,
            probe_confidence=0.85,
        )
        self.assertEqual(outcome, BehavioralOutcome.UNDETERMINED)
        self.assertEqual(failure_type, FailureCategory.UNDETERMINED)

    def test_case8_undetermined_ambiguous_contract(self):
        """
        Ambiguous probe contract with UNDETERMINED effect and no label relation.
        Result: UNDETERMINED
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.90,
            expected_effect="UNDETERMINED",
            semantic_intent="OTHER",
            expected_label_relation="",
        )
        self.assertEqual(outcome, BehavioralOutcome.UNDETERMINED)
        self.assertEqual(failure_type, FailureCategory.UNDETERMINED)

    # ----------------------------------------------------------------------
    # INDEPENDENCE AND INTEGRITY CHECKS
    # ----------------------------------------------------------------------
    def test_classifier_never_depends_on_model_name(self):
        """
        Classifier output must emerge strictly from the probe contract,
        predictions, and confidence deltas—never from model identity.
        """
        for dummy_model_name in ["distilbert-base-uncased", "roberta-large", "bert-multilingual", "llama-custom"]:
            meta = {"model_name": dummy_model_name}
            _, failure, _, _ = classify_behavior(
                original_label="POSITIVE",
                probe_label="POSITIVE",
                original_confidence=0.90,
                probe_confidence=0.90,
                expected_effect="invert",
                semantic_intent="REVERSE_POLARITY",
                probe_metadata=meta,
            )
            self.assertEqual(failure, FailureCategory.BLIND)

    def test_zero_failures_remain_zero(self):
        """
        If all probes behave according to expectations, zero failures must remain exactly zero.
        """
        # Model correctly inverts on negation
        _, f1, _, _ = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.90,
            probe_confidence=0.85,
            expected_effect="invert",
            semantic_intent="REVERSE_POLARITY",
        )
        # Model correctly preserves on synonym
        _, f2, _, _ = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.91,
            expected_effect="preserve",
            semantic_intent="PRESERVE_MEANING",
        )
        self.assertEqual(f1, FailureCategory.NONE)
        self.assertEqual(f2, FailureCategory.NONE)


if __name__ == "__main__":
    unittest.main()
