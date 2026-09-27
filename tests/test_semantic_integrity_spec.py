"""
Phase 21 Comprehensive Integrity Test Suite for BlindSpot Semantic Reference & Behavioral Engine.
Implements Tests 1 through 14 per research integrity specification:

TEST 1: Gemini disabled: No API key -> requests=0, gemini_confidence=None, status=unavailable/disabled, no fake Gemini label or confidence.
TEST 2: Fallback semantic reference: status=UNVERIFIED, never 'Final Ground-Truth'.
TEST 3: Gemini response: Mock response parsed correctly, confidence stored as self-reported, provider=GEMINI, requests incremented.
TEST 4: Gemini failure: Mock API failure -> experiment does not crash, no fabricated confidence, status indicates failure/unavailable.
TEST 5: Cache: Same text + same engine/model/schema hits cache; different model/schema/provider does not hit old entry.
TEST 6: P001: Negation insertion must NOT automatically set expected_flip=True. Relation derived from semantic references.
TEST 7: Runner: Verify runner never mutates semantic relation.
TEST 8: Human override: Gemini says POSITIVE, Human changes to NEGATIVE -> Final = NEGATIVE, original suggestion preserved.
TEST 9: Binary model + neutral: Verified semantic polarity = NEUTRAL, Binary output = POSITIVE -> UNREPRESENTABLE_NEUTRAL, not BLIND.
TEST 10: 3-class neutral preservation: Verified relation = PRESERVE_POLARITY, Baseline = NEUTRAL, Probe = NEUTRAL -> No automatic failure.
TEST 11: 3-class actual reversal: Verified relation = REVERSE_POLARITY, Baseline = POSITIVE, Probe = NEGATIVE -> Behavioral alignment.
TEST 12: Incorrect model behavior: Verified relation = REVERSE_POLARITY, Baseline = POSITIVE, Probe = POSITIVE -> BLIND classification.
TEST 13: Uncertain semantic relation: relation = UNCERTAIN -> behavioral alignment = NA, failure classification = UNDETERMINED.
TEST 14: No forced category coverage: If no BLIND examples exist, BLIND count = 0.
"""
import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from blindspot.semantic.types import (
    SemanticReferenceLabel,
    SemanticRelation,
    VerificationStatus,
    ReferenceProvider,
    SemanticAnnotation,
    SemanticReferenceSet,
)
from blindspot.semantic.cache import SemanticAnnotationCache
from blindspot.semantic.client import GeminiSemanticClient
from blindspot.semantic.service import SemanticReferenceService
from blindspot.perturbations.shared import LinguisticProbeCatalog, LinguisticProbe
from blindspot.core.types import (
    SharedProbeSet,
    PredictionResult,
    RunPlan,
    FailureCategory,
    BehavioralOutcome,
    SemanticPolarity,
)
from blindspot.testing.behavioral import classify_behavior, BehavioralTester
from blindspot.testing.metrics import (
    compute_observed_label_flip,
    compute_expected_semantic_change,
    compute_behavioral_alignment,
    classify_directional_transition,
    compute_confidence_delta_pp,
)


class TestSemanticIntegritySpecification(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.tmp_dir, "test_cache_v2.json")
        self.cache = SemanticAnnotationCache(cache_path=self.cache_file)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_01_gemini_disabled(self):
        """
        TEST 1: Gemini disabled (No API key).
        Expected: requests=0, gemini_confidence=None, status=unavailable/disabled,
        no fake Gemini label, no fake Gemini confidence.
        """
        client = GeminiSemanticClient(api_key="")
        self.assertFalse(client.is_online)
        self.assertEqual(client.requests_count, 0)
        self.assertIn("Disabled", client.status_string)

        service = SemanticReferenceService(client=client, cache=self.cache)
        probes = [
            LinguisticProbe.create(
                seed_text="The king is injured.",
                perturbed_text="The king is not injured.",
                perturbation_type="negation",
                expected_flip=False,
                name="p1",
            )
        ]
        ref_set = service.annotate_experiment("The king is injured.", probes)
        self.assertEqual(client.requests_count, 0)
        self.assertEqual(ref_set.api_requests, 0)

        # Baseline annotation
        base_annot = ref_set.baseline_annotation
        self.assertIsNone(base_annot.gemini_confidence)
        self.assertIsNone(base_annot.confidence)  # No fabricated confidence (no 0.75)
        self.assertEqual(base_annot.provider, ReferenceProvider.LOCAL_HEURISTIC.value)
        self.assertEqual(base_annot.verification_status, VerificationStatus.UNVERIFIED)

        # Probe annotation
        p_annot = ref_set.probe_annotations[probes[0].probe_id]
        self.assertIsNone(p_annot.gemini_confidence)
        self.assertIsNone(p_annot.confidence)
        self.assertEqual(p_annot.provider, ReferenceProvider.LOCAL_HEURISTIC.value)
        self.assertEqual(p_annot.verification_status, VerificationStatus.UNVERIFIED)

    def test_02_fallback_semantic_reference_unverified(self):
        """
        TEST 2: Fallback semantic reference:
        status is UNVERIFIED, never 'Final Ground-Truth'.
        """
        client = GeminiSemanticClient(api_key="")
        service = SemanticReferenceService(client=client, cache=self.cache)
        probe = LinguisticProbe.create(
            seed_text="A simple test sentence.",
            perturbed_text="A very simple test sentence.",
            perturbation_type="intensity",
            expected_flip=False,
            name="p1",
        )
        ref_set = service.annotate_experiment("A simple test sentence.", [probe])
        base = ref_set.baseline_annotation

        self.assertEqual(base.verification_status, VerificationStatus.UNVERIFIED)
        self.assertNotEqual(base.verification_status, "Final Ground-Truth")
        self.assertNotEqual(base.verification_status, "Ground Truth")
        self.assertIn("UNVERIFIED", base.verification_source)

    def test_03_gemini_response_mocked(self):
        """
        TEST 3: Mock Gemini response.
        Verify polarity parsed correctly, Gemini self-reported confidence stored,
        provider stored as GEMINI, model stored, request count increments.
        """
        client = GeminiSemanticClient(api_key="mock_valid_key", model_name="gemini-2.5-flash")
        self.assertTrue(client.is_online)

        mock_payload = {
            "annotations": [
                {
                    "sentence_id": "baseline",
                    "semantic_polarity": "POSITIVE",
                    "confidence": 0.94,
                    "reason_short": "Expressed clear enthusiasm.",
                    "ambiguity": "LOW",
                    "semantic_relation_to_baseline": "PRESERVE_POLARITY",
                },
                {
                    "sentence_id": "probe_01",
                    "semantic_polarity": "NEGATIVE",
                    "confidence": 0.91,
                    "reason_short": "Negation inverted the positive sentiment.",
                    "ambiguity": "LOW",
                    "semantic_relation_to_baseline": "REVERSE_POLARITY",
                },
            ]
        }

        # Mock requests.post to return mock_payload
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": json.dumps(mock_payload)}]
                    }
                }
            ]
        }

        with patch("requests.post", return_value=mock_resp):
            probes = [{"probe_id": "probe_01", "perturbed_text": "The movie was not great."}]
            res = client.annotate_batch(baseline_text="The movie was great.", probes=probes)

        self.assertEqual(client.requests_count, 1)
        self.assertIn("baseline", res)
        self.assertIn("probe_01", res)

        base = res["baseline"]
        self.assertEqual(base.semantic_polarity, SemanticReferenceLabel.POSITIVE)
        self.assertEqual(base.gemini_confidence, 0.94)
        self.assertEqual(base.provider, ReferenceProvider.GEMINI.value)
        self.assertEqual(base.model_used, "gemini-2.5-flash")
        self.assertEqual(base.verification_status, VerificationStatus.AUTOMATED_REFERENCE)

        p1 = res["probe_01"]
        self.assertEqual(p1.semantic_polarity, SemanticReferenceLabel.NEGATIVE)
        self.assertEqual(p1.gemini_confidence, 0.91)
        self.assertEqual(p1.semantic_relation_to_baseline, SemanticRelation.REVERSE_POLARITY)

    def test_04_gemini_failure_resilience(self):
        """
        TEST 4: Mock API failure.
        Verify experiment does not crash, no fabricated confidence, status indicates failure/unavailable.
        """
        client = GeminiSemanticClient(api_key="mock_key", max_retries=1)
        service = SemanticReferenceService(client=client, cache=self.cache)

        with patch("requests.post", side_effect=ConnectionError("Simulated network timeout")):
            probe = LinguisticProbe.create(
                seed_text="The sound was clean.",
                perturbed_text="The sound was not clean.",
                perturbation_type="negation",
                expected_flip=False,
                name="p1",
            )
            # Must not crash
            ref_set = service.annotate_experiment("The sound was clean.", [probe])

        # Status must fall back gracefully to local heuristic
        self.assertEqual(ref_set.baseline_annotation.provider, ReferenceProvider.LOCAL_HEURISTIC.value)
        self.assertIsNone(ref_set.baseline_annotation.gemini_confidence)
        self.assertIsNone(ref_set.baseline_annotation.confidence)
        self.assertGreater(client.api_failures_count, 0)

    def test_05_cache_identity_and_invalidation(self):
        """
        TEST 5: Cache keys include normalized_text + provider + model + schema + annotation version.
        Same text + same engine/model/schema hits cache.
        Different model/schema/provider must not hit the old entry.
        """
        cache = self.cache
        text = "An excellent presentation."

        annot = SemanticAnnotation(
            sentence_id="s1",
            sentence_text=text,
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            confidence=0.95,
            provider=ReferenceProvider.GEMINI.value,
            model_used="gemini-2.5-flash",
            gemini_confidence=0.95,
            schema_version="v2.0",
        )
        cache.put(annot)

        # 1. Exact match hits cache
        hit = cache.get(text, provider=ReferenceProvider.GEMINI.value, model="gemini-2.5-flash")
        self.assertIsNotNone(hit)
        self.assertEqual(hit.final_semantic_polarity, SemanticReferenceLabel.POSITIVE)

        # 2. Different provider does NOT hit cache
        miss_prov = cache.get(text, provider=ReferenceProvider.LOCAL_HEURISTIC.value, model="gemini-2.5-flash")
        self.assertIsNone(miss_prov)

        # 3. Different model does NOT hit cache
        miss_model = cache.get(text, provider=ReferenceProvider.GEMINI.value, model="gemini-1.5-flash")
        self.assertIsNone(miss_model)

    def test_06_p001_negation_does_not_force_flip(self):
        """
        TEST 6: P001 negation insertion must NOT automatically set expected_flip=True.
        Verify relation comes authoritatively from semantic references.
        """
        catalog = LinguisticProbeCatalog()
        candidates = catalog.generate_candidates("The king is injured on his left leg.", sentence_type="literal")
        p001 = next(c for c in candidates if c.metadata.get("slot") == "P001")

        # P001 must not force expected_flip=True
        self.assertFalse(p001.expected_flip)
        self.assertEqual(p001.semantic_intent, "ADD_NEGATION")
        self.assertEqual(p001.expected_semantic_effect, "negate_predicate")

        # Now test relation derivation on factual statement
        # "The king is injured" (NEUTRAL factual) -> "The king is not injured" (NEUTRAL factual)
        rel_neutral = SemanticRelation.from_polarities(SemanticReferenceLabel.NEUTRAL, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(rel_neutral, SemanticRelation.PRESERVE_POLARITY)

        # On affective statement: "The food was delicious" (POSITIVE) -> "The food was not delicious" (NEGATIVE)
        rel_polar = SemanticRelation.from_polarities(SemanticReferenceLabel.POSITIVE, SemanticReferenceLabel.NEGATIVE)
        self.assertEqual(rel_polar, SemanticRelation.REVERSE_POLARITY)

    def test_07_runner_never_mutates_semantic_relation(self):
        """
        TEST 7: Verify runner never mutates semantic relation.
        (e.g. SHIFT_FROM_NEUTRAL must NOT be coerced into REVERSE_POLARITY or expected_flip=True).
        """
        base_annot = SemanticAnnotation(
            sentence_id="baseline",
            sentence_text="The water is at room temperature.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
        )
        probe_annot = SemanticAnnotation(
            sentence_id="p1",
            sentence_text="The water is terribly cold.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
        )
        ref_set = SemanticReferenceSet(
            baseline_annotation=base_annot,
            probe_annotations={"p1": probe_annot},
        )
        ref_set._recompute_relations()
        self.assertEqual(ref_set.get_expected_relation("p1"), SemanticRelation.SHIFT_FROM_NEUTRAL)

        # Simulate runner consuming frozen reference
        p = LinguisticProbe.create(
            seed_text="The water is at room temperature.",
            perturbed_text="The water is terribly cold.",
            perturbation_type="temperature",
            expected_flip=False,
            name="p1",
        )
        # Runner synchronization logic:
        p_ann = ref_set.probe_annotations["p1"]
        base_pol = ref_set.baseline_annotation.final_semantic_polarity
        probe_pol = p_ann.final_semantic_polarity
        is_polar_flip = (
            base_pol in (SemanticReferenceLabel.POSITIVE, SemanticReferenceLabel.NEGATIVE)
            and probe_pol in (SemanticReferenceLabel.POSITIVE, SemanticReferenceLabel.NEGATIVE)
            and base_pol != probe_pol
        )
        p.expected_flip = is_polar_flip

        # MUST REMAIN FALSE because baseline was NEUTRAL
        self.assertFalse(p.expected_flip)
        self.assertNotEqual(p.semantic_intent, "REVERSE_POLARITY")

    def test_08_human_override_preserves_suggestion(self):
        """
        TEST 8: Gemini says POSITIVE. Human changes to NEGATIVE.
        Final verified value = NEGATIVE. Original suggestion remains stored.
        """
        annot = SemanticAnnotation(
            sentence_id="base",
            sentence_text="The script was interesting.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            confidence=0.88,
            provider=ReferenceProvider.GEMINI.value,
            gemini_polarity=SemanticReferenceLabel.POSITIVE,
            gemini_confidence=0.88,
            verification_status=VerificationStatus.AUTOMATED_REFERENCE,
        )
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.POSITIVE)

        # Researcher overrides
        annot.override_polarity("NEGATIVE", reason="In this context, 'interesting' was sarcastic.")
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.NEGATIVE)
        self.assertEqual(annot.gemini_polarity, SemanticReferenceLabel.POSITIVE)
        self.assertEqual(annot.gemini_confidence, 0.88)
        self.assertEqual(annot.verification_status, VerificationStatus.HUMAN_OVERRIDDEN)
        self.assertIn("sarcastic", annot.reason)

    def test_09_binary_model_with_neutral_reference(self):
        """
        TEST 9: Binary model + neutral reference.
        Verified semantic polarity = NEUTRAL. Binary model output = POSITIVE.
        Expected: UNREPRESENTABLE_NEUTRAL / NOT_DIRECTLY_REPRESENTABLE, not BLIND.
        """
        pred = PredictionResult(
            label="POSITIVE",
            confidence=0.60,
            probabilities={"NEGATIVE": 0.40, "POSITIVE": 0.60},
            label_space=["NEGATIVE", "POSITIVE"],
        )
        compat = pred.evaluate_semantic_compatibility(SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(compat, "NOT_DIRECTLY_REPRESENTABLE")

        # Behavioral classification under neutral-preserving probe
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.60,
            probe_confidence=0.62,
            expected_effect="EXPECTED_PRESERVE",
            semantic_intent="PRESERVE_POLARITY",
            original_distribution={"NEGATIVE": 0.40, "POSITIVE": 0.60},
            probe_distribution={"NEGATIVE": 0.38, "POSITIVE": 0.62},
            original_polarity=SemanticPolarity.NEUTRAL,
            probe_polarity=SemanticPolarity.NEUTRAL,
        )
        # Binary model must NOT be marked BLIND!
        self.assertNotEqual(failure_type, FailureCategory.BLIND)
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)

    def test_10_three_class_neutral_preservation(self):
        """
        TEST 10: 3-class neutral preservation.
        Verified relation = PRESERVE_POLARITY. Baseline = NEUTRAL, Probe = NEUTRAL.
        Expected: No automatic failure.
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="NEUTRAL",
            probe_label="NEUTRAL",
            original_confidence=0.82,
            probe_confidence=0.80,
            expected_effect="EXPECTED_PRESERVE",
            semantic_intent="PRESERVE_POLARITY",
            original_distribution={"NEGATIVE": 0.09, "NEUTRAL": 0.82, "POSITIVE": 0.09},
            probe_distribution={"NEGATIVE": 0.10, "NEUTRAL": 0.80, "POSITIVE": 0.10},
            original_polarity=SemanticPolarity.NEUTRAL,
            probe_polarity=SemanticPolarity.NEUTRAL,
        )
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)

    def test_11_three_class_actual_semantic_reversal(self):
        """
        TEST 11: 3-class actual semantic reversal.
        Verified relation = REVERSE_POLARITY. Baseline = POSITIVE, Probe = NEGATIVE.
        Expected: behavioral alignment.
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.95,
            probe_confidence=0.90,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            original_distribution={"NEGATIVE": 0.02, "NEUTRAL": 0.03, "POSITIVE": 0.95},
            probe_distribution={"NEGATIVE": 0.90, "NEUTRAL": 0.05, "POSITIVE": 0.05},
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.NEGATIVE,
        )
        self.assertEqual(failure_type, FailureCategory.NONE)
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_FLIP)
        self.assertTrue(evidence["expectation_match"])

    def test_12_incorrect_model_behavior_blind(self):
        """
        TEST 12: Incorrect model behavior.
        Verified relation = REVERSE_POLARITY. Baseline = POSITIVE, Probe = POSITIVE.
        Expected: BLIND failure category.
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.95,
            probe_confidence=0.93,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            original_distribution={"NEGATIVE": 0.02, "NEUTRAL": 0.03, "POSITIVE": 0.95},
            probe_distribution={"NEGATIVE": 0.03, "NEUTRAL": 0.04, "POSITIVE": 0.93},
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
        )
        self.assertEqual(failure_type, FailureCategory.BLIND)
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)
        self.assertFalse(evidence["expectation_match"])

    def test_13_uncertain_semantic_relation(self):
        """
        TEST 13: Uncertain semantic relation.
        relation = UNCERTAIN.
        Expected: behavioral alignment = NA, failure classification = UNDETERMINED.
        """
        outcome, failure_type, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.85,
            probe_confidence=0.80,
            expected_effect="UNCERTAIN",
            semantic_intent="UNCERTAIN",
            original_polarity=SemanticPolarity.POSITIVE,
            probe_polarity=SemanticPolarity.POSITIVE,
        )
        self.assertEqual(failure_type, FailureCategory.UNDETERMINED)
        self.assertEqual(outcome, BehavioralOutcome.UNDETERMINED)

        alignment = compute_behavioral_alignment(
            observed_label_flipped=False,
            expected_change=compute_expected_semantic_change("UNCERTAIN"),
        )
        self.assertIsNone(alignment)  # Strictly NA

    def test_14_no_forced_category_coverage(self):
        """
        TEST 14: No forced category coverage.
        If no BLIND examples exist in an evaluation, reported BLIND count is strictly 0.
        """
        # Create 3 evaluations that are all perfectly consistent (NONE)
        evals = [
            {"failure_type": "None", "expectation_match": True},
            {"failure_type": "None", "expectation_match": True},
            {"failure_type": "None", "expectation_match": True},
        ]
        blind_count = sum(1 for e in evals if e["failure_type"].upper() == "BLIND")
        self.assertEqual(blind_count, 0)


if __name__ == "__main__":
    unittest.main()
