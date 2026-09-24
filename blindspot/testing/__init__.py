"""
Testing module for BlindSpot framework.
Provides behavioral tester and statistical metrics.
"""
from .behavioral import BehavioralTester
from .metrics import (
    compute_flip_rate,
    compute_ece,
    compute_transition_matrix,
    compute_confidence_shifts,
    compute_prediction_agreement,
)

__all__ = [
    "BehavioralTester",
    "compute_flip_rate",
    "compute_ece",
    "compute_transition_matrix",
    "compute_confidence_shifts",
    "compute_prediction_agreement",
]
