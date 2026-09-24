# Probe #1 Diagnostic Detail

## Transformation Details
- **Perturbation Type**: `negation_insertion`
- **Description**: Inserted negation 'not' after auxiliary verb.
- **Perturbation Expectation**: Directional (Prediction Flip Expected)

## Sentence Comparison
- **Original Input**: "The food was delicious."
- **Perturbed Input**: "The food was not delicious."

## Behavioral & Confidence Diagnostics
- **Original Prediction**: `POSITIVE` (Conf: 0.9999)
- **Perturbed Prediction**: `NEGATIVE` (Conf: 0.9998)
- **Behavioral Response**: `Label Flipped` (Flipped: `True`, Expected Flip: `True`)
- **Confidence Response**: `-0.0001 (Confidence Decreased)`
- **Unexpected Behavior Detected**: `False`

## Explanation Response
- **Jaccard Top-Token Similarity**: 0.8000
- **Cosine Attribution Alignment**: -0.3252
