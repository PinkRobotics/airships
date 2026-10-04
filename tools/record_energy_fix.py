#!/usr/bin/env python3
"""Record moved generated numbers before replacing a diagnostic or profile publication.

The baseline directory is a local input only; its location is never published.
Numbers are compared at the documents' precision (six decimals for progress and
density, three otherwise). Exact old and new values remain in the JSON record.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REASONS = {
    'A': 'Refined force extrema and both sides of seams replace sampled phase peaks.',
    'B': 'Bisect held force with the least-power split until the available bus is spent.',
    'C': 'Bound return-join acceleration throughout the finite profile search.',
}


def changes(old, new, path=''):
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(old.keys() | new.keys()):
            yield from changes(old.get(key), new.get(key), path + '.' + key)
    elif isinstance(old, list) and isinstance(new, list):
        for i in range(max(len(old), len(new))):
            yield from changes(old[i] if i < len(old) else None,
                               new[i] if i < len(new) else None, f'{path}[{i}]')
    elif type(old) in (int, float) and type(new) in (int, float):
        digits = 6 if path.endswith(('.progress', '.rho', '.dragDensity')) else 3
        if round(old, digits) != round(new, digits):
            yield dict(field=path.lstrip('.'), old=old, new=new, decimals=digits)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--part', choices=REASONS, required=True)
    ap.add_argument('--before', type=Path, required=True)
    ap.add_argument('--after', type=Path, default=ROOT, help='Optional completed checkpoint; defaults to the current tree.')
    args = ap.parse_args()
    output = ROOT/'research/analysis/energy-fix-changes.json'
    data = json.loads(output.read_text()) if output.exists() else {'parts': []}
    rows = []
    for file in sorted((args.after/'research/analysis').glob('*.json')):
        if not (file.name.startswith('energy-') or file.name == 'descent.json'):
            continue
        if 'history' in file.name or file.name == output.name:
            continue
        rel = file.relative_to(args.after)
        before = args.before/rel
        if not before.exists():
            continue
        for row in changes(json.loads(before.read_text()), json.loads(file.read_text())):
            rows.append(dict(file=rel.as_posix(), **row))
    # These generated artifacts also publish model numbers outside the energy directory.
    for rel in map(Path, ['research/figures.json', 'tests/golden/seed7-snapshot.json', 'tests/golden/ui-seed7-snapshot.json']):
        before, after = args.before/rel, args.after/rel
        if before.exists() and after.exists():
            for row in changes(json.loads(before.read_text()), json.loads(after.read_text())):
                rows.append(dict(file=rel.as_posix(), **row))
    test = Path('tests/energy/unheld.mjs')
    pattern = r'unheldT-([0-9.]+)'
    a = re.search(pattern, (args.before/test).read_text())
    b = re.search(pattern, (args.after/test).read_text())
    if a and b and a[1] != b[1]:
        rows.append(dict(file=test.as_posix(), field='namedEndurance.worstUnheldT', old=float(a[1]), new=float(b[1]), decimals=9))
    data['parts'] = [p for p in data['parts'] if p['part'] != args.part]
    data['parts'].append(dict(part=args.part, reason=REASONS[args.part], changes=rows))
    data['parts'].sort(key=lambda p: p['part'])
    output.write_text(json.dumps(data, indent=2)+'\n')
    print(f'Recorded part {args.part}: {len(rows)} moved generated numbers at published precision.')


if __name__ == '__main__':
    main()
