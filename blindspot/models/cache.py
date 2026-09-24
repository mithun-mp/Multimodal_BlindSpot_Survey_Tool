"""
Thread-safe Dual Cache (Disk & RAM) for BlindSpot.
Maintains clear separation between persistent disk cache (HuggingFace Hub)
and transient RAM/VRAM resident models. Manages host memory consumption.
"""
from collections import OrderedDict
import threading
import gc
import os
import glob
import logging
from typing import Dict, Optional, List, Any

from blindspot.models.huggingface_wrapper import HuggingFaceWrapper

logger = logging.getLogger(__name__)


def get_hf_hub_cache_dir() -> str:
    """Resolves local Hugging Face hub cache directory."""
    if "HF_HUB_CACHE" in os.environ:
        return os.environ["HF_HUB_CACHE"]
    if "HF_HOME" in os.environ:
        return os.path.join(os.environ["HF_HOME"], "hub")
    return os.path.expanduser("~/.cache/huggingface/hub")


class ModelCache:
    """
    Thread-safe dual cache:
    1. Disk Cache Inspector: Inspects local weights, revisions, and storage footprint on disk.
    2. RAM / VRAM Resident Model Cache: LRU cache managing instantiated HuggingFaceWrapper objects.
    """
    _instance: Optional["ModelCache"] = None
    _singleton_lock = threading.Lock()

    def __init__(self, max_size: int = 5):
        # Default max_size=5 resident models in RAM for complete benchmark retention
        self._max_size = max_size
        self._cache: OrderedDict[str, HuggingFaceWrapper] = OrderedDict()
        self._meta: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()

    @classmethod
    def get_shared_cache(cls, max_size: int = 5) -> "ModelCache":
        """Singleton accessor for shared cross-component caching."""
        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = cls(max_size=max_size)
            elif cls._instance._max_size < max_size:
                cls._instance._max_size = max_size
            return cls._instance

    # ----------------------------------------------------------------------
    # 1. DISK CACHE TELEMETRY & MANAGEMENT
    # ----------------------------------------------------------------------

    @staticmethod
    def get_model_disk_info(model_id: str) -> Dict[str, Any]:
        """
        Inspects HuggingFace local hub cache for model files without loading into memory.
        Returns existence, disk size (MB), revision, and disk path.
        """
        hub_dir = get_hf_hub_cache_dir()
        folder_name = "models--" + model_id.replace("/", "--")
        model_hub_path = os.path.join(hub_dir, folder_name)

        if not os.path.exists(model_hub_path) and "/" not in model_id:
            # Check if an org-prefixed directory exists
            try:
                if os.path.exists(hub_dir):
                    matches = [
                        d for d in os.listdir(hub_dir)
                        if d.startswith("models--") and model_id in d
                    ]
                    if matches:
                        model_hub_path = os.path.join(hub_dir, matches[0])
            except Exception:
                pass

        if not os.path.exists(model_hub_path):
            return {
                "model_id": model_id,
                "cached_on_disk": False,
                "disk_size_mb": 0.0,
                "revision_hash": None,
                "disk_path": None,
            }

        # Calculate disk footprint
        total_bytes = 0
        try:
            for root, _, files in os.walk(model_hub_path):
                for f in files:
                    fp = os.path.join(root, f)
                    if os.path.isfile(fp) and not os.path.islink(fp):
                        total_bytes += os.path.getsize(fp)
                    elif os.path.islink(fp):
                        try:
                            total_bytes += os.path.getsize(fp)
                        except Exception:
                            pass
        except Exception:
            pass

        disk_size_mb = round(total_bytes / (1024 * 1024), 2)

        # Resolve revision hash from refs/main or snapshots
        revision = None
        refs_main = os.path.join(model_hub_path, "refs", "main")
        if os.path.exists(refs_main):
            try:
                with open(refs_main, "r", encoding="utf-8") as rf:
                    revision = rf.read().strip()[:10]
            except Exception:
                pass

        if not revision:
            snapshots_dir = os.path.join(model_hub_path, "snapshots")
            if os.path.exists(snapshots_dir):
                snaps = [
                    s for s in os.listdir(snapshots_dir)
                    if os.path.isdir(os.path.join(snapshots_dir, s))
                ]
                if snaps:
                    revision = snaps[0][:10]

        has_snapshots = False
        snapshots_dir = os.path.join(model_hub_path, "snapshots")
        if os.path.exists(snapshots_dir):
            has_snapshots = len(os.listdir(snapshots_dir)) > 0

        cached_on_disk = has_snapshots or disk_size_mb > 10.0

        return {
            "model_id": model_id,
            "cached_on_disk": cached_on_disk,
            "disk_size_mb": disk_size_mb,
            "revision_hash": revision or "cached",
            "disk_path": model_hub_path,
        }

    @classmethod
    def is_cached_on_disk(cls, model_id: str) -> bool:
        """Returns True if the model weights are already downloaded and present on disk."""
        info = cls.get_model_disk_info(model_id)
        return bool(info.get("cached_on_disk", False))

    def get_disk_cache_status(self, model_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Returns telemetry summary for specified models or active benchmark presets.
        Includes disk presence, size, revision, and RAM residency status.
        """
        if model_ids is None:
            from blindspot.models.registry import ModelRegistry
            model_ids = [m["model_id"] for m in ModelRegistry().list_presets(task="SENTIMENT")]

        results = []
        with self._lock:
            for m_id in model_ids:
                info = self.get_model_disk_info(m_id)
                info["is_resident_in_ram"] = any(
                    k.startswith(f"{m_id}:") for k in self._cache.keys()
                )
                results.append(info)
        return results

    # ----------------------------------------------------------------------
    # 2. RAM / VRAM RESIDENT MODEL CACHE (LRU)
    # ----------------------------------------------------------------------

    def get_or_load(self, model_id: str, device: Optional[str] = None) -> HuggingFaceWrapper:
        """
        Retrieves cached model or loads and caches a new HuggingFaceWrapper instance.
        If cache capacity is reached, evicts oldest resident model from RAM.
        Disk weights are NEVER deleted.
        """
        import time
        with self._lock:
            cache_key = f"{model_id}:{device or 'auto'}"
            if cache_key in self._cache:
                logger.info(f"RAM Cache HIT for {model_id}")
                self._cache.move_to_end(cache_key)
                if cache_key in self._meta:
                    self._meta[cache_key]["last_used"] = time.time()
                return self._cache[cache_key]

            logger.info(f"RAM Cache MISS for {model_id}. Loading into memory...")
            # If cache is full, evict LRU model from RAM
            while len(self._cache) >= self._max_size:
                evicted_key, evicted_model = self._cache.popitem(last=False)
                self._meta.pop(evicted_key, None)
                logger.info(f"Evicting model from RAM: {evicted_key}")
                del evicted_model
                self._cleanup_memory()

            model = HuggingFaceWrapper(model_name_or_path=model_id, device=device)
            self._cache[cache_key] = model
            self._meta[cache_key] = {
                "model_id": model_id,
                "device": device or "auto",
                "loaded_at": time.time(),
                "last_used": time.time(),
            }
            return model

    def put(self, model_id: str, model: Any, device: Optional[str] = None) -> None:
        """Stores a pre-instantiated model wrapper into the RAM cache."""
        import time
        with self._lock:
            if device:
                cache_key = f"{model_id}:{device}"
                self._cache[cache_key] = model
                self._meta[cache_key] = {
                    "model_id": model_id,
                    "device": device,
                    "loaded_at": time.time(),
                    "last_used": time.time(),
                }
                self._cache.move_to_end(cache_key)
            else:
                for d in ("auto", "cpu"):
                    k = f"{model_id}:{d}"
                    self._cache[k] = model
                    self._meta[k] = {
                        "model_id": model_id,
                        "device": d,
                        "loaded_at": time.time(),
                        "last_used": time.time(),
                    }

    def is_resident_in_ram(self, model_id: str, device: Optional[str] = None) -> bool:
        """Checks if model wrapper is currently resident in host RAM/VRAM."""
        with self._lock:
            if device:
                return f"{model_id}:{device}" in self._cache
            return any(k.startswith(f"{model_id}:") or k == model_id for k in self._cache.keys())

    def is_cached(self, model_id: str) -> bool:
        """Checks if model wrapper is currently resident in host RAM/VRAM."""
        return self.is_resident_in_ram(model_id)

    def evict_from_memory(self, model_id: str, device: Optional[str] = None) -> bool:
        """
        Evicts a model from host RAM/VRAM without touching disk weights.
        Returns True if the model was resident and evicted.
        """
        with self._lock:
            evicted_any = False
            keys_to_remove = [
                k for k in self._cache.keys()
                if k.startswith(f"{model_id}:") or k == model_id
            ]
            for k in keys_to_remove:
                evicted = self._cache.pop(k, None)
                self._meta.pop(k, None)
                if evicted is not None:
                    del evicted
                    evicted_any = True

            if evicted_any:
                self._cleanup_memory()
            return evicted_any

    def clear_memory_cache(self) -> None:
        """
        Frees all host RAM / VRAM resident models.
        Disk cache remains 100% intact.
        """
        with self._lock:
            self._cache.clear()
            self._meta.clear()
            self._cleanup_memory()
            logger.info("RAM model cache cleared. All resident models unloaded.")

    def clear(self) -> None:
        """Alias for clear_memory_cache() for backward compatibility."""
        self.clear_memory_cache()

    def size(self) -> int:
        with self._lock:
            return len(self._cache)

    def cached_model_ids(self) -> List[str]:
        with self._lock:
            return list(self._cache.keys())

    def get_cache_summary(self) -> Dict[str, Any]:
        """
        Returns telemetry summary of resident models adhering to Section 13:
        Capacity, Count, Loaded, Cached, Device, Memory, Last used.
        """
        with self._lock:
            resident_models = []
            for k, model in self._cache.items():
                m_id = k.split(":")[0]
                meta = self._meta.get(k, {})
                disk_info = self.get_model_disk_info(m_id)
                resident_models.append({
                    "model_id": m_id,
                    "loaded": True,
                    "cached_on_disk": disk_info.get("cached_on_disk", True),
                    "device": meta.get("device", getattr(model, "device", "cpu")),
                    "memory_mb": disk_info.get("disk_size_mb", 0.0),
                    "loaded_at": meta.get("loaded_at", 0.0),
                    "last_used": meta.get("last_used", 0.0),
                    "num_classes": len(getattr(model, "labels", [])),
                    "labels": getattr(model, "labels", []),
                })
            return {
                "capacity": self._max_size,
                "resident_count": len(self._cache),
                "models": resident_models,
            }

    @staticmethod
    def _cleanup_memory():
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass
