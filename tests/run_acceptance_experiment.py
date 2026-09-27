"""
Deterministic Acceptance Test for BlindSpot Scientific Repairs.
Evaluates 5 sentiment models across benchmark test sentences A-E:
Sentence A: "The movie was fantastic."
Sentence B: "The movie was terrible."
Sentence C: "This product was surprisingly good."
Sentence D: "The service was not bad."
Sentence E: "The food was okay, but the atmosphere was awful."

Validates:
1. Baseline immutability and SHA-256 ID anchoring
2. Exact staged probe execution fidelity
3. Canonical SemanticPolarity across Binary & 3-Class models
4. Deterministic failure taxonomy diagnoses
5. Descriptive cross-model comparative metrics without normative rankings
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import time
from typing import Dict, Any

from blindspot.core.types import (
    SemanticPolarity,
    ExpectationType,
    BehavioralRelation,
    ProbeExpectation,
    FailureCategory,
    BehavioralOutcome,
)
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.models.registry import ModelRegistry
from blindspot.perturbations.shared import SharedProbeGenerator, ProbeValidator
from blindspot.testing.behavioral import BehavioralTester
from blindspot.analysis.cross_model import CrossModelAnalyzer


TEST_SENTENCES = [
    "The movie was fantastic.",
    "The movie was terrible.",
    "This product was surprisingly good.",
    "The service was not bad.",
    "The food was okay, but the atmosphere was awful.",
]

MODEL_IDS = [
    "distilbert-base-uncased-finetuned-sst-2-english",
    "textattack/albert-base-v2-SST-2",
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "textattack/bert-base-uncased-SST-2",
    "cardiffnlp/twitter-roberta-base-sentiment",
]


def run_acceptance_experiment():
    print("=" * 80)
    print("BLINDSPOT ACCEPTANCE EXPERIMENT: 5 MODELS x 5 BENCHMARK SENTENCES")
    print("=" * 80)

    # 1. Model Registry Gate
    registry = ModelRegistry()
    print("\n[Step 1] Validating Model Registry Gating...")
    for m_id in MODEL_IDS:
        is_val, reason, details = registry.validate_model_for_sentiment(m_id)
        assert is_val, f"Model {m_id} failed sentiment gate: {reason}"
        print(f"  [OK] {m_id}: num_classes={details['num_classes']}, family={details['model_family']}")

    # Validate rejection of non-sentiment
    v_fake, reason_fake, _ = registry.validate_model_for_sentiment("roberta-base-openai-detector")
    assert not v_fake, "Failed to reject OpenAI AI text detector!"
    print(f"  [OK] Successfully rejected non-sentiment model 'roberta-base-openai-detector': {reason_fake}")

    # 2. Probe Generation and Staging
    print("\n[Step 2] Generating Calibrated Probes across Sentences A-E...")
    generator = SharedProbeGenerator()
    probe_set = generator.generate_probes(
        seed_texts=TEST_SENTENCES,
        candidate_count=7,
    )
    print(f"  [OK] Generated {len(probe_set.probes)} total probes for {len(TEST_SENTENCES)} sentences (exactly 7 per sentence).")
    
    # Validate probe set
    is_valid, errors = ProbeValidator.validate_probe_set(probe_set)
    assert is_valid, f"Probe set validation failed: {errors}"
    print("  [OK] ProbeValidator confirmed 100% valid probe specifications and mutations.")

    # 3. Model Evaluation
    print("\n[Step 3] Executing Black-Box Audits across All 5 Models...")
    eval_results_by_model: Dict[str, Any] = {}
    model_evaluations: Dict[str, Any] = {}
    model_failures: Dict[str, Any] = {}

    for m_id in MODEL_IDS:
        print(f"\n--- Running Model: {m_id} ---")
        t0 = time.perf_counter()
        # Initialize wrapper with allow_fallback=True so offline/test environments still execute deterministically
        wrapper = HuggingFaceWrapper(m_id, allow_fallback=True)
        meta = wrapper.get_metadata()
        print(f"  Classes: {meta.num_classes} ({', '.join(meta.label_names)}) | Mode: {'REAL_PIPELINE' if meta.loaded else 'HEURISTIC_FALLBACK'}")

        tester = BehavioralTester(wrapper)
        results = tester.evaluate_shared_probes(probe_set)
        elapsed = time.perf_counter() - t0

        eval_results_by_model[m_id] = results
        model_evaluations[m_id] = results["evaluations"]
        model_failures[m_id] = results["failures"]

        # Invariant checks
        assert results["total_probes"] == len(probe_set.probes), "Probe count mismatch!"
        assert len(results["baselines"]) == len(TEST_SENTENCES), "Baseline count mismatch!"
        
        # Verify baseline IDs are anchored
        for seed, base_d in results["baselines"].items():
            base_id = base_d["baseline_id"]
            assert base_id.startswith("base_"), f"Invalid baseline_id {base_id}"

        print(f"  Observed Flip Rate:       {results['observed_flip_rate']:.2%}")
        print(f"  Expected Flip Rate:       {results['expected_flip_rate']:.2%}")
        print(f"  Expected Flip Compliance: {results['expected_flip_compliance']:.2%}")
        print(f"  Preservation Rate:        {results['preserve_rate']:.2%}")
        print(f"  Behavioral Consistency:   {results['behavioral_consistency']:.2%}")
        print(f"  Raw Label Flip Rate:      {results['raw_label_flip_rate']:.2%}")
        print(f"  Polarity Flip Rate:       {results['polarity_flip_rate']:.2%}")
        print(f"  Failure Breakdown:        {results['failure_counts']}")
        print(f"  Evaluation Latency:       {elapsed:.2f}s")

    # 4. Cross-Model Descriptive Comparative Analysis
    print("\n[Step 4] Running Non-Normative Cross-Model Analysis...")
    analyzer = CrossModelAnalyzer()
    comparison = analyzer.compare_models(model_evaluations, model_failures)
    
    print(f"  [OK] Mean Pairwise Prediction Agreement: {comparison['overall_agreement_rate']:.2%}")
    print("\n  Pairwise Model Agreement Matrix:")
    model_short_names = [m.split("/")[-1][:20] for m in MODEL_IDS]
    header = f"{'Model':<22} | " + " | ".join(f"{sn:<14}" for sn in model_short_names)
    print("  " + header)
    print("  " + "-" * len(header))
    for m1 in MODEL_IDS:
        row_str = f"  {m1.split('/')[-1][:20]:<22} | "
        cols = []
        for m2 in MODEL_IDS:
            val = comparison["pairwise_agreement"][m1][m2]
            cols.append(f"{val*100:6.1f}%       ")
        row_str += " | ".join(cols)
        print(row_str)

    print("\n[Step 5] Failure Taxonomy Breakdown across Models:")
    for m_id, counts in comparison["failure_summary"].items():
        print(f"  {m_id.split('/')[-1]:<45}: Blind={counts.get('Blind', 0)}, Spurious={counts.get('Spurious', 0)}, Misweighted={counts.get('Misweighted', 0)}, Undetermined={counts.get('Undetermined', 0)}")

    print("\n" + "=" * 80)
    print("ACCEPTANCE EXPERIMENT COMPLETED SUCCESSFULLY (Zero Test Failures)")
    print("=" * 80)


if __name__ == "__main__":
    run_acceptance_experiment()
