"""
Model Comparison: Descriptive Cross-Model Matrix & Behavioral Analytics.
Provides high-density Model x Probe matrix with agreement flags, confidence deltas,
pairwise agreement tables, and behavioral fingerprints without subjective rankings.
"""
import os
import streamlit as st
import pandas as pd
from typing import Dict, Any, List

from blindspot.ui.components import render_empty_state
from blindspot.storage.run_store import RunStore


def render_comparison():
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                CROSS-MODEL BEHAVIORAL COMPARISON
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Descriptive evaluation of identical probe responses, prediction agreement, and behavioral fingerprints across target architectures.
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
            st.info("💡 No active experiment in the current browser session. Select and load a completed experiment run below to explore cross-model comparisons:")
            col1, col2 = st.columns([3, 1])
            with col1:
                run_opts = [r["experiment_id"] for r in available_runs]
                selected_run = st.selectbox(
                    "Select Completed Experiment:",
                    options=run_opts,
                    format_func=lambda x: f"{store.get_run_title(x)} ({x})",
                    key="comp_load_run_sel",
                )
            with col2:
                st.write("")
                st.write("")
                if st.button("LOAD RUN", key="comp_btn_load_run", use_container_width=True):
                    run_data = store.load_run(selected_run)
                    if "results" in run_data:
                        st.session_state["active_results"] = run_data["results"]
                        st.session_state["active_experiment_id"] = selected_run
                        st.session_state["active_experiment_title"] = store.get_run_title(selected_run)
                        st.rerun()

            st.markdown("<hr style='border:1px solid #1e293b; margin:20px 0;'>", unsafe_allow_html=True)

        clicked = render_empty_state(
            title="NO COMPARISON DATA LOADED",
            message="No active audit experiment results found in the session. Launch an audit in the Experiment Lab or load a historical run.",
            action_label="GO TO EXPERIMENT LAB",
            action_key="comp_empty_to_exp",
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
                    key="comp_switch_exp",
                )
            with c_sel2:
                st.write("")
                st.write("")
                if st.button("SWITCH RUN", key="comp_btn_switch", use_container_width=True):
                    if switch_exp != current_exp_id:
                        run_data = store.load_run(switch_exp)
                        if "results" in run_data:
                            st.session_state["active_results"] = run_data["results"]
                            st.session_state["active_experiment_id"] = switch_exp
                            st.session_state["active_experiment_title"] = store.get_run_title(switch_exp)
                            st.rerun()

    cross = results.get("cross_model_comparison", {})
    models_data = results.get("models", {})
    model_baselines = results.get("model_baselines", {})
    model_ids = list(models_data.keys())

    if len(model_ids) < 2:
        st.warning("⚠️ Cross-model comparison requires at least two evaluated models. The active experiment evaluated only one model.")
        return

    # ==========================================
    # PRIMARY RESEARCH THESIS: BASELINE vs PERTURBATION
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:14px 18px; margin-bottom:18px;">
            <div style="font-size:0.95rem; font-weight:700; color:#38bdf8; font-family:monospace; margin-bottom:6px;">
                ORIGINAL BASELINE STIMULI
            </div>
            <div style="color:#94a3b8; font-size:0.8rem; margin-bottom:10px;">
                Every probe perturbation is evaluated strictly relative to its original seed sentence baseline.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Render baseline cards per seed
    seeds = results.get("shared_probes", {}).get("seed_texts", [])

    for s_idx, seed in enumerate(seeds):
        with st.expander(f"Baseline #{s_idx + 1}: '{seed}'", expanded=True):
            b_cols = st.columns(len(model_ids))
            for m_idx, m_id in enumerate(model_ids):
                m_short = m_id.split("/")[-1]
                m_base = model_baselines.get(m_id, {}).get(seed, {})
                pred_data = m_base.get("prediction", {})
                lbl = pred_data.get("label", "N/A")
                conf = pred_data.get("confidence", 0.0) * 100.0

                with b_cols[m_idx]:
                    st.markdown(
                        f"""
                        <div style="background:#0f172a; border:1px solid #1e293b; border-radius:4px; padding:8px 10px; font-family:monospace;">
                            <div style="color:#94a3b8; font-size:0.75rem; margin-bottom:2px;">{m_short}</div>
                            <div style="font-size:0.9rem; font-weight:bold; color:#38bdf8;">{lbl}</div>
                            <div style="color:#cbd5e1; font-size:0.75rem;">Confidence: {conf:.1f}%</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # Stratified Behavioral Robustness Table
    st.markdown(
        """
        <div style="margin:16px 0 6px 0; font-family:monospace; font-size:0.85rem; font-weight:bold; color:#cbd5e1;">
            STRATIFIED BEHAVIORAL METRICS SUMMARY
        </div>
        """,
        unsafe_allow_html=True,
    )
    metric_rows = []
    for m_id in model_ids:
        m_info = models_data.get(m_id, {}).get("behavioral_metrics") or {}
        obs_flip = (m_info.get("observed_flip_rate") if m_info.get("observed_flip_rate") is not None else m_info.get("flip_rate", 0.0)) * 100.0
        exp_flip = (m_info.get("expected_flip_rate") or 0.0) * 100.0
        preserve = (m_info.get("preserve_rate") or 0.0) * 100.0
        accuracy = (m_info.get("behavioral_consistency") if m_info.get("behavioral_consistency") is not None else m_info.get("satisfaction_rate", 1.0)) * 100.0
        ece = m_info.get("ece") or 0.0
        conf_shifts = m_info.get("confidence_shifts")
        mean_shift = conf_shifts.get("mean_delta_pts", 0.0) if isinstance(conf_shifts, dict) else 0.0

        evals = models_data.get(m_id, {}).get("evaluations", [])
        confs = [e.get("perturbed_confidence", 0.0) for e in evals if e.get("perturbed_confidence") is not None]
        mean_conf = (sum(confs) / len(confs) * 100.0) if confs else 0.0

        b_cnt = sum(1 for e in evals if e.get("failure_type") == "Blind")
        s_cnt = sum(1 for e in evals if e.get("failure_type") == "Spurious")
        m_cnt = sum(1 for e in evals if e.get("failure_type") == "Misweighted")
        u_cnt = sum(1 for e in evals if e.get("failure_type") == "Undetermined")

        metric_rows.append({
            "Target Architecture": m_id.split("/")[-1],
            "Accuracy": f"{accuracy:.1f}%",
            "ECE": f"{ece:.4f}",
            "Mean Confidence": f"{mean_conf:.1f}%",
            "Observed Flip Rate": f"{obs_flip:.1f}%",
            "Expected Flip Rate": f"{exp_flip:.1f}%",
            "Preserve Rate": f"{preserve:.1f}%",
            "Blind": b_cnt,
            "Spurious": s_cnt,
            "Misweighted": m_cnt,
            "Undetermined": u_cnt,
            "Mean Confidence Shift": f"{mean_shift:+.1f} pp",
        })

    if metric_rows:
        st.dataframe(pd.DataFrame(metric_rows), use_container_width=True, hide_index=True)

    tab_matrix, tab_eval, tab_fingerprint, tab_visuals = st.tabs([
        "MODEL × PROBE MATRIX",
        "PER-MODEL AUDIT (EXPECTED vs PREDICTED)",
        "BEHAVIORAL FINGERPRINTS",
        "📈 COMPARATIVE CHARTS",
    ])

    # ==========================================
    # Tab 1: Model x Probe Matrix
    # ==========================================
    with tab_matrix:
        matrix_data = cross.get("model_probe_matrix", [])
        if not matrix_data:
            st.caption("No matrix records available.")
        else:
            # Filter bar
            col_f1, col_f2, col_f3 = st.columns([2, 2, 2])
            with col_f1:
                all_ptypes = sorted(list({item["perturbation_type"] for item in matrix_data}))
                ptype_filter = st.selectbox("Filter by Category:", options=["ALL"] + all_ptypes, key="comp_flt_cat")

            with col_f2:
                exp_filter = st.selectbox(
                    "Filter by Expected Behavior:",
                    options=["ALL", "EXPECTED FLIP", "EXPECTED PRESERVE"],
                    key="comp_flt_exp",
                )

            with col_f3:
                search_kw = st.text_input("Search Seed/Perturbation:", placeholder="Search text...", key="comp_flt_search")

            rows = []
            for item in matrix_data:
                ptype = item["perturbation_type"]
                if ptype_filter != "ALL" and ptype != ptype_filter:
                    continue

                exp_flip = item.get("expected_flip", False)
                if exp_filter == "EXPECTED FLIP" and not exp_flip:
                    continue
                if exp_filter == "EXPECTED PRESERVE" and exp_flip:
                    continue

                seed_t = item.get("seed_text", "")
                pert_t = item.get("perturbed_text", "")
                if search_kw.strip():
                    if search_kw.lower() not in seed_t.lower() and search_kw.lower() not in pert_t.lower():
                        continue

                m_outputs = item["models"]

                # Extract original baseline label across models
                orig_lbl = next(
                    (m_outputs[m].get("original_label") for m in model_ids if m in m_outputs and m_outputs[m].get("original_label")),
                    "POSITIVE",
                )
                if exp_flip:
                    target_lbl = "NEGATIVE" if orig_lbl == "POSITIVE" else "POSITIVE"
                    expected_desc = f"FLIP ➔ {target_lbl}"
                else:
                    expected_desc = f"PRESERVE ➔ {orig_lbl}"

                row = {
                    "Probe ID": item["probe_id"][:10],
                    "Category": ptype.upper(),
                    "Expected": expected_desc,
                }

                # Add compact model columns with predicted label and confidence
                confs = []
                for m in model_ids:
                    m_short = m.split("/")[-1][:14]
                    if m in m_outputs:
                        out = m_outputs[m]
                        lbl = out.get("perturbed_label", "UNK")
                        conf = out.get("perturbed_confidence", 0.0) * 100.0
                        confs.append(conf)
                        row[f"{m_short}"] = f"{lbl} ({conf:.1f}%)"
                    else:
                        row[f"{m_short}"] = "N/A"

                if len(confs) >= 2:
                    row["Conf Delta"] = f"{abs(confs[0] - confs[1]):.1f} pp"
                else:
                    row["Conf Delta"] = "--"

                row["Perturbed Stimulus"] = pert_t
                rows.append(row)

            st.caption(f"Displaying **{len(rows)}** of **{len(matrix_data)}** evaluated probe stimuli.")
            if rows:
                df_matrix = pd.DataFrame(rows)
                st.dataframe(df_matrix, use_container_width=True, hide_index=True)

    # ==========================================
    # Tab 2: Per-Model Audit (Expected vs Predicted)
    # ==========================================
    with tab_eval:
        st.subheader("Target Architecture: Expected vs Predicted Audit")
        st.caption("Drill-down into per-probe Expected behavior, Predicted labels, confidence distributions, and empirical Accuracy.")

        sel_m_col1, sel_m_col2 = st.columns([3, 1])
        with sel_m_col1:
            sel_model_id = st.selectbox(
                "Select Architecture:",
                options=model_ids,
                format_func=lambda x: x.split("/")[-1],
                key="comp_sel_eval_model",
            )

        m_eval_info = models_data.get(sel_model_id, {}).get("behavioral_metrics", {})
        m_evals = models_data.get(sel_model_id, {}).get("evaluations", [])

        m_acc = (m_eval_info.get("behavioral_consistency") if m_eval_info.get("behavioral_consistency") is not None else m_eval_info.get("satisfaction_rate", 1.0)) * 100.0
        m_ece = m_eval_info.get("ece", 0.0)
        m_confs = [e.get("perturbed_confidence", 0.0) for e in m_evals if e.get("perturbed_confidence") is not None]
        m_mean_conf = (sum(m_confs) / len(m_confs) * 100.0) if m_confs else 0.0
        m_sat = sum(1 for e in m_evals if e.get("expectation_satisfied"))

        # KPI Metrics Cards
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("Accuracy", f"{m_acc:.1f}%")
        with kpi2:
            st.metric("ECE (Calibration Error)", f"{m_ece:.4f}")
        with kpi3:
            st.metric("Mean Confidence", f"{m_mean_conf:.1f}%")
        with kpi4:
            st.metric("Compliance", f"{m_sat}/{len(m_evals)} Satisfied")

        eval_rows = []
        for e in m_evals:
            p_id = e.get("probe_id", "")[:10]
            cat = e.get("perturbation_type", "").upper()
            orig_lbl = e.get("original_label", "POSITIVE")
            pred_lbl = e.get("perturbed_label", "UNK")
            conf = e.get("perturbed_confidence", 0.0) * 100.0
            exp_flip = e.get("expected_flip", False)

            if exp_flip:
                opp_lbl = "NEGATIVE" if orig_lbl == "POSITIVE" else "POSITIVE"
                exp_desc = f"FLIP ➔ {opp_lbl}"
            else:
                exp_desc = f"PRESERVE ➔ {orig_lbl}"

            is_sat = e.get("expectation_satisfied", False)
            status_desc = "✓ ACCURATE" if is_sat else f"✗ {e.get('failure_type', 'FAIL').upper()}"

            eval_rows.append({
                "Probe ID": p_id,
                "Category": cat,
                "Baseline": orig_lbl,
                "Expected": exp_desc,
                "Predicted": pred_lbl,
                "Confidence": f"{conf:.1f}%",
                "Accuracy / Status": status_desc,
                "Confidence Shift": f"{e.get('confidence_delta_pts', 0.0):+.1f} pp",
                "Perturbed Stimulus": e.get("perturbed_text", ""),
            })

        if eval_rows:
            st.dataframe(pd.DataFrame(eval_rows), use_container_width=True, hide_index=True)
        else:
            st.caption("No evaluation records available for this model.")

    # ==========================================
    # Tab 3: Behavioral Fingerprints
    # ==========================================
    with tab_fingerprint:
        st.subheader("Descriptive Behavioral Profiles")
        st.caption("Quantitative operational characteristics across identical perturbation stimuli without normative rankings.")

        fps = cross.get("fingerprints", {})
        if fps:
            fp_rows = []
            for m_id, fp in fps.items():
                m_info = models_data.get(m_id, {}).get("behavioral_metrics") or {}
                m_evals = models_data.get(m_id, {}).get("evaluations", [])
                confs = [e.get("perturbed_confidence", 0.0) for e in m_evals if e.get("perturbed_confidence") is not None]
                mean_conf = (sum(confs) / len(confs) * 100.0) if confs else 0.0

                fp_rows.append({
                    "Model Architecture": m_id.split("/")[-1],
                    "Accuracy": f"{fp.get('satisfaction_rate', 0.0) * 100:.1f}%",
                    "ECE": f"{fp.get('ece', 0.0):.4f}",
                    "Mean Confidence": f"{mean_conf:.1f}%",
                    "Flip Rate": f"{fp.get('flip_rate', 0.0) * 100:.1f}%",
                    "Mean Shift": f"{fp.get('mean_confidence_shift_pts', 0.0):+.2f} pp",
                    "Total Probes": fp.get("total_probes", 0),
                })
            df_fp = pd.DataFrame(fp_rows)
            st.dataframe(df_fp, use_container_width=True, hide_index=True)
        else:
            st.caption("No behavioral fingerprints computed.")

    # ==========================================
    # Tab 4: Comparative Diagnostic Charts
    # ==========================================
    with tab_visuals:
        st.subheader("Cross-Model Diagnostic Visualizations")
        st.caption("Publication-grade comparative heatmaps, flip rates, and failure distributions.")

        exp_id = results.get("experiment_id", "")
        fig_dir = os.path.join("runs", exp_id, "figures") if exp_id else ""

        cross_figs = [
            ("fig08_model_probe_heatmap.png", "Figure 8: Model Probe Flip Matrix", "Heatmap of prediction flips (FLIP vs SAME) across all evaluated probes and models."),
            ("fig11_model_agreement.png", "Figure 11: Cross-Model Pairwise Agreement Matrix", "Pairwise percentage concordance heatmap across model architectures."),
            ("fig02_flip_rates.png", "Figure 2: Observed vs Expected Flip Rates", "Comparison of empirical flip rate against behavioral expectation."),
            ("fig04_taxonomy_distribution.png", "Figure 4: 4-Way Failure Taxonomy Distribution", "Proportional breakdown of Blind, Spurious, and Misweighted failures."),
        ]

        if fig_dir and os.path.exists(fig_dir):
            c_cols = st.columns(2)
            found_any = False
            for idx, (f_name, f_title, f_desc) in enumerate(cross_figs):
                f_path = os.path.join(fig_dir, f_name)
                if os.path.exists(f_path):
                    found_any = True
                    with c_cols[idx % 2]:
                        st.markdown(
                            f"""
                            <div style="background:#0f172a; border:1px solid #1e293b; border-radius:6px; padding:8px 12px; margin-top:10px;">
                                <div style="font-size:0.9rem; font-weight:bold; color:#f1f5f9;">{f_title}</div>
                                <div style="font-size:0.75rem; color:#94a3b8;">{f_desc}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.image(f_path, use_container_width=True)
            if not found_any:
                st.info("No comparative figure files found on disk for this experiment.")
        else:
            st.info("No figures directory found for this experiment run.")

