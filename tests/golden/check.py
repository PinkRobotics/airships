#!/usr/bin/env python3
"""The regression gate: re-run the page and prove nothing in it moved.

The unit tests in tests/cases assert that the model still makes sense. This asserts
something narrower and harder: that it still produces THE SAME NUMBERS. It serves the
repository, drives a headless browser at

    /?seed=7&data=snapshot

— the seed pins every choice the model makes, the snapshot pins every external input — and
compares two dumps against the files committed in this directory:

    seed7-snapshot.json      every model output: class table, ledger, a grid of planCycle
                             results, the allocated fleet, 240 samples of the state machine
                             per class, the narration, the built-in selftest
    ui-seed7-snapshot.json   what the page RENDERS: panel text, table text, dial counts,
                             a pixel digest of the map canvas

Any difference at all is a failure, including one that is an improvement. Regenerate
deliberately, read the diff, and commit the new baseline in the same change as the code:

    tests/golden/check.py --update

Requires: python3, chromium on PATH, and the `websockets` package (tools/js_eval.py uses
it). No node.

If AIRSHIPS_PORT (or PORT) names a development server that is already listening, this
reuses it — CI starts one for the whole job. Otherwise it serves the repository itself on
a free port and shuts that down on the way out.
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
import threading
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TOOLS = ROOT / "tools"

# (dump script, baseline, how long to let the page settle before evaluating)
TARGETS = [
    ("dump.js", "seed7-snapshot.json", 16),
    ("ui-dump.js", "ui-seed7-snapshot.json", 18),
]
QUERY = "?seed=7&data=snapshot"


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, *a):        # the server is scaffolding, not output
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def answers(port: int) -> bool:
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/sim/index.js", timeout=1).read(1)
        return True
    except (urllib.error.URLError, OSError):
        return False


def existing_server() -> "int | None":
    """Reuse a development server already listening, rather than binding a second one.

    CI starts `tools/serve.py` once for the whole job and expects every driver to use it;
    AIRSHIPS_PORT is how it says which one. Locally there is usually nothing listening and
    this returns None."""
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


def serve(port: int) -> Server:
    httpd = Server(("127.0.0.1", port), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    for _ in range(100):
        if answers(port):
            return httpd
        time.sleep(0.05)
    raise SystemExit("the local server never came up")


def dump(port: int, script: pathlib.Path, out: pathlib.Path, wait: int) -> None:
    """Load the page headless and evaluate `script`, writing its JSON result to `out`."""
    url = f"http://127.0.0.1:{port}/index.html{QUERY}"
    r = subprocess.run(
        [sys.executable, str(TOOLS / "js_eval.py"), url, str(script), str(out), str(wait)],
        cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0 or not out.exists():
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit(f"could not dump {script.name} — the page did not evaluate")
    # Written exactly as js_eval received it, so --update produces a baseline in the same
    # shape as the committed ones. Parsed here only to fail loudly on a truncated dump.
    try:
        json.loads(out.read_text())
    except json.JSONDecodeError as e:
        raise SystemExit(f"{script.name} produced something that is not JSON: {e}")


def diff(baseline: pathlib.Path, candidate: pathlib.Path, tol: str) -> int:
    r = subprocess.run(
        [sys.executable, str(TOOLS / "golden_diff.py"), str(baseline), str(candidate), "--tol", tol],
        capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--update", action="store_true",
                    help="overwrite the baselines with what the page produces now")
    ap.add_argument("--tol", default="0",
                    help="relative tolerance for numeric comparison (default 0: exact)")
    ap.add_argument("--only", choices=["model", "ui"], help="run one of the two dumps")
    ap.add_argument("--keep", action="store_true", help="leave the candidate dumps on disk")
    args = ap.parse_args()

    if shutil.which("chromium") is None:
        raise SystemExit("chromium is not on PATH; the golden gate needs a headless browser")

    targets = TARGETS
    if args.only == "model":
        targets = TARGETS[:1]
    elif args.only == "ui":
        targets = TARGETS[1:]

    port = existing_server()
    httpd = None
    if port is None:
        port = free_port()
        httpd = serve(port)
    else:
        print(f"reusing the development server already listening on {port}")
    failures = []
    try:
        for script_name, baseline_name, wait in targets:
            script = HERE / script_name
            baseline = HERE / baseline_name
            candidate = HERE / (baseline_name.replace(".json", ".candidate.json"))
            print(f"\n=== {baseline_name} " + "=" * (56 - len(baseline_name)))
            dump(port, script, candidate, wait)
            if args.update:
                candidate.replace(baseline)
                print(f"baseline updated: {baseline.relative_to(ROOT)}")
                continue
            if not baseline.exists():
                raise SystemExit(f"no baseline at {baseline}; run with --update to create one")
            rc = diff(baseline, candidate, args.tol)
            if rc != 0:
                failures.append(baseline_name)
            if not args.keep and candidate.exists():
                candidate.unlink()
    finally:
        if httpd is not None:
            httpd.shutdown()

    if args.update:
        print("\nBaselines rewritten. Read the diff before committing them.")
        return 0
    if failures:
        print(f"\nGOLDEN GATE FAILED: {', '.join(failures)}")
        print("Either the change was not meant to alter behaviour, or the baseline needs")
        print("updating in the same commit: tests/golden/check.py --update")
        return 1
    print("\nGOLDEN GATE PASSED: the page produces the committed numbers exactly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
