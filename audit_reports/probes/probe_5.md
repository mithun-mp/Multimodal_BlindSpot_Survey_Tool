# Probe #5 Diagnostic Detail

## Transformation Details
- **Perturbation Type**: `contrast_negative_append`
- **Description**: Appended context-aware negative contrast clause referencing 'food'.
- **Perturbation Expectation**: Directional (Prediction Flip Expected)

## Sentence Comparison
- **Original Input**: "The food was delicious."
- **Perturbed Input**: "The food was delicious, however it was surprisingly displeasing in comparison."

## Behavioral & Confidence Diagnostics
- **Original Prediction**: `POSITIVE` (Conf: 0.9999)
- **Perturbed Prediction**: `NEGATIVE` (Conf: 0.8219)
- **Behavioral Response**: `Label Flipped` (Flipped: `True`, Expected Flip: `True`)
- **Confidence Response**: `-0.1779 (Confidence Decreased)`
- **Unexpected Behavior Detected**: `False`

## Explanation Response
- **Jaccard Top-Token Similarity**: 0.1250
- **Cosine Attribution Alignment**: 0.5195
