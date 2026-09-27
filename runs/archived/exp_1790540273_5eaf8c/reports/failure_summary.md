# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790540273_5eaf8c`
**Total Diagnosed Failures**: 1

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_f8cfe5bc91e4` (N/A)
- **Original Input**: "The movie was great and the acting was top notch."
- **Perturbed Input**: "The movie was not great and the acting was top notch."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.
