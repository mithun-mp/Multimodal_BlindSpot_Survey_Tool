# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790530874_953eac`
**Total Diagnosed Failures**: 1

### Failure #1: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_de92c233126d` (N/A)
- **Original Input**: "the movie was good and the acting was top notch"
- **Perturbed Input**: "the movie was good and the acting was top notch, however it was surprisingly bad in comparison."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.41)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.
