# BlindSpot Test Status Report

**Document**: `TEST_STATUS.md`  
**Date**: September 22, 2026  
**Status**: ALL TESTS PASSING (118/118)  
**Execution Time**: 48.861 seconds  
**Test Suite**: `python run_tests.py`  

---

## 1. Summary of Test Results

| Test Module | Tests | Passing | Failing | Errors | Status |
|---|---|---|---|---|---|
| `tests.test_canonical_pipeline` | 20 | 20 | 0 | 0 | ✅ PASS |
| `tests.test_probe_integrity` | 20 | 20 | 0 | 0 | ✅ PASS |
| `tests.test_behavioral_taxonomy` | 14 | 14 | 0 | 0 | ✅ PASS |
| `tests.test_flip_analysis` | 8 | 8 | 0 | 0 | ✅ PASS |
| `tests.test_probe_calibration` | 4 | 4 | 0 | 0 | ✅ PASS |
| `tests.test_deterministic_acceptance` | 4 | 4 | 0 | 0 | ✅ PASS |
| `tests.test_multiclass` | 5 | 5 | 0 | 0 | ✅ PASS |
| `tests.test_research_repair` | 15 | 15 | 0 | 0 | ✅ PASS |
| `tests.test_model_registry` | 7 | 7 | 0 | 0 | ✅ PASS |
| `tests.test_persistence_and_lifecycle` | 6 | 6 | 0 | 0 | ✅ PASS |
| `tests.test_shared_probes` | 6 | 6 | 0 | 0 | ✅ PASS |
| `tests.test_cross_model` | 3 | 3 | 0 | 0 | ✅ PASS |
| `tests.test_resource_manager` | 2 | 2 | 0 | 0 | ✅ PASS |
| `tests.test_caching_and_batching` | 4 | 4 | 0 | 0 | ✅ PASS |
| **TOTAL** | **118** | **118** | **0** | **0** | **100% PASS** |

---

## 2. 20 Canonical Pipeline Specifications Verified

1. `test_01_generated_probe_count`: Exactly 7 diagnostic candidates generated per seed.
2. `test_02_selected_probe_count`: Exact probe subsets selected and preserved without mutation.
3. `test_03_executed_probe_count`: Execution count matches selection count exactly across models.
4. `test_04_selected_equals_executed_enforced`: Runner validation halts with exception on any count discrepancy.
5. `test_05_baseline_exists_for_every_model`: Baseline prediction recorded once per model prior to perturbations.
6. `test_06_binary_prediction_normalization`: SST-2 binary probabilities sum to 1.0; formatted percentage available.
7. `test_07_multiclass_prediction_normalization`: 3-class models normalized to NEGATIVE / NEUTRAL / POSITIVE.
8. `test_08_flip_detection_accuracy`: Binary and multiclass label transitions accurately detected.
9. `test_09_confidence_delta_calculation`: Signed confidence delta $\Delta c = c_{\text{pert}} - c_{\text{orig}}$ in percentage points.
10. `test_10_expected_vs_observed_behavior`: Verification of `EXPECTED_FLIP`, `EXPECTED_PRESERVE`, `UNEXPECTED_FLIP`, `MISSING_FLIP`.
11. `test_11_failure_taxonomy_classification`: Deterministic rule-based categorization into `Blind`, `Spurious`, `Misweighted`, `Undetermined`.
12. `test_12_incremental_persistence_per_model`: Granular artifact writing (`status.json`, `predictions.json`, `metrics.json`) as models finish.
13. `test_13_runner_resume_skips_completed_models`: Interrupted runs resume cleanly and skip completed model evaluations.
14. `test_14_safe_deletion_cleans_artifacts`: Safe deletion requires `confirmation=True` and removes only target run tree.
15. `test_15_five_model_cache_capacity`: LRU cache handles 5 models resident in memory simultaneously.
16. `test_16_completed_model_incremental_ui_state`: UI state reveals completed models progressively.
17. `test_17_thesis_graph_generation`: Generates all 15 publication figures and `source_data.json`.
18. `test_18_no_ai_failure_prediction_layer`: Verifies pure rule-based classifier without external ML inference.
19. `test_19_non_sentiment_model_rejection`: Sentiment validation gate strictly rejects detector models.
20. `test_20_custom_probe_lifecycle_execution`: Custom user-defined probes follow full canonical lifecycle and execute cleanly.

---

## 3. End-to-End Live Benchmark Verification

- **Script**: `scratch/run_5_model_acceptance_benchmark.py`
- **Models**: 5 genuine sentiment architectures (DistilBERT, ALBERT, Twitter RoBERTa Latest, BERT Base, Twitter RoBERTa Base)
- **Seed**: *"All that glitters is not gold."*
- **Probes**: 5 selected probes (Negation removal, Double negation, Intensifier, Downtoner, Proverb paraphrase)
- **Duration**: 50.69 seconds
- **Figures Generated**: 19 publication figures + `source_data.json`
- **Resume Validation**: Succeeded with status `COMPLETED` and 0 duplicate inferences.
