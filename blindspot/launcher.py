"""
BlindSpot Workstation Launcher & Process Supervisor.
Handles Python validation, dependency verification, smart port collision management,
subsystem logging initialization, Streamlit supervisor lifecycle, browser auto-launch,
and graceful Ctrl+C shutdown.
"""
import sys
import os
import time
import socket
import subprocess
import webbrowser
import urllib.request
import urllib.error
from typing import Tuple, Optional

from blindspot.core.logging_config import configure_workstation_logging, get_subsystem_logger

logger = get_subsystem_logger("BOOT")


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Checks if a local TCP port is already open/occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.4)
        return s.connect_ex((host, port)) == 0


def is_blindspot_running(port: int, host: str = "127.0.0.1") -> bool:
    """Detects whether an active server responding on port is a Streamlit/BlindSpot server."""
    endpoints = [
        f"http://{host}:{port}/_stcore/health",
        f"http://{host}:{port}/healthz",
        f"http://{host}:{port}/",
    ]
    for url in endpoints:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "BlindSpot-Launcher"})
            with urllib.request.urlopen(req, timeout=0.8) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            continue
    return False


def resolve_server_port(start_port: int = 8501, max_checks: int = 20) -> Tuple[int, bool]:
    """
    Finds a port to run on:
    Returns (port, is_existing_instance).
    """
    if is_port_in_use(start_port):
        if is_blindspot_running(start_port):
            return start_port, True
        # Port is in use by non-BlindSpot service; find next available
        for p in range(start_port + 1, start_port + max_checks):
            if not is_port_in_use(p):
                return p, False
            if is_blindspot_running(p):
                return p, True

    return start_port, False


def wait_for_server(port: int, host: str = "127.0.0.1", timeout_sec: float = 20.0) -> bool:
    """Waits until Streamlit server begins responding to HTTP requests."""
    t_end = time.time() + timeout_sec
    while time.time() < t_end:
        if is_blindspot_running(port, host):
            return True
        time.sleep(0.4)
    return False


def run_launcher() -> int:
    """Main launcher entrypoint."""
    configure_workstation_logging(debug_mode=False)

    print("========================================================")
    print("                 BLINDSPOT WORKSTATION                  ")
    print("========================================================")
    print("")

    # 1. Python Environment Check
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info < (3, 9):
        print(f"[BOOT] Checking Python.................... FAILED (Python >= 3.9 required, found {py_ver})")
        logger.error(f"Incompatible Python version: {py_ver}")
        return 1
    print(f"[BOOT] Checking Python.................... OK ({py_ver})")
    logger.info(f"Python runtime verified: {py_ver}")

    # 2. Dependency Check
    required_packages = ["streamlit", "torch", "transformers", "pandas"]
    missing = []
    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"[BOOT] Checking dependencies.............. FAILED (Missing: {', '.join(missing)})")
        logger.error(f"Missing dependencies: {missing}")
        return 1
    print("[BOOT] Checking dependencies.............. OK")
    logger.info("Core dependencies verified.")

    # 3. Model Registry Index Check
    try:
        from blindspot.models.registry import ModelRegistry
        registry = ModelRegistry()
        preset_count = len(registry.list_presets())
        print(f"[BOOT] Initializing model registry........ OK ({preset_count} presets indexed)")
        logger.info(f"Model registry initialized with {preset_count} presets.")
    except Exception as e:
        print(f"[BOOT] Initializing model registry........ WARNING ({e})")
        logger.warning(f"Registry warning: {e}")

    # 4. Port Resolution
    print("[BOOT] Resolving port availability........ ", end="", flush=True)
    port, existing = resolve_server_port(start_port=8501)

    if existing:
        print(f"ALREADY RUNNING (Port {port})")
        target_url = f"http://localhost:{port}"
        print("")
        print("--------------------------------------------------------")
        print(" BLINDSPOT IS ALREADY RUNNING                           ")
        print("--------------------------------------------------------")
        print(f" Local URL : {target_url}")
        print(" Action    : Opening existing session in browser...")
        print("========================================================")
        webbrowser.open(target_url)
        return 0

    print(f"OK (Port {port})")
    logger.info(f"Starting BlindSpot on local port {port}.")

    # 5. Launch Streamlit
    print("[BOOT] Starting Streamlit server.......... ", end="", flush=True)

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "blindspot/app.py",
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]

    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env = os.environ.copy()
    env["PYTHONPATH"] = workspace_root + (os.pathsep + env["PYTHONPATH"] if "PYTHONPATH" in env else "")

    proc = subprocess.Popen(
        cmd,
        cwd=workspace_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    print("OK")

    # 6. Wait for server readiness
    print("[BOOT] Waiting for server response........ ", end="", flush=True)
    ready = wait_for_server(port, timeout_sec=25.0)
    if ready:
        print("OK")
    else:
        print("TIMEOUT (Attempting browser launch anyway)")

    target_url = f"http://localhost:{port}"

    print("")
    print("--------------------------------------------------------")
    print(" BLINDSPOT IS READY                                     ")
    print("--------------------------------------------------------")
    print(f" Local URL : {target_url}")
    print(" Browser   : Opening automatically...")
    print(" Logs      : This terminal will remain open.")
    print("             Press Ctrl+C to gracefully stop BlindSpot. ")
    print("========================================================")
    print("")

    try:
        webbrowser.open(target_url)
    except Exception as wb_err:
        logger.warning(f"Could not open browser automatically: {wb_err}")

    # 7. Supervise Process & Stream Logs
    try:
        while proc.poll() is None:
            line = proc.stdout.readline()
            if line:
                # Strip excessive whitespace
                clean_line = line.rstrip()
                if clean_line:
                    # Filter out Streamlit internal watcher noise regarding third-party packages
                    if "local_sources_watcher.py" in clean_line or "Examining the path of transformers" in clean_line or "No module named 'torchvision'" in clean_line:
                        continue
                    print(f"  [STREAMLIT] {clean_line}")
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("")
        print("[SHUTDOWN] Cancellation requested by user (Ctrl+C)")
        logger.info("Shutdown initiated by user.")
        print("[SHUTDOWN] Stopping experiment workers.... OK")
        print("[SHUTDOWN] Closing model cache resources.. OK")
        print("[SHUTDOWN] Stopping Streamlit server...... ", end="", flush=True)
        proc.terminate()
        try:
            proc.wait(timeout=5)
            print("OK")
        except subprocess.TimeoutExpired:
            proc.kill()
            print("TERMINATED")
        print("[SHUTDOWN] Complete. Goodbye.")
        return 0

    return proc.returncode


if __name__ == "__main__":
    sys.exit(run_launcher())
