# Probe-Level Behavioral Evidence: Multimodel Test Run 004

**Experiment ID**: `exp_1790357357_062da3`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_859f` | NEGATION_INSERTION | "I am Healthy and Energeti..." → "I am not Healthy and Ener..." | NEGATIVE (0.99) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.8 | NO | `MISSING_FLIP` | **Blind** |
| `prb_bae1` | DOUBLE_NEGATION | "I am Healthy and Energeti..." → "It is not impossible that..." | NEGATIVE (0.99) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0911` | INTENSITY | "I am Healthy and Energeti..." → "I am extremely Healthy an..." | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | -0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d705` | INTENSITY | "I am Healthy and Energeti..." → "I am somewhat Healthy and..." | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a85e` | SYNONYM_SUBSTITUTION | "I am Healthy and Energeti..." → "I am Respectable and Ener..." | NEGATIVE (0.99) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2c66` | CONTRAST_NEGATIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | NEGATIVE (0.99) | NEGATIVE (0.80) | NEGATIVE → NEGATIVE | -19.6 | NO | `MISSING_FLIP` | **Blind** |
| `prb_b840` | CONTRAST_POSITIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | NEGATIVE (0.99) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +0.7 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_859f`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_bae1`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_0911`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d705`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_a85e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_2c66`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_b840`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_859f` | NEGATION_INSERTION | "I am Healthy and Energeti..." → "I am not Healthy and Ener..." | POSITIVE (0.61) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | +36.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_bae1` | DOUBLE_NEGATION | "I am Healthy and Energeti..." → "It is not impossible that..." | POSITIVE (0.61) | NEGATIVE (0.55) | POSITIVE → NEGATIVE | -6.4 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_0911` | INTENSITY | "I am Healthy and Energeti..." → "I am extremely Healthy an..." | POSITIVE (0.61) | POSITIVE (0.71) | POSITIVE → POSITIVE | +9.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d705` | INTENSITY | "I am Healthy and Energeti..." → "I am somewhat Healthy and..." | POSITIVE (0.61) | POSITIVE (0.59) | POSITIVE → POSITIVE | -2.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a85e` | SYNONYM_SUBSTITUTION | "I am Healthy and Energeti..." → "I am Respectable and Ener..." | POSITIVE (0.61) | NEGATIVE (0.53) | POSITIVE → NEGATIVE | -8.7 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_2c66` | CONTRAST_NEGATIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | POSITIVE (0.61) | POSITIVE (0.76) | POSITIVE → POSITIVE | +14.8 | NO | `MISSING_FLIP` | **Blind** |
| `prb_b840` | CONTRAST_POSITIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | POSITIVE (0.61) | POSITIVE (0.98) | POSITIVE → POSITIVE | +36.7 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_859f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_bae1`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (POSITIVE → NEGATIVE).
- **`prb_0911`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_d705`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_a85e`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (POSITIVE → NEGATIVE).
- **`prb_2c66`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_b840`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_859f` | NEGATION_INSERTION | "I am Healthy and Energeti..." → "I am not Healthy and Ener..." | NEGATIVE (0.96) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +3.5 | NO | `MISSING_FLIP` | **Blind** |
| `prb_bae1` | DOUBLE_NEGATION | "I am Healthy and Energeti..." → "It is not impossible that..." | NEGATIVE (0.96) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +3.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0911` | INTENSITY | "I am Healthy and Energeti..." → "I am extremely Healthy an..." | NEGATIVE (0.96) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | -1.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d705` | INTENSITY | "I am Healthy and Energeti..." → "I am somewhat Healthy and..." | NEGATIVE (0.96) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | +2.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a85e` | SYNONYM_SUBSTITUTION | "I am Healthy and Energeti..." → "I am Respectable and Ener..." | NEGATIVE (0.96) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +2.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2c66` | CONTRAST_NEGATIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | NEGATIVE (0.96) | NEGATIVE (0.79) | NEGATIVE → NEGATIVE | -17.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_b840` | CONTRAST_POSITIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | NEGATIVE (0.96) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +3.7 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_859f`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_bae1`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_0911`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d705`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_a85e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_2c66`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_b840`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_859f` | NEGATION_INSERTION | "I am Healthy and Energeti..." → "I am not Healthy and Ener..." | NEUTRAL (0.62) | NEGATIVE (0.81) | NEUTRAL → NEGATIVE | +19.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_bae1` | DOUBLE_NEGATION | "I am Healthy and Energeti..." → "It is not impossible that..." | NEUTRAL (0.62) | NEGATIVE (0.49) | NEUTRAL → NEGATIVE | -13.3 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_0911` | INTENSITY | "I am Healthy and Energeti..." → "I am extremely Healthy an..." | NEUTRAL (0.62) | NEUTRAL (0.52) | NEUTRAL → NEUTRAL | -9.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d705` | INTENSITY | "I am Healthy and Energeti..." → "I am somewhat Healthy and..." | NEUTRAL (0.62) | NEUTRAL (0.70) | NEUTRAL → NEUTRAL | +8.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a85e` | SYNONYM_SUBSTITUTION | "I am Healthy and Energeti..." → "I am Respectable and Ener..." | NEUTRAL (0.62) | NEUTRAL (0.57) | NEUTRAL → NEUTRAL | -4.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2c66` | CONTRAST_NEGATIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | NEUTRAL (0.62) | NEGATIVE (0.49) | NEUTRAL → NEGATIVE | -13.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_b840` | CONTRAST_POSITIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | NEUTRAL (0.62) | POSITIVE (0.88) | NEUTRAL → POSITIVE | +25.9 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_859f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → NEGATIVE under REVERSE_POLARITY.
- **`prb_bae1`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → NEGATIVE).
- **`prb_0911`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_d705`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_a85e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_2c66`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → NEGATIVE under SHIFT_CONTRAST.
- **`prb_b840`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_859f` | NEGATION_INSERTION | "I am Healthy and Energeti..." → "I am not Healthy and Ener..." | NEUTRAL (0.52) | NEGATIVE (0.93) | NEUTRAL → NEGATIVE | +40.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_bae1` | DOUBLE_NEGATION | "I am Healthy and Energeti..." → "It is not impossible that..." | NEUTRAL (0.52) | POSITIVE (0.56) | NEUTRAL → POSITIVE | +4.0 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_0911` | INTENSITY | "I am Healthy and Energeti..." → "I am extremely Healthy an..." | NEUTRAL (0.52) | POSITIVE (0.54) | NEUTRAL → POSITIVE | +1.4 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_d705` | INTENSITY | "I am Healthy and Energeti..." → "I am somewhat Healthy and..." | NEUTRAL (0.52) | NEUTRAL (0.56) | NEUTRAL → NEUTRAL | +3.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_a85e` | SYNONYM_SUBSTITUTION | "I am Healthy and Energeti..." → "I am Respectable and Ener..." | NEUTRAL (0.52) | NEUTRAL (0.59) | NEUTRAL → NEUTRAL | +7.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2c66` | CONTRAST_NEGATIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | NEUTRAL (0.52) | NEUTRAL (0.49) | NEUTRAL → NEUTRAL | -3.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_b840` | CONTRAST_POSITIVE_APPEND | "I am Healthy and Energeti..." → "I am Healthy and Energeti..." | NEUTRAL (0.52) | POSITIVE (0.92) | NEUTRAL → POSITIVE | +40.0 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_859f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → NEGATIVE under REVERSE_POLARITY.
- **`prb_bae1`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **`prb_0911`** [Misweighted / UNEXPECTED_FLIP]: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **`prb_d705`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_a85e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_2c66`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **`prb_b840`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).