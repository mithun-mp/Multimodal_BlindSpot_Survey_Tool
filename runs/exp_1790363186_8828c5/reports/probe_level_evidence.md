# Probe-Level Behavioral Evidence: Multimodel Test Run Heavy 001

**Experiment ID**: `exp_1790363186_8828c5`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ae5d` | NEGATION_INSERTION | "Although the product init..." → "Although the product init..." | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_1db9` | DOUBLE_NEGATION | "Although the product init..." → "It is not impossible that..." | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3701` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5463` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_626a` | SYNONYM_SUBSTITUTION | "Although the product init..." → "Although the item initial..." | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d257` | CONTRAST_NEGATIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.0 | NO | `MISSING_FLIP` | **Blind** |
| `prb_cce6` | CONTRAST_POSITIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (1.00) | POSITIVE (0.99) | NEGATIVE → POSITIVE | -0.6 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_ae5d`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_1db9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_3701`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_5463`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_626a`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d257`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_cce6`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ae5d` | NEGATION_INSERTION | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -0.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_1db9` | DOUBLE_NEGATION | "Although the product init..." → "It is not impossible that..." | NEGATIVE (0.98) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | -1.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3701` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | -0.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5463` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_626a` | SYNONYM_SUBSTITUTION | "Although the product init..." → "Although the item initial..." | NEGATIVE (0.98) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d257` | CONTRAST_NEGATIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +0.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_cce6` | CONTRAST_POSITIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | -3.4 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_ae5d`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_1db9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_3701`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_5463`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_626a`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d257`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_cce6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ae5d` | NEGATION_INSERTION | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | +0.4 | NO | `MISSING_FLIP` | **Blind** |
| `prb_1db9` | DOUBLE_NEGATION | "Although the product init..." → "It is not impossible that..." | NEGATIVE (0.98) | NEGATIVE (0.93) | NEGATIVE → NEGATIVE | -5.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3701` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5463` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_626a` | SYNONYM_SUBSTITUTION | "Although the product init..." → "Although the item initial..." | NEGATIVE (0.98) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d257` | CONTRAST_NEGATIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | +0.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_cce6` | CONTRAST_POSITIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (0.98) | POSITIVE (0.95) | NEGATIVE → POSITIVE | -3.1 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_ae5d`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_1db9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_3701`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_5463`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_626a`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d257`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_cce6`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ae5d` | NEGATION_INSERTION | "Although the product init..." → "Although the product init..." | NEGATIVE (0.80) | NEGATIVE (0.82) | NEGATIVE → NEGATIVE | +2.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_1db9` | DOUBLE_NEGATION | "Although the product init..." → "It is not impossible that..." | NEGATIVE (0.80) | NEGATIVE (0.65) | NEGATIVE → NEGATIVE | -14.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3701` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (0.80) | NEGATIVE (0.77) | NEGATIVE → NEGATIVE | -2.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5463` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (0.80) | NEGATIVE (0.79) | NEGATIVE → NEGATIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_626a` | SYNONYM_SUBSTITUTION | "Although the product init..." → "Although the item initial..." | NEGATIVE (0.80) | NEGATIVE (0.80) | NEGATIVE → NEGATIVE | +0.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d257` | CONTRAST_NEGATIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (0.80) | NEGATIVE (0.86) | NEGATIVE → NEGATIVE | +6.0 | NO | `MISSING_FLIP` | **Blind** |
| `prb_cce6` | CONTRAST_POSITIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (0.80) | NEGATIVE (0.44) | NEGATIVE → NEGATIVE | -35.9 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_ae5d`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_1db9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_3701`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_5463`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_626a`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d257`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_cce6`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_ae5d` | NEGATION_INSERTION | "Although the product init..." → "Although the product init..." | NEGATIVE (0.52) | NEGATIVE (0.50) | NEGATIVE → NEGATIVE | -1.8 | NO | `MISSING_FLIP` | **Blind** |
| `prb_1db9` | DOUBLE_NEGATION | "Although the product init..." → "It is not impossible that..." | NEGATIVE (0.52) | NEGATIVE (0.47) | NEGATIVE → NEGATIVE | -4.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3701` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (0.52) | NEGATIVE (0.49) | NEGATIVE → NEGATIVE | -2.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5463` | INTENSITY | "Although the product init..." → "Although the product init..." | NEGATIVE (0.52) | NEGATIVE (0.52) | NEGATIVE → NEGATIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_626a` | SYNONYM_SUBSTITUTION | "Although the product init..." → "Although the item initial..." | NEGATIVE (0.52) | NEGATIVE (0.52) | NEGATIVE → NEGATIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d257` | CONTRAST_NEGATIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (0.52) | NEGATIVE (0.57) | NEGATIVE → NEGATIVE | +5.5 | NO | `MISSING_FLIP` | **Blind** |
| `prb_cce6` | CONTRAST_POSITIVE_APPEND | "Although the product init..." → "Although the product init..." | NEGATIVE (0.52) | NEUTRAL (0.36) | NEGATIVE → NEUTRAL | -15.9 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_ae5d`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_1db9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_3701`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_5463`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_626a`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d257`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_cce6`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → NEUTRAL).