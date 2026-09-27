# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790551468_b787ce`
- **Run Plan Created**: `1790551468.85002`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`
- **Probe Set ID / Version**: `pset_1790551436_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 385.41s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "i am not well"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "i am not well..." | `LITERAL` | **NEGATIVE** | 0.9997 (100.0%) |
| `twitter-roberta-base-sentiment-latest` | "i am not well..." | `LITERAL` | **NEGATIVE** | 0.5709 (57.1%) |
| `twitter-roberta-base-sentiment` | "i am not well..." | `LITERAL` | **NEGATIVE** | 0.9266 (92.7%) |
| `albert-base-v2-SST-2` | "i am not well..." | `LITERAL` | **NEGATIVE** | 0.9941 (99.4%) |
| `bert-base-uncased-SST-2` | "i am not well..." | `LITERAL` | **NEGATIVE** | 0.9967 (99.7%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 2 (28.6%) | 0/2 (28.6%) | 5/5 (100.0%) | 85.7% | 0.1390 | -0.4 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 0/2 (28.6%) | 5/5 (100.0%) | 57.1% | 0.4099 | +11.6 pp |
| `twitter-roberta-base-sentiment` | 7 | 2 (28.6%) | 0/2 (28.6%) | 5/5 (100.0%) | 85.7% | 0.3438 | -15.1 pp |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 0/2 (28.6%) | 5/5 (100.0%) | 57.1% | 0.3403 | -8.2 pp |
| `bert-base-uncased-SST-2` | 7 | 2 (28.6%) | 0/2 (28.6%) | 5/5 (100.0%) | 85.7% | 0.1744 | -6.8 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 1 | 0 | 0 | 0 | 6 |
| `twitter-roberta-base-sentiment-latest` | 1 | 1 | 1 | 0 | 4 |
| `twitter-roberta-base-sentiment` | 1 | 0 | 0 | 0 | 6 |
| `albert-base-v2-SST-2` | 1 | 0 | 2 | 0 | 4 |
| `bert-base-uncased-SST-2` | 1 | 0 | 0 | 0 | 6 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 80.00%

### Pairwise Concordance Matrix
| Model | `Twitter-RoBERTa (Base)` | `Twitter-RoBERTa (Latest)` | `DistilBERT SST-2` | `ALBERT SST-2` | `BERT SST-2` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Twitter-RoBERTa (Base)` | 100.0% | 71.4% | 85.7% | 85.7% | 85.7% |
| `Twitter-RoBERTa (Latest)` | 71.4% | 100.0% | 57.1% | 57.1% | 57.1% |
| `DistilBERT SST-2` | 85.7% | 57.1% | 100.0% | 100.0% | 100.0% |
| `ALBERT SST-2` | 85.7% | 57.1% | 100.0% | 100.0% | 100.0% |
| `BERT SST-2` | 85.7% | 57.1% | 100.0% | 100.0% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |

## 8. Semantic Reference Methodology & Ground-Truth Alignment
1. **Canonical Semantic Label Space**: Ground-truth polarity is strictly confined to `POSITIVE`, `NEGATIVE`, and `NEUTRAL`. Non-canonical sentiment categories (such as `MIXED`, `AMBIGUOUS`, `SARCASTIC`) are rejected.
2. **Google Gemini Role**: Gemini operates exclusively as an external semantic annotator/verification layer for baseline and probe sentences. It is **never** a benchmark model, does not forecast model failures, and is strictly prohibited from generating the failure taxonomy.
3. **Human Verification & Override**: Every semantic reference can be verified and overridden by researchers (`[Accept]` / `[Change]`). Frozen semantic references are strictly immutable during model evaluation.
4. **Binary vs. Multiclass Alignment**: Binary models (e.g. 2-class SST-2) natively output `NEGATIVE` and `POSITIVE`. When semantic reference is `NEUTRAL`, binary models' forced polarity is recorded as `NOT_DIRECTLY_REPRESENTABLE` (`BINARY_FORCED_POLARITY`), preserving empirical truth rather than falsely modifying the reference.
5. **Independence of Model Outputs & Rule-Based Taxonomy**: Model predictions remain 100% empirical forward-pass outputs. The failure taxonomy (`Blind`, `Spurious`, `Misweighted`, `Undetermined`) is derived purely by deterministic rule-based behavioral analysis, completely independent of Gemini.