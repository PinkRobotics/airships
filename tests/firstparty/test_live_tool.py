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
from check_first_party import browser_user_agent, inspect, main


class Edge(http.server.BaseHTTPRequestHandler):
    requests = []

    def log_message(self, *args):
        pass

    def do_GET(self):
        Edge.requests.append((self.headers.get('User-Agent', ''), self.headers.get('Accept', '')))
        browser = 'Chrome/' in self.headers.get('User-Agent', '') and 'text/html' in self.headers.get('Accept', '')
        body = '<html><body>clean'
        if browser:
            body += '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js"></script>'
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


if __name__ == '__main__':
    unittest.main()
