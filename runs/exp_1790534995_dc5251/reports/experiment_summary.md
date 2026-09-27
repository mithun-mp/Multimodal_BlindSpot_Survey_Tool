# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790534995_dc5251`
- **Run Plan Created**: `1790534996.23711`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790534930_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 980.87s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "the sun rises in the east and sun sets in west"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "the sun rises in the east and sun sets i..." | `LITERAL` | **POSITIVE** | 0.9988 (99.9%) |
| `albert-base-v2-SST-2` | "the sun rises in the east and sun sets i..." | `LITERAL` | **POSITIVE** | 0.9378 (93.8%) |
| `bert-base-uncased-SST-2` | "the sun rises in the east and sun sets i..." | `LITERAL` | **POSITIVE** | 0.9906 (99.1%) |
| `twitter-roberta-base-sentiment-latest` | "the sun rises in the east and sun sets i..." | `LITERAL` | **NEUTRAL** | 0.9266 (92.7%) |
| `twitter-roberta-base-sentiment` | "the sun rises in the east and sun sets i..." | `LITERAL` | **NEUTRAL** | 0.5812 (58.1%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 2 (28.6%) | 1/3 (42.9%) | 4/4 (100.0%) | 100.0% | 0.0034 | -0.2 pp |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 1/3 (42.9%) | 4/4 (100.0%) | 100.0% | 0.0522 | +1.0 pp |
| `bert-base-uncased-SST-2` | 7 | 2 (28.6%) | 1/3 (42.9%) | 4/4 (100.0%) | 100.0% | 0.0278 | -1.8 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 1/3 (42.9%) | 4/4 (100.0%) | 57.1% | 0.3443 | -5.3 pp |
| `twitter-roberta-base-sentiment` | 7 | 2 (28.6%) | 1/3 (42.9%) | 3/4 (75.0%) | 57.1% | 0.4500 | +12.2 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 0 | 0 | 0 | 7 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `bert-base-uncased-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment-latest` | 2 | 0 | 1 | 0 | 4 |
| `twitter-roberta-base-sentiment` | 2 | 1 | 0 | 0 | 4 |

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