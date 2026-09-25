# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790354301_11f5af`
- **Run Plan Created**: `1790354302.615869`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790354293_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 482.39s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "i am healthy but still hospitalized."

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "i am healthy but still hospitalized...." | `LITERAL` | **NEGATIVE** | 0.8018 (80.2%) |
| `albert-base-v2-SST-2` | "i am healthy but still hospitalized...." | `LITERAL` | **NEGATIVE** | 0.6589 (65.9%) |
| `bert-base-uncased-SST-2` | "i am healthy but still hospitalized...." | `LITERAL` | **NEGATIVE** | 0.7436 (74.4%) |
| `twitter-roberta-base-sentiment-latest` | "i am healthy but still hospitalized...." | `LITERAL` | **NEUTRAL** | 0.7185 (71.9%) |
| `twitter-roberta-base-sentiment` | "i am healthy but still hospitalized...." | `LITERAL` | **NEUTRAL** | 0.4838 (48.4%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.3671 | +13.7 pp |
| `albert-base-v2-SST-2` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.4754 | +15.5 pp |
| `bert-base-uncased-SST-2` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.3358 | +10.7 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 5 (71.4%) | 2/2 (100.0%) | 2/5 (40.0%) | 57.1% | 0.4072 | -1.6 pp |
| `twitter-roberta-base-sentiment` | 7 | 5 (71.4%) | 1/2 (50.0%) | 1/5 (20.0%) | 28.6% | 0.5406 | +23.9 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 2 | 1 | 0 | 0 | 4 |
| `albert-base-v2-SST-2` | 2 | 1 | 0 | 0 | 4 |
| `bert-base-uncased-SST-2` | 2 | 1 | 0 | 0 | 4 |
| `twitter-roberta-base-sentiment-latest` | 0 | 2 | 1 | 0 | 4 |
| `twitter-roberta-base-sentiment` | 1 | 2 | 2 | 0 | 2 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 60.00%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 42.9% | 28.6% | 28.6% | 28.6% |
| `twitter-robe` | 42.9% | 100.0% | 57.1% | 57.1% | 57.1% |
| `distilbert-b` | 28.6% | 57.1% | 100.0% | 100.0% | 100.0% |
| `albert-base-` | 28.6% | 57.1% | 100.0% | 100.0% | 100.0% |
| `bert-base-un` | 28.6% | 57.1% | 100.0% | 100.0% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |