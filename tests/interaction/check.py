#!/usr/bin/env python3
"""Interaction regression: use the page, and prove it is still running afterwards.

WHY THIS EXISTS, precisely. Clicking a fire that no ship had been assigned to threw a
TypeError inside the map's `draw()`. `draw()` is called from the animation frame, and the
frame asks for the next one AFTER it returns, so the exception did not cost one frame: it
stopped the loop. The map froze, the clock stopped, the instruments stopped, the energy
ledger stopped integrating, and the page went on looking exactly like a page that works,
for the rest of the session. Every test in this repository asserted what the model
COMPUTES. Nothing asserted what the page does when somebody touches it, so nothing failed.

This driver touches things. It loads

    /index.html?seed=7&data=snapshot

in a headless browser, installs an error trap before the page's first line runs, and then
performs real interactions — mouse events through the debugger's input domain for the map,
real clicks on real controls elsewhere. After each one it asks two questions:

    did anything throw?                 window.__ierr, filled by the trap
    is the frame loop still turning?    S.lastFrame, which the loop writes every frame

`S.lastFrame` is the witness because it is the loop's own heartbeat and nothing else writes
it. A counter the test installed on requestAnimationFrame would be no witness at all: rAF
goes on working perfectly after the page's loop has died, which is exactly why the original
defect was invisible. `S.lastFrame` advances whether or not the clock is paused, so the
same check holds over the pause and speed steps.

Steps that have a checkable EFFECT are checked for it: the click on empty map must clear the
selection, the click on an unassigned fire must select that fire with no ship attached. Those
assertions are what stop this from becoming a test that cannot fail — a driver whose
synthetic clicks quietly landed nowhere would otherwise report a clean pass forever.

To confirm it has teeth, put the defect back — in app/map/render.js, the fire-selection
guard `(S.sel.f || (S.sel.m && S.sel.m.fire))` reverted to `S.sel.m.fire` — and run this.
The step named "map: click a fire with no ship assigned" must go red.

    tests/interaction/check.py             # run it
    tests/interaction/check.py -v          # print the numbers behind every step
    tests/interaction/check.py --settle 800

Requires: python3, chromium on PATH, and the `websockets` package (as tools/js_eval.py
does). No node. If AIRSHIPS_PORT (or PORT) names a development server that is already
listening this reuses it, as the other drivers do; otherwise it serves the repository
itself on a free port. The browser runs on a throwaway profile under the system temporary
directory; AIRSHIPS_TMPDIR moves that elsewhere, which is worth doing where /tmp is a RAM
disk or where a confined browser package cannot reach it.

Unlike tests/golden/check.py and tests/browser/run.py, this cannot shell out to
tools/js_eval.py: that evaluates one script and exits, and an interaction test needs to
act, observe, and act again in one live session. So it speaks the debugger protocol
directly, on a port of its own — two of these, or one of these and a golden run, do not
collide.
"""
import argparse
import asyncio
import http.server
import json
import os
import pathlib
import shutil
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request

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


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
QUERY = "?seed=7&data=snapshot"
CHROME = os.environ.get("CHROME", "chromium")

GREEN, RED, AMBER, DIM, OFF = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    GREEN = RED = AMBER = DIM = OFF = ""


# ---------- the server: the same arrangement as tests/golden/check.py ---------------------

def answers(port: int) -> bool:
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/sim/index.js", timeout=1).read(1)
        return True
    except (urllib.error.URLError, OSError):
        return False


def existing_server():
    for var in ("AIRSHIPS_PORT", "PORT"):
        raw = os.environ.get(var)
        if not raw:
            continue
        try:
            port = int(raw)
        except ValueError:
            continue
        if answers(port):
            return port
    return None


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, *a):
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def serve(port: int) -> Server:
    httpd = Server(("127.0.0.1", port), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    for _ in range(100):
        if answers(port):
            return httpd
        time.sleep(0.05)
    raise SystemExit("the local server never came up")


# ---------- the trap and the survival probe ------------------------------------------------

# Installed before the page's first line, so an exception thrown during boot is caught too.
#
# The listener is NOT registered with capture. A resource that fails to load fires an error
# event at its element and does not bubble, so only uncaught script errors reach window this
# way — which is what we want: the basemap's tiles come from a third-party host that a
# headless run has no reason to reach, and a missing tile is not a defect in this page.
TRAP = r"""
window.__ierr = [];
window.addEventListener('error', (e) => {
  window.__ierr.push(String(e.message || e.error || 'error'));
});
window.addEventListener('unhandledrejection', (e) => {
  const r = e.reason;
  window.__ierr.push('unhandled rejection: ' + ((r && r.message) || String(r)));
});
"""

# Sample the loop's heartbeat, wait, sample it again. Everything else in the returned record
# is context for the report; `alive` and `errs` are the verdict.
PROBE = r"""
(async (mark, settle) => {
  const S = window.AIRSHIPS && window.AIRSHIPS.app;
  const errs = () => (window.__ierr || []).slice(mark);
  if (!S) return { alive: false, why: 'window.AIRSHIPS is gone', errs: errs() };
  const f0 = S.lastFrame, t0 = S.simTime;
  await new Promise((r) => setTimeout(r, settle));
  const hud = document.getElementById('hudClock');
  return {
    alive: typeof S.lastFrame === 'number' && S.lastFrame > f0,
    frameMs: typeof S.lastFrame === 'number' && typeof f0 === 'number' ? S.lastFrame - f0 : null,
    simAdvance: S.simTime - t0,
    paused: !!S.paused,
    speed: S.speed,
    clock: hud ? hud.textContent : null,
    sel: S.sel ? { type: S.sel.type, ship: !!S.sel.m, fire: !!S.sel.f } : null,
    errs: errs(),
  };
})(%(mark)d, %(settle)d)
"""

# Wait for the fleet to exist rather than guessing at a number of seconds, then get the
# first-visit overlay out of the way — it covers the whole viewport and would swallow every
# click that follows. Dismissing it is itself the first interaction the page expects.
BOOT = r"""
(async () => {
  const t0 = Date.now();
  while (Date.now() - t0 < 90000) {
    const S = window.AIRSHIPS && window.AIRSHIPS.app;
    if (S && S.ready && S.missions.length) break;
    await new Promise((r) => setTimeout(r, 250));
  }
  const S = window.AIRSHIPS && window.AIRSHIPS.app;
  if (!S || !S.ready) return { ready: false, errs: window.__ierr || [] };
  const ov = document.getElementById('introOv');
  if (ov && !ov.hidden) ov.click();
  await new Promise((r) => setTimeout(r, 400));
  return {
    ready: true,
    fires: S.fires.length,
    flying: S.missions.filter((m) => !m.idle).length,
    unassigned: S.fires.filter((f) => !f.mission || f.mission.idle).length,
    rosterRows: document.querySelectorAll('#roster tr.r-ship').length,
    systemsButtons: [...document.querySelectorAll('[data-m3s]')].map((b) => b.dataset.m3s),
    model3d: !!document.querySelector('#m3dView canvas'),
    overlay: !!(ov && ov.hidden === false),
    errs: window.__ierr || [],
  };
})()
"""

# Put a chosen fire under the centre of the map, so the click that follows is aimed at a
# known target. `mercY` is the projection the page uses, four lines of it, repeated here
# rather than reached for: app/ is not importable from a page-level driver.
CENTRE_ON_FIRE = r"""
((wantShip) => {
  const S = window.AIRSHIPS.app;
  const mercY = (lat) => -Math.asinh(Math.tan(lat * Math.PI / 180)) * 180 / Math.PI;
  const has = (f) => !!(f.mission && !f.mission.idle);
  const pool = S.fires.filter((f) => has(f) === wantShip);
  if (!pool.length) return { found: false };
  // Largest first, ties broken on the fire number, so one snapshot always picks one fire.
  pool.sort((a, b) => (b.sizeHa - a.sizeHa) || (a.id < b.id ? -1 : 1));
  const f = pool[0];
  S.follow = false;                       // or the followed ship recentres us next frame
  S.view.cx = f.ll[0];
  S.view.cy = mercY(f.ll[1]);
  S.view.k = 900;
  return { found: true, id: f.id, name: f.name || null, sizeHa: f.sizeHa, pool: pool.length };
})(%(want)s)
"""

# Somewhere with nothing on it: five degrees of longitude east of the easternmost fire is
# outside British Columbia, and at this zoom every fire, ship, route and lake is thousands
# of pixels off-screen. Deterministic, unlike hunting for a gap between the markers.
CENTRE_ON_NOTHING = r"""
(() => {
  const S = window.AIRSHIPS.app;
  S.follow = false;
  S.view.cx = Math.max(...S.fires.map((f) => f.ll[0])) + 5;
  S.view.k = 900;
  return { cx: S.view.cx, cy: S.view.cy, k: S.view.k };
})()
"""

TWO_FRAMES = "new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))"

MAP_RECT = r"""
(() => {
  const r = document.getElementById('map').getBoundingClientRect();
  return { x: r.left, y: r.top, w: r.width, h: r.height };
})()
"""


# ---------- the debugger session -----------------------------------------------------------

class Page:
    """One live page over the DevTools protocol: evaluate, and dispatch real input."""

    def __init__(self, ws):
        self.ws = ws
        self.mid = 0

    async def call(self, method, params=None):
        self.mid += 1
        await self.ws.send(json.dumps({"id": self.mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(await self.ws.recv())
            if msg.get("id") == self.mid:
                if "error" in msg:
                    raise SystemExit(f"{method} failed: {msg['error']}")
                return msg.get("result", {})

    async def wait_event(self, method, timeout=60):
        """Read the stream until `method` arrives.

        Only safe with no call outstanding, which is the one place it is used: between
        Page.navigate returning and the first evaluate. Evaluating before the new document
        has a context is how a driver ends up quietly interrogating about:blank."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            try:
                raw = await asyncio.wait_for(self.ws.recv(), timeout=end - time.monotonic())
            except asyncio.TimeoutError:
                break
            msg = json.loads(raw)
            if msg.get("method") == method:
                return msg.get("params", {})
        raise SystemExit(f"the page never reported {method}")

    async def eval(self, expression):
        r = await self.call("Runtime.evaluate",
                            {"expression": expression, "returnByValue": True,
                             "awaitPromise": True})
        if "exceptionDetails" in r:
            det = r["exceptionDetails"]
            text = (det.get("exception") or {}).get("description") or det.get("text")
            raise SystemExit(f"the driver's own script threw: {text}\n{expression[:200]}")
        return r.get("result", {}).get("value")

    async def click(self, x, y):
        """A real left click at viewport coordinates, through the input domain.

        Not a synthesised PointerEvent: the map captures the pointer on pointerdown, and
        setPointerCapture throws for a pointer id that no real input ever created. A
        dispatched event would abort the handler and the click would never reach the map —
        the test would pass by not testing."""
        base = {"x": x, "y": y, "button": "left", "clickCount": 1}
        await self.call("Input.dispatchMouseEvent", dict(base, type="mouseMoved", buttons=0))
        await self.call("Input.dispatchMouseEvent", dict(base, type="mousePressed", buttons=1))
        await self.call("Input.dispatchMouseEvent", dict(base, type="mouseReleased", buttons=0))


class Run:
    """The step list and its verdicts."""

    def __init__(self, page, settle, verbose):
        self.page = page
        self.settle = settle
        self.verbose = verbose
        self.results = []

    async def step(self, name, action, expect=None):
        """Perform `action`, then require the page to be alive and quiet afterwards.

        `expect(probe)` returns None, or a string saying what it wanted instead — that is
        where a step asserts its own effect happened at all."""
        mark = await self.page.eval("(window.__ierr || []).length")
        detail = await action()
        probe = await self.page.eval(PROBE % {"mark": mark, "settle": self.settle})
        why = None
        if probe.get("errs"):
            why = "threw: " + "; ".join(probe["errs"][:3])
        elif not probe.get("alive"):
            why = ("the frame loop stopped — " + probe.get("why", "S.lastFrame did not advance")
                   + f" over {self.settle} ms")
        elif expect is not None:
            why = expect(probe)
        self.results.append({"name": name, "ok": why is None, "why": why,
                             "detail": detail, "probe": probe})
        tick = f"{GREEN}✓{OFF}" if why is None else f"{RED}✗{OFF}"
        print(f"  {tick} {name}" if why is None else f"  {tick} {name}\n    {RED}{why}{OFF}")
        if self.verbose:
            print(f"    {DIM}{json.dumps(detail)} · {json.dumps(probe)}{OFF}")

    async def click_control(self, name, selector, index=0):
        async def act():
            got = await self.page.eval(
                f"(() => {{ const e = document.querySelectorAll({selector!r})[{index}];"
                f" if (!e) return null; e.click(); return e.textContent.trim().slice(0, 40); }})()")
            if got is None:
                raise SystemExit(f"no element matched {selector} [{index}] — the page's "
                                 "markup moved and this test is asserting nothing")
            return {"clicked": got}
        await self.step(name, act)

    async def click_map_centre(self, name, expect=None):
        async def act():
            rect = await self.page.eval(MAP_RECT)
            await self.page.eval(TWO_FRAMES)          # let the staged view actually draw
            x = rect["x"] + rect["w"] / 2
            y = rect["y"] + rect["h"] / 2
            await self.page.click(x, y)
            return {"at": [round(x, 1), round(y, 1)], "map": rect}
        await self.step(name, act, expect)


# ---------- the steps ------------------------------------------------------------------------

async def drive(url: str, settle: int, verbose: bool) -> int:
    import websockets                       # imported late, as tools/js_eval.py does

    port = free_port()
    # ignore_cleanup_errors for the same reason tools/js_eval.py has it: Chromium's children
    # outlive the process we kill and can still be writing into the profile when the directory
    # is removed, which failed a CI run whose actual work had already succeeded.
    with tempfile.TemporaryDirectory(dir=os.environ.get("AIRSHIPS_TMPDIR") or None,
                                     ignore_cleanup_errors=True) as tmp:
        # A profile of its own: a browser sharing the default one with another headless run
        # refuses to start, and a fresh profile is also what makes the run reproducible —
        # empty localStorage means the first-visit overlay and the default map/model split.
        proc = subprocess.Popen([
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            *chrome_flags(),
            f"--remote-debugging-port={port}", "--remote-allow-origins=*",
            f"--user-data-dir={tmp}/profile",
            "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
            "--window-size=1600,1000", "about:blank",
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            return await session(websockets, port, url, settle, verbose)
        finally:
            proc.kill()


async def session(websockets, port, url, settle, verbose) -> int:
    ws_url = None
    for _ in range(100):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
            pages = [t for t in tabs if t["type"] == "page"]
            if pages:
                ws_url = pages[0]["webSocketDebuggerUrl"]
                break
        except Exception:
            pass
        time.sleep(0.2)
    if ws_url is None:
        raise SystemExit(f"{CHROME} never opened a debuggable page on {port}")

    async with websockets.connect(ws_url, max_size=64_000_000) as ws:
        page = Page(ws)
        await page.call("Page.enable")
        await page.call("Runtime.enable")
        await page.call("Page.addScriptToEvaluateOnNewDocument", {"source": TRAP})
        await page.call("Page.navigate", {"url": url})
        await page.wait_event("Page.loadEventFired")

        boot = await page.eval(BOOT)
        if not boot.get("ready"):
            print(f"{RED}the page never finished booting{OFF}: {json.dumps(boot)[:400]}")
            return 1
        print(f"booted: {boot['fires']} fires, {boot['flying']} flying, "
              f"{boot['unassigned']} of the fires unworked, {boot['rosterRows']} roster rows, "
              f"3D model {'mounted' if boot['model3d'] else 'ABSENT'}")
        if boot["errs"]:
            print(f"{RED}the page threw while booting{OFF}: {boot['errs'][:3]}")
            return 1
        # Both of these would leave steps below asserting nothing at all, quietly.
        if not boot["unassigned"]:
            print(f"{RED}no fire in this snapshot is without a ship{OFF} — the step this "
                  "whole file exists for cannot be performed")
            return 1
        if not boot["model3d"]:
            print(f"{RED}the 3D model did not mount{OFF} — the systems-button steps would "
                  "click through a handler that returns immediately and prove nothing")
            return 1

        run = Run(page, settle, verbose)
        print("\ninteractions")

        # 1. The regression itself. A fire with no ship: the selection carries `f` and no
        #    `m`, and until this week the map's draw dereferenced `S.sel.m.fire`.
        async def stage_free_fire():
            got = await page.eval(CENTRE_ON_FIRE % {"want": "false"})
            if not got.get("found"):
                raise SystemExit("no unworked fire to aim at")
            return got
        staged = await stage_free_fire()
        print(f"  {DIM}aiming at fire {staged['id']} ({staged['sizeHa']} ha), "
              f"no ship assigned{OFF}")
        await run.click_map_centre(
            "map: click a fire with no ship assigned",
            lambda p: None if (p["sel"] and p["sel"]["type"] == "fire" and not p["sel"]["ship"])
            else f"expected a fire selected with no ship, got {p['sel']}")

        # 2. The other side of the same branch: a fire a ship IS working selects the ship.
        worked = await page.eval(CENTRE_ON_FIRE % {"want": "true"})
        if worked.get("found"):
            await run.click_map_centre(
                "map: click a fire a ship is working",
                lambda p: None if (p["sel"] and p["sel"]["type"] == "ship" and p["sel"]["ship"])
                else f"expected the working ship selected, got {p['sel']}")

        # 3. The roster: a row is a click target with its own selection path.
        await run.click_control("roster: click a ship row", "#roster tr.r-ship", 0)
        await run.click_control("roster: click another ship row", "#roster tr.r-ship", 1)

        # 4. Every 3D systems button, in the order they sit on the page. "custom" is last
        #    and is the one that threw until this week.
        for i, key in enumerate(boot["systemsButtons"]):
            await run.click_control(f"3D systems: {key}", "[data-m3s]", i)

        # 5. The custom panel's own controls, which only do anything once "custom" is on.
        async def custom_view():
            return {"view": await page.eval(
                "(() => { const s = document.getElementById('m3cView');"
                " const other = [...s.options].map(o => o.value).find(v => v !== s.value);"
                " if (!other) return null; s.value = other;"
                " s.dispatchEvent(new Event('change')); return other; })()")}
        await run.step("3D custom: change the base view", custom_view)

        async def custom_cut():
            return {"cut": await page.eval(
                "(() => { const r = document.getElementById('m3cCut');"
                " r.value = String(Math.min(+r.max, +r.value + (+r.max - +r.min) * 0.3));"
                " r.dispatchEvent(new Event('input')); return r.value; })()")}
        await run.step("3D custom: drag the cut plane", custom_cut)
        await run.click_control("3D custom: switch off a system category", "[data-m3cat]", 0)

        # 6. The split flips the map and the model between stacked and side by side, which
        #    resizes the map canvas under the running loop. Which one it starts in depends
        #    on the window's shape (main.js), so the steps are named for the flip, not for
        #    the arrangement they land in.
        await run.click_control("layout: flip the map and the model", "#btnSplit")
        await run.click_control("layout: flip them back", "#btnSplit")

        # 7. The clock. `S.lastFrame` advances while paused — the loop still runs, it just
        #    stops adding to sim time — so the survival check means the same thing here.
        await run.click_control("clock: pause", "#btnPause")
        await run.step("clock: paused, and sim time is not advancing",
                       lambda: asyncio.sleep(0, result={}),
                       lambda p: None if p["paused"] and p["simAdvance"] == 0
                       else f"expected a stopped clock, got paused={p['paused']} "
                            f"advance={p['simAdvance']}")
        await run.click_control("clock: resume", "#btnPause")
        await run.click_control("clock: 60×", '[data-speed="60"]')
        await run.step("clock: running at 60×",
                       lambda: asyncio.sleep(0, result={}),
                       lambda p: None if (not p["paused"] and p["speed"] == 60
                                          and p["simAdvance"] > 0)
                       else f"expected sim time to advance at 60×, got {p['simAdvance']} s "
                            f"at {p['speed']}×")
        await run.click_control("clock: 5×", '[data-speed="5"]')

        # 8. The map with nothing under the pointer: the deselect path, and the proof that
        #    these clicks are reaching the canvas at all.
        empty = await page.eval(CENTRE_ON_NOTHING)
        print(f"  {DIM}aiming at empty map at {empty['cx']:.1f}°E{OFF}")
        await run.click_map_centre(
            "map: click the background",
            lambda p: None if p["sel"] is None
            else f"expected the selection cleared, got {p['sel']} — either the click missed "
                 "the canvas or something was drawn where nothing should be")

        failed = [r for r in run.results if not r["ok"]]
        colour = RED if failed else GREEN
        print(f"\n{colour}{len(run.results) - len(failed)} survived, {len(failed)} failed"
              f"{OFF} — {len(run.results)} interactions")
        if failed:
            print("\nThe page stopped working when someone used it. The frame loop requests"
                  "\nits successor after draw() returns, so anything that throws inside a"
                  "\ndraw takes the clock, the instruments and the ledger down with it.")
        return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--settle", type=int, default=500,
                    help="ms to watch the frame loop after each interaction (default 500)")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="print what each step did and what the page looked like afterwards")
    args = ap.parse_args()

    if shutil.which(CHROME) is None:
        raise SystemExit(f"{CHROME} is not on PATH; this test needs a headless browser")

    port = existing_server()
    httpd = None
    if port is None:
        port = free_port()
        httpd = serve(port)
    else:
        print(f"reusing the development server already listening on {port}")
    url = f"http://127.0.0.1:{port}/index.html{QUERY}"
    try:
        return asyncio.run(drive(url, args.settle, args.verbose))
    finally:
        if httpd is not None:
            httpd.shutdown()


if __name__ == "__main__":
    sys.exit(main())
