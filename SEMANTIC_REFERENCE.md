# BlindSpot Semantic Ground-Truth Reference Architecture

## 1. Executive Summary & Core Objective

BlindSpot evaluates multiple sentiment classification models against controlled linguistic probes. A central challenge in comparative NLP evaluation is comparing heterogeneous model architectures:
- **Binary Sentiment Models** output: `NEGATIVE`, `POSITIVE`
- **Three-Class Sentiment Models** output: `NEGATIVE`, `NEUTRAL`, `POSITIVE`

A binary classifier can **never** explicitly output `NEUTRAL`. When a sentence possesses an inherently neutral semantic meaning (e.g., *"The movie was released on Friday."*), a binary classifier is mathematically forced to assign probability strictly across its two available polarity classes. If the binary model assigns 52% to `POSITIVE` and 48% to `NEGATIVE`, this output is a **forced-polarity classification**, not an indicator that the underlying semantic meaning was positive.

Treating 2-class `POSITIVE` as directly equivalent to 3-class `POSITIVE` without anchoring to an independent semantic reference undermines experimental validity.

The BlindSpot **Semantic Ground-Truth Reference Layer** solves this problem by decoupling **empirical model predictions** from **canonical semantic ground truth**.

---

## 2. Canonical Semantic Label Space

BlindSpot enforces **one and only one** canonical semantic polarity label space:

```text
POSITIVE
NEGATIVE
NEUTRAL
```

### Invariants:
1. **No Ad-Hoc Categories**: Labels such as `MIXED`, `UNCERTAIN`, `VERY_POSITIVE`, `VERY_NEGATIVE`, `SARCASTIC`, `IRONIC`, `SUBJECTIVE`, or `AMBIGUOUS` are strictly rejected.
2. **Explicit Confidence**: Uncertainty is captured via a separate numerical confidence field (`confidence ∈ [0.0, 1.0]`), never by inventing non-canonical labels.
3. **Local Validation**: Any external model or API returning a non-canonical label is rejected, rather than silently coerced.

---

## 3. The Role of Google Gemini

Google Gemini is **not** a benchmark model and is **never** evaluated as part of the five benchmark classifiers. Gemini operates strictly as an external **semantic reference annotator and verification layer**.

### Permitted Gemini Functions:
1. Determine the canonical semantic polarity (`POSITIVE`, `NEGATIVE`, or `NEUTRAL`) of the baseline sentence.
2. Determine the canonical semantic polarity of each linguistic probe sentence.
3. Determine the expected semantic relationship between baseline and probe (`PRESERVE`, `REVERSE`, `SHIFT_TO_NEUTRAL`, `SHIFT_FROM_NEUTRAL`, `OTHER`).
4. Provide a linguistic rationale and confidence score for the annotation.

### Strictly Prohibited Functions:
- Gemini is **never** allowed to predict failure categories (`BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`).
- Gemini must **never** forecast whether a model will succeed or fail on a probe.
- Gemini must **never** rank, rate, or judge benchmark models.
- Gemini must **never** generate linguistic probes (probes are generated deterministically by `SharedProbeGenerator`).

All behavioral diagnoses and failure classifications remain 100% rule-based, derived from actual model forward passes and token attributions.

---

## 4. Human Verification & Override Layer

In the BlindSpot research methodology, automated AI annotations are hypotheses subject to researcher verification.

### Workflow:
1. Baseline sentence is annotated by Gemini (or heuristic fallback if offline).
2. The UI presents the baseline annotation along with confidence and rationale.
3. The researcher can accept (`[✓ Accept]`) or override (`[Change to POSITIVE]`, `[Change to NEGATIVE]`, `[Change to NEUTRAL]`).
4. Every probe is presented with baseline polarity, probe polarity, expected relation, and confidence.
5. If the researcher changes a label:
   ```json
   {
     "gemini_polarity": "NEUTRAL",
     "gemini_confidence": 0.91,
     "human_verified_polarity": "POSITIVE",
     "final_semantic_polarity": "POSITIVE",
     "verification_source": "HUMAN_OVERRIDE"
   }
   ```
6. When verified, the entire `SemanticReferenceSet` is **frozen** (`ref_set.freeze()`). Once frozen, it becomes immutable and is evaluated identically across all benchmark models.

---

## 5. Binary vs. Three-Class Model Alignment

BlindSpot maintains a strict ontological separation between:
1. **Semantic Reference Space**: `{POSITIVE, NEGATIVE, NEUTRAL}`
2. **Model Output Space**: 
   - Binary: `{NEGATIVE, POSITIVE}`
   - Multiclass: `{NEGATIVE, NEUTRAL, POSITIVE}`

Every `PredictionResult` and `ModelProbeEvaluation` explicitly records:
- `model_label_space`: The native output space of the model.
- `predicted_label`: The native class selected by the model.
- `model_confidence`: The native softmax confidence.
- `semantic_compatibility`: The compatibility relationship between native prediction and semantic ground truth.

### Compatibility Rules:
| Semantic Ground Truth | Multiclass Model Output | Compatibility Status | Interpretation |
| :--- | :--- | :--- | :--- |
| `POSITIVE` | `POSITIVE` | `DIRECTLY_COMPATIBLE` | Direct match |
| `NEGATIVE` | `NEGATIVE` | `DIRECTLY_COMPATIBLE` | Direct match |
| `NEUTRAL` | `NEUTRAL` | `DIRECTLY_COMPATIBLE` | Direct match |
| `NEUTRAL` | `POSITIVE` / `NEGATIVE` | `NOT_DIRECTLY_REPRESENTABLE` | Binary model forced choice; reference remains `NEUTRAL` |
| `POSITIVE` | `NEGATIVE` / `NEUTRAL` | `POLARITY_MISMATCH` | Model prediction diverges from semantic reference |

---

## 6. Semantic Expectation vs. Model Flips

A model flip is derived purely from observed model outputs:
- **Binary Model Flips**: `POSITIVE → NEGATIVE` or `NEGATIVE → POSITIVE`.
- **Three-Class Model Transitions**: All 9 state transitions (`POS→NEG`, `POS→NEU`, `NEU→NEG`, etc.) are preserved explicitly.

Expected semantic reversals (`REVERSE`) and observed model flips are distinct concepts:
- **Baseline Semantic: POSITIVE**, **Probe Semantic: NEGATIVE** $\rightarrow$ Expected Relation: `REVERSE`
  - Model predicts: `POSITIVE → NEGATIVE` $\rightarrow$ **COMPLIANT** (Observed Expected Reversal)
  - Model predicts: `POSITIVE → POSITIVE` $\rightarrow$ **UNEXPECTED_STABILITY** (Candidate Blind failure)
- **Baseline Semantic: POSITIVE**, **Probe Semantic: POSITIVE** $\rightarrow$ Expected Relation: `PRESERVE`
  - Model predicts: `POSITIVE → POSITIVE` $\rightarrow$ **COMPLIANT** (Observed Preserve)
  - Model predicts: `POSITIVE → NEGATIVE` $\rightarrow$ **UNEXPECTED_FLIP** (Candidate Spurious failure)

---

## 7. Caching, Batching & Offline Resilience

### Persistent Annotation Cache
To ensure fast execution, API quota preservation, and reproducibility, all semantic annotations are stored in a persistent cache (`cache/semantic_cache.json`).
- Cache Key: `SHA-256(normalize(sentence_text) + "|" + prompt_version)`
- Avoids duplicate API calls across runs and iterations.

### Batch Annotation
Baseline and probe sentences are submitted in structured batches (`annotate_batch`), validating each item individually.

### Offline / Manual Fallback
If `GEMINI_API_KEY` is not configured:
- The system gracefully transitions to `MANUAL MODE` (Status: `Offline (Manual Mode)`).
- Heuristic semantic inferences provide default suggestions.
- The researcher can manually verify and adjust references.
- BlindSpot continues functioning without crashes or simulated data.

---

## 8. Reproducibility & Provenance

Every experiment saves its frozen semantic reference to:
```text
runs/<experiment_id>/semantic_reference.json
```
This document records:
- `annotation_engine`: `"gemini"` or `"manual"`
- `model`: Exact model ID used (e.g., `gemini-2.5-flash`)
- `prompt_version`: Schema version
- `frozen`: `true`
- `cache_hits`: Number of cache hits
- `api_requests`: Number of live API calls
- `baseline`: Full baseline annotation with verification source
- `probes`: Map of probe annotations and expected relations
- `semantic_label_space`: `["POSITIVE", "NEGATIVE", "NEUTRAL"]`

---

## 9. Benchmark Invariant

```text
ONE SENTENCE
      ↓
ONE CANONICAL SEMANTIC REFERENCE (FROZEN)
      ↓
ONE CANONICAL PROBE SET
      ↓
FIVE HETEROGENEOUS BENCHMARK MODEL EVALUATIONS
```

All 5 benchmark models receive identical stimuli and evaluate against the exact same frozen semantic reference set.
