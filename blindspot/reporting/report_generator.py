import os
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

from blindspot.reporting.visualizer import Visualizer

class ReportGenerator:
    """
    Automated generator for all SRS diagnostic Markdown reports.
    """
    def __init__(self, output_dir: str = "audit_reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "probes"), exist_ok=True)
        self.visualizer = Visualizer(figures_dir=os.path.join(self.output_dir, "figures"))

    def generate_all_reports(
        self,
        model_name: str,
        audit_results: Dict[str, Any],
        failures: List[Dict[str, Any]],
        explanations_summary: List[Dict[str, Any]],
    ) -> List[str]:
        """
        Generates the 4 SRS required report documents + Matplotlib visual charts.
        Returns list of generated absolute filepaths.
        """
        # Generate all Matplotlib graphs first
        figures = self.visualizer.generate_all_plots(audit_results, failures, explanations_summary)

        generated_files = []

        # 1. model_behavior_report.md
        mb_path = os.path.join(self.output_dir, "model_behavior_report.md")
        mb_content = self._build_model_behavior_report(model_name, audit_results, failures, figures)
        with open(mb_path, "w", encoding="utf-8") as f:
            f.write(mb_content)
        generated_files.append(os.path.abspath(mb_path))

        # 2. failure_summary.md
        fs_path = os.path.join(self.output_dir, "failure_summary.md")
        fs_content = self._build_failure_summary_report(failures)
        with open(fs_path, "w", encoding="utf-8") as f:
            f.write(fs_content)
        generated_files.append(os.path.abspath(fs_path))

        # 3. explanation_comparison.md
        ec_path = os.path.join(self.output_dir, "explanation_comparison.md")
        ec_content = self._build_explanation_comparison_report(explanations_summary, figures)
        with open(ec_path, "w", encoding="utf-8") as f:
            f.write(ec_content)
        generated_files.append(os.path.abspath(ec_path))

        # 4. probes/*.md
        probe_details = audit_results.get("probe_details", [])
        for idx, probe in enumerate(probe_details):
            p_path = os.path.join(self.output_dir, "probes", f"probe_{idx+1}.md")
            p_content = self._build_probe_report(idx + 1, probe, explanations_summary[idx] if idx < len(explanations_summary) else {})
            with open(p_path, "w", encoding="utf-8") as f:
                f.write(p_content)
            generated_files.append(os.path.abspath(p_path))

        # Append figure paths
        for fig_path in figures.values():
            generated_files.append(fig_path)

        return generated_files

    def _build_model_behavior_report(self, model_name: str, audit_results: Dict[str, Any], failures: List[Dict[str, Any]], figures: Dict[str, str]) -> str:
        blind_count = sum(1 for f in failures if f["category"] == "Blind")
        spurious_count = sum(1 for f in failures if f["category"] == "Spurious")
        misweighted_count = sum(1 for f in failures if f["category"] == "Misweighted")

        suitability = audit_results.get("suitability_info", {})
        confidence_info = audit_results.get("confidence_info", {})

        suitability_status = suitability.get("status", "suitable").upper()
        suitability_warning = suitability.get("warning", "")
        low_conf_warning = confidence_info.get("warning", "")
        neutral_note = confidence_info.get("neutral_clarification", "")

        suit_section = f"- **Probe Suitability Status**: `{suitability_status}`\n"
        if suitability_warning:
            suit_section += f"- ⚠️ **Suitability Warning**: {suitability_warning}\n"
        if low_conf_warning:
            suit_section += f"- ⚠️ **Confidence Warning**: {low_conf_warning}\n"
        if neutral_note:
            suit_section += f"- ℹ️ **Neutral Class Note**: {neutral_note}\n"

        return f"""# Model Behavior Audit Report

## Target Model Overview
- **Model Reference**: `{model_name}`
- **Input Sentence**: "{audit_results.get('original_sentence', '')}"
- **Original Prediction**: `{audit_results.get('original_prediction', '')}` (Confidence: {audit_results.get('original_confidence', 0.0):.4f})
- **Total Perturbation Probes**: {audit_results.get('total_perturbations', 0)}
{suit_section}
## Diagnostic Summary Metrics
- **Prediction Flip Rate**: {audit_results.get('flip_rate', 0.0):.2%}
- **Expected Calibration Error (ECE)**: {audit_results.get('ece', 0.0):.4f} (Chart displays ECE × 100)
- **Total Detected Failures**: {len(failures)}

### Metric Interpretation Guidelines
1. **Prediction Flip Rate**:
   - **High Flip Rate $\\neq$ Automatically Good**, and **Low Flip Rate $\\neq$ Automatically Bad**.
   - Flip rate MUST be interpreted in context of perturbation types:
     - **Directional Perturbations** (single negation, negative contrast, concession): Prediction flip is **expected**. A label flip demonstrates that the model appropriately responded to semantic changes.
     - **Invariant Perturbations** (litotes double negation, synonym substitution): Prediction stability is **expected**. A label flip indicates model fragility.
2. **Expected Calibration Error (ECE)**:
   - Lower ECE indicates better confidence calibration.
   - ECE measures the difference between model confidence and observed accuracy across 10 binned confidence levels.
   - ECE alone does not prove that an individual prediction is correct; it assesses calibration across the evaluated probe set.

![Behavioral Metrics Chart](figures/behavioral_metrics.png)

## Failure Taxonomy Distribution
| Failure Category | Count | Primary Cause |
| :--- | :---: | :--- |
| **Blind** | {blind_count} | Model ignored negation operators |
| **Spurious** | {spurious_count} | Model over-relied on entity/domain nouns |
| **Misweighted** | {misweighted_count} | Model misallocated modifier token weights |

![Failure Taxonomy Distribution](figures/taxonomy_distribution.png)

## Actionable Recommendations
1. **Negation Retraining**: Augment training corpus with CheckList negation templates to resolve **Blind** failures.
2. **Adversarial Entity Replacement**: Apply entity swapping during model fine-tuning to prevent **Spurious** correlations.
3. **Contrastive Regularization**: Fine-tune with paired contrast clauses ('X, but Y') to resolve **Misweighted** attributions.
"""

    def _build_failure_summary_report(self, failures: List[Dict[str, Any]]) -> str:
        lines = ["# Failure Summary Report\n"]
        lines.append(f"Total Model Failures Identified: **{len(failures)}**\n")

        if not failures:
            lines.append("No diagnostic failures detected! Target model demonstrated robust predictions and consistent explanations across all probes.\n")
            return "\n".join(lines)

        for idx, fail in enumerate(failures, 1):
            lines.append(f"### Failure #{idx}: [{fail['category']}]")
            lines.append(f"- **Reason**: {fail['reason']}")
            lines.append(f"- **Details**: {fail['details']}")
            lines.append(f"- **Actionable Recommendation**: {fail['recommendation']}\n")

        return "\n".join(lines)

    def _build_explanation_comparison_report(self, explanations_summary: List[Dict[str, Any]], figures: Dict[str, str]) -> str:
        lines = ["# Explanation Comparison Report\n"]
        lines.append("This report details local token feature attributions (LIME & SHAP) compared between original and perturbed inputs.\n")
        lines.append("![Token Attribution Shift Comparison](figures/attribution_comparison.png)\n")
        lines.append("![Probe Explanation Alignment Summary](figures/probe_alignment_summary.png)\n")
        lines.append("\n## Detailed Probe Feature Attributions\n")

        for idx, item in enumerate(explanations_summary, 1):
            lines.append(f"### Probe #{idx}: {item.get('type', 'perturbation')}")
            lines.append(f"- **Original Input**: \"{item.get('original', '')}\"")
            lines.append(f"- **Perturbed Input**: \"{item.get('perturbed', '')}\"")
            lines.append(f"- **Jaccard Attribution Similarity**: {item.get('jaccard_similarity', 0.0):.4f}")
            lines.append(f"- **Cosine Attribution Alignment**: {item.get('cosine_alignment', 0.0):.4f}")
            lines.append("\n**Top Token Attributions (Perturbed)**:")
            exp_dict = item.get("pert_explanation", {})
            for word, weight in sorted(exp_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:5]:
                lines.append(f"  - `{word}`: {weight:+.4f}")
            lines.append("\n" + "-"*40 + "\n")

        return "\n".join(lines)

    def _build_probe_report(self, probe_id: int, probe: Dict[str, Any], explanation_info: Dict[str, Any]) -> str:
        p_type = probe.get("type", "")
        expected_flip = probe.get("expected_flip", False)
        expectation_str = "Directional (Prediction Flip Expected)" if expected_flip else "Invariant (Prediction Stability Expected)"
        
        is_flipped = probe.get("is_flipped", False)
        behavioral_str = "Label Flipped" if is_flipped else "Label Unchanged"
        
        conf_delta = probe.get("confidence_delta", 0.0)
        conf_response_str = f"{conf_delta:+.4f} (Confidence {'Increased' if conf_delta > 0 else 'Decreased'})"

        return f"""# Probe #{probe_id} Diagnostic Detail

## Transformation Details
- **Perturbation Type**: `{p_type}`
- **Description**: {probe.get('description', '')}
- **Perturbation Expectation**: {expectation_str}

## Sentence Comparison
- **Original Input**: "{probe.get('original', '')}"
- **Perturbed Input**: "{probe.get('perturbed', '')}"

## Behavioral & Confidence Diagnostics
- **Original Prediction**: `{probe.get('original_label', '')}` (Conf: {probe.get('original_confidence', 0.0):.4f})
- **Perturbed Prediction**: `{probe.get('perturbed_label', '')}` (Conf: {probe.get('perturbed_confidence', 0.0):.4f})
- **Behavioral Response**: `{behavioral_str}` (Flipped: `{is_flipped}`, Expected Flip: `{expected_flip}`)
- **Confidence Response**: `{conf_response_str}`
- **Unexpected Behavior Detected**: `{probe.get('unexpected_behavior', False)}`

## Explanation Response
- **Jaccard Top-Token Similarity**: {explanation_info.get('jaccard_similarity', 0.0):.4f}
- **Cosine Attribution Alignment**: {explanation_info.get('cosine_alignment', 0.0):.4f}
"""

