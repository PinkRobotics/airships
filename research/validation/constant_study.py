#!/usr/bin/env python3
"""Counterfactual only: regenerate published outputs in two disposable current-tree copies.

Run with an explicit TMPDIR. The repository and its constants are never written.
The complete leaf list goes to --out (JSON); adjacent Markdown summarizes magnitudes
and selected full rows under a byte budget, with exact omission counts. --normalize
rebuilds that summary from the recorded JSON without changing numerical results.
No network inputs: browser URLs use the bundled snapshot and the committed fire history.
"""
import argparse
from collections import Counter
import math
from statistics import median
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


def numeric(row):
    """Flags are categorical; JSON null marks an absent side in this study."""
    return type(row['old']) in (int, float) and type(row['new']) in (int, float)


def relative_effect(row):
    if numeric(row) and row['old'] != 0:
        return row['difference'] / abs(row['old'])
    return None


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')


def detail_row(row):
    effect = relative_effect(row)
    relative = (f'{effect:.12g}' if effect is not None else
                'undefined (fresh old zero)' if numeric(row) else 'n/a')
    vals = [row[k] for k in ('file', 'field', 'published_old', 'old', 'new', 'difference')]
    return '| ' + ' | '.join(cell(x) for x in [*vals, relative]) + ' |'


def special_kind(row):
    if row['old'] is None:
        return 'added'
    if row['new'] is None:
        return 'removed'
    return 'fresh old zero' if numeric(row) else 'text or flag'


def compact_ids(ids):
    """Inclusive ranges only for canonical decimal ids; preserve tuple positions."""
    if not all(len(parts) == 1 and str(int(parts[0])) == parts[0] for parts in ids):
        return ', '.join('/'.join(parts) for parts in ids)
    values = sorted(int(parts[0]) for parts in ids)
    runs = []
    for value in values:
        if runs and value == runs[-1][-1] + 1:
            runs[-1].append(value)
        else:
            runs.append([value])
    return ', '.join(f'{run[0]}..{run[-1]}' if len(run) > 2 else
                     ', '.join(map(str, run)) for run in runs)


def special_section(rows, budget, header):
    """Represent complete repeated records before admitting individual leaves."""
    kinds = ('text or flag', 'added', 'removed', 'fresh old zero')
    counts = Counter((r['file'], special_kind(r)) for r in rows)
    groups = {}
    for row in rows:
        parts = row['field'].split('/')
        pattern = '/'.join('{n}' if p.isdigit() else p for p in parts)
        groups.setdefault((row['file'], pattern, special_kind(row)), []).append(row)
    collapsed = [(key, group) for key, group in sorted(groups.items()) if len(group) > 10]
    full = sorted((r for group in groups.values() if len(group) <= 10 for r in group),
                  key=lambda r: (r['file'], r['field']))

    def render(chosen, details, cut=False):
        covered = sum(len(group) for _, group in chosen) + len(details)
        out = ['### Text, flags, absent sides and fresh old zero', '',
               f'All special rows listed: {covered}; omitted: {len(rows)-covered}.', '',
               '| Published/generated file | Text or flag | Added | Removed | Fresh old zero | Total |',
               '| --- | ---: | ---: | ---: | ---: | ---: |']
        for file in sorted({r['file'] for r in rows}):
            values = [counts[file, kind] for kind in kinds]
            out.append('| ' + ' | '.join(map(cell, [file, *values, sum(values)])) + ' |')
        totals = [sum(counts[file, kind] for file, k in counts if k == kind) for kind in kinds]
        out += ['| Total | ' + ' | '.join(map(str, [*totals, sum(totals)])) + ' |', '',
                'Replace each all-digit path segment with {n}; groups of more than 10 leaves collapse. '
                'P10000 stays literal. Id tuples follow placeholder order; .. denotes an inclusive range. '
                'Identical id sets share one reference. Changes compare fresh old with Standard R; '
                'a shared change is printed only when every leaf agrees.', '',
                f'Collapsed groups: {len(chosen)}; represented leaves: {sum(len(g) for _, g in chosen)}; '
                f'full special rows: {len(details)}.', '']
        if cut:
            out += ['Byte-limit selection: take whole collapsed groups by descending leaf count, '
                    'then full rows by kind (fresh old zero, added, removed, text or flag); '
                    'ties sort by file and field pattern. Stop at the first unit that does not fit. '
                    'Counts above include omitted leaves; all omitted detail remains in JSON.', '']
        if chosen:
            out += ['| Published/generated file | Field pattern | Kind | Shared change | Leaves | Id set |',
                    '| --- | --- | --- | --- | ---: | --- |']
            sets = {}
            for (file, pattern, kind), group in chosen:
                ids = tuple(sorted({tuple(p for p in r['field'].split('/') if p.isdigit()) for r in group},
                                   key=lambda ps: tuple((int(p), p) for p in ps)))
                if ids not in sets:
                    sets[ids] = f'S{len(sets)+1}'
                pairs = {(json.dumps(r['old'], ensure_ascii=False), json.dumps(r['new'], ensure_ascii=False))
                         for r in group}
                if len(pairs) == 1:
                    old, new = next(iter(pairs))
                    change = (f'value removed (fresh old: {old})' if kind == 'removed' else
                              f'value added: {new}' if kind == 'added' else f'{old} → {new}')
                else:
                    change = 'varies; see changed_fields in JSON'
                out.append('| ' + ' | '.join(map(cell, [file, pattern, kind, change, len(group), sets[ids]])) + ' |')
            out += ['', '| Id set | Numeric path ids (in placeholder order) |', '| --- | --- |']
            out += [f'| {name} | {cell(compact_ids(ids))} |' for ids, name in sets.items()]
            out += ['']
        out += [*header, *map(detail_row, details)]
        return out

    complete = render(collapsed, full)
    if len(('\n'.join(complete)+'\n').encode()) <= budget:
        return complete
    # An indivisible group always keeps its complete id set, even under a cut.
    chosen, details = [], []
    priority = {'fresh old zero': 0, 'added': 1, 'removed': 2, 'text or flag': 3}
    units = [('group', g) for g in sorted(collapsed, key=lambda g: (-len(g[1]), *g[0]))]
    units += [('row', r) for r in sorted(full, key=lambda r: (priority[special_kind(r)], r['file'], r['field']))]
    for kind, unit in units:
        trial_groups = chosen + [unit] if kind == 'group' else chosen
        trial_rows = details + [unit] if kind == 'row' else details
        trial = render(trial_groups, trial_rows, cut=True)
        if len(('\n'.join(trial)+'\n').encode()) > budget:
            break
        chosen, details = trial_groups, trial_rows
    return render(chosen, details, cut=True)


def summary(result):
    """Use only recorded results; never re-run the model to explain its effects.

    Magnitudes rank signed relative effects. Null is the comparison format's
    absent-side marker (it does not distinguish an explicit null from absence).
    A byte budget takes precedence over exhaustive exceptional-row display;
    exact omissions are visible and the JSON always retains the complete list.
    """
    rows = result['changed_fields']
    counts = Counter('added' if r['old'] is None else 'removed' if r['new'] is None else
                     'numeric' if numeric(r) else 'text or flag' for r in rows)
    effects = [(r, abs(relative_effect(r))) for r in rows if relative_effect(r) is not None]
    ranked = sorted(effects, key=lambda pair: (-pair[1], pair[0]['file'], pair[0]['field']))
    large = sum(effect >= 1e-3 for _, effect in ranked)
    selected = ranked[:min(large, 200)] if large > 40 else ranked[:40]
    special = sorted((r for r in rows if not numeric(r) or r['old'] == 0),
                     key=lambda r: (r['file'], r['field']))
    lines = ['# Counterfactual dry-air constant study', '',
             'Scratch copies only. All gas-specific constants and density dials stay unchanged.',
             'Old: ' + '; '.join(f'{side} {value!r}' for side, value in result['old_R_air'].items()) +
             f". New: {result['standard_definition']} = {result['standard_R_air']!r} J/(kg K).", '']
    for side, value in result['old_R_air'].items():
        change = (result['standard_R_air'] - value) / abs(value)
        lines.append(f'{side} constant relative change: {change:.12g} ({change*100:.12g}%).')
    lines += ['', f"{len(rows)} changed leaves: {counts['numeric']} numeric; {counts['text or flag']} text or flag; "
              f"{counts['added']} added; {counts['removed']} removed.",
              f"Baseline regeneration drift: {len(result['baseline_regeneration_drift'])} leaves.", '',
              'Old means a fresh original-constant run. Published old is the committed cache; '
              'any difference between these columns predates the constant change.', '',
              'Relative effect = constant effect / absolute fresh old value. It is signed; rankings, '
              'medians and decade bands use its magnitude. Text and flags have no relative effect; '
              'fresh old zero is undefined. JSON null is treated as an absent side.', '',
              'A large relative effect on a small residual does not imply a large physical change. '
              'These are model comparisons, not current drawn-hull float evidence.', '',
              '## Effects by output', '',
              '| Published/generated file | Changed leaves | Largest relative magnitude | Field | Median relative magnitude |',
              '| --- | ---: | ---: | --- | ---: |']
    for filename in result['outputs']:
        group = [(r, effect) for r, effect in ranked if r['file'] == filename]
        largest, field = (f'{group[0][1]:.12g}', group[0][0]['field']) if group else ('n/a', 'n/a')
        mid = f'{median(effect for _, effect in group):.12g}' if group else 'n/a'
        lines.append('| ' + ' | '.join(cell(x) for x in
                     [filename, sum(r['file'] == filename for r in rows), largest, field, mid]) + ' |')
    bands = Counter(math.floor(math.log10(effect)) for _, effect in effects if effect > 0)
    zero = sum(effect == 0 for _, effect in effects)
    rounding = sum(count for exponent, count in bands.items() if exponent < -12)
    lines += ['', '## Relative magnitudes by decade', '',
              f'{len(effects)} defined numeric relative effects; {len(rows)-len(effects)} undefined or categorical. '
              f'Rounding-scale band: magnitude below 1e-12 ({rounding} nonzero effects). '
              'This names a floating-point rounding scale, not a proof that every effect in it is rounding.', '',
              '| Relative magnitude band | Leaves |', '| --- | ---: |']
    if zero:
        lines.append(f'| zero | {zero} |')
    for exponent, count in sorted(bands.items()):
        lines.append(f'| [1e{exponent}, 1e{exponent+1}) | {count} |')
    lines += ['', '## Selected full rows', '',
              f'{large} numeric leaves have magnitude at least 1e-3. '
              'List the largest 40; when more than 40 meet that threshold, select all of them up to 200. '
              'Ties sort by file and field. Special rows sort by file and field.', '',
              'Complete rows remain in constant-study.json, changed_fields. '
              'The Markdown byte budget can omit special rows; exact counts follow.', '']
    header = ['| Published/generated file | Field | Published old | Fresh old | Standard R | Constant effect | Relative effect |',
              '| --- | --- | ---: | ---: | ---: | ---: | ---: |']
    tail = ['', '## Complete list', '',
            'Every changed leaf is in [constant-study.json](constant-study.json), `changed_fields`:', '',
            '```python', 'import json; print(json.dumps(json.load(open("research/validation/constant-study.json"))["changed_fields"], indent=2))',
            '```']
    # Reserve space for omission counts and section labels, then admit only full rows.
    budget = 39000 - len(('\n'.join(lines + header + header + tail) + '\n').encode()) - 800
    def admit(candidates):
        nonlocal budget
        admitted = []
        for row in candidates:
            line = detail_row(row)
            size = len((line + '\n').encode())
            if size <= budget:
                admitted.append(line)
                budget -= size
            else:
                # Keep a prefix of the prescribed order, never skip to cheaper rows.
                break
        return admitted
    numeric_lines = admit([r for r, _ in selected])
    lines += [f'Selected numeric rows: {len(selected)}; listed: {len(numeric_lines)}; '
              f'omitted by row cap: {len(ranked)-len(selected)}; '
              f'omitted by byte budget: {len(selected)-len(numeric_lines)}.', '',
              *header, *numeric_lines, '']
    special_budget = 39999 - len(('\n'.join(lines + tail) + '\n').encode())
    lines += special_section(special, special_budget, header) + tail
    text = '\n'.join(lines) + '\n'
    if len(text.encode()) >= 40000:
        raise ValueError('summary metadata alone exceeds the Markdown byte budget')
    return text


def write_study(result, output):
    """Write canonical JSON and a bounded summary computed entirely from it."""
    text = summary(result)
    output.write_text(json.dumps(result, indent=2)+'\n')
    output.with_suffix('.md').write_text(text)
    print(f"constant study: {len(result['changed_fields'])} changed leaves; baseline drift "
          f"{len(result['baseline_regeneration_drift'])}; summary {len(text.encode())} bytes", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--normalize', action='store_true', help='regenerate the Markdown summary from recorded JSON; no numerical changes')
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
