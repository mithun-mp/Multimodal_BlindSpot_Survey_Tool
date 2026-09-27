# BLINDSPOT — COMPREHENSIVE OUTPUT UI & DATA FLOW AUDIT
**Artifact File:** `audit_reports/OUTPUT_UI_DATA_AUDIT.md`  
**Date:** September 28, 2026  
**Auditor:** Senior Research-Data Visualization Engineer, UX Designer & Research-Software Auditor  
**System Evaluated:** BlindSpot Multimodal Behavioral & Explainability Auditing Workstation (v2.5.0 Canonical Protocol)

---

## 1. Executive Summary

An exhaustive audit of the BlindSpot Workstation output UI, comparison interfaces, failure displays, visualization pipelines, and underlying data transformations was conducted. The application possesses a solid backend execution engine and a rigorous scientific ground-truth contract. However, the presentation layer suffers from critical analytical, visual, and architectural deficiencies that obscure scientific insights:

1. **The Missing Twitter/RoBERTa Model Collision:**  
   In multiple modules (`comparison.py:285`, `thesis_graphs.py:81, 165, 449`, `runner.py:850`), model IDs are arbitrarily truncated via `.split('/')[-1][:14]` or `[:18]`. Both `cardiffnlp/twitter-roberta-base-sentiment-latest` and `cardiffnlp/twitter-roberta-base-sentiment` collapse to `"twitter-robert"` or `"twitter-roberta-ba"`. In dictionary-keyed matrices (`row[m_short] = ...`), the second Twitter model **silently overwrites** the first, reducing a 5-model audit to 4 columns. On charts and heatmaps, both models receive identical axis ticks, rendering figures uninterpretable.

2. **Absence of Cell-Level Deviation Highlighting:**  
   The primary comparison matrix renders predictions as raw text strings inside a standard Pandas DataFrame without cell-level status badges or deviation styling. When a model deviates from expected behavior (e.g. predicting `POSITIVE` when the verified ground truth expects `NEGATIVE [REVERSE]`), the cell blends into surrounding matches. Researchers cannot scan horizontally to spot model deviations in seconds.

3. **Missing Actionable Failure Table & Disconnected Summary:**  
   In the Failure Analysis view, there is no structured failure table (`Severity | Model | Probe | Expected | Observed | Failure Type | Evidence`). Failures are displayed only as large individual cards. Researchers have no compact tabular view to filter, sort, or scan behavioral failures across architectures.

4. **Misleading & Redundant Columns:**  
   The comparison matrix contains a `"Conf Delta"` column computed solely between the first two models (`abs(confs[0] - confs[1])`), which is meaningless when 3, 4, or 5 models are evaluated.

5. **Lack of Explicit Expected vs. Observed Directional Semantics:**  
   Tables frequently present either raw labels or ambiguous 0/1 binary flags rather than explicit directional transitions (`POS ➔ NEG`, `NEG ➔ POS`, `UNCHANGED`) and clear status tokens (`✓ MATCH`, `⚠ DEVIATION`, `✕ FAILURE`, `? UNDETERMINED`, `— NOT RUN`).

---

## 2. Model Registry & Identity Audit (Phases 2 & 3)

### 2.1 The Five Configured Sentiment Models
The BlindSpot research workstation supports five canonical sentiment architectures defined in `blindspot/models/registry.py`:

| Canonical Model ID | Organization / Provider | Task | Output Space | Short Alias (Buggy) | Canonical Display Name |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `distilbert-base-uncased-finetuned-sst-2-english` | HuggingFace / DistilBERT | SST-2 Sentiment | Binary (2-class) | `distilbert-bas` | **DistilBERT SST-2** |
| `textattack/albert-base-v2-SST-2` | TextAttack / ALBERT | SST-2 Sentiment | Binary (2-class) | `albert-base-v2` | **ALBERT Base SST-2** |
| `textattack/bert-base-uncased-SST-2` | TextAttack / BERT | SST-2 Sentiment | Binary (2-class) | `bert-base-unca` | **BERT Base SST-2** |
| `cardiffnlp/twitter-roberta-base-sentiment-latest` | CardiffNLP / RoBERTa | Twitter Sentiment | 3-Class (Neg/Neu/Pos) | `twitter-robert` (COLLISION) | **Twitter-RoBERTa (Latest)** |
| `cardiffnlp/twitter-roberta-base-sentiment` | CardiffNLP / RoBERTa | Twitter Sentiment | 3-Class (Neg/Neu/Pos) | `twitter-robert` (COLLISION) | **Twitter-RoBERTa (Base)** |

### 2.2 Root Cause Analysis of the Twitter Collision Bug
The missing Twitter model was traced across 4 files:

1. **`blindspot/ui/comparison.py` Line 285:**
   ```python
   for m in model_ids:
       m_short = m.split("/")[-1][:14]
       if m in m_outputs:
           out = m_outputs[m]
           lbl = out.get("perturbed_label", "UNK")
           conf = out.get("perturbed_confidence", 0.0) * 100.0
           confs.append(conf)
           row[f"{m_short}"] = f"{lbl} ({conf:.1f}%)"
   ```
   - For `cardiffnlp/twitter-roberta-base-sentiment-latest`, `m_short = "twitter-robert"`.
   - For `cardiffnlp/twitter-roberta-base-sentiment`, `m_short = "twitter-robert"`.
   - `row["twitter-robert"]` is written for the first model, then immediately **overwritten** by the second model. Only 1 column appears in the table.

2. **`blindspot/reporting/thesis_graphs.py` Lines 81, 122, 165, 187, 264, 302, 341, 417, 449, 488, 524, 561:**
   ```python
   short_names = [m.split("/")[-1][:14] for m in model_ids]
   # or
   model_names = [m.split("/")[-1][:18] for m in models_data.keys()]
   ```
   Both Twitter models produce `"twitter-robert"` or `"twitter-roberta-ba"`, resulting in identical ticks on `fig01_prediction_distribution.png` and duplicate labels on `fig11_model_agreement.png`.

3. **`blindspot/execution/runner.py` Lines 850 & 856:**
   ```python
   header_str = "| Model | " + " | ".join(f"`{m.split('/')[-1][:12]}`" for m in models_list) + " |"
   ```
   Both Twitter models truncate to `"twitter-robe"`.

---

## 3. Inventory of UI Tables & Data Components (Phase 1)

---

### Component 1: Primary Cross-Model Probe Matrix
- **Location:** `blindspot/ui/comparison.py` (Tab 1: `MODEL × PROBE MATRIX`)
- **Purpose:** Primary multi-model comparative grid evaluating model predictions against linguistic perturbation probes.
- **Data Source:** `active_results["cross_model_comparison"]["matrix"]` and `models[m]["evaluations"]`.
- **Columns (Current):** `Probe ID`, `Category`, `Expected (Gemini Ref)`, `<model_1>`, `<model_2>`, `<model_3>`, `<model_4>`, `Conf Delta`, `Perturbed Stimulus`.
- **Rows:** 1 row per evaluated probe stimulus (e.g. 7 rows for standard probe catalog).
- **Models Represented:** Currently only 4 models visible due to Twitter key collision!
- **Probe Information:** Shows truncated `Probe ID` (10 chars), `Category`, and full `Perturbed Stimulus` text.
- **Expected Behavior:** Renders raw string e.g. `NEGATIVE [REVERSE]` or `POSITIVE [PRESERVE]`.
- **Observed Behavior:** Renders string like `POSITIVE (99.4%)` in plain text.
- **Failure Information:** None in the table.
- **Problems:**
  1. Second Twitter model is overwritten and missing.
  2. Plain dataframe text: matching cells and deviating cells look identical.
  3. `Conf Delta` column is scientifically misleading (only compares model 1 and model 2).
  4. Truncated model names (`distilbert-bas`, `albert-base-v2`, `bert-base-unca`, `twitter-robert`) look unpolished.
  5. Directional transition from baseline is not shown (e.g. `POS ➔ NEG`).
  6. Clicking a row does nothing; no probe detail drawer exists.
- **Redundant Columns:** `Conf Delta` (should be removed from primary table or shown per-model as shift from baseline).
- **Missing Information:** Cell status badges (`✓ MATCH`, `⚠ DEVIATION`, `✕ FAIL`, `— NOT RUN`), transition badges (`POS ➔ NEG`), expected vs observed comparison token, probe validity badge.
- **Recommended Redesign:**
  - Replace `st.dataframe` with custom styled research data grid.
  - Fix model column keys to use canonical unique display names (`DistilBERT SST-2`, `ALBERT SST-2`, `BERT SST-2`, `Twitter-RoBERTa (Latest)`, `Twitter-RoBERTa (Base)`).
  - Include all 5 configured models; show `— NOT RUN` if a model was not executed.
  - Implement cell-level status badges with distinct visual borders, background tint, and accessible text/icon indicators (`✓ MATCH`, `⚠ DEVIATION`, `✕ FAIL`).
  - Add interactive row expansion / click-to-detail drawer exposing token diffs, validity, and attribution evidence.
  - Add quick deviation filter tabs: `ALL`, `DEVIATIONS ONLY`, `FAILURES ONLY`, `MATCHES ONLY`.

---

### Component 2: Stratified Behavioral Metrics Summary Table
- **Location:** `blindspot/ui/comparison.py` (Top of Comparison page)
- **Purpose:** Macro-level performance comparison across architectures (accuracy, flip rates, failure counts).
- **Data Source:** `active_results["models"][m]["behavioral_metrics"]`.
- **Columns (Current):** `Target Architecture`, `Accuracy`, `ECE`, `Mean Confidence`, `Observed Flip Rate`, `Expected Flip Rate`, `Reversal Compliance`, `Preserve Rate`, `Blind`, `Spurious`, `Misweighted`, `Undetermined`, `Mean Confidence Shift`.
- **Rows:** 1 row per evaluated model (5 rows in a 5-model run).
- **Models Represented:** All 5 models appear (rendered from `models_data.keys()`).
- **Probe Information:** None (aggregate summary).
- **Expected Behavior:** Shows aggregate `Expected Flip Rate`.
- **Observed Behavior:** Shows aggregate `Observed Flip Rate`, `Reversal Compliance`, `Preserve Rate`.
- **Failure Information:** Explicit counts of `Blind`, `Spurious`, `Misweighted`, `Undetermined`.
- **Problems:**
  - Table is overloaded with 13 columns, causing horizontal scroll and cognitive fatigue.
  - Architecture names are raw unformatted IDs (`distilbert-base-uncased-finetuned-sst-2-english`).
  - Missing visual distinction between 2-class binary models and 3-class models.
- **Redundant Columns:** `Preserve Rate` is redundant with `Reversal Compliance`; `ECE` is redundant in the quick summary.
- **Missing Information:** Model task indicator (2-Class vs 3-Class), status indicator (Completed vs Partial).
- **Recommended Redesign:**
  - Clean up column headers and format into a compact scorecard.
  - Use canonical display names with 2-Class / 3-Class badges.
  - Group failure taxonomy counts into a single consolidated failure badge or clean sub-columns.

---

### Component 3: Target Architecture Expected vs Predicted Audit (Tab 2)
- **Location:** `blindspot/ui/comparison.py` (Tab 2)
- **Purpose:** Per-model deep dive into expected vs predicted transitions for each probe.
- **Data Source:** `active_results["models"][sel_model]["evaluations"]`.
- **Columns (Current):** `Probe ID`, `Probe Type`, `Original Sentence`, `Perturbed Sentence`, `Orig Pred`, `Pert Pred`, `Orig Conf`, `Pert Conf`, `Conf Delta`, `Expected Flip`, `Observed Flip`, `Consistent`.
- **Rows:** 7 rows (1 per probe).
- **Models Represented:** Single model selected via dropdown.
- **Problems:**
  - Table contains 12 columns; full sentences are forced into table cells, making rows unreadable.
  - `Expected Flip` and `Observed Flip` are displayed as raw booleans (`True`/`False`), requiring mental translation.
- **Redundant Columns:** Repeating full `Original Sentence` and `Perturbed Sentence` in every cell of a 12-column table.
- **Missing Information:** Explicit directional semantics (`POS ➔ NEG`), ground truth reference polarity, failure diagnosis link.
- **Recommended Redesign:**
  - Use compact probe IDs and stimulus preview.
  - Replace raw boolean flips with directional badges (`POS ➔ NEG [FLIP]`).
  - Move full stimulus and token attribution to an expandable probe inspection panel.

---

### Component 4: Pairwise Consistency & Cohen's Kappa Matrix (Tab 3)
- **Location:** `blindspot/ui/comparison.py` (Tab 3)
- **Purpose:** Inter-model agreement matrix quantifying prediction concordance and Chance-corrected Cohen's Kappa.
- **Data Source:** `active_results["cross_model_comparison"]["pairwise_agreement"]`.
- **Columns:** Model columns matching model rows (N x N matrix).
- **Problems:**
  - Uses raw truncated model IDs (`m[:14]`), leading to identical labels for Twitter models.
- **Recommended Redesign:**
  - Use canonical short names (`DistilBERT`, `ALBERT`, `BERT`, `Twitter-Latest`, `Twitter-Base`).
  - Apply heatmap gradient with clear percentage labels.

---

### Component 5: Secondary Diagnostic Analysis — Failure Taxonomy
- **Location:** `blindspot/ui/failure_lab.py`
- **Purpose:** Diagnostic display of categorized model failures (Blind, Spurious, Misweighted, Undetermined).
- **Data Source:** `active_results["models"][m]["failures"]`.
- **Current Presentation:** KPI counter cards (`BLIND: 5`, `SPURIOUS: 3`, `MISWEIGHTED: 1`, `UNDETERMINED: 0`) followed by large vertical cards (`render_failure_record`).
- **Problems:**
  1. **NO SUMMARY OR FILTERABLE FAILURE TABLE:** If there are 15 failures, the researcher must scroll through 15 massive full-width cards.
  2. No visual severity indicator (`HIGH`, `MEDIUM`, `LOW`).
  3. No tabular comparison of expected vs observed behavior across failure modes.
- **Missing Information:**
  - Structured failure table: `Severity | Model | Probe | Expected | Observed | Failure Type | Evidence Summary`.
  - Failure rate relative to total evaluated probes.
- **Recommended Redesign (Phases 15 & 16):**
  - Add a **Failure Summary Banner** showing total deviations, confirmed failures, undetermined anomalies, and invalid probes.
  - Add a **Primary Failure Table** with clean status badges, model names, expected vs observed transitions, and actionable evidence snippets.
  - Allow clicking any failure table row to expand the detailed attribution/token explanation card below.

---

### Component 6: Recent Activity & Latest Findings (Overview Control Center)
- **Location:** `blindspot/ui/overview.py`
- **Purpose:** Dashboard entry point showing system hardware telemetry, active cache, recent runs, and latest findings.
- **Data Source:** `RunStore().list_runs()` and latest `results.json`.
- **Columns:** `Experiment Title`, `Run ID`, `Date`, `Models`, `Probes`, `Status`, `Duration`.
- **Problems:**
  - "Models" column shows just a numeric count (e.g. `5`) without showing which architectures were run.
  - If the user had a 1-model test run, it automatically overrides the 5-model run in the session state without warning.
- **Recommended Redesign:**
  - Show compact model badges in the recent runs table.
  - Provide a clear loaded-run indicator banner at the top of the workstation showing `Models: X / 5`.

---

### Component 7: Research Run Archive (Run History)
- **Location:** `blindspot/ui/run_history.py`
- **Purpose:** Historical experiment logs, artifact downloads, and run inspection.
- **Data Source:** Filesystem `runs/` metadata.
- **Columns:** `Experiment Title`, `Run ID`, `Date`, `Models`, `Probes`, `Status`, `Duration`.
- **Problems:**
  - In the inspector, model names are dumped as an unformatted comma-separated string.
  - When loading a run, the UI redirects to Overview rather than keeping the researcher in context.
- **Recommended Redesign:**
  - Render evaluated models as canonical pill badges.
  - Provide direct "Load & Inspect in Comparison" action button.

---

### Component 8: Publication-Grade Thesis Visualizations (15 Figures)
- **Location:** `blindspot/reporting/thesis_graphs.py` & `blindspot/ui/reports.py`
- **Purpose:** 15 publication-ready diagnostic charts generated to `runs/<id>/figures/*.png`.
- **Data Source:** `active_results["models"]`, `cross_model_comparison`, `probe_set`.
- **Problems:**
  - Lines 81, 122, 165, 187, 264, 302, 341, 417, 449, 488, 524, 561 all use `.split("/")[-1][:18]` or `[:14]`.
  - In `fig01_prediction_distribution.png`, the two Twitter models are both labeled `twitter-roberta-ba`.
  - In `fig11_model_agreement.png`, rows and columns 4 and 5 are both labeled `twitter-robert`.
- **Recommended Redesign:**
  - Replace all ad-hoc string slicing with a centralized `get_model_display_name(model_id)` function.
  - Ensure `Twitter-RoBERTa (Latest)` and `Twitter-RoBERTa (Base)` are always visually and semantically distinct.

---

## 4. Synthesis of Audit Findings

| Audit Dimension | Current Implementation | Identified Problem | Redesign Requirement |
| :--- | :--- | :--- | :--- |
| **Model Identity** | Sliced strings (`m.split('/')[-1][:14]`) | Collision: Twitter Latest & Base overwrite each other | Centralized canonical model identity manifest |
| **Model Completeness** | Missing models silently vanish | Researcher cannot tell if 4 or 5 models ran | Explicit `Models: 5 / 5` indicator; unrun models show `— NOT RUN` |
| **Primary Comparison** | Plain text dataframe without styling | Deviations and failures look identical to matches | Cell-level badges: `✓ MATCH`, `⚠ DEVIATION`, `✕ FAIL`, `— NOT RUN` |
| **Expected vs Observed** | Raw strings (`POSITIVE [PRESERVE]`) or booleans | Requires mental calculation to detect failure | Explicit directional badges: `NEG ➔ POS`, `POS ➔ POS` |
| **Failure Representation** | Large vertical cards only; no table | Cannot scan, filter, or sort failures | Actionable table (`Severity | Model | Probe | Expected | Observed | Failure | Evidence`) |
| **Information Hierarchy** | Raw data and long sentences dumped in grid | Cluttered, unreadable tables | 4-Level hierarchy: Overview ➔ Disagreement ➔ Evidence ➔ Raw Drawer |
| **Graphs** | Identical truncated labels on axes | Duplicate ticks; uninterpretable figures | Distinct canonical names on all 15 thesis figures |
| **Accessibility** | Dependent on color in some cards | Fails accessibility for color-blind researchers | Always combine color with explicit text tokens and iconography |

---
*End of Phase 1 Audit Report. Next Step: Phase 37 Implementation Plan.*
