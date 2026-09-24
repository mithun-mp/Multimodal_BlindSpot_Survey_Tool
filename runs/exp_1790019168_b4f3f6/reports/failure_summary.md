# Behavioral Failure Diagnoses: Multimodel Robustness Audit002

**Experiment ID**: `exp_1790019168_b4f3f6`
**Total Diagnosed Failures**: 11

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_38bf63d5b273` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "All Glitters are not Gold, however they do not be reliably."
- **Observed Transition**: `NEGATIVE (1.00)` → `NEGATIVE (0.98)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #2: [SPURIOUS] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_131f00590c08` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "All Glitters are not entirely non-Gold"
- **Observed Transition**: `NEGATIVE (0.94)` → `POSITIVE (0.94)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #3: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_131f00590c08` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "All Glitters are not entirely non-Gold"
- **Observed Transition**: `NEGATIVE (0.99)` → `POSITIVE (0.89)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #4: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_38bf63d5b273` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "All Glitters are not Gold, however they do not be reliably."
- **Observed Transition**: `NEGATIVE (0.99)` → `NEGATIVE (0.95)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #5: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_7140a40a75ba` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "All Glitters extremely are not Gold"
- **Observed Transition**: `NEUTRAL (0.55)` → `NEGATIVE (0.53)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model inverted prediction (NEUTRAL → NEGATIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Evidence**: Model inverted prediction (NEUTRAL → NEGATIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #6: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_e933443e2c93` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "Entirely Glitters are not Gold"
- **Observed Transition**: `NEUTRAL (0.55)` → `NEGATIVE (0.52)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → NEGATIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Spurious failures.

### Failure #7: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_38bf63d5b273` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "All Glitters are not Gold, however they do not be reliably."
- **Observed Transition**: `NEUTRAL (0.55)` → `NEUTRAL (0.61)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #8: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_131f00590c08` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "All Glitters are not entirely non-Gold"
- **Observed Transition**: `NEGATIVE (0.52)` → `NEUTRAL (0.85)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → NEUTRAL).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → NEUTRAL).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #9: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_781b951d1dbb` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "All Glitters somewhat are not Gold"
- **Observed Transition**: `NEGATIVE (0.52)` → `NEUTRAL (0.55)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model inverted prediction (NEGATIVE → NEUTRAL) when presented with a degree modifier (WEAKEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Evidence**: Model inverted prediction (NEGATIVE → NEUTRAL) when presented with a degree modifier (WEAKEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #10: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_38bf63d5b273` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "All Glitters are not Gold, however they do not be reliably."
- **Observed Transition**: `NEGATIVE (0.52)` → `NEGATIVE (0.70)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #11: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_9f9e1dadae1e` (N/A)
- **Original Input**: "All Glitters are not Gold"
- **Perturbed Input**: "In fact, all Glitters are not Gold"
- **Observed Transition**: `NEGATIVE (0.52)` → `NEUTRAL (0.50)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → NEUTRAL).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → NEUTRAL).
- **Actionable Recommendation**: Augment training data and regularize behavior against structure perturbations to fix Spurious failures.
