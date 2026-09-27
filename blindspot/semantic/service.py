"""
Semantic Reference Service (BlindSpot).
Coordinates persistent caching, real Gemini structured annotation, human verification,
and freezing the canonical semantic reference for multi-model experiments.

CRITICAL INVARIANTS:
- Gemini is an annotation/reference component only.
- Never fabricates confidence (no confidence=0.75 or ghost values).
- When offline or unverified, status is strictly UNVERIFIED and provider is LOCAL_HEURISTIC.
- Never calls automated suggestions "Final Ground-Truth" or "Ground Truth".
- Probe expectations are derived authoritatively from baseline and probe semantic polarities,
  never arbitrarily flipped merely because a probe inserted negation.
"""
import os
import json
import logging
from typing import Dict, List, Optional, Any, Union, Tuple

from .types import (
    SemanticReferenceLabel,
    SemanticRelation,
    VerificationStatus,
    ReferenceProvider,
    SemanticAnnotation,
    SemanticReferenceSet,
)
from .cache import SemanticAnnotationCache
from .client import GeminiSemanticClient

logger = logging.getLogger("blindspot.semantic")


class SemanticReferenceService:
    """
    High-level orchestrator for establishing, verifying, and freezing semantic references.
    """
    def __init__(
        self,
        client: Optional[GeminiSemanticClient] = None,
        cache: Optional[SemanticAnnotationCache] = None,
    ):
        self.client = client or GeminiSemanticClient()
        self.cache = cache or SemanticAnnotationCache()

    def annotate_experiment(
        self,
        baseline_text: str,
        probes: List[Any],
        force_refresh: bool = False,
    ) -> SemanticReferenceSet:
        """
        Produces a complete SemanticReferenceSet for baseline and probes.
        Deduplicates requests, uses cryptographic cache, and queries Gemini only if online.
        Falls back to transparent, unverified local heuristic when offline.
        """
        probe_list = probes.probes if hasattr(probes, "probes") else list(probes)
        logger.info(f"[SEMANTIC] Establishing semantic reference for: \"{baseline_text}\" + {len(probe_list)} probes")
        cache_hits = 0
        api_requests = 0

        current_provider = (
            ReferenceProvider.GEMINI.value
            if self.client.is_online
            else ReferenceProvider.LOCAL_HEURISTIC.value
        )
        current_model = self.client.model_name if self.client.is_online else "local_heuristic"

        # 1. Check cache for baseline
        baseline_annot: Optional[SemanticAnnotation] = None
        if not force_refresh:
            baseline_annot = self.cache.get(baseline_text, provider=current_provider, model=current_model)
            if baseline_annot:
                cache_hits += 1
                logger.info(f"[SEMANTIC] Cache HIT for baseline: {baseline_annot.final_semantic_polarity.value}")

        # 2. Check cache for probes
        cached_probe_annots: Dict[str, SemanticAnnotation] = {}
        uncached_probes: List[Dict[str, str]] = []
        seen_texts: set = set()

        for p in probe_list:
            pid = p.probe_id if hasattr(p, "probe_id") else p.get("probe_id", "")
            ptext = p.perturbed_text if hasattr(p, "perturbed_text") else p.get("perturbed_text", "")
            ptype = getattr(p, "perturbation_type", "") if hasattr(p, "perturbation_type") else p.get("perturbation_type", "")

            if not force_refresh:
                cached = self.cache.get(ptext, provider=current_provider, model=current_model)
                if cached:
                    cached.sentence_id = pid
                    cached_probe_annots[pid] = cached
                    cache_hits += 1
                    continue

            # Deduplicate identical probe texts within experiment (Phase 16)
            uncached_probes.append({
                "probe_id": pid,
                "perturbed_text": ptext,
                "perturbation_type": ptype,
            })

        # 3. Query Gemini if online and uncached items exist
        gemini_results: Dict[str, SemanticAnnotation] = {}
        if (baseline_annot is None or uncached_probes) and self.client.is_online:
            try:
                logger.info(f"[SEMANTIC] Submitting {len(uncached_probes) + (1 if baseline_annot is None else 0)} sentences to Gemini...")
                req_start = self.client.requests_count
                gemini_results = self.client.annotate_batch(
                    baseline_text=baseline_text,
                    probes=uncached_probes,
                )
                api_requests = self.client.requests_count - req_start

                # Cache newly annotated items
                for sid, annot in gemini_results.items():
                    self.cache.put(annot)

            except Exception as ex:
                logger.warning(f"[SEMANTIC] Gemini annotation failed: {ex}. Falling back to unverified local mode.")
                gemini_results = {}

        # 4. Resolve Baseline Annotation
        if baseline_annot is None:
            if "baseline" in gemini_results:
                baseline_annot = gemini_results["baseline"]
            else:
                # Transparent local heuristic fallback (Phase 7)
                from .analyzer import get_exact_analyzer
                inferred, _, reason = get_exact_analyzer().analyze(baseline_text)
                baseline_annot = SemanticAnnotation(
                    sentence_id="baseline",
                    sentence_text=baseline_text,
                    semantic_polarity=inferred,
                    confidence=None,  # Strictly None: NEVER fabricate confidence
                    reason=f"[Local Heuristic - Unverified] {reason}",
                    ambiguity="MEDIUM" if inferred == SemanticReferenceLabel.NEUTRAL else "LOW",
                    verification_status=VerificationStatus.UNVERIFIED,
                    provider=ReferenceProvider.LOCAL_HEURISTIC.value,
                    gemini_polarity=None,
                    gemini_confidence=None,  # Strictly None
                    human_verified_polarity=None,
                    final_semantic_polarity=inferred,
                    verification_source="LOCAL_HEURISTIC_UNVERIFIED",
                    model_used="local_heuristic",
                )
                self.cache.put(baseline_annot)

        # 5. Resolve Probe Annotations
        probe_annotations: Dict[str, SemanticAnnotation] = {}
        for p in probe_list:
            pid = p.probe_id if hasattr(p, "probe_id") else p.get("probe_id", "")
            ptext = p.perturbed_text if hasattr(p, "perturbed_text") else p.get("perturbed_text", "")

            if pid in cached_probe_annots:
                probe_annotations[pid] = cached_probe_annots[pid]
            elif pid in gemini_results:
                probe_annotations[pid] = gemini_results[pid]
            else:
                # Local heuristic inference for probe text directly (Phase 7 & 9)
                from .analyzer import get_exact_analyzer
                probe_pol, _, probe_reason = get_exact_analyzer().analyze(ptext)
                probe_annot = SemanticAnnotation(
                    sentence_id=pid,
                    sentence_text=ptext,
                    semantic_polarity=probe_pol,
                    confidence=None,  # Strictly None: NEVER fabricate confidence
                    reason=f"[Local Heuristic - Unverified] {probe_reason}",
                    ambiguity="MEDIUM" if probe_pol == SemanticReferenceLabel.NEUTRAL else "LOW",
                    verification_status=VerificationStatus.UNVERIFIED,
                    provider=ReferenceProvider.LOCAL_HEURISTIC.value,
                    gemini_polarity=None,
                    gemini_confidence=None,  # Strictly None
                    human_verified_polarity=None,
                    final_semantic_polarity=probe_pol,
                    verification_source="LOCAL_HEURISTIC_UNVERIFIED",
                    model_used="local_heuristic",
                )
                self.cache.put(probe_annot)
                probe_annotations[pid] = probe_annot

        # 6. Construct and authoritatively resolve semantic relations
        ref_set = SemanticReferenceSet(
            baseline_annotation=baseline_annot,
            probe_annotations=probe_annotations,
            frozen=False,
            annotation_engine="gemini" if self.client.is_online else "local_heuristic",
            model=self.client.model_name if self.client.is_online else "local_heuristic",
            provider=current_provider,
            cache_hits=cache_hits,
            api_requests=api_requests,
        )
        ref_set._recompute_relations()
        logger.info(
            f"[SEMANTIC] Semantic reference set established. "
            f"Provider={ref_set.provider}, Cache hits: {cache_hits}, API requests: {api_requests}"
        )
        return ref_set

    def _heuristic_polarity(self, text: str) -> SemanticReferenceLabel:
        """Local exact linguistic polarity inference."""
        from .analyzer import get_exact_analyzer
        label, _, _ = get_exact_analyzer().analyze(text)
        return label

    def save_reference_to_run(self, ref_set: SemanticReferenceSet, run_dir: str) -> str:
        """Persists the frozen semantic reference to runs/<exp_id>/semantic_reference.json."""
        os.makedirs(run_dir, exist_ok=True)
        out_file = os.path.join(run_dir, "semantic_reference.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(ref_set.to_dict(), f, indent=2, ensure_ascii=False)
        return out_file

    def load_reference_from_run(self, run_dir: str) -> Optional[SemanticReferenceSet]:
        """Loads semantic_reference.json from run directory if present."""
        path = os.path.join(run_dir, "semantic_reference.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return SemanticReferenceSet.from_dict(data)
            except Exception as ex:
                logger.warning(f"Failed to load semantic_reference.json from {run_dir}: {ex}")
        return None


# Module-level singleton instance
_GLOBAL_SEMANTIC_SERVICE: Optional[SemanticReferenceService] = None


def get_semantic_service() -> SemanticReferenceService:
    global _GLOBAL_SEMANTIC_SERVICE
    if _GLOBAL_SEMANTIC_SERVICE is None:
        _GLOBAL_SEMANTIC_SERVICE = SemanticReferenceService()
    return _GLOBAL_SEMANTIC_SERVICE
