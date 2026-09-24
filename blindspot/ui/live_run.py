"""
Live Run: Real-Time Execution Console and Telemetry Monitor.
Renders execution status, elapsed time, ETA, per-model evaluation meters,
terminal event streaming, and one-click transition to analytical findings.
"""
import streamlit as st
import time
from typing import Optional

from blindspot.execution.runner import ExperimentRunner
from blindspot.ui.components import render_console_log_line, render_empty_state


def format_duration(seconds: float) -> str:
    """Formats seconds into MM:SS string."""
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def render_live_run():
    runner: Optional[ExperimentRunner] = st.session_state.get("active_runner")

    if not runner:
        st.markdown(
            """
            <div style="margin-bottom:18px;">
                <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                    LIVE EXECUTION MONITOR
                </div>
                <div style="color:#94a3b8; font-size:0.85rem;">
                    Real-time execution telemetry, model progress meters, and asynchronous event streaming.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        clicked = render_empty_state(
            title="NO EXPERIMENT CURRENTLY RUNNING",
            message="No active audit experiment was detected in the session. Configure and launch an audit from the Experiment Lab.",
            action_label="CONFIGURE NEW EXPERIMENT",
            action_key="btn_empty_to_exp",
        )
        if clicked:
            st.session_state["current_page"] = "Experiment"
            st.rerun()
        return

    # Calculate timings
    t_now = time.time()
    t_start = getattr(runner, "start_time", None) or t_now
    t_end = getattr(runner, "end_time", None)
    elapsed_sec = (t_end - t_start) if t_end else (t_now - t_start)
    elapsed_str = format_duration(max(0.0, elapsed_sec))

    # Calculate ETA if running
    eta_str = "--:--"
    prog = max(0.01, min(1.0, runner.progress))
    if runner.status == "running" and prog > 0.05:
        est_total = elapsed_sec / prog
        rem_sec = max(0.0, est_total - elapsed_sec)
        eta_str = f"~{format_duration(rem_sec)}"
    elif runner.status == "completed":
        eta_str = "00:00"

    # Status styling
    status_bg = {
        "running": "#0369a1",
        "completed": "#065f46",
        "cancelled": "#92400e",
        "failed": "#991b1b",
        "idle": "#1e293b",
    }.get(runner.status, "#1e293b")

    status_color = {
        "running": "#38bdf8",
        "completed": "#34d399",
        "cancelled": "#fbbf24",
        "failed": "#f87171",
        "idle": "#94a3b8",
    }.get(runner.status, "#94a3b8")

    exp_title = getattr(runner.config, "experiment_name", None) or getattr(runner, "experiment_id", "Audit")

    # Top Telemetry Banner
    st.markdown(
        f"""
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:14px 18px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <span style="background:{status_bg}; color:#ffffff; font-weight:bold; font-family:monospace; padding:3px 10px; border-radius:4px; font-size:0.85rem; letter-spacing:0.05em;">
                        {runner.status.upper()}
                    </span>
                    <span style="color:#f1f5f9; font-weight:bold; font-size:1.1rem; margin-left:10px;">
                        {exp_title}
                    </span>
                    <span style="color:#64748b; font-family:monospace; font-size:0.78rem; margin-left:8px;">
                        [{runner.experiment_id}]
                    </span>
                </div>
                <div style="display:flex; gap:16px; font-family:monospace; font-size:0.85rem;">
                    <div>ELAPSED: <strong style="color:#f1f5f9;">{elapsed_str}</strong></div>
                    <div>ETA: <strong style="color:#38bdf8;">{eta_str}</strong></div>
                    <div>PROGRESS: <strong style="color:#f1f5f9;">{int(prog * 100)}%</strong></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress Bar
    st.progress(prog)

    # Current Step & Controls
    col_step, col_ctrl1, col_ctrl2 = st.columns([4, 1, 1])
    with col_step:
        st.markdown(
            f"""
            <div style="background:#0f172a; border:1px solid #1e293b; border-radius:4px; padding:6px 12px; font-family:monospace; font-size:0.8rem; color:#cbd5e1;">
                CURRENT OPERATION: <span style="color:#38bdf8; font-weight:bold;">{runner.current_step or 'Initializing...'}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_ctrl1:
        if runner.status == "running":
            if st.button("■ CANCEL RUN", key="live_btn_cancel", type="secondary", use_container_width=True):
                runner.cancel()
                st.warning("Cancellation requested.")
                st.rerun()

    with col_ctrl2:
        auto_refresh = st.checkbox("Auto-Refresh", value=(runner.status == "running"), key="chk_auto_refresh")

    # ==========================================
    # Per-Model Progress Meters & State Machine
    # ==========================================
    st.markdown(
        """
        <div style="margin:16px 0 8px 0; font-family:monospace; font-size:0.85rem; font-weight:bold; color:#cbd5e1;">
            TARGET MODEL EVALUATION STATUS
        </div>
        """,
        unsafe_allow_html=True,
    )

    active_model_ids = (
        getattr(runner, "run_plan", None).model_ids
        if getattr(runner, "run_plan", None)
        else runner.config.model_ids
    )

    model_prog_data = getattr(runner, "model_progress", {})
    model_states = getattr(runner, "model_run_states", {})
    cols_m = st.columns(max(1, len(active_model_ids)))

    for idx, m_id in enumerate(active_model_ids):
        m_state = model_states.get(m_id)
        p_info = model_prog_data.get(m_id, {"status": "pending", "done": 0, "total": 0})

        if m_state:
            st_val = m_state.status.value if hasattr(m_state.status, "value") else str(m_state.status)
            m_status = st_val.upper()
            m_done = m_state.probes_done
            m_total = m_state.total_probes or p_info.get("total", 0)
            m_timing = m_state.timing
        else:
            m_status = p_info.get("status", "QUEUED").upper()
            m_done = p_info.get("done", 0)
            m_total = p_info.get("total", 0)
            m_timing = None

        m_short = m_id.split("/")[-1]

        badge_color = {
            "COMPLETED": "#10b981",
            "RUNNING": "#0ea5e9",
            "LOADING": "#3b82f6",
            "QUEUED": "#64748b",
            "PENDING": "#64748b",
            "FAILED": "#ef4444",
        }.get(m_status, "#64748b")

        dur_text = f"{m_timing.total_duration_sec:.2f}s" if m_timing and m_timing.total_duration_sec > 0 else ""

        with cols_m[idx % len(cols_m)]:
            st.markdown(
                f"""
                <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:10px 12px; margin-bottom:6px; font-family:monospace;">
                    <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:4px;">
                        <strong style="color:#f1f5f9;">{m_short}</strong>
                        <span style="color:{badge_color}; font-weight:bold;">● {m_status}</span>
                    </div>
                    <div style="font-size:0.75rem; color:#94a3b8; display:flex; justify-content:space-between;">
                        <span>Probes: {m_done} / {m_total if m_total > 0 else '--'}</span>
                        <span style="color:#38bdf8;">{dur_text}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Interactive Progressive Inspection for Completed Models per Section 7
            if m_status == "COMPLETED":
                with st.expander(f"✓ Results: {m_short}", expanded=False):
                    m_result = runner.run_store.load_model_result(runner.experiment_id, m_id)
                    if m_result:
                        m_metrics = m_result.get("metrics", {})
                        m_baseline = m_result.get("baseline", {})
                        
                        # Display baseline
                        if m_baseline:
                            b_first = list(m_baseline.values())[0] if isinstance(m_baseline, dict) and m_baseline else None
                            if b_first and isinstance(b_first, dict):
                                b_pred = b_first.get("prediction", {})
                                b_lbl = b_pred.get("label", "N/A")
                                b_conf = b_pred.get("confidence", 0.0)
                                b_probs = b_pred.get("probabilities", {})
                                st.markdown(f"**Baseline Prediction:** `{b_lbl}` ({b_conf:.2%})")
                                if b_probs:
                                    prob_str = " | ".join(f"{k}: {v:.1%}" for k, v in b_probs.items())
                                    st.caption(f"Probabilities: {prob_str}")

                        st.markdown(
                            f"- **Flip Rate:** `{m_metrics.get('observed_flip_rate', 0.0):.1%}`\n"
                            f"- **Preserve Rate:** `{m_metrics.get('preserve_rate', 0.0):.1%}`\n"
                            f"- **Consistency:** `{m_metrics.get('behavioral_consistency', 0.0):.1%}`\n"
                            f"- **ECE:** `{m_metrics.get('ece', 0.0):.4f}`\n"
                            f"- **Failures:** `{len(m_result.get('taxonomy', []))}`"
                        )
                        m_rep = m_result.get("report_md")
                        if m_rep:
                            st.markdown("---")
                            st.markdown(m_rep)
                    else:
                        st.caption("Artifacts saved. Generating incremental summary...")

    # ==========================================
    # Event Logs Terminal Panel
    # ==========================================
    st.markdown(
        """
        <div style="margin:16px 0 6px 0; font-family:monospace; font-size:0.85rem; font-weight:bold; color:#cbd5e1; display:flex; justify-content:space-between; align-items:center;">
            <span>EXECUTION EVENT STREAM & BEHAVIORAL TELEMETRY</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    events = runner.events.get_history()

    tab_cards, tab_logs = st.tabs(["RESEARCH EVENT CARDS (DIAGNOSTIC)", "TERMINAL LOG STREAM"])

    with tab_cards:
        probe_events = [ev for ev in reversed(events) if ev.event_type == "probe_evaluated"]
        if not probe_events:
            st.caption("No probe evaluation telemetry recorded yet. Live evaluations will stream here...")
        else:
            for pev in probe_events[:20]:
                d = pev.data
                m_short = d.get("model_id", "").split("/")[-1]
                pid = d.get("probe_id", "")[:8]
                pcat = d.get("perturbation_type", "").upper()
                s_text = d.get("seed_text", "")
                p_text = d.get("perturbed_text", "")
                orig_lbl = d.get("original_label", "")
                orig_conf = d.get("original_confidence", 0.0)
                pert_lbl = d.get("perturbed_label", "")
                pert_conf = d.get("perturbed_confidence", 0.0)
                is_flip = "YES" if d.get("is_flipped") else "NO"
                exp_eff = d.get("expected_effect", "N/A")
                outcome = d.get("behavioral_outcome", "EVAL")
                ftype = d.get("failure_type", "None")
                delta_pts = d.get("confidence_delta_pts", 0.0)

                f_badge_color = {
                    "Blind": "#ef4444",
                    "Spurious": "#f59e0b",
                    "Misweighted": "#8b5cf6",
                    "Undetermined": "#64748b",
                    "None": "#10b981",
                }.get(ftype, "#10b981")

                st.markdown(
                    f"""
                    <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:10px 14px; margin-bottom:8px; font-family:monospace; font-size:0.75rem;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px; flex-wrap:wrap; gap:6px;">
                            <div style="display:flex; gap:6px; align-items:center;">
                                <span style="background:#1e293b; color:#38bdf8; font-weight:bold; padding:2px 6px; border-radius:3px;">MODEL: {m_short}</span>
                                <span style="background:#0f172a; color:#cbd5e1; padding:2px 6px; border-radius:3px;">PROBE: {pid}</span>
                                <span style="background:#0f172a; color:#a78bfa; padding:2px 6px; border-radius:3px;">CAT: {pcat}</span>
                            </div>
                            <div style="display:flex; gap:6px; align-items:center;">
                                <span style="background:#0f172a; color:#cbd5e1; padding:2px 6px; border-radius:3px;">OUTCOME: {outcome}</span>
                                <span style="background:{f_badge_color}22; color:{f_badge_color}; border:1px solid {f_badge_color}66; padding:2px 6px; border-radius:3px; font-weight:bold;">
                                    FAILURE: {ftype.upper()}
                                </span>
                            </div>
                        </div>
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; margin:6px 0; background:#0b0f19; padding:6px 8px; border-radius:4px;">
                            <div><strong style="color:#64748b;">Original:</strong> <span style="color:#cbd5e1;">"{s_text}"</span></div>
                            <div><strong style="color:#64748b;">Perturbed:</strong> <span style="color:#e2e8f0;">"{p_text}"</span></div>
                        </div>
                        <div style="display:flex; justify-content:space-between; color:#94a3b8; font-size:0.72rem; flex-wrap:wrap; gap:8px;">
                            <div>Baseline: <strong style="color:#38bdf8;">{orig_lbl}</strong> ({orig_conf:.2f})</div>
                            <div>Probe Output: <strong style="color:#38bdf8;">{pert_lbl}</strong> ({pert_conf:.2f})</div>
                            <div>Transition: <strong style="color:#f1f5f9;">{orig_lbl} → {pert_lbl}</strong></div>
                            <div>Δ Conf: <strong style="color:{'#10b981' if delta_pts >= 0 else '#f59e0b'};">{delta_pts:+.1f} pp</strong></div>
                            <div>Flip: <strong style="color:{'#f59e0b' if is_flip == 'YES' else '#94a3b8'};">{is_flip}</strong></div>
                            <div>Expected: <strong style="color:#cbd5e1;">{exp_eff}</strong></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with tab_logs:
        with st.container(height=320):
            if not events:
                st.caption("Waiting for execution telemetry events...")
            else:
                for ev in reversed(events[-50:]):
                    t_str = time.strftime("%H:%M:%S", time.localtime(ev.timestamp))
                    etype = ev.event_type
                    msg = ev.data.get("message", str(ev.data))
                    lvl = "INFO"
                    sub = "RUNNER"

                    if etype == "error":
                        lvl = "ERROR"
                    elif etype == "cancelled":
                        lvl = "WARNING"
                    elif etype == "completed":
                        lvl = "SUCCESS"
                    elif etype == "model_complete":
                        lvl = "SUCCESS"
                        sub = "MODEL"
                    elif etype == "model_start":
                        lvl = "INFO"
                        sub = "MODEL"
                    elif etype == "probe_evaluated":
                        lvl = "DEBUG"
                        sub = "PROBE"
                        m_id_short = ev.data.get("model_id", "").split("/")[-1]
                        p_id_short = ev.data.get("probe_id", "")[:8]
                        outcome = ev.data.get("behavioral_outcome", "EVAL")
                        delta_pts = ev.data.get("confidence_delta_pts", 0.0)
                        ftype = ev.data.get("failure_type", "None")
                        msg = f"[{m_id_short}] Probe {p_id_short} -> {outcome} ({delta_pts:+.1f} pp) | Failure: {ftype}"

                    render_console_log_line(timestamp_str=t_str, level=lvl, subsystem=sub, message=msg)

    # ==========================================
    # Post-Completion Action Gateway & Integrity Audit
    # ==========================================
    if runner.status == "completed":
        # Auto-load results into session if available
        if runner._result and "active_results" not in st.session_state:
            st.session_state["active_results"] = runner._result

        # Pipeline Count Integrity Audit Banner
        results = runner._result or {}
        integrity = results.get("pipeline_integrity", {})
        all_passed = integrity.get("all_passed", False)
        total_p = integrity.get("total_probes", 0)

        if all_passed:
            st.markdown(
                f"""
                <div style="background:#064e3b; border:1px solid #059669; border-radius:6px; padding:12px 16px; margin:16px 0; font-family:monospace;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <strong style="color:#ecfdf5; font-size:0.95rem;">✓ PIPELINE COUNT INTEGRITY VERIFIED</strong>
                            <div style="color:#a7f3d0; font-size:0.8rem; margin-top:2px;">
                                Planned ({total_p}) == Executed ({total_p}) == Analyzed ({total_p}) == Reported ({total_p}) across all {len(runner.config.model_ids)} models.
                            </div>
                        </div>
                        <span style="background:#059669; color:#ffffff; font-weight:bold; padding:2px 8px; border-radius:4px; font-size:0.75rem;">
                            CANONICAL AUDIT PASS
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="background:#451a03; border:1px solid #b45309; border-radius:6px; padding:12px 16px; margin:16px 0; font-family:monospace;">
                    <strong style="color:#fef3c7; font-size:0.95rem;">⚠️ PIPELINE INTEGRITY NOTICE</strong>
                    <div style="color:#fde68a; font-size:0.8rem; margin-top:2px;">
                        Discrepancies detected between planned and executed stimuli. Check audit details.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        col_act1, col_act2, col_act3, col_act4 = st.columns(4)
        with col_act1:
            if st.button("Model Comparison Matrix", key="live_to_comp", type="primary", use_container_width=True):
                st.session_state["active_results"] = runner._result
                st.session_state["current_page"] = "Comparison"
                st.rerun()
        with col_act2:
            if st.button("Failure Analysis Evidence", key="live_to_fail", use_container_width=True):
                st.session_state["active_results"] = runner._result
                st.session_state["current_page"] = "Failure Analysis"
                st.rerun()
        with col_act3:
            if st.button("Token Explainability Lab", key="live_to_xai", use_container_width=True):
                st.session_state["active_results"] = runner._result
                st.session_state["current_page"] = "Explainability"
                st.rerun()
        with col_act4:
            if st.button("View Diagnostic Reports", key="live_to_rep", use_container_width=True):
                st.session_state["active_results"] = runner._result
                st.session_state["current_page"] = "Reports"
                st.rerun()


    # Active auto-refresh loop (stable 3.5s refresh interval to eliminate blinking)
    if auto_refresh and runner.status == "running":
        time.sleep(3.5)
        st.rerun()
