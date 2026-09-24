# Probe-Level Behavioral Evidence: Multimodel Robustness Audit

**Experiment ID**: `exp_1790180229_bc0799`
Detailed probe-level records establishing full observable evidence for behavioral outcomes and failure classifications.


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