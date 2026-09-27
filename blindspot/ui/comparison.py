"""
Model Comparison: Descriptive Cross-Model Matrix & Behavioral Analytics.
Provides high-density Model x Probe matrix with cell-level deviation highlighting,
accessible status badges, directional transitions, model completeness tracking,
and interactive probe-level detail drawer without subjective rankings.
"""
import os
import textwrap
import streamlit as st
import pandas as pd
from typing import Dict, Any, List

from blindspot.ui.components import render_empty_state
from blindspot.storage.run_store import RunStore
from blindspot.models.registry import (
    get_model_display_name,
    get_model_short_name,
    CANONICAL_MODEL_NAMES,
)


def _html(content: str, unsafe_allow_html: bool = True):
    st.markdown(textwrap.dedent(content).strip(), unsafe_allow_html=unsafe_allow_html)


def render_comparison():
    _html(
        """
        <div style="margin-bottom:16px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                CROSS-MODEL BEHAVIORAL COMPARISON & DEVIATION AUDIT
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Descriptive evaluation of identical probe responses, cell-level deviation detection, and directional behavioral transitions across target architectures.
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
    
    # -------------------------------------------------------------
    # MODEL COMPLETENESS CONTRACT (Phases 4, 21, 22)
    # -------------------------------------------------------------
    config_models = results.get("config", {}).get("models") or results.get("metadata", {}).get("models", [])
    executed_models = list(models_data.keys())
    
    # Preserve full configured set in stable canonical order
    all_known_models = list(dict.fromkeys(config_models + executed_models))
    if not all_known_models:
        all_known_models = executed_models
        
    missing_models = [m for m in all_known_models if m not in executed_models]
    total_count = len(all_known_models)
    exec_count = len(executed_models)

    if missing_models:
        missing_names = ", ".join(get_model_display_name(m) for m in missing_models)
        _html(
            f"""
            <div class="model-completeness-banner model-completeness-warning">
                <div>
                    <span style="font-weight:700; color:#f59e0b;">⚠ PARTIAL MODEL SET:</span>
                    <span> <strong>{exec_count} / {total_count}</strong> configured models completed ({len(missing_models)} missing: <strong>{missing_names}</strong> [NOT RUN])</span>
                </div>
                <div style="color:#cbd5e1; font-size:0.75rem;">Missing architectures are explicitly retained in all table columns as <code>— NOT RUN</code></div>
            </div>
            """
        )
    else:
        _html(
            f"""
            <div class="model-completeness-banner">
                <div>
                    <span style="font-weight:700; color:#38bdf8;">✓ MODEL COMPLETENESS:</span>
                    <span> All <strong>{exec_count} / {total_count}</strong> configured architectures evaluated across identical stimuli</span>
                </div>
                <div style="color:#94a3b8; font-size:0.75rem;">
                    DistilBERT SST-2 &bull; ALBERT Base SST-2 &bull; BERT Base SST-2 &bull; Twitter-RoBERTa (Latest) &bull; Twitter-RoBERTa (Base)
                </div>
            </div>
            """
        )

    if len(all_known_models) < 2 and len(executed_models) < 2:
        st.warning("⚠️ Cross-model comparison requires at least two evaluated models. The active experiment evaluated only one model.")
        return

    # ==========================================
    # PRIMARY RESEARCH THESIS: BASELINE STIMULI
    # ==========================================
    _html(
        """
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 16px; margin-bottom:14px;">
            <div style="font-size:0.92rem; font-weight:700; color:#38bdf8; font-family:monospace; margin-bottom:4px;">
                ORIGINAL BASELINE STIMULI
            </div>
            <div style="color:#94a3b8; font-size:0.8rem;">
                Every perturbation is evaluated strictly relative to its original unperturbed sentence baseline.
            </div>
        </div>
        """
    )

    # Render baseline cards per seed with canonical names
    seeds = results.get("shared_probes", {}).get("seed_texts", [])
    for s_idx, seed in enumerate(seeds):
        with st.expander(f"Baseline #{s_idx + 1}: '{seed}'", expanded=True):
            b_cols = st.columns(len(all_known_models))
            for m_idx, m_id in enumerate(all_known_models):
                m_disp = get_model_display_name(m_id)
                m_task = CANONICAL_MODEL_NAMES.get(m_id, {}).get("task_badge", "Sentiment")
                
                with b_cols[m_idx]:
                    if m_id in models_data:
                        m_base = model_baselines.get(m_id, {}).get(seed, {})
                        pred_data = m_base.get("prediction", {})
                        lbl = pred_data.get("label", "N/A")
                        conf = pred_data.get("confidence", 0.0) * 100.0
                        _html(
                            f"""
                            <div style="background:#0f172a; border:1px solid #1e293b; border-radius:4px; padding:8px 10px; font-family:monospace; min-height:86px;">
                                <div style="color:#94a3b8; font-size:0.72rem; margin-bottom:2px; font-weight:bold;">{m_disp}</div>
                                <div style="font-size:0.95rem; font-weight:bold; color:#38bdf8;">{lbl}</div>
                                <div style="color:#cbd5e1; font-size:0.75rem;">Confidence: {conf:.1f}%</div>
                                <div style="color:#64748b; font-size:0.68rem; margin-top:2px;">{m_task}</div>
                            </div>
                            """
                        )
                    else:
                        _html(
                            f"""
                            <div style="background:#0b0f19; border:1px dashed #334155; border-radius:4px; padding:8px 10px; font-family:monospace; min-height:86px;">
                                <div style="color:#64748b; font-size:0.72rem; margin-bottom:2px;">{m_disp}</div>
                                <div style="font-size:0.9rem; font-weight:bold; color:#64748b;">— NOT RUN</div>
                                <div style="color:#475569; font-size:0.75rem;">No Execution</div>
                            </div>
                            """
                        )

    tab_matrix, tab_eval, tab_fingerprint, tab_failures, tab_visuals = st.tabs([
        "📊 MODEL × PROBE MATRIX",
        "🎯 PER-MODEL AUDIT (EXPECTED vs PREDICTED)",
        "🧬 BEHAVIORAL FINGERPRINTS",
        "🏷️ MODELS & FAILURES",
        "📈 COMPARATIVE CHARTS",
    ])

    # ==========================================
    # Tab 1: Primary Model x Probe Matrix
    # ==========================================
    with tab_matrix:
        matrix_data = cross.get("model_probe_matrix", [])
        if not matrix_data:
            st.caption("No matrix records available.")
        else:
            # View & Filter Bar (Phases 17 & 25)
            col_v1, col_v2, col_v3 = st.columns([3, 2, 2])
            with col_v1:
                view_mode = st.radio(
                    "View Filter:",
                    options=["ALL PROBES", "DEVIATIONS ONLY", "CONFIRMED FAILURES ONLY", "MATCHES ONLY"],
                    horizontal=True,
                    key="comp_view_mode",
                )
            with col_v2:
                all_ptypes = sorted(list({item["perturbation_type"] for item in matrix_data}))
                ptype_filter = st.selectbox("Category Filter:", options=["ALL"] + all_ptypes, key="comp_flt_cat_v2")
            with col_v3:
                search_kw = st.text_input("Search Stimulus:", placeholder="Filter keyword...", key="comp_flt_search_v2")

            # Legend Banner (Phases 9 & 10 - Accessible, non-color alone)
            _html(
                """
                <div style="display:flex; gap:12px; align-items:center; background:#111622; border:1px solid #1e2638; border-radius:4px; padding:6px 12px; margin:8px 0 14px 0; font-size:0.75rem; font-family:monospace; flex-wrap:wrap;">
                    <span style="color:#94a3b8; font-weight:bold;">LEGEND:</span>
                    <span class="status-pill pill-match">✓ MATCH</span> <span style="color:#64748b;">Agrees with Ground Truth</span>
                    <span class="status-pill pill-dev">⚠ DEVIATION</span> <span style="color:#64748b;">Contradicts Expectation</span>
                    <span class="status-pill pill-fail">✕ FAILURE</span> <span style="color:#64748b;">Taxonomy Diagnosed</span>
                    <span class="status-pill pill-undet">? UNDETERMINED</span> <span style="color:#64748b;">Insufficient Evidence</span>
                    <span class="status-pill pill-notrun">— NOT RUN</span> <span style="color:#64748b;">Not Executed</span>
                </div>
                """
            )

            # Process Matrix Rows with Cell-Level Deviation Flagging
            rendered_rows = []
            probe_map = {}

            for item in matrix_data:
                p_id = item["probe_id"]
                ptype = item["perturbation_type"]
                seed_t = item.get("seed_text", "")
                pert_t = item.get("perturbed_text", "")
                m_outputs = item.get("models", {})
                sem_ref = item.get("semantic_reference") or {}
                sem_pol = sem_ref.get("final_semantic_polarity", "")
                sem_rel = sem_ref.get("semantic_relation_to_baseline", "")
                exp_flip = item.get("expected_flip", False)

                probe_map[p_id] = item

                # Category filter
                if ptype_filter != "ALL" and ptype != ptype_filter:
                    continue

                # Search filter
                if search_kw.strip():
                    haystack = f"{p_id} {ptype} {seed_t} {pert_t}".lower()
                    if search_kw.lower() not in haystack:
                        continue

                # Expected Behavior description
                if sem_pol:
                    rel_tag = f" [{sem_rel}]" if sem_rel else ""
                    expected_desc = f"{sem_pol}{rel_tag}"
                    expected_token = "FLIP" if "REVERSE" in str(sem_rel).upper() else ("PRESERVE" if "PRESERVE" in str(sem_rel).upper() else "CHANGE")
                elif exp_flip:
                    orig_lbl = next(
                        (m_outputs[m].get("original_label") for m in all_known_models if m in m_outputs and m_outputs[m].get("original_label")),
                        "POSITIVE",
                    )
                    target_lbl = "NEGATIVE" if orig_lbl == "POSITIVE" else "POSITIVE"
                    expected_desc = f"FLIP ➔ {target_lbl}"
                    expected_token = "FLIP"
                else:
                    orig_lbl = next(
                        (m_outputs[m].get("original_label") for m in all_known_models if m in m_outputs and m_outputs[m].get("original_label")),
                        "POSITIVE",
                    )
                    expected_desc = f"PRESERVE ➔ {orig_lbl}"
                    expected_token = "PRESERVE"

                # Cell-Level Model Evaluations
                row_has_deviation = False
                row_has_failure = False
                row_all_match = True
                model_cells = {}

                for m_id in all_known_models:
                    if m_id not in m_outputs:
                        # Model not run
                        model_cells[m_id] = {
                            "status": "notrun",
                            "pill": "pill-notrun",
                            "badge": "— NOT RUN",
                            "label": "NOT RUN",
                            "conf": 0.0,
                            "conf_str": "—",
                            "transition": "—",
                        }
                        continue

                    out = m_outputs[m_id]
                    lbl = out.get("perturbed_label", "UNK")
                    conf = out.get("perturbed_confidence", 0.0) * 100.0
                    orig_lbl = out.get("original_label", "UNK")
                    is_sat = out.get("expectation_satisfied", True)
                    unexp = out.get("unexpected_behavior", False)
                    fail_type = out.get("failure_type")

                    # Directional Transition Badge
                    trans_text = f"{orig_lbl[:3]} ➔ {lbl[:3]}" if orig_lbl and lbl else "—"

                    # Classify cell-level deviation status
                    if fail_type and str(fail_type).lower() in ("blind", "spurious", "misweighted"):
                        status = "failure"
                        pill = "pill-fail"
                        badge = f"✕ {str(fail_type).upper()}"
                        row_has_failure = True
                        row_has_deviation = True
                        row_all_match = False
                    elif unexp or not is_sat:
                        status = "deviation"
                        pill = "pill-dev"
                        badge = "⚠ DEVIATION"
                        row_has_deviation = True
                        row_all_match = False
                    elif fail_type and str(fail_type).lower() == "undetermined":
                        status = "undetermined"
                        pill = "pill-undet"
                        badge = "? UNDETERMINED"
                        row_has_deviation = True
                        row_all_match = False
                    else:
                        status = "match"
                        pill = "pill-match"
                        badge = "✓ MATCH"

                    model_cells[m_id] = {
                        "status": status,
                        "pill": pill,
                        "badge": badge,
                        "label": lbl,
                        "conf": conf,
                        "conf_str": f"{conf:.1f}%",
                        "transition": trans_text,
                    }

                # View mode filter
                if view_mode == "DEVIATIONS ONLY" and not row_has_deviation:
                    continue
                if view_mode == "CONFIRMED FAILURES ONLY" and not row_has_failure:
                    continue
                if view_mode == "MATCHES ONLY" and not row_all_match:
                    continue

                rendered_rows.append({
                    "probe_id": p_id,
                    "category": ptype.upper(),
                    "expected_desc": expected_desc,
                    "expected_token": expected_token,
                    "model_cells": model_cells,
                    "perturbed_text": pert_t,
                })

            st.caption(f"Displaying **{len(rendered_rows)}** of **{len(matrix_data)}** evaluated probe stimuli under `{view_mode}`.")

            # RENDER CUSTOM RESEARCH HTML TABLE
            if rendered_rows:
                table_html = [
                    '<div class="bs-grid-container">',
                    '<table class="bs-table">',
                    '<thead><tr>',
                    '<th class="bs-col-sticky">Probe ID</th>',
                    '<th>Category</th>',
                    '<th>Expected (Ground Truth)</th>',
                ]

                # Model column headers with canonical names
                for m_id in all_known_models:
                    m_short = get_model_short_name(m_id)
                    table_html.append(f'<th>{m_short}</th>')

                table_html.append('<th>Perturbed Stimulus</th>')
                table_html.append('</tr></thead><tbody>')

                for r in rendered_rows:
                    table_html.append('<tr>')
                    # Sticky Probe ID
                    table_html.append(f'<td class="bs-col-sticky" style="font-family:monospace; font-weight:700; color:#38bdf8;">{r["probe_id"][:10]}</td>')
                    # Category
                    table_html.append(f'<td style="font-family:monospace; font-size:0.75rem; color:#cbd5e1;">{r["category"]}</td>')
                    # Expected Ground Truth
                    table_html.append(
                        f'<td><div style="font-family:monospace; font-size:0.78rem; font-weight:bold; color:#e2e8f0;">{r["expected_desc"]}</div>'
                        f'<div class="trans-badge" style="margin-top:2px;">EXP: {r["expected_token"]}</div></td>'
                    )

                    # Model Cells with Cell-Level Deviation Badges
                    for m_id in all_known_models:
                        c = r["model_cells"][m_id]
                        cell_content = (
                            f'<td><div class="cell-badge cell-{c["status"]}">'
                            f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                            f'<span style="font-weight:700;">{c["label"]}</span>'
                            f'<span style="font-size:0.7rem; color:#cbd5e1;">{c["conf_str"]}</span>'
                            f'</div>'
                            f'<div style="font-size:0.69rem; color:#94a3b8; margin:2px 0;">{c["transition"]}</div>'
                            f'<span class="status-pill {c["pill"]}">{c["badge"]}</span>'
                            f'</div></td>'
                        )
                        table_html.append(cell_content)

                    # Perturbed text preview
                    table_html.append(f'<td style="color:#94a3b8; font-size:0.78rem; max-width:280px; word-break:break-word;">{r["perturbed_text"]}</td>')
                    table_html.append('</tr>')

                table_html.append('</tbody></table></div>')
                clean_table_html = "".join(line.strip() for line in table_html)
                st.markdown(clean_table_html, unsafe_allow_html=True)
            else:
                st.info(f"No probes match the active filter criteria (`{view_mode}`).")

            # ==========================================
            # INTERACTIVE PROBE DETAIL DRAWER (Phase 14)
            # ==========================================
            st.markdown("---")
            _html(
                """
                <div style="font-size:1.05rem; font-weight:700; color:#f1f5f9; margin-bottom:4px;">
                    🔬 PROBE-LEVEL DETAIL DRAWER & EVIDENCE INSPECTOR
                </div>
                <div style="color:#94a3b8; font-size:0.8rem; margin-bottom:12px;">
                    Select any probe stimulus to inspect token differences, semantic reference rationale, and side-by-side model predictions.
                </div>
                """
            )

            all_pids = list(probe_map.keys())
            if all_pids:
                sel_pid = st.selectbox(
                    "Select Probe Stimulus to Inspect:",
                    options=all_pids,
                    format_func=lambda pid: f"[{pid[:10]}] {probe_map[pid].get('perturbation_type', '').upper()} ➔ {probe_map[pid].get('perturbed_text', '')[:75]}...",
                    key="comp_sel_drawer_probe",
                )

                if sel_pid and sel_pid in probe_map:
                    p_data = probe_map[sel_pid]
                    sem_ref = p_data.get("semantic_reference") or {}
                    
                    drw_c1, drw_c2 = st.columns([1, 1])
                    with drw_c1:
                        _html(
                            f"""
                            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 14px; font-family:monospace; margin-bottom:10px;">
                                <div style="color:#94a3b8; font-size:0.72rem; text-transform:uppercase;">Original Baseline Stimulus</div>
                                <div style="color:#f1f5f9; font-size:0.88rem; margin-top:4px; font-weight:bold;">"{p_data.get('seed_text', '')}"</div>
                            </div>
                            """
                        )
                    with drw_c2:
                        _html(
                            f"""
                            <div style="background:#141824; border:1px solid #38bdf8; border-radius:6px; padding:12px 14px; font-family:monospace; margin-bottom:10px;">
                                <div style="color:#38bdf8; font-size:0.72rem; text-transform:uppercase;">Perturbed Probe Stimulus</div>
                                <div style="color:#f1f5f9; font-size:0.88rem; margin-top:4px; font-weight:bold;">"{p_data.get('perturbed_text', '')}"</div>
                            </div>
                            """
                        )

                    # Semantic Ground Truth Reference Details
                    ref_pol = sem_ref.get("final_semantic_polarity", "N/A")
                    ref_rel = sem_ref.get("semantic_relation_to_baseline", "N/A")
                    ref_exp = sem_ref.get("expected_label_3class", "N/A")
                    ref_rat = sem_ref.get("reasoning_rationale", "Verified semantic ground truth contract.")
                    
                    _html(
                        f"""
                        <div style="background:#0f172a; border:1px solid #1e293b; border-left:4px solid #10b981; border-radius:4px; padding:10px 14px; font-family:monospace; margin-bottom:14px;">
                            <div style="display:flex; gap:20px; flex-wrap:wrap; font-size:0.78rem;">
                                <div><span style="color:#94a3b8;">SEMANTIC POLARITY:</span> <strong style="color:#10b981;">{ref_pol}</strong></div>
                                <div><span style="color:#94a3b8;">RELATION TO BASELINE:</span> <strong style="color:#38bdf8;">{ref_rel}</strong></div>
                                <div><span style="color:#94a3b8;">EXPECTED 3-CLASS:</span> <strong style="color:#e2e8f0;">{ref_exp}</strong></div>
                            </div>
                            <div style="color:#cbd5e1; font-size:0.75rem; margin-top:6px;"><strong>Rationale:</strong> {ref_rat}</div>
                        </div>
                        """
                    )

                    # Side-by-Side Model Comparison Grid
                    m_outs = p_data.get("models", {})
                    _html("<div style='font-size:0.85rem; font-weight:bold; color:#cbd5e1; font-family:monospace; margin-bottom:6px;'>MODEL PREDICTIONS & DEVIATION DIAGNOSES:</div>")
                    m_grid_cols = st.columns(len(all_known_models))

                    for idx, m_id in enumerate(all_known_models):
                        m_disp = get_model_display_name(m_id)
                        with m_grid_cols[idx]:
                            if m_id not in m_outs:
                                _html(
                                    f"""
                                    <div style="background:#0b0f19; border:1px dashed #334155; border-radius:6px; padding:10px; font-family:monospace; min-height:120px;">
                                        <div style="color:#64748b; font-size:0.72rem; font-weight:bold;">{m_disp}</div>
                                        <div style="color:#64748b; font-size:0.9rem; font-weight:bold; margin-top:8px;">— NOT RUN</div>
                                        <div style="color:#475569; font-size:0.7rem; margin-top:4px;">No execution data</div>
                                    </div>
                                    """
                                )
                            else:
                                o = m_outs[m_id]
                                p_lbl = o.get("perturbed_label", "UNK")
                                p_conf = o.get("perturbed_confidence", 0.0) * 100.0
                                o_lbl = o.get("original_label", "UNK")
                                o_conf = o.get("original_confidence", 0.0) * 100.0
                                delta_pts = (p_conf - o_conf)
                                is_sat = o.get("expectation_satisfied", True)
                                f_type = o.get("failure_type")

                                if f_type and str(f_type).lower() in ("blind", "spurious", "misweighted"):
                                    c_border = "#ef4444"
                                    c_bg = "rgba(239, 68, 68, 0.12)"
                                    status_tag = f"✕ {str(f_type).upper()}"
                                    tag_col = "#fca5a5"
                                elif not is_sat or o.get("unexpected_behavior"):
                                    c_border = "#f59e0b"
                                    c_bg = "rgba(245, 158, 11, 0.12)"
                                    status_tag = "⚠ DEVIATION"
                                    tag_col = "#fde68a"
                                else:
                                    c_border = "#10b981"
                                    c_bg = "rgba(16, 185, 129, 0.08)"
                                    status_tag = "✓ MATCH"
                                    tag_col = "#6ee7b7"

                                _html(
                                    f"""
                                    <div style="background:{c_bg}; border:1.5px solid {c_border}; border-radius:6px; padding:10px; font-family:monospace; min-height:120px;">
                                        <div style="color:#f1f5f9; font-size:0.72rem; font-weight:bold; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{m_disp}</div>
                                        <div style="font-size:1.05rem; font-weight:800; color:#f1f5f9; margin-top:4px;">{p_lbl}</div>
                                        <div style="font-size:0.72rem; color:#cbd5e1;">Conf: {p_conf:.1f}% ({delta_pts:+.1f} pp)</div>
                                        <div style="font-size:0.68rem; color:#94a3b8; margin:3px 0;">{o_lbl} ➔ {p_lbl}</div>
                                        <div style="color:{tag_col}; font-size:0.7rem; font-weight:bold; margin-top:4px;">{status_tag}</div>
                                    </div>
                                    """
                                )

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
                options=all_known_models,
                format_func=lambda x: get_model_display_name(x),
                key="comp_sel_eval_model_v2",
            )

        if sel_model_id not in models_data:
            st.warning(f"⚠️ {get_model_display_name(sel_model_id)} was not executed in this run.")
        else:
            m_eval_info = models_data[sel_model_id].get("behavioral_metrics", {})
            m_evals = models_data[sel_model_id].get("evaluations", [])

            m_acc = (m_eval_info.get("behavioral_consistency") if m_eval_info.get("behavioral_consistency") is not None else m_eval_info.get("satisfaction_rate", 1.0)) * 100.0
            m_ece = m_eval_info.get("ece", 0.0)
            m_confs = [e.get("perturbed_confidence", 0.0) for e in m_evals if e.get("perturbed_confidence") is not None]
            m_mean_conf = (sum(m_confs) / len(m_confs) * 100.0) if m_confs else 0.0
            m_sat = sum(1 for e in m_evals if e.get("expectation_satisfied"))

            # KPI Metrics Cards
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            with kpi1:
                st.metric("Accuracy / Consistency", f"{m_acc:.1f}%")
            with kpi2:
                st.metric("ECE (Calibration Error)", f"{m_ece:.4f}")
            with kpi3:
                st.metric("Mean Confidence", f"{m_mean_conf:.1f}%")
            with kpi4:
                st.metric("Compliance", f"{m_sat} / {len(m_evals)} Probes")

            eval_rows = []
            for e in m_evals:
                p_id = e.get("probe_id", "")[:10]
                cat = e.get("perturbation_type", "").upper()
                orig_lbl = e.get("original_label", "POSITIVE")
                pred_lbl = e.get("perturbed_label", "UNK")
                conf = e.get("perturbed_confidence", 0.0) * 100.0
                exp_flip = e.get("expected_flip", False)

                sem_ref = e.get("semantic_reference") or {}
                sem_pol = sem_ref.get("final_semantic_polarity", "")
                sem_rel = sem_ref.get("semantic_relation_to_baseline", "")

                if sem_pol:
                    exp_desc = f"{sem_pol} [{sem_rel}]" if sem_rel else sem_pol
                elif exp_flip:
                    opp_lbl = "NEGATIVE" if orig_lbl == "POSITIVE" else "POSITIVE"
                    exp_desc = f"FLIP ➔ {opp_lbl}"
                else:
                    exp_desc = f"PRESERVE ➔ {orig_lbl}"

                is_sat = e.get("expectation_satisfied", False)
                compat = e.get("semantic_compatibility", "DIRECTLY_COMPATIBLE")
                if is_sat:
                    if compat == "NOT_DIRECTLY_REPRESENTABLE":
                        status_desc = "✓ MATCH (FORCED BINARY)"
                    else:
                        status_desc = "✓ MATCH"
                else:
                    status_desc = f"✕ {e.get('failure_type', 'FAIL').upper()}"

                eval_rows.append({
                    "Probe ID": p_id,
                    "Category": cat,
                    "Baseline": orig_lbl,
                    "Expected": exp_desc,
                    "Predicted": pred_lbl,
                    "Confidence": f"{conf:.1f}%",
                    "Shift": f"{e.get('confidence_delta_pts', 0.0):+.1f} pp",
                    "Status": status_desc,
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
        st.subheader("Descriptive Behavioral Operational Profiles")
        st.caption("Quantitative operational characteristics across identical perturbation stimuli without normative rankings.")

        metric_rows = []
        for m_id in all_known_models:
            m_disp = get_model_display_name(m_id)
            m_task = CANONICAL_MODEL_NAMES.get(m_id, {}).get("task_badge", "Unknown")

            if m_id not in models_data:
                metric_rows.append({
                    "Model Architecture": m_disp,
                    "Task Space": m_task,
                    "Accuracy": "—",
                    "ECE": "—",
                    "Mean Confidence": "—",
                    "Observed Flip Rate": "—",
                    "Expected Flip Rate": "—",
                    "Compliance": "—",
                    "Mean Shift": "—",
                    "Total Probes": "NOT RUN",
                })
                continue

            m_info = models_data[m_id].get("behavioral_metrics") or {}
            obs_flip = (m_info.get("observed_flip_rate") if m_info.get("observed_flip_rate") is not None else m_info.get("flip_rate", 0.0)) * 100.0
            exp_flip = (m_info.get("suite_expected_flip_rate", m_info.get("expected_flip_rate", 0.0))) * 100.0
            compliance = (m_info.get("expected_flip_compliance", m_info.get("observed_expected_reversal_rate", 0.0))) * 100.0
            accuracy = (m_info.get("behavioral_consistency") if m_info.get("behavioral_consistency") is not None else m_info.get("satisfaction_rate", 1.0)) * 100.0
            ece = m_info.get("ece") or 0.0
            conf_shifts = m_info.get("confidence_shifts")
            mean_shift = conf_shifts.get("mean_delta_pts", 0.0) if isinstance(conf_shifts, dict) else 0.0

            evals = models_data[m_id].get("evaluations", [])
            confs = [e.get("perturbed_confidence", 0.0) for e in evals if e.get("perturbed_confidence") is not None]
            mean_conf = (sum(confs) / len(confs) * 100.0) if confs else 0.0

            metric_rows.append({
                "Model Architecture": m_disp,
                "Task Space": m_task,
                "Accuracy": f"{accuracy:.1f}%",
                "ECE": f"{ece:.4f}",
                "Mean Confidence": f"{mean_conf:.1f}%",
                "Observed Flip Rate": f"{obs_flip:.1f}%",
                "Expected Flip Rate": f"{exp_flip:.1f}%",
                "Compliance": f"{compliance:.1f}%",
                "Mean Shift": f"{mean_shift:+.1f} pp",
                "Total Probes": len(evals),
            })

        if metric_rows:
            st.dataframe(pd.DataFrame(metric_rows), use_container_width=True, hide_index=True)
        else:
            st.caption("No behavioral metrics computed.")

    # ==========================================
    # Tab 4: Models & Failures Breakdown
    # ==========================================
    with tab_failures:
        st.subheader("Target Architecture Failure Breakdown & Taxonomy Counts")
        st.caption("Empirical distribution of diagnosed failure categories (Blind, Spurious, Misweighted, Undetermined) across evaluated models without normative rankings.")

        fail_summary_rows = []
        all_failures_by_model: Dict[str, List[Dict[str, Any]]] = {}

        total_anomalies_all = 0
        total_blind_all = 0
        total_spurious_all = 0
        total_misweighted_all = 0
        total_undet_all = 0

        for m_id in all_known_models:
            m_disp = get_model_display_name(m_id)
            m_task = CANONICAL_MODEL_NAMES.get(m_id, {}).get("task_badge", "Unknown")

            if m_id not in models_data:
                fail_summary_rows.append({
                    "Model Architecture": m_disp,
                    "Task Space": m_task,
                    "Total Probes": "—",
                    "Total Failures": "NOT RUN",
                    "Failure Rate": "—",
                    "BLIND (Invariance)": "—",
                    "SPURIOUS (Shortcut)": "—",
                    "MISWEIGHTED (Clause)": "—",
                    "UNDETERMINED": "—",
                    "Primary Failure Mode": "NOT RUN",
                })
                continue

            m_evals = models_data[m_id].get("evaluations", [])
            m_fails = models_data[m_id].get("failures", [])
            all_failures_by_model[m_id] = m_fails

            total_probes = len(m_evals)
            total_fails = len(m_fails)
            fail_rate = (total_fails / total_probes * 100.0) if total_probes > 0 else 0.0

            c_blind = sum(1 for f in m_fails if str(f.get("category", "")).lower() == "blind")
            c_spurious = sum(1 for f in m_fails if str(f.get("category", "")).lower() == "spurious")
            c_misweighted = sum(1 for f in m_fails if str(f.get("category", "")).lower() == "misweighted")
            c_undet = sum(1 for f in m_fails if str(f.get("category", "")).lower() == "undetermined")

            total_anomalies_all += total_fails
            total_blind_all += c_blind
            total_spurious_all += c_spurious
            total_misweighted_all += c_misweighted
            total_undet_all += c_undet

            mode_counts = {
                "BLIND": c_blind,
                "SPURIOUS": c_spurious,
                "MISWEIGHTED": c_misweighted,
                "UNDETERMINED": c_undet,
            }
            top_mode = max(mode_counts, key=mode_counts.get) if total_fails > 0 and max(mode_counts.values()) > 0 else "NONE"

            fail_summary_rows.append({
                "Model Architecture": m_disp,
                "Task Space": m_task,
                "Total Probes": total_probes,
                "Total Failures": total_fails,
                "Failure Rate": f"{fail_rate:.1f}%",
                "BLIND (Invariance)": c_blind,
                "SPURIOUS (Shortcut)": c_spurious,
                "MISWEIGHTED (Clause)": c_misweighted,
                "UNDETERMINED": c_undet,
                "Primary Failure Mode": top_mode,
            })

        # Summary KPI cards
        kpi_c1, kpi_c2, kpi_c3, kpi_c4, kpi_c5 = st.columns(5)
        with kpi_c1:
            _html(
                f"""
                <div style="background:#111622; border:1px solid #1e293b; border-radius:6px; padding:10px 14px;">
                    <div style="color:#94a3b8; font-size:0.72rem; text-transform:uppercase;">Total Failures</div>
                    <div style="font-size:1.4rem; font-weight:800; color:#f87171; margin-top:2px;">{total_anomalies_all}</div>
                </div>
                """
            )
        with kpi_c2:
            _html(
                f"""
                <div style="background:#111622; border:1px solid #1e293b; border-radius:6px; padding:10px 14px;">
                    <div style="color:#94a3b8; font-size:0.72rem; text-transform:uppercase;">BLIND (Invariance)</div>
                    <div style="font-size:1.4rem; font-weight:800; color:#fb7185; margin-top:2px;">{total_blind_all}</div>
                </div>
                """
            )
        with kpi_c3:
            _html(
                f"""
                <div style="background:#111622; border:1px solid #1e293b; border-radius:6px; padding:10px 14px;">
                    <div style="color:#94a3b8; font-size:0.72rem; text-transform:uppercase;">SPURIOUS (Shortcut)</div>
                    <div style="font-size:1.4rem; font-weight:800; color:#fbbf24; margin-top:2px;">{total_spurious_all}</div>
                </div>
                """
            )
        with kpi_c4:
            _html(
                f"""
                <div style="background:#111622; border:1px solid #1e293b; border-radius:6px; padding:10px 14px;">
                    <div style="color:#94a3b8; font-size:0.72rem; text-transform:uppercase;">MISWEIGHTED (Clause)</div>
                    <div style="font-size:1.4rem; font-weight:800; color:#c084fc; margin-top:2px;">{total_misweighted_all}</div>
                </div>
                """
            )
        with kpi_c5:
            _html(
                f"""
                <div style="background:#111622; border:1px solid #1e293b; border-radius:6px; padding:10px 14px;">
                    <div style="color:#94a3b8; font-size:0.72rem; text-transform:uppercase;">UNDETERMINED</div>
                    <div style="font-size:1.4rem; font-weight:800; color:#94a3b8; margin-top:2px;">{total_undet_all}</div>
                </div>
                """
            )

        st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
        # Primary Cross-Model Failure Breakdown Table
        df_fails = pd.DataFrame(fail_summary_rows)
        st.dataframe(df_fails, use_container_width=True, hide_index=True)

        # Interactive Model-Specific Failure Inspector
        st.markdown("---")
        _html(
            """
            <div style="font-size:1.0rem; font-weight:700; color:#f1f5f9; margin-bottom:4px;">
                🔍 PER-MODEL FAILURE EVIDENCE LOG
            </div>
            <div style="color:#94a3b8; font-size:0.8rem; margin-bottom:10px;">
                Inspect probe-level failure evidence, observed model classifications, and failure modes for any target architecture.
            </div>
            """
        )

        sel_model_id = st.selectbox(
            "Select Target Architecture to Inspect Failures:",
            options=all_known_models,
            format_func=lambda m: f"{get_model_display_name(m)} [{len(all_failures_by_model.get(m, []))} failures]",
            key="comp_fail_tab_sel_model",
        )

        if sel_model_id:
            m_fails = all_failures_by_model.get(sel_model_id, [])
            if not m_fails:
                st.success(f"✓ Zero behavioral failures diagnosed for **{get_model_display_name(sel_model_id)}**. The model conformed to expected semantic transitions across all evaluated probes.")
            else:
                f_table_rows = []
                for f in m_fails:
                    f_table_rows.append({
                        "Severity": f.get("severity", "HIGH"),
                        "Probe ID": f.get("probe_id", "")[:10],
                        "Linguistic Category": str(f.get("probe_type", f.get("category", ""))).upper(),
                        "Expected Behavior": f.get("expected_behavior", "FLIP"),
                        "Observed Prediction": f.get("observed_prediction", "PRESERVE"),
                        "Failure Type": str(f.get("category", "UNDETERMINED")).upper(),
                        "Evidence Summary": f.get("evidence", "Behavioral transition contradicted expected ground truth."),
                    })
                st.dataframe(pd.DataFrame(f_table_rows), use_container_width=True, hide_index=True)

    # ==========================================
    # Tab 4: Comparative Diagnostic Charts
    # ==========================================
    with tab_visuals:
        st.subheader("Cross-Model Diagnostic Visualizations")
        st.caption("Publication-grade comparative heatmaps, flip rates, and failure distributions with distinct model identities.")

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
                        _html(
                            f"""
                            <div style="background:#0f172a; border:1px solid #1e293b; border-radius:6px; padding:8px 12px; margin-top:10px;">
                                <div style="font-size:0.9rem; font-weight:bold; color:#f1f5f9;">{f_title}</div>
                                <div style="font-size:0.75rem; color:#94a3b8;">{f_desc}</div>
                            </div>
                            """
                        )
                        st.image(f_path, use_container_width=True)
            if not found_any:
                st.info("No comparative figure files found on disk for this experiment.")
        else:
            st.info("No figures directory found for this experiment run.")
