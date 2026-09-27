"""
Tests for BlindSpot Canonical Semantic Reference Layer (Section 31).
Verifies:
1. Gemini output: POSITIVE accepted.
2. Gemini output: NEGATIVE accepted.
3. Gemini output: NEUTRAL accepted.
4. Gemini output: MIXED rejected.
5. Human overrides: Gemini = NEGATIVE, Human = POSITIVE, Final: POSITIVE.
6. Binary model + NEUTRAL reference (verify reference remains NEUTRAL, compatibility is NOT_DIRECTLY_REPRESENTABLE).
7. Three-class model + NEUTRAL reference (verify direct compatibility).
8. Positive -> negative negation (Expected relation: REVERSE).
9. Positive -> positive synonym (Expected relation: PRESERVE).
10. Gemini cannot create a failure taxonomy (rule-based engine isolation).
11. Semantic cache prevents duplicate API requests.
12. Offline/manual semantic annotation works.
13. Human override survives experiment persistence/reload.
14. Frozen semantic reference is identical across all benchmark models.
"""
import unittest
import os
import json
import tempfile
import shutil

from blindspot.semantic.types import (
    SemanticReferenceLabel,
    SemanticRelation,
    VerificationStatus,
    SemanticAnnotation,
    SemanticReferenceSet,
)
from blindspot.semantic.cache import SemanticAnnotationCache
from blindspot.semantic.client import GeminiSemanticClient
from blindspot.semantic.service import SemanticReferenceService
from blindspot.core.types import (
    LinguisticProbe,
    SharedProbeSet,
    PredictionResult,
    ModelProbeEvaluation,
)
from blindspot.storage.run_store import RunStore
from blindspot.testing.behavioral import BehavioralTester


class TestSemanticReferenceLayer(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.tmp_dir, "test_cache.json")
        self.cache = SemanticAnnotationCache(cache_path=self.cache_file)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_01_gemini_positive_accepted(self):
        """Test 1: Gemini output POSITIVE is accepted into canonical label space."""
        annot = SemanticAnnotation(
            sentence_id="base",
            sentence_text="The movie was fantastic.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            confidence=0.98,
        )
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.POSITIVE)
        self.assertIn(annot.final_semantic_polarity.value, ["POSITIVE", "NEGATIVE", "NEUTRAL"])

    def test_02_gemini_negative_accepted(self):
        """Test 2: Gemini output NEGATIVE is accepted into canonical label space."""
        annot = SemanticAnnotation(
            sentence_id="probe_1",
            sentence_text="The movie was terrible.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            confidence=0.95,
        )
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.NEGATIVE)
        self.assertIn(annot.final_semantic_polarity.value, ["POSITIVE", "NEGATIVE", "NEUTRAL"])

    def test_03_gemini_neutral_accepted(self):
        """Test 3: Gemini output NEUTRAL is accepted into canonical label space."""
        annot = SemanticAnnotation(
            sentence_id="probe_2",
            sentence_text="The movie was released on Friday.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            confidence=0.91,
        )
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertIn(annot.final_semantic_polarity.value, ["POSITIVE", "NEGATIVE", "NEUTRAL"])

    def test_04_gemini_mixed_rejected(self):
        """Test 4: Non-canonical label like MIXED must be rejected rather than silently transformed."""
        with self.assertRaises((ValueError, KeyError)):
            SemanticReferenceLabel("MIXED")

        # Client parsing validation rejecting invalid labels
        client = GeminiSemanticClient(api_key="mock_key")
        invalid_json = '{"sentence_id": "test", "semantic_polarity": "MIXED", "confidence": 0.8}'
        with self.assertRaises(ValueError):
            client._parse_structured_response(invalid_json)

    def test_05_human_override(self):
        """Test 5: Human overrides Gemini = NEGATIVE with Human = POSITIVE -> Final = POSITIVE."""
        annot = SemanticAnnotation(
            sentence_id="base",
            sentence_text="The movie was okay.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            confidence=0.60,
            gemini_polarity=SemanticReferenceLabel.NEGATIVE,
            gemini_confidence=0.60,
            verification_status=VerificationStatus.GEMINI_VERIFIED,
            verification_source="GEMINI",
        )
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.NEGATIVE)

        # Human override
        annot.override_human("POSITIVE")
        self.assertEqual(annot.final_semantic_polarity, SemanticReferenceLabel.POSITIVE)
        self.assertEqual(annot.human_verified_polarity, SemanticReferenceLabel.POSITIVE)
        self.assertEqual(annot.verification_status, VerificationStatus.HUMAN_OVERRIDDEN)
        self.assertEqual(annot.verification_source, "HUMAN_OVERRIDE")

    def test_06_binary_model_with_neutral_reference(self):
        """
        Test 6: Binary model + NEUTRAL reference.
        Verify that reference remains NEUTRAL, never rewritten as POSITIVE/NEGATIVE,
        and compatibility is recorded as NOT_DIRECTLY_REPRESENTABLE.
        """
        base_ref = SemanticAnnotation(
            sentence_id="baseline",
            sentence_text="The movie was released on Friday.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            confidence=0.95,
        )
        # Binary model outputs POSITIVE 55%
        pred = PredictionResult(
            label="POSITIVE",
            confidence=0.55,
            probabilities={"NEGATIVE": 0.45, "POSITIVE": 0.55},
            label_space=["NEGATIVE", "POSITIVE"],
            predicted_label="POSITIVE",
        )
        compat = pred.evaluate_semantic_compatibility(base_ref.final_semantic_polarity)

        # Invariant 1: Semantic reference must remain NEUTRAL
        self.assertEqual(base_ref.final_semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        # Invariant 2: Binary model cannot represent NEUTRAL
        self.assertEqual(compat, "NOT_DIRECTLY_REPRESENTABLE")

    def test_07_three_class_model_with_neutral_reference(self):
        """Test 7: Three-class model + NEUTRAL reference. Verify direct compatibility."""
        base_ref = SemanticAnnotation(
            sentence_id="baseline",
            sentence_text="The movie was released on Friday.",
            semantic_polarity=SemanticReferenceLabel.NEUTRAL,
            confidence=0.95,
        )
        # 3-class model outputs NEUTRAL 78%
        pred = PredictionResult(
            label="NEUTRAL",
            confidence=0.78,
            probabilities={"NEGATIVE": 0.10, "NEUTRAL": 0.78, "POSITIVE": 0.12},
            label_space=["NEGATIVE", "NEUTRAL", "POSITIVE"],
            predicted_label="NEUTRAL",
        )
        compat = pred.evaluate_semantic_compatibility(base_ref.final_semantic_polarity)
        self.assertEqual(compat, "DIRECTLY_COMPATIBLE")

    def test_08_positive_to_negative_negation_relation(self):
        """Test 8: Positive -> negative negation: Expected relation = REVERSE."""
        base_annot = SemanticAnnotation(
            sentence_id="baseline",
            sentence_text="The movie was excellent.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            confidence=0.98,
        )
        probe_annot = SemanticAnnotation(
            sentence_id="probe_1",
            sentence_text="The movie was not excellent.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            confidence=0.96,
        )
        ref_set = SemanticReferenceSet(
            baseline_annotation=base_annot,
            probe_annotations={"probe_1": probe_annot},
        )
        rel = ref_set.get_expected_relation("probe_1")
        self.assertEqual(rel, SemanticRelation.REVERSE)

    def test_09_positive_to_positive_synonym_relation(self):
        """Test 9: Positive -> positive synonym: Expected relation = PRESERVE."""
        base_annot = SemanticAnnotation(
            sentence_id="baseline",
            sentence_text="The movie was excellent.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            confidence=0.98,
        )
        probe_annot = SemanticAnnotation(
            sentence_id="probe_syn",
            sentence_text="The movie was outstanding.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            confidence=0.97,
        )
        ref_set = SemanticReferenceSet(
            baseline_annotation=base_annot,
            probe_annotations={"probe_syn": probe_annot},
        )
        rel = ref_set.get_expected_relation("probe_syn")
        self.assertEqual(rel, SemanticRelation.PRESERVE)

    def test_10_gemini_cannot_create_failure_taxonomy(self):
        """
        Test 10: Verify Gemini structured output and semantic module contains ZERO
        taxonomy logic. Failure taxonomy must be strictly rule-based and derived from
        benchmark models' empirical outputs.
        """
        client = GeminiSemanticClient(api_key="mock_key")
        schema = client._get_structured_schema()
        # Ensure schema properties only govern semantic annotation, not taxonomy
        props = schema["properties"]["annotations"]["items"]["properties"]
        self.assertIn("semantic_polarity", props)
        self.assertIn("semantic_relation_to_baseline", props)
        self.assertNotIn("failure_category", props)
        self.assertNotIn("predicted_failure", props)
        self.assertNotIn("taxonomy", props)

    def test_11_semantic_cache_prevents_duplicate_requests(self):
        """Test 11: Verify semantic cache prevents duplicate API requests for identical sentences."""
        cache = self.cache
        sentence = "The food was wonderfully prepared."
        key = cache.make_key(sentence)

        self.assertIsNone(cache.get(sentence))

        annot = SemanticAnnotation(
            sentence_id="s1",
            sentence_text=sentence,
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            confidence=0.96,
            model_used="gemini-2.5-flash",
        )
        cache.put(annot)

        # Persistent retrieval
        cached = cache.get(sentence)
        self.assertIsNotNone(cached)
        self.assertEqual(cached.final_semantic_polarity, SemanticReferenceLabel.POSITIVE)
        self.assertEqual(cached.confidence, 0.96)

        # New cache instance from same file
        reloaded_cache = SemanticAnnotationCache(cache_path=self.cache_file)
        self.assertTrue(reloaded_cache.has(sentence))
        self.assertEqual(reloaded_cache.get(sentence).final_semantic_polarity, SemanticReferenceLabel.POSITIVE)

    def test_12_offline_manual_annotation(self):
        """Test 12: Verify offline/manual semantic annotation works when Gemini API is unavailable."""
        offline_client = GeminiSemanticClient(api_key="")
        self.assertFalse(offline_client.is_online)

        service = SemanticReferenceService(client=offline_client, cache=self.cache)
        probe = LinguisticProbe.create(
            seed_text="The movie was great.",
            perturbed_text="The movie was not great.",
            perturbation_type="negation",
            expected_flip=True,
        )
        probes = [probe]
        ref_set = service.annotate_experiment("The movie was great.", probes)
        self.assertIn(ref_set.annotation_engine, ("manual", "local_heuristic"))
        self.assertIsNotNone(ref_set.baseline_annotation)
        self.assertIn(ref_set.baseline_annotation.verification_status, (VerificationStatus.MANUAL, VerificationStatus.UNVERIFIED))
        self.assertEqual(ref_set.baseline_annotation.final_semantic_polarity, SemanticReferenceLabel.POSITIVE)
        self.assertIn(probe.probe_id, ref_set.probe_annotations)
        self.assertEqual(ref_set.probe_annotations[probe.probe_id].final_semantic_polarity, SemanticReferenceLabel.NEGATIVE)
        self.assertEqual(ref_set.get_expected_relation(probe.probe_id), SemanticRelation.REVERSE)

    def test_13_human_override_survives_persistence_and_reload(self):
        """Test 13: Verify human override survives experiment persistence/reload."""
        store = RunStore(base_dir=self.tmp_dir)
        exp_id = "exp_test_override"

        base_annot = SemanticAnnotation(
            sentence_id="baseline",
            sentence_text="The acting was modest.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            confidence=0.70,
        )
        # Override to NEUTRAL
        base_annot.override_human("NEUTRAL")

        probe_annot = SemanticAnnotation(
            sentence_id="p_001",
            sentence_text="The acting was very modest.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            confidence=0.75,
        )
        ref_set = SemanticReferenceSet(
            baseline_annotation=base_annot,
            probe_annotations={"p_001": probe_annot},
            frozen=True,
        )
        saved_path = store.save_semantic_reference(exp_id, ref_set)
        self.assertTrue(os.path.exists(saved_path))

        loaded_data = store.load_semantic_reference(exp_id)
        self.assertIsNotNone(loaded_data)
        reloaded_set = SemanticReferenceSet.from_dict(loaded_data)

        self.assertEqual(reloaded_set.baseline_annotation.final_semantic_polarity, SemanticReferenceLabel.NEUTRAL)
        self.assertEqual(reloaded_set.baseline_annotation.verification_source, "HUMAN_OVERRIDE")
        self.assertTrue(reloaded_set.frozen)

    def test_14_frozen_reference_identical_across_benchmark_models(self):
        """
        Test 14: Verify the frozen semantic reference is identical across all benchmark models
        and cannot be altered by model execution.
        """
        base_annot = SemanticAnnotation(
            sentence_id="baseline",
            sentence_text="The experience was unforgettable.",
            semantic_polarity=SemanticReferenceLabel.POSITIVE,
            confidence=0.99,
        )
        p1 = SemanticAnnotation(
            sentence_id="probe_1",
            sentence_text="The experience was not unforgettable.",
            semantic_polarity=SemanticReferenceLabel.NEGATIVE,
            confidence=0.95,
        )
        ref_set = SemanticReferenceSet(
            baseline_annotation=base_annot,
            probe_annotations={"probe_1": p1},
            frozen=False,
        )
        ref_set.freeze()
        self.assertTrue(ref_set.frozen)

        # Frozen set blocks modification
        with self.assertRaises(RuntimeError):
            ref_set.override_baseline("NEGATIVE")

        with self.assertRaises(RuntimeError):
            ref_set.override_probe("probe_1", "POSITIVE")

        # Simulate 5 models receiving this exact same reference
        five_model_ids = [
            "distilbert-base-uncased-finetuned-sst-2-english",
            "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "siebert/sentiment-roberta-large-english",
            "finiteautomata/bertweet-base-sentiment-analysis",
            "ProsusAI/finbert",
        ]
        assigned_refs = {m: ref_set for m in five_model_ids}

        # Verify exact identity and consistency
        first_ref = assigned_refs[five_model_ids[0]]
        for m in five_model_ids[1:]:
            self.assertIs(assigned_refs[m], first_ref)
            self.assertEqual(assigned_refs[m].baseline_annotation.final_semantic_polarity, SemanticReferenceLabel.POSITIVE)
            self.assertEqual(assigned_refs[m].get_expected_relation("probe_1"), SemanticRelation.REVERSE)


if __name__ == "__main__":
    unittest.main()
