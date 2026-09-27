# BlindSpot Probe Execution Contract

## 1. Overview and Scientific Purpose

This contract defines the execution invariants that govern the BlindSpot benchmark runner.
The goal is complete experimental reproducibility, data provenance, and behavioral isolation across heterogeneous sentiment classifiers.

---

## 2. Immutable Baseline Contract

1. **Single Evaluation Anchor**:
   For every unique pair of $(\text{model\_id}, \text{seed\_text})$, the baseline prediction must be evaluated exactly once.
2. **Deterministic Baseline Identifier**:
   Each baseline evaluation is assigned an immutable `baseline_id` computed via:
   $$\text{baseline\_id} = \text{base\_}\text{SHA256}(\text{model\_id} \parallel \text{seed\_text})[:12]$$
3. **Immutability Invariant**:
   All subsequent probe evaluations for that model and seed text must reference this exact `baseline_id`.
   The baseline probability distribution, confidence, and predicted `SemanticPolarity` serve as the fixed point of comparison for all $\Delta \text{confidence}$ and polarity transition calculations.

---

## 3. Strict Probe Lifecycle Contract

BlindSpot strictly enforces three decoupled stages in the probe lifecycle:

$$\text{Generation} \longrightarrow \text{Selection / Staging (RunPlan)} \longrightarrow \text{Execution}$$

1. **Stage 1: Generation (`SharedProbeGenerator`)**:
   - Generates linguistic probe candidates from seed texts with stable probe identifiers:
     $$\text{probe\_id} = \text{prb\_}\text{SHA256}(\text{seed\_text} \parallel \text{perturbed\_text} \parallel \text{perturbation\_type} \parallel \text{expected\_effect})[:12]$$
   - Probes are packaged into an immutable `SharedProbeSet`.
2. **Stage 2: Staging (`RunPlan`)**:
   - The user or benchmark protocol stages a specific set of probe IDs: `selected_probe_ids`.
   - An immutable `RunPlan` is persisted to disk before any model forward pass begins.
3. **Stage 3: Execution (`ExperimentRunner` & `BehavioralTester`)**:
   - Execution runners must consume the exact staged probes.
   - **Zero Re-Generation**: The runner is strictly prohibited from silently re-generating probes or mutating text strings during model execution.
   - **Pipeline Integrity Validation**:
     Before persisting model results, the runner validates:
     $$\text{set}(\text{executed\_probe\_ids}) == \text{set}(\text{run\_plan.selected\_probe\_ids})$$
     Any violation triggers an immediate `RuntimeError` and blocks artifact persistence.

---

## 4. Lazy Explainability Contract

1. **Inference-First Priority**:
   Full behavioral auditing and failure taxonomy classification are performed strictly from forward inference outputs ($\text{probabilities}$, $\text{labels}$, $\text{confidences}$).
2. **Bounded Attributions**:
   LIME and SHAP token attributions are computationally expensive ($O(N \times K)$ model passes).
   Attribution generation is executed lazily:
   - Only when explicitly requested (`explainer_type != "none"`).
   - Only for probes exhibiting diagnosed behavioral failures (`BLIND`, `SPURIOUS`, `MISWEIGHTED`) or up to a pre-allocated sample cap (`explanation_sample_size`).

---

## 5. Non-Normative Cross-Model Reporting Contract

1. **Descriptive, Not Normative**:
   Cross-model comparisons present empirical behavioral fingerprints, pairwise prediction agreement matrices, and failure taxonomy distributions.
2. **Prohibition of Rankings**:
   The reporting subsystem must never assign a single aggregate "score", declare "best/worst" models, or rank classifiers into winners and losers.
   Models trained on different domains (e.g., SST-2 movie reviews vs Twitter social media) exhibit distinct domain-appropriate trade-offs that aggregate rankings distort.
