# Probe-Level Behavioral Evidence: Multimodel 003

**Experiment ID**: `exp_1790104901_f2922f`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_a642` | NEGATION_INSERTION | "I am healthy But still ho..." → "I am not healthy But stil..." | NEGATIVE (0.86) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +14.0 | NO | `MISSING_FLIP` | **Blind** |
| `prb_316d` | DOUBLE_NEGATION | "I am healthy But still ho..." → "It is not impossible that..." | NEGATIVE (0.86) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +13.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1b69` | INTENSITY | "I am healthy But still ho..." → "I am extremely healthy Bu..." | NEGATIVE (0.86) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +9.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d11d` | INTENSITY | "I am healthy But still ho..." → "I am somewhat healthy But..." | NEGATIVE (0.86) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +9.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_720e` | SYNONYM_SUBSTITUTION | "I am healthy But still ho..." → "I am goodish But still ho..." | NEGATIVE (0.86) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | +11.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f60e` | CONTRAST_NEGATIVE_APPEND | "I am healthy But still ho..." → "I am healthy But still ho..." | NEGATIVE (0.86) | NEGATIVE (0.71) | NEGATIVE → NEGATIVE | -14.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_e6a5` | STRUCTURE | "I am healthy But still ho..." → "In fact, i am healthy But..." | NEGATIVE (0.86) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +8.9 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_a642`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_316d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_1b69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d11d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_720e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_f60e`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_e6a5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_a642` | NEGATION_INSERTION | "I am healthy But still ho..." → "I am not healthy But stil..." | NEGATIVE (0.63) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +35.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_316d` | DOUBLE_NEGATION | "I am healthy But still ho..." → "It is not impossible that..." | NEGATIVE (0.63) | NEGATIVE (0.86) | NEGATIVE → NEGATIVE | +22.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1b69` | INTENSITY | "I am healthy But still ho..." → "I am extremely healthy Bu..." | NEGATIVE (0.63) | NEGATIVE (0.60) | NEGATIVE → NEGATIVE | -3.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d11d` | INTENSITY | "I am healthy But still ho..." → "I am somewhat healthy But..." | NEGATIVE (0.63) | NEGATIVE (0.68) | NEGATIVE → NEGATIVE | +4.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_720e` | SYNONYM_SUBSTITUTION | "I am healthy But still ho..." → "I am goodish But still ho..." | NEGATIVE (0.63) | NEGATIVE (0.52) | NEGATIVE → NEGATIVE | -11.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f60e` | CONTRAST_NEGATIVE_APPEND | "I am healthy But still ho..." → "I am healthy But still ho..." | NEGATIVE (0.63) | NEGATIVE (0.56) | NEGATIVE → NEGATIVE | -7.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_e6a5` | STRUCTURE | "I am healthy But still ho..." → "In fact, i am healthy But..." | NEGATIVE (0.63) | NEGATIVE (0.75) | NEGATIVE → NEGATIVE | +11.9 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_a642`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_316d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_1b69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d11d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_720e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_f60e`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_e6a5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_a642` | NEGATION_INSERTION | "I am healthy But still ho..." → "I am not healthy But stil..." | NEGATIVE (0.82) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +17.5 | NO | `MISSING_FLIP` | **Blind** |
| `prb_316d` | DOUBLE_NEGATION | "I am healthy But still ho..." → "It is not impossible that..." | NEGATIVE (0.82) | NEGATIVE (0.94) | NEGATIVE → NEGATIVE | +11.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1b69` | INTENSITY | "I am healthy But still ho..." → "I am extremely healthy Bu..." | NEGATIVE (0.82) | NEGATIVE (0.77) | NEGATIVE → NEGATIVE | -4.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d11d` | INTENSITY | "I am healthy But still ho..." → "I am somewhat healthy But..." | NEGATIVE (0.82) | NEGATIVE (0.87) | NEGATIVE → NEGATIVE | +5.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_720e` | SYNONYM_SUBSTITUTION | "I am healthy But still ho..." → "I am goodish But still ho..." | NEGATIVE (0.82) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | +13.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f60e` | CONTRAST_NEGATIVE_APPEND | "I am healthy But still ho..." → "I am healthy But still ho..." | NEGATIVE (0.82) | NEGATIVE (0.61) | NEGATIVE → NEGATIVE | -21.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_e6a5` | STRUCTURE | "I am healthy But still ho..." → "In fact, i am healthy But..." | NEGATIVE (0.82) | POSITIVE (0.61) | NEGATIVE → POSITIVE | -20.8 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_a642`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_316d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_1b69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_d11d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_720e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_f60e`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_e6a5`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_a642` | NEGATION_INSERTION | "I am healthy But still ho..." → "I am not healthy But stil..." | NEUTRAL (0.66) | NEGATIVE (0.84) | NEUTRAL → NEGATIVE | +18.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_316d` | DOUBLE_NEGATION | "I am healthy But still ho..." → "It is not impossible that..." | NEUTRAL (0.66) | NEUTRAL (0.60) | NEUTRAL → NEUTRAL | -5.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1b69` | INTENSITY | "I am healthy But still ho..." → "I am extremely healthy Bu..." | NEUTRAL (0.66) | POSITIVE (0.69) | NEUTRAL → POSITIVE | +2.6 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_d11d` | INTENSITY | "I am healthy But still ho..." → "I am somewhat healthy But..." | NEUTRAL (0.66) | NEUTRAL (0.64) | NEUTRAL → NEUTRAL | -1.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_720e` | SYNONYM_SUBSTITUTION | "I am healthy But still ho..." → "I am goodish But still ho..." | NEUTRAL (0.66) | NEUTRAL (0.51) | NEUTRAL → NEUTRAL | -15.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f60e` | CONTRAST_NEGATIVE_APPEND | "I am healthy But still ho..." → "I am healthy But still ho..." | NEUTRAL (0.66) | NEGATIVE (0.55) | NEUTRAL → NEGATIVE | -11.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_e6a5` | STRUCTURE | "I am healthy But still ho..." → "In fact, i am healthy But..." | NEUTRAL (0.66) | POSITIVE (0.53) | NEUTRAL → POSITIVE | -13.6 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_a642`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → NEGATIVE under REVERSE_POLARITY.
- **`prb_316d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_1b69`** [Misweighted / UNEXPECTED_FLIP]: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **`prb_d11d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_720e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_f60e`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → NEGATIVE under SHIFT_CONTRAST.
- **`prb_e6a5`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_a642` | NEGATION_INSERTION | "I am healthy But still ho..." → "I am not healthy But stil..." | POSITIVE (0.52) | NEGATIVE (0.95) | POSITIVE → NEGATIVE | +43.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_316d` | DOUBLE_NEGATION | "I am healthy But still ho..." → "It is not impossible that..." | POSITIVE (0.52) | POSITIVE (0.69) | POSITIVE → POSITIVE | +16.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_1b69` | INTENSITY | "I am healthy But still ho..." → "I am extremely healthy Bu..." | POSITIVE (0.52) | POSITIVE (0.81) | POSITIVE → POSITIVE | +28.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d11d` | INTENSITY | "I am healthy But still ho..." → "I am somewhat healthy But..." | POSITIVE (0.52) | POSITIVE (0.57) | POSITIVE → POSITIVE | +4.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_720e` | SYNONYM_SUBSTITUTION | "I am healthy But still ho..." → "I am goodish But still ho..." | POSITIVE (0.52) | POSITIVE (0.67) | POSITIVE → POSITIVE | +15.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_f60e` | CONTRAST_NEGATIVE_APPEND | "I am healthy But still ho..." → "I am healthy But still ho..." | POSITIVE (0.52) | NEUTRAL (0.51) | POSITIVE → NEUTRAL | -1.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_e6a5` | STRUCTURE | "I am healthy But still ho..." → "In fact, i am healthy But..." | POSITIVE (0.52) | POSITIVE (0.74) | POSITIVE → POSITIVE | +22.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_a642`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_316d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_1b69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_d11d`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_720e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_f60e`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEUTRAL under SHIFT_CONTRAST.
- **`prb_e6a5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.