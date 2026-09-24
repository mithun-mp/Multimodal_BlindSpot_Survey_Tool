# BlindSpot — Research Integrity Audit & Diagnostic Analysis
**Document Version**: 2.3.0  
**Audit Date**: 2026-09-20  
**Repository**: `c:\Dev\Projects\BlinkSpot-main`  
**Focus**: Behavioral Failure Taxonomy, Calibrated Probe Suite, Flip Analysis, and End-to-End Pipeline Integrity  

---

## Executive Summary

This comprehensive research-integrity audit investigates why the BlindSpot workstation frequently reports **ZERO behavioral failures** across evaluated models and probes. 

The investigation confirms that models are **not** producing zero failures because they are flawlessly robust. Rather, critical structural defects across probe effect inference, expectation tagging, taxonomy classifier gating, and classification rules have systematically prevented genuine behavioral failures from being recorded.

The most catastrophic root cause: **100% of generated negation, contrast, and inversion probes were being assigned `expected_flip = False` and `expected_semantic_effect = "preserve"` due to a string token mismatch in expectation inference.** When target models ignored negation operators (a classic *Blind* failure), the system recorded `is_flipped = False`, saw that `expected_flip == False`, declared the behavior an `EXPECTED_PRESERVE`, and recorded **zero failures**.

---

## 1. Current Architecture Trace

The behavioral auditing pipeline consists of the following components:

```
INPUT SENTENCE (e.g. "The movie was great...", "All that glitters is not gold.")
    ↓
PROBE GENERATION (SharedProbeGenerator via PerturbationEngine: Negation, Connective, Substitution, Intensity, Structure)
    ↓
PROBE CATALOG & EXPECTATION INFERENCE (infer_semantic_intent, infer_expected_semantic_effect)
    ↓
PROBE SELECTION & STAGING (Probe Research Workbench: session_state["staged_probe_set"])
    ↓
EXPERIMENT CONFIGURATION (ExperimentConfig consuming staged_probe_set or dynamic categories)
    ↓
RUN PLAN (Exact Run Plan: Baselines [M × S] + Probe Inferences [M × N] = Total Predictions)
    ↓
LIVE RUN (ExperimentRunner executing background async worker)
    ↓
MODEL INFERENCE & CACHE (HuggingFaceClassificationModel via ModelCache: batch evaluation)
    ↓
ORIGINAL BASELINE EVALUATION (Evaluated once per model, stored in results["model_baselines"])
    ↓
PROBE PREDICTIONS (Evaluated across all models with identical probe IDs and texts)
    ↓
BEHAVIORAL COMPARISON & FLIP DETECTION (is_prediction_flip, compute_confidence_shifts)
    ↓
FAILURE TAXONOMY (TaxonomyClassifier.classify_failure gated behind explainer_type != "none")
    ↓
AGGREGATION & REPORTING (CrossModelAnalyzer, RunStore, Markdown Report Generator, UI Shell)
```

---

## 2. Behavioral-Analysis Path Analysis

### 2.1 Baseline vs Probe Relationship
The baseline evaluation is executed prior to perturbation evaluations. However:
- The baseline prediction was not consistently encapsulated alongside the probe prediction in a unified `BehavioralProbeResult` object.
- Metrics were computed downstream by diffing arrays rather than evaluating atomic `(baseline, probe)` contract tuples.

### 2.2 Flip Detection
- Canonical flip detection ($y_0 \neq y_p$) was implemented in `types.py` as `is_prediction_flip(orig_label, pert_label)`, which is multiclass-safe.
- However, the behavioral outcome classification depended on `expected_flip`. Because `expected_flip` was universally `False`, flip detection never marked a missing flip as a failure.

---

## 3. Current Failure Taxonomy Implementation

The failure taxonomy is implemented in `blindspot/explainability/taxonomy.py` (`TaxonomyClassifier`):
1. **Blind**: Supposed to catch models failing to flip under negation.
2. **Spurious**: Supposed to catch models flipping on meaning-preserving perturbations or fixating on domain nouns.
3. **Misweighted**: Supposed to catch directionally inappropriate or unstable shifts.
4. **Undetermined**: Fallback when evidence is inconclusive.

---

## 4. Why Zero Failures Were Occurring: Root Cause Analysis

### Defect 1 (CRITICAL): Complete Expectation Inversion via Exact String Mismatch
- **Location**: `blindspot/perturbations/shared.py` (`infer_expected_semantic_effect`, `infer_semantic_intent`).
- **Mechanism**:
  - `NegationPerturber` produces items with `"type": "negation_insertion"` and `"type": "negation_removal"`.
  - `ConnectivePerturber` produces items with `"type": "contrast_positive_append"`, `"type": "contrast_negative_append"`, and `"type": "contrast_concession_prefix"`.
  - `infer_expected_semantic_effect` evaluated:
    ```python
    if ptype == "negation":
        return "invert", True
    elif ptype == "connective":
        ...
    return "preserve", False
    ```
  - `"negation_insertion" == "negation"` evaluated to `False`!
  - `"contrast_negative_append" == "connective"` evaluated to `False`!
  - **Every single negation and contrast probe fell through to the default `return "preserve", False`!**
- **Impact**: All probes across the entire system were tagged with `expected_flip = False` and `expected_semantic_effect = "preserve"`.
  - When a model was **blind** to negation (e.g. keeping `POSITIVE` on `"The movie was not great"`), `is_flipped` was `False`.
  - The system evaluated `is_flipped == expected_flip` $\to$ `False == False` (Match!).
  - The system declared the model's blindness to be an **`EXPECTED_PRESERVE`** with **zero failures**!

### Defect 2 (CRITICAL): Failure Taxonomy Completely Gated Behind Explainability
- **Location**: `blindspot/execution/runner.py` (lines 219–280).
- **Mechanism**:
  ```python
  failures = []
  if self.config.explainer_type != "none":
      # Only runs if explainer is active, and only up to explanation_sample_size!
      for ev in probes_to_explain:
          diag = self.taxonomy.classify_failure(...)
  ```
- **Impact**: If an experiment is run with `explainer_type = "none"` (standard for fast audits), failure classification is bypassed entirely. The model failures list remains permanently empty `[]`.

### Defect 3 (HIGH): Spurious Failure Classification Unreachable for Non-Movie Domains
- **Location**: `blindspot/explainability/taxonomy.py` (lines 166–184).
- **Mechanism**:
  - Spurious failures were only evaluated when `is_flipped == expected_flip`, and required:
    `all(w in {"movie", "book", "film", "it", "one", "thing", "actor", "scene"} for w in top_words)`.
  - If the input sentence is `"All that glitters is not gold."` or `"The restaurant service was terrible."`, the condition is mathematically impossible to satisfy.
  - Furthermore, when a meaning-preserving probe (`expected_flip = False`) caused an unexpected label flip (`is_flipped = True`), `taxonomy.py` routed it to `MISWEIGHTED` or `UNDETERMINED`, never `SPURIOUS`.

### Defect 4 (HIGH): Coupling Behavioral Failure to XAI Token Weights
- **Location**: `blindspot/explainability/taxonomy.py` (lines 56–100).
- **Mechanism**:
  - Negation blindness was only classified as `BLIND` if `neg_weight < 0.25` based on LIME/SHAP attributions.
  - If XAI attribution failed, was skipped, or allocated general weight to the negation token, `BLIND` was not returned; it fell into `MISWEIGHTED` or `UNDETERMINED`.
  - Behavioral outcomes (observable flips vs preservations) must be deterministic and decoupled from feature attribution computation. XAI must provide *supporting evidence*, not gate the behavioral diagnosis itself.

### Defect 5 (MEDIUM): Proverb & Figurative Semantic Handling
- **Location**: `blindspot/perturbations/` & `blindspot/ui/probe_lab.py`.
- **Mechanism**:
  - In proverbs like `"All that glitters is not gold."`, surface removal of negation (`"All that glitters is gold."`) reverses the proverbial meaning.
  - Without pragmatic sentence type awareness (`SentenceType.PROVERB`), heuristic perturbers treated the sentence as literal syntax.

---

## 5. Summary of Concrete Defects & Severities

| Defect ID | Description | Severity | Component |
| :--- | :--- | :--- | :--- |
| **DEF-01** | Exact equality mismatch in `infer_expected_semantic_effect` causing 100% of probes to be marked `expected_flip = False`. | **CRITICAL** | `perturbations/shared.py` |
| **DEF-02** | Failure classification gated inside `explainer_type != 'none'` and capped by `explanation_sample_size`. | **CRITICAL** | `execution/runner.py` |
| **DEF-03** | `SPURIOUS` classification requiring hardcoded movie terms and unreachable on unexpected flips. | **HIGH** | `explainability/taxonomy.py` |
| **DEF-04** | Behavioral outcome coupled to LIME/SHAP feature attribution rather than observable model behavior. | **HIGH** | `explainability/taxonomy.py` |
| **DEF-05** | Lack of canonical `BehavioralProbeResult` unified record storing baseline, probe, transition, and outcomes. | **MEDIUM** | `core/types.py` |
| **DEF-06** | Lack of isolated, pure deterministic `classify_behavior(...)` engine testable without UI/Streamlit. | **MEDIUM** | `testing/behavioral.py` |

---

## 6. Proposed Corrections & Architecture Restoration

1. **Canonical Probe & Outcome Hierarchy**:
   - Strictly separate **Primary Behavioral Outcome** (`EXPECTED_FLIP`, `MISSING_FLIP`, `UNEXPECTED_FLIP`, `EXPECTED_PRESERVE`, `UNEXPECTED_CHANGE`, `UNDETERMINED`) from **Secondary Failure Taxonomy** (`NONE`, `BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`).
2. **Robust Expectation Engine**:
   - Support prefix/category matching (`negation`, `negation_insertion`, `negation_removal`, `contrast_negative_append`, `intensity`, etc.).
   - Explicitly annotate each probe with `expected_label_relation` (`DIFFERENT_LABEL` vs `SAME_LABEL`) and `expected_confidence_relation`.
3. **Decoupled Deterministic Classifier (`classify_behavior`)**:
   - Pure function taking: `(original_pred, probe_pred, probe_contract, confidence_threshold_pp, attributions)`.
   - Evaluates every executed probe regardless of `explainer_type`.
   - Never depends on model names, UI state, or hardcoded entity dictionaries.
4. **Calibrated Diagnostic Probe Suite**:
   - Balanced generation of both expected-change probes and expected-preserve probes.
   - Explicit support for literal sentences and figurative/proverbs (`SentenceType.PROVERB`).
5. **Reconciliation & Integrity Verification**:
   - Guarantee: $\text{Generated} \to \text{Selected} \to \text{Planned} \to \text{Executed} \to \text{Analyzed} \to \text{Reported}$.

---

## 7. Required Tests to Prove Correction

1. **Synthetic Taxonomy Calibration Tests (`tests/test_behavioral_taxonomy.py`)**:
   - Case 1: Expected Flip $\to$ `EXPECTED_FLIP`, failure `NONE`.
   - Case 2: Synthetic Blind Case $\to$ `MISSING_FLIP`, failure `BLIND`.
   - Case 3: Expected Preserve $\to$ `EXPECTED_PRESERVE`, failure `NONE`.
   - Case 4: Synthetic Spurious Case $\to$ `UNEXPECTED_CHANGE`, failure `SPURIOUS`.
   - Case 5: Multiclass Flip (`POSITIVE` $\to$ `NEUTRAL`) $\to$ `is_prediction_flip = True`.
   - Case 6: Multiclass No Flip (`POSITIVE` $\to$ `POSITIVE`) $\to$ `is_prediction_flip = False`.
   - Case 7: Synthetic Misweighted Case (directional conflict / intensity inversion) $\to$ `MISWEIGHTED`.
   - Case 8: Insufficient Evidence / Ambiguous $\to$ `UNDETERMINED`.
2. **Probe Suite Calibration Tests (`tests/test_probe_calibration.py`)**:
   - Verify that probe generation produces a verified balance of `expected_flip = True` and `expected_flip = False`.
   - Verify proverb handling on `"All that glitters is not gold."`.
3. **Pipeline Reconciliation Tests (`tests/test_probe_integrity.py`)**:
   - Reconcile $\text{Generated} = \text{Selected} = \text{Planned} = \text{Executed} = \text{Analyzed} = \text{Reported}$.
