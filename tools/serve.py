#!/usr/bin/env python3
"""Static file server for local development.

    python3 tools/serve.py                 # http://127.0.0.1:8875
    python3 tools/serve.py --port 9000
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
"""
from __future__ import annotations

import argparse
import functools
import http.server
import pathlib
import sys

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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8875)
    ap.add_argument("--root", default=str(ROOT), help="directory to serve (default: repo root)")
    ap.add_argument("--quiet", action="store_true", help="do not log every request")
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

    base = f"http://127.0.0.1:{args.port}/"
    print(f"serving {root} — no-store, so a reload always gets the file you just saved")
    for name, path in PAGES:
        print(f"  {name}   {base}{path}")
    print(f"  replay          {base}{REPLAY}")
    print("Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
