"""
Overview: Central Research Control Center for BlindSpot Workstation.
Provides quick-launch action triggers, host telemetry status, recent activity tables,
and latest findings summary without static documentation bloat.
"""
import streamlit as st
import time
import pandas as pd
from typing import Dict, Any, List

from blindspot.execution.resources import ResourceManager
from blindspot.models.cache import ModelCache
from blindspot.storage.run_store import RunStore
from blindspot.ui.components import render_empty_state


def render_overview():
    store = RunStore()
    cache = ModelCache.get_shared_cache()
    telemetry = ResourceManager.get_live_telemetry()
    cached_models = cache.cached_model_ids()

    cpu = telemetry["cpu"]
    ram = telemetry["ram"]
    net = telemetry["network"]

    net_down = f"{net['speed_down_kbps']:.0f} KB/s" if net['speed_down_kbps'] < 1024 else f"{net['speed_down_kbps']/1024:.1f} MB/s"
    net_up = f"{net['speed_up_kbps']:.0f} KB/s" if net['speed_up_kbps'] < 1024 else f"{net['speed_up_kbps']/1024:.1f} MB/s"

    # ==========================================
    # Top Control Center Header & Quick Triggers
    # ==========================================
    st.markdown(
        """
        <div style="margin-bottom:14px;">
            <div style="font-size:1.35rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                RESEARCH CONTROL CENTER
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                High-performance multimodal behavioral auditing & explainability workstation.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_btn1, col_btn2, col_spacer = st.columns([2, 2, 5])
    with col_btn1:
        if st.button("▶ NEW EXPERIMENT", type="primary", use_container_width=True, key="ov_btn_new_exp"):
            st.session_state["current_page"] = "Experiment"
            st.rerun()

    with col_btn2:
        if st.button("📁 LOAD RUN", type="secondary", use_container_width=True, key="ov_btn_load_run"):
            st.session_state["current_page"] = "Run History"
            st.rerun()

    # ==========================================
    # System Hardware & Cache Telemetry Grid
    # ==========================================
    st.markdown(
        """
        <div style="margin:20px 0 8px 0; font-family:monospace; font-size:0.85rem; font-weight:bold; color:#cbd5e1; display:flex; justify-content:space-between; align-items:center;">
            <span>HOST TELEMETRY & HARDWARE SENSORS</span>
            <span style="font-size:0.7rem; color:#38bdf8; font-weight:normal;">● LIVE HARDWARE PROBE ACTIVE</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cache_count = len(cached_models)
    cache_desc = f"{cache_count} model(s) loaded" if cache_count > 0 else "0 models in memory"

    # Single Unified Row: CPU, RAM, Network Speed, Model Cache
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 14px; font-family:monospace; min-height:140px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#94a3b8; font-size:0.75rem;">CPU PROCESSOR</span>
                    <span style="color:#38bdf8; font-size:0.75rem;">{cpu['logical_cores']} Cores</span>
                </div>
                <div style="color:#f1f5f9; font-size:1.35rem; font-weight:bold; margin-top:4px;">{cpu['percent']:.1f}%</div>
                <div style="color:#cbd5e1; font-size:0.75rem; margin-top:2px;">{cpu['physical_cores']} Physical / {cpu['logical_cores']} Logical</div>
                <div style="color:#64748b; font-size:0.7rem; margin-top:2px;">Clock: {cpu['frequency_ghz']:.2f} GHz</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_s2:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 14px; font-family:monospace; min-height:140px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#94a3b8; font-size:0.75rem;">HOST MEMORY (RAM)</span>
                    <span style="color:#10b981; font-size:0.75rem;">Active</span>
                </div>
                <div style="color:#f1f5f9; font-size:1.35rem; font-weight:bold; margin-top:4px;">{ram['percent']:.1f}%</div>
                <div style="color:#cbd5e1; font-size:0.75rem; margin-top:2px;">{ram['used_gb']:.1f} GB Allocated</div>
                <div style="color:#64748b; font-size:0.7rem; margin-top:2px;">Dynamic OS Memory Pool</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_s3:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 14px; font-family:monospace; min-height:140px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#94a3b8; font-size:0.75rem;">NETWORK SPEED & I/O</span>
                    <span style="color:#a855f7; font-size:0.75rem;">Active</span>
                </div>
                <div style="color:#f1f5f9; font-size:1.35rem; font-weight:bold; margin-top:4px;">
                    <span style="color:#38bdf8;">↓ {net_down}</span> &nbsp; <span style="color:#a855f7;">↑ {net_up}</span>
                </div>
                <div style="color:#cbd5e1; font-size:0.75rem; margin-top:2px;">In: {net['total_recv_mb']:.1f} MB | Out: {net['total_sent_mb']:.1f} MB</div>
                <div style="color:#64748b; font-size:0.7rem; margin-top:2px;">Host Network Interface Counters</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_s4:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 14px; font-family:monospace; min-height:140px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#94a3b8; font-size:0.75rem;">RESIDENT MODEL CACHE</span>
                    <span style="color:#38bdf8; font-size:0.75rem;">LRU Managed</span>
                </div>
                <div style="color:#38bdf8; font-size:1.35rem; font-weight:bold; margin-top:4px;">{cache_count} / {cache._max_size}</div>
                <div style="color:#cbd5e1; font-size:0.75rem; margin-top:2px;">{cache_desc}</div>
                <div style="color:#64748b; font-size:0.7rem; margin-top:2px;">Zero-Disk Latency Model Serving</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ==========================================
    # Recent Activity Table
    # ==========================================
    st.markdown(
        """
        <div style="margin:24px 0 8px 0; font-family:monospace; font-size:0.85rem; font-weight:bold; color:#cbd5e1;">
            RECENT EXPERIMENT RUNS
        </div>
        """,
        unsafe_allow_html=True,
    )

    all_runs = store.list_runs()

    if not all_runs:
        st.caption("No persisted experiments found in `runs/`. Launch your first audit to populate recent activity.")
    else:
        recent_rows = []
        for r in all_runs[:5]:
            exp_id = r.get("experiment_id", "unknown")
            exp_name = r.get("experiment_name") or exp_id
            status = r.get("status", "unknown").upper()
            models_list = r.get("models", [])
            num_models = len(models_list)
            num_probes = r.get("num_probes")
            probes_str = str(num_probes) if num_probes is not None else "--"
            dur = r.get("total_duration_sec", 0.0)
            dur_str = f"{dur:.1f}s" if dur else "--"
            created_at = r.get("created_at", 0)
            date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(created_at)) if created_at else "--"

            recent_rows.append({
                "Experiment Title": exp_name,
                "Run ID": exp_id,
                "Date": date_str,
                "Models": str(num_models),
                "Probes": probes_str,
                "Status": status,
                "Duration": dur_str,
            })

        df_recent = pd.DataFrame(recent_rows)
        st.dataframe(df_recent[["Experiment Title", "Run ID", "Date", "Models", "Probes", "Status", "Duration"]], use_container_width=True, hide_index=True)

    # ==========================================
    # Latest Findings Dashboard
    # ==========================================
    st.markdown(
        """
        <div style="margin:24px 0 8px 0; font-family:monospace; font-size:0.85rem; font-weight:bold; color:#cbd5e1;">
            LATEST AUDIT FINDINGS
        </div>
        """,
        unsafe_allow_html=True,
    )

    active_results = st.session_state.get("active_results")

    # If no active results in memory but prior runs exist, attempt to load the latest run
    if not active_results and all_runs:
        try:
            latest_run_id = all_runs[0].get("experiment_id")
            if latest_run_id:
                latest_data = store.load_run(latest_run_id)
                active_results = latest_data.get("results")
                if active_results:
                    st.session_state["active_results"] = active_results
                    st.session_state["active_experiment_id"] = latest_run_id
                    st.session_state["active_experiment_title"] = all_runs[0].get("experiment_name") or store.get_run_title(latest_run_id)
        except Exception:
            pass

    if not active_results:
        clicked = render_empty_state(
            title="NO FINDINGS AVAILABLE YET",
            message="Execute an audit experiment to observe cross-model agreement, probe transition rates, and taxonomy diagnoses.",
            action_label="CONFIGURE FIRST AUDIT",
            action_key="ov_to_exp_empty",
        )
        if clicked:
            st.session_state["current_page"] = "Experiment"
            st.rerun()
    else:
        cross = active_results.get("cross_model_comparison", {})
        models_data = active_results.get("models", {})
        overall_agree = cross.get("overall_agreement_rate", 0.0)

        # Count total failures and compute mean shift
        total_failures = sum(len(m.get("failures", [])) for m in models_data.values())
        all_shifts = []
        for m in models_data.values():
            cs = m.get("behavioral_metrics", {}).get("confidence_shifts", {})
            if isinstance(cs, dict):
                all_shifts.append(cs.get("mean_delta_pts", 0.0))
            elif isinstance(cs, list):
                for s in cs:
                    if isinstance(s, dict):
                        all_shifts.append(s.get("confidence_shift_pts", 0.0))
                    elif isinstance(s, (int, float)):
                        all_shifts.append(float(s))
        mean_shift = sum(all_shifts) / len(all_shifts) if all_shifts else 0.0

        # Flip rate average across models
        all_flip_rates = [
            m.get("behavioral_metrics", {}).get("flip_rate", 0.0)
            for m in models_data.values()
        ]
        mean_flip = (sum(all_flip_rates) / len(all_flip_rates)) if all_flip_rates else 0.0

        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            st.metric("Model Agreement", f"{overall_agree * 100:.1f}%")
        with col_f2:
            st.metric("Probe Transition Rate", f"{mean_flip * 100:.1f}%")
        with col_f3:
            st.metric("Mean Confidence Shift", f"{mean_shift:+.2f} pp")
        with col_f4:
            st.metric("Failure Diagnoses", f"{total_failures}")

        col_nav_f1, col_nav_f2, col_nav_f3 = st.columns(3)
        with col_nav_f1:
            if st.button("Inspect Model x Probe Matrix", key="ov_btn_inspect_matrix", use_container_width=True):
                st.session_state["current_page"] = "Comparison"
                st.rerun()
        with col_nav_f2:
            if st.button("Review Failure Evidence", key="ov_btn_review_fail", use_container_width=True):
                st.session_state["current_page"] = "Failure Analysis"
                st.rerun()
        with col_nav_f3:
            if st.button("Examine Token Attributions", key="ov_btn_examine_xai", use_container_width=True):
                st.session_state["current_page"] = "Explainability"
                st.rerun()

    # ==========================================
    # Compact Methodology Reference
    # ==========================================
    st.markdown("---")
    st.caption("**Workstation Methodology:** BlindSpot generates deterministic SHA-256 perturbation probes across negation, connectives, and lexical substitution. All models evaluate identical stimuli, allowing descriptive cross-model alignment, token-level attribution comparison, and 4-way failure taxonomy categorization without normative ranking.")
