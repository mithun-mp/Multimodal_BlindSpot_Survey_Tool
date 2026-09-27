# Behavioral Failure Diagnoses: Multimodel 00001

**Experiment ID**: `exp_1790537272_6f4cc1`
**Total Diagnosed Failures**: 9

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_67a0966bf0ce` (N/A)
- **Original Input**: "He is a Good boy but very naughty"
- **Perturbed Input**: "He is a Good boy but very naughty, however he could not repeat that performance."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_40691ebad054` (N/A)
- **Original Input**: "He is a Good boy but very naughty"
- **Perturbed Input**: "He is not a Good boy but very naughty"
- **Observed Transition**: `POSITIVE (0.91)` → `POSITIVE (0.83)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #3: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_67a0966bf0ce` (N/A)
- **Original Input**: "He is a Good boy but very naughty"
- **Perturbed Input**: "He is a Good boy but very naughty, however he could not repeat that performance."
- **Observed Transition**: `POSITIVE (0.91)` → `POSITIVE (0.74)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #4: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_67a0966bf0ce` (N/A)
- **Original Input**: "He is a Good boy but very naughty"
- **Perturbed Input**: "He is a Good boy but very naughty, however he could not repeat that performance."
- **Observed Transition**: `POSITIVE (0.98)` → `POSITIVE (0.97)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #5: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_83a07c79c82d` (N/A)
- **Original Input**: "He is a Good boy but very naughty"
- **Perturbed Input**: "It is not impossible that he is a Good boy but very naughty"
- **Observed Transition**: `NEUTRAL (0.47)` → `POSITIVE (0.45)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #6: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_e47fc6c5c6c1` (N/A)
- **Original Input**: "He is a Good boy but very naughty"
- **Perturbed Input**: "He is a extremely Good boy but very naughty"
- **Observed Transition**: `NEUTRAL (0.47)` → `POSITIVE (0.69)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Intensifier inverted polarity (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Evidence**: Intensifier inverted polarity (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #7: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_b0b54e3d1fa3` (N/A)
- **Original Input**: "He is a Good boy but very naughty"
- **Perturbed Input**: "He is a Decent boy but very naughty"
- **Observed Transition**: `NEUTRAL (0.47)` → `NEGATIVE (0.48)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → NEGATIVE (NEGATIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Spurious failures.

### Failure #8: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_67a0966bf0ce` (N/A)
- **Original Input**: "He is a Good boy but very naughty"
- **Perturbed Input**: "He is a Good boy but very naughty, however he could not repeat that performance."
- **Observed Transition**: `NEUTRAL (0.47)` → `NEUTRAL (0.47)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #9: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_c550515af7da` (N/A)
- **Original Input**: "He is a Good boy but very naughty"
- **Perturbed Input**: "He is a Good boy but very naughty, and he displayed remarkable skill."
- **Observed Transition**: `NEUTRAL (0.47)` → `POSITIVE (0.86)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.
