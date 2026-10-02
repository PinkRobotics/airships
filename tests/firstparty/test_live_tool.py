"""The live inspector is exercised only against a loopback edge imitation."""
import contextlib
import http.server
import io
from pathlib import Path
import sys
import threading
import unittest
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from check_first_party import Loads, inspect, main


class Edge(http.server.BaseHTTPRequestHandler):
    requests = []

    def log_message(self, *args):
        pass

    def do_GET(self):
        Edge.requests.append((self.headers.get('User-Agent', ''), self.headers.get('Accept', '')))
        browser = 'Chrome/' in self.headers.get('User-Agent', '') and 'text/html' in self.headers.get('Accept', '')
        body = '<html><body>clean'
        if browser:
            body += {
                '/': '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js"></script>',
                '/module': '<script type="module" src="https://edge-module.invalid/beacon.js"></script>',
                '/fetch': '<script>fetch("https://edge-fetch.invalid/ping").catch(() => {});</script>',
                '/image-set': '<style>body {background: image-set("https://edge-image.invalid/x" 1x)}</style>',
                '/clean': '<script>fetch("/data/local.json"); const u="http://127.0.0.1/ok";</script>',
            }[self.path]
        body += '</body></html>'
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        if browser:
            self.send_header('report-to', '{"group":"edge"}')
            self.send_header('nel', '{"report_to":"edge"}')
        self.end_headers()
        self.wfile.write(body.encode())


class LiveToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Edge)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.address = f'http://127.0.0.1:{cls.server.server_port}/'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        Edge.requests.clear()

    def test_browser_request_finds_injected_module_and_reporting_headers(self):
        foreign, headers = inspect(self.address)
        self.assertEqual(len(Edge.requests), 1)
        self.assertIn('Chrome/', Edge.requests[0][0])
        self.assertIn('text/html', Edge.requests[0][1])
        self.assertEqual([host for host, _, _ in foreign], ['static.cloudflareinsights.com'])
        self.assertEqual(foreign[0][1], 'script[src]')
        self.assertEqual(headers['report-to'], ['{"group":"edge"}'])
        self.assertEqual(headers['nel'], ['{"report_to":"edge"}'])

    def test_plain_request_would_miss_it_and_cli_fails_closed(self):
        with urlopen(self.address) as response:
            self.assertNotIn(b'cloudflareinsights', response.read())
            self.assertIsNone(response.headers.get('report-to'))
        self.assertEqual(len(Edge.requests), 1)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            result = main([self.address])
        self.assertEqual(result, 1)
        self.assertIn('FOREIGN static.cloudflareinsights.com', out.getvalue())
        self.assertIn('report-to: {"group":"edge"}', out.getvalue())
        self.assertEqual(len(Edge.requests), 2)

    def test_both_browser_injections_and_image_set_fail_the_cli(self):
        for path, host, source in [
            ('module', 'edge-module.invalid', 'script[src]'),
            ('fetch', 'edge-fetch.invalid', 'named in an inline script'),
            ('image-set', 'edge-image.invalid', 'named in an inline style'),
        ]:
            with self.subTest(path=path):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    result = main([self.address + path])
                self.assertEqual(result, 1)
                self.assertIn(f'FOREIGN {host} {source}', out.getvalue())

    def test_same_host_inline_script_passes_the_cli(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            result = main([self.address + 'clean'])
        self.assertEqual(result, 0)
        self.assertIn('foreign HTML loads or inline addresses: none', out.getvalue())

    def test_inline_references_are_reported_without_claiming_a_request(self):
        parser = Loads(self.address)
        parser.feed('''<script>
          const unused = "https://unused.invalid/example";
          const socket = "wss://socket.invalid/x";
          fetch('//relative.invalid/x');
          fetch('/local'); const own = 'http://127.0.0.1/own';
        </script><style>
          p { background: image-set("//style.invalid/a" 1x, "https://style2.invalid/b" 2x) }
        </style><p style="background: image-set('//attribute.invalid/a' 1x)"></p>''')
        self.assertEqual({(host, source) for host, source, _ in parser.foreign()}, {
            ('unused.invalid', 'named in an inline script'),
            ('socket.invalid', 'named in an inline script'),
            ('relative.invalid', 'named in an inline script'),
            ('style.invalid', 'named in an inline style'),
            ('style2.invalid', 'named in an inline style'),
            ('attribute.invalid', 'named in an inline style'),
        })


if __name__ == '__main__':
    unittest.main()
