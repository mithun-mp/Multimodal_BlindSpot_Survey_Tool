import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from blindspot.perturbations import (
    NegationPerturber,
    DoubleNegationPerturber,
    ConnectivePerturber,
    SynonymSubstitutionPerturber,
    PerturbationEngine
)

def test_negation_perturber():
    perturber = NegationPerturber()
    sentence = "The movie was great."
    variants = perturber.perturb(sentence)
    assert len(variants) > 0
    assert any("not" in v["perturbed"].lower() for v in variants)

def test_double_negation_perturber():
    perturber = DoubleNegationPerturber()
    sentence = "The food was good."
    variants = perturber.perturb(sentence)
    assert len(variants) > 0
    assert any("not" in v["perturbed"].lower() for v in variants)

def test_connective_perturber():
    perturber = ConnectivePerturber()
    sentence = "The product works fine."
    variants = perturber.perturb(sentence)
    assert len(variants) >= 3
    types = [v["type"] for v in variants]
    assert "contrast_positive_append" in types
    assert "contrast_negative_append" in types
    assert "contrast_concession_prefix" in types

    # Ensure hardcoded customer review and static fallback phrases are completely eliminated
    banned_static = [
        "complete garbage",
        "overall experience was outstanding",
        "remarkably impressive",
        "satisfactory"
    ]
    for v in variants:
        for phrase in banned_static:
            assert phrase not in v["perturbed"]

    # Test dynamic generation on scientific statement
    sun_variants = perturber.perturb("The sun is hot.")
    neg_variant = next(v for v in sun_variants if v["type"] == "contrast_negative_append")
    assert "cold" in neg_variant["perturbed"] or "cool" in neg_variant["perturbed"]

    # Test dynamic generation on action/duration sentence
    batt_variants = perturber.perturb("The battery lasts 2 hours.")
    batt_neg = next(v for v in batt_variants if v["type"] == "contrast_negative_append")
    assert "last" in batt_neg["perturbed"]

    # Test dynamic generation on human agent & transitive action sentence
    human_variants = perturber.perturb("she smashes him")
    human_neg = next(v for v in human_variants if v["type"] == "contrast_negative_append")
    assert "heavy load" not in human_neg["perturbed"]
    assert "defeat" in human_neg["perturbed"] or "him" in human_neg["perturbed"]




def test_synonym_substitution_perturber():
    perturber = SynonymSubstitutionPerturber()
    sentence = "This is a great movie."
    variants = perturber.perturb(sentence)
    assert len(variants) > 0

def test_perturbation_engine():
    engine = PerturbationEngine()
    sentence = "The performance was awesome."
    all_variants = engine.generate_all(sentence)
    assert len(all_variants) >= 5

def test_linguistic_analyzer():
    from blindspot.perturbations import LinguisticAnalyzer
    analyzer = LinguisticAnalyzer()

    # Test 1: Simple factual statement
    f1 = analyzer.extract_features("The sun is hot.")
    assert f1.subject.lower() == "sun"
    assert f1.pronoun == "it"
    assert f1.copula == "is"
    assert f1.descriptor == "hot"
    assert "cold" in f1.antonyms or "freezing" in f1.antonyms

    # Test 2: Plural past tense
    f2 = analyzer.extract_features("The algorithms ran quickly.")
    assert f2.is_plural is True
    assert f2.pronoun == "they"
    assert f2.is_past_tense is True
    assert f2.copula == "were"
    assert f2.descriptor == "quickly"
    assert "slowly" in f2.antonyms

    # Test 3: Evaluative statement with past copula
    f3 = analyzer.extract_features("The food was delicious.")
    assert f3.subject.lower() == "food"
    assert f3.pronoun == "it"
    assert f3.is_past_tense is True
    assert f3.copula == "was"
    assert f3.descriptor == "delicious"
    assert len(f3.antonyms) > 0

