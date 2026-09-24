# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790181290_8ddb24`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c071` | NEGATION_INSERTION | "i am healthy but am still..." → "i am not healthy but am s..." | NEGATIVE (0.98) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +1.8 | NO | `MISSING_FLIP` | **Blind** |
| `prb_e424` | DOUBLE_NEGATION | "i am healthy but am still..." → "It is not impossible that..." | NEGATIVE (0.98) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +1.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f559` | INTENSITY | "i am healthy but am still..." → "i am extremely healthy bu..." | NEGATIVE (0.98) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_98d0` | INTENSITY | "i am healthy but am still..." → "i am somewhat healthy but..." | NEGATIVE (0.98) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_54ca` | SYNONYM_SUBSTITUTION | "i am healthy but am still..." → "i am tidy but am still ho..." | NEGATIVE (0.98) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +1.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3ff0` | CONTRAST_NEGATIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEGATIVE (0.98) | NEGATIVE (0.91) | NEGATIVE → NEGATIVE | -7.5 | NO | `MISSING_FLIP` | **Blind** |
| `prb_29a1` | CONTRAST_POSITIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEGATIVE (0.98) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +1.9 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_c071`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_e424`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_f559`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_98d0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_54ca`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_3ff0`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_29a1`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c071` | NEGATION_INSERTION | "i am healthy but am still..." → "i am not healthy but am s..." | NEGATIVE (0.59) | NEGATIVE (0.87) | NEGATIVE → NEGATIVE | +27.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_e424` | DOUBLE_NEGATION | "i am healthy but am still..." → "It is not impossible that..." | NEGATIVE (0.59) | NEGATIVE (0.73) | NEGATIVE → NEGATIVE | +13.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f559` | INTENSITY | "i am healthy but am still..." → "i am extremely healthy bu..." | NEGATIVE (0.59) | NEUTRAL (0.44) | NEGATIVE → NEUTRAL | -15.7 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_98d0` | INTENSITY | "i am healthy but am still..." → "i am somewhat healthy but..." | NEGATIVE (0.59) | NEGATIVE (0.49) | NEGATIVE → NEGATIVE | -10.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_54ca` | SYNONYM_SUBSTITUTION | "i am healthy but am still..." → "i am tidy but am still ho..." | NEGATIVE (0.59) | NEGATIVE (0.78) | NEGATIVE → NEGATIVE | +19.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3ff0` | CONTRAST_NEGATIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEGATIVE (0.59) | NEGATIVE (0.71) | NEGATIVE → NEGATIVE | +11.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_29a1` | CONTRAST_POSITIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEGATIVE (0.59) | POSITIVE (0.82) | NEGATIVE → POSITIVE | +22.2 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_c071`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_e424`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_f559`** [Misweighted / UNEXPECTED_FLIP]: Model inverted prediction (NEGATIVE → NEUTRAL) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **`prb_98d0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_54ca`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_3ff0`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_29a1`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c071` | NEGATION_INSERTION | "i am healthy but am still..." → "i am not healthy but am s..." | NEUTRAL (0.59) | NEGATIVE (0.94) | NEUTRAL → NEGATIVE | +34.7 | YES | `EXPECTED_FLIP` | **None** |
| `prb_e424` | DOUBLE_NEGATION | "i am healthy but am still..." → "It is not impossible that..." | NEUTRAL (0.59) | POSITIVE (0.61) | NEUTRAL → POSITIVE | +1.4 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_f559` | INTENSITY | "i am healthy but am still..." → "i am extremely healthy bu..." | NEUTRAL (0.59) | POSITIVE (0.65) | NEUTRAL → POSITIVE | +5.5 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_98d0` | INTENSITY | "i am healthy but am still..." → "i am somewhat healthy but..." | NEUTRAL (0.59) | NEUTRAL (0.56) | NEUTRAL → NEUTRAL | -2.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_54ca` | SYNONYM_SUBSTITUTION | "i am healthy but am still..." → "i am tidy but am still ho..." | NEUTRAL (0.59) | NEUTRAL (0.49) | NEUTRAL → NEUTRAL | -10.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3ff0` | CONTRAST_NEGATIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEUTRAL (0.59) | NEUTRAL (0.48) | NEUTRAL → NEUTRAL | -10.8 | NO | `MISSING_FLIP` | **Blind** |
| `prb_29a1` | CONTRAST_POSITIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEUTRAL (0.59) | POSITIVE (0.90) | NEUTRAL → POSITIVE | +30.6 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_c071`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → NEGATIVE under REVERSE_POLARITY.
- **`prb_e424`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **`prb_f559`** [Misweighted / UNEXPECTED_FLIP]: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **`prb_98d0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_54ca`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_3ff0`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **`prb_29a1`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c071` | NEGATION_INSERTION | "i am healthy but am still..." → "i am not healthy but am s..." | NEGATIVE (0.72) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +26.9 | NO | `MISSING_FLIP` | **Blind** |
| `prb_e424` | DOUBLE_NEGATION | "i am healthy but am still..." → "It is not impossible that..." | NEGATIVE (0.72) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +22.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f559` | INTENSITY | "i am healthy but am still..." → "i am extremely healthy bu..." | NEGATIVE (0.72) | NEGATIVE (0.66) | NEGATIVE → NEGATIVE | -6.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_98d0` | INTENSITY | "i am healthy but am still..." → "i am somewhat healthy but..." | NEGATIVE (0.72) | NEGATIVE (0.83) | NEGATIVE → NEGATIVE | +10.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_54ca` | SYNONYM_SUBSTITUTION | "i am healthy but am still..." → "i am tidy but am still ho..." | NEGATIVE (0.72) | NEGATIVE (0.93) | NEGATIVE → NEGATIVE | +20.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3ff0` | CONTRAST_NEGATIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEGATIVE (0.72) | NEGATIVE (0.52) | NEGATIVE → NEGATIVE | -20.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_29a1` | CONTRAST_POSITIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEGATIVE (0.72) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +27.6 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_c071`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_e424`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_f559`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_98d0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_54ca`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_3ff0`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_29a1`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c071` | NEGATION_INSERTION | "i am healthy but am still..." → "i am not healthy but am s..." | NEGATIVE (0.96) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +3.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_e424` | DOUBLE_NEGATION | "i am healthy but am still..." → "It is not impossible that..." | NEGATIVE (0.96) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | +1.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f559` | INTENSITY | "i am healthy but am still..." → "i am extremely healthy bu..." | NEGATIVE (0.96) | NEGATIVE (0.92) | NEGATIVE → NEGATIVE | -3.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_98d0` | INTENSITY | "i am healthy but am still..." → "i am somewhat healthy but..." | NEGATIVE (0.96) | NEGATIVE (0.94) | NEGATIVE → NEGATIVE | -2.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_54ca` | SYNONYM_SUBSTITUTION | "i am healthy but am still..." → "i am tidy but am still ho..." | NEGATIVE (0.96) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | +2.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_3ff0` | CONTRAST_NEGATIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEGATIVE (0.96) | NEGATIVE (0.89) | NEGATIVE → NEGATIVE | -6.8 | NO | `MISSING_FLIP` | **Blind** |
| `prb_29a1` | CONTRAST_POSITIVE_APPEND | "i am healthy but am still..." → "i am healthy but am still..." | NEGATIVE (0.96) | POSITIVE (0.98) | NEGATIVE → POSITIVE | +2.0 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_c071`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_e424`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_f559`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_98d0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_54ca`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_3ff0`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_29a1`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).