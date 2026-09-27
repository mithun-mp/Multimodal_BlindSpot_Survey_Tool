# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790528043_5b3eeb`
**Total Diagnosed Failures**: 3

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_6018c6f404b7` (N/A)
- **Original Input**: "the movie was great and the acting was top notch"
- **Perturbed Input**: "the movie was not great and the acting was top notch"
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.66)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_eea001d5b812` (N/A)
- **Original Input**: "the movie was great and the acting was top notch"
- **Perturbed Input**: "the movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.57)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_eea001d5b812` (N/A)
- **Original Input**: "the movie was great and the acting was top notch"
- **Perturbed Input**: "the movie was great and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.42)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.
