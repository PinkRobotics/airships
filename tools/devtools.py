"""Own a headless Chromium and read its chosen debugging endpoint from its profile.

page_target() uses a new profile directory, waits for DevToolsActivePort and a page
endpoint, and closes the owned process group on exit, including startup failure.
"""
from __future__ import annotations

import contextlib
import json
import os
import pathlib
import signal
import subprocess
import time
import urllib.request

# A cold CI runner is slower than a warm desktop; 60 s matches js_eval's old deadline.
DEFAULT_TIMEOUT = 60


class BrowserFailed(RuntimeError):
    """The browser exited early or did not offer a debuggable page before the deadline."""


def _wait_for(func, proc, deadline, timeout):
    """Poll func() until it returns, watching for the browser dying first."""
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise BrowserFailed(f"chromium exited with code {proc.returncode} "
                                "before opening a debuggable page")
        try:
            return func()
        except (OSError, ValueError, KeyError, IndexError, StopIteration):
            time.sleep(0.1)
    raise BrowserFailed("chromium was still running but never offered a debuggable page "
                        f"within {timeout} s")


def _chosen_port(profile: pathlib.Path):
    """Read the port the browser wrote to DevToolsActivePort in its own profile."""
    def read():
        first = (profile / "DevToolsActivePort").read_text().splitlines()[0]
        port = int(first)
        if not 0 < port < 65536:
            raise ValueError(port)
        return port
    return read


def _page_ws_url(port: int):
    def read():
        tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=1))
        return next(t["webSocketDebuggerUrl"] for t in tabs if t["type"] == "page")
    return read


@contextlib.contextmanager
def page_target(chrome, flags, profile, stderr=subprocess.DEVNULL,
                timeout=DEFAULT_TIMEOUT):
    """Yield (proc, ws_url): a headless Chromium on a debugging port it chose itself.

    `flags` are the caller's own — renderer, window, confinement. The debug port, the
    profile wiring and the teardown belong to this module. `profile` is the user-data-dir
    to create; an existing directory is refused so a stale endpoint cannot be reused.
    """
    profile = pathlib.Path(profile)
    profile.mkdir(parents=True, exist_ok=False)
    if any(flag.startswith(('--remote-debugging-', '--user-data-dir')) for flag in flags):
        raise ValueError('debugging and profile flags belong to page_target')
    proc = subprocess.Popen(
        [chrome, "--headless=new", "--remote-debugging-port=0", "--remote-allow-origins=*",
         "--remote-debugging-address=127.0.0.1", "--disable-background-networking",
         "--disable-component-update", "--disable-sync", "--no-first-run",
         f"--user-data-dir={profile}", *flags, "about:blank"],
        stdout=subprocess.DEVNULL, stderr=stderr, start_new_session=True)
    deadline = time.monotonic() + timeout
    try:
        port = _wait_for(_chosen_port(profile), proc, deadline, timeout)
        ws_url = _wait_for(_page_ws_url(port), proc, deadline, timeout)
        yield proc, ws_url
    finally:
        # The browser and every process it forked, as one group.
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()
