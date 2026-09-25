# Behavioral Failure Diagnoses: Multimodel Test Run 004

**Experiment ID**: `exp_1790357357_062da3`
**Total Diagnosed Failures**: 15

### Failure #1: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_859f5f7bfbf1` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am not Healthy and Energetic,But still i am Hospitalized"
- **Observed Transition**: `NEGATIVE (0.99)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #2: [BLIND] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_2c66cf98fc1f` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am Healthy and Energetic,But still i am Hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.99)` → `NEGATIVE (0.80)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #3: [SPURIOUS] — Model `distilbert-base-uncased-finetuned-sst-2-english`
- **Probe ID**: `prb_b84086ecdb68` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am Healthy and Energetic,But still i am Hospitalized, and I displayed remarkable skill."
- **Observed Transition**: `NEGATIVE (0.99)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #4: [SPURIOUS] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_bae1a417e4e6` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "It is not impossible that I am Healthy and Energetic,But still i am Hospitalized"
- **Observed Transition**: `POSITIVE (0.61)` → `NEGATIVE (0.55)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (POSITIVE → NEGATIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (POSITIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #5: [SPURIOUS] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_a85e33861176` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am Respectable and Energetic,But still i am Hospitalized"
- **Observed Transition**: `POSITIVE (0.61)` → `NEGATIVE (0.53)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (POSITIVE → NEGATIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (POSITIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against synonym_substitution perturbations to fix Spurious failures.

### Failure #6: [BLIND] — Model `albert-base-v2-SST-2`
- **Probe ID**: `prb_2c66cf98fc1f` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am Healthy and Energetic,But still i am Hospitalized, however I could not repeat that performance."
- **Observed Transition**: `POSITIVE (0.61)` → `POSITIVE (0.76)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (POSITIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #7: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_859f5f7bfbf1` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am not Healthy and Energetic,But still i am Hospitalized"
- **Observed Transition**: `NEGATIVE (0.96)` → `NEGATIVE (1.00)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against negation_insertion perturbations to fix Blind failures.

### Failure #8: [BLIND] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_2c66cf98fc1f` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am Healthy and Energetic,But still i am Hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEGATIVE (0.96)` → `NEGATIVE (0.79)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEGATIVE → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #9: [SPURIOUS] — Model `bert-base-uncased-SST-2`
- **Probe ID**: `prb_b84086ecdb68` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am Healthy and Energetic,But still i am Hospitalized, and I displayed remarkable skill."
- **Observed Transition**: `NEGATIVE (0.96)` → `POSITIVE (1.00)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEGATIVE → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #10: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_bae1a417e4e6` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "It is not impossible that I am Healthy and Energetic,But still i am Hospitalized"
- **Observed Transition**: `NEUTRAL (0.62)` → `NEGATIVE (0.49)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → NEGATIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → NEGATIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #11: [SPURIOUS] — Model `twitter-roberta-base-sentiment-latest`
- **Probe ID**: `prb_b84086ecdb68` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am Healthy and Energetic,But still i am Hospitalized, and I displayed remarkable skill."
- **Observed Transition**: `NEUTRAL (0.62)` → `POSITIVE (0.88)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.

### Failure #12: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_bae1a417e4e6` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "It is not impossible that I am Healthy and Energetic,But still i am Hospitalized"
- **Observed Transition**: `NEUTRAL (0.52)` → `POSITIVE (0.56)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against double_negation perturbations to fix Spurious failures.

### Failure #13: [MISWEIGHTED] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_09115dba0e79` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am extremely Healthy and Energetic ,But still i am Hospitalized"
- **Observed Transition**: `NEUTRAL (0.52)` → `POSITIVE (0.54)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Evidence**: Model inverted prediction (NEUTRAL → POSITIVE) when presented with a degree modifier (STRENGTHEN_POLARITY), indicating disproportionately skewed feature weighting.
- **Actionable Recommendation**: Augment training data and regularize behavior against intensity perturbations to fix Misweighted failures.

### Failure #14: [BLIND] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_2c66cf98fc1f` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am Healthy and Energetic,But still i am Hospitalized, however I could not repeat that performance."
- **Observed Transition**: `NEUTRAL (0.52)` → `NEUTRAL (0.49)`
- **Prediction Flipped**: `False` (Expected Flip: `True`)
- **Diagnostic Reason**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **Evidence**: The verified probe introduces a polarity-altering change (SHIFT_CONTRAST), but the model retained the same predicted class (NEUTRAL → NEUTRAL).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_negative_append perturbations to fix Blind failures.

### Failure #15: [SPURIOUS] — Model `twitter-roberta-base-sentiment`
- **Probe ID**: `prb_b84086ecdb68` (N/A)
- **Original Input**: "I am Healthy and Energetic ,But still i am Hospitalized"
- **Perturbed Input**: "I am Healthy and Energetic,But still i am Hospitalized, and I displayed remarkable skill."
- **Observed Transition**: `NEUTRAL (0.52)` → `POSITIVE (0.92)`
- **Prediction Flipped**: `True` (Expected Flip: `False`)
- **Diagnostic Reason**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Evidence**: The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class (NEUTRAL → POSITIVE).
- **Actionable Recommendation**: Augment training data and regularize behavior against contrast_positive_append perturbations to fix Spurious failures.
