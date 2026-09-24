"""
BlindSpot: End-to-End Canonical 5-Model Acceptance Benchmark
Executes the acceptance experiment per Section 37 on:
    "All that glitters is not gold."
across all 5 fine-tuned sentiment models:
    1. distilbert-base-uncased-finetuned-sst-2-english
    2. textattack/albert-base-v2-SST-2
    3. cardiffnlp/twitter-roberta-base-sentiment-latest
    4. textattack/bert-base-uncased-SST-2
    5. cardiffnlp/twitter-roberta-base-sentiment

Evaluations: 5 baselines + (5 models * 4 selected probes) = 25 total evaluations.
Saves per-model incremental artifacts and all 15 publication figures.
"""
import sys
import os
import time
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from blindspot.core.config import ExperimentConfig
from blindspot.perturbations.shared import SharedProbeGenerator
from blindspot.execution.runner import ExperimentRunner
from blindspot.storage.run_store import RunStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger("AcceptanceBenchmark")


def main():
    print("=" * 70)
    print(" BLINDSPOT: 5-MODEL CANONICAL ACCEPTANCE BENCHMARK")
    print("=" * 70)

    seed_text = "All that glitters is not gold."
    print(f"[*] Seed sentence: \"{seed_text}\"")

    # 1. Generate 7 canonical probe candidates
    generator = SharedProbeGenerator()
    pset = generator.generate_probes([seed_text], candidate_count=7)
    print(f"[*] Probes generated: {len(pset.probes)} candidates")
    for i, p in enumerate(pset.probes, 1):
        eff = getattr(p.expected_effect, "value", str(p.expected_effect))
        print(f"    [{i}] ({p.perturbation_type}) \"{p.perturbed_text}\" -> Expected: {eff}")


    # 2. Select first 4 canonical probes
    selected_probes = pset.probes[:4]
    selected_ids = [p.probe_id for p in selected_probes]
    sel_set = pset.get_selected(selected_ids)
    print(f"[*] Probes selected: {len(sel_set.probes)} probes for execution:")
    for i, p in enumerate(sel_set.probes, 1):
        print(f"    [{i}] ID: {p.probe_id[:16]}... | \"{p.perturbed_text}\"")

    # 3. Configure 5-model run
    model_ids = [
        "distilbert-base-uncased-finetuned-sst-2-english",
        "textattack/albert-base-v2-SST-2",
        "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "textattack/bert-base-uncased-SST-2",
        "cardiffnlp/twitter-roberta-base-sentiment",
    ]
    print(f"[*] Target models: {len(model_ids)} sentiment classifiers")
    for m in model_ids:
        print(f"    - {m}")

    config = ExperimentConfig(
        experiment_name="Canonical 5-Model Acceptance Benchmark",
        seed_texts=[seed_text],
        model_ids=model_ids,
        selected_probe_set=sel_set,
        selected_probe_ids=selected_ids,
        explainer_type="both",
        output_dir="runs",
    )

    runner = ExperimentRunner(config=config)
    exp_id = runner.experiment_id
    print(f"[*] Experiment ID: {exp_id}")
    print(f"[*] Target Directory: runs/{exp_id}")

    # Wire progress logging
    def on_progress(data):
        pct = data.get("progress", 0.0) * 100
        step = data.get("step", "")
        print(f"    >>> [{pct:5.1f}%] {step}")

    def on_log(data):
        msg = data.get("message", "")
        lvl = data.get("level", "INFO")
        if lvl in ("WARNING", "ERROR"):
            print(f"    [{lvl}] {msg}")

    runner.events.on("progress", on_progress)
    runner.events.on("log", on_log)

    # Execute
    t0 = time.time()
    print("\n" + "-" * 70)
    print(" STARTING EXECUTION...")
    print("-" * 70)
    runner.run()
    elapsed = time.time() - t0

    print("\n" + "=" * 70)
    print(f" BENCHMARK COMPLETE (Total time: {elapsed:.2f}s / {elapsed/60:.2f}m)")
    print("=" * 70)

    # 4. Verify outputs and print audit summary
    run_store = RunStore(base_dir="runs")
    run_dir = run_store.get_run_dir(exp_id)
    print(f"[*] Run artifacts directory: {run_dir}")

    # Verify per-model persistence
    completed = run_store.list_completed_models(exp_id)
    print(f"[*] Completed models in store: {len(completed)}/{len(model_ids)}")

    total_evals = 0
    for m_id in model_ids:
        m_res = run_store.load_model_result(exp_id, m_id)
        if m_res:
            evals = m_res.get("evaluations") or m_res.get("predictions") or []
            timing = m_res.get("timing", {})
            dur = timing.get("total_duration_sec", 0.0)
            baseline_map = m_res.get("baseline", {})
            b_info = next(iter(baseline_map.values()), {}) if baseline_map else {}
            b_pred = b_info.get("prediction", {})
            b_label = b_pred.get("label", "N/A")
            b_conf = b_pred.get("confidence", 0.0)
            failures = m_res.get("failures") or m_res.get("taxonomy") or []
            total_evals += 1 + len(evals)  # 1 baseline + N probes
            print(f"\n  Model: {m_id}")
            print(f"    Duration: {dur:.2f}s")
            print(f"    Baseline: label={b_label} conf={b_conf:.3f}")
            print(f"    Probe evals: {len(evals)}")
            print(f"    Failures diagnosed: {len(failures)}")
            for f in failures:
                print(f"      - [{f.get('failure_category')}] Probe: \"{f.get('probe_text', '')[:40]}...\" Reason: {f.get('diagnostic_reason', '')[:60]}")
        else:
            print(f"  Model: {m_id} -> NOT FOUND IN STORE")

    print(f"\n[*] Total evaluations executed: {total_evals} (Expected: {len(model_ids) * (1 + len(selected_ids))} = 25)")


    # Verify figures
    figures_dir = os.path.join(run_dir, "figures")
    fig_files = [f for f in os.listdir(figures_dir) if f.endswith(".png")] if os.path.exists(figures_dir) else []
    print(f"[*] Publication figures generated: {len(fig_files)}/15")
    for f in sorted(fig_files):
        fp = os.path.join(figures_dir, f)
        sz = os.path.getsize(fp) / 1024
        print(f"    - {f} ({sz:.1f} KB)")

    source_data_file = os.path.join(figures_dir, "source_data.json")
    print(f"[*] Figure source data: {'EXISTS' if os.path.exists(source_data_file) else 'MISSING'}")

    # Summary json
    summary = {
        "experiment_id": exp_id,
        "seed_text": seed_text,
        "total_elapsed_seconds": elapsed,
        "models_completed": completed,
        "total_evaluations": total_evals,
        "figures_count": len(fig_files),
        "figures_source_data_present": os.path.exists(source_data_file),
    }
    with open(os.path.join(run_dir, "acceptance_benchmark_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 70)
    print(" ACCEPTANCE CRITERIA VERIFICATION:")
    print(f"  - 5 models executed: {'PASS' if len(completed) == 5 else 'FAIL'}")
    print(f"  - Exactly 25 evaluations: {'PASS' if total_evals == 25 else 'FAIL'}")
    print(f"  - 15 publication figures: {'PASS' if len(fig_files) >= 15 else 'FAIL'}")
    print(f"  - Per-model incremental persistence: {'PASS' if len(completed) == 5 else 'FAIL'}")
    print("=" * 70)


if __name__ == "__main__":
    main()
