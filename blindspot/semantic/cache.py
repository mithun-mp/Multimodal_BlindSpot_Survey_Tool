"""
Persistent Semantic Annotation Cache for BlindSpot (Phase 15).
Ensures cache keys strictly incorporate:
- normalized text
- semantic provider/engine
- model name
- schema version
- annotation version

Guarantees legacy fallback entries (e.g. with fabricated confidence) cannot masquerade
as real Gemini API results.
"""
import os
import json
import hashlib
import threading
from typing import Dict, Any, Optional
from .types import SemanticAnnotation, SemanticReferenceLabel, ReferenceProvider

CURRENT_SCHEMA_VERSION = "v2.0"
CURRENT_ANNOTATION_VERSION = "v2.0"


class SemanticAnnotationCache:
    """
    Thread-safe persistent JSON cache for semantic annotations with cryptographic keying
    including provider, model, schema, and annotation versions.
    """
    def __init__(
        self,
        cache_file_path: Optional[str] = None,
        cache_path: Optional[str] = None,
        annotation_version: str = CURRENT_ANNOTATION_VERSION,
        schema_version: str = CURRENT_SCHEMA_VERSION,
    ):
        chosen_path = cache_path or cache_file_path
        if chosen_path is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            cache_dir = os.path.join(base_dir, "cache")
            os.makedirs(cache_dir, exist_ok=True)
            chosen_path = os.path.join(cache_dir, "semantic_cache_v2.json")

        self.cache_file_path = chosen_path
        self.annotation_version = annotation_version
        self.schema_version = schema_version
        self._lock = threading.Lock()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.hits: int = 0
        self.misses: int = 0
        self._load()

    def _normalize(self, text: str) -> str:
        return " ".join(str(text or "").strip().lower().split())

    def _compute_key(
        self,
        sentence_text: str,
        provider: str = "GEMINI",
        model: str = "gemini-2.5-flash",
    ) -> str:
        norm = self._normalize(sentence_text)
        prov = str(provider or "NONE").strip().upper()
        mod = str(model or "DEFAULT").strip().lower()
        raw = f"{norm}|{prov}|{mod}|{self.schema_version}|{self.annotation_version}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def make_key(
        self,
        sentence_text: str,
        provider: str = "GEMINI",
        model: str = "gemini-2.5-flash",
    ) -> str:
        return self._compute_key(sentence_text, provider=provider, model=model)

    def has(
        self,
        sentence_text: str,
        provider: str = "GEMINI",
        model: str = "gemini-2.5-flash",
    ) -> bool:
        key = self._compute_key(sentence_text, provider=provider, model=model)
        with self._lock:
            return key in self._cache

    def _load(self):
        """Loads cache file and automatically purges legacy or corrupted entries."""
        with self._lock:
            if os.path.exists(self.cache_file_path):
                try:
                    with open(self.cache_file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            # Invalidate legacy entries without v2 schema
                            valid_entries = {}
                            for k, v in data.items():
                                if not isinstance(v, dict):
                                    continue
                                # Reject legacy entries with fabricated 0.75 confidence masquerading as gemini
                                if v.get("gemini_confidence") == 0.75 and v.get("provider") != "GEMINI":
                                    continue
                                if v.get("schema_version") == self.schema_version:
                                    valid_entries[k] = v
                            self._cache = valid_entries
                except Exception:
                    self._cache = {}

    def _save(self):
        try:
            os.makedirs(os.path.dirname(self.cache_file_path), exist_ok=True)
            with open(self.cache_file_path, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def get(
        self,
        sentence_text: str,
        provider: str = "GEMINI",
        model: str = "gemini-2.5-flash",
    ) -> Optional[SemanticAnnotation]:
        """Looks up a cached annotation strictly matching text, provider, and model."""
        key = self._compute_key(sentence_text, provider=provider, model=model)
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                try:
                    annot = SemanticAnnotation.from_dict(entry)
                    # Double check schema integrity
                    if annot.schema_version != self.schema_version:
                        del self._cache[key]
                        self.misses += 1
                        return None
                    self.hits += 1
                    return annot
                except Exception:
                    del self._cache[key]
                    self.misses += 1
                    return None
            self.misses += 1
            return None

    def put(self, annotation: SemanticAnnotation):
        """Stores a validated annotation into the persistent cache using its true provenance."""
        prov = annotation.provider or ReferenceProvider.NONE.value
        mod = annotation.model_used or "manual"
        key = self._compute_key(annotation.sentence_text, provider=prov, model=mod)
        with self._lock:
            self._cache[key] = annotation.to_dict()
            self._save()

    def clear(self):
        """Clears memory and persistent cache."""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0
            self._save()

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            total = self.hits + self.misses
            hit_rate = (self.hits / total * 100.0) if total > 0 else 0.0
            return {
                "size": len(self._cache),
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate_pct": round(hit_rate, 2),
                "cache_file": self.cache_file_path,
                "schema_version": self.schema_version,
            }
