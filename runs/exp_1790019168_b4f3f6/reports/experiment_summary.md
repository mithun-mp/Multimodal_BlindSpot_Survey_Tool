# BlindSpot Research Audit Report: Multimodel Robustness Audit002

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790019168_b4f3f6`
- **Run Plan Created**: `1790019169.234945`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790019127_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 402.03s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "All Glitters are not Gold"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "All Glitters are not Gold..." | `LITERAL` | **NEGATIVE** | 0.9987 (99.9%) |
| `albert-base-v2-SST-2` | "All Glitters are not Gold..." | `LITERAL` | **NEGATIVE** | 0.9368 (93.7%) |
| `bert-base-uncased-SST-2` | "All Glitters are not Gold..." | `LITERAL` | **NEGATIVE** | 0.9859 (98.6%) |
| `twitter-roberta-base-sentiment-latest` | "All Glitters are not Gold..." | `LITERAL` | **NEUTRAL** | 0.5521 (55.2%) |
| `twitter-roberta-base-sentiment` | "All Glitters are not Gold..." | `LITERAL` | **NEGATIVE** | 0.5216 (52.2%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.1350 | -0.6 pp |
| `albert-base-v2-SST-2` | 7 | 3 (42.9%) | 2/2 (100.0%) | 4/5 (80.0%) | 85.7% | 0.1771 | -3.2 pp |
| `bert-base-uncased-SST-2` | 7 | 2 (28.6%) | 1/2 (50.0%) | 4/5 (80.0%) | 71.4% | 0.2233 | -4.8 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 3 (42.9%) | 1/2 (50.0%) | 3/5 (60.0%) | 57.1% | 0.3231 | +5.9 pp |
| `twitter-roberta-base-sentiment` | 7 | 4 (57.1%) | 1/2 (50.0%) | 2/5 (40.0%) | 42.9% | 0.4369 | +13.4 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 1 | 0 | 0 | 0 | 6 |
| `albert-base-v2-SST-2` | 0 | 1 | 0 | 0 | 6 |
| `bert-base-uncased-SST-2` | 1 | 1 | 0 | 0 | 5 |
| `twitter-roberta-base-sentiment-latest` | 1 | 1 | 1 | 0 | 4 |
| `twitter-roberta-base-sentiment` | 1 | 2 | 1 | 0 | 3 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 61.43%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 85.7% | 57.1% | 42.9% | 57.1% |
| `twitter-robe` | 85.7% | 100.0% | 42.9% | 42.9% | 42.9% |
| `distilbert-b` | 57.1% | 42.9% | 100.0% | 71.4% | 85.7% |
| `albert-base-` | 42.9% | 42.9% | 71.4% | 100.0% | 85.7% |
| `bert-base-un` | 57.1% | 42.9% | 85.7% | 85.7% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |