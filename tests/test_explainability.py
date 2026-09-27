import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.audit import AuditPipeline
from blindspot.explainability import (
    LimeExplainerWrapper,
    ShapExplainerWrapper,
    compute_jaccard_similarity,
    compute_attribution_cosine,
    TaxonomyClassifier
)

def test_explainers():
    model = HuggingFaceWrapper("distilbert-base-uncased-finetuned-sst-2-english")
    lime_exp = LimeExplainerWrapper(model)
    shap_exp = ShapExplainerWrapper(model)

    exp1 = lime_exp.explain("The movie was fantastic.")
    assert isinstance(exp1, dict)
    assert len(exp1) > 0

    exp2 = shap_exp.explain("The movie was fantastic.")
    assert isinstance(exp2, dict)
    assert len(exp2) > 0

    jaccard = compute_jaccard_similarity(exp1, exp2)
    assert 0.0 <= jaccard <= 1.0

    cosine = compute_attribution_cosine(exp1, exp2)
    assert -1.0 <= cosine <= 1.0

def test_audit_pipeline_explainer_selection():
    # Test LIME mode
    pipeline_lime = AuditPipeline(explainer_type="lime")
    res_lime = pipeline_lime.run_audit("The food was delicious.")
    assert "explanations_summary" in res_lime

    # Test SHAP mode
    pipeline_shap = AuditPipeline(explainer_type="shap")
    res_shap = pipeline_shap.run_audit("The food was delicious.")
    assert "explanations_summary" in res_shap

    # Test Combined 'both' mode
    pipeline_both = AuditPipeline(explainer_type="both")
    res_both = pipeline_both.run_audit("The food was delicious.")
    assert "explanations_summary" in res_both

def test_taxonomy_classifier():
    taxonomy = TaxonomyClassifier()
    fail = taxonomy.classify_failure(
        perturbation_type="negation_insertion",
        original_sentence="The service was great.",
        perturbed_sentence="The service was not great.",
        original_label="POSITIVE",
        perturbed_label="POSITIVE", # Failed to flip
        is_flipped=False,
        expected_flip=True,
        orig_explanation={"great": 0.5},
        pert_explanation={"not": 0.0, "great": 0.5}
    )
    assert fail is not None
    assert fail["category"] == "Blind"

def test_taxonomy_ui_presentation():
    from blindspot.app import resolve_failure_metadata, get_failure_narrative
    
    # 1. Test Blind Failure
    fail_blind = {
        "category": "Blind",
        "reason": "Model ignored negation operator.",
        "details": "Model failed to flip prediction under negation_prefix.",
        "recommendation": "Fine-tune target model on negation augmentations.",
        "probe_type": "negation_prefix",
        "original_sentence": "The movie was great.",
        "perturbed_sentence": "The movie was not great.",
        "original_label": "POSITIVE",
        "perturbed_label": "POSITIVE",
        "original_confidence": 0.99,
        "perturbed_confidence": 0.95,
        "is_flipped": False,
        "expected_flip": True,
        "pert_explanation": {"not": 0.38}
    }
    meta = resolve_failure_metadata(fail_blind, [], "The movie was great.", "POSITIVE", 0.99)
    assert meta["probe_type"] == "negation_prefix"
    assert meta["conf_delta_pts"] is not None
    assert round(meta["conf_delta_pts"], 1) == -4.0

    narrative = get_failure_narrative("Blind", meta["probe_type"], meta["original_label"], meta["perturbed_label"], meta["is_flipped"], meta["expected_flip"])
    assert "BLIND" in narrative["badge"]
    assert "negation" in narrative["title"].lower()
    assert len(narrative["improvements"]) > 0

    # 2. Test Double Negation
    narrative_dn = get_failure_narrative("Blind", "double_negation", "POSITIVE", "NEGATIVE", True, False)
    assert "double" in narrative_dn["title"].lower()

    # 3. Test Misweighted Contrast
    narrative_mw = get_failure_narrative("Misweighted", "contrast_positive_append", "NEGATIVE", "NEGATIVE", False, True)
    assert "MISWEIGHTED" in narrative_mw["badge"]
    assert "contrast" in narrative_mw["test_name"].lower()

    # 4. Test Spurious
    narrative_sp = get_failure_narrative("Spurious", "domain_entity", "POSITIVE", "POSITIVE", False, False)
    assert "SPURIOUS" in narrative_sp["badge"]

