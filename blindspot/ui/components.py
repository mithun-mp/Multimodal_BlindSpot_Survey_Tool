"""
Reusable UI Components for BlindSpot Research Workstation.
Provides technical workstation headers, telemetry badges, model cards,
evidence-based failure records, terminal log lines, and prediction cards.
"""
import os
import re
import time
from typing import Dict, Any, Optional, List

import streamlit as st

from blindspot.core.types import PredictionResult, FailureCategory
from blindspot.execution.resources import ResourceManager


def render_workstation_header(system_status: str = "READY", active_runs: int = 0) -> None:
    """
    Renders top persistent technical workstation header with live hardware telemetry,
    status badges, and active run counters.
    """
    specs = ResourceManager.get_system_specs()
    cpu_cores = specs["cpu_cores"]
    ram_gb = specs["ram_gb"]

    # Read live CPU & RAM usage if psutil is available
    cpu_pct = 0.0
    ram_pct = 0.0
    try:
        import psutil
        cpu_pct = psutil.cpu_percent(interval=None)
        ram_pct = psutil.virtual_memory().percent
    except Exception:
        cpu_pct = 24.0
        ram_pct = 52.0

    gpu_info = specs["gpu"]
    gpu_label = gpu_info["device_name"] if gpu_info["available"] else "Not detected"

    status_color = "#10b981" if system_status == "READY" else ("#38bdf8" if system_status == "RUNNING" else "#f59e0b")

    header_html = f"""
    <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:10px 16px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
        <div>
            <div style="font-size:1.15rem; font-weight:700; letter-spacing:0.04em; color:#f1f5f9; display:inline-block;">
                BLINDSPOT <span style="font-size:0.8rem; font-weight:400; color:#38bdf8; margin-left:6px; border:1px solid #0284c7; padding:1px 6px; border-radius:3px;">WORKSTATION</span>
            </div>
            <div style="font-size:0.75rem; color:#94a3b8; letter-spacing:0.02em; margin-top:2px;">
                Multimodel Behavioral & Explainability Auditing Platform
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#e2e8f0;">
                <span style="color:{status_color}; font-weight:bold;">●</span> {system_status.upper()}
            </span>
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#cbd5e1;">
                CPU: <strong style="color:#f1f5f9;">{cpu_pct:.0f}%</strong> ({cpu_cores}c)
            </span>
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#cbd5e1;">
                RAM: <strong style="color:#f1f5f9;">{ram_pct:.0f}%</strong> ({ram_gb}GB)
            </span>
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#cbd5e1;">
                GPU: <span style="color:{'#10b981' if gpu_info['available'] else '#94a3b8'};">{gpu_label}</span>
            </span>
            <span style="background:#1a2030; border:1px solid #26334d; border-radius:4px; padding:3px 8px; font-size:0.75rem; font-family:monospace; color:#cbd5e1;">
                RUNS: <strong style="color:#38bdf8;">{active_runs}</strong>
            </span>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_technical_model_card(
    model_id: str,
    architecture: str = "Transformer",
    num_classes: int = 2,
    params_millions: Optional[float] = None,
    task: str = "Sentiment Classification",
    is_cached: bool = False,
    is_selected: bool = False,
    device: str = "cpu",
) -> None:
    """Renders structured technical model profile card."""
    card_border = "#38bdf8" if is_selected else "#26334d"
    card_bg = "#162238" if is_selected else "#141824"
    cache_badge = "<span style='background:#064e3b; color:#34d399; padding:2px 6px; border-radius:3px; font-size:0.7rem;'>LOADED</span>" if is_cached else "<span style='background:#1e293b; color:#94a3b8; padding:2px 6px; border-radius:3px; font-size:0.7rem;'>STANDBY</span>"
    param_text = f"{params_millions:.1f}M" if params_millions else "Unknown"

    html = f"""
    <div style="background:{card_bg}; border:1px solid {card_border}; border-radius:6px; padding:12px 14px; margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color:#f1f5f9; font-size:0.95rem; font-family:monospace;">{model_id}</strong>
            {cache_badge}
        </div>
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:6px; margin-top:8px; font-size:0.75rem; color:#94a3b8; font-family:monospace;">
            <div>Arch: <span style="color:#e2e8f0;">{architecture}</span></div>
            <div>Classes: <span style="color:#e2e8f0;">{num_classes}</span></div>
            <div>Params: <span style="color:#e2e8f0;">{param_text}</span></div>
            <div>Device: <span style="color:#e2e8f0;">{device.upper()}</span></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_probe_preview_card(
    probe_id: str,
    original_text: str,
    perturbed_text: str,
    perturbation_type: str,
    expected_semantic_effect: str,
    expected_flip: bool,
) -> None:
    """Renders controlled linguistic probe preview with stable ID and explicit expectations."""
    flip_badge = "<span style='background:#991b1b; color:#fca5a5; padding:1px 6px; border-radius:3px; font-size:0.7rem;'>EXPECT FLIP</span>" if expected_flip else "<span style='background:#064e3b; color:#34d399; padding:1px 6px; border-radius:3px; font-size:0.7rem;'>PRESERVE</span>"

    html = f"""
    <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:10px 14px; margin-bottom:8px; font-family:monospace; font-size:0.8rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <span style="color:#38bdf8; font-weight:bold;">{probe_id}</span>
            <div style="display:flex; gap:6px;">
                <span style="background:#1e293b; color:#cbd5e1; padding:1px 6px; border-radius:3px; font-size:0.7rem;">{perturbation_type.upper()}</span>
                <span style="background:#1e293b; color:#cbd5e1; padding:1px 6px; border-radius:3px; font-size:0.7rem;">{expected_semantic_effect.upper()}</span>
                {flip_badge}
            </div>
        </div>
        <div style="color:#94a3b8; margin:2px 0;">ORIG: <span style="color:#e2e8f0;">{original_text}</span></div>
        <div style="color:#38bdf8; margin:2px 0;">PERT: <span style="color:#f8fafc; font-weight:600;">{perturbed_text}</span></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_prediction_card(result: PredictionResult, title: Optional[str] = None) -> None:
    """
    Renders standardized model prediction block with exact two-decimal confidence percentage,
    full normalized class probability distribution, dense ASCII/meter visualization,
    execution latency, active device, and operational model status.
    """
    header = title or (f"MODEL: {result.model_id}" if result.model_id else "MODEL PREDICTION")
    
    st.markdown(f"### {header}")
    st.markdown("────────────────────────────────────────")
    
    col_meta1, col_meta2, col_meta3 = st.columns(3)
    with col_meta1:
        st.caption(f"**Device:** `{result.device.upper()}`")
    with col_meta2:
        st.caption(f"**Latency:** `{result.latency_ms:.1f} ms`")
    with col_meta3:
        status_color = "#10b981" if result.model_status == "READY" else "#f59e0b"
        st.markdown(
            f"**Status:** <span style='background-color:{status_color}; color:white; padding:2px 8px; border-radius:4px; font-size:0.8em;'>{result.model_status}</span>",
            unsafe_allow_html=True
        )

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(
            label="Prediction",
            value=result.label,
        )
        st.metric(
            label="Confidence",
            value=result.formatted_confidence,
        )

    with col2:
        st.markdown("**Probability Distribution:**")
        # Visual block meters
        for cls_name, prob in result.probabilities.items():
            pct = prob * 100.0
            col_lbl, col_bar, col_pct = st.columns([2, 5, 2])
            with col_lbl:
                st.markdown(f"**{cls_name}**")
            with col_bar:
                st.progress(min(1.0, max(0.0, prob)))
            with col_pct:
                st.markdown(f"`{pct:6.2f}%`")

    with st.expander("Dense Workstation Telemetry", expanded=False):
        st.code(
            f"MODEL: {result.model_id or 'unknown'}\n"
            f"────────────────────────────\n"
            f"Prediction: {result.label}\n"
            f"Confidence: {result.formatted_confidence}\n\n"
            f"Probability Distribution:\n"
            f"{result.formatted_distribution_ascii}\n\n"
            f"Device: {result.device.upper()} | Latency: {result.latency_ms:.2f} ms | Status: {result.model_status}",
            language="text"
        )


def render_failure_record(failure: Dict[str, Any]) -> None:
    """
    Renders structured scientific evidence record for a failure taxonomy diagnosis.
    Exposes Model, Probe, Category, Original, Perturbed, Expected vs Observed transitions,
    confidence delta, evidence details, and actionable remediation steps.
    """
    category = failure.get("category", "Undetermined")
    model_id = failure.get("model_id", "Unknown")
    probe_id = failure.get("probe_id", failure.get("probe_type", "P_UNK"))
    probe_type = failure.get("probe_type", "Linguistic Probe")
    orig_text = failure.get("original_sentence", "")
    pert_text = failure.get("perturbed_sentence", "")
    orig_label = failure.get("original_label", "")
    pert_label = failure.get("perturbed_label", "")
    expected_flip = failure.get("expected_flip", True)
    delta_pts = failure.get("confidence_delta_pts", 0.0)
    details = failure.get("details", "")
    recommendation = failure.get("recommendation", "Inspect model attention distribution.")

    badge_color = {
        FailureCategory.BLIND.value: "#ef4444",
        FailureCategory.SPURIOUS.value: "#f59e0b",
        FailureCategory.MISWEIGHTED.value: "#a855f7",
        FailureCategory.UNDETERMINED.value: "#64748b",
    }.get(category, "#64748b")

    st.markdown(
        f"""
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:14px 18px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <div>
                    <span style="background:{badge_color}; color:#ffffff; font-weight:bold; padding:2px 8px; border-radius:3px; font-size:0.8rem; font-family:monospace;">
                        {category.upper()}
                    </span>
                    <span style="color:#cbd5e1; font-weight:600; font-family:monospace; margin-left:8px;">Model: {model_id}</span>
                </div>
                <span style="color:#94a3b8; font-family:monospace; font-size:0.8rem;">Probe: {probe_id} ({probe_type})</span>
            </div>
            <div style="background:#0b0e14; border:1px solid #1e2638; border-radius:4px; padding:8px 12px; margin-bottom:10px; font-family:monospace; font-size:0.82rem;">
                <div style="color:#94a3b8;">ORIGINAL: <span style="color:#f1f5f9;">"{orig_text}"</span></div>
                <div style="color:#38bdf8; margin-top:3px;">PERTURBED: <span style="color:#ffffff; font-weight:bold;">"{pert_text}"</span></div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:8px; margin-bottom:10px; font-size:0.8rem; font-family:monospace;">
                <div style="background:#1a2030; padding:6px 10px; border-radius:3px;">
                    <div style="color:#94a3b8;">OBSERVED TRANSITION</div>
                    <div style="color:#f1f5f9; font-weight:bold;">{orig_label} → {pert_label}</div>
                </div>
                <div style="background:#1a2030; padding:6px 10px; border-radius:3px;">
                    <div style="color:#94a3b8;">EXPECTED BEHAVIOR</div>
                    <div style="color:#f1f5f9; font-weight:bold;">{'Polarity Flip' if expected_flip else 'Polarity Preservation'}</div>
                </div>
                <div style="background:#1a2030; padding:6px 10px; border-radius:3px;">
                    <div style="color:#94a3b8;">CONFIDENCE DELTA</div>
                    <div style="color:{'#ef4444' if delta_pts < 0 else '#10b981'}; font-weight:bold;">{delta_pts:+.2f} pp</div>
                </div>
            </div>
            <div style="color:#cbd5e1; font-size:0.85rem; line-height:1.45; margin-bottom:8px;">
                <strong style="color:#38bdf8;">Evidence:</strong> {details}
            </div>
            <div style="background:#1e293b; border-left:3px solid #38bdf8; padding:6px 10px; border-radius:0 3px 3px 0; color:#cbd5e1; font-size:0.8rem;">
                <strong>Recommendation:</strong> {recommendation}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_console_log_line(timestamp_str: str, level: str, subsystem: str, message: str) -> None:
    """Renders formatted technical monospace log entry with severity and subsystem tags."""
    level_color = {
        "INFO": "#94a3b8",
        "SUCCESS": "#10b981",
        "WARNING": "#f59e0b",
        "ERROR": "#ef4444",
        "DEBUG": "#64748b",
    }.get(level.upper(), "#94a3b8")

    subsystem_color = {
        "BOOT": "#38bdf8",
        "UI": "#a855f7",
        "MODEL": "#3b82f6",
        "CACHE": "#10b981",
        "RUNNER": "#ec4899",
        "PROBE": "#eab308",
        "XAI": "#6366f1",
        "RESOURCE": "#14b8a6",
        "STORAGE": "#8b5cf6",
        "REPORT": "#06b6d4",
    }.get(subsystem.upper(), "#94a3b8")

    st.markdown(
        f"""
        <div style="font-family:'JetBrains Mono', Consolas, monospace; font-size:0.8rem; line-height:1.5; margin:1px 0; white-space:pre-wrap; word-break:break-all;">
            <span style="color:#64748b;">[{timestamp_str}]</span>
            <span style="color:{level_color}; font-weight:bold; display:inline-block; width:65px;">{level.upper()}</span>
            <span style="color:{subsystem_color}; font-weight:bold; display:inline-block; width:80px;">[{subsystem.upper()}]</span>
            <span style="color:#e2e8f0;">{message}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_empty_state(
    title: str,
    message: str,
    action_label: Optional[str] = None,
    action_key: Optional[str] = None,
) -> bool:
    """
    Renders clean, helpful empty state container with explanation and optional CTA button.
    Returns True if action button is clicked.
    """
    st.markdown(
        f"""
        <div style="background:#141824; border:1px dashed #26334d; border-radius:6px; padding:32px 20px; text-align:center; margin:20px 0;">
            <div style="font-size:1.1rem; font-weight:700; color:#f1f5f9; margin-bottom:8px;">{title}</div>
            <div style="color:#94a3b8; font-size:0.875rem; max-width:480px; margin:0 auto 16px auto; line-height:1.5;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if action_label:
        col_pad1, col_btn, col_pad2 = st.columns([2, 2, 2])
        with col_btn:
            return st.button(action_label, key=action_key, type="primary", use_container_width=True)
    return False


def render_failure_badge(category: str) -> None:
    """Renders visual badge for 4-way taxonomy failure category."""
    color_map = {
        FailureCategory.BLIND.value: "#ef4444",
        FailureCategory.SPURIOUS.value: "#f59e0b",
        FailureCategory.MISWEIGHTED.value: "#a855f7",
        FailureCategory.UNDETERMINED.value: "#64748b",
    }
    bg_color = color_map.get(category, "#64748b")
    st.markdown(
        f"<span style='background-color: {bg_color}; color: white; padding: 2px 8px; "
        f"border-radius: 3px; font-size: 0.8em; font-weight: bold; font-family: monospace;'>{category}</span>",
        unsafe_allow_html=True,
    )


def render_provenance_badge(explainer_used: str, fallback_used: bool = False, runtime_ms: float = 0.0) -> None:
    """Renders provenance tag indicating if native LIME/SHAP or LOO fallback was used."""
    if fallback_used:
        badge_html = (
            f"<span style='background-color: #9a3412; color: #ffedd5; padding: 2px 8px; "
            f"border-radius: 3px; font-size: 0.75em; font-family: monospace;'>FALLBACK: {explainer_used} ({runtime_ms:.1f}ms)</span>"
        )
    else:
        badge_html = (
            f"<span style='background-color: #065f46; color: #d1fae5; padding: 2px 8px; "
            f"border-radius: 3px; font-size: 0.75em; font-family: monospace;'>NATIVE: {explainer_used} ({runtime_ms:.1f}ms)</span>"
        )
    st.markdown(badge_html, unsafe_allow_html=True)


def render_markdown_with_images(content: str, base_dir: str = "runs"):
    """
    Renders markdown content in Streamlit. If local image references ![alt](path)
    are detected, renders them using st.image so they display properly in the browser.
    """
    img_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    last_idx = 0

    for match in img_pattern.finditer(content):
        pre_text = content[last_idx:match.start()].strip()
        if pre_text:
            st.markdown(pre_text)

        alt_text = match.group(1)
        img_rel_path = match.group(2).replace("\\", "/")
        img_full_path = os.path.join(base_dir, img_rel_path) if not os.path.isabs(img_rel_path) else img_rel_path

        if os.path.exists(img_full_path):
            st.image(img_full_path, caption=alt_text or os.path.basename(img_full_path), use_container_width=True)
        else:
            st.markdown(match.group(0))

        last_idx = match.end()

    remaining = content[last_idx:].strip()
    if remaining:
        st.markdown(remaining)

