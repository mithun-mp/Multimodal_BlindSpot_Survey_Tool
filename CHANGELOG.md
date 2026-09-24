# Changelog

All notable changes to the **BlindSpot** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.5.0] - 2026-09-22

### Added
- **Canonical Probe Lifecycle & Count Integrity Enforcement**:
  - Implemented bidirectional category matching table `DISPLAY_CATEGORY_TO_SUBTYPES` in `blindspot/perturbations/shared.py`.
  - Fixed 7 → 4 → 3 probe discrepancy bug where user category filtering caused silent probe drops.
  - Enforced runtime assertion: `planned == executed == analyzed == reported` across all models.
  - Added `RunPlan.validate_execution()` to strictly verify that executed probe IDs match selected probe IDs.
- **Pure Rule-Based Behavioral Taxonomy (Zero AI Predictions)**:
  - Formally verified and guaranteed that no predictive AI or LLM classifies model failures.
  - All diagnoses (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`, `NONE`) emerge purely from deterministic evaluation of model logits, signed confidence shifts ($\Delta c$), and explicit linguistic contracts.
- **5-Model Memory-Resident Cache Capacity**:
  - Configured default `model_cache_size = 5` in `ResourceConfig` across Balanced, Performance, and Custom modes.
  - Conditioned RAM eviction on `model_cache_size <= 1`, allowing all 5 benchmark models to stay warm in memory for sub-second repeat testing.
  - Added cache metadata tracking (`loaded_at`, `last_used`, `device`) and `get_cache_summary()`.
- **Progressive Completed-Model UI Revealing**:
  - Enhanced `blindspot/ui/live_run.py` to stream completed model metrics, baseline probabilities, flips, and failures immediately without blocking on remaining models.
  - Removed duplicate header markdown block.
  - Added interactive `▶ RESUME RUN` button in `blindspot/ui/run_history.py` wired to `ExperimentRunner.resume_run()`.
- **20-Point Canonical Pipeline Verification Suite (`tests/test_canonical_pipeline.py`)**:
  - Implemented exhaustive 20-point automated test covering every requirement: generated count, selected count, executed count, selection equality, baseline recording, binary normalization, multiclass normalization, flip detection, confidence delta calculation, behavioral outcomes, failure taxonomy, incremental persistence, resume capability, safe deletion, 5-model cache capacity, progressive UI state, 15 thesis figures, zero AI failure prediction, non-sentiment model rejection, and custom probe lifecycle.
  - Integrated into `run_tests.py` with 118/118 tests passing.
- **Safe Persistence & Lifecycle Engine (`blindspot/storage/run_store.py`)**:
  - Prohibited automatic run deletion. Historical experiment runs in `runs/` are strictly preserved.
  - Added `load_probe_set` and `load_run_plan` to faithfully restore exact probe stimuli upon run resumption.
  - Added `archive_run(exp_id)` to safely move runs to `runs/archived/<exp_id>`.
  - Added `delete_run(exp_id, confirmation=True)` requiring explicit confirmation for permanent deletion.
- **15 Publication-Grade Thesis Visualizations (`blindspot/reporting/thesis_graphs.py`)**:
  - Implemented 15 multi-model figures rendered at 300 DPI (`runs/<run_id>/figures/*.png`).
  - Saved raw plot data points into `runs/<run_id>/figures/source_data.json` for external chart reproduction.
  - Fixed token attribution unwrapping bug in `Visualizer.plot_attribution_comparison`.

## [2.4.0] - 2026-09-20


### Added
- **Model Validation Gate (`blindspot/models/registry.py`)**: Strict pre-benchmark registration gate enforcing task compatibility (`task == "SENTIMENT"`), label cardinality (`num_classes >= 2`), label mappings (`id2label`), numerical probability distributions, and documented semantics.
- **Active 5-Model Sentiment Benchmark Suite**: Validated 5 diverse sentiment architectures:
  1. `distilbert-base-uncased-finetuned-sst-2-english` (DistilBERT, 66.96M params, SST-2 binary)
  2. `textattack/albert-base-v2-SST-2` (ALBERT, 11.68M params, SST-2 binary)
  3. `cardiffnlp/twitter-roberta-base-sentiment-latest` (RoBERTa, 124.65M params, 3-class Twitter)
  4. `textattack/bert-base-uncased-SST-2` (BERT, 109.48M params, SST-2 binary)
  5. `cardiffnlp/twitter-roberta-base-sentiment` (RoBERTa Base, 124.65M params, 3-class Twitter)
- **Model Validation Report (`MODEL_VALIDATION_REPORT.md`)**: Full empirical audit detailing gate checks, architectural parameters, benchmark diagnostics on 5 standardized test sentences, and formal exclusion rationale for non-sentiment and incompatible checkpoints.
- **Research Repair Acceptance Matrix (`tests/test_research_repair.py`)**: 20 unit and deterministic acceptance tests covering model rejection, label normalization, strict count integrity ($\text{Planned} == \text{Executed} == \text{Analyzed} == \text{Reported}$), synthetic taxonomy calibration (BLIND, SPURIOUS, MISWEIGHTED, NONE, UNDETERMINED), and a $5 \times 1\text{ baseline} + 5 \times 4\text{ probes} = 25\text{ evaluations}$ acceptance run. All 118 tests in `run_tests.py` now pass.

### Fixed
- **DEF-01: Non-Sentiment Model Infiltration**: `roberta-base-openai-detector` was reclassified with task `AI_TEXT_DETECTION` and labels `["Fake", "Real"]`. Strictly rejected from sentiment experiments; silent remapping (`Fake` -> `Negative`, `Real` -> `Positive`) eliminated.
- **DEF-02: Category Key Matching Mismatch**: Enhanced `_is_category_match` in `blindspot/perturbations/shared.py` to robustly handle both string and list inputs, as well as lexical, syntax, and intensity aliases.
- **DEF-03: Silent Fallback to Heuristic Probabilities**: Added `allow_fallback=False` enforcement to `HuggingFaceWrapper` in benchmark mode. Broken or unloaded models raise explicit exceptions rather than silently generating pseudo-random heuristic predictions.
- **DEF-04: AttributeError on `ev.original_label` in Runner**: Resolved safe access across `PredictionResult`, `ModelProbeEvaluation`, and dict representations in `blindspot/execution/runner.py`.
- **DEF-05: Count Integrity Violations**: If a model fails or evaluations mismatch, run is marked `FAILED`/`INCOMPLETE` with analysis status `NO_VALID_ANALYSIS` and failure counts set to `None`, never converted to zero failures.
- **UI Model Filtering**: Updated `blindspot/ui/experiment_lab.py` to query `registry.list_sentiment_models()`, preventing non-sentiment models from entering benchmark runs. Added visual task badges in `blindspot/ui/model_lab.py`.

## [2.3.0] - 2026-09-20

### Added
- **Pure Isolated Behavioral Classifier (`blindspot/testing/behavioral.py`)**: Implemented standalone, deterministic `classify_behavior(...)` function with zero UI or model name bias. Classifies primary behavioral outcomes (`EXPECTED_FLIP`, `MISSING_FLIP`, `UNEXPECTED_FLIP`, `EXPECTED_PRESERVE`, `UNEXPECTED_CHANGE`, `UNDETERMINED`) and secondary failure taxonomy (`NONE`, `BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`).
- **Calibrated 7-Probe Diagnostic Suite (`blindspot/perturbations/shared.py`)**: Generates balanced expected flips and expected preserves across 7 diagnostic categories (`P001` negation reversal, `P002` double negation preserve, `P003` intensifier strengthen, `P004` downtoner weaken, `P005` synonym/proverb preserve, `P006` adversative contrast flip, `P007` structural framing preserve).
- **Pragmatic Proverb Support (`blindspot/core/types.py`, `blindspot/perturbations/shared.py`)**: Added `SentenceType.PROVERB` and calibrated semantic preservation for non-literal structures such as *"All that glitters is not gold."*.
- **Comprehensive Synthetic Calibration Suite (`tests/test_behavioral_taxonomy.py`)**: 14 unit tests proving all 8 synthetic benchmark cases: Case 1 Expected Flip, Case 2 Blind, Case 3 Expected Preserve, Case 4 Spurious, Case 5-6 Multiclass Flip/No-Flip, Case 7 Misweighted (strengthening drop, downtoning surge, flipped label), Case 8 Undetermined, model independence, and zero-failure retention.
- **Flip Analysis & Percentage-Point Delta Tests (`tests/test_flip_analysis.py`)**: 8 unit tests covering multiclass transitions, signed confidence shifts in percentage points ($(\text{probe} - \text{orig}) \times 100$), and transition matrix calculation.
- **Probe Calibration Tests (`tests/test_probe_calibration.py`)**: 4 unit tests covering the 7-candidate generator, proverb pragmatic processing, invalid probe execution blocking, and determinism.
- **Deterministic Acceptance Suite (`tests/test_deterministic_acceptance.py`)**: 4 unit tests covering Section 37 deterministic acceptance requirements: 7 generated / 4 selected / 2 models producing exactly 10 evaluations (2 baselines + 8 probes), 16 evals on 7 probes, 4 on 1 probe, and custom probe lifecycle.
- **Live Run Diagnostic Event Cards (`blindspot/ui/live_run.py`)**: Section 29 research event cards streaming model, probe ID, category, baseline/probe predictions, transition, confidence delta (pp), flip status, expected effect, behavioral outcome, and failure taxonomy.
- **Probe Lab Workbench Enhancements (`blindspot/ui/probe_lab.py`)**: Telemetry metrics (Generated, Selected, Verified), Select Category, Verify Selected, Edit Probe (new version generation with `USER_EDITED` status), and JSON probe set export.
- **All 21 Research-Valid Reporting Fields (`blindspot/execution/runner.py`)**: Reports (`experiment_summary.md`, `probe_level_evidence.md`, `failure_summary.md`) retain baseline evaluations, probe-level evidence, failure rationales, cross-model agreement, and never suppress zero categories.
- **Methodological Documentation**: Created `RESEARCH_INTEGRITY_AUDIT.md`, `FAILURE_TAXONOMY.md`, `PROBE_CALIBRATION.md`, and updated all project documentation.

### Fixed
- **Root Cause of Universal Zero Behavioral Failures**: Fixed key mismatch in `infer_expected_semantic_effect` where perturber types (`negation_insertion`, `negation_removal`, `contrast_negative_append`) defaulted to `expected_flip = False`. When models failed on negation, `is_flipped == expected_flip` (`False == False`), falsely rewarding model blindness as `EXPECTED_PRESERVE`.
- **7 → 4 → 3 Pipeline Count Discrepancy**: Eliminated re-generation and silent probe filtering; Live Run strictly executes the finalized `RunPlan`.
- **Decoupled XAI from Failure Diagnosis**: Failures are primary behavioral observations detected during inference regardless of whether explainability is enabled.

## [2.2.0] - 2026-09-20

### Added
- **Canonical Probe Protocol (`blindspot/core/types.py`, `blindspot/perturbations/shared.py`)**: Unified end-to-end data model for `LinguisticProbe` and `SharedProbeSet` with deterministic SHA-256 identification, schema versioning (`2.2.0`), pragmatic sentence tagging, semantic intent classification (`SemanticIntent`), and schema validation (`validate()`).
- **Dedicated Baseline Evaluation (`blindspot/core/types.py`, `blindspot/testing/behavioral.py`)**: Standalone `BaselineEvaluation` record evaluated and stored first per model prior to perturbation inference, establishing the true baseline for all transitions.
- **Canonical Prediction Flip & Stratified Behavioral Metrics (`blindspot/core/types.py`, `blindspot/testing/metrics.py`)**:
  - `is_prediction_flip(orig_label, pert_label)`: Multiclass-safe flip detection ($y_0 \neq y_p$).
  - `classify_behavioral_outcome(...)`: Canonical outcomes (`EXPECTED_FLIP`, `MISSING_FLIP`, `EXPECTED_PRESERVE`, `UNEXPECTED_FLIP`).
  - `compute_observed_flip_rate`: Volatility fraction across all executed probes.
  - `compute_expected_flip_rate`: Success rate on probes expecting polarity inversion.
  - `compute_preserve_rate`: Invariance rate on probes expecting label preservation.
  - `compute_behavioral_consistency`: Overall expectation compliance score.
  - `compute_confidence_flip_rate`: Sensitivity rate on drops $\ge 20.0$ percentage points.
- **Intensity & Structural Perturbation Engines (`blindspot/perturbations/intensity.py`, `structure.py`)**:
  - `IntensityPerturber`: Tests degree-sensitivity via intensifiers (`extremely`, `truly`) and downtoners (`somewhat`, `slightly`) with `expected_flip=False`.
  - `StructurePerturber`: Tests syntactic robustness via comma-separated clause inversion, discourse framing, and punctuation drift with `expected_flip=False`.
- **Interactive Probe Research Workbench (`blindspot/ui/probe_lab.py`)**: Interactive candidate catalog with checkboxes per probe, batch selection (`[Select All]`, `[Select None]`), pragmatic sentence presets (Literal, Proverb, Idiom, Figurative, Sarcastic, Ironic), custom probe injection (`+ Add Custom Probe`), schema validation, and 1-click staging (`[Send to Experiment Lab]`).
- **Top Navigation Workstation Layout (`blindspot/ui/shell.py`, `ui/design_system.py`)**: Sleek horizontal top navigation bar across the 7 functional domains (`Overview | Experiment | Probes | Run | Analyze | Reports | System`) with secondary domain subtabs, complemented by a minimized contextual sidebar.
- **Exact Run Plan & Count Integrity Verification (`blindspot/ui/experiment_lab.py`, `execution/runner.py`, `ui/live_run.py`)**:
  - Single-screen Run Plan table: Original Baselines ($M \times S$) + Selected Probes ($M \times N$) = Total Model Predictions.
  - Post-run count integrity verification audit guaranteeing $\text{planned} == \text{executed} == \text{analyzed} == \text{reported}$.
- **Baseline vs Perturbation Thesis Matrix (`blindspot/ui/comparison.py`)**: Dedicated thesis section rendering seed sentences with original model baseline predictions alongside stratified behavioral robustness summaries.
- **20 Targeted Probe Integrity Tests (`tests/test_probe_integrity.py`)**: Added full test suite verifying probe determinism, multiclass flip evaluation, behavioral outcomes, stratified rates, schema validation, perturbation engines, and execution count integrity. Total passing tests: 68.
- **Methodological Documentation**: Added `PROBE_PROTOCOL.md`, `PROBE_SELECTION.md`, `BEHAVIORAL_METRICS.md`, `FLIP_ANALYSIS.md`, `SEMANTIC_PROBE_DESIGN.md`, and `FINAL_RESEARCH_INTEGRITY_REPORT.md`.

### Changed
- **Pipeline Separation of Concerns**: Decoupled Generation $\neq$ Selection $\neq$ Execution. When a verified probe set is staged, `ExperimentRunner` executes it directly without re-generation.
- **Diagnostic Layer Framing (`blindspot/ui/failure_lab.py`)**: Framed 4-way failure taxonomy (`Blind`, `Spurious`, `Misweighted`, `Undetermined`) as a secondary diagnostic layer explaining root causes of behavioral failures, rather than dominating primary thesis metrics.

---

## [2.1.0] - 2026-09-20

### Added
- **One-Click Windows Launcher (`launch_blindspot.bat`)**: Double-clickable batch launcher with environment check, dependency validation, and browser auto-launch.
- **PowerShell Launcher & Desktop Shortcut (`launch_blindspot.ps1`, `create_blindspot_shortcut.ps1`)**: Native PowerShell launcher and non-admin Windows desktop shortcut generator.
- **Supervisor Process Manager (`blindspot/launcher.py`)**: Automatic port resolution (checks 8501, re-attaches to active instances, or locates next free port) and graceful Ctrl+C shutdown.
- **Structured Subsystem Logging (`blindspot/core/logging_config.py`)**: Added rotating file logging in `logs/blindspot.log` (5MB rotating handler) and formatted subsystem tagging (`BOOT`, `UI`, `MODEL`, `CACHE`, `RUNNER`, `PROBE`, `XAI`, `RESOURCE`, `STORAGE`, `REPORT`).
- **Dedicated System Console (`blindspot/ui/console.py`)**: Built-in monospace engineering terminal with real-time log streaming, severity filtering, subsystem filtering, substring search, and log download.
- **Centralized Workstation Dark Design System (`blindspot/ui/design_system.py`)**: Dark-first technical styling tokens, slim custom 6px scrollbars, and monospace telemetry typography.
- **Persistent Telemetry Header & Shell (`blindspot/ui/shell.py`)**: Host hardware telemetry (CPU%, cores, RAM%, GPU acceleration, persisted run counter) and grouped navigation across 6 functional domains.
- **Guided 5-Step Experiment Workflow (`blindspot/ui/experiment_lab.py`)**: Unified single-screen setup: `01 INPUT` (text area, research examples, token counter) -> `02 MODELS` (technical cards with `LOADED` vs `STANDBY` cache badges) -> `03 PROBES` (categories, deterministic SHA-256 badge, live probe preview) -> `04 EXECUTION` (specification card, prominent `▶ RUN EXPERIMENT` / `■ CANCEL RUN`) -> `05 REVIEW`.
- **Enhanced Live Run Experience (`blindspot/ui/live_run.py`)**: Live elapsed timer (`MM:SS`), dynamic ETA calculation (`~MM:SS`), per-model progress status meters (`DistilBERT: 18/18 ● COMPLETED`), and terminal event stream.
- **Control Center Overview (`blindspot/ui/overview.py`)**: Control center with quick-action buttons (`[NEW EXPERIMENT]`, `[LOAD RUN]`, `[OPEN CONSOLE]`), host resource cards, recent activity table, and latest findings summary.
- **Model × Probe Comparison Matrix (`blindspot/ui/comparison.py`)**: High-density response matrix with compact prediction columns, agreement filters, and confidence deltas.
- **Scientific Evidence Records (`blindspot/ui/failure_lab.py`)**: Structured evidence cards with observed vs expected behavioral transitions, confidence deltas, and actionable remediation steps.
- **Token Explainability Provenance (`blindspot/ui/explanation_lab.py`)**: Side-by-side attribution bars, alignment scores (Jaccard/Cosine), and transparent provenance badges (`NATIVE: SHAP`, `NATIVE: LIME`, `FALLBACK: LOO`).
- **Research Run Archive (`blindspot/ui/run_history.py`)**: Tabular run history with inspector, report download, and one-click session reloading.
- **5 Curated Model Presets (`blindspot/models/registry.py`)**: Added `cardiffnlp/twitter-roberta-base-sentiment` (Twitter RoBERTa Classic, 3-Class) as the 5th curated benchmark preset alongside DistilBERT SST-2, Twitter RoBERTa 3-Class Latest, BERT Base SST-2, and RoBERTa OpenAI Detector.
- **Import Resolution & Module Search Hardening**: Added `sys.path.insert` across `blindspot/app.py` and all 16 test files in `tests/`, injected `PYTHONPATH` in `blindspot/launcher.py`, `launch_blindspot.bat`, and `launch_blindspot.ps1`, and registered editable package in site-packages, eliminating all `ModuleNotFoundError` issues across all standalone and subprocess workflows.
- **UI & Launcher Test Suite (`tests/test_ui_and_launchers.py`)**: 6 comprehensive unit tests validating page modules, design tokens, components, structured logging, and port resolution.

### Changed
- **Entrypoint Cleanliness (`blindspot/app.py`)**: Encapsulated Streamlit startup inside clean `main()` entrypoint, eliminated dead legacy code blocks, and preserved all test-facing helper functions.

---

## [0.2.1] - 2026-09-19

### Hardened & Fixed (Production Reality Audit)
- **Multiclass Calibration (`blindspot/testing/behavioral.py`)**: Fixed multiclass ECE expected index calculation under expected flips; replaced inverted `1 - orig_idx` logic with dynamic expectation satisfaction mapping.
- **Dynamic Transition Narrative (`blindspot/app.py`)**: Removed hardcoded `opposite_label = NEGATIVE if POSITIVE else POSITIVE` in `get_failure_narrative`; now supports arbitrary multiclass label schemas.
- **Cross-Platform Console Compatibility (`blindspot/core/types.py`)**: Replaced Unicode block characters in `PredictionResult.formatted_distribution_ascii` with ASCII bracket meters (`[====================]`) to prevent `UnicodeEncodeError` on Windows cp1252/cp437 consoles.
- **Performance Mode Enums & Safety (`blindspot/core/config.py`, `execution/resources.py`)**: Added first-class `SAFE`, `BALANCED`, `PERFORMANCE`, `CUSTOM` modes and prevented Enum re-parsing recursion.
- **HuggingFace Pipeline Multi-Score Safety (`blindspot/models/huggingface_wrapper.py`)**: Added three-stage fallback for pipeline probability calls (`top_k=None`, `return_all_scores=True`) preventing top-1 probability clipping. Injected `device` and `model_status` into `PredictionResult`.
- **UI Research Telemetry (`blindspot/ui/components.py`, `ui/system_monitor.py`)**: Upgraded `render_prediction_card` to show active device, latency in ms, model readiness status, confidence %, class probability meters, and dense workstation telemetry. Set GPU metric to explicitly display `Not detected` when CUDA is unavailable.
- **Test Suite Expansion (`tests/test_shared_probes.py`, `tests/test_live_events_and_jobs.py`)**: Added `test_multimodel_identical_probe_stimuli_and_ids` proving Model A probe IDs == Model B probe IDs == Model C probe IDs, and `test_experiment_runner_async_and_cancellation` validating background thread cancellation.

## [0.2.0] - 2026-09-19

### Added
- **Core Types (`blindspot/core/types.py`)**: Added dataclasses `ModelMetadata`, `PredictionResult`, `LinguisticProbe`, `SharedProbeSet`, `ModelProbeEvaluation`, `ExplanationResult`, `FailureDiagnosis`, and enums `ExpectedSemanticEffect`, `FailureCategory`.
- **Event System (`blindspot/core/events.py`)**: Added `ExecutionEvent` and thread-safe `EventEmitter` pub/sub dispatcher for live UI log streaming and progress observation.
- **Configuration (`blindspot/core/config.py`)**: Added `PerformanceMode` (`SAFE`, `BALANCED`, `PERFORMANCE`, `CUSTOM`), `ResourceConfig`, and `ExperimentConfig`.
- **Model Registry & Verification (`blindspot/models/registry.py`)**: Added `ModelRegistry` supporting preset catalogs and pre-execution model verification without downloading multi-gigabyte checkpoints.
- **Model Caching (`blindspot/models/cache.py`)**: Added thread-safe `ModelCache` implementing LRU eviction and memory reclamation across multiple sentences and probes.
- **Shared Probe Protocol (`blindspot/perturbations/shared.py`)**: Added `SharedProbeGenerator` generating identical controlled linguistic probes with stable IDs (`probe_001`...) once per input, shared across all models.
- **Expectation Engine (`blindspot/perturbations/shared.py`)**: Added `infer_expected_semantic_effect` to scientifically distinguish expected reversals, preservation, and contrast shifts from anomalous behavior.
- **Multiclass Behavioral Metrics (`blindspot/testing/metrics.py`)**: Added `compute_transition_matrix`, `compute_confidence_shifts`, `compute_prediction_agreement`, and multiclass-safe `compute_ece`.
- **Behavioral Batch Inference (`blindspot/testing/behavioral.py`)**: Added batch inference acceleration for `SharedProbeSet` probe arrays and multiclass label transition tracking.
- **Explainability Provenance (`blindspot/explainability/`)**: Added provenance tracking to `LimeExplainerWrapper` and `ShapExplainerWrapper` recording requested explainer, actual explainer, fallback status, fallback reason, and runtime.
- **Refactored 4-Way Failure Taxonomy (`blindspot/explainability/taxonomy.py`)**: Expanded failure taxonomy to `Blind`, `Spurious`, `Misweighted`, and `Undetermined`, returning structured `FailureDiagnosisDict` with empirical evidence and actionable remedies.
- **Cross-Model Descriptive Analytics (`blindspot/analysis/`)**: Added `CrossModelAnalyzer` and `ModelBehavioralFingerprint` calculating Model × Probe Matrix, consensus agreement rates, and multi-dimensional behavioral profiles.
- **Resource Management & Concurrency (`blindspot/execution/`)**: Added `ResourceManager` with host hardware detection (CPU/RAM/GPU), `AuditScheduler`, and `ExperimentRunner` for non-blocking asynchronous background execution.
- **Reproducible Run Storage (`blindspot/storage/run_store.py`)**: Added `RunStore` managing self-contained run artifacts under `runs/<experiment_id>/` (`config.json`, `metadata.json`, `events.jsonl`, `results.json`, `reports/`, `figures/`).
- **Comparative Visualizations (`blindspot/reporting/visualizer.py`)**: Added `plot_model_probe_matrix`, `plot_cross_model_fingerprints`, and `plot_cross_model_failures`.
- **Executive Experiment Reporting (`blindspot/reporting/report_generator.py`)**: Added `generate_experiment_reports` generating `experiment_summary.md` and `cross_model_comparison.md`.
- **Modular Research UI (`blindspot/ui/`)**: Replaced monolithic UI with 11 modular research pages: Overview, Experiment Lab, Model Lab, Probe Lab, Live Run, Model Comparison, Explanation Lab, Failure Analysis, Reports & Artifacts, Run History, and System Monitor.

### Changed
- **Hugging Face Wrapper (`blindspot/models/huggingface_wrapper.py`)**: Generalised beyond binary `"NEGATIVE"`/`"POSITIVE"` labels to support arbitrary N-class classifiers with normalized label mappings, batch inference, latency timing, and CUDA OOM resilience.
- **Main Dashboard (`blindspot/app.py`)**: Refactored entrypoint to route cleanly across modular UI components with responsive session state while maintaining backward-compatible helper functions.

---

## [0.1.0] - 2026-09-01

### Added
- Initial SRS-compliant prototype implementation.
- Single-model `AuditPipeline`.
- Negation, double negation, connectives, and synonym substitution perturbation engines.
- Basic LIME and SHAP explainability wrappers with LOO fallback.
- 3-way SRS failure taxonomy (`Blind`, `Spurious`, `Misweighted`).
- Markdown report generator and Matplotlib visualizer.
- Streamlit dashboard and CLI.
