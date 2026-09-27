import asyncio
import json
import base64
import os
import subprocess
import time
import urllib.request
import websockets

AUDIT_DIR = r"C:\Dev\Projects\Multimodel_Blindspot-main\audit_reports\output_ui_redesign\after"
os.makedirs(AUDIT_DIR, exist_ok=True)

def safe_print(msg):
    clean = str(msg).encode('ascii', 'replace').decode('ascii')
    print(clean, flush=True)

async def run_capture():
    user_data = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "chrome_audit_master")
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--remote-debugging-port=9222",
        "--headless=new",
        "--disable-gpu",
        f"--user-data-dir={user_data}",
        "--window-size=1920,1080",
        "http://localhost:8501"
    ]
    proc = subprocess.Popen(cmd)
    await asyncio.sleep(3)

    try:
        with urllib.request.urlopen("http://localhost:9222/json") as resp:
            tabs = json.loads(resp.read().decode())
        tab = next(t for t in tabs if "BlindSpot" in t.get("title", "") or "8501" in t.get("url", ""))
        ws = await websockets.connect(tab["webSocketDebuggerUrl"], max_size=25*1024*1024)
        msg_id = 0

        async def send(method, params=None):
            nonlocal msg_id
            msg_id += 1
            req = {"id": msg_id, "method": method, "params": params or {}}
            await ws.send(json.dumps(req))
            while True:
                raw = await ws.recv()
                res = json.loads(raw)
                if res.get("id") == msg_id:
                    return res.get("result", {})

        async def eval_js(expr):
            res = await send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
            if "exceptionDetails" in res:
                safe_print(f"JS Exception: {res['exceptionDetails']}")
                return None
            return res.get("result", {}).get("value")

        async def wait_idle(timeout=30):
            start = time.time()
            while time.time() - start < timeout:
                running = await eval_js("Boolean(document.querySelector('.stAppRunning, [data-testid=\"stStatusWidget\"]'))")
                if not running:
                    await asyncio.sleep(1)
                    return True
                await asyncio.sleep(0.5)
            return False

        async def screenshot(filename):
            path = os.path.join(AUDIT_DIR, filename)
            res = await send("Page.captureScreenshot", {"format": "png"})
            data = base64.b64decode(res["data"])
            with open(path, "wb") as f:
                f.write(data)
            safe_print(f"Captured {filename} ({len(data)} bytes)")
            return path

        await send("Page.enable")
        await send("Runtime.enable")

        # Wait for Streamlit app to load
        for _ in range(20):
            ready = await eval_js("document.querySelectorAll('button').length > 3")
            if ready:
                break
            await asyncio.sleep(1)
        await asyncio.sleep(2)

        # Check current buttons
        btn_texts = await eval_js("Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)")
        safe_print(f"Current visible buttons: {btn_texts}")

        # Check if already on Analyze / Comparison or click Analyze
        is_on_comp = await eval_js("Boolean(document.body.innerText.includes('CROSS-MODEL BEHAVIORAL COMPARISON'))")
        safe_print(f"Already on Comparison page? {is_on_comp}")

        if not is_on_comp:
            safe_print("Navigating to Analyze page...")
            nav_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(btn => btn.innerText.includes('Analyze') || btn.innerText.includes('Model Comparison'));
                if (b) { b.click(); return b.innerText; }
                return null;
            })()
            """
            nav_clicked = await eval_js(nav_js)
            safe_print(f"Clicked nav: {nav_clicked}")
            await wait_idle()
            await asyncio.sleep(3)

        # Check if results are loaded
        has_results = await eval_js("Boolean(document.body.innerText.includes('MODEL \u00d7 PROBE MATRIX'))")
        safe_print(f"Has results loaded? {has_results}")

        if not has_results:
            safe_print("Checking for LOAD RUN button on Comparison page...")
            load_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(btn => btn.innerText.trim() === 'LOAD RUN');
                if (b) { b.click(); return 'clicked LOAD RUN'; }
                return 'no LOAD RUN';
            })()
            """
            l_res = await eval_js(load_js)
            safe_print(f"Load run clicked: {l_res}")
            await wait_idle()
            await asyncio.sleep(4)

        # Check tab buttons
        tab_names = await eval_js("""
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"], [role="tab"]'));
            return tabs.map(t => t.innerText.trim());
        })()
        """)
        safe_print(f"Detected tabs: {tab_names}")

        # 1. Capture Top of Comparison page showing Baseline Stimuli and Tabs (NO DUPLICATE TABLE ABOVE TABS!)
        safe_print("Capturing 05_comparison_matrix_no_top_table.png...")
        await screenshot("05_comparison_matrix_no_top_table.png")

        # Scroll down slightly to show tabs cleanly
        await eval_js("""
        (() => {
            const el = document.querySelector('section.main') || window;
            if (el.scrollTo) el.scrollTo({ top: 350, behavior: 'instant' });
            else window.scrollTo(0, 350);
        })()
        """)
        await asyncio.sleep(1)

        # 2. Click Tab: BEHAVIORAL FINGERPRINTS
        safe_print("Clicking BEHAVIORAL FINGERPRINTS tab...")
        click_fingerprints = """
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"], [role="tab"]'));
            const target = tabs.find(t => t.innerText.includes('FINGERPRINTS'));
            if (target) {
                target.scrollIntoView({behavior: 'instant', block: 'center'});
                target.click();
                return target.innerText;
            }
            return null;
        })()
        """
        clicked_f = await eval_js(click_fingerprints)
        safe_print(f"Clicked Tab: {clicked_f}")
        await asyncio.sleep(2)
        safe_print("Capturing 06_behavioral_fingerprints_table.png...")
        await screenshot("06_behavioral_fingerprints_table.png")

        # 3. Click Tab: MODELS & FAILURES
        safe_print("Clicking MODELS & FAILURES tab...")
        click_failures = """
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"], [role="tab"]'));
            const target = tabs.find(t => t.innerText.includes('MODELS & FAILURES'));
            if (target) {
                target.scrollIntoView({behavior: 'instant', block: 'center'});
                target.click();
                return target.innerText;
            }
            return null;
        })()
        """
        clicked_m = await eval_js(click_failures)
        safe_print(f"Clicked Tab: {clicked_m}")
        await asyncio.sleep(2)
        safe_print("Capturing 07_models_and_failures_tab.png...")
        await screenshot("07_models_and_failures_tab.png")

        # Scroll down in MODELS & FAILURES to show the Per-Model Evidence Log
        await eval_js("""
        (() => {
            const all = Array.from(document.querySelectorAll('h4, div, p, span'));
            const target = all.find(e => e.innerText && e.innerText.includes('PER-MODEL FAILURE EVIDENCE LOG'));
            if (target) {
                target.scrollIntoView({behavior: 'instant', block: 'start'});
                return "scrolled to evidence log";
            }
            return "evidence log heading not found";
        })()
        """)
        await asyncio.sleep(2)
        safe_print("Capturing 08_models_failures_evidence_log.png...")
        await screenshot("08_models_failures_evidence_log.png")

        await ws.close()
        safe_print("Automation completed successfully.")
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(run_capture())
