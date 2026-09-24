# Probe-Level Behavioral Evidence: Multimodel 0100

**Experiment ID**: `exp_1790188010_0408e9`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


## Model: `distilbert-base-uncased-finetuned-sst-2-english`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_f8cf` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | POSITIVE (1.00) | POSITIVE (0.99) | POSITIVE → POSITIVE | -1.4 | NO | `MISSING_FLIP` | **Blind** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (1.00) | NEGATIVE (1.00) | POSITIVE → NEGATIVE | -0.3 | YES | `EXPECTED_FLIP` | **None** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_f8cf`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_063f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under SHIFT_CONTRAST.
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `twitter-roberta-base-sentiment-latest`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_f8cf` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | POSITIVE (0.99) | NEGATIVE (0.80) | POSITIVE → NEGATIVE | -19.0 | YES | `EXPECTED_FLIP` | **None** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -1.9 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | -0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (0.99) | POSITIVE (0.63) | POSITIVE → POSITIVE | -36.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_f8cf`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_063f`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `twitter-roberta-base-sentiment`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_f8cf` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | POSITIVE (0.99) | NEGATIVE (0.91) | POSITIVE → NEGATIVE | -7.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | POSITIVE (0.99) | POSITIVE (0.97) | POSITIVE → POSITIVE | -2.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.2 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | POSITIVE (0.99) | POSITIVE (0.98) | POSITIVE → POSITIVE | -0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (0.99) | POSITIVE (0.42) | POSITIVE → POSITIVE | -57.1 | NO | `MISSING_FLIP` | **Blind** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (0.99) | POSITIVE (0.99) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_f8cf`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_063f`** [Blind / MISSING_FLIP]: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `albert-base-v2-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_f8cf` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | POSITIVE (1.00) | NEGATIVE (0.99) | POSITIVE → NEGATIVE | -0.5 | YES | `EXPECTED_FLIP` | **None** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | POSITIVE (1.00) | POSITIVE (0.95) | POSITIVE → POSITIVE | -4.7 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.1 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (1.00) | NEGATIVE (0.98) | POSITIVE → NEGATIVE | -1.4 | YES | `EXPECTED_FLIP` | **None** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.3 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_f8cf`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_063f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under SHIFT_CONTRAST.
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.

## Model: `bert-base-uncased-SST-2`

| Probe ID | Category | Original → Perturbed | Baseline | Probe Output | Transition | Δ Conf (pp) | Flip | Outcome | Failure |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `prb_f8cf` | NEGATION_INSERTION | "The movie was great and t..." → "The movie was not great a..." | POSITIVE (1.00) | NEGATIVE (0.73) | POSITIVE → NEGATIVE | -27.2 | YES | `EXPECTED_FLIP` | **None** |
| `prb_93a8` | DOUBLE_NEGATION | "The movie was great and t..." → "It is not impossible that..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_655b` | INTENSITY | "The movie was great and t..." → "The movie was extremely g..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_ad69` | INTENSITY | "The movie was great and t..." → "The movie was somewhat gr..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_0bcf` | SYNONYM_SUBSTITUTION | "The movie was great and t..." → "The film was great and th..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | -0.0 | NO | `EXPECTED_PRESERVE` | **None** |
| `prb_063f` | CONTRAST_NEGATIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (1.00) | NEGATIVE (0.87) | POSITIVE → NEGATIVE | -12.8 | YES | `EXPECTED_FLIP` | **None** |
| `prb_1fa8` | CONTRAST_POSITIVE_APPEND | "The movie was great and t..." → "The movie was great and t..." | POSITIVE (1.00) | POSITIVE (1.00) | POSITIVE → POSITIVE | +0.0 | NO | `EXPECTED_PRESERVE` | **None** |

### Probe Rationales & Evidence Notes
- **`prb_f8cf`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under REVERSE_POLARITY.
- **`prb_93a8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_655b`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_ad69`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_0bcf`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.
- **`prb_063f`** [None / EXPECTED_FLIP]: Model correctly flipped prediction from POSITIVE → NEGATIVE under SHIFT_CONTRAST.
- **`prb_1fa8`** [None / EXPECTED_PRESERVE]: Model correctly preserved prediction class (POSITIVE → POSITIVE) under meaning-preserving perturbation.