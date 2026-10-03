#!/usr/bin/env python3
"""Static file server for local development, and the one way a gate serves a directory.

    python3 tools/serve.py                 # http://127.0.0.1:8875
    python3 tools/serve.py --port 0        # the system chooses; the address bound is printed
    python3 tools/serve.py --root DIR      # default: the repository root

`python3 -m http.server` almost works. It gets three things wrong for this repository, and
the first one costs an hour before you notice it.

CACHING, WHICH BITES HARDEST WITH ES MODULES. There is no build step here: the modules the
browser executes are the files on disk. `http.server` sends `Last-Modified`, answers
`If-Modified-Since` with a 304, and sends no `Cache-Control` at all — which licenses the
browser to guess at freshness and reuse a response without asking. A module graph is worse
than an ordinary asset because it is fetched once and then held in the realm's module map:
edit sim/physics.js, reload, and Chromium can re-execute the copy it already had. You are
then reading one file and debugging another, and the symptom is that your change "did
nothing". This server sends `Cache-Control: no-store` and drops conditional-request headers
before they can produce a 304, so a reload always runs what you just saved. It is the same
defect that 3d/scripts/browser-tests.sh works around with `--disk-cache-size=1`.

MIME TYPES. A `<script type="module">` is refused outright unless it arrives with a
JavaScript MIME type, and `mimetypes` answers from the host's /etc/mime.types, which is not
the same file on every machine — .mjs, .json, .wasm and .webp are the ones that go missing.
They are pinned below so that "works on my machine" is not a property of the machine's mime
database.

BIND ADDRESS. `http.server` listens on 0.0.0.0, which puts your working tree on whatever
network you are attached to. This binds the loopback interface only.

serve_tree() is the context manager for automated callers. It binds a system-chosen
port once, yields its base address, and closes the socket when the caller finishes.
"""
from __future__ import annotations

import argparse
import contextlib
import functools
import http.server
import pathlib
import sys
import signal
import threading

ROOT = pathlib.Path(__file__).resolve().parent.parent

# What is worth opening, in the order you usually want them.
PAGES = [
    ("fleet monitor", "index.html"),
    ("how it works ", "concept/"),
    ("3D model lab ", "model-lab/"),
]

# The deterministic run: ?seed= pins the model's choices, ?data=snapshot pins its inputs.
# Printed because it is the URL every bug report and every golden comparison should use.
REPLAY = "index.html?seed=7&data=snapshot"


class Handler(http.server.SimpleHTTPRequestHandler):
    # Consulted before mimetypes, so these win regardless of the host's mime database.
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".json": "application/json",
        ".geojson": "application/json",
        ".map": "application/json",
        ".css": "text/css",
        ".html": "text/html",
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
        ".wasm": "application/wasm",
    }

    def send_head(self):
        # A 304 is a correct answer to a question this server does not want asked. Remove
        # the conditional headers before the base class can act on them.
        for header in ("If-Modified-Since", "If-None-Match"):
            del self.headers[header]
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_request(self, code="-", size="-"):
        if not self.server.quiet:                              # type: ignore[attr-defined]
            sys.stderr.write(f"  {self.command} {self.path} -> {getattr(code, 'value', code)}\n")

    def log_error(self, fmt, *args):
        # Kept even under --quiet: a 404 on a module is the thing you are looking for.
        sys.stderr.write(f"  {self.command} {self.path} -- {fmt % args}\n")


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    quiet = False


@contextlib.contextmanager
def serve_tree(root=None, handler=None):
    """Serve a directory on a port the system chose, for the length of the block.

    Yields "http://127.0.0.1:<port>/" from the listening socket itself. The server
    constructor binds and listens before the serving thread starts; no port is
    released and rebound, and no readiness delay is needed.

    `handler` defaults to this module's no-store Handler over `root` (the repository root
    by default). A driver with its own request handler — one that injects failures, or
    serves fixtures — passes its handler class instead, exactly as http.server accepts it.

    The server is stopped on the way out, including when the block raises.
    """
    if handler is None:
        root = pathlib.Path(root or ROOT).resolve()
        handler = functools.partial(Handler, directory=str(root))
    httpd = Server(("127.0.0.1", 0), handler)
    httpd.quiet = True
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    try:
        thread.start()
        yield f"http://127.0.0.1:{httpd.server_address[1]}/"
    finally:
        if thread.is_alive():
            httpd.shutdown()
            thread.join()
        httpd.server_close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8875)
    ap.add_argument("--root", default=str(ROOT), help="directory to serve (default: repo root)")
    ap.add_argument("--quiet", action="store_true", help="do not log every request")
    ap.add_argument("--addr-file", type=pathlib.Path,
                    help="write the bound base address here once listening (for scripts)")
    args = ap.parse_args()

    root = pathlib.Path(args.root).resolve()
    if not root.is_dir():
        print(f"serve: not a directory: {root}", file=sys.stderr)
        return 2

    handler = functools.partial(Handler, directory=str(root))
    try:
        httpd = Server(("127.0.0.1", args.port), handler)
    except OSError as exc:
        print(f"serve: cannot bind 127.0.0.1:{args.port} — {exc}", file=sys.stderr)
        print("       something is already listening there; pass --port to move.", file=sys.stderr)
        return 1
    httpd.quiet = args.quiet

    # server_address carries the port the system chose when --port was 0, and the port
    # asked for otherwise: one expression, and --port 0 prints the truth.
    base = f"http://127.0.0.1:{httpd.server_address[1]}/"
    print(f"listening on {base}", flush=True)
    if args.addr_file:
        pending = args.addr_file.with_name(args.addr_file.name + ".pending")
        pending.write_text(base + "\n")
        pending.replace(args.addr_file)
    print(f"serving {root} — no-store, so a reload always gets the file you just saved")
    for name, path in PAGES:
        print(f"  {name}   {base}{path}")
    print(f"  replay          {base}{REPLAY}")
    print("Ctrl-C to stop.")
    def stop(_signum, _frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
