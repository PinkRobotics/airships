#!/usr/bin/env python3
"""Fail if research/figures.json has drifted from the model that is supposed to produce it.

    python3 tools/check_figures_fresh.py

WHY THIS EXISTS, and it is the most important check in the repository.

`tools/check_figures.py` compares every number in the reports against `research/figures.json`
and prints "N cited figures match the model". That sentence was not true. `figures.json` is a
COMMITTED CACHE, regenerated only by `make factsheet`, which was in neither `make check` nor CI.

The failure is reachable through the documented workflow. Change a constant in `sim/`, update
the golden baselines the way `tests/README.md` says to, and run the whole gate: boundaries,
stamps, figures, goldens, 204 tests, 103 node tests, 32 browser tests, 25 interactions — all
green, while six published figures are wrong and two of them are wrong by 20%. The gate was
loudest exactly when it was lying, because its success line named the model and compared a file.

So: regenerate into scratch, compare, and fail on any difference. One browser start. It converts
the claim from "the reports agree with a file someone remembered to update" into the one the
README actually makes.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from serve import serve_tree

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMMITTED = ROOT / 'research' / 'figures.json'


def flatten(obj, prefix=''):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f'{prefix}{k}.'))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, f'{prefix}{i}.'))
    else:
        out[prefix[:-1]] = obj
    return out


def main() -> int:
    with tempfile.TemporaryDirectory(prefix='figfresh-') as td, serve_tree(ROOT) as base:
        scratch = pathlib.Path(td) / 'fresh.json'
        r = subprocess.run(
            [sys.executable, str(ROOT / 'tools' / 'js_eval.py'),
             f'{base}index.html?seed=7&data=snapshot',
             str(ROOT / 'tools' / 'figures_dump.js'), str(scratch), '20'],
            capture_output=True, text=True, errors='replace', cwd=ROOT, timeout=180)
        if r.returncode or not scratch.exists():
            print('check_figures_fresh: could not regenerate from the model\n'
                  + r.stdout[-1500:] + r.stderr[-1500:], file=sys.stderr)
            return 1
        fresh = flatten(json.loads(scratch.read_text()))
        have = flatten(json.loads(COMMITTED.read_text()))

    # `generated.*` is provenance, not a figure — it records how the file was made.
    keys = {k for k in set(fresh) | set(have) if not k.startswith('generated.')}
    drift = sorted(k for k in keys if fresh.get(k) != have.get(k))
    if not drift:
        print(f'check_figures_fresh: figures.json matches the live model ({len(keys)} figures)')
        return 0

    print(f'check_figures_fresh: figures.json is stale — {len(drift)} of {len(keys)} figures '
          'differ from what the model produces now:', file=sys.stderr)
    for k in drift[:25]:
        print(f'  {k}: committed {have.get(k)!r}, model says {fresh.get(k)!r}', file=sys.stderr)
    if len(drift) > 25:
        print(f'  … and {len(drift) - 25} more', file=sys.stderr)
    print('\nEvery report citing one of these is publishing a number the model no longer '
          'produces.\nRun `make factsheet`, read the diff, and commit it.', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
