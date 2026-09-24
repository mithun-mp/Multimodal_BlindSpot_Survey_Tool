"""
Unit Tests for Cross-Model Descriptive Analysis and Behavioral Fingerprinting.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.core.types import ModelProbeEvaluation, PredictionResult, FailureCategory
from blindspot.analysis.cross_model import CrossModelAnalyzer
from blindspot.analysis.fingerprint import compute_model_fingerprint


class TestCrossModelAnalysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = CrossModelAnalyzer()

        # Mock evaluations for two models
        pred_pos = PredictionResult(label="POSITIVE", confidence=0.95, probabilities={"NEGATIVE": 0.05, "POSITIVE": 0.95})
        pred_neg = PredictionResult(label="NEGATIVE", confidence=0.85, probabilities={"NEGATIVE": 0.85, "POSITIVE": 0.15})

        self.eval_m1 = [
            ModelProbeEvaluation(
                model_id="model_A",
                probe_id="prb_1",
                seed_text="The movie is good.",
                perturbed_text="The movie is not good.",
                perturbation_type="negation",
                expected_flip=True,
                expected_semantic_effect="invert",
                original_prediction=pred_pos,
                perturbed_prediction=pred_neg,
                is_flipped=True,
                confidence_delta=-0.10,
                confidence_delta_pts=-10.0,
                expectation_satisfied=True,
            ),
            ModelProbeEvaluation(
                model_id="model_A",
                probe_id="prb_2",
                seed_text="The acting was great.",
                perturbed_text="The acting was super great.",
                perturbation_type="synonym_substitution",
                expected_flip=False,
                expected_semantic_effect="preserve",
                original_prediction=pred_pos,
                perturbed_prediction=pred_pos,
                is_flipped=False,
                confidence_delta=0.0,
                confidence_delta_pts=0.0,
                expectation_satisfied=True,
            ),
        ]

        self.eval_m2 = [
            ModelProbeEvaluation(
                model_id="model_B",
                probe_id="prb_1",
                seed_text="The movie is good.",
                perturbed_text="The movie is not good.",
                perturbation_type="negation",
                expected_flip=True,
                expected_semantic_effect="invert",
                original_prediction=pred_pos,
                perturbed_prediction=pred_pos,  # Model B failed to flip!
                is_flipped=False,
                confidence_delta=0.0,
                confidence_delta_pts=0.0,
                expectation_satisfied=False,
            ),
            ModelProbeEvaluation(
                model_id="model_B",
                probe_id="prb_2",
                seed_text="The acting was great.",
                perturbed_text="The acting was super great.",
                perturbation_type="synonym_substitution",
                expected_flip=False,
                expected_semantic_effect="preserve",
                original_prediction=pred_pos,
                perturbed_prediction=pred_pos,
                is_flipped=False,
                confidence_delta=0.0,
                confidence_delta_pts=0.0,
                expectation_satisfied=True,
            ),
        ]

    def test_model_probe_matrix(self):
        evals_map = {"model_A": self.eval_m1, "model_B": self.eval_m2}
        matrix = self.analyzer.build_model_probe_matrix(evals_map)

        self.assertEqual(len(matrix), 2)
        prb1_row = next(r for r in matrix if r["probe_id"] == "prb_1")
        self.assertEqual(prb1_row["models"]["model_A"]["perturbed_label"], "NEGATIVE")
        self.assertEqual(prb1_row["models"]["model_B"]["perturbed_label"], "POSITIVE")

    def test_pairwise_agreement(self):
        evals_map = {"model_A": self.eval_m1, "model_B": self.eval_m2}
        pairwise = self.analyzer.compute_pairwise_agreement(evals_map)

        # On prb_1: disagree (NEG vs POS). On prb_2: agree (POS vs POS) -> 50% agreement
        self.assertEqual(pairwise["model_A"]["model_B"], 0.5)
        self.assertEqual(pairwise["model_B"]["model_A"], 0.5)
        self.assertEqual(pairwise["model_A"]["model_A"], 1.0)

    def test_behavioral_fingerprint(self):
        failures_b = [{"category": "Blind", "reason": "Ignored negation"}]
        fp_b = compute_model_fingerprint("model_B", self.eval_m2, failures_b)

        self.assertEqual(fp_b.model_id, "model_B")
        self.assertEqual(fp_b.total_probes, 2)
        self.assertEqual(fp_b.flip_rate, 0.0)
        self.assertEqual(fp_b.satisfaction_rate, 0.5)
        self.assertEqual(fp_b.failure_counts["Blind"], 1)
        self.assertEqual(fp_b.failure_counts["Spurious"], 0)


if __name__ == "__main__":
    unittest.main()
