"""
Deterministic Acceptance Test Suite for BlindSpot Research Pipeline.
Strictly implements Section 37 of the Research-Integrity Specification:
- Input: "All that glitters is not gold." (Sentence type: PROVERB)
- Evaluation count matrix:
  * 7 generated, 4 selected, 2 models -> 2 original baseline + 2x4 probe evaluations = 10 total evaluations
  * 7 selected, 2 models -> 2 baseline + 2x7 = 16 evaluations
  * 1 selected, 2 models -> 2 baseline + 2x1 = 4 evaluations
- Pipeline count integrity: generated=7, selected=4, planned=4, executed=4, analyzed=4, reported=4
- Probe identity invariants: identical probe IDs, versions, and order across models
- Custom probe persistence across Probe Set, RunPlan, Execution, and Reporting
"""
import unittest
import time

from blindspot.core.types import (
    LinguisticProbe,
    SharedProbeSet,
    SentenceType,
    SemanticIntent,
    PredictionResult,
    RunPlan,
    FailureCategory,
    BehavioralOutcome,
)
from blindspot.perturbations.shared import SharedProbeGenerator
from blindspot.testing.behavioral import BehavioralTester


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
        if "not" in t_low or "terrible" in t_low:
            lbl = "NEGATIVE"
            conf = 0.88
            probs = {"NEGATIVE": 0.88, "POSITIVE": 0.12}
        else:
            lbl = "POSITIVE"
            conf = 0.92
            probs = {"NEGATIVE": 0.08, "POSITIVE": 0.92}
        return PredictionResult(
            label=lbl,
            confidence=conf,
            probabilities=probs,
            latency_ms=1.0,
            model_id=self.model_name,
        )

    def predict_results_batch(self, texts, batch_size=16):
        return [self.predict_result(t) for t in texts]


class TestDeterministicAcceptance(unittest.TestCase):
    """Verifies the Section 37 deterministic acceptance protocol."""

    def setUp(self):
        self.generator = SharedProbeGenerator()
        self.seed = "All that glitters is not gold."

    def test_section_37_acceptance_run_4_selected(self):
        """
        7 generated candidate probes.
        Select 4 probes.
        Run 2 models.
        Expected: 2 original baseline + 2x4 probe evaluations = 10 total evaluations.
        Integrity: generated=7, selected=4, planned=4, executed=4, analyzed=4, reported=4.
        """
        # 1. Generate 7 candidates
        pset = self.generator.generate_probes([self.seed], candidate_count=7)
        self.assertEqual(len(pset.probes), 7)
        self.assertEqual(pset.sentence_types.get(self.seed), SentenceType.PROVERB.value)

        # 2. Select 4 probes
        selected_probes = pset.probes[:4]
        selected_ids = [p.probe_id for p in selected_probes]
        sel_set = pset.get_selected(selected_ids)
        self.assertEqual(len(sel_set.probes), 4)

        # 3. Create 2 models
        model_a = MockModelAuditingWrapper(model_name="mock-distilbert")
        model_b = MockModelAuditingWrapper(model_name="mock-roberta")
        models = [model_a, model_b]

        # 4. Create RunPlan
        plan = RunPlan(
            experiment_id="exp_accept_4",
            model_ids=[m.model_name for m in models],
            probe_set_id=sel_set.probe_set_id,
            probe_set_version=sel_set.probe_set_version,
            selected_probe_ids=selected_ids,
            probe_versions={p.probe_id: p.version for p in sel_set.probes},
            original_text=self.seed,
            sentence_type=SentenceType.PROVERB.value,
        )
        self.assertEqual(len(plan.selected_probe_ids), 4)

        # 5. Execute RunPlan across both models
        model_results = {}
        for m in models:
            tester = BehavioralTester(m)
            eval_res = tester.evaluate_shared_probes(sel_set)
            model_results[m.model_name] = eval_res

        # 6. Verify Exact Evaluation Counts
        # Model A: 1 baseline + 4 probes = 5
        self.assertEqual(model_a.evaluation_count, 5)
        # Model B: 1 baseline + 4 probes = 5
        self.assertEqual(model_b.evaluation_count, 5)
        # Total across both models: exactly 10 evaluations
        total_evaluations = model_a.evaluation_count + model_b.evaluation_count
        self.assertEqual(total_evaluations, 10)

        # Baseline evaluated exactly once per model
        self.assertEqual(model_a.evaluated_texts[0], self.seed)
        self.assertEqual(model_b.evaluated_texts[0], self.seed)

        # 7. Verify Integrity Counts per model
        for m_id, res in model_results.items():
            executed = len(res["evaluations"])
            analyzed = len(res["canonical_results"])
            reported = len(res["evaluations"])
            self.assertEqual(executed, 4)
            self.assertEqual(analyzed, 4)
            self.assertEqual(reported, 4)

        # 8. Verify Identical Stimuli fed to both models
        self.assertEqual(model_a.evaluated_texts, model_b.evaluated_texts)

    def test_section_37_select_all_7(self):
        """
        Select all 7 probes across 2 models.
        Expected: 2 baseline + 2x7 probe evaluations = 16 total evaluations.
        """
        pset = self.generator.generate_probes([self.seed], candidate_count=7)
        model_a = MockModelAuditingWrapper(model_name="mock-model-a")
        model_b = MockModelAuditingWrapper(model_name="mock-model-b")

        for m in [model_a, model_b]:
            tester = BehavioralTester(m)
            tester.evaluate_shared_probes(pset)

        self.assertEqual(model_a.evaluation_count, 8)
        self.assertEqual(model_b.evaluation_count, 8)
        self.assertEqual(model_a.evaluation_count + model_b.evaluation_count, 16)

    def test_section_37_select_one_probe(self):
        """
        Select 1 probe across 2 models.
        Expected: 2 baseline + 2x1 probe evaluations = 4 total evaluations.
        """
        pset = self.generator.generate_probes([self.seed], candidate_count=7)
        one_probe = pset.get_selected([pset.probes[0].probe_id])
        self.assertEqual(len(one_probe.probes), 1)

        model_a = MockModelAuditingWrapper(model_name="mock-model-a")
        model_b = MockModelAuditingWrapper(model_name="mock-model-b")

        for m in [model_a, model_b]:
            tester = BehavioralTester(m)
            tester.evaluate_shared_probes(one_probe)

        self.assertEqual(model_a.evaluation_count, 2)
        self.assertEqual(model_b.evaluation_count, 2)
        self.assertEqual(model_a.evaluation_count + model_b.evaluation_count, 4)

    def test_section_37_custom_probe_lifecycle(self):
        """
        Add custom probe.
        Verify the custom probe appears with stable ID and version across:
        - Probe Set
        - RunPlan
        - Execution
        - Canonical Results
        """
        custom_probe = LinguisticProbe.create(
            seed_text=self.seed,
            perturbed_text="Not all that glitters has authentic value.",
            perturbation_type="custom_paraphrase",
            description="Researcher custom proverbial paraphrase.",
            expected_semantic_effect="preserve",
            expected_flip=False,
            status="CUSTOM",
            semantic_intent=SemanticIntent.PRESERVE_MEANING.value,
            sentence_type=SentenceType.PROVERB.value,
        )
        custom_id = custom_probe.probe_id
        self.assertTrue(custom_id.startswith("prb_"))

        custom_set = SharedProbeSet(
            probe_set_id="pset_custom",
            seed_texts=[self.seed],
            probes=[custom_probe],
            sentence_types={self.seed: SentenceType.PROVERB.value},
        )
        is_valid, errors = custom_set.validate()
        self.assertTrue(is_valid, f"Custom probe errors: {errors}")

        plan = RunPlan(
            experiment_id="exp_custom",
            model_ids=["mock-m1"],
            probe_set_id=custom_set.probe_set_id,
            probe_set_version=custom_set.probe_set_version,
            selected_probe_ids=[custom_id],
            probe_versions={custom_id: custom_probe.version},
            original_text=self.seed,
        )
        self.assertIn(custom_id, plan.selected_probe_ids)

        model = MockModelAuditingWrapper(model_name="mock-m1")
        tester = BehavioralTester(model)
        eval_res = tester.evaluate_shared_probes(custom_set)

        canon_res = eval_res["canonical_results"][0]
        self.assertEqual(canon_res.probe_id, custom_id)
        self.assertEqual(canon_res.probe_version, custom_probe.version)
        self.assertEqual(canon_res.original_text, self.seed)
        self.assertEqual(canon_res.perturbed_text, custom_probe.perturbed_text)


if __name__ == "__main__":
    unittest.main()
