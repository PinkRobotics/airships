"""Disposable browser-readable scratch, honoring an explicit TMPDIR.

Confined browsers can see a different system temporary directory from Python.
Probe profile writes and file reads rather than guessing from the executable name.
An explicit TMPDIR is authoritative; unreadable scratch fails without a fallback.
Without it, try the checkout and then the account home for confined browsers.
"""
from contextlib import contextmanager
import os
from pathlib import Path
import pwd
import shlex
import signal
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
SCRATCH_NAME = '.browser-scratch'


def _readable(directory, chrome):
    marker = directory / 'probe.html'
    marker.write_text('<title>browser-scratch-readable</title>')
    env = dict(os.environ, TMPDIR=str(directory))
    proc = subprocess.Popen(
        [chrome, '--headless', '--no-sandbox', '--disable-gpu',
         '--disable-background-networking', '--no-first-run', '--no-default-browser-check',
         f'--user-data-dir={directory / "probe-profile"}', '--dump-dom', marker.as_uri()],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        try:
            out, _ = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            return False
        return (proc.returncode == 0 and b'<title>browser-scratch-readable</title>' in out
                and (directory / 'probe-profile' / 'Local State').is_file())
    finally:
        # Reap only this probe and the descendants in its own process group.
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.communicate()


@contextmanager
def browser_scratch(chrome='chromium'):
    """Yield scratch and route child js_eval profiles there; remove it on exit."""
    home = Path(pwd.getpwuid(os.getuid()).pw_dir).resolve()
    requested = os.environ.get('TMPDIR')
    parents = (Path(requested),) if requested else (ROOT / SCRATCH_NAME, home)
    for parent in dict.fromkeys(parents):
        try:
            if parent != home:
                parent.mkdir(exist_ok=True)
            temporary = tempfile.TemporaryDirectory(prefix='browser-check-', dir=parent)
        except OSError:
            continue
        with temporary as name:
            directory = Path(name)
            if not _readable(directory, chrome):
                continue
            location = ('TMPDIR/' if requested else f'./{SCRATCH_NAME}/' if parent != home else '~/') + directory.name
            reason = '' if requested or parent != home else 'checkout unavailable to Chromium; using account home; '
            cleanup = shlex.quote(str(directory))
            print(f'browser scratch: {reason}{location} (removed on exit; if interrupted, '
                  f'remove with rm -rf -- {cleanup}).',
                  file=sys.stderr)
            previous = {key: os.environ.get(key) for key in ('TMPDIR', 'AIRSHIPS_TMPDIR')}
            try:
                os.environ.update(TMPDIR=name, AIRSHIPS_TMPDIR=name)
                yield name
            finally:
                for key, value in previous.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value
            return
    if requested:
        raise RuntimeError('Chromium could not read and write explicit TMPDIR; check confinement')
    raise RuntimeError('Chromium could not read and write disposable scratch in the checkout '
                       'or account home; check browser confinement and checkout permissions')
