# BlindSpot Research Audit Report: Multimodel 003

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790104901_f2922f`
- **Run Plan Created**: `1790104903.1321862`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790104849_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 463.98s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "I am healthy But still hospitalized"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "I am healthy But still hospitalized..." | `LITERAL` | **NEGATIVE** | 0.8577 (85.8%) |
| `albert-base-v2-SST-2` | "I am healthy But still hospitalized..." | `LITERAL` | **NEGATIVE** | 0.6339 (63.4%) |
| `bert-base-uncased-SST-2` | "I am healthy But still hospitalized..." | `LITERAL` | **NEGATIVE** | 0.8187 (81.9%) |
| `twitter-roberta-base-sentiment-latest` | "I am healthy But still hospitalized..." | `LITERAL` | **NEUTRAL** | 0.6616 (66.2%) |
| `twitter-roberta-base-sentiment` | "I am healthy But still hospitalized..." | `LITERAL` | **POSITIVE** | 0.5199 (52.0%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 0 (0.0%) | 0/2 (0.0%) | 5/5 (100.0%) | 71.4% | 0.2188 | +7.5 pp |
| `albert-base-v2-SST-2` | 7 | 0 (0.0%) | 0/2 (0.0%) | 5/5 (100.0%) | 71.4% | 0.2871 | +7.5 pp |
| `bert-base-uncased-SST-2` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.3507 | +0.2 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 4 (57.1%) | 2/2 (100.0%) | 3/5 (60.0%) | 71.4% | 0.0921 | -3.9 pp |
| `twitter-roberta-base-sentiment` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.2953 | +18.5 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 2 | 0 | 0 | 0 | 5 |
| `albert-base-v2-SST-2` | 2 | 0 | 0 | 0 | 5 |
| `bert-base-uncased-SST-2` | 2 | 1 | 0 | 0 | 4 |
| `twitter-roberta-base-sentiment-latest` | 0 | 1 | 1 | 0 | 5 |
| `twitter-roberta-base-sentiment` | 0 | 0 | 0 | 0 | 7 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 47.14%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 42.9% | 14.3% | 14.3% | 28.6% |
| `twitter-robe` | 42.9% | 100.0% | 28.6% | 28.6% | 42.9% |
| `distilbert-b` | 14.3% | 28.6% | 100.0% | 100.0% | 85.7% |
| `albert-base-` | 14.3% | 28.6% | 100.0% | 100.0% | 85.7% |
| `bert-base-un` | 28.6% | 42.9% | 85.7% | 85.7% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |