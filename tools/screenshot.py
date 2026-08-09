#!/usr/bin/env python3
"""Load a page headless, collect console messages + page errors, report the <title>,
optionally screenshot. Usage: cdp-check.py URL [OUT.png] [WIDTH] [WAIT_S]"""
import os
import asyncio, base64, json, subprocess, sys, time, urllib.request

def chrome_flags():
    """Chromium cannot use its namespace sandbox on an Ubuntu 24.04 CI runner, and the
    small /dev/shm there crashes tabs with several canvases. Only on CI."""
    return ['--no-sandbox', '--disable-dev-shm-usage'] if os.environ.get('CI') else []


URL = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else None
WIDTH = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
WAIT = float(sys.argv[4]) if len(sys.argv) > 4 else 12
PORT = 9272

proc = subprocess.Popen([
    "chromium", "--headless=new", "--disable-gpu", "--hide-scrollbars",
    *chrome_flags(),
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
                ws_url = page[0]["webSocketDebuggerUrl"]
                break
        except Exception:
            pass
        time.sleep(0.2)
    if not ws_url:
        raise SystemExit("no debug target")

    import websockets
    logs = []
    async with websockets.connect(ws_url, max_size=200_000_000) as ws:
        mid = 0
        async def send(method, params=None):
            nonlocal mid
            mid += 1
            await ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
            return mid
        async def call(method, params=None):
            want = await send(method, params)
            while True:
                msg = json.loads(await ws.recv())
                collect(msg)
                if msg.get("id") == want:
                    return msg.get("result", {})
        def collect(msg):
            m = msg.get("method")
            if m == "Runtime.consoleAPICalled":
                args = [a.get("value", a.get("description", "?")) for a in msg["params"]["args"]]
                logs.append(f'[{msg["params"]["type"]}] ' + " ".join(str(a) for a in args))
            elif m == "Runtime.exceptionThrown":
                d = msg["params"]["exceptionDetails"]
                txt = d.get("exception", {}).get("description") or d.get("text")
                logs.append(f'[EXCEPTION] {txt} @line {d.get("lineNumber")}')
            elif m == "Log.entryAdded":
                e = msg["params"]["entry"]
                logs.append(f'[{e["level"]}/{e["source"]}] {e["text"]}')
        await call("Page.enable"); await call("Runtime.enable"); await call("Log.enable")
        await call("Emulation.setDeviceMetricsOverride", {"width": WIDTH, "height": 1600, "deviceScaleFactor": 1, "mobile": False})
        await call("Page.navigate", {"url": URL})
        end = time.time() + WAIT
        while time.time() < end:
            try:
                msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=max(0.1, end - time.time())))
                collect(msg)
            except asyncio.TimeoutError:
                break
        title = (await call("Runtime.evaluate", {"expression": "document.title", "returnByValue": True}))["result"].get("value")
        print("TITLE:", title)
        for l in logs:
            print(l)
        if OUT:
            metrics = await call("Page.getLayoutMetrics")
            h = int(metrics["cssContentSize"]["height"])
            shot = await call("Page.captureScreenshot", {
                "format": "png", "captureBeyondViewport": True,
                "clip": {"x": 0, "y": 0, "width": WIDTH, "height": min(h, 30000), "scale": 1},
            })
            open(OUT, "wb").write(base64.b64decode(shot["data"]))
            print(f"captured {WIDTH}x{h} -> {OUT}")

try:
    asyncio.run(main())
finally:
    proc.terminate()
