import asyncio
import json
import base64
import os
import subprocess
import time
import urllib.request
import websockets

AFTER_DIR = r"C:\Dev\Projects\Multimodel_Blindspot-main\audit_reports\output_ui_redesign\after"

async def capture_drawer_and_tabs():
    user_data = os.path.join(os.environ.get("TEMP", "C:\\Temp"), f"chrome_tabs_{int(time.time())}")
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

        # Navigate to Analyze
        nav_js = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const b = btns.find(btn => btn.innerText.includes('Analyze'));
            if (b) { b.click(); return true; }
            return false;
        })()
        """
        await eval_js(nav_js)
        await asyncio.sleep(3)

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

        # Scroll section.main down to drawer
        scroll_drw_js = """
        (() => {
            const main = document.querySelector('section.main');
            if (main) {
                main.scrollTop = 1750;
                return main.scrollTop;
            }
            return 0;
        })()
        """
        sy = await eval_js(scroll_drw_js)
        print("Scrolled section.main to:", sy, flush=True)
        await asyncio.sleep(2)
        await screenshot("01c_probe_detail_drawer_after.png")

        # Inspect tabs
        find_tabs_js = """
        (() => {
            const tabBtns = Array.from(document.querySelectorAll('button[data-baseweb="tab"], button[role="tab"], div[data-baseweb="tab-list"] button'));
            return tabBtns.map((b, i) => ({index: i, text: b.innerText}));
        })()
        """
        tab_list = await eval_js(find_tabs_js)
        print("Found tabs:", tab_list, flush=True)

        # Click Tab 2: "Target Architecture: Expected vs Predicted Audit"
        click_tab2_js = """
        (() => {
            const tabBtns = Array.from(document.querySelectorAll('button[data-baseweb="tab"], button[role="tab"], div[data-baseweb="tab-list"] button'));
            if (tabBtns.length > 1) {
                tabBtns[1].scrollIntoView({behavior: 'instant', block: 'center'});
                tabBtns[1].click();
                return tabBtns[1].innerText;
            }
            return null;
        })()
        """
        t2 = await eval_js(click_tab2_js)
        print("Clicked Tab 2:", t2, flush=True)
        await asyncio.sleep(2)
        await screenshot("02_model_comparison_after.png")

        # Click Tab 3: "Behavioral Fingerprints"
        click_tab3_js = """
        (() => {
            const tabBtns = Array.from(document.querySelectorAll('button[data-baseweb="tab"], button[role="tab"], div[data-baseweb="tab-list"] button'));
            if (tabBtns.length > 2) {
                tabBtns[2].scrollIntoView({behavior: 'instant', block: 'center'});
                tabBtns[2].click();
                return tabBtns[2].innerText;
            }
            return null;
        })()
        """
        t3 = await eval_js(click_tab3_js)
        print("Clicked Tab 3:", t3, flush=True)
        await asyncio.sleep(2)
        await screenshot("02b_behavioral_fingerprints_after.png")

        await ws.close()
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(capture_drawer_and_tabs())
