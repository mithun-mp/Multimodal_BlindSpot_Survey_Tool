"""
System Monitor: Real-Time Host Hardware & Cache Utilization Dashboard.
"""
import streamlit as st
from blindspot.execution.resources import ResourceManager
from blindspot.models.cache import ModelCache


def render_system_monitor():
    st.title("System Monitor: Hardware & Memory Dashboard")
    st.markdown("Inspect host hardware capabilities, VRAM allocation, and model cache utilization.")

    specs = ResourceManager.get_system_specs()
    cache = ModelCache.get_shared_cache()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CPU Cores", specs["cpu_cores"])
    with col2:
        st.metric("Host RAM", f"{specs['ram_gb']} GB")
    with col3:
        gpu_info = specs["gpu"]
        if gpu_info["available"]:
            st.metric("GPU Device", gpu_info["device_name"])
            st.caption(f"VRAM: {gpu_info['vram_gb']} GB")
        else:
            st.metric("GPU", "Not detected")

    st.markdown("---")
    st.subheader("In-Memory Model Cache")
    st.write(f"**Cached Models**: `{cache.size()}` / `{cache._max_size}`")

    cached_ids = cache.cached_model_ids()
    if cached_ids:
        for cid in cached_ids:
            st.write(f"- `{cid}`")
    else:
        st.caption("No models currently retained in memory cache.")

    if st.button("Clear Model Cache"):
        cache.clear()
        st.success("Model cache flushed and PyTorch memory reclaimed.")
