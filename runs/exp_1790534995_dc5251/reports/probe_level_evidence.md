# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790534995_dc5251`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_db77` | NEGATION_PREFIX | "the sun rises in the east..." → "It is not true that the s..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_5038` | DOUBLE_NEGATION | "the sun rises in the east..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_fc9a` | INTENSITY | "the sun rises in the east..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8472` | INTENSITY | "the sun rises in the east..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4a33` | SYNONYM_SUBSTITUTION | "the sun rises in the east..." → "the sunlight rises in the..." | `NEUTRAL (PRESERVE)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9200` | CONTRAST_NEGATIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.7 | YES | `EXPECTED_FLIP` | **None** |
| `prb_d265` | CONTRAST_POSITIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_db77`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_5038`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_fc9a`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_8472`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_4a33`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_9200`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_d265`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_db77` | NEGATION_PREFIX | "the sun rises in the east..." → "It is not true that the s..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (0.94) | NEGATIVE (0.93) | POSITIVE → NEGATIVE | -0.7 | YES | `EXPECTED_FLIP` | **None** |
| `prb_5038` | DOUBLE_NEGATION | "the sun rises in the east..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.94) | POSITIVE (0.93) | POSITIVE → POSITIVE | -1.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_fc9a` | INTENSITY | "the sun rises in the east..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.94) | POSITIVE (0.97) | POSITIVE → POSITIVE | +3.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8472` | INTENSITY | "the sun rises in the east..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.94) | POSITIVE (0.92) | POSITIVE → POSITIVE | -2.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4a33` | SYNONYM_SUBSTITUTION | "the sun rises in the east..." → "the sunlight rises in the..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.94) | POSITIVE (0.94) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9200` | CONTRAST_NEGATIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (0.94) | NEGATIVE (0.95) | POSITIVE → NEGATIVE | +1.6 | YES | `EXPECTED_FLIP` | **None** |
| `prb_d265` | CONTRAST_POSITIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (0.94) | POSITIVE (1.00) | POSITIVE → POSITIVE | +6.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_db77`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_5038`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_fc9a`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_8472`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_4a33`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_9200`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_d265`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_db77` | NEGATION_PREFIX | "the sun rises in the east..." → "It is not true that the s..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (0.99) | NEGATIVE (0.92) | POSITIVE → NEGATIVE | -7.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_5038` | DOUBLE_NEGATION | "the sun rises in the east..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.95) | POSITIVE → POSITIVE | -4.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_fc9a` | INTENSITY | "the sun rises in the east..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8472` | INTENSITY | "the sun rises in the east..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -2.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4a33` | SYNONYM_SUBSTITUTION | "the sun rises in the east..." → "the sunlight rises in the..." | `NEUTRAL (PRESERVE)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9200` | CONTRAST_NEGATIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (0.99) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | -0.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_d265` | CONTRAST_POSITIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.9 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_db77`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_5038`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_fc9a`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_8472`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_4a33`** [None / EXPECTED_PRESERVE]: Binary forced-polarity output preserved (POSITIVE → POSITIVE) under neutral reference probe.
- **`prb_9200`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (POSITIVE (POSITIVE) → NEGATIVE (NEGATIVE)) under DIFFERENT_LABEL expectation.
- **`prb_d265`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)) under meaning-preserving probe.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_db77` | NEGATION_PREFIX | "the sun rises in the east..." → "It is not true that the s..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.93) | NEUTRAL (0.79) | NEUTRAL → NEUTRAL | -13.3 | NO | `MISSING_FLIP` | **Blind** |
| `prb_5038` | DOUBLE_NEGATION | "the sun rises in the east..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.93) | NEUTRAL (0.74) | NEUTRAL → NEUTRAL | -18.8 | NO | `EXPECTED_PRESERVE` | **Misweighted** |
| `prb_fc9a` | INTENSITY | "the sun rises in the east..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.93) | NEUTRAL (0.92) | NEUTRAL → NEUTRAL | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8472` | INTENSITY | "the sun rises in the east..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.93) | NEUTRAL (0.93) | NEUTRAL → NEUTRAL | +0.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4a33` | SYNONYM_SUBSTITUTION | "the sun rises in the east..." → "the sunlight rises in the..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.93) | NEUTRAL (0.92) | NEUTRAL → NEUTRAL | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9200` | CONTRAST_NEGATIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.93) | NEUTRAL (0.95) | NEUTRAL → NEUTRAL | +2.2 | NO | `MISSING_FLIP` | **Blind** |
| `prb_d265` | CONTRAST_POSITIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.93) | POSITIVE (0.85) | NEUTRAL → POSITIVE | -7.4 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_db77`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_5038`** [Misweighted / EXPECTED_PRESERVE]: Polarity preserved, but confidence collapsed by 18.80 percentage points under meaning-preserving perturbation.
- **`prb_fc9a`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_8472`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_4a33`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_9200`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_d265`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Semantic Ref | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_db77` | NEGATION_PREFIX | "the sun rises in the east..." → "It is not true that the s..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.58) | NEUTRAL (0.49) | NEUTRAL → NEUTRAL | -9.6 | NO | `MISSING_FLIP` | **Blind** |
| `prb_5038` | DOUBLE_NEGATION | "the sun rises in the east..." → "It is not impossible that..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.58) | POSITIVE (0.76) | NEUTRAL → POSITIVE | +18.3 | YES | `UNEXPECTED_CHANGE` | **Spurious** |
| `prb_fc9a` | INTENSITY | "the sun rises in the east..." → "the sun extremely rises i..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.58) | NEUTRAL (0.58) | NEUTRAL → NEUTRAL | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_8472` | INTENSITY | "the sun rises in the east..." → "the sun somewhat rises in..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.58) | NEUTRAL (0.68) | NEUTRAL → NEUTRAL | +10.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_4a33` | SYNONYM_SUBSTITUTION | "the sun rises in the east..." → "the sunlight rises in the..." | `NEUTRAL (PRESERVE)` | NEUTRAL (0.58) | NEUTRAL (0.69) | NEUTRAL → NEUTRAL | +11.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_9200` | CONTRAST_NEGATIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `NEGATIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.58) | NEUTRAL (0.78) | NEUTRAL → NEUTRAL | +20.4 | NO | `MISSING_FLIP` | **Blind** |
| `prb_d265` | CONTRAST_POSITIVE_APPEND | "the sun rises in the east..." → "the sun rises in the east..." | `POSITIVE (SHIFT_FROM_NEUTRAL)` | NEUTRAL (0.58) | POSITIVE (0.93) | NEUTRAL → POSITIVE | +35.0 | YES | `EXPECTED_FLIP` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_db77`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_5038`** [Spurious / UNEXPECTED_CHANGE]: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **`prb_fc9a`** [None / EXPECTED_PRESERVE]: Intensifier preserved polarity.
- **`prb_8472`** [None / EXPECTED_PRESERVE]: Downtoner preserved polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_4a33`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)) under meaning-preserving probe.
- **`prb_9200`** [Blind / MISSING_FLIP]: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **`prb_d265`** [None / EXPECTED_FLIP]: Model correctly flipped and changed label (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)) under DIFFERENT_LABEL expectation.