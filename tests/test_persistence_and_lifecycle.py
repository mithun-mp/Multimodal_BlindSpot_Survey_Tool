"""
Comprehensive tests for granular persistence, data retention, archiving,
and incremental lifecycle management in RunStore.
"""
import os
import sys
import unittest
import tempfile
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.storage.run_store import RunStore
from blindspot.core.config import ExperimentConfig
from blindspot.core.types import ModelExecutionTiming, ModelStatus


class TestPersistenceAndLifecycle(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.store = RunStore(base_dir=self.temp_dir)

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_run_initialization_and_metadata_structure(self):
        exp_id = "test_run_init_001"
        cfg = ExperimentConfig(
            experiment_name="Audit Init Test",
            model_ids=["distilbert-sst2", "cardiffnlp/twitter-roberta-base-sentiment-latest"],
            seed_texts=["Sample seed text."],
        )
        run_dir = self.store.init_run(exp_id, cfg)
        self.assertTrue(os.path.isdir(run_dir))
        self.assertTrue(os.path.isdir(os.path.join(run_dir, "models")))
        self.assertTrue(os.path.isdir(os.path.join(run_dir, "aggregate")))
        self.assertTrue(os.path.isdir(os.path.join(run_dir, "figures")))
        self.assertTrue(os.path.isdir(os.path.join(run_dir, "reports")))

        runs = self.store.list_runs()
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["experiment_id"], exp_id)
        self.assertEqual(runs[0]["status"], "running")
        self.assertEqual(runs[0]["completed_models"], [])

    def test_per_model_incremental_persistence(self):
        exp_id = "test_run_inc_002"
        model_1 = "distilbert-base-uncased-finetuned-sst-2-english"
        model_2 = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        cfg = ExperimentConfig(
            experiment_name="Incremental Test",
            model_ids=[model_1, model_2],
            seed_texts=["Seed text"],
        )
        self.store.init_run(exp_id, cfg)

        timing_1 = ModelExecutionTiming(
            model_id=model_1,
            model_load_ms=120.0,
            baseline_inference_ms=15.0,
            probe_inference_ms=45.0,
            total_inference_ms=60.0,
            analysis_ms=5.0,
            total_duration_sec=0.25,
        )

        model_1_data = {
            "status": ModelStatus.COMPLETED,
            "baseline": {"label": "POSITIVE", "confidence": 0.98},
            "predictions": [{"probe_id": "p1", "prediction": "NEGATIVE", "confidence": 0.85}],
            "behavioral": [{"probe_id": "p1", "behavioral_outcome": "EXPECTED_FLIP"}],
            "metrics": {"observed_flip_rate": 1.0, "total_probes": 1},
            "failures": [],
            "timing": timing_1,
            "report_md": "# Model 1 Report\nAll passed.",
            "completed_at": time.time(),
        }

        # Save model 1 immediately
        self.store.save_model_result(exp_id, model_1, model_1_data)

        # Verify incremental state in metadata
        completed = self.store.list_completed_models(exp_id)
        self.assertEqual(completed, [model_1])

        runs = self.store.list_runs()
        self.assertIn(model_1, runs[0]["completed_models"])
        self.assertEqual(runs[0]["model_states"][model_1], "completed")
        self.assertEqual(runs[0]["model_states"][model_2], "queued")

        # Load model 1 result back
        loaded_m1 = self.store.load_model_result(exp_id, model_1)
        self.assertIsNotNone(loaded_m1)
        self.assertEqual(loaded_m1["status"], "COMPLETED")
        self.assertEqual(loaded_m1["baseline"]["label"], "POSITIVE")
        self.assertEqual(loaded_m1["timing"]["total_duration_sec"], 0.25)
        self.assertIn("All passed", loaded_m1["report_md"])

        # Now save model 2 with slash in name
        timing_2 = ModelExecutionTiming(
            model_id=model_2,
            total_duration_sec=0.40,
        )
        model_2_data = {
            "status": "COMPLETED",
            "baseline": {"label": "NEGATIVE", "confidence": 0.90},
            "metrics": {"observed_flip_rate": 0.0},
            "timing": timing_2,
            "completed_at": time.time(),
        }
        self.store.save_model_result(exp_id, model_2, model_2_data)

        completed = self.store.list_completed_models(exp_id)
        self.assertEqual(len(completed), 2)
        self.assertIn(model_1, completed)
        self.assertIn(model_2, completed)

        # Full run loader contains both models
        full_run = self.store.load_run(exp_id)
        self.assertIn("models", full_run)
        self.assertIn(model_1, full_run["models"])
        self.assertIn(model_2, full_run["models"])

    def test_run_archiving_preserves_data(self):
        exp_id = "test_run_arch_003"
        cfg = ExperimentConfig(
            experiment_name="Archive Test",
            model_ids=["distilbert-sst2"],
            seed_texts=["Test"],
        )
        self.store.init_run(exp_id, cfg)
        self.store.save_results(exp_id, {"status": "ok", "flip_rate": 0.5})

        # Archive
        arch_dest = self.store.archive_run(exp_id)
        self.assertTrue(os.path.exists(arch_dest))
        self.assertFalse(os.path.exists(self.store.get_run_dir(exp_id)))

        # Standard list_runs does not include archived runs
        active_runs = self.store.list_runs(include_archived=False)
        self.assertEqual(len(active_runs), 0)

        # With include_archived=True, it is found
        all_runs = self.store.list_runs(include_archived=True)
        self.assertEqual(len(all_runs), 1)
        self.assertTrue(all_runs[0].get("is_archived", False))

        # load_run falls back to archive
        loaded = self.store.load_run(exp_id)
        self.assertEqual(loaded["results"]["flip_rate"], 0.5)

    def test_delete_run_requires_explicit_confirmation(self):
        exp_id = "test_run_del_004"
        cfg = ExperimentConfig(
            experiment_name="Deletion Safety Test",
            model_ids=["distilbert-sst2"],
            seed_texts=["Test"],
        )
        self.store.init_run(exp_id, cfg)

        # Refuse deletion without confirmation
        with self.assertRaises(ValueError):
            self.store.delete_run(exp_id, confirmation=False)

        # Confirmed deletion succeeds
        success = self.store.delete_run(exp_id, confirmation=True)
        self.assertTrue(success)
        self.assertFalse(os.path.exists(self.store.get_run_dir(exp_id)))

    def test_runner_resume_and_15_figures_generation(self):
        """Verifies that ExperimentRunner saves per-model artifacts, generates 15 figures, and supports resume."""
        import numpy as np
        from blindspot.core.types import ModelMetadata
        from blindspot.execution.runner import ExperimentRunner
        from blindspot.models.cache import ModelCache

        class MockSentimentWrapper:
            def __init__(self, model_name: str):
                self.model_name = model_name
                self.labels = ["NEGATIVE", "POSITIVE"]
                self.num_classes = 2
                self.architecture = "MockClassifier"
                self.parameters_millions = 10.0

            def predict_proba(self, texts, batch_size: int = 32):
                if isinstance(texts, str):
                    texts = [texts]
                res = []
                for t in texts:
                    if "not" in str(t).lower():
                        res.append([0.85, 0.15])
                    else:
                        res.append([0.10, 0.90])
                return np.array(res)

            def predict_result(self, text: str):
                from blindspot.core.types import PredictionResult
                p = self.predict_proba([text])[0]
                idx = int(np.argmax(p))
                return PredictionResult(
                    label=self.labels[idx],
                    confidence=float(p[idx]),
                    probabilities={self.labels[i]: float(p[i]) for i in range(2)},
                    latency_ms=1.0,
                    model_id=self.model_name,
                )

            def predict_results_batch(self, texts, batch_size: int = 16):
                return [self.predict_result(t) for t in texts]

            def get_metadata(self):
                return ModelMetadata(
                    model_id=self.model_name,
                    architecture=self.architecture,
                    task="text-classification",
                    num_classes=2,
                    label_names=self.labels,
                    verified=True,
                )

        cache = ModelCache(max_size=5)
        cache.put("mock_model_1", MockSentimentWrapper("mock_model_1"))
        cache.put("mock_model_2", MockSentimentWrapper("mock_model_2"))

        exp_id = "test_run_resume_005"
        config = ExperimentConfig(
            experiment_name="Resume Test Audit",
            model_ids=["mock_model_1", "mock_model_2"],
            seed_texts=["This is great."],
            perturbation_types=["negation"],
            explainer_type="none",
            output_dir=self.temp_dir,
        )

        runner = ExperimentRunner(config=config, run_store=self.store, model_cache=cache)
        runner.experiment_id = exp_id
        results = runner.run_sync()

        self.assertEqual(runner.status, "completed")
        self.assertEqual(len(results["models"]), 2)

        # 1. Verify per-model incremental artifacts
        m1_result = self.store.load_model_result(exp_id, "mock_model_1")
        self.assertIsNotNone(m1_result)
        self.assertEqual(m1_result["status"], "COMPLETED")
        self.assertTrue(os.path.exists(os.path.join(self.store.get_model_dir(exp_id, "mock_model_1"), "predictions.json")))
        self.assertTrue(os.path.exists(os.path.join(self.store.get_model_dir(exp_id, "mock_model_1"), "status.json")))

        # 2. Verify all 15 figures were generated
        fig_dir = os.path.join(self.store.get_run_dir(exp_id), "figures")
        self.assertTrue(os.path.isdir(fig_dir))
        self.assertTrue(os.path.exists(os.path.join(fig_dir, "source_data.json")))

        generated_figs = [f for f in os.listdir(fig_dir) if f.endswith(".png")]
        self.assertGreaterEqual(len(generated_figs), 10)

        # 3. Test Resume: re-initialize runner in resume mode
        # Simulate third model added to config
        config_resumed = ExperimentConfig(
            experiment_name="Resume Test Audit",
            model_ids=["mock_model_1", "mock_model_2", "mock_model_3"],
            seed_texts=["This is great."],
            perturbation_types=["negation"],
            explainer_type="none",
            output_dir=self.temp_dir,
        )
        cache.put("mock_model_3", MockSentimentWrapper("mock_model_3"))

        resumed_runner = ExperimentRunner(config=config_resumed, run_store=self.store, model_cache=cache)
        resumed_runner.experiment_id = exp_id
        resumed_runner._resume_mode = True

        resumed_results = resumed_runner.run_sync()
        self.assertEqual(resumed_runner.status, "completed")
        self.assertEqual(len(resumed_results["models"]), 3)


if __name__ == "__main__":
    unittest.main()
