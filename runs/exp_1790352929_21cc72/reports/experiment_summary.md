# BlindSpot Research Audit Report: Multimodel Test Run 002

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790352929_21cc72`
- **Run Plan Created**: `1790352929.9912486`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790352896_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 549.54s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "The movie was great and the acting was top notch."

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9999 (100.0%) |
| `albert-base-v2-SST-2` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9957 (99.6%) |
| `bert-base-uncased-SST-2` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9996 (100.0%) |
| `twitter-roberta-base-sentiment-latest` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9870 (98.7%) |
| `twitter-roberta-base-sentiment` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9862 (98.6%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.1402 | -0.3 pp |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0126 | -0.8 pp |
| `bert-base-uncased-SST-2` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0576 | -5.7 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.1304 | -8.2 pp |
| `twitter-roberta-base-sentiment` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.0849 | -9.5 pp |

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