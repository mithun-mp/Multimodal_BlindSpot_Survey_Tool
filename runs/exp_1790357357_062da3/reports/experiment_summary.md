# BlindSpot Research Audit Report: Multimodel Test Run 004

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790357357_062da3`
- **Run Plan Created**: `1790357358.2585669`
- **Target Models**: `distilbert-base-uncased-finetuned-sst-2-english`, `textattack/albert-base-v2-SST-2`, `textattack/bert-base-uncased-SST-2`, `cardiffnlp/twitter-roberta-base-sentiment-latest`, `cardiffnlp/twitter-roberta-base-sentiment`
- **Probe Set ID / Version**: `pset_1790357329_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 571.90s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "I am Healthy and Energetic ,But still i am Hospitalized"

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | "I am Healthy and Energetic ,But still i ..." | `LITERAL` | **NEGATIVE** | 0.9916 (99.2%) |
| `albert-base-v2-SST-2` | "I am Healthy and Energetic ,But still i ..." | `LITERAL` | **POSITIVE** | 0.6141 (61.4%) |
| `bert-base-uncased-SST-2` | "I am Healthy and Energetic ,But still i ..." | `LITERAL` | **NEGATIVE** | 0.9622 (96.2%) |
| `twitter-roberta-base-sentiment-latest` | "I am Healthy and Energetic ,But still i ..." | `LITERAL` | **NEUTRAL** | 0.6192 (61.9%) |
| `twitter-roberta-base-sentiment` | "I am Healthy and Energetic ,But still i ..." | `LITERAL` | **NEUTRAL** | 0.5229 (52.3%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.3954 | -2.5 pp |
| `albert-base-v2-SST-2` | 7 | 3 (42.9%) | 1/2 (50.0%) | 3/5 (60.0%) | 57.1% | 0.1690 | +11.5 pp |
| `bert-base-uncased-SST-2` | 7 | 1 (14.3%) | 0/2 (0.0%) | 4/5 (80.0%) | 57.1% | 0.3857 | -0.5 pp |
| `twitter-roberta-base-sentiment-latest` | 7 | 4 (57.1%) | 2/2 (100.0%) | 3/5 (60.0%) | 71.4% | 0.2745 | +1.8 pp |
| `twitter-roberta-base-sentiment` | 7 | 4 (57.1%) | 1/2 (50.0%) | 2/5 (40.0%) | 42.9% | 0.2267 | +13.2 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 2 | 1 | 0 | 0 | 4 |
| `albert-base-v2-SST-2` | 1 | 2 | 0 | 0 | 4 |
| `bert-base-uncased-SST-2` | 2 | 1 | 0 | 0 | 4 |
| `twitter-roberta-base-sentiment-latest` | 0 | 2 | 0 | 0 | 5 |
| `twitter-roberta-base-sentiment` | 1 | 2 | 1 | 0 | 3 |

## 6. Cross-Model Descriptive Agreement
- **Overall Prediction Agreement**: 52.86%

### Pairwise Concordance Matrix
| Model | `twitter-robe` | `twitter-robe` | `distilbert-b` | `albert-base-` | `bert-base-un` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `twitter-robe` | 100.0% | 57.1% | 28.6% | 42.9% | 28.6% |
| `twitter-robe` | 57.1% | 100.0% | 57.1% | 42.9% | 57.1% |
| `distilbert-b` | 28.6% | 57.1% | 100.0% | 57.1% | 100.0% |
| `albert-base-` | 42.9% | 42.9% | 57.1% | 100.0% | 57.1% |
| `bert-base-un` | 28.6% | 57.1% | 100.0% | 57.1% | 100.0% |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `distilbert-base-uncased-finetuned-sst-2-english` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `bert-base-uncased-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment-latest` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |
| `twitter-roberta-base-sentiment` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |