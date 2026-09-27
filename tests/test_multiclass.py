"""
Unit Tests for Multiclass Prediction Normalization, Metrics, and Transition Matrices.
"""
import sys
import os
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.models.huggingface_wrapper import normalize_label_name
from blindspot.core.types import PredictionResult
from blindspot.testing.metrics import (
    compute_ece,
    compute_transition_matrix,
    compute_confidence_shifts,
    compute_flip_rate,
)


class TestMulticlassFeatures(unittest.TestCase):
    def test_normalize_label_name(self):
        # Binary normalization
        self.assertEqual(normalize_label_name("LABEL_0", 2), "NEGATIVE")
        self.assertEqual(normalize_label_name("0", 2), "NEGATIVE")
        self.assertEqual(normalize_label_name("neg", 2), "NEGATIVE")
        self.assertEqual(normalize_label_name("LABEL_1", 2), "POSITIVE")
        self.assertEqual(normalize_label_name("1", 2), "POSITIVE")
        self.assertEqual(normalize_label_name("pos", 2), "POSITIVE")

        # 3-Class normalization (e.g. RoBERTa sentiment)
        self.assertEqual(normalize_label_name("LABEL_0", 3), "NEGATIVE")
        self.assertEqual(normalize_label_name("LABEL_1", 3), "NEUTRAL")
        self.assertEqual(normalize_label_name("LABEL_2", 3), "POSITIVE")
        self.assertEqual(normalize_label_name("neu", 3), "NEUTRAL")

    def test_prediction_result_formatting(self):
        res = PredictionResult(
            label="POSITIVE",
            confidence=0.98734,
            probabilities={"NEGATIVE": 0.01266, "POSITIVE": 0.98734},
            latency_ms=12.4,
            model_id="distilbert-sst2",
        )
        self.assertEqual(res.formatted_confidence, "98.73%")
        self.assertEqual(res.formatted_probabilities["POSITIVE"], "98.73%")
        self.assertEqual(res.formatted_probabilities["NEGATIVE"], "1.27%")

    def test_multiclass_ece(self):
        # Perfectly calibrated predictions
        confidences = np.array([0.9, 0.9, 0.8, 0.8])
        predictions = np.array(["POSITIVE", "POSITIVE", "NEUTRAL", "NEGATIVE"])
        labels = np.array(["POSITIVE", "POSITIVE", "NEUTRAL", "NEGATIVE"])
        ece = compute_ece(confidences, predictions, labels, n_bins=5)
        # Calibration error should be bounded and non-negative
        self.assertGreaterEqual(ece, 0.0)
        self.assertLessEqual(ece, 1.0)

    def test_transition_matrix(self):
        orig_labels = ["POSITIVE", "POSITIVE", "NEUTRAL"]
        pert_labels = ["NEGATIVE", "POSITIVE", "NEGATIVE"]
        order = ["NEGATIVE", "NEUTRAL", "POSITIVE"]

        t_matrix = compute_transition_matrix(orig_labels, pert_labels, label_order=order)
        # POSITIVE -> NEGATIVE: 1, POSITIVE -> POSITIVE: 1
        self.assertEqual(t_matrix["POSITIVE"]["NEGATIVE"], 1)
        self.assertEqual(t_matrix["POSITIVE"]["POSITIVE"], 1)
        # NEUTRAL -> NEGATIVE: 1
        self.assertEqual(t_matrix["NEUTRAL"]["NEGATIVE"], 1)
        self.assertEqual(t_matrix["NEGATIVE"]["NEGATIVE"], 0)

    def test_confidence_shifts(self):
        orig_confs = [0.90, 0.80, 0.70]
        pert_confs = [0.82, 0.95, 0.70]
        # Deltas: -0.08, +0.15, 0.00 -> -8.0 pts, +15.0 pts, 0.0 pts
        shifts = compute_confidence_shifts(orig_confs, pert_confs)
        self.assertAlmostEqual(shifts["mean_delta_pts"], ((-8.0 + 15.0 + 0.0) / 3), places=2)
        self.assertAlmostEqual(shifts["max_gain_pts"], 15.0, places=2)
        self.assertAlmostEqual(shifts["max_drop_pts"], 8.0, places=2)


if __name__ == "__main__":
    unittest.main()
