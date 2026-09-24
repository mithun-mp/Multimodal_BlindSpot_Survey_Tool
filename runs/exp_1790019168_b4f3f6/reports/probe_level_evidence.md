# Probe-Level Behavioral Evidence: Multimodel Robustness Audit002

**Experiment ID**: `exp_1790019168_b4f3f6`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d6ee` | NEGATION_REMOVAL | "All Glitters are not Gold..." → "All Glitters are Gold..." | NEGATIVE (1.00) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +0.1 | YES | `EXPECTED_FLIP` | **None** |
| `prb_131f` | DOUBLE_NEGATION | "All Glitters are not Gold..." → "All Glitters are not enti..." | NEGATIVE (1.00) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -2.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7140` | INTENSITY | "All Glitters are not Gold..." → "All Glitters extremely ar..." | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_781b` | INTENSITY | "All Glitters are not Gold..." → "All Glitters somewhat are..." | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e933` | SYNONYM_SUBSTITUTION | "All Glitters are not Gold..." → "Entirely Glitters are not..." | NEGATIVE (1.00) | NEGATIVE (0.99) | NEGATIVE → NEGATIVE | -0.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_38bf` | CONTRAST_NEGATIVE_APPEND | "All Glitters are not Gold..." → "All Glitters are not Gold..." | NEGATIVE (1.00) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -1.9 | NO | `MISSING_FLIP` | **Blind** |
| `prb_9f9e` | STRUCTURE | "All Glitters are not Gold..." → "In fact, all Glitters are..." | NEGATIVE (1.00) | NEGATIVE (1.00) | NEGATIVE → NEGATIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d6ee`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEGATIVE → POSITIVE under REVERSE_POLARITY.
- **`prb_131f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_7140`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_781b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_e933`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_38bf`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_9f9e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d6ee` | NEGATION_REMOVAL | "All Glitters are not Gold..." → "All Glitters are Gold..." | NEGATIVE (0.94) | POSITIVE (0.99) | NEGATIVE → POSITIVE | +4.9 | YES | `EXPECTED_FLIP` | **None** |
| `prb_131f` | DOUBLE_NEGATION | "All Glitters are not Gold..." → "All Glitters are not enti..." | NEGATIVE (0.94) | POSITIVE (0.94) | NEGATIVE → POSITIVE | +0.2 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_7140` | INTENSITY | "All Glitters are not Gold..." → "All Glitters extremely ar..." | NEGATIVE (0.94) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | +3.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_781b` | INTENSITY | "All Glitters are not Gold..." → "All Glitters somewhat are..." | NEGATIVE (0.94) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | +3.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e933` | SYNONYM_SUBSTITUTION | "All Glitters are not Gold..." → "Entirely Glitters are not..." | NEGATIVE (0.94) | NEGATIVE (0.96) | NEGATIVE → NEGATIVE | +2.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_38bf` | CONTRAST_NEGATIVE_APPEND | "All Glitters are not Gold..." → "All Glitters are not Gold..." | NEGATIVE (0.94) | POSITIVE (0.55) | NEGATIVE → POSITIVE | -39.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_9f9e` | STRUCTURE | "All Glitters are not Gold..." → "In fact, all Glitters are..." | NEGATIVE (0.94) | NEGATIVE (0.97) | NEGATIVE → NEGATIVE | +3.2 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d6ee`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEGATIVE → POSITIVE under REVERSE_POLARITY.
- **`prb_131f`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **`prb_7140`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_781b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_e933`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_38bf`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEGATIVE → POSITIVE under SHIFT_CONTRAST.
- **`prb_9f9e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d6ee` | NEGATION_REMOVAL | "All Glitters are not Gold..." → "All Glitters are Gold..." | NEGATIVE (0.99) | POSITIVE (1.00) | NEGATIVE → POSITIVE | +1.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_131f` | DOUBLE_NEGATION | "All Glitters are not Gold..." → "All Glitters are not enti..." | NEGATIVE (0.99) | POSITIVE (0.89) | NEGATIVE → POSITIVE | -9.2 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_7140` | INTENSITY | "All Glitters are not Gold..." → "All Glitters extremely ar..." | NEGATIVE (0.99) | NEGATIVE (0.94) | NEGATIVE → NEGATIVE | -4.8 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_781b` | INTENSITY | "All Glitters are not Gold..." → "All Glitters somewhat are..." | NEGATIVE (0.99) | NEGATIVE (0.93) | NEGATIVE → NEGATIVE | -5.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e933` | SYNONYM_SUBSTITUTION | "All Glitters are not Gold..." → "Entirely Glitters are not..." | NEGATIVE (0.99) | NEGATIVE (0.87) | NEGATIVE → NEGATIVE | -12.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_38bf` | CONTRAST_NEGATIVE_APPEND | "All Glitters are not Gold..." → "All Glitters are not Gold..." | NEGATIVE (0.99) | NEGATIVE (0.95) | NEGATIVE → NEGATIVE | -3.2 | NO | `MISSING_FLIP` | **Blind** |
| `prb_9f9e` | STRUCTURE | "All Glitters are not Gold..." → "In fact, all Glitters are..." | NEGATIVE (0.99) | NEGATIVE (0.98) | NEGATIVE → NEGATIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d6ee`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEGATIVE → POSITIVE under REVERSE_POLARITY.
- **`prb_131f`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **`prb_7140`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_781b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_e933`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_38bf`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_9f9e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d6ee` | NEGATION_REMOVAL | "All Glitters are not Gold..." → "All Glitters are Gold..." | NEUTRAL (0.55) | POSITIVE (0.75) | NEUTRAL → POSITIVE | +20.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_131f` | DOUBLE_NEGATION | "All Glitters are not Gold..." → "All Glitters are not enti..." | NEUTRAL (0.55) | NEUTRAL (0.77) | NEUTRAL → NEUTRAL | +21.4 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_7140` | INTENSITY | "All Glitters are not Gold..." → "All Glitters extremely ar..." | NEUTRAL (0.55) | NEGATIVE (0.53) | NEUTRAL → NEGATIVE | -1.7 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_781b` | INTENSITY | "All Glitters are not Gold..." → "All Glitters somewhat are..." | NEUTRAL (0.55) | NEUTRAL (0.60) | NEUTRAL → NEUTRAL | +5.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_e933` | SYNONYM_SUBSTITUTION | "All Glitters are not Gold..." → "Entirely Glitters are not..." | NEUTRAL (0.55) | NEGATIVE (0.52) | NEUTRAL → NEGATIVE | -3.3 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_38bf` | CONTRAST_NEGATIVE_APPEND | "All Glitters are not Gold..." → "All Glitters are not Gold..." | NEUTRAL (0.55) | NEUTRAL (0.61) | NEUTRAL → NEUTRAL | +5.9 | NO | `MISSING_FLIP` | **Blind** |
| `prb_9f9e` | STRUCTURE | "All Glitters are not Gold..." → "In fact, all Glitters are..." | NEUTRAL (0.55) | NEUTRAL (0.49) | NEUTRAL → NEUTRAL | -6.6 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_d6ee`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEUTRAL → POSITIVE under REVERSE_POLARITY.
- **`prb_131f`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_7140`** [Misweighted / UNEXPECTED_FLIP]: Model inverted prediction (NEUTRAL → NEGATIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **`prb_781b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.
- **`prb_e933`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → NEGATIVE).
- **`prb_38bf`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **`prb_9f9e`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEUTRAL → NEUTRAL) under meaning-preserving perturbation.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_d6ee` | NEGATION_REMOVAL | "All Glitters are not Gold..." → "All Glitters are Gold..." | NEGATIVE (0.52) | POSITIVE (0.73) | NEGATIVE → POSITIVE | +20.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_131f` | DOUBLE_NEGATION | "All Glitters are not Gold..." → "All Glitters are not enti..." | NEGATIVE (0.52) | NEUTRAL (0.85) | NEGATIVE → NEUTRAL | +32.6 | YES | `UNEXPECTED_FLIP` | **Spurious** |
| `prb_7140` | INTENSITY | "All Glitters are not Gold..." → "All Glitters extremely ar..." | NEGATIVE (0.52) | NEGATIVE (0.60) | NEGATIVE → NEGATIVE | +8.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_781b` | INTENSITY | "All Glitters are not Gold..." → "All Glitters somewhat are..." | NEGATIVE (0.52) | NEUTRAL (0.55) | NEGATIVE → NEUTRAL | +2.5 | YES | `UNEXPECTED_FLIP` | **Misweighted** |
| `prb_e933` | SYNONYM_SUBSTITUTION | "All Glitters are not Gold..." → "Entirely Glitters are not..." | NEGATIVE (0.52) | NEGATIVE (0.66) | NEGATIVE → NEGATIVE | +14.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_38bf` | CONTRAST_NEGATIVE_APPEND | "All Glitters are not Gold..." → "All Glitters are not Gold..." | NEGATIVE (0.52) | NEGATIVE (0.70) | NEGATIVE → NEGATIVE | +17.9 | NO | `MISSING_FLIP` | **Blind** |
| `prb_9f9e` | STRUCTURE | "All Glitters are not Gold..." → "In fact, all Glitters are..." | NEGATIVE (0.52) | NEUTRAL (0.50) | NEGATIVE → NEUTRAL | -1.9 | YES | `UNEXPECTED_FLIP` | **Spurious** |

### Probe Rationales & Evidence Notes
- **`prb_d6ee`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from NEGATIVE → POSITIVE under REVERSE_POLARITY.
- **`prb_131f`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → NEUTRAL).
- **`prb_7140`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_781b`** [Misweighted / UNEXPECTED_FLIP]: Model inverted prediction (NEGATIVE → NEUTRAL) when presented with a degree modifier (WEAKEN_POLARITY), indicating disproportionately skewed feature weighting.
- **`prb_e933`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (NEGATIVE → NEGATIVE) under meaning-preserving perturbation.
- **`prb_38bf`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **`prb_9f9e`** [Spurious / UNEXPECTED_FLIP]: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → NEUTRAL).