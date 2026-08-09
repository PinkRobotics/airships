#!/usr/bin/env python3
"""Load a URL headless, evaluate a JS file, write the full result to disk.
Usage: evaljs.py URL SCRIPT.js OUT [WAIT_S]"""
import os
import asyncio, json, subprocess, sys, time, urllib.request, pathlib

def chrome_flags():
    """Extra Chromium flags this environment needs.

    Ubuntu 24.04 restricts unprivileged user namespaces, which is what Chromium's sandbox
    is built on, so on a CI runner the browser refuses to start at all. Dropping the
    sandbox is safe for what these tools do — drive a page we just served from this
    repository on loopback — but it is not something to do on a developer's machine by
    default, so it is switched on by the CI environment variable rather than always.

    /dev/shm on a runner is small enough that Chromium's shared-memory allocator falls over
    on a page with several canvases, which presents as an unexplained tab crash.
    """
    if os.environ.get('CI'):
        return ['--no-sandbox', '--disable-dev-shm-usage']
    return []


URL, JSFILE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
WAIT = float(sys.argv[4]) if len(sys.argv) > 4 else 14
PORT = 9281
JS = pathlib.Path(JSFILE).read_text()

proc = subprocess.Popen([
    "chromium", "--headless=new", "--disable-gpu", "--hide-scrollbars",
    *chrome_flags(),
    f"--remote-debugging-port={PORT}", "--remote-allow-origins=*",
    "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
    "--window-size=1600,1000", "about:blank",
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

async def main():
    ws_url = None
    for _ in range(80):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
            pages = [t for t in tabs if t["type"] == "page"]
            if pages:
                ws_url = pages[0]["webSocketDebuggerUrl"]; break
        except Exception: pass
        time.sleep(0.2)
    import websockets
    async with websockets.connect(ws_url, max_size=600_000_000) as ws:
        mid = 0
        async def call(method, params=None):
            nonlocal mid
            mid += 1
            await ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == mid:
                    return msg.get("result", {})
        await call("Page.enable"); await call("Runtime.enable")
        await call("Page.navigate", {"url": URL})
        await asyncio.sleep(WAIT)
        r = await call("Runtime.evaluate",
                       {"expression": JS, "returnByValue": True, "awaitPromise": True})
        res = r.get("result", {})
        if res.get("subtype") == "error" or "exceptionDetails" in r:
            print("ERROR:", json.dumps(r)[:900]); sys.exit(1)
        val = res.get("value")
        pathlib.Path(OUT).write_text(val if isinstance(val, str) else json.dumps(val, indent=1))
        print(f"wrote {OUT} ({len(val) if isinstance(val, str) else 0} bytes)")

try: asyncio.run(main())
finally: proc.kill()
