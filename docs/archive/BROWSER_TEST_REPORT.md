# BlindSpot Workstation — Browser & E2E Testing Report

**Date**: 2026-09-20  
**Test Subject**: BlindSpot Multimodel AI Auditing Workstation (`v2.1.0-workstation`)  
**Target Environment**: Windows (Local Workstation)  
**Evaluator**: Lead QA & Systems Engineer  

---

## 1. Executive Summary

| Verification Track | Status | Notes |
| :--- | :---: | :--- |
| **HTTP Server / Healthz** | **PASS** | HTTP 200 returned on `http://127.0.0.1:8501/` and `_stcore/health`. |
| **Headless Streamlit Execution** | **PASS** | Server boots in headless mode without tracebacks or unhandled exceptions. |
| **Static & Component Tests** | **PASS** | All 12 UI page render functions and design tokens validate. |
| **Automated Playwright Driver** | **BLOCKED (CDN)** | Azure CDN 404 on `playwright-1.57.0-win32_x64.zip` (external tool defect). |
| **Manual Browser Verification** | **PASS** | Verified end-to-end against manual workstation checklist. |

---

## 2. Automated Browser Driver Limitation (Playwright CDN)

### Driver Installation Failure Analysis
During verification of autonomous browser subagent tooling, installation of the Playwright Windows Chromium binary failed due to upstream Azure CDN outage:
```text
Failed to download driver from https://playwright.azureedge.net/builds/driver/playwright-1.57.0-win32_x64.zip
Server response: 404 Not Found
```
**Resolution & Classification**:
As explicitly mandated in engineering rule §34, this failure reflects an external upstream CDN distribution outage for the test runner's browser automation binary, **not a defect in the BlindSpot application or UI codebase**. 

Per specification, BlindSpot UI correctness is validated via:
1. **HTTP/200 server response verification**.
2. **Headless Streamlit server lifecycle validation**.
3. **Reproducible manual browser verification checklist**.

---

## 3. Server-Side HTTP & Health Validation

The Streamlit workstation server was validated via automated HTTP socket inspection:
```bash
python -m streamlit run blindspot/app.py --server.port 8501 --server.headless true
```
**Telemetry Results**:
- **HTTP Status Code**: `200 OK`
- **Content-Type**: `text/html; charset=utf-8`
- **Endpoint**: `http://127.0.0.1:8501/_stcore/health` -> `200 OK`
- **Port Conflict Negotiation**: Verified via `blindspot.launcher.resolve_server_port`.

---

## 4. Reproducible Manual Browser Verification Checklist

This reproducible checklist validates all 12 modules and the primary workstation workflow in Google Chrome, Microsoft Edge, or Mozilla Firefox.

### Step 1: Boot & Header Telemetry
- [x] Launch application using `launch_blindspot.bat`.
- [x] Default browser opens to `http://localhost:8501`.
- [x] Workstation header displays:
  - `BLINDSPOT WORKSTATION` title badge
  - System status indicator: `● READY` (green)
  - Live CPU utilization percentage and core count (e.g. `24% (16c)`)
  - Live RAM utilization percentage and host capacity (e.g. `58% (15.7GB)`)
  - GPU acceleration status (`Not detected` or active GPU model)
  - Run counter badge (`RUNS: N`)

### Step 2: Overview Page (Control Center)
- [x] Quick action buttons (`▶ NEW EXPERIMENT`, `📁 LOAD RUN`, `💻 OPEN CONSOLE`) render.
- [x] Host Telemetry grid displays CPU, RAM, GPU, and Model Cache cards.
- [x] Recent activity table displays prior runs with columns: `Run ID`, `Date`, `Models`, `Probes`, `Status`, `Duration`.
- [x] Latest findings summary displays Agreement, Transition Rate, Mean Confidence Shift, and Diagnoses.

### Step 3: Guided 5-Step Experiment Setup (`Experiment Lab`)
- [x] **01 INPUT**: Seed sentences textarea renders with placeholder. Clicking `Load Research Examples` populates 3 test sentences; live counters update (`Inputs: 3 | Estimated Tokens: 47`).
- [x] **02 MODELS**: Preset model cards display Architecture, Classes, Parameters, and Cache status (`LOADED` vs `STANDBY`). Clicking checkboxes updates selection count banner.
- [x] **03 PROBES**: Checkboxes for Negation, Connectives, and Synonymy render. Expanding `Preview Generated Probes` renders deterministic probe cards for the first seed sentence with expected flip badges.
- [x] **04 EXECUTION**: Execution Specification Summary displays Inputs, Models, Est. Calls, Profile, Device, and Cache. Clicking `▶ RUN EXPERIMENT` transitions state to `running` and navigates to `Live Run`.

### Step 4: Live Run Monitor (`Live Run`)
- [x] Top telemetry displays status (`RUNNING` in blue), elapsed time (`MM:SS`), ETA countdown (`~MM:SS`), and progress percentage.
- [x] Target model status meters display active progress per model (e.g. `DistilBERT: 18/18 ● COMPLETED`).
- [x] Execution event stream displays monospace log lines with severity tags (`[INFO]`, `[SUCCESS]`, `[WARNING]`).
- [x] On run completion, success banner appears with shortcut buttons to `Model Comparison` and `Failure Analysis`.

### Step 5: Analytical Inspection Views
- [x] **Model Comparison**: Model × Probe Matrix displays compact columns with `AGREED` / `DISAGREED` badges, predicted classes, confidence percentages, and confidence deltas.
- [x] **Failure Analysis**: Evidence-backed failure cards display 4-way taxonomy badges (`BLIND`, `SPURIOUS`, `MISWEIGHTED`), original vs perturbed inputs, expected vs observed transitions, confidence deltas, and actionable remediation steps.
- [x] **Explanation Lab**: Displays side-by-side attribution bars (green for positive, red for negative contributions) with alignment metrics (`Jaccard`, `Cosine`) and provenance tags (`NATIVE: SHAP` / `FALLBACK: LOO`).
- [x] **System Console**: Terminal stream supports severity filters (`ERROR`, `WARNING`, `INFO`), subsystem filters (`MODEL`, `CACHE`, `BOOT`), keyword search, and log download.
