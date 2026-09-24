# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790180229_bc0799`
- **Run Plan Created**: `1790180229.9774592`
- **Target Models**: `textattack/albert-base-v2-SST-2`
- **Probe Set ID / Version**: `pset_1790180216_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 58.09s
- **Pipeline Integrity Status**: `PASS`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "The movie was great and the acting was top notch."

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |
| `albert-base-v2-SST-2` | "The movie was great and the acting was t..." | `LITERAL` | **POSITIVE** | 0.9957 (99.6%) |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `albert-base-v2-SST-2` | 7 | 2 (28.6%) | 2/2 (100.0%) | 5/5 (100.0%) | 100.0% | 0.0126 | -0.8 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 7 |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **PASS** |