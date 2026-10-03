"""Plant every refused port shape in a tracked scratch tree; check exact allowances."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_ports

# The gate scans this file too. Its http.server commands are assembled at run time, so that the
# file's own text holds no command for the gate to read and no second layer of escaping.
SERVER = 'http.' + 'server'

BAD = {
    'loopback_address': 'url = "http://127.0.0.1:9001/page"',
    'zero_address': 'url = "http://127.0.0.1:0/page"',
    'other_host_address': 'url = "https://example.invalid:443/page"',
    'websocket_address': 'url = "ws://localhost:9001/page"',
    'port_argument': 'python3 tools/serve.py --port 9001',
    'quoted_argument': 'args = ["--port", "9001"]',
    'equals_argument': 'python3 tools/serve.py --port=9001',
    'argparse_default': 'parser.add_argument("--port", type=int, default=9001)',
    'assignment': 'PORT = 9001',
    'typed_assignment': 'port: int = 9001',
    'make_default': 'PORT ?= 9001',
    'camel_assignment': 'const debugPort = 9001;',
    'quoted_assignment': 'serve_port = "9001"',
    'list_assignment': 'DECOY_PORTS = (9001, 9002)',
    'bind': 'sock.bind(("127.0.0.1", 9001))',
    'multiline_bind': 'sock.bind((\n "localhost",\n 9001))',
    'server_constructor': 'server = ThreadingHTTPServer(("127.0.0.1", 9001), Handler)',
    'keyword_server': 'server = HTTPServer(server_address=("localhost", 9001), RequestHandlerClass=H)',
    'js_listen': 'http.createServer(handle).listen(9001);',
    'js_socket_read': 'const number = server.address().port;',
    'debug_number': 'args = ["--remote-debugging-port=9001"]',
    'debug_variable': 'args = [f"--remote-debugging-port={chosen}"]',
    'debug_split': 'args = ["--remote-debugging-port", chosen]',
    'socket_read': 'number = sock.getsockname()[1]',
    'server_address': 'number = server.server_address[1]',
    'server_port': 'number = server.server_port',
    'env_get': 'number = os.environ.get("PORT")',
    'env_index': 'number = os.environ["AIRSHIPS_PORT"]',
    'getenv': 'number = os.getenv("PORT")',
    'multiline_env': 'number = os.environ.get(\n "PORT")',
    'env_loop': 'for key in ("AIRSHIPS_PORT", "PORT"):\n    value = os.environ.get(key)',
    'shell_env': 'curl "http://127.0.0.1:$PORT/page"',
    'shell_default': 'number="${AIRSHIPS_PORT:-9001}"',
    'js_env': 'const number = process.env.PORT;',
    'js_env_index': 'const number = process.env["AIRSHIPS_PORT"];',
}

# Each http.server command and the one shape the gate reads from it: the port CPython 3.14's own
# parser binds for those words (8000 when none is named), argument:unreadable when that parser
# would refuse a word, and nothing when the port is computed or zero or only help is asked for.
SERVER_COMMANDS = {
    f'python3 -m {SERVER} 9001': 'argument:9001',
    f'python3 -m {SERVER} --bind 127.0.0.1 9001': 'argument:9001',
    f'python3 -m {SERVER} \\\n    --bind 127.0.0.1 9001': 'argument:9001',
    f'subprocess.Popen(["python3", "-m", "{SERVER}", "9001"])': 'argument:9001',
    f'subprocess.Popen(["python3", "-m", "{SERVER}", "--bind", "127.0.0.1", "9001"])':
        'argument:9001',
    f'subprocess.Popen([\n    "python3", "-m", "{SERVER}",\n    "-d", ".", "9001",\n])':
        'argument:9001',
    f'script.write_text("python3 -m {SERVER} 9001\\n")': 'argument:9001',
    f'command = "python3 -m {SERVER} \\"9001\\""': 'argument:9001',
    f'spawn("python3", ["-m", "{SERVER}", "9001"]);': 'argument:9001',
    # Long options by unique prefix, as argparse accepts them.
    f'python3 -m {SERVER} --dir site 9001': 'argument:9001',
    f'subprocess.Popen(["python3", "-m", "{SERVER}", "--prot", "HTTP/1.1", "9001"])':
        'argument:9001',
    # An expansion, a call or a quoted value is one word.
    f'python3 -m {SERVER} --directory $(SITE) 9001': 'argument:9001',
    f'subprocess.Popen([sys.executable, "-m", "{SERVER}", "--directory", str(root), "9001"])':
        'argument:9001',
    f'python3 -m {SERVER} -d "$(pwd)/site" 9001': 'argument:9001',
    f'python3 -m {SERVER} -d "my site" 9001': 'argument:9001',
    f'subprocess.Popen(("python3", "-m", "{SERVER}", "-d", os.fspath(root), "9001"))':
        'argument:9001',
    # Attached values, the end of options, joined switches, a string, a redirection, a comment.
    f'python3 -m {SERVER} -dsite --bind=127.0.0.1 -- 9001': 'argument:9001',
    f'python3 -Bm{SERVER} 9001': 'argument:9001',
    f'subprocess.Popen(["python3", "-m{SERVER}", "9001"])': 'argument:9001',
    f'subprocess.run("python3 -m {SERVER} --dir site 9001", shell=True)': 'argument:9001',
    f'python3 -m {SERVER} 9001 > server.log 2>&1 &': 'argument:9001',
    f'python3 -m {SERVER} 9001 2>server.log': 'argument:9001',
    f'command = [\n    sys.executable, "-m", "{SERVER}",\n    "--bind", "127.0.0.1",  # loopback\n'
    '    "9001",\n]': 'argument:9001',
    # The module name after a quote, a quoted switch, a continuation, a comment or a +.
    f'python3 -m "{SERVER}" 9001': 'argument:9001',
    f'os.system("python3 -m \'{SERVER}\' 9001")': 'argument:9001',
    f'command = "python3 -m \\"{SERVER}\\" 9001"': 'argument:9001',
    f'python3 "-m" {SERVER} 9001': 'argument:9001',
    f'python3 -m \\\n    {SERVER} 9001': 'argument:9001',
    f'subprocess.Popen([\n    sys.executable, "-m",  # stdlib\n    "{SERVER}", "9001",\n])':
        'argument:9001',
    f'os.system("python3 -m " + "{SERVER} 9001")': 'argument:9001',
    f'command = ("python3 -m "\n           "{SERVER} 9001")': 'argument:9001',
    # No port named: the parser's default.
    f'python3 -m {SERVER}': 'argument:8000',
    f'subprocess.Popen(["python3", "-m", "{SERVER}"])': 'argument:8000',
    f'python3 -m {SERVER} --bind 127.0.0.1 &': 'argument:8000',
    f'Prose names `python3 -m {SERVER}` in passing.': 'argument:8000',
    # A word the parser refuses, or a second positional word.
    f'python3 -m {SERVER} --verbose 9001': 'argument:unreadable',
    f'python3 -m {SERVER} --tls x 9001': 'argument:unreadable',
    f'python3 -m {SERVER} --cgi=yes 9001': 'argument:unreadable',
    f'python3 -m {SERVER} --bind': 'argument:unreadable',
    f'python3 -m {SERVER} "$port" 9001': 'argument:unreadable',
    f'Run python3 -m {SERVER} 9001. Then open the page.': 'argument:unreadable',
    f'# python3 -m {SERVER} mostly works': 'argument:unreadable',
    f'subprocess.Popen(["python3", "-m", "{SERVER}", *extra])': 'argument:unreadable',
    # Nothing fixed: zero, a computed port, help, or no command at all.
    f'python3 -m {SERVER} 0': None,
    f'chosen_by_system = ["python3", "-m", "{SERVER}", "0"]': None,
    f'command = ["python3", "-m", "{SERVER}", "--bind", "127.0.0.1", str(chosen)]': None,
    f'python3 -m {SERVER} "$port" --bind 127.0.0.1': None,
    f'python3 -m {SERVER} --help': None,
    f'import {SERVER}\nfrom {SERVER} import BaseHTTPRequestHandler': None,
    f'class Handler({SERVER}.SimpleHTTPRequestHandler):\n    pass': None,
    f"Python's own {SERVER} mostly works.": None,
}


class PortRules(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='portcheck-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / 'tools').mkdir()
        self.allow = self.root / check_ports.ALLOWLIST
        self.allow.write_text('')

    def plant(self, text, path='tools/probe.py', track=True):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text + '\n')
        if track:
            subprocess.run(['git', 'add', '--', path], cwd=self.root, check=True)

    def errors(self):
        return check_ports.check(self.root)[1]

    def test_zero_and_other_environment_names_pass(self):
        self.plant('sock.bind(("127.0.0.1", 0))\n'
                   'args = ["--remote-debugging-port=0", "--port", "0"]\n'
                   'transport = 9001\nprofile = os.environ.get("TMPDIR")')
        self.assertEqual(self.errors(), [])

    def test_http_server_commands_are_read_as_their_parser_reads_them(self):
        for text, shape in SERVER_COMMANDS.items():
            with self.subTest(text=text):
                self.plant(text)
                shapes = [found for found, _ in check_ports.scan('tools/probe.py', text + '\n')]
                self.assertEqual(shapes, [shape] if shape else [])
                self.assertEqual(bool(self.errors()), bool(shape))

    def test_http_server_port_is_counted_once_per_command(self):
        self.plant(f'python3 -m {SERVER} 8875\n'
                   f'command = ["python3", "-m", "{SERVER}", "--bind", "127.0.0.1", "8875"]')
        self.allow.write_text('tools/probe.py | argument:8875 | 2 | Person-facing example\n')
        self.assertEqual(self.errors(), [])

    def test_unreadable_command_cannot_be_allowed(self):
        self.plant(f'python3 -m {SERVER} --verbose 9001')
        self.allow.write_text('tools/probe.py | argument:unreadable | 1 | Person-facing example\n')
        with self.assertRaises(ValueError):
            self.errors()

    def test_socket_read_is_confined_to_serving_module(self):
        self.plant('port = server.server_address[1]', 'tools/serve.py')
        self.assertEqual(self.errors(), [])
        self.plant('port = server.server_address[1]', 'tools/other.py')
        self.assertTrue(self.errors())

    def test_all_scope_directories_suffixes_and_documents(self):
        for directory in check_ports.SCOPE_DIRS:
            for suffix in check_ports.SUFFIXES:
                path = directory + 'probe' + suffix
                with self.subTest(path=path):
                    self.plant('PORT = 9001', path)
                    self.assertTrue(any(path in error for error in self.errors()))
        for path in check_ports.SCOPE_FILES:
            with self.subTest(path=path):
                self.plant('PORT = 9001', path)
                self.assertTrue(any(path in error for error in self.errors()))

    def test_untracked_and_docs_files_are_outside_scope(self):
        self.plant('PORT = 9001', track=False)
        self.plant('PORT = 9001', 'docs/probe.py')
        self.assertEqual(self.errors(), [])

    def test_exact_allowance(self):
        self.plant('url = "http://127.0.0.1:8875/page"')
        self.allow.write_text('tools/probe.py | address:8875 | 1 | Person-facing example\n')
        self.assertEqual(self.errors(), [])

    def test_wrong_count(self):
        self.plant('url = "http://127.0.0.1:8875/page"')
        self.allow.write_text('tools/probe.py | address:8875 | 2 | Person-facing example\n')
        self.assertTrue(any('count 2, actual 1' in error for error in self.errors()))

    def test_same_line_occurrences_are_counted(self):
        self.plant('url = "http://127.0.0.1:8875/"; ' * 2)
        self.allow.write_text('tools/probe.py | address:8875 | 1 | Person-facing example\n')
        self.assertTrue(any('count 1, actual 2' in error for error in self.errors()))

    def test_row_no_longer_matches(self):
        self.plant('url = "plain"')
        self.allow.write_text('tools/probe.py | address:8875 | 1 | Person-facing example\n')
        self.assertTrue(any('actual 0' in error for error in self.errors()))

    def test_different_port_cannot_inherit_allowance(self):
        self.plant('url = "http://127.0.0.1:9001/page"')
        self.allow.write_text('tools/probe.py | address:8875 | 1 | Person-facing example\n')
        self.assertEqual(len(self.errors()), 2)

    def test_malformed_or_duplicate_allowance(self):
        row = 'tools/probe.py | address:8875 | 1 | Person-facing example\n'
        for text in [row + row, row.replace(' | 1 | ', ' | 0 | '),
                     row.replace('Person-facing example', ''), row.replace('address:8875', 'unknown'),
                     row.replace('tools/probe.py', '../elsewhere.py'), 'not a row']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.allow.write_text(text)
                self.errors()


def refused_case(name, text):
    def test(self):
        self.plant(text, 'tools/probe.mjs' if name.startswith('js_') else 'tools/probe.py')
        self.assertTrue(self.errors(), f'accepted refused shape: {text}')
    return test


for name, text in BAD.items():
    setattr(PortRules, 'test_refuses_' + name, refused_case(name, text))


if __name__ == '__main__':
    unittest.main()
