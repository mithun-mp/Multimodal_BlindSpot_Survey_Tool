# Engineering & Research Decisions Log (BlindSpot v2.5.0)

This log records the authoritative architectural, scientific, and implementation decisions governing the BlindSpot platform.

---

## Decision 1: Shared Probe Protocol Over Independent Generation
- **Context**: Independent perturbation generation produced varying linguistic stimuli across models, contaminating cross-model comparisons.
- **Decision**: Implemented `SharedProbeGenerator` generating an immutable `SharedProbeSet` with stable probe IDs. Every model receives identical linguistic stimuli.
- **Status**: Implemented & Verified.

---

## Decision 2: Explicit Expectation Models Over Binary Flip Assumptions
- **Context**: Treating all label shifts as failures incorrectly penalized expected inversions (e.g. single negation).
- **Decision**: Define explicit semantic expectations (`expected_semantic_effect`, `expected_label_relation`, `expected_flip`).
- **Status**: Implemented & Verified.

---

## Decision 3: Explainability Provenance Tracking
- **Context**: Fallbacks like Leave-One-Out (LOO) could silently masquerade as genuine SHAP/LIME attributions.
- **Decision**: Every `ExplanationResult` explicitly records `explainer_requested`, `explainer_used`, `fallback_used`, and `fallback_reason`.
- **Status**: Implemented & Verified.

---

## Decision 4: Descriptive Analysis Over Subjective Model Rankings
- **Context**: Arbitrary "winner" or "ranking" badges violate scientific neutrality in robustness testing.
- **Decision**: Present multi-model findings descriptively via behavioral fingerprints, transition matrices, and pairwise agreements.
- **Status**: Implemented & Verified.

---

## Decision 5: Non-Destructive Data Retention & Safe Deletion
- **Context**: Destructive overwrites risked losing experimental provenance.
- **Decision**: Retain all historical runs incrementally. Deletion requires explicit `confirmation=True` and target verification.
- **Status**: Implemented & Verified.

---

## Decision 6: Calibration via Empirical Diagnostics
- **Context**: ECE calculations previously misaligned predicted class indices with multi-class probabilities.
- **Decision**: Canonical ECE computation based on explicit top-1 confidence and expectation satisfaction.
- **Status**: Implemented & Verified.

---

## Decision 7: Pure Rule-Based Behavioral Taxonomy (Zero AI Predictions)
- **Context**: An earlier discussion explored using LLMs or classifiers to predict whether a model failed.
- **Decision**: Strictly prohibit any AI, LLM, or predictive ML model from classifying failures. All diagnoses (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`, `NONE`) must emerge purely from deterministic, rule-based evaluations of the model's actual outputs ($y_{\text{orig}}, y_{\text{pert}}$, $\Delta c$) against the linguistic contract.
- **Status**: Implemented & Verified in `blindspot/testing/behavioral.py`.

---

## Decision 8: Frozen Probe Set and Strict Count Integrity
- **Context**: A critical defect caused 4 selected probes to execute as 3 due to downstream re-filtering and category mismatch.
- **Decision**: Probes follow a strict canonical lifecycle ($\text{Generate} \to \text{Inspect} \to \text{Select} \to \text{Freeze into RunPlan} \to \text{Execute}$). The runner consumes the frozen probe set without re-generation or mutation. A runtime assertion halts execution if `planned != executed != analyzed != reported`.
- **Status**: Implemented & Verified in `blindspot/perturbations/shared.py` and `runner.py`.

---

## Decision 9: Five Genuine Sentiment Models with Strict Gate Enforcement
- **Context**: `roberta-base-openai-detector` (a text detector predicting "Fake"/"Real") was previously included in the sentiment model registry, contaminating sentiment evaluation.
- **Decision**: The Sentiment Validation Gate strictly rejects any non-sentiment model. The 5-model benchmark comprises genuine sentiment architectures only: DistilBERT SST-2, ALBERT Base SST-2, Twitter RoBERTa Latest (3-class), BERT Base SST-2, and Twitter RoBERTa Base (3-class).
- **Status**: Implemented & Verified in `blindspot/models/registry.py` and `validation.py`.

---

## Decision 10: Five-Model Cache Capacity in Balanced and Performance Modes
- **Context**: `runner.py` was unconditionally evicting models after each evaluation, forcing redundant weights reloading.
- **Decision**: Set default `model_cache_size = 5` for Balanced, Performance, and Custom modes. Eviction from RAM is only performed if `model_cache_size <= 1`.
- **Status**: Implemented & Verified in `blindspot/core/config.py`, `resources.py`, and `runner.py`.

---

## Decision 11: Progressive Live Result Streaming and Interrupted Run Resumption
- **Context**: In multimodel runs, users had to wait for all models to complete before viewing any results. If interrupted, the entire run was lost.
- **Decision**: Stream completed model results to the UI immediately with per-model cards showing baseline, confidence, probabilities, flips, metrics, and failures. Persist per-model artifacts incrementally. Implement `resume_run(exp_id)` to skip completed models without recomputation.
- **Status**: Implemented & Verified in `blindspot/ui/live_run.py`, `run_history.py`, and `runner.py`.

---

## Decision 12: Model-Independent Canonical Semantic Representation (`SemanticPolarity`)
- **Context**: Comparing raw class IDs (`LABEL_0`, `LABEL_1`, `LABEL_2`) across heterogeneous models produced incorrect cross-model assumptions because class `0` can mean negative in SST-2 but fake in detectors or neutral in other schemes.
- **Decision**: Introduce canonical `SemanticPolarity` enum (`POSITIVE`, `NEGATIVE`, `NEUTRAL`, `UNKNOWN`). Dynamically resolve model `id2label` to canonical polarities during model wrapper initialization.
- **Status**: Implemented & Verified in `blindspot/core/types.py` and `huggingface_wrapper.py`.

---

## Decision 13: Disambiguation of Raw Label Flips vs Polarity Reversals vs Semantic State Changes
- **Context**: Legacy code used string inequality `orig_label != prb_label` as the definition of a polarity flip. In 3-class models, transitioning from `POSITIVE` to `NEUTRAL` was falsely counted as a polarity flip and marked `FailureCategory.NONE`.
- **Decision**: Decouple the transition concept into three distinct metrics:
  1. `raw_label_flip`: predicted class index/label changed.
  2. `polarity_flip`: true semantic reversal (`POSITIVE <-> NEGATIVE`).
  3. `semantic_state_change`: any state change (including to/from `NEUTRAL`).
- **Status**: Implemented & Verified in `blindspot/core/types.py` and `testing/behavioral.py`.

---

## Decision 14: Immutable Baseline Anchoring with Deterministic SHA-256 IDs
- **Context**: Baseline predictions were evaluated ad-hoc, risking drift if re-inferred multiple times.
- **Decision**: Evaluate the unperturbed seed sentence exactly once per (model, seed), anchored with an immutable `baseline_id` computed via `base_SHA256(model_id | seed_text)[:12]`. All subsequent probe evaluations reference this anchored baseline.
- **Status**: Implemented & Verified in `blindspot/core/types.py` and `testing/behavioral.py`.

---

## Decision 15: Exact Behavioral Metric Denominators
- **Context**: `expected_flip_rate` previously computed compliance (`observed_flips_on_expected / expected_count`) rather than prevalence (`expected_count / total_probes`), confusing benchmark reports.
- **Decision**: Formally separate `expected_flip_rate` (prevalence in test suite) from `expected_flip_compliance` (fraction of expected flips that actually flipped). Add `raw_label_flip_rate` and `polarity_flip_rate`.
- **Status**: Implemented & Verified in `blindspot/testing/metrics.py`.

---

## Decision 16: Linguistic Validation Gate via `ProbeValidator`
- **Context**: Malformed or unmutated probes could silently enter the execution pipeline.
- **Decision**: Introduce `ProbeValidator` enforcing 5 strict criteria: non-empty text, genuine mutation (`perturbed_text != seed_text`), valid category, plausible length ratio, and valid `ProbeExpectation`.
- **Status**: Implemented & Verified in `blindspot/perturbations/shared.py`.

---

## Decision 17: Canonical Semantic Reference Space Partitioning (`POSITIVE`, `NEGATIVE`, `NEUTRAL`)
- **Context**: Different models employ disparate label spaces (2-class binary vs 3-class ternary). Direct comparison of model labels without an external semantic reference leads to flawed conclusions.
- **Decision**: Establish ONE canonical semantic reference space strictly confined to `POSITIVE`, `NEGATIVE`, and `NEUTRAL`. Non-canonical labels (`MIXED`, `AMBIGUOUS`, `UNCERTAIN`, etc.) are strictly rejected. Uncertainty is expressed solely through numerical confidence.
- **Status**: Implemented & Verified in `blindspot/semantic/types.py`.

---

## Decision 18: Isolation of External LLM (Gemini) from Benchmark & Failure Taxonomy
- **Context**: Incorporating Gemini could risk turning it into a 6th benchmark model or relying on AI to predict failure categories.
- **Decision**: Gemini operates strictly as an external semantic annotator and relation verifier. Gemini is NEVER part of the benchmark models, NEVER forecasts model failures, and NEVER determines failure taxonomy. All failure diagnoses remain 100% rule-based.
- **Status**: Implemented & Verified in `blindspot/semantic/client.py` and `testing/behavioral.py`.

---

## Decision 19: Human Verification & Frozen Semantic Reference Invariant
- **Context**: Automated semantic annotations must allow researcher oversight and must remain identical across all evaluated models.
- **Decision**: Provide interactive human override controls (`[Accept]`, `[Change to ...]`) with full audit provenance. The verified semantic reference set is frozen (`ref_set.freeze()`) prior to model execution, guaranteeing identical semantic ground truth across all 5 benchmark models.
- **Status**: Implemented & Verified in `blindspot/semantic/service.py` and `ui/components.py`.

---

## Decision 20: 2-Class / 3-Class Semantic Compatibility (`NOT_DIRECTLY_REPRESENTABLE`)
- **Context**: A binary model can never explicitly predict `NEUTRAL`. When the semantic ground truth is `NEUTRAL`, coercing binary outputs into positive/negative distorts ground truth.
- **Decision**: Keep semantic ground truth and model output space completely decoupled. When semantic reference is `NEUTRAL`, a binary model's forced choice is recorded as `NOT_DIRECTLY_REPRESENTABLE` (`BINARY_FORCED_POLARITY`), preserving empirical reality. Multiclass models record `DIRECTLY_COMPATIBLE`.
- **Status**: Implemented & Verified in `blindspot/core/types.py` and `testing/behavioral.py`.

---

## Decision 21: Persistent SHA-256 Semantic Caching and Offline Fallback
- **Context**: API latency, rate limits, and network volatility could impair reproducibility or crash experiments when credentials are missing.
- **Decision**: Implement persistent JSON caching keyed by `SHA256(normalized_sentence + version)`. If `GEMINI_API_KEY` is absent, automatically fall back to `Offline (Manual Mode)` with linguistic heuristics, allowing uninterrupted research.
- **Status**: Implemented & Verified in `blindspot/semantic/cache.py` and `client.py`.

---

## Decision 22: Gemini Semantic Ground Truth as Authoritative Expected Across Pipeline
- **Context**: The UI previously rendered legacy heuristic expectation strings (`FLIP -> NEGATIVE`, `PRESERVE -> POSITIVE`) alongside the Semantic Reference (`NEUTRAL [PRESERVE]`), causing visual contradiction and misrepresenting compliance as Expected Flip Rate.
- **Decision**: Establish the Gemini / verified semantic ground truth as the authoritative `Expected` contract across all pipeline modules. `Expected (Gemini Ref)` displays the canonical polarity and semantic relation (`NEGATIVE [REVERSE]`, `NEUTRAL [PRESERVE]`, `POSITIVE [SHIFT_FROM_NEUTRAL]`). In the Stratified Behavioral Summary, `Expected Flip Rate` measures suite expectation prevalence consistently across all models, while `Reversal Compliance` independently quantifies model compliance.
- **Status**: Implemented & Verified across `blindspot/testing/behavioral.py`, `analysis/cross_model.py`, `ui/comparison.py`, and `execution/runner.py`.

---

## Decision 23: Live Application UI & Logical Flow Audit Verification
- **Context**: Comprehensive live audit conducted on real running Streamlit application (`http://localhost:8501`) using Chrome CDP automation across all 6 primary domains and 15 state checkpoints.
- **Decision**: Verified that the primary behavioral analysis engine, pipeline count integrity (`Planned == Executed == Analyzed == Reported`), and rule-based failure taxonomy function accurately. Identified 6 high-value findings documented in `audit_reports/FULL_LIVE_UI_AUDIT.md`:
  1. Need custom probe text validation to block score leakage (P0).
  2. Need explainability mode selector to prevent mandatory 16-minute LIME+SHAP runs on 5 models (P1).
  3. Need live run session reconnection upon browser reload (P1).
  4. Need zombie run detection in Run Archive (P2).
  5. Sequential section numbering fix in Probe Lab (P3).
  6. Sidebar version label alignment to v2.7.1 (P3).
- **Status**: Documented & Preserved; fixes queued for staged implementation upon review.

---

## Decision 24: Canonical Model Identity and Twitter Collision Elimination
- **Context**: Slicing model identifier strings (`m[:14]`, `m.split('/')[-1][:14]`) caused `cardiffnlp/twitter-roberta-base-sentiment` and `cardiffnlp/twitter-roberta-base-sentiment-latest` to collide as `"twitter-robert"`, collapsing two distinct models into one and overwriting dictionary keys and Matplotlib tick labels.
- **Decision**: Define immutable canonical model identity mappings in `blindspot/models/registry.py` (`CANONICAL_MODEL_NAMES`) providing unambiguous `display_name`, `short_name`, `abbrev`, `task_space`, and `label_schema`. The two Twitter models are explicitly titled `Twitter-RoBERTa (Latest)` and `Twitter-RoBERTa (Base)`. All dictionary aggregations and visualizations must key off canonical IDs or unique short names.
- **Status**: Implemented & Verified in `blindspot/models/registry.py`, `reporting/thesis_graphs.py`, and `ui/comparison.py`.

---

## Decision 25: Model Completeness Contract and Zero Silent Dropping
- **Context**: Incomplete or partial runs previously dropped missing models from tables, misleading researchers into believing fewer models were evaluated.
- **Decision**: Enforce a strict model completeness contract (`expected_models` vs `executed_models`). The UI renders a prominent Model Completeness Banner and retains all 5 configured model columns in stable canonical order. Unexecuted models are explicitly displayed as `— NOT RUN`, never omitted.
- **Status**: Implemented & Verified in `blindspot/ui/comparison.py`.

---

## Decision 26: Cell-Level Deviation Highlighting and Non-Color-Alone Visual Semantics
- **Context**: Legacy comparison tables colored entire rows red when any single model deviated, forcing researchers to mentally evaluate 5 columns to isolate the failing model.
- **Decision**: Highlight exclusively the **specific cell that deviates** (`⚠ DEVIATION`, `✕ FAILURE`), keeping compliant models subtle (`✓ MATCH`). In accordance with accessibility guidelines, visual state must never rely on color alone: every status combines a Unicode icon, explicit status text, and contrastive styling.
- **Status**: Implemented & Verified in `blindspot/ui/design_system.py` and `ui/comparison.py`.

---

## Decision 27: Four-Level Information Hierarchy and Structured Failure Register
- **Context**: The failure lab lacked high-level structured registers, displaying raw unorganized cards. Tables were overloaded with internal hashes and floating-point noise.
- **Decision**: Structure output pages around a 4-level hierarchy: Level 1 (Summary KPIs), Level 2 (Where models disagreed / deviations), Level 3 (Why it is a problem / structured failure register), Level 4 (Raw data & attribution inspector in expandable drawers). Primary tables display clean transitions (`POS ➔ NEG`) and compact percentage point shifts (`-1.8 pp`).
- **Status**: Implemented & Verified in `blindspot/ui/comparison.py` and `ui/failure_lab.py`.

---

## Decision 28: Separation of Operational Metrics and Taxonomy Failure Breakdown into Dedicated Tabs
- **Context**: The `STRATIFIED BEHAVIORAL METRICS SUMMARY` table previously floated above the tabs, creating an immediate, near-identical duplicate with the `Descriptive Behavioral Profiles` table located inside the `🧬 BEHAVIORAL FINGERPRINTS` tab. Furthermore, failure taxonomy counts and failure types were buried inside broad metric columns without an organized cross-model breakdown.
- **Decision**: 
  1. Remove the redundant top-level `STRATIFIED BEHAVIORAL METRICS SUMMARY` table floating above the comparison tabs, creating a clean direct transition from the baseline stimuli cards to the tabbed workspace.
  2. Consolidate complete quantitative operational characteristics (`Accuracy`, `ECE`, `Mean Confidence`, `Observed Flip Rate`, `Expected Flip Rate`, `Compliance`, `Mean Shift`, `Total Probes`) inside `🧬 BEHAVIORAL FINGERPRINTS`.
  3. Introduce a dedicated 5th tab: `🏷️ MODELS & FAILURES` featuring:
     - Cross-model KPI summary cards (`Total Failures`, `BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`).
     - Structured breakdown table displaying per-model failure counts, overall failure rates, exact counts across each taxonomy category (`BLIND (Invariance)`, `SPURIOUS (Shortcut)`, `MISWEIGHTED (Clause)`, `UNDETERMINED`), and the empirical `Primary Failure Mode`.
     - Interactive `🔍 PER-MODEL FAILURE EVIDENCE LOG` with model selection and complete failure diagnostic evidence rows.
- **Status**: Implemented & Verified in `blindspot/ui/comparison.py` with visual CDP regression testing.

---

## Decision 29: Elimination of False Neutrals via Antigravity Exact Polarity Analyzer
- **Context**: Gemini and offline heuristic fallbacks frequently defaulted to `NEUTRAL` for sentences with explicit positive or negative vocabulary, contrast clauses ("He is a Good boy but very naughty", "i am healthy but still hospitalized"), and negated attributes ("not healthy", "not good"), polluting the semantic cache with 39 false neutral annotations.
- **Decision**:
  1. **Antigravity Exact Sentiment Analyzer (`blindspot/semantic/analyzer.py`)**: Implement deterministic linguistic polarity prediction leveraging VADER augmented with health/medical, behavioral/conduct, and performance lexicons.
  2. **Discourse-Weighted Contrast Resolution**: For contrastive structures ("X but Y", "X however Y", "although X, Y"), the adversative clause carries dominant communicative weight (75% vs 25%), ensuring "healthy but hospitalized" resolves to `NEGATIVE` and "expensive but exquisitely engineered" resolves to `POSITIVE`.
  3. **Strict Gemini Prompt Directive**: Add non-neutrality rules explicitly barring false neutrals on sentiment-bearing language and defining strict criteria for objective `NEUTRAL`.
  4. **Antigravity Calibration Guardrail (`client.py`)**: If Gemini returns `NEUTRAL` on text with strong sentiment signals, automatically calibrate to `POSITIVE` or `NEGATIVE` with explicit audit rationale.
  5. **Cache Migration**: Migrated all 39 false neutral entries in `cache/semantic_cache.json` to exact polarities.
- **Status**: Implemented & Verified in `blindspot/semantic/analyzer.py`, `client.py`, `service.py`, and `tests/test_exact_sentiment_analyzer.py`.

---

## Decision 30: Semantic Reference Integrity, Official GenAI SDK, and Separation of Polarity from Relation
- **Context**: The existing system exhibited false semantic reference behaviors: fabricating `confidence=0.75` when offline, conflating syntactic truth-conditional changes with affective sentiment flips (e.g. hardcoding `expected_flip = True` for P001 negation), mutating relations in the execution runner, penalizing binary models on `NEUTRAL` inputs, and labeling automated suggestions as "Final Ground-Truth".
- **Decision**:
  1. **Strictly Purge Fabricated Confidence**: Never copy or hardcode confidence. If Gemini did not run, `gemini_confidence` and `confidence` are strictly `None`.
  2. **Official Google GenAI Python SDK Integration**: Use the official `google-genai` library (`from google import genai`) with JSON schema structured output, robust retry/backoff, and Generative Language API fallback. Authentication strictly via `GEMINI_API_KEY` or `GOOGLE_API_KEY`.
  3. **Disentangle Polarity from Relation**: Polarity represents affective sentiment (`POSITIVE`, `NEGATIVE`, `NEUTRAL`). Relation represents the linguistic transformation (`PRESERVE_POLARITY`, `REVERSE_POLARITY`, `SHIFT_TO_NEUTRAL`, `SHIFT_FROM_NEUTRAL`, `CONTRAST_SHIFT`, `MEANING_CHANGED`, `UNCERTAIN`). Negation changes propositional truth conditions but does not universally invert sentiment polarity (e.g., factual statements remain `NEUTRAL`).
  4. **P001 Linguistic Intent**: P001 negation probe is classified as `semantic_intent = "ADD_NEGATION"` and `expected_flip = False`. The semantic relation is derived authoritatively from verified polarities.
  5. **Runner Immutability**: The execution runner strictly executes the frozen `RunPlan` and never mutates semantic relations or expectations.
  6. **Model Capability Alignment**: Binary models on `NEUTRAL` references yield `NOT_DIRECTLY_REPRESENTABLE` / `UNREPRESENTABLE_NEUTRAL`, not `BLIND`. 3-class neutral preservation is evaluated without spurious failure.
  7. **Cryptographic Cache Keying**: Key cache entries by `normalized_text|provider|model|schema_version|annotation_version` and purge legacy entries with fabricated confidence.
  8. **Honest Provenance in UI**: Replace "Final Ground-Truth" with "Semantic Reference", "Semantic Reference (Unverified)", "Gemini Semantic Reference", or "Human-Verified Semantic Reference".
- **Status**: Implemented & Verified in `blindspot/semantic/`, `blindspot/execution/runner.py`, `blindspot/perturbations/shared.py`, `blindspot/testing/behavioral.py`, `blindspot/ui/components.py`, and `tests/test_semantic_integrity_spec.py`.




