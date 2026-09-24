"""
Automated Test Suite for Behavioral Flip Analysis and Confidence Delta Metrics.
Strictly verifies multiclass flip logic, label transitions, and percentage-point deltas
per Sections 8, 9, 23 of the Research-Integrity Specification.
"""
import unittest

from blindspot.core.types import is_prediction_flip
from blindspot.testing.metrics import (
    compute_transition_matrix,
    compute_confidence_shifts,
    compute_flip_rate,
)


class TestFlipAnalysis(unittest.TestCase):
    """Verifies non-binary flip detection and exact percentage-point confidence calculations."""

    def test_flip_detection_binary_opposite(self):
        self.assertTrue(is_prediction_flip("POSITIVE", "NEGATIVE"))
        self.assertTrue(is_prediction_flip("NEGATIVE", "POSITIVE"))

    def test_flip_detection_multiclass(self):
        # POSITIVE -> NEUTRAL is an empirical flip
        self.assertTrue(is_prediction_flip("POSITIVE", "NEUTRAL"))
        self.assertTrue(is_prediction_flip("NEGATIVE", "NEUTRAL"))
        self.assertTrue(is_prediction_flip("NEUTRAL", "POSITIVE"))
        self.assertTrue(is_prediction_flip("NEUTRAL", "NEGATIVE"))

    def test_flip_detection_identical_label(self):
        # Same class is NEVER a flip
        self.assertFalse(is_prediction_flip("POSITIVE", "POSITIVE"))
        self.assertFalse(is_prediction_flip("NEGATIVE", "NEGATIVE"))
        self.assertFalse(is_prediction_flip("NEUTRAL", "NEUTRAL"))

    def test_flip_detection_normalization(self):
        # Case insensitivity and whitespace tolerance
        self.assertFalse(is_prediction_flip(" positive ", "POSITIVE"))
        self.assertFalse(is_prediction_flip("NEGATIVE", "negative"))
        self.assertTrue(is_prediction_flip(" positive ", "negative"))

    def test_flip_detection_empty_or_none(self):
        self.assertFalse(is_prediction_flip("", "POSITIVE"))
        self.assertFalse(is_prediction_flip("POSITIVE", ""))
        self.assertFalse(is_prediction_flip(None, "POSITIVE"))
        self.assertFalse(is_prediction_flip("POSITIVE", None))

    def test_confidence_delta_percentage_points(self):
        # Section 9: delta_pp = (probe_confidence - original_confidence) * 100
        # original = 0.82, probe = 0.61 -> delta = -21.0 pp
        orig_conf = 0.82
        probe_conf = 0.61
        delta_pp = (probe_conf - orig_conf) * 100.0
        self.assertAlmostEqual(delta_pp, -21.0, places=4)

        # positive surge: 0.50 -> 0.95 -> delta = +45.0 pp
        orig_conf2 = 0.50
        probe_conf2 = 0.95
        delta_pp2 = (probe_conf2 - orig_conf2) * 100.0
        self.assertAlmostEqual(delta_pp2, 45.0, places=4)

    def test_confidence_shifts_aggregation(self):
        orig_confs = [0.82, 0.50, 0.70]
        probe_confs = [0.61, 0.95, 0.70]
        shifts = compute_confidence_shifts(orig_confs, probe_confs)
        self.assertEqual(shifts["num_increased"], 1)
        self.assertEqual(shifts["num_decreased"], 1)
        self.assertEqual(shifts["num_unchanged"], 1)
        self.assertAlmostEqual(shifts["mean_delta_pts"], ((-21.0 + 45.0 + 0.0) / 3.0), places=2)

    def test_multiclass_transition_matrix(self):
        labels = ["NEGATIVE", "NEUTRAL", "POSITIVE"]
        origs = ["POSITIVE", "POSITIVE", "NEGATIVE"]
        perts = ["NEGATIVE", "NEUTRAL", "NEGATIVE"]
        matrix = compute_transition_matrix(origs, perts, labels)
        
        # POSITIVE -> NEGATIVE: 1
        self.assertEqual(matrix["POSITIVE"]["NEGATIVE"], 1)
        # POSITIVE -> NEUTRAL: 1
        self.assertEqual(matrix["POSITIVE"]["NEUTRAL"], 1)
        # NEGATIVE -> NEGATIVE: 1 (no flip)
        self.assertEqual(matrix["NEGATIVE"]["NEGATIVE"], 1)


if __name__ == "__main__":
    unittest.main()
