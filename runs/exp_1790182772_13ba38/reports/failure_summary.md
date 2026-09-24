# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790182772_13ba38`
**Total Diagnosed Failures**: 3

### Failure #1: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_d97f2ee9eebc` (N/A)
- **Original Input**: "the way he talked to me was amazing i was in love with his voice"
- **Perturbed Input**: "the way he talked to me was not amazing i was in love with his voice"
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.73)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_7f63c77edd80` (N/A)
- **Original Input**: "the way he talked to me was amazing i was in love with his voice"
- **Perturbed Input**: "the way he talked to me was amazing i was in love with his voice, however it was surprisingly unimpressive in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.91)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_7f63c77edd80` (N/A)
- **Original Input**: "the way he talked to me was amazing i was in love with his voice"
- **Perturbed Input**: "the way he talked to me was amazing i was in love with his voice, however it was surprisingly unimpressive in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.92)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.
