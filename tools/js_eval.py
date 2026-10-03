#!/usr/bin/env python3
"""Load a URL headless, evaluate a JS file, write the full result to disk.
Usage: evaljs.py URL SCRIPT.js OUT [WAIT_S]"""
import os
import asyncio, json, pathlib, subprocess, sys, tempfile

from devtools import BrowserFailed, page_target

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
JS = pathlib.Path(JSFILE).read_text()

# ignore_cleanup_errors, because the profile is disposable and the run is already over by the
# time it is removed. Chromium's zygote and renderer children outlive the browser process we
# kill and keep writing into the profile for a moment afterwards, so a strict rmtree loses a
# race — and lost it on CI, raising "Directory not empty" AFTER the dump had been written
# successfully and turning a green run red. Cleanup must never be able to fail the work.
TMP = tempfile.TemporaryDirectory(dir=os.environ.get("AIRSHIPS_TMPDIR") or None,
                                  ignore_cleanup_errors=True)
# Chromium's own stderr, kept rather than discarded. When the browser fails to start —
# which is what a CI runner does, and what a developer's machine almost never does — the
# reason is printed here and nowhere else.
LOG = pathlib.Path(TMP.name) / "chromium.log"
_log = LOG.open("w")

# SOFTWARE BY DEFAULT, HARDWARE ON REQUEST. swiftshader is deterministic, needs no display
# server and is the right thing for a probe that only reads numbers out of a page. It is also
# software: a full-quality WebGL render of the vehicle through it takes minutes and comes out
# without multisampling. Set A3D_GPU=1 for the ANGLE/Vulkan path, which on this machine gives
# a real WebGL 2 context. Anything that captures an image should ask for it; nothing that
# reads a number should.
GPU = os.environ.get("A3D_GPU") == "1"
GL_FLAGS = (["--use-gl=angle", "--use-angle=vulkan", "--enable-gpu"] if GPU
            else ["--disable-gpu", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
WIN = os.environ.get("A3D_WINDOW", "1600,1000")

# THE DEBUG PORT IS THE BROWSER'S OWN. This used to pick a "free" port by binding a socket
# to 0 and releasing it, then handing the number to Chromium — a window in which another
# process could take the port between our release and the browser's bind, the same
# pick-release race the serving side of this repository removed. devtools.page_target
# starts Chromium with --remote-debugging-port=0 and reads back the port the browser
# chose from DevToolsActivePort, so the socket is the browser's from the moment it exists.
FLAGS = ["--hide-scrollbars", *chrome_flags(), *GL_FLAGS, f"--window-size={WIN}"]

async def main(ws_url):
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
        # A3D_VIEWPORT=390x844 emulates a phone. It has to be a device-metrics
        # override rather than --window-size, because Chromium refuses to make a
        # window narrower than 500 px and silently gives you 500 — which reads as a
        # tablet to any media query and quietly tests the wrong layout.
        if os.environ.get("A3D_VIEWPORT"):
            vw, _, vh = os.environ["A3D_VIEWPORT"].partition("x")
            await call("Emulation.setDeviceMetricsOverride", {
                "width": int(vw), "height": int(vh),
                "deviceScaleFactor": 1, "mobile": True})
            await call("Emulation.setTouchEmulationEnabled",
                       {"enabled": True, "maxTouchPoints": 5})
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

try:
    with page_target("chromium", FLAGS, pathlib.Path(TMP.name) / "profile",
                     stderr=_log) as (_proc, ws_url):
        asyncio.run(main(ws_url))
except BrowserFailed as exc:
    # Say what happened, not what it made the next library do. The old code passed None
    # into websockets.connect and the traceback blamed the URI scheme.
    _log.flush()
    tail = LOG.read_text().strip().splitlines()[-25:]
    print(f"js_eval: {exc}", file=sys.stderr)
    print("its stderr:" if tail else "it printed nothing to stderr.", file=sys.stderr)
    for line in tail:
        print("  " + line, file=sys.stderr)
    sys.exit(1)
finally:
    _log.close(); TMP.cleanup()
