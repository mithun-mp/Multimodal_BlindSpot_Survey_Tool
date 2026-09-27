import asyncio
import json
import base64
import os
import subprocess
import time
import urllib.request
import websockets

AFTER_DIR = r"C:\Dev\Projects\Multimodel_Blindspot-main\audit_reports\output_ui_redesign\after"

async def capture_new_tabs():
    user_data = os.path.join(os.environ.get("TEMP", "C:\\Temp"), f"chrome_mf_{int(time.time())}")
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
        ws = await websockets.connect(tab["webSocketDebuggerUrl"], max_size=20*1024*1024)
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
                print("JS Exception:", res["exceptionDetails"])
                return None
            return res.get("result", {}).get("value")

        async def screenshot(filename):
            path = os.path.join(AFTER_DIR, filename)
            res = await send("Page.captureScreenshot", {"format": "png"})
            data = base64.b64decode(res["data"])
            with open(path, "wb") as f:
                f.write(data)
            print(f"Captured {filename} ({len(data)} bytes)", flush=True)

        await send("Page.enable")
        await send("Runtime.enable")

        # Wait for Streamlit app to load
        for _ in range(20):
            ready = await eval_js("document.querySelectorAll('button').length > 5")
            if ready:
                break
            await asyncio.sleep(1)
        await asyncio.sleep(2)

        # Navigate to Analyze
        nav_js = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const b = btns.find(btn => btn.innerText.includes('Analyze'));
            if (b) { b.click(); return "clicked Analyze"; }
            return "no Analyze button";
        })()
        """
        n_res = await eval_js(nav_js)
        print("Navigate to Analyze:", n_res, flush=True)
        await asyncio.sleep(4)

        # Click LOAD RUN if present
        load_run_js = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const b = btns.find(btn => btn.innerText.includes('LOAD RUN'));
            if (b) { b.click(); return "clicked LOAD RUN"; }
            return "no LOAD RUN button";
        })()
        """
        lr = await eval_js(load_run_js)
        print("LOAD RUN status:", lr, flush=True)
        await asyncio.sleep(3)

        # 1. Capture top of page showing clean transition directly into tabs without duplicate table!
        await screenshot("05_comparison_matrix_no_top_table.png")

        # 2. Click Tab 3: "🧬 BEHAVIORAL FINGERPRINTS"
        click_tab3_js = """
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"]'));
            const target = tabs.find(t => t.innerText.includes('FINGERPRINTS'));
            if (target) {
                target.scrollIntoView({behavior: 'instant', block: 'center'});
                target.click();
                return target.innerText;
            }
            return null;
        })()
        """
        t3 = await eval_js(click_tab3_js)
        print("Clicked Tab 3:", t3, flush=True)
        await asyncio.sleep(2)
        await screenshot("06_behavioral_fingerprints_table.png")

        # 3. Click Tab 4: "🏷️ MODELS & FAILURES"
        click_tab4_js = """
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"]'));
            const target = tabs.find(t => t.innerText.includes('MODELS & FAILURES'));
            if (target) {
                target.scrollIntoView({behavior: 'instant', block: 'center'});
                target.click();
                return target.innerText;
            }
            return null;
        })()
        """
        t4 = await eval_js(click_tab4_js)
        print("Clicked Tab 4:", t4, flush=True)
        await asyncio.sleep(2)
        await screenshot("07_models_and_failures_tab.png")

        await ws.close()
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(capture_new_tabs())
