import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from blindspot.reporting.visualizer import Visualizer

def test_visualizer_generate_all_plots(tmp_path):
    figures_dir = str(tmp_path / "figures")
    visualizer = Visualizer(figures_dir=figures_dir)

    audit_results = {
        "flip_rate": 0.25,
        "ece": 0.082,
    }
    failures = [
        {"category": "Blind", "reason": "Ignored negation"},
        {"category": "Misweighted", "reason": "Skewed weight"},
    ]
    explanations_summary = [
        {
            "type": "single_negation",
            "original": "The food was delicious.",
            "perturbed": "The food was not delicious.",
            "orig_explanation": {"delicious": 0.8, "food": 0.1},
            "pert_explanation": {"not": -0.5, "delicious": 0.6},
            "jaccard_similarity": 0.5,
            "cosine_alignment": 0.72,
        }
    ]

    plots = visualizer.generate_all_plots(audit_results, failures, explanations_summary)

    assert "taxonomy_distribution" in plots
    assert "behavioral_metrics" in plots
    assert "attribution_comparison" in plots
    assert "probe_alignment" in plots

    for key, img_path in plots.items():
        assert os.path.exists(img_path)
        assert os.path.getsize(img_path) > 0
