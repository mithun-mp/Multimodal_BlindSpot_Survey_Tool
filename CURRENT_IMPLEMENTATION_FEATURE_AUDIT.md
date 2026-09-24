# BLINDSPOT — COMPLETE PRE-IMPLEMENTATION FEATURE AUDIT
**Document**: `CURRENT_IMPLEMENTATION_FEATURE_AUDIT.md`  
**Audit Type**: Complete Read-Only Architectural, Scientific, and Engineering Integrity Audit  
**Date**: September 21, 2026  
**Auditor**: Lead Research-Software Architect & NLP Behavioral Evaluation Specialist  
**Workspace**: `c:\Dev\Projects\BlinkSpot-main`  
**Target File**: Single audit report generated at root; zero existing source files modified.

---

## 1. Executive Summary

This audit performs an exhaustive, empirical, read-only analysis of the **BlindSpot** text classifier auditing framework. 

BlindSpot is designed to answer a fundamental scientific question in explainable, robust NLP:
> *"Does a target sentiment classifier maintain behavioral and explanatory integrity under controlled, meaning-preserving or polarity-reversing linguistic perturbations, or does it exhibit systematic behavioral blind spots?"*

### Overall System Status:
1. **Core Scientific Integrity**:
   - The framework's diagnostic engine ([blindspot/testing/behavioral.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/testing/behavioral.py)) operates strictly via **empirical behavioral observation** ($y_{\text{orig}}$ vs $y_{\text{pert}}$, $\Delta c$) contrasted against explicit linguistic contracts (`expected_flip`, `expected_label_relation`).
   - **Zero AI-prediction heuristics** or "AI-predicted failure" models exist in the code. The taxonomy classification (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`, `NONE`) is a deterministic, rule-based diagnostic evaluation of actual transformer forward passes.
2. **Multimodel Benchmark Health**:
   - Evaluates **5 validated sentiment models** (DistilBERT SST-2, ALBERT Base SST-2, RoBERTa Twitter Latest 3-class, BERT Base SST-2, and RoBERTa Twitter Base 3-class).
   - The non-sentiment `roberta-base-openai-detector` (AI text detector) is isolated and marked ineligible for sentiment benchmarks.
   - Benchmark execution time has been reduced from $\sim 1\text{ hour}$ to **94.98 seconds (1.58 minutes)** for 5 models $\times$ 5 stimuli (25 evaluations) with LIME and SHAP explainability.
3. **Graph & Visualization Mechanisms**:
   - Features dual visualizers: **15 publication-grade thesis figures** at 300 DPI + `source_data.json` ([thesis_graphs.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/reporting/thesis_graphs.py)) and **4 classic diagnostic engineering plots** ([visualizer.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/reporting/visualizer.py)).
   - Fully exposed in the Streamlit UI with an interactive single-figure inspector, multi-column gallery, comparative charts, and inline markdown report rendering.
4. **Key Remaining Issues**:
   - `P0`: In `SharedProbeGenerator.generate_probes()`, when `candidate_count == 7` (the default), `_generate_calibrated_7_probes()` generates all 7 probes without filtering by `perturbation_types` unless filtered downstream by `selected_probe_ids`.
   - `P1`: Experiment resumption (`ExperimentRunner.resume_run`) is fully implemented in the backend, but is not exposed as a button in the UI (`run_history.py`).
   - `P2`: Redundant duplicate header rendering in `blindspot/ui/live_run.py` lines 134-153.
   - `P3`: Subtly conflicting versions in UI footer/sidebar (`v2.2.0` vs `v2.3.0`).
   - `P4`: Legacy `audit_reports/` directory contains dead single-model artifacts superseded by `runs/`.

---

## 2. Current Architecture

BlindSpot is structured as a layered, modular research workstation:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             STREAMLIT UI WORKSTATION                             │
│  Overview  |  Experiment Lab  |  Probe Lab  |  Live Run  |  Comparison  | Reports │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ Configures / Inspects
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            EXECUTION RUNNER & RUN PLAN                           │
│  • ExperimentRunner (Background Daemon Thread, Event Emitter, Resume Mode)        │
│  • RunPlan (Immutable Audit Manifest: Model IDs, Probe IDs, Seed Baselines)      │
│  • ResourceManager (Host CPU Cores, Memory Headroom, CUDA / Device Allocation)  │
└──────────────────┬─────────────────────────────────────────────┬─────────────────┘
                   │ Sequential Model Execution                  │ Probe Staging
                   ▼                                             ▼
┌──────────────────────────────────────┐     ┌─────────────────────────────────────┐
│       DUAL-TIER MODEL CACHE          │     │       SHARED PROBE PROTOCOL         │
│ • Disk Cache (HuggingFace Hub: 6.3GB)│     │ • PerturbationEngine (6 perturbers) │
│ • Resident RAM LRU Cache (max_size=1)│     │ • SharedProbeGenerator (7 Calibrated│
│ • HuggingFaceWrapper (Pipelines)     │     │ • Deterministic SHA-256 Identifiers │
└──────────────────┬───────────────────┘     └──────────────────┬──────────────────┘
                   │ Forward Passes                             │ Identical Stimuli
                   └─────────────────────┬──────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           BEHAVIORAL TESTING ENGINE                              │
│  • Baseline Evaluation (Evaluated once per unique seed sentence per model)       │
│  • Batch Probe Inference (Batch size 16/32, vectorized Softmax distributions)    │
│  • Pure Behavioral Outcome Classifier (classify_behavior: Flip vs Preserve)      │
│  • 4-Way Failure Taxonomy (BLIND, SPURIOUS, MISWEIGHTED, UNDETERMINED, NONE)     │
│  • Behavioral Metrics (Observed/Expected Flip, Preserve, Consistency, ECE)       │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ Explanations & Artifacts
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                        EXPLAINABILITY & PERSISTENCE                              │
│  • LimeExplainerWrapper & ShapExplainerWrapper (with LOO Fallback & Provenance)  │
│  • RunStore (Incremental per-model disk persistence, metadata.json, events.jsonl)│
│  • Visualizers (15 Publication Figures + 4 Classic Diagnostic Charts + JSON Data)│
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Original Thesis Functionality

The core scientific objective of the original BlindSpot thesis is the **empirical auditing of black-box NLP classification models through controlled semantic perturbations**.

### Input
- **Original Sentence ($x_0$)**: The unperturbed seed sentence provided by the researcher (e.g. `"All that glitters is not gold."` or `"The movie was great and the acting was top notch."`).
- **Original Prediction ($\hat{y}_0$)**: The discrete predicted class label on $x_0$ (e.g. `POSITIVE`, `NEGATIVE`, `NEUTRAL`).
- **Original Confidence ($c_0$)**: The maximum Softmax posterior probability $P(\hat{y}_0 \mid x_0) \in [0.0, 1.0]$.
- **Original Probability Distribution ($p_0$)**: Full vector over the label space (e.g. `{"NEGATIVE": 0.0018, "POSITIVE": 0.9982}`).

### Linguistic Perturbation Mechanisms
The original thesis defined four primary perturbation categories, now extended to six:
1. **Negation (`negation`)**: Polarity-reversing syntactic negation insertion (`"is not"`, `"did not"`) or removal.
2. **Double Negation (`double_negation`)**: Meaning-preserving double syntactic negation (`"not untrue"`, `"not entirely without merit"`).
3. **Connective / Contrast Manipulation (`connective`)**: Discourse connective shifts appending adversative or concessive clauses (`", however it failed..."`, `"Although..."`).
4. **Lexical Synonym Substitution (`synonym_substitution`)**: Meaning-preserving WordNet adjective/verb replacements (`"great"` $\to$ `"superb"`).
5. **Intensity Modulation (`intensity`)**: Meaning-preserving degree intensification (`"extremely"`) or downtoning (`"somewhat"`).
6. **Syntactic Structure Variation (`structure`)**: Meaning-preserving clause fronting or discourse framing (`"In fact, ..."`).

### Behavioral Analysis
- **Prediction Comparison**: Compares $\hat{y}_0$ against $\hat{y}_p$ (perturbed prediction).
- **Observed Flip Detection**: Binary or multiclass inequality: $\hat{y}_0 \neq \hat{y}_p$.
- **Signed Confidence Shift**: $\Delta c_{\text{pts}} = (c_p - c_0) \times 100.0$ percentage points.
- **Contract Fulfillment**: Verifies whether observed transitions match probe expectations (`expected_flip == is_flipped`).
- **Behavioral Consistency**: Proportion of evaluable probes satisfying contract expectations.

### Explainability
- **LIME (`LimeExplainerWrapper`)**: Local linear surrogates over perturbed word masks.
- **SHAP (`ShapExplainerWrapper`)**: Game-theoretic Shapley values using partition tree maskers.
- **LOO Fallback (`_leave_one_out_explain`)**: Deterministic word-omission importance scoring when third-party libraries fail.
- **Token Alignment (`align_token_attributions`)**: Positional alignment tracking word attribution shifts before and after perturbation.

---

## 4. Current Multimodel Functionality

The following table summarizes all modern multimodel enhancements:

| Component | File Path | Implementation Status | Pipeline Connected? | UI Exposed? |
| :--- | :--- | :---: | :---: | :---: |
| **Model Registry** | [blindspot/models/registry.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/models/registry.py) | Complete | Yes | Yes (Step 02) |
| **Dual Model Cache** | [blindspot/models/cache.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/models/cache.py) | Complete | Yes | Yes (Meters/Settings) |
| **Shared Probe Protocol** | [blindspot/perturbations/shared.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/perturbations/shared.py) | Complete | Yes | Yes (Probe Lab) |
| **Cross-Model Analysis** | [blindspot/analysis/cross_model.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/analysis/cross_model.py) | Complete | Yes | Yes (Comparison) |
| **Model $\times$ Probe Matrix** | [blindspot/analysis/cross_model.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/analysis/cross_model.py) | Complete | Yes | Yes (Comparison) |
| **Behavioral Fingerprints** | [blindspot/analysis/fingerprint.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/analysis/fingerprint.py) | Complete | Yes | Yes (Comparison) |
| **Resource Manager** | [blindspot/execution/resources.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/execution/resources.py) | Complete | Yes | Yes (Workstation Header) |
| **Async Runner** | [blindspot/execution/runner.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/execution/runner.py) | Complete | Yes | Yes (Live Run) |
| **Granular RunStore** | [blindspot/storage/run_store.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/storage/run_store.py) | Complete | Yes | Yes (Run History) |
| **Thesis Visualizer (15 Figs)**| [blindspot/reporting/thesis_graphs.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/reporting/thesis_graphs.py) | Complete | Yes | Yes (Reports Tab 1) |
| **Classic Visualizer (4 Figs)**| [blindspot/reporting/visualizer.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/reporting/visualizer.py) | Complete | Yes | Yes (Reports Tab 2) |

---

## 5. Critical: Observed Failure vs Predicted Failure Audit

The prompt requires a thorough audit to verify whether any code in BlindSpot uses an AI system to "predict" future failures instead of observing actual model behavior.

### Repository Search Results:
A comprehensive regex search across all source and test files for:
`predicted.*(failure|category|blind|spurious|misweighted)|failure.*prediction|expected.*failure`
yielded **zero matches** for predictive AI failure estimators.

### Categorization Table of Found Occurrences:
| File | Line | Symbol / Context | What It Actually Does | Real Model Behavior? | Keep in Thesis? |
| :--- | :---: | :--- | :--- | :---: | :---: |
| [blindspot/testing/behavioral.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/testing/behavioral.py) | 40–213 | `classify_behavior()` | Compares actual $y_{\text{orig}}$ vs $y_{\text{pert}}$ against probe contract (`expected_flip`) | **Yes (Empirical Observation)** | **YES** |
| [blindspot/explainability/taxonomy.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/explainability/taxonomy.py) | 31–110 | `TaxonomyClassifier.classify_failure()` | Delegates to `classify_behavior()` and enriches with XAI token weights | **Yes (Empirical Observation)** | **YES** |
| [blindspot/core/types.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/core/types.py) | 259–310 | `classify_behavioral_outcome()` | Enum mapping of $(y_{\text{orig}} \neq y_{\text{pert}}, \text{expected\_flip})$ | **Yes (Deterministic Mapping)** | **YES** |
| [blindspot/ui/components.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/ui/components.py) | 209 | `render_failure_record()` | Displays observed failure card with baseline vs probe predictions | **Yes (UI Display)** | **YES** |
| [blindspot/app.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/app.py) | 366 | `render_failure_lab()` | Explanatory text: "The observed prediction differed from expected..." | **Yes (Descriptive Label)** | **YES** |

### Verification of Scientific Chain:
BlindSpot strictly implements the **empirical evaluation architecture**:
```text
Original Sentence
       ↓
Original Model Output (Forward Pass)
       ↓
Controlled Probe
       ↓
Perturbed Model Output (Forward Pass)
       ↓
Actual Behavioral Difference (is_flipped = y_orig != y_pert)
       ↓
Confidence / Flip Analysis (Delta = pert_conf - orig_conf)
       ↓
Empirical Evidence (classify_behavior)
       ↓
Failure Taxonomy (BLIND, SPURIOUS, MISWEIGHTED, UNDETERMINED, NONE)
```
**Conclusion**: There is zero heuristic AI guessing or failure prediction in BlindSpot.

---

## 6. Model Audit

The active registry contains five default sentiment presets and one explicitly rejected non-sentiment model:

### Model Specifications Summary:
```text
Model ID: distilbert-base-uncased-finetuned-sst-2-english
Provider: HuggingFace (distilbert)
Architecture: DistilBertForSequenceClassification (66.96M params)
Task: SENTIMENT
Number of classes: 2
Actual labels: ["NEGATIVE", "POSITIVE"]
Actual output format: PredictionResult(label, confidence, probabilities, latency_ms)
Confidence source: Softmax posterior probability on top logit
Binary / multiclass: Binary
Sentiment classifier?: YES
Compatible with BlindSpot sentiment thesis?: YES
Currently actually loaded?: YES (HuggingFaceWrapper)
Currently actually executed?: YES (Verified in acceptance benchmark)

Model ID: textattack/albert-base-v2-SST-2
Provider: HuggingFace (textattack)
Architecture: AlbertForSequenceClassification (11.68M params)
Task: SENTIMENT
Number of classes: 2
Actual labels: ["NEGATIVE", "POSITIVE"]
Actual output format: PredictionResult(label, confidence, probabilities, latency_ms)
Confidence source: Softmax posterior probability on top logit
Binary / multiclass: Binary
Sentiment classifier?: YES
Compatible with BlindSpot sentiment thesis?: YES
Currently actually loaded?: YES
Currently actually executed?: YES (Verified in acceptance benchmark)

Model ID: cardiffnlp/twitter-roberta-base-sentiment-latest
Provider: HuggingFace (cardiffnlp)
Architecture: RobertaForSequenceClassification (124.65M params)
Task: SENTIMENT
Number of classes: 3
Actual labels: ["NEGATIVE", "NEUTRAL", "POSITIVE"]
Actual output format: PredictionResult(label, confidence, probabilities, latency_ms)
Confidence source: Softmax posterior probability on top logit
Binary / multiclass: Multiclass (3-class)
Sentiment classifier?: YES
Compatible with BlindSpot sentiment thesis?: YES
Currently actually loaded?: YES
Currently actually executed?: YES (Verified in acceptance benchmark)

Model ID: textattack/bert-base-uncased-SST-2
Provider: HuggingFace (textattack)
Architecture: BertForSequenceClassification (109.48M params)
Task: SENTIMENT
Number of classes: 2
Actual labels: ["NEGATIVE", "POSITIVE"]
Actual output format: PredictionResult(label, confidence, probabilities, latency_ms)
Confidence source: Softmax posterior probability on top logit
Binary / multiclass: Binary
Sentiment classifier?: YES
Compatible with BlindSpot sentiment thesis?: YES
Currently actually loaded?: YES
Currently actually executed?: YES (Verified in acceptance benchmark)

Model ID: cardiffnlp/twitter-roberta-base-sentiment
Provider: HuggingFace (cardiffnlp)
Architecture: RobertaForSequenceClassification (124.65M params)
Task: SENTIMENT
Number of classes: 3
Actual labels: ["NEGATIVE", "NEUTRAL", "POSITIVE"]
Actual output format: PredictionResult(label, confidence, probabilities, latency_ms)
Confidence source: Softmax posterior probability on top logit
Binary / multiclass: Multiclass (3-class)
Sentiment classifier?: YES
Compatible with BlindSpot sentiment thesis?: YES
Currently actually loaded?: YES
Currently actually executed?: YES (Verified in acceptance benchmark)

Model ID: roberta-base-openai-detector [REJECTED NON-SENTIMENT MODEL]
Provider: HuggingFace (openai)
Architecture: RobertaForSequenceClassification (124.65M params)
Task: AI_TEXT_DETECTION
Number of classes: 2
Actual labels: ["Fake", "Real"]
Actual output format: N/A (Excluded by validation gate)
Confidence source: N/A
Binary / multiclass: Binary
Sentiment classifier?: NO (AI generated text detector)
Compatible with BlindSpot sentiment thesis?: NO (INCOMPATIBLE)
Currently actually loaded?: NO (Validation gate blocks admission)
Currently actually executed?: NO (Default: False in registry)
```

---

## 7. Model Output Contract

Every model execution produces a standardized [PredictionResult](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/core/types.py#L314-L365) object.

### Binary Classification Canonical Output:
```text
Model: DistilBERT SST-2
Prediction: POSITIVE
Confidence: 98.73%

Probabilities:
NEGATIVE: 1.27%
POSITIVE: 98.73%
```

### Multiclass (3-Class) Canonical Output:
```text
Model: Twitter RoBERTa Latest (3-Class)
Prediction: POSITIVE
Confidence: 91.42%

Probabilities:
NEGATIVE: 2.10%
NEUTRAL: 6.48%
POSITIVE: 91.42%
```

### Verification Across Models:
- `label`: String normalized via `normalize_label_name()` (`NEGATIVE`, `POSITIVE`, `NEUTRAL`).
- `confidence`: Strict float $\in [0.0, 1.0]$.
- `probabilities`: Normalized dictionary summing to $1.0$.
- `latency_ms`: Measured via high-resolution `time.perf_counter()`.
- `is_prediction_flip`: Computed via `is_prediction_flip(y_0, y_p)`.

---

## 8. Complete Probe Lifecycle

The lifecycle of linguistic probes proceeds through the following stages:

```text
[1] Probe Generation
    • File: blindspot/perturbations/shared.py (SharedProbeGenerator)
    • Output: SharedProbeSet with deterministic LinguisticProbe objects
    • Probe ID: SHA-256 hash: seed | pert | type | effect (e.g. prb_c6ffb5b3e187)

[2] Probe Validation
    • File: blindspot/core/types.py (SharedProbeSet.validate)
    • Checks: Non-empty text, non-identical perturbation, valid expected effect, uniqueness

[3] Probe Selection / Staging
    • File: blindspot/ui/probe_lab.py (Probe Research Workbench)
    • Staged into: st.session_state["staged_probe_set"]
    • Controls: Select All, Select None, Category Select, Custom Probe Injection

[4] Experiment Configuration
    • File: blindspot/ui/experiment_lab.py
    • Output: ExperimentConfig carrying selected_probe_set or perturbation_types

[5] Run Plan Formation
    • File: blindspot/execution/runner.py (lines 201–216)
    • Output: Immutable RunPlan persisted to runs/<run_id>/run_plan.json
    • Invariant: Exactly len(run_plan.selected_probe_ids) probes scheduled

[6] Live Run Execution
    • File: blindspot/execution/runner.py (_execute)
    • Streaming: Emits probe_evaluated events to runs/<run_id>/events.jsonl

[7] Model Inference
    • File: blindspot/testing/behavioral.py (BehavioralTester.evaluate_shared_probes)
    • Invariant: Evaluates baseline first, then batch evaluates identical probes across models

[8] Behavioral Analysis & Failure Taxonomy
    • File: blindspot/testing/behavioral.py (classify_behavior)
    • Output: ModelProbeEvaluation & BehavioralProbeResult records

[9] Reports & Visualizations
    • Files: blindspot/reporting/report_generator.py & thesis_graphs.py
    • Output: Markdown reports, JSON metrics, 15 thesis figures, 4 diagnostic figures
```

---

## 9. Investigation of the 7 → 4 → 3 Probe Problem

The user specifically requested tracing the discrepancy:
$$\text{Probe Generator: 7 probes} \longrightarrow \text{Experiment UI: 4 options} \longrightarrow \text{Live Run: 3 executed probes}$$

### Exact Root Cause Analysis:
1. **Probe Generator produced 7 candidates**:
   - In `blindspot/perturbations/shared.py`: `_generate_calibrated_7_probes()` generated 7 slots (`P001` through `P007`).
2. **Experiment UI showed 4 category checkboxes**:
   - In `blindspot/ui/experiment_lab.py` (legacy v2.0): The UI only presented 4 category checkboxes:
     `Negation`, `Double Negation`, `Connectives`, and `Synonym Substitution`.
   - `Intensity` and `Structure` were omitted from the UI checkboxes.
3. **Runner silently dropped probes down to 3**:
   - When the user selected `Connectives`, `ConnectivePerturber` produced variants with internal subtype tags:
     `"contrast_negative_append"`, `"contrast_positive_append"`, and `"contrast_concession_prefix"`.
   - In `blindspot/perturbations/shared.py` (legacy `_is_category_match`):
     ```python
     if ptype == allowed_type: # exact string match!
     ```
     `"contrast_negative_append" == "connective"` evaluated to **`False`**!
   - Consequently, the connective probe was silently dropped during runner-internal filtering.
   - For proverbs, negation removal generated `"negation_removal"`, which failed exact matching against `"negation"`.
   - Only 3 probes survived string matching, causing the run to execute only 3 probes.

### Current Status in v2.3.0:
- **RESOLVED**:
  1. `_is_category_match` was rewritten to support category-family prefix and substring matching (lines 149–175 of `shared.py`).
  2. The Experiment Lab UI now exposes all 6 categories (`Negation`, `Double Negation`, `Connectives`, `Synonym Substitution`, `Intensity`, `Structure`).
  3. The `RunPlan` enforces strict equality:
     $$\text{Planned Probes} = \text{Executed Probes} = \text{Reported Probes}$$
     Verified by automated unit test `test_pipeline_count_integrity` (`tests/test_probe_integrity.py`).

---

## 10. Original Baseline Verification

A major defect in earlier versions was that the original unperturbed sentence was treated as just another probe or discarded if all probes failed.

### Current Baseline Architecture:
1. **Evaluated Exactly Once**:
   - In `blindspot/testing/behavioral.py` lines 339–350:
     ```python
     for seed in probe_set.seed_texts:
         pred = self.model.predict_result(seed)
         baselines[seed] = BaselineEvaluation(...)
     ```
2. **First-Class Persistence**:
   - Stored in `runs/<run_id>/models/<model_slug>/baseline.json` immediately upon model completion.
   - Stored in aggregate `results.json` under `model_baselines[model_id][seed_text]`.
3. **Immutability & Association**:
   - Every `BehavioralProbeResult` stores `original_label`, `original_confidence`, and `original_distribution` directly alongside probe outputs.
   - Cannot be contaminated by prior runs or another model because the baseline is recomputed per active model instance and keyed by `model_id`.

---

## 11. Behavioral Metrics Audit

The table below documents every behavioral metric implemented in [blindspot/testing/metrics.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/testing/metrics.py):

| Metric | Mathematical Formula | Definition | Source File & Line | Used in Reports? | Displayed in UI? |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **Observed Flip Rate** | $\frac{\sum \mathbb{I}(\hat{y}_0 \neq \hat{y}_p)}{N_{\text{total}}}$ | Fraction of all executed probes that flipped the predicted label. | `metrics.py:66` | Yes | Yes |
| **Expected Flip Rate** | $\frac{\sum_{p \in \text{ExpFlip}} \mathbb{I}(\hat{y}_0 \neq \hat{y}_p)}{|\text{ExpFlip}|}$ | Proportion of probes with `expected_flip=True` that successfully flipped. | `metrics.py:80` | Yes | Yes |
| **Preserve Rate** | $\frac{\sum_{p \in \text{ExpPreserve}} \mathbb{I}(\hat{y}_0 == \hat{y}_p)}{|\text{ExpPreserve}|}$ | Proportion of probes with `expected_flip=False` that preserved prediction. | `metrics.py:98` | Yes | Yes |
| **Behavioral Consistency** | $\frac{N_{\text{satisfied}}}{N_{\text{total}}}$ | Fraction of all probes whose observed behavior matched contract expectation. | `metrics.py:116` | Yes | Yes |
| **Confidence Flip Rate** | $\frac{\sum \mathbb{I}(\Delta c \le -\tau)}{N_{\text{total}}}$ | Proportion of probes where confidence dropped by $\ge \tau$ percentage points. | `metrics.py:130` | Yes | Yes |
| **Mean Confidence Shift** | $\frac{1}{N} \sum (c_p - c_0) \times 100$ | Average signed confidence change across all evaluations in percentage points. | `metrics.py:168` | Yes | Yes |
| **Expected Calibration Error (ECE)** | $\sum_{m=1}^M \frac{|B_m|}{N} |\text{acc}(B_m) - \text{conf}(B_m)|$ | Binned calibration error between predicted confidence and contract accuracy. | `metrics.py:9` | Yes | Yes |
| **Transition Matrix** | $T_{i,j} = \sum \mathbb{I}(\hat{y}_0 = i \land \hat{y}_p = j)$ | Count of transitions from original class $i$ to perturbed class $j$. | `metrics.py:150` | Yes | Yes |
| **Pairwise Model Agreement** | $\frac{1}{N} \sum \mathbb{I}(\hat{y}_{p}^{A} = \hat{y}_{p}^{B})$ | Percentage of identical probe predictions between two models. | `metrics.py:205` | Yes | Yes |

---

## 12. Failure Taxonomy Audit

The failure taxonomy is governed by `classify_behavior()` in `blindspot/testing/behavioral.py`:

```text
                                  is_expected_flip?
                                  /              \
                             YES /                \ NO
                                /                  \
                        is_flipped?              is_flipped?
                        /         \              /         \
                   YES /           \ NO     YES /           \ NO
                      /             \          /             \
                  COMPLIANT        BLIND    SPURIOUS     COMPLIANT
                   (None)          FAILURE  FAILURE        (None)
                                                           /    \
                                            |Δc| > 15pp?  /      \ Normal
                                                         /        \
                                                   MISWEIGHTED    COMPLIANT
```

### Detailed Decision Specifications:

#### 1. BLIND FAILURE
- **Required Evidence**: Probe introduces polarity-altering change (`is_expected_flip = True`), but model prediction does not flip (`is_flipped = False`).
- **Actual Evidence Collected**: $y_{\text{orig}}$, $y_{\text{pert}}$, $c_{\text{orig}}$, $c_{\text{pert}}$, transition string, probe contract.
- **Decision Rule**: `if is_expected_flip and not is_flipped: return FailureCategory.BLIND`
- **Source Code**: `blindspot/testing/behavioral.py:169-175`.
- **Can real model trigger it?**: **YES**. Observed empirically in `twitter-roberta-base-sentiment-latest` on negation removal from `"All that glitters is not gold."` (retained `NEUTRAL`).

#### 2. SPURIOUS FAILURE
- **Required Evidence**: Probe is meaning-preserving (`is_expected_flip = False`), but model unexpectedly flips class label (`is_flipped = True`).
- **Actual Evidence Collected**: $y_{\text{orig}}$, $y_{\text{pert}}$, transition string, semantic intent.
- **Decision Rule**: `if not is_expected_flip and is_flipped and intent not in ("STRENGTHEN_POLARITY", "WEAKEN_POLARITY"): return FailureCategory.SPURIOUS`
- **Source Code**: `blindspot/testing/behavioral.py:198-210`.
- **Can real model trigger it?**: **YES**. Observed empirically in `albert-base-v2-SST-2` and `bert-base-uncased-SST-2` on double negation (flipped from `NEGATIVE` to `POSITIVE`).

#### 3. MISWEIGHTED FAILURE
- **Required Evidence**: Degree modification probe (intensifier or downtoner) produces an inverted label flip or an irrational confidence shift ($>15\text{ pp}$ drop on intensifier or $>15\text{ pp}$ surge on downtoner).
- **Actual Evidence Collected**: Signed $\Delta c_{\text{pts}}$, semantic intent, degree modifier token.
- **Decision Rule**: `if intent == "STRENGTHEN_POLARITY" and delta_pp < -15.0: return FailureCategory.MISWEIGHTED`
- **Source Code**: `blindspot/testing/behavioral.py:178-193`.
- **Can real model trigger it?**: **YES**. Triggerable by intense degree adverbs reducing prediction confidence.

#### 4. UNDETERMINED
- **Required Evidence**: Missing labels, null confidence, or ambiguous probe contracts without expected relation.
- **Decision Rule**: Missing input validation or unresolved contract.
- **Source Code**: `blindspot/testing/behavioral.py:64-93`.

### Why Previous Real Experiments Produced 0 Failures:
The earlier investigation identified two root causes:
1. **Defect 1**: Exact string mismatch in `infer_expected_semantic_effect` marked 100% of probes with `expected_flip = False`. When models failed to flip under negation, the system saw `expected_flip == False` and `is_flipped == False` $\to$ declared it an `EXPECTED_PRESERVE` with 0 failures!
2. **Defect 2**: Failure classification was gated behind `if self.config.explainer_type != "none":`. If explainability was disabled for fast execution, failure classification was completely bypassed.

---

## 13. Explainability Audit

### Implementations:
1. **LIME ([lime_explainer.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/explainability/lime_explainer.py))**:
   - Uses `lime.lime_text.LimeTextExplainer` with fixed random seeds for reproducibility.
   - Bounded sampling (`num_samples=50`, `num_features=10`) prevents evaluation hangs.
2. **SHAP ([shap_explainer.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/explainability/shap_explainer.py))**:
   - Uses `shap.Explainer` with `shap.maskers.Text()`.
   - Bounded evaluation count (`max_evals=50`) prevents exponential Shapley computation.
3. **Leave-One-Out Fallback (`_leave_one_out_explain`)**:
   - Word-omission importance scoring activates gracefully if LIME or SHAP packages are missing or fail.
4. **Token Attribution Provenance**:
   - Every explanation stores: `explainer_requested`, `explainer_used`, `fallback_used`, `fallback_reason`, `runtime_ms`, `random_seed`.

---

## 14. Graph & Visualization Audit

The system generates two complete tiers of visual artifacts:

### Tier 1: Publication Thesis Figures (15 Figures + Telemetry JSON)
Generated by `ThesisVisualizer` ([thesis_graphs.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/reporting/thesis_graphs.py)) into `runs/<run_id>/figures/`:
1. `fig01_prediction_distribution.png`: Model prediction distribution across classes.
2. `fig02_flip_rates.png`: Observed vs expected flip rate comparison.
3. `fig03_expected_vs_observed.png`: Semantic behavioral compliance rate.
4. `fig04_taxonomy_distribution.png`: 4-way behavioral failure taxonomy distribution.
5. `fig05_confidence_delta_by_probe.png`: Signed confidence shift by linguistic probe category.
6. `fig06_confidence_delta_distribution.png`: Confidence delta distribution density.
7. `fig07_probe_level_comparison.png`: Probe-level response across models.
8. `fig08_model_probe_heatmap.png`: Model $\times$ Probe flip matrix heatmap.
9. `fig09_transition_matrix.png`: Label transition dynamics under perturbation.
10. `fig10_probe_consistency.png`: Probe behavioral consistency by category.
11. `fig11_model_agreement.png`: Cross-model pairwise agreement matrix.
12. `fig12_change_vs_preserve.png`: Invariance vs sensitivity profile.
13. `fig13_per_model_scorecard.png`: Comprehensive robustness scorecard.
14. `fig14_runtime_profile.png`: Execution latency and profiling breakdown.
15. `fig15_probe_category_comparison.png`: Probe category robustness comparison.
16. `source_data.json`: Machine-readable raw coordinates and telemetry for publication re-plotting.

### Tier 2: Classic Diagnostic Charts (4 Figures)
Generated by `Visualizer` ([visualizer.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/reporting/visualizer.py)):
1. `taxonomy_distribution.png`: Failure taxonomy breakdown donut chart.
2. `behavioral_metrics.png`: Behavioral consistency vs flip rates across models.
3. `attribution_comparison.png`: Token attribution divergence (LIME vs SHAP).
4. `probe_alignment_summary.png`: Perturbation category sensitivity and explanation alignment.

### UI Integration:
- **`reports_view.py`**: 4-tab hub offering single-figure interactive inspection, multi-column gallery, 300 DPI downloads, and raw JSON exploration.
- **`comparison.py`**: Comparative charts tab rendering heatmaps, agreement matrices, and flip rates.
- **`explanation_lab.py`**: Inline attribution divergence graphs and probe alignment summaries.

---

## 15. Multimodel Architecture Audit

| Component | Status | Implementation Detail |
| :--- | :---: | :--- |
| **Model Registry** | Fully Functional | 5 presets indexed, custom registration, schema validation. |
| **Dual Model Cache** | Fully Functional | Disk cache isolated from RAM; sequential RAM eviction frees memory. |
| **Shared Probe Protocol** | Fully Functional | Generates identical stimuli across models with deterministic SHA-256 IDs. |
| **Cross-Model Analysis** | Fully Functional | Computes Model $\times$ Probe matrices and pairwise concordance. |
| **Resource Manager** | Fully Functional | Live CPU/RAM telemetry, device allocation (CPU/CUDA). |
| **Async Runner** | Fully Functional | Background daemon thread, non-blocking UI, event emission. |
| **RunStore** | Fully Functional | Granular per-model persistence, atomic metadata updates. |
| **Workstation UI** | Fully Functional | Streamlit shell with top navigation, live meters, and report tabs. |

---

## 16. Cache Audit

1. **Capacity & Policy**:
   - `ModelCache` uses an `OrderedDict` LRU cache with default `max_size = 1` resident model in RAM.
   - When 5 models are evaluated sequentially, model $M_k$ is loaded into RAM, evaluated, and immediately evicted via `evict_from_memory(model_id)` to keep RAM usage strictly bounded.
2. **Disk Cache**:
   - Persistent HuggingFace hub cache stores model weights (6.33 GB total for all 5 models).
   - Disk weights are never deleted by RAM eviction.
3. **Model Identity Keying**:
   - Cache keys are strictly formatted as `f"{model_id}:{device}"`.
   - Results are keyed by `model_id`, preventing cross-model contamination.
4. **Blinking / UI Flashing**:
   - The 1.0s aggressive page refresh was replaced by a calm 3.5s refresh cycle in `live_run.py`.
   - Model cards strictly query `runner.run_plan.model_ids`, eliminating stale model leakage.

---

## 17. Experiment State Audit

| State / Operation | Backend Supported? | UI Supported? | Implementation Notes |
| :--- | :---: | :---: | :--- |
| **Completed Run** | YES | YES | Fully viewable in Reports, History, Comparison. |
| **Running Job** | YES | YES | Live meters, ETA, event console in `live_run.py`. |
| **Failed Run** | YES | YES | Logged to `error.json`, status marked `FAILED`. |
| **Cancelled Run** | YES | YES | Cancel button sets `_cancel_flag`, terminates gracefully. |
| **Paused Run** | NO | NO | Not implemented; cancellation is supported. |
| **Resumable Run** | **YES** | **PARTIAL** | Backend `ExperimentRunner.resume_run()` works; no UI resume button. |
| **Load Historical Run**| YES | YES | One-click loader in History, Comparison, Explanation Lab. |
| **Delete Run** | YES | NO | `RunStore.delete_run(confirmation=True)` exists; no UI delete button. |
| **Archive Run** | YES | NO | `RunStore.archive_run()` exists; no UI archive button. |

---

## 18. Run Storage Audit

### Directory Inventory:
- **`runs/` (Canonical)**:
  - 24 persisted experiment directories.
  - Active benchmark run `runs/exp_1789931356_a67ae6/` contains:
    * `models/`: Per-model artifacts (`baseline.json`, `predictions.json`, `metrics.json`, `taxonomy.json`, `timing.json`, `report.md`).
    * `aggregate/`: `comparison.json`, `metrics.json`, `taxonomy.json`.
    * `figures/`: 20 image files + `source_data.json`.
    * `reports/`: `summary.md`, `failure_summary.md`, `probe_level_evidence.md`.
    * `results.json`, `run_plan.json`, `probe_set.json`, `events.jsonl`.
- **`audit_reports/` (Legacy)**:
  - Contains obsolete artifacts from earlier single-model prototype runs (`explanation_comparison.md`, `failure_summary.md`, `model_behavior_report.md`).
  - Should be archived or kept read-only as legacy provenance.

---

## 19. Performance Audit

### Historical vs Current Performance:
- **Prior Bottleneck**: A 5-model evaluation took $\sim 1\text{ hour}$ because:
  1. Models were loaded from disk and re-initialized repeatedly.
  2. Inference was unbatched ($N$ separate forward passes).
  3. LIME and SHAP explainability ran unconstrained sample sizes ($>500$ samples) across all probes sequentially.
  4. Disk I/O was unbuffered with excessive debug printing.
- **Current Architecture**:
  - Batched pipeline inference (`batch_size=16` or `32`).
  - Bounded XAI evaluation (`num_samples=50` for LIME, `max_evals=50` for SHAP).
  - RAM LRU cache with sequential eviction.
  - Result: **94.98 seconds (1.58 minutes)** for 5 models $\times$ 5 stimuli with full LIME + SHAP.

---

## 20. UI Architecture Audit

### Structure:
- **Application Header**: Real-time hardware telemetry (CPU cores, RAM headroom, device, active run counter).
- **Primary Top Navigation**: Horizontal buttons:
  `Overview` | `Experiment` | `Probes` | `Run` | `Analyze` | `Reports` | `System`
- **Secondary Domain Subtabs**:
  - `Run` $\to$ `Live Run`, `Run Details`, `Events`
  - `Analyze` $\to$ `Comparison`, `Explainability`, `Failure Analysis`
  - `Reports` $\to$ `Reports`, `Run History`, `Models`
  - `System` $\to$ `Monitor`, `Console`, `Settings`
- **Contextual Sidebar**: Minimalist session context displaying active Experiment ID and status.

### UI Observations & Defects:
1. `blindspot/ui/live_run.py` (lines 134–153): Renders the `TARGET MODEL EVALUATION STATUS` header twice consecutively.
2. Sidebar footer displays `v2.2.0 • Canonical Protocol` while other components report `v2.3.0`.

---

## 21. Documentation Audit

### Categorization of Project Markdown Files:

| Category | File | Recommendation |
| :--- | :--- | :---: |
| **KEEP** | `README.md` | Primary entrypoint and quickstart guide. |
| **KEEP** | `ARCHITECTURE.md` | Core technical architectural document. |
| **KEEP** | `docs/BEHAVIORAL_METRICS.md` | Canonical mathematical definitions of metrics. |
| **KEEP** | `docs/FAILURE_TAXONOMY.md` | Traceable 4-way failure taxonomy definitions. |
| **KEEP** | `docs/DIAGNOSTIC_GRAPHS_GUIDE.md`| Complete documentation for all 19 figures. |
| **KEEP** | `docs/CODEBASE_FILE_GUIDE.md` | Complete repository map and symbol index. |
| **MERGE** | `docs/FLIP_ANALYSIS.md` | Merge into `docs/BEHAVIORAL_METRICS.md`. |
| **MERGE** | `docs/PROBE_PROTOCOL.md` & `PROBE_SELECTION.md` | Merge into `docs/PROBE_CALIBRATION.md`. |
| **ARCHIVE**| `CURRENT_STATE_AUDIT_REPORT.md` | Move to `docs/archive/` (historical record). |
| **ARCHIVE**| `MODEL_VALIDATION_REPORT.md` | Move to `docs/archive/` (historical record). |
| **ARCHIVE**| `PROBE_PIPELINE_AUDIT.md` | Move to `docs/archive/` (historical record). |
| **ARCHIVE**| `RESEARCH_INTEGRITY_AUDIT.md` | Move to `docs/archive/` (historical record). |
| **ARCHIVE**| `CHANGELOG.md` | Retain as historical release record. |
| **REMOVE** | `audit_reports/*.md` | Legacy markdown files superseded by `runs/`. |

---

## 22. Test Suite Audit

### Test Execution Results:
- **Fast Unit Test Runner**: `python run_tests.py`
  - **Total Tests**: **98 tests**
  - **Passed**: **98**
  - **Failed**: **0**
  - **Duration**: **53.13 seconds**
- **Acceptance Benchmark**: `python run_acceptance_benchmark.py`
  - 5 real HuggingFace transformer models executed.
  - Exactly 25 evaluations (5 baselines + $5 \times 4$ probes).
  - All 20 visualization artifacts generated.
  - Incremental persistence confirmed.
  - Total Duration: **94.98 seconds**.

### Test Quality Breakdown:
1. **Synthetic Isolation Tests**:
   - `test_behavioral_taxonomy.py`: 14 tests verifying Case 1 (Expected Flip), Case 2 (Blind), Case 3 (Preserve), Case 4 (Spurious), Cases 5–6 (Multiclass), Case 7 (Misweighted), Case 8 (Undetermined), and model-independence.
2. **Deterministic Pipeline Integrity Tests**:
   - `test_probe_integrity.py`: Asserts count equality across generation, selection, planning, execution, analysis, and reporting.
3. **End-to-End Real Model Tests**:
   - `test_research_repair.py` & `run_acceptance_benchmark.py`: Evaluates real transformer weights and checks genuine empirical failure classifications.

---

## 23. Dead / Duplicate / Unnecessary Code

1. **Dead Class `ModelPrediction` ([types.py:218](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/core/types.py#L218))**:
   - Dataclass defined in `types.py` but never instantiated or imported anywhere in the project. `PredictionResult` is the canonical class used throughout.
2. **Duplicate Similarity Functions ([alignment.py](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/explainability/alignment.py))**:
   - `compute_jaccard_similarity` and `compute_attribution_cosine` exist in `alignment.py` but are re-implemented in `token_attributions.py`.
3. **Duplicate UI Header Render ([live_run.py:134-153](file:///c:/Dev/Projects/BlinkSpot-main/blindspot/ui/live_run.py#L134-L153))**:
   - `TARGET MODEL EVALUATION STATUS` is rendered twice consecutively.
4. **Legacy Prototype Directory `audit_reports/`**:
   - Superseded by `runs/`.

---

## 24. Original vs Current Architecture Matrix

| Feature | Original BlindSpot (v1.0) | Current Multimodel BlindSpot (v2.3.0) | Current Status |
| :--- | :--- | :--- | :---: |
| **Model Scope** | Single model (DistilBERT) | 5 validated multi-architecture sentiment models | **Complete** |
| **Inference Mode**| Unbatched, sequential | Batched pipeline inference (`batch_size=16/32`) | **Complete** |
| **Baseline Anchor**| Subsumed into probe records | First-class `BaselineEvaluation` evaluated once | **Complete** |
| **Probe Staging** | Ephemeral, non-selectable | Interactive Probe Workbench, stage/curate | **Complete** |
| **Probe Matching**| Exact string equality (broken) | Prefix & family matching (`_is_category_match`)| **Complete** |
| **Flip Calculation**| Conflated flips & preserves | Stratified: Observed Flip, Expected Flip, Preserve | **Complete** |
| **Failure Taxonomy**| Gated inside explainer loop | Decoupled pure classifier (`classify_behavior`) | **Complete** |
| **Explainability** | Unconstrained LIME/SHAP | Bounded LIME & SHAP with LOO fallback | **Complete** |
| **Visualizations** | 4 classic matplotlib charts | 15 thesis figures + 4 classic figures + JSON | **Complete** |
| **Persistence** | Unbuffered root markdown | Granular incremental per-model disk persistence | **Complete** |
| **Interrupted Run**| Run lost if interrupted | Resumable without re-running forward passes | **Complete (Backend)** |
| **UI Shell** | Single page / sidebar | Top bar navigation with domain subtabs | **Complete** |

---

## 25. Critical Defects & Implementation Priorities

### P0 — Scientific Correctness
*Issues affecting research validity or mathematical correctness:*

1. **Unfiltered Calibrated Generator in Runner**:
   - **Problem**: When `selected_probe_set` is None and `candidate_count == 7` (default), `SharedProbeGenerator.generate_probes()` invokes `_generate_calibrated_7_probes()` which generates all 7 probes without filtering by `perturbation_types`.
   - **Evidence**: `blindspot/perturbations/shared.py` lines 214–218.
   - **Impact**: If a user deselects "Intensity" and launches an audit without staged probes, all 7 probes are generated anyway.
   - **Required Fix**: In `_generate_calibrated_7_probes()`, filter candidates by `perturbation_types` if provided, or pass `candidate_count=None` when specific categories are selected.
   - **Risk if Unchanged**: User category unchecking in Step 03 is ignored unless using Probe Workbench.

---

### P1 — Pipeline Integrity
*Issues causing features or capabilities to be unreachable:*

1. **Resume Run Not Exposed in UI**:
   - **Problem**: `ExperimentRunner.resume_run(experiment_id)` is fully implemented in the backend, but `run_history.py` only offers "Load This Run" (for inspection). There is no "Resume Experiment" button for interrupted or failed runs.
   - **Evidence**: `blindspot/ui/run_history.py` lines 100–110.
   - **Impact**: If a 5-model run is cancelled after 3 models, the user cannot click "Resume" from the UI.
   - **Required Fix**: Add a "Resume Interrupted Run" button in `run_history.py` that launches `ExperimentRunner.resume_run(exp_id).run_async()`.
   - **Risk if Unchanged**: Users must re-run from scratch if an audit is stopped.

---

### P2 — Performance & Optimization
*Issues affecting execution speed or redundant rendering:*

1. **Duplicate Header in Live Run UI**:
   - **Problem**: `TARGET MODEL EVALUATION STATUS` header HTML block is duplicated.
   - **Evidence**: `blindspot/ui/live_run.py` lines 134–141 and 146–153.
   - **Impact**: Harmless visual duplication in the Live Run monitor.
   - **Required Fix**: Delete the redundant markdown block.

---

### P3 — UX & Navigation
*UI consistency and layout improvements:*

1. **Version Number Inconsistency in UI**:
   - **Problem**: Sidebar states `v2.2.0 • Canonical Protocol` while core types and reports indicate `v2.3.0`.
   - **Evidence**: `blindspot/ui/shell.py` line 130.
   - **Impact**: Minor version display mismatch.
   - **Required Fix**: Update string to `v2.3.0`.

---

### P4 — Cleanup & Technical Debt
*Dead code, obsolete files, and documentation consolidation:*

1. **Dead Class `ModelPrediction`**:
   - **Evidence**: `blindspot/core/types.py` lines 218–245.
   - **Impact**: Confusing dead code. `PredictionResult` is canonical.
   - **Required Fix**: Remove or deprecate `ModelPrediction`.
2. **Consolidate Root Markdown Files**:
   - Move `CURRENT_STATE_AUDIT_REPORT.md`, `PROBE_PIPELINE_AUDIT.md`, `RESEARCH_INTEGRITY_AUDIT.md`, and `MODEL_VALIDATION_REPORT.md` to `docs/archive/`.
3. **Archive Legacy `audit_reports/` Prototype Artifacts**:
   - Move legacy prototype files in `audit_reports/` into `runs/archived/` or mark read-only.
