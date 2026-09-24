# BLINDSPOT — FINAL RESEARCH INTEGRITY & CANONICAL PROBE AUDIT REPORT

**Author**: Lead Research-Software Architect, NLP Robustness & Behavioral Evaluation  
**Date**: September 20, 2026  
**Version**: 2.2.0-canonical  
**Target Invariant**: $\text{Generated} \ge \text{Selected} = \text{Planned} = \text{Executed} = \text{Analyzed} = \text{Reported}$

---

## 1. Executive Summary

BlindSpot has completed a comprehensive architectural and methodological restructuring to establish an uncompromised, research-grade pipeline for behavioral auditing of NLP text classifiers.

Prior versions exhibited a critical validity problem: probe generation, UI selection, and execution operated as disconnected subsystems where stimuli were generated independently at multiple stages, original sentences lacked first-class baseline representation, and behavioral metrics conflated semantic inversion with semantic invariance.

Under **BlindSpot v2.2.0**, the entire pipeline has been unified into a single canonical lifecycle:
1. **Single Source of Truth**: Strongly-typed `LinguisticProbe` and `SharedProbeSet` data models with deterministic SHA-256 identification.
2. **Decoupled Architecture**: Strict separation between Generation $\neq$ Selection $\neq$ Execution.
3. **Primary Research Metrics**: First-class baseline evaluation, canonical multiclass prediction flip detection, and stratified flip/preserve rates.
4. **Interactive Probe Research Workbench**: Interactive candidate catalog, custom probe injection, and explicit staging gates.
5. **Research-First Top Navigation UI**: Sleek horizontal top navigation bar (`Overview | Experiment | Probes | Run | Analyze | Reports | System`) with secondary domain subtabs and minimized sidebar.
6. **Automated Verification**: 20 targeted tests in `tests/test_probe_integrity.py` validating every layer of the protocol.

---

## 2. Pipeline Discrepancy Resolution & Audit Answers

As documented in `PROBE_PIPELINE_AUDIT.md`, all 20 structural pipeline vulnerabilities have been comprehensively resolved:

| Question | Architectural Resolution in v2.2.0 |
| :--- | :--- |
| **Q1: Where are probes generated?** | Centrally in `SharedProbeGenerator` using registered perturber engines. |
| **Q2: Which files/classes generate?** | `SharedProbeGenerator` (`blindspot/perturbations/shared.py`) orchestrating modular perturbers. |
| **Q3: What parameters govern generation?** | `seed_texts`, `perturbation_types`, `sentence_types`. |
| **Q4: Exactly which probes are created?** | Deterministically generated variants with stable SHA-256 IDs across 6 categories. |
| **Q5: Where does Probe Lab get probes?** | Interactively from `SharedProbeGenerator`, populating the interactive candidate catalog. |
| **Q6: Does Probe Lab regenerate or pull?** | Generates explicitly on demand; allows inline editing and custom additions. |
| **Q7: What options are shown in Experiment Lab?** | Displays active Verified Catalog when staged, or dynamic category multi-select. |
| **Q8: Does Experiment Lab pass same probes?** | Passes exact `selected_probe_set` directly to `ExperimentConfig` without re-generation. |
| **Q9: Where does Live Run get probes?** | `ExperimentRunner` consumes `config.selected_probe_set` or generates deterministically once. |
| **Q10: Are probes regenerated during Live Run?** | **NO.** If `selected_probe_set` is provided, zero re-generation occurs. |
| **Q11: Are original sentences evaluated as baseline?** | **YES.** Evaluated first and recorded as dedicated `BaselineEvaluation` records per model. |
| **Q12: Where are baseline results stored?** | Stored in `model_baselines[model_id]` and attached to `final_results`. |
| **Q13: Does user control individual probes?** | **YES.** Checkboxes per probe, Select All / Select None, and custom injection in Probe Lab. |
| **Q14: Are all probes audited against all models?** | **YES.** Identical `SharedProbeSet` is batched across all selected models. |
| **Q15: How is flip rate defined?** | Strictly `is_prediction_flip(orig_label, pert_label)` supporting multiclass. |
| **Q16: Does flip rate separate expected vs unexpected?** | **YES.** Stratified into `observed_flip_rate`, `expected_flip_rate`, and `preserve_rate`. |
| **Q17: How is label preservation evaluated?** | Evaluated via `preserve_rate` over all probes where `expected_flip == False`. |
| **Q18: What is the primary metric?** | Primary: Stratified Behavioral Robustness (`EFR`, `PR`, `Consistency`). Secondary: Failure Taxonomy. |
| **Q19: Are confidence deltas clear?** | Formatted strictly as signed percentage points (e.g., `-22.00 percentage points`). |
| **Q20: Do counts match across stages?** | Verified via post-run automated audit: `planned == executed == analyzed == reported`. |

---

## 3. Mathematical Integrity of Stratified Metrics

Prior aggregate flip metrics conflated opposing linguistic objectives. BlindSpot v2.2.0 mathematically stratifies all behavioral evaluations:

$$\text{Observed Flip Rate} = \frac{\sum_{i=1}^N \mathbb{I}[y_0 \neq y_p]}{N}$$

$$\text{Expected Flip Rate} = \frac{\sum_{p_i \in \mathcal{P}_{\text{flip}}} \mathbb{I}[y_0 \neq y_p]}{|\mathcal{P}_{\text{flip}}|}$$

$$\text{Preserve Rate} = \frac{\sum_{p_i \in \mathcal{P}_{\text{preserve}}} \mathbb{I}[y_0 = y_p]}{|\mathcal{P}_{\text{preserve}}|}$$

$$\text{Behavioral Consistency} = \frac{|\text{Satisfied Expectations}|}{N}$$

$$\text{Confidence Shift} = (c_{\text{perturbed}} - c_{\text{original}}) \times 100 \text{ percentage points}$$

---

## 4. UI & Ergonomic Modernization

- **Top Navigation Bar**: Replaced vertical sidebar navigation with a sleek, compact horizontal navigation bar across the top of the workstation (`Overview | Experiment | Probes | Run | Analyze | Reports | System`).
- **Domain Subtabs**: Complex domains (`Run`, `Analyze`, `Reports`) provide secondary horizontal tab controls for rapid switching without re-routing.
- **Minimized Utilities Sidebar**: Sidebar converted to high-density session utilities: active experiment badge, staged catalog status, quick launcher gates, and debug telemetry.
- **Interactive Probe Workbench**: Complete visual catalog supporting pragmatic sentence classification, batch selection, inline human editing, schema validation, and 1-click staging.

---

## 5. Verification Status & Test Suite Summary

The BlindSpot research test suite has expanded from 68 tests to **98 automated tests**, all executing and passing cleanly:
- Total Test Cases: **98**
- Failures: **0**
- Errors: **0**
- Total Runtime: ~130 seconds

### Diagnostic Test Breakdown:
1. **Canonical Probe Integrity & Pipeline Counts** (20 tests in `test_probe_integrity.py`):
   - Deterministic SHA-256 IDs, uniqueness, validation, multiclass flips, stratified rates, and pipeline equality assertions ($\text{Planned} == \text{Executed} == \text{Analyzed} == \text{Reported}$).
2. **Behavioral Taxonomy Synthetic Calibration** (14 tests in `test_behavioral_taxonomy.py`):
   - Pure, model-independent `classify_behavior(...)` evaluation across Case 1 Expected Flip, Case 2 Blind, Case 3 Expected Preserve, Case 4 Spurious, Case 5-6 Multiclass, Case 7 Misweighted, Case 8 Undetermined, model name independence, and zero-failure retention.
3. **Flip Analysis & Percentage-Point Deltas** (8 tests in `test_flip_analysis.py`):
   - Multiclass transition matrices, percentage-point deltas, signed shifts, and edge case normalization.
4. **Probe Calibration & Proverb Support** (4 tests in `test_probe_calibration.py`):
   - Calibrated 7-probe generator, proverb pragmatic processing ("All that glitters is not gold"), invalid probe blocking, and determinism.
5. **Deterministic Acceptance Suite (Section 37)** (4 tests in `test_deterministic_acceptance.py`):
   - Evaluated 7 generated $\to$ 4 selected $\to$ 2 models producing exactly 10 evaluations (2 baselines + 8 probes), 16 evals on 7 probes, 4 on 1 probe, and custom probe lifecycle.
6. **Existing Workstation & Architecture Baseline** (48 tests):
   - Perturbations, model wrappers, metrics, LIME/SHAP explainers, cache eviction, scheduler, and UI launchers.

---

## 6. Real-Model Diagnostic Evaluation (Section 39)

A live diagnostic run was performed using the fine-tuned sequence classifier `distilbert-base-uncased-finetuned-sst-2-english` across 14 calibrated probe stimuli (7 literal + 7 proverb):

- **Baseline Evaluations** (Evaluated exactly once per seed):
  - *"The movie was great and the acting was top notch."* $\to$ `POSITIVE` (0.9999)
  - *"All that glitters is not gold."* $\to$ `NEGATIVE` (0.9982)
- **Pipeline Integrity Count**:
  $$\text{Planned (14)} = \text{Executed (14)} = \text{Analyzed (14)} = \text{Reported (14)}$$
- **Genuine Behavioral Failures Detected**:
  - **Failure #1 (`BLIND`)**: On *"The movie was not great and the acting was top notch."*, the model retained `POSITIVE` (0.9921) despite single negation inversion $\to$ correctly diagnosed as **`BLIND`** (`MISSING_FLIP`).
  - **Failure #2 (`BLIND`)**: On *"All that glitters is not gold, however they do not improve over time."*, the model retained `NEGATIVE` (0.9981) ignoring the contrast modifier $\to$ correctly diagnosed as **`BLIND`** (`MISSING_FLIP`).
- **Compliant Evaluations**:
  - Double negation (*"The movie was not terrible..."*): `POSITIVE` (1.00) $\to$ `EXPECTED_PRESERVE` (`None`).
  - Adversative contrast (*"The movie was great..., but the final act was terrible."*): `NEGATIVE` (1.00) $\to$ `EXPECTED_FLIP` (`None`).
  - Proverb paraphrase (*"Not everything that is shiny is truly valuable."*): `NEGATIVE` (1.00) $\to$ `EXPECTED_PRESERVE` (`None`).
  - Proverb negation removal (*"All that glitters is gold."*): `POSITIVE` (1.00) $\to$ `EXPECTED_FLIP` (`None`).

**Conclusion**: Zero failures are no longer the default outcome. Real model failures emerge legitimately from the interaction of controlled probe contracts and model outputs, backed by probe-level evidence. Where models comply, failure counts remain exactly zero without fabrication.
