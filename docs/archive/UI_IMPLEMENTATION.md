# BlindSpot Workstation — Complete UI/UX Implementation Report

**Release**: BlindSpot Multimodel AI Auditing Workstation (`v2.1.0-workstation`)  
**Architecture**: Streamlit + Dark Technical Design System + Supervisor Process Launcher  
**Status**: Production Polish Complete  

---

## 1. Architectural Overview

BlindSpot has been transformed from a fragmented set of prototype pages into a coherent, high-density **local AI research workstation**.

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│ BLINDSPOT WORKSTATION                    ● SYSTEM READY   CPU 24%  RAM 58% GPU — │
├─────────────────┬────────────────────────────────────────────────────────────────┤
│ WORKSPACE       │                                                                │
│ ◉ Overview      │                   CENTRAL RESEARCH WORKSPACE                   │
│   Experiment    │                                                                │
│                 │   01 INPUT  ->  02 MODELS  ->  03 PROBES  ->  04 EXECUTION     │
│ INSPECT         │                                                                │
│   Models        │   [ Technical Model Cards with Cache Status: LOADED / STANDBY ]│
│   Probes        │                                                                │
│                 │   [ Deterministic SHA-256 Probes Preview with Invariance Tags ]│
│ RUN             │                                                                │
│   Live Run      │   [▶ RUN EXPERIMENT] (High visual dominance)                   │
│   Console       │                                                                │
│                 │   Live Elapsed & ETA Timers | Active Model Progress Meters     │
│ ANALYZE         │                                                                │
│   Comparison    │   Model x Probe Response Matrix with Agreement & Delta Flags   │
│   Explainability│                                                                │
│   Failures      │   Evidence Records with Observed vs Expected Behavioral Diffs  │
│                 │                                                                │
│ OUTPUT          │                                                                │
│   Reports       │                                                                │
│   Run History   │                                                                │
│                 │                                                                │
│ SYSTEM          │                                                                │
│   System Monitor│                                                                │
└─────────────────┴────────────────────────────────────────────────────────────────┘
```

---

## 2. Implemented Subsystems & Modules

### 2.1 Central Design System (`blindspot/ui/design_system.py`)
- **Visual Aesthetic**: Dark-first technical workstation palette (`#0b0e14` background, `#141824` surface, `#38bdf8` restrained cyan accent).
- **Slim Custom Scrollbars**: 6px Webkit scrollbars with hover states.
- **Monospace Telemetry**: JetBrains Mono / Consolas styling for probe IDs, token metrics, and memory addresses.
- **Button Hierarchy**: Primary action buttons highlighted with vibrant cyan-blue, secondary actions styled in subtle borders without neon clutter.

### 2.2 Application Shell & Telemetry Header (`blindspot/ui/shell.py`)
- **Persistent Header**: Mounts at the top of every screen rendering live host hardware telemetry (CPU%, core count, host RAM%, GPU acceleration state, and total persisted runs).
- **Grouped Sidebar Navigation**: Organizes 12 workstation modules into 6 logical domains:
  - `WORKSPACE`: Overview, Experiment
  - `INSPECT`: Models, Probes
  - `RUN`: Live Run, Console
  - `ANALYZE`: Comparison, Explainability, Failure Analysis
  - `OUTPUT`: Reports, Run History
  - `SYSTEM`: System Monitor
- **Active Session Context**: Displays active experiment ID badge and Debug Telemetry toggle in the sidebar footer.

### 2.3 Research Control Center (`blindspot/ui/overview.py`)
- **Action Triggers**: Immediate one-click access to `[▶ NEW EXPERIMENT]`, `[📁 LOAD RUN]`, and `[💻 OPEN CONSOLE]`.
- **Host Hardware Telemetry Grid**: 4 technical cards detailing CPU, RAM, GPU, and Model Cache occupancy (`LOADED` vs `STANDBY`).
- **Recent Activity Table**: Reads persistent experiment runs from `runs/`, displaying Run ID, Date, Model count, Probes, Status, and Duration.
- **Latest Findings Dashboard**: Computes cross-model concordance, probe flip rates, mean confidence shifts, and failure taxonomy counts.

### 2.4 Guided 5-Step Experiment Workflow (`blindspot/ui/experiment_lab.py`)
Replaces multi-page bouncing with a single coherent screen structured in 5 research steps:
- **01 INPUT**: Seed sentences textarea with live sentence, token, and character counters. Provides `[ Load Research Examples ]` and `[ Clear Input ]` actions.
- **02 MODELS**: Technical cards for each preset model displaying Architecture, Classes, Parameters, Device, and real-time Cache status (`LOADED` in green vs `STANDBY` in gray). Supports selecting presets and registering custom HuggingFace models.
- **03 PROBES**: Grouped checkboxes across Negation, Connectives, and Synonymy. Displays deterministic protocol badge (`Deterministic SHA-256 | Shared across all models | Seed: 42`) and an interactive **Live Probe Preview** table.
- **04 EXECUTION**: Comprehensive execution specification summary (Inputs, Models, Expected calls, Performance mode, Device, Memory Cache). Prominent `▶ RUN EXPERIMENT` button that transitions to `■ CANCEL RUN` during active execution.
- **05 REVIEW**: Workstation jump gates to `Live Run`, `Console`, `Comparison`, and `Run History`.

### 2.5 Real-Time Execution Monitor (`blindspot/ui/live_run.py`)
- **Temporal Telemetry**: Live elapsed time counter (`MM:SS`) and dynamic ETA calculation (`~MM:SS`).
- **Model Progress Meters**: Displays granular progress for each target model (e.g. `DistilBERT: 18/18 ● COMPLETED`).
- **Terminal Event Stream**: Monospace event viewer with severity tags (`[INFO]`, `[SUCCESS]`, `[WARNING]`, `[ERROR]`) and auto-refresh loop.
- **Result Transition Gateway**: Immediate one-click shortcuts to `Model Comparison`, `Failure Analysis`, and `Explainability` once the job completes.

### 2.6 System Console & Engineering Terminal (`blindspot/ui/console.py`)
- Monospace terminal log viewer with real-time log ingestion from both application boot and experiment runners.
- Live filtering by severity level (`INFO`, `SUCCESS`, `WARNING`, `ERROR`, `DEBUG`).
- Live filtering by subsystem (`BOOT`, `UI`, `MODEL`, `CACHE`, `RUNNER`, `PROBE`, `XAI`, `RESOURCE`, `STORAGE`, `REPORT`).
- Substring search and one-click log file download.

### 2.7 Model × Probe Comparison Matrix (`blindspot/ui/comparison.py`)
- High-density matrix displaying each shared probe stimulus evaluated across all target models.
- Compact columns for probe ID, perturbation category, expected flip, model predictions + confidence percentages, concordance flag (`AGREED` / `DISAGREED`), and confidence delta.
- Pairwise cross-model concordance matrix and quantitative behavioral fingerprints.

### 2.8 Scientific Failure Analysis (`blindspot/ui/failure_lab.py`)
- Structured evidence cards for each failure record exposing Model, Probe, Category (`BLIND`, `SPURIOUS`, `MISWEIGHTED`), Original vs Perturbed inputs, Observed vs Expected behavioral transitions, Confidence Deltas in percentage points, and actionable engineering remediation steps.

### 2.9 Token-Level Explainability & Provenance (`blindspot/ui/explanation_lab.py`)
- Side-by-side attribution bars for original vs perturbed inputs with signed weights (green for positive contribution, red for negative).
- Quantitative attribution alignment metrics (`Jaccard Similarity`, `Cosine Alignment`).
- Transparent provenance badges (`NATIVE: SHAP`, `NATIVE: LIME`, `FALLBACK: LOO`).

### 2.10 Persistent Run History (`blindspot/ui/run_history.py`)
- Research archive table with dates, model counts, probe counts, durations, and statuses.
- Run inspector with one-click reloading of historical runs into active session memory.
- Downloadable Markdown summary reports.

---

## 3. Windows Launchers & Supervisor (`blindspot/launcher.py`)
- **`launch_blindspot.bat`**: Double-clickable batch launcher for Windows.
- **`launch_blindspot.ps1`**: PowerShell equivalent with error handling.
- **`create_blindspot_shortcut.ps1`**: Generates a desktop shortcut pointing to the launcher without requiring administrator privileges.
- **Smart Port Negotiation**: Automatically detects if port 8501 is occupied. If an active BlindSpot instance is already running, attaches to it and opens the browser; otherwise finds the next available port (`8502`, `8503`...).
- **Graceful Shutdown**: Catches Ctrl+C in terminal to stop background worker threads and clear PyTorch/cache memory without zombie processes.
