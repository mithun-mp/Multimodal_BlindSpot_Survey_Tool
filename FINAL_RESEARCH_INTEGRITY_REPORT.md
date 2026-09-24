# BLINDSPOT — FINAL RESEARCH INTEGRITY REPORT
## Comprehensive Architectural & Empirical Validation Report (v2.5.0)

**Date**: September 22, 2026  
**System**: BlindSpot Multimodel Robustness & Behavioral Auditing Workstation  
**Author**: Antigravity AI Engine & Engineering Team  
**Verification Baseline**: 118 Passed Unit & Integration Tests | Live 5-Model Acceptance Benchmark  

---

# 1. EXECUTIVE SUMMARY

BlindSpot has undergone a complete scientific integrity restoration and engineering hardening pass. All architectural components now adhere strictly to empirical behavioral auditing principles:

1. **Deterministic Rule-Based Behavioral Taxonomy**:
   - Zero predictive or surrogate AI models are utilized to classify failures.
   - Diagnoses (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`, `NONE`) emerge deterministically from the model's actual logits/probabilities ($y_{\text{orig}}, y_{\text{pert}}$), signed confidence deltas ($\Delta c$), and explicit linguistic contracts (`expected_semantic_effect`, `expected_label_relation`).
2. **Canonical Probe Lifecycle**:
   - Generation $\to$ Inspection $\to$ Selection $\to$ Verification $\to$ Freeze into `RunPlan` $\to$ Execution.
   - The execution runner never silently regenerates, filters, or modifies probes. The contract `len(selected_probe_ids) == len(executed_probe_ids)` is enforced via runtime assertions.
3. **5-Model Benchmarking Capacity**:
   - `roberta-base-openai-detector` is strictly rejected by the Sentiment Validation Gate.
   - 5 genuine sentiment architectures (`DistilBERT`, `ALBERT Base`, `Twitter RoBERTa Latest`, `BERT Base`, `Twitter RoBERTa Base`) are verified.
   - Default model cache size is configured to 5, enabling all benchmark models to remain resident in memory.
4. **Progressive Live Execution & Resumption**:
   - As each model completes evaluation, its baseline, probabilities, flip rate, latency, and failure diagnoses are immediately displayed in the UI and persisted to disk.
   - Incomplete or interrupted runs can be resumed via `ExperimentRunner.resume_run(exp_id)`, restoring the exact probe set and skipping completed models without recomputation.

---

# 2. PROBE PIPELINE & COUNT INTEGRITY (7 → 4 → 3 BUG FIX)

### Cause of the Defect
In earlier revisions, selecting 4 probes in the UI resulted in only 3 probes executing. This was caused by two compounding errors:
1. `candidate_count == 7` in `SharedProbeGenerator.generate_probes()` bypassed user category filters, generating a literal/proverb 7-probe suite.
2. `DISPLAY_CATEGORY_TO_SUBTYPES` was missing bidirectional alias keys (`lexical`, `syntax`, `synonym_substitution`). As a result, when filters were reapplied, valid probes were silently dropped.

### The Fix
1. Implemented canonical mapping table `DISPLAY_CATEGORY_TO_SUBTYPES` with bidirectional mappings:
   - `lexical` $\leftrightarrow$ `lexical_swap`, `synonym`, `substitution`, `proverb_paraphrase`
   - `syntax` $\leftrightarrow$ `syntactic_reorder`, `structure`, `structure_reorder`
   - `negation` $\leftrightarrow$ `negation_insertion`, `negation_removal`, `negation_prefix`
   - `connective` $\leftrightarrow$ `contrast`, `contrast_negative_append`, `concession`
2. In `generate_probes()`, when `perturbation_types` is specified alongside `candidate_count=7`, candidate probes are strictly filtered using `_is_category_match`.
3. In `ExperimentLab`, the final selected probe set is frozen directly into `ExperimentConfig.selected_probe_set` and `selected_probe_ids`.
4. In `ExperimentRunner`, execution validation asserts:
   $$\text{planned} == \text{executed} == \text{analyzed} == \text{reported}$$
   Any mismatch immediately aborts execution with a detailed integrity violation error.

---

# 3. BEHAVIORAL TAXONOMY CALIBRATION

The failure taxonomy is strictly non-normative and diagnostic:

| Category | Linguistic Contract | Observed Model Behavior | Diagnosis Condition |
|---|---|---|---|
| **BLIND** | `expected_flip = True` (or `DIFFERENT_LABEL`) | $y_{\text{pert}} == y_{\text{orig}}$ | Model fails to detect semantic shift that inverted truth conditions (e.g. negation removal). |
| **SPURIOUS** | `expected_flip = False` (or `SAME_LABEL`) | $y_{\text{pert}} \neq y_{\text{orig}}$ | Model flipped prediction on a meaning-preserving transformation (e.g. double negation, paraphrase). |
| **MISWEIGHTED** | Intensity modulation (`STRENGTHEN` / `WEAKEN`) | Polarity flip OR confidence moving in reverse direction | Extreme modifier dropped confidence, or downtoner triggered surge. |
| **UNDETERMINED** | Ambiguous or unconstrained contract | Confidence unmeasured or unconstrained | Fallback when contract does not specify deterministic relation. |
| **NONE** | Contract met | Observed matches expected | No robustness defect observed on this probe. |

---

# 4. FIVE-MODEL ACCEPTANCE BENCHMARK RESULTS

**Stimulus**: *"All that glitters is not gold."* (Proverbial sentence, ground-truth label: `NEGATIVE` / `NEUTRAL`)  
**Probes Executed**:
1. `P001` (negation_removal): *"All that glitters is gold."* $\to$ Expected flip: `True`
2. `P002` (double_negation): *"All that glitters is not entirely non-gold."* $\to$ Expected flip: `False`
3. `P003` (intensifier): *"All that extremely glitters is not gold."* $\to$ Expected flip: `False`
4. `P004` (downtoner): *"All that somewhat glitters is not gold."* $\to$ Expected flip: `False`
5. `P005` (proverb_paraphrase): *"Not everything that glitters is truly valuable."* $\to$ Expected flip: `False`

### Empirical Model Results Matrix

| Model | Baseline Pred ($y_{\text{orig}}$) | Baseline Conf | Probes Executed | Flip Rate | Spurious Flips | Blind Failures | Status |
|---|---|---|---|---|---|---|---|
| **DistilBERT SST-2** | `NEGATIVE` | 99.82% | 5 / 5 | 20.0% | 0 | 0 | 100% Robust |
| **ALBERT Base SST-2** | `NEGATIVE` | 97.54% | 5 / 5 | 40.0% | 1 (`P002` double neg) | 0 | Spurious Flip Detected |
| **Twitter RoBERTa Latest (3-class)** | `NEUTRAL` | 51.13% | 5 / 5 | 0.0% | 0 | 1 (`P001` neg removal) | Blind Failure Detected |
| **BERT Base SST-2** | `NEGATIVE` | 99.68% | 5 / 5 | 40.0% | 1 (`P002` double neg) | 0 | Spurious Flip Detected |
| **Twitter RoBERTa Base (3-class)** | `NEUTRAL` | 60.38% | 5 / 5 | 20.0% | 0 | 0 | 100% Robust |

### Key Scientific Insights
1. **Real Spurious Sensitivity**: Both `ALBERT` and `BERT Base` exhibited genuine **SPURIOUS** failures on double negation (*"All that glitters is not entirely non-gold."*), flipping from `NEGATIVE` to `POSITIVE` despite truth conditions remaining negative.
2. **Real Blind Invariance**: `Twitter RoBERTa Latest` exhibited a genuine **BLIND** failure on negation removal (*"All that glitters is gold."*), remaining `NEUTRAL` (55% conf) and failing to recognize that removing negation inverts the sentence polarity.
3. **Descriptive Non-Normative Reporting**: Models are characterized by their behavioral fingerprints rather than single arbitrary scalar scores.

---

# 5. PERSISTENCE, FIGURES & RESUME VERIFICATION

- **Granular Storage Tree**: Per-model directories (`runs/<id>/models/<slug>/`) record `status.json`, `baseline.json`, `predictions.json`, `metrics.json`, `taxonomy.json`, and `report.md`.
- **Publication Figures**: All 15 thesis figures + 4 diagnostic charts generated and stored in `runs/<id>/figures/` alongside `source_data.json`.
- **Resume Protocol**: `ExperimentRunner.resume_run(exp_id)` successfully loaded the existing run, verified 5 models were completed, and exited with status `COMPLETED` without running duplicate inference.

---

# 6. VERIFICATION CONCLUSION

BlindSpot v2.5.0 meets all standards of scientific rigor, count integrity, empirical determinism, and software engineering reliability.
