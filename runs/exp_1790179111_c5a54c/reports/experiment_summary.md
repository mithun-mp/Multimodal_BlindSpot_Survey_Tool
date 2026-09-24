# BlindSpot Research Audit Report: Multimodel Robustness Audit

## 1. Experiment Metadata & Configuration
- **Experiment ID**: `exp_1790179111_c5a54c`
- **Run Plan Created**: `1790179112.4426837`
- **Target Models**: `textattack/albert-base-v2-SST-2`
- **Probe Set ID / Version**: `pset_1790179098_sel` (v2.2.0)
- **Generator Version**: `2.2.0`
- **Total Selected Probes**: 7
- **Execution Runtime**: 17.13s
- **Pipeline Integrity Status**: `WARNING`

## 2. Seed Sentences & Pragmatic Classifications
- **Seed #1** `[LITERAL]`: "The movie was great and the acting was top notch."

## 3. Original Sentence Baselines (Evaluated Once Per Model)
| Model | Seed Sentence | Type | Predicted Label | Confidence |
| :--- | :--- | :---: | :---: | :---: |

## 4. Primary Research Metrics
| Model | Probes | Observed Flips (Rate) | Expected Flips (Rate) | Expected Preserves (Rate) | Consistency | ECE | Mean Δ (pp) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `albert-base-v2-SST-2` | 0 | 0 (0.0%) | 0/0 (0.0%) | 0/0 (0.0%) | 100.0% | 0.0000 | +0.0 pp |

## 5. Behavioral Failure Taxonomy Counts (Never Suppressed)
| Model | Blind | Spurious | Misweighted | Undetermined | Compliant (None) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `albert-base-v2-SST-2` | 0 | 0 | 0 | 0 | 0 |

## 7. Pipeline Count Integrity Audit
| Model | Generated | Selected | Verified | Planned | Executed | Analyzed | Reported | Audit Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `albert-base-v2-SST-2` | 7 | 7 | 7 | 7 | 0 | 0 | 0 | **FAIL** |