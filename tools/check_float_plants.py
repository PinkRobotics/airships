#!/usr/bin/env python3
"""Require a full-plants pass for these exact gate contents; --run earns the receipt.

The tracked receipt is portable and deterministic, not a signature. See
tools/FLOAT-PLANTS.md for its scope and the independent CI check.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
RECORD = 'research/analysis/float-plants-pass.json'
SCHEMA = 'float-plants-pass/1'
GLOBS = ('tools/float_*.py', 'tools/check_float_*.py', 'tools/tests/test_float_*.py')
REQUIRED = (
    'tools/float_text.py', 'tools/float_claims.py', 'tools/check_float_ledger.py',
    'tools/check_float_plants.py', 'tools/review_gate_motion.py',
    'tools/update_float_records.py', 'tools/tests/float_plants.py',
    'tools/tests/test_float_hardening.py', 'tools/tests/test_float_motion.py',
    'tools/tests/test_float_plant_state.py',
)
EXTRA = ('tools/float_dispositions.json', 'tools/float_verdict_templates.json',
         'tools/gen_float_pages.py', 'tools/gen_float_verdicts.py', 'tools/numeric_tokens.py')
RULES = ('ledgercheck', 'ledgercheck-selftest', 'floatplants', 'floatplantshard', 'floatplantcheck')
BASELINES = ('unplanted', 'unplanted-floatpagecheck', 'unplanted-censuscheck',
             'unplanted-cellparity')


def expected_cases():
    sys.path.insert(0, str(ROOT / 'tools/tests'))
    from test_float_hardening import specs
    return sorted(specs())


def parse_shard(value):
    if not re.fullmatch(r'[1-9][0-9]*/[1-9][0-9]*', value):
        raise ValueError('shard must be I/N with 1 <= I <= N')
    index, count = map(int, value.split('/'))
    if index > count:
        raise ValueError('shard must be I/N with 1 <= I <= N')
    return index, count


def shard_cases(cases, index, count):
    """Sorted round-robin: case i belongs to shard (i mod N) + 1."""
    if (type(index) is not int or type(count) is not int
            or not 1 <= index <= count <= len(cases) or len(set(cases)) != len(cases)):
        raise ValueError('shards must partition unique cases with no empty shard')
    return sorted(cases)[index - 1::count]


def snapshot(root=ROOT):
    paths = set(REQUIRED) | set(EXTRA)
    for pattern in GLOBS:
        paths.update(p.relative_to(root).as_posix() for p in root.glob(pattern))
    hashes = {}
    for rel in sorted(paths):
        path = root / rel
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'{rel}: gate inputs must be files inside the tree')
        try:
            hashes[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            raise ValueError(f'{rel}: gate input is missing or unreadable') from None
    # Only the claim gate recipes: unrelated Makefile edits need no new receipt.
    makefile = (root / 'Makefile').read_text(encoding='utf-8')
    for target in RULES:
        rules = re.findall(r'^' + target + r':[^\n]*\n(?:\t[^\n]*\n)*', makefile, re.M)
        if len(rules) != 1:
            raise ValueError(f'Makefile: expected one explicit {target} recipe')
        hashes['Makefile#' + target] = hashlib.sha256(rules[0].encode()).hexdigest()
    cases = expected_cases()
    content = dict(files=hashes, cases=cases)
    digest = hashlib.sha256(json.dumps(content, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return dict(schema=SCHEMA, sha256=digest, **content)


def check(root=ROOT):
    current = snapshot(root)
    try:
        recorded = json.loads((root / RECORD).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return f'{RECORD}: missing or invalid receipt; run make floatplants'
    if recorded != current:
        old = recorded.get('files', {}) if isinstance(recorded, dict) else {}
        if not isinstance(old, dict):
            old = {}
        changed = sorted(k for k in old.keys() | current['files'].keys()
                         if old.get(k) != current['files'].get(k))
        detail = ', '.join(changed) or 'receipt schema, digest or case list'
        return f'gate contents differ from the full-plants pass: {detail}; run make floatplants'
    return None


def validate_report(rows, cases):
    """A zero exit alone cannot certify an empty, selected or observe-only run."""
    wanted = set(cases) | set(BASELINES)
    ids = [row['id'] for row in rows]
    if len(ids) != len(set(ids)) or set(ids) != wanted:
        raise ValueError('full plant report has missing, duplicate or unexpected cases')
    for row in rows:
        if type(row['green']) is not bool or type(row['code']) is not int:
            raise ValueError(f'{row["id"]}: invalid plant result')
        if row['green'] != (row['code'] == 0):
            raise ValueError(f'{row["id"]}: plant did not give its required result')
        if not row['green'] and row['expected'] not in row['output']:
            raise ValueError(f'{row["id"]}: refusal lacks its expected reason')


def run_full(root=ROOT):
    before = snapshot(root)
    scratch = os.environ.get('TMPDIR')
    if not scratch:
        raise ValueError('set TMPDIR to test scratch before make floatplants')
    with tempfile.TemporaryDirectory(prefix='float-pass-', dir=scratch) as tmp:
        report = Path(tmp) / 'report.json'
        env = dict(os.environ, FLOAT_PLANT_MODE='all', FLOAT_PLANT_CASES='',
                   FLOAT_PLANT_REPORT=str(report), PYTHONDONTWRITEBYTECODE='1')
        command = [sys.executable, '-m', 'unittest', 'discover', '-v',
                   '-s', 'tools/tests', '-p', 'test_float_hardening.py']
        run = subprocess.run(command, cwd=root, env=env)
        if run.returncode:
            return run.returncode
        try:
            rows = json.loads(report.read_text(encoding='utf-8'))
            validate_report(rows, before['cases'])
        except (OSError, ValueError, KeyError, TypeError):
            raise ValueError('full plants did not produce a complete passing report; receipt unchanged') from None
        if snapshot(root) != before:
            raise ValueError('gate inputs changed during full plants; receipt unchanged; run make floatplants')
        destination = root / RECORD
        body = json.dumps(before, sort_keys=True, indent=2) + '\n'
        # Replace only after all checks succeed; a failed run preserves the old pass.
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=destination.parent,
                                         prefix='.float-pass-', delete=False) as file:
            temporary = Path(file.name)
            file.write(body)
        try:
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
    print(f'Full plants PASS: {len(before["cases"])} cases; recorded {RECORD}; sha256 {before["sha256"]}')
    return 0


def run_shard(value, root=ROOT):
    index, count = parse_shard(value)
    before = snapshot(root)
    cases = shard_cases(before['cases'], index, count)
    scratch = os.environ.get('TMPDIR')
    if not scratch:
        raise ValueError('set TMPDIR to test scratch before make floatplantshard')
    with tempfile.TemporaryDirectory(prefix='float-shard-', dir=scratch) as tmp:
        report = Path(tmp) / 'report.json'
        env = dict(os.environ, FLOAT_PLANT_MODE='all', FLOAT_PLANT_CASES=','.join(cases),
                   FLOAT_PLANT_REPORT=str(report), PYTHONDONTWRITEBYTECODE='1')
        command = [sys.executable, '-m', 'unittest', 'discover', '-v',
                   '-s', 'tools/tests', '-p', 'test_float_hardening.py']
        run = subprocess.run(command, cwd=root, env=env)
        if run.returncode:
            return run.returncode
        try:
            rows = json.loads(report.read_text(encoding='utf-8'))
            validate_report(rows, cases)
        except (OSError, ValueError, KeyError, TypeError):
            raise ValueError('shard plants did not produce a complete passing report; no receipt written') from None
        if snapshot(root) != before:
            raise ValueError('gate inputs changed during shard plants; no receipt written')
    print(f'Shard {index}/{count} PASS: {len(cases)} cases and {len(BASELINES)} baselines; no receipt written')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--run', action='store_true', help='run all plants and record their exact gate state')
    modes.add_argument('--shard', metavar='I/N', help='run a sorted round-robin share and baselines; never write a receipt')
    args = parser.parse_args()
    try:
        if args.run:
            return run_full()
        if args.shard is not None:
            return run_shard(args.shard)
        error = check()
        if error:
            print('floatplantcheck FAIL: ' + error)
            return 1
        print('floatplantcheck PASS: gate contents match the recorded full-plants pass')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # OSError may contain a local absolute filename; never print that filename.
        reason = str(exc) if not isinstance(exc, OSError) else 'cannot read or write plant state'
        print('floatplantcheck FAIL: ' + reason + '; run make floatplants', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
