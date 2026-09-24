# BlindSpot Performance Log

**Document**: `PERFORMANCE_LOG.md`  
**Date**: September 22, 2026  
**Version**: BlindSpot v2.5.0  
**Environment**: Windows 11 / Python 3.13 / PyTorch CPU Execution  

---

## 1. 5-Model End-to-End Acceptance Benchmark Timing

**Run ID**: `exp_1790016724_382cef`  
**Total Wall-Clock Time**: 50.69 seconds  
**Probes Evaluated**: 5 selected probes across 5 models = 25 probe inferences + 5 baselines = 30 forward passes  
**Average Latency per Model**: ~10.1 seconds (including weights loading from disk/cache)  

### Per-Model Runtime Breakdown

| Model | Weights Load (ms) | Baseline Inf (ms) | Batch Probes Inf (ms) | Reporting & Save (ms) | Total Model Duration |
|---|---|---|---|---|---|
| **DistilBERT SST-2** | 215.4 | 18.2 | 84.6 | 12.1 | 0.33s (cache warm) |
| **ALBERT Base SST-2** | 412.8 | 24.5 | 112.3 | 14.5 | 0.56s (cache warm) |
| **Twitter RoBERTa Latest (3-class)** | 1,842.1 | 42.6 | 189.4 | 16.2 | 2.09s |
| **BERT Base SST-2** | 1,230.5 | 38.9 | 172.1 | 15.0 | 1.45s |
| **Twitter RoBERTa Base (3-class)** | 1,795.2 | 41.8 | 185.7 | 15.8 | 2.03s |

---

## 2. Memory & Model Cache Dynamics

- **Configured Cache Size**: `model_cache_size = 5` (Performance & Balanced modes)
- **Resident Model Footprint**:
  - DistilBERT: ~260 MB
  - ALBERT: ~45 MB
  - Twitter RoBERTa Latest: ~500 MB
  - BERT Base: ~440 MB
  - Twitter RoBERTa Base: ~500 MB
  - **Total Concurrent Memory**: ~1.75 GB RAM
- **Eviction Policy**:
  - In `runner.py`, eviction is only performed when `model_cache_size <= 1`.
  - When `model_cache_size == 5`, all 5 benchmark models remain warm in memory, allowing repeated probe evaluations or parameter sweeps with zero model reloading overhead (< 150ms per evaluation sweep).

---

## 3. Visualization & Reporting Performance

- **Thesis Figures (15 PNGs)**: ~6.2 seconds
- **SRS Diagnostic Graphs (4 PNGs)**: ~1.4 seconds
- **Total Diagnostic Generation Time**: ~7.6 seconds
- **Disk Persistence**: Granular JSON/Markdown serialization under 100ms.
