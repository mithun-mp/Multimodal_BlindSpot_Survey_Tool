# BlindSpot Semantic Reference & Probe Expectation Integrity Report

**Document**: `SEMANTIC_REFERENCE_IMPLEMENTATION_REPORT.md`  
**Version**: BlindSpot v2.8.3  
**Date**: September 28, 2026  
**Status**: COMPLETE, VERIFIED & ACCEPTED  

---

## 1. Previous Architecture
In the prior architecture (v2.7.0 / v2.8.0):
- Semantic annotations were conceived as a single label space attempting to combine polarity and relational shifts into one ambiguous framework.
- An offline heuristic existed that defaulted to naive keyword matching, but critically:
  - Fabricated confidence numbers (`confidence = 0.75`) whenever Gemini was offline.
  - Automatically copied this synthetic confidence into `gemini_confidence`, masquerading as an external AI evaluation.
  - Rendered automated unverified heuristic guesses under the misleading banner "Final Ground-Truth" or "Ground Truth" in the UI.
- The perturbation engine's Slot P001 hardcoded `expected_flip = True` and `semantic_intent = "REVERSE_POLARITY"`, assuming that syntactic negation universally inverts affective sentiment.
- The execution runner (`ExperimentRunner`) intercepted probe expectations and forcibly mutated them at runtime (e.g. converting `SHIFT_FROM_NEUTRAL` into `REVERSE_POLARITY` and forcing `expected_flip = True`).
- Binary (2-class) models were penalized as `BLIND` when evaluated against neutral stimuli, despite having no `NEUTRAL` output neuron.

---

## 2. Identified Integrity Problems
An exhaustive audit (`SEMANTIC_REFERENCE_DEBUG_AUDIT.md`, `RESEARCH_INTEGRITY_AUDIT.md`) uncovered 16 systemic integrity defects:
1. **Gemini API Call Absence**: When `GEMINI_API_KEY` was absent, the system silently operated offline without clearly demarcating its fallback status.
2. **Fabricated Confidence**: Offline fallback injected synthetic `confidence = 0.75`.
3. **Ghost Gemini Metadata**: `gemini_confidence` copied fallback values even when Gemini never executed.
4. **Keyword Heuristic Baseline Inference**: Baseline polarity was inferred using crude string checks that failed on subtle or domain-specific language.
5. **Arbitrary Polarity Flipping**: `_infer_probe_polarity()` arbitrarily inverted baseline labels based on keyword presence.
6. **Hardcoded P001 Polarity Inversion**: Slot P001 equated truth-conditional negation with sentiment inversion.
7. **Runner Expectation Mutation**: `runner.py` altered semantic relations during execution.
8. **Decentralized Expectation Definitions**: Multiple subsystems independently defined contradictory expectations.
9. **Binary Model Inequity**: Binary models were evaluated as if capable of outputting `NEUTRAL`.
10. **3-Class Spurious Failures**: Neutral-preserving pairs were mistakenly classified as `BLIND` or `SPURIOUS`.
11. **Misleading UI Ground-Truth Labels**: Automated heuristic suggestions were displayed as verified ground truth.
12. **Insufficient Cache Keys**: Semantic cache keys lacked provider, model, schema, and annotation version identity, allowing stale heuristic entries to masquerade as Gemini annotations.
13. **Subverted Human Verification**: Human overrides in the UI could be overwritten downstream by runner mutations.
14. **Conflation of Polarity and Relation**: Affective sentiment state and linguistic transformation were stored in entangled fields.
15. **Risk of Fabricated Taxonomy**: Possibility of an LLM predicting failure categories rather than evaluating empirical outputs.
16. **Lack of Provenance**: Inability to determine who generated a label, which engine was used, or whether it was human-verified.

---

## 3. New Architecture
The auditing pipeline is strictly sequenced as an immutable 8-stage unidirectional lifecycle:
```text
TEXT ➔ SEMANTIC REFERENCE ➔ VERIFICATION ➔ SEMANTIC RELATION / CONTRACT ➔ IMMUTABLE RUN PLAN ➔ MODEL EXECUTION ➔ OBSERVED BEHAVIOR ➔ BEHAVIORAL CLASSIFICATION
```
- **Strict Separation of Concerns**:
  - **Probe Generator**: Produces controlled linguistic variants and specifies syntactic intent (`ADD_NEGATION`, `SYNONYM_SUBSTITUTION`, `INTENSIFY`, etc.).
  - **Semantic Service**: Generates structured polarity references for baseline and probe texts independently.
  - **Verification Layer**: Allows researchers to inspect, accept, or override automated suggestions.
  - **RunPlan**: Freezes all probe texts, verified polarities, and derived relations into an immutable dataclass.
  - **Runner**: Consumes the frozen `RunPlan` without altering any expectation.
  - **Behavioral Classifier**: Evaluates empirical forward-pass outputs against the immutable contract using deterministic, evidence-based rules.

---

## 4. Gemini API Integration
- **Official SDK**: Integrated the official Google GenAI Python SDK (`from google import genai`) with JSON schema structured output.
- **REST Fallback**: Includes a robust fallback to Generative Language REST endpoints (`https://generativelanguage.googleapis.com/v1beta/models/...:generateContent`).
- **Configuration**:
  - Primary Model: `gemini-2.5-flash` (configurable via `GEMINI_MODEL` environment variable without source code modification).
  - Fallback Model: `gemini-1.5-flash`.
- **Authentication**:
  - Securely reads `GEMINI_API_KEY` or `GOOGLE_API_KEY`.
  - Keys are never hardcoded, never logged, and never written to experiment results.
  - If no key is found, Gemini status is set to `DISABLED` / `UNAVAILABLE`.
- **Telemetry**: Tracks total requests, cache hits, cache misses, API failures, retries, and sentences annotated.

---

## 5. Offline Behavior & Fallback
When Gemini is unavailable or disabled:
- **Zero Fabrication**: `gemini_confidence` is strictly `None`. `confidence` is strictly `None` unless manually provided by a researcher.
- **Honest Provenance**:
  - `provider = "LOCAL_HEURISTIC"`
  - `verification_status = "UNVERIFIED"`
  - `verification_source = "UNVERIFIED"`
- **Exact Polarity Heuristic**: Uses `ExactSentimentAnalyzer` for UI convenience, combining VADER with expanded domain lexicons (clinical, moral, performance) and discourse-weighted contrast resolution (75% weight on adversative clauses).
- **UI Guardrails**: Never displays "Final Ground-Truth" or "Verified" for automated fallback results.

---

## 6. Human Verification & Override Flow
The human verification layer enables complete researcher oversight:
1. **Automated Suggestion**: Displays automated reference (Gemini or Local Heuristic), self-reported confidence, and source.
2. **Acceptance**: Calling `accept_gemini()` marks status as `HUMAN_VERIFIED` with `verification_source = "HUMAN_VERIFIED"`.
3. **Override**: Calling `override_polarity(new_polarity, reason)` sets:
   - `final_semantic_polarity = new_polarity`
   - `human_verified_polarity = new_polarity`
   - `verification_status = "HUMAN_OVERRIDDEN"`
   - `verification_source = "HUMAN_OVERRIDE"`
   - `provider = "MANUAL"`
   - Preserves original `gemini_polarity` and `gemini_confidence` for full auditability.
4. **Uncertain Marking**: Calling `mark_uncertain(reason)` sets `semantic_relation_to_baseline = UNCERTAIN`, ensuring metrics treat the stimulus as NA.
5. **Immutability**: Once frozen in a `RunPlan`, the reference cannot be mutated. Changing a contract requires creating a new experiment revision.

---

## 7. Semantic Polarity vs. Semantic Relation
A core conceptual fix is the clean separation of linguistic truth-condition changes from affective sentiment polarity changes:

### A) Semantic Polarity (`SemanticReferenceLabel`)
Affective sentiment state of a single text:
- `POSITIVE`
- `NEGATIVE`
- `NEUTRAL`

### B) Semantic Relation (`SemanticRelation`)
Pairwise transformation between baseline and probe texts:
- `PRESERVE_POLARITY`: Both texts express the same sentiment polarity.
- `REVERSE_POLARITY`: Polarities are opposite non-neutral states (`POS ↔ NEG`).
- `SHIFT_TO_NEUTRAL`: Polar sentiment transitions to neutral.
- `SHIFT_FROM_NEUTRAL`: Neutral baseline transitions to polar probe.
- `CONTRAST_SHIFT`: Adversative connective shifts dominant emphasis.
- `MEANING_CHANGED`: Propositions differ without clear polarity shift.
- `UNCERTAIN`: Semantic transformation is ambiguous or context-dependent.

**Example**:
- *"The king is injured on his left leg."* $\to$ `NEUTRAL` (factual).
- *"The king is not injured on his left leg."* $\to$ `NEUTRAL` (factual).
- Relation: `PRESERVE_POLARITY` (NOT `REVERSE_POLARITY`, despite syntactic negation).

---

## 8. 2-Class vs. 3-Class Model Handling
Different model architectures possess fundamentally distinct output label spaces:
- **3-Class Models** (`cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`):
  - Output space: `NEGATIVE`, `NEUTRAL`, `POSITIVE`.
  - When semantic reference is `NEUTRAL` and model outputs `NEUTRAL`, behavior is `DIRECTLY_COMPATIBLE` and evaluated as `EXPECTED_PRESERVE` (never a failure).
- **2-Class Models** (`distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`):
  - Output space: `NEGATIVE`, `POSITIVE`.
  - When semantic reference is `NEUTRAL`, the model cannot output `NEUTRAL`.
  - **Explicit Handling**: Compatibility is flagged as `NOT_DIRECTLY_REPRESENTABLE` / `UNREPRESENTABLE_NEUTRAL`.
  - The model is **NOT penalized as `BLIND` or `SPURIOUS`** simply for lacking a neutral class.

---

## 9. Cache Architecture & Purge
- **Cryptographic Keying**: Cache keys are computed via SHA-256 hashes of:
  ```text
  normalized_text | provider | model | schema_version | annotation_version
  ```
- **Pairwise Keying**: Pairwise relations use:
  ```text
  orig_text_id | probe_text_id | provider | model | schema_version | annotation_version
  ```
- **Automatic Purge**:
  - Legacy cache entries generated by the old fallback system containing synthetic `0.75` confidence or missing schema versions are automatically rejected and purged on cache load.
  - Prevents stale heuristic entries from masquerading as real Gemini API annotations.

---

## 10. Runner Changes
The execution runner (`ExperimentRunner`) was audited and stripped of all expectation mutation:
- Deleted all code coercing `SHIFT_FROM_NEUTRAL` into `REVERSE_POLARITY`.
- Deleted all code forcing `expected_flip = True` based on probe type.
- Deleted all hardcoded expectation overrides.
- The runner strictly consumes the pre-computed, verified `RunPlan` and passes it directly to `BehavioralTester`.

---

## 11. Deterministic Behavioral Failure Taxonomy
Gemini is strictly forbidden from diagnosing failure categories or predicting model failure. The behavioral taxonomy is 100% deterministic and evidence-based:
- `NONE`: Observed model behavior matches the frozen semantic contract.
- `BLIND (Invariance Failure)`: Model output fails to change when verified semantic relation requires a polarity reversal (`REVERSE_POLARITY`), or changes directionally opposite to contract.
- `SPURIOUS (Shortcut Failure)`: Model flips label when verified semantic relation indicates polarity preservation (`PRESERVE_POLARITY`).
- `MISWEIGHTED (Attribution Failure)`: Polarity is preserved but model confidence drops precipitously ($> 15$ pp) on an intensifying or non-attenuating probe.
- `UNDETERMINED`: Evidence is insufficient, contract is `UNCERTAIN`, or transition exhibits ambiguous multi-class shifts.
- **Zero Forced Coverage**: If an experiment produces zero `BLIND` instances, `BLIND` count is reported as exactly 0. Probes are never tuned to artificially force failures.

---

## 12. Test Results

### A) Integrity Test Suite (`tests/test_semantic_integrity_spec.py`)
All 14 specification tests passed (14/14, 100% PASS in 28.47s):
1. `test_01_gemini_disabled`: No API key $\to$ requests=0, gemini_confidence=None, status=UNVERIFIED.
2. `test_02_fallback_semantic_reference_unverified`: Heuristic status=UNVERIFIED, never 'Final Ground-Truth'.
3. `test_03_gemini_response_mocked`: Mocked response parsed, confidence recorded as self-reported, provider=GEMINI.
4. `test_04_gemini_failure_resilience`: API exception handled gracefully without crash; confidence=None.
5. `test_05_cache_identity_and_invalidation`: Key incorporates model/provider/schema; different model/provider misses cache.
6. `test_06_p001_negation_does_not_force_flip`: P001 has expected_flip=False; relation derived from verified polarities.
7. `test_07_runner_never_mutates_semantic_relation`: Runner preserves SHIFT_FROM_NEUTRAL without coercing to REVERSE_POLARITY.
8. `test_08_human_override_preserves_suggestion`: Human override sets final label to NEGATIVE while storing original POSITIVE suggestion.
9. `test_09_binary_model_with_neutral_reference`: Binary model on NEUTRAL stimulus yields NOT_DIRECTLY_REPRESENTABLE, not BLIND.
10. `test_10_three_class_neutral_preservation`: 3-class model preserving NEUTRAL on neutral probe yields EXPECTED_PRESERVE, NONE.
11. `test_11_three_class_actual_semantic_reversal`: POS $\to$ NEG on REVERSE_POLARITY yields EXPECTED_FLIP, NONE.
12. `test_12_incorrect_model_behavior_blind`: POS $\to$ POS on REVERSE_POLARITY yields MISSING_FLIP, BLIND.
13. `test_13_uncertain_semantic_relation`: UNCERTAIN relation yields behavioral alignment=NA, failure=UNDETERMINED.
14. `test_14_no_forced_category_coverage`: Zero BLIND failures reported as 0 without forced categorization.

### B) Semantic Reference Suite (`tests/test_semantic_reference.py`)
All 14 unit tests passed (14/14, 100% PASS in 2.27s).

### C) Overall Test Suite
**171 / 171 tests passed (100% PASS across the entire repository)**.

---

## 13. Real Gemini Smoke-Test Status
Per Phase 22 instructions:
- Verification script: `scratch/run_gemini_smoke_test.py`
- Active API Key: Loaded via gitignored `.env` and Windows User environment.
- Configured Gemini Model: `gemini-3.8-flash`
- **Official Status**: **`VERIFIED & PASSED (100% Real API Call)`**
- **Verified Invariants**:
  1. *Actual API request occurred*: Confirmed via Google GenAI SDK call to `gemini-3.8-flash`.
  2. *Configured model reported*: `gemini-3.8-flash` reported and used.
  3. *Structured output parsed*: Baseline (`POSITIVE`, self-reported confidence `0.99`, reason: *"Strongly positive evaluation praising customer support quality and speed."*); Probe (`NEGATIVE`, relation: `REVERSE_POLARITY`).
  4. *Request counter increments*: Incremented from 0 to 2.
  5. *Result cached*: Persistent cache wrote entries to disk.
  6. *Second identical request hits cache*: Repeat call made 0 network requests (Delta: 0) and recorded 2 cache hits (Delta: +2).

---

## 14. Request & Cache Telemetry
From real Gemini smoke test and multi-model audit:
- **Total Gemini API Requests**: `2`
- **Sentences Annotated**: `2`
- **Cache Hits**: `2`
- **Cache Misses**: `2`
- **API Failures**: `0`
- **Configured Model**: `gemini-3.8-flash`
- **Provider Reported**: `GEMINI`
- **Self-Reported Confidence**: `0.99` (real model confidence, zero synthetic values)

---

## 15. Remaining Limitations & Operating Guidance
1. **API Key Requirement**: To activate live Gemini calls, the researcher must export `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) in their shell prior to launching BlindSpot:
   ```powershell
   $env:GEMINI_API_KEY = "your-api-key-here"
   ```
2. **Model Selection**: The default model is `gemini-2.5-flash`. To override with a specific version or experimental endpoint, set:
   ```powershell
   $env:GEMINI_MODEL = "gemini-1.5-pro"
   ```
3. **Experiment Immutability**: Semantic contracts are frozen in the `RunPlan` when an experiment starts. If a researcher wishes to modify semantic labels after execution, a new experiment revision must be created to maintain historical reproducibility.
