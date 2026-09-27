# BlindSpot Research Audit Report: Multimodel 00001

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790537272_6f4cc1`
- **Run Plan Created**: `1790537274.0473785`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790537241_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 950.50s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "He is a Good boy but very naughty"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "He is a Good boy but very naughty..." | `LITERAL` | **POSITIVE** | 0.9977 (99.8%) |
| `albert-base-v2-SST-2` | "He is a Good boy but very naughty..." | `LITERAL` | **POSITIVE** | 0.9126 (91.3%) |
| `bert-base-uncased-SST-2` | "He is a Good boy but very naughty..." | `LITERAL` | **POSITIVE** | 0.9815 (98.1%) |
| `twitter-roberta-base-sentiment-latest` | "He is a Good boy but very naughty..." | `LITERAL` | **POSITIVE** | 0.6078 (60.8%) |
| `twitter-roberta-base-sentiment` | "He is a Good boy but very naughty..." | `LITERAL` | **NEUTRAL** | 0.4701 (47.0%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 0/2 (28.6%) | 5/5 (100.0%) | 85.7% | 0.1556 | -1.8 pp |
| `albert-base-v2-SST-2` | 7 | 0 (0.0%) | 0/2 (28.6%) | 5/5 (100.0%) | 71.4% | 0.2073 | -2.8 pp |
| `bert-base-uncased-SST-2` | 7 | 1 (14.3%) | 0/2 (28.6%) | 5/5 (100.0%) | 85.7% | 0.1262 | -3.2 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 0/2 (28.6%) | 5/5 (100.0%) | 100.0% | 0.3376 | +5.5 pp |
| `twitter-roberta-base-sentiment` | 7 | 5 (71.4%) | 0/2 (28.6%) | 1/5 (20.0%) | 28.6% | 0.5041 | +15.7 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 1 | 0 | 0 | 0 | 6 |
| `albert-base-v2-SST-2` | 2 | 0 | 0 | 0 | 5 |
| `bert-base-uncased-SST-2` | 1 | 0 | 0 | 0 | 6 |
| `twitter-roberta-base-sentiment-latest` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment` | 1 | 3 | 1 | 0 | 2 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 74.29%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 71.4% | 57.1% | 42.9% | 57.1% |
| `twitter-robe` | 71.4% | 100.0% | 85.7% | 71.4% | 85.7% |
| `distilbert-b` | 57.1% | 85.7% | 100.0% | 85.7% | 100.0% |
| `albert-base-` | 42.9% | 71.4% | 85.7% | 100.0% | 85.7% |
| `bert-base-un` | 57.1% | 85.7% | 100.0% | 85.7% | 100.0% |

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