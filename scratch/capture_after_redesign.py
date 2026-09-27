import asyncio
import json
import base64
import os
import subprocess
import time
import urllib.request
import websockets

AFTER_DIR = r"C:\Dev\Projects\Multimodel_Blindspot-main\audit_reports\output_ui_redesign\after"
os.makedirs(AFTER_DIR, exist_ok=True)

class AfterAuditor:
    def __init__(self, port=9222):
        self.port = port
        self.proc = None
        self.ws = None
        self.msg_id = 0

    def start(self):
        user_data = os.path.join(os.environ.get("TEMP", "C:\\Temp"), f"chrome_after_{int(time.time())}")
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
        path = os.path.join(AFTER_DIR, filename)
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

async def capture_all_after():
    auditor = AfterAuditor()
    auditor.start()
    try:
        await auditor.connect()

        # 1. Navigate to Analyze (Comparison)
        print("1. Navigating to Analyze (Comparison)...", flush=True)
        await auditor.click_button_by_text("Analyze")
        await asyncio.sleep(4)

        # Ensure active_results is loaded; click LOAD RUN if needed
        await auditor.click_button_by_text("LOAD RUN")
        await asyncio.sleep(2)

        # Capture top of Comparison (Model Completeness Banner & Baseline Stimuli)
        await auditor.screenshot("01_comparison_matrix_after.png")

        # Scroll to the redesigned HTML matrix table
        scroll_matrix_js = """
        (() => {
            const table = document.querySelector('.bs-grid-container');
            if (table) {
                table.scrollIntoView({behavior: 'instant', block: 'center'});
                return "scrolled to .bs-grid-container";
            }
            window.scrollTo(0, 750);
            return "scrolled 750px";
        })()
        """
        scrolled = await auditor.eval_js(scroll_matrix_js)
        print("Scrolled to matrix:", scrolled, flush=True)
        await asyncio.sleep(2)
        await auditor.screenshot("01b_comparison_matrix_scrolled_after.png")

        # Scroll to probe drawer
        scroll_drawer_js = """
        (() => {
            const selects = document.querySelectorAll('[data-baseweb="select"]');
            if (selects.length > 0) {
                selects[selects.length - 1].scrollIntoView({behavior: 'instant', block: 'center'});
                return "scrolled to drawer";
            }
            window.scrollTo(0, 1400);
            return "scrolled 1400px";
        })()
        """
        scrolled_drw = await auditor.eval_js(scroll_drawer_js)
        print("Scrolled to drawer:", scrolled_drw, flush=True)
        await asyncio.sleep(2)
        await auditor.screenshot("01c_probe_detail_drawer_after.png")

        # 2. Switch to Tab 2: "Target Architecture: Expected vs Predicted Audit"
        print("2. Switching to Tab 2: Per-Model Audit...", flush=True)
        tab2_js = """
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[role="tab"]'));
            if (tabs.length > 1) {
                tabs[1].click();
                return tabs[1].innerText;
            }
            return null;
        })()
        """
        clicked_tab2 = await auditor.eval_js(tab2_js)
        print("Clicked Tab 2:", clicked_tab2, flush=True)
        await asyncio.sleep(3)
        await auditor.screenshot("02_model_comparison_after.png")

        # 3. Switch to Tab 3: "Behavioral Fingerprints"
        print("3. Switching to Tab 3: Fingerprints...", flush=True)
        tab3_js = """
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[role="tab"]'));
            if (tabs.length > 2) {
                tabs[2].click();
                return tabs[2].innerText;
            }
            return null;
        })()
        """
        clicked_tab3 = await auditor.eval_js(tab3_js)
        print("Clicked Tab 3:", clicked_tab3, flush=True)
        await asyncio.sleep(2)
        await auditor.screenshot("02b_behavioral_fingerprints_after.png")

        # 4. Navigate to Failure Analysis
        print("4. Navigating to Failure Analysis...", flush=True)
        await auditor.click_button_by_text("Failure Analysis")
        await asyncio.sleep(4)
        await auditor.screenshot("03_failure_analysis_after.png")

        # Scroll down in Failure Analysis to show structured table
        scroll_fail_js = """
        (() => {
            const table = document.querySelector('[data-testid="stDataFrame"]');
            if (table) {
                table.scrollIntoView({behavior: 'instant', block: 'center'});
                return "scrolled to failure table";
            }
            window.scrollTo(0, 500);
            return "scrolled 500px";
        })()
        """
        scrolled_fail = await auditor.eval_js(scroll_fail_js)
        print("Scrolled failure table:", scrolled_fail, flush=True)
        await asyncio.sleep(2)
        await auditor.screenshot("03b_failure_table_after.png")

        # 5. Navigate to Reports -> Thesis Visualizations
        print("5. Navigating to Reports...", flush=True)
        await auditor.click_button_by_text("Reports")
        await asyncio.sleep(3)
        await auditor.screenshot("04_graphs_after.png")

    finally:
        auditor.stop()

if __name__ == "__main__":
    asyncio.run(capture_all_after())
