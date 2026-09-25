"""
System Monitor: Real-Time Host Hardware & Cache Utilization Dashboard.
Streams actual CPU, RAM, Network I/O, and Model Cache sensors in a single unified row
with zero mock data and universal compatibility across all host configurations.
"""
import streamlit as st
from blindspot.execution.resources import ResourceManager
from blindspot.models.cache import ModelCache


def render_system_monitor():
    st.markdown(
        """
        <div style="margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:1.35rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                    SYSTEM TELEMETRY & HARDWARE MONITOR
                </div>
                <div style="color:#94a3b8; font-size:0.85rem;">
                    Live physical processor sensors, host memory allocation, network transfer, and resident model cache.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Fetch fresh live telemetry
    telemetry = ResourceManager.get_live_telemetry()
    cpu = telemetry["cpu"]
    ram = telemetry["ram"]
    net = telemetry["network"]
    cache = ModelCache.get_shared_cache()

    col_btn_ref, _ = st.columns([2, 8])
    with col_btn_ref:
        if st.button("🔄 Refresh Telemetry", type="primary", use_container_width=True, key="btn_refresh_sys_mon"):
            st.rerun()

    st.markdown("")

    # ==========================================
    # UNIFIED SINGLE-ROW HARDWARE TELEMETRY GRID
    # ==========================================
    net_down = f"{net['speed_down_kbps']:.0f} KB/s" if net['speed_down_kbps'] < 1024 else f"{net['speed_down_kbps']/1024:.1f} MB/s"
    net_up = f"{net['speed_up_kbps']:.0f} KB/s" if net['speed_up_kbps'] < 1024 else f"{net['speed_up_kbps']/1024:.1f} MB/s"

    cached_ids = cache.cached_model_ids()
    cache_len = len(cached_ids)

    col_c1, col_c2, col_c3, col_c4 = st.columns(4)

    # 1. CPU Monitor
    with col_c1:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:16px; font-family:monospace; min-height:190px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#38bdf8; font-size:0.85rem;">🖥 CPU PROCESSOR</strong>
                    <span style="color:#10b981; font-size:0.75rem; font-weight:bold;">● ONLINE</span>
                </div>
                <div style="color:#f1f5f9; font-size:1.5rem; font-weight:bold; margin-top:8px;">
                    {cpu['percent']:.1f}% <span style="font-size:0.75rem; color:#94a3b8; font-weight:normal;">load</span>
                </div>
                <div style="color:#cbd5e1; font-size:0.75rem; margin-top:4px; font-weight:600;">
                    {cpu['physical_cores']} Physical / {cpu['logical_cores']} Logical Cores
                </div>
                <div style="color:#94a3b8; font-size:0.72rem; margin-top:4px;">
                    Current Clock: <strong style="color:#f1f5f9;">{cpu['frequency_ghz']:.2f} GHz</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(1.0, max(0.0, cpu['percent'] / 100.0)))

    # 2. RAM Monitor
    with col_c2:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:16px; font-family:monospace; min-height:190px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#10b981; font-size:0.85rem;">🧠 HOST MEMORY (RAM)</strong>
                    <span style="color:#38bdf8; font-size:0.75rem; font-weight:bold;">● ALLOCATED</span>
                </div>
                <div style="color:#f1f5f9; font-size:1.5rem; font-weight:bold; margin-top:8px;">
                    {ram['percent']:.1f}% <span style="font-size:0.75rem; color:#94a3b8; font-weight:normal;">utilization</span>
                </div>
                <div style="color:#cbd5e1; font-size:0.75rem; margin-top:4px; font-weight:600;">
                    {ram['used_gb']:.1f} GB In Use
                </div>
                <div style="color:#94a3b8; font-size:0.72rem; margin-top:4px;">
                    Available Headroom: <strong style="color:#10b981;">{ram['free_gb']:.1f} GB</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(1.0, max(0.0, ram['percent'] / 100.0)))

    # 3. Network Monitor
    with col_c3:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:16px; font-family:monospace; min-height:190px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#a855f7; font-size:0.85rem;">🌐 NETWORK I/O</strong>
                    <span style="color:#10b981; font-size:0.75rem; font-weight:bold;">● ACTIVE</span>
                </div>
                <div style="display:flex; gap:16px; margin-top:8px;">
                    <div>
                        <div style="color:#94a3b8; font-size:0.7rem;">DOWN</div>
                        <div style="color:#38bdf8; font-size:1.25rem; font-weight:bold;">↓ {net_down}</div>
                    </div>
                    <div>
                        <div style="color:#94a3b8; font-size:0.7rem;">UP</div>
                        <div style="color:#a855f7; font-size:1.25rem; font-weight:bold;">↑ {net_up}</div>
                    </div>
                </div>
                <div style="color:#cbd5e1; font-size:0.75rem; margin-top:8px;">
                    In: <strong style="color:#f1f5f9;">{net['total_recv_mb']:.1f} MB</strong> | Out: <strong style="color:#f1f5f9;">{net['total_sent_mb']:.1f} MB</strong>
                </div>
                <div style="color:#64748b; font-size:0.72rem; margin-top:4px;">
                    Host Network Traffic Counters
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(1.0)

    # 4. Resident Model Cache
    with col_c4:
        st.markdown(
            f"""
            <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:16px; font-family:monospace; min-height:190px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#f59e0b; font-size:0.85rem;">📦 MODEL CACHE (LRU)</strong>
                    <span style="color:#10b981; font-size:0.75rem; font-weight:bold;">● READY</span>
                </div>
                <div style="color:#f1f5f9; font-size:1.5rem; font-weight:bold; margin-top:8px;">
                    {cache_len} / {cache._max_size} <span style="font-size:0.75rem; color:#94a3b8; font-weight:normal;">slot(s)</span>
                </div>
                <div style="color:#cbd5e1; font-size:0.75rem; margin-top:4px; font-weight:600;">
                    Zero-Disk Latency Model Serving
                </div>
                <div style="color:#94a3b8; font-size:0.72rem; margin-top:4px;">
                    Hot models: <strong style="color:#f59e0b;">{cache_len} resident</strong> in RAM
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(1.0, max(0.0, cache_len / max(1, cache._max_size))))

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    # Per-core breakdown expander
    if cpu.get("per_core"):
        with st.expander("🖥 Inspect Per-Core Processor Load Breakdown", expanded=False):
            per_core = cpu["per_core"]
            cols = st.columns(4)
            for idx, c_val in enumerate(per_core):
                with cols[idx % 4]:
                    st.caption(f"Core #{idx}: **{c_val:.1f}%**")
                    st.progress(min(1.0, max(0.0, c_val / 100.0)))

    # Cache models inspector expander
    with st.expander("📦 Inspect Hot Models in Memory & Cache Controls", expanded=(cache_len > 0)):
        if cached_ids:
            for cid in cached_ids:
                st.markdown(
                    f"""
                    <div style="background:#0d111a; border-left:3px solid #38bdf8; padding:8px 12px; margin-bottom:6px; font-family:monospace; font-size:0.85rem; color:#f1f5f9;">
                        ✓ <strong>{cid}</strong> &nbsp; <span style="color:#10b981; font-size:0.75rem;">HOT IN-MEMORY</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No models currently resident in RAM. Models load on demand when starting an audit.")

        st.markdown("")
        col_flush, _ = st.columns([3, 7])
        with col_flush:
            if st.button("🗑 Flush Resident Model Cache", type="secondary", use_container_width=True, key="btn_flush_model_cache"):
                cache.clear()
                st.success("Model cache flushed and host memory reclaimed.")
                st.rerun()
