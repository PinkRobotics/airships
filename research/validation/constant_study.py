#!/usr/bin/env python3
"""Counterfactual only: regenerate published outputs in two disposable HEAD copies.

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
import socket
import subprocess
import sys
import tarfile
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
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
    log.append({'variant': root.name, 'command': command, 'exit': p.returncode,
                'output': (p.stdout+p.stderr).replace(str(root), '<scratch-copy>')[-4000:]})
    if p.returncode:
        raise RuntimeError(f'{root.name}: {command[0]} exited {p.returncode}: '+p.stderr[-1000:])


def regenerate(root, log):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    server = subprocess.Popen([sys.executable, 'tools/serve.py', '--port', str(port), '--quiet'],
                              cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1)
        for script, output in [('tools/figures_dump.js', 'research/figures.json'),
                               ('research/analysis/water-availability.js', 'research/analysis/water-availability.json'),
                               ('research/analysis/descent.js', 'research/analysis/descent.json')]:
            run(root, ['python3', '-B', 'tools/js_eval.py',
                       f'http://127.0.0.1:{port}/index.html?seed=7&data=snapshot', script, output, '20'], log)
    finally:
        server.terminate()
        server.wait(timeout=10)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    if not os.environ.get('TMPDIR'):
        ap.error('an explicit TMPDIR is required')
    r_air = 8314.32 / 28.9644  # 1976 prose R* / dry-air molar mass; not the Table 2 exponent error.
    log = []
    with tempfile.TemporaryDirectory(prefix='constant-study-', dir=os.environ['TMPDIR']) as tmp:
        tmp = Path(tmp)
        archive = tmp/'base.tar'
        with archive.open('wb') as f:
            subprocess.run(['git', 'archive', 'HEAD'], cwd=ROOT, stdout=f, check=True)
        base = tmp/'original'
        base.mkdir()
        with tarfile.open(archive) as f:
            f.extractall(base, filter='data')
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
                  'old_R_air': {'JS': 287.0528, 'Python': 287.05}, 'standard_R_air': r_air,
                  'standard_definition': '8314.32 J/(kmol K) / 28.9644 kg/kmol',
                  'replacements': replacements, 'outputs': OUTPUTS,
                  'baseline_regeneration_drift': baseline_drift, 'changed_fields': differences, 'commands': log}
        args.out.write_text(json.dumps(result, indent=2)+'\n')
        lines = ['# Counterfactual dry-air constant study', '',
                 'Scratch copies only. All gas-specific constants and density dials stay unchanged. ',
                 f'Old: JS 287.0528; Python 287.05. New: 8314.32 / 28.9644 = {r_air!r} J/(kg K).', '',
                 f'{len(differences)} changed leaves. Baseline regeneration drift: {len(baseline_drift)} leaves.', '',
                 'Old means a fresh original-constant run. Published old is the committed cache; '
                 'any difference between these columns predates the constant change.', '',
                 '| Published/generated file | Field | Published old | Fresh old | Standard R | Constant effect |',
                 '| --- | --- | ---: | ---: | ---: | ---: |']
        for row in differences:
            vals = [row[k] for k in ('file', 'field', 'published_old', 'old', 'new', 'difference')]
            lines.append('| '+' | '.join(str(x).replace('|', '\\|').replace('\n',' ') for x in vals)+' |')
        args.out.with_suffix('.md').write_text('\n'.join(lines)+'\n')
        print(f'constant study: {len(differences)} changed leaves; baseline drift {len(baseline_drift)}', flush=True)


if __name__ == '__main__':
    main()
