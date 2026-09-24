# BlindSpot — Comprehensive UI/UX Audit

**Date**: 2026-09-20  
**Auditor**: Lead Product & UX Systems Architect  
**Workspace**: `c:\Dev\Projects\BlinkSpot-main`  
**Current State**: Technically functional prototype after multimodel restructuring and production hardening.

---

## 1. Current State Description

The existing BlindSpot user interface is built on Streamlit (`streamlit==1.63.0`) and provides 11 modular views rendered via a sidebar selectbox inside `blindspot/app.py`, alongside a legacy "Single-Model Audit (Classic)" radio mode.

While the underlying analytical and execution engines are functionally complete and verified across 38 tests, the current user experience exhibits significant UX fragmentation, visual noise, and workflow disjointedness:
- **Visual Aesthetic**: Generic Streamlit dashboard look, inconsistent typography, ad-hoc emoji headers, excessive vertical scrolling, and lack of visual density suitable for a high-performance research workstation.
- **Workflow Fragmentation**: The primary user journey (creating an experiment) is fractured across multiple distinct screens (`Experiment Lab`, `Model Lab`, `Probe Lab`). The user has to click through separate pages to understand models and probe definitions before running an experiment.
- **Observability Gap**: Execution logs are confined to a basic container in `Live Run` with no dedicated system console, no subsystem tagging, no search/filtering, and no persistent rotating file logging.
- **Startup Complexity**: Requires manual terminal commands (`streamlit run blindspot/app.py`). No one-click Windows launcher, no intelligent port collision handling, and no automatic browser launch.
- **State Resilience**: Streamlit reruns cause momentary loss of context, repeated model metadata lookups, and unguided empty states when experiments have not yet been executed.

---

## 2. Granular UX/UI Problem Matrix

| ID | Issue Description | Severity | Affected Workflow | Recommended Solution | Priority |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **UX-01** | **Monolithic Navigation & Flat Page List**: 11 equally weighted pages presented in a flat dropdown without logical categorization creates cognitive overload. | High | Global Navigation | Implement an application shell with grouped navigation: `WORKSPACE`, `INSPECT`, `RUN`, `ANALYZE`, `OUTPUT`, `SYSTEM`. | **P0** |
| **UX-02** | **Fragmented Experiment Setup**: Configuring models, inspecting probes, and running an experiment requires bouncing between 3 separate tabs. | High | Experiment Creation | Build a unified guided 5-step experiment workflow on a single coherent screen: `01 INPUT` → `02 MODELS` → `03 PROBES` → `04 EXECUTION` → `05 REVIEW`. | **P0** |
| **UX-03** | **No One-Click Launcher**: Users must open PowerShell/CMD and type CLI arguments. Port 8501 collisions are unhandled. | High | Application Boot & Launch | Create `launch_blindspot.bat`, `launch_blindspot.ps1`, and `create_blindspot_shortcut.ps1` with port auto-detection, ANSI boot logs, and auto-browser launch. | **P0** |
| **UX-04** | **Lack of Central Design System**: Inline styles, inconsistent colors, generic buttons, and emoji-heavy headers dilute the professional research feel. | High | Visual Experience | Create a centralized technical design system (`blindspot/ui/design_system.py`) featuring dark-first technical palettes, restrained cyan/blue accents, and consistent typography. | **P0** |
| **UX-05** | **Absence of Dedicated Console**: Logs are only partially displayed in `Live Run` and cannot be paused, searched, or filtered by subsystem. | Medium | Observability & Debugging | Build a dedicated `System Console` page (`RUN → Console`) with real-time log streaming, subsystem tags (`BOOT`, `UI`, `MODEL`, etc.), and rotating file logging in `logs/`. | **P1** |
| **UX-06** | **Overview Page is Static Documentation**: The current overview is a static text explanation rather than a research control center. | Medium | First-Time & Returning UX | Redesign Overview as a technical command center: quick-action triggers (`[NEW EXPERIMENT]`, `[LOAD RUN]`), hardware telemetry cards, recent activity table, and latest findings. | **P1** |
| **UX-07** | **Passive Failure Analysis Cards**: Diagnoses are rendered as plain text strings without structured evidence records. | Medium | Diagnostic Analysis | Redesign failure diagnoses as formal scientific evidence records exposing original vs perturbed text, confidence deltas, observed vs expected transitions, and remediation steps. | **P1** |
| **UX-08** | **Raw Attributions Without Comparative Provenance**: Feature attributions display raw tables rather than side-by-side comparative bars and clear provenance tags. | Medium | Explainability Workflow | Redesign Explanation Lab with comparative bar charts, token rankings, and clear provenance indicators (`Native: SHAP`, `Native: LIME`, `Fallback: LOO`). | **P1** |
| **UX-09** | **Blank / Unguided Empty States**: Navigating to Comparison, Failures, or Reports before running an experiment displays generic warnings. | Low | Onboarding | Implement actionable empty states with guidance and direct shortcuts to launch the first audit. | **P2** |
| **UX-10** | **Legacy Code Sprawl in `app.py`**: Over 580 lines of legacy single-model dashboard code remain inside `app.py`, complicating maintenance. | Medium | Architecture & Code Quality | Modularize `app.py` to route strictly through the design system and application shell while preserving 100% single-model API compatibility. | **P1** |

---

## 3. Detailed Workflow Breakdowns

### Workflow A: Application Startup
- *Current*: User opens terminal, types `python -m streamlit run blindspot/app.py`, copies URL, opens browser manually. If port 8501 is in use, server crashes or silently moves ports without telling browser.
- *Target*: Double-click `launch_blindspot.bat`. Terminal displays ANSI boot diagnostics, verifies environment, checks port availability, starts server, automatically opens default browser to active port, and handles clean Ctrl+C shutdown.

### Workflow B: Running an Audit
- *Current*: User views Overview, clicks Experiment Lab, types sentences, selects presets in multiselect, clicks button, switches to Live Run tab, waits for logs to trickle.
- *Target*: User enters `01 INPUT` (text or examples with live token counters), clicks technical model cards in `02 MODELS` with instant cache status badges, verifies deterministic probe preview in `03 PROBES`, reviews resource allocation in `04 EXECUTION`, and clicks prominent `▶ RUN EXPERIMENT` with live inline execution transition.

### Workflow C: Inspecting Findings
- *Current*: User navigates between Model Comparison, Explanation Lab, and Failure Analysis, manually reconciling disparate probe IDs.
- *Target*: Structured Model × Probe matrix with instant agreement indicators, expandable evidence cards for each failure category, and side-by-side token attribution shifts.

---

## 4. Implementation Priorities & Phasing

1. **PHASE 12 — UI/UX AUDIT**: Deliver baseline findings document (`UI_UX_AUDIT.md`).
2. **PHASE 13 — DESIGN SYSTEM**: Build technical styling tokens, CSS injection, and reusable components (`design_system.py`, `components.py`, `UI_UX_DESIGN.md`).
3. **PHASE 14 — APPLICATION SHELL**: Implement persistent header (system status, CPU%, RAM%, GPU state, active runs) and grouped sidebar navigation (`shell.py`, `app.py`).
4. **PHASE 15 — EXPERIMENT WORKFLOW**: Construct unified 5-step guided experiment screen.
5. **PHASE 16 — LIVE RUN + CONSOLE**: Real-time progress monitor and dedicated subsystem terminal log console.
6. **PHASE 17 — RESULTS EXPERIENCE**: Redesign Overview control center, Model Comparison matrix, Failure evidence records, and Run History archive.
7. **PHASE 18 — LAUNCHER & SHORTCUT**: Build Windows `.bat`, `.ps1`, shortcut script, and port conflict resolution (`launch_blindspot.bat`, `launch_blindspot.ps1`, `create_blindspot_shortcut.ps1`).
8. **PHASE 19 — LOGGING & OBSERVABILITY**: Structured subsystem logging with rotating file handlers in `logs/` (`logging_config.py`).
9. **PHASE 20 — BROWSER / E2E QA**: Full verification, HTTP server validation, and regression test execution.
10. **PHASE 21 — FINAL RELEASE**: Complete release documentation (`FINAL_UI_RELEASE_REPORT.md`).
