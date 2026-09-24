# BlindSpot Architecture Specification

## 1. Architectural Overview

BlindSpot is a research-grade, model-agnostic auditing framework for black-box text classification models. It stress-tests classifiers against controlled linguistic perturbations, extracts and compares local feature attributions, diagnoses behavioral and reasoning failure patterns, and provides comparative multi-model research analytics.

```text
                                BLINDSPOT ARCHITECTURE
                                          │
        ┌─────────────────────────────────┴─────────────────────────────────┐
        │                                                                   │
   RESEARCH UI                                                       EXECUTION ENGINE
   (Streamlit Modular Pages)                                         (Asynchronous Worker)
        │                                                                   │
        ├── Overview & System Monitor                                ┌──────┴──────┐
        ├── Experiment Lab (Configuration)                           │             │
        ├── Model Lab (Registry & Cache)                      Model Registry  Model Cache
        ├── Probe Lab (Interactive Generator)                        │             │
        ├── Live Run Console (Log & Progress Stream)                 └──────┬──────┘
        ├── Model Comparison (Matrix & Fingerprints)                        │
        ├── Explanation Lab (Token Alignment & Provenance)            ResourceManager
        ├── Failure Analysis (4-Way Taxonomy)                               │
        ├── Reports & Artifacts Explorer                              AuditScheduler
        └── Run History Explorer                                            │
                                                                 Shared Probe Generator
                                                                            │
                                                                   ┌────────┴────────┐
                                                                   ▼                 ▼
                                                            Model A (Cached)  Model B (Cached)
                                                                   │                 │
                                                            Behavior & XAI    Behavior & XAI
                                                                   │                 │
                                                                   └────────┬────────┘
                                                                            ▼
                                                                   CrossModelAnalyzer
                                                                            │
                                                                   ┌────────┴────────┐
                                                                   ▼                 ▼
                                                             Run Persistence   Report Generator
                                                           (runs/<exp_id>/)   (Markdown & PNGs)
```

---

## 2. Core Modules & Responsibilities

| Package / Module | Responsibility | Key Abstractions |
| :--- | :--- | :--- |
| `blindspot.core` | Core type definitions, event pub/sub, configuration | `ModelMetadata`, `PredictionResult`, `LinguisticProbe`, `SharedProbeSet`, `ExecutionEvent`, `EventEmitter`, `ExperimentConfig` |
| `blindspot.models` | HF model wrapping, label normalization, caching, registry | `HuggingFaceWrapper`, `ModelRegistry`, `ModelCache`, `normalize_label_name` |
| `blindspot.perturbations` | Linguistic synthesis, shared probe sets, expectation models | `SharedProbeGenerator`, `infer_expected_semantic_effect`, `NegationPerturber`, `ConnectivePerturber`, `SynonymSubstitutionPerturber` |
| `blindspot.testing` | Multiclass behavioral testing, ECE calibration, transition matrices | `BehavioralTester`, `compute_ece`, `compute_flip_rate`, `compute_transition_matrix`, `compute_prediction_agreement` |
| `blindspot.explainability` | Feature attributions, provenance, alignment, failure taxonomy | `LimeExplainerWrapper`, `ShapExplainerWrapper`, `TaxonomyClassifier`, `align_token_attributions`, `ExplanationResult` |
| `blindspot.analysis` | Cross-model comparative matrices, agreement, fingerprints | `CrossModelAnalyzer`, `ModelBehavioralFingerprint`, `compute_model_fingerprint` |
| `blindspot.execution` | Hardware monitoring, performance modes, async experiment runner | `ResourceManager`, `AuditScheduler`, `ExperimentRunner`, `PerformanceMode` |
| `blindspot.storage` | Self-contained run persistence and artifact discovery | `RunStore` |
| `blindspot.reporting` | Diagnostic Markdown reports and Matplotlib figures | `ReportGenerator`, `Visualizer` |
| `blindspot.ui` | Modular Streamlit research workstation interface | `render_overview`, `render_experiment_lab`, `render_comparison`, `render_live_run`, etc. |

---

## 3. Data & Execution Lifecycle

1. **Configuration**: The user specifies 1..N models, 1..N input sentences, perturbation engines, explainer methods, and performance modes in the **Experiment Lab**.
2. **Shared Probe Protocol**: `SharedProbeGenerator` executes linguistic transformations **once** per input sentence. Each probe is assigned a stable ID (`probe_001`...) and an explicit `ExpectedSemanticEffect` (`REVERSE_POLARITY`, `PRESERVE_POLARITY`, `CONTRAST_SHIFT`, `INVARIANT`, or `UNCERTAIN`).
3. **Model Evaluation & Caching**: Models are requested from `ModelCache`. If not present, the model is initialized, its label schema inspected and normalized into `id2label`, and resident in memory. Probes are evaluated in accelerated batches via `predict_proba_batch()`.
4. **Explainability Extraction**: `LimeExplainerWrapper` or `ShapExplainerWrapper` computes local token attributions for original and perturbed texts. Provenance metadata (`explainer_requested`, `explainer_used`, `fallback_used`, `fallback_reason`, `runtime_ms`) is recorded.
5. **Taxonomy Diagnosis**: `TaxonomyClassifier` evaluates observed transitions and attribution patterns against traceable rules, classifying anomalies into `Blind`, `Spurious`, `Misweighted`, or `Undetermined`.
6. **Cross-Model Descriptive Synthesis**: `CrossModelAnalyzer` correlates outputs across models, computing:
   - Consensus agreement statistics (pairwise and unanimous)
   - Model × Probe Matrix (prediction, confidence %, and anomaly flag)
   - Model Behavioral Fingerprints (multi-dimensional sensitivity radar)
   - Cross-model attribution similarity
7. **Storage & Reporting**: `RunStore` persists all outputs to `runs/<experiment_id>/`. `ReportGenerator` compiles publication-grade Markdown reports and Matplotlib charts.
