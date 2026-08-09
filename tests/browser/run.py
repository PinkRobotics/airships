#!/usr/bin/env python3
"""Run the unit suite headless and report it in a terminal.

`make test` calls this. It is a driver, not a second implementation: the assertions are the
same tests/cases/*.cases.js modules that tests/node/run.mjs runs, executed by the same
tests/browser/index.html a person opens in a browser. All this does is load that page in a
headless Chromium, read the record the page leaves on `window.__tests`, print it, and exit
non-zero if anything failed.

    tests/browser/run.py                 # reuse or start a server, run, report
    tests/browser/run.py --verbose       # list every test, not just the failures

If AIRSHIPS_PORT (or PORT) names a server that is already listening, this reuses it — CI
starts one for the whole job. Otherwise it serves the repository itself on a free port.

A "known" result is a test that is expected to fail against a defect that is open and
tracked; see the Known failures section of tests/README.md. Those do not fail the run. A
known-failing test that starts PASSING does, because the marker has to come off.

Requires: python3, chromium on PATH, and the `websockets` package (tools/js_eval.py uses it).
"""
import argparse
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

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TOOLS = ROOT / "tools"

# Read the record the page publishes, waiting for it rather than guessing how long the
# imports take. The page sets window.__tests once, at the end of the run.
GRAB = r"""
(async () => {
  for (let i = 0; i < 300 && !window.__tests; i++) await new Promise(r => setTimeout(r, 100));
  if (!window.__tests) return JSON.stringify({ error: 'the suite never finished', title: document.title });
  return JSON.stringify(window.__tests);
})()
"""


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


GREEN, RED, AMBER, DIM, OFF = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    GREEN = RED = AMBER = DIM = OFF = ""


def report(rec: dict, verbose: bool) -> int:
    for suite in rec["suites"]:
        shown = [t for t in suite["tests"] if verbose or t["status"] != "pass"]
        if not shown:
            continue
        print(f"\n{suite['name']}")
        for t in shown:
            if t["status"] == "pass":
                print(f"  {GREEN}✓{OFF} {DIM}{t['name']}{OFF}")
            elif t["status"] == "known":
                print(f"  {AMBER}✗ {t['name']}{OFF}")
                print(f"    {DIM}known failure — {t['known']}{OFF}")
                print(f"    {DIM}{t['error']}{OFF}")
            else:
                print(f"  {RED}✗ {t['name']}{OFF}")
                print(f"    {t['error']}")

    colour = RED if rec["fail"] else GREEN
    print(f"\n{colour}{rec['pass']} passed, {rec['fail']} failed, {rec['known']} known-failing"
          f"{OFF} — {rec['total']} tests in {len(rec['suites'])} suites, {rec['ms']:.0f} ms")
    return 1 if rec["fail"] else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", "-v", action="store_true", help="list passing tests too")
    ap.add_argument("--wait", type=int, default=4, help="seconds to let the page load (default 4)")
    args = ap.parse_args()

    if shutil.which("chromium") is None:
        raise SystemExit("chromium is not on PATH; the browser suite needs a headless browser")

    port = existing_server()
    httpd = None
    if port is None:
        port = free_port()
        httpd = serve(port)
    else:
        print(f"reusing the development server already listening on {port}")

    try:
        with tempfile.TemporaryDirectory() as tmp:
            script = pathlib.Path(tmp) / "grab.js"
            script.write_text(GRAB)
            out = pathlib.Path(tmp) / "result.json"
            r = subprocess.run(
                [sys.executable, str(TOOLS / "js_eval.py"),
                 f"http://127.0.0.1:{port}/tests/browser/index.html",
                 str(script), str(out), str(args.wait)],
                cwd=str(ROOT), capture_output=True, text=True)
            if r.returncode != 0 or not out.exists():
                sys.stderr.write(r.stdout + r.stderr)
                raise SystemExit("the test page did not run")
            rec = json.loads(out.read_text())
    finally:
        if httpd is not None:
            httpd.shutdown()

    if "error" in rec:
        print(f"{RED}{rec['error']}{OFF} (title was {rec.get('title')!r})")
        return 1
    return report(rec, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
