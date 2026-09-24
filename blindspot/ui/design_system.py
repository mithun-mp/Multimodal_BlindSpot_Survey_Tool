"""
BlindSpot Technical Design System & Styling Tokens.
Provides dark-first workstation theme injection, cohesive color tokens,
typography rules, and responsive CSS for Streamlit.
"""
import streamlit as st
from typing import Dict, Any


THEME_COLORS = {
    "bg_dark": "#0b0e14",
    "surface_1": "#141824",
    "surface_2": "#1a2030",
    "surface_3": "#232b40",
    "border_subtle": "#1e2638",
    "border_card": "#26334d",
    "border_focus": "#38bdf8",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "accent": "#38bdf8",
    "accent_hover": "#0ea5e9",
    "accent_active": "#0284c7",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
    "purple": "#a855f7",
    "teal": "#14b8a6",
}


WORKSTATION_CSS = """
<style>
/* Root CSS Variables */
:root {
    --bs-bg-dark: #0b0e14;
    --bs-surface-1: #141824;
    --bs-surface-2: #1a2030;
    --bs-surface-3: #232b40;
    --bs-border: #26334d;
    --bs-border-subtle: #1e2638;
    --bs-text-primary: #f1f5f9;
    --bs-text-secondary: #94a3b8;
    --bs-accent: #38bdf8;
    --bs-success: #10b981;
    --bs-warning: #f59e0b;
    --bs-error: #ef4444;
}

@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* Global Container & Typography Adjustments */
html, body, button, input, select, textarea {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: var(--bs-text-primary);
}

/* Material Symbols & Streamlit Icon Typography Guard:
   Prevents ligature stripping (e.g. arrow_right, keyboard_double, dark_mode, contrast) */
[data-testid*="stIcon"],
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined,
.material-icons,
[class*="material-symbols"],
[class*="material-icons"],
.stIcon,
span[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-feature-settings: 'liga' 1 !important;
    -webkit-font-feature-settings: 'liga' 1 !important;
    text-rendering: optimizeLegibility !important;
    -webkit-font-smoothing: antialiased !important;
    display: inline-block !important;
    line-height: 1 !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    word-wrap: normal !important;
    white-space: nowrap !important;
    direction: ltr !important;
}

/* Slim Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0b0e14;
}
::-webkit-scrollbar-thumb {
    background: #232b40;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #38bdf8;
}

/* Technical Monospace Elements */
code, pre, .stCode, .terminal-text {
    font-family: "JetBrains Mono", "Cascadia Code", "Fira Code", Consolas, "Courier New", monospace !important;
}

/* Workstation Header Styles */
.workstation-header {
    background: #141824;
    border: 1px solid #26334d;
    border-radius: 6px;
    padding: 12px 18px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.workstation-header-title {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: #f1f5f9;
    margin: 0;
}

.workstation-header-sub {
    font-size: 0.8rem;
    color: #94a3b8;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

.telemetry-badge {
    display: inline-flex;
    align-items: center;
    background: #1a2030;
    border: 1px solid #26334d;
    border-radius: 4px;
    padding: 3px 8px;
    font-size: 0.75rem;
    font-family: monospace;
    color: #e2e8f0;
    margin-left: 6px;
}

/* Technical Metric Cards */
.tech-card {
    background: #141824;
    border: 1px solid #26334d;
    border-radius: 6px;
    padding: 14px 16px;
    margin-bottom: 12px;
}

.tech-card:hover {
    border-color: #38bdf8;
}

.tech-card-selected {
    background: #162238;
    border: 1px solid #38bdf8 !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);
}

.tech-badge {
    padding: 2px 7px;
    border-radius: 3px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: monospace;
    display: inline-block;
}

/* Workstation Terminal Logs Box */
.terminal-window {
    background-color: #080b10;
    border: 1px solid #1e2638;
    border-radius: 4px;
    padding: 10px 12px;
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 0.82rem;
    line-height: 1.45;
    color: #cbd5e1;
    overflow-y: auto;
    max-height: 480px;
}

.terminal-line {
    margin: 2px 0;
    white-space: pre-wrap;
    word-break: break-all;
}

/* Remove giant top margin from main block */
.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 96% !important;
}

/* Primary Workstation Buttons */
.stButton > button[kind="primary"] {
    background-color: #0284c7 !important;
    border-color: #0284c7 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
    letter-spacing: 0.03em !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: #0369a1 !important;
    border-color: #0369a1 !important;
}

.stButton > button[kind="secondary"] {
    background-color: #141824 !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
    border-radius: 4px !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
}

/* Input fields & Selectboxes */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #141824 !important;
    border-color: #26334d !important;
    color: #f1f5f9 !important;
    border-radius: 4px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 1px #38bdf8 !important;
}

/* Compact Top Navigation Bar */
.top-nav-bar {
    display: flex;
    gap: 6px;
    background: #141824;
    border: 1px solid #26334d;
    border-radius: 6px;
    padding: 6px 10px;
    margin-bottom: 16px;
    align-items: center;
    overflow-x: auto;
}

.top-subnav-bar {
    display: flex;
    gap: 8px;
    background: #0f131d;
    border: 1px solid #1e2638;
    border-radius: 4px;
    padding: 4px 10px;
    margin-bottom: 14px;
    align-items: center;
}
</style>

"""


def inject_workstation_theme():
    """Injects workstation dark CSS tokens into Streamlit document."""
    st.markdown(WORKSTATION_CSS, unsafe_allow_html=True)
