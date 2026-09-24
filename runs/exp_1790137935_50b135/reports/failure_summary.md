# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790137935_50b135`
**Total Diagnosed Failures**: 4

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_8ecd031cfa51` (N/A)
- **Original Input**: "The film was amazing,me and family enjoyed it well"
- **Perturbed Input**: "The film was not amazing,me and family enjoyed it well"
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_aa4499ef9818` (N/A)
- **Original Input**: "The film was amazing,me and family enjoyed it well"
- **Perturbed Input**: "The film was amazing,me and family enjoyed it well, however it was surprisingly unimpressive in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.97)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_8ecd031cfa51` (N/A)
- **Original Input**: "The film was amazing,me and family enjoyed it well"
- **Perturbed Input**: "The film was not amazing,me and family enjoyed it well"
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.98)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #4: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_aa4499ef9818` (N/A)
- **Original Input**: "The film was amazing,me and family enjoyed it well"
- **Perturbed Input**: "The film was amazing,me and family enjoyed it well, however it was surprisingly unimpressive in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.97)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.
