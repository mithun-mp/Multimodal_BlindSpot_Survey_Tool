"""
Failure Analysis: Scientific Evidence-Backed Taxonomy Diagnoses.
Provides structured diagnostic evidence cards for Blind, Spurious, Misweighted,
and Undetermined failure modes with explicit observed vs expected transitions.
"""
import streamlit as st
from typing import Dict, Any, List

from blindspot.core.types import FailureCategory
from blindspot.ui.components import render_failure_record, render_empty_state


def render_failure_lab():
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                SECONDARY DIAGNOSTIC ANALYSIS — FAILURE TAXONOMY
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

    # Filter Controls
    col_flt1, col_flt2, col_flt3 = st.columns([2, 2, 2])
    with col_flt1:
        cat_options = ["ALL"] + [c.value for c in FailureCategory]
        selected_cat = st.selectbox("Taxonomy Category:", options=cat_options, key="fail_sel_cat")

    with col_flt2:
        model_options = ["ALL"] + list(models_data.keys())
        selected_model = st.selectbox("Target Model:", options=model_options, key="fail_sel_model")

    with col_flt3:
        search_term = st.text_input("Search Text/Probe ID:", placeholder="Filter keyword...", key="fail_sel_search")

    filtered = []
    for f in all_failures:
        if selected_cat != "ALL" and f.get("category") != selected_cat:
            continue
        if selected_model != "ALL" and f.get("model_id") != selected_model:
            continue
        if search_term.strip():
            text_haystack = f"{f.get('original_sentence', '')} {f.get('perturbed_sentence', '')} {f.get('probe_id', '')}".lower()
            if search_term.lower() not in text_haystack:
                continue
        filtered.append(f)

    # Category Breakdown Metrics
    cat_counts = {}
    for f in all_failures:
        c = f.get("category", "Undetermined")
        cat_counts[c] = cat_counts.get(c, 0) + 1

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("BLIND", f"{cat_counts.get('Blind', 0)}")
    with col_m2:
        st.metric("SPURIOUS", f"{cat_counts.get('Spurious', 0)}")
    with col_m3:
        st.metric("MISWEIGHTED", f"{cat_counts.get('Misweighted', 0)}")
    with col_m4:
        st.metric("UNDETERMINED", f"{cat_counts.get('Undetermined', 0)}")

    st.caption(f"Showing **{len(filtered)}** of **{len(all_failures)}** diagnosed failure records.")

    # Render Evidence Records
    for idx, failure in enumerate(filtered):
        render_failure_record(failure, idx=idx)
