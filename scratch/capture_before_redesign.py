import asyncio
import json
import base64
import os
import subprocess
import time
import urllib.request
import websockets

BEFORE_DIR = r"C:\Dev\Projects\Multimodel_Blindspot-main\audit_reports\output_ui_redesign\before"
os.makedirs(BEFORE_DIR, exist_ok=True)

class BeforeAuditor:
    def __init__(self, port=9222):
        self.port = port
        self.proc = None
        self.ws = None
        self.msg_id = 0

    def start(self):
        user_data = os.path.join(os.environ.get("TEMP", "C:\\Temp"), f"chrome_before_{int(time.time())}")
        cmd = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            f"--remote-debugging-port={self.port}",
            "--headless=new",
            "--disable-gpu",
            f"--user-data-dir={user_data}",
            "--window-size=1920,1080",
            "http://localhost:8501"
        ]
        self.proc = subprocess.Popen(cmd)
        time.sleep(3)

    async def connect(self):
        with urllib.request.urlopen(f"http://localhost:{self.port}/json") as resp:
            tabs = json.loads(resp.read().decode())
        tab = next(t for t in tabs if "BlindSpot" in t.get("title", "") or "8501" in t.get("url", ""))
        self.ws = await websockets.connect(tab["webSocketDebuggerUrl"], max_size=20*1024*1024)
        await self.send("Page.enable")
        await self.send("Runtime.enable")
        await asyncio.sleep(2)

    async def send(self, method, params=None):
        self.msg_id += 1
        req = {"id": self.msg_id, "method": method, "params": params or {}}
        await self.ws.send(json.dumps(req))
        while True:
            raw = await self.ws.recv()
            res = json.loads(raw)
            if res.get("id") == self.msg_id:
                return res.get("result", {})

    async def eval_js(self, expr):
        res = await self.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        if "exceptionDetails" in res:
            print("JS Exception:", res["exceptionDetails"])
            return None
        return res.get("result", {}).get("value")

    async def screenshot(self, filename):
        path = os.path.join(BEFORE_DIR, filename)
        res = await self.send("Page.captureScreenshot", {"format": "png"})
        data = base64.b64decode(res["data"])
        with open(path, "wb") as f:
            f.write(data)
        print(f"Captured {filename} ({len(data)} bytes)", flush=True)
        return path

    async def click_button_by_text(self, text):
        js = f"""
        (() => {{
            const btns = Array.from(document.querySelectorAll('button'));
            const target = btns.find(b => b.innerText.includes('{text}'));
            if (!target) return false;
            target.scrollIntoView({{behavior: 'instant', block: 'center'}});
            target.click();
            return true;
        }})()
        """
        res = await self.eval_js(js)
        return res

    def stop(self):
        if self.proc:
            self.proc.terminate()

async def capture_all_before():
    auditor = BeforeAuditor()
    auditor.start()
    try:
        await auditor.connect()

        # 1. Navigate to Run History and select exp_1790537272_6f4cc1
        print("1. Navigating to Reports -> Run History to load 5-model run...", flush=True)
        await auditor.click_button_by_text("Reports")
        await asyncio.sleep(3)
        await auditor.click_button_by_text("Run History")
        await asyncio.sleep(3)

        # Select exp_1790537272_6f4cc1 if dropdown exists, or click INSPECT RUN
        select_exp_js = """
        (() => {
            const selects = Array.from(document.querySelectorAll('[data-baseweb="select"]'));
            return selects.length;
        })()
        """
        sel_count = await auditor.eval_js(select_exp_js)
        print(f"Found {sel_count} select elements in Run History", flush=True)

        # Click "INSPECT RUN" if available
        await auditor.click_button_by_text("INSPECT RUN")
        await asyncio.sleep(2)
        await auditor.screenshot("05_run_details_before.png")

        # 2. Navigate to Analyze -> Comparison
        print("2. Navigating to Analyze (Comparison)...", flush=True)
        await auditor.click_button_by_text("Analyze")
        await asyncio.sleep(4)

        # Check if LOAD RUN button is present
        loaded = await auditor.click_button_by_text("LOAD RUN")
        if loaded:
            print("Clicked LOAD RUN in Comparison view", flush=True)
            await asyncio.sleep(3)

        # Tab 1: Cross-Model Matrix Before
        await auditor.screenshot("01_comparison_matrix_before.png")

        # Tab 2: Model Comparison (Target Architecture: Expected vs Predicted Audit)
        print("3. Switching to Model Comparison tab...", flush=True)
        tab_click_js = """
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[role="tab"]'));
            const targetTab = tabs.find(t => t.innerText.includes("Target Architecture") || t.innerText.includes("Audit"));
            if (targetTab) {
                targetTab.click();
                return true;
            }
            return false;
        })()
        """
        clicked_tab = await auditor.eval_js(tab_click_js)
        print(f"Clicked Target Architecture tab: {clicked_tab}", flush=True)
        await asyncio.sleep(3)
        await auditor.screenshot("02_model_comparison_before.png")

        # 4. Navigate to Failure Analysis
        print("4. Navigating to Failure Analysis...", flush=True)
        await auditor.click_button_by_text("Failure Analysis")
        await asyncio.sleep(4)
        await auditor.screenshot("03_failure_analysis_before.png")

        # 5. Navigate to Reports -> Thesis Visualizations
        print("5. Navigating to Reports...", flush=True)
        await auditor.click_button_by_text("Reports")
        await asyncio.sleep(3)
        await auditor.click_button_by_text("Reports") # subpage
        await asyncio.sleep(3)
        await auditor.screenshot("04_graphs_before.png")

    finally:
        auditor.stop()

if __name__ == "__main__":
    asyncio.run(capture_all_before())
