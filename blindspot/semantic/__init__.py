"""
BlindSpot Semantic Reference & Verification Layer (v2.7.0).
Provides canonical semantic ground-truth references, structured Gemini verification,
persistent caching, human overrides, and 2-class/3-class alignment.
"""
from .types import (
    SemanticReferenceLabel,
    SemanticRelation,
    VerificationStatus,
    SemanticAnnotation,
    SemanticReferenceSet,
)
from .cache import SemanticAnnotationCache
from .client import GeminiSemanticClient
from .service import SemanticReferenceService, get_semantic_service
from .analyzer import ExactSentimentAnalyzer, get_exact_analyzer

__all__ = [
    "SemanticReferenceLabel",
    "SemanticRelation",
    "VerificationStatus",
    "SemanticAnnotation",
    "SemanticReferenceSet",
    "SemanticAnnotationCache",
    "GeminiSemanticClient",
    "SemanticReferenceService",
    "get_semantic_service",
    "ExactSentimentAnalyzer",
    "get_exact_analyzer",
]
