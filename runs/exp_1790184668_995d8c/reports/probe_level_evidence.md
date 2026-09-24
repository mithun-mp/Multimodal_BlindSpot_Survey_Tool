# Probe-Level Behavioral Evidence: Multimodel00002

**Experiment ID**: `exp_1790184668_995d8c`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d97f` | NEGATION_INSERTION | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9afd` | DOUBLE_NEGATION | "the way he talked to me w..." → "It is not impossible that..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0c2` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d71c` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_302f` | SYNONYM_SUBSTITUTION | "the way he talked to me w..." → "the style he talked to me..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7f63` | CONTRAST_NEGATIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -1.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_eb6c` | CONTRAST_POSITIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d97f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_9afd`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_b0c2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_d71c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_302f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_7f63`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under SHIFT_CONTRAST.
- **`prb_eb6c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d97f` | NEGATION_INSERTION | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.73) | POSITIVE → POSITIVE | -25.2 | NO | `MISSING_FLIP` | **Blind** |
| `prb_9afd` | DOUBLE_NEGATION | "the way he talked to me w..." → "It is not impossible that..." | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0c2` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d71c` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_302f` | SYNONYM_SUBSTITUTION | "the way he talked to me w..." → "the style he talked to me..." | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7f63` | CONTRAST_NEGATIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.91) | POSITIVE → POSITIVE | -7.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_eb6c` | CONTRAST_POSITIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d97f`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_9afd`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_b0c2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_d71c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_302f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_7f63`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_eb6c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d97f` | NEGATION_INSERTION | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | NEUTRAL (0.38) | POSITIVE → NEUTRAL | -60.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9afd` | DOUBLE_NEGATION | "the way he talked to me w..." → "It is not impossible that..." | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0c2` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d71c` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_302f` | SYNONYM_SUBSTITUTION | "the way he talked to me w..." → "the style he talked to me..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7f63` | CONTRAST_NEGATIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.92) | POSITIVE → POSITIVE | -6.7 | NO | `MISSING_FLIP` | **Blind** |
| `prb_eb6c` | CONTRAST_POSITIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d97f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEUTRAL under REVERSE_POLARITY.
- **`prb_9afd`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_b0c2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_d71c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_302f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_7f63`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_eb6c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d97f` | NEGATION_INSERTION | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | -1.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9afd` | DOUBLE_NEGATION | "the way he talked to me w..." → "It is not impossible that..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0c2` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d71c` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_302f` | SYNONYM_SUBSTITUTION | "the way he talked to me w..." → "the style he talked to me..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7f63` | CONTRAST_NEGATIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | NEGATIVE (0.71) | POSITIVE → NEGATIVE | -29.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_eb6c` | CONTRAST_POSITIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d97f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_9afd`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_b0c2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_d71c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_302f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_7f63`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under SHIFT_CONTRAST.
- **`prb_eb6c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d97f` | NEGATION_INSERTION | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9afd` | DOUBLE_NEGATION | "the way he talked to me w..." → "It is not impossible that..." | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -1.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_b0c2` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_d71c` | INTENSITY | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_302f` | SYNONYM_SUBSTITUTION | "the way he talked to me w..." → "the style he talked to me..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7f63` | CONTRAST_NEGATIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | +0.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_eb6c` | CONTRAST_POSITIVE_APPEND | "the way he talked to me w..." → "the way he talked to me w..." | POSITIVE (0.99) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.5 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d97f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_9afd`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_b0c2`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_d71c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_302f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_7f63`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under SHIFT_CONTRAST.
- **`prb_eb6c`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.