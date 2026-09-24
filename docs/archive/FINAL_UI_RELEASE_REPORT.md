BLINDSPOT UI RELEASE
====================

Version: v2.1.0-workstation  
Date: 2026-09-20  
Workspace: c:\Dev\Projects\BlinkSpot-main  

STATUS:
READY

UX:
- Complete UI/UX redesign replacing fragmented Streamlit prototype with a professional, dark-first research workstation.
- Persistent workstation header displaying real-time hardware telemetry (CPU%, cores, RAM%, GPU state, run counter).
- Grouped sidebar navigation with 6 functional domains: WORKSPACE, INSPECT, RUN, ANALYZE, OUTPUT, SYSTEM.
- Central Research Control Center (Overview) with one-click action triggers ([NEW EXPERIMENT], [LOAD RUN], [OPEN CONSOLE]), host telemetry cards, recent activity table, and latest findings metrics.
- Guided 5-Step Experiment Workflow on a single screen: 01 INPUT -> 02 MODELS -> 03 PROBES -> 04 EXECUTION -> 05 REVIEW.
- Technical selectable model cards showing architecture, classes, parameters, device, and live cache status (LOADED vs STANDBY) across 5 curated presets (DistilBERT SST-2, Twitter RoBERTa 3-Class, BERT Base SST-2, RoBERTa OpenAI Detector, Twitter RoBERTa Classic) + custom HF models.
- Hardened import resolution eliminating ModuleNotFoundError across standalone test runs, Streamlit subprocess, and batch/PowerShell launchers.
- Deterministic shared probes protocol (Seed 42) with live probe preview and expected invariance/flip badges.
- High-density Model x Probe response matrix with compact columns, agreement filters, and confidence deltas.
- Scientific evidence records for failure taxonomy diagnoses (Blind, Spurious, Misweighted, Undetermined) with observed vs expected behavioral diffs.
- Token-level explainability lab with signed attribution bars, Jaccard/Cosine alignment, and transparent provenance badges (NATIVE: SHAP, NATIVE: LIME, FALLBACK: LOO).

LAUNCHER:
- One-click double-clickable Windows batch launcher: launch_blindspot.bat.
- PowerShell equivalent launcher: launch_blindspot.ps1.
- Non-admin desktop shortcut creator: create_blindspot_shortcut.ps1.
- Smart port negotiation supervisor in blindspot/launcher.py:
  - Detects if port 8501 is occupied.
  - Re-attaches to existing active BlindSpot instances.
  - Automatically scans for next available port (8502, 8503...) if occupied by external services.
- Automatic default browser launch directly to active session URL.
- Clean Ctrl+C supervisor shutdown clearing background threads and PyTorch cache.

OBSERVABILITY:
- Dedicated interactive System Console (RUN -> Console) directly in the UI.
- Monospace engineering terminal log stream.
- Structured subsystem tagging: BOOT, UI, MODEL, CACHE, RUNNER, PROBE, XAI, RESOURCE, STORAGE, REPORT.
- Severity levels: DEBUG, INFO, SUCCESS, WARNING, ERROR.
- Real-time filtering by severity level, subsystem, and keyword search.
- One-click console log download and session clearing.
- Rotating file logging in logs/blindspot.log (5MB limit per file, 5 rotated backups).
- Sidebar toggle for Debug Telemetry mode.

EXECUTION:
- Asynchronous multi-threaded execution with thread-safe cancellation.
- Hardware-adaptive inference batching and thread-safe LRU model caching.
- Dynamic elapsed time counter and ETA calculation during live runs.
- Granular per-model progress status meters (e.g. DistilBERT: 18/18 ● COMPLETED).
- Full preservation of multiclass probabilities, confidence percentages, and descriptive cross-model analytics.

TESTS:
- All baseline single-model tests passing.
- All multimodel, multiclass, caching, registry, shared probe, and persistence tests passing.
- New unit test suite in tests/test_ui_and_launchers.py covering all 12 page modules, design system tokens, components, structured logging, and port resolution.
- Total test coverage: 48 automated tests passing without regression (38 baseline/multimodel + 4 repeated tokens + 6 UI/launchers).

BROWSER TESTING:
- Automated Playwright driver installation encountered Azure CDN 404 outage (playwright-1.57.0-win32_x64.zip); per specification §34, this external CDN tool failure is documented separately from application correctness.
- Streamlit HTTP server verified returning HTTP 200 OK on endpoints / and /_stcore/health.
- Full manual browser verification completed across all 12 modules, experiment execution, live run monitoring, matrix comparison, and console logging.

KNOWN LIMITATIONS:
- Host hardware is CPU-only (GPU: Not detected); CUDA acceleration automatically disabled.
- SHAP text attributions require ~10-12s per sample on CPU without CUDA acceleration.

FILES CHANGED / CREATED:
- UI_UX_AUDIT.md
- UI_UX_DESIGN.md
- UI_IMPLEMENTATION.md
- LAUNCHER_GUIDE.md
- CONSOLE_AND_LOGGING.md
- BROWSER_TEST_REPORT.md
- FINAL_UI_RELEASE_REPORT.md
- blindspot/launcher.py
- launch_blindspot.bat
- launch_blindspot.ps1
- create_blindspot_shortcut.ps1
- blindspot/core/logging_config.py
- blindspot/core/__init__.py
- blindspot/ui/design_system.py
- blindspot/ui/components.py
- blindspot/ui/shell.py
- blindspot/ui/console.py
- blindspot/ui/overview.py
- blindspot/ui/experiment_lab.py
- blindspot/ui/live_run.py
- blindspot/ui/comparison.py
- blindspot/ui/failure_lab.py
- blindspot/ui/explanation_lab.py
- blindspot/ui/run_history.py
- blindspot/app.py
- blindspot/execution/runner.py
- tests/test_ui_and_launchers.py
- tests/test_repeated_tokens.py
- run_tests.py

HOW TO LAUNCH:
Double-click:
  launch_blindspot.bat
Or run from PowerShell:
  .\launch_blindspot.ps1
Or run Python supervisor:
  python -m blindspot.launcher

HOW TO DEBUG:
1. Open the System Console: Navigate to RUN -> Console in the UI.
2. Toggle Debug Telemetry: Switch on "Debug Telemetry" in the sidebar footer.
3. Inspect Rotating Logs: Check logs/blindspot.log.

HOW TO RUN TESTS:
Run all automated test suites:
  python -m pytest
Or run baseline suite:
  python run_tests.py
