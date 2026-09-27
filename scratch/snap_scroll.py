import asyncio
import json
import base64
import urllib.request
import websockets

async def snap():
    with urllib.request.urlopen("http://localhost:9222/json") as r:
        tabs = json.loads(r.read().decode())
    tab = next(t for t in tabs if "BlindSpot" in t.get("title", "") or "8501" in t.get("url", ""))
    ws = await websockets.connect(tab["webSocketDebuggerUrl"], max_size=25*1024*1024)
    msg_id = 0
    async def send(method, params=None):
        nonlocal msg_id
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        while True:
            res = json.loads(await ws.recv())
            if res.get("id") == msg_id:
                return res.get("result", {})

    scroll_js = """
    (() => {
        const c = document.querySelector('[data-testid="stAppViewContainer"]') || document.querySelector('section.main');
        if (c) {
            c.scrollTop = 550;
            return c.scrollTop;
        }
        return -1;
    })()
    """
    res = await send("Runtime.evaluate", {"expression": scroll_js, "returnByValue": True})
    print("Scrolled:", res.get("result", {}).get("value"))
    await asyncio.sleep(1)
    shot = await send("Page.captureScreenshot", {"format": "png"})
    with open(r"audit_reports\output_ui_redesign\after\08_models_failures_evidence_log.png", "wb") as f:
        f.write(base64.b64decode(shot["data"]))
    print("Saved 08!")
    await ws.close()

if __name__ == "__main__":
    asyncio.run(snap())
