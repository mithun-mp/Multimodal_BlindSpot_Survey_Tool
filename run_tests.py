import unittest
import sys
import os
import warnings

# Suppress non-actionable third-party deprecation warnings (Transformers, SHAP, PyTorch)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Add workspace to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tests.test_perturbations import (
    test_negation_perturber,
    test_double_negation_perturber,
    test_connective_perturber,
    test_synonym_substitution_perturber,
    test_perturbation_engine,
    test_linguistic_analyzer
)
from tests.test_models import test_huggingface_wrapper
from tests.test_behavioral import test_metrics, test_behavioral_tester
from tests.test_explainability import test_explainers, test_audit_pipeline_explainer_selection, test_taxonomy_classifier
from tests.test_reports import test_report_generator
from tests.test_visualizer import test_visualizer_generate_all_plots

from tests.test_multiclass import TestMulticlassFeatures
from tests.test_model_registry import TestModelRegistry
from tests.test_shared_probes import TestSharedProbes
from tests.test_cross_model import TestCrossModelAnalysis
from tests.test_resource_manager import TestResourceManager
from tests.test_caching_and_batching import TestCachingAndBatching
from tests.test_live_events_and_jobs import TestLiveEventsAndJobs
from tests.test_experiment_persistence import TestExperimentPersistence
from tests.test_repeated_tokens import TestRepeatedTokenAttributions
from tests.test_ui_and_launchers import TestUiAndLaunchers
from tests.test_probe_integrity import TestProbeIntegrity
from tests.test_behavioral_taxonomy import TestBehavioralTaxonomyCalibration
from tests.test_flip_analysis import TestFlipAnalysis
from tests.test_probe_calibration import TestProbeCalibration
from tests.test_deterministic_acceptance import TestDeterministicAcceptance
from tests.test_research_repair import (
    TestModelValidationGate,
    TestProbePipelineAndCountIntegrity,
    TestTaxonomyClassifierCalibration,
    TestDeterministicBenchmarkAcceptance,
)

import tempfile
import pathlib


class TestBlindSpotBaseline(unittest.TestCase):
    def test_01_negation(self):
        test_negation_perturber()

    def test_02_double_negation(self):
        test_double_negation_perturber()

    def test_03_connective(self):
        test_connective_perturber()

    def test_04_synonym_substitution(self):
        test_synonym_substitution_perturber()

    def test_05_engine(self):
        test_perturbation_engine()

    def test_05b_linguistic_analyzer(self):
        test_linguistic_analyzer()

    def test_06_model_wrapper(self):
        test_huggingface_wrapper()

    def test_07_metrics(self):
        test_metrics()

    def test_08_behavioral_tester(self):
        test_behavioral_tester()

    def test_09_explainability(self):
        test_explainers()

    def test_10_pipeline_explainer_selection(self):
        test_audit_pipeline_explainer_selection()

    def test_11_taxonomy(self):
        test_taxonomy_classifier()

    def test_12_reports(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_report_generator(pathlib.Path(tmp_dir))

    def test_13_visualizer(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_visualizer_generate_all_plots(pathlib.Path(tmp_dir))


from tests.test_persistence_and_lifecycle import TestPersistenceAndLifecycle
from tests.test_canonical_pipeline import TestCanonicalPipeline


def load_suite(full_benchmark: bool = False) -> unittest.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Fast deterministic unit and regression tests
    suite.addTests(loader.loadTestsFromTestCase(TestCanonicalPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestModelValidationGate))
    suite.addTests(loader.loadTestsFromTestCase(TestProbePipelineAndCountIntegrity))
    suite.addTests(loader.loadTestsFromTestCase(TestTaxonomyClassifierCalibration))
    suite.addTests(loader.loadTestsFromTestCase(TestModelRegistry))
    suite.addTests(loader.loadTestsFromTestCase(TestPersistenceAndLifecycle))
    suite.addTests(loader.loadTestsFromTestCase(TestExperimentPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestSharedProbes))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossModelAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestResourceManager))
    suite.addTests(loader.loadTestsFromTestCase(TestCachingAndBatching))
    suite.addTests(loader.loadTestsFromTestCase(TestRepeatedTokenAttributions))
    suite.addTests(loader.loadTestsFromTestCase(TestProbeIntegrity))
    suite.addTests(loader.loadTestsFromTestCase(TestBehavioralTaxonomyCalibration))
    suite.addTests(loader.loadTestsFromTestCase(TestFlipAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestProbeCalibration))
    suite.addTests(loader.loadTestsFromTestCase(TestDeterministicAcceptance))
    suite.addTests(loader.loadTestsFromTestCase(TestMulticlassFeatures))

    if full_benchmark:
        # Full heavy transformer inference suite (evaluates all 5 models)
        suite.addTests(loader.loadTestsFromTestCase(TestBlindSpotBaseline))
        suite.addTests(loader.loadTestsFromTestCase(TestDeterministicBenchmarkAcceptance))
        suite.addTests(loader.loadTestsFromTestCase(TestLiveEventsAndJobs))

    return suite


if __name__ == "__main__":
    is_full = "--full" in sys.argv
    suite = load_suite(full_benchmark=is_full)
    runner = unittest.TextTestRunner(verbosity=2)
    mode_str = "FULL BENCHMARK" if is_full else "FAST UNIT TEST SUITE (use --full for full transformer benchmark)"
    print(f"\n=======================================================")
    print(f" BLINDSPOT TEST RUNNER: {mode_str}")
    print(f"=======================================================\n")
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
