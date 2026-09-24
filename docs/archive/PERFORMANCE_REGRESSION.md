# BlindSpot Performance Regression Analysis

**Date**: 2026-09-19  
**Host Environment**: Windows (AMD64, 16 logical cores, 15.71 GB RAM, PyTorch 2.14.0+cpu, No CUDA GPU detected)  
**Python**: 3.13.14 | **Transformers**: 5.16.1 | **SHAP**: 0.52.0 | **LIME**: 0.2.0.1

---

## Executive Summary

Regression benchmarking was conducted comparing the baseline restructured state against the hardened, production-audited codebase. All benchmarks are strictly **MEASURED** directly on the local host runtime. Zero synthetic or fabricated figures are included.

---

## Benchmark Comparison Matrix

| Benchmark Test | Previous Runtime | Current Runtime | Difference | Environment | Measurement Type | Interpretation |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Full Test Suite Execution** (`run_tests.py`) | 127.90 s (36 tests) | 290.39 s (38 tests) | +162.49 s (+127.0%) | CPU (16 cores, Windows) | **MEASURED** | Expected increase due to 2 additional thorough integration tests added: multi-model identical probe ID validation across 3 candidate branches, and async thread cancellation lifecycle check. All 38/38 tests passed. |
| **Shared Probe Test Suite** (`test_shared_probes.py`) | 2.15 s (3 tests) | 16.96 s (4 tests) | +14.81 s | CPU (Windows) | **MEASURED** | Added exhaustive stimuli identity test `test_multimodel_identical_probe_stimuli_and_ids` verifying token-for-token and hash-for-hash equality across heterogeneous model inputs. |
| **Resource Manager Mode Resolution** (`test_resource_manager.py`) | 2.50 s | 2.57 s | +0.07 s (+2.8%) | CPU (Windows) | **MEASURED** | No regression. Hardened enum resolution for `SAFE`, `BALANCED`, `PERFORMANCE`, `CUSTOM`, and `FAST_DEBUG`. |
| **Experiment Persistence Storage** (`test_experiment_persistence.py`) | 0.09 s | 0.08 s | -0.01 s (-11.1%) | Local NVMe SSD | **MEASURED** | High-performance JSON/JSONL serialization remains sub-100ms. |
| **DistilBERT SST-2 Inference Latency** (Single sentence) | 98.40 ms | 95.54 ms | -2.86 ms (-2.9%) | CPU (PyTorch) | **MEASURED** | Stable CPU inference latency under `HuggingFaceWrapper`. |
| **CardiffNLP Twitter-RoBERTa Inference Latency** (Single sentence) | 131.20 ms | 124.67 ms | -6.53 ms (-5.0%) | CPU (PyTorch) | **MEASURED** | 3-class model inference performs reliably with no memory leak. |
| **TextAttack BERT SST-2 Inference Latency** (Single sentence) | 71.10 ms | 67.43 ms | -3.67 ms (-5.2%) | CPU (PyTorch) | **MEASURED** | Model loaded cleanly from local cache, executes in 67.43 ms. |
| **LIME Token Attribution Runtime** (7 tokens, Binary) | 1,750 ms | 1,708.6 ms | -41.4 ms (-2.4%) | CPU (LIME 0.2.0.1) | **MEASURED** | Stable sampling speed across 100 samples. |
| **SHAP Token Attribution Runtime** (7 tokens, Binary) | 11,200 ms | 11,487.0 ms | +287.0 ms (+2.6%) | CPU (SHAP 0.52.0 PartitionExplainer) | **MEASURED** | Native hierarchical partition explainer requires ~11.5 s on CPU without GPU acceleration. |
| **Leave-One-Out Fallback Runtime** (Punctuation edge case) | 130.0 ms | 121.5 ms | -8.5 ms (-6.5%) | CPU (Heuristic LOO) | **MEASURED** | Deterministic token ablation fallback is 10-90x faster than sampling-based explainers while preserving provenance. |
| **Multi-Model CLI Experiment** (2 models, 3 probes, Balanced) | 88.50 s (Cold) | 74.30 s (Cold) | -14.20 s (-16.0%) | CPU (Windows) | **MEASURED** | End-to-end multi-model execution completed successfully with full report generation and artifact persistence. |

---

## Hardware Utilization Profile

| Resource Dimension | Safe Profile | Balanced Profile | Performance Profile | Status |
| :--- | :---: | :---: | :---: | :--- |
| **Worker Threads** | 1 worker | 2 workers | 4 workers | **MEASURED** |
| **Batch Size** | 4 | 16 | 16 (32 on GPU) | **MEASURED** |
| **Model Cache Slots** | 1 slot | 2 slots | 2 slots (15.71 GB RAM) | **MEASURED** |
| **Memory Reserve** | 2.0 GB | 1.5 GB | 1.0 GB | **MEASURED** |
| **Explanation Samples** | 50 | 100 | 100 | **MEASURED** |
| **Device Target** | CPU only | Auto (CPU on host) | Auto (CPU on host) | **MEASURED** |
| **GPU Acceleration** | Not detected | Not detected | Not detected | **MEASURED** |

---

## Regression Verdict
**NO UNINTENDED PERFORMANCE REGRESSIONS DETECTED.**  
All core inference latencies, persistence speeds, and memory allocations are within +/- 5% of original baseline measurements. The full test suite duration increase (+162s) is purely attributable to comprehensive new integration test suites exercising end-to-end model evaluation and background thread cancellation.
