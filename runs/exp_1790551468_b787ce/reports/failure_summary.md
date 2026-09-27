# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790551468_b787ce`
**Total Diagnosed Failures**: 9

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_45d543e2dcef` (N/A)
- **Original Input**: "i am not well"
- **Perturbed Input**: "i am not well, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (1.00)` → `NEGATIVE (0.98)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #2: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_fd37a1e79bb7` (N/A)
- **Original Input**: "i am not well"
- **Perturbed Input**: "i am somewhat not well"
- **Observed Transition**: `NEGATIVE (0.57)` → `NEGATIVE (0.76)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Downtoner caused confidence to surge: confidence increased by 18.73 percentage points (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Downtoner caused confidence to surge: confidence increased by 18.73 percentage points (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #3: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_597650cbb446` (N/A)
- **Original Input**: "i am not well"
- **Perturbed Input**: "i am non well"
- **Observed Transition**: `NEGATIVE (0.57)` → `NEUTRAL (0.66)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → NEUTRAL (NEUTRAL)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEGATIVE (NEGATIVE) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Spurious failures.

### Failure #4: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_45d543e2dcef` (N/A)
- **Original Input**: "i am not well"
- **Perturbed Input**: "i am not well, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.57)` → `NEGATIVE (0.89)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #5: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_45d543e2dcef` (N/A)
- **Original Input**: "i am not well"
- **Perturbed Input**: "i am not well, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.93)` → `NEGATIVE (0.96)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #6: [MISWEIGHTED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_99363fb2f65a` (N/A)
- **Original Input**: "i am not well"
- **Perturbed Input**: "i am not entirely non-well"
- **Observed Transition**: `NEGATIVE (0.99)` → `NEGATIVE (0.64)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 35.69 percentage points under meaning-preserving perturbation.
- **Evidence**: Polarity preserved, but confidence collapsed by 35.69 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Misweighted failures.

### Failure #7: [MISWEIGHTED] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_597650cbb446` (N/A)
- **Original Input**: "i am not well"
- **Perturbed Input**: "i am non well"
- **Observed Transition**: `NEGATIVE (0.99)` → `NEGATIVE (0.81)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 18.41 percentage points under meaning-preserving perturbation.
- **Evidence**: Polarity preserved, but confidence collapsed by 18.41 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Misweighted failures.

### Failure #8: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_45d543e2dcef` (N/A)
- **Original Input**: "i am not well"
- **Perturbed Input**: "i am not well, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.99)` → `NEGATIVE (0.97)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #9: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_45d543e2dcef` (N/A)
- **Original Input**: "i am not well"
- **Perturbed Input**: "i am not well, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (1.00)` → `NEGATIVE (0.98)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Evidence**: Probe introduces a polarity reversal (PRESERVE_POLARITY), but model retained the same predicted class and polarity (NEGATIVE (NEGATIVE) → NEGATIVE (NEGATIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.
