# CURRENT_LOGICAL_STATE_AUDIT.md
**Comprehensive Read-Only Logical & Architectural State Audit of the BlindSpot Platform**  
**Date**: September 27, 2026  
**Auditor**: Antigravity AI (Pair Programming with Lead Researcher)  
**Status**: READ-ONLY AUDIT COMPLETE — ZERO SOURCE CODE MODIFIED  

---

## 1. Executive Summary

This audit establishes the empirical, architectural, and logical state of the **BlindSpot** text classification robustness auditing platform prior to any modifications.

The core thesis objective is:
> *Given an original sentence and controlled linguistic probes, measure how sentiment classifiers behave under those changes, measure expected vs observed behavioral changes, measure polarity flips, measure confidence changes, measure behavioral consistency, and diagnose failures such as Blind, Spurious, Misweighted, or Undetermined when sufficient empirical evidence exists.*

The platform currently operates as a modular Python/Streamlit system with an asynchronous worker engine, a shared probe protocol, and multi-model evaluation routines. While earlier refactorings established a 5-model sentiment registry and rule-based failure taxonomy, this audit reveals critical logical defects in:
1. **Conflation of Label Inequality with Sentiment Polarity Flips**: `is_prediction_flip` treats any string inequality (`orig_label != pert_label`) as a flip, conflating binary reversals (`POSITIVE ↔ NEGATIVE`) with partial shifts (`POSITIVE → NEUTRAL`).
2. **Universal Boolean Flip Expectation vs Model-Specific Semantics**: The expectation engine forces a single boolean `expected_flip` (`SAME_LABEL` vs `DIFFERENT_LABEL`), failing to resolve how a linguistic transformation (`REVERSE_POLARITY`, `DOWNTONE`) maps differently onto 2-class vs 3-class models.
3. **Absence of Canonical Semantic Label Space**: Raw model outputs and normalized sentiment categories are merged. Binary models and 3-class models cannot be compared under a principled model-independent polarity representation.
4. **Baseline Disconnection & Attribution Provenance**: The original seed sentence is evaluated as a baseline, but lacks a persistent `baseline_id` linking immutably to all downstream probe evaluations. The system also risks conflating model-predicted baseline with objective ground truth.
5. **Metric Conflation**: Observed flip rate, expected flip compliance, preservation rate, and consistency are computed using inconsistent denominators and conflate raw label changes with genuine polarity reversals.
6. **Hardcoded Class-Index Assumptions**: Several normalization functions assume `LABEL_0 = NEGATIVE` and `LABEL_1 = POSITIVE` without strictly verifying against the model's actual configuration.

---

## 2. Active Model Registry & Actual Model Labels

### 2.1 Presets in `blindspot/models/registry.py`

| Model Identifier | Display Name | Task | Num Classes | Declared Labels | HF Hub id2label Mapping | Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `distilbert-base-uncased-finetuned-sst-2-english` | DistilBERT SST-2 | `SENTIMENT` | 2 | `["NEGATIVE", "POSITIVE"]` | `{0: "NEGATIVE", 1: "POSITIVE"}` | `DistilBertForSequenceClassification` |
| `textattack/albert-base-v2-SST-2` | ALBERT Base SST-2 | `SENTIMENT` | 2 | `["NEGATIVE", "POSITIVE"]` | `{0: "LABEL_0", 1: "LABEL_1"}` / `{0: "NEGATIVE", 1: "POSITIVE"}` | `AlbertForSequenceClassification` |
| `cardiffnlp/twitter-roberta-base-sentiment-latest` | Twitter RoBERTa Latest | `SENTIMENT` | 3 | `["NEGATIVE", "NEUTRAL", "POSITIVE"]` | `{0: "negative", 1: "neutral", 2: "positive"}` | `RobertaForSequenceClassification` |
| `textattack/bert-base-uncased-SST-2` | BERT Base SST-2 | `SENTIMENT` | 2 | `["NEGATIVE", "POSITIVE"]` | `{0: "NEGATIVE", 1: "POSITIVE"}` | `BertForSequenceClassification` |
| `cardiffnlp/twitter-roberta-base-sentiment` | Twitter RoBERTa Base | `SENTIMENT` | 3 | `["NEGATIVE", "NEUTRAL", "POSITIVE"]` | `{0: "LABEL_0", 1: "LABEL_1", 2: "LABEL_2"}` (0=neg, 1=neu, 2=pos) | `RobertaForSequenceClassification` |
| `roberta-base-openai-detector` | RoBERTa OpenAI Detector | `AI_TEXT_DETECTION` | 2 | `["Fake", "Real"]` | `{0: "Fake", 1: "Real"}` | Gated / INELIGIBLE for sentiment experiments |

### 2.2 Inspection of Label Normalization Logic

In [blindspot/models/huggingface_wrapper.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/models/huggingface_wrapper.py#L20-L41):
```python
def normalize_label_name(label: str, num_classes: int = 2) -> str:
    cleaned = str(label).strip()
    upper = cleaned.upper()
    if num_classes == 2:
        if upper in {"LABEL_0", "0", "NEG", "NEGATIVE"}:
            return "NEGATIVE"
        if upper in {"LABEL_1", "1", "POS", "POSITIVE"}:
            return "POSITIVE"
    elif num_classes == 3:
        if upper in {"LABEL_0", "0", "NEG", "NEGATIVE"}:
            return "NEGATIVE"
        if upper in {"LABEL_1", "1", "NEU", "NEUTRAL"}:
            return "NEUTRAL"
        if upper in {"LABEL_2", "2", "POS", "POSITIVE"}:
            return "POSITIVE"
    return upper
```

#### Defect / Assumption:
- Hardcodes index assumptions (`LABEL_0` is negative, `LABEL_1` is positive or neutral).
- Does not inspect the actual model config mapping `id2label` to verify semantic meanings.
- If a future or custom model has `{0: "POSITIVE", 1: "NEGATIVE"}` or uses `LABEL_0` for positive, this logic inverts the model's semantics.

---

## 3. Binary vs Multiclass Handling

### 3.1 Two-Class vs Three-Class Representations
- **Binary Sentiment Classifiers**: Predict only over $\{\text{NEGATIVE}, \text{POSITIVE}\}$. There is no neutral state.
- **Three-Class Sentiment Classifiers**: Predict over $\{\text{NEGATIVE}, \text{NEUTRAL}, \text{POSITIVE}\}$.

### 3.2 Places Where 2-Class Assumptions Exist
1. **Fallback Classifier in [blindspot/models/huggingface_wrapper.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/models/huggingface_wrapper.py#L248-L259)**:
   Defaults to `[p_neg, p_pos]` and only handles 3 classes via artificial weighting `p_neu = 0.2, p_pos = p_pos * 0.8, p_neg = p_neg * 0.8`.
2. **Binary Flip Assumption in [blindspot/core/types.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/core/types.py#L271-L280)**:
   `is_prediction_flip(orig, pert)` is evaluated simply as string inequality `orig != pert`. In binary classification, string inequality equals a polarity flip. In 3-class classification, `POSITIVE → NEUTRAL` is not a polarity flip, but `is_prediction_flip` returns `True`.
3. **Default ModelMetadata in [blindspot/core/types.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/core/types.py#L311-L312)**:
   Defaults `num_classes = 2` and `label_names = ["NEGATIVE", "POSITIVE"]`.

### 3.3 Places Where 3-Class Assumptions Exist
1. **Reporting Proportions in [blindspot/reporting/thesis_graphs.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/reporting/thesis_graphs.py#L86-L92)**:
   Hardcodes 3 stacked bars: `"POS" in lbl`, `"NEG" in lbl`, else `neu_c += 1`. For binary models, it assumes any non-POS/non-NEG label is neutral.
2. **Transition Matrix in [blindspot/testing/metrics.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/testing/metrics.py#L170-L195)**:
   Assumes square matrices across arbitrary model labels, but does not separate binary models from 3-class models when comparing cross-model transitions.

---

## 4. Current Baseline Handling

### 4.1 Implementation in `runner.py` and `behavioral.py`
In [blindspot/testing/behavioral.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/testing/behavioral.py#L338-L350):
```python
for seed in probe_set.seed_texts:
    pred = self.model.predict_result(seed)
    seed_predictions[seed] = pred
    stype = probe_set.sentence_types.get(seed, SentenceType.LITERAL.value)
    baselines[seed] = BaselineEvaluation(
        model_id=self.model.model_name,
        seed_text=seed,
        sentence_type=stype,
        prediction=pred,
        latency_ms=pred.latency_ms,
    )
```

### 4.2 Identified Gaps in Baseline Handling
1. **No `baseline_id`**: The `BaselineEvaluation` record lacks a unique, immutable `baseline_id` (e.g. `base_<hash>` or `base_<uuid>`).
2. **Unanchored Probe Records**: Neither `ModelProbeEvaluation` nor `BehavioralProbeResult` stores `baseline_id`. They embed a copy of `original_prediction`, but cannot be formally traced back to a specific immutable baseline record.
3. **Conflation of Model Observation with Linguistic Reality**:
   - The system records `original_prediction.label` as the "original label" of the sentence.
   - When no human ground-truth annotation exists, the model's prediction is merely an **observed baseline**, not the objective polarity of the sentence.
   - There is no distinction between `reference_polarity` (annotator ground truth or UNKNOWN) and `model_observed_polarity`.

---

## 5. End-to-End Execution Trace

The lifecycle follows this trajectory:

```text
Original Seed Sentence
      ↓ [1] Probe Generation: SharedProbeGenerator.generate_probes()
Candidate Probe Set (7 Calibrated Slots P001-P007)
      ↓ [2] Probe Selection: User checkboxes in Probe Lab UI
Selected Probe Set
      ↓ [3] Probe Validation: SharedProbeSet.validate() & LinguisticProbe.validate()
Staged Probe Set in Session State
      ↓ [4] Run Plan Formation: Staged set passed into ExperimentConfig -> RunPlan
Runner Execution Thread (runner.py)
      ↓ [5] Baseline Evaluation: Model evaluated ONCE on original seed sentence
BaselineEvaluation (Stored in memory and persisted to disk)
      ↓ [6] Batched Perturbation Inference: Model evaluated on perturbed texts
Perturbed Prediction Results
      ↓ [7] Behavioral Analysis: classify_behavior()
Outcome Classification (EXPECTED_FLIP, MISSING_FLIP, EXPECTED_PRESERVE, UNEXPECTED_FLIP)
      ↓ [8] Metrics Aggregation: compute_observed_flip_rate, compute_ece, etc.
Model Metrics Dictionary
      ↓ [9] Failure Diagnosis: TaxonomyClassifier / classify_behavior()
Rule-based Taxonomy (BLIND, SPURIOUS, MISWEIGHTED, UNDETERMINED, NONE)
      ↓ [10] Persistence & Reporting: RunStore writes JSONs; Visualizer renders PNGs
Run Directory (runs/<exp_id>/)
      ↓ [11] Research UI Presentation: Live Run streaming & Reports Inspector
Streamlit Dashboard
```

### 5.1 Verification of Probe Regeneration / Silent Modification
- **Does the runner silently regenerate probes?**
  - **No, when `config.selected_probe_set` is provided**: In [blindspot/execution/runner.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/execution/runner.py#L165-L183), the runner consumes `self.config.selected_probe_set` directly without re-generation.
  - **However, fallback exists**: If `config.selected_probe_set is None`, the runner generates brand new probes from scratch via `SharedProbeGenerator().generate_probes()`.
  - **Probe ID Stability**: IDs are generated deterministically using SHA-256 over `seed_text|perturbed_text|perturbation_type|expected_semantic_effect`. Probe IDs remain stable across stages.

---

## 6. Current Expectation & Flip Calculation Logic

### 6.1 Expectation Logic
In [blindspot/perturbations/shared.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/perturbations/shared.py#L91-L148):
- Probe semantic intent is mapped to:
  - `invert` / `REVERSE_POLARITY` -> `expected_flip = True`, `DIFFERENT_LABEL`
  - `preserve` / `PRESERVE_MEANING` -> `expected_flip = False`, `SAME_LABEL`
  - `strengthen` / `STRENGTHEN_POLARITY` -> `expected_flip = False`, `SAME_LABEL`, `INCREASE`
  - `weaken` / `WEAKEN_POLARITY` -> `expected_flip = False`, `SAME_LABEL`, `DECREASE`
  - `concession` / `SHIFT_CONTRAST` -> `expected_flip = True`, `DIFFERENT_LABEL`

### 6.2 Flip Calculation Deficiencies
In [blindspot/testing/behavioral.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/testing/behavioral.py#L101):
```python
flipped = is_prediction_flip(orig_lbl, prb_lbl)
```
Where `is_prediction_flip` is:
```python
return str(original_label).strip().upper() != str(perturbed_label).strip().upper()
```

#### Why This Breaks Science:
1. **Raw Label Flip vs Polarity Flip**:
   - For a binary model: `POSITIVE → NEGATIVE` is both a raw label flip and a polarity flip.
   - For a 3-class model: `POSITIVE → NEUTRAL` is a raw label change, but NOT a polarity flip (it is a partial shift / neutralization).
   - Currently, `flipped` evaluates to `True` for both.
2. **Missing Distinction Between 5 Transition Categories**:
   - `raw_label_flip`: `original_raw_label != perturbed_raw_label`
   - `polarity_flip`: `POSITIVE → NEGATIVE` or `NEGATIVE → POSITIVE`
   - `semantic_state_change`: any state change in $\{\text{POS}, \text{NEG}, \text{NEU}\}$
   - `expectation_match`: whether observed transition satisfies the probe's linguistic expectation
   - `preservation`: whether the model preserved the expected semantic state

---

## 7. Current Failure Classification Analysis

### 7.1 Implementation in `classify_behavior()`
In [blindspot/testing/behavioral.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/testing/behavioral.py#L162-L212):
- **Case 1**: `is_expected_flip and flipped` -> `BehavioralOutcome.EXPECTED_FLIP`, `FailureCategory.NONE`
- **Case 2**: `is_expected_flip and not flipped` -> `BehavioralOutcome.MISSING_FLIP`, `FailureCategory.BLIND`
- **Case 3**: `not is_expected_flip and not flipped` ->
  - If `STRENGTHEN` and $\Delta c < -15\text{ pp}$ -> `FailureCategory.MISWEIGHTED`
  - If `WEAKEN` and $\Delta c > +15\text{ pp}$ -> `FailureCategory.MISWEIGHTED`
  - Else -> `BehavioralOutcome.EXPECTED_PRESERVE`, `FailureCategory.NONE`
- **Case 4**: `not is_expected_flip and flipped` ->
  - If `STRENGTHEN` or `WEAKEN` -> `FailureCategory.MISWEIGHTED`
  - Else -> `BehavioralOutcome.UNEXPECTED_FLIP`, `FailureCategory.SPURIOUS`

### 7.2 AI / LLM Failure Prediction Audit
- A thorough search across the codebase for terms like `"predicted failure"`, `"failure prediction"`, `"predicted taxonomy"`, `"AI diagnosis"`, `"LLM diagnosis"`, `"predicted misweighted"`, `"predicted blind"`, and `"predicted spurious"` was conducted.
- **Result: Zero AI/LLM failure predictions exist in the codebase.**
- The existing failure categorization is entirely rule-based and derived from model outputs.
- However, the rules suffer from the binary flip assumption detailed in Section 6.2 (e.g. `POSITIVE → NEUTRAL` under negation is treated as a successful flip rather than a partial shift or weakening).

---

## 8. Current Metrics Analysis

In [blindspot/testing/metrics.py](file:///c:/Dev/Projects/Multimodel_Blindspot-main/blindspot/testing/metrics.py):
1. `observed_flip_rate`:
   $$\text{observed\_flip\_rate} = \frac{\text{flips}}{\text{total\_evaluations}}$$
   Conflates raw label changes with polarity flips.
2. `expected_flip_rate`:
   $$\text{expected\_flip\_rate} = \frac{\text{flips\_on\_expected}}{\text{count}(\text{expected\_flip} == \text{True})}$$
   This is actually **Expected Flip Compliance**, NOT the Expected Flip Rate (which should be probes expected to reverse divided by applicable probes).
3. `preserve_rate`:
   $$\text{preserve\_rate} = \frac{\text{preserves\_on\_expected}}{\text{count}(\text{expected\_flip} == \text{False})}$$
4. `behavioral_consistency`:
   $$\text{consistency} = \frac{\text{expectation\_satisfied}}{\text{total\_evaluations}}$$
5. `confidence_flip_rate`:
   $$\text{fraction with } \Delta c < -20\text{ percentage points}$$

#### Missing Canonical Thesis Metrics:
- **Observed Flip Rate**: $\frac{\text{polarity\_flips}}{\text{applicable\_probes}}$
- **Expected Flip Rate**: $\frac{\text{probes\_expected\_to\_reverse}}{\text{applicable\_probes}}$
- **Expected Flip Compliance**: $\frac{\text{correctly\_reversed}}{\text{probes\_expected\_to\_reverse}}$
- **Preservation Rate**: $\frac{\text{correctly\_preserved}}{\text{probes\_expected\_to\_preserve}}$
- **Behavioral Consistency**: $\frac{\text{expectation\_matches}}{\text{applicable\_probes}}$
- **Confidence Shift**: $\Delta c_{\text{pp}} = (c_{\text{pert}} - c_{\text{orig}}) \times 100$
- **Raw Label Flip Rate**: $\frac{\text{raw\_label\_flips}}{\text{total\_evaluations}}$
- **Polarity Flip Rate**: $\frac{\text{actual\_positive\_negative\_reversals}}{\text{polarity\_applicable\_probes}}$

---

## 9. Current UI & Live-Run Execution Path

1. **Probe Lab (`blindspot/ui/probe_lab.py`)**:
   - Generates candidates for source sentence.
   - User toggles selection.
   - User clicks "Send to Experiment Lab", creating `st.session_state["staged_probe_set"]`.
2. **Experiment Lab (`blindspot/ui/experiment_lab.py`)**:
   - Displays staged probes.
   - User selects target models.
   - Clicking "RUN EXPERIMENT" passes `staged_probe_set` and `selected_probe_ids` to `ExperimentRunner`.
3. **Live Run (`blindspot/ui/live_run.py`)**:
   - Polls active runner.
   - Renders telemetry banner, progress bar, per-model cards, and execution event stream.
   - Allows incremental inspection of completed models.
4. **Comparison (`blindspot/ui/comparison.py`)**:
   - Compares metrics across models.
5. **Reports (`blindspot/ui/reports_view.py`)**:
   - Shows summary statistics and publication figures.

---

## 10. Summary of Architectural Discrepancies & Duplicated Logic

| Item | Location A | Location B | Discrepancy / Problem |
| :--- | :--- | :--- | :--- |
| **Label Normalization** | `models/huggingface_wrapper.py:normalize_label_name` | `models/registry.py:normalize_label_name` | Duplicated function. Hardcodes label index assumptions. |
| **Flip Detection** | `core/types.py:is_prediction_flip` | `testing/behavioral.py:is_prediction_flip` | Duplicated. Treats any string inequality as a flip. |
| **Taxonomy Diagnosis** | `testing/behavioral.py:classify_behavior` | `explainability/taxonomy.py:TaxonomyClassifier` | Duplicated logic. `TaxonomyClassifier` introduces secondary rules that override behavioral definitions based solely on XAI token counts. |
| **Probe Versioning** | `SharedProbeSet.generator_version = "2.3.0"` | `SharedProbeSet.probe_set_version = "2.2.0"` | Conflicting version metadata. |
| **Baseline Storage** | Embedded inside `ModelProbeEvaluation` | Standalone `BaselineEvaluation` dictionary | No persistent, foreign-keyed `baseline_id` tying probes to baselines. |

---

## 11. Read-Only Audit Verdict

The architecture is fundamentally capable of executing the thesis, but its scientific validity is undermined by:
1. Conflating raw class inequality with sentiment polarity flips.
2. Forcing a binary boolean expectation (`expected_flip`) across both 2-class and 3-class models.
3. Lack of a canonical semantic label space (`POSITIVE`, `NEGATIVE`, `NEUTRAL`, `UNKNOWN`).
4. Inaccurate metric definitions (e.g. Expected Flip Rate vs Expected Flip Compliance).
5. Unanchored baseline records without explicit `baseline_id`.

**Zero source code was modified during this audit phase.**  
We are now ready to proceed to **Phase 1: Model Policy** and subsequent phases.
