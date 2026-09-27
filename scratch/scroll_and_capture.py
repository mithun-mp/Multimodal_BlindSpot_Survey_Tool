import asyncio
import json
import base64
import os
import subprocess
import time
import urllib.request
import websockets

BEFORE_DIR = r"C:\Dev\Projects\Multimodel_Blindspot-main\audit_reports\output_ui_redesign\before"

async def scroll_and_capture():
    user_data = os.path.join(os.environ.get("TEMP", "C:\\Temp"), f"chrome_scroll_{int(time.time())}")
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        f"--remote-debugging-port=9222",
        "--headless=new",
        "--disable-gpu",
        f"--user-data-dir={user_data}",
        "--window-size=1920,1080",
        "http://localhost:8501"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(3)
    try:
        with urllib.request.urlopen("http://localhost:9222/json") as resp:
            tabs = json.loads(resp.read().decode())
        tab = next(t for t in tabs if "BlindSpot" in t.get("title", "") or "8501" in t.get("url", ""))
        ws = await websockets.connect(tab["webSocketDebuggerUrl"], max_size=20*1024*1024)
        msg_id = 0
        async def send(m, p=None):
            nonlocal msg_id
            msg_id += 1
            await ws.send(json.dumps({"id": msg_id, "method": m, "params": p or {}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == msg_id: return r.get("result", {})

        await send("Page.enable")
        await send("Runtime.enable")
        await asyncio.sleep(2)

        # Click Analyze
        js_click = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const b = btns.find(x => x.innerText.includes('Analyze'));
            if (b) { b.click(); return true; }
            return false;
        })()
        """
        await send("Runtime.evaluate", {"expression": js_click, "returnByValue": True, "awaitPromise": True})
        await asyncio.sleep(3)

        # Scroll down to the matrix table
        scroll_js = """
        (() => {
            const tables = document.querySelectorAll('[data-testid="stDataFrame"]');
            if (tables.length > 1) {
                tables[1].scrollIntoView({behavior: 'instant', block: 'center'});
                return "scrolled to table 2";
            } else if (tables.length === 1) {
                tables[0].scrollIntoView({behavior: 'instant', block: 'center'});
                return "scrolled to table 1";
            }
            window.scrollTo(0, 1000);
            return "scrolled 1000px";
        })()
        """
        res_scroll = await send("Runtime.evaluate", {"expression": scroll_js, "returnByValue": True, "awaitPromise": True})
        print("Scroll result:", res_scroll, flush=True)
        await asyncio.sleep(2)

        res = await send("Page.captureScreenshot", {"format": "png"})
        with open(os.path.join(BEFORE_DIR, "01b_comparison_matrix_scrolled.png"), "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("Captured 01b_comparison_matrix_scrolled.png", flush=True)

    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(scroll_and_capture())
