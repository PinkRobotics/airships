"""The live inspector is exercised only against a loopback edge imitation."""
import contextlib
import http.server
import io
from pathlib import Path
import sys
import unittest
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from check_first_party import Loads, inspect, main
from serve import serve_tree


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
                '/srcdoc': '<iframe srcdoc="&lt;img src=\'https://frame-image.invalid/x\'&gt;"></iframe>',
                '/apple-icon': '<link rel="apple-touch-icon" href="https://apple-icon.invalid/icon.png">',
                '/image-attribute': '<div style="background: image-set(\'https://attribute-image.invalid/x\' 1x)"></div>',
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
        cls.serving = serve_tree(handler=Edge)
        cls.address = cls.serving.__enter__()
        cls.addClassCleanup(cls.serving.__exit__, None, None, None)

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
            ('image-attribute', 'attribute-image.invalid', 'named in an inline style'),
            ('srcdoc', 'frame-image.invalid', 'iframe[srcdoc] img[src]'),
            ('apple-icon', 'apple-icon.invalid', 'link[href]'),
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

    def test_srcdoc_inherits_base_and_uses_its_own_base_when_present(self):
        parser = Loads(self.address)
        parser.feed("""<base href="https://parent-base.invalid/dir/">
          <iframe srcdoc="&lt;img src='relative.png'&gt;"></iframe>
          <iframe srcdoc="&lt;base href='nested/'&gt;&lt;img src='x.png'&gt;"></iframe>
          <iframe srcdoc="&lt;base href='https://child-base.invalid/'&gt;&lt;img src='child.png'&gt;"></iframe>""")
        self.assertEqual({url for _, _, url in parser.foreign()}, {
            'https://parent-base.invalid/dir/relative.png', 'https://child-base.invalid/child.png',
            'https://parent-base.invalid/dir/nested/x.png'})

    def test_nested_srcdoc_loads_and_same_host_pass(self):
        parser = Loads(self.address)
        parser.feed("""<iframe srcdoc="&lt;iframe srcdoc=&quot;&amp;lt;img src='https://nested.invalid/x'&amp;gt;&quot;&gt;&lt;/iframe&gt;"></iframe>""")
        self.assertEqual(parser.foreign(), [('nested.invalid', 'iframe[srcdoc] iframe[srcdoc] img[src]',
                                             'https://nested.invalid/x')])
        own = Loads(self.address)
        own.feed("""<iframe srcdoc="&lt;img src='/local.png'&gt;"></iframe>""")
        self.assertEqual(own.foreign(), [])

    def test_interaction_only_addresses_remain_out_of_scope(self):
        parser = Loads(self.address)
        parser.feed('<form action="https://form.invalid/x"></form><a href="/local" ping="https://ping.invalid/x">go</a>')
        self.assertEqual(parser.foreign(), [])


if __name__ == '__main__':
    unittest.main()
