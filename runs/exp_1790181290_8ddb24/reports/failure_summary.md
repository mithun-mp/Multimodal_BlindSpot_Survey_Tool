# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790181290_8ddb24`
**Total Diagnosed Failures**: 17

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_c071178618a0` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am not healthy but am still hospitalised"
- **Observed Transition**: `NEGATIVE (0.98)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_3ff06983da19` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.98)` → `NEGATIVE (0.91)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [SPURIOUS] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_29a13b717c6d` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, and I displayed remarkable skill."
- **Observed Transition**: `NEGATIVE (0.98)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #4: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_c071178618a0` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am not healthy but am still hospitalised"
- **Observed Transition**: `NEGATIVE (0.59)` → `NEGATIVE (0.87)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #5: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_f559684f20e0` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am extremely healthy but am still hospitalised"
- **Observed Transition**: `NEGATIVE (0.59)` → `NEUTRAL (0.44)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model inverted prediction (NEGATIVE → NEUTRAL) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Evidence**: Model inverted prediction (NEGATIVE → NEUTRAL) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #6: [BLIND] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_3ff06983da19` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.59)` → `NEGATIVE (0.71)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #7: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_29a13b717c6d` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, and I displayed remarkable skill."
- **Observed Transition**: `NEGATIVE (0.59)` → `POSITIVE (0.82)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #8: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_e42413de5490` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "It is not impossible that i am healthy but am still hospitalised"
- **Observed Transition**: `NEUTRAL (0.59)` → `POSITIVE (0.61)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #9: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_f559684f20e0` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am extremely healthy but am still hospitalised"
- **Observed Transition**: `NEUTRAL (0.59)` → `POSITIVE (0.65)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Evidence**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #10: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_3ff06983da19` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, however I could not repeat that performance."
- **Observed Transition**: `NEUTRAL (0.59)` → `NEUTRAL (0.48)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #11: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_29a13b717c6d` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, and I displayed remarkable skill."
- **Observed Transition**: `NEUTRAL (0.59)` → `POSITIVE (0.90)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #12: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_c071178618a0` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am not healthy but am still hospitalised"
- **Observed Transition**: `NEGATIVE (0.72)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #13: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_3ff06983da19` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.72)` → `NEGATIVE (0.52)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #14: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_29a13b717c6d` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, and I displayed remarkable skill."
- **Observed Transition**: `NEGATIVE (0.72)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #15: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_c071178618a0` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am not healthy but am still hospitalised"
- **Observed Transition**: `NEGATIVE (0.96)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #16: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_3ff06983da19` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.96)` → `NEGATIVE (0.89)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #17: [SPURIOUS] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_29a13b717c6d` (N/A)
- **Original Input**: "i am healthy but am still hospitalised"
- **Perturbed Input**: "i am healthy but am still hospitalised, and I displayed remarkable skill."
- **Observed Transition**: `NEGATIVE (0.96)` → `POSITIVE (0.98)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.
