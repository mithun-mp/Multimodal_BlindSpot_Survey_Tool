# BlindSpot — UI/UX Technical Design Specification

**Document**: `UI_UX_DESIGN.md`  
**Target Release**: BlindSpot 2.1 (Research Workstation Edition)  
**Design Philosophy**: Serious Technical Workstation, High Information Density, Zero Gimmicks.

---

## 1. Visual Language & Tone

BlindSpot is designed as a **local scientific supercomputing workstation for AI behavioral audits**, drawing inspiration from developer observability platforms, Bloomberg terminals, and IDE telemetry consoles.

### Core Aesthetic Principles:
1. **Dark-First Technical Workstation**: Engineered for prolonged deep-work auditing sessions. Low-glare dark surfaces with crisp, high-contrast typography.
2. **High Information Density**: Eliminate giant whitespace and bloated marketing hero sections. Maximize visible data per square inch while retaining clean visual hierarchy and padding.
3. **Restrained Color Semantics**: Color is never decorative; color strictly communicates operational state and statistical significance:
   - **Neutral Dark Background**: `#0b0e14`
   - **Card / Surface Background**: `#141824`
   - **Elevated Surface**: `#1c2233`
   - **Hairline Borders**: `#262f45`
   - **Primary Text**: `#f1f5f9` (Slate 100)
   - **Secondary / Muted Text**: `#94a3b8` (Slate 400)
   - **Workstation Accent**: `#38bdf8` (Cyan/Sky 400)
   - **Success State**: `#10b981` (Emerald 500)
   - **Warning State**: `#f59e0b` (Amber 500)
   - **Error / Failure State**: `#ef4444` (Rose 500)
   - **Subsystem / Tag Colors**: Slate, Indigo, Purple, Teal.
4. **Universal Typography**: Clean sans-serif (`Inter`, system sans-serif) for labels and headers; high-clarity monospace (`Consolas`, `JetBrains Mono`, `Menlo`, monospace) for probe IDs, tokens, attributions, probability meters, and console logs.
5. **No Decorative Fluff**: No random emojis in headers, no oversized SaaS landing banners, no gratuitous animations that delay user interaction.

---

## 2. Application Shell Architecture

The workstation interface operates inside a unified, responsive application shell:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│ BLINDSPOT                         ● SYSTEM READY   CPU 18%  RAM 46%  GPU —  RUNS 4│
│ Multimodel Behavioral Workstation                                                │
├─────────────────┬────────────────────────────────────────────────────────────────┤
│                 │                                                                │
│ WORKSPACE       │  [ HEADER BAR: BREADCRUMBS & CONTEXT ACTIONS ]                 │
│ ◉ Overview      │                                                                │
│   Experiment    │  [ WORKSPACE CONTENT VIEW ]                                    │
│                 │  - Dense information hierarchy                                 │
│ INSPECT         │  - Technical metric cards                                      │
│   Models        │  - Responsive grid layouts                                     │
│   Probes        │  - Non-blocking asynchronous interaction                       │
│                 │                                                                │
│ RUN             │                                                                │
│   Live Run      │                                                                │
│   Console       │                                                                │
│                 │                                                                │
│ ANALYZE         │                                                                │
│   Comparison    │                                                                │
│   Explainability│                                                                │
│   Failures      │                                                                │
│                 │                                                                │
│ OUTPUT          │                                                                │
│   Reports       │                                                                │
│   Run History   │                                                                │
│                 │                                                                │
│ SYSTEM          │                                                                │
│   System Monitor│                                                                │
│                 │                                                                │
│ v2.1.0-prod     │                                                                │
└─────────────────┴────────────────────────────────────────────────────────────────┘
```

### Persistent Telemetry Header
Located prominently at the top of the main container:
- **Application Identifier**: `BLINDSPOT` with technical subtitle `Multimodel Behavioral Audit Workstation`.
- **System Readiness Indicator**: Pulsing status badge (`● READY`, `● RUNNING`, `● CACHED`).
- **Live Host Telemetry**: Real-time CPU utilization %, Host RAM utilization %, active GPU status (`GPU: Not detected` or GPU device name), and total persisted runs counter.

### Grouped Workspace Navigation
Categorized into functional engineering domains:
1. **WORKSPACE**:
   - `Overview`: Operations control center, quick actions, host specs, recent activity table, latest audit findings.
   - `Experiment`: Unified 5-step guided research workflow (`01 INPUT` → `02 MODELS` → `03 PROBES` → `04 EXECUTION` → `05 REVIEW`).
2. **INSPECT**:
   - `Models`: Verified model catalog, parameters, class distribution inspector.
   - `Probes`: Linguistic perturbation engine inspector and live probe generator with deterministic SHA-256 hashes.
3. **RUN**:
   - `Live Run`: Real-time execution monitor with per-model progress bars, current operation details, and streaming event logs.
   - `Console`: Dedicated subsystem terminal log console with level/subsystem filtering, auto-scroll, copy, and clear.
4. **ANALYZE**:
   - `Comparison`: Descriptive Model × Probe matrix, pairwise agreement heatmap, and multi-dimensional behavioral fingerprints.
   - `Explainability`: Side-by-side feature attribution bars, token shift diffs, and explainer provenance tags.
   - `Failure Analysis`: Structured scientific evidence records for `Blind`, `Spurious`, `Misweighted`, and `Undetermined` categories.
5. **OUTPUT**:
   - `Reports`: Comprehensive Markdown and tabular reports with one-click export.
   - `Run History`: Chronological audit archive with run reloader and multi-run comparison.
6. **SYSTEM**:
   - `System Monitor`: Host CPU cores, RAM allocation, memory reserve threshold, model cache controls, and performance mode inspector.

---

## 3. Reusable Workstation Components

| Component | Visual Specification | Purpose |
| :--- | :--- | :--- |
| `render_workstation_header` | Dark technical banner with telemetry badges and system status | Gives instant observability of host resources and active experiments. |
| `render_technical_model_card` | Dark border card with status badge, architecture, class count, parameters, cache state, and selection toggle | Selectable model card in Experiment and Model Lab. |
| `render_probe_preview_card` | Monospace code container displaying Probe ID, Original, Perturbed, Expected Effect, and Category | Visualizes exact linguistic probe stimuli before execution. |
| `render_prediction_card` | High-density card with class name, confidence %, safe ASCII meter, latency, active device, and status | Standardized prediction format across all model evaluations. |
| `render_failure_record` | Structured scientific evidence card with Original vs Perturbed text, observed vs expected transitions, confidence delta, evidence summary, and remedies | Replaces unguided failure text with actionable audit records. |
| `render_console_log_line` | Monospace terminal line with timestamp, colored severity badge, subsystem tag, and message | Renders log entries in Console and Live Run. |
| `render_empty_state` | Informational container with explanation and primary action button | Eliminates blank pages on fresh sessions. |

---

## 4. Responsive & Accessibility Standards

- **Screen Resolution**: Guaranteed baseline support for 1366×768 (standard laptop display) up to 3840×2160 (4K monitors).
- **No Horizontal Scroll**: All tables, matrices, and code containers wrap or use internal scroll containers (`use_container_width=True`).
- **Contrast Ratios**: Text contrast strictly conforms to WCAG 2.1 AA standards (minimum 4.5:1 for normal text, 7:1 for headers).
- **Non-Color Dependence**: Every colored status badge pairs color with explicit text labels (`READY`, `FAILED`, `CANCELLED`, `FLIPPED`).
