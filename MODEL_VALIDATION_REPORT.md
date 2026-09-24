# BLINDSPOT — MODEL VALIDATION REPORT
**Generated**: September 20, 2026  
**Auditor**: BlindSpot Research Integrity Gate  
**Task Domain**: Sentiment Robustness Benchmark (`SENTIMENT`)  
**Runtime**: Python 3.13.14 (Windows AMD64), PyTorch 2.14.0+cpu, Transformers 4.49.0  

---

## 1. Executive Summary

This report documents the rigorous pre-benchmark validation of candidate models for the BlindSpot behavioral robustness testing framework. In compliance with research integrity requirements, every candidate model must pass an automated, deterministic pre-registration gate before admission into the active benchmark suite.

### Key Decisions & Actions:
1. **Rejection of `roberta-base-openai-detector`**:
   - Reclassified with task `AI_TEXT_DETECTION` and labels `["Fake", "Real"]`.
   - Strictly rejected from sentiment robustness benchmarks. No label remapping (`Fake` -> `Negative`, `Real` -> `Positive`) is permitted.
2. **Admission of 5 Validated Sentiment Models**:
   - 5 models representing distinct architectures (DistilBERT, ALBERT, RoBERTa-Twitter-Latest, BERT, and RoBERTa-Twitter-Base) passed all 6 validation criteria.
3. **Exclusion of Incompatible/Broken Checkpoints**:
   - `jbeno/electra-base-classifier-sentiment`: Saved with custom MLP head (`classifier.layers.*`) incompatible with standard HuggingFace `ElectraClassificationHead`, leaving head uninitialized. Excluded.
   - `sileod/deberta-v3-base-tasksource-sentiment`: Disentangled attention relies on `torch.jit.script` causing deprecation deadlock / failure on Python 3.13. Excluded.
   - `cardiffnlp/twitter-xlm-roberta-base-sentiment`: Standard checkpoint files unavailable on current hub mirror. Excluded.

---

## 2. Model Validation Gate Criteria

Each model must deterministically satisfy six mandatory conditions to enter the benchmark:

| Gate | Check | Condition | Failure Action |
|---|---|---|---|
| **G1** | Task Compatibility | `spec.task == "SENTIMENT"` | Reject model immediately |
| **G2** | Non-Sentiment Isolation | Model ID does not contain `detector` or detection labels | Reject model immediately |
| **G3** | Label Cardinality | `num_classes >= 2` | Reject model |
| **G4** | Label Semantics & Mapping | `id2label` exists, semantics documented (e.g. Negative/Positive) | Reject model |
| **G5** | Numerical Predictions | Model produces valid logits, non-trivial probability distribution | Reject model |
| **G6** | Architecture & Parameters | Valid architecture class and parameter count determined | Reject model |

---

## 3. Active 5-Model Sentiment Benchmark Suite

| # | Model ID | Architecture | Classes | Labels | Parameters | Domain | License | Gate Status |
|---|---|---|---|---|---|---|---|---|
| **M1** | `distilbert-base-uncased-finetuned-sst-2-english` | `DistilBertForSequenceClassification` | 2 | NEGATIVE, POSITIVE | 66.96M | SST-2 (Movie Reviews) | Apache-2.0 | **VALID** |
| **M2** | `textattack/albert-base-v2-SST-2` | `AlbertForSequenceClassification` | 2 | NEGATIVE, POSITIVE | 11.68M | SST-2 (Movie Reviews) | Apache-2.0 | **VALID** |
| **M3** | `cardiffnlp/twitter-roberta-base-sentiment-latest` | `RobertaForSequenceClassification` | 3 | NEGATIVE, NEUTRAL, POSITIVE | 124.65M | Social Media (Tweets) | MIT | **VALID** |
| **M4** | `textattack/bert-base-uncased-SST-2` | `BertForSequenceClassification` | 2 | NEGATIVE, POSITIVE | 109.48M | SST-2 (Movie Reviews) | Apache-2.0 | **VALID** |
| **M5** | `cardiffnlp/twitter-roberta-base-sentiment` | `RobertaForSequenceClassification` | 3 | NEGATIVE, NEUTRAL, POSITIVE | 124.65M | Social Media (Tweets) | MIT | **VALID** |

---

## 4. Empirical Diagnostics Across Standard Benchmark Sentences

All models were evaluated across five standardized diagnostic sentences testing basic polarity, neutral nuance, double negation, and figurative/proverbial language:
- **S1**: *"I loved the movie."* (Strong Positive)
- **S2**: *"I hated the movie."* (Strong Negative)
- **S3**: *"The movie was okay."* (Mild/Neutral Polarity)
- **S4**: *"I don't think the movie was not entirely without merit."* (Complex Double Negation)
- **S5**: *"All that glitters is not gold."* (Figurative Idiom / Negative implication)

### Diagnostic Results Table

| Sentence | DistilBERT (M1) | ALBERT (M2) | RoBERTa-Latest (M3) | BERT Base (M4) | RoBERTa-Base (M5) | OpenAI Detector (Rejected) |
|---|---|---|---|---|---|---|
| **S1: "I loved the movie."** | POSITIVE (0.9999) | POSITIVE (0.9997) | POSITIVE (0.9805) | POSITIVE (0.9995) | POSITIVE (0.9886) | FAKE (0.8962) ❌ |
| **S2: "I hated the movie."** | NEGATIVE (0.9997) | NEGATIVE (0.9990) | NEGATIVE (0.9183) | NEGATIVE (0.9990) | NEGATIVE (0.9782) | FAKE (0.8246) ❌ |
| **S3: "The movie was okay."** | POSITIVE (0.9998) | POSITIVE (0.9865) | POSITIVE (0.8963) | POSITIVE (0.9929) | POSITIVE (0.8830) | FAKE (0.9314) ❌ |
| **S4: Double Negation** | POSITIVE (0.9980) | POSITIVE (0.8281) | NEUTRAL (0.4985) | POSITIVE (0.9827) | NEUTRAL (0.7142) | FAKE (0.8488) ❌ |
| **S5: "All that glitters is not gold."** | NEGATIVE (0.9982) | NEGATIVE (0.9754) | NEUTRAL (0.5113) | NEGATIVE (0.9968) | NEUTRAL (0.6038) | FAKE (0.6106) ❌ |

---

## 5. Excluded and Incompatible Models

### A. `roberta-base-openai-detector`
- **Assigned Task**: `AI_TEXT_DETECTION`
- **Output Labels**: `["Fake", "Real"]`
- **Parameter Count**: 124.65M (`RobertaForSequenceClassification`)
- **Diagnostic Behavior**: Predicted `Fake` with 61% to 93% confidence across all sentiment sentences.
- **Audit Finding**: Completely irrelevant to sentiment analysis. Previously masqueraded as a sentiment model by silently mapping `Fake` to `Negative` and `Real` to `Positive`.
- **Validation Status**: **REJECTED (INELIGIBLE)**.

### B. `jbeno/electra-base-classifier-sentiment`
- **Assigned Task**: `SENTIMENT`
- **Architecture**: ELECTRA Base (`ElectraForSequenceClassification`)
- **Defect Description**: The checkpoint was saved with a custom sequential MLP classifier head (`classifier.layers.0`, `classifier.layers.3`, `classifier.layers.6`). Standard HuggingFace `ElectraForSequenceClassification` expects `classifier.dense` and `classifier.out_proj`. Loading through standard Hugging Face pipelines leaves the classification head randomly initialized, producing uniform random output probabilities (~0.34 to ~0.37) on all inputs.
- **Validation Status**: **REJECTED (CHECKPOINT_HEAD_MISMATCH)**.

### C. `sileod/deberta-v3-base-tasksource-sentiment`
- **Assigned Task**: `SENTIMENT`
- **Architecture**: DeBERTa-v3 (`DebertaV2ForSequenceClassification`)
- **Defect Description**: In Python 3.13 / PyTorch 2.14+, `DebertaV2SelfAttention` invokes `torch.jit.script` for disentangled relative attention, triggering a deprecation failure and runtime deadlock.
- **Validation Status**: **REJECTED (RUNTIME_INCOMPATIBLE)**.

### D. `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- **Assigned Task**: `SENTIMENT`
- **Architecture**: XLM-RoBERTa (`XLMRobertaForSequenceClassification`)
- **Defect Description**: Standard `pytorch_model.bin` / `model.safetensors` weight files unavailable in current local cache and upstream mirror.
- **Validation Status**: **REJECTED (MISSING_WEIGHTS)**.

---

## 6. Verification Audit Conclusion

The 5-model active benchmark suite (`DistilBERT`, `ALBERT`, `RoBERTa-Twitter-Latest`, `BERT-Base`, `RoBERTa-Twitter-Base`) provides:
1. **Architectural Diversity**: DistilBERT (student distillation), ALBERT (cross-layer parameter sharing & factorized embeddings), BERT Base (standard masked language model), and RoBERTa (optimized byte-pair encoding pretraining).
2. **Label Diversity**: Binary sentiment classification (`NEGATIVE` / `POSITIVE`) alongside ternary sentiment classification (`NEGATIVE` / `NEUTRAL` / `POSITIVE`).
3. **Domain Diversity**: Formal review corpora (SST-2) alongside informal microblog corpora (Twitter).
4. **100% Real Inference**: Strict pipeline verification guarantees zero silent heuristic fallbacks during robustness benchmarking.
