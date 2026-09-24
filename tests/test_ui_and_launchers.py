"""
Unit tests for BlindSpot UI/UX components, design system, structured logging, and launchers.
"""
import sys
import os
import unittest
import tempfile
import pathlib
from unittest.mock import patch, MagicMock

# Ensure workspace root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.ui import (
    render_overview,
    render_experiment_lab,
    render_model_lab,
    render_probe_lab,
    render_live_run,
    render_console,
    render_comparison,
    render_explanation_lab,
    render_failure_lab,
    render_reports,
    render_run_history,
    render_system_monitor,
    render_shell,
)
from blindspot.ui.design_system import (
    THEME_COLORS,
    WORKSTATION_CSS,
    inject_workstation_theme,
)
from blindspot.ui.components import (
    render_workstation_header,
    render_technical_model_card,
    render_probe_preview_card,
    render_failure_record,
    render_console_log_line,
    render_empty_state,
    render_failure_badge,
    render_provenance_badge,
)
from blindspot.core.logging_config import (
    configure_workstation_logging,
    close_workstation_logging,
    get_subsystem_logger,
    SubsystemFormatter,
)
from blindspot.launcher import resolve_server_port, is_port_in_use


class TestUiAndLaunchers(unittest.TestCase):
    """Test suite covering UI pages, design system tokens, loggers, and launcher scripts."""

    def test_ui_page_modules_callable(self):
        """Verifies that all 12 workstation UI page modules exist and are callable."""
        pages = [
            render_overview,
            render_experiment_lab,
            render_model_lab,
            render_probe_lab,
            render_live_run,
            render_console,
            render_comparison,
            render_explanation_lab,
            render_failure_lab,
            render_reports,
            render_run_history,
            render_system_monitor,
        ]
        for page_fn in pages:
            self.assertTrue(callable(page_fn))

    def test_design_system_tokens(self):
        """Verifies color tokens and CSS theme presence."""
        self.assertIn("bg_dark", THEME_COLORS)
        self.assertIn("accent", THEME_COLORS)
        self.assertIn("success", THEME_COLORS)
        self.assertIn("warning", THEME_COLORS)
        self.assertIn("font-family", WORKSTATION_CSS)
        self.assertIn(":root", WORKSTATION_CSS)

    @patch("streamlit.markdown")
    def test_component_rendering(self, mock_markdown):
        """Verifies that design system components generate valid HTML without throwing exceptions."""
        render_technical_model_card(
            model_id="distilbert-base-uncased-finetuned-sst-2-english",
            architecture="DistilBERT",
            num_classes=2,
            params_millions=66.96,
            is_cached=True,
            is_selected=True,
        )
        self.assertTrue(mock_markdown.called)

        render_probe_preview_card(
            probe_id="P001",
            original_text="The film was great.",
            perturbed_text="The film was not great.",
            perturbation_type="negation",
            expected_semantic_effect="invert",
            expected_flip=True,
        )
        self.assertTrue(mock_markdown.called)

        render_failure_record({
            "category": "Blind",
            "model_id": "test-model",
            "probe_id": "P001",
            "probe_type": "negation",
            "original_sentence": "Good.",
            "perturbed_sentence": "Not good.",
            "original_label": "POSITIVE",
            "perturbed_label": "POSITIVE",
            "expected_flip": True,
            "confidence_delta_pts": -20.0,
            "details": "Model failed to invert.",
            "recommendation": "Fine-tune on negation pairs.",
        })
        self.assertTrue(mock_markdown.called)

    def test_structured_subsystem_logging(self):
        """Verifies structured rotating logging and subsystem formatting."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                log_dir = os.path.join(tmp_dir, "test_logs")
                configure_workstation_logging(log_dir=log_dir, log_file="test_audit.log")

                logger = get_subsystem_logger("MODEL")
                logger.info("Loaded model weights into cache.")

                log_file = os.path.join(log_dir, "test_audit.log")
                self.assertTrue(os.path.exists(log_file))
                with open(log_file, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertIn("MODEL", content)
                self.assertIn("Loaded model weights into cache.", content)
            finally:
                close_workstation_logging()

    def test_launcher_scripts_exist(self):
        """Verifies the presence of Windows batch and PowerShell launchers on disk."""
        self.assertTrue(os.path.exists("launch_blindspot.bat"), "launch_blindspot.bat is missing")
        self.assertTrue(os.path.exists("launch_blindspot.ps1"), "launch_blindspot.ps1 is missing")
        self.assertTrue(os.path.exists("create_blindspot_shortcut.ps1"), "create_blindspot_shortcut.ps1 is missing")

    def test_port_resolution_behavior(self):
        """Verifies port detection handles unbound ports gracefully."""
        test_port = 59123
        self.assertFalse(is_port_in_use(test_port))
        port, is_existing = resolve_server_port(start_port=test_port)
        self.assertEqual(port, test_port)
        self.assertFalse(is_existing)


if __name__ == "__main__":
    unittest.main()
