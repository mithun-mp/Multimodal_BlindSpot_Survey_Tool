# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790137935_50b135`
- **Run Plan Created**: `1790137936.0064576`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790137856_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 1477.75s
- **Pipeline Integrity Status**: `WARNING`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "The film was amazing,me and family enjoyed it well"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "The film was amazing,me and family enjoy..." | `LITERAL` | **POSITIVE** | 0.9999 (100.0%) |
| `twitter-roberta-base-sentiment-latest` | "The film was amazing,me and family enjoy..." | `LITERAL` | **POSITIVE** | 0.9888 (98.9%) |
| `bert-base-uncased-SST-2` | "The film was amazing,me and family enjoy..." | `LITERAL` | **POSITIVE** | 0.9996 (100.0%) |
| `twitter-roberta-base-sentiment` | "The film was amazing,me and family enjoy..." | `LITERAL` | **POSITIVE** | 0.9920 (99.2%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.1349 | -0.8 pp |
| `albert-base-v2-SST-2` | 0 | 0 (0.0%) | 0/0 (0.0%) | 0/0 (0.0%) | 100.0% | 0.0000 | +0.0 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.2157 | -8.6 pp |
| `bert-base-uncased-SST-2` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.2039 | -6.8 pp |
| `twitter-roberta-base-sentiment` | 7 | 1 (14.3%) | 1/2 (50.0%) | 5/5 (100.0%) | 85.7% | 0.2174 | -9.0 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 1 | 0 | 0 | 0 | 6 |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 0 |
| `twitter-roberta-base-sentiment-latest` | 1 | 0 | 0 | 0 | 6 |
| `bert-base-uncased-SST-2` | 1 | 0 | 0 | 0 | 6 |
| `twitter-roberta-base-sentiment` | 1 | 0 | 0 | 0 | 6 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 48.57%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 100.0% | 71.4% | 0.0% | 71.4% |
| `twitter-robe` | 100.0% | 100.0% | 71.4% | 0.0% | 71.4% |
| `distilbert-b` | 71.4% | 71.4% | 100.0% | 0.0% | 100.0% |
| `albert-base-` | 0.0% | 0.0% | 0.0% | 100.0% | 0.0% |
| `bert-base-un` | 71.4% | 71.4% | 100.0% | 0.0% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 0 | 0 | 0 | **FAIL** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |