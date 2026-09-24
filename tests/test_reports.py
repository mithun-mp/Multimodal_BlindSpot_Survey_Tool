import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import shutil
from blindspot.reporting import ReportGenerator

def test_report_generator(tmp_path):
    output_dir = str(tmp_path / "test_reports")
    generator = ReportGenerator(output_dir=output_dir)

    audit_results = {
        "original_sentence": "The food was delicious.",
        "original_prediction": "POSITIVE",
        "original_confidence": 0.98,
        "total_perturbations": 1,
        "flip_rate": 1.0,
        "ece": 0.05,
        "probe_details": [{
            "type": "negation_insertion",
            "description": "inserted not",
            "original": "The food was delicious.",
            "perturbed": "The food was not delicious.",
            "original_label": "POSITIVE",
            "original_confidence": 0.98,
            "perturbed_label": "NEGATIVE",
            "perturbed_confidence": 0.92,
            "is_flipped": True,
            "expected_flip": True,
            "unexpected_behavior": False,
        }]
    }

    failures = []
    explanations_summary = [{
        "type": "negation_insertion",
        "original": "The food was delicious.",
        "perturbed": "The food was not delicious.",
        "jaccard_similarity": 0.5,
        "cosine_alignment": 0.8,
        "pert_explanation": {"not": -0.6, "delicious": 0.3}
    }]

    files = generator.generate_all_reports("distilbert-sst2", audit_results, failures, explanations_summary)
    assert len(files) >= 4
    for fpath in files:
        assert os.path.exists(fpath)
