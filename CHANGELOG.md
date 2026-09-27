# Changelog

All notable changes to the **BlindSpot** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.8.3] - 2026-09-28

### Fixed & Enhanced
- **Semantic Reference & Probe Expectation Integrity Fix (Phases 0–27)**:
  - **Eliminated Fabricated Fallback Confidence**: Completely purged all hardcoded `confidence=0.75` values and ghost `gemini_confidence` copies across constructors, serializers, cache loaders, and UI renderers. If Gemini did not run or is disabled, `gemini_confidence` and `confidence` are strictly `None`.
  - **Official Google GenAI SDK Integration**: Integrated official `google-genai` Python SDK (`from google import genai`) with JSON schema structured output, robust retry/backoff, and Generative Language API fallback. Reads securely from `GEMINI_API_KEY` or `GOOGLE_API_KEY` with zero key leakage.
  - **Separation of Polarity from Relation**: Disentangled affective sentiment polarity (`POSITIVE`, `NEGATIVE`, `NEUTRAL`) from semantic relation (`PRESERVE_POLARITY`, `REVERSE_POLARITY`, `SHIFT_TO_NEUTRAL`, `SHIFT_FROM_NEUTRAL`, `CONTRAST_SHIFT`, `MEANING_CHANGED`, `UNCERTAIN`). Negation changes syntactic truth conditions, but does not unconditionally invert affective sentiment polarity.
  - **Slot P001 Negation Expectation Correction**: Removed hardcoded `expected_flip = True` and `REVERSE_POLARITY` from `SharedProbeGenerator` P001. P001 is now classified with `semantic_intent = "ADD_NEGATION"` and `expected_flip = False`. Relation is derived strictly from baseline and probe verified polarities.
  - **Eliminated Runner Expectation Overwrites**: Removed all logic in `ExperimentRunner` that mutated semantic relations (e.g. coercing `SHIFT_FROM_NEUTRAL` into `REVERSE_POLARITY` or forcing `expected_flip = True`). Runner strictly consumes and preserves the frozen `RunPlan`.
  - **Deterministic 2-Class vs. 3-Class Alignment**: Explicitly handle 2-class binary models on `NEUTRAL` references as `NOT_DIRECTLY_REPRESENTABLE` / `UNREPRESENTABLE_NEUTRAL`, preventing binary models from being spuriously flagged as `BLIND`. 3-class neutral-preserving pairs evaluated without spurious failure.
  - **Cryptographic Cache Invalidation**: Keyed cache by `normalized_text|provider|model|schema_version|annotation_version`. Automatically purges stale legacy entries with fabricated 0.75 confidence.
  - **Honest Provenance & UI Terminology**: Replaced all misleading "Final Ground-Truth" text with "Semantic Reference", "Semantic Reference (Unverified)", "Gemini Semantic Reference", or "Human-Verified Semantic Reference". Displays exact provider and self-reported Gemini confidence.
  - **Deterministic Failure Taxonomy**: Guarded `classify_behavior` to be evidence-based and deterministic from observed forward passes and verified contracts. Forbade Gemini from predicting failure categories or model diagnostics.
  - **Comprehensive 14-Point Test Suite**: Implemented `tests/test_semantic_integrity_spec.py` covering all 14 Phase 21 requirements with 100% pass rate.

## [2.8.2] - 2026-09-28

### Added
- **Exact Sentiment Polarity Analyzer (Antigravity Engine)**:
  - Implemented `ExactSentimentAnalyzer` in `blindspot/semantic/analyzer.py` combining VADER with expanded clinical, behavioral, moral, and performance domain lexicons.
  - Implemented discourse-weighted contrastive clause analysis ("X but Y", "X however Y", "although X, Y"), allocating 75% discourse weight to the dominant adversative clause.
  - Implemented syntactic negation scope detection ("not healthy" -> `NEGATIVE`, "not bad" -> `POSITIVE`) and double negation resolution.
  - Implemented Antigravity calibration guardrail in `GeminiSemanticClient._validate_and_build_annotations` to intercept and correct false neutrals returned by external LLM services.
- **Dedicated Test Suite (`tests/test_exact_sentiment_analyzer.py`)**:
  - 7 unit tests covering contrast clause dominance, negation, domain vocabulary, objective neutrals, and calibration guardrails.

### Fixed
- **False Neutral Output Bug on Sentiment-Bearing Language**:
  - Fixed issue where sentences containing positive or negative words (e.g. "He is a Good boy but very naughty", "i am healthy but still hospitalized") defaulted to `NEUTRAL`.
  - Upgraded `SemanticReferenceService` offline and fallback methods from a 14-word heuristic tuple to the exact Antigravity analyzer.
  - Migrated and corrected all 39 false neutral entries in `cache/semantic_cache.json`.
  - Added `force_refresh=True` to Probe Workbench "⚡ Annotate / Refresh Semantics" button in `blindspot/ui/probe_lab.py`.

## [2.8.1] - 2026-09-28

### Changed
- **Deduplication of Operational Behavioral Profiles Table**:
  - Removed redundant `STRATIFIED BEHAVIORAL METRICS SUMMARY` table floating above comparison tabs.
  - Baseline stimuli cards now cleanly and directly lead into the tabbed analytics workspace without visual duplication.
  - Consolidated complete operational metrics table (`Model Architecture`, `Task Space`, `Accuracy`, `ECE`, `Mean Confidence`, `Observed Flip Rate`, `Expected Flip Rate`, `Compliance`, `Mean Shift`, `Total Probes`) inside `🧬 BEHAVIORAL FINGERPRINTS`.

### Added
- **Dedicated Models & Failures Tab (`🏷️ MODELS & FAILURES`)**:
  - Added 5th tab to Comparison workspace providing an empirical, non-normative breakdown of diagnosed failure types across evaluated architectures.
  - Summary KPI cards: `TOTAL FAILURES`, `BLIND (INVARIANCE)`, `SPURIOUS (SHORTCUT)`, `MISWEIGHTED (CLAUSE)`, `UNDETERMINED`.
  - Comprehensive failure breakdown table displaying per-architecture probe totals, failure counts, failure rates, failure counts per taxonomy category, and empirical `Primary Failure Mode`.
  - Interactive `🔍 PER-MODEL FAILURE EVIDENCE LOG` with model selection and full diagnostic failure records (`Severity`, `Probe ID`, `Linguistic Category`, `Expected Behavior`, `Observed Prediction`, `Failure Type`, `Evidence Summary`).

## [2.8.0] - 2026-09-28

### Added
- **Canonical Model Identity & Collision Elimination**:
  - Implemented `CANONICAL_MODEL_NAMES` in `blindspot/models/registry.py` with immutable mappings for all 5 sentiment models: `model_id`, `display_name`, `short_name`, `abbrev`, `task_badge`, `task_space`, `label_schema`, and `provider`.
  - Permanently fixed the Twitter model identity collision bug (`[:14]` string slice) where `twitter-roberta-base-sentiment` and `twitter-roberta-base-sentiment-latest` collapsed into `"twitter-robert"`. Both models are now distinct: `Twitter-RoBERTa (Latest)` and `Twitter-RoBERTa (Base)`.
- **Model Completeness Contract**:
  - Prominent Model Completeness Banner displaying `✓ MODEL COMPLETENESS: All 5 / 5 configured architectures evaluated across identical stimuli` or `⚠ PARTIAL MODEL SET: 4 / 5 configured models completed (1 missing: [NOT RUN])`.
  - Zero silent model dropping; unexecuted models explicitly display `— NOT RUN` in all table views.
- **Cell-Level Deviation Highlighting & Non-Color-Alone Semantics**:
  - Replaced whole-row coloring with isolated cell-level deviation highlighting (`✓ MATCH`, `⚠ DEVIATION`, `✕ FAILURE`, `? UNDETERMINED`, `— NOT RUN`).
  - Strict compliance with accessibility guidelines: every cell combines an explicit Unicode glyph, status label text, and high-contrast styling.
  - Added directional transitions badge (`POS ➔ NEG`, `NEU ➔ POS`, `POS ➔ POS`) and single-decimal confidences with percentage points delta (`+18.3 pp`, `−24.7 pp`).
- **Interactive Probe-Level Detail Drawer & Evidence Inspector**:
  - High-density expandable drawer beneath the primary comparison table allowing side-by-side inspection of baseline stimulus, perturbed probe, verified semantic reference rationale, and individual model predictions.
- **Structured Behavioral Failure Register (`blindspot/ui/failure_lab.py`)**:
  - 4-level information hierarchy: summary KPI metric cards (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`), multi-attribute filter bar, structured failure register table with explicit severity, and expandable token attribution explanation cards.
- **Thesis Visualization Overhaul (`blindspot/reporting/thesis_graphs.py`)**:
  - Replaced all 12 instances of slice truncation with `get_model_short_name()`; regenerated all 15 figures with distinct labels and zero collision.
- **Dedicated Phase 38 Test Suite (`tests/test_model_identity_and_ui_completeness.py`)**:
  - Automated tests validating 5 canonical model identities, Twitter collision prevention, completeness accounting, cell-level status semantics, and invalid probe handling.

## [2.7.2] - 2026-09-28

### Audited
- **Full Live Application UI, Logical Flow & End-to-End Audit**:
  - Conducted full live audit on real running application (`http://localhost:8501`) across all 6 primary navigation domains and 15 state checkpoints with Chrome CDP automation.
  - Verified resolution of `NameError: name 'pert_label_clean' is not defined` on live failure taxonomy cards.
  - Verified live experiment execution (`exp_1790540273_5eaf8c`), asynchronous streaming telemetry, and strict pipeline count integrity (`Planned == Executed == Analyzed == Reported`).
  - Verified 15 publication figures generation at 300 DPI and permanent deletion safeguards.
  - Produced comprehensive audit report in `audit_reports/FULL_LIVE_UI_AUDIT.md` and captured all 15 audit screenshots in `audit_reports/live_ui_audit/`.
  - Identified 6 priority findings: P0 custom probe sanitization, P1 live run session reconnect, P1 explainability selector, P2 zombie run cleaner, P3 section numbering, and P3 version label alignment.

## [2.7.1] - 2026-09-28

### Changed
- **Gemini Predicted Polarity as Authoritative Expected Across Benchmark Pipeline**:
  - Replaced legacy heuristic expectation strings (`FLIP ➔ NEGATIVE`, `PRESERVE ➔ POSITIVE`) with authoritative Gemini / Semantic Reference expectations (`NEGATIVE [REVERSE]`, `NEUTRAL [PRESERVE]`, `POSITIVE [SHIFT_FROM_NEUTRAL]`).
  - Unified `Expected (Gemini Ref)` column in Model × Probe Matrix, eliminating contradictory columns (`Semantic Reference: NEUTRAL [PRESERVE]` vs `Expected: FLIP ➔ NEGATIVE`).
  - Aligned Per-Model Audit to display `Expected (Gemini)` and report honest compatibility (`✓ COMPLIANT (FORCED BINARY)` for binary models on neutral stimuli).
  - Synchronized probe expectation properties (`expected_flip`, `expected_semantic_effect`, `semantic_intent`) directly from the frozen semantic reference set before model execution.
- **Stratified Behavioral Summary Metric Disambiguation**:
  - Disambiguated `Expected Flip Rate` (suite expectation prevalence, e.g. 28.6% across all models) from `Reversal Compliance` (observed flips where reversal was expected).
  - Added `Reversal Compliance` column to the Stratified Behavioral Summary table, eliminating visual discrepancies between models.
- **Heuristic Semantic Inference Refinement**:
  - Enhanced offline heuristic polarity inference to analyze probe text for explicit sentiment cues and contrastive clauses, ensuring factual baseline perturbations correctly infer `NEGATIVE` / `POSITIVE` rather than defaulting all probes to neutral.

## [2.7.0] - 2026-09-27

### Added
- **Canonical Semantic Ground-Truth Reference Layer (`blindspot/semantic/`)**:
  - Implemented strict 3-class canonical semantic label space: `POSITIVE`, `NEGATIVE`, `NEUTRAL`.
  - Added strict validation rejecting invalid labels (`MIXED`, `AMBIGUOUS`, `UNCERTAIN`, `SARCASTIC`, etc.).
  - Created `blindspot/semantic/types.py` defining `SemanticReferenceLabel`, `SemanticRelation`, `VerificationStatus`, `SemanticAnnotation`, and immutable `SemanticReferenceSet`.
- **Google Gemini Semantic Verification Engine (`blindspot/semantic/client.py`)**:
  - Implemented `GeminiSemanticClient` with structured JSON schema (`responseMimeType: application/json`).
  - Decoupled Gemini completely from benchmark models and failure diagnosis (Gemini **never** predicts failures or rates models).
  - Configurable model selection (`GEMINI_SEMANTIC_MODEL`, default `gemini-2.5-flash`, fallback `gemini-1.5-flash`).
  - Secure credential management via `GEMINI_API_KEY` (never logged, never committed).
- **Persistent Semantic Annotation Cache & Batching (`blindspot/semantic/cache.py`)**:
  - Implemented `SemanticAnnotationCache` persistent JSON store at `cache/semantic_cache.json`.
  - Keys based on `SHA256(normalized_sentence + version)` preventing redundant API calls.
  - Implemented structured batch annotation (`annotate_batch`) with independent per-item validation.
- **Human Verification & Override Layer**:
  - Added interactive researcher verification controls (`[✓ Accept]`, `[Change to POSITIVE]`, `[Change to NEGATIVE]`, `[Change to NEUTRAL]`).
  - Freezing mechanism (`ref_set.freeze()`) locking semantic references prior to model execution.
  - Full provenance tracking (`verification_source`: `GEMINI_ACCEPTED` vs `HUMAN_OVERRIDE`).
- **Binary vs. Multiclass 2-Class / 3-Class Alignment**:
  - Decoupled semantic reference space from native model output spaces.
  - When reference is `NEUTRAL`, binary models' forced choice is recorded as `NOT_DIRECTLY_REPRESENTABLE` / `BINARY_FORCED_POLARITY`, preventing reference corruption.
  - Added `evaluate_semantic_compatibility()` to `PredictionResult` and `ModelProbeEvaluation`.
- **Reporting & Storage Integration (`runner.py`, `run_store.py`, `report_generator.py`)**:
  - Saved `runs/<experiment_id>/semantic_reference.json` preserving complete semantic reference provenance.
  - Added Section 8 `SEMANTIC REFERENCE METHODOLOGY` to `experiment_summary.md` and `model_behavior_report.md`.
  - Added `Semantic Ref` column to `probe_level_evidence.md` and Model x Probe comparison matrix.
- **UI Research Workbench Integration (`components.py`, `probe_lab.py`, `experiment_lab.py`, `comparison.py`)**:
  - Added dedicated Semantic Reference panel with Provider, Model, Status, telemetry, baseline card, and probe table.
  - Added Gemini request count tracking and cache hit statistics panel.
- **Comprehensive Unit & End-to-End Test Suite**:
  - Added `tests/test_semantic_reference.py` verifying all 14 Section 31 requirements (100% pass).
  - Executed real 5-model end-to-end acceptance experiment (`verify_e2e_semantic_experiment.py`) verifying all scientific invariants.

## [2.6.0] - 2026-09-27

### Added
- **Canonical Semantic Polarity Contract (`blindspot/core/types.py`)**:
  - Implemented `SemanticPolarity` enum (`NEGATIVE`, `NEUTRAL`, `POSITIVE`, `UNKNOWN`) decoupling internal semantic analysis from model-specific raw vocabulary or token IDs.
  - Implemented `SemanticPolarity.from_str()` supporting 2-class, 3-class, Twitter sentiment, star ratings, and integer strings.
  - Added transition predicates: `is_raw_label_flip`, `is_polarity_flip`, and `is_semantic_state_change` preventing false flips on intra-polarity transitions or neutral states.
- **Multi-State Expectation & Behavioral Relation Engine (`blindspot/core/types.py`)**:
  - Implemented `ExpectationType` (`PRESERVE_POLARITY`, `INVERT_POLARITY`, `STRENGTHEN_CONFIDENCE`, `WEAKEN_CONFIDENCE`, `INTENSIFY`, `ATTENUATE`, `SPECIFIC_POLARITY`).
  - Implemented `BehavioralRelation` (`SAME_POLARITY`, `OPPOSITE_POLARITY`, `TRANSITION_TO_NEUTRAL`, `TRANSITION_FROM_NEUTRAL`, `POLARITY_STRENGTHENED`, `POLARITY_WEAKENED`, `UNEXPECTED_CHANGE`).
  - Implemented `ProbeExpectation` data contract with `resolve_expected_behavioral_relation()` and `determine_observed_behavioral_relation()` supporting binary and ternary sentiment spaces.
- **Dynamic Model Card & Label Space Resolver (`blindspot/models/huggingface_wrapper.py`)**:
  - Inspected model configuration to detect architecture, label mappings (`id2label`), and cardinality ($K=2$ vs $K=3$).
  - Eliminated naive assumptions like `LABEL_0 = NEGATIVE` without config verification or `1 - original_label` inversions.
  - Normalized probability distributions across both binary and 3-class models to canonical `normalized_probabilities` indexed by `SemanticPolarity`.
- **Strengthened Model Registry & Non-Normative Guardrails (`blindspot/models/registry.py`)**:
  - Enhanced `validate_model_for_sentiment()` to reject non-sentiment checkpoints: AI text detectors (fake/real), spam/ham classifiers, NLI entailment models, toxicity detectors, and multi-topic classifiers.
  - Enforced non-normative comparative reporting; eliminated best/worst rankings, leaderboards, and winner/loser labels in favor of descriptive behavioral vulnerability profiles.
- **Probe Integrity & Validation System (`blindspot/perturbations/shared.py`)**:
  - Implemented `ProbeValidator` to enforce probe text presence, non-vacuous mutation ($p \neq s$), category validity, length plausibility, and expectation consistency prior to staging or execution.
  - Immutable baseline anchoring via deterministic SHA-256 `baseline_id` tying all executed probes to an explicit pre-perturbation inference.
- **Disambiguated Scientific Behavioral Metrics (`blindspot/testing/metrics.py`, `blindspot/testing/behavioral.py`)**:
  - Separated `observed_flip_rate` (empirical polarity flips observed) from `expected_flip_rate` (prevalence of flip-expecting probes in the suite).
  - Implemented `expected_flip_compliance` ($\text{observed flips} / \text{expected flips}$) to measure compliance with polarity inversion probes.
  - Added granular reporting of `raw_label_flip_rate` vs `polarity_flip_rate`.
  - Refactored `classify_behavior()` to evaluate transitions against `ProbeExpectation` and classify `BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`, or `NONE` deterministically with zero AI/LLM prediction.
- **Comprehensive Scientific Unit Test Suite (`tests/test_scientific_repairs.py`)**:
  - 25 dedicated unit tests covering `SemanticPolarity` mapping, flip predicates, confidence deltas, metric disambiguation, `classify_behavior` calibration, baseline immutability, probe validation, non-normative reporting, and registry gate enforcement (100% pass).
- **Multi-Model Acceptance Benchmark (`tests/run_acceptance_experiment.py`)**:
  - Verified 5 real sentiment checkpoints across 5 linguistic test sentences (A-E), evaluating 35 probes per model (175 inferences) with real pipeline execution, deterministic failure diagnosis, and non-normative reporting.
- **Foundational Architecture & Specification Artifacts**:
  - Created `SEMANTIC_EXPECTATION_SPEC.md` documenting formal state-transition logic for binary and 3-class sentiment spaces.
  - Created `PROBE_EXECUTION_CONTRACT.md` detailing probe lifecycle, immutability guarantees, and validation invariants.
  - Updated `ARCHITECTURE.md`, `DECISIONS.md` (Decisions 12-16), and `IMPLEMENTATION_PROGRESS.md` (Milestone 9).
  - Documented audit in `CURRENT_LOGICAL_STATE_AUDIT.md` and complete synthesis in `FINAL_LOGICAL_FIX_REPORT.md`.

## [2.5.0] - 2026-09-22

### Added
- **Canonical Probe Lifecycle & Count Integrity Enforcement**:
  - Implemented bidirectional category matching table `DISPLAY_CATEGORY_TO_SUBTYPES` in `blindspot/perturbations/shared.py`.
  - Fixed 7 → 4 → 3 probe discrepancy bug where user category filtering caused silent probe drops.
  - Enforced runtime assertion: `planned == executed == analyzed == reported` across all models.
  - Added `RunPlan.validate_execution()` to strictly verify that executed probe IDs match selected probe IDs.
- **Pure Rule-Based Behavioral Taxonomy (Zero AI Predictions)**:
  - Formally verified and guaranteed that no predictive AI or LLM classifies model failures.
  - All diagnoses (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`, `NONE`) emerge purely from deterministic evaluation of model logits, signed confidence shifts ($\Delta c$), and explicit linguistic contracts.
- **5-Model Memory-Resident Cache Capacity**:
  - Configured default `model_cache_size = 5` in `ResourceConfig` across Balanced, Performance, and Custom modes.
  - Conditioned RAM eviction on `model_cache_size <= 1`, allowing all 5 benchmark models to stay warm in memory for sub-second repeat testing.
  - Added cache metadata tracking (`loaded_at`, `last_used`, `device`) and `get_cache_summary()`.
- **Progressive Completed-Model UI Revealing**:
  - Enhanced `blindspot/ui/live_run.py` to stream completed model metrics, baseline probabilities, flips, and failures immediately without blocking on remaining models.
  - Removed duplicate header markdown block.
  - Added interactive `▶ RESUME RUN` button in `blindspot/ui/run_history.py` wired to `ExperimentRunner.resume_run()`.
- **20-Point Canonical Pipeline Verification Suite (`tests/test_canonical_pipeline.py`)**:
  - Implemented exhaustive 20-point automated test covering every requirement: generated count, selected count, executed count, selection equality, baseline recording, binary normalization, multiclass normalization, flip detection, confidence delta calculation, behavioral outcomes, failure taxonomy, incremental persistence, resume capability, safe deletion, 5-model cache capacity, progressive UI state, 15 thesis figures, zero AI failure prediction, non-sentiment model rejection, and custom probe lifecycle.
  - Integrated into `run_tests.py` with 118/118 tests passing.
- **Safe Persistence & Lifecycle Engine (`blindspot/storage/run_store.py`)**:
  - Prohibited automatic run deletion. Historical experiment runs in `runs/` are strictly preserved.
  - Added `load_probe_set` and `load_run_plan` to faithfully restore exact probe stimuli upon run resumption.
  - Added `archive_run(exp_id)` to safely move runs to `runs/archived/<exp_id>`.
  - Added `delete_run(exp_id, confirmation=True)` requiring explicit confirmation for permanent deletion.
- **15 Publication-Grade Thesis Visualizations (`blindspot/reporting/thesis_graphs.py`)**:
  - Implemented 15 multi-model figures rendered at 300 DPI (`runs/<run_id>/figures/*.png`).
  - Saved raw plot data points into `runs/<run_id>/figures/source_data.json` for external chart reproduction.
  - Fixed token attribution unwrapping bug in `Visualizer.plot_attribution_comparison`.

## [2.4.0] - 2026-09-20


### Added
- **Model Validation Gate (`blindspot/models/registry.py`)**: Strict pre-benchmark registration gate enforcing task compatibility (`task == "SENTIMENT"`), label cardinality (`num_classes >= 2`), label mappings (`id2label`), numerical probability distributions, and documented semantics.
- **Active 5-Model Sentiment Benchmark Suite**: Validated 5 diverse sentiment architectures:
  1. `distilbert-base-uncased-finetuned-sst-2-english` (DistilBERT, 66.96M params, SST-2 binary)
  2. `textattack/albert-base-v2-SST-2` (ALBERT, 11.68M params, SST-2 binary)
  3. `cardiffnlp/twitter-roberta-base-sentiment-latest` (RoBERTa, 124.65M params, 3-class Twitter)
  4. `textattack/bert-base-uncased-SST-2` (BERT, 109.48M params, SST-2 binary)
  5. `cardiffnlp/twitter-roberta-base-sentiment` (RoBERTa Base, 124.65M params, 3-class Twitter)
- **Model Validation Report (`MODEL_VALIDATION_REPORT.md`)**: Full empirical audit detailing gate checks, architectural parameters, benchmark diagnostics on 5 standardized test sentences, and formal exclusion rationale for non-sentiment and incompatible checkpoints.
- **Research Repair Acceptance Matrix (`tests/test_research_repair.py`)**: 20 unit and deterministic acceptance tests covering model rejection, label normalization, strict count integrity ($\text{Planned} == \text{Executed} == \text{Analyzed} == \text{Reported}$), synthetic taxonomy calibration (BLIND, SPURIOUS, MISWEIGHTED, NONE, UNDETERMINED), and a $5 \times 1\text{ baseline} + 5 \times 4\text{ probes} = 25\text{ evaluations}$ acceptance run. All 118 tests in `run_tests.py` now pass.

### Fixed
- **DEF-01: Non-Sentiment Model Infiltration**: `roberta-base-openai-detector` was reclassified with task `AI_TEXT_DETECTION` and labels `["Fake", "Real"]`. Strictly rejected from sentiment experiments; silent remapping (`Fake` -> `Negative`, `Real` -> `Positive`) eliminated.
- **DEF-02: Category Key Matching Mismatch**: Enhanced `_is_category_match` in `blindspot/perturbations/shared.py` to robustly handle both string and list inputs, as well as lexical, syntax, and intensity aliases.
- **DEF-03: Silent Fallback to Heuristic Probabilities**: Added `allow_fallback=False` enforcement to `HuggingFaceWrapper` in benchmark mode. Broken or unloaded models raise explicit exceptions rather than silently generating pseudo-random heuristic predictions.
- **DEF-04: AttributeError on `ev.original_label` in Runner**: Resolved safe access across `PredictionResult`, `ModelProbeEvaluation`, and dict representations in `blindspot/execution/runner.py`.
- **DEF-05: Count Integrity Violations**: If a model fails or evaluations mismatch, run is marked `FAILED`/`INCOMPLETE` with analysis status `NO_VALID_ANALYSIS` and failure counts set to `None`, never converted to zero failures.
- **UI Model Filtering**: Updated `blindspot/ui/experiment_lab.py` to query `registry.list_sentiment_models()`, preventing non-sentiment models from entering benchmark runs. Added visual task badges in `blindspot/ui/model_lab.py`.

## [2.3.0] - 2026-09-20

### Added
- **Pure Isolated Behavioral Classifier (`blindspot/testing/behavioral.py`)**: Implemented standalone, deterministic `classify_behavior(...)` function with zero UI or model name bias. Classifies primary behavioral outcomes (`EXPECTED_FLIP`, `MISSING_FLIP`, `UNEXPECTED_FLIP`, `EXPECTED_PRESERVE`, `UNEXPECTED_CHANGE`, `UNDETERMINED`) and secondary failure taxonomy (`NONE`, `BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`).
- **Calibrated 7-Probe Diagnostic Suite (`blindspot/perturbations/shared.py`)**: Generates balanced expected flips and expected preserves across 7 diagnostic categories (`P001` negation reversal, `P002` double negation preserve, `P003` intensifier strengthen, `P004` downtoner weaken, `P005` synonym/proverb preserve, `P006` adversative contrast flip, `P007` structural framing preserve).
- **Pragmatic Proverb Support (`blindspot/core/types.py`, `blindspot/perturbations/shared.py`)**: Added `SentenceType.PROVERB` and calibrated semantic preservation for non-literal structures such as *"All that glitters is not gold."*.
- **Comprehensive Synthetic Calibration Suite (`tests/test_behavioral_taxonomy.py`)**: 14 unit tests proving all 8 synthetic benchmark cases: Case 1 Expected Flip, Case 2 Blind, Case 3 Expected Preserve, Case 4 Spurious, Case 5-6 Multiclass Flip/No-Flip, Case 7 Misweighted (strengthening drop, downtoning surge, flipped label), Case 8 Undetermined, model independence, and zero-failure retention.
- **Flip Analysis & Percentage-Point Delta Tests (`tests/test_flip_analysis.py`)**: 8 unit tests covering multiclass transitions, signed confidence shifts in percentage points ($(\text{probe} - \text{orig}) \times 100$), and transition matrix calculation.
- **Probe Calibration Tests (`tests/test_probe_calibration.py`)**: 4 unit tests covering the 7-candidate generator, proverb pragmatic processing, invalid probe execution blocking, and determinism.
- **Deterministic Acceptance Suite (`tests/test_deterministic_acceptance.py`)**: 4 unit tests covering Section 37 deterministic acceptance requirements: 7 generated / 4 selected / 2 models producing exactly 10 evaluations (2 baselines + 8 probes), 16 evals on 7 probes, 4 on 1 probe, and custom probe lifecycle.
- **Live Run Diagnostic Event Cards (`blindspot/ui/live_run.py`)**: Section 29 research event cards streaming model, probe ID, category, baseline/probe predictions, transition, confidence delta (pp), flip status, expected effect, behavioral outcome, and failure taxonomy.
- **Probe Lab Workbench Enhancements (`blindspot/ui/probe_lab.py`)**: Telemetry metrics (Generated, Selected, Verified), Select Category, Verify Selected, Edit Probe (new version generation with `USER_EDITED` status), and JSON probe set export.
- **All 21 Research-Valid Reporting Fields (`blindspot/execution/runner.py`)**: Reports (`experiment_summary.md`, `probe_level_evidence.md`, `failure_summary.md`) retain baseline evaluations, probe-level evidence, failure rationales, cross-model agreement, and never suppress zero categories.
- **Methodological Documentation**: Created `RESEARCH_INTEGRITY_AUDIT.md`, `FAILURE_TAXONOMY.md`, `PROBE_CALIBRATION.md`, and updated all project documentation.

### Fixed
- **Root Cause of Universal Zero Behavioral Failures**: Fixed key mismatch in `infer_expected_semantic_effect` where perturber types (`negation_insertion`, `negation_removal`, `contrast_negative_append`) defaulted to `expected_flip = False`. When models failed on negation, `is_flipped == expected_flip` (`False == False`), falsely rewarding model blindness as `EXPECTED_PRESERVE`.
- **7 → 4 → 3 Pipeline Count Discrepancy**: Eliminated re-generation and silent probe filtering; Live Run strictly executes the finalized `RunPlan`.
- **Decoupled XAI from Failure Diagnosis**: Failures are primary behavioral observations detected during inference regardless of whether explainability is enabled.

## [2.2.0] - 2026-09-20

### Added
- **Canonical Probe Protocol (`blindspot/core/types.py`, `blindspot/perturbations/shared.py`)**: Unified end-to-end data model for `LinguisticProbe` and `SharedProbeSet` with deterministic SHA-256 identification, schema versioning (`2.2.0`), pragmatic sentence tagging, semantic intent classification (`SemanticIntent`), and schema validation (`validate()`).
- **Dedicated Baseline Evaluation (`blindspot/core/types.py`, `blindspot/testing/behavioral.py`)**: Standalone `BaselineEvaluation` record evaluated and stored first per model prior to perturbation inference, establishing the true baseline for all transitions.
- **Canonical Prediction Flip & Stratified Behavioral Metrics (`blindspot/core/types.py`, `blindspot/testing/metrics.py`)**:
  - `is_prediction_flip(orig_label, pert_label)`: Multiclass-safe flip detection ($y_0 \neq y_p$).
  - `classify_behavioral_outcome(...)`: Canonical outcomes (`EXPECTED_FLIP`, `MISSING_FLIP`, `EXPECTED_PRESERVE`, `UNEXPECTED_FLIP`).
  - `compute_observed_flip_rate`: Volatility fraction across all executed probes.
  - `compute_expected_flip_rate`: Success rate on probes expecting polarity inversion.
  - `compute_preserve_rate`: Invariance rate on probes expecting label preservation.
  - `compute_behavioral_consistency`: Overall expectation compliance score.
  - `compute_confidence_flip_rate`: Sensitivity rate on drops $\ge 20.0$ percentage points.
- **Intensity & Structural Perturbation Engines (`blindspot/perturbations/intensity.py`, `structure.py`)**:
  - `IntensityPerturber`: Tests degree-sensitivity via intensifiers (`extremely`, `truly`) and downtoners (`somewhat`, `slightly`) with `expected_flip=False`.
  - `StructurePerturber`: Tests syntactic robustness via comma-separated clause inversion, discourse framing, and punctuation drift with `expected_flip=False`.
- **Interactive Probe Research Workbench (`blindspot/ui/probe_lab.py`)**: Interactive candidate catalog with checkboxes per probe, batch selection (`[Select All]`, `[Select None]`), pragmatic sentence presets (Literal, Proverb, Idiom, Figurative, Sarcastic, Ironic), custom probe injection (`+ Add Custom Probe`), schema validation, and 1-click staging (`[Send to Experiment Lab]`).
- **Top Navigation Workstation Layout (`blindspot/ui/shell.py`, `ui/design_system.py`)**: Sleek horizontal top navigation bar across the 7 functional domains (`Overview | Experiment | Probes | Run | Analyze | Reports | System`) with secondary domain subtabs, complemented by a minimized contextual sidebar.
- **Exact Run Plan & Count Integrity Verification (`blindspot/ui/experiment_lab.py`, `execution/runner.py`, `ui/live_run.py`)**:
  - Single-screen Run Plan table: Original Baselines ($M \times S$) + Selected Probes ($M \times N$) = Total Model Predictions.
  - Post-run count integrity verification audit guaranteeing $\text{planned} == \text{executed} == \text{analyzed} == \text{reported}$.
- **Baseline vs Perturbation Thesis Matrix (`blindspot/ui/comparison.py`)**: Dedicated thesis section rendering seed sentences with original model baseline predictions alongside stratified behavioral robustness summaries.
- **20 Targeted Probe Integrity Tests (`tests/test_probe_integrity.py`)**: Added full test suite verifying probe determinism, multiclass flip evaluation, behavioral outcomes, stratified rates, schema validation, perturbation engines, and execution count integrity. Total passing tests: 68.
- **Methodological Documentation**: Added `PROBE_PROTOCOL.md`, `PROBE_SELECTION.md`, `BEHAVIORAL_METRICS.md`, `FLIP_ANALYSIS.md`, `SEMANTIC_PROBE_DESIGN.md`, and `FINAL_RESEARCH_INTEGRITY_REPORT.md`.

### Changed
- **Pipeline Separation of Concerns**: Decoupled Generation $\neq$ Selection $\neq$ Execution. When a verified probe set is staged, `ExperimentRunner` executes it directly without re-generation.
- **Diagnostic Layer Framing (`blindspot/ui/failure_lab.py`)**: Framed 4-way failure taxonomy (`Blind`, `Spurious`, `Misweighted`, `Undetermined`) as a secondary diagnostic layer explaining root causes of behavioral failures, rather than dominating primary thesis metrics.

---

## [2.1.0] - 2026-09-20

### Added
- **One-Click Windows Launcher (`launch_blindspot.bat`)**: Double-clickable batch launcher with environment check, dependency validation, and browser auto-launch.
- **PowerShell Launcher & Desktop Shortcut (`launch_blindspot.ps1`, `create_blindspot_shortcut.ps1`)**: Native PowerShell launcher and non-admin Windows desktop shortcut generator.
- **Supervisor Process Manager (`blindspot/launcher.py`)**: Automatic port resolution (checks 8501, re-attaches to active instances, or locates next free port) and graceful Ctrl+C shutdown.
- **Structured Subsystem Logging (`blindspot/core/logging_config.py`)**: Added rotating file logging in `logs/blindspot.log` (5MB rotating handler) and formatted subsystem tagging (`BOOT`, `UI`, `MODEL`, `CACHE`, `RUNNER`, `PROBE`, `XAI`, `RESOURCE`, `STORAGE`, `REPORT`).
- **Dedicated System Console (`blindspot/ui/console.py`)**: Built-in monospace engineering terminal with real-time log streaming, severity filtering, subsystem filtering, substring search, and log download.
- **Centralized Workstation Dark Design System (`blindspot/ui/design_system.py`)**: Dark-first technical styling tokens, slim custom 6px scrollbars, and monospace telemetry typography.
- **Persistent Telemetry Header & Shell (`blindspot/ui/shell.py`)**: Host hardware telemetry (CPU%, cores, RAM%, GPU acceleration, persisted run counter) and grouped navigation across 6 functional domains.
- **Guided 5-Step Experiment Workflow (`blindspot/ui/experiment_lab.py`)**: Unified single-screen setup: `01 INPUT` (text area, research examples, token counter) -> `02 MODELS` (technical cards with `LOADED` vs `STANDBY` cache badges) -> `03 PROBES` (categories, deterministic SHA-256 badge, live probe preview) -> `04 EXECUTION` (specification card, prominent `▶ RUN EXPERIMENT` / `■ CANCEL RUN`) -> `05 REVIEW`.
- **Enhanced Live Run Experience (`blindspot/ui/live_run.py`)**: Live elapsed timer (`MM:SS`), dynamic ETA calculation (`~MM:SS`), per-model progress status meters (`DistilBERT: 18/18 ● COMPLETED`), and terminal event stream.
- **Control Center Overview (`blindspot/ui/overview.py`)**: Control center with quick-action buttons (`[NEW EXPERIMENT]`, `[LOAD RUN]`, `[OPEN CONSOLE]`), host resource cards, recent activity table, and latest findings summary.
- **Model × Probe Comparison Matrix (`blindspot/ui/comparison.py`)**: High-density response matrix with compact prediction columns, agreement filters, and confidence deltas.
- **Scientific Evidence Records (`blindspot/ui/failure_lab.py`)**: Structured evidence cards with observed vs expected behavioral transitions, confidence deltas, and actionable remediation steps.
- **Token Explainability Provenance (`blindspot/ui/explanation_lab.py`)**: Side-by-side attribution bars, alignment scores (Jaccard/Cosine), and transparent provenance badges (`NATIVE: SHAP`, `NATIVE: LIME`, `FALLBACK: LOO`).
- **Research Run Archive (`blindspot/ui/run_history.py`)**: Tabular run history with inspector, report download, and one-click session reloading.
- **5 Curated Model Presets (`blindspot/models/registry.py`)**: Added `cardiffnlp/twitter-roberta-base-sentiment` (Twitter RoBERTa Classic, 3-Class) as the 5th curated benchmark preset alongside DistilBERT SST-2, Twitter RoBERTa 3-Class Latest, BERT Base SST-2, and RoBERTa OpenAI Detector.
- **Import Resolution & Module Search Hardening**: Added `sys.path.insert` across `blindspot/app.py` and all 16 test files in `tests/`, injected `PYTHONPATH` in `blindspot/launcher.py`, `launch_blindspot.bat`, and `launch_blindspot.ps1`, and registered editable package in site-packages, eliminating all `ModuleNotFoundError` issues across all standalone and subprocess workflows.
- **UI & Launcher Test Suite (`tests/test_ui_and_launchers.py`)**: 6 comprehensive unit tests validating page modules, design tokens, components, structured logging, and port resolution.

### Changed
- **Entrypoint Cleanliness (`blindspot/app.py`)**: Encapsulated Streamlit startup inside clean `main()` entrypoint, eliminated dead legacy code blocks, and preserved all test-facing helper functions.

---

## [0.2.1] - 2026-09-19

### Hardened & Fixed (Production Reality Audit)
- **Multiclass Calibration (`blindspot/testing/behavioral.py`)**: Fixed multiclass ECE expected index calculation under expected flips; replaced inverted `1 - orig_idx` logic with dynamic expectation satisfaction mapping.
- **Dynamic Transition Narrative (`blindspot/app.py`)**: Removed hardcoded `opposite_label = NEGATIVE if POSITIVE else POSITIVE` in `get_failure_narrative`; now supports arbitrary multiclass label schemas.
- **Cross-Platform Console Compatibility (`blindspot/core/types.py`)**: Replaced Unicode block characters in `PredictionResult.formatted_distribution_ascii` with ASCII bracket meters (`[====================]`) to prevent `UnicodeEncodeError` on Windows cp1252/cp437 consoles.
- **Performance Mode Enums & Safety (`blindspot/core/config.py`, `execution/resources.py`)**: Added first-class `SAFE`, `BALANCED`, `PERFORMANCE`, `CUSTOM` modes and prevented Enum re-parsing recursion.
- **HuggingFace Pipeline Multi-Score Safety (`blindspot/models/huggingface_wrapper.py`)**: Added three-stage fallback for pipeline probability calls (`top_k=None`, `return_all_scores=True`) preventing top-1 probability clipping. Injected `device` and `model_status` into `PredictionResult`.
- **UI Research Telemetry (`blindspot/ui/components.py`, `ui/system_monitor.py`)**: Upgraded `render_prediction_card` to show active device, latency in ms, model readiness status, confidence %, class probability meters, and dense workstation telemetry. Set GPU metric to explicitly display `Not detected` when CUDA is unavailable.
- **Test Suite Expansion (`tests/test_shared_probes.py`, `tests/test_live_events_and_jobs.py`)**: Added `test_multimodel_identical_probe_stimuli_and_ids` proving Model A probe IDs == Model B probe IDs == Model C probe IDs, and `test_experiment_runner_async_and_cancellation` validating background thread cancellation.

## [0.2.0] - 2026-09-19

### Added
- **Core Types (`blindspot/core/types.py`)**: Added dataclasses `ModelMetadata`, `PredictionResult`, `LinguisticProbe`, `SharedProbeSet`, `ModelProbeEvaluation`, `ExplanationResult`, `FailureDiagnosis`, and enums `ExpectedSemanticEffect`, `FailureCategory`.
- **Event System (`blindspot/core/events.py`)**: Added `ExecutionEvent` and thread-safe `EventEmitter` pub/sub dispatcher for live UI log streaming and progress observation.
- **Configuration (`blindspot/core/config.py`)**: Added `PerformanceMode` (`SAFE`, `BALANCED`, `PERFORMANCE`, `CUSTOM`), `ResourceConfig`, and `ExperimentConfig`.
- **Model Registry & Verification (`blindspot/models/registry.py`)**: Added `ModelRegistry` supporting preset catalogs and pre-execution model verification without downloading multi-gigabyte checkpoints.
- **Model Caching (`blindspot/models/cache.py`)**: Added thread-safe `ModelCache` implementing LRU eviction and memory reclamation across multiple sentences and probes.
- **Shared Probe Protocol (`blindspot/perturbations/shared.py`)**: Added `SharedProbeGenerator` generating identical controlled linguistic probes with stable IDs (`probe_001`...) once per input, shared across all models.
- **Expectation Engine (`blindspot/perturbations/shared.py`)**: Added `infer_expected_semantic_effect` to scientifically distinguish expected reversals, preservation, and contrast shifts from anomalous behavior.
- **Multiclass Behavioral Metrics (`blindspot/testing/metrics.py`)**: Added `compute_transition_matrix`, `compute_confidence_shifts`, `compute_prediction_agreement`, and multiclass-safe `compute_ece`.
- **Behavioral Batch Inference (`blindspot/testing/behavioral.py`)**: Added batch inference acceleration for `SharedProbeSet` probe arrays and multiclass label transition tracking.
- **Explainability Provenance (`blindspot/explainability/`)**: Added provenance tracking to `LimeExplainerWrapper` and `ShapExplainerWrapper` recording requested explainer, actual explainer, fallback status, fallback reason, and runtime.
- **Refactored 4-Way Failure Taxonomy (`blindspot/explainability/taxonomy.py`)**: Expanded failure taxonomy to `Blind`, `Spurious`, `Misweighted`, and `Undetermined`, returning structured `FailureDiagnosisDict` with empirical evidence and actionable remedies.
- **Cross-Model Descriptive Analytics (`blindspot/analysis/`)**: Added `CrossModelAnalyzer` and `ModelBehavioralFingerprint` calculating Model × Probe Matrix, consensus agreement rates, and multi-dimensional behavioral profiles.
- **Resource Management & Concurrency (`blindspot/execution/`)**: Added `ResourceManager` with host hardware detection (CPU/RAM/GPU), `AuditScheduler`, and `ExperimentRunner` for non-blocking asynchronous background execution.
- **Reproducible Run Storage (`blindspot/storage/run_store.py`)**: Added `RunStore` managing self-contained run artifacts under `runs/<experiment_id>/` (`config.json`, `metadata.json`, `events.jsonl`, `results.json`, `reports/`, `figures/`).
- **Comparative Visualizations (`blindspot/reporting/visualizer.py`)**: Added `plot_model_probe_matrix`, `plot_cross_model_fingerprints`, and `plot_cross_model_failures`.
- **Executive Experiment Reporting (`blindspot/reporting/report_generator.py`)**: Added `generate_experiment_reports` generating `experiment_summary.md` and `cross_model_comparison.md`.
- **Modular Research UI (`blindspot/ui/`)**: Replaced monolithic UI with 11 modular research pages: Overview, Experiment Lab, Model Lab, Probe Lab, Live Run, Model Comparison, Explanation Lab, Failure Analysis, Reports & Artifacts, Run History, and System Monitor.

### Changed
- **Hugging Face Wrapper (`blindspot/models/huggingface_wrapper.py`)**: Generalised beyond binary `"NEGATIVE"`/`"POSITIVE"` labels to support arbitrary N-class classifiers with normalized label mappings, batch inference, latency timing, and CUDA OOM resilience.
- **Main Dashboard (`blindspot/app.py`)**: Refactored entrypoint to route cleanly across modular UI components with responsive session state while maintaining backward-compatible helper functions.

---

## [0.1.0] - 2026-09-01

### Added
- Initial SRS-compliant prototype implementation.
- Single-model `AuditPipeline`.
- Negation, double negation, connectives, and synonym substitution perturbation engines.
- Basic LIME and SHAP explainability wrappers with LOO fallback.
- 3-way SRS failure taxonomy (`Blind`, `Spurious`, `Misweighted`).
- Markdown report generator and Matplotlib visualizer.
- Streamlit dashboard and CLI.
