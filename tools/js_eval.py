#!/usr/bin/env python3
"""Load a URL headless, evaluate a JS file, write the full result to disk.
Usage: evaljs.py URL SCRIPT.js OUT [WAIT_S]"""
import os
import asyncio, json, signal, socket, subprocess, sys, tempfile, time, urllib.request, pathlib

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


def free_port():
    """A port the kernel just told us is free, rather than a number we hope is.

    This used to be a hardcoded 9281, which made two of these collide: the second browser
    found the port taken, quietly served no debuggable page, and the run died pointing at
    the websocket library instead of at the collision.
    """
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


URL, JSFILE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
WAIT = float(sys.argv[4]) if len(sys.argv) > 4 else 14
JS = pathlib.Path(JSFILE).read_text()

PORT = free_port()
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

proc = subprocess.Popen([
    "chromium", "--headless=new", "--hide-scrollbars",
    *chrome_flags(), *GL_FLAGS,
    f"--remote-debugging-port={PORT}", "--remote-allow-origins=*",
    # A profile of its own, in a directory we know is writable. Without this the browser
    # takes the default profile, which a second headless run cannot share and a confined
    # (snap/flatpak) install may not be able to write at all — both of which present as a
    # browser that starts and then never answers on the debug port.
    f"--user-data-dir={TMP.name}/profile",
    f"--window-size={WIN}", "about:blank",
# Its own session, so the browser and every process it forks can be killed as one group.
# Killing the parent alone leaves the zygote and renderers running.
], stdout=subprocess.DEVNULL, stderr=_log, start_new_session=True)

async def main():
    ws_url = None
    deadline = time.monotonic() + 60          # a cold runner is slower than a warm desktop
    while time.monotonic() < deadline:
        if proc.poll() is not None:           # died: stop waiting for a page it cannot open
            break
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
            pages = [t for t in tabs if t["type"] == "page"]
            if pages:
                ws_url = pages[0]["webSocketDebuggerUrl"]; break
        except Exception: pass
        time.sleep(0.2)
    if ws_url is None:
        # Say what happened, not what it made the next library do. The old code passed None
        # into websockets.connect and the traceback blamed the URI scheme.
        _log.flush()
        why = "exited with code %s" % proc.returncode if proc.poll() is not None \
            else "was still running but never opened a debuggable page"
        tail = LOG.read_text().strip().splitlines()[-25:]
        print(f"chromium {why} within 60 s on port {PORT}", file=sys.stderr)
        print("its stderr:" if tail else "it printed nothing to stderr.", file=sys.stderr)
        for line in tail:
            print("  " + line, file=sys.stderr)
        sys.exit(1)
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
finally:
    try: os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError): proc.kill()
    proc.wait()
    _log.close(); TMP.cleanup()
