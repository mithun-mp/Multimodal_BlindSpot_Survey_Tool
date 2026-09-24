"""
Hardware Detection and Resource Management for BlindSpot.
Detects host CPU, RAM, and GPU/VRAM to configure safe execution profiles without oversubscribing.
"""
import os
import logging
from typing import Dict, Any, Optional, Union

from blindspot.core.config import PerformanceMode, ResourceConfig

logger = logging.getLogger(__name__)


class ResourceManager:
    """
    Detects hardware capabilities and resolves safe, high-performance execution parameters.
    """
    @staticmethod
    def get_system_specs() -> Dict[str, Any]:
        """Detects current hardware environment."""
        cpu_count = os.cpu_count() or 4
        ram_gb = 8.0  # Safe default fallback

        try:
            import psutil
            ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        except Exception:
            pass

        gpu_info = {
            "available": False,
            "device_name": None,
            "vram_gb": 0.0,
        }

        try:
            import torch
            if torch.cuda.is_available():
                props = torch.cuda.get_device_properties(0)
                gpu_info = {
                    "available": True,
                    "device_name": props.name,
                    "vram_gb": round(props.total_memory / (1024 ** 3), 2),
                }
        except Exception:
            pass

        return {
            "cpu_cores": cpu_count,
            "ram_gb": ram_gb,
            "gpu": gpu_info,
        }

    @classmethod
    def resolve_config(
        cls,
        mode: Union[PerformanceMode, str] = PerformanceMode.BALANCED,
        batch_size_override: Optional[int] = None,
        max_workers_override: Optional[int] = None,
        device_override: Optional[str] = None,
    ) -> ResourceConfig:
        """
        Derives an optimal ResourceConfig based on hardware and the selected PerformanceMode.
        Supports SAFE, BALANCED, PERFORMANCE, CUSTOM, and FAST_DEBUG.
        """
        if isinstance(mode, str) and not isinstance(mode, PerformanceMode):
            mode = PerformanceMode.from_str(mode)

        specs = cls.get_system_specs()
        cpu_cores = specs["cpu_cores"]
        has_gpu = specs["gpu"]["available"]
        default_device = "cuda" if has_gpu else "cpu"
        device = device_override or default_device

        if mode in {PerformanceMode.SAFE, PerformanceMode.LOW_MEMORY}:
            config = ResourceConfig(
                mode=mode,
                max_workers=max_workers_override or 1,
                batch_size=batch_size_override or 4,
                model_cache_size=1,
                device="cpu",  # Strict CPU containment to prevent GPU memory pressure
                memory_reserve_gb=2.0,
                explanation_sample_size=50,
            )
        elif mode in {PerformanceMode.PERFORMANCE, PerformanceMode.HIGH_THROUGHPUT}:
            workers = max_workers_override or min(4, max(1, cpu_cores // 2))
            config = ResourceConfig(
                mode=mode,
                max_workers=workers,
                batch_size=batch_size_override or (32 if has_gpu else 16),
                model_cache_size=5,
                device=device,
                memory_reserve_gb=1.0,
                explanation_sample_size=100,
            )
        elif mode == PerformanceMode.CUSTOM:
            config = ResourceConfig(
                mode=mode,
                max_workers=max_workers_override or min(2, max(1, cpu_cores // 2)),
                batch_size=batch_size_override or 16,
                model_cache_size=5,
                device=device,
                memory_reserve_gb=1.5,
                explanation_sample_size=100,
            )
        elif mode == PerformanceMode.FAST_DEBUG:
            config = ResourceConfig(
                mode=mode,
                max_workers=max_workers_override or 1,
                batch_size=batch_size_override or 8,
                model_cache_size=1,
                device=device,
                memory_reserve_gb=0.5,
                explanation_sample_size=30,
            )
        else:
            # PerformanceMode.BALANCED / PerformanceMode.DEFAULT
            config = ResourceConfig(
                mode=mode,
                max_workers=max_workers_override or min(2, max(1, cpu_cores // 2)),
                batch_size=batch_size_override or 16,
                model_cache_size=5,
                device=device,
                memory_reserve_gb=1.5,
                explanation_sample_size=100,
            )

        return config
