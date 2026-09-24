# Architectural Design & Pipeline

**BlindSpot** is structured into five core subpackages under `blindspot/`, designed for modularity, maintainability, and model independence.

---

## 1. Model-Agnostic Interface (`blindspot.models`)

The model layer wraps black-box text classifiers to provide a standardized probabilistic interface.

- **Class**: `HuggingFaceWrapper` ([huggingface_wrapper.py](file:///d:/BlindSpot/blindspot/models/huggingface_wrapper.py))
- **Primary Function**: `predict_proba(texts: List[str]) -> np.ndarray`
  - Accepts a list of $N$ input strings and returns a NumPy array of shape $(N, K)$ representing class probabilities.
  - Automatically queries Hugging Face sequence classification pipelines.
  - Includes a zero-dependency fallback heuristic classifier for offline testing.

---

## 2. Perturbation Engine (`blindspot.perturbations`)

Generates linguistically controlled variants from a single input sentence.

- **Base Class**: `BasePerturber` ([base.py](file:///d:/BlindSpot/blindspot/perturbations/base.py))
- **Engines**:
  - `SingleNegationPerturber` & `DoubleNegationPerturber` ([negation.py](file:///d:/BlindSpot/blindspot/perturbations/negation.py)): Injects auxiliary negation operators (`not`, `never`) and double negative constructs (`not impossible`).
  - `ContrastiveConnectivePerturber` ([connectives.py](file:///d:/BlindSpot/blindspot/perturbations/connectives.py)): Appends contrast clauses (`however the service was terrible`).
  - `SynonymSubstitutionPerturber` ([substitution.py](file:///d:/BlindSpot/blindspot/perturbations/substitution.py)): Replaces key sentiment adjectives with WordNet synonyms.
- **Aggregator**: `PerturbationEngine` ([engine.py](file:///d:/BlindSpot/blindspot/perturbations/engine.py)) executes all perturbers and returns structured probe dictionaries.

---

## 3. Behavioral Testing Engine (`blindspot.testing`)

Probes classifier stability and quantifies diagnostic metrics.

- **Class**: `BehavioralTester` ([behavioral.py](file:///d:/BlindSpot/blindspot/testing/behavioral.py))
- **Metrics Calculation** ([metrics.py](file:///d:/BlindSpot/blindspot/testing/metrics.py)):
  - **Flip Rate**: $\text{Flip Rate} = \frac{N_{\text{flipped}}}{N_{\text{total}}}$
  - **Expected Calibration Error (ECE)**:
    $$\text{ECE} = \sum_{b=1}^B \frac{|B_b|}{N} |\text{acc}(B_b) - \text{conf}(B_b)|$$

---

## 4. Explainability & Taxonomy Engine (`blindspot.explainability`)

Pairs LIME and SHAP feature attributions before and after perturbation to evaluate reasoning shifts.

- **Lime & SHAP Wrappers**: [lime_explainer.py](file:///d:/BlindSpot/blindspot/explainability/lime_explainer.py) & [shap_explainer.py](file:///d:/BlindSpot/blindspot/explainability/shap_explainer.py)
- **Attribution Alignment** ([alignment.py](file:///d:/BlindSpot/blindspot/explainability/alignment.py)):
  - **Jaccard Attribution Similarity**: Top-$K$ feature token set overlap.
  - **Cosine Attribution Alignment**: Cosine similarity between feature weight vectors over shared vocabulary.
- **Taxonomy Classifier** ([taxonomy.py](file:///d:/BlindSpot/blindspot/explainability/taxonomy.py)): Categorizes model failures into **Blind**, **Spurious**, and **Misweighted**.

---

## 5. Automated Reporting & Visualization (`blindspot.reporting`)

Compiles diagnostic data into Markdown documents and publication graphs.

- **Report Generator**: `ReportGenerator` ([report_generator.py](file:///d:/BlindSpot/blindspot/reporting/report_generator.py)) builds Markdown reports (`model_behavior_report.md`, `failure_summary.md`, `explanation_comparison.md`, `probes/*.md`).
- **Visualizer**: `Visualizer` ([visualizer.py](file:///d:/BlindSpot/blindspot/reporting/visualizer.py)) creates 4 Matplotlib PNG charts (`taxonomy_distribution.png`, `behavioral_metrics.png`, `attribution_comparison.png`, `probe_alignment_summary.png`).
