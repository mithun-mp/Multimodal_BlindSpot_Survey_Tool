# Probe-Level Behavioral Evidence: E2E Semantic Ground-Truth Benchmark

**Experiment ID**: `exp_1790507964_b60751`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_976d` | NEGATION_INSERTION | "The movie was absolutely ..." → "The movie was not absolut..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_3308` | DOUBLE_NEGATION | "The movie was absolutely ..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4e98` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8f2a` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_28b5` | SYNONYM_SUBSTITUTION | "The movie was absolutely ..." → "The film was absolutely f..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2f02` | CONTRAST_NEGATIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | POSITIVE (0.80) | POSITIVE → POSITIVE | -20.0 | NO | `MISSING_FLIP` | **Blind** |
| `prb_8a84` | CONTRAST_POSITIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_976d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_3308`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4e98`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_8f2a`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_28b5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2f02`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_8a84`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_976d` | NEGATION_INSERTION | "The movie was absolutely ..." → "The movie was not absolut..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_3308` | DOUBLE_NEGATION | "The movie was absolutely ..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4e98` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8f2a` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_28b5` | SYNONYM_SUBSTITUTION | "The movie was absolutely ..." → "The film was absolutely f..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2f02` | CONTRAST_NEGATIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | POSITIVE (0.92) | POSITIVE → POSITIVE | -7.6 | NO | `MISSING_FLIP` | **Blind** |
| `prb_8a84` | CONTRAST_POSITIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_976d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_3308`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4e98`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_8f2a`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_28b5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2f02`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_8a84`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_976d` | NEGATION_INSERTION | "The movie was absolutely ..." → "The movie was not absolut..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | NEGATIVE (0.83) | POSITIVE → NEGATIVE | -16.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_3308` | DOUBLE_NEGATION | "The movie was absolutely ..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4e98` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8f2a` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_28b5` | SYNONYM_SUBSTITUTION | "The movie was absolutely ..." → "The film was absolutely f..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2f02` | CONTRAST_NEGATIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -1.6 | NO | `MISSING_FLIP` | **Blind** |
| `prb_8a84` | CONTRAST_POSITIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_976d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_3308`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4e98`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_8f2a`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_28b5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2f02`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_8a84`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_976d` | NEGATION_INSERTION | "The movie was absolutely ..." → "The movie was not absolut..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_3308` | DOUBLE_NEGATION | "The movie was absolutely ..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4e98` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8f2a` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_28b5` | SYNONYM_SUBSTITUTION | "The movie was absolutely ..." → "The film was absolutely f..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2f02` | CONTRAST_NEGATIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | POSITIVE (0.69) | POSITIVE → POSITIVE | -30.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_8a84` | CONTRAST_POSITIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_976d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_3308`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4e98`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_8f2a`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_28b5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2f02`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_8a84`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_976d` | NEGATION_INSERTION | "The movie was absolutely ..." → "The movie was not absolut..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | NEGATIVE (0.66) | POSITIVE → NEGATIVE | -32.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_3308` | DOUBLE_NEGATION | "The movie was absolutely ..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4e98` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8f2a` | INTENSITY | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_28b5` | SYNONYM_SUBSTITUTION | "The movie was absolutely ..." → "The film was absolutely f..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2f02` | CONTRAST_NEGATIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | POSITIVE (0.93) | POSITIVE → POSITIVE | -5.6 | NO | `MISSING_FLIP` | **Blind** |
| `prb_8a84` | CONTRAST_POSITIVE_APPEND | "The movie was absolutely ..." → "The movie was absolutely ..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_976d`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_3308`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4e98`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_8f2a`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_28b5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2f02`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_8a84`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.