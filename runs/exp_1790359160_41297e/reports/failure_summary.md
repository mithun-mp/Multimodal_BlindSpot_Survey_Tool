# Behavioral Failure Diagnoses: Multimodel Robustness Audit 003

**Experiment ID**: `exp_1790359160_41297e`
**Total Diagnosed Failures**: 3

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_f8cfe5bc91e4` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.63)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_063fe37511e1` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.42)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.
