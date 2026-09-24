# Test Status

## Baseline

Tests before restructuring:
- Total: 14
- Passed: 14
- Failed: 0
- Skipped: 0

## Current (v2.3.0 Research-Integrity Release)

- **Total**: 98
- **Passed**: 98
- **Failed**: 0
- **Skipped**: 0

## Test Suite Breakdown

| Suite | Tests | Status | Notes |
|---|:---:|:---:|---|
| Baseline Perturbations (Negation, Double Negation, Connectives, Substitution, Engine, Linguistic Analyzer) | 6 | PASS | Native spaCy + NLTK fallback verified |
| Baseline Models & Metrics | 2 | PASS | HuggingFaceWrapper and ECE verified |
| Baseline Behavioral Tester | 1 | PASS | Single-model probe evaluation |
| Baseline Explainability & Taxonomy | 3 | PASS | LIME, SHAP, Explainer selection, Taxonomy |
| Baseline Reports & Visualizer | 2 | PASS | Markdown report generation & Matplotlib plots |
| **Multiclass & Normalization** | 5 | PASS | Label mapping, ECE, transitions, shifts, formatted % |
| **Model Registry** | 3 | PASS | Preset catalog, custom registration, pre-verification |
| **Shared Probe Protocol** | 4 | PASS | Deterministic SHA-256 IDs, stimuli identity across Model A/B/C |
| **Cross-Model Analytics** | 3 | PASS | Model x Probe matrix, pairwise agreement, fingerprints |
| **Resource Manager** | 2 | PASS | Hardware detection, SAFE/BALANCED/PERFORMANCE/CUSTOM profiles |
| **Cache & Batching** | 2 | PASS | Thread-safe LRU eviction, batch consistency |
| **Live Events & Scheduler** | 4 | PASS | EventEmitter, AuditScheduler, Runner, Async cancellation |
| **Run Persistence** | 1 | PASS | RunStore lifecycle (config, metadata, events, results) |
| **Repeated Token Attribution & Position Awareness** | 4 | PASS | Positional attributions, non-contiguous indexing, alignment |
| **UI Components, Design System & Launchers** | 6 | PASS | Workstation design tokens, launcher scripts, port detection, rotating logging |
| **Canonical Probe Integrity & Pipeline Counts** | 20 | PASS | Determinism, multiclass flips, behavioral outcomes, stratified rates, validation, engines, pipeline count integrity |
| **Behavioral Taxonomy Synthetic Calibration** | 14 | PASS | Pure `classify_behavior`: Case 1 expected flip, Case 2 blind, Case 3 preserve, Case 4 spurious, Case 5-6 multiclass, Case 7 misweighted, Case 8 undetermined, model-independence, zero-retention |
| **Flip Analysis & Percentage-Point Deltas** | 8 | PASS | Multiclass transitions, `y_orig != y_pert`, pp delta calculations, aggregation |
| **Probe Calibration & Proverb Support** | 4 | PASS | Calibrated 7-probe suite, proverb pragmatic handling ("All that glitters is not gold"), invalid probe blocking, determinism |
| **Deterministic Acceptance Suite (Section 37)** | 4 | PASS | 7 generated / 4 selected / 2 models (exact 10 evaluations), all 7 (16 evals), 1 probe (4 evals), custom probe lifecycle |

## Last Test Run

- **Command**: `python run_tests.py`
- **Result**: `Ran 98 tests in 130.424s — OK`
