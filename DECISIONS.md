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
