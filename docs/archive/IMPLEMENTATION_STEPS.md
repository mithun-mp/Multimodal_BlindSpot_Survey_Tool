# BlindSpot: Step-by-Step Implementation Guide

This document records the comprehensive step-by-step implementation roadmap, software dependencies, file architecture, test suite design, and execution guidelines for **BlindSpot: A Behavioral and Explainable-AI Framework for Auditing Text Classifiers** as specified in the SRS report ([srs.pdf](file:///d:/BlindSpot/srs.pdf)).

---

## 1. Project Overview & Core Objectives

**BlindSpot** is a lightweight, model-agnostic auditing framework for black-box text classification models (such as Hugging Face Transformers). It operates on a strict **"pretrained model in, diagnostic report out"** principle:

- **Model-Agnostic Auditing**: Evaluates pretrained classifiers without retraining, model modifications, or internal gradient access.
- **Controlled Linguistic Perturbations**: Generates single negation, double negation, contrastive connectives (`however`, `but`), and synonym substitutions.
- **Behavioral Metric Evaluation**: Measures prediction flip rates, confidence shifts, and Expected Calibration Error (ECE).
- **Explainability (XAI) Analysis**: Extracts local token attributions using LIME and SHAP before and after perturbations, calculating attribution shifts and alignment scores.
- **Failure Taxonomy Classification**: Automatically classifies model failures into a three-way taxonomy:
  1. **Blind**: Model fails to recognize negation operators.
  2. **Spurious**: Model relies heavily on entity/domain nouns or irrelevant cues.
  3. **Misweighted**: Model misallocates feature weights across modifiers or contrast clauses.
- **Automated Report Generation**: Output structured Markdown behavior reports (`model_behavior_report.md`, `failure_summary.md`, `explanation_comparison.md`, `probes/*.md`).

---

## 2. Environment Setup & Prerequisites

### System Configuration
- **Operating System**: Windows 10/11, Ubuntu 22.04 LTS, or macOS
- **Python Version**: Python 3.11+

### Software Dependencies (`requirements.txt`)
```text
transformers>=4.30.0
torch>=2.0.0
huggingface_hub
spacy>=3.5.0
nltk>=3.8.1
lime>=0.2.0.1
shap>=0.42.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.2.0
matplotlib>=3.7.0
pytest>=7.3.0
pytest-cov>=4.1.0
mkdocs>=1.4.0
mkdocs-material>=9.1.0
streamlit>=1.24.0
```

---

## 3. Comprehensive Implementation Steps

### Phase 1: Environment & Workspace Scaffolding
1. Initialize the project directory `d:\BlindSpot`.
2. Create `requirements.txt`, `setup.py`, and `mkdocs.yml`.
3. Create the modular package structure:
   - `blindspot/models/`
   - `blindspot/perturbations/`
   - `blindspot/testing/`
   - `blindspot/explainability/`
   - `blindspot/reporting/`
   - `tests/`
   - `docs/`

### Phase 2: Black-Box Classifier Interface & Perturbation Engines
1. **Model Wrapper** ([huggingface_wrapper.py](file:///d:/BlindSpot/blindspot/models/huggingface_wrapper.py)):
   - Implement `HuggingFaceWrapper` wrapping Hugging Face pipelines with standardized `predict_proba(texts)` returning NumPy probability matrices `[N, num_classes]`.
   - Include heuristic fallback classifier for offline/lightweight execution.
2. **Base Perturber** ([base.py](file:///d:/BlindSpot/blindspot/perturbations/base.py)):
   - Define abstract `BasePerturber` interface returning original, perturbed text, type, and description.
3. **Negation & Double Negation Perturbers** ([negation.py](file:///d:/BlindSpot/blindspot/perturbations/negation.py)):
   - Single Negation: Inserts "not" after auxiliary verbs or prefixes negation frames.
   - Double Negation: Converts negation to double negative forms ("not impossible", "not un-").
4. **Contrastive Connective Perturber** ([connectives.py](file:///d:/BlindSpot/blindspot/perturbations/connectives.py)):
   - Inserts contrastive clauses ("but the overall experience was outstanding", "however the service was complete garbage").
5. **Synonym Substitution Perturber** ([substitution.py](file:///d:/BlindSpot/blindspot/perturbations/substitution.py)):
   - Swaps adjectives/verbs with synonyms using NLTK WordNet and spaCy parsing with fallback mapping tables.
6. **Perturbation Aggregator** ([engine.py](file:///d:/BlindSpot/blindspot/perturbations/engine.py)):
   - Combines all perturbers in `PerturbationEngine`.

### Phase 3: Behavioral Testing & Metric Calculation
1. **Metrics Calculation** ([metrics.py](file:///d:/BlindSpot/blindspot/testing/metrics.py)):
   - Implement prediction flip rate calculation.
   - Implement Expected Calibration Error (ECE) metric binning formula:
     $$\text{ECE} = \sum_{b=1}^B \frac{|B_b|}{N} |\text{acc}(B_b) - \text{conf}(B_b)|$$
2. **Behavioral Tester Engine** ([behavioral.py](file:///d:/BlindSpot/blindspot/testing/behavioral.py)):
   - Evaluates probes, tracks prediction flips, confidence deltas, and compares actual behavior against expected flip flags.

### Phase 4: Explainability (XAI) & 3-Way Taxonomy Classifier
1. **LIME & SHAP Explainer Wrappers** ([lime_explainer.py](file:///d:/BlindSpot/blindspot/explainability/lime_explainer.py), [shap_explainer.py](file:///d:/BlindSpot/blindspot/explainability/shap_explainer.py)):
   - Extract local token attributions for original and perturbed inputs.
2. **Explanation Alignment** ([alignment.py](file:///d:/BlindSpot/blindspot/explainability/alignment.py)):
   - Calculate Jaccard similarity of top-K attribution tokens.
   - Calculate Cosine attribution vector alignment across common vocabulary.
3. **Taxonomy Classifier** ([taxonomy.py](file:///d:/BlindSpot/blindspot/explainability/taxonomy.py)):
   - Classify model failures into **Blind** (ignored negation), **Spurious** (relied on generic nouns), and **Misweighted** (skewed modifier weights).

### Phase 5: Automated Markdown Report Generator
1. Implement `ReportGenerator` ([report_generator.py](file:///d:/BlindSpot/blindspot/reporting/report_generator.py)):
   - `model_behavior_report.md`: High-level summary of model performance, flip rate, ECE, taxonomy distribution, and recommendations.
   - `failure_summary.md`: Detailed breakdown of detected failure instances.
   - `explanation_comparison.md`: Token-level attribution shifts and alignment scores.
   - `probes/probe_<id>.md`: Per-probe detailed diagnostic logs.

### Phase 6: Orchestrator, CLI & Web Dashboard
1. Implement `AuditPipeline` ([audit.py](file:///d:/BlindSpot/blindspot/audit.py)) connecting model, perturbations, testing, XAI, taxonomy, and reporting.
2. Implement CLI launcher ([cli.py](file:///d:/BlindSpot/blindspot/cli.py)).
3. Implement Streamlit web app ([app.py](file:///d:/BlindSpot/blindspot/app.py)).

### Phase 7: Verification & Test Suite
1. Build `pytest` test suite in `tests/`:
   - `test_perturbations.py`: Unit tests for perturbation engines.
   - `test_models.py`: Unit tests for classifier wrapper.
   - `test_behavioral.py`: Unit tests for flip rates & ECE metrics.
   - `test_explainability.py`: Unit tests for LIME/SHAP and taxonomy classifier.
   - `test_reports.py`: Integration tests for Markdown report generation.
2. Execute automated test suites (`python -m pytest -v`).

---

## 4. Directory & File Mapping

```
d:\BlindSpot\
├── IMPLEMENTATION_STEPS.md          # Implementation Reference Guide (This Document)
├── requirements.txt                 # Dependencies
├── setup.py                         # Package Setup
├── mkdocs.yml                       # MkDocs Site Configuration
├── run_tests.py                     # Standalone Test Runner
├── blindspot/
│   ├── __init__.py
│   ├── audit.py                     # AuditPipeline Main Orchestrator
│   ├── cli.py                       # CLI Launcher
│   ├── app.py                       # Streamlit Web App
│   ├── models/
│   │   ├── __init__.py
│   │   └── huggingface_wrapper.py   # HF Black-Box Wrapper
│   ├── perturbations/
│   │   ├── __init__.py
│   │   ├── base.py                  # BasePerturber Interface
│   │   ├── negation.py              # Negation Engines
│   │   ├── connectives.py           # Contrast Connective Engine
│   │   ├── substitution.py          # Synonym Substitution Engine
│   │   └── engine.py                # PerturbationEngine Aggregator
│   ├── testing/
│   │   ├── __init__.py
│   │   ├── behavioral.py            # Behavioral Probe Runner
│   │   └── metrics.py               # ECE & Flip Rate Metrics
│   ├── explainability/
│   │   ├── __init__.py
│   │   ├── lime_explainer.py        # LIME Wrapper
│   │   ├── shap_explainer.py        # SHAP Wrapper
│   │   ├── alignment.py             # Jaccard & Cosine Alignment
│   │   └── taxonomy.py              # Blind/Spurious/Misweighted Classifier
│   └── reporting/
│       ├── __init__.py
│       └── report_generator.py      # SRS Markdown Report Generator
├── audit_reports/                   # Generated Output Reports
│   ├── model_behavior_report.md
│   ├── failure_summary.md
│   ├── explanation_comparison.md
│   └── probes/
├── tests/                           # Pytest Test Suites
│   ├── test_perturbations.py
│   ├── test_models.py
│   ├── test_behavioral.py
│   ├── test_explainability.py
│   └── test_reports.py
└── docs/
    └── index.md                     # Documentation Homepage
```

---

## 5. Execution Commands

### Run Audit via Command Line (CLI)
```powershell
python -m blindspot.cli --model "distilbert-base-uncased-finetuned-sst-2-english" --sentence "The food was delicious and the service was amazing."
```

### Run Full Test Suite
```powershell
python -m pytest -v
```
or
```powershell
python run_tests.py
```

### Launch Interactive Web Dashboard (Streamlit)
```powershell
streamlit run blindspot/app.py
```
