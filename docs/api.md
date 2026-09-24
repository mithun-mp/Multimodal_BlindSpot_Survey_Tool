# Python API Reference

Comprehensive reference for all subpackages in the `blindspot` package.

---

## 1. Orchestrator Package (`blindspot.audit`)

### `AuditPipeline`

```python
class AuditPipeline(model_name_or_path: str = "distilbert-base-uncased-finetuned-sst-2-english", output_dir: str = "audit_reports", explainer_type: str = "lime")
```

Main orchestrator class implementing the *"pretrained model in, diagnostic report out"* auditing workflow.

#### Methods

##### `run_audit(sentence: str) -> Dict[str, Any]`
Runs the complete 5-step auditing pipeline on an input sentence string:
1. Generates linguistic variants via `PerturbationEngine`.
2. Probes model predictions via `BehavioralTester`.
3. Extracts token attributions via `LimeExplainerWrapper` & `ShapExplainerWrapper`.
4. Classifies failure instances via `TaxonomyClassifier`.
5. Compiles Markdown reports & Matplotlib figures via `ReportGenerator`.

---

## 2. Models Package (`blindspot.models`)

### `HuggingFaceWrapper`

```python
class HuggingFaceWrapper(model_name_or_path: str)
```

Black-box interface for Hugging Face Transformers classification pipelines.

#### Methods
- `predict_proba(texts: Union[str, List[str]]) -> np.ndarray`: Returns probability array of shape `(N, num_classes)`.
- `predict(texts: Union[str, List[str]]) -> List[str]`: Returns top predicted string labels.

---

## 3. Perturbations Package (`blindspot.perturbations`)

### `PerturbationEngine`
Aggregates all perturbation sub-modules:
- `SingleNegationPerturber`
- `DoubleNegationPerturber`
- `ContrastiveConnectivePerturber`
- `SynonymSubstitutionPerturber`

#### Methods
- `generate_all(sentence: str) -> List[Dict[str, Any]]`: Returns list of probe dictionaries containing `perturbed`, `type`, `description`, and `expected_flip`.

---

## 4. Testing Package (`blindspot.testing`)

### `BehavioralTester`

```python
class BehavioralTester(model: HuggingFaceWrapper)
```

Evaluates probes and records prediction changes.

#### Methods
- `evaluate_probe(original_sentence: str, perturbations: List[Dict[str, Any]]) -> Dict[str, Any]`: Computes prediction flip rates, calibration error (ECE), and probe details.

---

## 5. Explainability Package (`blindspot.explainability`)

### Alignment Functions
- `compute_jaccard_similarity(exp1: Dict[str, float], exp2: Dict[str, float], top_k: int = 5) -> float`
- `compute_attribution_cosine(exp1: Dict[str, float], exp2: Dict[str, float]) -> float`

### `TaxonomyClassifier`
- `classify_failure(...) -> Optional[Dict[str, Any]]`: Evaluates prediction shifts vs explanation shifts to classify failures into `Blind`, `Spurious`, or `Misweighted`.

---

## 6. Reporting Package (`blindspot.reporting`)

### `Visualizer`
- `generate_all_plots(audit_results, failures, explanations_summary) -> Dict[str, str]`

### `ReportGenerator`
- `generate_all_reports(model_name, audit_results, failures, explanations_summary) -> List[str]`
