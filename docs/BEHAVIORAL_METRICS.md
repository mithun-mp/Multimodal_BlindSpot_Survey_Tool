# BlindSpot Stratified Behavioral Metrics & Mathematical Formulations

## 1. Motivation: Why Stratification is Mathematically Mandatory

In early behavioral testing implementations, a simplistic metric called "Flip Rate" was often calculated as:
$$\text{Crude Flip Rate} = \frac{\text{Total Observed Prediction Flips}}{\text{Total Probes Evaluated}}$$

This unstratified metric is **scientifically invalid**:
- For **negation probes**, an ideal model *must* flip its prediction. A flip indicates successful compositional comprehension.
- For **synonym probes**, an ideal model *must preserve* its prediction. A flip indicates brittle spurious sensitivity.

Lumping both into an aggregate flip rate produces meaningless numbers: a model that correctly flips on negation and preserves on synonyms would get a 50% "flip rate", exactly the same score as a model that incorrectly flips on synonyms and ignores negation!

BlindSpot resolves this problem through **Stratified Behavioral Metrics**.

---

## 2. Canonical Mathematical Formulations

Let $\mathcal{P} = \{p_1, p_2, \dots, p_N\}$ be the set of executed probes for a model $M$.
Let $y_0(p_i)$ denote the model's prediction on the original seed text, and $y_p(p_i)$ denote the prediction on the perturbed text.
Let $F(p_i) \in \{0, 1\}$ be the indicator for prediction flip:
$$F(p_i) = \mathbb{I}[y_0(p_i) \neq y_p(p_i)]$$

Let $E(p_i) \in \{0, 1\}$ indicate whether a flip was expected under the probe's linguistic transformation:
$$E(p_i) = \mathbb{I}[\text{probe expects flip}]$$

---

### 2.1 Observed Flip Rate ($\text{OFR}$)
Fraction of all executed probes where the prediction label changed:
$$\text{OFR} = \frac{1}{N} \sum_{i=1}^N F(p_i)$$

*Interpretation*: Descriptive measurement of output volatility across all transformations.

---

### 2.2 Expected Flip Rate ($\text{EFR}$)
Fraction of probes where a flip was expected that actually flipped:
$$\mathcal{P}_{\text{flip}} = \{p_i \in \mathcal{P} \mid E(p_i) = 1\}$$
$$\text{EFR} = \frac{1}{|\mathcal{P}_{\text{flip}}|} \sum_{p_i \in \mathcal{P}_{\text{flip}}} F(p_i) \quad (\text{defined as } 0 \text{ if } |\mathcal{P}_{\text{flip}}| = 0)$$

*Interpretation*: Measures the model's sensitivity to semantic inversion (e.g. negation, adversative shift). High values ($>90\%$) indicate strong semantic responsiveness.

---

### 2.3 Preserve Rate ($\text{PR}$)
Fraction of probes where prediction was expected to remain unchanged that successfully retained their label:
$$\mathcal{P}_{\text{preserve}} = \{p_i \in \mathcal{P} \mid E(p_i) = 0\}$$
$$\text{PR} = \frac{1}{|\mathcal{P}_{\text{preserve}}|} \sum_{p_i \in \mathcal{P}_{\text{preserve}}} (1 - F(p_i)) \quad (\text{defined as } 0 \text{ if } |\mathcal{P}_{\text{preserve}}| = 0)$$

*Interpretation*: Measures model invariance to meaning-preserving transformations (e.g. synonyms, double negation, intensity adverbs, clause reordering). High values ($>90\%$) indicate robust invariance.

---

### 2.4 Behavioral Consistency ($\text{BC}$)
Fraction of all probes where the observed behavioral outcome complied with the linguistic expectation:
$$\text{BC} = \frac{1}{N} \left[ \sum_{p_i \in \mathcal{P}_{\text{flip}}} F(p_i) + \sum_{p_i \in \mathcal{P}_{\text{preserve}}} (1 - F(p_i)) \right]$$

*Interpretation*: Overall measure of compliance with controlled linguistic truth-conditions. A perfect model scores $1.00$ ($100\%$).

---

### 2.5 Confidence Flip Rate ($\text{CFR}_\tau$)
Fraction of probes where model confidence dropped by more than a sensitivity threshold $\tau$ (default $\tau = 20.0$ percentage points):
$$\Delta c(p_i) = (c_p(p_i) - c_0(p_i)) \times 100$$
$$\text{CFR}_\tau = \frac{1}{N} \sum_{i=1}^N \mathbb{I}[\Delta c(p_i) \le -\tau]$$

*Interpretation*: Identifies "silent failures" where the discrete label may not have flipped, but model certainty suffered a severe degradation under perturbation.
