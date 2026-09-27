# Probe-Level Behavioral Evidence: mul01

**Experiment ID**: `exp_1790529126_68517a`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7d98` | NEGATION_PREFIX | "the sun rises in east and..." → "It is not true that the s..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_7bb9` | DOUBLE_NEGATION | "the sun rises in east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c7e3` | INTENSITY | "the sun rises in east and..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b6da` | INTENSITY | "the sun rises in east and..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9953` | SYNONYM_SUBSTITUTION | "the sun rises in east and..." → "the insolate rises in eas..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | POSITIVE (0.96) | POSITIVE → POSITIVE | -3.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2dd2` | CONTRAST_NEGATIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.7 | YES | `EXPECTED_FLIP` | **None** |
| `prb_6cbf` | CONTRAST_POSITIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_7d98`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_7bb9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c7e3`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_b6da`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_9953`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2dd2`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_6cbf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7d98` | NEGATION_PREFIX | "the sun rises in east and..." → "It is not true that the s..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.93) | NEGATIVE (0.93) | POSITIVE → NEGATIVE | +0.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_7bb9` | DOUBLE_NEGATION | "the sun rises in east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.93) | POSITIVE (0.94) | POSITIVE → POSITIVE | +1.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c7e3` | INTENSITY | "the sun rises in east and..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.93) | POSITIVE (0.97) | POSITIVE → POSITIVE | +4.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b6da` | INTENSITY | "the sun rises in east and..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.93) | POSITIVE (0.93) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9953` | SYNONYM_SUBSTITUTION | "the sun rises in east and..." → "the insolate rises in eas..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.93) | POSITIVE (0.82) | POSITIVE → POSITIVE | -10.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2dd2` | CONTRAST_NEGATIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.93) | NEGATIVE (0.96) | POSITIVE → NEGATIVE | +2.7 | YES | `EXPECTED_FLIP` | **None** |
| `prb_6cbf` | CONTRAST_POSITIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.93) | POSITIVE (1.00) | POSITIVE → POSITIVE | +6.8 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_7d98`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_7bb9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c7e3`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_b6da`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_9953`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_2dd2`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_6cbf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7d98` | NEGATION_PREFIX | "the sun rises in east and..." → "It is not true that the s..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | NEGATIVE (0.93) | POSITIVE → NEGATIVE | -5.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_7bb9` | DOUBLE_NEGATION | "the sun rises in east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.95) | POSITIVE → POSITIVE | -4.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_c7e3` | INTENSITY | "the sun rises in east and..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b6da` | INTENSITY | "the sun rises in east and..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -1.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9953` | SYNONYM_SUBSTITUTION | "the sun rises in east and..." → "the insolate rises in eas..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.53) | POSITIVE → POSITIVE | -45.4 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_2dd2` | CONTRAST_NEGATIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | -0.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_6cbf` | CONTRAST_POSITIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +1.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_7d98`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_7bb9`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.
- **`prb_c7e3`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_b6da`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **`prb_9953`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 45.44 percentage points under meaning-preserving perturbation.
- **`prb_2dd2`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_6cbf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7d98` | NEGATION_PREFIX | "the sun rises in east and..." → "It is not true that the s..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.92) | NEUTRAL (0.78) | NEUTRAL → NEUTRAL | -14.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_7bb9` | DOUBLE_NEGATION | "the sun rises in east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.92) | NEUTRAL (0.73) | NEUTRAL → NEUTRAL | -19.2 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_c7e3` | INTENSITY | "the sun rises in east and..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.92) | NEUTRAL (0.92) | NEUTRAL → NEUTRAL | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b6da` | INTENSITY | "the sun rises in east and..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.92) | NEUTRAL (0.93) | NEUTRAL → NEUTRAL | +0.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9953` | SYNONYM_SUBSTITUTION | "the sun rises in east and..." → "the insolate rises in eas..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.92) | NEUTRAL (0.93) | NEUTRAL → NEUTRAL | +0.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2dd2` | CONTRAST_NEGATIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.92) | NEUTRAL (0.95) | NEUTRAL → NEUTRAL | +2.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_6cbf` | CONTRAST_POSITIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.92) | POSITIVE (0.86) | NEUTRAL → POSITIVE | -6.5 | YES | `UNEXPECTED_CHANGE` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_7d98`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_7bb9`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 19.19 percentage points under meaning-preserving perturbation.
- **`prb_c7e3`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_b6da`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_9953`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_2dd2`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_6cbf`** [Spurious / UNEXPECTED_CHANGE]: The perturbation is meaning-preserving (PRESERVE_MEANING), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_7d98` | NEGATION_PREFIX | "the sun rises in east and..." → "It is not true that the s..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.61) | NEUTRAL (0.49) | NEUTRAL → NEUTRAL | -12.5 | NO | `MISSING_FLIP` | **Blind** |
| `prb_7bb9` | DOUBLE_NEGATION | "the sun rises in east and..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.61) | POSITIVE (0.75) | NEUTRAL → POSITIVE | +13.8 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_c7e3` | INTENSITY | "the sun rises in east and..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.61) | NEUTRAL (0.62) | NEUTRAL → NEUTRAL | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b6da` | INTENSITY | "the sun rises in east and..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.61) | NEUTRAL (0.68) | NEUTRAL → NEUTRAL | +7.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9953` | SYNONYM_SUBSTITUTION | "the sun rises in east and..." → "the insolate rises in eas..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.61) | NEUTRAL (0.82) | NEUTRAL → NEUTRAL | +20.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_2dd2` | CONTRAST_NEGATIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.61) | NEUTRAL (0.79) | NEUTRAL → NEUTRAL | +17.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_6cbf` | CONTRAST_POSITIVE_APPEND | "the sun rises in east and..." → "the sun rises in east and..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.61) | POSITIVE (0.93) | NEUTRAL → POSITIVE | +31.2 | YES | `UNEXPECTED_CHANGE` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_7d98`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_7bb9`** [Spurious / UNEXPECTED_CHANGE]: The perturbation is meaning-preserving (PRESERVE_MEANING), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **`prb_c7e3`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_b6da`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_9953`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_2dd2`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_6cbf`** [Spurious / UNEXPECTED_CHANGE]: The perturbation is meaning-preserving (PRESERVE_MEANING), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).