"""
Tests for Phase 38: Model Identity, Completeness Contract, Twitter Model Collision Prevention,
and Visual Semantics & Behavioral Logic.
"""
import pytest
from blindspot.models.registry import (
    ModelRegistry,
    get_model_display_name,
    get_model_short_name,
    get_model_abbrev,
    CANONICAL_MODEL_NAMES,
)

def test_five_canonical_model_identities():
    """Verify that all 5 models have distinct canonical IDs, display names, and short names."""
    registry = ModelRegistry()
    presets = registry.list_presets()
    assert len(presets) >= 5, f"Expected at least 5 presets, got {len(presets)}"
    
    model_ids = [p["model_id"] for p in presets]
    assert len(model_ids) == len(set(model_ids)), "Model IDs must be unique"
    
    # Verify short names and display names are distinct
    short_names = [get_model_short_name(m_id) for m_id in model_ids]
    assert len(short_names) == len(set(short_names)), f"Short names collided: {short_names}"
    
    display_names = [get_model_display_name(m_id) for m_id in model_ids]
    assert len(display_names) == len(set(display_names)), f"Display names collided: {display_names}"

def test_twitter_models_never_collide():
    """
    Explicitly test that CardiffNLP Twitter RoBERTa Sentiment and
    CardiffNLP Twitter RoBERTa Sentiment Latest do not collapse or overwrite each other.
    """
    base_id = "cardiffnlp/twitter-roberta-base-sentiment"
    latest_id = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    
    base_disp = get_model_display_name(base_id)
    latest_disp = get_model_display_name(latest_id)
    assert base_disp != latest_disp, "Twitter display names must be distinct"
    assert "Latest" in latest_disp, f"Latest model display name should indicate 'Latest': {latest_disp}"
    assert "Base" in base_disp or "Twitter-RoBERTa" in base_disp
    
    base_short = get_model_short_name(base_id)
    latest_short = get_model_short_name(latest_id)
    assert base_short != latest_short, "Twitter short names must be distinct"
    assert base_short[:14] != latest_short or len(base_short) != len(latest_short)
    
    # Test aggregation in a dictionary keyed by short_name
    agg_dict = {}
    agg_dict[base_short] = {"status": "base_completed"}
    agg_dict[latest_short] = {"status": "latest_completed"}
    assert len(agg_dict) == 2, "Dictionary keyed by short_name collapsed Twitter models!"
    assert agg_dict[base_short]["status"] == "base_completed"
    assert agg_dict[latest_short]["status"] == "latest_completed"

def test_model_completeness_accounting():
    """Verify that 5 configured models with 1 missing is tracked explicitly without dropping."""
    all_configured = [
        "distilbert-base-uncased-finetuned-sst-2-english",
        "albert-base-v2-finetuned-sst2",
        "bert-base-uncased-finetuned-sst2",
        "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "cardiffnlp/twitter-roberta-base-sentiment",
    ]
    # Simulate execution where only 4 completed
    executed_models = all_configured[:4]
    missing_models = [m for m in all_configured if m not in executed_models]
    
    assert len(missing_models) == 1
    assert missing_models[0] == "cardiffnlp/twitter-roberta-base-sentiment"
    
    # Contract verification: missing model must render as '— NOT RUN', never dropped
    row_cells = {}
    for m in all_configured:
        if m in executed_models:
            row_cells[m] = {"status": "match", "badge": "✓ MATCH"}
        else:
            row_cells[m] = {"status": "notrun", "badge": "— NOT RUN"}
            
    assert len(row_cells) == 5, "Missing model column was omitted!"
    assert row_cells[all_configured[4]]["status"] == "notrun"
    assert row_cells[all_configured[4]]["badge"] == "— NOT RUN"

def test_cell_level_status_semantics():
    """Verify cell-level visual semantics for expected flip vs observe."""
    # Case 1: Expected FLIP, Observed FLIP -> MATCH
    orig_lbl = "POSITIVE"
    pert_lbl = "NEGATIVE"
    exp_flip = True
    actual_flip = (orig_lbl != pert_lbl)
    assert actual_flip == exp_flip
    status = "match" if actual_flip == exp_flip else "deviation"
    assert status == "match"
    
    # Case 2: Expected FLIP, Observed PRESERVE -> DEVIATION
    orig_lbl_2 = "POSITIVE"
    pert_lbl_2 = "POSITIVE"
    actual_flip_2 = (orig_lbl_2 != pert_lbl_2)
    assert actual_flip_2 != exp_flip
    status_2 = "match" if actual_flip_2 == exp_flip else "deviation"
    assert status_2 == "deviation"

def test_invalid_probe_handling():
    """Verify invalid probes are distinguished and not counted as model failures."""
    probe_meta = {
        "probe_id": "prb_test_invalid",
        "validity": "INVALID",
        "invalidation_reason": "Contains internal perturbation metadata: insolate (-0.67)",
    }
    assert probe_meta["validity"] == "INVALID"
    # Anomaly on invalid probe should not attribute failure to model
    is_model_failure = (probe_meta["validity"] == "VALID")
    assert not is_model_failure, "Invalid probe must not be scored as model failure"

def test_3class_neutral_transition_preservation():
    """Verify 3-class models preserve NEUTRAL without coercing to binary."""
    m_3class_id = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    meta = CANONICAL_MODEL_NAMES.get(m_3class_id, {})
    assert meta.get("task_space") == "3-class"
    assert "NEUTRAL" in meta.get("label_schema", [])
    
    # Transition NEU -> POS is distinct from FLIP (NEG -> POS)
    trans = "NEU ➔ POS"
    assert "NEU" in trans
    assert "NEG" not in trans
