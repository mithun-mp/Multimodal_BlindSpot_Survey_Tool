"""
Unit Tests for Experiment Run Persistence and Artifact Storage.
"""
import sys
import os
import unittest
import tempfile
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.storage.run_store import RunStore
from blindspot.core.config import ExperimentConfig
from blindspot.core.events import ExecutionEvent


class TestExperimentPersistence(unittest.TestCase):
    def test_run_store_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            store = RunStore(base_dir=tmp_dir)
            exp_id = "test_exp_123"
            config = ExperimentConfig(
                experiment_name="Persistence Test",
                model_ids=["distilbert-sst2"],
                seed_texts=["Sample text."],
            )

            # 1. Initialize run
            run_dir = store.init_run(exp_id, config)
            self.assertTrue(os.path.exists(run_dir))
            self.assertTrue(os.path.exists(os.path.join(run_dir, "config.json")))
            self.assertTrue(os.path.exists(os.path.join(run_dir, "metadata.json")))

            # 2. Log event
            event = ExecutionEvent(event_type="log", data={"message": "Inference running"})
            store.log_event(exp_id, event)
            events_file = os.path.join(run_dir, "events.jsonl")
            self.assertTrue(os.path.exists(events_file))
            with open(events_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.assertEqual(len(lines), 1)

            # 3. Save report
            report_path = store.save_report(exp_id, "summary.md", "# Test Report Content")
            self.assertTrue(os.path.exists(report_path))

            # 4. Save results
            sample_results = {"accuracy": 0.95, "status": "ok"}
            store.save_results(exp_id, sample_results, metadata={"runtime_sec": 4.5})
            self.assertTrue(os.path.exists(os.path.join(run_dir, "results.json")))

            # 5. List runs
            runs = store.list_runs()
            self.assertEqual(len(runs), 1)
            self.assertEqual(runs[0]["experiment_id"], exp_id)
            self.assertEqual(runs[0]["status"], "completed")

            # 6. Load run
            loaded = store.load_run(exp_id)
            self.assertEqual(loaded["experiment_id"], exp_id)
            self.assertEqual(loaded["results"]["accuracy"], 0.95)
            self.assertIn("summary.md", loaded["reports"])
            self.assertEqual(loaded["reports"]["summary.md"], "# Test Report Content")

            # 7. Experiment title resolution
            self.assertEqual(runs[0].get("experiment_name"), "Persistence Test")
            self.assertEqual(store.get_run_title(exp_id), "Persistence Test")
            self.assertEqual(store.get_run_title("non_existent_exp"), "non_existent_exp")
            self.assertEqual(store.get_run_title(None), "No Active Experiment")


if __name__ == "__main__":
    unittest.main()
