"""
Reports View: Interactive Diagnostic Visualizations, Graphs, and Markdown Audit Reports.
Features publication-grade figure gallery, single-figure inspector with mathematical interpretations,
raw source data exporter, and markdown report viewer with embedded figures.
"""
import streamlit as st
import os
import json
from typing import Dict, Any, List

from blindspot.storage.run_store import RunStore
from blindspot.ui.components import render_empty_state, render_markdown_with_images


THESIS_FIGURE_METADATA = {
    "fig01_prediction_distribution.png": {
        "title": "Figure 1: Model Prediction Distribution",
        "category": "Behavioral Responses",
        "description": "Normalized distribution of predicted sentiment classes across all evaluated perturbation probes for each model architecture.",
        "interpretation": "Reveals whether models exhibit systematic classification skew under semantic perturbations.",
    },
    "fig02_flip_rates.png": {
        "title": "Figure 2: Observed vs Expected Flip Rates",
        "category": "Behavioral Responses",
        "description": "Compares empirical prediction flip percentage against the theoretical expected flip contract.",
        "interpretation": "High divergence indicates model sensitivity to invariant edits or blindness to polarity reversals.",
    },
    "fig03_expected_vs_observed.png": {
        "title": "Figure 3: Expected vs Observed Semantic Behavioral Rate",
        "category": "Behavioral Responses",
        "description": "Quantifies the proportion of probes where observed behavioral transitions matched the expected semantic effect.",
        "interpretation": "Direct measure of model behavioral compliance against linguistic invariants.",
    },
    "fig04_taxonomy_distribution.png": {
        "title": "Figure 4: 4-Way Behavioral Failure Taxonomy Distribution",
        "category": "Taxonomy & Failures",
        "description": "Proportional distribution of diagnosed behavioral failures: BLIND, SPURIOUS, MISWEIGHTED, and COMPLIANT (None).",
        "interpretation": "Primary thesis visualization diagnosing the structural nature of model brittleness.",
    },
    "fig05_confidence_delta_by_probe.png": {
        "title": "Figure 5: Signed Confidence Shift by Linguistic Category",
        "category": "Confidence Dynamics",
        "description": "Box/bar visualization of signed confidence changes in percentage points across probe categories.",
        "interpretation": "Tracks whether downtoners correctly reduce confidence and intensifiers strengthen it.",
    },
    "fig06_confidence_delta_distribution.png": {
        "title": "Figure 6: Overall Confidence Shift Density",
        "category": "Confidence Dynamics",
        "description": "Density distribution of signed confidence deltas across all models and probe evaluations.",
        "interpretation": "Highlights whether model predictions experience subtle confidence erosion even without discrete label flips.",
    },
    "fig07_probe_level_comparison.png": {
        "title": "Figure 7: Probe-Level Response Across Models",
        "category": "Probe Analysis",
        "description": "Side-by-side bar chart of perturbed prediction confidence for individual diagnostic probes across target architectures.",
        "interpretation": "Identifies which specific linguistic structures trigger cross-architecture consensus vs disagreement.",
    },
    "fig08_model_probe_heatmap.png": {
        "title": "Figure 8: Model Probe Flip Matrix",
        "category": "Cross-Model Concordance",
        "description": "Interactive matrix displaying prediction stability (FLIP vs SAME) for every probe across all models.",
        "interpretation": "Instantly visualizes shared vs architecture-specific failure modes.",
    },
    "fig09_transition_matrix.png": {
        "title": "Figure 9: Label Transition Matrix",
        "category": "Behavioral Responses",
        "description": "Heatmap depicting transition dynamics from original predicted classes to perturbed predicted classes.",
        "interpretation": "Highlights directional transition biases (e.g. Negative to Neutral vs Negative to Positive).",
    },
    "fig10_probe_consistency.png": {
        "title": "Figure 10: Behavioral Consistency by Category",
        "category": "Probe Analysis",
        "description": "Behavioral consistency score (%) achieved by each model broken down by perturbation category.",
        "interpretation": "Pinpoints linguistic categories where specific models are robust or brittle.",
    },
    "fig11_model_agreement.png": {
        "title": "Figure 11: Cross-Model Pairwise Agreement Matrix",
        "category": "Cross-Model Concordance",
        "description": "Heatmap displaying pairwise prediction agreement percentages between all evaluated models.",
        "interpretation": "Evaluates architectural diversity and consensus behavior across distinct model families.",
    },
    "fig12_change_vs_preserve.png": {
        "title": "Figure 12: Change vs Preserve Sensitivity Profile",
        "category": "Behavioral Responses",
        "description": "Scatter comparison of flip rate on meaning-altering probes vs preserve rate on meaning-preserving probes.",
        "interpretation": "The ideal robust classifier sits in the top-right quadrant (100% change, 100% preserve).",
    },
    "fig13_per_model_scorecard.png": {
        "title": "Figure 13: Comprehensive Robustness Scorecard",
        "category": "Scorecards & Profiling",
        "description": "Multi-metric performance summary per model incorporating consistency, preserve rate, and ECE calibration.",
        "interpretation": "Holistic executive scorecard for model auditing and deployment readiness.",
    },
    "fig14_runtime_profile.png": {
        "title": "Figure 14: Execution Latency & Profiling Breakdown",
        "category": "Scorecards & Profiling",
        "description": "Runtime latency profiling separating inference, explainability (LIME/SHAP), and analysis overhead.",
        "interpretation": "Documents computational efficiency and batching performance.",
    },
    "fig15_probe_category_comparison.png": {
        "title": "Figure 15: Cross-Category Resilience Comparison",
        "category": "Probe Analysis",
        "description": "Comparative bar chart summarizing failure frequencies across linguistic perturbation families.",
        "interpretation": "Guides targeted dataset augmentation and adversarial regularization.",
    },
}


def render_reports():
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                DIAGNOSTIC VISUALIZATIONS & ARTIFACTS
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Publication-grade thesis figures, behavioral failure distributions, and comprehensive Markdown audit documents.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    store = RunStore()
    available_runs = store.list_runs(include_archived=False)

    # Resolve active experiment ID
    active_results = st.session_state.get("active_results")
    default_exp_id = active_results.get("experiment_id", "") if active_results else ""

    if not default_exp_id and available_runs:
        default_exp_id = available_runs[0].get("experiment_id", "")

    if not default_exp_id:
        render_empty_state(
            title="NO EXPERIMENT DATA FOUND",
            message="No active or historical audit runs are available. Launch an audit in Experiment Lab to generate diagnostic figures and reports.",
            action_label="GO TO EXPERIMENT LAB",
            action_key="rep_empty_to_exp",
        )
        return

    # Run selector in top header
    run_options = [r.get("experiment_id", "") for r in available_runs if r.get("experiment_id")]
    if default_exp_id not in run_options:
        run_options.insert(0, default_exp_id)

    col_exp1, col_exp2 = st.columns([3, 1])
    with col_exp1:
        sel_idx = run_options.index(default_exp_id) if default_exp_id in run_options else 0
        selected_exp_id = st.selectbox(
            "Selected Experiment Artifacts:",
            options=run_options,
            index=sel_idx,
            format_func=lambda x: f"{store.get_run_title(x)} ({x})",
            key="rep_sel_exp_id",
        )

    exp_dir = store.get_run_dir(selected_exp_id)
    figures_dir = os.path.join(exp_dir, "figures")
    reports_dir = os.path.join(exp_dir, "reports")

    sel_title = store.get_run_title(selected_exp_id)
    with col_exp2:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:4px; padding:6px 12px; margin-top:24px; font-family:monospace; font-size:0.75rem; color:#94a3b8; text-align:center;">
                <div style="color:#64748b; font-size:0.68rem;">EXPERIMENT:</div>
                <div style="color:#38bdf8; font-weight:bold; font-size:0.82rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="{sel_title}">{sel_title}</div>
                <div style="color:#64748b; font-size:0.65rem;">{selected_exp_id}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Main Tabs
    tab_graphs, tab_classic, tab_reports, tab_source = st.tabs([
        "📈 Publication Thesis Visualizations (15 Figures)",
        "🔬 Classic Diagnostic Charts",
        "📑 Markdown Audit Reports",
        "📊 Raw Telemetry Data (source_data.json)",
    ])

    # -------------------------------------------------------------
    # TAB 1: 15 PUBLICATION THESIS VISUALIZATIONS
    # -------------------------------------------------------------
    with tab_graphs:
        if not os.path.exists(figures_dir):
            st.info(f"No figures directory found at `{figures_dir}` for this run.")
        else:
            all_fig_files = [f for f in sorted(os.listdir(figures_dir)) if f.startswith("fig") and f.endswith(".png")]
            if not all_fig_files:
                st.info("No publication thesis figures found for this experiment run.")
            else:
                col_mode1, col_mode2 = st.columns([3, 1])
                with col_mode1:
                    view_mode = st.radio(
                        "Display Mode:",
                        options=["Interactive Inspector (Detailed)", "Full Gallery (Multi-Column)"],
                        horizontal=True,
                        key="fig_view_mode",
                    )

                if "Interactive" in view_mode:
                    fig_select_options = [
                        f"{f} — {THESIS_FIGURE_METADATA.get(f, {}).get('title', f)}"
                        for f in all_fig_files
                    ]
                    sel_fig_label = st.selectbox("Select Figure to Inspect:", options=fig_select_options, key="sel_single_fig")
                    sel_fig_file = sel_fig_label.split(" — ")[0]
                    fig_path = os.path.join(figures_dir, sel_fig_file)

                    meta = THESIS_FIGURE_METADATA.get(sel_fig_file, {})
                    title = meta.get("title", sel_fig_file)
                    desc = meta.get("description", "")
                    interp = meta.get("interpretation", "")
                    cat = meta.get("category", "General")

                    st.markdown(
                        f"""
                        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 18px; margin:14px 0;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <span style="font-size:1.05rem; font-weight:700; color:#f1f5f9;">{title}</span>
                                <span style="background:#0284c7; color:#f0f9ff; padding:2px 8px; border-radius:3px; font-size:0.75rem; font-family:monospace;">{cat.upper()}</span>
                            </div>
                            <div style="color:#cbd5e1; font-size:0.85rem; margin-bottom:4px;">{desc}</div>
                            <div style="color:#38bdf8; font-size:0.8rem; font-style:italic;">💡 Interpretation: {interp}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.image(fig_path, use_container_width=True)

                    with open(fig_path, "rb") as fp:
                        st.download_button(
                            label=f"⬇️ Download {sel_fig_file} (300 DPI)",
                            data=fp.read(),
                            file_name=sel_fig_file,
                            mime="image/png",
                            key=f"dl_btn_{sel_fig_file}",
                        )

                else:
                    # Gallery View (2 columns)
                    cols = st.columns(2)
                    for i, fig_file in enumerate(all_fig_files):
                        fig_path = os.path.join(figures_dir, fig_file)
                        meta = THESIS_FIGURE_METADATA.get(fig_file, {})
                        title = meta.get("title", fig_file)
                        desc = meta.get("description", "")

                        with cols[i % 2]:
                            with st.container():
                                st.markdown(
                                    f"""
                                    <div style="background:#0f172a; border:1px solid #1e293b; border-radius:6px; padding:8px 12px; margin-top:10px;">
                                        <div style="font-size:0.9rem; font-weight:bold; color:#f1f5f9;">{title}</div>
                                        <div style="font-size:0.75rem; color:#94a3b8; margin-top:2px;">{desc}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                st.image(fig_path, use_container_width=True)
                                with open(fig_path, "rb") as fp:
                                    st.download_button(
                                        label=f"Download {fig_file}",
                                        data=fp.read(),
                                        file_name=fig_file,
                                        mime="image/png",
                                        key=f"dl_gal_{fig_file}",
                                    )

    # -------------------------------------------------------------
    # TAB 2: CLASSIC DIAGNOSTIC CHARTS
    # -------------------------------------------------------------
    with tab_classic:
        st.markdown(
            """
            <div style="color:#94a3b8; font-size:0.85rem; margin-bottom:12px;">
                Original core diagnostic visualizations specified in <code>DIAGNOSTIC_GRAPHS_GUIDE.md</code> covering taxonomy distributions, behavioral metrics, attribution shifts, and probe alignments.
            </div>
            """,
            unsafe_allow_html=True,
        )

        classic_figs = [
            ("taxonomy_distribution.png", "Behavioral Failure Taxonomy Donut", "Categorizes failures into Blind, Spurious, and Misweighted modes. Shows 100% Robust green ring on zero failures."),
            ("behavioral_metrics.png", "Behavioral Testing Diagnostic Metrics", "Dual horizontal bar chart comparing aggregate Prediction Flip Rate (%) and Expected Calibration Error (ECE x100)."),
            ("attribution_comparison.png", "Token Attribution Shift", "Original vs Perturbed token-level feature importance attribution weights (LIME / SHAP)."),
            ("probe_alignment_summary.png", "Explanation Alignment Across Probes", "Jaccard top-k similarity and Cosine attribution alignment scores across perturbation probes."),
        ]

        c_cols = st.columns(2)
        found_any = False
        for idx, (cf_name, cf_title, cf_desc) in enumerate(classic_figs):
            # Check in figures_dir or exp_dir
            cf_path = os.path.join(figures_dir, cf_name)
            if not os.path.exists(cf_path):
                cf_path = os.path.join(exp_dir, cf_name)
            if not os.path.exists(cf_path):
                cf_path = os.path.join("audit_reports", "figures", cf_name)

            if os.path.exists(cf_path):
                found_any = True
                with c_cols[idx % 2]:
                    st.markdown(
                        f"""
                        <div style="background:#0f172a; border:1px solid #1e293b; border-radius:6px; padding:10px 14px; margin-top:10px;">
                            <div style="font-size:0.95rem; font-weight:bold; color:#38bdf8;">{cf_title}</div>
                            <div style="font-size:0.75rem; color:#94a3b8; margin-top:2px;">{cf_desc}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.image(cf_path, use_container_width=True)
                    with open(cf_path, "rb") as fp:
                        st.download_button(
                            label=f"⬇️ Download {cf_name}",
                            data=fp.read(),
                            file_name=cf_name,
                            mime="image/png",
                            key=f"dl_classic_{cf_name}",
                        )

        if not found_any:
            st.info("Classic diagnostic charts have not been rendered for this run. Launch a full audit to compile them.")

    # -------------------------------------------------------------
    # TAB 3: MARKDOWN AUDIT REPORTS
    # -------------------------------------------------------------
    with tab_reports:
        reports_found = {}
        if os.path.exists(reports_dir):
            for fname in os.listdir(reports_dir):
                if fname.endswith(".md"):
                    with open(os.path.join(reports_dir, fname), "r", encoding="utf-8") as f:
                        reports_found[fname] = f.read()

        # Also check model directory report.md files
        models_dir = os.path.join(exp_dir, "models")
        if os.path.exists(models_dir):
            for slug in os.listdir(models_dir):
                m_report_path = os.path.join(models_dir, slug, "report.md")
                if os.path.exists(m_report_path):
                    with open(m_report_path, "r", encoding="utf-8") as f:
                        reports_found[f"model_{slug}.md"] = f.read()

        if not reports_found:
            st.info("No saved report files found on disk for this experiment.")
        else:
            col_rep_sel, col_rep_dl = st.columns([3, 1])
            with col_rep_sel:
                selected_report = st.selectbox("Select Report Document:", options=list(reports_found.keys()), key="sel_report_doc")
            content = reports_found[selected_report]

            with col_rep_dl:
                st.download_button(
                    label=f"⬇️ Download {selected_report}",
                    data=content,
                    file_name=selected_report,
                    mime="text/markdown",
                    key="dl_report_btn",
                )

            st.markdown("---")
            render_markdown_with_images(content, base_dir=exp_dir)

    # -------------------------------------------------------------
    # TAB 4: RAW TELEMETRY DATA (source_data.json)
    # -------------------------------------------------------------
    with tab_source:
        source_data_path = os.path.join(figures_dir, "source_data.json")
        if not os.path.exists(source_data_path):
            st.info(f"No source_data.json found at `{source_data_path}`.")
        else:
            with open(source_data_path, "r", encoding="utf-8") as f:
                source_json = json.load(f)

            st.markdown(
                """
                <div style="color:#94a3b8; font-size:0.85rem; margin-bottom:10px;">
                    Raw numerical coordinates and metrics backing all 15 publication figures. Exportable for external plotting tools (Origin, Prism, LaTeX TikZ).
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.download_button(
                label="⬇️ Download source_data.json",
                data=json.dumps(source_json, indent=2),
                file_name=f"{selected_exp_id}_source_data.json",
                mime="application/json",
                key="dl_source_json_btn",
            )

            st.json(source_json)
