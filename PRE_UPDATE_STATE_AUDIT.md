# BLINDSPOT — PRE-UPDATE STATE AUDIT REPORT
**Generated**: September 20, 2026  
**Auditor**: BlindSpot Research Architecture & Engineering Audit  
**Workspace**: `c:\Dev\Projects\BlinkSpot-main`  
**Runtime**: Python 3.13.14 (Windows AMD64), PyTorch 2.14.0+cpu, Transformers 4.49.0  

---

## 1. Executive Summary

This audit assesses the current state of the BlindSpot repository across persistence, caching, UI state synchronization, execution architecture, reporting, visualization, logging, test performance, and disk footprint prior to commencing the P0/P1 Research Pipeline, Performance, and Persistence Repair.

---

## 2. Inventory of Current Models & Validation Status

| # | Model ID | Architecture | Classes | Task | Parameters | Validation Status | Cache State |
|---|---|---|---|---|---|---|---|
| **M1** | `distilbert-base-uncased-finetuned-sst-2-english` | `DistilBertForSequenceClassification` | 2 | SENTIMENT | 66.96M | **VALID** | Cached on disk |
| **M2** | `textattack/albert-base-v2-SST-2` | `AlbertForSequenceClassification` | 2 | SENTIMENT | 11.68M | **VALID** | Cached on disk |
| **M3** | `cardiffnlp/twitter-roberta-base-sentiment-latest` | `RobertaForSequenceClassification` | 3 | SENTIMENT | 124.65M | **VALID** | Cached on disk |
| **M4** | `textattack/bert-base-uncased-SST-2` | `BertForSequenceClassification` | 2 | SENTIMENT | 109.48M | **VALID** | Cached on disk |
| **M5** | `cardiffnlp/twitter-roberta-base-sentiment` | `RobertaForSequenceClassification` | 3 | SENTIMENT | 124.65M | **VALID** | Cached on disk |
| **M6** | `nlptown/bert-base-multilingual-uncased-sentiment` | `BertForSequenceClassification` | 5 | SENTIMENT | 167.33M | **VALID (Auxiliary)** | Cached on disk |
| **M7** | `jbeno/electra-base-classifier-sentiment` | `ElectraModel` + Custom MLP Head | 3 | SENTIMENT | 109.48M | **REJECTED (Head Mismatch)** | Weights cached; non-standard head |
| **M8** | `sileod/deberta-v3-base-tasksource-sentiment` | `DebertaV2ForSequenceClassification` | 3 | SENTIMENT | 86.85M | **REJECTED (Runtime Deadlock)** | Python 3.13 torch.jit deprecation |
| **M9** | `cardiffnlp/twitter-xlm-roberta-base-sentiment` | `XLMRobertaForSequenceClassification` | 3 | SENTIMENT | 278.04M | **REJECTED (Missing Weights)** | Checkpoint unavailable |
| **M10**| `roberta-base-openai-detector` | `RobertaForSequenceClassification` | 2 | AI_TEXT_DETECTION | 124.65M | **REJECTED (Non-Sentiment)** | Cached; isolated from sentiment |

---

## 3. Current Cache Behavior

1. **In-Memory Cache (`blindspot/models/cache.py`)**:
   - `ModelCache` is an in-memory `OrderedDict` with a hardcoded `max_size = 2`.
   - **Flaw**: Evaluating 5 models causes models 1, 2, 3 to be evicted as models 3, 4, 5 are loaded. If a model is accessed again (e.g. for explainability or retry), it must reload.
   - **No Disk vs. RAM Separation**: The cache treats in-memory object caching and on-disk model weight storage as the same thing.
2. **On-Disk Weight Cache (`~/.cache/huggingface/hub`)**:
   - Total size: **6.33 GB** across 180 files.
   - Currently caches models M1, M2, M3, M4, M5, M6, M7, M10.
   - There is no application-level UI screen to inspect on-disk model cache status, validate cache integrity, or see cache hit/miss statistics.

---

## 4. Current Run Persistence & Storage Architecture

1. **Storage Structure (`runs/`)**:
   - Currently contains 13 historical runs (2.53 MB total).
   - In each run folder:
     * `config.json`: Run configuration.
     * `metadata.json`: High-level run metadata.
     * `results.json`: Monolithic results blob written **only at the very end of the entire multi-model experiment**.
     * `events.jsonl`: Event log stream.
     * `reports/`: Markdown reports written only at the end.
     * `figures/`: **Empty directory**. No graphs are currently persisted.
2. **Critical Architectural Defects**:
   - **No Per-Model Granularity**: Completed models (e.g. Model 1, Model 2) do NOT persist their individual results until ALL models finish.
   - **No Partial Run Persistence**: If execution is interrupted after Model 3 completes, Model 1, 2, and 3 results are lost from disk.
   - **No Resume Support**: Runs cannot be resumed from the last completed model.
   - **No Safe Deletion / Archival Management**: No UI exists to safely archive or permanently delete runs with explicit user confirmation.

---

## 5. Current UI State Synchronization & Refresh Behavior

1. **Blinking / Refresh Flaw (`blindspot/ui/live_run.py`)**:
   - `live_run.py` employs an active auto-refresh loop with `time.sleep(1.0)` and `st.rerun()`.
   - On every 1-second tick, the entire Streamlit script re-executes from top to bottom, recreating DOM elements, progress bars, and markdown blocks.
   - This causes noticeable visual blinking, widget remounting, and CPU overhead.
2. **Stale Model Names Bug**:
   - `overview.py` automatically loads the latest completed run from disk into `st.session_state["active_results"]` if empty.
   - When a user launches a new experiment with a different model subset, `active_results` in `session_state` can still point to the old run.
   - UI views (`Comparison`, `Failure Analysis`, `Reports`) read from `st.session_state["active_results"]`, displaying stale model names and outdated results while a new run is executing.
   - **Fix Required**: Model names and active execution telemetry must be derived strictly from the active `RunPlan` and immutable `run_id`, never from un-scoped session cache.

---

## 6. Current Execution Architecture & Performance Bottlenecks

1. **Why 5-Model Execution Takes ~1 Hour**:
   - Forward pass inference on 4 probes + 1 baseline takes only **~1 to 2 seconds per model** on CPU (total ~10 seconds for all 5 models).
   - **The 1-Hour Bottleneck is Explainability (LIME & SHAP)**:
     * When `explainer_type` is `"both"` or `"lime"`, LIME executes 500 perturbations on `seed_text` and 500 on `perturbed_text`.
     * SHAP executes 100-200 background forward passes.
     * Total forward passes per probe: $\approx 1,300$.
     * For 4 probes across 5 models: $4 \times 5 \times 1,300 = \mathbf{26,000}$ forward passes on CPU!
     * At $\approx 70\text{ ms}$ per unbatched forward pass: $26,000 \times 0.07\text{ s} \approx \mathbf{1,820\text{ seconds}} = \mathbf{30.3\text{ minutes}}$ (up to 60 minutes with 3-class RoBERTa).
2. **Batching Opportunities**:
   - Probes are currently evaluated in a single batch in `evaluate_shared_probes`, but LIME/SHAP explanations run single unbatched forward passes.
   - Controlled XAI sampling and batched forward passes can reduce runtime by $>10\times$.

---

## 7. Current Visualization & Thesis Graphs

1. **Current Visualizer (`blindspot/reporting/visualizer.py`)**:
   - Only implements 4 single-model graphs:
     1. `plot_taxonomy_distribution` (Donut chart)
     2. `plot_behavioral_metrics` (Horizontal bar chart)
     3. `plot_attribution_comparison` (Token attribution shift)
     4. `plot_probe_alignment` (Jaccard & Cosine alignment)
   - These graphs are NOT automatically generated or saved into `runs/<run_id>/figures/` during runner execution (`figures/` remains empty).
2. **Missing Thesis Visualizations (Section 28 Requirements)**:
   - Needs full 15-graph suite:
     1. Model prediction distribution
     2. Behavioral flip rate by model
     3. Expected vs observed behavior
     4. Failure taxonomy distribution
     5. Confidence delta by probe
     6. Confidence delta by model
     7. Probe-level model comparison
     8. Model x probe behavioral heatmap
     9. Label transition matrix
     10. Probe consistency
     11. Model agreement
     12. Expected-change vs expected-preserve behavior
     13. Per-model performance summary
     14. Runtime/performance profile
     15. Probe category comparison

---

## 8. Current Reporting Architecture

1. **Current State**:
   - `ReportGenerator` produces `experiment_summary.md`, `failure_summary.md`, `probe_level_evidence.md` only at the end of the entire experiment.
   - No per-model report is generated incrementally upon model completion.
   - If 2 of 5 models are complete, no report exists for models 1 and 2.

---

## 9. Current Logging Architecture

1. **Current State**:
   - Uses standard Python `logging` and free-form prints.
   - `events.jsonl` records fine-grained events, but event types are ad-hoc strings.
   - `runner.py` emits `probe_evaluated` events with full text and dictionary payloads.
   - Console logs occasionally print tensor warning outputs from PyTorch / Transformers.

---

## 10. Current Test Runtime

1. **Current Test Runtime**:
   - `run_tests.py` ran 118 tests in **389.43 seconds (6.5 minutes)**.
   - **Bottleneck**: Tests load real HuggingFace transformer models (DistilBERT, ALBERT, RoBERTa, BERT) and execute full CPU forward passes and SHAP/LIME explainers inside unit test classes!
   - Unit tests must be decoupled from heavy real model weights using deterministic synthetic fixtures, bringing `run_tests.py` down to $<10$ seconds.

---

## 11. Storage Footprint & Repository Hygiene Inventory

### A. Storage Footprint Summary
- `runs/`: 45 files, **2.53 MB** (13 historical experiments — MUST BE PRESERVED).
- `logs/`: 1 file, **0.00 MB**.
- `scratch/`: 32 files, **0.07 MB** (diagnostic and audit scripts).
- `audit_reports/`: 31 files, **0.61 MB**.
- `blindspot/`: 122 files, **1.06 MB**.
- `tests/`: 60 files, **0.37 MB**.
- `docs/`: 5 files, **0.01 MB**.
- HuggingFace hub cache: 180 files, **6,331.82 MB (6.33 GB)**.
- Workspace total: 356 files, **5.27 MB** (excluding `.git` and HF cache).

### B. Documentation Sprawl Inventory (35 Markdown Files in Root)

| Category | File | Proposed Action | Rationale |
|---|---|---|---|
| **Research Protocol** | `PROBE_PROTOCOL.md` | **KEEP / MOVE TO `docs/`** | Canonical probe schema and contract specification |
| **Research Protocol** | `PROBE_SELECTION.md` | **KEEP / MOVE TO `docs/`** | Canonical probe selection rules |
| **Research Protocol** | `SEMANTIC_PROBE_DESIGN.md` | **KEEP / MOVE TO `docs/`** | Linguistic perturbation rules |
| **Architecture** | `ARCHITECTURE.md` | **KEEP / MOVE TO `docs/`** | System architecture specification |
| **Taxonomy** | `FAILURE_TAXONOMY.md` | **KEEP / MOVE TO `docs/`** | 4-way failure taxonomy definition |
| **Metrics** | `BEHAVIORAL_METRICS.md` | **KEEP / MOVE TO `docs/`** | Mathematical formulations for flip rate, consistency |
| **Metrics** | `FLIP_ANALYSIS.md` | **KEEP / MOVE TO `docs/`** | Prediction flip and transition mathematics |
| **Visualizations** | `DIAGNOSTIC_GRAPHS_GUIDE.md` | **KEEP / MOVE TO `docs/`** | Graph interpretations and visual guide |
| **Core Reference** | `CHANGELOG.md` | **KEEP IN ROOT** | Chronological record of releases and fixes |
| **Model Audit** | `MODEL_VALIDATION_REPORT.md` | **KEEP IN ROOT / `docs/`** | Empirical model audit and validation gate evidence |
| **Historical Audit** | `CURRENT_STATE_AUDIT_REPORT.md` | **KEEP IN ROOT** | Baseline audit of defects |
| **Historical Audit** | `PROBE_PIPELINE_AUDIT.md` | **KEEP IN ROOT** | 20-question probe protocol audit |
| **Historical Audit** | `RESEARCH_INTEGRITY_AUDIT.md` | **KEEP IN ROOT** | Behavioral taxonomy audit |
| **Obsolete Task Report** | `BROWSER_TEST_REPORT.md` | **ARCHIVE / CONSOLIDATE** | Historical task report |
| **Obsolete Task Report** | `FINAL_IMPLEMENTATION_REPORT.md` | **ARCHIVE / CONSOLIDATE** | Historical task report |
| **Obsolete Task Report** | `FINAL_PRODUCTION_READINESS_REPORT.md` | **ARCHIVE / CONSOLIDATE** | Historical task report |
| **Obsolete Task Report** | `FINAL_RESEARCH_INTEGRITY_REPORT.md` | **ARCHIVE / CONSOLIDATE** | Historical task report |
| **Obsolete Task Report** | `FINAL_UI_RELEASE_REPORT.md` | **ARCHIVE / CONSOLIDATE** | Historical task report |
| **Obsolete Task Report** | `IMPLEMENTATION_PROGRESS.md` | **ARCHIVE / CONSOLIDATE** | Historical task report |
| **Obsolete Task Report** | `IMPLEMENTATION_STEPS.md` | **ARCHIVE / CONSOLIDATE** | Historical task report |
| **Obsolete Task Report** | `PERFORMANCE_LOG.md` | **ARCHIVE / CONSOLIDATE** | Superseded performance log |
| **Obsolete Task Report** | `PERFORMANCE_REGRESSION.md` | **ARCHIVE / CONSOLIDATE** | Superseded performance log |
| **Obsolete Task Report** | `PRODUCTION_AUDIT.md` | **ARCHIVE / CONSOLIDATE** | Superseded production audit |
| **Obsolete Task Report** | `PRODUCTION_HARDENING.md` | **ARCHIVE / CONSOLIDATE** | Superseded hardening log |
| **Obsolete Task Report** | `PROJECT_STATE_REPORT.md` | **ARCHIVE / CONSOLIDATE** | Superseded project report |
| **Obsolete Task Report** | `TEST_STATUS.md` | **ARCHIVE / CONSOLIDATE** | Superseded test status report |
| **Obsolete Task Report** | `UI_IMPLEMENTATION.md` | **ARCHIVE / CONSOLIDATE** | Superseded UI report |
| **Obsolete Task Report** | `UI_UX_AUDIT.md` | **ARCHIVE / CONSOLIDATE** | Superseded UI audit |
| **Obsolete Task Report** | `UI_UX_DESIGN.md` | **ARCHIVE / CONSOLIDATE** | Superseded design spec |
| **Obsolete Task Report** | `project_questions_and_doubts.md` | **ARCHIVE / CONSOLIDATE** | Historical scratch notes |
| **Scratch Scripts** | `scratch/test_*.py` (30 scripts) | **MOVE ESSENTIAL TO `tests/` / ARCHIVE** | One-off diagnostic test scripts |

---

## 12. Verification & Next Steps

This pre-update state audit establishes the baseline facts of the repository. No source code or historical experiment runs were modified or deleted. We proceed to formulate the complete technical implementation plan adhering to all 12 implementation phases.
