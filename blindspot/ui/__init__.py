"""
UI Module for BlindSpot Framework.
Provides modular views for the research workstation and Streamlit dashboard.
"""
from blindspot.ui.overview import render_overview
from blindspot.ui.experiment_lab import render_experiment_lab
from blindspot.ui.model_lab import render_model_lab
from blindspot.ui.probe_lab import render_probe_lab
from blindspot.ui.live_run import render_live_run
from blindspot.ui.comparison import render_comparison
from blindspot.ui.explanation_lab import render_explanation_lab
from blindspot.ui.failure_lab import render_failure_lab
from blindspot.ui.reports_view import render_reports
from blindspot.ui.run_history import render_run_history
from blindspot.ui.system_monitor import render_system_monitor
from blindspot.ui.console import render_console
from blindspot.ui.shell import render_shell

__all__ = [
    "render_overview",
    "render_experiment_lab",
    "render_model_lab",
    "render_probe_lab",
    "render_live_run",
    "render_console",
    "render_comparison",
    "render_explanation_lab",
    "render_failure_lab",
    "render_reports",
    "render_run_history",
    "render_system_monitor",
    "render_shell",
]
