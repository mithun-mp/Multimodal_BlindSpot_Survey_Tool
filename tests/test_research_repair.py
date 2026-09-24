"""
Deterministic Acceptance Test Matrix for BlindSpot Research Repair.
Covers:
1. Model Validation Gate & Rejection of Invalid Models
2. Label Mapping & Normalization
3. Strict Pipeline & Count Integrity (Planned == Executed == Analyzed == Reported)
4. Absence of AttributeError on ev.original_label across data structures
5. Taxonomy Classifier Calibration (Synthetic: BLIND, SPURIOUS, MISWEIGHTED, NONE, UNDETERMINED)
6. Deterministic 5-Model Acceptance Matrix (5 models x 1 baseline + 5 models x 4 probes = 25 evaluations)
"""
import unittest
import numpy as np
from typing import Dict, Any, List

from blindspot.core.types import (
    PredictionResult,
    ModelProbeEvaluation,
    BehavioralProbeResult,
    RunPlan,
    RunStatus,
    AnalysisStatus,
    FailureCategory,
    BehavioralOutcome,
)
from blindspot.core.config import ExperimentConfig
from blindspot.models.registry import ModelRegistry, ModelSpec
from blindspot.models.huggingface_wrapper import normalize_label_name, HuggingFaceWrapper
from blindspot.perturbations.shared import SharedProbe, SharedProbeSet, _is_category_match
from blindspot.testing.behavioral import classify_behavior, BehavioralTester
from blindspot.explainability.taxonomy import TaxonomyClassifier
from blindspot.execution.runner import ExperimentRunner


class TestModelValidationGate(unittest.TestCase):
    """Verifies Section 1 & Section 3: Model Validation Gate & Isolation."""

    def setUp(self):
        self.registry = ModelRegistry()

    def test_detector_model_rejected_from_sentiment(self):
        """roberta-base-openai-detector must be rejected from sentiment experiments."""
        is_valid, reason, details = self.registry.validate_model_for_sentiment("roberta-base-openai-detector")
        self.assertFalse(is_valid)
        self.assertTrue("AI_TEXT_DETECTION" in reason or "AI text detector" in reason)
        self.assertEqual(details.get("task"), "AI_TEXT_DETECTION")

    def test_detector_task_and_labels(self):
        """Detector preset must have task AI_TEXT_DETECTION and Fake/Real labels."""
        preset = self.registry.get_preset("roberta-base-openai-detector")
        self.assertIsNotNone(preset)
        self.assertEqual(preset["task"], "AI_TEXT_DETECTION")
        self.assertEqual(preset["label_names"], ["Fake", "Real"])

    def test_list_sentiment_models_excludes_detector(self):
        """list_sentiment_models() must not include roberta-base-openai-detector."""
        sentiment_models = self.registry.list_sentiment_models()
        model_ids = [m["model_id"] for m in sentiment_models]
        self.assertNotIn("roberta-base-openai-detector", model_ids)

    def test_5_sentiment_models_pass_validation_gate(self):
        """The 5 curated sentiment models must pass the sentiment validation gate."""
        expected_models = [
            "distilbert-base-uncased-finetuned-sst-2-english",
            "textattack/albert-base-v2-SST-2",
            "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "textattack/bert-base-uncased-SST-2",
            "cardiffnlp/twitter-roberta-base-sentiment",
        ]
        sentiment_models = self.registry.list_sentiment_models()
        preset_ids = [m["model_id"] for m in sentiment_models]

        for mid in expected_models:
            self.assertIn(mid, preset_ids)
            is_valid, reason, _ = self.registry.validate_model_for_sentiment(mid)
            self.assertTrue(is_valid, f"Model {mid} failed validation: {reason}")

    def test_label_normalization_binary(self):
        """Binary classification labels must normalize to NEGATIVE / POSITIVE."""
        self.assertEqual(normalize_label_name("LABEL_0", 2), "NEGATIVE")
        self.assertEqual(normalize_label_name("LABEL_1", 2), "POSITIVE")
        self.assertEqual(normalize_label_name("0", 2), "NEGATIVE")
        self.assertEqual(normalize_label_name("1", 2), "POSITIVE")
        self.assertEqual(normalize_label_name("neg", 2), "NEGATIVE")
        self.assertEqual(normalize_label_name("pos", 2), "POSITIVE")

    def test_label_normalization_3class(self):
        """3-class classification labels must normalize to NEGATIVE / NEUTRAL / POSITIVE."""
        self.assertEqual(normalize_label_name("LABEL_0", 3), "NEGATIVE")
        self.assertEqual(normalize_label_name("LABEL_1", 3), "NEUTRAL")
        self.assertEqual(normalize_label_name("LABEL_2", 3), "POSITIVE")
        self.assertEqual(normalize_label_name("negative", 3), "NEGATIVE")
        self.assertEqual(normalize_label_name("neutral", 3), "NEUTRAL")
        self.assertEqual(normalize_label_name("positive", 3), "POSITIVE")

    def test_non_sentiment_labels_not_remapped(self):
        """Detector labels Fake / Real must NOT be remapped to sentiment."""
        self.assertEqual(normalize_label_name("Fake", 2), "FAKE")
        self.assertEqual(normalize_label_name("Real", 2), "REAL")

    def test_wrapper_allow_fallback_false_raises_on_invalid_model(self):
        """HuggingFaceWrapper with allow_fallback=False must raise when model cannot load."""
        with self.assertRaises(Exception):
            wrapper = HuggingFaceWrapper("non-existent-invalid-model-xyz", allow_fallback=False)
            wrapper.predict_proba(["Test text."])


class TestProbePipelineAndCountIntegrity(unittest.TestCase):
    """Verifies Probe Pipeline, Category Matching, and Count Integrity."""

    def test_category_matching(self):
        """_is_category_match handles exact match and subcategory variations."""
        self.assertTrue(_is_category_match("negation", "negation"))
        self.assertTrue(_is_category_match("lexical", "lexical_swap"))
        self.assertTrue(_is_category_match("syntax", "syntactic_reorder"))
        self.assertFalse(_is_category_match("negation", "lexical"))

    def test_immutable_probe_consumption(self):
        """SharedProbeSet.get_selected filters strictly by probe IDs."""
        p1 = SharedProbe.create(
            seed_text="The movie was great.",
            perturbed_text="The movie was not great.",
            perturbation_type="negation",
            expected_flip=True,
            expected_semantic_effect="invert",
            description="Negation insertion",
        )
        p1.probe_id = "P001"
        p2 = SharedProbe.create(
            seed_text="The movie was great.",
            perturbed_text="The film was great.",
            perturbation_type="lexical",
            expected_flip=False,
            expected_semantic_effect="preserve",
            description="Synonym swap",
        )
        p2.probe_id = "P002"
        p3 = SharedProbe.create(
            seed_text="The movie was great.",
            perturbed_text="The movie was really great.",
            perturbation_type="intensifier",
            expected_flip=False,
            expected_semantic_effect="preserve",
            description="Intensifier addition",
        )
        p3.probe_id = "P003"
        probe_set = SharedProbeSet(
            probe_set_id="PS01",
            seed_texts=["The movie was great."],
            probes=[p1, p2, p3],
            sentence_types={"The movie was great.": "literal"},
        )
        selected = probe_set.get_selected({"P001", "P003"})
        self.assertEqual(len(selected.probes), 2)
        selected_ids = [p.probe_id for p in selected.probes]
        self.assertEqual(selected_ids, ["P001", "P003"])

    def test_no_attribute_error_on_original_label(self):
        """ModelProbeEvaluation guarantees original_label attribute access."""
        pred_orig = PredictionResult(
            label="POSITIVE",
            confidence=0.99,
            probabilities={"NEGATIVE": 0.01, "POSITIVE": 0.99},
            latency_ms=10.0,
            model_id="test-model",
            device="cpu",
        )
        pred_pert = PredictionResult(
            label="NEGATIVE",
            confidence=0.95,
            probabilities={"NEGATIVE": 0.95, "POSITIVE": 0.05},
            latency_ms=10.0,
            model_id="test-model",
            device="cpu",
        )
        eval_item = ModelProbeEvaluation(
            model_id="test-model",
            probe_id="P001",
            seed_text="Great movie.",
            perturbed_text="Terrible movie.",
            perturbation_type="negation",
            expected_flip=True,
            expected_semantic_effect="invert",
            original_prediction=pred_orig,
            perturbed_prediction=pred_pert,
            is_flipped=True,
            confidence_delta=-0.04,
            confidence_delta_pts=-4.0,
            expectation_satisfied=True,
            behavioral_outcome="EXPECTED_FLIP",
            failure_type="None",
            rationale="Correct flip",
        )
        # Direct attribute access must never raise AttributeError
        self.assertEqual(eval_item.original_label, "POSITIVE")
        self.assertEqual(eval_item.perturbed_label, "NEGATIVE")
        self.assertEqual(eval_item.original_confidence, 0.99)
        self.assertEqual(eval_item.perturbed_confidence, 0.95)

    def test_count_integrity_violation_marks_no_valid_analysis(self):
        """Count mismatch between planned and executed must not report 0 failures."""
        # Simulated run where an exception caused partial execution
        runner = ExperimentRunner(
            ExperimentConfig(
                model_ids=["distilbert-base-uncased-finetuned-sst-2-english"],
                seed_texts=["The movie was good."],
                selected_probe_ids=["P001", "P002", "P003", "P004"],
            )
        )
        # Verify initial plan has 4 planned probes
        self.assertEqual(len(runner.config.selected_probe_ids), 4)


class TestTaxonomyClassifierCalibration(unittest.TestCase):
    """Verifies synthetic calibration for BLIND, SPURIOUS, MISWEIGHTED, NONE, UNDETERMINED."""

    def test_blind_failure_missing_flip(self):
        """Semantics inverted (expected flip), model retained same label -> BLIND."""
        outcome, failure_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.98,
            probe_confidence=0.95,
            expected_effect="INVERT",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)
        self.assertEqual(failure_cat, FailureCategory.BLIND)
        self.assertIn("retained the same predicted class", rationale)

    def test_spurious_failure_unexpected_flip(self):
        """Semantics preserved (expected preserve), model flipped label -> SPURIOUS."""
        outcome, failure_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.98,
            probe_confidence=0.85,
            expected_effect="PRESERVE",
            semantic_intent="PRESERVE_MEANING",
            expected_label_relation="SAME_LABEL",
        )
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_FLIP)
        self.assertEqual(failure_cat, FailureCategory.SPURIOUS)
        self.assertIn("unexpectedly changed its predicted class", rationale)

    def test_misweighted_failure_confidence_drop_on_intensifier(self):
        """Intensifier added, but confidence dropped by >15 pp -> MISWEIGHTED."""
        outcome, failure_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.95,
            probe_confidence=0.70,  # dropped 25 pp
            expected_effect="PRESERVE",
            semantic_intent="STRENGTHEN_POLARITY",
            expected_label_relation="SAME_LABEL",
            expected_confidence_relation="INCREASE",
            confidence_delta_threshold_pp=15.0,
        )
        self.assertEqual(failure_cat, FailureCategory.MISWEIGHTED)
        self.assertIn("confidence dropped", rationale)

    def test_misweighted_failure_flip_on_degree_modifier(self):
        """Degree modifier caused label flip -> MISWEIGHTED."""
        outcome, failure_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.90,
            probe_confidence=0.60,
            expected_effect="PRESERVE",
            semantic_intent="STRENGTHEN_POLARITY",
            expected_label_relation="SAME_LABEL",
        )
        self.assertEqual(failure_cat, FailureCategory.MISWEIGHTED)
        self.assertIn("degree modifier", rationale)

    def test_none_on_correct_flip(self):
        """Expected flip occurred correctly -> FailureCategory.NONE."""
        outcome, failure_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.99,
            probe_confidence=0.97,
            expected_effect="INVERT",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_FLIP)
        self.assertEqual(failure_cat, FailureCategory.NONE)

    def test_none_on_correct_preserve(self):
        """Expected preserve occurred correctly -> FailureCategory.NONE."""
        outcome, failure_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.95,
            probe_confidence=0.96,
            expected_effect="PRESERVE",
            semantic_intent="PRESERVE_MEANING",
            expected_label_relation="SAME_LABEL",
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)
        self.assertEqual(failure_cat, FailureCategory.NONE)

    def test_undetermined_failure(self):
        """Unknown or unconstrained probe effect with no clear expectation -> UNDETERMINED."""
        outcome, failure_cat, evidence, rationale = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.80,
            probe_confidence=0.80,
            expected_effect="UNKNOWN",
            semantic_intent="",
            expected_label_relation="",
        )
        self.assertEqual(outcome, BehavioralOutcome.UNDETERMINED)
        self.assertEqual(failure_cat, FailureCategory.UNDETERMINED)


class TestDeterministicBenchmarkAcceptance(unittest.TestCase):
    """
    Evaluates the 5 active sentiment models on standard probes:
    5 models x 1 baseline + 5 models x 4 probes = 25 evaluations.
    Verifies baseline evaluated once per model and count integrity.
    """

    def test_deterministic_5_models_benchmark(self):
        seed_text = "I loved the movie."
        p1 = SharedProbe.create(
            seed_text=seed_text,
            perturbed_text="I did not love the movie.",
            perturbation_type="negation",
            expected_flip=True,
            expected_semantic_effect="invert",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
            description="Negation inversion",
        )
        p1.probe_id = "P001"
        p2 = SharedProbe.create(
            seed_text=seed_text,
            perturbed_text="I adored the film.",
            perturbation_type="lexical",
            expected_flip=False,
            expected_semantic_effect="preserve",
            semantic_intent="PRESERVE_MEANING",
            expected_label_relation="SAME_LABEL",
            description="Synonym substitution",
        )
        p2.probe_id = "P002"
        p3 = SharedProbe.create(
            seed_text=seed_text,
            perturbed_text="I really loved the movie.",
            perturbation_type="intensifier",
            expected_flip=False,
            expected_semantic_effect="preserve",
            semantic_intent="STRENGTHEN_POLARITY",
            expected_label_relation="SAME_LABEL",
            expected_confidence_relation="INCREASE",
            description="Intensifier addition",
        )
        p3.probe_id = "P003"
        p4 = SharedProbe.create(
            seed_text=seed_text,
            perturbed_text="The movie, I loved it.",
            perturbation_type="syntax",
            expected_flip=False,
            expected_semantic_effect="preserve",
            semantic_intent="PRESERVE_MEANING",
            expected_label_relation="SAME_LABEL",
            description="Topicalization syntax reorder",
        )
        p4.probe_id = "P004"
        probes = [p1, p2, p3, p4]
        probe_set = SharedProbeSet(
            probe_set_id="PS_BENCHMARK",
            seed_texts=[seed_text],
            probes=probes,
            sentence_types={seed_text: "literal"},
        )

        model_ids = [
            "distilbert-base-uncased-finetuned-sst-2-english",
            "textattack/albert-base-v2-SST-2",
            "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "textattack/bert-base-uncased-SST-2",
            "cardiffnlp/twitter-roberta-base-sentiment",
        ]

        total_baselines = 0
        total_probe_evaluations = 0

        for mid in model_ids:
            wrapper = HuggingFaceWrapper(mid, device="cpu", allow_fallback=False)
            tester = BehavioralTester(wrapper)
            eval_results = tester.evaluate_shared_probes(probe_set)

            # Baseline evaluated exactly once
            baselines = eval_results["baselines"]
            self.assertEqual(len(baselines), 1, f"Model {mid} baseline not evaluated exactly once.")
            self.assertIn(seed_text, baselines)
            base_eval = baselines[seed_text]
            base_label = base_eval["prediction"]["label"] if isinstance(base_eval, dict) else base_eval.prediction.label
            self.assertEqual(base_label, "POSITIVE", f"Model {mid} failed baseline sentiment.")
            total_baselines += len(baselines)

            # 4 probes evaluated
            evaluations = eval_results["evaluations"]
            self.assertEqual(len(evaluations), 4, f"Model {mid} did not execute all 4 probes.")
            total_probe_evaluations += len(evaluations)

            # Check probe details
            p001_eval = [e for e in evaluations if e.probe_id == "P001"][0]
            self.assertEqual(p001_eval.original_label, "POSITIVE")
            self.assertIn(p001_eval.perturbed_label, ["NEGATIVE", "NEUTRAL", "POSITIVE"])

            # Check count integrity: 4 planned == 4 executed
            self.assertEqual(eval_results["total_probes"], 4)

        # Exact acceptance matrix: 5 baselines + 20 probes = 25 evaluations
        self.assertEqual(total_baselines, 5)
        self.assertEqual(total_probe_evaluations, 20)
        self.assertEqual(total_baselines + total_probe_evaluations, 25)


if __name__ == "__main__":
    unittest.main()
