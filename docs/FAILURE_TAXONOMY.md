# BlindSpot Research Behavioral Failure Taxonomy

## 1. Executive Summary & Foundational Principle

In the BlindSpot research architecture, behavioral auditing is strictly decoupled into two distinct layers:
1. **Primary Behavioral Outcome**: Observable empirical relationship between the original baseline prediction and the probe prediction under linguistic perturbation (`EXPECTED_FLIP`, `MISSING_FLIP`, `UNEXPECTED_FLIP`, `EXPECTED_PRESERVE`, `UNEXPECTED_CHANGE`, `UNDETERMINED`).
2. **Secondary Failure Taxonomy**: Interpretive classification under the verified probe contract into formal failure categories (`NONE`, `BLIND`, `SPURIOUS`, `MISWEIGHTED`, `UNDETERMINED`).

A label flip is an **observation**. Blind, Spurious, and Misweighted are **interpretations** of the behavioral evidence relative to explicit probe expectations.

---

## 2. Formal Failure Categories

### A. BLIND
- **Definition**: The probe introduces a linguistically meaningful modification intended to alter semantic polarity, truth value, or dominant clause interpretation, but the target model fails to respond appropriately.
- **Typical Pattern**: `Expected Semantic Change (REVERSE_POLARITY)` + `Observed Prediction Invariance (MISSING_FLIP)`.
- **Multiclass Formalism**:
  - Original: $y_{\text{orig}}$
  - Perturbed: $y_{\text{pert}}$
  - If expected effect is `REVERSE_POLARITY` or `EXPECTED_FLIP`, a failure to flip ($y_{\text{orig}} == y_{\text{pert}}$) is classified as **BLIND**.
  - Any label shift ($y_{\text{orig}} \neq y_{\text{pert}}$, e.g. $\text{POSITIVE} \to \text{NEUTRAL}$ or $\text{POSITIVE} \to \text{NEGATIVE}$) constitutes a flip and satisfies the change criterion.
- **Example**:
  - *Seed*: "The movie was great and the acting was top notch." [POSITIVE, 0.9999]
  - *Probe*: "The movie was not great and the acting was top notch." [POSITIVE, 0.9921]
  - *Observed*: POSITIVE $\to$ POSITIVE ($\text{Flip}=\text{FALSE}$).
  - *Diagnosis*: **BLIND** — "The verified probe introduces a polarity-altering change (REVERSE_POLARITY), but the model retained the same predicted class."

---

### B. SPURIOUS
- **Definition**: The probe performs a meaning-preserving transformation (e.g. litotes/double negation, lexical substitution, syntactic reordering, or proverb paraphrase), but the model changes its prediction or exhibits drastic confidence erosion in response to the irrelevant perturbation.
- **Typical Pattern**: `Expected Semantic Preservation (PRESERVE_MEANING)` + `Observed Prediction Flip (UNEXPECTED_CHANGE)`.
- **Multiclass Formalism**:
  - If expected effect is `PRESERVE_MEANING` or `EXPECTED_PRESERVE`, any label alteration ($y_{\text{orig}} \neq y_{\text{pert}}$, e.g. $\text{POSITIVE} \to \text{NEGATIVE}$ or $\text{POSITIVE} \to \text{NEUTRAL}$) is classified as **SPURIOUS**.
- **Example**:
  - *Seed*: "The movie was excellent." [POSITIVE, 0.98]
  - *Probe*: "The movie was really excellent." [NEGATIVE, 0.52]
  - *Observed*: POSITIVE $\to$ NEGATIVE ($\text{Flip}=\text{TRUE}$).
  - *Diagnosis*: **SPURIOUS** — "The verified perturbation is meaning-preserving (PRESERVE_MEANING), but the model unexpectedly changed its predicted class."

---

### C. MISWEIGHTED
- **Definition**: The model responds to the linguistic modification, but the response is directionally inappropriate, disproportionately strong, or contradicts the specified modifier intent (e.g., intensifier causes confidence drop; downtoner causes confidence surge; contrast modifier alters dominant clause focus incorrectly).
- **Formal Criteria**:
  1. *Polarity Strengthening Direction Inversion*:
     - Expected: `STRENGTHEN_POLARITY`
     - Observed: Prediction flips to opposite class or confidence drops significantly ($> 15.0$ percentage points).
  2. *Polarity Weakening Direction Inversion*:
     - Expected: `WEAKEN_POLARITY`
     - Observed: Confidence surges significantly ($> 15.0$ percentage points) in the positive direction despite weakening downtoners.
- **Example**:
  - *Seed*: "The movie was good." [POSITIVE, 0.85]
  - *Probe*: "The movie was absolutely magnificent." [POSITIVE, 0.45]
  - *Confidence Delta*: $-40.0$ percentage points.
  - *Diagnosis*: **MISWEIGHTED** — "Expected polarity strengthening, but model confidence dropped by -40.0 pp."

---

### D. UNDETERMINED
- **Definition**: Used strictly when available empirical evidence cannot reliably distinguish the behavioral outcome.
- **Trigger Conditions**:
  - Ambiguous probe contracts without defined expected effect or semantic intent (`UNDETERMINED`).
  - Missing model output probabilities or malformed predictions.
  - Insufficient information to establish directional consistency.
- **Constraint**: `UNDETERMINED` must never serve as a catch-all for unexplained failures.

---

### E. NONE (Compliant Behavior)
- **Definition**: The model responds in exact conformity with the verified linguistic probe contract:
  - Expected flips produce observed prediction flips.
  - Meaning-preserving probes produce stable invariant predictions.
  - Directional modifiers yield consistent probability movements.
- **Research Integrity Guarantee**: When a validated model produces zero failures, that zero remains **0** and is fully backed by probe-level evidence.

---

## 3. Pure Deterministic Classifier: `classify_behavior`

The failure classification engine is implemented in `blindspot/testing/behavioral.py` as an isolated pure function:

```python
def classify_behavior(
    original_label: str,
    probe_label: str,
    original_confidence: float,
    probe_confidence: float,
    expected_effect: str,
    semantic_intent: str,
    expected_label_relation: Optional[str] = None,
    expected_confidence_relation: str = "UNCONSTRAINED",
    original_distribution: Optional[Dict[str, float]] = None,
    probe_distribution: Optional[Dict[str, float]] = None,
    probe_metadata: Optional[Dict[str, Any]] = None,
    confidence_threshold_pp: float = 15.0,
) -> Tuple[BehavioralOutcome, FailureCategory, Dict[str, Any], str]:
```

### Architectural Guarantees
1. **Zero UI Dependency**: Independent of Streamlit, session state, and reporting layout.
2. **Zero Model Bias**: Operates without inspecting model names (`model_id` is never used in classification decisions).
3. **Multiclass Support**: Never assumes binary labels ($y_{\text{orig}} \neq y_{\text{pert}}$ operates across arbitrary $K$-class models).
4. **Unit-Testable in Isolation**: 100% covered by synthetic calibration test cases in `tests/test_behavioral_taxonomy.py`.
