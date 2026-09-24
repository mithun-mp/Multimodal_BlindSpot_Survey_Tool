# BlindSpot: Project Questions, Doubts & Technical Resolutions Log

This document serves as an ongoing knowledge base tracking all questions, technical doubts, design queries, bug reports, and implementation decisions raised during the development and auditing of **BlindSpot: A Behavioral and Explainable-AI Framework for Auditing Text Classifiers**.

---

## 📋 Log Summary Table

| ID | Topic / Category | Question / Doubt Summary | Status | Resolution / Artifact |
| :-: | :--- | :--- | :-: | :--- |
| **Q1** | Implementation Audit | Itemize current implementation state against SRS (`srs.pdf`). | **Resolved** | Verified ~100% completion across all SRS modules. |
| **Q2** | Pipeline Execution | Run the audit pipeline and test suite. | **Resolved** | Executed CLI pipeline and pytest test suite. |
| **Q3** | User Interface | Launch interactive Streamlit web dashboard. | **Resolved** | Streamlit app running at `http://localhost:8501`. |
| **Q4** | Output Sample | Provide actual audit output for `"I had fun at the festival."`. | **Resolved** | Generated 6 probes, flip rate (50%), ECE, and attributions. |
| **Q5** | Perturbation Quality | Fix formatting, spacing, comma, hyphen, and case bugs in perturbations. | **Resolved** | Refactored `negation.py`, `connectives.py`, `substitution.py`. |
| **Q6** | Grammar / Vocabulary | Is "un-awesome" a valid English word for double-negation? | **Resolved** | Replaced with standard litotes (`"It is not untrue that..."`). |
| **Q7** | System Architecture | Is a rule-based perturbation engine a bad choice for this project? | **Resolved** | Detailed scientific rationale: Rule-based + NLP heuristics is optimal. |
| **Q8** | Code Access | Run the updated pipeline and provide full source code. | **Resolved** | Verified 7 probes; provided source for all 4 perturber modules. |
| **Q9** | Scripting & Automation | Create a `run.ps1` PowerShell script to launch CLI, UI, tests, and docs. | **Resolved** | Created `d:\BlindSpot\run.ps1` with parameter modes. |
| **Q10** | OS & Execution Security | How to fix `UnauthorizedAccess` / `ExecutionPolicy` error on `run.ps1`? | **Resolved** | Provided `-ExecutionPolicy Bypass`, `Set-ExecutionPolicy`, & `python` direct. |
| **Q11** | Web Dashboard Security | Why are `file:///` markdown report links blocked in Streamlit? | **Resolved** | Browser Same-Origin Policy. Rendered reports in Streamlit expanders. |
| **Q12** | Input Validation | Validate input text for type, min/max length, and non-emptiness. | **Resolved** | Added `validate_input()` (3–500 chars) + Streamlit & pytest coverage. |
| **Q13** | Documentation | Create a persistent Markdown file tracking all project doubts & Q&A. | **Resolved** | Created `d:\BlindSpot\project_questions_and_doubts.md`. |
| **Q14** | Pipeline Robustness | Add Probe Suitability Check, confidence warnings, numeric text handling, and directional vs. invariant flip rate interpretation. | **Resolved** | Refactored `audit.py`, `report_generator.py`, `app.py`, and `test_behavioral.py`. |
| **Q15** | Metrics & XAI Interpretation | Explain Flip Rate & ECE visualization interpretation and token attribution weight computation & shifts. | **Resolved** | Detailed directional vs. invariant flip rate expectations, ECE calibration gap, LIME/SHAP matrix derivation, and token weight shift mechanisms. |
| **Q16** | Future Improvements & Features | What improvements and additional features can be added to the project? | **Resolved** | Categorized roadmap: Expanded Perturbation Probes (typos/NER), Multi-model benchmarking, Counterfactual Data Export, Multi-class support, & HTML token highlighting. |
| **Q17** | Web UI Deprecation | Resolve Streamlit `use_column_width` deprecation warning in dashboard. | **Resolved** | Replaced `use_column_width=True` with standard `use_container_width=True` across all `st.image()` calls in `blindspot/app.py`. |
| **Q18** | Visualizer Graph Bug | Fix taxonomy donut chart text overlapping and zero-width slice glitches. | **Resolved** | Filtered active categories with $>0$ counts and rendered unified green donut ring (`100% Robust`) for zero-failure runs in `visualizer.py`. |
| **Q19** | Codebase Analysis & Learning Guide | Deep architectural analysis, test suite execution, file-by-file guide, and pedagogical learning roadmap. | **Resolved** | Created `CODEBASE_FILE_GUIDE.md`, updated state report, validated 13/13 tests, and provided comprehensive viva defense & honest critique. |
| **Q20** | Diagnostic Visualizations | Deep-dive explanation of all 4 generated figures: importance, significance, mathematical basis, and diagnostic interpretation. | **Resolved** | Detailed breakdown of behavioral_metrics, taxonomy_distribution, attribution_comparison, and probe_alignment_summary charts. |
| **Q21** | Graph Guide Documentation | Create a dedicated `.md` file with complete details, formulas, importance, significance, and concrete case study examples for all 4 figures. | **Resolved** | Created `d:\BlindSpot\DIAGNOSTIC_GRAPHS_GUIDE.md` with complete mathematical derivations, case study on active run, and defense scripts. |





---

## 🔍 Detailed Question & Technical Resolution Log

### Q1: Implementation State Audit based on SRS (`srs.pdf`)
- **Date**: 2026-08-31
- **User Question**: *"itemize the state of the amount of implementation that has been done based on @srs.pdf"*
- **Technical Analysis**:
  - Compared SRS §1 (Objectives), §3 (Environmental & Tech Stack), and §4 (System Analysis & Functional Requirements) against `d:\BlindSpot`.
- **Resolution**:
  - All core functional components (`HuggingFaceWrapper`, `PerturbationEngine`, `BehavioralTester`, `LimeExplainerWrapper`, `ShapExplainerWrapper`, `TaxonomyClassifier`, `ReportGenerator`, `Visualizer`, `AuditPipeline`, Streamlit Dashboard, and `pytest` suite) are **~100% complete**.

---

### Q2: Execution of Audit Pipeline & Tests
- **Date**: 2026-08-31
- **User Question**: *"can you run this?"*
- **Resolution**:
  - Ran `python -m blindspot.cli` and `run_tests.py` in the background. All 13 unit tests passed (`OK`), and diagnostic reports were generated in `audit_reports/`.

---

### Q3: Interactive Web Interface (Streamlit)
- **Date**: 2026-08-31
- **User Question**: *"i want the streamkit user interface"*
- **Resolution**:
  - Launched Streamlit web dashboard (`python -m streamlit run blindspot/app.py`) on port `8501`.
  - Bypassed initial email telemetry prompt and confirmed UI accessibility at `http://localhost:8501`.

---

### Q4: Sample Audit Output for Sentence
- **Date**: 2026-08-31
- **User Question**: *`"I had fun at the festival."` Can you give what the actual output for this sentence would be*
- **Resolution**:
  - Target model prediction: `POSITIVE` (Confidence: 99.98%).
  - Flip rate: **50.00%** (3 of 6 probes flipped label as expected under negation and contrast).
  - ECE: **0.0007**.
  - Total taxonomy failures detected: **0** (Model handled negation and contrast clauses properly).

---

### Q5: Perturbation Engine Formatting & Spacing Bugs
- **Date**: 2026-08-31
- **User Question**: Pointed out specific output formatting errors:
  - `"This is awesome , but..."` (Space before comma)
  - `"This is awesome , however..."` (Space before comma)
  - `"Although this is awesome , it..."` (Space before comma)
  - `"This is not un- awesome"` (Space after hyphen)
  - `"This cost awesome"` (Invalid substitution for "is")
  - `"Although i had fun..."` (Lowercased pronoun "I")
  - `"ane had fun..."` (Obscure NLTK lemma for pronoun "I")
- **Technical Fixes**:
  1. Implemented `_clean_text()` helper using regex `re.sub(r"\s+([,.\!?])", r"\1", text)` to eliminate space before punctuation.
  2. Implemented hyphen prefix cleaner `re.sub(r"\b(un|non|in|im|dis|re)-\s+(\w+)", r"\1-\2", text)`.
  3. Implemented `_format_subject()` helper to preserve upper-case `"I"` pronouns (`"Although I had fun..."`).
  4. Added a `stop_words` filter set to prevent replacing pronouns and structural auxiliary verbs with NLTK WordNet lemmas.

---

### Q6: Validity of "un-awesome" in Double Negation
- **Date**: 2026-08-31
- **User Question**: *"un-awesome isnt a word right?"*
- **Technical Rationale**:
  - `"un-awesome"` is non-standard English in formal dictionaries.
- **Resolution**:
  - Refactored `DoubleNegationPerturber` ([negation.py](file:///d:/BlindSpot/blindspot/perturbations/negation.py)) to generate standard English litotes:
    - `"It is not impossible that this is awesome."`
    - `"It is not untrue that this is awesome."`

---

### Q7: Choice of Rule-Based Perturbation Engine vs. LLMs
- **Date**: 2026-08-31
- **User Question**: *"is a rule based pertubation engine a bad chice for this project?"*
- **Technical Rationale**:
  - **Why Rule-Based is Essential**: Model auditing (like CheckList / AI-Q) requires *strict experimental control* of the independent variable. Generative LLM paraphrasing alters multiple words and tone simultaneously, obscuring root cause analysis. Rule-based execution is also deterministic, lightweight (zero GPU required), and model-agnostic (§SRS 1.1).
  - **Hybrid Engine Solution**: BlindSpot uses a hybrid design—rule-based structural templates combined with NLTK/spaCy POS lookup, stopword filtering, and automated text sanitization.

---

### Q8: Code Request & Execution Verification
- **Date**: 2026-09-07
- **User Question**: *"Run it and provide the code"*
- **Resolution**:
  - Executed audit pipeline inline on `"This is awesome."` (7 probes generated, 42.86% flip rate).
  - Provided full Python source code for `negation.py`, `connectives.py`, `substitution.py`, and `engine.py`.

---

### Q9: PowerShell Execution Script (`run.ps1`)
- **Date**: 2026-09-07
- **User Question**: *"can you create a run.ps1 file yto execute this project?"*
- **Resolution**:
  - Created `d:\BlindSpot\run.ps1` supporting positional and named arguments:
    - `.\run.ps1 cli -Sentence "..."`
    - `.\run.ps1 dashboard`
    - `.\run.ps1 test`
    - `.\run.ps1 docs`

---

### Q10: PowerShell `UnauthorizedAccess` / Script Execution Error
- **Date**: 2026-09-07
- **User Question**: Provided error: *`.\run.ps1 : File D:\BlindSpot\run.ps1 cannot be loaded because running scripts is disabled on this system.`*
- **Resolution**:
  - Explained Windows ExecutionPolicy restrictions and provided 3 workarounds:
    1. Single-command bypass: `powershell -ExecutionPolicy Bypass -File .\run.ps1 dashboard`
    2. User-level execution policy update: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
    3. Direct Python commands (`python -m streamlit run blindspot/app.py`).

---

### Q11: Browser Security & Blocked Markdown Reports
- **Date**: 2026-09-07
- **User Question**: *"why are the md reports blocked?"*
- **Technical Explanation**:
  - Modern web browsers enforce Same-Origin Policies blocking `http://localhost:8501` pages from opening `file:///` local disk links.
- **Resolution**:
  - Updated [blindspot/app.py](file:///d:/BlindSpot/blindspot/app.py) to read `.md` file contents dynamically and display them inside Streamlit expanders (`st.expander()`) with a **`⬇️ Download <report>.md`** button.

---

### Q12: Input Text Validation & Length Constraints
- **Date**: 2026-09-07
- **User Question**: *"validate the input given for specific length, whether it is a valid input or not"*
- **Technical Implementation**:
  - Created `AuditPipeline.validate_input(sentence, min_length=3, max_length=500)` enforcing:
    1. String type validation (`isinstance(sentence, str)`).
    2. Non-empty & non-whitespace check.
    3. Minimum length of 3 characters.
    4. Maximum length of 500 characters.
    5. Meaningful alphabetic text check (`any(c.isalpha() for c in clean_sentence)`).
  - Integrated into Streamlit `app.py` with friendly error banners and added unit tests in `tests/test_behavioral.py`.

---

### Q13: Project Questions & Doubts Tracker File
- **Date**: 2026-09-07
- **User Question**: *"i need you to create md file which tracks all my doubts and questions based on project,update this files whenever i ask questions"*
- **Resolution**:
  - Created `d:\BlindSpot\project_questions_and_doubts.md` to automatically log all user queries, technical rationales, code fixes, and resolution statuses.

---

### Q14: Pipeline Robustness, Probe Suitability, Numeric Handling & Directional Flip Rate Interpretation
- **Date**: 2026-09-07
- **User Request**: Enhance pipeline robustness without changing core architecture or removing existing functionality by implementing:
  1. **Probe Suitability Check**: Distinguish invalid inputs (digits/symbols only), valid but weak/ambiguous inputs (`"the movie"`, `"The movie was normal."` $\rightarrow$ accepted with warning), and suitable inputs (`"The movie was excellent."`).
  2. **Numeric Text Handling**: Allow numbers when occurring alongside alphabetic natural language text (`"The movie was 10/10."`), while rejecting pure numeric strings (`"12345"`).
  3. **No Neutral Class & Low Confidence Warning**: Preserve 2-class Positive/Negative classifier; report confidence warnings when $\text{conf} \le 0.65$ with an explicit note clarifying that weak inputs do not have a 3rd neutral class.
  4. **Directional vs. Invariant Flip Rate Interpretation**: Differentiate directional probes (flip expected) from invariant probes (stability expected); clarify in reports that high flip rate is not automatically good and low flip rate is not automatically bad.
  5. **Streamlit UI Badges**: Display ❌ Invalid Input, ⚠️ Probe Suitability Warning, or ✅ Suitable Probe status banners.
  6. **Unit Tests**: Add 8 comprehensive test cases in `tests/test_behavioral.py`.
- **Implementation Location**:
  - `blindspot/audit.py`: Added `check_suitability()`, `confidence_threshold`, and validation error message formatting.
  - `blindspot/reporting/report_generator.py`: Updated `_build_model_behavior_report()` and `_build_probe_report()` with suitability warnings, ECE explanation, flip rate interpretation guidelines, and structured probe response fields.
  - `blindspot/app.py`: Added UI status banners (❌, ⚠️, ✅).
  - `tests/test_behavioral.py`: Added `test_input_validation_and_suitability()`.
- **Verification**: All 13 unit tests passed in `run_tests.py` (`OK`). Tested 5 specific pipeline examples (`"The movie was excellent."`, `"The movie was normal."`, `"the movie"`, `"12345"`, `"The movie was 10/10."`).

---

### Q15: Flip Rate, ECE Visualization Interpretation & Token Attribution Shift Mechanism
- **Date**: 2026-09-07
- **User Question**: 
  1. *"based on the visualition diagnosis of fliprate and ECE what does the graph convey , how to identify whether it is as excecpted or not?"*
  2. *"also the the token attribution from where the weights of words are coming.and how the weights are changed"*
- **Detailed Technical Resolution**:
  1. **Behavioral Diagnostic Metrics Interpretation**:
     * **Prediction Flip Rate (%)**: Percentage of perturbed inputs that caused the classifier model to change its predicted class label.
       * *Directional Probes (Single Negation)*: Expected Flip Rate is **HIGH (~100%)**. Low flip rate indicates a **Blind Failure** (model ignores "not").
       * *Invariant Probes (Double Negation, Contrast Appends, Synonyms)*: Expected Flip Rate is **LOW (~0%)**. High flip rate indicates a **Misweighted/Fragility Failure**.
     * **Expected Calibration Error (ECE)**: Difference between predicted confidence scores and empirical accuracy across probability bins ($0.0$ to $1.0$).
       * *Expected Behavior*: **LOW ECE (< 5%)**, indicating well-calibrated confidence probabilities. High ECE (> 15%) indicates overconfidence or poor calibration.
  2. **Token Attribution Source & Shift Mechanics**:
     * **Weight Sources**: Calculated dynamically via **LIME** (fitting a local linear regression over masked perturbations), **SHAP** (Shapley game theory coalition values), or **Leave-One-Out (LOO)** probability delta ($\Delta P = P(\text{full}) - P(\text{masked})$).
     * **Weight Shift Mechanics**: Compares word weights in original text vs perturbed text. Quantified via **Top-K Jaccard Similarity** and **Cosine Attribution Vector Alignment**. High cosine alignment during a flip indicates structural failure (spurious feature reliance).

---

### Q16: Project Improvement & Feature Enhancement Roadmap
- **Date**: 2026-09-07
- **User Question**: *"does this project needs any improvements? what are the additional features i can add to this project?"*
- **Detailed Feature Roadmap**:
  1. **Expanded Linguistic Probes**: Add Typographical noise (character swap/typo perturbers), Named Entity (NER) swapping, and Sentiment Adverb scaling.
  2. **Multi-Model Benchmarking**: Add a comparative audit dashboard mode to compare 2+ HuggingFace models side-by-side on identical probes.
  3. **Counterfactual Training Data Export**: Export failed probes as CSV/JSON datasets for data augmentation and fine-tuning.
  4. **Multi-Class Classifier Support**: Extend beyond binary (2-class) sentiment classification to 5-star, multi-class, and multi-label text classifiers.
  5. **Interactive HTML Token Highlighting**: Render color-coded word importance overlays directly in Streamlit UI.

---

### Q17: Streamlit `use_column_width` Deprecation Warning Resolution
- **Date**: 2026-09-07
- **User Question**: *"The use_column_width parameter has been deprecated and will be removed in a future release. Please utilize the width parameter instead. this message is shown in the web . deal it"*
- **Technical Explanation & Resolution**:
  - In recent Streamlit releases (v1.35+), the `use_column_width` parameter in `st.image()` was deprecated in favor of `use_container_width=True` or explicit `width` bounds.
  - Replaced all 4 instances of `use_column_width=True` with `use_container_width=True` in [blindspot/app.py](file:///d:/BlindSpot/blindspot/app.py).
  - Streamlit dashboard automatically reloads and eliminates the warning banner.

---

### Q18: Taxonomy Donut Chart Glitch & Text Overlap Resolution
- **Date**: 2026-09-07
- **User Question**: *"sometimes there is a glitch in the taxonomy donut graph. fix it"*
- **Technical Root Cause & Fix**:
  - *Root Cause 1*: When some failure categories had $0$ count, the visualizer assigned a dummy value `0.001`, causing Matplotlib to render microscopic zero-width slice lines with overlapping label text and `0` autotext values jammed together.
  - *Root Cause 2*: When no failures occurred ($0$ total failures), the donut was split into 3 redundant green slices labeled `"No Blind Failures"`, `"No Spurious Failures"`, and `"No Misweighted Failures"`, creating text collision.
  - *Resolution*: Updated `plot_taxonomy_distribution()` in [visualizer.py](file:///d:/BlindSpot/blindspot/reporting/visualizer.py):
    1. Filtered active slices so only categories with count $> 0$ are rendered in the pie chart.
    2. Rendered a unified, solid green donut ring (`"0 Failures Detected"`, center text `"100% Robust"`) when total failures equals $0$.
    3. Displayed the total failure count (`Total N`) in the donut center for non-zero failure runs.

---

### Q19: Complete Codebase Analysis, Test Verification & Comprehensive File-by-File Study Guide
- **Date**: 2026-09-07
- **User Request**: *"I need you to analyse the project, test it and study it. I was going to study the project from start and I need you to guide me through it and learn me. Check and update md files if needed. Create an md file that tells what each file does in detail. Also provide your honest openion. DO NOT EDIT CODE"*
- **Technical Analysis & Verification**:
  1. **Test Suite Execution**: Executed `python run_tests.py` verifying all 13 unit tests pass (`OK`) in 131.3s across all test modules (behavioral, explainability, models, perturbations, reporting, visualizer).
  2. **Pipeline End-to-End Execution**: Verified CLI execution on `"This is an incredible movie."` generating 7 probes (42.86% flip rate, 0 failures, 4 markdown reports, and 4 PNG figures).
  3. **File Guide Creation**: Authored [CODEBASE_FILE_GUIDE.md](file:///d:/BlindSpot/CODEBASE_FILE_GUIDE.md) detailing every single file in the repository (role, classes, methods, inputs/outputs, dependencies, fallbacks, and execution trace).
  4. **State Report Synchronization**: Updated [PROJECT_STATE_REPORT.md](file:///d:/BlindSpot/PROJECT_STATE_REPORT.md) Section 6 to track questions Q1 through Q19.
  5. **Academic & Architectural Critique**: Provided honest appraisal of framework strengths, real-world limitations, and preparation tips for academic evaluation/defense.

---

### Q20: Deep-Dive Analysis of the 4 Diagnostic Figures: Significance & Importance
- **Date**: 2026-09-07
- **User Question**: *"i need you to explain all my 4 figures and the importaance of each one and what they signify"*
- **Technical Analysis & Interpretation**:
  1. **Figure 1 (`behavioral_metrics.png`)**: Measures holistic behavioral sensitivity (Prediction Flip Rate %) and probabilistic honesty/calibration (ECE $\times$ 100). Essential for checking whether the model overreacts or underreacts, and whether its confidence is well-calibrated.
  2. **Figure 2 (`taxonomy_distribution.png`)**: Donut chart categorizing failure root causes into **Blind** (ignored negation), **Spurious** (noun reliance), and **Misweighted** (modifier skew), or rendering a unified solid green donut (`100% Robust`) on zero-failure runs. Crucial for direct, actionable ML fine-tuning recommendations.
  3. **Figure 3 (`attribution_comparison.png`)**: Grouped bar chart comparing local token weights (LIME/SHAP) between the original sentence and Probe #1 (negation insertion). Explains the exact *internal reasoning mechanism* driving prediction flips (e.g. `not` commanding strong negative weight like $-0.8633$).
  4. **Figure 4 (`probe_alignment_summary.png`)**: Dual grouped bar chart evaluating explanation consistency (Jaccard Top-K feature overlap and Cosine vector alignment) across all probes ($P_1 \dots P_7$). Verifies whether model reasoning remains semantically stable across linguistic transformations.

---

### Q21: Dedicated Diagnostic Figures Documentation Artifact (`DIAGNOSTIC_GRAPHS_GUIDE.md`)
- **Date**: 2026-09-08
- **User Question**: *"Create an .md file saying all the details that you currently said about the graphs. It should have all details, importance, significance etc with an example"*
- **Technical Implementation & Artifact**:
  - Authored comprehensive standalone reference document [DIAGNOSTIC_GRAPHS_GUIDE.md](file:///d:/BlindSpot/DIAGNOSTIC_GRAPHS_GUIDE.md).
  - Documented complete architectural anatomy, colors, axes, and visual layouts for all 4 figures.
  - Included rigorous mathematical formulas: Prediction Flip Rate, 10-bin ECE summation, LIME surrogate loss, SHAP Shapley values, Top-K Jaccard set overlap, and Cosine vector angle.
  - Provided complete real-world case study based on the active run (`"she was playing football really well."` with DistilBERT), tracking the exact quantitative metrics: Flip Rate $42.9\%$, ECE $2.6\%$, 1 Misweighted failure, Probe #1 `not` weight $-0.8633$, and Probes $P_1-P_7$ Jaccard/Cosine metrics.
  - Included a 4-part Viva & Presentation Defense Script tailored for academic evaluation.

