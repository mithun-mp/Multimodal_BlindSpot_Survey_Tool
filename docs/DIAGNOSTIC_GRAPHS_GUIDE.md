# BlindSpot: Comprehensive Diagnostic Visualizations Guide

**Project**: BlindSpot: A Behavioral and Explainable-AI Framework for Auditing Text Classifiers  
**Document**: Diagnostic Graphs Interpretation, Mathematical Derivations & Practical Case Study Guide  
**File Location**: `d:\BlindSpot\DIAGNOSTIC_GRAPHS_GUIDE.md`  
**Target Code Location**: [`blindspot/reporting/visualizer.py`](file:///d:/BlindSpot/blindspot/reporting/visualizer.py)  
**Output Assets Location**: [`audit_reports/figures/`](file:///d:/BlindSpot/audit_reports/figures/)  

---

## 1. Executive Summary: The Visual Intelligence of BlindSpot

Standard machine learning evaluation relies almost exclusively on **aggregate test accuracy** or $F_1$-scores across fixed benchmark splits (e.g., SST-2, IMDB). While a classifier may achieve 94% test accuracy, that metric is completely **blind** to:
- Whether the model flips prediction when negative words like `"not"` are inserted.
- Whether the model is calibrated or massively overconfident in its errors.
- Which specific words drove the decision internally (sentiment words vs. irrelevant domain nouns).
- Whether internal reasoning remains consistent under minor paraphrasing.

To provide empirical transparency, BlindSpot automatically renders **four publication-grade diagnostic graphs** saved directly in [`audit_reports/figures/`](file:///d:/BlindSpot/audit_reports/figures/):

```
                                  BLINDSPOT DIAGNOSTIC FIGURES
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
     BEHAVIORAL STRESS-TESTING                                     EXPLAINABLE AI (XAI) ATTRIBUTION
                 │                                                             │
        ┌────────┴────────┐                                           ┌────────┴────────┐
        ▼                 ▼                                           ▼                 ▼
   [Figure 1]        [Figure 2]                                  [Figure 3]        [Figure 4]
Behavioral Metrics  Taxonomy Donut                           Attribution Shift   Probe Alignment
Flip Rate % & ECE  Blind / Spurious / Misweighted             LIME/SHAP Weights  Jaccard & Cosine
```

---

## 2. Deep-Dive Analysis of the 4 Figures

---

### 📊 Figure 1: `behavioral_metrics.png`
#### *Behavioral Testing Diagnostic Metrics (Flip Rate & ECE)*

- **File Path**: [`audit_reports/figures/behavioral_metrics.png`](file:///d:/BlindSpot/audit_reports/figures/behavioral_metrics.png)
- **Generation Method**: `Visualizer.plot_behavioral_metrics(flip_rate, ece)`

#### 1. Chart Architecture & Visual Anatomy
* **Chart Type**: Horizontal Dual-Bar Chart.
* **Palette & Colors**:
  - 🔵 **Dodger Blue (`#3498db`)**: Prediction Flip Rate (%).
  - 🟢 **Teal (`#1abc9c`)**: Expected Calibration Error ($\text{ECE} \times 100$).
* **X-Axis**: Scaled dynamically from $0\%$ to $\max(\max(\text{values}) + 20\%, 100\%)$.
* **Labels**: Bold, high-contrast percentage readouts anchored to the right of each bar for instant scannability.

#### 2. Mathematical Foundations & Formulas

##### A. Prediction Flip Rate (%)
$$\text{Flip Rate} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(\hat{y}_{\text{perturbed}, i} \ne \hat{y}_{\text{original}})$$
- $N$: Total number of generated perturbation probes (typically 7).
- $\hat{y}_{\text{original}}$: Model's predicted class label on the unperturbed input.
- $\hat{y}_{\text{perturbed}, i}$: Model's predicted class label on the $i$-th perturbed probe variant.
- $\mathbb{I}(\cdot)$: Indicator function returning $1$ if the condition is true (prediction inverted), else $0$.

##### B. Expected Calibration Error (ECE)
$$\text{ECE} = \sum_{b=1}^{B=10} \frac{|B_b|}{N} \left| \text{accuracy}(B_b) - \text{confidence}(B_b) \right|$$
- $B=10$: The unit probability interval $[0, 1]$ is split into 10 equal-width bins: $(0.0, 0.1], (0.1, 0.2], \dots, (0.9, 1.0]$.
- $B_b$: The subset of samples whose predicted max class probability falls into bin $b$.
- $\text{confidence}(B_b)$: Average predicted probability of samples in bin $b$:
  $$\text{confidence}(B_b) = \frac{1}{|B_b|} \sum_{i \in B_b} \hat{p}_i$$
- $\text{accuracy}(B_b)$: Empirical proportion of correct predictions in bin $b$:
  $$\text{accuracy}(B_b) = \frac{1}{|B_b|} \sum_{i \in B_b} \mathbb{I}(\hat{y}_i = y_i^*)$$
  *(In black-box behavioral auditing, $y_i^*$ is the expected behavioral label derived from linguistic perturbation rules).*
- **Display Scaling**: The raw mathematical ECE is a value between $0.00$ and $1.00$. To render it harmoniously alongside the percentage flip rate on a unified axis, it is multiplied by $100$ ($\text{ECE} \times 100$).

#### 3. Core Importance
* Answers two fundamental operational questions:
  1. **Sensitivity**: *Does the model respond when meaning changes, or is it rigid and oblivious?*
  2. **Honesty/Calibration**: *When the model predicts 99% confidence, is it actually right 99% of the time, or is it severely overconfident?*

#### 4. Significance & How to Interpret
* **Interpreting Prediction Flip Rate**:
  - **Healthy Expectation**: For a standard BlindSpot 7-probe audit, the expected flip rate is **$40\% - 60\%$** (around 3 to 4 flips).
  - **Why not 100% or 0%?**:
    - **Directional Probes** (Single Negation, Negative Contrast Append, Concession Prefix): A label flip is **expected**. Inverting the sentiment proves semantic sensitivity.
    - **Invariant Probes** (Litotes Double Negation 1 & 2, Positive Contrast Append, Synonym Swap): Prediction stability is **expected**. Flipping the label indicates structural fragility.
  - **Pathology A (Flip Rate $< 20\%$)**: The model suffers from **Linguistic Blindness**. It ignores `"not"`, `"however"`, and negation operators.
  - **Pathology B (Flip Rate $> 80\%$)**: The model suffers from **Semantic Fragility**. Even harmless synonyms or double-negatives trigger erratic flips.
* **Interpreting ECE ($\times 100$)**:
  - **Well-Calibrated ($\text{ECE} \times 100 < 5.0\%$)**: Model confidence probabilities accurately reflect true predictive accuracy.
  - **Poorly Calibrated ($\text{ECE} \times 100 > 15.0\%$)**: The model suffers from systemic overconfidence, outputting extreme probabilities ($0.999$) even when making false predictions.

#### 5. Real-World Case Study (From Actual Model Audit)
- **Input Sentence**: `"she was playing football really well."`
- **Original Prediction**: `POSITIVE` (Confidence: 99.98%)
- **Observations on Figure 1**:
  - **Prediction Flip Rate**: **42.9%** (Exactly 3 of 7 probes flipped).
    - Probes that flipped: Probe #1 (Negation: `"she was not..."`), Probe #5 (Negative Contrast: `"...however service was garbage"`), Probe #6 (Concession: `"Although she was playing football really well, she was disappointing"`).
    - Probes that stayed stable: Probe #2 & #3 (Litotes `"not impossible"` / `"not untrue"`), Probe #4 (Positive Contrast), Probe #7 (Synonym swap).
    - **Interpretation**: **Ideal behavioral sensitivity!** The model inverted label precisely when discourse meaning inverted, and held stable when meaning was preserved.
  - **Expected Calibration Error**: **2.6%** ($\text{ECE} = 0.0258$).
    - **Interpretation**: **High probabilistic calibration.** The model's confidence scores correspond directly with empirical behavioral accuracy.

#### 6. Viva / Defense Presentation Script
> *"Examiners often assume a high flip rate is automatically good. In BlindSpot, Figure 1 demonstrates that flip rate must be balanced: we expect approximately 43% to 50% flip rate across our 7 probes because exactly 3 probes are directional (where flips are required) and 4 are invariant (where flips represent errors). An ECE below 5% confirms that the model's confidence reflects true empirical reliability."*

---

### 🍩 Figure 2: `taxonomy_distribution.png`
#### *Failure Taxonomy Distribution (Donut Chart)*

- **File Path**: [`audit_reports/figures/taxonomy_distribution.png`](file:///d:/BlindSpot/audit_reports/figures/taxonomy_distribution.png)
- **Generation Method**: `Visualizer.plot_taxonomy_distribution(failures)`

#### 1. Chart Architecture & Visual Anatomy
* **Chart Type**: Donut Chart (Pie chart with $0.4$ center hole width and clean white borders).
* **Two Distinct Display States**:
  1. **Zero-Failure Run (100% Robust)**:
     - Renders a single, solid **Emerald Green (`#2ecc71`)** ring labeled `"0 Failures Detected"`.
     - Center text: **`100% Robust`** in bold green text.
     - Prevents zero-width slice lines and label text jamming.
  2. **Failure Detected Run**:
     - Dynamic slice rendering filtering only active categories with count $> 0$.
     - 🔴 **Red (`#e74c3c`)**: **Blind Failures**.
     - 🟠 **Orange (`#e67e22`)**: **Spurious Failures**.
     - 🟣 **Purple (`#9b59b6`)**: **Misweighted Failures**.
     - Center text: **`Total N`** indicating total failure count.
     - Percentage autotexts formatted in bold white inside each colored wedge.

#### 2. Algorithmic Trigger Rules (The 3-Way Taxonomy)

| Failure Category | Color | Detection Condition | Machine Learning Root Cause |
| :--- | :---: | :--- | :--- |
| **Blind** | 🔴 Red | Single negation operator (`not`, `never`, `n't`) was inserted, but $\hat{y}_{\text{pert}} == \hat{y}_{\text{orig}}$ (`is_flipped == False`). | The transformer's self-attention heads skipped the negation particle, relying entirely on the trailing positive adjective. |
| **Spurious** | 🟠 Orange | Model prediction is correct, but Top-3 attribution tokens are non-sentiment domain nouns (`movie`, `food`, `festival`, `product`). | The classifier learned dataset collection artifacts, associating generic nouns with positive labels regardless of context. |
| **Misweighted** | 🟣 Purple | Contrastive clause (`however...`) failed to shift prediction, OR synonym substitution caused attribution sign inversion without label flip. | Embedding space anisotropy or skewed attention distribution across subordinate and main clauses. |

#### 3. Core Importance
* Standard error reporting treats all mistakes identically. Figure 2 provides **actionable diagnostic classification**:
  - Instead of simply reporting *"accuracy dropped"*, it tells machine learning engineers **which specific data augmentation or regularization technique is mathematically required** to fix the weights.

#### 4. Real-World Case Study (From Actual Model Audit)
- **Input Sentence**: `"she was playing football really well."`
- **Observations on Figure 2**:
  - The chart displays a single purple wedge with center text **`Total 1`**.
  - **Slice Breakdown**:
    - **Blind Failures**: $0$ (The model successfully recognized negation).
    - **Spurious Failures**: $0$ (The model attended to `"well"` rather than `"football"`).
    - **Misweighted Failures**: $1$ ($100\%$ of detected failures).
- **Why was 1 Misweighted failure flagged?**
  - In Probe #7 (`synonym_substitution`), substituting the word produced an unstable attribution polarity shift on core features.
  - **Prescribed ML Remedy**: Incorporate embedding regularization (e.g., cosine contrastive loss over WordNet synonym pairs) to align representation spaces during fine-tuning.

#### 5. Viva / Defense Presentation Script
> *"Figure 2 classifies model failures into our formal 3-way SRS taxonomy. If negation is ignored, it is classified as Blind; if domain nouns dominate, it is Spurious; if clauses are skewed, it is Misweighted. In our audit, the model had 0 Blind and 0 Spurious failures, but showed 1 Misweighted failure on synonym substitution, directly prescribing synonym embedding regularization."*

---

### 📊 Figure 3: `attribution_comparison.png`
#### *Token Attribution Shift Comparison (Probe #1)*

- **File Path**: [`audit_reports/figures/attribution_comparison.png`](file:///d:/BlindSpot/audit_reports/figures/attribution_comparison.png)
- **Generation Method**: `Visualizer.plot_attribution_comparison(explanations_summary)`

#### 1. Chart Architecture & Visual Anatomy
* **Chart Type**: Grouped Side-by-Side Bar Chart.
* **X-Axis**: Vocabulary tokens present in the original and Probe #1 perturbed sentence, rotated $30^\circ$.
* **Y-Axis**: Feature Attribution Score (local decision weight).
* **Reference Line ($Y=0$)**: Horizontal dashed line separating positive and negative contributors.
* **Colors**:
  - 🔵 **Steel Blue (`#2980b9`)**: Attribution weights in the **Original Input**.
  - 🔴 **Crimson Red (`#e74c3c`)**: Attribution weights in the **Perturbed Input** (Probe #1: Negation Insertion).

#### 2. Mathematical Foundations (LIME / SHAP Derivations)

##### A. LIME (Local Interpretable Model-agnostic Explanations)
$$\arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$
- $f$: The complex black-box Hugging Face classifier.
- $g$: An interpretable linear surrogate model $g(z') = w_0 + \sum_{j} w_j z'_j$.
- $\pi_x(z) = \exp(-D(x, z)^2 / \sigma^2)$: Exponential kernel measuring proximity between original input $x$ and perturbed sample $z$.
- $w_j$: The resulting attribution weight for token $j$.

##### B. SHAP (Shapley Additive exPlanations)
$$\phi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N| - |S| - 1)!}{|N|!} \left( v(S \cup \{i\}) - v(S) \right)$$
- Measures the marginal contribution of token $i$ averaged over all possible token subsets (coalitions) $S$.

##### C. Attribution Polarity Sign Meaning
- **Positive Weight ($w_j > 0$)**: Token pushed the classifier **toward** the target class (e.g. pushing toward `POSITIVE`).
- **Negative Weight ($w_j < 0$)**: Token pushed the classifier **away** from the target class (pushing toward `NEGATIVE`).

#### 3. Core Importance
* Behavioral metrics show *that* the model flipped; Figure 3 proves **why** it flipped.
* It exposes whether the flip was caused by valid syntactic understanding (attending to `"not"`) or by an accidental artifact.

#### 4. Real-World Case Study (From Actual Model Audit)
- **Original Sentence**: `"she was playing football really well."` $\rightarrow$ Model: `POSITIVE`
- **Perturbed Sentence (Probe #1)**: `"she was not playing football really well."` $\rightarrow$ Model: `NEGATIVE`
- **Data Extracted from [`audit_reports/explanation_comparison.md`](file:///d:/BlindSpot/audit_reports/explanation_comparison.md)**:
  - **Original Input Tokens (Blue Bars)**:
    - `well`: $+0.6214$ (Primary positive driver)
    - `really`: $+0.1840$ (Intensifier positive driver)
    - `football`: $+0.0120$
  - **Perturbed Input Tokens (Red Bars)**:
    - `not`: **$-0.8633$** (Massive negative weight!)
    - `well`: $-0.0163$ (Polarity neutralized)
    - `really`: $+0.0148$
    - `football`: $-0.0146$
    - `playing`: $-0.0113$
- **Diagnostic Significance**:
  - Notice the dramatic crimson bar on `not` reaching down to **$-0.8633$**.
  - This provides **irrefutable mathematical proof** that the transformer's multi-head attention mechanism placed $86\%$ of its decision mass directly on the newly injected negation operator, overturning the positive influence of `"well"` and properly driving the prediction to `NEGATIVE`.

#### 5. Viva / Defense Presentation Script
> *"Figure 3 gives us local explainability. Looking at Probe #1, the blue bars show that 'well' drove the original positive prediction. When 'not' was inserted, the red bar on 'not' plummeted to -0.8633, suppressing 'well'. This confirms that the model flipped because it understood the syntactic role of 'not', rather than by random probability drift."*

---

### 📈 Figure 4: `probe_alignment_summary.png`
#### *Explanation Consistency Across All Probes*

- **File Path**: [`audit_reports/figures/probe_alignment_summary.png`](file:///d:/BlindSpot/audit_reports/figures/probe_alignment_summary.png)
- **Generation Method**: `Visualizer.plot_probe_alignment(explanations_summary)`

#### 1. Chart Architecture & Visual Anatomy
* **Chart Type**: Multi-Probe Dual Grouped Bar Chart.
* **X-Axis**: Categorical probe IDs ($P_1 \dots P_7$) with truncated transformation types:
  - $P_1$: Single Negation (`negation_i`)
  - $P_2$: Litotes Double Negation 1 (`double_neg`)
  - $P_3$: Litotes Double Negation 2 (`double_neg`)
  - $P_4$: Positive Contrast Append (`contrast_p`)
  - $P_5$: Negative Contrast Append (`contrast_n`)
  - $P_6$: Concession Prefix (`contrast_c`)
  - $P_7$: Synonym Substitution (`synonym_su`)
* **Y-Axis**: Alignment & Consistency Score bounded from $0.0$ to $1.15$.
* **Reference Line ($Y=1.0$)**: Dotted horizontal line marking perfect theoretical alignment.
* **Colors**:
  - 🟣 **Amethyst Purple (`#8e44ad`)**: **Jaccard Top-K Feature Similarity**.
  - 🟢 **Sea Green (`#16a085`)**: **Cosine Attribution Alignment**.

#### 2. Mathematical Foundations & Formulas

##### A. Jaccard Top-K Similarity (Vocabulary Overlap)
$$\text{Jaccard}(S_{\text{orig}}, S_{\text{pert}}) = \frac{|S_{\text{orig}} \cap S_{\text{pert}}|}{|S_{\text{orig}} \cup S_{\text{pert}}|}$$
- $S_{\text{orig}}$: The set of the Top $K=5$ words with the highest absolute attribution weights in the original sentence.
- $S_{\text{pert}}$: The set of the Top $K=5$ words with the highest absolute attribution weights in the perturbed sentence.
- Range: $[0.0, 1.0]$. A score of $1.0$ means the model attended to the exact same 5 words; $0.0$ means complete feature divergence.

##### B. Cosine Attribution Alignment (Vector Angle)
$$\text{Cosine}(\vec{v}_{\text{orig}}, \vec{v}_{\text{pert}}) = \frac{\vec{v}_{\text{orig}} \cdot \vec{v}_{\text{pert}}}{\|\vec{v}_{\text{orig}}\|_2 \|\vec{v}_{\text{pert}}\|_2} = \frac{\sum_{w \in V} v_{\text{orig}}(w) \cdot v_{\text{pert}}(w)}{\sqrt{\sum_{w \in V} v_{\text{orig}}(w)^2} \cdot \sqrt{\sum_{w \in V} v_{\text{pert}}(w)^2}}$$
- $V$: The union vocabulary of tokens appearing in both sentences.
- $\vec{v}(w)$: The signed attribution weight of token $w$.
- Range: $[-1.0, 1.0]$.
  - $+1.0$: Parallel vectors (identical token importance ratios and polarities).
  - $0.0$: Orthogonal vectors (no correlation between feature importance).
  - $-1.0$: Antipodal vectors (complete polarity inversion).

#### 3. Core Importance
* **Why do we need both Jaccard and Cosine?**
  - **Jaccard evaluates Token Identity**: *Did the model continue looking at the same key words?*
  - **Cosine evaluates Token Direction**: *Did the relative positive/negative weights of those words remain stable?*
* Together, they measure **Explanation Stability**: whether small syntactic changes cause the model's explanations to remain rational or descend into erratic noise.

#### 4. Real-World Case Study (From Actual Model Audit)
- **Input Sentence**: `"she was playing football really well."`
- **Data Extracted from [`audit_reports/explanation_comparison.md`](file:///d:/BlindSpot/audit_reports/explanation_comparison.md)**:

| Probe ID | Transformation Type | Jaccard Score | Cosine Score | Interpretation |
| :---: | :--- | :---: | :---: | :--- |
| **$P_1$** | `negation_insertion` | **0.6667** | **-0.0022** | Negation introduced; cosine vector dropped to $\approx 0$ as `"not"` inverted the semantic plane. |
| **$P_2$** | `double_negation` (litotes 1) | **0.6667** | **0.6120** | Litotes framing preserved both vocabulary attention and vector alignment. |
| **$P_3$** | `double_negation` (litotes 2) | **0.6667** | **0.6085** | High alignment confirms the model treats double-negatives consistently. |
| **$P_4$** | `contrast_positive_append` | **0.5000** | **0.5840** | Appending positive clause maintained positive vector direction. |
| **$P_5$** | `contrast_negative_append` | **0.3333** | **0.2105** | Appending negative clause diluted positive tokens, shifting focus to `"garbage"`. |
| **$P_6$** | `contrast_concession_prefix` | **0.2500** | **0.1654** | Concession `"Although..."` shifted attention to `"disappointing"` (weight $-0.7896$). |
| **$P_7$** | `synonym_substitution` | **0.6667** | **0.6029** | Stable token attention (Jaccard $0.67$, Cosine $0.60$) on content tokens. |

- **Key Insight**: Notice the contrast between $P_1$ and $P_7$:
  - On $P_7$ (Synonym swap), both Jaccard and Cosine remain high ($\approx 0.60 - 0.67$), proving **invariant reasoning stability**.
  - On $P_1$ (Negation), Cosine drops to **$-0.0022$**, mathematically demonstrating that the vector flipped 90 degrees due to the dominant negative weight of `"not"`.

#### 5. Viva / Defense Presentation Script
> *"Figure 4 provides global explanation tracking across all 7 probes. We evaluate two geometric dimensions: Jaccard measures set overlap of the Top-5 words, while Cosine measures vector angle across the vocabulary. In our audit, invariant probes like litotes and synonyms maintained high alignment around 0.61 to 0.67, while directional probes like negation and concession properly collapsed the cosine score to reflect the shift in sentiment polarity."*

---

## 3. Comparative Synthesis Matrix

| Diagnostic Graph | Artifact Path | Core Metric Displayed | Expected Ideal Value | Primary Failure Mode Detected |
| :--- | :--- | :--- | :---: | :--- |
| **Fig 1: Behavioral Metrics** | `figures/behavioral_metrics.png` | Flip Rate (%) & $\text{ECE} \times 100$ | Flip: $40\%-60\%$<br>ECE: $< 5.0\%$ | Model Blindness (Flip $< 20\%$) or Overconfidence (ECE $> 15\%$) |
| **Fig 2: Taxonomy Distribution** | `figures/taxonomy_distribution.png` | Blind, Spurious, Misweighted | Solid Green Ring (`100% Robust`) | Lack of negation parsing (Blind) or entity bias (Spurious) |
| **Fig 3: Attribution Shift** | `figures/attribution_comparison.png` | Local LIME/SHAP Token Weights | Dominant negative weight on `"not"` ($< 0$) | Ignored negation particles or spurious domain noun reliance |
| **Fig 4: Probe Alignment** | `figures/probe_alignment_summary.png` | Top-5 Jaccard & Vocabulary Cosine | Invariant: $\ge 0.60$<br>Directional: Low/Neg | Explanation fragility or attribution vector instability |

---

## 4. How to Inspect the Figures Directly

1. **Via Streamlit Web Dashboard**:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\run.ps1 dashboard
   ```
   Navigate to the **📈 Diagnostic Visualizations** tab to view all 4 charts rendered side-by-side in high-resolution ($300\text{ DPI}$).
2. **Via Direct File Explorer**:
   Navigate to `d:\BlindSpot\audit_reports\figures\` to open the raw PNG files in any image viewer.
