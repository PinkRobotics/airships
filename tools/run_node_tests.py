#!/usr/bin/env python3
"""Run the existing Node suites and require every committed test identity."""
import os
import tempfile
from pathlib import Path
import subprocess
import sys
from test_inventory import ROOT, check_files, check_record, console_record, run_native


def main():
    bad = check_files('shared') + check_files('node')
    for line in bad:
        print(line, file=sys.stderr)
    if bad:
        return 1
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / 'modules.log'
        env = dict(os.environ, TEST_INVENTORY_MODULE_LOG=str(log))
        shared = subprocess.run(['node', '--import=./tools/test_inventory_boot.mjs', 'tests/node/run.mjs'],
                                cwd=ROOT, capture_output=True, text=True, env=env)
        loaded = sorted(set(log.read_text().splitlines())) if log.exists() else []
    print('\n'.join(line for line in shared.stdout.splitlines()
                    if not line.startswith('TEST_INVENTORY ')))
    print(shared.stderr, end='', file=sys.stderr)
    try:
        record = console_record(shared.stdout, 'shared')
        record['files'] = loaded
        good = check_record('shared', record)
    except (ValueError, KeyError) as exc:
        print(f'test inventory shared: invalid runner record: {exc}', file=sys.stderr)
        good = False
    if shared.returncode:
        return shared.returncode
    try:
        native, record = run_native()
    except (OSError, ValueError, KeyError) as exc:
        print(f'test inventory node: invalid runner record: {exc}', file=sys.stderr)
        return 1
    print(native.stdout, end='')
    good = check_record('node', record) and good
    print(native.stderr, end='', file=sys.stderr)
    return native.returncode or int(not good)


if __name__ == '__main__':
    sys.exit(main())
