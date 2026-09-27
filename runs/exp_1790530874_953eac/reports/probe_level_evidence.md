# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790530874_953eac`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_408f` | NEGATION_INSERTION | "the movie was good and th..." → "the movie was not good an..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (0.86) | POSITIVE → NEGATIVE | -13.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_61b8` | DOUBLE_NEGATION | "the movie was good and th..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_654c` | INTENSITY | "the movie was good and th..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_abc5` | INTENSITY | "the movie was good and th..." → "the movie was somewhat go..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5c75` | SYNONYM_SUBSTITUTION | "the movie was good and th..." → "the film was good and the..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_de92` | CONTRAST_NEGATIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_a597` | CONTRAST_POSITIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_408f`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_61b8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_654c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_abc5`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_5c75`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_de92`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_a597`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_408f` | NEGATION_INSERTION | "the movie was good and th..." → "the movie was not good an..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | +0.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_61b8` | DOUBLE_NEGATION | "the movie was good and th..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.88) | POSITIVE → POSITIVE | -11.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_654c` | INTENSITY | "the movie was good and th..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_abc5` | INTENSITY | "the movie was good and th..." → "the movie was somewhat go..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5c75` | SYNONYM_SUBSTITUTION | "the movie was good and th..." → "the film was good and the..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_de92` | CONTRAST_NEGATIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | NEGATIVE (0.94) | POSITIVE → NEGATIVE | -5.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_a597` | CONTRAST_POSITIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.4 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_408f`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_61b8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_654c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_abc5`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_5c75`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_de92`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_a597`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_408f` | NEGATION_INSERTION | "the movie was good and th..." → "the movie was not good an..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (0.77) | POSITIVE → NEGATIVE | -23.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_61b8` | DOUBLE_NEGATION | "the movie was good and th..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_654c` | INTENSITY | "the movie was good and th..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_abc5` | INTENSITY | "the movie was good and th..." → "the movie was somewhat go..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5c75` | SYNONYM_SUBSTITUTION | "the movie was good and th..." → "the film was good and the..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_de92` | CONTRAST_NEGATIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (0.83) | POSITIVE → NEGATIVE | -17.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_a597` | CONTRAST_POSITIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_408f`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_61b8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_654c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_abc5`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_5c75`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_de92`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_a597`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_408f` | NEGATION_INSERTION | "the movie was good and th..." → "the movie was not good an..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | NEGATIVE (0.86) | POSITIVE → NEGATIVE | -12.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_61b8` | DOUBLE_NEGATION | "the movie was good and th..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.95) | POSITIVE → POSITIVE | -3.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_654c` | INTENSITY | "the movie was good and th..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_abc5` | INTENSITY | "the movie was good and th..." → "the movie was somewhat go..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5c75` | SYNONYM_SUBSTITUTION | "the movie was good and th..." → "the film was good and the..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_de92` | CONTRAST_NEGATIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | POSITIVE (0.41) | POSITIVE → POSITIVE | -57.9 | NO | `MISSING_FLIP` | **Blind** |
| `prb_a597` | CONTRAST_POSITIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_408f`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_61b8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_654c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_abc5`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_5c75`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_de92`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_a597`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_408f` | NEGATION_INSERTION | "the movie was good and th..." → "the movie was not good an..." | `NEGATIVE (REVERSE)` | POSITIVE (0.98) | NEGATIVE (0.96) | POSITIVE → NEGATIVE | -2.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_61b8` | DOUBLE_NEGATION | "the movie was good and th..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (0.95) | POSITIVE → POSITIVE | -3.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_654c` | INTENSITY | "the movie was good and th..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_abc5` | INTENSITY | "the movie was good and th..." → "the movie was somewhat go..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5c75` | SYNONYM_SUBSTITUTION | "the movie was good and th..." → "the film was good and the..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_de92` | CONTRAST_NEGATIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `NEGATIVE (REVERSE)` | POSITIVE (0.98) | NEUTRAL (0.36) | POSITIVE → NEUTRAL | -62.7 | NO | `EXPECTED_FLIP` | **None** |
| `prb_a597` | CONTRAST_POSITIVE_APPEND | "the movie was good and th..." → "the movie was good and th..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (0.98) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_408f`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_61b8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_654c`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_abc5`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_5c75`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_de92`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEUTRAL (NEUTRAL)) under DIFFERENT_LABEL expectation.
- **`prb_a597`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.