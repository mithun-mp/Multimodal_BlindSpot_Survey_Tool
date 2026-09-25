# Behavioral Failure Diagnoses: Multimodel Robustness Audit

**Experiment ID**: `exp_1790354301_11f5af`
**Total Diagnosed Failures**: 17

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_7ee094120fc4` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am not healthy but still hospitalized."
- **Observed Transition**: `NEGATIVE (0.80)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_40cdd98cd562` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am healthy but still hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.80)` → `NEGATIVE (0.71)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [SPURIOUS] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_953d67a0201e` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am healthy but still hospitalized, and I displayed remarkable skill."
- **Observed Transition**: `NEGATIVE (0.80)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #4: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_7ee094120fc4` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am not healthy but still hospitalized."
- **Observed Transition**: `NEGATIVE (0.66)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #5: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_40cdd98cd562` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am healthy but still hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.66)` → `NEGATIVE (0.56)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #6: [SPURIOUS] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_953d67a0201e` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am healthy but still hospitalized, and I displayed remarkable skill."
- **Observed Transition**: `NEGATIVE (0.66)` → `POSITIVE (0.99)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #7: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_7ee094120fc4` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am not healthy but still hospitalized."
- **Observed Transition**: `NEGATIVE (0.74)` → `NEGATIVE (0.99)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #8: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_40cdd98cd562` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am healthy but still hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.74)` → `NEGATIVE (0.61)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #9: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_953d67a0201e` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am healthy but still hospitalized, and I displayed remarkable skill."
- **Observed Transition**: `NEGATIVE (0.74)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #10: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_8c69777126a9` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am extremely healthy but still hospitalized."
- **Observed Transition**: `NEUTRAL (0.72)` → `POSITIVE (0.49)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Evidence**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #11: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_c5ddeee1e059` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am salubrious but still hospitalized."
- **Observed Transition**: `NEUTRAL (0.72)` → `NEGATIVE (0.71)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → NEGATIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Spurious failures.

### Failure #12: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_953d67a0201e` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am healthy but still hospitalized, and I displayed remarkable skill."
- **Observed Transition**: `NEUTRAL (0.72)` → `POSITIVE (0.93)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #13: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_dfaae507ee27` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "It is not impossible that i am healthy but still hospitalized."
- **Observed Transition**: `NEUTRAL (0.48)` → `POSITIVE (0.72)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #14: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_8c69777126a9` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am extremely healthy but still hospitalized."
- **Observed Transition**: `NEUTRAL (0.48)` → `POSITIVE (0.78)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Evidence**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #15: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_a7a8d8210313` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am somewhat healthy but still hospitalized."
- **Observed Transition**: `NEUTRAL (0.48)` → `POSITIVE (0.55)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (WEAKEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Evidence**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (WEAKEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #16: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_40cdd98cd562` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am healthy but still hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEUTRAL (0.48)` → `NEUTRAL (0.51)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #17: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_953d67a0201e` (N/A)
- **Original Input**: "i am healthy but still hospitalized."
- **Perturbed Input**: "i am healthy but still hospitalized, and I displayed remarkable skill."
- **Observed Transition**: `NEUTRAL (0.48)` → `POSITIVE (0.92)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.
