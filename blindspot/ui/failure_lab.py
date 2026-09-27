"""
Failure Analysis: Scientific Evidence-Backed Taxonomy Diagnoses.
Provides structured diagnostic failure table, compact multi-metric failure summary,
severity classification, and interactive token attribution cards without model ranking.
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any, List

from blindspot.core.types import FailureCategory
from blindspot.ui.components import render_failure_record, render_empty_state
from blindspot.models.registry import get_model_display_name, get_model_short_name


def render_failure_lab():
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                SECONDARY DIAGNOSTIC ANALYSIS — FAILURE TAXONOMY & EVIDENCE
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Traceable diagnostic evidence classifying behavioral inconsistencies into Blind, Spurious, Misweighted, and Undetermined failure modes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    results = st.session_state.get("active_results")
    if not results:
        runner = st.session_state.get("active_runner")
        if runner and runner.status == "completed" and getattr(runner, "_result", None):
            results = runner._result
            st.session_state["active_results"] = results

    if not results:
        clicked = render_empty_state(
            title="NO FAILURE RECORDS LOADED",
            message="No active audit experiment results found in session. Execute an audit or load a run from Run History.",
            action_label="GO TO EXPERIMENT LAB",
            action_key="fail_empty_to_exp",
        )
        if clicked:
            st.session_state["current_page"] = "Experiment"
            st.rerun()
        return

    models_data = results.get("models", {})
    all_failures: List[Dict[str, Any]] = []

    for m_id, m_dict in models_data.items():
        for f in m_dict.get("failures", []):
            item = dict(f)
            item["model_id"] = m_id
            all_failures.append(item)

    if not all_failures:
        st.markdown(
            """
            <div style="background:#064e3b; border:1px solid #059669; border-radius:6px; padding:20px; text-align:center; margin:20px 0;">
                <div style="font-size:1.1rem; font-weight:bold; color:#ecfdf5;">ZERO BEHAVIORAL FAILURES DETECTED</div>
                <div style="color:#a7f3d0; font-size:0.85rem; margin-top:4px;">All evaluated models complied with expected semantic transition criteria across all probes.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Count failure categories and deviations
    cat_counts = {"Blind": 0, "Spurious": 0, "Misweighted": 0, "Undetermined": 0}
    for f in all_failures:
        c = f.get("category", "Undetermined")
        cat_counts[c] = cat_counts.get(c, 0) + 1

    total_probes_eval = sum(len(m.get("evaluations", [])) for m in models_data.values())
    confirmed_failures = cat_counts["Blind"] + cat_counts["Spurious"] + cat_counts["Misweighted"]
    undetermined_anomalies = cat_counts["Undetermined"]

    # ==========================================
    # FAILURE SUMMARY BANNER (Phase 16)
    # ==========================================
    st.markdown(
        f"""
        <div style="background:#111622; border:1px solid #26334d; border-radius:6px; padding:14px 18px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-bottom:12px;">
                <div>
                    <span style="font-size:1.05rem; font-weight:bold; color:#f1f5f9; font-family:monospace;">FAILURES DETECTED SUMMARY</span>
                    <span style="color:#94a3b8; font-size:0.8rem; margin-left:12px;">Descriptive categorization without model rankings</span>
                </div>
                <div style="font-family:monospace; font-size:0.82rem; color:#cbd5e1;">
                    Evaluations: <strong>{total_probes_eval}</strong> &bull; Total Anomalies: <strong style="color:#f87171;">{len(all_failures)}</strong>
                </div>
            </div>
            <div class="failure-summary-grid">
                <div class="failure-metric-card" style="border-left:3px solid #ef4444;">
                    <div style="color:#94a3b8; font-size:0.72rem;">BLIND (Invariance)</div>
                    <div class="failure-metric-card-val" style="color:#f87171;">{cat_counts.get('Blind', 0)}</div>
                    <div style="color:#64748b; font-size:0.68rem;">Ignored perturbation</div>
                </div>
                <div class="failure-metric-card" style="border-left:3px solid #f97316;">
                    <div style="color:#94a3b8; font-size:0.72rem;">SPURIOUS (Shortcut)</div>
                    <div class="failure-metric-card-val" style="color:#fb923c;">{cat_counts.get('Spurious', 0)}</div>
                    <div style="color:#64748b; font-size:0.68rem;">Lexical cue reliance</div>
                </div>
                <div class="failure-metric-card" style="border-left:3px solid #a855f7;">
                    <div style="color:#94a3b8; font-size:0.72rem;">MISWEIGHTED (Clause)</div>
                    <div class="failure-metric-card-val" style="color:#c084fc;">{cat_counts.get('Misweighted', 0)}</div>
                    <div style="color:#64748b; font-size:0.68rem;">Subordinate dominance</div>
                </div>
                <div class="failure-metric-card" style="border-left:3px solid #64748b;">
                    <div style="color:#94a3b8; font-size:0.72rem;">UNDETERMINED</div>
                    <div class="failure-metric-card-val" style="color:#cbd5e1;">{cat_counts.get('Undetermined', 0)}</div>
                    <div style="color:#64748b; font-size:0.68rem;">Inconclusive saliency</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Filter Controls (Phases 17 & 25)
    col_flt1, col_flt2, col_flt3 = st.columns([2, 2, 2])
    with col_flt1:
        cat_options = ["ALL"] + [c.value for c in FailureCategory]
        selected_cat = st.selectbox("Taxonomy Category Filter:", options=cat_options, key="fail_sel_cat_v2")

    with col_flt2:
        model_options = ["ALL"] + list(models_data.keys())
        selected_model = st.selectbox(
            "Target Architecture Filter:",
            options=model_options,
            format_func=lambda m: "ALL ARCHITECTURES" if m == "ALL" else get_model_display_name(m),
            key="fail_sel_model_v2",
        )

    with col_flt3:
        search_term = st.text_input("Filter Text / Probe ID:", placeholder="Search keywords...", key="fail_sel_search_v2")

    # Filter Records
    filtered: List[Dict[str, Any]] = []
    for f in all_failures:
        if selected_cat != "ALL" and f.get("category") != selected_cat:
            continue
        if selected_model != "ALL" and f.get("model_id") != selected_model:
            continue
        if search_term.strip():
            haystack = f"{f.get('original_sentence', '')} {f.get('perturbed_sentence', '')} {f.get('probe_id', '')} {f.get('details', '')}".lower()
            if search_term.lower() not in haystack:
                continue
        filtered.append(f)

    st.caption(f"Displaying **{len(filtered)}** of **{len(all_failures)}** diagnosed failure records.")

    # ==========================================
    # PRIMARY STRUCTURED FAILURE TABLE (Phase 15)
    # ==========================================
    if filtered:
        st.markdown(
            """
            <div style="font-family:monospace; font-size:0.85rem; font-weight:bold; color:#cbd5e1; margin:14px 0 6px 0;">
                STRUCTURED BEHAVIORAL FAILURE REGISTER
            </div>
            """,
            unsafe_allow_html=True,
        )

        table_rows = []
        for idx, f in enumerate(filtered):
            m_id = f.get("model_id", "")
            m_disp = get_model_display_name(m_id)
            p_id = (f.get("probe_id") or f.get("probe_type") or f"P{idx+1}")[:10]
            cat = f.get("category", "Undetermined")

            # Determine severity based on category and confidence shift
            conf_delta = abs(f.get("confidence_shift_pts", 0.0))
            if cat in ("Blind", "Spurious"):
                severity = "HIGH"
                sev_color = "#ef4444"
            elif cat == "Misweighted" or conf_delta >= 25.0:
                severity = "MEDIUM"
                sev_color = "#f59e0b"
            else:
                severity = "LOW"
                sev_color = "#64748b"

            orig_lbl = f.get("original_label", "UNK")
            pert_lbl = f.get("perturbed_label", "UNK")
            exp_flip = f.get("expected_flip")

            if exp_flip is True:
                exp_trans = f"FLIP ({orig_lbl} ➔ { 'NEG' if 'POS' in orig_lbl else 'POS' })"
            elif exp_flip is False:
                exp_trans = f"PRESERVE ({orig_lbl})"
            else:
                exp_trans = "FLIP / CHANGE"

            obs_trans = f"{orig_lbl[:3]} ➔ {pert_lbl[:3]} ({f.get('perturbed_confidence', 0.0)*100:.1f}%)"
            evidence_snip = f.get("details", "") or f.get("why_failure", "")
            if len(evidence_snip) > 90:
                evidence_snip = evidence_snip[:88] + "..."

            table_rows.append({
                "Severity": severity,
                "Model": m_disp,
                "Probe": p_id,
                "Expected Behavior": exp_trans,
                "Observed Behavior": obs_trans,
                "Failure Type": cat.upper(),
                "Evidence Summary": evidence_snip,
            })

        df_fail = pd.DataFrame(table_rows)
        st.dataframe(df_fail, use_container_width=True, hide_index=True)

        # ==========================================
        # INTERACTIVE EVIDENCE & ATTRIBUTION CARDS
        # ==========================================
        st.markdown("---")
        st.markdown(
            """
            <div style="font-size:1.05rem; font-weight:700; color:#f1f5f9; margin-bottom:4px;">
                🔍 IN-DEPTH TOKEN ATTRIBUTION & FAILURE EXPLANATION CARDS
            </div>
            <div style="color:#94a3b8; font-size:0.8rem; margin-bottom:12px;">
                Expand individual failure records below to inspect token-level attribution weights, saliency shifts, and remediation strategies.
            </div>
            """,
            unsafe_allow_html=True,
        )

        for idx, failure in enumerate(filtered):
            with st.expander(
                f"Failure #{idx + 1}: [{failure.get('category', 'Failure').upper()}] {get_model_display_name(failure.get('model_id', ''))} ➔ {failure.get('probe_id', '')[:10]}",
                expanded=(idx < 2),
            ):
                render_failure_record(failure, idx=idx)
    else:
        st.info("No failure records matched your filter criteria.")
