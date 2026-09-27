# Probe-Level Behavioral Evidence: Multimodel 00001

**Experiment ID**: `exp_1790537272_6f4cc1`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_4069` | NEGATION_INSERTION | "He is a Good boy but very..." → "He is not a Good boy but ..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | NEGATIVE (0.88) | POSITIVE → NEGATIVE | -11.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_83a0` | DOUBLE_NEGATION | "He is a Good boy but very..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e47f` | INTENSITY | "He is a Good boy but very..." → "He is a extremely Good bo..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0a25` | INTENSITY | "He is a Good boy but very..." → "He is a somewhat Good boy..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0b5` | SYNONYM_SUBSTITUTION | "He is a Good boy but very..." → "He is a Decent boy but ve..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_67a0` | CONTRAST_NEGATIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `NEGATIVE (REVERSE)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_c550` | CONTRAST_POSITIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `POSITIVE (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_4069`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_83a0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_e47f`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_0a25`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_b0b5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_67a0`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_c550`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_4069` | NEGATION_INSERTION | "He is a Good boy but very..." → "He is not a Good boy but ..." | `NEGATIVE (REVERSE)` | POSITIVE (0.91) | POSITIVE (0.83) | POSITIVE → POSITIVE | -8.5 | NO | `MISSING_FLIP` | **Blind** |
| `prb_83a0` | DOUBLE_NEGATION | "He is a Good boy but very..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.91) | POSITIVE (0.89) | POSITIVE → POSITIVE | -2.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e47f` | INTENSITY | "He is a Good boy but very..." → "He is a extremely Good bo..." | `POSITIVE (PRESERVE)` | POSITIVE (0.91) | POSITIVE (0.94) | POSITIVE → POSITIVE | +3.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0a25` | INTENSITY | "He is a Good boy but very..." → "He is a somewhat Good boy..." | `POSITIVE (PRESERVE)` | POSITIVE (0.91) | POSITIVE (0.93) | POSITIVE → POSITIVE | +1.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0b5` | SYNONYM_SUBSTITUTION | "He is a Good boy but very..." → "He is a Decent boy but ve..." | `POSITIVE (PRESERVE)` | POSITIVE (0.91) | POSITIVE (0.86) | POSITIVE → POSITIVE | -5.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_67a0` | CONTRAST_NEGATIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `NEGATIVE (REVERSE)` | POSITIVE (0.91) | POSITIVE (0.74) | POSITIVE → POSITIVE | -17.0 | NO | `MISSING_FLIP` | **Blind** |
| `prb_c550` | CONTRAST_POSITIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `POSITIVE (PRESERVE)` | POSITIVE (0.91) | POSITIVE (1.00) | POSITIVE → POSITIVE | +8.7 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_4069`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_83a0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_e47f`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_0a25`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_b0b5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_67a0`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_c550`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_4069` | NEGATION_INSERTION | "He is a Good boy but very..." → "He is not a Good boy but ..." | `NEGATIVE (REVERSE)` | POSITIVE (0.98) | NEGATIVE (0.95) | POSITIVE → NEGATIVE | -3.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_83a0` | DOUBLE_NEGATION | "He is a Good boy but very..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (0.91) | POSITIVE → POSITIVE | -7.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e47f` | INTENSITY | "He is a Good boy but very..." → "He is a extremely Good bo..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.6 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0a25` | INTENSITY | "He is a Good boy but very..." → "He is a somewhat Good boy..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (0.95) | POSITIVE → POSITIVE | -3.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0b5` | SYNONYM_SUBSTITUTION | "He is a Good boy but very..." → "He is a Decent boy but ve..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (0.88) | POSITIVE → POSITIVE | -10.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_67a0` | CONTRAST_NEGATIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `NEGATIVE (REVERSE)` | POSITIVE (0.98) | POSITIVE (0.97) | POSITIVE → POSITIVE | -0.9 | NO | `MISSING_FLIP` | **Blind** |
| `prb_c550` | CONTRAST_POSITIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `POSITIVE (PRESERVE)` | POSITIVE (0.98) | POSITIVE (1.00) | POSITIVE → POSITIVE | +1.8 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_4069`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_83a0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_e47f`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_0a25`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_b0b5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_67a0`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_c550`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_4069` | NEGATION_INSERTION | "He is a Good boy but very..." → "He is not a Good boy but ..." | `NEGATIVE (REVERSE)` | POSITIVE (0.61) | NEGATIVE (0.86) | POSITIVE → NEGATIVE | +25.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_83a0` | DOUBLE_NEGATION | "He is a Good boy but very..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | POSITIVE (0.61) | POSITIVE (0.48) | POSITIVE → POSITIVE | -12.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e47f` | INTENSITY | "He is a Good boy but very..." → "He is a extremely Good bo..." | `POSITIVE (PRESERVE)` | POSITIVE (0.61) | POSITIVE (0.87) | POSITIVE → POSITIVE | +26.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0a25` | INTENSITY | "He is a Good boy but very..." → "He is a somewhat Good boy..." | `POSITIVE (PRESERVE)` | POSITIVE (0.61) | POSITIVE (0.50) | POSITIVE → POSITIVE | -10.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0b5` | SYNONYM_SUBSTITUTION | "He is a Good boy but very..." → "He is a Decent boy but ve..." | `POSITIVE (PRESERVE)` | POSITIVE (0.61) | POSITIVE (0.58) | POSITIVE → POSITIVE | -2.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_67a0` | CONTRAST_NEGATIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `NEGATIVE (REVERSE)` | POSITIVE (0.61) | NEUTRAL (0.43) | POSITIVE → NEUTRAL | -17.5 | NO | `EXPECTED_FLIP` | **None** |
| `prb_c550` | CONTRAST_POSITIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `POSITIVE (PRESERVE)` | POSITIVE (0.61) | POSITIVE (0.90) | POSITIVE → POSITIVE | +29.7 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_4069`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_83a0`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_e47f`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_0a25`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_b0b5`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_67a0`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEUTRAL (NEUTRAL)) under DIFFERENT_LABEL expectation.
- **`prb_c550`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_4069` | NEGATION_INSERTION | "He is a Good boy but very..." → "He is not a Good boy but ..." | `NEGATIVE (REVERSE)` | NEUTRAL (0.47) | NEGATIVE (0.93) | NEUTRAL → NEGATIVE | +45.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_83a0` | DOUBLE_NEGATION | "He is a Good boy but very..." → "It is not impossible that..." | `POSITIVE (PRESERVE)` | NEUTRAL (0.47) | POSITIVE (0.45) | NEUTRAL → POSITIVE | -1.6 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_e47f` | INTENSITY | "He is a Good boy but very..." → "He is a extremely Good bo..." | `POSITIVE (PRESERVE)` | NEUTRAL (0.47) | POSITIVE (0.69) | NEUTRAL → POSITIVE | +22.2 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_0a25` | INTENSITY | "He is a Good boy but very..." → "He is a somewhat Good boy..." | `POSITIVE (PRESERVE)` | NEUTRAL (0.47) | NEUTRAL (0.50) | NEUTRAL → NEUTRAL | +3.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0b5` | SYNONYM_SUBSTITUTION | "He is a Good boy but very..." → "He is a Decent boy but ve..." | `POSITIVE (PRESERVE)` | NEUTRAL (0.47) | NEGATIVE (0.48) | NEUTRAL → NEGATIVE | +1.1 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_67a0` | CONTRAST_NEGATIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `NEGATIVE (REVERSE)` | NEUTRAL (0.47) | NEUTRAL (0.47) | NEUTRAL → NEUTRAL | +0.5 | NO | `MISSING_FLIP` | **Blind** |
| `prb_c550` | CONTRAST_POSITIVE_APPEND | "He is a Good boy but very..." → "He is a Good boy but very..." | `POSITIVE (PRESERVE)` | NEUTRAL (0.47) | POSITIVE (0.86) | NEUTRAL → POSITIVE | +38.8 | YES | `UNEXPECTED_CHANGE` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_4069`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEUTRAL (NEUTRAL) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_83a0`** [Spurious / UNEXPECTED_CHANGE]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **`prb_e47f`** [Misweighted / UNEXPECTED_FLIP]: Intensifier inverted polarity (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **`prb_0a25`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_b0b5`** [Spurious / UNEXPECTED_CHANGE]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → NEGATIVE (NEGATIVE)).
- **`prb_67a0`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_c550`** [Spurious / UNEXPECTED_CHANGE]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).