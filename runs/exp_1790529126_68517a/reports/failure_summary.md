# Behavioral Failure Diagnoses: mul01

**Experiment ID**: `exp_1790529126_68517a`
**Total Diagnosed Failures**: 9

### Failure #1: [MISWEIGHTED] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_9953ed325bb4` (N/A)
- **Original Input**: "the sun rises in east and sun sets in the west"
- **Perturbed Input**: "the insolate rises in east and sun sets in the west"
- **Observed Transition**: `POSITIVE (0.99)` → `POSITIVE (0.53)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 45.44 percentage points under meaning-preserving perturbation.
- **Evidence**: Polarity preserved, but confidence collapsed by 45.44 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Misweighted failures.

### Failure #2: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_7d985d4473b4` (N/A)
- **Original Input**: "the sun rises in east and sun sets in the west"
- **Perturbed Input**: "It is not true that the sun rises in east and sun sets in the west"
- **Observed Transition**: `NEUTRAL (0.92)` → `NEUTRAL (0.78)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_prefix perturbations to fix Blind failures.

### Failure #3: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_7bb95d12e74a` (N/A)
- **Original Input**: "the sun rises in east and sun sets in the west"
- **Perturbed Input**: "It is not impossible that the sun rises in east and sun sets in the west"
- **Observed Transition**: `NEUTRAL (0.92)` → `NEUTRAL (0.73)`
- **Prediction Flipped**: `False` (Expected Flip: `False`)
- **Diagnostic Reason**: Polarity preserved, but confidence collapsed by 19.19 percentage points under meaning-preserving perturbation.
- **Evidence**: Polarity preserved, but confidence collapsed by 19.19 percentage points under meaning-preserving perturbation.
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Misweighted failures.

### Failure #4: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_2dd2530ec5a0` (N/A)
- **Original Input**: "the sun rises in east and sun sets in the west"
- **Perturbed Input**: "the sun rises in east and sun sets in the west, however it does not rise reliably."
- **Observed Transition**: `NEUTRAL (0.92)` → `NEUTRAL (0.95)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #5: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_6cbfa56f29de` (N/A)
- **Original Input**: "the sun rises in east and sun sets in the west"
- **Perturbed Input**: "the sun rises in east and sun sets in the west, and it delivered good results in practice."
- **Observed Transition**: `NEUTRAL (0.92)` → `POSITIVE (0.86)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_MEANING), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_MEANING), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #6: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_7d985d4473b4` (N/A)
- **Original Input**: "the sun rises in east and sun sets in the west"
- **Perturbed Input**: "It is not true that the sun rises in east and sun sets in the west"
- **Observed Transition**: `NEUTRAL (0.61)` → `NEUTRAL (0.49)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Evidence**: Probe introduces a polarity reversal (REVERSE_POLARITY), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_prefix perturbations to fix Blind failures.

### Failure #7: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_7bb95d12e74a` (N/A)
- **Original Input**: "the sun rises in east and sun sets in the west"
- **Perturbed Input**: "It is not impossible that the sun rises in east and sun sets in the west"
- **Observed Transition**: `NEUTRAL (0.61)` → `POSITIVE (0.75)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_MEANING), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_MEANING), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #8: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_2dd2530ec5a0` (N/A)
- **Original Input**: "the sun rises in east and sun sets in the west"
- **Perturbed Input**: "the sun rises in east and sun sets in the west, however it does not rise reliably."
- **Observed Transition**: `NEUTRAL (0.61)` → `NEUTRAL (0.79)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Evidence**: Probe introduces a polarity reversal (SHIFT_CONTRAST), but model retained the same predicted class and polarity (NEUTRAL (NEUTRAL) → NEUTRAL (NEUTRAL)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #9: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_6cbfa56f29de` (N/A)
- **Original Input**: "the sun rises in east and sun sets in the west"
- **Perturbed Input**: "the sun rises in east and sun sets in the west, and it delivered good results in practice."
- **Observed Transition**: `NEUTRAL (0.61)` → `POSITIVE (0.93)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The perturbation is meaning-preserving (PRESERVE_MEANING), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Evidence**: The perturbation is meaning-preserving (PRESERVE_MEANING), but model unexpectedly changed its predicted class and altered its predicted state (NEUTRAL (NEUTRAL) → POSITIVE (POSITIVE)).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.
