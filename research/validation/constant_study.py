#!/usr/bin/env python3
"""Counterfactual only: regenerate published outputs in two disposable current-tree copies.

Run with an explicit TMPDIR. The repository and its constants are never written.
Output tables go to --out (a JSON file); an adjacent Markdown table lists every leaf.
No network inputs: browser URLs use the bundled snapshot and the committed fire history.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from serve import serve_tree
OUTPUTS = ['research/figures.json'] + [f'research/analysis/{name}.json' for name in
    ('mass-budget', 'delivery', 'vacuum-cell', 'helium', 'water-availability', 'descent')]
OUTPUTS += ['research/geometry/skin/loaded-skin.json', 'ship/skin.generated.js',
            'research/validation/report.json']
CHANGES = ['sim/atmosphere.js', 'research/analysis/vacuum-cell.py',
           'research/analysis/helium.py', 'research/analysis/mass-budget.py', 'tools/gen_skin.py']


def flattened(value, path=''):
    if isinstance(value, dict):
        return {k2: v2 for k, v in value.items()
                for k2, v2 in flattened(v, path+'/'+str(k)).items()}
    if isinstance(value, list):
        return {k2: v2 for k, v in enumerate(value)
                for k2, v2 in flattened(v, path+'/'+str(k)).items()}
    return {path: value}


def load(path):
    s = path.read_text()
    if path.suffix == '.js':
        s = s.split('export const SKIN = ', 1)[1].split(';', 1)[0]
    return flattened(json.loads(s))


def run(root, command, log):
    print(root.name+': '+' '.join(command), flush=True)
    p = subprocess.run(command, cwd=root, text=True, capture_output=True, timeout=900,
                       env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    recorded_command = [re.sub(r'http://127\.0\.0\.1:\d+/', '{base}', arg) for arg in command]
    log.append({'variant': root.name, 'command': recorded_command, 'exit': p.returncode,
                'output': (p.stdout+p.stderr).replace(str(root), '<scratch-copy>')[-4000:]})
    if p.returncode:
        raise RuntimeError(f'{root.name}: {command[0]} exited {p.returncode}: '+p.stderr[-1000:])


def regenerate(root, log):
    with serve_tree(root) as base:
        for script, output in [('tools/figures_dump.js', 'research/figures.json'),
                               ('research/analysis/water-availability.js', 'research/analysis/water-availability.json'),
                               ('research/analysis/descent.js', 'research/analysis/descent.json')]:
            run(root, ['python3', '-B', 'tools/js_eval.py',
                       f'{base}index.html?seed=7&data=snapshot', script, output, '20'], log)
    for name in ['mass-budget', 'delivery', 'vacuum-cell', 'helium']:
        run(root, ['python3', '-B', f'research/analysis/{name}.py', '--json', f'research/analysis/{name}.json'], log)
    run(root, ['python3', '-B', 'tools/gen_skin.py'], log)
    run(root, ['python3', '-B', 'research/validation/check.py', '--update'], log)


def compare(old, new):
    differences = []
    for filename in OUTPUTS:
        a, b = load(old/filename), load(new/filename)
        for key in sorted(a.keys() | b.keys()):
            if a.get(key) != b.get(key):
                differences.append(dict(file=filename, field=key, old=a.get(key), new=b.get(key),
                                        difference=b[key]-a[key] if isinstance(a.get(key), (int,float))
                                        and isinstance(b.get(key), (int,float)) else None))
    return differences


def write_study(result, output):
    """Canonical report writer; numerical results come from the recorded fresh runs."""
    result['source_basis'] = 'Current working files; base_commit names HEAD, not the uncommitted candidate tree.'
    for command in result['commands']:
        command['command'] = [re.sub(r'http://127\.0\.0\.1:\d+/', '{base}', arg)
                              for arg in command['command']]
    output.write_text(json.dumps(result, indent=2)+'\n')
    lines = ['# Counterfactual dry-air constant study', '',
             'Scratch copies only. Only the chosen dry-air constant changes; other gas constants and density dials stay unchanged.',
             f'Old: JS 287.0528; Python 287.05. New: 8314.32 / 28.9644 = {result['standard_R_air']!r} J/(kg K).', '',
             f'{len(result['changed_fields'])} changed leaves. Baseline regeneration drift: {len(result['baseline_regeneration_drift'])} leaves.', '',
             'Old means a fresh original-constant run. Published old names the captured current working-tree cache; '
             'any difference between these columns predates the constant change.', '',
             '| Published/generated file | Field | Published old | Fresh old | Standard R | Constant effect |',
             '| --- | --- | ---: | ---: | ---: | ---: |']
    for row in result['changed_fields']:
        vals = [row[k] for k in ('file', 'field', 'published_old', 'old', 'new', 'difference')]
        lines.append('| '+' | '.join(str(x).replace('|', '\\|').replace('\n',' ') for x in vals)+' |')
    output.with_suffix('.md').write_text('\n'.join(lines)+'\n')
    print(f'constant study: {len(result['changed_fields'])} changed leaves; baseline drift {len(result['baseline_regeneration_drift'])}', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--normalize', action='store_true', help='rewrite report metadata from an already completed fresh run; no numerical changes')
    ap.add_argument('--check', action='store_true', help='compare both report files with fresh original/standard-constant runs; write nothing to the repository')
    args = ap.parse_args()
    if args.normalize and args.check:
        ap.error('--normalize and --check are separate operations')
    if args.normalize:
        write_study(json.loads(args.out.read_text()), args.out)
        return
    if not os.environ.get('TMPDIR'):
        ap.error('an explicit TMPDIR is required')
    r_air = 8314.32 / 28.9644  # 1976 prose R* / dry-air molar mass; not the Table 2 exponent error.
    log = []
    with tempfile.TemporaryDirectory(prefix='constant-study-', dir=os.environ['TMPDIR']) as tmp:
        tmp = Path(tmp)
        base = tmp/'original'
        base.mkdir()
        # Use the current files so a later closure fix is included. No older revision
        # is opened; untracked worker hand-ups and replay artifacts are not inputs.
        tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
        for filename in filter(None, tracked):
            if filename == 'docs/HANDOFF.md':
                continue
            src, dest = ROOT/filename, base/filename
            if src.is_file():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dest)
        before, after = tmp/'old', tmp/'standard'
        shutil.copytree(base, before)
        shutil.copytree(base, after)
        replacements = []
        for filename in CHANGES:
            p = after/filename
            old = p.read_text()
            new, count = re.subn(r'(?<![\d.])287\.05(?:28)?(?![\d.])', repr(r_air), old)
            if not count:
                raise ValueError('no constant in '+filename)
            p.write_text(new)
            replacements.append(dict(file=filename, occurrences=count))
        regenerate(before, log)
        regenerate(after, log)
        differences = compare(before, after)
        baseline_drift = compare(base, before)
        drift_index = {(r['file'], r['field']): r for r in baseline_drift}
        for row in differences:
            drift = drift_index.get((row['file'], row['field']))
            row['published_old'] = drift['old'] if drift else row['old']
        result = {'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  'source_basis': 'Current working files; base_commit names HEAD, not the uncommitted candidate tree.',
                  'old_R_air': {'JS': 287.0528, 'Python': 287.05}, 'standard_R_air': r_air,
                  'standard_definition': '8314.32 J/(kmol K) / 28.9644 kg/kmol',
                  'replacements': replacements, 'outputs': OUTPUTS,
                  'baseline_regeneration_drift': baseline_drift, 'changed_fields': differences, 'commands': log}
    if args.check:
        with tempfile.TemporaryDirectory(prefix='constant-report-', dir=os.environ['TMPDIR']) as report:
            fresh=Path(report)/args.out.name
            write_study(result,fresh)
            changed=[p.name for p in [args.out,args.out.with_suffix('.md')]
                     if not p.is_file() or p.read_bytes()!=fresh.with_suffix(p.suffix).read_bytes()]
        if changed:
            print('FAIL stale constant study: '+', '.join(changed))
            raise SystemExit(1)
        print('PASS constant study: JSON and Markdown match fresh original and standard-constant runs')
    else:
        write_study(result, args.out)


if __name__ == '__main__':
    main()
