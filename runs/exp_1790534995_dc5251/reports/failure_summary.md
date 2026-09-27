# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790534995_dc5251`
**Total Diagnosed Failures**: 6

### Failure #1: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_db77fceb6f8f` (N/A)
- **Original Input**: "the sun rises in the east and sun sets in west"
- **Perturbed Input**: "It is not true that the sun rises in the east and sun sets in west"
- **Observed Transition**: `NEUTRAL (0.93)` → `NEUTRAL (0.79)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_prefix perturbations to fix Blind failures.

### Failure #2: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_5038061b3249` (N/A)
- **Original Input**: "the sun rises in the east and sun sets in west"
- **Perturbed Input**: "It is not impossible that the sun rises in the east and sun sets in west"
- **Observed Transition**: `NEUTRAL (0.93)` → `NEUTRAL (0.74)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 18.80 percentage points under meaning-preserving perturbation.
- **Evidence**: Polarity preserved, but confidence collapsed by 18.80 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Misweighted failures.

### Failure #3: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_920083d672b4` (N/A)
- **Original Input**: "the sun rises in the east and sun sets in west"
- **Perturbed Input**: "the sun rises in the east and sun sets in west, however it does not rise reliably."
- **Observed Transition**: `NEUTRAL (0.93)` → `NEUTRAL (0.95)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #4: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_db77fceb6f8f` (N/A)
- **Original Input**: "the sun rises in the east and sun sets in west"
- **Perturbed Input**: "It is not true that the sun rises in the east and sun sets in west"
- **Observed Transition**: `NEUTRAL (0.58)` → `NEUTRAL (0.49)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_prefix perturbations to fix Blind failures.

### Failure #5: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_5038061b3249` (N/A)
- **Original Input**: "the sun rises in the east and sun sets in west"
- **Perturbed Input**: "It is not impossible that the sun rises in the east and sun sets in west"
- **Observed Transition**: `NEUTRAL (0.58)` → `POSITIVE (0.76)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_POLARITY), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #6: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_920083d672b4` (N/A)
- **Original Input**: "the sun rises in the east and sun sets in west"
- **Perturbed Input**: "the sun rises in the east and sun sets in west, however it does not rise reliably."
- **Observed Transition**: `NEUTRAL (0.58)` → `NEUTRAL (0.78)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.
