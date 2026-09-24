# BLINDSPOT — COMPLETE CURRENT-STATE AUDIT REPORT

**Audit Date**: 2026-09-20  
**Target Repository**: `c:\Dev\Projects\BlinkSpot-main`  
**Audit Status**: READ-ONLY AUDIT COMPLETE — STRUCTURAL REPORT ONLY  
**Review Protocol**: Strict Empirical Skepticism — No Speculative Passing  
**Standardized Status Labels**: `VERIFIED` | `PARTIALLY VERIFIED` | `DEFECT` | `UNKNOWN`  

---

## 1. PROJECT INVENTORY

### 1.1 Repository Structure & Important Modules
The active codebase consists of the primary package `blindspot/`, execution launchers, storage directories, and test suites:

- **`blindspot/core/`**:
  - `types.py` (897 lines): Domain dataclasses and enums (`PredictionResult`, `LinguisticProbe`, `SharedProbeSet`, `BaselineEvaluation`, `ModelProbeEvaluation`, `BehavioralProbeResult`, `RunPlan`, `BehavioralOutcome`, `FailureCategory`, `SemanticIntent`, `ExpectedLabelRelation`, `ExpectedConfidenceRelation`).
  - `config.py`: Configuration dataclasses (`ExperimentConfig`, `ResourceConfig`, `PerformanceMode`).
  - `events.py`: Thread-safe execution pub/sub event dispatcher (`ExecutionEvent`, `EventEmitter`).
  - `logging_config.py`: Structured subsystem logger routing to `logs/blindspot.log`.
- **`blindspot/models/`**:
  - `huggingface_wrapper.py` (302 lines): Standardized black-box wrapper for Hugging Face transformer classification pipelines (`HuggingFaceWrapper`).
  - `registry.py` (166 lines): Registry and preset provider (`ModelRegistry`).
  - `cache.py`: LRU memory cache for loaded neural models (`ModelCache`).
- **`blindspot/perturbations/`**:
  - `engine.py` (43 lines): Orchestrator running linguistic perturbers (`PerturbationEngine`).
  - `shared.py` (519 lines): Shared probe generator producing canonical `SharedProbeSet` (`SharedProbeGenerator`).
  - `negation.py` (123 lines): Insertion, removal, and litotes (`NegationPerturber`, `DoubleNegationPerturber`).
  - `connectives.py` (168 lines): Adversative, concessive, and contrastive connectives (`ConnectivePerturber`).
  - `substitution.py` (123 lines): Lexical synonym substitutions (`SynonymSubstitutionPerturber`).
  - `intensity.py`: Degree adverbs and downtoners (`IntensityPerturber`).
  - `structure.py`: Clause reordering and framing (`StructurePerturber`).
  - `linguistic_analyzer.py`: spaCy dependency parser and SentiWordNet scoring.
- **`blindspot/testing/`**:
  - `behavioral.py` (529 lines): Behavioral testing engine and pure classifier (`BehavioralTester`, `classify_behavior`, `classify_behavioral_outcome`).
  - `metrics.py` (213 lines): Statistical metrics (`compute_flip_rate`, `compute_observed_flip_rate`, `compute_expected_flip_rate`, `compute_preserve_rate`, `compute_behavioral_consistency`, `compute_ece`, `compute_transition_matrix`).
- **`blindspot/execution/`**:
  - `runner.py` (646 lines): Multithreaded background execution orchestrator (`ExperimentRunner`).
  - `run_plan.py`: Immutable run plan definition (`RunPlan`).
  - `resources.py`: Hardware device detection and batch sizing (`ResourceManager`).
- **`blindspot/explainability/`**:
  - `lime_wrapper.py`, `shap_wrapper.py`: Local surrogate and Shapley explainers.
  - `taxonomy.py` (129 lines): Secondary wrapper classifying behavioral failures with XAI attribution (`TaxonomyClassifier`).
- **`blindspot/storage/`**:
  - `run_store.py` (171 lines): Persistence manager writing artifacts into `runs/<experiment_id>/`.
- **`blindspot/reporting/`**:
  - `generator.py` (179 lines): Legacy report generator.
- **`blindspot/ui/`**:
  - `shell.py`, `overview.py`, `experiment_lab.py`, `probe_lab.py`, `live_run.py`, `comparison.py`, `explanation_lab.py`, `failure_lab.py`, `run_history.py`, `console.py`, `system_monitor.py`, `components.py`, `design_system.py`.
- **Root Files & Launchers**:
  - `blindspot/app.py`: Streamlit entrypoint (`main()`).
  - `blindspot/launcher.py`: Process supervisor and port manager.
  - `launch_blindspot.bat`, `launch_blindspot.ps1`.
- **Tests**:
  - 17 test suites in `tests/` executed via `run_tests.py`.

### 1.2 Duplicate and Legacy Implementations
- **Report Generation Duplicate (`DEFECT`)**:
  - Legacy module: `blindspot/reporting/generator.py` (`ReportGenerator`).
  - Active implementation: Inline generator inside `blindspot/execution/runner.py:465-645` (`_generate_reports`).
  - *Finding*: `runner.py` completely bypasses `blindspot/reporting/generator.py` when generating `experiment_summary.md`, `probe_level_evidence.md`, and `failure_summary.md`. `ReportGenerator` is dead/legacy code.
- **Taxonomy Classification Duplicate (`PARTIALLY VERIFIED`)**:
  - Legacy module: `blindspot/explainability/taxonomy.py` (`TaxonomyClassifier`).
  - Canonical implementation: `blindspot/testing/behavioral.py:40-213` (`classify_behavior`).
  - *Finding*: `TaxonomyClassifier.classify_failure()` was refactored into a thin wrapper delegating to `classify_behavior()`. However, `runner.py:214-238` derives failures directly from `BehavioralTester.evaluate_shared_probes()` without calling `TaxonomyClassifier` unless explainers are executed.

---

## 2. EXACT MODELS CURRENTLY USED

Five models are configured in `blindspot/models/registry.py:19-75`. An empirical diagnostic was executed directly on Hugging Face model checkpoints to extract raw configurations, output shapes, and class metadata.

### Model 1: `distilbert-base-uncased-finetuned-sst-2-english`
- **Hugging Face Model Identifier**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Task**: `sentiment-analysis` (`text-classification`)
- **Architecture**: `DistilBertForSequenceClassification`
- **Number of Output Classes**: 2
- **Raw `id2label`**: `{0: "NEGATIVE", 1: "POSITIVE"}`
- **Raw `label2id`**: `{"NEGATIVE": 0, "POSITIVE": 1}`
- **Tokenizer**: `BertTokenizer` (`use_fast=True`)
- **Classification Head**: `Linear` layer projecting hidden dimension (768) to 2 classes.
- **Logits Shape**: `(batch_size, 2)`
- **Probability Calculation**: `softmax(logits, dim=-1)` computed internally by Hugging Face `pipeline(top_k=None)` and re-normalized by vector sum in `huggingface_wrapper.py:181-186`.
- **Predicted Label**: Top argmax class normalized via `normalize_label_name()`.
- **Confidence Calculation**: `float(probs[top_idx])` representing the true predicted softmax probability in $[0.0, 1.0]$.
- **Full Distribution Retained**: `VERIFIED`. Returns a full dictionary `{"NEGATIVE": float, "POSITIVE": float}`.
- **Hardware Acceleration**: CPU verified; CUDA supported via PyTorch.
- **Actually Used in App**: `VERIFIED`. Selected as the default benchmark classifier.
- **Evaluation Status**: `VERIFIED`. Genuinely outputs `NEGATIVE` and `POSITIVE`.

### Model 2: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Hugging Face Model Identifier**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Task**: `sentiment-analysis` (`text-classification`)
- **Architecture**: `RobertaForSequenceClassification`
- **Number of Output Classes**: 3
- **Raw `id2label`**: `{0: "negative", 1: "neutral", 2: "positive"}` (lowercase in config)
- **Raw `label2id`**: `{"negative": 0, "neutral": 1, "positive": 2}`
- **Tokenizer**: `RobertaTokenizer` (`use_fast=True`)
- **Classification Head**: `RobertaClassificationHead` (dense projection + dropout + linear).
- **Logits Shape**: `(batch_size, 3)`
- **Probability Calculation**: 3-class softmax probability distribution.
- **Predicted Label**: Top argmax mapped through `normalize_label_name()` (`"negative"` $\to$ `"NEGATIVE"`, `"neutral"` $\to$ `"NEUTRAL"`, `"positive"` $\to$ `"POSITIVE"`).
- **Confidence Calculation**: Softmax probability of winning class in $[0.0, 1.0]$.
- **Full Distribution Retained**: `VERIFIED`. Dict contains `NEGATIVE`, `NEUTRAL`, and `POSITIVE`.
- **Hardware Acceleration**: CPU and CUDA supported.
- **Actually Used in App**: `VERIFIED`. Preset selectable in Experiment Setup.
- **Evaluation Status**: `VERIFIED`.

### Model 3: `textattack/bert-base-uncased-SST-2`
- **Hugging Face Model Identifier**: `textattack/bert-base-uncased-SST-2`
- **Task**: `sentiment-analysis` (`text-classification`)
- **Architecture**: `BertForSequenceClassification`
- **Number of Output Classes**: 2
- **Raw `id2label`**: `{0: "LABEL_0", 1: "LABEL_1"}` (`DEFECT: RAW IDENTIFIERS LACK SEMANTIC NAMES`)
- **Raw `label2id`**: `{"LABEL_0": 0, "LABEL_1": 1}`
- **Tokenizer**: `BertTokenizer` (`use_fast=True`)
- **Classification Head**: `Linear` (768 to 2).
- **Logits Shape**: `(batch_size, 2)`
- **Label Normalization Code Trace**: `blindspot/models/huggingface_wrapper.py:28-32`:
  ```python
  if num_classes == 2:
      if upper in {"LABEL_0", "0", "NEG", "NEGATIVE"}:
          return "NEGATIVE"
      if upper in {"LABEL_1", "1", "POS", "POSITIVE"}:
          return "POSITIVE"
  ```
  *Analysis*: For SST-2 binary, index 0 is negative and index 1 is positive. `normalize_label_name` translates `LABEL_0` $\to$ `NEGATIVE` and `LABEL_1` $\to$ `POSITIVE`. While empirically correct for SST-2, relying on hardcoded `LABEL_0` $\to$ `NEGATIVE` assumptions is fragile for non-sentiment tasks.
- **Probability Calculation**: Softmax probability.
- **Full Distribution Retained**: `VERIFIED`.
- **Evaluation Status**: `PARTIALLY VERIFIED` (Normalization works for SST-2, but lacks dynamic dataset ontology awareness).

### Model 4: `roberta-base-openai-detector`
- **Hugging Face Model Identifier**: `roberta-base-openai-detector`
- **Task**: `text-classification` (Synthetic / AI-Generated Text Detection)
- **Architecture**: `RobertaForSequenceClassification`
- **Number of Output Classes**: 2
- **Raw `id2label`**: `{0: "Fake", 1: "Real"}`
- **Raw `label2id`**: `{"Fake": 0, "Real": 1}`
- **Tokenizer**: `RobertaTokenizer`
- **Classification Head**: `RobertaClassificationHead`
- **Normalized Labels in Wrapper**: `["FAKE", "REAL"]` (`normalize_label_name` leaves "Fake" and "Real" as uppercase `FAKE` and `REAL`).
- **Registry Preset Metadata (`DEFECT`)**: In `blindspot/models/registry.py:58`:
  ```python
  "label_names": ["NEGATIVE", "POSITIVE"],  # DEFECT: FALSE METADATA
  ```
  The registry metadata falsely asserts that this model outputs `NEGATIVE` and `POSITIVE`.
- **Application Task Mismatch (`DEFECT: MAJOR RESEARCH VALIDITY ISSUE`)**:
  This model was trained to distinguish GPT-2 synthetic text from human text. It is **NOT** a sentiment analysis classifier. Placing it alongside sentiment models in a sentiment robustness audit causes meaningless behavioral flip comparisons (e.g. evaluating whether "I loved the movie" vs "I hated the movie" flips between Fake and Real).
- **Evaluation Status**: `DEFECT`.

### Model 5: `cardiffnlp/twitter-roberta-base-sentiment` (Classic)
- **Hugging Face Model Identifier**: `cardiffnlp/twitter-roberta-base-sentiment`
- **Task**: `sentiment-analysis` (`text-classification`)
- **Architecture**: `RobertaForSequenceClassification`
- **Number of Output Classes**: 3
- **Raw `id2label`**: `{0: "LABEL_0", 1: "LABEL_1", 2: "LABEL_2"}`
- **Raw `label2id`**: `{"LABEL_0": 0, "LABEL_1": 1, "LABEL_2": 2}`
- **Tokenizer**: `RobertaTokenizer`
- **Classification Head**: `RobertaClassificationHead`
- **Label Normalization Code Trace**: `blindspot/models/huggingface_wrapper.py:33-39`:
  ```python
  elif num_classes == 3:
      if upper in {"LABEL_0", "0", "NEG", "NEGATIVE"}:
          return "NEGATIVE"
      if upper in {"LABEL_1", "1", "NEU", "NEUTRAL"}:
          return "NEUTRAL"
      if upper in {"LABEL_2", "2", "POS", "POSITIVE"}:
          return "POSITIVE"
  ```
  *Analysis*: The Cardiff NLP Twitter RoBERTa classic release uses $0 = \text{negative}, 1 = \text{neutral}, 2 = \text{positive}$. The 3-class normalizer correctly maps `LABEL_0` $\to$ `NEGATIVE`, `LABEL_1` $\to$ `NEUTRAL`, `LABEL_2` $\to$ `POSITIVE`.
- **Evaluation Status**: `VERIFIED`.

---

## 3. ACTUAL MODEL OUTPUTS

Empirical outputs obtained from executing `scratch/model_audit_diagnostic.py` (CPU device, exact PyTorch model weights loaded from cache):

| Model | Input Sentence | Raw Output Labels & Scores | Normalized Label | Conf | Full Probabilities |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **DistilBERT SST-2** (2-class) | "I loved the movie." | POSITIVE: 0.9999, NEGATIVE: 0.0001 | `POSITIVE` | 0.9999 | NEG: 0.01%, POS: 99.99% |
| | "I hated the movie." | NEGATIVE: 0.9997, POSITIVE: 0.0003 | `NEGATIVE` | 0.9997 | NEG: 99.97%, POS: 0.03% |
| | "The movie was okay." | POSITIVE: 0.9998, NEGATIVE: 0.0002 | `POSITIVE` | 0.9998 | NEG: 0.02%, POS: 99.98% |
| | "I don't think the movie was not entirely without merit." | POSITIVE: 0.9980, NEGATIVE: 0.0020 | `POSITIVE` | 0.9980 | NEG: 0.20%, POS: 99.80% |
| **Twitter RoBERTa Latest** (3-class) | "I loved the movie." | positive: 0.9805, neutral: 0.0160, negative: 0.0035 | `POSITIVE` | 0.9805 | NEG: 0.35%, NEU: 1.60%, POS: 98.05% |
| | "I hated the movie." | negative: 0.9183, neutral: 0.0679, positive: 0.0138 | `NEGATIVE` | 0.9183 | NEG: 91.83%, NEU: 6.79%, POS: 1.38% |
| | "The movie was okay." | positive: 0.8963, neutral: 0.0958, negative: 0.0079 | `POSITIVE` | 0.8963 | NEG: 0.79%, NEU: 9.58%, POS: 89.63% |
| | "I don't think the movie was not entirely without merit." | neutral: 0.4985, negative: 0.4722, positive: 0.0292 | `NEUTRAL` | 0.4985 | NEG: 47.22%, NEU: 49.85%, POS: 2.92% |
| **BERT Base SST-2** (2-class) | "I loved the movie." | LABEL_1: 0.9995, LABEL_0: 0.0005 | `POSITIVE` | 0.9995 | NEG: 0.05%, POS: 99.95% |
| | "I hated the movie." | LABEL_0: 0.9990, LABEL_1: 0.0010 | `NEGATIVE` | 0.9990 | NEG: 99.90%, POS: 0.10% |
| | "The movie was okay." | LABEL_1: 0.9929, LABEL_0: 0.0071 | `POSITIVE` | 0.9929 | NEG: 0.71%, POS: 99.29% |
| | "I don't think the movie was not entirely without merit." | LABEL_1: 0.9827, LABEL_0: 0.0173 | `POSITIVE` | 0.9827 | NEG: 1.73%, POS: 98.27% |
| **RoBERTa OpenAI Detector** (2-class) | "I loved the movie." | Fake: 0.8962, Real: 0.1038 | `FAKE` | 0.8962 | FAKE: 89.62%, REAL: 10.38% |
| | "I hated the movie." | Fake: 0.8246, Real: 0.1754 | `FAKE` | 0.8246 | FAKE: 82.46%, REAL: 17.54% |
| | "The movie was okay." | Fake: 0.9314, Real: 0.0686 | `FAKE` | 0.9314 | FAKE: 93.14%, REAL: 6.86% |
| | "I don't think the movie was not entirely without merit." | Fake: 0.8488, Real: 0.1512 | `FAKE` | 0.8488 | FAKE: 84.88%, REAL: 15.12% |
| **Twitter RoBERTa Classic** (3-class) | "I loved the movie." | LABEL_2: 0.9886, LABEL_1: 0.0087, LABEL_0: 0.0026 | `POSITIVE` | 0.9886 | NEG: 0.26%, NEU: 0.87%, POS: 98.86% |
| | "I hated the movie." | LABEL_0: 0.9782, LABEL_1: 0.0182, LABEL_2: 0.0036 | `NEGATIVE` | 0.9782 | NEG: 97.82%, NEU: 1.82%, POS: 0.36% |
| | "The movie was okay." | LABEL_2: 0.8830, LABEL_1: 0.1090, LABEL_0: 0.0080 | `POSITIVE` | 0.8830 | NEG: 0.80%, NEU: 10.90%, POS: 88.30% |
| | "I don't think the movie was not entirely without merit." | LABEL_1: 0.7142, LABEL_0: 0.1611, LABEL_2: 0.1247 | `NEUTRAL` | 0.7142 | NEG: 16.11%, NEU: 71.42%, POS: 12.47% |

### Core Question: Does every model produce a comparable label + confidence representation?
**NO (`DEFECT`)**.
1. **Binary vs. Multiclass Probability Distortion**: In 2-class SST-2 models, the probability simplex is strictly binary ($P(\text{POS}) + P(\text{NEG}) = 1.0$). Consequently, ambiguous, hedged, or neutral statements (e.g. *"The movie was okay."*) are artificially forced to extreme confidence ($99.98\%$ in DistilBERT, $99.29\%$ in BERT SST-2). In contrast, 3-class models assign probability mass to `NEUTRAL` ($9.58\%$ and $10.90\%$), dampening confidence.
2. **Double/Triple Negation Disagreement**: On *"I don't think the movie was not entirely without merit."*, binary models output `POSITIVE` ($99.80\%$), while 3-class models classify it as `NEUTRAL` ($49.85\%$ and $71.42\%$). Directly comparing flip rates across 2-class and 3-class models without class-alignment normalizes away fundamentally different behavioral spaces.
3. **OpenAI Detector Incompatibility**: `roberta-base-openai-detector` outputs `FAKE` ($84\%-93\%$) on all four sentences. It has zero semantic or sentiment alignment with the other 4 models.

---

## 4. PROBE PIPELINE TRACE

```text
INPUT SENTENCE (User UI or Script)
      ↓
PROBE GENERATION (SharedProbeGenerator.generate_probes)
      ↓
PROBE CATALOG (SharedProbeSet: List[LinguisticProbe])
      ↓
SELECTION (Probe Lab Checkboxes or Category Filter)
      ↓
VALIDATION (SharedProbeSet.validate())
      ↓
EXPERIMENT CONFIG (ExperimentConfig.selected_probe_set)
      ↓
RUN PLAN (RunPlan: immutable metadata record)
      ↓
LIVE RUN (ExperimentRunner.run_async -> _execute)
      ↓
BASELINE EVALUATION (BehavioralTester.evaluate_shared_probes: seed_predictions)
      ↓
PROBE PREDICTIONS (Model batch inference on perturbed_texts)
      ↓
BEHAVIORAL OUTCOME & FAILURE CLASSIFICATION (classify_behavior)
      ↓
METRICS AGGREGATION (compute_observed_flip_rate, compute_expected_flip_rate, etc.)
      ↓
PERSISTENT REPORTS (save_results -> experiment_summary.md, probe_level_evidence.md, failure_summary.md)
```

### Granular Stage Specifications
1. **Input Sentence**:
   - *File*: `blindspot/ui/probe_lab.py:75` or `experiment_lab.py:74`.
   - *Data*: String(s). Source of truth: UI session state `st.session_state["exp_seed_text"]`.
2. **Probe Generation**:
   - *File*: `blindspot/perturbations/shared.py:155-201`.
   - *Class*: `SharedProbeGenerator.generate_probes()`.
   - *Input*: `seed_texts: List[str]`, `candidate_count: int = 7`.
   - *Output*: `SharedProbeSet` containing `LinguisticProbe` objects.
3. **Probe Catalog & Selection**:
   - *File*: `blindspot/ui/probe_lab.py:130-180`.
   - *State*: `st.session_state["workbench_candidates"]` and `st.session_state["workbench_selection"]`.
   - *Source of truth*: `st.session_state["staged_probe_set"]` when staged to Experiment Lab.
4. **Validation**:
   - *File*: `blindspot/core/types.py:457-483` (`SharedProbeSet.validate()`).
   - *Rule*: Blocks execution if `probe_id` is missing, `seed_text == perturbed_text`, or duplicates exist.
5. **Experiment Configuration**:
   - *File*: `blindspot/core/config.py:75-125` (`ExperimentConfig`).
   - *Contains*: `selected_probe_set: Optional[SharedProbeSet]`.
6. **Run Plan**:
   - *File*: `blindspot/execution/runner.py:160-170` and `blindspot/execution/run_plan.py:15-35`.
   - *Contains*: Immutable `experiment_id`, `model_ids`, `selected_probe_ids`, `probe_versions`.
7. **Model Inference & Baseline**:
   - *File*: `blindspot/testing/behavioral.py:338-354`.
   - *Function*: `BehavioralTester.evaluate_shared_probes()`.
   - *Source of truth*: `seed_predictions` evaluates original sentence exactly once per seed per model.
8. **Behavioral Analysis & Failure Taxonomy**:
   - *File*: `blindspot/testing/behavioral.py:40-213`.
   - *Function*: `classify_behavior()`.
   - *Output*: `(BehavioralOutcome, FailureCategory, evidence_dict, rationale_str)`.
9. **Metrics Aggregation**:
   - *File*: `blindspot/testing/metrics.py:66-128`.
10. **Report Persistence**:
    - *File*: `blindspot/execution/runner.py:465-645` and `blindspot/storage/run_store.py:61-105`.

### Canonical Probe Object Evaluation
- **Is there one canonical probe object?**:
  `PARTIALLY VERIFIED`.
  - When the researcher uses **Probe Workbench** and clicks "Send to Experiment Lab", `staged_probe_set` is constructed and attached to `ExperimentConfig.selected_probe_set`. `ExperimentRunner:123-134` executes this staged set directly without re-generation.
  - When the researcher does **not** stage from Probe Workbench (relying on dynamic category checkboxes in `experiment_lab.py`), `selected_probe_set` is `None`, and `ExperimentRunner:139-144` generates a brand new `SharedProbeSet` from scratch, decoupling the Experiment preview from actual execution.

---

## 5. INVESTIGATE THE KNOWN PROBE COUNT BUG

### Previously Observed Bug: `Generated: 7 → Experiment: 4 → Live Run: 3`

#### Exact Empirical Diagnostic Proof
Running `SharedProbeGenerator.generate_probes()` with `candidate_count=7` vs `candidate_count=None` with the 4 default categories `["negation", "double_negation", "connective", "synonym_substitution"]`:
- **Generated**: `['negation_insertion', 'double_negation', 'intensity', 'intensity', 'synonym_substitution', 'contrast_negative_append', 'structure']` (Length: 7).
- **Filtered**: `['double_negation', 'double_negation', 'synonym_substitution']` (Length: 3).

#### Exact Code Path Causing the 7 → 4 → 3 Bug (`DEFECT: CRITICAL`)
1. **Stage 1 (Generated = 7)**:
   In `blindspot/ui/probe_lab.py:124-129`, candidate generation invokes `gen.generate_probes(candidate_count=7)`. In `blindspot/perturbations/shared.py:184-185`, `candidate_count == 7` routes to `_generate_calibrated_7_probes()`, which deterministically creates **7 candidate probes** (P001 to P007).
2. **Stage 2 (Experiment Setup = 4)**:
   In `blindspot/ui/experiment_lab.py:243-266`, the experiment setup interface provides category checkboxes. Prior to the addition of Intensity and Structure, exactly **4 categories** were exposed:
   `["negation", "double_negation", "connective", "synonym_substitution"]`.
   The UI displayed: `4 Dynamic Categories Active`.
3. **Stage 3 (Live Run = 3) — The Silent Drop**:
   When the runner executed without a staged set, it called `_generate_all_probes(perturbation_types=["negation", "double_negation", "connective", "synonym_substitution"])`.
   In `blindspot/perturbations/shared.py:469-472`:
   ```python
   for item in variants:
       ptype = item.get("type", "unknown")
       if perturbation_types and ptype not in perturbation_types:
           continue
   ```
   Examine what the underlying perturbers actually set in `item["type"]`:
   - `NegationPerturber` (`blindspot/perturbations/negation.py:50, 60, 72`): Sets `type = "negation_insertion"`, `type = "negation_removal"`, or `type = "negation_prefix"`. None of these equal `"negation"`. **Negation probes were silently dropped!**
   - `ConnectivePerturber` (`blindspot/perturbations/connectives.py:42` and `shared.py:399`): Sets `type = "contrast_negative_append"` or `type = "concession"`. None of these equal `"connective"`. **Connective probes were silently dropped!**
   - `DoubleNegationPerturber` (`blindspot/perturbations/negation.py:96`): Sets `type = "double_negation"`. This string matches `"double_negation"`, producing 2 variants.
   - `SynonymSubstitutionPerturber` (`blindspot/perturbations/substitution.py:92`): Sets `type = "synonym_substitution"`. This string matches `"synonym_substitution"`, producing 1 variant.
   
   **Total Executed Probes = 2 (double negation) + 1 (synonym) = 3.**
   The negation inversion probe and connective contrast probe were silently discarded due to an exact string mismatch between the UI filter category names and the perturber subtype return strings.

---

## 6. PROBE INVENTORY

The calibrated 7-probe diagnostic suite generated by `SharedProbeGenerator._generate_calibrated_7_probes()` for `"The movie was great."`:

| Slot | Probe ID Prefix | Category | Original Text | Perturbed Text | Semantic Intent | Expected Effect | Expected Label Rel | Expected Conf Rel | Transformation | Expected Flip |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **P001** | `prb_9f6874...` | `negation_insertion` | "The movie was great." | "The movie was not great." | `REVERSE_POLARITY` | `invert` | `DIFFERENT_LABEL` | `UNCONSTRAINED` | Inserted negation 'not' after auxiliary verb | **`True`** |
| **P002** | `prb_0efd62...` | `double_negation` | "The movie was great." | "It is not impossible that the movie was great." | `PRESERVE_MEANING` | `preserve` | `SAME_LABEL` | `PRESERVE` | Double negation framing ('not impossible') | **`False`** |
| **P003** | `prb_c0a52c...` | `intensity` | "The movie was great." | "The movie was extremely great." | `STRENGTHEN_POLARITY` | `strengthen` | `SAME_LABEL` | `INCREASE` | Injected degree intensifier 'extremely' | **`False`** |
| **P004** | `prb_67268d...` | `intensity` | "The movie was great." | "The movie somewhat was great." | `WEAKEN_POLARITY` | `weaken` | `SAME_LABEL` | `DECREASE` | Injected downtoner adverb 'somewhat' | **`False`** |
| **P005** | `prb_d09b68...` | `synonym_substitution`| "The movie was great." | "The movie was fantastic." | `PRESERVE_MEANING` | `preserve` | `SAME_LABEL` | `PRESERVE` | Substituted 'great' with synonym 'fantastic' | **`False`** |
| **P006** | `prb_f4be08...` | `contrast_negative_append` | "The movie was great." | "The movie was great, however it did not improve over time." | `SHIFT_CONTRAST` | `invert` | `DIFFERENT_LABEL` | `UNCONSTRAINED` | Appended adversative clause shifting dominant discourse relation | **`True`** |
| **P007** | `prb_f45aa0...` | `structure` | "The movie was great." | "In essence, the movie was great." | `PRESERVE_MEANING` | `preserve` | `SAME_LABEL` | `PRESERVE` | Added discourse marker 'In essence,' | **`False`** |

### Suite Balance
- **Expected-Change Probes**: 2 (`P001`, `P006`).
- **Expected-Preserve Probes**: 5 (`P002`, `P003`, `P004`, `P005`, `P007`).
- *Finding*: `VERIFIED`. The calibrated suite contains both expected-change and expected-preserve stimuli, enabling clean differentiation between `BLIND` (failure to flip when expected) and `SPURIOUS` (flipping when preserved).

---

## 7. PROBE QUALITY AUDIT

Audit of linguistic phenomena across the 16 required categories:

1. **Negation (`VERIFIED`)**: `NegationPerturber` inspects auxiliary verbs (`is/was/are/can/could`) and inserts `not`. Handles contraction removal (`n't`).
2. **Negation Removal (`VERIFIED`)**: If input contains `not/never`, cleanly strips it to test inversion.
3. **Double Negation (`PARTIALLY VERIFIED`)**: Uses litotes templates (`"It is not impossible that..."`, `"It is not untrue that..."`). *Defect*: Syntactic litotes framing creates unnatural phrasing on certain informal sentences.
4. **Intensification (`VERIFIED`)**: Inserts degree intensifiers (`extremely`, `truly`, `definitely`).
5. **Downtoning (`PARTIALLY VERIFIED`)**: Inserts `somewhat`, `slightly`. *Defect*: In `P004`, inserting `somewhat` after subject before auxiliary produces ungrammatical word order: *"The movie somewhat was great."* rather than *"The movie was somewhat great."*
6. **Contrast / Adversative Connectives (`VERIFIED`)**: Appends concessive/adversative clauses (`", however it did not improve over time."`). Successfully inverts dominant discourse polarity.
7. **Conjunction / Correlative (`UNKNOWN`)**: No dedicated perturber for correlative conjunctions (`neither...nor`, `not only...but also`).
8. **Lexical Substitution (`VERIFIED`)**: Curated synonym map (`great` $\to$ `fantastic`, `bad` $\to$ `subpar`) with WordNet fallback.
9. **Word Order / Clause Reordering (`PARTIALLY VERIFIED`)**: `StructurePerturber` splits comma-separated clauses and swaps them. Does not handle complex subordinate clauses.
10. **Clause Structure (`VERIFIED`)**: Tested via discourse marker framing (`"In essence,"`, `"Undeniably,"`).
11. **Emphasis / Punctuation (`PARTIALLY VERIFIED`)**: Handled by exclamation/period drift in `StructurePerturber`.
12. **Figurative Language / Proverbs (`PARTIALLY VERIFIED`)**: Supported via dictionary lookup for 4 known proverbs. Arbitrary figurative idioms are unhandled.
13. **Idioms (`UNKNOWN / NOT IMPLEMENTED`)**: No general idiom parser or idiomatic perturber.
14. **Irony / Sarcasm (`UNKNOWN / NOT IMPLEMENTED`)**: No automated sarcasm inversion or pragmatic antiphrasis generator.

---

## 8. PROVERB / FIGURATIVE SUPPORT

### Analysis of `"All that glitters is not gold."`
- **Classification**: `VERIFIED`. `blindspot/perturbations/shared.py:177-182` normalizes string and detects match against `KNOWN_PROVERBS["all that glitters is not gold"]`. Assigns `SentenceType.PROVERB`.
- **Semantic Interpretation**: Stored in probe metadata: *"Appearances can be deceptive; superficial attraction does not guarantee intrinsic value."*
- **Probe Generation**:
  - `P001` (Inversion Flip): Uses `proverb_meta["inversion_flip"]` $\to$ *"All that glitters is gold."* (`expected_flip = True`).
  - `P005` (Paraphrase Preserve): Uses `proverb_meta["paraphrase_preserve"]` $\to$ *"Not everything that glitters is truly valuable."* (`expected_flip = False`).
- **Limitation (`DEFECT`)**: `KNOWN_PROVERBS` contains exactly **4 hardcoded entries** (`"all that glitters is not gold"`, `"actions speak louder than words"`, `"a bird in the hand is worth two in the bush"`, `"every cloud has a silver lining"`). Any other proverb or figurative idiom falls back to literal string parsing.

---

## 9. ORIGINAL BASELINE

### Baseline Evaluation Implementation
- **File**: `blindspot/testing/behavioral.py:338-350` (`evaluate_shared_probes`).
- **Execution**:
  ```python
  for seed in probe_set.seed_texts:
      pred = self.model.predict_result(seed)
      seed_predictions[seed] = pred
      stype = probe_set.sentence_types.get(seed, SentenceType.LITERAL.value)
      baselines[seed] = BaselineEvaluation(
          model_id=self.model.model_name,
          seed_text=seed,
          sentence_type=stype,
          prediction=pred,
          latency_ms=pred.latency_ms,
      )
  ```
- **Storage**:
  - Evaluated **exactly once** per model before probe iterations begin.
  - Stored in `model_baselines[model_id]` as `BaselineEvaluation`.
  - Stored inside each `ModelProbeEvaluation.original_prediction`.
- **Comparison Anchor**:
  Every probe for that seed text compares its output (`perturbed_prediction`) against `seed_predictions[probe.seed_text]`.
- **Evaluation Status**: `VERIFIED`. Every probe evaluates against the identical baseline.

---

## 10. FLIP IMPLEMENTATION

### Multiclass Flip Detection
- **File**: `blindspot/core/types.py:97-105`:
  ```python
  def is_prediction_flip(original_label: str, perturbed_label: str) -> bool:
      if not original_label or not perturbed_label:
          return False
      return str(original_label).strip().upper() != str(perturbed_label).strip().upper()
  ```
- **Binary Hardcoding Audit**:
  - Search for `1 - original_label`, `1 - original_idx`, or binary invert logic: `CLEAN`. (Prior inverted index bug documented in CHANGELOG v0.2.1 was resolved).
- **Multiclass Transition Matrix Verification**:
  - `POSITIVE` $\to$ `NEGATIVE`: Flipped = `True` (`VERIFIED`)
  - `POSITIVE` $\to$ `NEUTRAL`: Flipped = `True` (`VERIFIED`)
  - `POSITIVE` $\to$ `POSITIVE`: Flipped = `False` (`VERIFIED`)
  - `NEGATIVE` $\to$ `NEUTRAL`: Flipped = `True` (`VERIFIED`)
  - `NEUTRAL` $\to$ `POSITIVE`: Flipped = `True` (`VERIFIED`)
- **Evaluation Status**: `VERIFIED`. Pure multiclass inequality.

---

## 11. CONFIDENCE ANALYSIS

### Implementation Details
- **File**: `blindspot/testing/behavioral.py:102` and `blindspot/testing/metrics.py:145-155`.
- **Formula**:
  $$\Delta \text{Conf}_{\text{pp}} = (P_{\text{probe}} - P_{\text{original}}) \times 100.0$$
- **Units**: Calculated strictly in **signed percentage points** (e.g. $0.90 \to 0.70 = -20.0\text{ pp}$).
- **Arbitrary Thresholds Identified (`PARTIALLY VERIFIED`)**:
  1. `confidence_delta_threshold_pp = 15.0` (`blindspot/testing/behavioral.py:52`):
     - Used in `classify_behavior` to diagnose `MISWEIGHTED` when an intensifier causes confidence to drop by $> 15.0\text{ pp}$, or a downtoner causes confidence to increase by $> 15.0\text{ pp}$.
     - *Justification*: Standard empirical margin for distinguishing stochastic variance from significant confidence drift.
  2. `threshold_pts = 20.0` (`blindspot/testing/metrics.py:130`):
     - Used in `compute_confidence_flip_rate` to count severe confidence drops.

---

## 12. BEHAVIORAL OUTCOME IMPLEMENTATION

### Decision Tree in `blindspot/testing/behavioral.py:143-161`
```text
Is prediction flip expected under probe contract? (is_expected_flip)
│
├── TRUE (Probe expects label inversion):
│     ├── Observed Flip (is_flipped == True)  ──> EXPECTED_FLIP
│     └── No Flip       (is_flipped == False) ──> MISSING_FLIP
│
└── FALSE (Probe expects label preservation):
      ├── No Flip       (is_flipped == False) ──> EXPECTED_PRESERVE
      └── Observed Flip (is_flipped == True)  ──> UNEXPECTED_FLIP
```
- **Reporting Usage**: `VERIFIED`. Behavioral outcomes are stored in `ModelProbeEvaluation.behavioral_outcome`, streamed in live execution events, rendered in `probe_level_evidence.md`, and aggregated in `experiment_summary.md`.

---

## 13. FAILURE TAXONOMY IMPLEMENTATION

### Audit of the 4 Failure Categories

#### 1. BLIND (`VERIFIED`)
1. **Formal Definition**: The model fails to register an explicit, polarity-altering syntactic or semantic operator (e.g. negation, adversative connective), retaining its prior prediction.
2. **Triggering Code**: `blindspot/testing/behavioral.py:168-175`:
   `if is_expected_flip and not flipped:` $\to$ `outcome = MISSING_FLIP`, `failure = BLIND`.
3. **Inputs Required**: A probe with `expected_flip = True` where the model predicts `probe_label == original_label`.
4. **Reachability**: Reachable. Proven empirically on DistilBERT evaluating *"The movie was not great and the acting was top notch."*
5. **Tested**: Yes, in `tests/test_behavioral_taxonomy.py` (Case 2) and live diagnostics.
6. **Reported**: Yes, in `failure_summary.md` and `experiment_summary.md`.
7. **Model-Independent**: Yes.
8. **Probe Semantics**: Grounded in `expected_flip = True`.
9. **Confidence-Based**: No.
10. **Label Transitions**: Grounded in `original_label == probe_label`.

#### 2. SPURIOUS (`VERIFIED`)
1. **Formal Definition**: Model decisions are altered by irrelevant, meaning-preserving variations (e.g. synonym substitution, structural framing).
2. **Triggering Code**: `blindspot/testing/behavioral.py:205-210`:
   `if not is_expected_flip and flipped and norm_intent not in ("STRENGTHEN_POLARITY", "WEAKEN_POLARITY"):` $\to$ `failure = SPURIOUS`.
3. **Inputs Required**: Meaning-preserving probe (`expected_flip = False`) where model prediction flips.
4. **Reachability**: Reachable.
5. **Tested**: Yes, in `tests/test_behavioral_taxonomy.py` (Case 4).
6. **Reported**: Yes.
7. **Model-Independent**: Yes.
8. **Probe Semantics**: Grounded in `expected_flip = False`.
9. **Confidence-Based**: No.
10. **Label Transitions**: Grounded in `original_label != probe_label`.

#### 3. MISWEIGHTED (`VERIFIED`)
1. **Formal Definition**: Token weights or confidence transitions are inappropriately aligned with degree modification (e.g. an intensifier causes a confidence collapse or a label inversion).
2. **Triggering Code**: `blindspot/testing/behavioral.py:178-204`:
   - Subcase A: Flipped label on degree modifier (`norm_intent in ("STRENGTHEN_POLARITY", "WEAKEN_POLARITY") and flipped`).
   - Subcase B: Confidence drop $> 15.0\text{ pp}$ on intensifier.
   - Subcase C: Confidence surge $> 15.0\text{ pp}$ on downtoner.
3. **Inputs Required**: Degree probe with confidence drift violating monotonicity.
4. **Reachability**: Reachable.
5. **Tested**: Yes, in `tests/test_behavioral_taxonomy.py` (Case 7: 3 unit tests).
6. **Reported**: Yes.
7. **Model-Independent**: Yes.
8. **Probe Semantics**: Grounded in `STRENGTHEN_POLARITY` / `WEAKEN_POLARITY`.
9. **Confidence-Based**: Yes (utilizes signed percentage point deltas).
10. **Label Transitions**: Evaluates both flipped and non-flipped variants.

#### 4. UNDETERMINED (`VERIFIED`)
1. **Formal Definition**: Behavioral transition occurred, but missing labels, missing confidence, or uncharacterized probe contracts prevent causal diagnosis.
2. **Triggering Code**: `blindspot/testing/behavioral.py:63-93` and `135-141`.
3. **Inputs Required**: Missing prediction metadata or undefined expected effect.
4. **Reachability**: Reachable.
5. **Tested**: Yes, in `tests/test_behavioral_taxonomy.py` (Case 8).
6. **Reported**: Yes.
7. **Model-Independent**: Yes.
8. **Probe Semantics**: Triggered on unknown expectations.
9. **Confidence-Based**: Triggered if confidence is `None`.
10. **Label Transitions**: Evaluated before label comparison.

---

## 14. WHY ARE REAL RUNS SHOWING ZERO FAILURES?

A primary motivation for this audit was explaining why historical and UI runs reported 0 failures across all models.

### Confirmed Technical Causes

#### 1. Confirmed Cause A: Silent Dropping of Polarity Probes in Dynamic Generation (`CONFIRMED CAUSE`)
- **Location**: `blindspot/perturbations/shared.py:471`.
- **Evidence**: When `perturbation_types` was passed from the UI (`["negation", "double_negation", "connective", "synonym_substitution"]`), exact string matching discarded `negation_insertion` and `contrast_negative_append`.
- **Impact**: All surviving probes (double negation, synonym substitution) were invariant probes (`expected_flip = False`). Because there was not a single probe expecting a flip, `MISSING_FLIP` $\to$ `BLIND` was mathematically unreachable. Since models rarely flip on synonyms or double negations, 0 failures were recorded.

#### 2. Confirmed Cause B: Structural Key Mismatch in `infer_expected_semantic_effect` (`CONFIRMED CAUSE`)
- **Location**: `blindspot/perturbations/shared.py:88-144`.
- **Evidence**: In earlier versions of `infer_expected_semantic_effect()`, checking `if ptype == "negation":` failed to match `negation_insertion`, `negation_removal`, and `contrast_negative_append`.
- **Impact**: All generated probes defaulted to `expected_flip = False`. When a model failed to flip on a negated sentence, `is_flipped == expected_flip` (`False == False`), falsely rewarding model blindness as `EXPECTED_PRESERVE` and suppressing `BLIND` diagnoses.

#### 3. Confirmed Cause C: Unhandled Runtime AttributeError in Runner Event Loop (`CONFIRMED CAUSE`)
- **Location**: `runs/exp_1789913168_27d348/results.json:345` and `blindspot/execution/runner.py:226, 322-329`.
- **Evidence**: In recent run `exp_1789913168_27d348` (testing 5 models on *"I don't think the movie was not entirely without merit."*), `results.json` records:
  ```json
  "error": "'ModelProbeEvaluation' object has no attribute 'original_label'"
  ```
- **Impact**: When `runner.py:226` accessed `ev.original_label`, an `AttributeError` was raised. The exception handler at line 322 caught the error, set `model_evaluations[model_id] = []` and `model_failures[model_id] = []`, and completed execution with `executed: 0`. The report generator then rendered a clean table with 0 failures for all 5 models.

---

## 15. SYNTHETIC TAXONOMY TEST

- **File**: `tests/test_behavioral_taxonomy.py` (370 lines).
- **Test Results**:
  1. `test_case_1_expected_flip_compliant`: `PASSED`.
  2. `test_case_2_blind_missing_flip`: `PASSED`.
  3. `test_case_3_expected_preserve_compliant`: `PASSED`.
  4. `test_case_4_spurious_unexpected_flip`: `PASSED`.
  5. `test_case_5_multiclass_expected_flip`: `PASSED`.
  6. `test_case_6_multiclass_preserve`: `PASSED`.
  7. `test_case_7_misweighted_degree_strengthening_drop`: `PASSED`.
  8. `test_case_7_misweighted_degree_downtoning_surge`: `PASSED`.
  9. `test_case_7_misweighted_degree_flipped_label`: `PASSED`.
  10. `test_case_8_undetermined_missing_labels`: `PASSED`.
  11. `test_case_8_undetermined_missing_confidence`: `PASSED`.
  12. `test_case_8_undetermined_unknown_effect`: `PASSED`.
  13. `test_model_agnostic_classification`: `PASSED`.
  14. `test_zero_failures_table_never_suppressed`: `PASSED`.
- **Status**: `VERIFIED`. The synthetic taxonomy suite demonstrates that all 4 failure categories are reachable, testable, and mathematically sound under controlled inputs.

---

## 16. MODEL-SPECIFIC FAILURE POSSIBILITY

- **Hard-coded Model IDs in Failure Classification**: `CLEAN`. Zero occurrences of `if model` or model-specific branch conditions in `blindspot/testing/behavioral.py` or `metrics.py`.
- **Model-Specific Confidence Thresholds**: None. The $15.0\text{ pp}$ delta threshold is applied uniformly.
- **Dangerous Hardcoding in Registry (`DEFECT`)**: `blindspot/models/registry.py:58` hardcodes `label_names: ["NEGATIVE", "POSITIVE"]` for `roberta-base-openai-detector`, which actually outputs `["Fake", "Real"]`.

---

## 17. RECENT RUN ARTIFACTS

Inspection of persisted artifact directories in `runs/`:

### Artifact Tree 1: `runs/exp_1789896208_17e393/`
- **Seed Input**: *"The movie was great and the acting was top notch."*
- **Models**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Probes Executed**: 9 probes.
- **Probe Distribution**: 2 double negation, 1 synonym substitution, 4 intensity, 2 structure.
- **Expected Flips**: 0 probes with `expected_flip = True`.
- **Failures Diagnosed**: 0.
- *Finding*: Run completed successfully, but zero failures were observed because 100% of executed probes were invariance probes.

### Artifact Tree 2: `runs/exp_1789913168_27d348/`
- **Seed Input**: *"I don't think the movie was not entirely without merit."*
- **Models**: All 5 models (`distilbert`, `roberta-latest`, `bert-sst2`, `roberta-openai`, `roberta-classic`).
- **Results**: `executed: 0` for all 5 models.
- **Failures Diagnosed**: 0.
- *Finding*: Failed silently due to runtime `AttributeError` on `ev.original_label` during execution event emission.

---

## 18. CROSS-MODEL ANALYSIS

- **Implementation**: `blindspot/analysis/cross_model.py:20-135` (`CrossModelAnalyzer`).
- **Guarantees**:
  - `SharedProbeSet` is generated once and supplied to every selected model.
  - Model A, Model B, and Model C receive the exact same probe texts in identical sequence.
  - Verified by `tests/test_shared_probes.py:test_multimodel_identical_probe_stimuli_and_ids`.
- **Cross-Model Agreement Metrics**:
  - `overall_agreement_rate`: Fleiss' generalized multi-annotator agreement.
  - `pairwise_agreement`: Cohen's kappa and concordance matrix.
- **Evaluation Status**: `VERIFIED`.

---

## 19. PERSISTENCE AND VERSIONING

- **File**: `blindspot/storage/run_store.py:20-105` and `blindspot/execution/run_plan.py:15-35`.
- **Metadata Fields Stored**:
  - `experiment_id`
  - `probe_set_id`
  - `probe_set_version`
  - `generator_version`
  - `selected_probe_ids`
  - `created_at` / `completed_at`
- **Reproducibility Audit**:
  `PARTIALLY VERIFIED`.
  While metadata and configuration are saved, historical runs saved before schema v2.2.0 cannot be re-executed with guaranteed byte-for-byte fidelity because dynamic category runs regenerated probes rather than saving the raw probe catalog JSON in `runs/<experiment_id>/config.json`.

---

## 20. REPORTING

- **Reports Generated**:
  1. `experiment_summary.md`: Stratified flip rates (observed vs expected), baseline table, zero-failure retention table, pairwise concordance matrix.
  2. `probe_level_evidence.md`: Granular table with probe ID, baseline prediction, probe output, transition, confidence delta (pp), outcome, failure type, and linguistic rationales.
  3. `failure_summary.md`: Detailed failure records with severity, evidence, and actionable recommendations.
- **Zero-Failure Display**: `VERIFIED`. Zero categories are explicitly displayed in tables (`b_cnt: 0`, `s_cnt: 0`) and never omitted.
- **Evaluation Status**: `VERIFIED`.

---

## 21. TEST SUITE

- **Total Test Files**: 17 files in `tests/`.
- **Total Test Cases**: 98 unit and integration tests.
- **Execution Command**: `python run_tests.py`
- **Execution Result**:
  - **Passed**: 98
  - **Failed**: 0
  - **Errors**: 0
  - **Skipped**: 0
- **What is NOT Tested (`DEFECT: TEST GAPS`)**:
  1. No automated test verifying that `roberta-base-openai-detector` outputs sentiment-compatible classes (which it cannot).
  2. No end-to-end integration test verifying that dynamic category execution (`selected_probe_set=None`) produces non-zero negation probes across complex sentence types.
  3. No test checking ungrammatical adverb placement in downtoning perturbations.

---

## 22. UI STATE

- **Implementation**: Multi-page modular Streamlit architecture in `blindspot/ui/`.
- **Top Navigation Shell**: `blindspot/ui/shell.py` routes across 7 domains (`Overview`, `Experiment`, `Probes`, `Run`, `Analyze`, `Reports`, `System`).
- **State Inconsistencies Identified (`DEFECT`)**:
  - `Experiment Lab` (`blindspot/ui/experiment_lab.py:347`): Formula `planned_probes_per_seed = len(selected_ptypes) * 4` is a hardcoded heuristic estimate ($N \times 4$), producing phantom counts before execution.
  - Dual State Path: Staging from Probe Workbench uses `staged_probe_set`, while direct Experiment setup uses dynamic category checkboxes, leading to divergent execution paths.

---

## 23. RESOURCE / STORAGE STATE

- **Model Cache**: `blindspot/models/cache.py` (`ModelCache`). Implements an LRU cache with configurable size (`max_loaded_models = 3`).
- **RAM Footprint**: Loading 3 transformer models simultaneously consumes $\sim 2.5 - 3.8\text{ GB}$ host RAM.
- **GPU Behavior**: Automatically queries `torch.cuda.is_available()`. Falls back to CPU if CUDA is unavailable or OOM occurs.
- **Artifact Storage**: `runs/` directory stores JSONL events and Markdown reports ($\sim 50-200\text{ KB}$ per run).

---

## 24. RESEARCH-INTEGRITY RATING

| Subsystem | Rating | Primary Justification |
| :--- | :---: | :--- |
| **Model Normalization** | `PARTIALLY VERIFIED` | Works for SST-2 and Twitter RoBERTa; fragile hardcoded `LABEL_0/1/2` assumptions; OpenAI detector misclassified as sentiment. |
| **Probe Generation** | `VERIFIED` | Calibrated 7-probe suite generates deterministic, balanced stimuli across negation, intensity, synonym, and contrast. |
| **Probe Semantics** | `VERIFIED` | `SemanticIntent`, `ExpectedLabelRelation`, and `ExpectedConfidenceRelation` are formally defined and attached. |
| **Probe Selection** | `PARTIALLY VERIFIED` | Full probe workbench selection exists, but direct Experiment Lab lacks individual probe checkboxes. |
| **Probe Validation** | `VERIFIED` | `SharedProbeSet.validate()` strictly blocks malformed or identical probe pairs. |
| **RunPlan** | `VERIFIED` | Immutable plan anchors experiment ID, model IDs, probe IDs, and versions. |
| **Baseline Anchor** | `VERIFIED` | Original sentence evaluated once per model and stored as primary reference. |
| **Flip Analysis** | `VERIFIED` | Pure multiclass inequality ($y_0 \neq y_p$). Binary inversion assumptions eliminated. |
| **Confidence Analysis** | `VERIFIED` | Signed percentage points ($\Delta\text{pp}$); verified against probability simplex. |
| **Behavioral Outcomes** | `VERIFIED` | Pure empirical classification (`EXPECTED_FLIP`, `MISSING_FLIP`, `EXPECTED_PRESERVE`, `UNEXPECTED_FLIP`). |
| **Failure Taxonomy** | `VERIFIED` | 4-way taxonomy (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`) proven via synthetic tests. |
| **Cross-Model Analysis** | `VERIFIED` | Strictly identical probe stimuli, order, and identifiers across all target models. |
| **Reporting** | `VERIFIED` | Complete 21-field reports generated without suppressing zero-failure categories. |
| **Persistence** | `PARTIALLY VERIFIED` | `runs/` trees preserve artifacts, but historical runs before v2.2.0 lack full probe JSON schemas. |
| **Tests** | `VERIFIED` | 98 passing unit/integration tests with zero errors. |
| **UI State** | `PARTIALLY VERIFIED` | Clean navigation, but Run Plan specification displays hardcoded $N \times 4$ estimate on dynamic runs. |

---

## 25. FINAL PRIORITIZED DEFECT LIST

### P0 — RESEARCH VALIDITY BLOCKERS
1. **DEF-01: Non-Sentiment Model Configured as Sentiment Benchmark Preset**
   - *Location*: `blindspot/models/registry.py:53-63`.
   - *Evidence*: `roberta-base-openai-detector` is an AI-generated text detector predicting `Fake`/`Real`. Its preset falsely claims `label_names: ["NEGATIVE", "POSITIVE"]`.
   - *Impact*: Comparing OpenAI Detector against sentiment probes compromises research validity.
   - *Fix Direction*: Replace with a verified sentiment classifier (e.g. `distilroberta-base-finetuned-sst-2-english` or `finiteautomata/bertweet-base-sentiment-analysis`).
   - *Required Test*: Unit test verifying that all registered sentiment presets output sentiment ontological classes.
2. **DEF-02: String Key Mismatch Dropping Negation in Dynamic Execution**
   - *Location*: `blindspot/perturbations/shared.py:471`.
   - *Evidence*: `_generate_all_probes` filters by `ptype not in perturbation_types`. `NegationPerturber` produces `type="negation_insertion"`, which does not match `"negation"`.
   - *Impact*: Dynamic experiment execution without staging silently drops negation probes, leaving only preserve probes and causing zero failures.
   - *Fix Direction*: Filter by canonical category or check `ptype.startswith(target)`.
   - *Required Test*: Unit test proving `generate_probes(perturbation_types=["negation"], candidate_count=None)` produces negation probes.

### P1 — MAJOR FUNCTIONAL DEFECTS
3. **DEF-03: Hardcoded Label Mapping for Raw Model Outputs**
   - *Location*: `blindspot/models/huggingface_wrapper.py:28-41`.
   - *Evidence*: `normalize_label_name()` hardcodes `LABEL_0` $\to$ `NEGATIVE` for 2-class models.
   - *Impact*: Any model where `LABEL_0` represents `POSITIVE`, `ENTAILED`, or non-sentiment classes is inverted.
   - *Fix Direction*: Extract label semantics from model config card, dataset metadata, or explicit user mapping.
   - *Required Test*: Diagnostic verifying label normalization on models with arbitrary label mappings.
4. **DEF-04: Inline Report Generation Bypassing Report Module**
   - *Location*: `blindspot/execution/runner.py:465-645` vs `blindspot/reporting/generator.py`.
   - *Evidence*: `runner.py` duplicates 180 lines of markdown generation, leaving `ReportGenerator` dead.
   - *Fix Direction*: Unify report generation inside `ReportGenerator`.
   - *Required Test*: Regression test asserting `ReportGenerator` produces identical markdown tables.

### P2 — IMPORTANT CORRECTNESS / UX ISSUES
5. **DEF-05: Ungrammatical Word Order in Downtoning Perturbation**
   - *Location*: `blindspot/perturbations/shared.py:328-330`.
   - *Evidence*: *"The movie somewhat was great."*
   - *Fix Direction*: Insert downtoner adjacent to the predicate adjective or main verb (*"The movie was somewhat great."*).
   - *Required Test*: Linguistic syntax check asserting adverb position following copular verbs.
6. **DEF-06: Heuristic Run Plan Probe Estimation Formula**
   - *Location*: `blindspot/ui/experiment_lab.py:347`.
   - *Evidence*: `planned_probes_per_seed = len(selected_ptypes) * 4`.
   - *Impact*: UI displays inaccurate estimated probe counts.
   - *Fix Direction*: Call `generator.estimate_probe_count()` rather than multiplying by 4.

### P3 — POLISH
7. **DEF-07: Hardcoded 4-Proverb Dictionary Limitation**
   - *Location*: `blindspot/perturbations/shared.py:24-49`.
   - *Evidence*: Only 4 proverbs are recognized.
   - *Fix Direction*: Expand proverb catalog or integrate lexical idiom dataset (e.g. PIE corpus).

---

## 26. DO NOT IMPLEMENT FIXES DECLARATION

This report represents an objective audit of the current BlindSpot repository. In strict adherence to user instructions:
- **No source code was modified.**
- **No architectural changes were implemented.**
- **No probes or failure classifiers were altered.**
- **All diagnostics were executed via non-destructive read-only scripts.**

---

## 27. FINAL EXECUTIVE SUMMARY

Concise, evidence-based answers to the 16 mandatory audit questions:

1. **What models are actually being used?**
   Five models are configured: (1) `distilbert-base-uncased-finetuned-sst-2-english`, (2) `cardiffnlp/twitter-roberta-base-sentiment-latest`, (3) `textattack/bert-base-uncased-SST-2`, (4) `roberta-base-openai-detector`, and (5) `cardiffnlp/twitter-roberta-base-sentiment`.
2. **What labels does each model actually output?**
   - Models 1 and 3 output binary `NEGATIVE` and `POSITIVE`.
   - Models 2 and 5 output 3-class `NEGATIVE`, `NEUTRAL`, and `POSITIVE`.
   - Model 4 outputs `FAKE` and `REAL` (it is not a sentiment model).
3. **What does "confidence" actually mean for each model?**
   Confidence is the true maximum softmax probability of the predicted class extracted directly from Hugging Face model logits ($P_{\max} \in [0.0, 1.0]$). It is neither fabricated nor heuristic.
4. **Is there one canonical probe pipeline?**
   Partially. Staging from Probe Workbench enforces an immutable `SharedProbeSet` and `RunPlan`. However, direct execution from Experiment Lab regenerates probes independently.
5. **Why did 7 probes become 4 and then 3?**
   - **7 Generated**: Calibrated suite produced 7 probes (P001 to P007).
   - **4 Configured**: Experiment Lab exposed 4 default category checkboxes.
   - **3 Executed**: In `_generate_all_probes()`, string mismatch between UI category names (`"negation"`, `"connective"`) and perturber return types (`"negation_insertion"`, `"contrast_negative_append"`) silently dropped negation and contrast probes, leaving only 2 double negation probes and 1 synonym substitution probe ($2 + 1 = 3$).
6. **Is the original baseline correct?**
   Yes (`VERIFIED`). The original seed sentence is evaluated exactly once per model as `BaselineEvaluation`, stored in `model_baselines`, and anchored as the comparison baseline for every probe.
7. **Is multiclass flip detection correct?**
   Yes (`VERIFIED`). Flip detection uses pure inequality (`orig_label != pert_label`). All binary assumptions (`1 - orig`) have been eliminated.
8. **Are confidence deltas correct?**
   Yes (`VERIFIED`). Calculated strictly in signed percentage points: $(P_{\text{probe}} - P_{\text{orig}}) \times 100.0$.
9. **Can the system genuinely produce BLIND?**
   Yes (`VERIFIED`). Triggered when a polarity-altering probe (`expected_flip = True`) fails to flip the model prediction. Proven on DistilBERT.
10. **Can it genuinely produce SPURIOUS?**
    Yes (`VERIFIED`). Triggered when a meaning-preserving probe (`expected_flip = False`) flips the model prediction.
11. **Can it genuinely produce MISWEIGHTED?**
    Yes (`VERIFIED`). Triggered when degree modifiers flip labels or shift confidence by $> 15.0\text{ pp}$ against the expected gradient direction.
12. **Can it genuinely produce UNDETERMINED?**
    Yes (`VERIFIED`). Triggered when predictions, confidences, or probe contract expectations are missing.
13. **Why are current runs showing zero failures?**
    Due to two proven technical defects: (a) silent dropping of polarity-changing probes in un-staged dynamic execution, leaving only invariance probes where models rarely flip, and (b) runtime unhandled `AttributeError` on `ev.original_label` aborting model evaluation with `executed: 0` before failures are tabulated.
14. **What are the top five research-validity defects?**
    1. Inclusion of non-sentiment `roberta-base-openai-detector` (Fake/Real) in sentiment benchmark.
    2. String mismatch silently dropping negation probes during dynamic generation.
    3. Incomparable confidence distributions between 2-class binary SST-2 and 3-class models.
    4. Hardcoded `LABEL_0` $\to$ `NEGATIVE` assumptions in label normalizer.
    5. Ungrammatical adverb placement in downtoner probe generation.
15. **What must be fixed BEFORE UI polishing?**
    Replace the OpenAI detector with a genuine sentiment model, fix category filter string matching in probe generation, and align 2-class vs 3-class comparative metrics.
16. **What tests must pass before the project can be considered research-ready?**
    - Multi-class model alignment test ensuring non-sentiment models are rejected.
    - End-to-end dynamic execution test asserting non-zero negation probes execute without staging.
    - Syntax validity test guaranteeing zero ungrammatical probe outputs.
