# BlindSpot: Complete Project State & Architectural Specification Report

**Project Title**: BlindSpot: A Behavioral and Explainable-AI Framework for Auditing Text Classifiers  
**Author**: Ziya Fathima M P (TCR25MCA-2060)  
**Institution**: Department of Computer Applications, Government Engineering College, Thrissur  
**Repository Path**: `d:\BlindSpot`  
**Completion Status**: **100% Fully Implemented & Verified**  
**Date**: September 2026  

---

## 1. Executive Summary

**BlindSpot** is a lightweight, model-agnostic auditing framework designed to stress-test black-box text classification models (such as Hugging Face Transformers) without requiring model retraining, architecture modification, or access to internal gradients. 

Operating on a strict **"pretrained model in, diagnostic report out"** principle, BlindSpot combines:
1. **Controlled Linguistic Perturbations**: Synthesizing negation, litotes double negation, contrastive connectives, and synonym substitutions.
2. **Behavioral Metric Testing**: Quantifying prediction flip rates, confidence shifts, and Expected Calibration Error (ECE).
3. **Explainable AI (XAI) Attribution**: Extracting local token attributions using LIME and SHAP before and after perturbations, measuring Top-K Jaccard similarity and Cosine attribution vector alignment.
4. **3-Way Failure Taxonomy Classification**: Automatically categorizing model failures into **Blind** (ignored negation), **Spurious** (noun over-reliance), and **Misweighted** (skewed modifier weights).
5. **Automated Diagnostic Reporting & Visualization**: Generating structured Markdown reports (`model_behavior_report.md`, `failure_summary.md`, `explanation_comparison.md`, `probes/*.md`) and publication-grade Matplotlib charts.

---

## 2. SRS Compliance Matrix

The implementation has been benchmarked against the Software Requirements Specification ([srs.pdf](file:///d:/BlindSpot/srs.pdf)):

| SRS Section | Feature / Requirement | Implementation Location | Compliance | Details |
| :--- | :--- | :--- | :---: | :--- |
| **§1.1, §4.4** | **Black-Box Model-Agnostic Auditing** | [blindspot/audit.py](file:///d:/BlindSpot/blindspot/audit.py) | **100%** | Operates on pretrained Hugging Face models via standardized probability vectors. |
| **§3.1, §3.2** | **Technology Stack** | Core codebase | **100%** | Python 3.11+, Transformers, PyTorch, NLTK WordNet, spaCy, LIME, SHAP, pandas, NumPy, Matplotlib, Streamlit, pytest, MkDocs. |
| **§4.6.1** | **User Interface & Input Validation** | [app.py](file:///d:/BlindSpot/blindspot/app.py), [cli.py](file:///d:/BlindSpot/blindspot/cli.py) | **100%** | Interactive Streamlit dashboard (`http://localhost:8501`) and CLI. Input validation enforces string type, non-emptiness, length limits (3–500 chars), and text validity. |
| **§4.6.2** | **Perturbation Generation** | [blindspot/perturbations/](file:///d:/BlindSpot/blindspot/perturbations) | **100%** | Generates Single Negation, Litotes Double Negation (`"It is not untrue that..."`), Contrast Appends/Prefixes, and Synonym Substitutions with stopword filtering. |
| **§4.6.3** | **Behavioral Testing & Metrics** | [blindspot/testing/](file:///d:/BlindSpot/blindspot/testing) | **100%** | Evaluates original vs. perturbed inputs, computing prediction flip rates and Expected Calibration Error (ECE). |
| **§4.6.4** | **Explainability & Alignment** | [blindspot/explainability/](file:///d:/BlindSpot/blindspot/explainability) | **100%** | Extracts LIME and SHAP token attributions, computing Jaccard Top-K similarity and Cosine attribution alignment. |
| **§4.6.5** | **Automated Report Generation** | [blindspot/reporting/](file:///d:/BlindSpot/blindspot/reporting) | **100%** | Generates all 4 required Markdown reports and 4 Matplotlib PNG charts in `audit_reports/`. |
| **§4.6.5** | **3-Way Failure Taxonomy** | [taxonomy.py](file:///d:/BlindSpot/blindspot/explainability/taxonomy.py) | **100%** | Classifies model failures into **Blind**, **Spurious**, and **Misweighted** categories with actionable recommendations. |
| **§4.7** | **Non-Functional Requirements** | Package architecture | **100%** | High performance, modular maintainability, offline fallbacks, and zero-crash reliability. |

---

## 3. Directory & Package File Mapping

```text
d:\BlindSpot\
├── PROJECT_STATE_REPORT.md             # Complete Architectural & State Specification (This File)
├── CODEBASE_FILE_GUIDE.md              # Detailed File-by-File Technical Guide & Reference
├── DIAGNOSTIC_GRAPHS_GUIDE.md          # Comprehensive Guide to the 4 Diagnostic Visualizations
├── project_questions_and_doubts.md     # Persistent Q&A & Technical Doubts Log (Q1–Q21)
├── IMPLEMENTATION_STEPS.md             # Implementation Roadmap Reference
├── run.ps1                             # PowerShell Execution Launcher Script
├── requirements.txt                    # Python Dependencies Manifest
├── setup.py                            # Package Setup Script
├── run_tests.py                        # Standalone Test Suite Runner
├── mkdocs.yml                          # MkDocs Site Configuration
├── srs.pdf                             # Software Requirements Specification
│
├── blindspot/                          # Main Package Core
│   ├── __init__.py                     # Package Initialization & Exports
│   ├── audit.py                        # AuditPipeline Main Orchestrator & Input Validation
│   ├── cli.py                          # Command Line Launcher
│   ├── app.py                          # Streamlit Web App (Interactive Dashboard & Report Viewer)
│   ├── models/
│   │   ├── __init__.py
│   │   └── huggingface_wrapper.py      # HF Classification Wrapper + Offline Heuristic Fallback
│   ├── perturbations/
│   │   ├── __init__.py
│   │   ├── base.py                     # BasePerturber Abstract Class
│   │   ├── negation.py                 # Single Negation & Litotes Double Negation Perturbers
│   │   ├── connectives.py              # Contrastive Connective Append & Concession Perturbers
│   │   ├── substitution.py             # Synonym Substitution with Stopword/Pronoun Filtering
│   │   └── engine.py                   # PerturbationEngine Aggregator
│   ├── testing/
│   │   ├── __init__.py
│   │   ├── behavioral.py               # Behavioral Probe Runner & Confidence Tracker
│   │   └── metrics.py                  # Flip Rate & ECE Binning Metrics
│   ├── explainability/
│   │   ├── __init__.py
│   │   ├── lime_explainer.py           # LIME Token Attribution Extractor + LOO Fallback
│   │   ├── shap_explainer.py           # SHAP Token Attribution Extractor + LOO Fallback
│   │   ├── alignment.py                # Jaccard Top-K & Cosine Attribution Vector Alignment
│   │   └── taxonomy.py                 # 3-Way SRS Failure Taxonomy Classifier
│   └── reporting/
│       ├── __init__.py
│       ├── report_generator.py         # Automated Markdown Report Compiler
│       └── visualizer.py               # Matplotlib Diagnostic Graph Generator
│
├── audit_reports/                      # Diagnostic Output Reports & Figures
│   ├── model_behavior_report.md        # Executive Behavior Audit Summary
│   ├── failure_summary.md              # Detailed Breakdown of Failure Instances
│   ├── explanation_comparison.md       # Token Attribution Shifts & Alignment Scores
│   ├── figures/                        # Matplotlib Diagnostic Charts
│   │   ├── behavioral_metrics.png
│   │   ├── taxonomy_distribution.png
│   │   ├── attribution_comparison.png
│   │   └── probe_alignment_summary.png
│   └── probes/                         # Detailed Per-Probe Diagnostic Logs
│       ├── probe_1.md ... probe_7.md
│
├── tests/                              # Automated Pytest Suite (100% Passing)
│   ├── test_perturbations.py
│   ├── test_models.py
│   ├── test_behavioral.py
│   ├── test_explainability.py
│   ├── test_reports.py
│   └── test_visualizer.py
│
└── docs/                               # MkDocs Technical Documentation Source
    ├── index.md                        # Framework Overview
    ├── architecture.md                 # System Pipeline Architecture
    ├── taxonomy.md                     # Failure Taxonomy Guide
    ├── usage.md                        # CLI & Web App User Guide
    └── api.md                          # Python API Reference
```

---

## 4. Core System Components Detailed

### 4.1 Black-Box Model Wrapper ([huggingface_wrapper.py](file:///d:/BlindSpot/blindspot/models/huggingface_wrapper.py))
- **Role**: Wraps Hugging Face text classification pipelines.
- **Key Method**: `predict_proba(texts: Union[str, List[str]]) -> np.ndarray` returning shape `(N, num_classes)` with sum-to-1 probability normalization.
- **Reliability Fallback**: Includes a heuristic keyword-probability fallback classifier if offline or if Hugging Face downloads fail.

### 4.2 Perturbation Engine Suite ([blindspot/perturbations/](file:///d:/BlindSpot/blindspot/perturbations))
- **`NegationPerturber`**: Inserts "not" after auxiliary verbs (`is`, `was`, `are`, `can`, `has`) or applies explicit negation framing (`"It is not true that..."`).
- **`DoubleNegationPerturber`**: Generates natural English double-negation litotes (`"It is not impossible that..."`, `"It is not untrue that..."`).
- **`ConnectivePerturber`**: Appends positive contrast (`", but the overall experience was outstanding."`), negative contrast (`", however the service was complete garbage."`), or concession prefixes (`"Although..."`).
- **`SynonymSubstitutionPerturber`**: Uses NLTK WordNet and curated dictionaries to replace key sentiment/content words while ignoring pronouns (`I`, `this`, `it`) and structural stopwords. Preserves original capitalization (`"Awesome"` $\rightarrow$ `"Impressive"`).
- **`_clean_text()`**: Regex post-processor eliminating space before punctuation (`"awesome ,"` $\rightarrow$ `"awesome,"`) and space after prefix hyphens (`"un- awesome"` $\rightarrow$ `"un-awesome"`).

### 4.3 Behavioral Testing & Calibration ([blindspot/testing/](file:///d:/BlindSpot/blindspot/testing))
- **`BehavioralTester`**: Evaluates original and perturbed probe sentences, tracking prediction outcomes, confidence shifts ($\Delta_{\text{conf}}$), label flip flags, and unexpected behavior flags.
- **`compute_flip_rate()`**: Calculates the percentage of probes that flipped prediction relative to the original text.
- **`compute_ece()`**: Computes Expected Calibration Error (ECE) using 10 probability confidence bins:
  $$\text{ECE} = \sum_{b=1}^{10} \frac{|B_b|}{N} |\text{accuracy}(B_b) - \text{confidence}(B_b)|$$

### 4.4 Explainability & Alignment ([blindspot/explainability/](file:///d:/BlindSpot/blindspot/explainability))
- **`LimeExplainerWrapper` & `ShapExplainerWrapper`**: Extract local token feature attributions for original and perturbed sentences. Includes Leave-One-Out (LOO) importance estimation as a fallback.
- **`compute_jaccard_similarity()`**: Computes set overlap of Top-K attribution tokens:
  $$\text{Jaccard} = \frac{|S_{\text{orig}} \cap S_{\text{pert}}|}{|S_{\text{orig}} \cup S_{\text{pert}}|}$$
- **`compute_attribution_cosine()`**: Computes Cosine similarity of attribution vectors across common vocabulary words:
  $$\text{Cosine} = \frac{\vec{v}_1 \cdot \vec{v}_2}{\|\vec{v}_1\| \|\vec{v}_2\|}$$

### 4.5 3-Way SRS Failure Taxonomy Classifier ([taxonomy.py](file:///d:/BlindSpot/blindspot/explainability/taxonomy.py))
- **`Blind`**: Detected when negation operators (`not`, `never`, `n't`) fail to flip the model's prediction outcome.
- **`Spurious`**: Detected when feature attributions are concentrated on generic domain/entity nouns (`movie`, `food`, `festival`) rather than sentiment modifiers.
- **`Misweighted`**: Detected when the model misallocates relative token weights across contrastive clauses (`X, but Y`) or synonym substitutions.
- Provides actionable remediation recommendations for each failure type (e.g. fine-tuning on CheckList negation templates or applying adversarial entity replacement).

### 4.6 Automated Reporting & Visualizations ([blindspot/reporting/](file:///d:/BlindSpot/blindspot/reporting))
- **`ReportGenerator`**: Generates all 4 SRS required Markdown reports:
  1. `model_behavior_report.md`
  2. `failure_summary.md`
  3. `explanation_comparison.md`
  4. `probes/probe_<id>.md`
- **`Visualizer`**: Generates 4 publication-grade Matplotlib charts saved in `audit_reports/figures/`:
  1. `behavioral_metrics.png` (Flip Rate % & ECE x100)
  2. `taxonomy_distribution.png` (Blind, Spurious, Misweighted Donut Chart)
  3. `attribution_comparison.png` (Original vs. Perturbed Token Attributions)
  4. `probe_alignment_summary.png` (Jaccard & Cosine Alignment across probes)

### 4.7 Input Validation Engine ([blindspot/audit.py](file:///d:/BlindSpot/blindspot/audit.py#L57-L79))
Enforces strict pre-audit input sanitization:
1. **Type Check**: Must be a `str`.
2. **Emptiness Check**: Rejects empty or whitespace-only inputs.
3. **Minimum Length**: Minimum **3 characters**.
4. **Maximum Length**: Maximum **500 characters**.
5. **Text Validity**: Requires at least one alphabetic word character.

---

## 5. Diagnostic Visualizations Explained in Detail

1. **`behavioral_metrics.png`**:
   - **Horizontal Bar Chart**: Displays Prediction Flip Rate (%) and ECE (x100).
   - High flip rates under directional perturbations (negation/contrast) show sensitivity to meaning changes. Low ECE indicates calibrated model confidence.
2. **`taxonomy_distribution.png`**:
   - **Donut Chart**: Shows the proportion of Blind (Red), Spurious (Orange), and Misweighted (Purple) failure categories detected during the audit.
3. **`attribution_comparison.png`**:
   - **Side-by-Side Bar Chart**: Compares local token attributions for Probe #1 (Original Blue vs. Perturbed Red). Positive values ($>0$) push predictions positive; negative values ($<0$) push predictions negative.
4. **`probe_alignment_summary.png`**:
   - **Dual Bar Chart**: Compares Jaccard Top-K Similarity (Purple) and Cosine Attribution Alignment (Teal) across all probes ($P_1 \dots P_7$) on a scale from $0.0$ to $1.0$.

---

## 6. Project Questions & Doubts Tracker (Summary of Q1–Q21)

All user queries, design decisions, and bug resolutions are tracked in [project_questions_and_doubts.md](file:///d:/BlindSpot/project_questions_and_doubts.md):

- **Q1–Q4**: Verified ~100% SRS compliance, executed CLI/tests, launched Streamlit UI (`http://localhost:8501`), and validated outputs for sample sentences (`"I had fun at the festival."`).
- **Q5**: Refactored perturbation formatting (spacing before commas, hyphens, pronoun case preservation).
- **Q6**: Replaced non-standard `"un-awesome"` with standard litotes (`"It is not untrue that..."`).
- **Q7**: Documented scientific rationale for Rule-Based + NLP Heuristic Hybrid engines in model auditing.
- **Q8**: Re-tested pipeline inline and provided full Python source code for perturbation modules.
- **Q9–Q10**: Created `run.ps1` PowerShell script and provided `-ExecutionPolicy Bypass` workarounds.
- **Q11**: Solved browser Same-Origin Policy `file:///` blocking by rendering Markdown reports directly inside Streamlit expanders with download buttons.
- **Q12**: Implemented `validate_input()` enforcing 3–500 char length limits, non-emptiness, and alphabetic validity.
- **Q13**: Created persistent Q&A tracking document `project_questions_and_doubts.md`.
- **Q14**: Implemented Probe Suitability Check, low-confidence prediction warnings, numeric text preservation, and directional vs invariant flip rate metrics.
- **Q15**: Documented mathematical interpretation of Flip Rate, ECE calibration gap, LIME/SHAP attribution derivations, and token weight shift mechanisms.
- **Q16**: Outlined comprehensive future improvement roadmap (typo probes, multi-model benchmarking, counterfactual data export).
- **Q17**: Resolved Streamlit `use_column_width` deprecation warning by adopting `use_container_width=True`.
- **Q18**: Resolved visualizer taxonomy donut chart glitch, zero-slice overlapping, and rendered unified green donut (`100% Robust`) for zero-failure audits.
- **Q19**: Conducted end-to-end test verification (13/13 passing in 131s), authored exhaustive [CODEBASE_FILE_GUIDE.md](file:///d:/BlindSpot/CODEBASE_FILE_GUIDE.md), and compiled learning roadmap & honest architectural review.
- **Q20**: Detailed architectural breakdown of all 4 diagnostic figures (`behavioral_metrics.png`, `taxonomy_distribution.png`, `attribution_comparison.png`, `probe_alignment_summary.png`), their mathematical basis, and viva interpretation.
- **Q21**: Authored dedicated comprehensive visualization reference guide [DIAGNOSTIC_GRAPHS_GUIDE.md](file:///d:/BlindSpot/DIAGNOSTIC_GRAPHS_GUIDE.md) detailing complete visual layouts, formulas, interpretations, and practical case studies.

---

## 7. How to Execute & Verify the Project

### Option A: Using PowerShell Script (`run.ps1`)
```powershell
# 1. Run Audit CLI
powershell -ExecutionPolicy Bypass -File .\run.ps1 cli -Sentence "This is awesome."

# 2. Launch Streamlit Web Dashboard
powershell -ExecutionPolicy Bypass -File .\run.ps1 dashboard

# 3. Run Pytest Verification Suite
powershell -ExecutionPolicy Bypass -File .\run.ps1 test

# 4. Serve Documentation Site
powershell -ExecutionPolicy Bypass -File .\run.ps1 docs
```

### Option B: Direct Python Execution
```powershell
# 1. Audit CLI
python -m blindspot.cli --sentence "This is awesome."

# 2. Web Dashboard (Access at http://localhost:8501)
python -m streamlit run blindspot/app.py

# 3. Automated Test Suite (13 tests passing)
python run_tests.py
```
