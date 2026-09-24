"""
Explanation Lab: Feature Attributions, Token Impact, and Explainer Provenance.
Visualizes signed token attribution scores, side-by-side perturbation attribution shifts,
and provenance verification (Native vs Fallback).
"""
import os
import streamlit as st
import pandas as pd
from typing import Dict, Any, List

from blindspot.ui.components import render_provenance_badge, render_empty_state
from blindspot.storage.run_store import RunStore


def render_explanation_lab():
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                TOKEN-LEVEL EXPLAINABILITY & PROVENANCE
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Model-specific feature attributions (LIME / SHAP / LOO), token weight sensitivity shifts, and runtime provenance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    store = RunStore()
    available_runs = [
        r for r in store.list_runs(include_archived=False)
        if os.path.exists(os.path.join(store.get_run_dir(r.get("experiment_id", "")), "results.json"))
    ]

    results = st.session_state.get("active_results")
    if not results:
        runner = st.session_state.get("active_runner")
        if runner and runner.status == "completed" and getattr(runner, "_result", None):
            results = runner._result
            st.session_state["active_results"] = results

    if not results:
        if available_runs:
            st.info("💡 No active experiment in the current browser session. Select and load a completed experiment run below to explore feature attributions:")
            col1, col2 = st.columns([3, 1])
            with col1:
                run_opts = [r["experiment_id"] for r in available_runs]
                selected_run = st.selectbox(
                    "Select Completed Experiment:",
                    options=run_opts,
                    format_func=lambda x: f"{store.get_run_title(x)} ({x})",
                    key="xai_load_run_sel",
                )
            with col2:
                st.write("")
                st.write("")
                if st.button("LOAD RUN", key="xai_btn_load_run", use_container_width=True):
                    run_data = store.load_run(selected_run)
                    if "results" in run_data:
                        st.session_state["active_results"] = run_data["results"]
                        st.session_state["active_experiment_id"] = selected_run
                        st.session_state["active_experiment_title"] = store.get_run_title(selected_run)
                        st.rerun()

            st.markdown("<hr style='border:1px solid #1e293b; margin:20px 0;'>", unsafe_allow_html=True)

        clicked = render_empty_state(
            title="NO EXPLAINABILITY RECORDS LOADED",
            message="No active audit experiment results found in session. Execute an audit with explainability enabled in Experiment Lab or load a completed run.",
            action_label="GO TO EXPERIMENT LAB",
            action_key="xai_empty_to_exp",
        )
        if clicked:
            st.session_state["current_page"] = "Experiment"
            st.rerun()
        return

    # Run switcher header if multiple runs exist
    if available_runs and len(available_runs) > 1:
        current_exp_id = results.get("experiment_id", "")
        with st.expander("🔄 Switch Loaded Experiment Run", expanded=False):
            c_sel1, c_sel2 = st.columns([3, 1])
            with c_sel1:
                run_opts = [r["experiment_id"] for r in available_runs]
                idx = run_opts.index(current_exp_id) if current_exp_id in run_opts else 0
                switch_exp = st.selectbox(
                    "Switch Experiment:",
                    options=run_opts,
                    index=idx,
                    format_func=lambda x: f"{store.get_run_title(x)} ({x})",
                    key="xai_switch_exp",
                )
            with c_sel2:
                st.write("")
                st.write("")
                if st.button("SWITCH RUN", key="xai_btn_switch", use_container_width=True):
                    if switch_exp != current_exp_id:
                        run_data = store.load_run(switch_exp)
                        if "results" in run_data:
                            st.session_state["active_results"] = run_data["results"]
                            st.session_state["active_experiment_id"] = switch_exp
                            st.session_state["active_experiment_title"] = store.get_run_title(switch_exp)
                            st.rerun()

    models_data = results.get("models", {})
    model_ids = list(models_data.keys())

    col_sel1, col_sel2 = st.columns([2, 4])
    with col_sel1:
        selected_model = st.selectbox("Target Model Architecture:", options=model_ids, key="xai_sel_model")

    m_info = models_data.get(selected_model, {})
    explanations = m_info.get("explanations", [])

    if not explanations:
        st.warning(f"No explanation records available for '{selected_model}'. Ensure explainability was enabled during experiment execution.")
        return

    probe_labels = [
        f"Probe #{i + 1}: [{e.get('perturbation_type', 'UNK').upper()}] - {e.get('perturbed_text', '')[:40]}..."
        for i, e in enumerate(explanations)
    ]
    with col_sel2:
        selected_idx = st.selectbox(
            "Select Probe Evaluation Stimulus:",
            options=range(len(probe_labels)),
            format_func=lambda i: probe_labels[i],
            key="xai_sel_probe",
        )

    record = explanations[selected_idx]
    ptype = record.get("perturbation_type", "Unknown")
    seed_t = record.get("seed_text", "")
    pert_t = record.get("perturbed_text", "")

    st.markdown(
        f"""
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 16px; margin:14px 0;">
            <div style="font-family:monospace; font-size:0.8rem; color:#38bdf8; font-weight:bold; margin-bottom:6px;">
                EVALUATION CONTEXT: {ptype.upper()}
            </div>
            <div style="font-family:monospace; font-size:0.8rem; color:#94a3b8; margin:3px 0;">
                ORIGINAL: <span style="color:#f1f5f9;">"{seed_t}"</span>
            </div>
            <div style="font-family:monospace; font-size:0.8rem; color:#38bdf8; margin:3px 0;">
                PERTURBED: <span style="color:#ffffff; font-weight:bold;">"{pert_t}"</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Attribution Alignment Scores
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        jaccard = record.get("jaccard_similarity", 0.0)
        st.metric(
            label="Attribution Jaccard Similarity",
            value=f"{jaccard:.3f}",
            help="Overlap of top salient feature tokens between original and perturbed text.",
        )
    with col_a2:
        cosine = record.get("cosine_alignment", 0.0)
        st.metric(
            label="Attribution Cosine Alignment",
            value=f"{cosine:.3f}",
            help="Directional alignment of attribution vectors in feature space.",
        )

    # Side-by-Side Original vs Perturbed Attributions
    col_orig, col_pert = st.columns(2)

    with col_orig:
        st.markdown("#### ORIGINAL ATTRIBUTION")
        orig_data = record.get("orig_explanation", {})
        render_provenance_badge(
            explainer_used=orig_data.get("explainer_used", "unknown"),
            fallback_used=orig_data.get("fallback_used", False),
            runtime_ms=orig_data.get("runtime_ms", 0.0),
        )

        weights_orig = orig_data.get("token_weights", {})
        if not weights_orig:
            st.caption("No token weights extracted.")
        else:
            sorted_orig = sorted(weights_orig.items(), key=lambda x: abs(x[1]), reverse=True)
            for token, score in sorted_orig[:10]:
                bar_color = "#10b981" if score >= 0 else "#ef4444"
                pct = min(100.0, abs(score) * 100.0)
                st.markdown(
                    f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; font-family:monospace; font-size:0.8rem; margin:3px 0;">
                        <span style="color:#f1f5f9; width:120px; overflow:hidden; text-overflow:ellipsis;">{token}</span>
                        <div style="flex-grow:1; margin:0 8px; background:#1e293b; border-radius:3px; height:8px;">
                            <div style="width:{pct:.1f}%; background:{bar_color}; height:8px; border-radius:3px;"></div>
                        </div>
                        <span style="color:{bar_color}; font-weight:bold; width:60px; text-align:right;">{score:+.3f}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with col_pert:
        st.markdown("#### PERTURBED ATTRIBUTION")
        pert_data = record.get("pert_explanation", {})
        render_provenance_badge(
            explainer_used=pert_data.get("explainer_used", "unknown"),
            fallback_used=pert_data.get("fallback_used", False),
            runtime_ms=pert_data.get("runtime_ms", 0.0),
        )

        weights_pert = pert_data.get("token_weights", {})
        if not weights_pert:
            st.caption("No token weights extracted.")
        else:
            sorted_pert = sorted(weights_pert.items(), key=lambda x: abs(x[1]), reverse=True)
            for token, score in sorted_pert[:10]:
                bar_color = "#10b981" if score >= 0 else "#ef4444"
                pct = min(100.0, abs(score) * 100.0)
                st.markdown(
                    f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; font-family:monospace; font-size:0.8rem; margin:3px 0;">
                        <span style="color:#f1f5f9; width:120px; overflow:hidden; text-overflow:ellipsis;">{token}</span>
                        <div style="flex-grow:1; margin:0 8px; background:#1e293b; border-radius:3px; height:8px;">
                            <div style="width:{pct:.1f}%; background:{bar_color}; height:8px; border-radius:3px;"></div>
                        </div>
                        <span style="color:{bar_color}; font-weight:bold; width:60px; text-align:right;">{score:+.3f}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Attribution Diagnostic Visualizations
    exp_id = results.get("experiment_id", "")
    fig_dir = os.path.join("runs", exp_id, "figures") if exp_id else ""
    if fig_dir and os.path.exists(fig_dir):
        xai_figs = [
            ("fig05_confidence_delta_by_probe.png", "Figure 5: Confidence Delta by Probe Category"),
            ("fig06_confidence_delta_distribution.png", "Figure 6: Overall Confidence Shift Density"),
            ("attribution_comparison.png", "Token Attribution Shift"),
            ("probe_alignment_summary.png", "Explanation Alignment Across Probes"),
        ]
        available_xai = [f for f, t in xai_figs if os.path.exists(os.path.join(fig_dir, f))]
        if available_xai:
            st.markdown("---")
            with st.expander("📈 Diagnostic Graphs: Attribution Shifts & Confidence Dynamics", expanded=False):
                g_cols = st.columns(2)
                for idx, f_name in enumerate(available_xai):
                    f_title = next(t for f, t in xai_figs if f == f_name)
                    with g_cols[idx % 2]:
                        st.caption(f"**{f_title}**")
                        st.image(os.path.join(fig_dir, f_name), use_container_width=True)

