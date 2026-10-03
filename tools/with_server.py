#!/usr/bin/env python3
"""Run a command with each {base} replaced by this tree's bound base address.

    python3 tools/with_server.py -- command '{base}path'

The server listens before the command starts. It closes when the command finishes,
including on failure or a termination signal. The command's status is preserved.
"""
import os
import signal
import subprocess
import sys

from serve import serve_tree


def main():
    if len(sys.argv) < 3 or sys.argv[1] != '--':
        print(__doc__, file=sys.stderr)
        return 2

    def interrupted(signum, _frame):
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, interrupted)
    with serve_tree() as base:
        command = [part.replace('{base}', base) for part in sys.argv[2:]]
        proc = subprocess.Popen(command, start_new_session=True)
        try:
            return proc.wait()
        finally:
            # The command's own group, including children still alive after it exits.
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=5)
            finally:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()


if __name__ == '__main__':
    sys.exit(main())
