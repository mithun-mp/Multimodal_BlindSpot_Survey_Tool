import os
from typing import Dict, Any, List, Optional
import matplotlib
matplotlib.use('Agg')  # Headless mode for server & CLI execution
import matplotlib.pyplot as plt
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Visualizer:
    """
    Generates publication-grade Matplotlib diagnostic graphs for BlindSpot.
    """
    def __init__(self, figures_dir: str = "audit_reports/figures"):
        self.figures_dir = figures_dir
        os.makedirs(self.figures_dir, exist_ok=True)
        # Apply clean, modern styling parameters
        plt.rcParams.update({
            'axes.grid': True,
            'grid.alpha': 0.3,
            'grid.linestyle': '--',
            'axes.edgecolor': '#cccccc',
            'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
            'font.family': 'sans-serif',
        })

    def plot_taxonomy_distribution(self, failures: List[Dict[str, Any]], filename: str = "taxonomy_distribution.png") -> str:
        """
        Generates a Donut Chart showing failure taxonomy distribution (Blind, Spurious, Misweighted).
        Prevents text overlapping and zero-width slice glitches by filtering active categories.
        """
        out_path = os.path.join(self.figures_dir, filename)
        
        category_map = {
            "Blind": ("Blind", '#e74c3c'),
            "Spurious": ("Spurious", '#e67e22'),
            "Misweighted": ("Misweighted", '#9b59b6')
        }

        counts = {
            cat: sum(
                1 for f in failures
                if str(f.get("category", "")).lower() == cat.lower()
                or str(f.get("failure_category", "")).lower() == cat.lower()
                or str(f.get("failure_type", "")).lower() == cat.lower()
            )
            for cat in category_map
        }

        total_failures = sum(counts.values())

        fig, ax = plt.subplots(figsize=(6, 5), dpi=300)

        if total_failures == 0:
            # Clean, unified green donut ring for zero failures
            wedges, texts = ax.pie(
                [1],
                labels=["0 Failures Detected"],
                startangle=90,
                colors=['#2ecc71'],
                wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
                textprops=dict(fontsize=11, fontweight='bold', color='#27ae60')
            )
            ax.text(0, 0, "100%\nRobust", ha='center', va='center', fontsize=12, fontweight='bold', color='#27ae60')
        else:
            # Filter to only active categories with >0 failures to prevent overlapping zero-slice glitches
            active_cats = [cat for cat, cnt in counts.items() if cnt > 0]
            display_counts = [counts[cat] for cat in active_cats]
            labels = [f"{cat} ({counts[cat]})" for cat in active_cats]
            colors = [category_map[cat][1] for cat in active_cats]

            wedges, texts, autotexts = ax.pie(
                display_counts,
                labels=labels,
                autopct=lambda pct: f'{int(round(pct * total_failures / 100.0))}',
                startangle=140,
                colors=colors,
                wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
                pctdistance=0.75,
                textprops=dict(fontsize=10, fontweight='bold')
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_weight('bold')

            ax.text(0, 0, f"Total\n{total_failures}", ha='center', va='center', fontsize=12, fontweight='bold', color='#333333')

        ax.set_title("Failure Taxonomy Distribution", fontsize=14, fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return os.path.abspath(out_path)

    def plot_behavioral_metrics(self, flip_rate: float, ece: float, filename: str = "behavioral_metrics.png") -> str:
        """
        Generates a summary horizontal bar chart of key behavioral metrics (Flip Rate % & ECE).
        """
        out_path = os.path.join(self.figures_dir, filename)

        metrics = ['Prediction Flip Rate (%)', 'Expected Calibration Error (ECE x100)']
        values = [flip_rate * 100.0, ece * 100.0]
        colors = ['#3498db', '#1abc9c']

        fig, ax = plt.subplots(figsize=(7, 3.5), dpi=300)
        bars = ax.barh(metrics, values, color=colors, height=0.45, edgecolor='black', linewidth=0.8)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1.5, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                    va='center', ha='left', fontsize=11, fontweight='bold')

        ax.set_xlim(0, max(max(values) + 20, 100))
        ax.set_xlabel("Percentage (%)", fontsize=11, fontweight='bold')
        ax.set_title("Behavioral Testing Diagnostic Metrics", fontsize=13, fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return os.path.abspath(out_path)

    def plot_attribution_comparison(self, explanations_summary: List[Dict[str, Any]], filename: str = "attribution_comparison.png") -> str:
        """
        Generates a bar chart comparing original vs perturbed token attributions for the first probe.
        """
        out_path = os.path.join(self.figures_dir, filename)

        if not explanations_summary:
            fig, ax = plt.subplots(figsize=(6, 3), dpi=300)
            ax.text(0.5, 0.5, "No Explanation Data Available", ha='center', va='center')
            plt.savefig(out_path, dpi=300)
            plt.close(fig)
            return os.path.abspath(out_path)

        first_exp = explanations_summary[0]
        orig_dict = first_exp.get("orig_explanation", {})
        pert_dict = first_exp.get("pert_explanation", {})

        if isinstance(orig_dict, dict) and "token_weights" in orig_dict:
            orig_dict = orig_dict["token_weights"]
        if isinstance(pert_dict, dict) and "token_weights" in pert_dict:
            pert_dict = pert_dict["token_weights"]

        # Collect top tokens
        all_tokens = list(set(list(orig_dict.keys())[:5] + list(pert_dict.keys())[:5]))[:8]
        if not all_tokens:
            all_tokens = ["(N/A)"]
            orig_vals = [0.0]
            pert_vals = [0.0]
        else:
            orig_vals = [float(orig_dict.get(t, 0.0)) if isinstance(orig_dict.get(t), (int, float)) else 0.0 for t in all_tokens]
            pert_vals = [float(pert_dict.get(t, 0.0)) if isinstance(pert_dict.get(t), (int, float)) else 0.0 for t in all_tokens]

        x = np.arange(len(all_tokens))
        width = 0.35

        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
        ax.bar(x - width/2, orig_vals, width, label='Original Input', color='#2980b9', edgecolor='black', linewidth=0.5)
        ax.bar(x + width/2, pert_vals, width, label='Perturbed Input', color='#e74c3c', edgecolor='black', linewidth=0.5)

        ax.set_ylabel('Attribution Weight', fontsize=11, fontweight='bold')
        ax.set_title(f"Token Attribution Shift Probe #{1} ({first_exp.get('type', 'perturbation')})", fontsize=13, fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(all_tokens, rotation=30, ha='right', fontsize=10)
        ax.legend(frameon=True, facecolor='white', framealpha=0.9)
        ax.axhline(0, color='black', linewidth=0.8, linestyle='--')

        plt.tight_layout()
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return os.path.abspath(out_path)

    def plot_probe_alignment(self, explanations_summary: List[Dict[str, Any]], filename: str = "probe_alignment_summary.png") -> str:
        """
        Generates a group bar chart of Jaccard Similarity & Cosine Alignment across all probes.
        """
        out_path = os.path.join(self.figures_dir, filename)

        if not explanations_summary:
            probe_labels = ["Probe 1"]
            jaccard_scores = [1.0]
            cosine_scores = [1.0]
        else:
            probe_labels = [f"P{i+1}: {item.get('type', '')[:10]}" for i, item in enumerate(explanations_summary)]
            jaccard_scores = [item.get("jaccard_similarity", 0.0) for item in explanations_summary]
            cosine_scores = [item.get("cosine_alignment", 0.0) for item in explanations_summary]

        x = np.arange(len(probe_labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(max(7, len(probe_labels)*1.5), 4.5), dpi=300)
        rects1 = ax.bar(x - width/2, jaccard_scores, width, label='Jaccard Top-K Similarity', color='#8e44ad', edgecolor='black', linewidth=0.5)
        rects2 = ax.bar(x + width/2, cosine_scores, width, label='Cosine Attribution Alignment', color='#16a085', edgecolor='black', linewidth=0.5)

        ax.set_ylabel('Consistency Score (0.0 to 1.0)', fontsize=11, fontweight='bold')
        ax.set_title('Explanation Alignment Across Perturbation Probes', fontsize=13, fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(probe_labels, rotation=25, ha='right', fontsize=9)
        ax.set_ylim(0, 1.15)
        ax.legend(loc='upper right', frameon=True, facecolor='white')
        ax.axhline(1.0, color='gray', linestyle=':', alpha=0.7)

        plt.tight_layout()
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return os.path.abspath(out_path)

    def generate_all_plots(
        self,
        audit_results: Dict[str, Any],
        failures: List[Dict[str, Any]],
        explanations_summary: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Generates all 4 publication graphs and returns dict mapping chart keys to absolute file paths.
        """
        flip_rate = audit_results.get("flip_rate", 0.0)
        ece = audit_results.get("ece", 0.0)

        tax_path = self.plot_taxonomy_distribution(failures)
        met_path = self.plot_behavioral_metrics(flip_rate, ece)
        att_path = self.plot_attribution_comparison(explanations_summary)
        alg_path = self.plot_probe_alignment(explanations_summary)

        return {
            "taxonomy_distribution": tax_path,
            "behavioral_metrics": met_path,
            "attribution_comparison": att_path,
            "probe_alignment": alg_path,
        }

    def generate_thesis_figures(self, experiment_results: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates all 15 publication-grade thesis figures and saves source_data.json.
        """
        from blindspot.reporting.thesis_graphs import ThesisVisualizer
        tv = ThesisVisualizer(figures_dir=self.figures_dir)
        return tv.generate_all_15_figures(experiment_results)
