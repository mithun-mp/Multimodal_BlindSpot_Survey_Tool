# Behavioral Failure Diagnoses: Multimodel Test Run Heavy 001

**Experiment ID**: `exp_1790363186_8828c5`
**Total Diagnosed Failures**: 13

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_ae5df0ccd318` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was not nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Observed Transition**: `NEGATIVE (1.00)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_d257d7394e56` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it, however it did not be reliably."
- **Observed Transition**: `NEGATIVE (1.00)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [SPURIOUS] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_cce6e49acab2` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it, and it delivered good results in practice."
- **Observed Transition**: `NEGATIVE (1.00)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #4: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_ae5df0ccd318` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was not nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Observed Transition**: `NEGATIVE (0.98)` → `NEGATIVE (0.98)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #5: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_d257d7394e56` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it, however it did not be reliably."
- **Observed Transition**: `NEGATIVE (0.98)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #6: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_ae5df0ccd318` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was not nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Observed Transition**: `NEGATIVE (0.98)` → `NEGATIVE (0.98)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #7: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_d257d7394e56` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it, however it did not be reliably."
- **Observed Transition**: `NEGATIVE (0.98)` → `NEGATIVE (0.98)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #8: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_cce6e49acab2` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it, and it delivered good results in practice."
- **Observed Transition**: `NEGATIVE (0.98)` → `POSITIVE (0.95)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #9: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_ae5df0ccd318` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was not nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Observed Transition**: `NEGATIVE (0.80)` → `NEGATIVE (0.82)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #10: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_d257d7394e56` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it, however it did not be reliably."
- **Observed Transition**: `NEGATIVE (0.80)` → `NEGATIVE (0.86)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #11: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_ae5df0ccd318` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was not nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Observed Transition**: `NEGATIVE (0.52)` → `NEGATIVE (0.50)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #12: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_d257d7394e56` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it, however it did not be reliably."
- **Observed Transition**: `NEGATIVE (0.52)` → `NEGATIVE (0.57)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #13: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_cce6e49acab2` (N/A)
- **Original Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."
- **Perturbed Input**: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it, and it delivered good results in practice."
- **Observed Transition**: `NEGATIVE (0.52)` → `NEUTRAL (0.36)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → NEUTRAL).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → NEUTRAL).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.
