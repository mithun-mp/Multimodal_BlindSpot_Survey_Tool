import os
import sys

# Ensure workspace root is always in sys.path
_workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _workspace_root not in sys.path:
    sys.path.insert(0, _workspace_root)

import streamlit as st
import pandas as pd
import numpy as np
import re
from blindspot.audit import AuditPipeline
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

def render_markdown_with_images(content: str, base_dir: str = "audit_reports"):
    """
    Renders markdown content in Streamlit. If local image references ![alt](path)
    are detected, renders them using st.image so they display properly in the browser.
    """
    img_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    last_idx = 0

    for match in img_pattern.finditer(content):
        pre_text = content[last_idx:match.start()].strip()
        if pre_text:
            st.markdown(pre_text)

        alt_text = match.group(1)
        img_rel_path = match.group(2).replace("\\", "/")
        img_full_path = os.path.join(base_dir, img_rel_path)

        if os.path.exists(img_full_path):
            st.image(img_full_path, caption=alt_text or os.path.basename(img_full_path), use_container_width=True)
        else:
            st.markdown(match.group(0))

        last_idx = match.end()

    remaining = content[last_idx:].strip()
    if remaining:
        st.markdown(remaining)

def resolve_failure_metadata(fail: dict, beh_probes: list, original_text: str, orig_pred: str, orig_conf: float) -> dict:
    """
    Extracts or resolves full probe context for a failure item using existing backend data.
    """
    p_type = fail.get("probe_type")
    orig_sentence = fail.get("original_sentence") or original_text
    pert_sentence = fail.get("perturbed_sentence")
    orig_label = fail.get("original_label") or orig_pred
    pert_label = fail.get("perturbed_label")
    orig_c = fail.get("original_confidence", orig_conf)
    pert_c = fail.get("perturbed_confidence")
    is_flipped = fail.get("is_flipped")
    expected_flip = fail.get("expected_flip")
    pert_exp = fail.get("pert_explanation", {})
    orig_exp = fail.get("orig_explanation", {})

    # Fallback resolution from beh_probes if direct fields are missing
    if not p_type or not pert_sentence or pert_label is None:
        details_str = fail.get("details", "")
        for p in beh_probes:
            if p.get("type", "") in details_str:
                p_type = p.get("type")
                pert_sentence = p.get("perturbed")
                pert_label = p.get("perturbed_label")
                pert_c = p.get("perturbed_confidence")
                is_flipped = p.get("is_flipped")
                expected_flip = p.get("expected_flip")
                break
        if not pert_sentence and beh_probes:
            for p in beh_probes:
                if p.get("unexpected_behavior"):
                    p_type = p.get("type", p_type)
                    pert_sentence = p.get("perturbed")
                    pert_label = p.get("perturbed_label")
                    pert_c = p.get("perturbed_confidence")
                    is_flipped = p.get("is_flipped")
                    expected_flip = p.get("expected_flip")
                    break

    # Calculate confidence change in percentage points if available
    conf_delta_pts = None
    if orig_c is not None and pert_c is not None:
        conf_delta_pts = (pert_c - orig_c) * 100.0

    aligned_tokens = fail.get("aligned_tokens")
    if not aligned_tokens:
        from blindspot.explainability.token_attributions import align_token_attributions
        aligned_tokens = align_token_attributions(orig_sentence, pert_sentence or "", orig_exp, pert_exp)

    return {
        "probe_type": p_type or "linguistic_perturbation",
        "original_sentence": orig_sentence,
        "perturbed_sentence": pert_sentence or "Modified input unavailable",
        "original_label": orig_label or "Unknown",
        "perturbed_label": pert_label if pert_label is not None else "Unknown",
        "original_confidence": orig_c if orig_c is not None else 1.0,
        "perturbed_confidence": pert_c if pert_c is not None else 1.0,
        "is_flipped": is_flipped,
        "expected_flip": expected_flip,
        "conf_delta_pts": conf_delta_pts,
        "orig_explanation": orig_exp,
        "pert_explanation": pert_exp,
        "aligned_tokens": aligned_tokens,
        "severity": fail.get("severity")
    }

def find_key_misweighted_token(aligned_tokens: list = None, orig_exp: dict = None, pert_exp: dict = None) -> dict:
    """
    Identifies the key token occurrence whose attribution inverted polarity or changed
    most significantly between original and perturbed inputs. Preserves token occurrence identity.
    """
    if aligned_tokens:
        # Priority 1: Explicitly flagged key shift
        for r in aligned_tokens:
            if r.get("is_key_shift") and r.get("orig_val") is not None and r.get("pert_val") is not None:
                orig_val = r["orig_val"]
                pert_val = r["pert_val"]
                delta = r.get("delta", pert_val - orig_val)
                orig_dir = "Positive" if orig_val >= 0 else "Negative"
                pert_dir = "Positive" if pert_val >= 0 else "Negative"
                return {
                    "token": r["token"],
                    "position": r.get("orig_pos") or r.get("pert_pos") or 1,
                    "occurrence": r.get("orig_occ") or r.get("pert_occ") or 1,
                    "total_occ": r.get("total_occ", 1),
                    "orig_val": orig_val,
                    "pert_val": pert_val,
                    "delta": delta,
                    "orig_dir": orig_dir,
                    "pert_dir": pert_dir,
                    "polarity_changed": r.get("polarity_changed", False),
                    "direction_text": f"{orig_dir} → {pert_dir}"
                }
        # Priority 2: Inverted polarity, then max absolute delta
        candidates = [r for r in aligned_tokens if r.get("orig_val") is not None and r.get("pert_val") is not None]
        if candidates:
            pol_cands = [r for r in candidates if r.get("polarity_changed")]
            best = max(pol_cands, key=lambda r: abs(r.get("delta") or (r["pert_val"] - r["orig_val"]))) if pol_cands else max(candidates, key=lambda r: abs(r.get("delta") or (r["pert_val"] - r["orig_val"])))
            orig_val = best["orig_val"]
            pert_val = best["pert_val"]
            delta = best.get("delta", pert_val - orig_val)
            orig_dir = "Positive" if orig_val >= 0 else "Negative"
            pert_dir = "Positive" if pert_val >= 0 else "Negative"
            return {
                "token": best["token"],
                "position": best.get("orig_pos") or best.get("pert_pos") or 1,
                "occurrence": best.get("orig_occ") or best.get("pert_occ") or 1,
                "total_occ": best.get("total_occ", 1),
                "orig_val": orig_val,
                "pert_val": pert_val,
                "delta": delta,
                "orig_dir": orig_dir,
                "pert_dir": pert_dir,
                "polarity_changed": best.get("polarity_changed", False),
                "direction_text": f"{orig_dir} → {pert_dir}"
            }

    # Fallback to dicts if aligned_tokens not provided
    if not orig_exp or not pert_exp:
        return None
    
    syn_keys = [k for k in orig_exp if k in pert_exp]
    if not syn_keys:
        return None
    
    inverted = [
        k for k in syn_keys
        if (orig_exp[k] >= 0 and pert_exp[k] < 0) or (orig_exp[k] < 0 and pert_exp[k] >= 0)
    ]
    key_k = max(inverted, key=lambda k: abs(pert_exp[k] - orig_exp[k])) if inverted else max(syn_keys, key=lambda k: abs(pert_exp[k] - orig_exp[k]))
    orig_val = orig_exp[key_k]
    pert_val = pert_exp[key_k]
    delta = pert_val - orig_val
    orig_dir = "Positive" if orig_val >= 0 else "Negative"
    pert_dir = "Positive" if pert_val >= 0 else "Negative"
    return {
        "token": key_k,
        "position": 1,
        "occurrence": 1,
        "total_occ": 1,
        "orig_val": orig_val,
        "pert_val": pert_val,
        "delta": delta,
        "orig_dir": orig_dir,
        "pert_dir": pert_dir,
        "polarity_changed": (orig_val >= 0) != (pert_val >= 0),
        "direction_text": f"{orig_dir} → {pert_dir}"
    }

def generate_attribution_interpretation(p_type: str, pert_label: str, pert_exp: dict, orig_exp: dict = None, key_ev: dict = None) -> str:
    """
    Connects quantitative attribution weights directly to the observed behavioral failure.
    """
    pt_lower = (p_type or "").lower()
    if "negation" in pt_lower:
        neg_tokens = [w for w in pert_exp.keys() if w.lower() in {"not", "never", "no", "n't"}]
        if neg_tokens:
            top_neg = max(neg_tokens, key=lambda w: abs(pert_exp[w]))
            top_weight = pert_exp[top_neg]
            if abs(top_weight) >= 0.05:
                return (
                    f"The negation token '{top_neg}' receives a measurable attribution weight ({top_weight:+.4f}), "
                    f"yet the overall classification remained {pert_label}. This indicates that the negation cue "
                    f"was outweighed by remaining sentiment-bearing tokens in the sentence representation."
                )
            else:
                return (
                    f"The negation token '{top_neg}' receives minimal attribution ({top_weight:+.4f}), "
                    f"indicating that the explanation method assigns negligible decision importance to the negation operator "
                    f"relative to dominant sentiment keywords."
                )
        return (
            "The observed prediction did not shift under negation. The attribution distribution indicates that the decision "
            "continues to be dominated by lexical sentiment tokens rather than the syntactic modifier."
        )
    elif "contrast" in pt_lower:
        return (
            "The attribution distribution shows feature weights dispersed across both clauses. "
            "Although the contrastive connective introduced an opposing proposition, the model prediction remained aligned "
            "with the dominant initial clause, indicating an imbalance in clause weighting."
        )
    elif "substitution" in pt_lower:
        if key_ev:
            occ_str = f" (occurrence #{key_ev['occurrence']} at position {key_ev['position']})" if key_ev.get("total_occ", 1) > 1 else f" (at position {key_ev['position']})"
            return (
                f"The synonym substitution did not change the predicted class ({pert_label}) or confidence. "
                f"However, the attribution assigned to the highlighted token '{key_ev['token']}'{occ_str} changed from "
                f"{key_ev['orig_dir'].lower()} to {key_ev['pert_dir'].lower()} ({key_ev['orig_val']:+.4f} → {key_ev['pert_val']:+.4f}). "
                f"This indicates that the model's local feature weighting is sensitive to the lexical substitution "
                f"even though the final decision remains stable."
            )
        return (
            "The synonym substitution did not change the predicted class or confidence. "
            "However, the attribution pattern changed across semantically similar inputs. "
            "This suggests local sensitivity in the model's feature weighting across semantically similar inputs."
        )
    elif "spurious" in pt_lower:
        return (
            "Feature attributions are heavily concentrated on non-sentiment domain entity tokens, indicating that "
            "the model's prediction depends on non-causal lexical associations."
        )
    return (
        "The token attribution pattern provides empirical evidence of feature reliance during inference under this perturbation."
    )

def get_failure_narrative(category: str, p_type: str, orig_label: str, pert_label: str, is_flipped: bool, expected_flip: bool) -> dict:
    """
    Returns intermediate-level scientific titles, explanations, and actionable remediation text
    tailored for ML/NLP students, researchers, and developers.
    """
    cat_lower = (category or "").lower()
    pt_lower = (p_type or "").lower()

    if "blind" in cat_lower:
        if "double" in pt_lower:
            badge = "BLIND"
            title = "Model struggled with double negation"
            short_desc = "The classifier did not change its prediction as expected after a double negation structure was introduced."
            test_name = "Double Negation"
            test_desc = "A second negation cue was introduced to evaluate whether the classifier correctly combines their effects."
            why_failure = (
                "Double negation requires the model to combine multiple linguistic cues rather than treating each token independently. "
                "The model did not change its prediction as expected, suggesting difficulty in composing multiple negation signals."
            )
            recommended_step = (
                "Incorporate paired litotes and double-negation constructions in the fine-tuning corpus to teach compound modifier resolution."
            )
            additional_steps = [
                "Test paired assertions where double negation mathematically resolves back to the affirmative meaning.",
                "Evaluate attention attribution shifts across both negation tokens to verify joint composition."
            ]
        else:
            badge = "BLIND"
            title = "Model did not respond correctly to negation"
            short_desc = "The classifier did not change its prediction as expected after a negation cue was introduced."
            test_name = "Negation"
            test_desc = "A controlled negation perturbation was applied to evaluate whether the model responds appropriately to a change in sentence meaning."
            why_failure = (
                "The perturbation introduced a negation cue that should have affected the classifier's decision according to the defined probe expectation. "
                "However, the predicted class remained unchanged. This indicates that the model may not be assigning sufficient decision-level importance to the negation cue."
            )
            recommended_step = (
                "Increase the diversity of negation examples in evaluation and training datasets, and re-test the model across multiple negation probes."
            )
            additional_steps = [
                "Include counterfactual pairs where adding or removing negation explicitly inverts the sentiment label.",
                "Verify whether the classifier consistently responds to negation rather than relying primarily on unigram sentiment keywords."
            ]
    elif "misweighted" in cat_lower:
        if "contrast" in pt_lower:
            badge = "MISWEIGHTED"
            title = "Model assigned unexpected importance to the contrast structure"
            short_desc = "The prediction differed from the expected behavior, and the attribution pattern suggests uneven importance across the contrasting clauses."
            test_name = "Contrast Clause"
            test_desc = "The test introduces a contrast structure to examine whether the model appropriately weighs information across the clauses."
            why_failure = (
                "The observed prediction differs from the expected behavior under the contrast perturbation, "
                "suggesting that the model may be placing inappropriate importance on one part of the sentence rather than balancing information across clauses."
            )
            recommended_step = (
                "Evaluate the model on multiple contrast constructions and verify whether the final clause receives appropriate influence."
            )
            additional_steps = [
                "Augment the training dataset with balanced contrastive sentences ('X, but Y').",
                "Expose the classifier to diverse discourse connectives ('however', 'although', 'yet') to balance clause attributions."
            ]
        else:
            badge = "MISWEIGHTED"
            title = "Attribution changed unexpectedly after synonym substitution"
            short_desc = "The model preserved the prediction, but the token attribution pattern changed across semantically similar inputs."
            test_name = "Synonym Substitution"
            test_desc = "A content word was replaced with a close semantic equivalent to evaluate whether prediction confidence and explanation polarities remain stable."
            why_failure = (
                "The model produced the same sentiment prediction for semantically similar inputs, which is behaviorally correct. "
                "However, the explanation assigned a different direction of contribution to an overlapping token. "
                "This attribution pattern suggests local sensitivity in the model's feature weighting across semantically similar inputs."
            )
            recommended_step = (
                "Evaluate attribution stability across a larger set of semantically equivalent substitutions. "
                "If similar polarity or ranking changes occur repeatedly, consider training or regularization strategies that encourage more stable representations for semantic equivalents."
            )
            additional_steps = [
                "Evaluate explanation stability across paraphrase equivalents and lexical substitutions.",
                "Verify whether nearby token embeddings preserve explanation consistency."
            ]
    elif "spurious" in cat_lower:
        badge = "SPURIOUS"
        title = "Model relied on entity or domain cues instead of sentiment signals"
        short_desc = "The prediction appears to depend on an irrelevant or unintended feature."
        test_name = "Domain & Entity Sensitivity"
        test_desc = "Evaluated whether non-sentiment domain nouns or neutral entities dominate the model's explanation."
        why_failure = (
            "Top feature attributions were concentrated on generic entity tokens rather than sentiment signals. "
            "This suggests the model may have learned non-causal correlations between domain nouns and sentiment labels during training."
        )
        recommended_step = (
            "Apply adversarial entity replacement (e.g. swapping domain nouns) during fine-tuning to break spurious correlations."
        )
        additional_steps = [
            "Regularize token feature attributions to penalize reliance on neutral domain tokens.",
            "Diversify training datasets across multiple domain contexts to decouple entities from labels."
        ]
    else:
        badge = category.upper()
        title = f"Model behavior deviated under {p_type}"
        short_desc = "The classifier's response diverged from expected behavior under the controlled perturbation test."
        test_name = f"Linguistic Perturbation ({p_type})"
        test_desc = "Evaluated target classifier robustness against systematic input variations."
        why_failure = "The observed prediction differed from the expected baseline behavior under this probe."
        recommended_step = "Inspect model sensitivity and fine-tune on balanced counterfactuals."
        additional_steps = ["Evaluate attribution alignment across syntactic variations."]

    # Expected behavior transition
    orig_upper = str(orig_label).upper()
    if orig_upper == "POSITIVE":
        opposite_label = "NEGATIVE"
    elif orig_upper == "NEGATIVE":
        opposite_label = "POSITIVE"
    else:
        opposite_label = f"NON-{orig_label}"
    if expected_flip is True:
        expected_transition = f"{orig_label} → {opposite_label}"
        expected_desc = "The perturbation was expected to change the model's prediction according to the defined probe behavior."
    elif expected_flip is False:
        expected_transition = f"{orig_label} → {orig_label}"
        expected_desc = "The perturbation was expected to preserve the model's original prediction category."
    else:
        expected_transition = "Expected behavior information unavailable"
        expected_desc = "No directional expectation specified for this probe."

    # Actual behavior transition
    actual_transition = f"{orig_label} → {pert_label}"
    if is_flipped is False:
        actual_desc = f"The model retained the original {orig_label} prediction."
    elif is_flipped is True:
        actual_desc = f"The model's prediction shifted to {pert_label}."
    else:
        actual_desc = f"The model predicted {pert_label}."

    improvements = [recommended_step] + additional_steps

    return {
        "badge": badge,
        "title": title,
        "short_desc": short_desc,
        "test_name": test_name,
        "test_desc": test_desc,
        "why_failure": why_failure,
        "recommended_step": recommended_step,
        "additional_steps": additional_steps,
        "improvements": improvements,
        "expected_transition": expected_transition,
        "expected_desc": expected_desc,
        "actual_transition": actual_transition,
        "actual_desc": actual_desc,
        "expected_text": f"{expected_transition} ({expected_desc})",
        "actual_text": f"{actual_transition} ({actual_desc})",
    }

def render_html(html_str: str):
    """
    Renders HTML safely in Streamlit without Markdown interpreting indented lines as code blocks.
    """
    clean_html = "\n".join(line.strip() for line in html_str.strip().splitlines())
    st.markdown(clean_html, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="BlindSpot - Behavioral Auditing Workstation",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    pages_registry = {
        "Overview": render_overview,
        "Experiment": render_experiment_lab,
        "Experiment Lab": render_experiment_lab,
        "Models": render_model_lab,
        "Probes": render_probe_lab,
        "Probe Lab": render_probe_lab,
        "Live Run": render_live_run,
        "Run Details": render_run_history,
        "Events": render_console,
        "Console": render_console,
        "Comparison": render_comparison,
        "Explainability": render_explanation_lab,
        "Failure Analysis": render_failure_lab,
        "Reports": render_reports,
        "Run History": render_run_history,
        "System": render_system_monitor,
        "System Monitor": render_system_monitor,
        "Monitor": render_system_monitor,
        "Settings": render_system_monitor,
    }

    render_shell(pages_registry)


if __name__ == "__main__":
    main()
