# BlindSpot Canonical Linguistic Probe Protocol (v2.2.0)

## 1. Executive Summary

In behavioral auditing of black-box NLP classifiers, consistency and reproducibility depend entirely on stimulus control. Prior versions of BlindSpot suffered from pipeline divergence where candidate probes generated in exploration did not strictly correspond to the stimuli executed during experiments. 

Under the **Canonical Probe Protocol (v2.2.0)**, BlindSpot enforces a unified, strongly-typed contract across the entire lifecycle:
$$\text{Generation} \longrightarrow \text{Selection / Verification} \longrightarrow \text{Execution} \longrightarrow \text{Analysis} \longrightarrow \text{Reporting}$$

The cardinal invariant of BlindSpot is:
$$\text{Generated Probes} \ge \text{Selected Probes} = \text{Planned Inferences} = \text{Executed Inferences} = \text{Analyzed Records} = \text{Reported Records}$$

---

## 2. Core Data Contracts

### 2.1 LinguisticProbe (`blindspot.core.types.LinguisticProbe`)
Every perturbation variant is represented by a strongly-typed `LinguisticProbe` instance:

```python
@dataclass
class LinguisticProbe:
    probe_id: str                    # Deterministic SHA-256 hash (16 chars)
    seed_text: str                   # Original unperturbed source text
    perturbed_text: str              # Transformed stimulus fed to models
    perturbation_type: str           # Canonical category (e.g., 'negation', 'intensity')
    description: str                 # Human-readable rule explanation
    expected_semantic_effect: str    # 'invert', 'preserve', 'strengthen', 'weaken', 'concession'
    expected_flip: bool              # True iff truth-conditions or polarity invert
    category: str                    # Category grouping
    name: str                        # Human-readable rule name
    semantic_intent: str             # Canonical SemanticIntent enum value
    status: str                      # 'GENERATED', 'VERIFIED', 'USER_EDITED', 'CUSTOM'
    transformation: str              # Description of exact syntactic transformation
    version: str = "2.2.0"           # Schema version
    subtype: Optional[str] = None    # Sub-operator identifier
    metadata: Dict[str, Any]         # Token indices, replacement tokens, rule IDs
```

### 2.2 Deterministic Probe Identification
To guarantee that heterogeneous models are audited against identically indexed stimuli, probe IDs are calculated deterministically via SHA-256:

$$\text{hash\_input} = \text{seed\_text} \parallel \text{perturbed\_text} \parallel \text{perturbation\_type} \parallel \text{expected\_semantic\_effect}$$
$$\text{probe\_id} = \text{SHA256}(\text{hash\_input})[:16]$$

This mathematical guarantee ensures:
1. Identical inputs and transformations yield identical IDs across runs and processes.
2. Distinct linguistic perturbations never collide.
3. Cross-model alignment tables can join evaluations reliably using `probe_id`.

### 2.3 SharedProbeSet (`blindspot.core.types.SharedProbeSet`)
A collection of probes shared across all evaluated models:

```python
@dataclass
class SharedProbeSet:
    probe_set_id: str                # Unique catalog instance ID
    seed_texts: List[str]            # List of original input sentences
    probes: List[LinguisticProbe]    # Ordered list of canonical probes
    created_at: float                # Generation timestamp
    probe_set_version: str = "2.2.0" # Schema version
    generator_version: str = "2.2.0" # Generator version
    sentence_types: Dict[str, str]   # Map of {seed_text: pragmatic_type}
```

Validation methods enforce:
- `validate()`: Verifies that no probe has an empty ID, no duplicate IDs exist within the set, and all required text fields are populated.
- `get_selected()`: Filters active probes staged for execution.
- `find_by_id(probe_id)`: Quick $O(1)$ or $O(N)$ probe lookup.

---

## 3. Separation of Concerns: Generation $\neq$ Selection $\neq$ Execution

1. **Generation (Probe Research Workbench)**:
   The perturber engines (`NegationPerturber`, `DoubleNegationPerturber`, `ConnectivePerturber`, `SynonymSubstitutionPerturber`, `IntensityPerturber`, `StructurePerturber`) synthesize candidate variants for a given seed text.
2. **Selection & Verification**:
   The researcher reviews candidate variants in the Workbench. Probes can be individually toggled, edited, or custom injected. Once reviewed, the researcher clicks **[Send to Experiment Lab]**, creating a frozen `SharedProbeSet` staged in session state.
3. **Execution (ExperimentRunner)**:
   When `ExperimentConfig.selected_probe_set` is populated, `ExperimentRunner` consumes it directly. **No re-generation occurs.** Exactly the selected probes are executed across all target models.

---

## 4. Standalone Baseline Evaluation

Before any probe perturbations are evaluated, `ExperimentRunner` evaluates each seed sentence in isolation, recording a dedicated `BaselineEvaluation`:

```python
@dataclass
class BaselineEvaluation:
    model_id: str
    seed_text: str
    sentence_type: str               # literal, proverb, idiom, figurative, sarcastic, ironic
    prediction: PredictionResult     # label, confidence, full probability distribution
    latency_ms: float
```

Every subsequent `ModelProbeEvaluation` records `original_prediction` from this baseline, ensuring that confidence deltas and label flips are measured relative to the verified seed stimulus.
