"""
Audit Scheduler for Multimodel Experiments in BlindSpot.
Optimizes execution sequence using model locality to eliminate cache thrashing.
"""
from dataclasses import dataclass
from typing import List, Dict, Any

from blindspot.core.config import ExperimentConfig


@dataclass
class ScheduledTask:
    task_id: str
    task_type: str  # probe_generation, model_evaluation, model_explanation, cross_model_analysis, reporting
    model_id: str = ""
    description: str = ""


class AuditScheduler:
    """
    Schedules experiment stages and model evaluation batches.
    """
    def __init__(self, config: ExperimentConfig):
        self.config = config

    def create_plan(self) -> List[ScheduledTask]:
        """
        Creates an ordered sequence of tasks minimizing model reloading.
        """
        tasks: List[ScheduledTask] = []

        # 1. Shared probe generation
        tasks.append(
            ScheduledTask(
                task_id="task_probe_gen",
                task_type="probe_generation",
                description=f"Generate shared linguistic probes across {len(self.config.seed_texts)} seed text(s)",
            )
        )

        # 2. Per-model evaluation & explanations (model-locality ordered)
        for idx, model_id in enumerate(self.config.model_ids):
            tasks.append(
                ScheduledTask(
                    task_id=f"task_eval_model_{idx}",
                    task_type="model_evaluation",
                    model_id=model_id,
                    description=f"Run batched behavioral evaluation for model '{model_id}'",
                )
            )
            if self.config.explainer_type != "none":
                tasks.append(
                    ScheduledTask(
                        task_id=f"task_explain_model_{idx}",
                        task_type="model_explanation",
                        model_id=model_id,
                        description=f"Generate token explanations and diagnoses for model '{model_id}'",
                    )
                )

        # 3. Cross-model analysis
        if len(self.config.model_ids) > 1:
            tasks.append(
                ScheduledTask(
                    task_id="task_cross_model",
                    task_type="cross_model_analysis",
                    description="Compute cross-model agreement, Model x Probe matrix, and failure breakdown",
                )
            )

        # 4. Final Reporting & Persistence
        tasks.append(
            ScheduledTask(
                task_id="task_persistence",
                task_type="reporting",
                description="Persist experiment results and generate Markdown audit reports",
            )
        )

        return tasks
