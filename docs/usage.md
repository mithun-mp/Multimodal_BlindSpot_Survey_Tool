# User & Developer Guide

This guide covers how to execute audits, run test suites, and configure **BlindSpot**.

---

## 1. CLI Usage

Run audits directly from the command line using `blindspot.cli`:

```bash
python -m blindspot.cli --model <HF_MODEL_NAME_OR_PATH> --sentence <INPUT_TEXT> --output-dir <OUTPUT_DIRECTORY>
```

### Options

| Parameter | Type | Default | Description |
| :--- | :---: | :--- | :--- |
| `--model` | `str` | `distilbert-base-uncased-finetuned-sst-2-english` | Hugging Face Hub model ID or local directory path. |
| `--sentence` | `str` | `"The movie was great..."` | Input text string to audit. |
| `--output-dir` | `str` | `audit_reports` | Output directory path for generated Markdown reports and Matplotlib charts. |

---

## 2. Interactive Web Dashboard (Streamlit)

Launch the interactive dashboard to audit models, view probe matrices, and inspect diagnostic graphs:

```bash
streamlit run blindspot/app.py
```

### Dashboard Features
- **Audit Configuration Sidebar**: Specify model ID and input text snippet.
- **Metric Highlights**: Display Original Prediction, Prediction Flip Rate, ECE score, and Total Failures.
- **Diagnostic Visualizations Tab**: Render 2x2 grid of publication-grade Matplotlib charts.
- **Perturbation Probe Matrix Tab**: Interactive DataFrame showing probe details.
- **Failure Taxonomy Tab**: Expandable detail view of detected failures and actionable recommendations.

---

## 3. Python API Integration

Import `AuditPipeline` directly into custom Python scripts or Jupyter Notebooks:

```python
from blindspot.audit import AuditPipeline

# Initialize pipeline
pipeline = AuditPipeline(
    model_name_or_path="distilbert-base-uncased-finetuned-sst-2-english",
    output_dir="audit_reports"
)

# Run end-to-end audit
results = pipeline.run_audit("The food was delicious and the service was amazing.")

# Access diagnostic outputs
print("Prediction Flip Rate:", results["behavioral_results"]["flip_rate"])
print("Total Failures:", len(results["failures"]))
```

---

## 4. Running Test Suites

Run unit and integration tests using `pytest` or `run_tests.py`:

```bash
python run_tests.py
```

Or via `pytest`:

```bash
pytest -v
```
