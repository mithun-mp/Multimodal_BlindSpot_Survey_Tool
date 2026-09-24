# Probe #4 Diagnostic Detail

## Transformation Details
- **Perturbation Type**: `contrast_positive_append`
- **Description**: Appended context-aware positive contrast clause referencing 'food'.
- **Perturbation Expectation**: Invariant (Prediction Stability Expected)

## Sentence Comparison
- **Original Input**: "The food was delicious."
- **Perturbed Input**: "The food was delicious, and every portion was fresh and generous."

## Behavioral & Confidence Diagnostics
- **Original Prediction**: `POSITIVE` (Conf: 0.9999)
- **Perturbed Prediction**: `POSITIVE` (Conf: 0.9999)
- **Behavioral Response**: `Label Unchanged` (Flipped: `False`, Expected Flip: `False`)
- **Confidence Response**: `+0.0000 (Confidence Increased)`
- **Unexpected Behavior Detected**: `False`

## Explanation Response
- **Jaccard Top-Token Similarity**: 0.1250
- **Cosine Attribution Alignment**: 0.3956
