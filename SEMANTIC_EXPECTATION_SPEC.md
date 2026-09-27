# BlindSpot Semantic Expectation Specification

## 1. Overview and Core Philosophy

In black-box sentiment classifier auditing, linguistic perturbations are applied to an original text to observe how model predictions transition.
To ensure scientific validity, model comparisons must never operate on raw class IDs (`0`, `1`, `2`) or unverified arbitrary label strings (`LABEL_0`, `LABEL_1`). 

Instead, BlindSpot establishes a **Model-Independent Canonical Semantic Representation** (`SemanticPolarity`) that anchors all predictions across both binary and multiclass models, decoupled from internal tokenizers or training artifact label orders.

---

## 2. Canonical Semantic Representation

All model predictions are projected into the canonical `SemanticPolarity` space:

| `SemanticPolarity` | Meaning | Binary Model Mapping | 3-Class Model Mapping |
| :--- | :--- | :--- | :--- |
| `POSITIVE` | Explicit positive sentiment | Class `1` (or label indicating positive) | Label indicating positive |
| `NEGATIVE` | Explicit negative sentiment | Class `0` (or label indicating negative) | Label indicating negative |
| `NEUTRAL` | Neutral, objective, or ambivalent | *Not applicable* | Label indicating neutral |
| `UNKNOWN` | Unrecognized or undetermined | Non-conforming output | Non-conforming output |

---

## 3. Linguistic Expectation Types

Controlled probes carry an immutable linguistic expectation contract (`ProbeExpectation`):

| `ExpectationType` | Linguistic Intent | Typical Perturbations | Expected Behavioral Relation |
| :--- | :--- | :--- | :--- |
| `REVERSE_POLARITY` | Invert truth-conditional sentiment | Negation insertion, negation removal | `POLARITY_REVERSED` |
| `PRESERVE_POLARITY` | Preserve semantic evaluation | Synonym substitution, paraphrase, double negation | `SAME_POLARITY` |
| `CONTRAST_SHIFT` | Shift dominant discourse sentiment | Adversative contrast clause append | `POLARITY_REVERSED` |
| `INTENSIFY` | Strengthen sentiment magnitude | Degree adverb intensifier (`extremely`, `remarkably`) | `POLARITY_STRENGTHENED` |
| `DOWNTONE` | Attenuate sentiment magnitude | Degree adverb downtoner (`somewhat`, `partially`) | `POLARITY_WEAKENED` |
| `STRUCTURAL_SHIFT` | Syntactic reordering | Clause order inversion | `SAME_POLARITY` |
| `UNKNOWN` | Undetermined linguistic contract | Unclassified custom probe | `UNKNOWN` |

---

## 4. Observed Behavioral Relations

Given the original model prediction $(\text{pol}_0, \text{conf}_0)$ and perturbed prediction $(\text{pol}_t, \text{conf}_t)$:

| `BehavioralRelation` | Formal Condition |
| :--- | :--- |
| `SAME_POLARITY` | $\text{pol}_t = \text{pol}_0$ and $|\Delta \text{conf}| \le 15\,\text{pp}$ |
| `POLARITY_REVERSED` | $(\text{pol}_0 = \text{POS} \land \text{pol}_t = \text{NEG}) \lor (\text{pol}_0 = \text{NEG} \land \text{pol}_t = \text{POS})$ |
| `POLARITY_STRENGTHENED` | $\text{pol}_t = \text{pol}_0$ and $\Delta \text{conf} > +15\,\text{pp}$ |
| `POLARITY_WEAKENED` | $\text{pol}_t = \text{pol}_0$ and $\Delta \text{conf} < -15\,\text{pp}$ |
| `POSITIVE_TO_NEUTRAL` | $\text{pol}_0 = \text{POS} \land \text{pol}_t = \text{NEU}$ |
| `NEGATIVE_TO_NEUTRAL` | $\text{pol}_0 = \text{NEG} \land \text{pol}_t = \text{NEU}$ |
| `NEUTRAL_TO_POSITIVE` | $\text{pol}_0 = \text{NEU} \land \text{pol}_t = \text{POS}$ |
| `NEUTRAL_TO_NEGATIVE` | $\text{pol}_0 = \text{NEU} \land \text{pol}_t = \text{NEG}$ |
| `OTHER` | Unclassified state transition |
| `UNKNOWN` | Missing label or confidence output |

---

## 5. Three Distinct Flip & Transition Definitions

BlindSpot strictly distinguishes between three transition metrics:

1. **Raw Label Flip (`raw_label_flip`)**:
   $$\text{raw\_label}_t \ne \text{raw\_label}_0$$
   Tracks whether the raw predicted class index or label string changed.

2. **Polarity Flip (`polarity_flip`)**:
   $$(\text{pol}_0 = \text{POS} \land \text{pol}_t = \text{NEG}) \lor (\text{pol}_0 = \text{NEG} \land \text{pol}_t = \text{POS})$$
   Tracks genuine semantic sentiment reversal. A transition from `POSITIVE` to `NEUTRAL` is **not** a polarity flip.

3. **Semantic State Change (`semantic_state_change`)**:
   $$\text{pol}_t \ne \text{pol}_0$$
   Tracks any canonical sentiment movement, including `POS → NEU`, `NEU → NEG`, etc.

---

## 6. Diagnostic Failure Taxonomy Mapping

The primary outcome (`BehavioralOutcome`) and secondary diagnostic failure (`FailureCategory`) are derived deterministically:

| Expectation | Observed Behavior | Primary Outcome | Failure Category | Scientific Rationale |
| :--- | :--- | :--- | :--- | :--- |
| `REVERSE_POLARITY` | `POLARITY_REVERSED` | `EXPECTED_FLIP` | `NONE` | Model correctly reversed polarity under truth-conditional alteration. |
| `REVERSE_POLARITY` | `SAME_POLARITY` | `MISSING_FLIP` | `BLIND` | Model failed to respond to polarity-altering operator (e.g., negation). |
| `REVERSE_POLARITY` | `POSITIVE_TO_NEUTRAL` / `NEGATIVE_TO_NEUTRAL` | `UNEXPECTED_CHANGE` | `MISWEIGHTED` | Model attenuated sentiment to neutral instead of fully reversing polarity. |
| `PRESERVE_POLARITY` | `SAME_POLARITY` ($\Delta \text{conf} \ge -15\,\text{pp}$) | `EXPECTED_PRESERVE` | `NONE` | Model maintained semantic evaluation stably. |
| `PRESERVE_POLARITY` | `SAME_POLARITY` ($\Delta \text{conf} < -15\,\text{pp}$) | `EXPECTED_PRESERVE` | `MISWEIGHTED` | Model maintained label but confidence collapsed (> 15 pp) under neutral change. |
| `PRESERVE_POLARITY` | `POLARITY_REVERSED` | `UNEXPECTED_FLIP` | `SPURIOUS` | Model inverted polarity under meaning-preserving perturbation. |
| `PRESERVE_POLARITY` | Transition to `NEUTRAL` | `UNEXPECTED_CHANGE` | `SPURIOUS` | Model drifted from confident sentiment under meaning-preserving perturbation. |
| `INTENSIFY` | `SAME_POLARITY` ($\Delta \text{conf} \ge -15\,\text{pp}$) | `EXPECTED_PRESERVE` | `NONE` | Model preserved polarity under intensifier. |
| `INTENSIFY` | $\Delta \text{conf} < -15\,\text{pp}$ | `EXPECTED_PRESERVE` | `MISWEIGHTED` | Intensifier caused confidence drop > 15 pp. |
| `INTENSIFY` | `POLARITY_REVERSED` | `UNEXPECTED_FLIP` | `MISWEIGHTED` | Degree modifier caused full polarity inversion. |
| `DOWNTONE` | `POLARITY_REVERSED` | `UNEXPECTED_FLIP` | `MISWEIGHTED` | Degree modifier caused full polarity inversion. |
| `UNKNOWN` | Any | `UNDETERMINED` | `UNDETERMINED` | Expectation contract is ambiguous or undetermined. |
