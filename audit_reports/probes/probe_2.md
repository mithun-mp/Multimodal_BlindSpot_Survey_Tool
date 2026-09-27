# Probe #2 Diagnostic Detail

## Transformation Details
- **Perturbation Type**: `double_negation`
- **Description**: Framed sentence with double negation ('It is not impossible that').
- **Perturbation Expectation**: Invariant (Prediction Stability Expected)

## Sentence Comparison
- **Original Input**: "The food was delicious."
- **Perturbed Input**: "It is not impossible that the food was delicious."

## Behavioral & Confidence Diagnostics
- **Original Prediction**: `POSITIVE` (Conf: 0.9999)
- **Perturbed Prediction**: `POSITIVE` (Conf: 0.9994)
- **Behavioral Response**: `Label Unchanged` (Flipped: `False`, Expected Flip: `False`)
- **Confidence Response**: `-0.0005 (Confidence Decreased)`
- **Unexpected Behavior Detected**: `False`

## Explanation Response
- **Jaccard Top-Token Similarity**: 0.2857
- **Cosine Attribution Alignment**: 0.5155
