#!/usr/bin/env python3
"""Refuse fixed serving ports, borrowed endpoints, and released-port discovery.

Scan tracked Python, shell and JavaScript under tools, tests, 3d/scripts, research
and pipeline; also Makefile, the CI workflow and the four command documents.
Comments and string examples are included. Nothing under docs is scanned.

Recognized shapes, drawn from the port inventory (decimal literals):
- address: a numeric port in an HTTP/WebSocket URL or a loopback host:port;
- argument: a numeric port option, its argparse default, the port an http.server
  command binds (8000 when it names none), or a JavaScript listen/bind argument.
  An http.server command with a word its own parser would refuse, or a Python module
  switch whose module name is computed, is argument:unreadable, which no allowance
  can excuse. An explicit runpy.run_module call for http.server is unreadable too:
  its serving arguments come from sys.argv rather than the call's arguments;
- assignment: a numeric value/list assigned to port, PORT, *_port(s), *_PORT(S)
  or a camel-case *Port(s) name, including Makefile defaults;
- bind: a nonzero literal in a bind/HTTPServer/TCPServer/Server address tuple;
- debug: a Chromium debugging-port flag whose literal argument is not zero;
- socket: getsockname(), server_address, server_port or address().port outside
  tools/serve.py;
- environment: direct Python/JavaScript/shell reads of PORT or AIRSHIPS_PORT,
  plus the former Python loop over those literal names before an environment read.

Each numeric shape includes its literal value, so an allowance for the person's
address cannot excuse changing it to a different fixed port. Counts are matching
occurrences per path and shape. Every allowance needs an exact path, shape,
positive count and row-specific reason; obsolete rows fail too.

Limits: this is a syntax guard, not dataflow analysis. Constructed strings, aliased
APIs, computed or nondecimal numbers and ports hidden behind differently named variables can
escape it. A switch on an explicitly named Python executable (including sys.executable
and the Makefile's PY) with a computed module name fails closed; adjacent string literals
are read as their one constant. Explicit runpy.run_module calls naming http.server are
refused without attempting to infer sys.argv. A computed port on a literal module command
is trusted to be chosen at run time. Files outside the scope, untracked
files, installed dependencies and external services are not inspected. `make portproof`
checks the actual isolation of the eight browser gates independently of these patterns.
"""
from __future__ import annotations

import argparse
import ast
from collections import defaultdict
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCOPE_DIRS = ('tools/', 'tests/', '3d/scripts/', 'research/', 'pipeline/')
SUFFIXES = ('.py', '.sh', '.js', '.mjs')
SCOPE_FILES = {'Makefile', '.github/workflows/ci.yml', 'README.md', 'CONTRIBUTING.md',
               'tests/README.md', 'tools/README.md'}
ALLOWLIST = 'tools/ports_allowlist.txt'
NAME = r'(?:PORTS?|[A-Z0-9_]+_PORTS?|ports?|[a-z0-9_]+_ports?|[a-zA-Z0-9_]*Port(?:s)?)'
NUMERIC = (
    ('address', re.compile(r'(?:https?|wss?)://(?:\[[^\]\s]+\]|[\w.-]+):([0-9]{1,5})\b|'
                           r'(?<![\w.])(?:127\.0\.0\.1|localhost):([0-9]{1,5})\b')),
    ('argument', re.compile(r'--(?:[\w]+-)*port(?:=|[\s\x22\x27,]+)([0-9]{1,5})\b|'
                            r'--port[^\n]{0,80}?\bdefault\s*=\s*([0-9]{1,5})\b')),
    ('bind', re.compile(r'(?:\.bind|\b[\w.]*(?:HTTPServer|TCPServer|Server))\s*\(\s*'
                        r'(?:server_address\s*=\s*)?\(\s*'
                        r'[^,\n]+,\s*([0-9]{1,5})\b')),
)
ASSIGNED = re.compile(r'\b' + NAME + r'[\x22\x27]?(?:\s*:\s*(?:int|str))?\s*(?:[?:+]?=|:)\s*'
                      r'([\x22\x27]?[0-9]{1,5}\b|[\[(][0-9,\s]+[\])])')
DEBUG = re.compile(r'--remote-debugging-port')
ZERO_ARGUMENT = re.compile(r'^(?:=0(?=[\s\x22\x27,)\]]|$)|'
                           r'(?:[\x22\x27]\s*,\s*[\x22\x27]|\s+)0(?=[\s\x22\x27,)\]]|$))')
SOCKET = re.compile(r'\.getsockname\s*\(|\.server_(?:address|port)\b|\.address\(\)\.port\b')
ENVIRONMENT = (
    re.compile(r'(?:os\.)?(?:environ\s*\[\s*|environ\.get\s*\(\s*|getenv\s*\(\s*)'
               r'[\x22\x27](PORT|AIRSHIPS_PORT)[\x22\x27]'),
    re.compile(r'\bprocess\.env(?:\.(PORT|AIRSHIPS_PORT)\b|\[\s*[\x22\x27](PORT|AIRSHIPS_PORT)[\x22\x27])'),
    re.compile(r'\$(?:\{(PORT|AIRSHIPS_PORT)(?:\}|[:?+-])|(PORT|AIRSHIPS_PORT)\b)'),
)
ENV_LOOP = re.compile(r'for\s+\w+\s+in\s*\([^)]*[\x22\x27](?:PORT|AIRSHIPS_PORT)[\x22\x27]'
                      r'[^)]*\)\s*:[\s\S]{0,160}?\benviron(?:\.get|\[)')
# An http.server command is found where the module name follows Python's module switch with
# only whitespace, quotes, commas, a +, backslashes or comments to the line's end between
# them, as shell words or as list elements. It is read to its end: a shell separator, the
# close of the string that holds it, or its list's closing bracket. Its words are read as
# CPython 3.14's parser reads them: long options by exact name or unique prefix, with or
# without =value; short options with the value next, attached or after =; then at most one
# positional port. $VAR, $(...), a call or a name is one computed value, and a computed port
# is not a fixed one.
HTTP_SERVER = re.compile(r'(?<![\w-])-[A-Za-z]*m(?P<gap>(?:[\s\x22\x27\\,+]|#[^\n]*\n)*?)'
                         r'http\.server(?![\w.])')
MODULE_SWITCH = re.compile(r'(?<![\w-])-[A-Za-z]*m(?![\w.-])')
RUN_MODULE = re.compile(r'(?<![\w.])runpy\.run_module\s*\(')
PYTHON_COMMAND = re.compile(r'(?<![\w.])python(?:[0-9]+(?:\.[0-9]+)*)?\b|\bsys\.executable\b|'
                            r'\$\(\s*PY\s*\)|\$\{?PY(?:THON)?\}?\b')
SERVER_OPTIONS = {'--bind': True, '--directory': True, '--protocol': True, '--tls-cert': True,
                  '--tls-key': True, '--tls-password-file': True, '--cgi': False, '--help': False}
SERVER_SHORT = {'-b': '--bind', '-d': '--directory', '-p': '--protocol', '-h': '--help'}
SHELL_END = re.compile(r'[\n;&|)`#<>]|[0-9]+[<>]')
ESCAPES = {'n': '\n', 'r': '\n', 't': ' ', '\n': '', '\\': '\\', '\x22': '\x22', '\x27': '\x27',
           '`': '`'}
UNREADABLE = object()


def closing(text, i):
    """The index of the quote that closes the one at i (or the end); escapes are skipped."""
    j = i + 1
    while j < len(text) and text[j] != text[i]:
        j += 2 if text[j] == '\\' else 1
    return min(j, len(text))


def bracket_end(text, i):
    """The index after the bracket that closes the one at i; quoted text is skipped."""
    depth = 0
    while i < len(text):
        if text[i] in '\x22\x27`':
            i = closing(text, i) + 1
            continue
        depth += (text[i] in '([{') - (text[i] in ')]}')
        i += 2 if text[i] == '\\' else 1
        if depth == 0:
            break
    return i


def open_quote(prefix):
    """The quote still open at the end of a line's prefix, and where it opened."""
    quote, opened, i = None, -1, 0
    while i < len(prefix):
        if prefix[i] == '\\':
            i += 1
        elif quote is None and prefix[i] in '\x22\x27`':
            quote, opened = prefix[i], i
        elif prefix[i] == quote:
            quote = None
        i += 1
    return quote, opened


def string_body(text, i, quote):
    """The rest of the string holding a command, unescaped: to its closing quote or line end."""
    end = i
    while end < len(text) and text[end] not in (quote, '\n'):
        end += 2 if text[end] == '\\' else 1
    return re.sub(r'\\(.)', lambda m: ESCAPES.get(m.group(1), m.group()), text[i:end], flags=re.S)


def shell_word(text, i):
    """The shell word at i, or None if any part of it is expanded; and the index after it."""
    parts, computed = [], False
    while i < len(text) and text[i] not in ' \t\r\n;&|)`<>':
        if text[i] == '\\':
            parts.append(text[i + 1:i + 2].strip('\n'))
            i += 2
        elif text[i] == '\x27':
            end = text.find('\x27', i + 1)
            end = len(text) if end < 0 else end
            parts.append(text[i + 1:end])
            i = end + 1
        elif text[i] == '\x22':
            end = closing(text, i)
            computed = computed or bool(re.search(r'(?<!\\)[$`]', text[i + 1:end]))
            parts.append(re.sub(r'\\(.)', r'\1', text[i + 1:end], flags=re.S))
            i = end + 1
        elif text[i] == '$':
            computed = True
            i = bracket_end(text, i + 1) if text[i + 1:i + 2] in ('(', '{') else i + 1
        else:
            parts.append(text[i])
            i += 1
    return (None if computed else ''.join(parts)), i


def shell_words(text, i=0):
    """The words of a shell command from i to its end."""
    words = []
    while i < len(text):
        if text[i] in ' \t\r' or text.startswith('\\\n', i):
            i += 2 if text[i] == '\\' else 1
        elif SHELL_END.match(text, i):
            break
        else:
            word, i = shell_word(text, i)
            words.append(word)
    return words


def list_element(source):
    """A literal string or number as its text; another expression (computed) as None."""
    if source.startswith(('*', '...')):
        return UNREADABLE
    if source.startswith('`'):
        return None if '${' in source else source.strip('`')
    try:
        value = ast.literal_eval(source)
    except ValueError:
        return None
    except (SyntaxError, TypeError, MemoryError, RecursionError):
        return UNREADABLE
    return str(value) if type(value) in (str, int) else UNREADABLE


def list_words(text, i):
    """The elements of an argument list from i to its closing bracket at depth 0."""
    words, depth, piece = [], 0, []
    while i < len(text):
        if text[i] in '\x22\x27`':
            end = closing(text, i) + 1
            piece.append(text[i:end])
            i = end
            continue
        if text[i] == '#':
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
            continue
        if text[i] in ',)]}' and depth == 0:
            element = re.sub(r'\s*\n\s*', ' ', ''.join(piece)).strip()
            if element:
                words.append(list_element(element))
            if text[i] != ',':
                break
            piece = []
        else:
            depth += (text[i] in '([{') - (text[i] in ')]}')
            piece.append(text[i])
        i += 1
    return words


def server_option(word):
    """The option a word names and its attached value, or (None, None) if the parser refuses
    the word: unknown, an ambiguous prefix, or a value given to a flag."""
    if word.startswith('--'):
        name, equals, value = word.partition('=')
        prefixed = [option for option in SERVER_OPTIONS if option.startswith(name)]
        names = [name] if name in SERVER_OPTIONS else prefixed
        if len(names) != 1 or (equals and not SERVER_OPTIONS[names[0]]):
            return None, None
        return names[0], value if equals else None
    option, value = SERVER_SHORT.get(word[:2]), word[2:]
    if option is None:
        return None, None
    if value.startswith('='):
        value = value[1:]
    return option, value if word[2:] else None


def server_port(words):
    """The port an argument list binds (8000 if it names none); None for a computed port or a
    help request; UNREADABLE for a word the parser refuses or a second positional word."""
    words, positional, options = iter(words), [], True
    for word in words:
        if word is UNREADABLE:
            return UNREADABLE
        if options and word is not None and word.startswith('-') and word != '-':
            if word == '--':
                options = False
                continue
            option, value = server_option(word)
            if option is None:
                return UNREADABLE
            if option == '--help':
                return None
            if SERVER_OPTIONS[option] and value is None and next(words, UNREADABLE) is UNREADABLE:
                return UNREADABLE
        else:
            positional.append(word)
    if len(positional) > 1:
        return UNREADABLE
    port = positional[0] if positional else '8000'
    if port is None:
        return None
    return int(port) if re.fullmatch(r'[0-9]{1,5}', port) else UNREADABLE


def http_server_ports(text):
    """Yield (port, offset) for each http.server command whose port is fixed or unreadable."""
    covered = set()
    for match in HTTP_SERVER.finditer(text):
        covered.add(match.start())
        line = text.rfind('\n', 0, match.start()) + 1
        quote, opened = open_quote(text[line:match.start()])
        element = quote and line + opened == match.start() - 1  # the switch opens an element
        opener = re.search(r'\\?[\x22\x27]$', match.group('gap'))
        closer = opener.group() if opener else quote if element else None
        end = match.end()
        closed = closer is not None and text.startswith(closer, end)
        if closed:
            end += len(closer)  # past the quote closing the module's word or element
        if element and closed:
            words = list_words(text, end)
        elif quote:
            words = shell_words(string_body(text, end, quote))
        else:
            words = shell_words(text, end)
        port = server_port(words)
        if port is not None:
            yield port, match.start()
    for match in MODULE_SWITCH.finditer(text):
        if match.start() in covered:
            continue
        # A message switch on a Git command is not a Python module switch. Look in
        # the same shell command or the still-open argument list for its executable.
        start = max(text.rfind('\n', 0, match.start()), text.rfind(';', 0, match.start())) + 1
        prefix = text[start:match.start()]
        if not PYTHON_COMMAND.search(prefix):
            opening = max(text.rfind('[', 0, match.start()), text.rfind('(', 0, match.start()))
            prefix = text[opening:match.start()] if opening >= 0 else ''
            if any(end in prefix for end in '])') or not PYTHON_COMMAND.search(prefix):
                continue
        line = text.rfind('\n', 0, match.start()) + 1
        quote, opened = open_quote(text[line:match.start()])
        element = quote and line + opened == match.start() - 1
        end = match.end()
        if element and text.startswith(quote, end):
            end += 1
            words = (list_words(text, end) if re.match(r'\s*,', text[end:])
                     else shell_words(text, end))
        elif quote:
            words = shell_words(string_body(text, end, quote))
        else:
            words = shell_words(text, end)
        if not words:
            continue
        module, *arguments = words
        if module is None or module is UNREADABLE:
            yield UNREADABLE, match.start()
        elif module == 'http.server':
            port = server_port(arguments)
            if port is not None:
                yield port, match.start()
    for match in RUN_MODULE.finditer(text):
        words = list_words(text, match.end())
        if words and words[0] == 'http.server':
            yield UNREADABLE, match.start()


def in_scope(path):
    return path in SCOPE_FILES or (path.startswith(SCOPE_DIRS) and path.endswith(SUFFIXES))


def scan(path, text):
    hits = []

    def hit(shape, offset):
        hits.append((shape, text.count('\n', 0, offset) + 1))

    for kind, pattern in NUMERIC:
        for match in pattern.finditer(text):
            value = int(next(v for v in match.groups() if v is not None))
            if (kind == 'address' and value == 0) or 0 < value <= 65535:
                hit(f'{kind}:{value}', match.start())
    for value, offset in http_server_ports(text):
        if value is UNREADABLE:
            hit('argument:unreadable', offset)
        elif 0 < value <= 65535:
            hit(f'argument:{value}', offset)
    if path.endswith(('.js', '.mjs')):
        for match in re.finditer(r'\.(?:listen|bind)\s*\(\s*([0-9]{1,5})\b', text):
            if 0 < int(match.group(1)) <= 65535:
                hit('argument:' + str(int(match.group(1))), match.start())
    for match in ASSIGNED.finditer(text):
        for value in re.findall(r'\d+', match.group(1)):
            if 0 < int(value) <= 65535:
                hit(f'assignment:{int(value)}', match.start())
    for match in DEBUG.finditer(text):
        if not ZERO_ARGUMENT.match(text[match.end():]):
            hit('debug', match.start())
    if path != 'tools/serve.py':
        for match in SOCKET.finditer(text):
            hit('socket', match.start())
    for pattern in ENVIRONMENT:
        for match in pattern.finditer(text):
            name = next(v for v in match.groups() if v is not None)
            hit('environment:' + name, match.start())
    for match in ENV_LOOP.finditer(text):
        hit('environment:loop', match.start())
    return sorted(hits)


def tracked_files(root):
    output = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root)
    return sorted(set(path for path in output.decode().split('\0') if path and in_scope(path)))


def read_allowlist(root):
    rows = {}
    for line in (root / ALLOWLIST).read_text().splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        parts = [p.strip() for p in line.split('|', 3)]
        if len(parts) != 4:
            raise ValueError('allowlist rows need path | shape | count | reason')
        path, shape, count, reason = parts
        if not in_scope(path) or Path(path).is_absolute() or '..' in Path(path).parts:
            raise ValueError(f'allowlist path is outside scope: {path}')
        if not re.fullmatch(r'address:0|(?:address|argument|assignment|bind):[1-9][0-9]{0,4}|'
                            r'debug|socket|environment:(?:PORT|AIRSHIPS_PORT|loop)', shape):
            raise ValueError(f'unknown allowlist shape: {shape}')
        if not count.isdecimal() or int(count) < 1 or not reason:
            raise ValueError(f'allowlist needs a positive count and a reason: {path} | {shape}')
        if (path, shape) in rows:
            raise ValueError(f'duplicate allowlist row: {path} | {shape}')
        rows[path, shape] = (int(count), reason)
    return rows


def check(root):
    actual = defaultdict(list)
    for path in tracked_files(root):
        for shape, line in scan(path, (root / path).read_text()):
            actual[path, shape].append(line)
    allowed = read_allowlist(root)
    errors = []
    for key in sorted(set(actual) | set(allowed)):
        lines = actual.get(key, [])
        expected = allowed.get(key)
        if expected is None:
            errors.append(f'{key[0]}:{",".join(map(str, lines))}: refused {key[1]} ({len(lines)} hits)')
        elif len(lines) != expected[0]:
            errors.append(f'{key[0]} | {key[1]}: allowlist count {expected[0]}, actual {len(lines)}')
    return dict(actual), errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        actual, errors = check(args.root)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'portcheck: FAIL: {error}', file=sys.stderr)
        return 1
    for (path, shape), lines in sorted(actual.items()):
        print(f'{path}:{",".join(map(str, lines))} | {shape} | {len(lines)}')
    for error in errors:
        print(error, file=sys.stderr)
    print(f'portcheck: {"FAIL" if errors else "PASS"}; {len(tracked_files(args.root))} tracked files, '
          f'{len(actual)} matched rows')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
