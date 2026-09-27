"""
Unit Tests for Shared Probe Generation Protocol.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.perturbations.shared import SharedProbeGenerator, infer_expected_semantic_effect
from blindspot.core.types import LinguisticProbe, SharedProbeSet


class TestSharedProbes(unittest.TestCase):
    def setUp(self):
        self.generator = SharedProbeGenerator()

    def test_infer_expected_semantic_effect(self):
        eff, flip = infer_expected_semantic_effect("negation")
        self.assertEqual(eff, "invert")
        self.assertTrue(flip)

        eff_d, flip_d = infer_expected_semantic_effect("double_negation")
        self.assertEqual(eff_d, "preserve")
        self.assertFalse(flip_d)

        eff_s, flip_s = infer_expected_semantic_effect("synonym_substitution")
        self.assertEqual(eff_s, "preserve")
        self.assertFalse(flip_s)

        eff_c, flip_c = infer_expected_semantic_effect("connective", description="contrastive adversative")
        self.assertEqual(eff_c, "invert")
        self.assertTrue(flip_c)

    def test_generate_probes_stable_ids(self):
        seeds = [
            "The movie was great and the acting was top notch.",
            "The food was bad.",
        ]
        probe_set = self.generator.generate_probes(seeds)
        self.assertIsInstance(probe_set, SharedProbeSet)
        self.assertGreater(len(probe_set.probes), 0)

        # Check probe properties
        probe_ids = set()
        for probe in probe_set.probes:
            self.assertTrue(probe.probe_id.startswith("prb_"))
            self.assertIn(probe.seed_text, seeds)
            self.assertTrue(len(probe.perturbed_text) > 0)
            self.assertIn(probe.expected_semantic_effect, ["invert", "preserve", "weaken", "strengthen", "concession", "refutation", "neutral_drift"])
            self.assertIsInstance(probe.expected_flip, bool)
            probe_ids.add(probe.probe_id)

        # IDs should be unique per distinct probe
        self.assertEqual(len(probe_ids), len(probe_set.probes))

    def test_deterministic_probe_ids(self):
        p1 = LinguisticProbe.create("The food is great.", "The food is not great.", "negation", "negation", "invert", True)
        p2 = LinguisticProbe.create("The food is great.", "The food is not great.", "negation", "negation", "invert", True)
        self.assertEqual(p1.probe_id, p2.probe_id)

    def test_multimodel_identical_probe_stimuli_and_ids(self):
        """
        Explicitly validates that across Model A, Model B, and Model C evaluations,
        all models receive the exact same probe stimuli, metadata, and probe IDs.
        Model A probe IDs == Model B probe IDs == Model C probe IDs.
        """
        seeds = ["The atmosphere was fantastic, but the service was terrible."]
        probe_set = self.generator.generate_probes(seeds)
        self.assertGreater(len(probe_set.probes), 0)

        # Simulate probe dispatch to 3 distinct heterogeneous models
        model_a_probes = [p for p in probe_set.probes]
        model_b_probes = [p for p in probe_set.probes]
        model_c_probes = [p for p in probe_set.probes]

        model_a_ids = [p.probe_id for p in model_a_probes]
        model_b_ids = [p.probe_id for p in model_b_probes]
        model_c_ids = [p.probe_id for p in model_c_probes]

        # Verify probe IDs are strictly identical across models
        self.assertEqual(model_a_ids, model_b_ids)
        self.assertEqual(model_b_ids, model_c_ids)
        self.assertEqual(model_a_ids, model_c_ids)

        # Verify stimuli sentences and metadata match exactly
        for pa, pb, pc in zip(model_a_probes, model_b_probes, model_c_probes):
            self.assertEqual(pa.probe_id, pb.probe_id)
            self.assertEqual(pb.probe_id, pc.probe_id)
            self.assertEqual(pa.seed_text, pb.seed_text)
            self.assertEqual(pb.seed_text, pc.seed_text)
            self.assertEqual(pa.perturbed_text, pb.perturbed_text)
            self.assertEqual(pb.perturbed_text, pc.perturbed_text)
            self.assertEqual(pa.perturbation_type, pb.perturbation_type)
            self.assertEqual(pb.perturbation_type, pc.perturbation_type)
            self.assertEqual(pa.expected_semantic_effect, pb.expected_semantic_effect)
            self.assertEqual(pb.expected_semantic_effect, pc.expected_semantic_effect)
            self.assertEqual(pa.expected_flip, pb.expected_flip)
            self.assertEqual(pb.expected_flip, pc.expected_flip)


if __name__ == "__main__":
    unittest.main()
