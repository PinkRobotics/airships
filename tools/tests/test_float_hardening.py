"""Counterexamples on copies of the tracked tree; never plant in the checkout.

Run directly with --observe to record old-gate misses without suppressing their failures.
FLOAT_PLANT_REPORT names an optional JSON evidence file outside the tracked tree.
"""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import float_plants


def specs():
    cases = {}
    def register(name, description, edits=(), json_edits=(), gates=(), commands=(), py_edits=()):
        cases[name] = dict(description=description, edits=edits, json_edits=json_edits,
                           py_edits=py_edits, gates=gates, commands=commands)
    float_plants.register(register)
    cases['M1-concept'] = dict(edits=[('concept/index.html', '</body>',
        '<p>The hull is lighter than the air it pushes aside, so it rises on its own.</p>\n</body>')])
    cases['M2-dated-audit'] = dict(append=('docs/audit/26-10-02-energy-carry.md',
        '\nThe 52 m hull floats at sea level.\n'))
    cases['M5-landing-body'] = dict(append=('docs/governance/landing-attestations.md',
        '\nThe 52 m hull floats at sea level.\n'))
    # The exact landing heading is the positive control for the narrow history shape.
    cases['M5-landing-heading'] = dict(append=('docs/governance/landing-attestations.md',
        '\n## Landing 999 — The float gate hardening\n'), green=True)
    # Each A5 sentence must fail independently; an aggregate red hides missing sentences.
    phrasings = ['The 52 m hull floats.', 'The 52 m hull is neutrally buoyant at sea level.',
        'The 52 m hull is lighter than the air it displaces.',
        'On the drawn hull, lift exceeds weight at sea level.',
        'The drawn hull’s net lift is positive at sea level.',
        'The 52 m hull rises unaided from the ground.',
        'The 52 m hull carries its own structure with lift to spare.',
        'The 52 m hull needs ballast to stay down.',
        'The 52 m hull weighs less than nothing in air.',
        'On the drawn hull the deficit is closed at sea level.']
    for i, sentence in enumerate(phrasings, 1):
        for file in ('docs/FLOAT.md', 'index.html'):
            cases[f'M1-phrase-{i:02}-{Path(file).stem}'] = dict(append=(file,
                '\n'+(f'<p>{sentence}</p>' if file.endswith('.html') else sentence)+'\n'))
    # All three qualifier attacks stay red after regenerating their served pages too.
    for name in ('A2c-basis-swap', 'A4-altitude-swap', 'A4-short-to-over'):
        cases[name+'-rendered'] = dict(cases[name], regenerate=['floatpages'])
    return cases


def command(root, argv):
    p = subprocess.run(argv, cwd=root, text=True, capture_output=True, timeout=240)
    return p.returncode, p.stdout + p.stderr


def copy_tree(destination, files, source=ROOT):
    for rel in files:
        src = source / rel
        if not src.is_file():
            continue
        dst = destination / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    # Read-only repository identity/history, no git mutation runs in the plant harness.
    (destination / '.git').symlink_to((ROOT / '.git').resolve(), target_is_directory=True)


def plant(root, spec):
    for file, old, new in spec.get('edits', ()):
        p = root / file
        text = p.read_text()
        if text.count(old) != 1:
            raise AssertionError(f'{file}: plant anchor occurs {text.count(old)} times')
        p.write_text(text.replace(old, new))
    for file, fn in spec.get('json_edits', ()):
        p = root / file
        doc = json.loads(p.read_text())
        fn(doc)
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=1)+'\n')
    for file, fn in spec.get('py_edits', ()):
        p = root / file
        p.write_text(fn(p.read_text()))
    if 'append' in spec:
        file, text = spec['append']
        p = root / file
        p.write_text(p.read_text()+text)


def run_case(root, name, spec):
    previous = Path.cwd()
    try:
        os.chdir(root)  # Supplied callbacks open relative paths in this disposable copy.
        plant(root, spec)
    finally:
        os.chdir(previous)
    outputs = []
    regen = spec.get('regenerate', [])
    if name == 'A7b-sf-regenerated':
        regen = ['ledger', 'floatpages']
    for target in regen:
        code, out = command(root, ['make', target])
        if code:
            if name == 'A7b-sf-regenerated' and 'SELF-CHECK FAILED' in out:
                return dict(id=name,code=code,expected='SELF-CHECK FAILED',command='make '+target,output=out,green=False)
            raise AssertionError(f'{name}: regeneration failed: {out}')
        outputs.append(out)
    if name.startswith('A9-float-'):
        argv = ['make', 'floatpagecheck']
        expected = 'differs from a fresh render'
    elif name.startswith('A10-'):
        argv = ['make', 'censuscheck']
        expected = 'CENSUS CHECK FAILED'
    elif name == 'A7-jsmirror-knockdown':
        argv = ['make', 'cellparity']
        expected = 'CELL PARITY'
    else:
        argv = ['make', 'ledgercheck']
        expected = ('fresh generation differs' if name == 'A3-hand-ledger' else
                    'SELF-CHECK FAILED' if name.startswith('A7-') else
                    'record line' if name == 'A8-wrong-line' else
                    'basis qualifier' if name.startswith('A2c') else
                    'figure qualifier' if name.startswith('A4-altitude') or name.startswith('A4b-altitude') else
                    'margin sign' if name.startswith('A4-short') else
                    'requires a checked binding' if name == 'A6-classes' else
                    'stale entry' if name in ('A8-orphan', 'A8-onechar') else
                    'float-claims' if name == 'A8-dup-shard' else
                    'reason must' if name == 'A8-empty-reason' else
                    'bound figure' if name in ('A2a-float-shown','A2b-readme-shown','A4-transpose','A4-20-places') else
                    'ratios print to three decimals' if name.startswith('A4-round') else
                    'No disposition')
    code, out = command(root, argv)
    outputs.append(out)
    return dict(id=name, code=code, expected=expected, command=' '.join(argv),
                output='\n'.join(outputs), green=spec.get('green', False))


# One case per distinct finding, plus every positive control. The complete suite
# remains mandatory for changes to the tools, schema or plants.
FAST_CASES = (
    'A1-float-headline', 'A2a-float-shown', 'A2c-basis-swap', 'A3-hand-ledger',
    'A4-altitude-swap', 'A4-short-to-over', 'A4-round-1.00', 'A6-classes',
    'A7-knockdown', 'A7-jsmirror-knockdown', 'A8-orphan', 'A8-dup-shard',
    'A8-wrong-line', 'A8-empty-reason', 'A9-float-index', 'A10-census-json',
)


def workers():
    value = os.environ.get('FLOAT_PLANT_WORKERS')
    count = int(value) if value is not None else (os.cpu_count() or 1)
    if count < 1:
        raise ValueError('FLOAT_PLANT_WORKERS must be a positive integer')
    return min(count, 8)


def selected_cases(mode):
    cases = specs()
    if mode == 'all':
        return cases
    if mode != 'fast':
        raise ValueError('FLOAT_PLANT_MODE must be all or fast')
    return {name: spec for name, spec in cases.items()
            if name in FAST_CASES or spec.get('green')}


def run_one(base, files, name):
    # Callbacks are built inside this process; no closure is pickled. chdir in
    # run_case is process-local, so independent plants cannot cross trees.
    with tempfile.TemporaryDirectory(prefix='case-', dir=base.parent) as td:
        tree = Path(td)
        copy_tree(tree, files, source=base)
        started = time.monotonic()
        row = run_case(tree, name, specs()[name])
        row['seconds'] = round(time.monotonic() - started, 3)
        return row


class PlantedTree(unittest.TestCase):
    def test_counterexamples(self):
        scratch = Path(os.environ['TMPDIR'])
        scratch.mkdir(parents=True, exist_ok=True)
        tracked = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT).decode().split('\0')
        files = sorted({f for f in tracked if f and not f.startswith(('inputs/', 'series/')) and f != 'HANDUP.md'} | {
            'tools/tests/float_plants.py', 'tools/tests/test_float_hardening.py'})
        rows = []
        mode = os.environ.get('FLOAT_PLANT_MODE', 'all')
        cases = selected_cases(mode)
        count = workers()
        print(f'Plant suite: {mode}; {len(cases)} cases; {count} workers', flush=True)
        try:
            with tempfile.TemporaryDirectory(prefix='float-plants-', dir=scratch) as tmp:
                base = Path(tmp) / 'base'
                base.mkdir()
                copy_tree(base, files)
                for target in ('ledgercheck','floatpagecheck','censuscheck','cellparity'):
                    code, out = command(base, ['make', target])
                    rows.append(dict(id='unplanted' if target=='ledgercheck' else 'unplanted-'+target, code=code, output=out, green=True))
                    self.assertEqual(code, 0, out)
                with ProcessPoolExecutor(max_workers=count) as pool:
                    futures = [pool.submit(run_one, base, files, name) for name in cases]
                    # Read futures in registration order, never completion order. Each
                    # case's complete stdout/stderr stays in its row in the report.
                    for name, future in zip(cases, futures):
                        with self.subTest(plant=name):
                            row = future.result()
                            rows.append(row)
                            print(f'PLANT {name}: {"GREEN" if row["code"] == 0 else "RED"}', flush=True)
                            if not OBSERVE:
                                if row['green']:
                                    self.assertEqual(row['code'], 0, row['output'])
                                else:
                                    self.assertNotEqual(row['code'], 0, row['output'])
                                    self.assertIn(row['expected'], row['output'])
        finally:
            if report := os.environ.get('FLOAT_PLANT_REPORT'):
                Path(report).write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n')


OBSERVE = '--observe' in sys.argv
if __name__ == '__main__':
    if OBSERVE:
        sys.argv.remove('--observe')
    unittest.main()
