# BLINDSPOT — PROBE PIPELINE AUDIT

**Author**: Lead Research-Software Architect, NLP Robustness & Behavioral Evaluation Team  
**Date**: 2026-09-20  
**Status**: AUDIT COMPLETE — STRUCTURAL DEFECTS IDENTIFIED  

---

## 1. Executive Summary

This audit examines the complete end-to-end linguistic probe pipeline within BlindSpot across generation, configuration, execution, inference, analysis, reporting, and UI display:

```text
INPUT SENTENCE
      ↓
PROBE GENERATOR
      ↓
PROBE CATALOG
      ↓
EXPERIMENT CONFIGURATION
      ↓
SELECTED PROBES
      ↓
RUN PLAN
      ↓
LIVE RUN
      ↓
MODEL INFERENCE
      ↓
ORIGINAL BASELINE
      ↓
PROBE PREDICTIONS
      ↓
BEHAVIORAL ANALYSIS
      ↓
FLIP / CONFIDENCE / ACCURACY METRICS
      ↓
REPORT
```

The audit reveals a fundamental research-validity defect: **probes are generated independently at multiple decoupled points, selections are not propagated into execution, the original baseline sentence is subsumed inside probe evaluations rather than anchored as a primary comparison, and flip-rate metrics combine conflicting behavioral expectations.**

---

## 2. Granular Answers to the 20 Pipeline Questions

### Q1: How many probes are generated?
- **Probe Lab** (`blindspot/ui/probe_lab.py:24`): Generates variants for a single input text using `PerturbationEngine.generate_all()`. For a typical sentence with an auxiliary verb, negation, and content adjectives (e.g., *"The movie was great and the acting was top notch."*), this generates between **6 and 14 candidate probes**.
- **Experiment Lab Preview** (`blindspot/ui/experiment_lab.py:252`): Generates candidate probes only for the **first seed sentence** (`seed_lines[0]`), even if the researcher provided 5 sentences.
- **Experiment Runner Execution** (`blindspot/execution/runner.py:122`): Re-runs `generate_probes()` across **all seed sentences** (`self.config.seed_texts`). If there are 3 sentences, it generates `3 × N` probes (e.g., ~24-36 probes).

### Q2: Where are they generated?
Probes are generated independently in **three separate locations**:
1. `blindspot/ui/probe_lab.py:24`: Ephemeral generation for UI inspection.
2. `blindspot/ui/experiment_lab.py:252`: Ephemeral generation for preview in an expander.
3. `blindspot/execution/runner.py:122`: Generation inside the background execution thread.

### Q3: How many are displayed?
- In **Probe Lab**: All probes generated for the single input text are displayed.
- In **Experiment Lab**: Only up to **6 probes** are displayed (`sample_set.probes[:6]`), with a text caption stating `"... and N additional probes in full set"`.
- In **Live Run**: Only numeric progress counters (`m_done / m_total`) and high-level logs are displayed; individual probe IDs, perturbed texts, and predictions are not displayed during inference.
- In **Model Comparison**: All executed probes that made it into `cross_model_comparison["model_probe_matrix"]` are displayed in a table.

### Q4: Where are they filtered?
- In `SharedProbeGenerator.generate_probes()`: Probes are filtered solely by string category matching (`perturbation_types`).
- In `experiment_lab.py`: The preview filters down to the 1st input sentence and truncates to 6 rows.
- In `runner.py`: No probe-level filtering occurs. All probes generated for active categories are executed.
- **Critical Gap**: The researcher has **zero control** to select, deselect, or exclude individual generated probes.

### Q5: How many enter Experiment configuration?
**Zero probes enter `ExperimentConfig`.**
In `blindspot/ui/experiment_lab.py:364-371`, `ExperimentConfig` is constructed with:
```python
config = ExperimentConfig(
    experiment_name=exp_title,
    model_ids=selected_models_list,
    seed_texts=seed_lines,
    perturbation_types=selected_ptypes,
    explainer_type=xai_mode,
    performance_mode=PerformanceMode.from_str(perf_mode),
)
```
The config carries string category names (`perturbation_types`), but **does not contain any `LinguisticProbe` or `SharedProbeSet` objects**.

### Q6: How many enter the actual run plan?
Because `ExperimentConfig` contains no probe objects, `ExperimentRunner._execute()` generates a brand new `SharedProbeSet` from scratch:
```python
probe_gen = SharedProbeGenerator()
probe_set = probe_gen.generate_probes(
    seed_texts=self.config.seed_texts,
    perturbation_types=self.config.perturbation_types,
)
```
Whatever this runner-internal call generates becomes the actual run plan.

### Q7: How many are actually executed?
All probes in the runner-generated `probe_set` are executed across all selected models:
`Total Executed Probes = len(probe_set.probes)`.

### Q8: Why can those counts differ?
Counts differ because there is **no single canonical probe object passed through the lifecycle**:
1. Probe Lab displays $N_1$ probes for a sample sentence.
2. Experiment Lab previews $N_2$ probes (1st sentence clipped at 6).
3. Experiment Lab specification card estimates $N_{est} = \text{inputs} \times \text{models} \times (\text{categories} \times 4)$.
4. Runner executes $N_3$ probes (re-generated for all input sentences and active categories).
Because Generation $\neq$ Selection $\neq$ Execution, the researcher experiences unexpected and unpredictable evaluation counts.

### Q9: Is the original sentence evaluated?
Yes, in `BehavioralTester.evaluate_shared_probes()` (`blindspot/testing/behavioral.py:130-132`):
```python
for seed in probe_set.seed_texts:
    seed_predictions[seed] = self.model.predict_result(seed)
```
However, the original sentence is treated merely as an internal lookup dictionary to compare against perturbed variants. It is **not represented as a first-class baseline record** in the run plan or the primary results.

### Q10: Is the original prediction stored?
It is redundantly duplicated inside each `ModelProbeEvaluation.original_prediction`. If an experiment runs with 0 probes (or if all probes fail), the original baseline prediction is completely discarded.

### Q11: Are probes deterministic?
Yes. `LinguisticProbe.create()` computes a deterministic SHA-256 hash based on:
`seed_text | perturbed_text | perturbation_type | expected_semantic_effect`.

### Q12: Does every model receive exactly the same selected probe stimuli?
Yes. Within a single execution run, `probe_set` is generated once in `runner.py` and passed sequentially or in parallel to each model wrapper via `tester.evaluate_shared_probes(probe_set)`.

### Q13: Are probe IDs preserved from generation through reporting?
- **Internally within the runner**: Yes. The `probe_id` generated in `runner.py` survives into `ModelProbeEvaluation`, `results.json`, and Markdown reports.
- **Between UI preview and execution**: **No.** The `probe_id`s displayed in Probe Lab or Experiment Lab preview come from independent `SharedProbeSet` instances and are discarded when execution launches.

### Q14: Are expected semantic effects preserved?
Yes. `expected_semantic_effect` (e.g., `invert`, `preserve`, `concession`, `strengthen`) and `expected_flip` (`True`/`False`) are attached to `LinguisticProbe` and preserved on `ModelProbeEvaluation`.

### Q15: Can the user explicitly choose individual probes?
**No.** Currently, the UI only allows toggling 4 coarse category checkboxes. Individual probes cannot be checked or unchecked.

### Q16: Can the user choose a complete probe category?
Yes. Category checkboxes exist in `experiment_lab.py` (Negation, Double Negation, Connectives, Substitution).

### Q17: Can the user select all probes?
Only at the category level; not at the granular probe level.

### Q18: Can the user deselect all probes?
No. Deselecting all categories triggers a blocking validation error: *"Please select at least one probe category in Step 03."*

### Q19: Can the user add/customize probes?
**No.** There is no functionality to create a custom probe (`+ ADD CUSTOM PROBE`), edit a generated perturbation, or override the expected semantic effect.

### Q20: Are the reported flip-rate calculations mathematically tied to the executed probes?
**No, the current calculation is scientifically flawed.**
In `blindspot/testing/behavioral.py:194-195`:
```python
flips = sum(1 for e in evaluations if e.is_flipped)
flip_rate = float(flips / total_probes) if total_probes > 0 else 0.0
```
This conflates probes that are **expected to flip** (e.g. single negation) with probes that are **expected to preserve** (e.g. synonym substitution, double negation). If a model correctly preserves sentiment on a synonym substitution (i.e. does not flip), this non-flip is treated as a "failure to flip," artificially suppressing the flip rate.

---

## 3. Severity & Impact Analysis

| Issue Code | Area | Description | Severity | Impact |
| :--- | :--- | :--- | :---: | :--- |
| **AUD-01** | Architecture | Runner regenerates probes rather than executing user-selected set | **CRITICAL (P0)** | Experimental disconnect; UI cannot control what executes |
| **AUD-02** | Metrics | Flip rate combines expected flips and expected preserves | **CRITICAL (P0)** | Scientifically invalid flip-rate metrics |
| **AUD-03** | Baseline | Original sentence not represented as an explicit baseline comparison | **HIGH (P1)** | Cannot inspect baseline independent of perturbations |
| **AUD-04** | UI Selection | No individual probe selection, "Select All", or "Select None" | **HIGH (P1)** | Researcher forced to run unwanted or noisy perturbations |
| **AUD-05** | Extensibility | No custom probe entry or human probe verification/editing | **HIGH (P1)** | Cannot audit custom edge cases or non-templated stimuli |
| **AUD-06** | UI Layout | Sidebar consumes horizontal viewport width needed for research tables | **MEDIUM (P2)** | Horizontal overflow on standard 1366x768 / 1080p monitors |
| **AUD-07** | Observability | Live run does not display individual Probe IDs and outcomes | **MEDIUM (P2)** | Researcher cannot trace which probe is running during live execution |

---

## 4. Architectural Corrective Actions

1. **Establish Canonical Probe Invariant**:
   `Generation (Candidate Catalog) → Selection (SelectedProbeSet) → Validation → Execution (RunPlan)`.
   The runner will execute `config.selected_probe_set` without regeneration.
2. **Stratify Behavioral Flip Metrics**:
   - $\text{Observed Flip Rate} = \frac{\text{Observed Flips}}{\text{Executed Probes}}$
   - $\text{Expected Flip Rate} = \frac{\text{Correct Observed Flips}}{\text{Probes with Expected Flip = True}}$
   - $\text{Preserve Rate} = \frac{\text{Correct Preserved}}{\text{Probes with Expected Flip = False}}$
   - $\text{Behavioral Consistency} = \frac{\text{Expected Flips} + \text{Expected Preserves}}{\text{Total Evaluable Probes}}$
3. **Explicit Original Baseline**:
   Evaluate original sentence first per model as `BaselineEvaluation`. Render primary `BASELINE → PROBE` comparison cards.
4. **Interactive Probe Research Workbench**:
   Allow selecting all, selecting none, toggling individual probes, adding custom probes, and editing/verifying probes.
5. **Top Navigation Redesign**:
   Migrate primary routing to a compact top bar (`Overview | Experiment | Probes | Run | Analyze | Reports | System`) with secondary tabs, expanding workspace width.

---

## 5. Audit Resolution & Canonical Verification (v2.3.0)

All identified issues (**AUD-01** through **AUD-07**) have been completely resolved and verified by automated regression tests:

1. **Elimination of the 7 → 4 → 3 Discrepancy**:
   - Live Run strictly consumes the finalized immutable `RunPlan`.
   - Probes are never regenerated or silently dropped during execution.
   - If 4 probes are selected, exactly 4 are executed, analyzed, and reported.
2. **Deterministic Baseline Anchor**:
   - The original baseline sentence is evaluated exactly once per seed sentence per model.
   - Stored explicitly in `model_baselines` and anchored as the primary reference point.
3. **Calibrated Behavioral Outcome & Failure Taxonomy**:
   - Disentangled observable flip behavior (`is_prediction_flip = y_orig != y_pert`) from secondary failure interpretations (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`, `NONE`).
   - Implemented pure, testable `classify_behavior(...)` in `blindspot/testing/behavioral.py`.
4. **Interactive Staging & Verification Workbench**:
   - `Probe Lab` supports candidate generation (7 calibrated stimuli), select all/none, category selection, human verification, custom probe injection, probe editing, and JSON export.
   - Staged probe catalog persists through `SharedProbeSet` directly into `ExperimentConfig`.
5. **Pipeline Count Integrity**:
   - Validated across all models with automated equality assertion:
     $$\text{Generated} \to \text{Selected} \to \text{Planned} \to \text{Executed} \to \text{Analyzed} \to \text{Reported}$$
   - Confirmed by `test_pipeline_count_integrity` and real-model diagnostic runs.
