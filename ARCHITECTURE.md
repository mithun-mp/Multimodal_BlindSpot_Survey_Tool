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
| `blindspot.core` | Core type definitions, event pub/sub, configuration | `SemanticPolarity`, `ExpectationType`, `BehavioralRelation`, `ProbeExpectation`, `ModelMetadata`, `PredictionResult`, `BaselineEvaluation`, `LinguisticProbe`, `SharedProbeSet`, `RunPlan`, `ExecutionEvent`, `EventEmitter`, `ExperimentConfig` |
| `blindspot.semantic` | Canonical semantic ground truth, Gemini verification, human override, caching | `SemanticReferenceLabel`, `SemanticRelation`, `VerificationStatus`, `SemanticAnnotation`, `SemanticReferenceSet`, `SemanticAnnotationCache`, `GeminiSemanticClient`, `SemanticReferenceService` |
| `blindspot.models` | HF model wrapping, label normalization, caching, registry | `HuggingFaceWrapper`, `ModelRegistry`, `ModelCache`, `map_raw_label_to_semantic_polarity`, `normalize_label_name` |
| `blindspot.perturbations` | Linguistic synthesis, shared probe sets, expectation models, validation | `SharedProbeGenerator`, `ProbeValidator`, `infer_expected_semantic_effect`, `NegationPerturber`, `ConnectivePerturber`, `SynonymSubstitutionPerturber` |
| `blindspot.testing` | Multiclass behavioral testing, ECE calibration, transition matrices, metrics | `BehavioralTester`, `classify_behavior`, `compute_ece`, `compute_observed_flip_rate`, `compute_expected_flip_rate`, `compute_expected_flip_compliance`, `compute_preserve_rate`, `compute_behavioral_consistency`, `compute_raw_label_flip_rate`, `compute_polarity_flip_rate` |
| `blindspot.explainability` | Feature attributions, provenance, alignment, failure taxonomy | `LimeExplainerWrapper`, `ShapExplainerWrapper`, `TaxonomyClassifier`, `align_token_attributions`, `ExplanationResult` |
| `blindspot.analysis` | Cross-model comparative matrices, agreement, fingerprints | `CrossModelAnalyzer`, `ModelBehavioralFingerprint`, `compute_model_fingerprint` |
| `blindspot.execution` | Hardware monitoring, performance modes, async experiment runner | `ResourceManager`, `AuditScheduler`, `ExperimentRunner`, `PerformanceMode` |
| `blindspot.storage` | Self-contained run persistence and artifact discovery | `RunStore` |
| `blindspot.reporting` | Diagnostic Markdown reports and Matplotlib figures | `ReportGenerator`, `ThesisVisualizer` |
| `blindspot.ui` | Modular Streamlit research workstation interface | `render_overview`, `render_experiment_lab`, `render_comparison`, `render_live_run`, `render_semantic_reference_panel`, etc. |

---

## 3. Data & Execution Lifecycle
The auditing pipeline follows an immutable 8-stage sequence:
```text
TEXT ➔ SEMANTIC REFERENCE ➔ VERIFICATION ➔ SEMANTIC RELATION / CONTRACT ➔ IMMUTABLE RUN PLAN ➔ MODEL EXECUTION ➔ OBSERVED BEHAVIOR ➔ BEHAVIORAL CLASSIFICATION
```

1. **Configuration & Model Gate**: The researcher selects 1..N verified sentiment models from `ModelRegistry`. Models are cataloged by capability (2-class binary vs 3-class ternary). Non-sentiment models are gated and rejected.
2. **Immutable Baseline Evaluation**: Baseline stimuli are evaluated once per model, establishing anchored `BaselineEvaluation` records with full probability distributions and execution timing.
3. **Linguistic Probe Generation**: `SharedProbeGenerator` generates controlled probe stimuli. Probe definitions describe linguistic transformations (`semantic_intent = "ADD_NEGATION"`), NOT pre-judged model behavior or forced flips.
4. **Semantic Reference Annotation & Verification**:
   - Automated annotation via official `google-genai` SDK (`gemini-2.5-flash`) or local heuristic fallback (`LOCAL_HEURISTIC`, `UNVERIFIED`).
   - Pure affective polarity (`POSITIVE`, `NEGATIVE`, `NEUTRAL`) is separated from semantic relation (`PRESERVE_POLARITY`, `REVERSE_POLARITY`, `SHIFT_TO_NEUTRAL`, `SHIFT_FROM_NEUTRAL`, `CONTRAST_SHIFT`, `MEANING_CHANGED`, `UNCERTAIN`).
   - Human verification flow enables accepting, overriding, or marking uncertain. Overrides preserve original suggestions.
   - If Gemini is offline/disabled, confidence is strictly `None` (zero fabricated 0.75 confidence).
5. **Frozen RunPlan Staging**: All probe IDs, input texts, verified semantic polarities, and relations are locked into an immutable `RunPlan`. The execution runner is strictly prohibited from mutating semantic expectations.
6. **Execution Without Re-Generation**: `BehavioralTester` evaluates benchmark models against the frozen `RunPlan`. Raw predictions are recorded as empirical facts ($y_{\text{orig}}, y_{\text{pert}}$, probabilities, confidence).
7. **Deterministic Empirical Failure Diagnosis**:
   - Model capability-aware: Binary 2-class models on `NEUTRAL` inputs yield `NOT_DIRECTLY_REPRESENTABLE` / `UNREPRESENTABLE_NEUTRAL`, not `BLIND`.
   - 3-class neutral preservation is evaluated without spurious failure.
   - Diagnosed failure categories (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`, `NONE`) are derived deterministically from observed model outputs vs the frozen semantic contract. Gemini NEVER predicts failures.
8. **Storage, Reporting & Publication Visualizations**:
   - All provenance is persisted in `runs/<exp_id>/semantic_reference.json`, `predictions.json`, and Markdown reports.
   - Publication figures (15 thesis graphs) represent empirical observations without combining incompatible semantic conditions.
