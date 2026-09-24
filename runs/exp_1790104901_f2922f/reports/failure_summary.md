# Behavioral Failure Diagnoses: Multimodel 003

**Experiment ID**: `exp_1790104901_f2922f`
**Total Diagnosed Failures**: 9

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_a6425d7f08c0` (N/A)
- **Original Input**: "I am healthy But still hospitalized"
- **Perturbed Input**: "I am not healthy But still hospitalized"
- **Observed Transition**: `NEGATIVE (0.86)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_f60ef40b5902` (N/A)
- **Original Input**: "I am healthy But still hospitalized"
- **Perturbed Input**: "I am healthy But still hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.86)` → `NEGATIVE (0.71)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_a6425d7f08c0` (N/A)
- **Original Input**: "I am healthy But still hospitalized"
- **Perturbed Input**: "I am not healthy But still hospitalized"
- **Observed Transition**: `NEGATIVE (0.63)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #4: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_f60ef40b5902` (N/A)
- **Original Input**: "I am healthy But still hospitalized"
- **Perturbed Input**: "I am healthy But still hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.63)` → `NEGATIVE (0.56)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #5: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_a6425d7f08c0` (N/A)
- **Original Input**: "I am healthy But still hospitalized"
- **Perturbed Input**: "I am not healthy But still hospitalized"
- **Observed Transition**: `NEGATIVE (0.82)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #6: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_f60ef40b5902` (N/A)
- **Original Input**: "I am healthy But still hospitalized"
- **Perturbed Input**: "I am healthy But still hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.82)` → `NEGATIVE (0.61)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #7: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_e6a55be8b972` (N/A)
- **Original Input**: "I am healthy But still hospitalized"
- **Perturbed Input**: "In fact, i am healthy But still hospitalized"
- **Observed Transition**: `NEGATIVE (0.82)` → `POSITIVE (0.61)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against structure perturbations to fix Spurious failures.

### Failure #8: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_1b690ad14693` (N/A)
- **Original Input**: "I am healthy But still hospitalized"
- **Perturbed Input**: "I am extremely healthy But still hospitalized"
- **Observed Transition**: `NEUTRAL (0.66)` → `POSITIVE (0.69)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Evidence**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #9: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_e6a55be8b972` (N/A)
- **Original Input**: "I am healthy But still hospitalized"
- **Perturbed Input**: "In fact, i am healthy But still hospitalized"
- **Observed Transition**: `NEUTRAL (0.66)` → `POSITIVE (0.53)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against structure perturbations to fix Spurious failures.
