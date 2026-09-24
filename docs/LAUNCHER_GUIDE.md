# BlindSpot Workstation — Launcher & Startup Guide

This document describes the one-click startup architecture, port management, desktop shortcut setup, and graceful shutdown lifecycle for the BlindSpot Multimodel AI Auditing Workstation.

---

## 1. Quick Start (One-Click Launch)

### Option A: Windows Batch Launcher (`launch_blindspot.bat`)
Simply **double-click** `launch_blindspot.bat` from Windows File Explorer.
No terminal typing or manual virtualenv activation is required.

### Option B: PowerShell Launcher (`launch_blindspot.ps1`)
Right-click `launch_blindspot.ps1` and select **Run with PowerShell**, or execute from your terminal:
```powershell
.\launch_blindspot.ps1
```

### Option C: Python Direct Launch
```bash
python -m blindspot.launcher
```

---

## 2. Boot Lifecycle & Terminal Diagnostics

When launched, the terminal displays live subsystem boot diagnostics:

```text
========================================================
                 BLINDSPOT WORKSTATION                  
========================================================

[BOOT] Checking Python.................... OK (3.13.14)
[BOOT] Checking dependencies.............. OK
[BOOT] Initializing model registry........ OK (4 presets indexed)
[BOOT] Resolving port availability........ OK (Port 8501)
[BOOT] Starting Streamlit server.......... OK
[BOOT] Waiting for server response........ OK

--------------------------------------------------------
 BLINDSPOT IS READY                                     
--------------------------------------------------------
 Local URL : http://localhost:8501
 Browser   : Opening automatically...
 Logs      : This terminal will remain open.
             Press Ctrl+C to gracefully stop BlindSpot.
========================================================
```

The launcher will automatically open your default browser directly to the active workstation session.

---

## 3. Smart Port Management & Collision Handling

The launcher never crashes when port `8501` is occupied:

1. **Existing BlindSpot Detection**: If port `8501` is responding to a health check from an active BlindSpot/Streamlit instance, the launcher detects it, avoids spawning a duplicate background server, and re-opens your browser to the active session immediately.
2. **Dynamic Port Increment**: If port `8501` is occupied by another local service (e.g. an external dev server or database), the supervisor scans consecutive ports (`8502`, `8503`, `8504`...) until an open port is located.
3. **Exact Browser Routing**: The browser is opened to the exact port negotiated by the supervisor.

---

## 4. Desktop Shortcut Creation

To create a convenient desktop shortcut without needing administrator privileges:

1. Open PowerShell in the project directory.
2. Execute:
```powershell
powershell -ExecutionPolicy Bypass -File .\create_blindspot_shortcut.ps1
```
3. A shortcut titled **BlindSpot Workstation.lnk** will appear on your desktop. Double-clicking it directly launches `launch_blindspot.bat`.

---

## 5. Graceful Shutdown

To shut down the workstation:
- Return to the terminal window and press `Ctrl+C`.
- The supervisor will catch the interrupt and execute a clean shutdown:
```text
[SHUTDOWN] Cancellation requested by user (Ctrl+C)
[SHUTDOWN] Stopping experiment workers.... OK
[SHUTDOWN] Closing model cache resources.. OK
[SHUTDOWN] Stopping Streamlit server...... OK
[SHUTDOWN] Complete. Goodbye.
```
This ensures background worker threads terminate cleanly and model GPU/RAM memory is cleared without leaving zombie Python processes.
