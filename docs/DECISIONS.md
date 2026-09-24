# Engineering & Research Decisions Log (BlindSpot)

## Decision 1: Shared Probe Protocol Over Independent Generation

### Context
In single-model testing, perturbations were generated on-the-fly per model invocation. In multi-model auditing, running separate perturbation passes would cause non-identical wording or random substitutions across models.

### Decision
Implement `SharedProbeGenerator` which generates an immutable `SharedProbeSet` with stable probe IDs (`probe_001`, `probe_002`...) once per input sentence. The identical probe set is evaluated across every selected model.

### Reason
Controlled comparative auditing requires that differences in observed model behavior stem solely from the models themselves, not from varying perturbation text.

### Alternatives Considered
- Generating perturbations independently inside each model wrapper: Rejected due to loss of controlled experimental comparison.

### Date
2026-09-19

---

## Decision 2: Explicit Expectation Models Over Binary Flip Assumptions

### Context
Earlier prototypes assumed `prediction changed = failure` or `negation = flip`. However, in natural language, double negation should preserve polarity, synonym substitution should preserve class, and neutral/ambiguous sentences have no single correct direction.

### Decision
Define `ExpectedSemanticEffect` (`REVERSE_POLARITY`, `PRESERVE_POLARITY`, `CONTRAST_SHIFT`, `INVARIANT`, `UNCERTAIN`).

### Reason
Prevents false-positive failure diagnoses and scientifically aligns evaluation with linguistic semantics.

### Alternatives Considered
- Treating all label changes as failures: Scientifically unsound.

### Date
2026-09-19

---

## Decision 3: Explainability Provenance Tracking

### Context
Third-party explainer libraries (such as SHAP or LIME) may experience runtime failures or missing dependencies, triggering fallback mechanisms such as Leave-One-Out (LOO) importance.

### Decision
Every `ExplanationResult` explicitly records `explainer_requested`, `explainer_used`, `fallback_used`, `fallback_reason`, `random_seed`, and `runtime_ms`. Never silently present LOO output as genuine SHAP.

### Reason
Academic and research integrity requires clear provenance and reproducibility.

### Date
2026-09-19

---

## Decision 4: Descriptive Analysis Over Subjective Model Rankings

### Context
Multi-model dashboards often rank models as "Best Model", "Winner", or "Rank 1".

### Decision
Cross-model analytics are strictly descriptive: Model × Probe Matrix, Consensus Agreement %, and Model Behavioral Fingerprints (negation sensitivity, contrast response, calibration, failure distribution).

### Reason
Classifier suitability depends on deployment context (e.g. strict negation compliance vs. tolerance for ambiguity). Subjective ranking is scientifically inappropriate.

### Date
2026-09-19

---

## Decision 5: Non-Blocking Background Execution Architecture

### Context
Streamlit re-runs scripts on widget interaction. Running expensive multi-model inference and SHAP computations directly in the UI render loop freezes the interface.

### Decision
Implement `ExperimentRunner` executing in a dedicated background worker thread, emitting structured `ExecutionEvent` objects to an `EventEmitter`. The UI observes and streams events using periodic rerun checks.

### Reason
Maintains UI responsiveness and enables real-time progress bars, live log streaming, and graceful cancellation.

### Date
2026-09-19

---

## Decision 6: Multiclass Expectation-Aligned Calibration (ECE)

### Context
In multiclass models, when a probe specifies an expected flip, mapping the expected class index to `orig_idx` or `1 - orig_idx` fails because there are more than 2 classes. If the model flips correctly, evaluating `predictions == orig_idx` falsely penalizes the model.

### Decision
Align expected indices in calibration directly with `expectation_satisfied`. If the model satisfied the behavioral test expectation, `exp_idx = pred_idx` (scoring accuracy as 1.0); if the model violated expectation, `exp_idx = (pred_idx + 1) % num_classes` (scoring accuracy as 0.0).

### Reason
Eliminates all hardcoded binary assumptions and yields mathematically sound multiclass calibration metrics.

### Date
2026-09-19

---

## Decision 7: Cross-Platform Safe Progress Meter Representations

### Context
Using UTF-8 block glyphs (`█`, `▏`) causes `UnicodeEncodeError` in Windows console and logging environments where default codepages are `cp1252` or `cp437`.

### Decision
Format terminal and text distribution meters using ASCII bracket representations `[====================]` while retaining rich graphical Streamlit progress bars in the browser interface.

### Reason
Ensures 100% crash-proof cross-platform execution across Windows PowerShell, CMD, Linux shells, and headless CI environments.

### Date
2026-09-19
