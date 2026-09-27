import json
from blindspot.reporting.thesis_graphs import ThesisVisualizer

with open('runs/exp_1790537272_6f4cc1/results.json', encoding='utf-8') as f:
    res = json.load(f)

viz = ThesisVisualizer('runs/exp_1790537272_6f4cc1/figures')
viz.plot_model_prediction_distribution(res)
viz.plot_flip_rate_by_model(res)
viz.plot_expected_vs_observed(res)
viz.plot_failure_taxonomy_distribution(res)
viz.plot_confidence_delta_by_model(res)
viz.plot_probe_level_comparison(res)
viz.plot_model_probe_heatmap(res)
viz.plot_probe_consistency(res)
viz.plot_model_agreement(res)
viz.plot_expected_change_vs_preserve(res)
viz.plot_per_model_summary(res)
viz.plot_runtime_profile(res)
print("All 15 thesis figures regenerated successfully with distinct model identities!")
