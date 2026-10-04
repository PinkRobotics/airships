"""Evaluate a gate's browser probe, keeping its failure tied to the page."""
import json
from pathlib import Path
import subprocess
import sys


def run_probe(root, address, script, output, wait, *, env=None):
    result = subprocess.run([sys.executable, str(root / 'tools/js_eval.py'),
                             address, str(script), str(output), str(wait)],
                            cwd=root, capture_output=True, text=True, env=env)
    # Strip the ephemeral serving origin: the repository page is the useful identity.
    from urllib.parse import urlsplit
    page = urlsplit(address).path.lstrip('/')
    if result.returncode:
        detail = (result.stdout + result.stderr).strip()
        raise SystemExit(f'{page}: browser probe failed\n{detail}')
    try:
        record = json.loads(Path(output).read_text())
    except (OSError, ValueError) as exc:
        raise SystemExit(f'{page}: browser probe returned no readable JSON ({type(exc).__name__})')
    if not isinstance(record, dict):
        raise SystemExit(f'{page}: browser probe returned no object')
    return record


# A missing selector is data for the gate, not a JS exception that hides the key.
CHECKED_TEXT = r"""
  out.bindingFailures = [];
  const shown = (selector) => {
    const el = document.querySelector(selector);
    if (!el) {
      const key = selector.match(/data-n="([^"]+)"/)?.[1] || selector;
      out.bindingFailures.push({key, expected: selector});
      return null;
    }
    return el.textContent.replace(/,/g, '');
  };
"""


def binding_failures(page, record):
    return [f'{page}: checked key {entry["key"]}: missing binding; expected {entry["expected"]}'
            for entry in record.get('bindingFailures', [])]
