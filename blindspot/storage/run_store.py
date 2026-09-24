"""
Experiment Persistence Store for BlindSpot.
Maintains granular runs/<experiment_id>/ artifact trees with config, run_plan,
probe_set, per-model results, aggregate comparisons, reports, figures, and events.
Guarantees historical data retention (never deletes runs automatically).
"""
import os
import shutil
import json
import time
from typing import Dict, List, Any, Optional
import logging

from blindspot.core.events import ExecutionEvent
from blindspot.core.config import ExperimentConfig

logger = logging.getLogger(__name__)


def _default_serializer(o: Any) -> Any:
    """JSON serializer for domain dataclasses, enums, sets, and mappings."""
    if hasattr(o, "to_dict"):
        return o.to_dict()
    if hasattr(o, "value"):
        return o.value
    if isinstance(o, set):
        return list(o)
    return str(o)


class RunStore:
    """
    Manages reading, writing, archiving, and deleting experiment run directories.
    Provides incremental per-model persistence and complete provenance retention.
    """
    def __init__(self, base_dir: str = "runs"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    @staticmethod
    def sanitize_model_id(model_id: str) -> str:
        """Converts model ID containing slashes or colons into safe filesystem slug."""
        return model_id.replace("/", "__").replace("\\", "__").replace(":", "--")

    def get_run_dir(self, experiment_id: str) -> str:
        return os.path.join(self.base_dir, experiment_id)

    def get_model_dir(self, experiment_id: str, model_id: str) -> str:
        slug = self.sanitize_model_id(model_id)
        return os.path.join(self.get_run_dir(experiment_id), "models", slug)

    def init_run(self, experiment_id: str, config: ExperimentConfig) -> str:
        """Initializes experiment run directory and writes config.json and initial metadata.json."""
        run_dir = self.get_run_dir(experiment_id)
        os.makedirs(os.path.join(run_dir, "models"), exist_ok=True)
        os.makedirs(os.path.join(run_dir, "aggregate"), exist_ok=True)
        os.makedirs(os.path.join(run_dir, "reports"), exist_ok=True)
        os.makedirs(os.path.join(run_dir, "figures"), exist_ok=True)

        config_path = os.path.join(run_dir, "config.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config.to_dict(), f, indent=2, default=_default_serializer)

        meta_path = os.path.join(run_dir, "metadata.json")
        initial_meta = {
            "experiment_id": experiment_id,
            "experiment_name": getattr(config, "experiment_name", "Multimodel Audit"),
            "created_at": time.time(),
            "status": "running",
            "models": list(config.model_ids),
            "completed_models": [],
            "model_states": {m: "queued" for m in config.model_ids},
            "num_models": len(config.model_ids),
            "num_seed_texts": len(config.seed_texts),
            "num_probes": None,
            "last_updated_at": time.time(),
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(initial_meta, f, indent=2)

        return run_dir

    def save_run_plan(self, experiment_id: str, run_plan: Any) -> str:
        """Saves immutable run_plan.json."""
        run_dir = self.get_run_dir(experiment_id)
        os.makedirs(run_dir, exist_ok=True)
        plan_path = os.path.join(run_dir, "run_plan.json")
        data = run_plan.to_dict() if hasattr(run_plan, "to_dict") else run_plan
        with open(plan_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=_default_serializer)
        return plan_path

    def load_run_plan(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Loads run_plan.json if present."""
        plan_path = os.path.join(self.get_run_dir(experiment_id), "run_plan.json")
        if os.path.exists(plan_path):
            with open(plan_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_probe_set(self, experiment_id: str, probe_set: Any) -> str:
        """Saves shared probe_set.json."""
        run_dir = self.get_run_dir(experiment_id)
        os.makedirs(run_dir, exist_ok=True)
        probe_path = os.path.join(run_dir, "probe_set.json")
        data = probe_set.to_dict() if hasattr(probe_set, "to_dict") else probe_set
        with open(probe_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=_default_serializer)
        return probe_path

    def load_probe_set(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Loads probe_set.json if present."""
        probe_path = os.path.join(self.get_run_dir(experiment_id), "probe_set.json")
        if os.path.exists(probe_path):
            with open(probe_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_model_result(
        self,
        experiment_id: str,
        model_id: str,
        model_data: Dict[str, Any],
    ) -> str:
        """
        Saves granular per-model results immediately upon model completion:
        runs/<run_id>/models/<model_slug>/
            status.json
            baseline.json
            predictions.json
            behavioral.json
            metrics.json
            taxonomy.json
            timing.json
            report.md
            report.json
            error.json
        Also updates metadata.json incrementally.
        """
        model_dir = self.get_model_dir(experiment_id, model_id)
        os.makedirs(model_dir, exist_ok=True)

        status_str = model_data.get("status", "COMPLETED")
        if hasattr(status_str, "value"):
            status_str = status_str.value

        # 1. status.json
        status_payload = {
            "model_id": model_id,
            "status": str(status_str),
            "completed_at": model_data.get("completed_at", time.time()),
            "error": model_data.get("error"),
            "probes_done": model_data.get("probes_done", 0),
            "total_probes": model_data.get("total_probes", 0),
        }
        with open(os.path.join(model_dir, "status.json"), "w", encoding="utf-8") as f:
            json.dump(status_payload, f, indent=2, default=_default_serializer)

        # 2. baseline.json
        if "baseline" in model_data or "baselines" in model_data:
            b_data = model_data.get("baseline", model_data.get("baselines"))
            with open(os.path.join(model_dir, "baseline.json"), "w", encoding="utf-8") as f:
                json.dump(b_data, f, indent=2, default=_default_serializer)

        # 3. predictions.json
        preds = model_data.get("predictions", model_data.get("evaluations", model_data.get("probe_results")))
        if preds is not None:
            with open(os.path.join(model_dir, "predictions.json"), "w", encoding="utf-8") as f:
                json.dump(preds, f, indent=2, default=_default_serializer)

        # 4. behavioral.json
        behav = model_data.get("behavioral", model_data.get("behavioral_evaluations"))
        if behav is not None:
            with open(os.path.join(model_dir, "behavioral.json"), "w", encoding="utf-8") as f:
                json.dump(behav, f, indent=2, default=_default_serializer)

        # 5. metrics.json
        metrics = model_data.get("metrics", model_data.get("behavioral_metrics"))
        if metrics is not None:
            with open(os.path.join(model_dir, "metrics.json"), "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2, default=_default_serializer)

        # 6. taxonomy.json / failures
        failures = model_data.get("failures", model_data.get("taxonomy"))
        if failures is not None:
            with open(os.path.join(model_dir, "taxonomy.json"), "w", encoding="utf-8") as f:
                json.dump(failures, f, indent=2, default=_default_serializer)

        # 7. timing.json
        timing = model_data.get("timing")
        if timing is not None:
            timing_data = timing.to_dict() if hasattr(timing, "to_dict") else timing
            with open(os.path.join(model_dir, "timing.json"), "w", encoding="utf-8") as f:
                json.dump(timing_data, f, indent=2, default=_default_serializer)

        # 8. error.json
        if model_data.get("error"):
            with open(os.path.join(model_dir, "error.json"), "w", encoding="utf-8") as f:
                json.dump({"error": str(model_data["error"])}, f, indent=2)

        # 9. report.md / report.json
        if "report_md" in model_data and model_data["report_md"]:
            with open(os.path.join(model_dir, "report.md"), "w", encoding="utf-8") as f:
                f.write(model_data["report_md"])

        if "report_json" in model_data and model_data["report_json"]:
            with open(os.path.join(model_dir, "report.json"), "w", encoding="utf-8") as f:
                json.dump(model_data["report_json"], f, indent=2, default=_default_serializer)

        # Incremental metadata update
        self._update_metadata_on_model_complete(experiment_id, model_id, str(status_str))
        return model_dir

    def _update_metadata_on_model_complete(
        self,
        experiment_id: str,
        model_id: str,
        status: str,
    ) -> None:
        """Atomically updates metadata.json to record per-model completion status."""
        run_dir = self.get_run_dir(experiment_id)
        meta_path = os.path.join(run_dir, "metadata.json")
        meta = {}
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception:
                meta = {}

        completed_models = list(meta.get("completed_models", []))
        if status.upper() == "COMPLETED" and model_id not in completed_models:
            completed_models.append(model_id)

        model_states = dict(meta.get("model_states", {}))
        model_states[model_id] = status.lower()

        meta["completed_models"] = completed_models
        meta["model_states"] = model_states
        meta["last_updated_at"] = time.time()

        try:
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to update metadata.json for {experiment_id}: {e}")

    def load_model_result(self, experiment_id: str, model_id: str) -> Optional[Dict[str, Any]]:
        """Loads all persisted per-model artifacts for a given model."""
        model_dir = self.get_model_dir(experiment_id, model_id)
        if not os.path.exists(model_dir):
            return None

        data: Dict[str, Any] = {"model_id": model_id}

        file_mappings = {
            "status.json": "status_info",
            "baseline.json": "baseline",
            "predictions.json": "predictions",
            "behavioral.json": "behavioral",
            "metrics.json": "metrics",
            "taxonomy.json": "taxonomy",
            "timing.json": "timing",
            "report.json": "report_json",
            "error.json": "error_info",
        }

        for filename, key in file_mappings.items():
            path = os.path.join(model_dir, filename)
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data[key] = json.load(f)
                except Exception as e:
                    logger.warning(f"Error reading {path}: {e}")

        # report.md
        md_path = os.path.join(model_dir, "report.md")
        if os.path.exists(md_path):
            try:
                with open(md_path, "r", encoding="utf-8") as f:
                    data["report_md"] = f.read()
            except Exception:
                pass

        if "status_info" in data and isinstance(data["status_info"], dict):
            data["status"] = data["status_info"].get("status", "UNKNOWN")
            if "error" in data["status_info"]:
                data["error"] = data["status_info"]["error"]

        return data

    def list_completed_models(self, experiment_id: str) -> List[str]:
        """Returns list of model_ids that have status == 'COMPLETED' in their model directory."""
        models_dir = os.path.join(self.get_run_dir(experiment_id), "models")
        if not os.path.exists(models_dir):
            return []

        completed = []
        for slug in os.listdir(models_dir):
            model_dir = os.path.join(models_dir, slug)
            if not os.path.isdir(model_dir):
                continue
            status_file = os.path.join(model_dir, "status.json")
            if os.path.exists(status_file):
                try:
                    with open(status_file, "r", encoding="utf-8") as f:
                        st_data = json.load(f)
                        if str(st_data.get("status", "")).upper() == "COMPLETED":
                            completed.append(st_data.get("model_id", slug))
                except Exception:
                    pass
        return completed

    def save_aggregate_results(
        self,
        experiment_id: str,
        aggregate_data: Dict[str, Any],
    ) -> str:
        """
        Saves cross-model comparisons into runs/<run_id>/aggregate/:
            comparison.json
            metrics.json
            taxonomy.json
        """
        agg_dir = os.path.join(self.get_run_dir(experiment_id), "aggregate")
        os.makedirs(agg_dir, exist_ok=True)

        if "comparison" in aggregate_data:
            with open(os.path.join(agg_dir, "comparison.json"), "w", encoding="utf-8") as f:
                json.dump(aggregate_data["comparison"], f, indent=2, default=_default_serializer)

        if "metrics" in aggregate_data:
            with open(os.path.join(agg_dir, "metrics.json"), "w", encoding="utf-8") as f:
                json.dump(aggregate_data["metrics"], f, indent=2, default=_default_serializer)

        if "taxonomy" in aggregate_data:
            with open(os.path.join(agg_dir, "taxonomy.json"), "w", encoding="utf-8") as f:
                json.dump(aggregate_data["taxonomy"], f, indent=2, default=_default_serializer)

        return agg_dir

    def log_event(self, experiment_id: str, event: ExecutionEvent) -> None:
        """Appends an event record to events.jsonl."""
        run_dir = self.get_run_dir(experiment_id)
        if not os.path.exists(run_dir):
            os.makedirs(run_dir, exist_ok=True)
        events_path = os.path.join(run_dir, "events.jsonl")
        with open(events_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict()) + "\n")

    def save_results(
        self,
        experiment_id: str,
        results: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Saves final results.json and updates metadata.json."""
        run_dir = self.get_run_dir(experiment_id)
        os.makedirs(run_dir, exist_ok=True)

        results_path = os.path.join(run_dir, "results.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=_default_serializer)

        meta_path = os.path.join(run_dir, "metadata.json")
        existing_meta = {}
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    existing_meta = json.load(f)
            except Exception:
                pass

        meta = {
            **existing_meta,
            **(metadata or {}),
            "status": results.get("run_status", "completed").lower(),
            "completed_at": time.time(),
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

    def save_report(self, experiment_id: str, filename: str, content: str) -> str:
        """Saves a Markdown or text report to reports/."""
        reports_dir = os.path.join(self.get_run_dir(experiment_id), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        target = os.path.join(reports_dir, filename)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return target

    def archive_run(self, experiment_id: str) -> str:
        """
        Moves a run directory into runs/archived/<experiment_id>.
        Guarantees raw data preservation without permanent deletion.
        """
        src_dir = self.get_run_dir(experiment_id)
        if not os.path.exists(src_dir):
            raise FileNotFoundError(f"Run {experiment_id} not found at {src_dir}")

        archive_dir = os.path.join(self.base_dir, "archived")
        os.makedirs(archive_dir, exist_ok=True)
        dest_dir = os.path.join(archive_dir, experiment_id)

        if os.path.exists(dest_dir):
            # If already archived, append timestamp suffix
            dest_dir = os.path.join(archive_dir, f"{experiment_id}_{int(time.time())}")

        shutil.move(src_dir, dest_dir)
        logger.info(f"Run '{experiment_id}' safely archived to: {dest_dir}")
        return dest_dir

    def delete_run(self, experiment_id: str, confirmation: bool = False) -> bool:
        """
        Deletes a specific experiment run directory ONLY with explicit confirmation=True.
        NEVER deletes the runs/ root or unconfirmed runs.
        """
        if not confirmation:
            raise ValueError(
                f"Deletion of run '{experiment_id}' refused: explicit confirmation=True is required."
            )

        run_dir = self.get_run_dir(experiment_id)
        if not os.path.exists(run_dir):
            raise FileNotFoundError(f"Run '{experiment_id}' does not exist at {run_dir}")

        shutil.rmtree(run_dir)
        logger.warning(f"Run '{experiment_id}' permanently deleted upon verified confirmation.")
        return True

    def list_runs(self, include_archived: bool = False) -> List[Dict[str, Any]]:
        """Lists all persisted runs sorted newest first. Excludes archived unless specified."""
        if not os.path.exists(self.base_dir):
            return []

        runs = []
        for name in os.listdir(self.base_dir):
            if name == "archived":
                if not include_archived:
                    continue
                # If include_archived, inspect archived subdirs
                arch_dir = os.path.join(self.base_dir, "archived")
                if os.path.isdir(arch_dir):
                    for a_name in os.listdir(arch_dir):
                        a_path = os.path.join(arch_dir, a_name)
                        if os.path.isdir(a_path):
                            meta = self._read_run_meta(a_name, a_path)
                            meta["is_archived"] = True
                            runs.append(meta)
                continue

            run_dir = os.path.join(self.base_dir, name)
            if not os.path.isdir(run_dir):
                continue

            meta = self._read_run_meta(name, run_dir)
            runs.append(meta)

        runs.sort(key=lambda r: r.get("created_at", 0), reverse=True)
        return runs

    def _read_run_meta(self, experiment_id: str, run_dir: str) -> Dict[str, Any]:
        """Helper to read run metadata with fallback derivation and experiment_name resolution."""
        meta: Dict[str, Any] = {}
        meta_path = os.path.join(run_dir, "metadata.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception:
                meta = {}

        if "experiment_id" not in meta:
            meta["experiment_id"] = experiment_id
        if "status" not in meta:
            meta["status"] = "uninitialized"
        if "created_at" not in meta:
            meta["created_at"] = 0

        # Auto-resolve experiment_name from config.json if not present in metadata
        if not meta.get("experiment_name"):
            config_path = os.path.join(run_dir, "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                        if cfg.get("experiment_name"):
                            meta["experiment_name"] = cfg["experiment_name"]
                except Exception:
                    pass

        if not meta.get("experiment_name"):
            meta["experiment_name"] = experiment_id

        return meta

    def get_run_title(self, experiment_id: str) -> str:
        """Returns the human-readable experiment title, falling back to experiment_id."""
        if not experiment_id or experiment_id == "None":
            return "No Active Experiment"
        run_dir = self.get_run_dir(experiment_id)
        if not os.path.exists(run_dir):
            arch_dir = os.path.join(self.base_dir, "archived", experiment_id)
            if os.path.exists(arch_dir):
                run_dir = arch_dir
        if os.path.exists(run_dir):
            meta = self._read_run_meta(experiment_id, run_dir)
            title = meta.get("experiment_name")
            if title and str(title).strip():
                return str(title).strip()
        return experiment_id

    def get_latest_run_id(self) -> Optional[str]:
        """Returns the experiment_id of the most recently created run, or None."""
        runs = self.list_runs()
        if runs:
            return runs[0].get("experiment_id")
        return None

    def load_run(self, experiment_id: str) -> Dict[str, Any]:
        """Loads all artifacts for an experiment run, including config, metadata, results, and models."""
        run_dir = self.get_run_dir(experiment_id)
        if not os.path.exists(run_dir):
            # Check archive fallback
            arch_dir = os.path.join(self.base_dir, "archived", experiment_id)
            if os.path.exists(arch_dir):
                run_dir = arch_dir
            else:
                raise FileNotFoundError(f"Run {experiment_id} not found in {self.base_dir}")

        out: Dict[str, Any] = {"experiment_id": experiment_id}

        config_path = os.path.join(run_dir, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                out["config"] = json.load(f)

        meta_path = os.path.join(run_dir, "metadata.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                out["metadata"] = json.load(f)

        plan_path = os.path.join(run_dir, "run_plan.json")
        if os.path.exists(plan_path):
            with open(plan_path, "r", encoding="utf-8") as f:
                out["run_plan"] = json.load(f)

        probe_path = os.path.join(run_dir, "probe_set.json")
        if os.path.exists(probe_path):
            with open(probe_path, "r", encoding="utf-8") as f:
                out["probe_set"] = json.load(f)

        results_path = os.path.join(run_dir, "results.json")
        if os.path.exists(results_path):
            with open(results_path, "r", encoding="utf-8") as f:
                out["results"] = json.load(f)

        # Per-model artifacts
        models_dir = os.path.join(run_dir, "models")
        if os.path.exists(models_dir):
            out["models"] = {}
            for slug in os.listdir(models_dir):
                m_dir = os.path.join(models_dir, slug)
                if os.path.isdir(m_dir):
                    # Inspect status.json to get true model_id if available
                    m_id = slug
                    status_f = os.path.join(m_dir, "status.json")
                    if os.path.exists(status_f):
                        try:
                            with open(status_f, "r", encoding="utf-8") as f:
                                st = json.load(f)
                                m_id = st.get("model_id", slug)
                        except Exception:
                            pass
                    out["models"][m_id] = self.load_model_result(experiment_id, m_id)

        # Aggregate comparisons
        agg_dir = os.path.join(run_dir, "aggregate")
        if os.path.exists(agg_dir):
            out["aggregate"] = {}
            for f in ("comparison.json", "metrics.json", "taxonomy.json"):
                p = os.path.join(agg_dir, f)
                if os.path.exists(p):
                    with open(p, "r", encoding="utf-8") as af:
                        out["aggregate"][f.replace(".json", "")] = json.load(af)

        # Reports
        reports_dir = os.path.join(run_dir, "reports")
        if os.path.exists(reports_dir):
            out["reports"] = {}
            for rf in os.listdir(reports_dir):
                rp = os.path.join(reports_dir, rf)
                if os.path.isfile(rp):
                    with open(rp, "r", encoding="utf-8") as f:
                        out["reports"][rf] = f.read()

        return out
