# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790528043_5b3eeb`
- **Run Plan Created**: `1790528043.872931`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790527601_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 711.44s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "the movie was great and the acting was top notch"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "the movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9999 (100.0%) |
| `albert-base-v2-SST-2` | "the movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9936 (99.4%) |
| `bert-base-uncased-SST-2` | "the movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9996 (100.0%) |
| `twitter-roberta-base-sentiment-latest` | "the movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9872 (98.7%) |
| `twitter-roberta-base-sentiment` | "the movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9863 (98.6%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.0945 | -4.9 pp |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0162 | -1.0 pp |
| `bert-base-uncased-SST-2` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0534 | -5.3 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.1208 | -8.8 pp |
| `twitter-roberta-base-sentiment` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.0843 | -9.3 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 1 | 0 | 0 | 0 | 6 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `bert-base-uncased-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment-latest` | 1 | 0 | 0 | 0 | 6 |
| `twitter-roberta-base-sentiment` | 1 | 0 | 0 | 0 | 6 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 85.71%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 100.0% | 71.4% | 85.7% | 85.7% |
| `twitter-robe` | 100.0% | 100.0% | 71.4% | 85.7% | 85.7% |
| `distilbert-b` | 71.4% | 71.4% | 100.0% | 85.7% | 85.7% |
| `albert-base-` | 85.7% | 85.7% | 85.7% | 100.0% | 100.0% |
| `bert-base-un` | 85.7% | 85.7% | 85.7% | 100.0% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |

## 8. Semantic Reference Methodology & Ground-Truth Alignment
1. **Canonical Semantic Label Space**: Ground-truth polarity is strictly confined to `POSITIVE`, `NEGATIVE`, and `NEUTRAL`. Non-canonical sentiment categories (such as `MIXED`, `AMBIGUOUS`, `SARCASTIC`) are rejected.
2. **Google Gemini Role**: Gemini operates exclusively as an external semantic annotator/verification layer for baseline and probe sentences. It is **never** a benchmark model, does not forecast model failures, and is strictly prohibited from generating the failure taxonomy.
3. **Human Verification & Override**: Every semantic reference can be verified and overridden by researchers (`[Accept]` / `[Change]`). Frozen semantic references are strictly immutable during model evaluation.
4. **Binary vs. Multiclass Alignment**: Binary models (e.g. 2-class SST-2) natively output `NEGATIVE` and `POSITIVE`. When semantic reference is `NEUTRAL`, binary models' forced polarity is recorded as `NOT_DIRECTLY_REPRESENTABLE` (`BINARY_FORCED_POLARITY`), preserving empirical truth rather than falsely modifying the reference.
5. **Independence of Model Outputs & Rule-Based Taxonomy**: Model predictions remain 100% empirical forward-pass outputs. The failure taxonomy (`Blind`, `Spurious`, `Misweighted`, `Undetermined`) is derived purely by deterministic rule-based behavioral analysis, completely independent of Gemini.