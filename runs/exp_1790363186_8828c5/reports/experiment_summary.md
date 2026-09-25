# BlindSpot Research Audit Report: Multimodel Test Run Heavy 001

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790363186_8828c5`
- **Run Plan Created**: `1790363187.459701`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790363158_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 930.69s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "Although the product initially seemed impressively promising, it was nowhere near as reliable as the glowing reviews suggested, and despite a few genuinely excellent features, I cannot honestly say that I would recommend it."

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "Although the product initially seemed im..." | `LITERAL` | **NEGATIVE** | 0.9985 (99.8%) |
| `albert-base-v2-SST-2` | "Although the product initially seemed im..." | `LITERAL` | **NEGATIVE** | 0.9837 (98.4%) |
| `bert-base-uncased-SST-2` | "Although the product initially seemed im..." | `LITERAL` | **NEGATIVE** | 0.9806 (98.1%) |
| `twitter-roberta-base-sentiment-latest` | "Although the product initially seemed im..." | `LITERAL` | **NEGATIVE** | 0.7954 (79.5%) |
| `twitter-roberta-base-sentiment` | "Although the product initially seemed im..." | `LITERAL` | **NEGATIVE** | 0.5194 (51.9%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.4258 | -0.1 pp |
| `albert-base-v2-SST-2` | 7 | 0 (0.0%) | 0/2 (0.0%) | 5/5 (100.0%) | 71.4% | 0.2622 | -0.7 pp |
| `bert-base-uncased-SST-2` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.3973 | -1.2 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 0 (0.0%) | 0/2 (0.0%) | 5/5 (100.0%) | 71.4% | 0.4039 | -6.3 pp |
| `twitter-roberta-base-sentiment` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.2170 | -2.8 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 2 | 1 | 0 | 0 | 4 |
| `albert-base-v2-SST-2` | 2 | 0 | 0 | 0 | 5 |
| `bert-base-uncased-SST-2` | 2 | 1 | 0 | 0 | 4 |
| `twitter-roberta-base-sentiment-latest` | 2 | 0 | 0 | 0 | 5 |
| `twitter-roberta-base-sentiment` | 2 | 1 | 0 | 0 | 4 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 88.57%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 85.7% | 85.7% | 85.7% | 85.7% |
| `twitter-robe` | 85.7% | 100.0% | 85.7% | 100.0% | 85.7% |
| `distilbert-b` | 85.7% | 85.7% | 100.0% | 85.7% | 100.0% |
| `albert-base-` | 85.7% | 100.0% | 85.7% | 100.0% | 85.7% |
| `bert-base-un` | 85.7% | 85.7% | 100.0% | 85.7% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |