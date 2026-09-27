"""
Unit Tests for Event Streaming, Scheduler, and Experiment Execution.
"""
import sys
import os
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.core.events import EventEmitter, ExecutionEvent
from blindspot.core.config import ExperimentConfig, PerformanceMode
from blindspot.execution.scheduler import AuditScheduler
from blindspot.execution.runner import ExperimentRunner
from blindspot.storage.run_store import RunStore


class TestLiveEventsAndJobs(unittest.TestCase):
    def test_event_emitter(self):
        emitter = EventEmitter()
        received = []

        emitter.on("log", lambda e: received.append(e.data["message"]))
        emitter.emit("log", message="Test message 1")
        emitter.emit("log", message="Test message 2")

        self.assertEqual(len(received), 2)
        self.assertEqual(received[0], "Test message 1")
        self.assertEqual(len(emitter.get_history()), 2)

    def test_audit_scheduler_plan(self):
        config = ExperimentConfig(
            model_ids=["model_1", "model_2"],
            seed_texts=["Test sentence."],
        )
        scheduler = AuditScheduler(config)
        plan = scheduler.create_plan()

        # Should have probe_gen, eval_model_1, explain_model_1, eval_model_2, explain_model_2, cross_model, reporting
        task_types = [t.task_type for t in plan]
        self.assertIn("probe_generation", task_types)
        self.assertIn("model_evaluation", task_types)
        self.assertIn("cross_model_analysis", task_types)
        self.assertIn("reporting", task_types)

    def test_experiment_runner_sync(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = ExperimentConfig(
                experiment_name="Unit Test Audit",
                model_ids=["distilbert-base-uncased-finetuned-sst-2-english"],
                seed_texts=["The movie was great."],
                perturbation_types=["negation"],
                explainer_type="none",  # Fast execution for unit test
                performance_mode=PerformanceMode.FAST_DEBUG,
                output_dir=tmp_dir,
            )

            runner = ExperimentRunner(config=config, run_store=RunStore(base_dir=tmp_dir))
            results = runner.run_sync()

            self.assertEqual(runner.status, "completed")
            self.assertEqual(runner.progress, 1.0)
            self.assertIn("shared_probes", results)
            self.assertIn("distilbert-base-uncased-finetuned-sst-2-english", results["models"])

    def test_experiment_runner_async_and_cancellation(self):
        """Tests that runner runs on background thread and can be cancelled gracefully."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = ExperimentConfig(
                experiment_name="Async Test Audit",
                model_ids=["distilbert-base-uncased-finetuned-sst-2-english"],
                seed_texts=["The food was extraordinary."],
                perturbation_types=["negation", "double_negation"],
                explainer_type="none",
                performance_mode=PerformanceMode.FAST_DEBUG,
                output_dir=tmp_dir,
            )

            runner = ExperimentRunner(config=config, run_store=RunStore(base_dir=tmp_dir))
            thread = runner.run_async()
            self.assertTrue(thread.is_alive())
            
            # Immediately request cancellation
            runner.cancel()
            thread.join(timeout=10.0)
            
            self.assertIn(runner.status, ["cancelled", "completed"])


if __name__ == "__main__":
    unittest.main()
