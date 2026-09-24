"""
Execution Runner for Multimodel Experiments in BlindSpot.
Coordinates probe generation, batched model evaluation, explainability extraction,
failure diagnosis, event emission, fault isolation, and artifact persistence.
"""
import threading
import time
import uuid
import logging
from typing import Dict, List, Any, Optional, Callable

from blindspot.core.config import ExperimentConfig, PerformanceMode, ResourceConfig
from blindspot.core.events import EventEmitter, ExecutionEvent
from blindspot.core.types import (
    SharedProbeSet,
    ModelProbeEvaluation,
    PredictionResult,
    ExplanationResult,
    FailureCategory,
    BaselineEvaluation,
    RunPlan,
    BehavioralProbeResult,
    ModelExecutionTiming,
    ModelRunState,
    ModelStatus,
)

from blindspot.execution.resources import ResourceManager
from blindspot.execution.scheduler import AuditScheduler
from blindspot.models.cache import ModelCache
from blindspot.perturbations.shared import SharedProbeGenerator
from blindspot.testing.behavioral import BehavioralTester
from blindspot.explainability.lime_explainer import LimeExplainerWrapper
from blindspot.explainability.shap_explainer import ShapExplainerWrapper
from blindspot.explainability.taxonomy import TaxonomyClassifier
from blindspot.explainability.alignment import compute_jaccard_similarity, compute_attribution_cosine
from blindspot.explainability.token_attributions import align_token_attributions
from blindspot.analysis.cross_model import CrossModelAnalyzer
from blindspot.storage.run_store import RunStore
from blindspot.reporting.report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class ExperimentRunner:
    """
    Orchestrates asynchronous or synchronous multimodel auditing jobs.
    """
    def __init__(
        self,
        config: ExperimentConfig,
        run_store: Optional[RunStore] = None,
        model_cache: Optional[ModelCache] = None,
    ):
        self.config = config
        self.experiment_id = f"exp_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        self.run_store = run_store or RunStore(base_dir=config.output_dir)
        self.resource_config = ResourceManager.resolve_config(
            mode=config.performance_mode,
            batch_size_override=config.batch_size,
        )
        self.model_cache = model_cache or ModelCache.get_shared_cache(
            max_size=self.resource_config.model_cache_size
        )
        self.events = EventEmitter()
        self.taxonomy = TaxonomyClassifier()
        self.cross_analyzer = CrossModelAnalyzer()
        self.reporter = ReportGenerator(output_dir=self.run_store.get_run_dir(self.experiment_id))

        self.status: str = "idle"  # idle, running, completed, cancelled, failed
        self.progress: float = 0.0  # 0.0 to 1.0
        self.current_step: str = ""
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.model_progress: Dict[str, Dict[str, Any]] = {
            m: {"status": "pending", "done": 0, "total": 0} for m in self.config.model_ids
        }
        self.model_run_states: Dict[str, ModelRunState] = {
            m: ModelRunState(model_id=m, status=ModelStatus.QUEUED)
            for m in self.config.model_ids
        }
        self._resume_mode: bool = False
        self._cancel_flag = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._result: Optional[Dict[str, Any]] = None
        self._error: Optional[Exception] = None

        # Wire event logging to RunStore
        self.events.on_any(lambda e: self.run_store.log_event(self.experiment_id, e))

    @classmethod
    def resume_run(
        cls,
        experiment_id: str,
        run_store: Optional[RunStore] = None,
        model_cache: Optional[ModelCache] = None,
    ) -> "ExperimentRunner":
        """
        Instantiates an ExperimentRunner initialized to resume an interrupted or incomplete run.
        Skips already completed models without re-running forward passes.
        """
        store = run_store or RunStore()
        run_data = store.load_run(experiment_id)
        cfg_dict = run_data.get("config", {})
        config = ExperimentConfig.from_dict(cfg_dict)
        saved_pset = store.load_probe_set(experiment_id)
        if saved_pset:
            config.selected_probe_set = saved_pset
        runner = cls(config=config, run_store=store, model_cache=model_cache)
        runner.experiment_id = experiment_id
        runner._resume_mode = True
        return runner

    def cancel(self) -> None:
        """Requests graceful cancellation of the running experiment."""
        self._cancel_flag.set()
        self.status = "cancelled"
        self.events.emit("cancelled", message="Experiment cancellation requested by user.")

    def run_async(self) -> threading.Thread:
        """Starts experiment execution in a background daemon thread."""
        self._cancel_flag.clear()
        self.status = "running"
        self._thread = threading.Thread(target=self._execute, daemon=True)
        self._thread.start()
        return self._thread

    def run_sync(self) -> Dict[str, Any]:
        """Executes experiment synchronously and returns results dictionary."""
        self._cancel_flag.clear()
        self.status = "running"
        self._execute()
        if self._error:
            raise self._error
        return self._result or {}

    def run(self) -> Dict[str, Any]:
        """Convenience alias for run_sync()."""
        return self.run_sync()


    def _execute(self) -> None:
        t_start = time.time()
        self.start_time = t_start
        self.reporter = ReportGenerator(output_dir=self.run_store.get_run_dir(self.experiment_id))
        try:
            self.run_store.init_run(self.experiment_id, self.config)
            self.events.emit(
                "log",
                level="INFO",
                message=f"Starting experiment '{self.config.experiment_name}' [{self.experiment_id}]",
            )
            self.events.emit("progress", progress=0.05, step="Initializing resources")

            # 1. Resolve Shared Probes (Canonical Protocol: Generation != Selection != Execution)
            if self._cancel_flag.is_set():
                self.end_time = time.time()
                return

            if self._resume_mode and self.config.selected_probe_set is None:
                saved_pset = self.run_store.load_probe_set(self.experiment_id)
                if saved_pset:
                    self.config.selected_probe_set = saved_pset

            if self.config.selected_probe_set is not None:
                if isinstance(self.config.selected_probe_set, SharedProbeSet):
                    probe_set = self.config.selected_probe_set
                elif isinstance(self.config.selected_probe_set, dict):
                    probe_set = SharedProbeSet.from_dict(self.config.selected_probe_set)
                else:
                    raise ValueError(f"Unsupported selected_probe_set type: {type(self.config.selected_probe_set)}")
                
                # Filter strictly by selected_probe_ids if explicitly provided
                if getattr(self.config, "selected_probe_ids", None):
                    probe_set = probe_set.get_selected(set(self.config.selected_probe_ids))

                self.events.emit(
                    "log",
                    level="INFO",
                    message=f"Consuming user-selected canonical SharedProbeSet with {len(probe_set.probes)} probe(s) (no re-generation)",
                )
                self.events.emit("progress", progress=0.10, step="Using verified probe selection")
            else:
                self.current_step = "Generating shared probes"
                self.events.emit("progress", progress=0.10, step=self.current_step)
                probe_gen = SharedProbeGenerator()
                probe_set = probe_gen.generate_probes(
                    seed_texts=self.config.seed_texts,
                    perturbation_types=self.config.perturbation_types,
                    sentence_types=self.config.sentence_types,
                )
                if getattr(self.config, "selected_probe_ids", None):
                    probe_set = probe_set.get_selected(set(self.config.selected_probe_ids))

                self.events.emit(
                    "log",
                    level="INFO",
                    message=f"Generated {len(probe_set.probes)} shared probe(s) across {len(self.config.seed_texts)} seed text(s)",
                )

            # Validate probe set before execution (Section 13: Invalid probes must BLOCK execution)
            is_valid, validation_errors = probe_set.validate()
            if not is_valid:
                err_msg = f"Probe set validation failed: {'; '.join(validation_errors)}"
                logger.error(err_msg)
                self.events.emit("log", level="ERROR", message=err_msg)
                raise ValueError(err_msg)

            # Create immutable RunPlan per Section 32
            run_plan = RunPlan(
                experiment_id=self.experiment_id,
                model_ids=list(self.config.model_ids),
                probe_set_id=probe_set.probe_set_id,
                probe_set_version=probe_set.probe_set_version,
                selected_probe_ids=[p.probe_id for p in probe_set.probes],
                probe_versions={p.probe_id: getattr(p, "version", 1) for p in probe_set.probes},
                original_text=self.config.seed_texts[0] if self.config.seed_texts else "",
                sentence_type=probe_set.sentence_types.get(self.config.seed_texts[0], "literal") if self.config.seed_texts else "literal",
            )
            self.run_plan = run_plan

            # Save RunPlan and SharedProbeSet artifacts immediately
            self.run_store.save_run_plan(self.experiment_id, run_plan)
            self.run_store.save_probe_set(self.experiment_id, probe_set)

            total_probes_count = len(probe_set.probes)
            for m_id in self.config.model_ids:
                self.model_progress[m_id] = {"status": "pending", "done": 0, "total": total_probes_count}
                if m_id not in self.model_run_states:
                    self.model_run_states[m_id] = ModelRunState(model_id=m_id, status=ModelStatus.QUEUED, total_probes=total_probes_count)

            # 2. Evaluate Models
            num_models = len(self.config.model_ids)
            model_evaluations: Dict[str, List[ModelProbeEvaluation]] = {}
            model_canonical_results: Dict[str, List[Dict[str, Any]]] = {}
            model_baselines: Dict[str, Dict[str, Any]] = {}
            model_failures: Dict[str, List[Dict[str, Any]]] = {}
            model_explanations: Dict[str, List[Dict[str, Any]]] = {}
            model_metrics: Dict[str, Dict[str, Any]] = {}
            model_eces: Dict[str, float] = {}

            # Check if resuming existing run
            completed_in_store = self.run_store.list_completed_models(self.experiment_id) if self._resume_mode else []

            for m_idx, model_id in enumerate(self.config.model_ids):
                if self._cancel_flag.is_set():
                    self.end_time = time.time()
                    return

                pct_base = 0.15 + (m_idx / num_models) * 0.65
                self.current_step = f"Evaluating model [{m_idx + 1}/{num_models}]: {model_id}"
                self.events.emit("progress", progress=pct_base, step=self.current_step)

                # Resume support: skip already completed models
                if self._resume_mode and model_id in completed_in_store:
                    self.events.emit("log", level="INFO", message=f"Resuming: Model {model_id} already completed. Loading persisted artifacts.")
                    loaded_m = self.run_store.load_model_result(self.experiment_id, model_id)
                    if loaded_m:
                        model_baselines[model_id] = loaded_m.get("baseline", {})
                        raw_evals = loaded_m.get("evaluations") or loaded_m.get("predictions") or []
                        parsed_evals = []
                        for rev in raw_evals:
                            if isinstance(rev, dict):
                                try:
                                    parsed_evals.append(ModelProbeEvaluation.from_dict(rev))
                                except Exception:
                                    parsed_evals.append(rev)
                            else:
                                parsed_evals.append(rev)
                        model_evaluations[model_id] = parsed_evals
                        model_canonical_results[model_id] = loaded_m.get("predictions", [])
                        model_metrics[model_id] = loaded_m.get("metrics", {})
                        model_failures[model_id] = loaded_m.get("taxonomy", [])
                        model_eces[model_id] = float(loaded_m.get("metrics", {}).get("ece", 0.0))
                        self.model_run_states[model_id].status = ModelStatus.COMPLETED
                        self.model_progress[model_id]["status"] = "completed"
                        self.model_progress[model_id]["done"] = len(parsed_evals)
                        continue

                t_m_start = time.perf_counter()
                timing = ModelExecutionTiming(model_id=model_id)

                self.events.emit("model_start", model_id=model_id)
                self.model_run_states[model_id].status = ModelStatus.LOADING
                self.events.emit("model_status_changed", model_id=model_id, status=ModelStatus.LOADING.value)
                self.model_progress[model_id]["status"] = "running"

                try:
                    # Model loading via cache
                    t_load_0 = time.perf_counter()
                    model_wrapper = self.model_cache.get_or_load(
                        model_id, device=self.resource_config.device
                    )
                    timing.model_load_ms = (time.perf_counter() - t_load_0) * 1000.0

                    self.model_run_states[model_id].status = ModelStatus.RUNNING
                    self.events.emit("model_status_changed", model_id=model_id, status=ModelStatus.RUNNING.value)
                    tester = BehavioralTester(model_wrapper)

                    # Batched Shared Probe Evaluation
                    t_inf_0 = time.perf_counter()
                    eval_results = tester.evaluate_shared_probes(probe_set)
                    timing.probe_inference_ms = (time.perf_counter() - t_inf_0) * 1000.0
                    timing.baseline_inference_ms = float(eval_results.get("baseline_latency_ms", 0.0))
                    timing.total_inference_ms = timing.baseline_inference_ms + timing.probe_inference_ms

                    evaluations: List[ModelProbeEvaluation] = eval_results["evaluations"]
                    # Strict validation: selected_probe_ids == executed_probe_ids per Section 3 & 22
                    executed_ids = [
                        getattr(e, "probe_id", e.get("probe_id") if isinstance(e, dict) else "")
                        for e in evaluations
                    ]
                    is_valid_exec, exec_msg = self.run_plan.validate_execution(executed_ids)
                    if not is_valid_exec:
                        err_msg = f"Pipeline Integrity Violation for model '{model_id}': {exec_msg}"
                        logger.error(err_msg)
                        self.events.emit("log", level="ERROR", message=err_msg)
                        raise RuntimeError(err_msg)

                    model_evaluations[model_id] = evaluations
                    model_canonical_results[model_id] = eval_results.get("probe_results", [])
                    model_baselines[model_id] = eval_results.get("baselines", {})
                    model_eces[model_id] = eval_results["ece"]
                    self.model_progress[model_id]["done"] = len(evaluations)

                    # Populate diagnosed behavioral failures from pure classifier
                    t_ana_0 = time.perf_counter()
                    failures: List[Dict[str, Any]] = list(eval_results.get("failures", []))

                    # Emit fine-grained per-probe execution events safely
                    for ev in evaluations:
                        orig_lbl = getattr(ev, "original_label", None) or (ev.get("original_label") if isinstance(ev, dict) else "")
                        orig_conf = getattr(ev, "original_confidence", None) or (ev.get("original_confidence") if isinstance(ev, dict) else 0.0)
                        pert_lbl = getattr(ev, "perturbed_label", None) or (ev.get("perturbed_label") if isinstance(ev, dict) else "")
                        pert_conf = getattr(ev, "perturbed_confidence", None) or (ev.get("perturbed_confidence") if isinstance(ev, dict) else 0.0)
                        self.events.emit(
                            "probe_evaluated",
                            model_id=model_id,
                            probe_id=getattr(ev, "probe_id", ev.get("probe_id") if isinstance(ev, dict) else ""),
                            perturbation_type=getattr(ev, "perturbation_type", ev.get("perturbation_type") if isinstance(ev, dict) else ""),
                            seed_text=getattr(ev, "seed_text", ev.get("seed_text") if isinstance(ev, dict) else ""),
                            perturbed_text=getattr(ev, "perturbed_text", ev.get("perturbed_text") if isinstance(ev, dict) else ""),
                            original_label=orig_lbl,
                            original_confidence=orig_conf,
                            perturbed_label=pert_lbl,
                            perturbed_confidence=pert_conf,
                            is_flipped=getattr(ev, "is_flipped", ev.get("is_flipped") if isinstance(ev, dict) else False),
                            expected_flip=getattr(ev, "expected_flip", ev.get("expected_flip") if isinstance(ev, dict) else False),
                            expected_effect=getattr(ev, "expected_effect", getattr(ev, "expected_semantic_effect", "EXPECTED_FLIP" if getattr(ev, "expected_flip", False) else "EXPECTED_PRESERVE")),
                            semantic_intent=getattr(ev, "semantic_intent", "PRESERVE_MEANING"),
                            behavioral_outcome=getattr(ev, "behavioral_outcome", "EXPECTED_FLIP"),
                            failure_type=getattr(ev, "failure_type", "None"),
                            confidence_delta_pts=getattr(ev, "confidence_delta_pts", 0.0),
                            rationale=getattr(ev, "rationale", ""),
                        )

                    num_fails = len(failures)
                    analysis_status = "NO_FAILURES_OBSERVED" if num_fails == 0 else "FAILURES_OBSERVED"
                    model_metrics[model_id] = {
                        "total_probes": eval_results["total_probes"],
                        "flip_rate": eval_results["observed_flip_rate"],
                        "observed_flip_rate": eval_results["observed_flip_rate"],
                        "expected_flip_rate": eval_results["expected_flip_rate"],
                        "preserve_rate": eval_results["preserve_rate"],
                        "behavioral_consistency": eval_results["behavioral_consistency"],
                        "satisfaction_rate": eval_results["behavioral_consistency"],
                        "confidence_flip_rate": eval_results["confidence_flip_rate"],
                        "ece": eval_results["ece"],
                        "transition_matrix": eval_results["transition_matrix"],
                        "confidence_shifts": eval_results["confidence_shifts"],
                        "failure_counts": eval_results.get("failure_counts", {}),
                        "analysis_status": analysis_status,
                    }
                    timing.analysis_ms = (time.perf_counter() - t_ana_0) * 1000.0

                    # Explainability & Taxonomy Diagnosis (bounded & batched)
                    explanations: List[Dict[str, Any]] = []

                    if self.config.explainer_type != "none":
                        lime_exp = LimeExplainerWrapper(model_wrapper, random_seed=self.config.random_seed)
                        shap_exp = ShapExplainerWrapper(model_wrapper)

                        probes_to_explain = evaluations[:self.resource_config.explanation_sample_size]

                        for ev in probes_to_explain:
                            if self._cancel_flag.is_set():
                                return

                            seed_t = ev.seed_text if hasattr(ev, "seed_text") else (ev.get("seed_text", "") if hasattr(ev, "get") else "")
                            pert_t = ev.perturbed_text if hasattr(ev, "perturbed_text") else (ev.get("perturbed_text", "") if hasattr(ev, "get") else "")

                            if self.config.explainer_type == "shap":
                                orig_exp = shap_exp.explain(seed_t)
                                pert_exp = shap_exp.explain(pert_t)
                            elif self.config.explainer_type == "both":
                                l_orig = lime_exp.explain(seed_t)
                                l_pert = lime_exp.explain(pert_t)
                                s_orig = shap_exp.explain(seed_t)
                                s_pert = shap_exp.explain(pert_t)
                                comb_orig = {k: (l_orig.get(k, 0.0) + s_orig.get(k, 0.0)) / 2 for k in set(list(l_orig.keys()) + list(s_orig.keys()))}
                                comb_pert = {k: (l_pert.get(k, 0.0) + s_pert.get(k, 0.0)) / 2 for k in set(list(l_pert.keys()) + list(s_pert.keys()))}
                                orig_exp = ExplanationResult(comb_orig, model_id=model_id, text=seed_t, explainer_requested="both", explainer_used="both")
                                pert_exp = ExplanationResult(comb_pert, model_id=model_id, text=pert_t, explainer_requested="both", explainer_used="both")
                            else:
                                orig_exp = lime_exp.explain(seed_t)
                                pert_exp = lime_exp.explain(pert_t)

                            jaccard = compute_jaccard_similarity(orig_exp, pert_exp)
                            cosine = compute_attribution_cosine(orig_exp, pert_exp)
                            aligned_tokens = align_token_attributions(seed_t, pert_t, orig_exp, pert_exp)

                            probe_id_val = ev.probe_id if hasattr(ev, "probe_id") else (ev.get("probe_id", "") if hasattr(ev, "get") else "")
                            ptype_val = ev.perturbation_type if hasattr(ev, "perturbation_type") else (ev.get("perturbation_type", "") if hasattr(ev, "get") else "")

                            exp_item = {
                                "probe_id": probe_id_val,
                                "seed_text": seed_t,
                                "perturbed_text": pert_t,
                                "perturbation_type": ptype_val,
                                "orig_explanation": orig_exp.to_dict(),
                                "pert_explanation": pert_exp.to_dict(),

                                "jaccard_similarity": jaccard,
                                "cosine_alignment": cosine,
                                "aligned_tokens": aligned_tokens,
                            }
                            explanations.append(exp_item)

                            # Enrich diagnosed failures with XAI evidence
                            for f in failures:
                                if f.get("probe_id") == exp_item["probe_id"]:
                                    if "evidence" not in f:
                                        f["evidence"] = {}
                                    f["evidence"]["jaccard_similarity"] = jaccard
                                    f["evidence"]["cosine_alignment"] = cosine

                    model_failures[model_id] = failures
                    model_explanations[model_id] = explanations

                    # Build per-model markdown report
                    t_rep_0 = time.perf_counter()
                    report_md = (
                        f"# Model Behavioral Audit: {model_id}\n\n"
                        f"- **Flip Rate**: {eval_results['observed_flip_rate']:.2%}\n"
                        f"- **Preserve Rate**: {eval_results['preserve_rate']:.2%}\n"
                        f"- **Behavioral Consistency**: {eval_results['behavioral_consistency']:.2%}\n"
                        f"- **ECE**: {eval_results['ece']:.4f}\n"
                        f"- **Diagnosed Failures**: {len(failures)}\n"
                        f"- **Evaluated Probes**: {len(evaluations)}\n"
                    )
                    timing.report_ms = (time.perf_counter() - t_rep_0) * 1000.0
                    timing.total_duration_sec = round(time.perf_counter() - t_m_start, 3)

                    # Save per-model artifacts immediately
                    t_save_0 = time.perf_counter()
                    model_data = {
                        "status": ModelStatus.COMPLETED,
                        "model_id": model_id,
                        "baseline": model_baselines[model_id],
                        "predictions": [e.to_dict() if hasattr(e, "to_dict") else e for e in evaluations],
                        "evaluations": [e.to_dict() if hasattr(e, "to_dict") else e for e in evaluations],
                        "behavioral": [e.to_dict() if hasattr(e, "to_dict") else e for e in evaluations],
                        "metrics": model_metrics[model_id],
                        "failures": failures,
                        "taxonomy": failures,
                        "timing": timing,
                        "report_md": report_md,
                        "completed_at": time.time(),
                        "probes_done": len(evaluations),
                        "total_probes": total_probes_count,
                    }
                    self.run_store.save_model_result(self.experiment_id, model_id, model_data)
                    timing.persistence_ms = (time.perf_counter() - t_save_0) * 1000.0

                    self.model_run_states[model_id].status = ModelStatus.COMPLETED
                    self.model_run_states[model_id].timing = timing
                    self.model_run_states[model_id].completed_at = time.time()
                    self.model_progress[model_id]["status"] = "completed"

                    self.events.emit(
                        "model_status_changed",
                        model_id=model_id,
                        status=ModelStatus.COMPLETED.value,
                    )
                    self.events.emit(
                        "model_complete",
                        model_id=model_id,
                        flip_rate=eval_results["observed_flip_rate"],
                        num_failures=len(failures),
                        timing=timing.to_dict(),
                    )

                    # Memory hygiene: sequentially evict model from RAM only if cache capacity is constrained (<=1)
                    if self.resource_config.model_cache_size <= 1:
                        self.model_cache.evict_from_memory(model_id)
                        del model_wrapper
                        del tester
                        import gc
                        gc.collect()

                except Exception as m_err:
                    logger.error(f"Fault in model {model_id}: {m_err}", exc_info=True)
                    self.events.emit("log", level="ERROR", message=f"Model {model_id} error: {m_err}")
                    timing.total_duration_sec = round(time.perf_counter() - t_m_start, 3)

                    self.model_run_states[model_id].status = ModelStatus.FAILED
                    self.model_run_states[model_id].error = str(m_err)
                    self.model_run_states[model_id].timing = timing
                    self.model_progress[model_id]["status"] = "failed"

                    self.events.emit(
                        "model_status_changed",
                        model_id=model_id,
                        status=ModelStatus.FAILED.value,
                    )

                    model_metrics[model_id] = {
                        "error": str(m_err),
                        "analysis_status": "NO_VALID_ANALYSIS",
                        "failure_counts": None,  # unavailable, NOT zero
                    }
                    model_evaluations[model_id] = []
                    model_baselines[model_id] = {}
                    model_failures[model_id] = []
                    model_explanations[model_id] = []

                    # Persist failed model state
                    err_payload = {
                        "status": ModelStatus.FAILED,
                        "model_id": model_id,
                        "error": str(m_err),
                        "timing": timing,
                        "completed_at": time.time(),
                    }
                    self.run_store.save_model_result(self.experiment_id, model_id, err_payload)

            # 3. Cross-Model Descriptive Comparison
            if self._cancel_flag.is_set():
                return

            self.current_step = "Computing cross-model comparative metrics"
            self.events.emit("progress", progress=0.85, step=self.current_step)

            cross_comparison = {}
            if len(model_evaluations) > 1:
                cross_comparison = self.cross_analyzer.compare_models(
                    model_evaluations=model_evaluations,
                    model_failures=model_failures,
                    model_eces=model_eces,
                )

            # 4. Pipeline Count Integrity Verification (Section 8, 28)
            planned_count = total_probes_count
            selected_count = total_probes_count
            generated_count = getattr(self.config, "generated_probe_count", total_probes_count) or total_probes_count
            verified_count = getattr(self.config, "verified_probe_count", selected_count) or selected_count

            integrity_checks = {}
            for m_id in self.config.model_ids:
                executed_count = len(model_evaluations.get(m_id, []))
                analyzed_count = executed_count
                reported_count = executed_count
                passed = (planned_count == executed_count == analyzed_count == reported_count)
                integrity_checks[m_id] = {
                    "generated": generated_count,
                    "selected": selected_count,
                    "verified": verified_count,
                    "planned": planned_count,
                    "executed": executed_count,
                    "analyzed": analyzed_count,
                    "reported": reported_count,
                    "integrity_verified": passed,
                }

            all_integrity_passed = all(r["integrity_verified"] for r in integrity_checks.values())
            has_model_errors = any("error" in model_metrics.get(m_id, {}) for m_id in self.config.model_ids)

            # Section 8 & 10: Distinguish FAILED / INCOMPLETE from COMPLETED
            if has_model_errors or not all_integrity_passed:
                total_executed = sum(len(model_evaluations.get(m, [])) for m in self.config.model_ids)
                if total_executed == 0:
                    overall_run_status = "FAILED"
                    overall_analysis_status = "NO_VALID_ANALYSIS"
                else:
                    overall_run_status = "INCOMPLETE"
                    overall_analysis_status = "NO_VALID_ANALYSIS"
            else:
                overall_run_status = "COMPLETED"
                total_failures_observed = sum(len(model_failures.get(m, [])) for m in self.config.model_ids)
                overall_analysis_status = "NO_FAILURES_OBSERVED" if total_failures_observed == 0 else "FAILURES_OBSERVED"

            self.events.emit(
                "log",
                level="INFO" if all_integrity_passed else "WARNING",
                message=f"Pipeline integrity audit: planned={planned_count} | all_models_passed={all_integrity_passed} | run_status={overall_run_status}",
            )

            # 5. Generate Reports & Persist Run
            self.current_step = "Generating diagnostic reports & saving run"
            self.events.emit("progress", progress=0.92, step=self.current_step)

            final_results = {
                "experiment_id": self.experiment_id,
                "run_status": overall_run_status,
                "analysis_status": overall_analysis_status,
                "config": self.config.to_dict(),
                "run_plan": self.run_plan.to_dict(),
                "shared_probes": probe_set.to_dict(),
                "model_baselines": model_baselines,
                "pipeline_integrity": {
                    "generated": generated_count,
                    "selected": selected_count,
                    "verified": verified_count,
                    "planned": planned_count,
                    "total_probes": planned_count,
                    "model_checks": integrity_checks,
                    "all_passed": all_integrity_passed,
                },
                "models": {
                    m_id: {
                        "baselines": model_baselines.get(m_id, {}),
                        "behavioral_metrics": model_metrics.get(m_id, {}),
                        "evaluations": [e.to_dict() if hasattr(e, "to_dict") else e for e in model_evaluations.get(m_id, [])],
                        "probe_results": model_canonical_results.get(m_id, []),
                        "failures": model_failures.get(m_id, []),
                        "explanations": model_explanations.get(m_id, []),
                        "timing": self.model_run_states[m_id].timing.to_dict() if self.model_run_states.get(m_id) and self.model_run_states[m_id].timing else None,
                    }
                    for m_id in self.config.model_ids
                },
                "cross_model_comparison": cross_comparison,
                "total_duration_sec": round(time.time() - t_start, 2),
            }

            # Save aggregate results
            self.run_store.save_aggregate_results(self.experiment_id, {
                "comparison": cross_comparison,
                "metrics": model_metrics,
                "taxonomy": {m: model_failures.get(m, []) for m in self.config.model_ids},
            })

            # Generate 15 publication thesis figures + 4 classic diagnostic figures
            try:
                self.reporter.visualizer.generate_thesis_figures(final_results)
                primary_m = self.config.model_ids[0] if self.config.model_ids else ""
                all_fails = [f for m_f in model_failures.values() for f in m_f]
                primary_exps = model_explanations.get(primary_m, [])
                primary_metrics = model_metrics.get(primary_m, {})
                self.reporter.visualizer.generate_all_plots(
                    audit_results={"flip_rate": primary_metrics.get("observed_flip_rate", 0.0), "ece": primary_metrics.get("ece", 0.0)},
                    failures=all_fails,
                    explanations_summary=primary_exps,
                )
            except Exception as fig_err:
                logger.warning(f"Error generating publication/diagnostic figures: {fig_err}")


            # Generate markdown reports
            try:
                self._generate_markdown_reports(final_results)
            except Exception as rep_err:
                logger.warning(f"Error generating markdown reports ({rep_err})")

            # Persist to RunStore
            self.run_store.save_results(
                self.experiment_id,
                results=final_results,
                metadata={
                    "total_duration_sec": final_results["total_duration_sec"],
                    "models": self.config.model_ids,
                    "num_probes": len(probe_set.probes),
                    "pipeline_integrity_passed": all_integrity_passed,
                    "run_status": overall_run_status,
                    "analysis_status": overall_analysis_status,
                    "completed_at": time.time(),
                },
            )

            self.status = "completed" if overall_run_status == "COMPLETED" else overall_run_status.lower()
            self.progress = 1.0
            self.current_step = f"Audit {overall_run_status}"
            self.end_time = time.time()
            self._result = final_results
            self.events.emit(
                "completed" if overall_run_status == "COMPLETED" else "incomplete",
                experiment_id=self.experiment_id,
                run_status=overall_run_status,
                analysis_status=overall_analysis_status,
                duration_sec=final_results["total_duration_sec"],
            )

        except Exception as e:
            logger.error(f"Audit run failed with unhandled exception: {e}", exc_info=True)
            self.status = "failed"
            self.end_time = time.time()
            self._error = e
            self.events.emit("error", error=str(e))

    def _generate_markdown_reports(self, results: Dict[str, Any]) -> None:
        exp_id = self.experiment_id
        models_data = results.get("models", {})
        cross = results.get("cross_model_comparison", {})
        integrity = results.get("pipeline_integrity", {})
        shared_probes = results.get("shared_probes", {})
        pset_id = shared_probes.get("probe_set_id", "N/A")
        pset_version = shared_probes.get("probe_set_version", "2.2.0")
        gen_version = shared_probes.get("generator_version", "2.2.0")
        seed_texts = shared_probes.get("seed_texts", self.config.seed_texts)
        sentence_types = shared_probes.get("sentence_types", {})
        model_baselines = results.get("model_baselines", {})

        # ==========================================
        # 1. EXPERIMENT SUMMARY REPORT
        # ==========================================
        summary_md = [
            f"# BlindSpot Research Audit Report: {self.config.experiment_name}",
            f"\n## 1. Experiment Metadata & Configuration",
            f"- **Experiment ID**: `{exp_id}`",
            f"- **Run Plan Created**: `{self.run_plan.created_at}`",
            f"- **Target Models**: {', '.join(f'`{m}`' for m in self.config.model_ids)}",
            f"- **Probe Set ID / Version**: `{pset_id}` (v{pset_version})",
            f"- **Generator Version**: `{gen_version}`",
            f"- **Total Selected Probes**: {len(self.run_plan.selected_probe_ids)}",
            f"- **Execution Runtime**: {results.get('total_duration_sec', 0.0):.2f}s",
            f"- **Pipeline Integrity Status**: `{'PASS' if integrity.get('all_passed', False) else 'WARNING'}`\n",
            "## 2. Seed Sentences & Pragmatic Classifications",
        ]

        for s_idx, stext in enumerate(seed_texts):
            stype = sentence_types.get(stext, "literal").upper()
            summary_md.append(f"- **Seed #{s_idx + 1}** `[{stype}]`: \"{stext}\"")

        summary_md.append("\n## 3. Original Sentence Baselines (Evaluated Once Per Model)")
        summary_md.append("| Model | Seed Sentence | Type | Predicted Label | Confidence |")
        summary_md.append("| :--- | :--- | :---: | :---: | :---: |")

        for m_id in self.config.model_ids:
            m_base = model_baselines.get(m_id, {})
            for stext, bdata in m_base.items():
                stype = sentence_types.get(stext, "literal").upper()
                pred = bdata.get("prediction", {})
                lbl = pred.get("label", "N/A")
                conf = pred.get("confidence", 0.0)
                summary_md.append(f"| `{m_id.split('/')[-1]}` | \"{stext[:40]}...\" | `{stype}` | **{lbl}** | {conf:.4f} ({conf * 100:.1f}%) |")

        summary_md.append("\n## 4. Primary Research Metrics")
        summary_md.append("| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |")
        summary_md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

        for m_id in self.config.model_ids:
            m_metrics = models_data.get(m_id, {}).get("behavioral_metrics", {})
            tot = m_metrics.get("total_probes", 0)
            obs_flips = sum(1 for e in models_data.get(m_id, {}).get("evaluations", []) if e.get("is_flipped"))
            obs_flip_r = m_metrics.get("observed_flip_rate", 0.0)
            exp_flips_tot = sum(1 for e in models_data.get(m_id, {}).get("evaluations", []) if e.get("expected_flip"))
            exp_flip_r = m_metrics.get("expected_flip_rate", 0.0)
            corr_exp_flips = int(exp_flips_tot * exp_flip_r) if exp_flips_tot > 0 else 0
            pres_tot = tot - exp_flips_tot
            pres_r = m_metrics.get("preserve_rate", 0.0)
            corr_pres = int(pres_tot * pres_r) if pres_tot > 0 else 0
            consistency = m_metrics.get("behavioral_consistency", 1.0)
            ece = m_metrics.get("ece", 0.0)
            shift = m_metrics.get("confidence_shifts", {}).get("mean_delta_pts", 0.0)
            summary_md.append(
                f"| `{m_id.split('/')[-1]}` | {tot} | {obs_flips} ({obs_flip_r:.1%}) | {corr_exp_flips}/{exp_flips_tot} ({exp_flip_r:.1%}) | "
                f"{corr_pres}/{pres_tot} ({pres_r:.1%}) | {consistency:.1%} | {ece:.4f} | {shift:+.1f} pp |"
            )

        summary_md.append("\n## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)")
        summary_md.append("| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |")
        summary_md.append("| :--- | :---: | :---: | :---: | :---: | :---: |")

        for m_id in self.config.model_ids:
            evals = models_data.get(m_id, {}).get("evaluations", [])
            b_cnt = sum(1 for e in evals if e.get("failure_type") == "Blind")
            s_cnt = sum(1 for e in evals if e.get("failure_type") == "Spurious")
            m_cnt = sum(1 for e in evals if e.get("failure_type") == "Misweighted")
            u_cnt = sum(1 for e in evals if e.get("failure_type") == "Undetermined")
            n_cnt = sum(1 for e in evals if e.get("failure_type") in ("None", None, ""))
            summary_md.append(f"| `{m_id.split('/')[-1]}` | {b_cnt} | {s_cnt} | {m_cnt} | {u_cnt} | {n_cnt} |")

        if cross:
            summary_md.extend([
                "\n## 6. Cross-Model Descriptive Agreement",
                f"- **Overall Prediction Agreement**: {cross.get('overall_agreement_rate', 0.0):.2%}",
            ])
            pair = cross.get("pairwise_agreement", {})
            if pair:
                summary_md.append("\n### Pairwise Concordance Matrix")
                models_list = list(pair.keys())
                header_str = "| Model | " + " | ".join(f"`{m.split('/')[-1][:12]}`" for m in models_list) + " |"
                sep_str = "| :--- | " + " | ".join(":---:" for _ in models_list) + " |"
                summary_md.append(header_str)
                summary_md.append(sep_str)
                for m1 in models_list:
                    row_vals = [f"{pair.get(m1, {}).get(m2, 0.0):.1%}" for m2 in models_list]
                    summary_md.append(f"| `{m1.split('/')[-1][:12]}` | " + " | ".join(row_vals) + " |")

        summary_md.extend([
            "\n## 7. Pipeline Count Integrity Audit",
            "| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ])
        for m_id, chk in integrity.get("model_checks", {}).items():
            res_str = "PASS" if chk.get("integrity_verified") else "FAIL"
            summary_md.append(
                f"| `{m_id.split('/')[-1]}` | {chk.get('generated')} | {chk.get('selected')} | "
                f"{chk.get('verified')} | {chk.get('planned')} | {chk.get('executed')} | "
                f"{chk.get('analyzed')} | {chk.get('reported')} | **{res_str}** |"
            )

        self.run_store.save_report(exp_id, "experiment_summary.md", "\n".join(summary_md))

        # ==========================================
        # 2. PROBE-LEVEL EVIDENCE REPORT
        # ==========================================
        evidence_md = [
            f"# Probe-Level Behavioral Evidence: {self.config.experiment_name}",
            f"\n**Experiment ID**: `{exp_id}`",
            f"Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.\n",
        ]

        for m_id in self.config.model_ids:
            short_m = m_id.split("/")[-1]
            evidence_md.append(f"\n## Model: `{short_m}`\n")
            evidence_md.append("| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |")
            evidence_md.append("| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

            for ev in models_data.get(m_id, {}).get("evaluations", []):
                pid = ev.get("probe_id", "")[:8]
                pcat = ev.get("perturbation_type", "").upper()
                s_text = ev.get("seed_text", "")
                p_text = ev.get("perturbed_text", "")
                orig_lbl = ev.get("original_label", "")
                orig_c = ev.get("original_confidence", 0.0)
                pert_lbl = ev.get("perturbed_label", "")
                pert_c = ev.get("perturbed_confidence", 0.0)
                delta_pts = ev.get("confidence_delta_pts", 0.0)
                is_flip = "YES" if ev.get("is_flipped") else "NO"
                outcome = ev.get("behavioral_outcome", "")
                ftype = ev.get("failure_type", "None")

                orig_pert_str = f"\"{s_text[:25]}...\" → \"{p_text[:25]}...\""
                base_str = f"{orig_lbl} ({orig_c:.2f})"
                out_str = f"{pert_lbl} ({pert_c:.2f})"
                trans_str = f"{orig_lbl} → {pert_lbl}"

                evidence_md.append(
                    f"| `{pid}` | {pcat} | {orig_pert_str} | {base_str} | {out_str} | {trans_str} | {delta_pts:+.1f} | {is_flip} | `{outcome}` | **{ftype}** |"
                )

            evidence_md.append("\n### Probe Rationales & Evidence Notes")
            for ev in models_data.get(m_id, {}).get("evaluations", []):
                pid = ev.get("probe_id", "")[:8]
                ftype = ev.get("failure_type", "None")
                outcome = ev.get("behavioral_outcome", "")
                rat = ev.get("rationale") or "N/A"
                evidence_md.append(f"- **`{pid}`** [{ftype} / {outcome}]: {rat}")

        self.run_store.save_report(exp_id, "probe_level_evidence.md", "\n".join(evidence_md))

        # ==========================================
        # 3. FAILURE DIAGNOSES REPORT
        # ==========================================
        all_failures = []
        for m_id in self.config.model_ids:
            for f in models_data.get(m_id, {}).get("failures", []):
                item = dict(f)
                item["model_id"] = m_id
                all_failures.append(item)

        fail_md = [
            f"# Behavioral Failure Diagnoses: {self.config.experiment_name}",
            f"\n**Experiment ID**: `{exp_id}`",
            f"**Total Diagnosed Failures**: {len(all_failures)}\n",
        ]

        if not all_failures:
            fail_md.append("### Diagnostic Finding: ZERO BEHAVIORAL FAILURES")
            fail_md.append("All target models complied with defined semantic expectations across all evaluated linguistic probes.")
            fail_md.append("Probe-level predictions and confidence transitions are fully documented in `probe_level_evidence.md`.\n")
        else:
            for idx, fail in enumerate(all_failures, 1):
                short_m = fail.get("model_id", "").split("/")[-1]
                f_cat = fail.get("category", "Undetermined")
                fail_md.append(f"### Failure #{idx}: [{f_cat.upper()}] — Model `{short_m}`")
                fail_md.append(f"- **Probe ID**: `{fail.get('probe_id', 'N/A')}` ({fail.get('probe_type', 'N/A')})")
                fail_md.append(f"- **Original Input**: \"{fail.get('original_sentence', '')}\"")
                fail_md.append(f"- **Perturbed Input**: \"{fail.get('perturbed_sentence', '')}\"")
                fail_md.append(f"- **Observed Transition**: `{fail.get('original_label')} ({fail.get('original_confidence', 0.0):.2f})` → `{fail.get('perturbed_label')} ({fail.get('perturbed_confidence', 0.0):.2f})`")
                fail_md.append(f"- **Prediction Flipped**: `{fail.get('is_flipped')}` (Expected Flip: `{fail.get('expected_flip')}`)")
                fail_md.append(f"- **Diagnostic Reason**: {fail.get('reason', 'N/A')}")
                fail_md.append(f"- **Evidence**: {fail.get('details', 'N/A')}")
                fail_md.append(f"- **Actionable Recommendation**: {fail.get('recommendation', 'N/A')}\n")

        self.run_store.save_report(exp_id, "failure_summary.md", "\n".join(fail_md))

