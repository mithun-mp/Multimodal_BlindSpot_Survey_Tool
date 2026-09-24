# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790182772_13ba38`
- **Run Plan Created**: `1790182773.505855`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`, `textattack/bert-base-uncased-SST-2`, `textattack/albert-base-v2-SST-2`
- **Probe Set ID / Version**: `pset_1790182711_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 114.23s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "the way he talked to me was amazing i was in love with his voice"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "the way he talked to me was amazing i wa..." | `LITERAL` | **POSITIVE** | 0.9999 (100.0%) |
| `twitter-roberta-base-sentiment-latest` | "the way he talked to me was amazing i wa..." | `LITERAL` | **POSITIVE** | 0.9856 (98.6%) |
| `twitter-roberta-base-sentiment` | "the way he talked to me was amazing i wa..." | `LITERAL` | **POSITIVE** | 0.9881 (98.8%) |
| `bert-base-uncased-SST-2` | "the way he talked to me was amazing i wa..." | `LITERAL` | **POSITIVE** | 0.9995 (99.9%) |
| `albert-base-v2-SST-2` | "the way he talked to me was amazing i wa..." | `LITERAL` | **POSITIVE** | 0.9904 (99.0%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0022 | -0.2 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 0 (0.0%) | 0/2 (0.0%) | 5/5 (100.0%) | 71.4% | 0.2239 | -4.7 pp |
| `twitter-roberta-base-sentiment` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.2111 | -9.7 pp |
| `bert-base-uncased-SST-2` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0442 | -4.4 pp |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0096 | -0.0 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 0 | 0 | 0 | 0 | 7 |
| `twitter-roberta-base-sentiment-latest` | 2 | 0 | 0 | 0 | 5 |
| `twitter-roberta-base-sentiment` | 1 | 0 | 0 | 0 | 6 |
| `bert-base-uncased-SST-2` | 0 | 0 | 0 | 0 | 7 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 7 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 81.43%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 85.7% | 71.4% | 71.4% | 71.4% |
| `twitter-robe` | 85.7% | 100.0% | 71.4% | 71.4% | 71.4% |
| `distilbert-b` | 71.4% | 71.4% | 100.0% | 100.0% | 100.0% |
| `albert-base-` | 71.4% | 71.4% | 100.0% | 100.0% | 100.0% |
| `bert-base-un` | 71.4% | 71.4% | 100.0% | 100.0% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |