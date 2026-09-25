# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790354301_11f5af`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7ee0` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | NEGATIVE (0.80) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +19.6 | NO | `MISSING_FLIP` | **Blind** |
| `prb_dfaa` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | NEGATIVE (0.80) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +19.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8c69` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | NEGATIVE (0.80) | NEGATIVE (0.94) | NEGATIVE → NEGATIVE | +13.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a7a8` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | NEGATIVE (0.80) | NEGATIVE (0.94) | NEGATIVE → NEGATIVE | +13.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c5dd` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am salubrious but still..." | NEGATIVE (0.80) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +18.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_40cd` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEGATIVE (0.80) | NEGATIVE (0.71) | NEGATIVE → NEGATIVE | -8.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_953d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEGATIVE (0.80) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +19.8 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_7ee0`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_dfaa`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_8c69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_a7a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_c5dd`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_40cd`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_953d`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7ee0` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | NEGATIVE (0.66) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +33.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_dfaa` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | NEGATIVE (0.66) | NEGATIVE (0.87) | NEGATIVE → NEGATIVE | +21.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8c69` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | NEGATIVE (0.66) | NEGATIVE (0.61) | NEGATIVE → NEGATIVE | -4.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a7a8` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | NEGATIVE (0.66) | NEGATIVE (0.70) | NEGATIVE → NEGATIVE | +4.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c5dd` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am salubrious but still..." | NEGATIVE (0.66) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | +31.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_40cd` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEGATIVE (0.66) | NEGATIVE (0.56) | NEGATIVE → NEGATIVE | -9.6 | NO | `MISSING_FLIP` | **Blind** |
| `prb_953d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEGATIVE (0.66) | POSITIVE (0.99) | NEGATIVE → POSITIVE | +33.2 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_7ee0`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_dfaa`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_8c69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_a7a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_c5dd`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_40cd`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_953d`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7ee0` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | NEGATIVE (0.74) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +25.0 | NO | `MISSING_FLIP` | **Blind** |
| `prb_dfaa` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | NEGATIVE (0.74) | NEGATIVE (0.92) | NEGATIVE → NEGATIVE | +17.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8c69` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | NEGATIVE (0.74) | NEGATIVE (0.65) | NEGATIVE → NEGATIVE | -9.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a7a8` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | NEGATIVE (0.74) | NEGATIVE (0.80) | NEGATIVE → NEGATIVE | +5.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c5dd` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am salubrious but still..." | NEGATIVE (0.74) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +24.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_40cd` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEGATIVE (0.74) | NEGATIVE (0.61) | NEGATIVE → NEGATIVE | -13.8 | NO | `MISSING_FLIP` | **Blind** |
| `prb_953d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEGATIVE (0.74) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +25.6 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_7ee0`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_dfaa`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_8c69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_a7a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_c5dd`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_40cd`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_953d`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7ee0` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | NEUTRAL (0.72) | NEGATIVE (0.86) | NEUTRAL → NEGATIVE | +14.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_dfaa` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | NEUTRAL (0.72) | NEUTRAL (0.52) | NEUTRAL → NEUTRAL | -20.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8c69` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | NEUTRAL (0.72) | POSITIVE (0.49) | NEUTRAL → POSITIVE | -22.7 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_a7a8` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | NEUTRAL (0.72) | NEUTRAL (0.76) | NEUTRAL → NEUTRAL | +4.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c5dd` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am salubrious but still..." | NEUTRAL (0.72) | NEGATIVE (0.71) | NEUTRAL → NEGATIVE | -1.2 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_40cd` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEUTRAL (0.72) | NEGATIVE (0.66) | NEUTRAL → NEGATIVE | -6.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_953d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEUTRAL (0.72) | POSITIVE (0.93) | NEUTRAL → POSITIVE | +20.7 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_7ee0`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → NEGATIVE under REVERSE_POLARITY.
- **`prb_dfaa`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_8c69`** [Misweighted / UNEXPECTED_FLIP]: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **`prb_a7a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_c5dd`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → NEGATIVE).
- **`prb_40cd`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → NEGATIVE under SHIFT_CONTRAST.
- **`prb_953d`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7ee0` | NEGATION_INSERTION | "i am healthy but still ho..." → "i am not healthy but stil..." | NEUTRAL (0.48) | NEGATIVE (0.94) | NEUTRAL → NEGATIVE | +45.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_dfaa` | DOUBLE_NEGATION | "i am healthy but still ho..." → "It is not impossible that..." | NEUTRAL (0.48) | POSITIVE (0.72) | NEUTRAL → POSITIVE | +23.7 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_8c69` | INTENSITY | "i am healthy but still ho..." → "i am extremely healthy bu..." | NEUTRAL (0.48) | POSITIVE (0.78) | NEUTRAL → POSITIVE | +29.8 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_a7a8` | INTENSITY | "i am healthy but still ho..." → "i am somewhat healthy but..." | NEUTRAL (0.48) | POSITIVE (0.55) | NEUTRAL → POSITIVE | +6.6 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_c5dd` | SYNONYM_SUBSTITUTION | "i am healthy but still ho..." → "i am salubrious but still..." | NEUTRAL (0.48) | NEUTRAL (0.64) | NEUTRAL → NEUTRAL | +15.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_40cd` | CONTRAST_NEGATIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEUTRAL (0.48) | NEUTRAL (0.51) | NEUTRAL → NEUTRAL | +2.9 | NO | `MISSING_FLIP` | **Blind** |
| `prb_953d` | CONTRAST_POSITIVE_APPEND | "i am healthy but still ho..." → "i am healthy but still ho..." | NEUTRAL (0.48) | POSITIVE (0.92) | NEUTRAL → POSITIVE | +43.5 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_7ee0`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → NEGATIVE under REVERSE_POLARITY.
- **`prb_dfaa`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **`prb_8c69`** [Misweighted / UNEXPECTED_FLIP]: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **`prb_a7a8`** [Misweighted / UNEXPECTED_FLIP]: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (WEAKEN_POLARITY), indicating disproportionately skewed feature weighting.
- **`prb_c5dd`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_40cd`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **`prb_953d`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).