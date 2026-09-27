# BlindSpot Research Audit Report: mul01

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790529126_68517a`
- **Run Plan Created**: `1790529127.3496554`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790529059_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 690.81s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "the sun rises in east and sun sets in the west"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "the sun rises in east and sun sets in th..." | `LITERAL` | **POSITIVE** | 0.9986 (99.9%) |
| `albert-base-v2-SST-2` | "the sun rises in east and sun sets in th..." | `LITERAL` | **POSITIVE** | 0.9292 (92.9%) |
| `bert-base-uncased-SST-2` | "the sun rises in east and sun sets in th..." | `LITERAL` | **POSITIVE** | 0.9871 (98.7%) |
| `twitter-roberta-base-sentiment-latest` | "the sun rises in east and sun sets in th..." | `LITERAL` | **NEUTRAL** | 0.9249 (92.5%) |
| `twitter-roberta-base-sentiment` | "the sun rises in east and sun sets in th..." | `LITERAL` | **NEUTRAL** | 0.6149 (61.5%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0092 | -0.8 pp |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0632 | +0.8 pp |
| `bert-base-uncased-SST-2` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 85.7% | 0.1005 | -7.8 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 42.9% | 0.4448 | -5.2 pp |
| `twitter-roberta-base-sentiment` | 7 | 2 (28.6%) | 0/2 (0.0%) | 3/5 (60.0%) | 42.9% | 0.5492 | +11.1 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 0 | 0 | 0 | 7 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `bert-base-uncased-SST-2` | 0 | 0 | 1 | 0 | 6 |
| `twitter-roberta-base-sentiment-latest` | 2 | 1 | 1 | 0 | 3 |
| `twitter-roberta-base-sentiment` | 2 | 2 | 0 | 0 | 3 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 51.43%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 85.7% | 28.6% | 28.6% | 28.6% |
| `twitter-robe` | 85.7% | 100.0% | 14.3% | 14.3% | 14.3% |
| `distilbert-b` | 28.6% | 14.3% | 100.0% | 100.0% | 100.0% |
| `albert-base-` | 28.6% | 14.3% | 100.0% | 100.0% | 100.0% |
| `bert-base-un` | 28.6% | 14.3% | 100.0% | 100.0% | 100.0% |

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