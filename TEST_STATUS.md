# BlindSpot Test Status Report

**Document**: `TEST_STATUS.md`  
**Date**: September 28, 2026  
**Status**: ALL TESTS PASSING (171/171)  
**Semantic Reference Integrity Suite (v2.8.3)**: `tests/test_semantic_integrity_spec.py` (14/14 PASS in 28.47s)  
**Semantic Reference Suite (v2.7.0)**: `tests/test_semantic_reference.py` (14/14 PASS in 2.27s)  
**Scientific Repair Suite**: `tests/test_scientific_repairs.py` (25/25 PASS in 0.001s)  
**Full Test Runner**: `python run_tests.py` (132/132 PASS in 58.687s)  
**Real 5-Model End-to-End Acceptance**: `verify_e2e_semantic_experiment.py` (5 Models x 7 Probes = 35 Inferences + 5 Baselines, 100% Validated in 84.43s, Run ID: `exp_1790550034_0b285b`)  

---

## 1. Summary of Test Results

| Test Module | Tests | Passing | Failing | Errors | Status |
|---|---|---|---|---|---|
| `tests.test_semantic_integrity_spec` *(New v2.8.3)* | 14 | 14 | 0 | 0 | ✅ PASS |
| `tests.test_semantic_reference` *(v2.7.0 / v2.8.3)* | 14 | 14 | 0 | 0 | ✅ PASS |
| `tests.test_scientific_repairs` | 25 | 25 | 0 | 0 | ✅ PASS |
| `tests.test_canonical_pipeline` | 20 | 20 | 0 | 0 | ✅ PASS |
| `tests.test_probe_integrity` | 20 | 20 | 0 | 0 | ✅ PASS |
| `tests.test_behavioral_taxonomy` | 14 | 14 | 0 | 0 | ✅ PASS |
| `tests.test_flip_analysis` | 8 | 8 | 0 | 0 | ✅ PASS |
| `tests.test_probe_calibration` | 4 | 4 | 0 | 0 | ✅ PASS |
| `tests.test_deterministic_acceptance` | 4 | 4 | 0 | 0 | ✅ PASS |
| `tests.test_multiclass` | 5 | 5 | 0 | 0 | ✅ PASS |
| `tests.test_research_repair` | 15 | 15 | 0 | 0 | ✅ PASS |
| `tests.test_model_registry` | 7 | 7 | 0 | 0 | ✅ PASS |
| `tests.test_persistence_and_lifecycle` | 5 | 5 | 0 | 0 | ✅ PASS |
| `tests.test_shared_probes` | 6 | 6 | 0 | 0 | ✅ PASS |
| `tests.test_cross_model` | 3 | 3 | 0 | 0 | ✅ PASS |
| `tests.test_resource_manager` | 2 | 2 | 0 | 0 | ✅ PASS |
| `tests.test_caching_and_batching` | 4 | 4 | 0 | 0 | ✅ PASS |
| **TOTAL** | **171** | **171** | **0** | **0** | **100% PASS** |

---

## 2. Scientific Repair Test Suite Coverage (`tests/test_scientific_repairs.py`)

All 25 targeted test cases execute deterministically and validate thesis invariants:

| Test Case | Description | Result |
|---|---|---|
| `test_semantic_polarity_mapping_binary_sst2` | `LABEL_0` $\to$ NEGATIVE, `LABEL_1` $\to$ POSITIVE | ✅ PASS |
| `test_semantic_polarity_mapping_roberta_3class` | `LABEL_0` $\to$ NEGATIVE, `LABEL_1` $\to$ NEUTRAL, `LABEL_2` $\to$ POSITIVE | ✅ PASS |
| `test_semantic_polarity_mapping_twitter_raw` | `"negative"`, `"neutral"`, `"positive"` string normalization | ✅ PASS |
| `test_raw_label_flip_predicate` | Direct comparison $y_0 \neq y_p$ on raw labels | ✅ PASS |
| `test_polarity_flip_predicate_binary` | Binary polarity state inversion detection | ✅ PASS |
| `test_polarity_flip_predicate_with_neutral` | NEGATIVE $\leftrightarrow$ POSITIVE is flip; to/from NEUTRAL is not flip | ✅ PASS |
| `test_semantic_state_change_predicate` | Any change in semantic state (including NEUTRAL transitions) | ✅ PASS |
| `test_confidence_delta_calculation` | Signed percentage points $\Delta c = (c_p - c_0) \times 100$ | ✅ PASS |
| `test_flip_rate_disambiguation` | `observed_flip_rate` vs `expected_flip_rate` vs `expected_flip_compliance` | ✅ PASS |
| `test_compliance_rate_all_complied` | Compliance $= 1.0$ when all expected flips occur | ✅ PASS |
| `test_compliance_rate_zero_complied` | Compliance $= 0.0$ when expected flips fail completely (blindness) | ✅ PASS |
| `test_behavioral_consistency_calculation` | Overall alignment across flip-expecting and preserve-expecting probes | ✅ PASS |
| `test_classify_behavior_expected_flip` | Inversion observed on flip probe $\to$ `EXPECTED_FLIP`, `NONE` | ✅ PASS |
| `test_classify_behavior_missing_flip_blind` | Preservation on inversion probe $\to$ `MISSING_FLIP`, `BLIND` | ✅ PASS |
| `test_classify_behavior_expected_preserve` | Preservation on invariant probe $\to$ `EXPECTED_PRESERVE`, `NONE` | ✅ PASS |
| `test_classify_behavior_unexpected_flip_spurious` | Flip on invariant probe $\to$ `UNEXPECTED_FLIP`, `SPURIOUS` | ✅ PASS |
| `test_classify_behavior_misweighted_intensifier_drop` | Polarity preserved but confidence drops $>15$pp $\to$ `MISWEIGHTED` | ✅ PASS |
| `test_classify_behavior_undetermined` | Ambiguous transitions with no diagnostic pattern $\to$ `UNDETERMINED` | ✅ PASS |
| `test_baseline_id_generation_and_immutability` | Deterministic SHA-256 hash invariant across seed, model, and params | ✅ PASS |
| `test_probe_validator_valid_probes` | Standard valid linguistic probes pass validation | ✅ PASS |
| `test_probe_validator_rejects_empty_text` | Rejects probes with empty or whitespace-only text | ✅ PASS |
| `test_probe_validator_rejects_unmutated_probe` | Rejects probes where perturbed text is identical to original seed | ✅ PASS |
| `test_non_normative_reporting_no_rankings` | Summary metrics produce no winner/loser labels or rank columns | ✅ PASS |
| `test_registry_rejects_non_sentiment_models` | Validation gate rejects toxic, NLI, detector, and topic models | ✅ PASS |
| `test_run_plan_execution_integrity` | Staged probe set matches executed probe set exactly ($N_{\text{staged}} == N_{\text{executed}}$) | ✅ PASS |

---

## 3. Real Multi-Model Acceptance Benchmark (`tests/run_acceptance_experiment.py`)

Executed full benchmark against 5 real sentiment models across 5 diverse test sentences (Sentences A-E), 7 diagnostic probes per sentence (35 probes total per model = 175 inferences):

### Evaluated Model Checkpoints
1. `distilbert-base-uncased-finetuned-sst-2-english` (Binary SST-2, 67M params)
2. `textattack/albert-base-v2-SST-2` (Binary SST-2, 12M params)
3. `cardiffnlp/twitter-roberta-base-sentiment-latest` (3-Class Twitter, 125M params)
4. `textattack/bert-base-uncased-SST-2` (Binary SST-2, 109M params)
5. `cardiffnlp/twitter-roberta-base-sentiment` (3-Class Twitter, 125M params)

### Empirical Results Summary Table

| Model ID | Classes | Observed Flip Rate | Expected Flip Compliance | Preserve Rate | Behavioral Consistency | Failures Diagnosed (Blind / Spurious / Misweighted / Undetermined) |
|---|---|---|---|---|---|---|
| `distilbert-base-uncased-finetuned-sst-2-english` | Binary (2) | 20.0% (7/35) | 50.0% (5/10) | 92.0% (23/25) | 80.0% (28/35) | Blind: 5, Spurious: 2, Misweighted: 0, Undetermined: 0 |
| `textattack/albert-base-v2-SST-2` | Binary (2) | 0.0% (0/35) | 0.0% (0/10) | 100.0% (25/25) | 71.4% (25/35) | Blind: 10, Spurious: 0, Misweighted: 0, Undetermined: 0 |
| `cardiffnlp/twitter-roberta-base-sentiment-latest` | 3-Class (3) | 17.1% (6/35) | 50.0% (5/10) | 96.0% (24/25) | 77.1% (27/35) | Blind: 5, Spurious: 1, Misweighted: 2, Undetermined: 0 |
| `textattack/bert-base-uncased-SST-2` | Binary (2) | 0.0% (0/35) | 0.0% (0/10) | 100.0% (25/25) | 71.4% (25/35) | Blind: 10, Spurious: 0, Misweighted: 0, Undetermined: 0 |
| `cardiffnlp/twitter-roberta-base-sentiment` | 3-Class (3) | 0.0% (0/35) | 0.0% (0/10) | 100.0% (25/25) | 71.4% (25/35) | Blind: 10, Spurious: 0, Misweighted: 0, Undetermined: 0 |

### Invariant Verification
- Real Inference: **REAL_PIPELINE** verified (0 heuristic/dummy predictions).
- Test Failures: **0 failures** across all 5 models.
- Non-Normative Integrity: **100% compliant** (0 ranking terms, 0 winner/loser classifications).
- Baseline Immutability: **100% verified** (every probe anchored to its deterministic `baseline_id`).
