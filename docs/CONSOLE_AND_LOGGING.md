# BlindSpot Workstation — Console & Observability Architecture

This guide details the observability, structured logging, rotating file handlers, and interactive system console implemented in the BlindSpot Workstation.

---

## 1. Structured Logging Format

All BlindSpot modules log through standardized subsystem adapters producing uniform, fixed-width records:

```text
YYYY-MM-DD HH:MM:SS | LEVEL    | SUBSYSTEM | Message
```

### Canonical Subsystems

| Subsystem | Responsibilities |
| :--- | :--- |
| **BOOT** | Python verification, dependency validation, port allocation, server lifecycle. |
| **UI** | Application shell, session state routing, component rendering. |
| **MODEL** | Weights loading, HuggingFace pipeline wrapping, device transfer, inference batching. |
| **CACHE** | Thread-safe LRU cache hits, evictions, memory garbage collection. |
| **RUNNER** | Asynchronous experiment orchestration, scheduling, step advancement, cancellation. |
| **PROBE** | Shared deterministic linguistic perturbation generation, expected semantic effect inference. |
| **XAI** | Feature attributions (LIME, SHAP, Leave-One-Out fallback), alignment similarity computation. |
| **RESOURCE**| CPU utilization polling, host RAM tracking, GPU telemetry, batch size tuning. |
| **STORAGE** | Artifact directory initialization, event journaling (`events.jsonl`), results serialization. |
| **REPORT** | Markdown summary and comparative report generation. |

### Severity Levels
- `DEBUG`: Verbose internal diagnostics, timing records, tensor shapes.
- `INFO`: Normal operational milestones, model load hits, probe counts.
- `SUCCESS`: Job completions, verification passes.
- `WARNING`: Graceful fallbacks, cache misses, high memory pressure.
- `ERROR`: Model loading failures, unhandled exceptions, process termination.

---

## 2. Rotating File Handlers (`logs/blindspot.log`)

BlindSpot employs a standard `RotatingFileHandler` configured in `blindspot/core/logging_config.py`:
- **File Location**: `logs/blindspot.log`
- **Max File Size**: 5 MB per file
- **Backup History**: 5 rotated files (`blindspot.log.1`, `blindspot.log.2`, etc.)
- **Encoding**: UTF-8

This guarantees that application logs never grow unchecked on disk during extensive multi-hour auditing campaigns.

---

## 3. Dedicated System Console (`RUN -> Console`)

The workstation provides an interactive engineering console directly within the user interface:

### Capabilities:
1. **Live Log Stream**: Ingests both system bootstrap messages and active experiment event streams in real time.
2. **Severity Filtering**: Filter by `ALL`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, or `DEBUG`.
3. **Subsystem Filtering**: Isolate logs strictly to `MODEL`, `CACHE`, `XAI`, or any other subsystem.
4. **Keyword Search**: Instant live substring filtering across all log messages.
5. **Log Export**: One-click download button (`blindspot_console_<timestamp>.log`) to save console sessions locally.
6. **Log Clearing**: Immediate console reset without modifying persistent disk archives.

---

## 4. Debug Mode Configuration

Debug telemetry can be toggled at any time:
- **Sidebar Switch**: Toggle the **Debug Telemetry** switch at the bottom of the sidebar navigation.
- **Log Level**: Dynamically switches root logging level from `INFO` to `DEBUG`, surfacing internal execution timings, tensor allocations, and scheduler queue events.
