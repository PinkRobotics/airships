#!/usr/bin/env python3
"""Load page, run a JS expression, wait, screenshot a clip (or full page).
Usage: cdp-interact.py URL OUT.png JS [WIDTH] [WAIT_BEFORE] [WAIT_AFTER] [CLIP_SEL]"""
import asyncio, base64, json, subprocess, sys, time, urllib.request

URL, OUT, JS = sys.argv[1], sys.argv[2], sys.argv[3]
WIDTH = int(sys.argv[4]) if len(sys.argv) > 4 else 1440
WAIT1 = float(sys.argv[5]) if len(sys.argv) > 5 else 8
WAIT2 = float(sys.argv[6]) if len(sys.argv) > 6 else 3
CLIP_SEL = sys.argv[7] if len(sys.argv) > 7 else None
PORT = 9273

proc = subprocess.Popen([
    "chromium", "--headless=new", "--disable-gpu", "--hide-scrollbars",
    f"--remote-debugging-port={PORT}", "--remote-allow-origins=*", "--use-angle=swiftshader",
    f"--window-size={WIDTH},1600", "about:blank",
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

async def main():
    ws_url = None
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
            page = [t for t in tabs if t["type"] == "page"]
            if page:
                ws_url = page[0]["webSocketDebuggerUrl"]; break
        except Exception: pass
        time.sleep(0.2)
    import websockets
    async with websockets.connect(ws_url, max_size=200_000_000) as ws:
        mid = 0
        async def call(method, params=None):
            nonlocal mid
            mid += 1
            await ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == mid:
                    return msg.get("result", {})
        await call("Page.enable")
        await call("Emulation.setDeviceMetricsOverride", {"width": WIDTH, "height": 1600, "deviceScaleFactor": 1, "mobile": False})
        await call("Page.navigate", {"url": URL})
        await asyncio.sleep(WAIT1)
        r = await call("Runtime.evaluate", {"expression": JS, "returnByValue": True, "awaitPromise": True})
        print("EVAL:", json.dumps(r.get("result", {}).get("value"))[:300])
        await asyncio.sleep(WAIT2)
        clip = None
        if CLIP_SEL:
            r = await call("Runtime.evaluate", {"expression":
                f"(()=>{{const e=document.querySelector({CLIP_SEL!r});const b=e.getBoundingClientRect();return {{x:b.x+scrollX,y:b.y+scrollY,w:b.width,h:b.height}}}})()",
                "returnByValue": True})
            b = r["result"]["value"]
            clip = {"x": b["x"], "y": max(0, b["y"] - 8), "width": b["w"], "height": b["h"] + 16, "scale": 1}
        else:
            metrics = await call("Page.getLayoutMetrics")
            h = int(metrics["cssContentSize"]["height"])
            clip = {"x": 0, "y": 0, "width": WIDTH, "height": min(h, 30000), "scale": 1}
        shot = await call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True, "clip": clip})
        open(OUT, "wb").write(base64.b64decode(shot["data"]))
        print("captured ->", OUT)

try:
    asyncio.run(main())
finally:
    proc.terminate()
