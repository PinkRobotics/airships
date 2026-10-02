#!/usr/bin/env python3
"""Recompute every committed analysis artifact in scratch; never refresh the baseline."""
from __future__ import annotations

from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / 'research/analysis'


def main():
    stale = []
    with tempfile.TemporaryDirectory(prefix='analysisfresh-') as td:
        scratch = Path(td)

        def run(argv):
            result = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
            if result.returncode:
                print(result.stdout + result.stderr, file=sys.stderr)
                raise RuntimeError(f'generator failed: {argv[1]}')

        def compare(path, output):
            if not path.is_file() or path.read_bytes() != output.read_bytes():
                stale.append(str(path.relative_to(ROOT)))

        for name in ('mass-budget', 'delivery', 'vacuum-cell', 'helium'):
            output = scratch / f'{name}.json'
            run([sys.executable, str(ANALYSIS / f'{name}.py'), '--json', str(output)])
            compare(ANALYSIS / output.name, output)

        # Use only the dated capture. No agency refresh is part of this target.
        if not (ROOT / 'data/fire-history-bc.json').is_file():
            raise RuntimeError('dated fire capture missing: data/fire-history-bc.json')
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        server = subprocess.Popen([sys.executable, '-m', 'http.server', '--bind',
                                   '127.0.0.1', str(port)], cwd=ROOT,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(100):
                if server.poll() is not None:
                    raise RuntimeError('scratch analysis server failed to start')
                try:
                    with socket.create_connection(('127.0.0.1', port), timeout=.1):
                        break
                except OSError:
                    time.sleep(.05)
            else:
                raise RuntimeError('scratch analysis server did not become ready')
            for name in ('water-availability', 'descent'):
                output = scratch / f'{name}.json'
                run([sys.executable, 'tools/js_eval.py',
                     f'http://127.0.0.1:{port}/index.html?seed=7&data=snapshot',
                     f'research/analysis/{name}.js', str(output), '20'])
                compare(ANALYSIS / output.name, output)
        finally:
            server.terminate()
            server.wait()

        output = scratch / 'ship-scoping.json'
        run([sys.executable, 'tools/ship_scoping.py', '--json', str(output)])
        compare(ANALYSIS / output.name, output)
        # Measure both new analyses and their paired notes without writing baselines.
        run([sys.executable, 'tools/check_member_census.py'])
        # The ledger generator owns its paired Markdown/JSON atomic write contract.
        run([sys.executable, 'tools/float_ledger.py', '--check'])
    if stale:
        print('analysisfresh: fresh generation differs: ' + ', '.join(stale))
        return 1
    print('analysisfresh: every analysis equals fresh generation')
    return 0


if __name__ == '__main__':
    sys.exit(main())
