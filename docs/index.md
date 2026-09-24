# BlindSpot: A Behavioral and Explainable-AI Framework for Auditing Text Classifiers

Welcome to the official technical documentation for **BlindSpot**.

`BlindSpot` is a lightweight, model-agnostic auditing framework for black-box text classification models (such as Hugging Face Transformers). It operates on a strict **"pretrained model in, diagnostic report out"** principle:

- **Model-Agnostic Auditing**: Evaluates pretrained classifiers without requiring retraining, model architecture modifications, or access to internal gradients.
- **Controlled Linguistic Perturbations**: Generates single negation, double negation, contrastive connectives (`however`, `but`), and synonym substitutions.
- **Behavioral Metric Evaluation**: Measures prediction flip rates, confidence shifts, and Expected Calibration Error (ECE).
- **Explainability (XAI) Analysis**: Extracts local token attributions using LIME and SHAP before and after perturbations, calculating attribution shifts and alignment scores.
- **Failure Taxonomy Classification**: Automatically classifies model failures into a three-way taxonomy: **Blind**, **Spurious**, and **Misweighted**.
- **Automated Report Generation**: Outputs structured Markdown behavior reports (`model_behavior_report.md`, `failure_summary.md`, `explanation_comparison.md`, `probes/*.md`) along with Matplotlib visual chart assets.

---

## Quick Start

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/user/BlindSpot.git
cd BlindSpot
pip install -r requirements.txt
```

### Run an Audit via CLI

To audit a pretrained Hugging Face model on a single input sentence:

```bash
python -m blindspot.cli --model "distilbert-base-uncased-finetuned-sst-2-english" --sentence "The food was delicious and the service was top notch."
```

### Launch Interactive Web Dashboard

To launch the Streamlit web dashboard:

```bash
streamlit run blindspot/app.py
```

---

## Core Audit Workflow

```
[Input Sentence + Model ID]
            │
            ▼
┌───────────────────────────┐
│ Perturbation Generation   │ (Negation, Connectives, Substitution)
└─────────────┬─────────────┘
            │
            ▼
┌───────────────────────────┐
│   Behavioral Testing      │ (Flip Rate, Confidence, ECE)
└─────────────┬─────────────┘
            │
            ▼
┌───────────────────────────┐
│ Explainability Extraction │ (LIME & SHAP Attributions, Alignment)
└─────────────┬─────────────┘
            │
            ▼
┌───────────────────────────┐
│ Taxonomy Classification   │ (Blind, Spurious, Misweighted)
└─────────────┬─────────────┘
            │
            ▼
┌───────────────────────────┐
│ Diagnostic Report Build   │ (Markdown Reports + Matplotlib Graphs)
└───────────────────────────┘
```
