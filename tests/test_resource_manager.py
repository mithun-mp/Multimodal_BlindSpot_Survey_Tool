"""
Unit Tests for Hardware Detection and Resource Manager.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.execution.resources import ResourceManager
from blindspot.core.config import PerformanceMode, ResourceConfig


class TestResourceManager(unittest.TestCase):
    def test_get_system_specs(self):
        specs = ResourceManager.get_system_specs()
        self.assertIn("cpu_cores", specs)
        self.assertGreater(specs["cpu_cores"], 0)
        self.assertIn("ram_gb", specs)
        self.assertGreater(specs["ram_gb"], 0.0)
        self.assertIn("gpu", specs)
        self.assertIn("available", specs["gpu"])

    def test_resolve_modes(self):
        # Default mode
        cfg_def = ResourceManager.resolve_config(PerformanceMode.DEFAULT)
        self.assertEqual(cfg_def.mode, PerformanceMode.DEFAULT)
        self.assertGreaterEqual(cfg_def.max_workers, 1)
        self.assertGreaterEqual(cfg_def.batch_size, 8)

        # Fast debug mode
        cfg_dbg = ResourceManager.resolve_config(PerformanceMode.FAST_DEBUG)
        self.assertEqual(cfg_dbg.mode, PerformanceMode.FAST_DEBUG)
        self.assertEqual(cfg_dbg.max_workers, 1)
        self.assertEqual(cfg_dbg.model_cache_size, 1)
        self.assertLessEqual(cfg_dbg.explanation_sample_size, 50)

        # Low memory mode
        cfg_low = ResourceManager.resolve_config(PerformanceMode.LOW_MEMORY)
        self.assertEqual(cfg_low.mode, PerformanceMode.LOW_MEMORY)
        self.assertEqual(cfg_low.device, "cpu")
        self.assertEqual(cfg_low.model_cache_size, 1)

        # High throughput mode
        cfg_high = ResourceManager.resolve_config(PerformanceMode.HIGH_THROUGHPUT)
        self.assertEqual(cfg_high.mode, PerformanceMode.HIGH_THROUGHPUT)
        self.assertGreaterEqual(cfg_high.batch_size, 16)


if __name__ == "__main__":
    unittest.main()
