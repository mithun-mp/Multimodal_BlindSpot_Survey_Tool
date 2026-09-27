import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import numpy as np
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.testing.behavioral import BehavioralTester
from blindspot.testing.metrics import compute_flip_rate, compute_ece

def test_metrics():
    flip_rate = compute_flip_rate("POSITIVE", ["POSITIVE", "NEGATIVE", "NEGATIVE", "POSITIVE"])
    assert flip_rate == 0.5

    confidences = np.array([0.9, 0.8, 0.95, 0.7])
    predictions = np.array([1, 1, 0, 1])
    labels = np.array([1, 1, 1, 1])
    ece = compute_ece(confidences, predictions, labels)
    assert 0.0 <= ece <= 1.0

def test_behavioral_tester():
    model = HuggingFaceWrapper("distilbert-base-uncased-finetuned-sst-2-english")
    tester = BehavioralTester(model)

    items = [
        {"perturbed": "The movie was not great.", "type": "negation_insertion", "description": "negated"},
        {"perturbed": "The movie was fantastic.", "type": "synonym_substitution", "description": "synonym"}
    ]
    res = tester.evaluate_probe("The movie was great.", items)
    assert res["total_perturbations"] == 2
    assert "flip_rate" in res
    assert "ece" in res

def test_input_validation_and_suitability():
    from blindspot.audit import AuditPipeline

    pipeline = AuditPipeline(explainer_type="lime")

    # 1. 12345 -> rejected
    with pytest.raises(ValueError, match="meaningful natural-language text"):
        pipeline.validate_input("12345")

    # 2. !!! -> rejected
    with pytest.raises(ValueError, match="meaningful natural-language text"):
        pipeline.validate_input("!!!")

    # 3. 'the movie' -> accepted with suitability warning
    clean_3 = pipeline.validate_input("the movie")
    suit_3 = pipeline.check_suitability(clean_3)
    assert suit_3["status"] == "unsuitable"
    assert "Warning" in suit_3["warning"]

    # 4. 'The movie was normal.' -> accepted, potentially ambiguous warning
    clean_4 = pipeline.validate_input("The movie was normal.")
    suit_4 = pipeline.check_suitability(clean_4)
    assert suit_4["status"] == "unsuitable"
    assert suit_4["is_ambiguous"] is True
    assert "weak/ambiguous" in suit_4["warning"]

    # 5. 'The movie was excellent.' -> suitable
    clean_5 = pipeline.validate_input("The movie was excellent.")
    suit_5 = pipeline.check_suitability(clean_5)
    assert suit_5["status"] == "suitable"
    assert suit_5["warning"] is None

    # 6. 'The movie was 10/10.' -> accepted (numbers in text allowed)
    clean_6 = pipeline.validate_input("The movie was 10/10.")
    assert clean_6 == "The movie was 10/10."
    suit_6 = pipeline.check_suitability(clean_6)
    assert suit_6["status"] == "suitable"

    # 7. 'The movie received a rating of 2/10.' -> accepted (numbers in text allowed)
    clean_7 = pipeline.validate_input("The movie received a rating of 2/10.")
    assert clean_7 == "The movie received a rating of 2/10."
    suit_7 = pipeline.check_suitability(clean_7)
    assert suit_7["status"] == "suitable"

    # 8. Existing valid inputs continue to work
    clean_8 = pipeline.validate_input("I really enjoyed this movie.")
    assert clean_8 == "I really enjoyed this movie."
    suit_8 = pipeline.check_suitability(clean_8)
    assert suit_8["status"] == "suitable"


