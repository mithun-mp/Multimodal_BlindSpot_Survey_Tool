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

class BeforeSwitcher:
    def __init__(self, port=9222):
        self.port = port
        self.proc = None
        self.ws = None
        self.msg_id = 0

    def start(self):
        user_data = os.path.join(os.environ.get("TEMP", "C:\\Temp"), f"chrome_switch_{int(time.time())}")
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

async def switch_and_capture():
    switcher = BeforeSwitcher()
    switcher.start()
    try:
        await switcher.connect()

        # 1. Navigate to Analyze -> Comparison
        print("Navigating to Analyze...", flush=True)
        await switcher.click_button_by_text("Analyze")
        await asyncio.sleep(3)

        # 2. Open "Switch Loaded Experiment Run" expander
        open_exp_js = """
        (() => {
            const expanders = Array.from(document.querySelectorAll('[data-testid="stExpander"] details'));
            const switchExp = expanders.find(e => e.innerText.includes('Switch Loaded Experiment Run'));
            if (switchExp) {
                switchExp.open = true;
                return true;
            }
            return false;
        })()
        """
        opened = await switcher.eval_js(open_exp_js)
        print("Opened switch expander:", opened, flush=True)
        await asyncio.sleep(1)

        # 3. Click the select box inside the expander and choose exp_1790537272_6f4cc1
        select_run_js = """
        (() => {
            const selectDiv = document.querySelector('[data-testid="stExpander"] [data-baseweb="select"]');
            if (!selectDiv) return false;
            const input = selectDiv.querySelector('input');
            if (input) {
                input.focus();
                selectDiv.click();
                return true;
            }
            selectDiv.click();
            return true;
        })()
        """
        await switcher.eval_js(select_run_js)
        await asyncio.sleep(1)

        # In base-web select dropdown, find option containing exp_1790537272_6f4cc1
        choose_option_js = """
        (() => {
            const options = Array.from(document.querySelectorAll('[role="option"]'));
            const opt = options.find(o => o.innerText.includes('1790537272') || o.innerText.includes('6f4cc1') || o.innerText.includes('Multimodel 00001'));
            if (opt) {
                opt.click();
                return opt.innerText;
            }
            return null;
        })()
        """
        chosen = await switcher.eval_js(choose_option_js)
        print("Chosen option in select dropdown:", chosen, flush=True)
        await asyncio.sleep(1)

        # Click "SWITCH RUN"
        clicked_switch = await switcher.click_button_by_text("SWITCH RUN")
        print("Clicked SWITCH RUN:", clicked_switch, flush=True)
        await asyncio.sleep(4)

        # Capture 01_comparison_matrix_before.png
        await switcher.screenshot("01_comparison_matrix_before.png")

        # Click Tab 2: "Target Architecture: Expected vs Predicted Audit"
        click_tab2_js = """
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[role="tab"]'));
            if (tabs.length > 1) {
                tabs[1].click();
                return tabs[1].innerText;
            }
            return null;
        })()
        """
        tab2_clicked = await switcher.eval_js(click_tab2_js)
        print("Clicked Tab 2:", tab2_clicked, flush=True)
        await asyncio.sleep(2)
        await switcher.screenshot("02_model_comparison_before.png")

        # Click Tab 3: "Pairwise Consistency & Cohen's Kappa"
        click_tab3_js = """
        (() => {
            const tabs = Array.from(document.querySelectorAll('button[role="tab"]'));
            if (tabs.length > 2) {
                tabs[2].click();
                return tabs[2].innerText;
            }
            return null;
        })()
        """
        tab3_clicked = await switcher.eval_js(click_tab3_js)
        print("Clicked Tab 3:", tab3_clicked, flush=True)
        await asyncio.sleep(2)
        await switcher.screenshot("02b_pairwise_kappa_before.png")

        # 4. Navigate to Failure Analysis
        print("Navigating to Failure Analysis...", flush=True)
        await switcher.click_button_by_text("Failure Analysis")
        await asyncio.sleep(3)
        await switcher.screenshot("03_failure_analysis_before.png")

        # 5. Navigate to Reports
        print("Navigating to Reports...", flush=True)
        await switcher.click_button_by_text("Reports")
        await asyncio.sleep(3)
        await switcher.click_button_by_text("Reports") # subpage
        await asyncio.sleep(3)
        await switcher.screenshot("04_graphs_before.png")

    finally:
        switcher.stop()

if __name__ == "__main__":
    asyncio.run(switch_and_capture())
