# BlindSpot Performance Log

## Environment

- **CPU**: 16 logical cores
- **RAM**: 15.71 GB
- **GPU**: None (CPU execution)
- **VRAM**: 0.0 GB
- **OS**: Windows (AMD64)
- **Python**: 3.13.14
- **PyTorch**: 2.14.0+cpu
- **Transformers**: 5.16.1
- **SHAP**: 0.52.0
- **LIME**: 0.2.0.1
- **spaCy**: 3.8.16 (model: `en_core_web_sm`)

---

## Benchmarks (Observed Measurements)

### Benchmark 1: Fast Debug Execution Mode (Inference Only)
- **Configuration**:
  - Models: `distilbert-base-uncased-finetuned-sst-2-english`
  - Seed Sentences: 2
  - Probes Generated: 6
  - Explainer: `none`
  - Batch Size: 8
  - Performance Mode: `fast_debug`
  - Device: `cpu`
- **Observed Results**:
  - Total Runtime: 14.251 s (including initial model load)
  - Probes Evaluated: 6
  - Inference Throughput: 0.42 probes/sec
  - Process Peak RSS: 842.15 MB

### Benchmark 2: Default Execution Mode with Feature Attributions (Cached Model)
- **Configuration**:
  - Models: `distilbert-base-uncased-finetuned-sst-2-english`
  - Seed Sentences: 1
  - Probes Generated: 3
  - Explainer: `lime`
  - Batch Size: 16
  - Performance Mode: `default`
  - Device: `cpu`
  - Model Cache State: HIT (0.00 s load time)
- **Observed Results**:
  - Total Runtime: 7.092 s
  - Probes Evaluated: 3
  - End-to-End Throughput: 0.42 probes/sec
  - Process Peak RSS: 897.92 MB

### Benchmark 3: Multimodel Audit in Balanced Mode (Cold Load)
- **Configuration**:
  - Models: `distilbert-base-uncased-finetuned-sst-2-english`, `cardiffnlp/twitter-roberta-base-sentiment`
  - Seed Sentences: 1
  - Probes Generated: 3
  - Explainer: `lime`
  - Performance Mode: `balanced`
  - Device: `cpu`
- **Observed Results**:
  - Total Runtime: 74.30 s (including pipeline downloads and initialization)
  - Probes Evaluated: 3 x 2 models = 6 probe evaluations
  - Pairwise Agreement: 100.0%
  - Memory Peak RSS: 897.0 MB

---

## Comparison Table

| Configuration | Models | Explainer | Cache State | Runtime (s) | Probes/sec | Memory (MB) |
|---|:---:|:---:|:---:|---:|---:|---:|
| Fast Debug (Cold) | 1 | None | Miss | 14.251 | 0.42 | 842.15 |
| Default (Warm) | 1 | LIME | Hit | 7.092 | 0.42 | 897.92 |
| Balanced Multimodel | 2 | LIME | Miss/Hit | 74.300 | 0.08 | 897.00 |

## Single-Sentence Model Inference Latency (CPU)

| Model Architecture | Task | Classes | Measured Latency | Device |
|---|---|:---:|---:|:---:|
| `distilbert-base-uncased-finetuned-sst-2-english` | Binary SST-2 | 2 | 95.54 ms | CPU |
| `cardiffnlp/twitter-roberta-base-sentiment` | 3-Class Sentiment | 3 | 124.67 ms | CPU |
| `textattack/bert-base-uncased-SST-2` | Binary SST-2 | 2 | 67.43 ms | CPU |
