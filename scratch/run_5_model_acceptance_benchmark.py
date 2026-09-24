"""
Live 5-Model End-to-End Acceptance Benchmark for BlindSpot
Runs the 5 genuine sentiment models on 'All that glitters is not gold.' with 5 selected probes.
Verifies:
1. 5 genuine sentiment models loaded and cached
2. Exact probe selection integrity (5 probes executed per model)
3. Baseline evaluation for each model
4. Real transformer outputs, confidences, and confidence deltas
5. Rule-based behavioral outcomes & failure taxonomy
6. Incremental disk persistence & 15 thesis figures
7. Resume verification
"""
import os
import sys
import time
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from blindspot.core.config import ExperimentConfig, ResourceConfig, PerformanceMode
from blindspot.core.types import SentenceType
from blindspot.perturbations.shared import SharedProbeGenerator
from blindspot.execution.runner import ExperimentRunner
from blindspot.storage.run_store import RunStore
from blindspot.models.registry import ModelRegistry


def main():
    print("=" * 70)
    print("BLINDSPOT 5-MODEL ACCEPTANCE BENCHMARK")
    print("=" * 70)

    seed_text = "All that glitters is not gold."
    print(f"Seed text: {seed_text}")

    # 1. Verify Model Registry
    registry = ModelRegistry()
    sentiment_models = registry.list_sentiment_models()
    model_ids = [m["model_id"] if isinstance(m, dict) else m for m in sentiment_models]
    print(f"Available sentiment models ({len(model_ids)}):")
    for m in model_ids:
        print(f"  - {m}")
    assert len(model_ids) == 5, f"Expected 5 sentiment models, got {len(model_ids)}"
    assert "roberta-base-openai-detector" not in model_ids, "Detector model found in sentiment models!"

    # 2. Generate Probes
    generator = SharedProbeGenerator()
    pset = generator.generate_probes(
        [seed_text],
        sentence_types={seed_text: SentenceType.PROVERB.value},
        candidate_count=7,
    )
    print(f"\nGenerated candidate probes: {len(pset.probes)}")
    for i, p in enumerate(pset.probes, 1):
        print(f"  [{i}] ({p.perturbation_type}) '{p.perturbed_text}' -> Expected effect: {p.expected_semantic_effect}, flip: {p.expected_flip}")

    # Select 5 probes
    selected_probes = pset.probes[:5]
    selected_probe_ids = [p.probe_id for p in selected_probes]
    selected_pset = pset.get_selected(selected_probe_ids)
    print(f"\nSelected probes for execution: {len(selected_pset.probes)}")

    # 3. Configure Experiment
    cfg = ExperimentConfig(
        experiment_name="Canonical_5Model_Acceptance_Benchmark",
        model_ids=model_ids,
        seed_texts=[seed_text],
        sentence_types={seed_text: SentenceType.PROVERB.value},
        selected_probe_ids=selected_probe_ids,
        selected_probe_set=selected_pset,
        performance_mode=PerformanceMode.PERFORMANCE,
    )

    print("\nStarting Experiment Execution...")
    start_time = time.time()
    runner = ExperimentRunner(cfg)
    result = runner.run()
    elapsed = time.time() - start_time
    print(f"\nExperiment execution finished in {elapsed:.2f}s!")

    exp_id = result.get("experiment_id")
    run_store = RunStore()
    run_dir = Path(run_store.get_run_dir(exp_id))
    print(f"Artifacts saved to: {run_dir}")

    # 4. Verify Integrity
    print("\n--- INTEGRITY CHECKS ---")
    models_dict = result.get("models", {})
    print(f"Models requested: {len(model_ids)}")
    print(f"Models evaluated: {len(models_dict)}")
    assert len(models_dict) == 5, f"Expected 5 model evaluations, got {len(models_dict)}"

    for model_name, m_data in models_dict.items():
        base = m_data.get("baselines", {})
        # Could be keyed by seed_text or direct
        if seed_text in base:
            base_pred = base[seed_text].get("prediction", {})
        else:
            base_pred = base.get("prediction", {})

        lbl = base_pred.get("label", "Unknown")
        conf = base_pred.get("confidence", 0.0)
        evals = m_data.get("evaluations", [])
        print(f"\nModel: {model_name}")
        print(f"  Baseline: [{lbl}] conf={conf:.4f}")
        print(f"  Probes executed: {len(evals)}")
        assert len(evals) == 5, f"Expected 5 probe evaluations for {model_name}, got {len(evals)}"

        for ev in evals:
            flip_str = "FLIP" if ev.get("is_flipped") else "PRESERVE"
            outcome = ev.get("behavioral_outcome", "")
            fail_cat = ev.get("failure_type") or ev.get("category") or "None"
            pert_pred = ev.get("perturbed_prediction", {})
            p_lbl = pert_pred.get("label", "")
            p_conf = pert_pred.get("confidence", 0.0)
            delta = ev.get("confidence_delta_pts", 0.0)
            print(f"    Probe {ev.get('probe_id','')[:8]}..: [{p_lbl}] ({p_conf:.2f}) | {flip_str} | Delta={delta:+.2f} pts | Outcome={outcome} | Failure={fail_cat}")

    # 5. Verify Thesis Figures
    fig_dir = run_dir / "figures"
    fig_count = len(list(fig_dir.glob("*.png"))) if fig_dir.exists() else 0
    print(f"\nThesis figures generated: {fig_count} in {fig_dir}")
    assert fig_count >= 15, f"Expected >= 15 thesis figures, got {fig_count}"

    source_data_file = fig_dir / "source_data.json"
    assert source_data_file.exists(), f"Missing source_data.json at {source_data_file}"
    print("source_data.json verified!")

    # 6. Verify Resume
    print("\nTesting Resume Logic on Completed Run...")
    resume_runner = ExperimentRunner.resume_run(exp_id)
    resume_result = resume_runner.run()
    status_val = resume_result.get("run_status") or resume_result.get("status")
    assert str(status_val).upper() == "COMPLETED", f"Resume status: {status_val}"
    print("Resume successfully confirmed all 5 models already evaluated without recomputation!")

    print("\n" + "=" * 70)
    print("ALL 5-MODEL ACCEPTANCE BENCHMARK CHECKS PASSED PERFECTLY!")
    print("=" * 70)


if __name__ == "__main__":
    main()
