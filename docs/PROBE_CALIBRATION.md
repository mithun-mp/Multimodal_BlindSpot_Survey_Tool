# BlindSpot Calibrated Diagnostic Probe Suite & Pragmatic Calibration

## 1. Research Motivation & Diagnostic Coverage

Prior implementations generated perturbations solely to inflate probe counts, frequently emitting semantically weak variants where perturber types did not match taxonomy categories. 

The calibrated diagnostic probe framework ensures that **every probe has an explicit linguistic rationale**, balanced between:
1. **Expected-Change Probes**: Polarities, negations, and contrastive modifiers that must alter model predictions.
2. **Expected-Preserve Probes**: Lexical substitutions, double negations, and syntactic reorderings that must preserve predictions.

Without both classes in balanced proportions, a diagnostic suite cannot detect both Blindness (missing flips) and Spuriousness (unexpected flips).

---

## 2. Canonical 7-Probe Diagnostic Composition

For any input sentence, `SharedProbeGenerator` generates a deterministic, calibrated 7-probe candidate set adhering to canonical slots:

| Slot | Probe ID | Perturbation Category | Semantic Intent | Expected Effect | Expected Label Relation | Diagnostic Purpose |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **P001** | `prb_P001_*` | `negation_insertion` | `REVERSE_POLARITY` | `EXPECTED_FLIP` | `DIFFERENT_LABEL` | Tests syntactic negation sensitivity; diagnoses **Blind** behavior if label is preserved. |
| **P002** | `prb_P002_*` | `double_negation` | `PRESERVE_MEANING` | `EXPECTED_PRESERVE` | `SAME_LABEL` | Tests litotes understanding; diagnoses **Spurious** sensitivity if label flips. |
| **P003** | `prb_P003_*` | `intensity` (Intensifier) | `STRENGTHEN_POLARITY` | `EXPECTED_CONFIDENCE_INCREASE` | `SAME_LABEL` | Tests degree adverb processing; diagnoses **Misweighted** behavior if confidence drops or label flips. |
| **P004** | `prb_P004_*` | `intensity` (Downtoner) | `WEAKEN_POLARITY` | `EXPECTED_CONFIDENCE_DECREASE` | `SAME_LABEL` | Tests attenuator processing; diagnoses **Misweighted** behavior if confidence surges. |
| **P005** | `prb_P005_*` | `synonym_substitution` / `proverb_paraphrase` | `PRESERVE_MEANING` | `EXPECTED_PRESERVE` | `SAME_LABEL` | Tests lexical robustness and non-literal semantic preservation. |
| **P006** | `prb_P006_*` | `contrast_negative_append` | `SHIFT_CONTRAST` | `EXPECTED_FLIP` | `DIFFERENT_LABEL` | Tests discourse connective dominance ('X, but Y'); diagnoses **Blind** behavior if model ignores contrast clause. |
| **P007** | `prb_P007_*` | `structure` (Clause Inversion / Framing) | `PRESERVE_MEANING` | `EXPECTED_PRESERVE` | `SAME_LABEL` | Tests word order invariance and syntactic framing robustness. |

---

## 3. Proverb & Figurative Language Support

Special linguistic structures (proverbs, idioms, metaphors) cannot be audited using naive literal sentiment dictionaries. BlindSpot incorporates explicit pragmatic type tracking:
- `SentenceType.LITERAL`
- `SentenceType.PROVERB`
- `SentenceType.IDIOM`
- `SentenceType.FIGURATIVE`
- `SentenceType.SARCASTIC`
- `SentenceType.IRONIC`

### Curated Pragmatic Calibration: "All that glitters is not gold."
For the acceptance proverb *"All that glitters is not gold."*:
1. **Sentence Pragmatic Type**: `SentenceType.PROVERB`
2. **Baseline Evaluation**: Evaluated exactly once per model (DistilBERT predicts `NEGATIVE` with 0.9982 confidence).
3. **Calibrated Probes**:
   - `negation_removal`: *"All that glitters is gold."* $\to$ `REVERSE_POLARITY` / `EXPECTED_FLIP` (DistilBERT correctly flips to `POSITIVE`, 1.00).
   - `double_negation`: *"Not everything that glitters fails to be ungold."* $\to$ `PRESERVE_MEANING` / `EXPECTED_PRESERVE` (DistilBERT maintains `NEGATIVE`, 0.92).
   - `proverb_paraphrase`: *"Not everything that is shiny is truly valuable."* $\to$ `PRESERVE_MEANING` / `EXPECTED_PRESERVE` (DistilBERT maintains `NEGATIVE`, 1.00).
   - `contrast_negative_append`: *"All that glitters is not gold, however they do not improve over time."* $\to$ `SHIFT_CONTRAST` / `EXPECTED_FLIP` (DistilBERT retains `NEGATIVE` $\to$ diagnosed as **BLIND**).

---

## 4. Deterministic Acceptance Run (Section 37)

The calibration suite is validated deterministically in `tests/test_deterministic_acceptance.py`:
- **Candidate Set**: 7 generated candidate probes.
- **Selection**: Exactly 4 probes selected.
- **Models**: 2 models evaluated (`distilbert` and `roberta`).
- **Exact Model Inferences**:
  - 2 original baseline evaluations (1 per model).
  - $2 \times 4 = 8$ probe evaluations.
  - **Total Evaluations**: Exactly 10 inferences.
- **Count Integrity**:
  $$\text{Generated (7)} \to \text{Selected (4)} \to \text{Planned (4)} \to \text{Executed (4)} \to \text{Analyzed (4)} \to \text{Reported (4)}$$
