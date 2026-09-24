import os
import sys
import argparse
import logging
import warnings

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Suppress third-party library deprecation noise
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from blindspot.audit import AuditPipeline, run_multimodel_audit
from blindspot.core.config import PerformanceMode, ExperimentConfig
from blindspot.execution.runner import ExperimentRunner
from blindspot.storage.run_store import RunStore

def main():
    parser = argparse.ArgumentParser(description="BlindSpot: Text Classifier Auditing Framework")
    parser.add_argument("--model", type=str, default=None, help="Single Hugging Face model ID or path (backward compatible)")
    parser.add_argument("--models", type=str, default=None, help="Comma-separated list of Hugging Face model IDs or paths")
    parser.add_argument("--sentence", type=str, default="The movie was great and the acting was top notch.", help="Input sentence to audit")
    parser.add_argument("--sentences", type=str, default=None, help="Comma-separated list of sentences to audit")
    parser.add_argument("--output-dir", type=str, default="audit_reports", help="Directory to save generated Markdown reports / runs")
    parser.add_argument("--explainer", type=str, default="lime", choices=["lime", "shap", "both", "none"], help="Explainer method (lime, shap, both, none)")
    parser.add_argument(
        "--performance-mode",
        type=str,
        default="balanced",
        choices=["balanced", "safe", "performance", "custom", "fast_debug", "default", "high_throughput", "low_memory"],
        help="Resource execution mode (balanced, safe, performance, custom, fast_debug)"
    )
    parser.add_argument("--batch-size", type=int, default=None, help="Inference batch size override")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    print("=" * 70)
    print("BlindSpot: Behavioral & Explainable-AI Framework for Auditing Text Classifiers")
    print("=" * 70)

    # Resolve target models
    target_models = []
    if args.models:
        target_models = [m.strip() for m in args.models.split(",") if m.strip()]
    elif args.model:
        target_models = [args.model.strip()]
    else:
        target_models = ["distilbert-base-uncased-finetuned-sst-2-english"]

    # Resolve sentences
    if args.sentences:
        sentences = [s.strip() for s in args.sentences.split(",") if s.strip()]
    else:
        sentences = [args.sentence]

    if len(target_models) == 1:
        # Preserve existing single-model output flow for full backward compatibility
        model_id = target_models[0]
        print(f"Target Model: {model_id}")
        print(f"Auditing Input: '{sentences[0]}'")
        pipeline = AuditPipeline(
            model_name_or_path=model_id,
            output_dir=args.output_dir,
            explainer_type=args.explainer if args.explainer != "none" else "lime",
        )
        results = pipeline.run_audit(sentences[0])

        print("\nAudit Execution Completed Successfully!")
        print(f"Prediction Flip Rate: {results['behavioral_results']['flip_rate']:.2%}")
        print(f"Total Detected Failures: {len(results['failures'])}")
        print(f"\nGenerated Diagnostic Reports in '{args.output_dir}':")
        for r in results['generated_reports']:
            print(f"  - {r}")
        print("=" * 70)
    else:
        # Multi-model audit workflow
        print(f"Target Models ({len(target_models)}): {', '.join(target_models)}")
        print(f"Auditing {len(sentences)} sentence(s) with performance mode: {args.performance_mode}")

        perf_mode = PerformanceMode.from_str(args.performance_mode)
        config = ExperimentConfig(
            model_ids=target_models,
            seed_texts=sentences,
            performance_mode=perf_mode,
            explainer_type=args.explainer,
            batch_size=args.batch_size,
        )

        runner = ExperimentRunner(config=config, run_store=RunStore(base_dir=args.output_dir))
        runner.events.on("log", lambda e: print(f"  [{e.data.get('level', 'INFO')}] {e.data.get('message', '')}"))

        print("\nExecuting multimodel audit...")
        results = runner.run_sync()

        print("\nMultimodel Audit Completed Successfully!")
        print(f"Experiment ID: {runner.experiment_id}")
        models_eval = results.get("models", {})
        for m_id, m_data in models_eval.items():
            eval_metrics = m_data.get("behavioral_metrics", {})
            print(f"  - Model: {m_id}")
            print(f"    Flip Rate: {eval_metrics.get('flip_rate', 0.0):.2%}")
            print(f"    Failures Detected: {len(m_data.get('failures', []))}")

        cross = results.get("cross_model_comparison", {})
        if cross:
            print(f"Cross-Model Agreement Rate: {cross.get('overall_agreement_rate', 0.0):.2%}")

        print(f"\nPersisted Experiment Artifacts saved in: {args.output_dir}/{runner.experiment_id}")
        print("=" * 70)

if __name__ == "__main__":
    main()
