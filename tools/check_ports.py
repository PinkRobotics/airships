#!/usr/bin/env python3
"""Refuse fixed serving ports, borrowed endpoints, and released-port discovery.

Scan tracked Python, shell and JavaScript under tools, tests, 3d/scripts, research
and pipeline; also Makefile, the CI workflow and the four command documents.
Comments and string examples are included. Nothing under docs is scanned.

Recognized shapes, drawn from the port inventory (decimal literals):
- address: a numeric port in an HTTP/WebSocket URL or a loopback host:port;
- argument: a numeric port option, its argparse default, an http.server command, or
  a JavaScript listen/bind argument;
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
escape it. Files outside the scope, untracked files, installed dependencies and
external services are not inspected. `make portproof` checks the actual isolation
of the eight browser gates independently of these patterns.
"""
from __future__ import annotations

import argparse
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
                            r'--port[^\n]{0,80}?\bdefault\s*=\s*([0-9]{1,5})\b|'
                            r'\bhttp\.server\s+[\x22\x27]?([0-9]{1,5})\b')),
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
