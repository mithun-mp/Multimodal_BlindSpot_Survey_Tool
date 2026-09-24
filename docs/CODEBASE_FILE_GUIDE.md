# BlindSpot: Comprehensive Codebase File-by-File Technical Guide

**Project**: BlindSpot: A Behavioral and Explainable-AI Framework for Auditing Text Classifiers  
**Author**: Ziya Fathima M P (TCR25MCA-2060)  
**Institution**: Department of Computer Applications, Government Engineering College, Thrissur  
**Repository Path**: `d:\BlindSpot`  

---

## 1. Executive System Overview

**BlindSpot** is an empirical, black-box diagnostic auditing framework for text classifiers (such as Hugging Face Transformers). It addresses a fundamental flaw in modern Natural Language Processing (NLP): **standard benchmark test accuracy fails to detect severe linguistic and behavioral vulnerabilities** (e.g., ignoring negation words, relying on spurious domain nouns, or exhibiting brittle confidence under minor synonym shifts).

The framework implements a strict **"pretrained model in, diagnostic report out"** paradigm:
1. It takes an un-retrained black-box classification model and an input sentence.
2. It performs deep syntactic and lexical analysis (spaCy dependency parsing, animacy typing, NLTK SentiWordNet polarity ranking) and generates systematic linguistic perturbations (controlled mutations).
3. It performs behavioral stress-testing (flip rates, confidence shifts, Expected Calibration Error).
4. It extracts local feature attributions using Explainable AI (LIME and SHAP) before and after mutations, preserving occurrence identity for repeated words via sequence alignment.
5. It classifies failures into a 3-way Failure Taxonomy (**Blind**, **Spurious**, **Misweighted**).
6. It compiles self-contained diagnostic Markdown reports and publication-quality Matplotlib figures.

```
                      ┌────────────────────────────────────────┐
                      │    Input Sentence + Pretrained Model   │
                      └───────────────────┬────────────────────┘
                                          │
                                          ▼
                               ┌─────────────────────┐
                               │  AuditPipeline      │ (audit.py)
                               │  - Input Validation │
                               │  - Suitability Check│
                               └──────────┬──────────┘
                                          │
        ┌─────────────────────────────────┼─────────────────────────────────┐
        │                                 │                                 │
        ▼                                 ▼                                 ▼
┌───────────────────────────┐     ┌───────────────────────┐     ┌───────────────────────┐
│ PerturbationEngine        │     │ BehavioralTester      │     │ Explainers & Taxonomy │
│ (perturbations/)          │     │ (testing/)            │     │ (explainability/)     │
│ - LinguisticAnalyzer      │     │ - Probabilities       │     │ - LIME Token Weights  │
│ - Single Negation         │     │ - Prediction Flips    │     │ - SHAP Token Weights  │
│ - Double Negation         │     │ - Flip Rate & ECE     │     │ - TokenAttributions   │
│ - Contextual Connectives  │     │ - Unexpected Behavior │     │ - Occurrence Align    │
│ - Synonym Swap            │     │                       │     │ - 3-Way Classifier    │
└───────────────────────────┘     └───────────────────────┘     └───────────────────────┘
        │                                 │                                 │
        └─────────────────────────────────┼─────────────────────────────────┘
                                          │
                                          ▼
                               ┌─────────────────────┐
                               │  Reporting Engine   │ (reporting/)
                               │  - Markdown Reports │
                               │  - Matplotlib Charts│
                               └──────────┬──────────┘
                                          │
                      ┌───────────────────┴────────────────────┐
                      ▼                                        ▼
           ┌──────────────────────┐               ┌───────────────────────┐
           │ Streamlit Web App    │               │ CLI & File System     │
           │ (app.py :8501)       │               │ (cli.py / reports/)   │
           └──────────────────────┘               └───────────────────────┘
```

---

## 2. Master File Index

| File Path | Primary Responsibility | Key Classes / Functions |
| :--- | :--- | :--- |
| [`setup.py`](file:///d:/BlindSpot/setup.py) | Package distribution & installation manifest | `setup()` |
| [`requirements.txt`](file:///d:/BlindSpot/requirements.txt) | Python dependencies specification | Core & visualization libraries |
| [`run.ps1`](file:///d:/BlindSpot/run.ps1) | Multi-mode PowerShell execution launcher | CLI, Dashboard, Test, Docs commands |
| [`run_tests.py`](file:///d:/BlindSpot/run_tests.py) | Standalone verification test runner | `TestBlindSpotFramework` (14 tests) |
| [`mkdocs.yml`](file:///d:/BlindSpot/mkdocs.yml) | Technical documentation configuration | MkDocs Material theme & navigation |
| [`srs.pdf`](file:///d:/BlindSpot/srs.pdf) | Software Requirements Specification document | Academic SRS requirements & architecture |
| [`IMPLEMENTATION_STEPS.md`](file:///d:/BlindSpot/IMPLEMENTATION_STEPS.md) | Step-by-step roadmap & milestones tracking | Phase 1 to Phase 6 engineering milestones |
| [`PROJECT_STATE_REPORT.md`](file:///d:/BlindSpot/PROJECT_STATE_REPORT.md) | Complete project state & SRS compliance audit | 100% SRS compliance matrix, directory map |
| [`project_questions_and_doubts.md`](file:///d:/BlindSpot/project_questions_and_doubts.md) | Persistent technical Q&A & viva defense log | Q1–Q21 technical justifications |
| [`DIAGNOSTIC_GRAPHS_GUIDE.md`](file:///d:/BlindSpot/DIAGNOSTIC_GRAPHS_GUIDE.md) | Comprehensive guide to the 4 diagnostic visualizations | Chart anatomy, formulas, case studies, defense scripts |
| [`blindspot/__init__.py`](file:///d:/BlindSpot/blindspot/__init__.py) | Core package initialization & exports | `AuditPipeline`, `HuggingFaceWrapper` |
| [`blindspot/audit.py`](file:///d:/BlindSpot/blindspot/audit.py) | Central pipeline orchestrator, alignment & enrichment | `AuditPipeline` |
| [`blindspot/cli.py`](file:///d:/BlindSpot/blindspot/cli.py) | Command-line interface launcher | `main()` |
| [`blindspot/app.py`](file:///d:/BlindSpot/blindspot/app.py) | Interactive Streamlit web dashboard & diagnostic viewer | UI tabs, failure narratives, aligned diffs, image renderer |
| [`blindspot/models/__init__.py`](file:///d:/BlindSpot/blindspot/models/__init__.py) | Models subpackage exporter | `HuggingFaceWrapper` |
| [`blindspot/models/huggingface_wrapper.py`](file:///d:/BlindSpot/blindspot/models/huggingface_wrapper.py) | Black-box Hugging Face wrapper + heuristic fallback | `HuggingFaceWrapper` |
| [`blindspot/perturbations/__init__.py`](file:///d:/BlindSpot/blindspot/perturbations/__init__.py) | Perturbations subpackage exporter | Perturbers, `LinguisticAnalyzer`, `SentenceFeatures` |
| [`blindspot/perturbations/base.py`](file:///d:/BlindSpot/blindspot/perturbations/base.py) | Abstract base class for perturbation generators | `BasePerturber` |
| [`blindspot/perturbations/linguistic_analyzer.py`](file:///d:/BlindSpot/blindspot/perturbations/linguistic_analyzer.py) | Syntactic deconstruction, animacy typing & WordNet lexical opposites | `SentenceFeatures`, `LinguisticAnalyzer` |
| [`blindspot/perturbations/negation.py`](file:///d:/BlindSpot/blindspot/perturbations/negation.py) | Single negation & litotes double negation engines | `NegationPerturber`, `DoubleNegationPerturber` |
| [`blindspot/perturbations/connectives.py`](file:///d:/BlindSpot/blindspot/perturbations/connectives.py) | Context-aware contrastive connective & concession engines | `ConnectivePerturber` |
| [`blindspot/perturbations/substitution.py`](file:///d:/BlindSpot/blindspot/perturbations/substitution.py) | Stopword-filtered WordNet synonym substitution | `SynonymSubstitutionPerturber` |
| [`blindspot/perturbations/engine.py`](file:///d:/BlindSpot/blindspot/perturbations/engine.py) | Aggregator combining all perturbers | `PerturbationEngine` |
| [`blindspot/testing/__init__.py`](file:///d:/BlindSpot/blindspot/testing/__init__.py) | Testing subpackage exporter | `BehavioralTester`, metrics |
| [`blindspot/testing/behavioral.py`](file:///d:/BlindSpot/blindspot/testing/behavioral.py) | Probe evaluation runner & confidence delta tracker | `BehavioralTester` |
| [`blindspot/testing/metrics.py`](file:///d:/BlindSpot/blindspot/testing/metrics.py) | Diagnostic mathematical metrics calculation | `compute_flip_rate()`, `compute_ece()` |
| [`blindspot/explainability/__init__.py`](file:///d:/BlindSpot/blindspot/explainability/__init__.py) | Explainability subpackage exporter | Explainers, alignment, taxonomy, token attributions |
| [`blindspot/explainability/lime_explainer.py`](file:///d:/BlindSpot/blindspot/explainability/lime_explainer.py) | LIME token attribution extractor + positional records & seed support | `LimeExplainerWrapper` |
| [`blindspot/explainability/shap_explainer.py`](file:///d:/BlindSpot/blindspot/explainability/shap_explainer.py) | SHAP token attribution extractor + positional records & LOO fallback | `ShapExplainerWrapper` |
| [`blindspot/explainability/token_attributions.py`](file:///d:/BlindSpot/blindspot/explainability/token_attributions.py) | Occurrence-aware attribution preservation & sequence alignment | `TokenAttributionsDict`, `align_token_attributions()`, `extract_words_with_positions()` |
| [`blindspot/explainability/alignment.py`](file:///d:/BlindSpot/blindspot/explainability/alignment.py) | Top-K Jaccard & Cosine attribution alignment | `compute_jaccard_similarity()`, `compute_attribution_cosine()` |
| [`blindspot/explainability/taxonomy.py`](file:///d:/BlindSpot/blindspot/explainability/taxonomy.py) | 3-way failure classifier & remediation adviser | `TaxonomyClassifier` |
| [`blindspot/reporting/__init__.py`](file:///d:/BlindSpot/blindspot/reporting/__init__.py) | Reporting subpackage exporter | `ReportGenerator`, `Visualizer` |
| [`blindspot/reporting/report_generator.py`](file:///d:/BlindSpot/blindspot/reporting/report_generator.py) | Automated Markdown diagnostic compiler | `ReportGenerator` |
| [`blindspot/reporting/visualizer.py`](file:///d:/BlindSpot/blindspot/reporting/visualizer.py) | Publication-grade Matplotlib chart generator | `Visualizer` |
| [`tests/test_behavioral.py`](file:///d:/BlindSpot/tests/test_behavioral.py) | Tests for behavioral metrics & input validation | 3 test functions |
| [`tests/test_explainability.py`](file:///d:/BlindSpot/tests/test_explainability.py) | Tests for LIME, SHAP, alignment, taxonomy & UI narratives | 4 test functions |
| [`tests/test_models.py`](file:///d:/BlindSpot/tests/test_models.py) | Tests for Hugging Face wrapper & probability shapes | 1 test function |
| [`tests/test_perturbations.py`](file:///d:/BlindSpot/tests/test_perturbations.py) | Tests for perturbers, linguistic analyzer & engine | 6 test functions |
| [`tests/test_repeated_tokens.py`](file:///d:/BlindSpot/tests/test_repeated_tokens.py) | Tests for occurrence-aware repeated tokens & attribution alignment | 4 test functions |
| [`tests/test_reports.py`](file:///d:/BlindSpot/tests/test_reports.py) | Tests for Markdown report file generation | 1 test function |
| [`tests/test_visualizer.py`](file:///d:/BlindSpot/tests/test_visualizer.py) | Tests for Matplotlib figure generation | 1 test function |

---

## 3. Detailed File-by-File Breakdown

### 3.1 Root Configuration & Infrastructure Files

#### [`setup.py`](file:///d:/BlindSpot/setup.py)
- **Purpose**: Defines the packaging specification for BlindSpot, making it installable via `pip install -e .`.
- **Key Elements**:
  - `find_packages()`: Automatically detects the `blindspot` package and all child subpackages.
  - Package metadata: Name (`blindspot`), version (`0.1.0`), author.
  - Dependencies: References core libraries (PyTorch, Transformers, spaCy, NLTK, LIME, SHAP, Matplotlib, Streamlit).
- **Execution Role**: Used during environment setup so that `import blindspot` works globally in any directory.

#### [`requirements.txt`](file:///d:/BlindSpot/requirements.txt)
- **Purpose**: Specifies exact package dependencies and version constraints for reproducible environments.
- **Included Libraries**:
  - `transformers>=4.30.0`, `torch>=2.0.0`, `huggingface_hub`: Transformer neural network execution and pretrained weights downloading.
  - `spacy>=3.5.0`, `nltk>=3.8.1`: Linguistic analysis, dependency parsing, WordNet synset lookup, and SentiWordNet scoring.
  - `lime>=0.2.0.1`, `shap>=0.42.0`: Local feature attribution and game-theoretic Shapley values.
  - `pandas>=2.0.0`, `numpy>=1.24.0`, `scikit-learn>=1.2.0`: Numerical matrix manipulation and metric evaluation.
  - `matplotlib>=3.7.0`: Publication-grade chart generation.
  - `pytest>=7.3.0`, `pytest-cov>=4.1.0`: Automated unit testing framework.
  - `streamlit>=1.24.0`: Interactive web dashboard.
  - `mkdocs>=1.4.0`, `mkdocs-material>=9.1.0`: Technical documentation server.

#### [`run.ps1`](file:///d:/BlindSpot/run.ps1)
- **Purpose**: A unified PowerShell launcher providing single-command convenience for running the CLI, web dashboard, unit test suite, and documentation server.
- **Key Parameters**:
  - `-Mode`: Execution mode: `"cli"`, `"dashboard"`, `"test"`, `"docs"`, or `"help"`. Default is `"cli"`.
  - `-Sentence`: Custom input string to audit when running in `"cli"` mode.
  - `-Model`: Hugging Face model repository ID (default: `distilbert-base-uncased-finetuned-sst-2-english`).
  - `-Explainer`: Attribution method: `"lime"`, `"shap"`, or `"both"`.
  - `-OutputDir`: Target folder for reports (default: `audit_reports`).
- **Internal Logic**: Sets working directory to script root, suppresses unauthorized path anomalies, and branches to `python -m blindspot.cli`, `streamlit run`, `python run_tests.py`, or `mkdocs serve`.

#### [`run_tests.py`](file:///d:/BlindSpot/run_tests.py)
- **Purpose**: Standalone test suite execution script utilizing Python's built-in `unittest` runner. Runs 14 unit tests across the entire framework without requiring external pytest plugins.
- **Key Class**:
  - `TestBlindSpotFramework(unittest.TestCase)`: Wraps all unit test functions across perturbations, linguistic analyzer (`test_05b_linguistic_analyzer`), models, behavioral metrics, explainability, reports, and visualizer.
  - Isolates report and visualizer tests inside temporary directories (`tempfile.TemporaryDirectory`) to avoid overwriting production audit outputs.

#### [`mkdocs.yml`](file:///d:/BlindSpot/mkdocs.yml)
- **Purpose**: Static documentation site configuration file for MkDocs.
- **Key Configuration**:
  - Theme: `material` with dark/light mode toggle.
  - Navigation hierarchy:
    - Overview: `docs/index.md`
    - Architecture: `docs/architecture.md`
    - Failure Taxonomy: `docs/taxonomy.md`
    - User Guide: `docs/usage.md`
    - Python API: `docs/api.md`

#### [`srs.pdf`](file:///d:/BlindSpot/srs.pdf)
- **Purpose**: Software Requirements Specification reference document defining the project requirements, academic objectives, failure taxonomy specifications, and system architectural constraints.

#### [`IMPLEMENTATION_STEPS.md`](file:///d:/BlindSpot/IMPLEMENTATION_STEPS.md)
- **Purpose**: Comprehensive step-by-step implementation guide recording the development roadmap, software dependencies, architectural milestones (Phase 1: Scaffolding to Phase 6: Web Dashboard & Documentation), and verification checklists.

#### [`PROJECT_STATE_REPORT.md`](file:///d:/BlindSpot/PROJECT_STATE_REPORT.md)
- **Purpose**: Complete architectural and state specification report auditing the repository against all SRS functional and non-functional requirements (§1.1 through §4.7), establishing 100% compliance across all subsystems.

#### [`project_questions_and_doubts.md`](file:///d:/BlindSpot/project_questions_and_doubts.md)
- **Purpose**: Persistent technical Q&A and viva defense log tracking 21 key architectural questions (Q1–Q21), design choices, mathematical metric justifications, and theoretical explanations for project presentations.

#### [`DIAGNOSTIC_GRAPHS_GUIDE.md`](file:///d:/BlindSpot/DIAGNOSTIC_GRAPHS_GUIDE.md)
- **Purpose**: Dedicated reference guide explaining all 4 Matplotlib diagnostic charts generated by the visualizer (`behavioral_metrics.png`, `taxonomy_distribution.png`, `attribution_comparison.png`, `probe_alignment_summary.png`).
- **Key Sections**:
  - Detailed visual anatomy, colors, and axes specifications for each chart.
  - Complete mathematical formulations (Flip Rate, 10-bin ECE, LIME surrogate regression, SHAP Shapley values, Top-5 Jaccard overlap, Cosine angle equation).
  - Practical case study on real audit run tracking exact empirical scores.
  - Viva and defense scripts for presenting each chart during evaluations.

---

### 3.2 Core Package: `blindspot/`

#### [`blindspot/__init__.py`](file:///d:/BlindSpot/blindspot/__init__.py)
- **Purpose**: Declares `blindspot` as a top-level Python package, sets `__version__ = "0.1.0"`, and exposes top-level entrypoints (`AuditPipeline`, `HuggingFaceWrapper`).
- **Safety Feature**: Globally suppresses non-critical third-party deprecation noise (PyTorch `set_bad`, Transformers `WordPiece` warnings) to ensure clean console logs.

#### [`blindspot/audit.py`](file:///d:/BlindSpot/blindspot/audit.py)
- **Purpose**: Master orchestrator coordinating all subpackages to execute the 5-stage auditing workflow.
- **Key Class**: `AuditPipeline`
  - `__init__(model_name_or_path, output_dir, explainer_type, confidence_threshold=0.65, random_seed=42)`: Initializes model wrapper, perturbation engine, behavioral tester, explainers (with deterministic `random_seed`), taxonomy classifier, and report generator.
  - `validate_input(sentence, min_length=3, max_length=500) -> str`: Strict pre-audit input sanitizer. Checks type (`str`), non-emptiness, presence of alphabetic characters, and length limits (3 to 500 characters). Rejects invalid inputs with clear error messages.
  - `check_suitability(sentence) -> Dict[str, Any]`: Analyzes valid input for completeness and emotional clarity. Flags ambiguous phrases ($\le 2$ words) or neutral words (`normal`, `okay`, `average`) without halting execution, attaching suitability warning metadata.
  - `_get_explanation(text) -> Dict[str, float]`: Dynamically routes token attribution extraction to LIME, SHAP, or an ensemble average (`"both"`).
  - `run_audit(sentence) -> Dict[str, Any]`: Executes the complete pipeline:
    1. Sanitizes and validates input.
    2. Generates linguistic variants via `PerturbationEngine`.
    3. Runs behavioral evaluation and confidence tracking via `BehavioralTester`.
    4. Computes token attributions and pairwise alignment (Jaccard & Cosine) plus sequence-based token alignment via `align_token_attributions()`.
    5. Evaluates failure taxonomy rules via `TaxonomyClassifier`.
    6. Decorates detected failures with comprehensive probe context, original/perturbed labels, confidences, confidence deltas, and token-level attribution records (`aligned_tokens`, `orig_token_attributions`, `pert_token_attributions`).
    7. Generates Markdown documents and Matplotlib charts via `ReportGenerator`.

#### [`blindspot/cli.py`](file:///d:/BlindSpot/blindspot/cli.py)
- **Purpose**: Command-line entrypoint for headless environments, automated shell scripts, and CI/CD pipelines.
- **Key Function**: `main()`
  - Uses `argparse` to handle `--model`, `--sentence`, `--output-dir`, and `--explainer`.
  - Instantiates `AuditPipeline`, executes `run_audit()`, and outputs high-level summary statistics to standard output (Flip Rate, Detected Failures, paths of generated `.md` reports).

#### [`blindspot/app.py`](file:///d:/BlindSpot/blindspot/app.py)
- **Purpose**: Interactive graphical user interface built with Streamlit.
- **Key Helper Functions & UI Components**:
  - `render_markdown_with_images(content, base_dir="audit_reports")`: Parses markdown content and intercepts local image syntax (`![alt](path)`), rendering high-resolution figures directly inside Streamlit with `st.image(..., use_container_width=True)`.
  - `resolve_failure_metadata(fail, beh_probes, original_text, orig_pred, orig_conf) -> dict`: Robustly reconstructs and resolves complete probe context for every detected failure, calculating percentage-point confidence deltas ($\Delta_{\text{conf}}$) and resolving aligned tokens.
  - `find_key_misweighted_token(aligned_tokens, orig_exp, pert_exp) -> dict`: Analyzes aligned token rows to pinpoint the exact token occurrence causing attribution polarity inversion ($+\rightarrow -$ or $-\rightarrow +$) or exhibiting the maximum absolute weight shift, preserving position and occurrence identity.
  - `generate_attribution_interpretation(p_type, pert_label, pert_exp, orig_exp, key_ev) -> str`: Translates raw numerical attribution scores into clear, scientifically sound explanations connecting feature importance to observed behavioral failures.
  - `get_failure_narrative(category, p_type, orig_label, pert_label, is_flipped, expected_flip) -> dict`: Synthesizes intermediate-level scientific titles, test descriptions, root cause diagnostics, and actionable remediation steps tailored for students, researchers, and viva defense.
- **Four Structured Tabs**:
  1. *Diagnostic Visualizations*: 2x2 grid displaying high-resolution Matplotlib figures.
  2. *Perturbation Matrix*: Interactive data table listing all generated variants, original labels, perturbed labels, flip flags, and unexpected behavior flags.
  3. *Failure Taxonomy & Reports*: Expandable diagnostic failure cards featuring badge indicators, scientific explanations, token-level attribution diff tables with occurrence indices, and rendered Markdown reports with instant `⬇️ Download` buttons.
  4. *Technical Documentation*: In-app live reader for MkDocs markdown files.

---

### 3.3 Model Layer: `blindspot/models/`

#### [`blindspot/models/__init__.py`](file:///d:/BlindSpot/blindspot/models/__init__.py)
- **Purpose**: Subpackage initializer exporting `HuggingFaceWrapper`.

#### [`blindspot/models/huggingface_wrapper.py`](file:///d:/BlindSpot/blindspot/models/huggingface_wrapper.py)
- **Purpose**: Provides a standardized, model-agnostic classification wrapper around Hugging Face sequence classification pipelines.
- **Key Class**: `HuggingFaceWrapper`
  - `__init__(model_name_or_path)`: Loads Hugging Face pipeline using `pipeline("text-classification", model=..., top_k=None)`. Resolves label mapping (`id2label`) to support variable class labels (`POSITIVE`, `NEGATIVE`, `LABEL_0`, `LABEL_1`).
  - `predict_proba(texts: Union[str, List[str], np.ndarray]) -> np.ndarray`:
    - Sanitizes input types (converts NumPy arrays, single strings, or iterables into clean Python strings).
    - Queries the model pipeline and extracts probability scores for each class.
    - Applies normalization ($\sum p_i = 1.0$) to guarantee valid probability distributions.
    - Returns a 2D NumPy array of shape $(N, \text{num\_classes})$.
  - **Zero-Crash Heuristic Fallback**: If Hugging Face is unreachable, if the user is offline, or if GPU/CPU loading fails, the class automatically falls back to an internal lexicon-based probabilistic classifier. This guarantees that the entire BlindSpot framework, UI, and test suite run without crashing.
  - `predict(texts) -> List[str]`: Convenience method returning the argmax string label for each input text.

---

### 3.4 Perturbations Layer: `blindspot/perturbations/`

#### [`blindspot/perturbations/__init__.py`](file:///d:/BlindSpot/blindspot/perturbations/__init__.py)
- **Purpose**: Subpackage initializer exposing `BasePerturber`, `NegationPerturber`, `DoubleNegationPerturber`, `ConnectivePerturber`, `SynonymSubstitutionPerturber`, `PerturbationEngine`, `LinguisticAnalyzer`, and `SentenceFeatures`.

#### [`blindspot/perturbations/base.py`](file:///d:/BlindSpot/blindspot/perturbations/base.py)
- **Purpose**: Defines the abstract base class `BasePerturber` using Python's `abc` module.
- **Key Elements**:
  - `__init__(name: str, perturbation_type: str)`: Stores metadata name and type identifier.
  - `@abstractmethod perturb(sentence: str) -> List[Dict[str, Any]]`: Enforces a uniform contract across all mutation engines. Every variant returned must include:
    - `"original"`: Source sentence string.
    - `"perturbed"`: Mutated sentence string.
    - `"type"`: Specific perturbation identifier (e.g., `"negation_insertion"`, `"contrast_negative_append"`).
    - `"description"`: Human-readable explanation of the transformation.

#### [`blindspot/perturbations/linguistic_analyzer.py`](file:///d:/BlindSpot/blindspot/perturbations/linguistic_analyzer.py)
- **Purpose**: Performs syntactic deconstruction, morphological analysis, animacy typing, and lexical semantics via spaCy (`en_core_web_sm`) and NLTK, enabling context-aware, grammatically coherent perturbations without selectional restriction violations.
- **Key Dataclass**: `SentenceFeatures`
  - Encapsulates linguistic properties: `tokens`, `pos_tags`, `subject`, `pronoun`, `possessive_pronoun`, `is_plural`, `is_past_tense`, `copula`, `negative_copula`, `aux_do`, `aux_do_not`, `root_lemma`, `direct_object`, `is_human_agent`, `is_human_object`, `entity_domain` (`human`, `weather`, `food`, `media`, `service`, `tech`, `general`), `descriptor`, `descriptor_pos`, `descriptor_lemma`, `is_negative_sentiment`, `antonyms`, and `noun_chunks`.
- **Key Class**: `LinguisticAnalyzer`
  - `_ensure_resources()`: Automatically verifies and downloads required NLTK corpora (`punkt_tab`, `averaged_perceptron_tagger_eng`, `wordnet`, `sentiwordnet`, `vader_lexicon`).
  - `_init_spacy()`: Loads or downloads `en_core_web_sm`.
  - `is_human_entity(token_text, ent_type) -> bool`: Determines animacy using personal pronouns, spaCy NER tags (`PERSON`, `NORP`), and NLTK WordNet hypernym paths tracing to `person.n.01`.
  - `detect_entity_domain(text, is_human) -> str`: Classifies sentence domain based on keyword clusters and animacy.
  - `is_negative_word(word, pos_tag) -> bool` & `get_word_sentiment(word, pos_tag) -> float`: Evaluates net sentiment score using NLTK SentiWordNet synsets.
  - `get_ranked_opposites(word, pos_tag) -> List[str]`: Queries WordNet synset lemmas and satellite synsets (`similar_tos`), ranking candidate antonyms by degree of SentiWordNet polarity inversion.
  - `extract_features(sentence) -> SentenceFeatures`: Performs full syntactic dependency parsing and morphological feature extraction with an automated regex-based fallback if spaCy is unavailable.

#### [`blindspot/perturbations/negation.py`](file:///d:/BlindSpot/blindspot/perturbations/negation.py)
- **Purpose**: Generates single negation and litotes double negation linguistic variants.
- **Helper Functions**:
  - `_clean_text(text)`: Regex sanitizer eliminating duplicate spaces, space before punctuation, and space after hyphens.
  - `_format_subject(sentence)`: Adjusts grammatical capitalization when embedding clauses, preserving uppercase `"I"` pronouns.
- **Key Classes**:
  1. `NegationPerturber(BasePerturber)`:
     - Detects auxiliary verbs (`is`, `was`, `are`, `can`, `could`, `would`, `should`, `has`, `had`, `feels`, `seems`) and injects `"not"` immediately after the verb.
     - If the sentence already contains negation (`not`, `never`, `n't`), it removes the negation operator to test inverse sensitivity.
     - If no auxiliary verb is matched, it applies an explicit negation frame: `"It is not true that [sentence]"`.
     - *Expected Model Behavior*: **Directional flip** (sentiment must invert).
  2. `DoubleNegationPerturber(BasePerturber)`:
     - Constructs natural English litotes structures:
       - Variant 1: `"It is not impossible that [sentence]"`
       - Variant 2: `"It is not untrue that [sentence]"`
     - *Expected Model Behavior*: **Invariant stability** (semantic polarity is preserved; prediction must not flip).

#### [`blindspot/perturbations/connectives.py`](file:///d:/BlindSpot/blindspot/perturbations/connectives.py)
- **Purpose**: Generates context-aware discourse-level contrastive connectives and concession clauses grounded in input semantics using `LinguisticAnalyzer`, completely eliminating static review templates ("complete garbage", "overall experience was outstanding") that cause selectional restriction violations.
- **Key Class**: `ConnectivePerturber(BasePerturber)`
  - `__init__()`: Initializes `LinguisticAnalyzer` for syntactic and semantic grounding.
  - `_build_positive_contrast(clean_sentence, features)`: Dynamically generates positive contrast grounded in the entity domain (e.g., human agent: `"and she displayed remarkable skill"`; weather: `"but staying indoors is comfortable"`; negative input redemption: `"but it was genuinely [opposite] in practice"`).
  - `_build_negative_contrast(clean_sentence, features)`: Constructs context-grounded negative contrast and concession predicates respecting transitivity, competition verbs, plural agreements, and animacy (e.g., `"however she could not defeat him consistently"` / `"she struggled in the rematch"`).
  - *Expected Model Behavior*:
    - In standard discourse semantics, the subordinate clause following `"however"` or `"but"` carries the dominant discourse weight. Models that over-rely on initial tokens fail to recognize the contrastive shift.

#### [`blindspot/perturbations/substitution.py`](file:///d:/BlindSpot/blindspot/perturbations/substitution.py)
- **Purpose**: Generates semantically invariant synonym substitutions targeting content words while strictly preserving pronouns and stopwords.
- **Key Class**: `SynonymSubstitutionPerturber(BasePerturber)`
  - `stop_words`: Comprehensive set of 60+ English functional tokens (`i`, `me`, `my`, `you`, `they`, `is`, `was`, `the`, `and`, `to`, `for`) excluded from substitution.
  - `synonym_map`: Curated dictionary of high-frequency sentiment terms (`awesome` $\rightarrow$ `impressive`, `great` $\rightarrow$ `fantastic`, `bad` $\rightarrow$ `subpar`, `movie` $\rightarrow$ `film`).
  - `_match_case(original, replacement)`: Matches original capitalization (`"Awesome"` $\rightarrow$ `"Impressive"`, `"AWESOME"` $\rightarrow$ `"IMPRESSIVE"`).
  - `_get_nltk_synonyms(word)`: Fallback method querying NLTK WordNet synsets for lemma synonyms ($\ge 3$ characters, alphabetic only).
  - *Expected Model Behavior*: **Invariant stability** (prediction label should remain identical).

#### [`blindspot/perturbations/engine.py`](file:///d:/BlindSpot/blindspot/perturbations/engine.py)
- **Purpose**: Aggregates all perturbers into a unified generator.
- **Key Class**: `PerturbationEngine`
  - Instantiates `NegationPerturber`, `DoubleNegationPerturber`, `ConnectivePerturber`, and `SynonymSubstitutionPerturber`.
  - `generate_all(sentence: str) -> List[Dict[str, Any]]`: Iterates over each perturber, collecting and returning the complete list of 7 controlled linguistic variants.

---

### 3.5 Testing & Metrics Layer: `blindspot/testing/`

#### [`blindspot/testing/__init__.py`](file:///d:/BlindSpot/blindspot/testing/__init__.py)
- **Purpose**: Subpackage initializer exporting `BehavioralTester`, `compute_flip_rate`, and `compute_ece`.

#### [`blindspot/testing/metrics.py`](file:///d:/BlindSpot/blindspot/testing/metrics.py)
- **Purpose**: Pure mathematical implementations of behavioral auditing metrics.
- **Key Functions**:
  1. `compute_flip_rate(original_label: str, perturbed_labels: List[str]) -> float`:
     - Calculates the empirical fraction of perturbed probes where predicted label $\ne$ original label:
       $$\text{Flip Rate} = \frac{\sum_{i=1}^N \mathbb{I}(\hat{y}_{\text{pert}, i} \ne \hat{y}_{\text{orig}})}{N}$$
  2. `compute_ece(confidences: np.ndarray, predictions: np.ndarray, labels: np.ndarray, n_bins: int = 10) -> float`:
     - Calculates Expected Calibration Error across $B=10$ equal-width probability bins between $0.0$ and $1.0$:
       $$\text{ECE} = \sum_{b=1}^B \frac{|B_b|}{N} \left| \text{acc}(B_b) - \text{conf}(B_b) \right|$$
     - Measures whether the model's confidence scores accurately reflect empirical prediction accuracy.

#### [`blindspot/testing/behavioral.py`](file:///d:/BlindSpot/blindspot/testing/behavioral.py)
- **Purpose**: Evaluates model behavioral responses across original and perturbed probes.
- **Key Class**: `BehavioralTester`
  - `__init__(model_wrapper: HuggingFaceWrapper)`: Binds the target model interface.
  - `evaluate_probe(original_text, perturbed_items) -> Dict[str, Any]`:
    - Runs inference on original text and extracts predicted class label and baseline confidence.
    - Evaluates each perturbed text, calculating:
      - `is_flipped`: Whether the prediction label changed.
      - `expected_flip`: Directional expectation (`True` for single negation and negative contrast; `False` for litotes and synonyms).
      - `unexpected_behavior`: Flagged when `is_flipped != expected_flip`.
      - `confidence_delta`: $\Delta_{\text{conf}} = \text{conf}_{\text{pert}} - \text{conf}_{\text{orig}}$.
    - Computes aggregate `flip_rate` and `ece`.
    - Returns structured dictionary consumed by report generator and taxonomy classifier.

---

### 3.6 Explainability Layer: `blindspot/explainability/`

#### [`blindspot/explainability/__init__.py`](file:///d:/BlindSpot/blindspot/explainability/__init__.py)
- **Purpose**: Subpackage initializer exposing `LimeExplainerWrapper`, `ShapExplainerWrapper`, `TaxonomyClassifier`, `TokenAttributionsDict`, `align_token_attributions`, `compute_jaccard_similarity`, and `compute_attribution_cosine`.

#### [`blindspot/explainability/token_attributions.py`](file:///d:/BlindSpot/blindspot/explainability/token_attributions.py)
- **Purpose**: Solves the repeated words token collision problem and provides sequence-aligned attribution tracking across mutations.
- **Key Classes & Functions**:
  1. `TokenAttributionsDict(dict)`:
     - Subclasses standard Python dictionary to maintain 100% backward compatibility for dictionary-style lookups (`dict[word]`), while encapsulating a structured `token_attributions` list of dictionaries containing individual token records (`token`, `position`, `occurrence`, `attribution`).
  2. `extract_words_with_positions(text: str) -> List[Dict[str, Any]]`:
     - Tokenizes text using word boundary regular expressions (`\b\w+\b`) and computes 1-based sequential word positions, running occurrence counters for repeated words (`occurrence`), and character span indices (`char_start`, `char_end`).
  3. `align_token_attributions(orig_text, pert_text, orig_exp, pert_exp) -> List[Dict[str, Any]]`:
     - Uses Python's `difflib.SequenceMatcher` to perform structural sequence alignment between original and perturbed token sequences.
     - Categorizes aligned pairs into `aligned`, `inserted`, and `removed` statuses.
     - Preserves occurrence identity, tracks numerical attribution shift (`delta = pert_val - orig_val`), detects polarity inversions (`polarity_changed`), and identifies the key misweighted attribution shift (`is_key_shift`).

#### [`blindspot/explainability/lime_explainer.py`](file:///d:/BlindSpot/blindspot/explainability/lime_explainer.py)
- **Purpose**: Extracts local token-level feature attributions using LIME (Local Interpretable Model-agnostic Explanations) with position-aware token packaging and deterministic random seed support.
- **Key Class**: `LimeExplainerWrapper`
  - `__init__(model_wrapper, random_seed=42)`: Initializes explainer with specified random seed for reproducible neighborhood perturbations.
  - `explain(text: str, num_features: int = 10) -> TokenAttributionsDict`:
    - Perturbs local neighborhood (100 samples) and fits an interpretable linear surrogate model.
    - Safely handles available label indices to prevent dictionary `KeyError` exceptions.
    - Constructs and returns a `TokenAttributionsDict` packaging both dictionary weights and positional token records.
  - `_leave_one_out_explain(text: str) -> TokenAttributionsDict`: Robust fallback mechanism measuring probability drops upon masking individual words.

#### [`blindspot/explainability/shap_explainer.py`](file:///d:/BlindSpot/blindspot/explainability/shap_explainer.py)
- **Purpose**: Extracts cooperative game-theoretic Shapley value attributions for tokens using SHAP with multidimensional tensor handling.
- **Key Class**: `ShapExplainerWrapper`
  - `_init_explainer()`: Initializes `shap.Explainer` with a text masker (`shap.maskers.Text()`) and an adapter prediction function.
  - `explain(text: str) -> TokenAttributionsDict`:
    - Computes Shapley additive explanations across token coalitions.
    - Robustly handles multi-dimensional output array shapes (1D, 2D, and 3D tensors) across different SHAP library versions.
    - Returns a `TokenAttributionsDict` preserving token positions and attributions.
  - `_leave_one_out_explain(text: str) -> TokenAttributionsDict`: Provides zero-dependency Leave-One-Out Shapley approximation if SHAP initialization fails.

#### [`blindspot/explainability/alignment.py`](file:///d:/BlindSpot/blindspot/explainability/alignment.py)
- **Purpose**: Quantifies feature attribution shifts between original and perturbed inputs using two distinct geometric metrics.
- **Key Functions**:
  1. `compute_jaccard_similarity(exp1, exp2, top_k=5) -> float`:
     - Extracts Top-$K$ most important tokens (by absolute attribution weight) from both explanations and calculates set intersection over union:
       $$\text{Jaccard}(S_1, S_2) = \frac{|S_1 \cap S_2|}{|S_1 \cup S_2|}$$
  2. `compute_attribution_cosine(exp1, exp2) -> float`:
     - Aligns attribution weights into vector representations over the shared vocabulary and computes cosine similarity:
       $$\text{Cosine}(\vec{v}_1, \vec{v}_2) = \frac{\vec{v}_1 \cdot \vec{v}_2}{\|\vec{v}_1\| \|\vec{v}_2\|}$$

#### [`blindspot/explainability/taxonomy.py`](file:///d:/BlindSpot/blindspot/explainability/taxonomy.py)
- **Purpose**: Implements the 3-Way Failure Taxonomy defined in the project specification, classifying model audit failures and prescribing actionable training remediations.
- **Key Class**: `TaxonomyClassifier`
  - `classify_failure(...) -> Optional[Dict[str, Any]]`:
    - **1. Blind Failure**: Single negation inserted, but model prediction fails to flip (`is_flipped == False`). Recommendation: Fine-tune on CheckList negation suites and adjust attention head weights on syntactic modifiers.
    - **2. Spurious Failure**: Top attribution tokens belong exclusively to generic domain nouns (`movie`, `book`, `film`) rather than sentiment adjectives. Recommendation: Apply adversarial entity replacement during fine-tuning.
    - **3. Misweighted Failure**: Contrastive clauses (`however...`) or synonym swaps cause unexpected label flips or invert attribution polarities. Recommendation: Augment training data with contrastive clause pairs (`X, but Y`) and apply embedding regularization.

---

### 3.7 Reporting & Visualization Layer: `blindspot/reporting/`

#### [`blindspot/reporting/__init__.py`](file:///d:/BlindSpot/blindspot/reporting/__init__.py)
- **Purpose**: Subpackage initializer exporting `ReportGenerator` and `Visualizer`.

#### [`blindspot/reporting/report_generator.py`](file:///d:/BlindSpot/blindspot/reporting/report_generator.py)
- **Purpose**: Compiles audit metrics, probe details, explanations, and figure links into four structured Markdown reports.
- **Key Class**: `ReportGenerator`
  - `__init__(output_dir="audit_reports")`: Prepares output directories (`audit_reports/` and `audit_reports/probes/`) and initializes the visualizer.
  - `generate_all_reports(model_name, audit_results, failures, explanations_summary) -> List[str]`:
    - Generates all Matplotlib charts first via `Visualizer`.
    - Generates the 4 required report documents:
      1. `model_behavior_report.md`: High-level executive summary detailing input sentence, original prediction, flip rate %, ECE, suitability status, failure summary table, and embedded figures.
      2. `failure_summary.md`: Detailed list of every detected failure, root cause category, and actionable training recommendations.
      3. `explanation_comparison.md`: Token attribution weights comparison, Jaccard scores, and Cosine alignment across probes.
      4. `probes/probe_<id>.md`: Deep diagnostic logs for each individual probe ($P_1 \dots P_7$) detailing input comparison, label change, confidence delta, and token weights.

#### [`blindspot/reporting/visualizer.py`](file:///d:/BlindSpot/blindspot/reporting/visualizer.py)
- **Purpose**: Generates publication-grade Matplotlib diagnostic charts saved to `audit_reports/figures/`.
- **Key Features & Methods**:
  - Sets `matplotlib.use('Agg')` for headless execution in scripts, servers, and Docker containers without GUI displays.
  - `plot_taxonomy_distribution(failures, filename)`: Donut Chart displaying proportions of Blind, Spurious, and Misweighted failures (renders a unified solid green `"100% Robust"` donut when zero failures occur).
  - `plot_behavioral_metrics(flip_rate, ece, filename)`: Horizontal Bar Chart showing Prediction Flip Rate (%) and ECE ($\times 100$).
  - `plot_attribution_comparison(explanations_summary, filename)`: Side-by-side comparative bar chart showing original vs perturbed token attributions for Probe #1.
  - `plot_probe_alignment_summary(explanations_summary, filename)`: Dual-grouped bar chart comparing Jaccard Top-K Similarity and Cosine Attribution Alignment across all probes ($P_1 \dots P_7$).

---

### 3.8 Automated Pytest Suite: `tests/`

#### [`tests/test_behavioral.py`](file:///d:/BlindSpot/tests/test_behavioral.py)
- **Test Functions**:
  - `test_metrics()`: Verifies `compute_flip_rate()` returns $0.5$ on balanced predictions, and `compute_ece()` produces valid calibration values between $0.0$ and $1.0$.
  - `test_behavioral_tester()`: Evaluates `BehavioralTester` on sample probes, ensuring output keys (`flip_rate`, `ece`, `probe_details`) exist and match expected types.
  - `test_input_validation_and_suitability()`: Checks 8 edge cases: pure numeric rejection, punctuation rejection, incomplete phrase warnings, neutral word warnings, sentiment text acceptance, numeric context acceptance, rating acceptance, and natural text preservation.

#### [`tests/test_explainability.py`](file:///d:/BlindSpot/tests/test_explainability.py)
- **Test Functions**:
  - `test_explainers()`: Runs `LimeExplainerWrapper` and `ShapExplainerWrapper` on test text, ensuring non-empty attribution dicts, $0 \le \text{Jaccard} \le 1$, and $-1 \le \text{Cosine} \le 1$.
  - `test_audit_pipeline_explainer_selection()`: Tests `AuditPipeline` running in `"lime"`, `"shap"`, and `"both"` modes.
  - `test_taxonomy_classifier()`: Simulates an un-flipped negation probe and asserts that `TaxonomyClassifier` identifies a `Blind` failure.
  - `test_taxonomy_ui_presentation()`: Verifies failure metadata resolution (`resolve_failure_metadata`) and failure narrative formatting (`get_failure_narrative`) for Blind, Double Negation, and Misweighted failure instances.

#### [`tests/test_models.py`](file:///d:/BlindSpot/tests/test_models.py)
- **Test Functions**:
  - `test_huggingface_wrapper()`: Verifies that `predict_proba()` returns a 2D NumPy array of shape $(1, K)$, probabilities sum to $1.0 \pm 10^{-3}$, and `predict()` returns valid class labels.

#### [`tests/test_perturbations.py`](file:///d:/BlindSpot/tests/test_perturbations.py)
- **Test Functions**:
  - `test_negation_perturber()`: Asserts single negation generates $\ge 1$ variant containing `"not"`.
  - `test_double_negation_perturber()`: Asserts litotes double negation generates valid variants.
  - `test_connective_perturber()`: Asserts generation of positive contrast, negative contrast, and concession clauses while strictly guaranteeing complete elimination of hardcoded static phrases ("complete garbage", "overall experience was outstanding").
  - `test_synonym_substitution_perturber()`: Asserts replacement of sentiment adjectives.
  - `test_perturbation_engine()`: Asserts aggregated engine produces $\ge 5$ total probe variants.
  - `test_linguistic_analyzer()`: Tests spaCy dependency parsing, plurality, past-tense copula resolution, descriptor extraction, and NLTK WordNet antonym retrieval across diverse sentence structures.

#### [`tests/test_repeated_tokens.py`](file:///d:/BlindSpot/tests/test_repeated_tokens.py)
- **Test Functions**:
  - `test_extract_words_with_positions()`: Verifies that sentences with repeated words (e.g., `"The movie was great and the acting was great."`) assign distinct 1-based positions and sequential occurrence numbers to each instance.
  - `test_align_token_attributions_repeated_words()`: Verifies that `align_token_attributions` correctly maintains distinct attribution weights for individual occurrences of words (position 4 vs position 9) and accurately classifies substituted tokens as `removed` and `inserted`.
  - `test_contrast_repeated_words()`: Verifies word position and occurrence indexing under complex contrastive sentences.
  - `test_find_key_misweighted_token_occurrence_awareness()`: Verifies that `find_key_misweighted_token` identifies the specific occurrence of a repeated token that flipped polarity or underwent the largest attribution shift.

#### [`tests/test_reports.py`](file:///d:/BlindSpot/tests/test_reports.py)
- **Test Functions**:
  - `test_report_generator(tmp_path)`: Mocks audit results and verifies that `ReportGenerator` creates all 4 Markdown files and that all files exist on disk with non-zero size.

#### [`tests/test_visualizer.py`](file:///d:/BlindSpot/tests/test_visualizer.py)
- **Test Functions**:
  - `test_visualizer_generate_all_plots(tmp_path)`: Verifies that `Visualizer` renders all 4 chart PNGs (`taxonomy_distribution`, `behavioral_metrics`, `attribution_comparison`, `probe_alignment`) with non-zero byte size.

---

### 3.9 Documentation Suite: `docs/`

- [`docs/index.md`](file:///d:/BlindSpot/docs/index.md): System overview, feature highlights, installation instructions, and quick-start CLI examples.
- [`docs/architecture.md`](file:///d:/BlindSpot/docs/architecture.md): Complete pipeline architectural specifications detailing data flow across the five subpackages.
- [`docs/taxonomy.md`](file:///d:/BlindSpot/docs/taxonomy.md): Formal definitions of the 3-Way Failure Taxonomy (**Blind**, **Spurious**, **Misweighted**), mathematical trigger conditions, and concrete remediation advice.
- [`docs/usage.md`](file:///d:/BlindSpot/docs/usage.md): Practical usage guide covering CLI options, Streamlit dashboard workflows, and PowerShell script usage.
- [`docs/api.md`](file:///d:/BlindSpot/docs/api.md): Complete Python API reference detailing classes, constructors, methods, and return signatures.

---

## 4. End-to-End Execution Trace: Life of an Audit Request

To understand how these files cooperate at runtime, follow what occurs when a user audits the sentence:
`"This is an incredible movie."`

```text
Step 1: Ingestion & Sanitization (blindspot/audit.py)
  ├── AuditPipeline.validate_input()
  │     └── Passes type check, length check (29 chars), alphabetic validity.
  └── AuditPipeline.check_suitability()
        └── Analyzes token count (5 words) -> Status: "SUITABLE" (No ambiguity).

Step 2: Perturbation Generation (blindspot/perturbations/engine.py & linguistic_analyzer.py)
  ├── LinguisticAnalyzer.extract_features()
  │     └── Extracts subject ("movie"), copula ("is"), descriptor ("incredible"), domain ("media").
  ├── NegationPerturber: Matches 'is' -> "This is not an incredible movie." (negation_insertion)
  ├── DoubleNegationPerturber: Litotes -> "It is not impossible that this is an incredible movie."
  ├── DoubleNegationPerturber: Litotes -> "It is not untrue that this is an incredible movie."
  ├── ConnectivePerturber: Context-aware positive append -> "This is an incredible movie, and the overall storyline was engaging."
  ├── ConnectivePerturber: Context-aware negative append -> "This is an incredible movie, however the plot lost direction halfway through."
  ├── ConnectivePerturber: Concession prefix -> "Although this is an incredible movie, it felt incomplete."
  └── SynonymSubstitutionPerturber: Curated swap -> "This is an impressive movie."

Step 3: Behavioral Testing (blindspot/testing/behavioral.py)
  ├── HuggingFaceWrapper.predict_proba("This is an incredible movie.")
  │     └── Model output: POSITIVE (99.98% confidence).
  ├── Loop over all 7 perturbed variants:
  │     ├── Variant 1 (negation): Prediction flips to NEGATIVE (99.85%) -> is_flipped=True (Expected!)
  │     ├── Variant 2 (litotes):  Prediction stays POSITIVE (99.91%)     -> is_flipped=False (Expected!)
  │     ├── Variant 3 (litotes):  Prediction stays POSITIVE (99.92%)     -> is_flipped=False (Expected!)
  │     ├── Variant 4 (contrast+): Prediction stays POSITIVE (99.95%)    -> is_flipped=False (Expected!)
  │     ├── Variant 5 (contrast-): Prediction flips to NEGATIVE (99.80%) -> is_flipped=True (Expected!)
  │     ├── Variant 6 (concession): Prediction flips to NEGATIVE (99.78%)-> is_flipped=True (Expected!)
  │     └── Variant 7 (synonym):  Prediction stays POSITIVE (99.96%)     -> is_flipped=False (Expected!)
  └── Metrics Calculation (blindspot/testing/metrics.py)
        ├── Flip Rate: 3 / 7 = 42.86%
        └── Expected Calibration Error (ECE): 0.0008

Step 4: Explainability & Occurrence-Aware Alignment (blindspot/explainability/)
  ├── LimeExplainerWrapper / ShapExplainerWrapper extracts token weights for original text:
  │     └── TokenAttributionsDict: {'incredible': +0.68, 'movie': +0.12, 'this': +0.02}
  ├── Loop over variants to extract perturbed token weights into TokenAttributionsDict:
  │     └── Variant 1: {'not': -0.54, 'incredible': +0.32, 'movie': +0.08}
  ├── align_token_attributions() computes sequence alignment preserving position & occurrence index.
  ├── compute_jaccard_similarity() and compute_attribution_cosine() quantify alignment.
  └── TaxonomyClassifier.classify_failure():
        └── Checks Blind, Spurious, and Misweighted conditions -> 0 Failures Detected (Model is robust).

Step 5: Diagnostic Report Generation (blindspot/reporting/)
  ├── Visualizer: Generates 4 publication PNG figures in audit_reports/figures/.
  ├── ReportGenerator: Writes model_behavior_report.md, failure_summary.md,
  │   explanation_comparison.md, and probes/probe_1.md through probe_7.md.
  └── Returns filepaths to caller:
        ├── CLI outputs summary table and report paths to standard output.
        └── Streamlit UI dynamically renders interactive metrics, aligned diff tables, and download buttons.
```

---

## 5. Architectural Summary & Design Patterns Used

1. **Model-Agnostic Adapter Pattern** ([`huggingface_wrapper.py`](file:///d:/BlindSpot/blindspot/models/huggingface_wrapper.py)):
   - Standardizes disparate third-party model inference outputs into a uniform `predict_proba()` contract.
2. **Strategy / Composite Pattern** ([`perturbations/`](file:///d:/BlindSpot/blindspot/perturbations)):
   - `BasePerturber` defines the strategy interface, and `PerturbationEngine` acts as the composite executor.
3. **Linguistic Feature Grounding** ([`linguistic_analyzer.py`](file:///d:/BlindSpot/blindspot/perturbations/linguistic_analyzer.py)):
   - Combines spaCy dependency parsing, animacy typing, and NLTK SentiWordNet lexical opposites to generate grammatically valid, contextually grounded mutations without selectional restriction errors.
4. **Position-Preserving Backward-Compatible Subclassing** ([`token_attributions.py`](file:///d:/BlindSpot/blindspot/explainability/token_attributions.py)):
   - `TokenAttributionsDict` subclasses Python's `dict` to provide seamless backward compatibility while carrying positional and occurrence metadata, solving the repeated words collision problem during token alignment.
5. **Graceful Degradation Pattern**:
   - Every single component that depends on heavy external machine learning packages (Transformers, LIME, SHAP, NLTK, spaCy) includes an automated, zero-crash fallback (LOO importance, heuristic probabilities, regex tokenizer fallbacks, curated dictionaries).
6. **Separation of Concerns**:
   - Testing logic (`testing/`) knows nothing about reports or UI; XAI extraction (`explainability/`) knows nothing about web servers. The `AuditPipeline` orchestrator binds them together cleanly.
