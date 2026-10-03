#!/usr/bin/env python3
"""Prove that browser gates serve their own trees. Run alone: eight fixed ports are bound.

A: a named mutation fails alone, then still fails beside a server for the good tree.
B: the unmodified tree passes while eight logging decoys occupy the retired ports.
C: the same gate starts concurrently in good and mutated copies; only the good one passes.
A includes the seven formerly fixed-port gates; B and C also include cellparity.

Exit 3 means a required port is occupied; exit 1 means a proof failed. --before records
A on a source tree from before the migration, without expecting isolation to hold.
Copies live only under explicit TMPDIR and are removed on exit. Full gate output,
request logs and summary.jsonl remain in --log-dir. No agency endpoint is contacted.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager, ExitStack
import functools
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from serve import Handler

DECOY_PORTS = (8791, 8871, 8898, 8899, 8907, 8909, 8911, 8913)
EXIT_BUSY = 3
# gate: old ports, file, old text, replacement, diagnostic required from a failing gate.
CASES = {
    'test': ((8791,), '3d/render/styles.js', "const ID = 'airship3d-styles';",
             "const ID = 'portproof-wrong-style';", 'the stylesheet injects exactly once'),
    'fallbackcheck': ((8871,), 'sim/config.js', 'name: "P-100",',
                      'name: "P-100 proof",', 'FALLBACK-ROSTER: committed block differs'),
    'figfresh': ((8898,), 'sim/config.js', 'rhoAir: 1.10,', 'rhoAir: 1.11,', 'assumptions.rhoAir:'),
    'explorercheck': ((8909, 8911), 'ship/index.html', 'data-n="ship.ratio" data-f="3"',
                      'data-n="ship.ratio" data-f="2"', 'displayed shipRatio:'),
    'levelscheck': ((8911,), 'cell/levels.html', 'id="fig-cell"', 'id="fig-cellX"',
                    '#fig-cell is missing'),
    'bandcheck': ((8911,), 'ship/model.js', 'K_LOCAL = 0.3', 'K_LOCAL = 0.31',
                  'frame1450at80.totalT:'),
    'shipcheck': ((8913,), 'cell/ship.html', 'data-n="plan.sfDeclared"',
                  'data-n="plan.sfDeclaredX"', 'plan.sfDeclaredX'),
    'cellparity': ((), 'ship/model.js', 'K_LOCAL = 0.3', 'K_LOCAL = 0.31', 'ship0'),
}


class BusyPort(RuntimeError):
    pass


class Logging(Handler):
    def log_request(self, code='-', size='-'):
        self.server.requests.append({'method': self.command, 'path': self.path, 'status': int(code)})

    def log_error(self, *args):
        pass


class Decoy(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'<!doctype html><title>decoy</title><p>This page is a decoy.</p>'
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    do_HEAD = do_GET

    def log_request(self, code='-', size='-'):
        self.server.requests.append({'method': self.command, 'path': self.path, 'status': int(code)})

    def log_message(self, *args):
        pass


@contextmanager
def decoys(ports, directory=None):
    """Bind only the proof's deliberate decoys; close all of them if any bind fails."""
    with ExitStack() as cleanup:
        servers = []
        for port in ports:
            handler = functools.partial(Logging, directory=str(directory)) if directory else Decoy
            try:
                server = ThreadingHTTPServer(('127.0.0.1', port), handler)
            except OSError as error:
                raise BusyPort(f'portproof: port {port} is busy; run alone ({error})') from error
            cleanup.callback(server.server_close)
            server.requests = []
            server.proof_port = port
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            cleanup.callback(thread.join)
            cleanup.callback(server.shutdown)
            servers.append(server)
        yield servers


def request_log(servers):
    return [{'port': s.proof_port, 'requests': s.requests} for s in servers]


def copy_tree(source, dest):
    shutil.copytree(source, dest, ignore=shutil.ignore_patterns(
        'series', 'HANDUP.md', '__pycache__', '.browser-scratch', 'portproof-logs'))


def mutate(root, gate):
    _, file, old, new, _ = CASES[gate]
    path = root / file
    text = path.read_text()
    if text.count(old) != 1:
        raise ValueError(f'portproof: {file}: mutation anchor occurs {text.count(old)} times')
    path.write_text(text.replace(old, new))


class Proof:
    def __init__(self, source, scratch, logs):
        self.source, self.scratch, self.logs = source, scratch, logs
        self.rows = []
        logs.mkdir(parents=True, exist_ok=False)
        self.good = scratch / 'G'
        copy_tree(source, self.good)

    @contextmanager
    def broken(self, gate):
        path = self.scratch / 'B'
        copy_tree(self.source, path)
        try:
            mutate(path, gate)
            yield path
        finally:
            shutil.rmtree(path)

    def run(self, gate, tree, label, barrier=None):
        path = self.logs / f'{gate}-{label}.log'
        with path.open('w') as output:
            if barrier:
                barrier.wait()
            start = time.monotonic()
            env = dict(os.environ, PORT=str(DECOY_PORTS[0]), AIRSHIPS_PORT=str(DECOY_PORTS[0]))
            proc = subprocess.Popen(['make', '--no-print-directory', gate], cwd=tree, env=env,
                                    stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = proc.wait(timeout=2400)
            finally:
                if proc.poll() is None:
                    os.killpg(proc.pid, signal.SIGTERM)
                    try:
                        proc.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGKILL)
                        proc.wait()
            elapsed = round(time.monotonic() - start, 2)
        print(f'{gate} {label}: exit {code}, {elapsed}s', flush=True)
        return {'exit': code, 'seconds': elapsed, 'log': path.name,
                'caught': code != 0 and CASES[gate][4] in path.read_text()}

    def record(self, phase, gate, ok, **details):
        row = dict(proof=phase, gate=gate, ok=ok, **details)
        self.rows.append(row)
        with (self.logs / 'summary.jsonl').open('a') as output:
            output.write(json.dumps(row) + '\n')
        print(json.dumps(row), flush=True)

    def requests(self, gate, phase, servers):
        rows = request_log(servers)
        path = self.logs / f'{gate}-{phase}-requests.json'
        path.write_text(json.dumps(rows, indent=2) + '\n')
        return sum(len(row['requests']) for row in rows), path.name

    def a(self, gates, before=False):
        for gate in gates:
            if gate == 'cellparity':
                continue
            with self.broken(gate) as broken:
                alone = self.run(gate, broken, 'A-alone')
                with decoys(CASES[gate][0], self.good) as servers:
                    beside = self.run(gate, broken, 'A-beside')
                count, log = self.requests(gate, 'A', servers)
                ok = alone['caught'] and (before or (beside['caught'] and count == 0))
                self.record('A-before' if before else 'A', gate, ok, alone=alone, beside=beside,
                            requests=count, request_log=log, mutation=CASES[gate][1:4])

    def b(self, gates):
        with decoys(DECOY_PORTS) as servers:
            for gate in gates:
                good = self.run(gate, self.good, 'B')
                count, log = self.requests(gate, 'B', servers)
                self.record('B', gate, good['exit'] == 0 and count == 0, good=good,
                            requests=count, request_log=log)

        count, log = self.requests('all-decoys', 'B-final', servers)
        self.record('B-audit', 'all-decoys', count == 0, requests=count, request_log=log)

    def c(self, gates):
        from concurrent.futures import ThreadPoolExecutor
        for gate in gates:
            with self.broken(gate) as broken, ThreadPoolExecutor(max_workers=2) as pool:
                barrier = threading.Barrier(2)
                g = pool.submit(self.run, gate, self.good, 'C-G', barrier)
                b = pool.submit(self.run, gate, broken, 'C-B', barrier)
                good, bad = g.result(), b.result()
                self.record('C', gate, good['exit'] == 0 and bad['caught'], good=good, bad=bad,
                            requests=None, mutation=CASES[gate][1:4])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT)
    parser.add_argument('--phase', choices=['A', 'B', 'C', 'all'], default='all')
    parser.add_argument('--gate', action='append', choices=CASES)
    parser.add_argument('--before', action='store_true')
    parser.add_argument('--log-dir', type=Path)
    args = parser.parse_args()
    if not os.environ.get('TMPDIR'):
        parser.error('set TMPDIR to disposable scratch')
    if args.before and args.phase != 'A':
        parser.error('--before requires --phase A')
    logs = args.log_dir or Path(os.environ['TMPDIR']) / ('portproof-logs-' + str(time.time_ns()))
    try:
        # Refuse a busy retired port before starting any gate or copying the tree.
        with decoys(DECOY_PORTS):
            pass
        with tempfile.TemporaryDirectory(prefix='portproof-') as td:
            proof = Proof(args.source.resolve(), Path(td), logs)
            gates = args.gate or list(CASES)
            if args.phase in ('A', 'all'):
                proof.a(gates, args.before)
            if args.phase in ('B', 'all'):
                proof.b(gates)
            if args.phase in ('C', 'all'):
                proof.c(gates)
        passed = all(row['ok'] for row in proof.rows)
        print(f'portproof: {"PASS" if passed else "FAIL"}; {len(proof.rows)} rows; logs {logs}')
        return 0 if passed else 1
    except BusyPort as error:
        print(error, file=sys.stderr)
        return EXIT_BUSY


if __name__ == '__main__':
    sys.exit(main())
