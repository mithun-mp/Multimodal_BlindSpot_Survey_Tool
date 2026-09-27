# Behavioral Failure Diagnoses: E2E Semantic Ground-Truth Benchmark

**Experiment ID**: `exp_1790522163_2f0f27`
**Total Diagnosed Failures**: 5

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_2f02bf775223` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was absolutely fantastic and thrilling, however it did not be reliably."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.80)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_2f02bf775223` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was absolutely fantastic and thrilling, however it did not be reliably."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.92)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_2f02bf775223` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was absolutely fantastic and thrilling, however it did not be reliably."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.97)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #4: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_2f02bf775223` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was absolutely fantastic and thrilling, however it did not be reliably."
- **Observed Transition**: `POSITIVE (1.00)` → `POSITIVE (0.69)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #5: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_2f02bf775223` (N/A)
- **Original Input**: "The movie was absolutely fantastic and thrilling."
- **Perturbed Input**: "The movie was absolutely fantastic and thrilling, however it did not be reliably."
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.93)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (POSITIVE (POSITIVE) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.
