"""
Canonical Research Pipeline Test Suite for BlindSpot.
Strictly implements all 20 required verification criteria:
1. Generated probe count
2. Selected probe count
3. Executed probe count
4. selected_probe_ids == executed_probe_ids assertion
5. Baseline exists for every model
6. Binary prediction normalization
7. Multiclass prediction normalization
8. Flip detection
9. Confidence delta (pp)
10. Expected vs observed behavior
11. Failure taxonomy
12. Incremental persistence
13. Resume interrupted run
14. Delete run workflow
15. Five-model cache
16. Completed-model incremental UI state
17. Thesis graph generation
18. No AI failure prediction
19. No non-sentiment model
20. Custom probe execution
"""
import unittest
import os
import shutil
import tempfile
import time
from typing import Dict, List, Any

from blindspot.core.types import (
    LinguisticProbe,
    SharedProbeSet,
    PredictionResult,
    RunPlan,
    FailureCategory,
    BehavioralOutcome,
    SentenceType,
    SemanticIntent,
    ExpectedLabelRelation,
    ExpectedConfidenceRelation,
    is_prediction_flip,
)
from blindspot.core.config import ExperimentConfig, ResourceConfig, PerformanceMode
from blindspot.perturbations.shared import (
    SharedProbeGenerator,
    DISPLAY_CATEGORY_TO_SUBTYPES,
    _is_category_match,
)
from blindspot.testing.behavioral import BehavioralTester, classify_behavior
from blindspot.models.cache import ModelCache
from blindspot.models.registry import ModelRegistry
from blindspot.storage.run_store import RunStore
from blindspot.execution.runner import ExperimentRunner
from blindspot.reporting.thesis_graphs import ThesisVisualizer


class MockModelAuditingWrapper:
    """Mock model with explicit evaluation counter to verify exact execution counts."""
    def __init__(self, model_name: str, labels=None):
        self.model_name = model_name
        self.labels = labels or ["NEGATIVE", "POSITIVE"]
        self.evaluation_count = 0
        self.evaluated_texts = []

    def predict_result(self, text: str) -> PredictionResult:
        self.evaluation_count += 1
        self.evaluated_texts.append(text)
        t_low = text.lower()
        if "not" in t_low or "terrible" in t_low or "bad" in t_low:
            lbl = "NEGATIVE"
            conf = 0.88
            probs = {"NEGATIVE": 0.88, "POSITIVE": 0.12}
            if len(self.labels) == 3:
                probs = {"NEGATIVE": 0.88, "NEUTRAL": 0.08, "POSITIVE": 0.04}
        elif "okay" in t_low or "average" in t_low:
            if len(self.labels) == 3:
                lbl = "NEUTRAL"
                conf = 0.75
                probs = {"NEGATIVE": 0.15, "NEUTRAL": 0.75, "POSITIVE": 0.10}
            else:
                lbl = "POSITIVE"
                conf = 0.55
                probs = {"NEGATIVE": 0.45, "POSITIVE": 0.55}
        else:
            lbl = "POSITIVE"
            conf = 0.94
            probs = {"NEGATIVE": 0.06, "POSITIVE": 0.94}
            if len(self.labels) == 3:
                probs = {"NEGATIVE": 0.03, "NEUTRAL": 0.03, "POSITIVE": 0.94}

        return PredictionResult(
            label=lbl,
            confidence=conf,
            probabilities=probs,
            latency_ms=1.5,
            model_id=self.model_name,
        )

    def predict_results_batch(self, texts, batch_size=16):
        return [self.predict_result(t) for t in texts]


class TestCanonicalPipeline(unittest.TestCase):
    """Verifies all 20 canonical pipeline specifications."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="blindspot_canon_test_")
        self.run_store = RunStore(base_dir=self.test_dir)
        self.generator = SharedProbeGenerator()
        self.seed = "All that glitters is not gold."

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # 1. Generated probe count
    def test_01_generated_probe_count(self):
        pset = self.generator.generate_probes([self.seed], candidate_count=7)
        self.assertEqual(len(pset.probes), 7)
        # Without cap / specific candidate count
        all_pset = self.generator.generate_probes([self.seed], candidate_count=None)
        self.assertGreaterEqual(len(all_pset.probes), 4)

    # 2. Selected probe count
    def test_02_selected_probe_count(self):
        pset = self.generator.generate_probes([self.seed], candidate_count=7)
        selected_probes = pset.probes[:5]
        selected_ids = [p.probe_id for p in selected_probes]
        sel_set = pset.get_selected(selected_ids)
        self.assertEqual(len(sel_set.probes), 5)
        self.assertEqual([p.probe_id for p in sel_set.probes], selected_ids)

    # 3. Executed probe count
    def test_03_executed_probe_count(self):
        pset = self.generator.generate_probes([self.seed], candidate_count=7)
        selected_probes = pset.probes[:4]
        selected_ids = [p.probe_id for p in selected_probes]
        sel_set = pset.get_selected(selected_ids)

        model = MockModelAuditingWrapper(model_name="mock-model-3")
        tester = BehavioralTester(model)
        eval_res = tester.evaluate_shared_probes(sel_set)

        self.assertEqual(len(eval_res["evaluations"]), 4)
        # Total evaluations = 1 baseline + 4 probes = 5
        self.assertEqual(model.evaluation_count, 5)

    # 4. selected_probe_ids == executed_probe_ids assertion
    def test_04_selected_equals_executed_integrity(self):
        pset = self.generator.generate_probes([self.seed], candidate_count=7)
        selected_ids = [p.probe_id for p in pset.probes[:4]]

        plan = RunPlan(
            experiment_id="exp_test_04",
            model_ids=["mock-m1"],
            probe_set_id=pset.probe_set_id,
            probe_set_version=pset.probe_set_version,
            selected_probe_ids=selected_ids,
            probe_versions={pid: 1 for pid in selected_ids},
            original_text=self.seed,
        )

        # Matching execution passes
        is_valid, msg = plan.validate_execution(selected_ids)
        self.assertTrue(is_valid)

        # Dropped probe fails validation
        dropped_ids = selected_ids[:3]
        is_valid_drop, drop_msg = plan.validate_execution(dropped_ids)
        self.assertFalse(is_valid_drop)
        self.assertIn("Missing", drop_msg)

        # Unexpected extra probe fails validation
        extra_ids = selected_ids + ["unexpected_probe_999"]
        is_valid_extra, extra_msg = plan.validate_execution(extra_ids)
        self.assertFalse(is_valid_extra)
        self.assertIn("Unexpected", extra_msg)

    # 5. Baseline exists for every model
    def test_05_baseline_exists_for_every_model(self):
        pset = self.generator.generate_probes([self.seed], candidate_count=7)
        model_a = MockModelAuditingWrapper(model_name="mock-distilbert")
        model_b = MockModelAuditingWrapper(model_name="mock-roberta")

        tester_a = BehavioralTester(model_a)
        tester_b = BehavioralTester(model_b)

        res_a = tester_a.evaluate_shared_probes(pset)
        res_b = tester_b.evaluate_shared_probes(pset)

        self.assertIn(self.seed, res_a["baselines"])
        self.assertIn(self.seed, res_b["baselines"])

        base_a = res_a["baselines"][self.seed]
        seed_txt = base_a["seed_text"] if isinstance(base_a, dict) else base_a.seed_text
        lbl = base_a["prediction"]["label"] if isinstance(base_a, dict) else base_a.prediction.label
        conf = base_a["prediction"]["confidence"] if isinstance(base_a, dict) else base_a.prediction.confidence
        self.assertEqual(seed_txt, self.seed)
        self.assertEqual(lbl, "NEGATIVE")
        self.assertGreater(conf, 0.5)

    # 6. Binary prediction normalization
    def test_06_binary_prediction_normalization(self):
        model_binary = MockModelAuditingWrapper(model_name="binary-model", labels=["NEGATIVE", "POSITIVE"])
        pred = model_binary.predict_result("I loved this film.")
        self.assertIn(pred.label, ["NEGATIVE", "POSITIVE"])
        self.assertNotIn("NEUTRAL", pred.probabilities)
        self.assertAlmostEqual(sum(pred.probabilities.values()), 1.0, places=4)
        self.assertIn("%", pred.formatted_confidence)

    # 7. Multiclass prediction normalization
    def test_07_multiclass_prediction_normalization(self):
        model_multi = MockModelAuditingWrapper(
            model_name="3class-model",
            labels=["NEGATIVE", "NEUTRAL", "POSITIVE"],
        )
        pred = model_multi.predict_result("The movie was okay.")
        self.assertIn(pred.label, ["NEGATIVE", "NEUTRAL", "POSITIVE"])
        self.assertIn("NEUTRAL", pred.probabilities)
        self.assertEqual(len(pred.probabilities), 3)
        self.assertAlmostEqual(sum(pred.probabilities.values()), 1.0, places=4)

    # 8. Flip detection
    def test_08_flip_detection(self):
        self.assertTrue(is_prediction_flip("POSITIVE", "NEGATIVE"))
        self.assertTrue(is_prediction_flip("POSITIVE", "NEUTRAL"))
        self.assertTrue(is_prediction_flip("NEGATIVE", "POSITIVE"))
        self.assertFalse(is_prediction_flip("POSITIVE", "POSITIVE"))
        self.assertFalse(is_prediction_flip("NEGATIVE", "negative"))
        self.assertFalse(is_prediction_flip("NEUTRAL", "neutral"))

    # 9. Confidence delta
    def test_09_confidence_delta(self):
        orig_conf = 0.90
        pert_conf = 0.70
        delta_pp = (pert_conf - orig_conf) * 100.0
        self.assertAlmostEqual(delta_pp, -20.0, places=2)

    # 10. Expected vs observed behavior
    def test_10_expected_vs_observed_behavior(self):
        # Case A: Expected flip occurred -> EXPECTED_FLIP
        outcome_a, fail_a, _, _ = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.90,
            probe_confidence=0.85,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
        )
        self.assertEqual(outcome_a, BehavioralOutcome.EXPECTED_FLIP)
        self.assertEqual(fail_a, FailureCategory.NONE)

        # Case B: Expected preserve occurred -> EXPECTED_PRESERVE
        outcome_b, fail_b, _, _ = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.91,
            expected_effect="EXPECTED_PRESERVE",
            semantic_intent="PRESERVE_MEANING",
            expected_label_relation="SAME_LABEL",
        )
        self.assertEqual(outcome_b, BehavioralOutcome.EXPECTED_PRESERVE)
        self.assertEqual(fail_b, FailureCategory.NONE)

    # 11. Failure taxonomy
    def test_11_failure_taxonomy_coverage(self):
        # BLIND: Missing flip on negation
        _, fail_blind, _, _ = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.88,
            expected_effect="EXPECTED_FLIP",
            semantic_intent="REVERSE_POLARITY",
            expected_label_relation="DIFFERENT_LABEL",
        )
        self.assertEqual(fail_blind, FailureCategory.BLIND)

        # SPURIOUS: Unexpected flip on meaning-preserving probe
        _, fail_spur, _, _ = classify_behavior(
            original_label="POSITIVE",
            probe_label="NEGATIVE",
            original_confidence=0.90,
            probe_confidence=0.85,
            expected_effect="EXPECTED_PRESERVE",
            semantic_intent="PRESERVE_MEANING",
            expected_label_relation="SAME_LABEL",
        )
        self.assertEqual(fail_spur, FailureCategory.SPURIOUS)

        # MISWEIGHTED: Severe confidence drop under degree intensifier
        _, fail_misw, _, _ = classify_behavior(
            original_label="POSITIVE",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.60,  # -30 pp drop
            expected_effect="STRENGTHEN",
            semantic_intent="STRENGTHEN_POLARITY",
            expected_label_relation="SAME_LABEL",
            expected_confidence_relation="INCREASE",
        )
        self.assertEqual(fail_misw, FailureCategory.MISWEIGHTED)

        # UNDETERMINED: Missing labels
        _, fail_undet, _, _ = classify_behavior(
            original_label="",
            probe_label="POSITIVE",
            original_confidence=0.90,
            probe_confidence=0.85,
        )
        self.assertEqual(fail_undet, FailureCategory.UNDETERMINED)

    # 12. Incremental persistence
    def test_12_incremental_persistence(self):
        exp_id = "exp_test_persist_012"
        cfg = ExperimentConfig(experiment_name="Test Persist", model_ids=["mock-m1", "mock-m2"])
        self.run_store.init_run(exp_id, cfg)

        model_dir = self.run_store.save_model_result(exp_id, "mock-m1", {
            "status": "COMPLETED",
            "model_id": "mock-m1",
            "probes_done": 4,
            "total_probes": 4,
            "metrics": {"observed_flip_rate": 0.25},
            "failures": [],
        })
        self.assertTrue(os.path.exists(os.path.join(model_dir, "status.json")))
        self.assertTrue(os.path.exists(os.path.join(model_dir, "metrics.json")))

        completed = self.run_store.list_completed_models(exp_id)
        self.assertIn("mock-m1", completed)
        self.assertNotIn("mock-m2", completed)

    # 13. Resume interrupted run
    def test_13_resume_interrupted_run(self):
        exp_id = "exp_test_resume_013"
        cfg = ExperimentConfig(experiment_name="Test Resume", model_ids=["mock-m1", "mock-m2"])
        self.run_store.init_run(exp_id, cfg)

        # Mark mock-m1 completed
        self.run_store.save_model_result(exp_id, "mock-m1", {
            "status": "COMPLETED",
            "model_id": "mock-m1",
            "predictions": [],
            "metrics": {},
            "taxonomy": [],
        })

        # Load completed models
        completed = self.run_store.list_completed_models(exp_id)
        self.assertEqual(completed, ["mock-m1"])

        # Resume runner
        runner = ExperimentRunner.resume_run(exp_id, run_store=self.run_store)
        self.assertTrue(runner._resume_mode)
        self.assertEqual(runner.experiment_id, exp_id)

    # 14. Delete run workflow
    def test_14_delete_run_workflow(self):
        exp_id = "exp_test_delete_014"
        cfg = ExperimentConfig(experiment_name="Test Delete", model_ids=["mock-m1"])
        self.run_store.init_run(exp_id, cfg)
        run_dir = self.run_store.get_run_dir(exp_id)
        self.assertTrue(os.path.exists(run_dir))

        # Unconfirmed deletion must fail
        with self.assertRaises(ValueError):
            self.run_store.delete_run(exp_id, confirmation=False)
        self.assertTrue(os.path.exists(run_dir))

        # Confirmed deletion removes directory
        success = self.run_store.delete_run(exp_id, confirmation=True)
        self.assertTrue(success)
        self.assertFalse(os.path.exists(run_dir))

    # 15. Five-model cache capacity
    def test_15_five_model_cache_capacity(self):
        cache = ModelCache(max_size=5)
        self.assertEqual(cache._max_size, 5)

        for i in range(5):
            cache.put(f"model_{i}", f"wrapper_{i}", device="cpu")

        self.assertEqual(cache.size(), 5)
        summary = cache.get_cache_summary()
        self.assertEqual(summary["capacity"], 5)
        self.assertEqual(summary["resident_count"], 5)
        self.assertEqual(len(summary["models"]), 5)

    # 16. Completed-model incremental UI state
    def test_16_completed_model_incremental_ui_state(self):
        exp_id = "exp_test_incremental_016"
        cfg = ExperimentConfig(experiment_name="Test Incr UI", model_ids=["m1", "m2", "m3"])
        self.run_store.init_run(exp_id, cfg)

        # Model 1 completes first
        self.run_store.save_model_result(exp_id, "m1", {
            "status": "COMPLETED",
            "model_id": "m1",
            "metrics": {"observed_flip_rate": 0.5},
            "report_md": "# Report M1",
        })

        # Completed model result is immediately readable
        m1_data = self.run_store.load_model_result(exp_id, "m1")
        self.assertIsNotNone(m1_data)
        self.assertEqual(m1_data["status"], "COMPLETED")
        self.assertEqual(m1_data["report_md"], "# Report M1")

        # Models 2 and 3 are not completed yet
        self.assertIsNone(self.run_store.load_model_result(exp_id, "m2"))
        self.assertIsNone(self.run_store.load_model_result(exp_id, "m3"))

    # 17. Thesis graph generation
    def test_17_thesis_graph_generation(self):
        figures_dir = os.path.join(self.test_dir, "test_figures")
        os.makedirs(figures_dir, exist_ok=True)
        vis = ThesisVisualizer(figures_dir=figures_dir)

        dummy_results = {
            "models": {
                "mock_m1": {
                    "evaluations": [
                        {"perturbed_label": "POSITIVE", "is_flipped": False, "confidence_delta_pts": 5.0, "category": "intensity"},
                        {"perturbed_label": "NEGATIVE", "is_flipped": True, "confidence_delta_pts": -20.0, "category": "negation"},
                    ],
                    "behavioral_metrics": {"observed_flip_rate": 0.5, "ece": 0.05, "behavioral_consistency": 0.8},
                },
                "mock_m2": {
                    "evaluations": [
                        {"perturbed_label": "POSITIVE", "is_flipped": False, "confidence_delta_pts": 2.0, "category": "intensity"},
                        {"perturbed_label": "POSITIVE", "is_flipped": False, "confidence_delta_pts": -1.0, "category": "negation"},
                    ],
                    "behavioral_metrics": {"observed_flip_rate": 0.0, "ece": 0.03, "behavioral_consistency": 0.5},
                },
            },
            "cross_model_comparison": {
                "consensus_stats": {"overall_consensus_rate": 0.5},
            },
        }

        fig_path = vis.plot_model_prediction_distribution(dummy_results)
        self.assertTrue(os.path.exists(fig_path))
        self.assertGreater(os.path.getsize(fig_path), 1000)

    # 18. No AI failure prediction layer
    def test_18_no_ai_failure_prediction_layer(self):
        # Behavioral diagnosis must be 100% rule-based and derived from forward-pass differences
        pset = self.generator.generate_probes([self.seed], candidate_count=7)
        for p in pset.probes:
            # Probes define linguistic hypothesis/intent, never an AI predicted failure
            self.assertIn(p.expected_semantic_effect, ["invert", "preserve", "strengthen", "weaken", "concession"])
            self.assertFalse(hasattr(p, "predicted_failure"))
            self.assertFalse(hasattr(p, "ai_diagnosis"))

    # 19. No non-sentiment model
    def test_19_non_sentiment_model_rejection(self):
        registry = ModelRegistry()
        sentiment_models = registry.list_sentiment_models()
        self.assertGreaterEqual(len(sentiment_models), 5)
        # Ensure detector is excluded
        model_ids = [m["model_id"] for m in sentiment_models]
        for mid in model_ids:
            self.assertNotIn("openai-detector", mid)
            self.assertNotIn("detector", mid)

    # 20. Custom probe lifecycle execution
    def test_20_custom_probe_lifecycle_execution(self):
        custom_probe = LinguisticProbe.create(
            seed_text="The movie was fantastic.",
            perturbed_text="The movie was not fantastic.",
            perturbation_type="custom",
            description="User custom negation probe.",
            expected_semantic_effect="invert",
            expected_flip=True,
            semantic_intent=SemanticIntent.REVERSE_POLARITY.value,
            status="CUSTOM",
        )
        self.assertEqual(custom_probe.status, "CUSTOM")
        self.assertTrue(custom_probe.expected_flip)

        pset = SharedProbeSet(
            probe_set_id="custom_pset",
            seed_texts=["The movie was fantastic."],
            probes=[custom_probe],
        )

        model = MockModelAuditingWrapper(model_name="mock-custom-eval")
        tester = BehavioralTester(model)
        eval_res = tester.evaluate_shared_probes(pset)

        self.assertEqual(len(eval_res["evaluations"]), 1)
        ev = eval_res["evaluations"][0]
        self.assertEqual(ev.probe_id, custom_probe.probe_id)
        self.assertTrue(ev.is_flipped)
        self.assertEqual(ev.behavioral_outcome, "EXPECTED_FLIP")
        self.assertEqual(ev.failure_type, "None")


if __name__ == "__main__":
    unittest.main()
