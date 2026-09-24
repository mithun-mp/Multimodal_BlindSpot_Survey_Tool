"""
Automated Test Suite for Calibrated Probe Suite and Proverb Support.
Verifies Section 11, 12, 13, 37 of the Research-Integrity Specification:
- Exact 7 calibrated diagnostic candidates
- Both expected-flip and expected-preserve stimulus coverage
- Proverb & figurative semantic preservation/inversion
- Probe contract validation and invalid probe rejection
"""
import unittest

from blindspot.core.types import (
    LinguisticProbe,
    SharedProbeSet,
    SentenceType,
    SemanticIntent,
)
from blindspot.perturbations.shared import SharedProbeGenerator, KNOWN_PROVERBS


class TestProbeCalibration(unittest.TestCase):
    """Verifies calibrated diagnostic probe generation and proverbial semantics."""

    def setUp(self):
        self.generator = SharedProbeGenerator()

    def test_calibrated_7_probes_literal_sentence(self):
        """Generates exactly 7 diagnostic candidates for literal sentence."""
        seed = "The movie was great and the acting was top notch."
        pset = self.generator.generate_probes([seed], candidate_count=7)
        self.assertEqual(len(pset.probes), 7)

        # Verify probe validity
        is_valid, errors = pset.validate()
        self.assertTrue(is_valid, f"Validation errors: {errors}")

        # Check balance: both flip and preserve must exist
        flip_probes = [p for p in pset.probes if p.expected_flip]
        preserve_probes = [p for p in pset.probes if not p.expected_flip]
        self.assertTrue(len(flip_probes) >= 1, "Must contain at least 1 expected-flip probe.")
        self.assertTrue(len(preserve_probes) >= 1, "Must contain at least 1 expected-preserve probe.")

        # Check intensity: strengthening and weakening
        strengthen_probes = [p for p in pset.probes if p.semantic_intent == SemanticIntent.STRENGTHEN_POLARITY.value]
        weaken_probes = [p for p in pset.probes if p.semantic_intent == SemanticIntent.WEAKEN_POLARITY.value]
        self.assertEqual(len(strengthen_probes), 1)
        self.assertEqual(len(weaken_probes), 1)

    def test_proverb_support_glitters(self):
        """
        Acceptance sentence per Section 12 & 37:
        'All that glitters is not gold.'
        """
        seed = "All that glitters is not gold."
        pset = self.generator.generate_probes([seed], candidate_count=7)
        self.assertEqual(len(pset.probes), 7)
        self.assertEqual(pset.sentence_types.get(seed), SentenceType.PROVERB.value)

        # 1. Proverb paraphrase must exist and be meaning-preserving
        paraphrase_probes = [p for p in pset.probes if "paraphrase" in p.perturbation_type or "paraphrase" in p.description.lower()]
        self.assertEqual(len(paraphrase_probes), 1)
        p_para = paraphrase_probes[0]
        self.assertIn("Not everything that glitters is truly valuable.", p_para.perturbed_text)
        self.assertFalse(p_para.expected_flip)
        self.assertEqual(p_para.semantic_intent, SemanticIntent.PRESERVE_MEANING.value)
        self.assertTrue(len(p_para.metadata.get("semantic_interpretation", "")) > 0)

        # 2. Proverb inversion (negation removal) must flip
        inversion_probes = [p for p in pset.probes if p.expected_flip]
        self.assertTrue(len(inversion_probes) >= 1)
        has_gold = any("All that glitters is gold" in p.perturbed_text for p in inversion_probes)
        self.assertTrue(has_gold)

        # Validation
        is_valid, errors = pset.validate()
        self.assertTrue(is_valid, f"Validation errors: {errors}")

    def test_probe_id_determinism(self):
        """Identical inputs produce identical probe IDs across generations."""
        seed = "The service at the restaurant was terrible and the food was cold."
        pset1 = self.generator.generate_probes([seed], candidate_count=7)
        pset2 = self.generator.generate_probes([seed], candidate_count=7)

        ids1 = [p.probe_id for p in pset1.probes]
        ids2 = [p.probe_id for p in pset2.probes]
        self.assertEqual(ids1, ids2)

    def test_invalid_probe_blocks_execution(self):
        """Invalid probe (identical text, missing effect, etc.) fails validate()."""
        invalid_probe = LinguisticProbe.create(
            seed_text="Same text",
            perturbed_text="Same text",
            perturbation_type="synonym",
            expected_semantic_effect="preserve",
            expected_flip=False,
        )
        is_valid, errors = invalid_probe.validate()
        self.assertFalse(is_valid)
        self.assertTrue(any("identical" in e.lower() for e in errors))

        # Check in SharedProbeSet
        bad_set = SharedProbeSet(
            probe_set_id="pset_bad",
            seed_texts=["Same text"],
            probes=[invalid_probe],
        )
        set_valid, set_errors = bad_set.validate()
        self.assertFalse(set_valid)


if __name__ == "__main__":
    unittest.main()
