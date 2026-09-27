# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790551468_b787ce`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c8c1` | NEGATION_REMOVAL | "i am not well..." → "i am well..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (1.00) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +0.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9936` | DOUBLE_NEGATION | "i am not well..." → "i am not entirely non-wel..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5fee` | INTENSITY | "i am not well..." → "i am extremely not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_fd37` | INTENSITY | "i am not well..." → "i am somewhat not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5976` | SYNONYM_SUBSTITUTION | "i am not well..." → "i am non well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_45d5` | CONTRAST_NEGATIVE_APPEND | "i am not well..." → "i am not well, however I ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -2.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_3bd1` | CONTRAST_POSITIVE_APPEND | "i am not well..." → "i am not well, and I disp..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (1.00) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +0.0 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c8c1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.
- **`prb_9936`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_5fee`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_fd37`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_5976`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_45d5`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_3bd1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c8c1` | NEGATION_REMOVAL | "i am not well..." → "i am well..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (0.57) | POSITIVE (0.70) | NEGATIVE → POSITIVE | +13.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9936` | DOUBLE_NEGATION | "i am not well..." → "i am not entirely non-wel..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.57) | NEUTRAL (0.54) | NEGATIVE → NEUTRAL | -3.3 | NO | `EXPECTED_FLIP` | **None** |
| `prb_5fee` | INTENSITY | "i am not well..." → "i am extremely not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.57) | NEGATIVE (0.84) | NEGATIVE → NEGATIVE | +26.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_fd37` | INTENSITY | "i am not well..." → "i am somewhat not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.57) | NEGATIVE (0.76) | NEGATIVE → NEGATIVE | +18.7 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_5976` | SYNONYM_SUBSTITUTION | "i am not well..." → "i am non well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.57) | NEUTRAL (0.66) | NEGATIVE → NEUTRAL | +8.5 | NO | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_45d5` | CONTRAST_NEGATIVE_APPEND | "i am not well..." → "i am not well, however I ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.57) | NEGATIVE (0.89) | NEGATIVE → NEGATIVE | +31.5 | NO | `MISSING_FLIP` | **Blind** |
| `prb_3bd1` | CONTRAST_POSITIVE_APPEND | "i am not well..." → "i am not well, and I disp..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (0.57) | NEUTRAL (0.43) | NEGATIVE → NEUTRAL | -13.9 | NO | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c8c1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.
- **`prb_9936`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → NEUTRAL (NEUTRAL)) under DIFFERENT_LABEL expectation.
- **`prb_5fee`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_fd37`** [Misweighted / EXPECTED_PRESERVE]: Downtoner caused confidence to surge: confidence increased by 18.73 percentage points (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_5976`** [Spurious / UNEXPECTED_CHANGE]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → NEUTRAL (NEUTRAL)).
- **`prb_45d5`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_3bd1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → NEUTRAL (NEUTRAL)) under DIFFERENT_LABEL expectation.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c8c1` | NEGATION_REMOVAL | "i am not well..." → "i am well..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (0.93) | POSITIVE (0.80) | NEGATIVE → POSITIVE | -12.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9936` | DOUBLE_NEGATION | "i am not well..." → "i am not entirely non-wel..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.93) | NEUTRAL (0.51) | NEGATIVE → NEUTRAL | -42.0 | NO | `EXPECTED_FLIP` | **None** |
| `prb_5fee` | INTENSITY | "i am not well..." → "i am extremely not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.93) | NEGATIVE (0.96) | NEGATIVE → NEGATIVE | +3.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_fd37` | INTENSITY | "i am not well..." → "i am somewhat not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.93) | NEGATIVE (0.90) | NEGATIVE → NEGATIVE | -3.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5976` | SYNONYM_SUBSTITUTION | "i am not well..." → "i am non well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.93) | NEGATIVE (0.87) | NEGATIVE → NEGATIVE | -5.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_45d5` | CONTRAST_NEGATIVE_APPEND | "i am not well..." → "i am not well, however I ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.93) | NEGATIVE (0.96) | NEGATIVE → NEGATIVE | +3.2 | NO | `MISSING_FLIP` | **Blind** |
| `prb_3bd1` | CONTRAST_POSITIVE_APPEND | "i am not well..." → "i am not well, and I disp..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (0.93) | POSITIVE (0.44) | NEGATIVE → POSITIVE | -48.7 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c8c1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.
- **`prb_9936`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → NEUTRAL (NEUTRAL)) under DIFFERENT_LABEL expectation.
- **`prb_5fee`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_fd37`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_5976`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_45d5`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_3bd1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c8c1` | NEGATION_REMOVAL | "i am not well..." → "i am well..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (0.99) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +0.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9936` | DOUBLE_NEGATION | "i am not well..." → "i am not entirely non-wel..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (0.99) | NEGATIVE (0.64) | NEGATIVE → NEGATIVE | -35.7 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_5fee` | INTENSITY | "i am not well..." → "i am extremely not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_fd37` | INTENSITY | "i am not well..." → "i am somewhat not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5976` | SYNONYM_SUBSTITUTION | "i am not well..." → "i am non well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.81) | NEGATIVE → NEGATIVE | -18.4 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_45d5` | CONTRAST_NEGATIVE_APPEND | "i am not well..." → "i am not well, however I ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (0.99) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | -2.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_3bd1` | CONTRAST_POSITIVE_APPEND | "i am not well..." → "i am not well, and I disp..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (0.99) | POSITIVE (0.98) | NEGATIVE → POSITIVE | -1.6 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c8c1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.
- **`prb_9936`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 35.69 percentage points under meaning-preserving perturbation.
- **`prb_5fee`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_fd37`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_5976`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 18.41 percentage points under meaning-preserving perturbation.
- **`prb_45d5`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_3bd1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_c8c1` | NEGATION_REMOVAL | "i am not well..." → "i am well..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (1.00) | POSITIVE (0.99) | NEGATIVE → POSITIVE | -0.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9936` | DOUBLE_NEGATION | "i am not well..." → "i am not entirely non-wel..." | `NEUTRAL (SHIFT_TO_NEUTRAL)` | NEGATIVE (1.00) | NEGATIVE (0.90) | NEGATIVE → NEGATIVE | -9.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5fee` | INTENSITY | "i am not well..." → "i am extremely not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_fd37` | INTENSITY | "i am not well..." → "i am somewhat not well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_5976` | SYNONYM_SUBSTITUTION | "i am not well..." → "i am non well..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_45d5` | CONTRAST_NEGATIVE_APPEND | "i am not well..." → "i am not well, however I ..." | `NEGATIVE (PRESERVE_POLARITY)` | NEGATIVE (1.00) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -2.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_3bd1` | CONTRAST_POSITIVE_APPEND | "i am not well..." → "i am not well, and I disp..." | `POSITIVE (REVERSE_POLARITY)` | NEGATIVE (1.00) | POSITIVE (0.64) | NEGATIVE → POSITIVE | -35.7 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_c8c1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.
- **`prb_9936`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_5fee`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_fd37`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_5976`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)) under meaning-preserving probe.
- **`prb_45d5`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **`prb_3bd1`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEGATIVE (NEGATIVE) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.