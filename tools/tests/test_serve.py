"""Unit tests for tools/serve.py — the one way a gate serves a directory.

They cover the contract the gates rely on: serve_tree() yields a base address that is
really bound and serves the directory it was asked to serve; the port closes when the
block ends, whether it ends by return or by raise; a driver's own handler class passes
through; the default responses are no-store; and the CLI form binds port 0 when asked,
reports the address it bound, and stops on SIGTERM.
"""
from __future__ import annotations

import socket
import selectors
import http.server
import pathlib
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import serve  # noqa: E402


def fetch(base, path="/"):
    """GET {base}{path} with caching headers a browser might send; return (status, headers)."""
    req = urllib.request.Request(base.rstrip("/") + path,
                                 headers={"If-Modified-Since": "Mon, 01 Jan 2024 00:00:00 GMT"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, dict(resp.headers)


def port_is_closed(base):
    """Refusal proves closure; an HTTP error or timeout does not."""
    from urllib.parse import urlsplit
    address = urlsplit(base)
    try:
        with socket.create_connection((address.hostname, address.port), timeout=1):
            return False
    except ConnectionRefusedError:
        return True


class ServeTree(unittest.TestCase):
    def test_two_servers_two_dirs_two_ports(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            (pathlib.Path(a) / "probe.txt").write_text("alpha\n")
            (pathlib.Path(b) / "probe.txt").write_text("beta\n")
            with serve.serve_tree(a) as base_a, serve.serve_tree(b) as base_b:
                self.assertNotIn(":0/", base_a)
                self.assertNotEqual(base_a, base_b)
                status, _ = fetch(base_a, "/probe.txt")
                self.assertEqual(status, 200)
                with urllib.request.urlopen(base_a + "/probe.txt", timeout=10) as resp:
                    self.assertEqual(resp.read(), b"alpha\n")
                with urllib.request.urlopen(base_b + "/probe.txt", timeout=10) as resp:
                    self.assertEqual(resp.read(), b"beta\n")

    def test_port_closes_on_exit(self):
        with tempfile.TemporaryDirectory() as d:
            with serve.serve_tree(d) as base:
                self.assertEqual(fetch(base)[0], 200)
        self.assertTrue(port_is_closed(base), f"still listening after the block: {base}")

    def test_port_closes_on_raise(self):
        base = None
        with self.assertRaises(RuntimeError):
            with serve.serve_tree() as b:
                base = b
                raise RuntimeError("gate failed mid-run")
        self.assertIsNotNone(base)
        self.assertTrue(port_is_closed(base), f"still listening after a raise: {base}")

    def test_custom_handler_passes_through(self):
        class Fixture(http.server.BaseHTTPRequestHandler):
            hits = []

            def do_GET(self):
                Fixture.hits.append(self.path)
                body = b"fixture says no"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        Fixture.hits = []
        with serve.serve_tree(handler=Fixture) as base:
            with urllib.request.urlopen(base + "/anything/at/all", timeout=10) as resp:
                self.assertEqual(resp.read(), b"fixture says no")
        self.assertEqual(Fixture.hits, ["/anything/at/all"])

    def test_no_store_is_the_default(self):
        with tempfile.TemporaryDirectory() as d:
            (pathlib.Path(d) / "page.html").write_text("<!doctype html><p>hi</p>\n")
            with serve.serve_tree(d) as base:
                status, headers = fetch(base, "/page.html")
        self.assertEqual(status, 200)
        self.assertIn("no-store", headers.get("Cache-Control", ""))
        # A conditional header must not turn the answer into a 304 (the browser reusing
        # a stale ES module is the failure this header exists to prevent).
        self.assertNotIn("304", str(status))


class Cli(unittest.TestCase):
    """`tools/serve.py --port 0` — the shell caller's half of the same contract."""

    def test_port_zero_prints_and_binds_then_stops_on_term(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = pathlib.Path(scratch) / "tree"
            root.mkdir()
            (root / "probe.txt").write_text("cli\n")
            addr_file = pathlib.Path(scratch) / "addr"
            proc = subprocess.Popen(
                [sys.executable, str(serve.ROOT / "tools" / "serve.py"),
                 "--root", str(root), "--port", "0", "--quiet",
                 "--addr-file", str(addr_file)],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            try:
                base = None
                deadline = time.monotonic() + 30
                while time.monotonic() < deadline:
                    if addr_file.exists():
                        base = addr_file.read_text().strip()
                        break
                    self.assertIsNone(proc.poll(), "serve.py exited before binding")
                    time.sleep(0.05)
                self.assertIsNotNone(base, "no address written within 30s")
                self.assertTrue(base.startswith("http://127.0.0.1:"), base)
                self.assertNotIn(":0/", base)                    # the system chose a real port
                with urllib.request.urlopen(base + "/probe.txt", timeout=10) as resp:
                    self.assertEqual(resp.read(), b"cli\n")
                with selectors.DefaultSelector() as ready:
                    ready.register(proc.stdout, selectors.EVENT_READ)
                    self.assertTrue(ready.select(5), "CLI did not print its bound address")
                    first_line = proc.stdout.readline().strip()
            finally:
                proc.terminate()
                out = proc.communicate(timeout=10)[0]
            self.assertIsNotNone(proc.returncode)
            self.assertTrue(port_is_closed(base), f"CLI still listening after TERM: {base}")
            # First line names the address that was really bound — the fact, not a guess.
            self.assertIn("listening on", first_line)
            self.assertIn(base, first_line + out)


    def test_wrapper_preserves_failure_and_closes_server(self):
        result = subprocess.run(
            [sys.executable, str(serve.ROOT / 'tools/with_server.py'), '--',
             sys.executable, '-c',
             'import sys, urllib.request; '
             'urllib.request.urlopen(sys.argv[1], timeout=5).close(); '
             'print(sys.argv[1]); sys.exit(17)', '{base}'],
            capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 17, result.stderr)
        base = result.stdout.strip()
        self.assertTrue(base.startswith('http://127.0.0.1:'))
        self.assertTrue(port_is_closed(base))


if __name__ == "__main__":
    unittest.main()
