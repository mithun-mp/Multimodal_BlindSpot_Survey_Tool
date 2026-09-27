# BLINDSPOT — OUTPUT UI / TABLE / COMPARISON / FAILURE VISUALIZATION REDESIGN PLAN
**Artifact File:** `audit_reports/OUTPUT_UI_REDESIGN_PLAN.md`  
**Date:** September 28, 2026  
**Status:** Approved for Phased Implementation  
**Target:** BlindSpot Multimodal Behavioral & Explainability Auditing Workstation

---

## Architecture Principles & UX Objectives

1. **Research Logic Visible at a Glance:**  
   A researcher looking at a result table must immediately identify:
   - What was expected (verified semantic ground truth),
   - What each model actually did,
   - Which model deviated,
   - What type of deviation or failure occurred,
   - What evidence supports the classification.

2. **No Model Identity Collisions:**  
   The two CardiffNLP Twitter RoBERTa models (`...sentiment-latest` vs `...sentiment`) must NEVER collide, collapse, or overwrite each other. Every model has a canonical identity, display name, and short name.

3. **Cell-Level Deviation Highlighting (Not Row-Level Alone):**  
   Highlight the specific cell that deviates with unambiguous status tokens:
   - `✓ MATCH` (subtle neutral/positive styling)
   - `⚠ DEVIATION` (clear amber warning badge)
   - `✕ FAILURE` (strong crimson failure badge with taxonomy label)
   - `? UNDETERMINED` (slate neutral badge)
   - `— NOT RUN` (muted disabled badge)

4. **Multi-Level Information Hierarchy:**  
   - **Level 1 (Summary):** Experiment context, status, model completeness indicator (`Models: 5 / 5`).
   - **Level 2 (Disagreement):** Primary Expected vs. Observed comparison matrix with directional transition badges (`POS ➔ NEG`).
   - **Level 3 (Diagnosis):** Dedicated deviation/failure view with structured table and evidence summary.
   - **Level 4 (Raw & Attributions):** Interactive expandable probe detail drawer.

5. **Accessibility & Color Independence:**  
   Never rely solely on color (`green = good`, `red = bad`). Every highlighted state includes clear text labels, semantic icons, and high-contrast badges.

---

## Phased Implementation Stages

### Stage 1: Canonical Model Identity & Completeness Contract
- **Target Modules:**
  - `blindspot/models/registry.py`
  - `blindspot/core/types.py`
  - `blindspot/execution/runner.py`
- **Implementation Specifications:**
  1. Add a canonical model identity registry helper:
     ```python
     MODEL_CANONICAL_NAMES = {
         "distilbert-base-uncased-finetuned-sst-2-english": {
             "display_name": "DistilBERT SST-2",
             "short_name": "DistilBERT",
             "task": "2-Class (Binary)",
             "classes": ["NEGATIVE", "POSITIVE"],
         },
         "textattack/albert-base-v2-SST-2": {
             "display_name": "ALBERT Base SST-2",
             "short_name": "ALBERT SST-2",
             "task": "2-Class (Binary)",
             "classes": ["NEGATIVE", "POSITIVE"],
         },
         "textattack/bert-base-uncased-SST-2": {
             "display_name": "BERT Base SST-2",
             "short_name": "BERT SST-2",
             "task": "2-Class (Binary)",
             "classes": ["NEGATIVE", "POSITIVE"],
         },
         "cardiffnlp/twitter-roberta-base-sentiment-latest": {
             "display_name": "Twitter-RoBERTa (Latest)",
             "short_name": "Twitter-Latest",
             "task": "3-Class (Neg/Neu/Pos)",
             "classes": ["NEGATIVE", "NEUTRAL", "POSITIVE"],
         },
         "cardiffnlp/twitter-roberta-base-sentiment": {
             "display_name": "Twitter-RoBERTa (Base)",
             "short_name": "Twitter-Base",
             "task": "3-Class (Neg/Neu/Pos)",
             "classes": ["NEGATIVE", "NEUTRAL", "POSITIVE"],
         },
     }
     ```
  2. Implement helper functions `get_model_display_name(model_id: str) -> str` and `get_model_short_name(model_id: str) -> str`.
  3. Ensure runner metadata persists `expected_models`, `completed_models`, `failed_models`, and `missing_models`.

---

### Stage 2: Canonical Result Data Contract & Model Completeness
- **Target Modules:**
  - `blindspot/analysis/cross_model.py`
  - `blindspot/ui/comparison.py`
- **Implementation Specifications:**
  1. Update `cross_model.py` matrix generation to track all configured models. If a configured model did not execute, record its status as `NOT_RUN` rather than omitting it.
  2. Add the **Model Completeness Banner** at the top of the comparison interface:
     - When all models present: `✓ Models Evaluated: 5 / 5 [DistilBERT, ALBERT, BERT, Twitter-Latest, Twitter-Base]`
     - When models missing: `⚠ Models Evaluated: 4 / 5 (1 model did not produce results: Twitter-Base [NOT RUN])`
  3. Prevent any key collision when assembling the matrix rows.

---

### Stage 3: Primary Expected-vs-Observed Comparison Table
- **Target Modules:**
  - `blindspot/ui/comparison.py`
- **Implementation Specifications:**
  1. Eliminate the character slice bug (`m.split('/')[-1][:14]`) on line 285. Use canonical short names as column headers.
  2. Remove the misleading `"Conf Delta"` column (which only subtracted model 1 and model 2).
  3. Format the table columns cleanly:
     `Probe ID | Category | Expected Behavior | DistilBERT | ALBERT SST-2 | BERT SST-2 | Twitter-Latest | Twitter-Base | Stimulus Preview`
  4. Ensure each model cell communicates:
     - Predicted Label,
     - Confidence percentage (`92.4%`),
     - Behavior relative to expectation (`✓ MATCH`, `⚠ DEVIATION`, `✕ FAIL`).

---

### Stage 4: Cell-Level Deviation Highlighting & Visual Styling
- **Target Modules:**
  - `blindspot/ui/design_system.py`
  - `blindspot/ui/comparison.py`
- **Implementation Specifications:**
  1. Inject modern CSS classes into the workstation theme for cell-level status badges:
     - `.cell-match`: Subtle green/cyan border (`#059669`), dark tint (`#064e3b22`), `✓ MATCH` indicator.
     - `.cell-deviation`: Amber border (`#d97706`), subtle amber background (`#78350f22`), `⚠ DEVIATION` indicator.
     - `.cell-failure`: Red border (`#dc2626`), crimson tint (`#7f1d1d22`), `✕ FAIL` indicator with taxonomy tag (e.g. `[BLIND]`).
     - `.cell-undetermined`: Slate/gray border (`#64748b`), neutral tint, `? UNDET` indicator.
     - `.cell-notrun`: Muted border (`#334155`), disabled styling, `— NOT RUN`.
  2. Render the primary comparison table using custom HTML table formatting or Pandas Styler so that each individual cell receives its exact semantic class.

---

### Stage 5: Dedicated Deviation/Failure View & Failure Table Redesign
- **Target Modules:**
  - `blindspot/ui/failure_lab.py`
  - `blindspot/ui/comparison.py`
- **Implementation Specifications:**
  1. Add quick view toggles in the Comparison view:
     `[ALL PROBES] | [DEVIATIONS ONLY] | [CONFIRMED FAILURES] | [MATCHES ONLY]`
     Selecting `DEVIATIONS ONLY` filters the matrix to display strictly rows containing at least one model deviation.
  2. Redesign `failure_lab.py`:
     - Add **Failure Summary Banner** (Total Deviations, Confirmed Failures, Undetermined Anomalies, Invalid Probes).
     - Add **Structured Failure Table**:
       `Severity | Target Model | Probe ID | Expected Behavior | Observed Behavior | Failure Taxonomy | Evidence Summary`
     - Keep the detailed attribution cards expandable under the table rows for complete scientific traceability.

---

### Stage 6: Interactive Probe Detail Drawer
- **Target Modules:**
  - `blindspot/ui/comparison.py`
- **Implementation Specifications:**
  1. Provide an expandable probe drawer or modal below the matrix:
     - Original baseline text + baseline model predictions,
     - Perturbed stimulus text + highlighted perturbation tokens,
     - Semantic ground truth reference (Gemini / verified contract),
     - Expected relation (`REVERSE_POLARITY` vs `PRESERVE_POLARITY`),
     - Side-by-side model prediction grid with confidence deltas in percentage points (`+18.3 pp`),
     - Attribution / saliency evidence where available.

---

### Stage 7: Model Comparison & Behavioral Matrix View
- **Target Modules:**
  - `blindspot/ui/comparison.py` (Tabs 2, 3, 4)
- **Implementation Specifications:**
  1. Tab 2 (Per-Model Audit): Show independent behavioral statistics for each architecture without subjective rankings (no "Best", "Worst", "Winner", or "Loser").
  2. Tab 3 (Pairwise Consistency): Replace raw strings with canonical short names, showing Chance-corrected Cohen's Kappa with proper contrast.
  3. Tab 4 (Behavioral Fingerprints): Update radar/bar metrics to use distinct Twitter models.

---

### Stage 8: Graph & Visualization Overhaul
- **Target Modules:**
  - `blindspot/reporting/thesis_graphs.py`
- **Implementation Specifications:**
  1. Replace all 12 instances of `.split('/')[-1][:18]` or `[:14]` with `get_model_short_name(m_id)`.
  2. Ensure `fig01_prediction_distribution.png`, `fig08_model_probe_heatmap.png`, and `fig11_model_agreement.png` display distinct labels:
     - `Twitter-Latest` vs `Twitter-Base`
  3. Re-generate all 15 figures for the active 5-model run so disk artifacts match the redesigned UI.

---

### Stage 9: Responsive Design & Accessibility Polish
- **Target Modules:**
  - `blindspot/ui/design_system.py`
  - `blindspot/ui/comparison.py`
- **Implementation Specifications:**
  1. Add horizontal scrolling containers with sticky first columns (`Probe ID / Stimulus`) so all 5 model columns remain legible on desktop displays.
  2. Ensure all badges have high contrast ratios (WCAG AA compliant).
  3. Add tooltips explaining scientific terminology:
     - `⚠ DEVIATION`: *"Model output contradicts verified semantic expectation."*
     - `? UNDETERMINED`: *"Behavioral anomaly detected, but token attribution is dispersed or inconclusive."*
     - `INVALID PROBE`: *"Perturbation contains internal artifact; excluded from model failure scoring."*

---

### Stage 10: Tests & Regression Verification
- **Target Modules:**
  - `tests/test_ui_model_identity.py`
  - `tests/test_comparison_matrix.py`
  - End-to-end verification script with Chrome CDP.
- **Verification Criteria:**
  1. All 5 models appear simultaneously in Comparison matrix, Failure Analysis, and Thesis Graphs.
  2. Twitter Base and Twitter Latest never overwrite each other.
  3. Cell-level deviation badges render properly on deviating cells.
  4. Missing models render as `— NOT RUN`.
  5. Capture AFTER screenshots into `audit_reports/output_ui_redesign/after/`.
  6. Deliver `audit_reports/OUTPUT_UI_REDESIGN_FINAL.md`.

---
*End of Redesign Plan. Ready for Stage 1 execution.*
