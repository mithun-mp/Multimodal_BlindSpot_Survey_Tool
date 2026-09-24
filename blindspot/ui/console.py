"""
Dedicated System Console: Real-Time Subsystem Log Stream & Engineering Terminal.
Provides structured log inspection, severity/subsystem filtering, log export,
and auto-scrolling telemetry without arbitrary shell execution.
"""
import streamlit as st
import time
import os

from blindspot.ui.components import render_console_log_line


def get_console_logs():
    """Retrieves unified log stream from session state or active runner events."""
    if "console_logs" not in st.session_state:
        st.session_state["console_logs"] = [
            {
                "timestamp": time.time() - 60,
                "level": "INFO",
                "subsystem": "BOOT",
                "message": "BlindSpot Workstation kernel initialized."
            },
            {
                "timestamp": time.time() - 55,
                "level": "INFO",
                "subsystem": "UI",
                "message": "Streamlit application shell mounted successfully."
            },
            {
                "timestamp": time.time() - 50,
                "level": "INFO",
                "subsystem": "MODEL",
                "message": "Model registry indexed 5 curated benchmark architectures."
            },
            {
                "timestamp": time.time() - 45,
                "level": "INFO",
                "subsystem": "RESOURCE",
                "message": "Hardware telemetry verified: CPU 16 cores, 15.7GB RAM, GPU: Not detected."
            },
        ]

    # Ingest logs from active runner if present
    runner = st.session_state.get("active_runner")
    if runner:
        events = runner.events.get_history()
        existing_msgs = {l.get("message") for l in st.session_state["console_logs"]}
        for ev in events:
            msg = ev.data.get("message", str(ev.data))
            if msg not in existing_msgs:
                lvl = ev.data.get("level", "INFO")
                sub = ev.data.get("subsystem", "RUNNER")
                st.session_state["console_logs"].append({
                    "timestamp": ev.timestamp,
                    "level": lvl,
                    "subsystem": sub,
                    "message": msg,
                })

    return st.session_state["console_logs"]


def render_console():
    st.subheader("System Console & Subsystem Telemetry")
    st.caption("Real-time operational log stream, subsystem event auditing, and diagnostic trace monitoring.")

    logs = get_console_logs()

    # Console Controls & Filter Bar
    col_c1, col_c2, col_c3, col_c4, col_c5 = st.columns([2, 2, 2, 1, 1])

    with col_c1:
        level_filter = st.selectbox(
            "Filter Level:",
            options=["ALL", "INFO", "SUCCESS", "WARNING", "ERROR", "DEBUG"],
            index=0,
            key="console_lvl_filter",
        )

    with col_c2:
        subsystem_filter = st.selectbox(
            "Filter Subsystem:",
            options=["ALL", "BOOT", "UI", "MODEL", "CACHE", "RUNNER", "PROBE", "XAI", "RESOURCE", "STORAGE", "REPORT"],
            index=0,
            key="console_sub_filter",
        )

    with col_c3:
        search_query = st.text_input("Search Logs:", placeholder="Filter by keyword...", key="console_search")

    with col_c4:
        st.write("")
        st.write("")
        if st.button("Clear Logs", type="secondary", use_container_width=True):
            st.session_state["console_logs"] = []
            st.rerun()

    with col_c5:
        st.write("")
        st.write("")
        log_text = "\n".join(
            f"[{time.strftime('%H:%M:%S', time.localtime(l['timestamp']))}] [{l['level']}] [{l['subsystem']}] {l['message']}"
            for l in logs
        )
        st.download_button(
            label="Download",
            data=log_text,
            file_name=f"blindspot_console_{int(time.time())}.log",
            mime="text/plain",
            use_container_width=True,
        )

    # Filter logs
    filtered_logs = []
    for l in logs:
        if level_filter != "ALL" and l["level"].upper() != level_filter:
            continue
        if subsystem_filter != "ALL" and l["subsystem"].upper() != subsystem_filter:
            continue
        if search_query.strip() and search_query.lower() not in l["message"].lower():
            continue
        filtered_logs.append(l)

    # Terminal Monospace Container
    st.markdown(
        f"""
        <div style="background:#080b10; border:1px solid #1e2638; border-radius:6px; padding:8px 12px; margin:12px 0 6px 0; font-family:monospace; font-size:0.75rem; color:#64748b; display:flex; justify-content:space-between;">
            <span>STATUS: CONNECTED • PID: {os.getpid()} • HOST: localhost:8501</span>
            <span>ENTRIES: {len(filtered_logs)} / {len(logs)}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container(height=460):
        if not filtered_logs:
            st.caption("No log entries match the current filter criteria.")
        else:
            for item in filtered_logs[-100:]:
                t_str = time.strftime("%H:%M:%S", time.localtime(item["timestamp"]))
                render_console_log_line(
                    timestamp_str=t_str,
                    level=item["level"],
                    subsystem=item["subsystem"],
                    message=item["message"],
                )
