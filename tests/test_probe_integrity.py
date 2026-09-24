"""
Automated Test Suite for BlindSpot Canonical Probe Protocol & Behavioral Flip Integrity.
Implements the 20 required verification tests for probe determinism, multiclass flip logic,
stratified behavioral metrics, schema validation, perturbation engines, and pipeline integrity.
"""
import unittest
import tempfile
import pathlib

from blindspot.core.types import (
    LinguisticProbe,
    SharedProbeSet,
    BehavioralOutcome,
    ProbeStatus,
    SemanticIntent,
    SentenceType,
    PredictionResult,
    ModelProbeEvaluation,
    BaselineEvaluation,
    is_prediction_flip,
    classify_behavioral_outcome,
)
from blindspot.testing.metrics import (
    compute_observed_flip_rate,
    compute_expected_flip_rate,
    compute_preserve_rate,
    compute_behavioral_consistency,
    compute_confidence_flip_rate,
)
from blindspot.perturbations.intensity import IntensityPerturber
from blindspot.perturbations.structure import StructurePerturber
from blindspot.perturbations.shared import SharedProbeGenerator
from blindspot.core.config import ExperimentConfig, PerformanceMode
from blindspot.execution.runner import ExperimentRunner


class DummyModelWrapper:
    """Mock model wrapper for deterministic, fast behavioral evaluation tests."""
    def __init__(self, model_name: str = "mock-model", labels=None):
        self.model_name = model_name
        self.labels = labels or ["NEGATIVE", "POSITIVE"]

    def predict_result(self, text: str) -> PredictionResult:
        # Simple deterministic rule for mock tests:
        # "not", "terrible", "awful" -> NEGATIVE, else POSITIVE
        t_low = text.lower()
        if "not" in t_low or "terrible" in t_low or "awful" in t_low:
            lbl = "NEGATIVE"
            conf = 0.90
            probs = {"NEGATIVE": 0.90, "POSITIVE": 0.10}
        else:
            lbl = "POSITIVE"
            conf = 0.95
            probs = {"NEGATIVE": 0.05, "POSITIVE": 0.95}

        return PredictionResult(
            label=lbl,
            confidence=conf,
            probabilities=probs,
            latency_ms=1.5,
        )

    def predict_results_batch(self, texts, batch_size=16):
        return [self.predict_result(t) for t in texts]


class TestProbeIntegrity(unittest.TestCase):
    """20 Canonical Probe Integrity and Behavioral Flip Tests."""

    # 1. Deterministic Probe ID
    def test_probe_id_determinism(self):
        p1 = LinguisticProbe.create(
            seed_text="The film was great.",
            perturbed_text="The film was not great.",
            perturbation_type="negation",
            description="Negation insertion",
            expected_semantic_effect="invert",
            expected_flip=True,
        )
        p2 = LinguisticProbe.create(
            seed_text="The film was great.",
            perturbed_text="The film was not great.",
            perturbation_type="negation",
            description="Different description",  # Description does not change ID
            expected_semantic_effect="invert",
            expected_flip=True,
        )
        self.assertEqual(p1.probe_id, p2.probe_id)
        self.assertTrue(len(p1.probe_id) >= 16)

    # 2. Unique Probe IDs for Different Perturbations
    def test_probe_id_uniqueness(self):
        p1 = LinguisticProbe.create(
            seed_text="The film was great.",
            perturbed_text="The film was not great.",
            perturbation_type="negation",
            expected_semantic_effect="invert",
            expected_flip=True,
        )
        p2 = LinguisticProbe.create(
            seed_text="The film was great.",
            perturbed_text="The film was truly great.",
            perturbation_type="intensity",
            expected_semantic_effect="strengthen",
            expected_flip=False,
        )
        self.assertNotEqual(p1.probe_id, p2.probe_id)

    # 3. Canonical Multiclass Prediction Flip Definition
    def test_multiclass_prediction_flip_canonical(self):
        # 3-class sentiment: NEGATIVE -> NEUTRAL is a flip
        self.assertTrue(is_prediction_flip("NEGATIVE", "NEUTRAL"))
        self.assertTrue(is_prediction_flip("neutral", "positive"))
        self.assertTrue(is_prediction_flip("LABEL_0", "LABEL_2"))

    # 4. Same Label Does Not Flip Even With Confidence Shifts
    def test_multiclass_prediction_flip_same_label(self):
        self.assertFalse(is_prediction_flip("POSITIVE", "POSITIVE"))
        self.assertFalse(is_prediction_flip("negative", "NEGATIVE"))
        self.assertFalse(is_prediction_flip("Neutral", "neutral"))

    # 5. Behavioral Outcome: Expected Flip
    def test_behavioral_outcome_expected_flip(self):
        outcome = classify_behavioral_outcome(
            original_label="POSITIVE",
            perturbed_label="NEGATIVE",
            expected_flip=True,
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_FLIP)

    # 6. Behavioral Outcome: Missing Flip
    def test_behavioral_outcome_missing_flip(self):
        outcome = classify_behavioral_outcome(
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            expected_flip=True,
        )
        self.assertEqual(outcome, BehavioralOutcome.MISSING_FLIP)

    # 7. Behavioral Outcome: Expected Preserve
    def test_behavioral_outcome_expected_preserve(self):
        outcome = classify_behavioral_outcome(
            original_label="POSITIVE",
            perturbed_label="POSITIVE",
            expected_flip=False,
        )
        self.assertEqual(outcome, BehavioralOutcome.EXPECTED_PRESERVE)

    # 8. Behavioral Outcome: Unexpected Flip
    def test_behavioral_outcome_unexpected_flip(self):
        outcome = classify_behavioral_outcome(
            original_label="POSITIVE",
            perturbed_label="NEGATIVE",
            expected_flip=False,
        )
        self.assertEqual(outcome, BehavioralOutcome.UNEXPECTED_FLIP)

    # 9. BaselineEvaluation Record
    def test_baseline_evaluation_record(self):
        pred = PredictionResult(label="POSITIVE", confidence=0.98, probabilities={"POSITIVE": 0.98, "NEGATIVE": 0.02})
        base = BaselineEvaluation(
            model_id="bert-sst2",
            seed_text="The food was outstanding.",
            sentence_type=SentenceType.LITERAL.value,
            prediction=pred,
            latency_ms=12.4,
        )
        self.assertEqual(base.model_id, "bert-sst2")
        self.assertEqual(base.sentence_type, "literal")
        self.assertEqual(base.prediction.label, "POSITIVE")
        d = base.to_dict()
        self.assertIn("seed_text", d)
        self.assertEqual(d["latency_ms"], 12.4)

    # 10. Stratified Observed Flip Rate
    def test_stratified_observed_flip_rate(self):
        evals = [
            {"is_flipped": True, "expected_flip": True},
            {"is_flipped": False, "expected_flip": True},
            {"is_flipped": True, "expected_flip": False},
            {"is_flipped": False, "expected_flip": False},
        ]
        # 2 flips out of 4 executed probes = 50%
        rate = compute_observed_flip_rate(evals)
        self.assertAlmostEqual(rate, 0.50, places=4)

    # 11. Stratified Expected Flip Rate
    def test_stratified_expected_flip_rate(self):
        evals = [
            {"is_flipped": True, "expected_flip": True},   # hit
            {"is_flipped": False, "expected_flip": True},  # miss
            {"is_flipped": True, "expected_flip": False},  # irrelevant to expected flip rate
        ]
        # 1 hit out of 2 expected flip probes = 50%
        rate = compute_expected_flip_rate(evals)
        self.assertAlmostEqual(rate, 0.50, places=4)

    # 12. Stratified Preserve Rate
    def test_stratified_preserve_rate(self):
        evals = [
            {"is_flipped": False, "expected_flip": False},  # preserved
            {"is_flipped": False, "expected_flip": False},  # preserved
            {"is_flipped": True, "expected_flip": False},   # broken
            {"is_flipped": True, "expected_flip": True},    # irrelevant to preserve rate
        ]
        # 2 preserves out of 3 expected preserve probes = 66.67%
        rate = compute_preserve_rate(evals)
        self.assertAlmostEqual(rate, 2 / 3, places=4)

    # 13. Stratified Behavioral Consistency
    def test_stratified_behavioral_consistency(self):
        evals = [
            {"expectation_satisfied": True},
            {"expectation_satisfied": True},
            {"expectation_satisfied": False},
            {"expectation_satisfied": True},
        ]
        # 3 satisfied out of 4 = 75%
        rate = compute_behavioral_consistency(evals)
        self.assertAlmostEqual(rate, 0.75, places=4)

    # 14. Confidence Flip Rate (Sensitivity)
    def test_confidence_flip_rate(self):
        evals = [
            {"confidence_delta_pts": -25.0},  # drop >= 20 pts
            {"confidence_delta_pts": -10.0},  # smaller drop
            {"confidence_delta_pts": +5.0},   # gain
            {"confidence_delta_pts": -30.0},  # drop >= 20 pts
        ]
        rate = compute_confidence_flip_rate(evals, threshold_pts=20.0)
        self.assertAlmostEqual(rate, 0.50, places=4)

    # 15. Probe Set Validation: Passes on Valid Set
    def test_probe_set_validation_passes_valid(self):
        p1 = LinguisticProbe.create(seed_text="Hello world.", perturbed_text="Hello universe.", perturbation_type="synonym_substitution")
        p2 = LinguisticProbe.create(seed_text="Hello world.", perturbed_text="Hello not world.", perturbation_type="negation")
        pset = SharedProbeSet(probe_set_id="valid_set", seed_texts=["Hello world."], probes=[p1, p2])
        is_valid, issues = pset.validate()
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)

    # 16. Probe Set Validation: Catches Empty Probe ID
    def test_probe_set_validation_catches_empty_probe_id(self):
        p1 = LinguisticProbe.create(seed_text="Test", perturbed_text="Test pert", perturbation_type="test")
        p1.probe_id = ""  # Corrupt probe ID
        pset = SharedProbeSet(probe_set_id="bad_set", seed_texts=["Test"], probes=[p1])
        is_valid, issues = pset.validate()
        self.assertFalse(is_valid)
        self.assertTrue(any("missing probe_id" in issue for issue in issues))

    # 17. Probe Set Validation: Catches Duplicate Probe IDs
    def test_probe_set_validation_catches_duplicates(self):
        p1 = LinguisticProbe.create(seed_text="Test", perturbed_text="Test pert", perturbation_type="test")
        pset = SharedProbeSet(probe_set_id="dup_set", seed_texts=["Test"], probes=[p1, p1])
        is_valid, issues = pset.validate()
        self.assertFalse(is_valid)
        self.assertTrue(any("Duplicate probe_id" in issue for issue in issues))


    # 18. Intensity Perturber Generates Degree Variants
    def test_intensity_perturber_generates_variants(self):
        perturber = IntensityPerturber()
        variants = perturber.perturb("The movie was great.")
        self.assertTrue(len(variants) >= 2)
        for v in variants:
            self.assertEqual(v["type"], "intensity")
            self.assertFalse(v["expected_flip"])
            self.assertIn(v["expected_semantic_effect"], ["strengthen", "weaken"])

    # 19. Structure Perturber Generates Syntactic Variants
    def test_structure_perturber_generates_variants(self):
        perturber = StructurePerturber()
        variants = perturber.perturb("Because the weather was bad, the flight was delayed.")
        self.assertTrue(len(variants) >= 1)
        for v in variants:
            self.assertEqual(v["type"], "structure")
            self.assertFalse(v["expected_flip"])
            self.assertEqual(v["expected_semantic_effect"], "preserve")

    # 20. Pipeline Count Integrity: Planned == Executed == Analyzed == Reported
    def test_pipeline_count_integrity(self):
        p1 = LinguisticProbe.create(seed_text="Great plot.", perturbed_text="Awful plot.", perturbation_type="negation", expected_flip=True)
        p2 = LinguisticProbe.create(seed_text="Great plot.", perturbed_text="Extremely great plot.", perturbation_type="intensity", expected_flip=False)
        selected_pset = SharedProbeSet(
            probe_set_id="canonical_test_set",
            seed_texts=["Great plot."],
            probes=[p1, p2],
            sentence_types={"Great plot.": "literal"},
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            config = ExperimentConfig(
                experiment_name="Integrity Verification Run",
                model_ids=["distilbert-base-uncased-finetuned-sst-2-english"],
                seed_texts=["Great plot."],
                selected_probe_set=selected_pset,
                output_dir=tmp_dir,
                explainer_type="none",
                performance_mode=PerformanceMode.FAST_DEBUG,
            )
            runner = ExperimentRunner(config=config)
            # Use mock wrapper to prevent external network calls during fast test
            runner.model_cache.put("distilbert-base-uncased-finetuned-sst-2-english", DummyModelWrapper())

            results = runner.run_sync()
            integrity = results.get("pipeline_integrity", {})

            self.assertTrue(integrity.get("all_passed", False))
            self.assertEqual(integrity.get("total_probes"), 2)

            m_check = integrity.get("model_checks", {}).get("distilbert-base-uncased-finetuned-sst-2-english", {})
            self.assertEqual(m_check.get("planned"), 2)
            self.assertEqual(m_check.get("executed"), 2)
            self.assertEqual(m_check.get("analyzed"), 2)
            self.assertEqual(m_check.get("reported"), 2)
            self.assertTrue(m_check.get("integrity_verified"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
