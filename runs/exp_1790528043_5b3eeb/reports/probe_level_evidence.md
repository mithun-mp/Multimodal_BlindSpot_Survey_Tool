# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790528043_5b3eeb`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6018` | NEGATION_INSERTION | "the movie was great and t..." → "the movie was not great a..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | POSITIVE (0.66) | POSITIVE → POSITIVE | -34.2 | NO | `MISSING_FLIP` | **Blind** |
| `prb_01d9` | DOUBLE_NEGATION | "the movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4c26` | INTENSITY | "the movie was great and t..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f9c4` | INTENSITY | "the movie was great and t..." → "the movie was somewhat gr..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_06eb` | SYNONYM_SUBSTITUTION | "the movie was great and t..." → "the film was great and th..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eea0` | CONTRAST_NEGATIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_2464` | CONTRAST_POSITIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6018`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_01d9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4c26`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_f9c4`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_06eb`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eea0`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_2464`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6018` | NEGATION_INSERTION | "the movie was great and t..." → "the movie was not great a..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_01d9` | DOUBLE_NEGATION | "the movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.93) | POSITIVE → POSITIVE | -6.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4c26` | INTENSITY | "the movie was great and t..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f9c4` | INTENSITY | "the movie was great and t..." → "the movie was somewhat gr..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_06eb` | SYNONYM_SUBSTITUTION | "the movie was great and t..." → "the film was great and th..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eea0` | CONTRAST_NEGATIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | -1.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_2464` | CONTRAST_POSITIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6018`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_01d9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4c26`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_f9c4`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_06eb`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eea0`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_2464`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6018` | NEGATION_INSERTION | "the movie was great and t..." → "the movie was not great a..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (0.76) | POSITIVE → NEGATIVE | -24.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_01d9` | DOUBLE_NEGATION | "the movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4c26` | INTENSITY | "the movie was great and t..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f9c4` | INTENSITY | "the movie was great and t..." → "the movie was somewhat gr..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_06eb` | SYNONYM_SUBSTITUTION | "the movie was great and t..." → "the film was great and th..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eea0` | CONTRAST_NEGATIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (0.87) | POSITIVE → NEGATIVE | -12.8 | YES | `EXPECTED_FLIP` | **None** |
| `prb_2464` | CONTRAST_POSITIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6018`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_01d9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4c26`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_f9c4`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_06eb`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eea0`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_2464`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6018` | NEGATION_INSERTION | "the movie was great and t..." → "the movie was not great a..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | NEGATIVE (0.80) | POSITIVE → NEGATIVE | -18.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_01d9` | DOUBLE_NEGATION | "the movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -1.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4c26` | INTENSITY | "the movie was great and t..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f9c4` | INTENSITY | "the movie was great and t..." → "the movie was somewhat gr..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_06eb` | SYNONYM_SUBSTITUTION | "the movie was great and t..." → "the film was great and th..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eea0` | CONTRAST_NEGATIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | POSITIVE (0.57) | POSITIVE → POSITIVE | -41.9 | NO | `MISSING_FLIP` | **Blind** |
| `prb_2464` | CONTRAST_POSITIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6018`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_01d9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4c26`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_f9c4`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_06eb`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eea0`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_2464`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_6018` | NEGATION_INSERTION | "the movie was great and t..." → "the movie was not great a..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | NEGATIVE (0.92) | POSITIVE → NEGATIVE | -6.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_01d9` | DOUBLE_NEGATION | "the movie was great and t..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -2.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4c26` | INTENSITY | "the movie was great and t..." → "the movie was extremely g..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f9c4` | INTENSITY | "the movie was great and t..." → "the movie was somewhat gr..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_06eb` | SYNONYM_SUBSTITUTION | "the movie was great and t..." → "the film was great and th..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_eea0` | CONTRAST_NEGATIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `NEGATIVE (REVERSE)` | POSITIVE (0.99) | POSITIVE (0.42) | POSITIVE → POSITIVE | -56.4 | NO | `MISSING_FLIP` | **Blind** |
| `prb_2464` | CONTRAST_POSITIVE_APPEND | "the movie was great and t..." → "the movie was great and t..." | `POSITIVE (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_6018`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_01d9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_4c26`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_f9c4`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_06eb`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_eea0`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_2464`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.