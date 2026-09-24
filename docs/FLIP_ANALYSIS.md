# BlindSpot Prediction Flip Analysis & Transition Dynamics

## 1. Multiclass Definition of Prediction Flip

A prediction flip in BlindSpot is strictly defined as:
```python
def is_prediction_flip(original_label: str, perturbed_label: str) -> bool:
    if not original_label or not perturbed_label:
        return False
    return str(original_label).strip().upper() != str(perturbed_label).strip().upper()
```

### Non-Binary Architectural Support
Unlike naive sentiment-analysis scripts that compute `flip = 1 - label_idx`, BlindSpot natively supports:
- **Binary Classifiers**: `POSITIVE` $\longleftrightarrow$ `NEGATIVE`
- **3-Class Sentiment**: `NEGATIVE` $\longleftrightarrow$ `NEUTRAL` $\longleftrightarrow$ `POSITIVE`
- **N-Way Topic Classifiers**: `WORLD`, `SPORTS`, `BUSINESS`, `TECH`
- **Emotion Classifiers**: `JOY`, `SADNESS`, `ANGER`, `FEAR`, `SURPRISE`, `DISGUST`

A transition from `NEGATIVE` to `NEUTRAL` is correctly recognized as a prediction flip.

---

## 2. Behavioral Outcome Classification

Every evaluation of a probe against a model produces one of the following canonical outcomes:

| Outcome | Expected Flip? | Observed Flipped? | Meaning |
| :--- | :---: | :---: | :--- |
| **`EXPECTED_FLIP`** | `True` | `True` | **Success**: Model appropriately reversed polarity under negation/contrast. |
| **`MISSING_FLIP`** | `True` | `False` | **Failure (Blindness)**: Model failed to detect semantic negation. |
| **`EXPECTED_PRESERVE`** | `False` | `False` | **Success**: Model maintained invariant prediction under synonym/intensity/structure. |
| **`UNEXPECTED_FLIP`** | `False` | `True` | **Failure (Spuriousness)**: Model broke prediction on meaning-preserving stimulus. |

---

## 3. Label Transition Matrices

To understand directional confusion, BlindSpot computes a full $|L| \times |L|$ transition matrix:
$$T_{j, k} = \sum_{i=1}^N \mathbb{I}[y_0(p_i) = l_j \land y_p(p_i) = l_k]$$

Example 3-Class Transition Matrix:
| From \ To | NEGATIVE | NEUTRAL | POSITIVE |
| :--- | :---: | :---: | :---: |
| **NEGATIVE** | 12 | 4 | 0 |
| **NEUTRAL** | 1 | 8 | 2 |
| **POSITIVE** | 3 | 5 | 15 |

---

## 4. Confidence Deltas in Signed Percentage Points

Confidence deltas are always expressed in **signed percentage points** rather than ambiguous decimal fractions:

$$\Delta c_{\text{pts}} = (c_{\text{perturbed}} - c_{\text{original}}) \times 100$$

- Example: If original confidence is $0.94$ ($94.0\%$) and perturbed confidence is $0.72$ ($72.0\%$), the delta is formatted as:
  $$\mathbf{-22.00 \text{ percentage points}}$$
- In reports and UI cards, deltas are clearly labeled with `+` or `-` and percentage points (`pts` or `pp`) to prevent conflation with relative percentage drops.
