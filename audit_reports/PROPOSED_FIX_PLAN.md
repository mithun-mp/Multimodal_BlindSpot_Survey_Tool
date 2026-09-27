# BLINDSPOT — ARCHITECTURAL FIX PLAN FOR SEMANTIC REFERENCE & PROBE EXPECTATION

**Document Reference**: `audit_reports/PROPOSED_FIX_PLAN.md`  
**Prerequisite Document**: `audit_reports/SEMANTIC_REFERENCE_DEBUG_AUDIT.md`  
**Status**: PROPOSED — PENDING USER APPROVAL (READ-ONLY AUDIT PHASE)  
**Target System**: Semantic Reference Engine, Probe Generation, Behavioral Testing, Runner, Cache, and UI

---

## 1. ARCHITECTURAL OVERVIEW

Following the findings of the comprehensive debug audit, this plan details the exact architectural refactoring required to restore scientific integrity to BlindSpot.

### Core Principle: The Decoupled Semantic-Behavioral Hierarchy
1. **Linguistic Perturbation Engine**: Generates controlled structural/lexical mutations with linguistic intent (`ADD_NEGATION`, `SYNONYM_SUBSTITUTION`, `APPEND_ADVERSATIVE`), but **never hardcodes sentiment flips**.
2. **Canonical Semantic Reference Layer**: Establishes objective polarity (`POSITIVE`, `NEGATIVE`, `NEUTRAL`) for baseline and perturbed text via Gemini API (when online) or deterministic exact linguistic parsing (`ExactSentimentAnalyzer`).
3. **Semantic Relation Contract**: Derives the exact semantic relationship between baseline and probe (`PRESERVE_POLARITY`, `REVERSE_POLARITY`, `SHIFT_TO_NEUTRAL`, `SHIFT_FROM_NEUTRAL`, `INTENSIFY`, `DOWNTONE`).
4. **Capability-Aware Behavioral Evaluator**: Evaluates benchmark models against the semantic relation according to their label space (2-class SST-2 vs. 3-class RoBERTa), preventing false failure diagnoses.

```text
               ORIGINAL TEXT
                     │
                     ▼
          BASELINE SEMANTIC REFERENCE
          (Gemini / Exact Analyzer)
                     │
                     ├───────────────────────────────┐
                     ▼                               ▼
            Human Verification                Target Models
                     │                               │
            VERIFIED BASELINE LABEL           MODEL PREDICTIONS
                     │                               │
                     │                               │
             PERTURBED PROBE                         │
                     │                               │
                     ▼                               │
           PROBE SEMANTIC REFERENCE                  │
          (Gemini / Exact Analyzer)                  │
                     │                               │
                     ▼                               ▼
          CANONICAL SEMANTIC RELATION         OBSERVED TRANSITIONS
       (PRESERVE, REVERSE, SHIFT_TO/FROM)   (e.g., NEU → NEU, POS → NEG)
                     │                               │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     CAPABILITY-AWARE EXPECTATION CHECK
                       (2-Class vs. 3-Class Mapping)
                                     │
                                     ▼
                      EMPIRICAL FAILURE TAXONOMY
                      (BLIND, SPURIOUS, MISWEIGHTED)
```

---

## 2. DETAILED ACTIONABLE FIX PROPOSALS

### FIX 1: Disentangle Syntactic Negation from Sentiment Polarity Reversal (SR-001)

#### Problem:
`blindspot/perturbations/shared.py` (lines 105–106 and 374–386) unconditionally assumes that inserting a negation operator (`not`) constitutes a sentiment reversal (`expected_flip=True`, `semantic_intent=REVERSE_POLARITY`, `expected_label_relation=DIFFERENT_LABEL`). This assumption is false for neutral/factual statements ("The king is injured" $\to$ "The king is not injured").

#### Implementation Plan:
1. In `blindspot/perturbations/shared.py`:
   - Change `LinguisticProbeCatalog.generate_candidates()` for slot `P001`:
     - Set `semantic_intent = SemanticIntent.ADD_NEGATION.value` (or `SemanticIntent.INVERT_TRUTH_VALUE`).
     - Remove hardcoded `expected_flip = True`.
     - Set `expected_flip = None` (dynamically resolved once semantic references exist) or default to `expected_flip = False` when baseline polarity is unknown.
     - Set `rationale = "Linguistic negation altering propositional truth conditions."` (explicitly removing the misleading phrase "truth-conditional semantic polarity").
2. In `blindspot/perturbations/shared.py` (`infer_expected_semantic_effect`):
   - For `negation`: return `("negate_predicate", False)` instead of `("invert", True)`.
3. In `SemanticReferenceSet._recompute_relations()` (`types.py`):
   - Make `_recompute_relations()` the **sole authoritative resolver** of expected sentiment transitions.
   - If `base_pol in (POSITIVE, NEGATIVE)` and `probe_pol == opposite`: `expected_flip = True`, `relation = REVERSE`.
   - If `base_pol == probe_pol`: `expected_flip = False`, `relation = PRESERVE`.
   - If `base_pol == NEUTRAL` and `probe_pol == NEUTRAL`: `expected_flip = False`, `relation = PRESERVE`.
   - If `base_pol == NEUTRAL` and `probe_pol in (POSITIVE, NEGATIVE)`: `expected_flip = False` (for binary models) / `expected_state_change = True` (for 3-class models), `relation = SHIFT_FROM_NEUTRAL`.

- **Files Affected**: `blindspot/perturbations/shared.py`, `blindspot/semantic/types.py`, `blindspot/core/types.py`
- **Data Contract Affected**: `LinguisticProbe` schema, `ProbeExpectation` schema.
- **UI Affected**: Probe Lab Section 02 badge renders `ALTERS TRUTH CONDITION` instead of false `EXPECTS FLIP`.
- **Research Interpretation**: Eliminates the fundamental scientific error of demanding sentiment flips on factual negations.
- **Backward Compatibility**: Fully backward compatible; existing datasets with explicit sentiment reversals (`POSITIVE → NEGATIVE`) resolve to `expected_flip = True` dynamically.
- **Tests Required**: Unit tests verifying "The king is injured" $\to$ "The king is not injured" yields `expected_flip = False`.

---

### FIX 2: Eliminate Fabricated 75% Confidence and Ghost Gemini Values (SR-004, SR-005)

#### Problem:
Offline fallback constructors hardcode `confidence = 0.75` and write it to `gemini_confidence`, causing the UI to display `Confidence: 75%` as if Gemini had produced an empirical probability estimate.

#### Implementation Plan:
1. In `blindspot/semantic/types.py`:
   - In `SemanticAnnotation.__post_init__`, **DELETE** lines 140–141:
     ```python
     # REMOVE THIS BUG:
     # if self.gemini_confidence is None:
     #     self.gemini_confidence = self.confidence
     ```
   - If `verification_source == "MANUAL"` or `verification_source == "ANTIGRAVITY_EXACT"`:
     - `gemini_polarity = None`
     - `gemini_confidence = None`
     - `confidence = None` (or `confidence = exact_analyzer_score` with `is_calibrated = False`).
2. In `blindspot/semantic/service.py`:
   - Remove all occurrences of hardcoded `0.75`.
   - When Gemini is offline, set `confidence = analyzer_conf` if exact analyzer is used, or `None` if manual unannotated.
   - Set `reason` to clearly state: `"[Offline Exact Engine] {reason}"` or `"[Unverified Manual Baseline]"`.
3. In `blindspot/ui/components.py`:
   - In lines 837 and 890, check if `annot.confidence` is `None` or if source is `MANUAL`:
     - If `annot.confidence is not None and annot.verification_source != "MANUAL"`: render `{annot.confidence*100:.0f}%`.
     - Else: render `<span style="color:#94a3b8;">N/A (Offline/Manual)</span>`.

- **Files Affected**: `blindspot/semantic/types.py`, `blindspot/semantic/service.py`, `blindspot/ui/components.py`
- **Data Contract Affected**: `SemanticAnnotation` (allows `confidence: Optional[float] = None`, `gemini_confidence: Optional[float] = None`).
- **UI Affected**: Semantic Reference Panel renders `Confidence: N/A (Manual)` instead of `75%`.
- **Research Interpretation**: Restores statistical integrity; stops fabricating model confidence.
- **Backward Compatibility**: Deserializer handles `None` or missing confidence gracefully.
- **Tests Required**: Regression tests ensuring `gemini_confidence` is strictly `None` when offline.

---

### FIX 3: Disambiguate "Ground-Truth" Terminology in UI & System Reports (SR-006)

#### Problem:
The UI renders `Final Ground-Truth: NEUTRAL` even when the label was generated by an unverified automated heuristic.

#### Implementation Plan:
1. In `blindspot/ui/components.py`:
   - Update line 838:
     - If `base_annot.verification_status == VerificationStatus.HUMAN_OVERRIDE` or `VerificationStatus.HUMAN_VERIFIED`:
       `<div>Verified Ground-Truth: <strong style="color:#10b981;">{base_annot.final_semantic_polarity.value}</strong> (Human Verified)</div>`
     - Else if `base_annot.verification_source == "ANTIGRAVITY_EXACT"`:
       `<div>Canonical Reference: <strong style="color:#38bdf8;">{base_annot.final_semantic_polarity.value}</strong> (Exact Semantic Analyzer)</div>`
     - Else:
       `<div>Semantic Reference: <strong style="color:#f59e0b;">{base_annot.final_semantic_polarity.value}</strong> (Unverified Suggestion)</div>`
2. In `blindspot/ui/comparison.py`:
   - Rename `SEMANTIC GROUND TRUTH REFERENCE DETAILS` to `CANONICAL SEMANTIC REFERENCE & EXPECTATION CONTRACT`.
3. In `blindspot/reporting/report_generator.py`:
   - Clarify Section 132: "Canonical Semantic Reference labels serve as the evaluation benchmark. Unverified automated labels are designated as references, while human-confirmed labels are designated as verified ground truth."

- **Files Affected**: `blindspot/ui/components.py`, `blindspot/ui/comparison.py`, `blindspot/reporting/report_generator.py`
- **Data Contract Affected**: None (string presentation and UI semantics only).
- **UI Affected**: Accurate, honest labeling across Probe Lab, Experiment Lab, and Comparison tabs.
- **Research Interpretation**: Respects academic standards by reserving "Ground Truth" for verified labels.
- **Backward Compatibility**: 100% backward compatible.
- **Tests Required**: UI component snapshot tests verifying label strings under different verification statuses.

---

### FIX 4: Remove Runner Overwrite of Semantic Contracts (SR-002, SR-003)

#### Problem:
`blindspot/execution/runner.py` (lines 235–239) forcibly overwrites probe objects:
```python
is_flip = rel_val in ("REVERSE", "SHIFT_FROM_NEUTRAL")
p.expected_flip = is_flip
p.expected_semantic_effect = "invert" if is_flip else "preserve"
p.semantic_intent = "REVERSE_POLARITY" if is_flip else "PRESERVE_MEANING"
p.expected_label_relation = "DIFFERENT_LABEL" if is_flip else "SAME_LABEL"
```
This forces `SHIFT_FROM_NEUTRAL` to be treated as `REVERSE_POLARITY`, corrupting the probe contract.

#### Implementation Plan:
1. In `blindspot/execution/runner.py`:
   - **DELETE** the forced overwrite in lines 235–239.
   - Replace with structured semantic contract propagation:
     ```python
     if p_annot:
         p.semantic_reference = p_annot.to_dict()
         p.reference_polarity = p_annot.final_semantic_polarity.value
         sem_rel = p_annot.semantic_relation_to_baseline
         p.semantic_relation = sem_rel.value if hasattr(sem_rel, "value") else str(sem_rel)
         
         # Ground-truth sentiment flip is ONLY true when polarities genuinely reverse:
         base_pol = probe_set.semantic_reference_set.baseline_annotation.final_semantic_polarity.value
         probe_pol = p_annot.final_semantic_polarity.value
         
         p.expected_flip = (base_pol in ("POSITIVE", "NEGATIVE") and 
                            probe_pol in ("POSITIVE", "NEGATIVE") and 
                            base_pol != probe_pol)
         p.semantic_intent = p.semantic_relation
         p.expected_label_relation = "DIFFERENT_LABEL" if p.expected_flip else ("STATE_CHANGE" if base_pol != probe_pol else "SAME_LABEL")
     ```

- **Files Affected**: `blindspot/execution/runner.py`
- **Data Contract Affected**: `LinguisticProbe` instances stored in `run_plan.json` and `results.json`.
- **UI Affected**: None (preserves correct underlying contract for visualization).
- **Research Interpretation**: Completely removes the bug that manufactured false expectation flips.
- **Backward Compatibility**: Fully backward compatible with legacy runs.
- **Tests Required**: End-to-end execution test ensuring runner does NOT mutate `SHIFT_FROM_NEUTRAL` into `REVERSE_POLARITY`.

---

### FIX 5: Capability-Aware Model Evaluation (2-Class vs. 3-Class) (SR-007)

#### Problem:
`blindspot/testing/behavioral.py` does not differentiate between 2-class models (which cannot represent `NEUTRAL`) and 3-class models (which can), causing false `BLIND` failure diagnoses on neutral baselines.

#### Implementation Plan:
1. In `blindspot/core/types.py` (`resolve_expected_behavioral_relation`):
   - Refactor to take `num_classes` into account:
     ```python
     def resolve_expected_behavioral_relation(
         expectation_type: ExpectationType,
         original_polarity: SemanticPolarity,
         num_classes: int = 2,
     ) -> BehavioralRelation:
         if original_polarity == SemanticPolarity.NEUTRAL:
             if num_classes == 2:
                 # 2-class models are forced to pick POSITIVE or NEGATIVE;
                 # A neutral baseline cannot mandate a deterministic flip.
                 return BehavioralRelation.UNCONSTRAINED
             elif num_classes == 3:
                 if expectation_type == ExpectationType.REVERSE_POLARITY:
                     return BehavioralRelation.SAME_POLARITY  # Neutral factual statement remains Neutral
                 elif expectation_type == ExpectationType.SHIFT_FROM_NEUTRAL:
                     return BehavioralRelation.NEUTRAL_TO_TARGET
         ...
     ```
2. In `blindspot/testing/behavioral.py` (`classify_behavior`):
   - Add capability guard:
     - If `orig_pol == SemanticPolarity.NEUTRAL` and model predicts `NEUTRAL → NEUTRAL` under factual negation:
       `outcome = BehavioralOutcome.EXPECTED_PRESERVE`, `failure = FailureCategory.NONE`, `rationale = "Model correctly maintained neutral classification across factual negation."`
     - If binary model predicts `NEGATIVE → NEGATIVE` on factual negation of adverse condition:
       `outcome = BehavioralOutcome.EXPECTED_PRESERVE`, `failure = FailureCategory.NONE`, `rationale = "Binary model retained adverse class across factual negation (no sentiment reversal required)."`

- **Files Affected**: `blindspot/core/types.py`, `blindspot/testing/behavioral.py`
- **Data Contract Affected**: `BehavioralRelation` enum (adds `UNCONSTRAINED`, `NEUTRAL_TO_TARGET`).
- **UI Affected**: Failure Lab and Models & Failures tab show accurate zero-failure counts for correct model behaviors.
- **Research Interpretation**: Eliminates spurious failure inflation in academic evaluations.
- **Backward Compatibility**: Preserves all existing valid test cases for true reversals.
- **Tests Required**: Tests with binary SST-2 and 3-class RoBERTa models across all 7 controlled test sentences.

---

### FIX 6: Multi-Factor Semantic Cache Invalidation (SR-008)

#### Problem:
`cache/semantic_cache.json` keys on `norm(text)|v1.0`. Improvements to analyzers or switching between manual and Gemini mode hit stale fallback entries.

#### Implementation Plan:
1. In `blindspot/semantic/cache.py`:
   - Upgrade cache schema version to `v2.0`.
   - Update `_compute_key()`:
     ```python
     def _compute_key(self, sentence_text: str, engine: str = "default", model: str = "default") -> str:
         norm = self._normalize(sentence_text)
         raw = f"{norm}|{engine}|{model}|v2.0"
         return hashlib.sha256(raw.encode("utf-8")).hexdigest()
     ```
   - Provide a migration/purge routine `clear_stale_fallbacks()` that strips all entries where `model_used == "manual_fallback"`.
2. Add a `Purge Stale Cache` button in Probe Lab settings to give researchers immediate control over cached annotations.

- **Files Affected**: `blindspot/semantic/cache.py`, `blindspot/ui/probe_lab.py`
- **Data Contract Affected**: Cache key format in `semantic_cache.json`.
- **UI Affected**: Stale entries with 75% confidence are immediately purged and replaced with exact analyzer results.
- **Research Interpretation**: Guarantees that active experiments reflect current algorithms, not stale runs.
- **Backward Compatibility**: Auto-detects legacy keys and flushes obsolete fallback records.
- **Tests Required**: Cache migration tests verifying distinct keys for Gemini vs. local analyzer.

---

## 3. CONTROLLED SENTENCE VALIDATION MATRIX (POST-FIX SPECIFICATION)

The table below defines the required ground-truth and expectation behavior for the 7 controlled test cases specified in Section 19:

| Case # | Original Sentence | Perturbed Sentence | Linguistic Operation | Baseline Ref | Probe Ref | Canonical Relation | Expected Flip (2-Class) | Expected Flip (3-Class) | Scientific Justification |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Case 1** | "The movie was excellent." | "The movie was terrible." | Antonym substitution | `POSITIVE` | `NEGATIVE` | `REVERSE_POLARITY` | **YES (`True`)** | **YES (`True`)** | True evaluative sentiment reversal. |
| **Case 2** | "The king is injured." | "The king is not injured." | Factual negation | `NEUTRAL` | `NEUTRAL` | `PRESERVE_POLARITY`| **NO (`False`)** | **NO (`False`)** | Factual negation of physical condition; sentiment stance remains neutral. |
| **Case 3** | "The movie was excellent." | "The movie was outstanding."| Synonym substitution | `POSITIVE` | `POSITIVE` | `PRESERVE_POLARITY`| **NO (`False`)** | **NO (`False`)** | Meaning preservation; test against spurious sensitivity. |
| **Case 4** | "The movie was good." | "The movie was extremely good." | Degree intensifier | `POSITIVE` | `POSITIVE` | `INTENSIFY` | **NO (`False`)** | **NO (`False`)** | Polarity class invariant; affective intensity increases. |
| **Case 5** | "The movie was excellent." | "The movie was somewhat good." | Degree downtoner | `POSITIVE` | `POSITIVE` | `DOWNTONE` | **NO (`False`)** | **NO / STATE CHANGE** | Attenuation; preserves positive class in binary, may approach neutral in 3-class. |
| **Case 6** | "The king is injured on his left leg." | "The king is not injured on his left leg." | Factual negation with PP | `NEUTRAL` | `NEUTRAL` | `PRESERVE_POLARITY`| **NO (`False`)** | **NO (`False`)** | News/medical factual proposition; truth condition inverts, sentiment does not. |
| **Case 7** | "The movie was good." | "The movie was good, but the ending was terrible." | Adversative contrast | `POSITIVE` | `NEGATIVE` | `SHIFT_CONTRAST` | **YES (`True`)** | **YES (`True`)** | Discourse concessive clause carries primary weight; dominant evaluation shifts to negative. |

---

## 4. REGRESSION TEST SPECIFICATION

Following approval of this plan, the test suite `tests/test_semantic_expectation_integrity.py` will be created with the following 12 mandatory test cases:

- [ ] **Test A**: `test_case_01_clear_sentiment_reversal()` ("excellent" $\to$ "terrible" yields `REVERSE_POLARITY`, `expected_flip=True`).
- [ ] **Test B**: `test_case_02_factual_negation()` ("king is injured" $\to$ "king is not injured" yields `PRESERVE_POLARITY`, `expected_flip=False`).
- [ ] **Test C**: `test_case_03_clear_preservation()` ("excellent" $\to$ "outstanding" yields `PRESERVE_POLARITY`, `expected_flip=False`).
- [ ] **Test D**: `test_case_04_intensification()` ("good" $\to$ "extremely good" yields `INTENSIFY`, `expected_flip=False`).
- [ ] **Test E**: `test_case_05_downtoning()` ("excellent" $\to$ "somewhat good" yields `DOWNTONE`, `expected_flip=False`).
- [ ] **Test F**: `test_case_06_neutral_factual_statement()` (Verifies truth-conditional change does not trigger sentiment flip).
- [ ] **Test G**: `test_case_07_binary_model_neutral_reference()` (Verifies SST-2 is not flagged as `BLIND` on neutral references).
- [ ] **Test H**: `test_case_08_three_class_model_neutral_reference()` (Verifies Twitter-RoBERTa predicting `NEU $\to$ NEU` is `EXPECTED_PRESERVE`).
- [ ] **Test I**: `test_case_09_gemini_offline_no_fabricated_confidence()` (Verifies `confidence` is `None` or marked uncalibrated when offline).
- [ ] **Test J**: `test_case_10_gemini_confidence_isolation()` (Verifies `gemini_confidence` is strictly `None` when offline).
- [ ] **Test K**: `test_case_11_human_override_authoritative()` (Verifies researcher override takes absolute precedence over automated engine).
- [ ] **Test L**: `test_case_12_cache_key_multidimensionality()` (Verifies cache separates Gemini annotations from local fallback annotations).

---

## 5. SUMMARY FOR USER REVIEW

| Step | Action | Status |
| :---: | :--- | :---: |
| **Stage 1** | Read-Only Audit of Codebase, Runs, and Caches | ✅ **COMPLETED** (`audit_reports/SEMANTIC_REFERENCE_DEBUG_AUDIT.md`) |
| **Stage 2** | Architectural Fix Plan Formulation | ✅ **COMPLETED** (`audit_reports/PROPOSED_FIX_PLAN.md`) |
| **Stage 3** | User Review and Alignment | ⏳ **AWAITING USER FEEDBACK** |
| **Stage 4** | Implementation of Fixes 1–6 | ⏸️ **BLOCKED UNTIL APPROVED** |
| **Stage 5** | Regression Test Execution & Live Verification | ⏸️ **BLOCKED UNTIL APPROVED** |

*No source code has been modified during this audit phase.*
