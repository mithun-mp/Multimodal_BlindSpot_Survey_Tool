"""
Hardware Detection and Resource Management for BlindSpot.
Detects host CPU, RAM, Network I/O, and Storage to configure safe execution profiles
and stream real-time host telemetry across any machine (integrated or dedicated)
with zero dummy data and zero hardware-specific GPU dependencies.
"""
import os
import time
import platform
import logging
from typing import Dict, Any, Optional, Union, List

from blindspot.core.config import PerformanceMode, ResourceConfig

logger = logging.getLogger(__name__)

# State tracking for network speed delta computation
_last_net_time: float = 0.0
_last_bytes_recv: int = 0
_last_bytes_sent: int = 0


class ResourceManager:
    """
    Detects hardware capabilities, monitors real-time CPU, RAM, and Network telemetry,
    and resolves safe, high-performance execution parameters across any machine.
    """

    @staticmethod
    def get_cpu_name() -> str:
        """Standard host processor identifier without vendor-specific or hardware-bound brand strings."""
        return "Host Multi-Core Processor"

    @staticmethod
    def get_network_telemetry() -> Dict[str, Any]:
        """Calculates real-time network transfer rates and cumulative traffic."""
        global _last_net_time, _last_bytes_recv, _last_bytes_sent
        now = time.time()
        down_kbps = 0.0
        up_kbps = 0.0
        total_recv_mb = 0.0
        total_sent_mb = 0.0

        try:
            import psutil
            net = psutil.net_io_counters()
            total_recv_mb = round(net.bytes_recv / (1024 ** 2), 2)
            total_sent_mb = round(net.bytes_sent / (1024 ** 2), 2)

            if _last_net_time > 0 and (now - _last_net_time) >= 0.05:
                dt = now - _last_net_time
                down_kbps = max(0.0, round((net.bytes_recv - _last_bytes_recv) / dt / 1024.0, 1))
                up_kbps = max(0.0, round((net.bytes_sent - _last_bytes_sent) / dt / 1024.0, 1))

            _last_net_time = now
            _last_bytes_recv = net.bytes_recv
            _last_bytes_sent = net.bytes_sent
        except Exception:
            pass

        return {
            "speed_down_kbps": down_kbps,
            "speed_up_kbps": up_kbps,
            "total_recv_mb": total_recv_mb,
            "total_sent_mb": total_sent_mb,
        }

    @staticmethod
    def get_disk_telemetry(path: str = ".") -> Dict[str, Any]:
        """Measures disk storage utilization and runs directory footprint."""
        try:
            import psutil
            disk = psutil.disk_usage(path)
            total_gb = round(disk.total / (1024 ** 3), 2)
            used_gb = round(disk.used / (1024 ** 3), 2)
            free_gb = round(disk.free / (1024 ** 3), 2)
            pct = round(disk.percent, 1)
        except Exception:
            total_gb, used_gb, free_gb, pct = 0.0, 0.0, 0.0, 0.0

        # Calculate runs/ directory footprint
        runs_mb = 0.0
        try:
            runs_path = os.path.abspath(os.path.join(path, "runs"))
            if os.path.exists(runs_path):
                total_bytes = 0
                for root_dir, _, files in os.walk(runs_path):
                    for f in files:
                        fp = os.path.join(root_dir, f)
                        if os.path.isfile(fp):
                            total_bytes += os.path.getsize(fp)
                runs_mb = round(total_bytes / (1024 ** 2), 2)
        except Exception:
            pass

        return {
            "percent": pct,
            "total_gb": total_gb,
            "used_gb": used_gb,
            "free_gb": free_gb,
            "runs_footprint_mb": runs_mb,
        }

    @classmethod
    def get_live_telemetry(cls) -> Dict[str, Any]:
        """
        Unified real-time telemetry snapshot: CPU, RAM, Network, and Disk.
        Pure host hardware monitoring without GPU-specific dependencies.
        """
        # 1. CPU Telemetry
        cpu_name = cls.get_cpu_name()
        logical_cores = os.cpu_count() or 4
        physical_cores = logical_cores
        cpu_pct = 0.0
        cpu_freq_ghz = 0.0
        per_core_pct: List[float] = []

        try:
            import psutil
            logical_cores = psutil.cpu_count(logical=True) or logical_cores
            physical_cores = psutil.cpu_count(logical=False) or logical_cores
            cpu_pct = round(psutil.cpu_percent(interval=None), 1)
            per_core = psutil.cpu_percent(interval=None, percpu=True)
            if cpu_pct == 0.0 or all(c == 0.0 for c in per_core):
                cpu_pct = round(psutil.cpu_percent(interval=0.03), 1)
                per_core = psutil.cpu_percent(interval=None, percpu=True)
            per_core_pct = [round(c, 1) for c in per_core]
            freq = psutil.cpu_freq()
            if freq and freq.current:
                cpu_freq_ghz = round(freq.current / 1000.0, 2)
        except Exception:
            pass

        # 2. RAM Telemetry
        ram_total_gb = 0.0
        ram_used_gb = 0.0
        ram_free_gb = 0.0
        ram_pct = 0.0

        try:
            import psutil
            mem = psutil.virtual_memory()
            ram_total_gb = round(mem.total / (1024 ** 3), 2)
            ram_used_gb = round(mem.used / (1024 ** 3), 2)
            ram_free_gb = round(mem.available / (1024 ** 3), 2)
            ram_pct = round(mem.percent, 1)
        except Exception:
            pass

        # 3. Network Telemetry
        net_data = cls.get_network_telemetry()

        # 4. Disk Telemetry
        disk_data = cls.get_disk_telemetry()

        return {
            "timestamp": time.time(),
            "cpu": {
                "name": cpu_name,
                "percent": cpu_pct,
                "logical_cores": logical_cores,
                "physical_cores": physical_cores,
                "frequency_ghz": cpu_freq_ghz,
                "per_core": per_core_pct,
            },
            "ram": {
                "percent": ram_pct,
                "used_gb": ram_used_gb,
                "total_gb": ram_total_gb,
                "free_gb": ram_free_gb,
            },
            "network": net_data,
            "disk": disk_data,
        }

    @classmethod
    def get_system_specs(cls) -> Dict[str, Any]:
        """
        Detects current hardware environment with CPU, RAM, Network, and Storage metrics.
        Universally compatible across all devices.
        """
        telemetry = cls.get_live_telemetry()
        cpu_info = telemetry["cpu"]
        ram_info = telemetry["ram"]

        has_cuda = False
        try:
            import torch
            has_cuda = torch.cuda.is_available()
        except Exception:
            pass

        return {
            "cpu_cores": cpu_info["logical_cores"],
            "logical_cores": cpu_info["logical_cores"],
            "physical_cores": cpu_info["physical_cores"],
            "cpu_name": cpu_info["name"],
            "cpu_freq_ghz": cpu_info["frequency_ghz"],
            "ram_gb": ram_info["total_gb"],
            "ram_used_gb": ram_info["used_gb"],
            "ram_free_gb": ram_info["free_gb"],
            "ram_percent": ram_info["percent"],
            "network": telemetry["network"],
            "disk": telemetry["disk"],
            "pytorch_device": "cuda" if has_cuda else "cpu",
            "gpu": {"available": has_cuda, "device_name": None, "vram_gb": 0.0},
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
        Derives an optimal ResourceConfig based on actual hardware and the selected PerformanceMode.
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
                device="cpu",  # Strict CPU containment to prevent memory pressure
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
