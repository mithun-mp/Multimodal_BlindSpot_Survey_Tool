# Failure Taxonomy & Remediation Guide

**BlindSpot** automatically sorts identified model failure instances into a three-way taxonomy to provide clear diagnostic guidance and actionable remediation strategies.

---

## 1. The Three Failure Categories

| Taxonomy Category | Definition & Failure Symptom | Underlying Model Defect |
| :--- | :--- | :--- |
| **Blind** | Model prediction fails to flip when input negation operators (`not`, `never`, `didn't`) are introduced. | The classifier ignores negation tokens and relies purely on unigram sentiment keywords. |
| **Spurious** | Model prediction flips unexpectedly or relies on unrelated domain nouns, brand names, or neutral entities. | The model over-fits to non-causal entity correlations present in the fine-tuning data. |
| **Misweighted** | Model prediction fails to weigh contrastive connectives (`however`, `but`) or double negatives properly. | The model misallocates feature weights across clauses, giving priority to the wrong sentence segment. |

---

## 2. Empirical Examples & Diagnostic Signatures

### A. Blind Failure Example

- **Original Sentence**: `"The hotel room was very clean."` $\rightarrow$ **POSITIVE** (Conf: `0.98`)
- **Perturbed Sentence**: `"The hotel room was not very clean."` $\rightarrow$ **POSITIVE** (Conf: `0.95`)
- **Observed Behavior**: Prediction failed to flip to **NEGATIVE**.
- **Explanation Signature**: LIME/SHAP attributions show high positive weights assigned to `clean`, while `not` is assigned near-zero weight ($< 0.02$).

### B. Spurious Failure Example

- **Original Sentence**: `"The movie was great."` $\rightarrow$ **POSITIVE**
- **Perturbed Sentence**: `"The movie in Paris was great."` $\rightarrow$ **NEGATIVE**
- **Observed Behavior**: Prediction flipped unexpectedly due to the neutral location noun `Paris`.
- **Explanation Signature**: `Paris` received a large negative attribution weight.

### C. Misweighted Failure Example

- **Original Sentence**: `"The plot was weak."` $\rightarrow$ **NEGATIVE**
- **Perturbed Sentence**: `"The plot was weak, but the acting was outstanding."` $\rightarrow$ **NEGATIVE**
- **Observed Behavior**: Model ignored the contrast clause (`acting was outstanding`).
- **Explanation Signature**: High negative weight on `weak`, near-zero weight on `outstanding`.

---

## 3. Actionable Remediation Strategies

1. **For Blind Failures**:
   - Augment fine-tuning data with CheckList negation templates.
   - Apply counterfactual data augmentation (CDA) pairing positive and negated negative sentences during training.

2. **For Spurious Failures**:
   - Apply adversarial entity swapping (e.g. swapping named entities, locations, brand names) during training.
   - Use feature attribution regularization (e.g. RRR - Right for the Right Reasons loss penalty).

3. **For Misweighted Failures**:
   - Train on paired contrastive clause datasets (`X, but Y`).
   - Fine-tune attention heads to attend to discourse markers (`however`, `yet`, `although`).
