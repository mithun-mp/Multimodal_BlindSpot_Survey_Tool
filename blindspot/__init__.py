"""
BlindSpot: A Behavioral and Explainable-AI Framework for Auditing Text Classifiers
"""
import warnings

# Global warning suppression for third-party libraries (Transformers, SHAP, PyTorch)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

__version__ = "0.2.0"

from blindspot.audit import AuditPipeline, run_multimodel_audit
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.models.registry import ModelRegistry
from blindspot.models.cache import ModelCache
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
from blindspot.perturbations.shared import SharedProbeGenerator, infer_expected_semantic_effect
from blindspot.execution.resources import ResourceManager
from blindspot.execution.scheduler import AuditScheduler
from blindspot.execution.runner import ExperimentRunner
from blindspot.storage.run_store import RunStore
from blindspot.analysis.cross_model import CrossModelAnalyzer

__all__ = [
    "AuditPipeline",
    "run_multimodel_audit",
    "HuggingFaceWrapper",
    "ModelRegistry",
    "ModelCache",
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
    "SharedProbeGenerator",
    "infer_expected_semantic_effect",
    "ResourceManager",
    "AuditScheduler",
    "ExperimentRunner",
    "RunStore",
    "CrossModelAnalyzer",
]
