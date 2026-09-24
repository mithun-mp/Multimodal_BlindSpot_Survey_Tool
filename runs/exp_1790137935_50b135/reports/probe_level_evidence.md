# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790137935_50b135`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_8ecd` | NEGATION_INSERTION | "The film was amazing,me a..." → "The film was not amazing,..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_e233` | DOUBLE_NEGATION | "The film was amazing,me a..." → "It is not impossible that..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_696d` | INTENSITY | "The film was amazing,me a..." → "The film extremely was am..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e397` | INTENSITY | "The film was amazing,me a..." → "The film somewhat was ama..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3f29` | SYNONYM_SUBSTITUTION | "The film was amazing,me a..." → "The cinema was amazing,me..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_aa44` | CONTRAST_NEGATIVE_APPEND | "The film was amazing,me a..." → "The film was amazing,me a..." | POSITIVE (1.00) | NEGATIVE (0.95) | POSITIVE → NEGATIVE | -5.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_f5c7` | CONTRAST_POSITIVE_APPEND | "The film was amazing,me a..." → "The film was amazing,me a..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_8ecd`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_e233`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_696d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_e397`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_3f29`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_aa44`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under SHIFT_CONTRAST.
- **`prb_f5c7`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |

### Probe Rationales & Evidence Notes

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_8ecd` | NEGATION_INSERTION | "The film was amazing,me a..." → "The film was not amazing,..." | POSITIVE (0.99) | NEGATIVE (0.40) | POSITIVE → NEGATIVE | -58.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_e233` | DOUBLE_NEGATION | "The film was amazing,me a..." → "It is not impossible that..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_696d` | INTENSITY | "The film was amazing,me a..." → "The film extremely was am..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e397` | INTENSITY | "The film was amazing,me a..." → "The film somewhat was ama..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3f29` | SYNONYM_SUBSTITUTION | "The film was amazing,me a..." → "The cinema was amazing,me..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_aa44` | CONTRAST_NEGATIVE_APPEND | "The film was amazing,me a..." → "The film was amazing,me a..." | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -1.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_f5c7` | CONTRAST_POSITIVE_APPEND | "The film was amazing,me a..." → "The film was amazing,me a..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_8ecd`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_e233`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_696d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_e397`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_3f29`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_aa44`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_f5c7`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_8ecd` | NEGATION_INSERTION | "The film was amazing,me a..." → "The film was not amazing,..." | POSITIVE (1.00) | POSITIVE (0.98) | POSITIVE → POSITIVE | -2.4 | NO | `MISSING_FLIP` | **Blind** |
| `prb_e233` | DOUBLE_NEGATION | "The film was amazing,me a..." → "It is not impossible that..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_696d` | INTENSITY | "The film was amazing,me a..." → "The film extremely was am..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e397` | INTENSITY | "The film was amazing,me a..." → "The film somewhat was ama..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3f29` | SYNONYM_SUBSTITUTION | "The film was amazing,me a..." → "The cinema was amazing,me..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_aa44` | CONTRAST_NEGATIVE_APPEND | "The film was amazing,me a..." → "The film was amazing,me a..." | POSITIVE (1.00) | NEGATIVE (0.55) | POSITIVE → NEGATIVE | -45.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_f5c7` | CONTRAST_POSITIVE_APPEND | "The film was amazing,me a..." → "The film was amazing,me a..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_8ecd`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_e233`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_696d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_e397`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_3f29`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_aa44`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under SHIFT_CONTRAST.
- **`prb_f5c7`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_8ecd` | NEGATION_INSERTION | "The film was amazing,me a..." → "The film was not amazing,..." | POSITIVE (0.99) | NEGATIVE (0.40) | POSITIVE → NEGATIVE | -59.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_e233` | DOUBLE_NEGATION | "The film was amazing,me a..." → "It is not impossible that..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_696d` | INTENSITY | "The film was amazing,me a..." → "The film extremely was am..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e397` | INTENSITY | "The film was amazing,me a..." → "The film somewhat was ama..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3f29` | SYNONYM_SUBSTITUTION | "The film was amazing,me a..." → "The cinema was amazing,me..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_aa44` | CONTRAST_NEGATIVE_APPEND | "The film was amazing,me a..." → "The film was amazing,me a..." | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -2.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_f5c7` | CONTRAST_POSITIVE_APPEND | "The film was amazing,me a..." → "The film was amazing,me a..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_8ecd`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_e233`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_696d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_e397`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_3f29`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_aa44`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_f5c7`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.