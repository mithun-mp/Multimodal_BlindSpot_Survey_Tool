"""
Application Shell and Navigation Orchestrator for BlindSpot Workstation.
Features a compact top navigation bar with secondary domain tabs,
minimized sidebar for contextual utilities, persistent telemetry,
and robust session-state routing.
"""
import streamlit as st
from typing import Dict, Callable, Any, List

from blindspot.ui.design_system import inject_workstation_theme
from blindspot.ui.components import render_workstation_header
from blindspot.storage.run_store import RunStore


PRIMARY_DOMAINS = [
    ("Overview", "Overview", "📊"),
    ("Probes", "Probes", "🔬"),
    ("Experiment", "Experiment", "⚙️"),
    ("Run", "Live Run", "⚡"),
    ("Analyze", "Comparison", "📈"),
    ("Reports", "Reports", "📑"),
]

DOMAIN_SUBPAGES = {
    "Overview": ["Overview"],
    "Probes": ["Probes"],
    "Experiment": ["Experiment"],
    "Run": ["Live Run", "Run Details"],
    "Analyze": ["Comparison", "Explainability", "Failure Analysis"],
    "Reports": ["Reports", "Run History", "Models"],
}

PAGE_TO_DOMAIN = {
    "Overview": "Overview",
    "Probes": "Probes",
    "Experiment": "Experiment",
    "Live Run": "Run",
    "Run Details": "Run",
    "Events": "Run",
    "Console": "Run",
    "Comparison": "Analyze",
    "Explainability": "Analyze",
    "Failure Analysis": "Analyze",
    "Reports": "Reports",
    "Run History": "Reports",
    "Models": "Reports",
}


def render_shell(page_registry: Dict[str, Callable[[], None]]) -> None:
    """
    Renders the unified workstation shell:
    1. Injects workstation CSS theme.
    2. Renders persistent technical telemetry header.
    3. Renders horizontal top navigation bar with domain subtabs.
    4. Renders compact sidebar for session context and quick utilities.
    5. Routes to active page component.
    """
    inject_workstation_theme()

    # Determine system status & active runs
    runner = st.session_state.get("active_runner")
    if runner and runner.status == "running":
        system_status = "RUNNING"
    elif runner and runner.status == "completed":
        system_status = "COMPLETED"
    else:
        system_status = "READY"

    # Count persisted runs
    store = RunStore()
    persisted_runs = len(store.list_runs())

    # Persistent Top Telemetry Header
    render_workstation_header(system_status=system_status, active_runs=persisted_runs)

    # Initialize current page in session state if missing or invalidated
    if "current_page" not in st.session_state or st.session_state["current_page"] in ["System", "System Monitor", "Monitor", "Console", "Settings"]:
        st.session_state["current_page"] = "Overview"

    current_page = st.session_state["current_page"]
    current_domain = PAGE_TO_DOMAIN.get(current_page, "Overview")

    # ==========================================
    # COMPACT TOP NAVIGATION BAR
    # ==========================================
    nav_cols = st.columns(len(PRIMARY_DOMAINS))
    for idx, (dom_name, default_target, icon) in enumerate(PRIMARY_DOMAINS):
        is_active_dom = (dom_name == current_domain)
        with nav_cols[idx]:
            btn_label = f"{icon} {dom_name}"
            btn_type = "primary" if is_active_dom else "secondary"
            if st.button(btn_label, key=f"topnav_{dom_name}", type=btn_type, use_container_width=True):
                # When clicking domain, if already in domain stay on current subpage, else default
                if current_domain != dom_name:
                    st.session_state["current_page"] = default_target
                    st.rerun()

    # Secondary Domain Subtabs (for domains with multiple modules)
    subpages = DOMAIN_SUBPAGES.get(current_domain, [current_page])
    if len(subpages) > 1:
        st.markdown("<div style='margin-top:4px; margin-bottom:12px;'>", unsafe_allow_html=True)
        sub_cols = st.columns(len(subpages) + 2)
        for s_idx, sp in enumerate(subpages):
            is_active_sub = (sp == current_page)
            with sub_cols[s_idx]:
                sub_label = f"● {sp}" if is_active_sub else sp
                sub_type = "primary" if is_active_sub else "secondary"
                if st.button(sub_label, key=f"subnav_{sp}", type=sub_type, use_container_width=True):
                    st.session_state["current_page"] = sp
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================
    # MINIMIZED UTILITIES SIDEBAR
    # ==========================================
    with st.sidebar:
        st.markdown(
            """
            <div style="padding:4px 0 12px 0; border-bottom:1px solid #1e2638; margin-bottom:12px;">
                <div style="font-size:1.05rem; font-weight:bold; letter-spacing:0.04em; color:#f1f5f9;">
                    ⚡ BLINDSPOT
                </div>
                <div style="font-size:0.72rem; color:#94a3b8; letter-spacing:0.02em;">
                    v2.5.0 • Canonical Protocol
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("**SESSION CONTEXT**")
        active_exp_id = st.session_state.get("active_experiment_id", "None")
        active_title = st.session_state.get("active_experiment_title")
        if not active_title and active_exp_id and active_exp_id != "None":
            try:
                active_title = store.get_run_title(active_exp_id)
            except Exception:
                active_title = active_exp_id

        if active_exp_id and active_exp_id != "None":
            display_title = active_title or active_exp_id
            st.markdown(
                f"""
                <div style="background:#141824; border:1px solid #26334d; border-radius:4px; padding:8px 10px; margin-bottom:10px; font-family:monospace; font-size:0.75rem;">
                    <div style="color:#64748b; font-size:0.7rem;">Active Experiment:</div>
                    <div style="color:#38bdf8; font-weight:bold; word-break:break-word; font-size:0.82rem; margin-top:2px;">{display_title}</div>
                    <div style="color:#64748b; font-size:0.68rem; margin-top:4px; border-top:1px dashed #1e293b; padding-top:4px;">ID: <span style="color:#94a3b8;">{active_exp_id}</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="background:#141824; border:1px solid #26334d; border-radius:4px; padding:6px 10px; margin-bottom:10px; font-family:monospace; font-size:0.75rem;">
                    <div style="color:#64748b;">Active Experiment:</div>
                    <div style="color:#94a3b8; font-style:italic;">None</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.caption("**STAGED PROBE SET**")
        staged_probes = st.session_state.get("staged_probe_set")
        if staged_probes:
            num_staged = len(staged_probes.probes) if hasattr(staged_probes, "probes") else len(staged_probes.get("probes", []))
            st.markdown(
                f"""
                <div style="background:#0b2518; border:1px solid #10b981; border-radius:4px; padding:6px 10px; margin-bottom:12px; font-family:monospace; font-size:0.75rem;">
                    <div style="color:#10b981; font-weight:bold;">✓ {num_staged} Probes Staged</div>
                    <div style="color:#6ee7b7; font-size:0.7rem;">Verified Catalog Active</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Clear Staged Probes", key="btn_clear_staged_sidebar", use_container_width=True):
                del st.session_state["staged_probe_set"]
                st.rerun()
        else:
            st.markdown(
                """
                <div style="background:#141824; border:1px solid #26334d; border-radius:4px; padding:6px 10px; margin-bottom:12px; font-family:monospace; font-size:0.72rem; color:#94a3b8;">
                    No staged catalog.<br>Probes generated on launch.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.caption("**QUICK LAUNCHERS**")
        if st.button("🔬 Probe Workbench", key="side_quick_probes", use_container_width=True):
            st.session_state["current_page"] = "Probes"
            st.rerun()
        if st.button("+ New Experiment", key="side_quick_exp", use_container_width=True):
            st.session_state["current_page"] = "Experiment"
            st.rerun()
        if st.button("📈 Model Comparison", key="side_quick_comp", use_container_width=True):
            st.session_state["current_page"] = "Comparison"
            st.rerun()

        st.divider()
        st.caption("**MONITORING**")
        debug_mode = st.toggle("Debug Telemetry", value=st.session_state.get("debug_mode", False), key="toggle_debug_mode")
        st.session_state["debug_mode"] = debug_mode

    # Route and render active page
    active_page_name = st.session_state.get("current_page", "Overview")
    render_fn = page_registry.get(active_page_name, page_registry.get("Overview"))
    if render_fn:
        render_fn()
    else:
        st.error(f"Navigation module '{active_page_name}' could not be resolved.")
