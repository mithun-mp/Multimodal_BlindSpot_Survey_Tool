"""
Core Module for BlindSpot Framework.
Exports foundational types, event systems, and configuration classes.
"""
from blindspot.core.types import (
    ModelMetadata,
    PredictionResult,
    LinguisticProbe,
    SharedProbeSet,
    ModelProbeEvaluation,
    ExplanationResult,
    FailureCategory,
    FailureDiagnosis,
)
from blindspot.core.events import ExecutionEvent, EventEmitter
from blindspot.core.config import PerformanceMode, ResourceConfig, ExperimentConfig
from blindspot.core.logging_config import configure_workstation_logging, get_subsystem_logger

__all__ = [
    "ModelMetadata",
    "PredictionResult",
    "LinguisticProbe",
    "SharedProbeSet",
    "ModelProbeEvaluation",
    "ExplanationResult",
    "FailureCategory",
    "FailureDiagnosis",
    "ExecutionEvent",
    "EventEmitter",
    "PerformanceMode",
    "ResourceConfig",
    "ExperimentConfig",
    "configure_workstation_logging",
    "get_subsystem_logger",
]
