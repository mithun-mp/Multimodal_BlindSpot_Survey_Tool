# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790181290_8ddb24`
- **Run Plan Created**: `1790181291.432789`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`, `textattack/bert-base-uncased-SST-2`, `textattack/albert-base-v2-SST-2`
- **Probe Set ID / Version**: `pset_1790181276_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 166.25s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "i am healthy but am still hospitalised"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "i am healthy but am still hospitalised..." | `LITERAL` | **NEGATIVE** | 0.9811 (98.1%) |
| `twitter-roberta-base-sentiment-latest` | "i am healthy but am still hospitalised..." | `LITERAL` | **NEGATIVE** | 0.5940 (59.4%) |
| `twitter-roberta-base-sentiment` | "i am healthy but am still hospitalised..." | `LITERAL` | **NEUTRAL** | 0.5909 (59.1%) |
| `bert-base-uncased-SST-2` | "i am healthy but am still hospitalised..." | `LITERAL` | **NEGATIVE** | 0.7232 (72.3%) |
| `albert-base-v2-SST-2` | "i am healthy but am still hospitalised..." | `LITERAL` | **NEGATIVE** | 0.9568 (95.7%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.4094 | -0.0 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 2 (28.6%) | 0/2 (0.0%) | 3/5 (60.0%) | 42.9% | 0.2826 | +9.7 pp |
| `twitter-roberta-base-sentiment` | 7 | 4 (57.1%) | 1/2 (50.0%) | 2/5 (40.0%) | 42.9% | 0.3820 | +6.9 pp |
| `bert-base-uncased-SST-2` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.4149 | +11.6 pp |
| `albert-base-v2-SST-2` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.3811 | -0.4 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 2 | 1 | 0 | 0 | 4 |
| `twitter-roberta-base-sentiment-latest` | 2 | 1 | 1 | 0 | 3 |
| `twitter-roberta-base-sentiment` | 1 | 2 | 1 | 0 | 3 |
| `bert-base-uncased-SST-2` | 2 | 1 | 0 | 0 | 4 |
| `albert-base-v2-SST-2` | 2 | 1 | 0 | 0 | 4 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 67.14%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 28.6% | 28.6% | 28.6% | 28.6% |
| `twitter-robe` | 28.6% | 100.0% | 85.7% | 85.7% | 85.7% |
| `distilbert-b` | 28.6% | 85.7% | 100.0% | 100.0% | 100.0% |
| `albert-base-` | 28.6% | 85.7% | 100.0% | 100.0% | 100.0% |
| `bert-base-un` | 28.6% | 85.7% | 100.0% | 100.0% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |