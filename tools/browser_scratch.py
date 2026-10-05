"""Disposable browser-readable scratch, honoring an explicit TMPDIR.

Confined browsers can see a different system temporary directory from Python.
Probe profile writes and file reads rather than guessing from the executable name.
An explicit TMPDIR is authoritative; unreadable scratch fails without a fallback.
Without it, try the checkout and then the account home for confined browsers.
"""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import pwd
import shlex
import sys
import tempfile
import time
from urllib.parse import urlsplit
import urllib.request

from devtools import DEFAULT_TIMEOUT, BrowserFailed, page_target

ROOT = Path(__file__).resolve().parent.parent
SCRATCH_NAME = '.browser-scratch'
TITLE = 'browser-scratch-readable'


def _page_titles(port):
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/json', timeout=1) as reply:
        return [target.get('title') for target in json.load(reply) if target.get('type') == 'page']


def _readable(directory, chrome):
    """Whether the browser writes its profile here and reads a page written here.

    The browser starts as the gates start it (devtools.page_target): the debugging port
    it writes into its profile proves the write, and the page's title proves the read.
    The probe does not wait for --dump-dom: Chrome for Testing 154 never prints the dump
    for this page, which is also why 3d/scripts/browser-tests.sh reads its page's own
    output. A failure prints the browser's stderr, the only place the cause is written.
    One cause is a long TMPDIR: Chromium aborts when the path of its singleton socket
    under TMPDIR is longer than 107 bytes.
    """
    marker = directory / 'probe.html'
    marker.write_text(f'<title>{TITLE}</title>')
    log = directory / 'probe-chromium.log'
    started = time.monotonic()
    try:
        with log.open('wb') as stderr, page_target(
                chrome, ['--no-sandbox', '--disable-gpu', '--no-default-browser-check'],
                directory / 'probe-profile', stderr=stderr, url=marker.as_uri(),
                env=dict(os.environ, TMPDIR=str(directory))) as (proc, ws_url):
            port = urlsplit(ws_url).port
            while time.monotonic() < started + DEFAULT_TIMEOUT:
                try:
                    if TITLE in _page_titles(port):
                        return True
                except (OSError, ValueError):
                    pass
                if proc.poll() is not None:
                    raise BrowserFailed(f'chromium exited with code {proc.returncode} '
                                        'before the page showed its title')
                time.sleep(0.1)
            raise BrowserFailed(f'the page did not show its title within {DEFAULT_TIMEOUT} s')
    except BrowserFailed as failure:
        lines = log.read_text(errors='replace').splitlines()
        if len(lines) > 50:
            lines = lines[:40] + [f'... {len(lines) - 50} lines omitted ...'] + lines[-10:]
        print(f'browser scratch: {chrome} failed the probe in {directory} after '
              f'{time.monotonic() - started:.1f} s: {failure}. Its stderr:',
              *(f'  {line}' for line in lines), sep='\n', file=sys.stderr)
        return False


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
