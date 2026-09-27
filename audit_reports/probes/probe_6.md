# Probe #6 Diagnostic Detail

## Transformation Details
- **Perturbation Type**: `contrast_concession_prefix`
- **Description**: Prefixed context-aware contrastive concession clause referencing 'food'.
- **Perturbation Expectation**: Directional (Prediction Flip Expected)

## Sentence Comparison
- **Original Input**: "The food was delicious."
- **Perturbed Input**: "Although the food was delicious, it was surprisingly displeasing in comparison."

## Behavioral & Confidence Diagnostics
- **Original Prediction**: `POSITIVE` (Conf: 0.9999)
- **Perturbed Prediction**: `NEGATIVE` (Conf: 0.9897)
- **Behavioral Response**: `Label Flipped` (Flipped: `True`, Expected Flip: `True`)
- **Confidence Response**: `-0.0102 (Confidence Decreased)`
- **Unexpected Behavior Detected**: `False`

## Explanation Response
- **Jaccard Top-Token Similarity**: 0.5000
- **Cosine Attribution Alignment**: 0.4631
