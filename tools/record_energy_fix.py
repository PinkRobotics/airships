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
    'SOLAR': 'Projected solar collection is 85% of each current capsule footprint, an unvalidated coverage assumption; physical sheet area remains a separate material-budget assumption. The table gives class and publication summaries; the [complete per-field movement record](../research/analysis/solar-input-changes.json) includes route records and golden snapshots. Regeneration on an integrated tree can include other model corrections; this publication comparison does not isolate their individual effects.',
}


def changes(old, new, path='', published_only=True):
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(old.keys() | new.keys()):
            yield from changes(old.get(key), new.get(key), path + '.' + key, published_only)
    elif isinstance(old, list) and isinstance(new, list):
        for i in range(max(len(old), len(new))):
            yield from changes(old[i] if i < len(old) else None,
                               new[i] if i < len(new) else None, f'{path}[{i}]', published_only)
    elif type(old) in (int, float) and type(new) in (int, float):
        digits = 6 if path.endswith(('.progress', '.rho', '.dragDensity')) else 3
        if old != new and (not published_only or round(old, digits) != round(new, digits)):
            yield dict(field=path.lstrip('.'), old=old, new=new, decimals=digits)


def changed_text_and_flags(old, new, path=''):
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(old.keys() | new.keys()):
            yield from changed_text_and_flags(old.get(key), new.get(key), path + '.' + key)
    elif isinstance(old, list) and isinstance(new, list):
        for i in range(max(len(old), len(new))):
            yield from changed_text_and_flags(old[i] if i < len(old) else None,
                                             new[i] if i < len(new) else None, f'{path}[{i}]')
    elif type(old) is type(new) and old != new and (
            isinstance(old, bool) or isinstance(old, str) and (re.search(r'\d', old) or re.search(r'\d', new))):
        yield dict(field=path.lstrip('.'), old=old, new=new)


def added_or_removed_numbers(old, new, path=''):
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(old.keys() | new.keys()):
            yield from added_or_removed_numbers(old.get(key), new.get(key), path + '.' + key)
    elif isinstance(old, list) and isinstance(new, list):
        for i in range(max(len(old), len(new))):
            yield from added_or_removed_numbers(old[i] if i < len(old) else None,
                                                new[i] if i < len(new) else None, f'{path}[{i}]')
    elif old is None and isinstance(new, (dict, list)):
        empty = {} if isinstance(new, dict) else []
        yield from added_or_removed_numbers(empty, new, path)
    elif new is None and isinstance(old, (dict, list)):
        empty = {} if isinstance(old, dict) else []
        yield from added_or_removed_numbers(old, empty, path)
    elif (type(old) in (int, float) and new is None or
          old is None and type(new) in (int, float)):
        yield dict(field=path.lstrip('.'), old=old, new=new)


def public_fields(rows):
    # Phase-position keys use '@'; encode it so paths cannot resemble email addresses.
    return [dict(row, field=row['field'].replace('%', '%25').replace('@', '%40')) for row in rows]


SOLAR_GROUPS = {'changes': ('file', 'field', 'old', 'new', 'decimals'),
                'textAndFlagChanges': ('file', 'field', 'old', 'new'),
                'addedOrRemovedNumericFields': ('file', 'field', 'old', 'new')}
SOLAR_KEYS = {'reason', 'comparison', 'fieldEncoding', *SOLAR_GROUPS}


def write_if_changed(path, text):
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def compact_solar_record(record):
    """Front-code paths per file, keeping list order and every original value."""
    if record.get('format') == 'compact-solar-v1':
        expand_solar_record(record)  # validate even an already converted input
        return record
    if set(record) != SOLAR_KEYS:
        raise ValueError('unrecognised solar record keys')
    files = list(dict.fromkeys(row['file'] for key in SOLAR_GROUPS for row in record[key]))
    ids = {file: i for i, file in enumerate(files)}
    result = {key: value for key, value in record.items() if key not in SOLAR_GROUPS}
    result.update(format='compact-solar-v1', files=files)
    for key, keys in SOLAR_GROUPS.items():
        previous = {}; rows = []
        for row in record[key]:
            if set(row) != set(keys) or not isinstance(row['field'], str):
                raise ValueError('unrecognised solar row')
            file = ids[row['file']]; field = row['field']; old = previous.get(file, '')
            prefix = 0
            while prefix < min(len(old), len(field)) and old[prefix] == field[prefix]:
                prefix += 1
            rows.append([file, prefix, field[prefix:], *[row[k] for k in keys[2:]]])
            previous[file] = field
        result[key] = rows
    return result


def expand_solar_record(record):
    """Recover the old object rows, including their order and path encoding."""
    if record.get('format') != 'compact-solar-v1':
        if set(record) != SOLAR_KEYS:
            raise ValueError('unrecognised solar record')
        return record
    if set(record) != SOLAR_KEYS | {'format', 'files'}:
        raise ValueError('unrecognised compact solar keys')
    files = record['files']
    if not isinstance(files, list) or any(not isinstance(f, str) for f in files) or len(set(files)) != len(files):
        raise ValueError('invalid solar file table')
    result = {key: value for key, value in record.items() if key not in {'format', 'files', *SOLAR_GROUPS}}
    for key, keys in SOLAR_GROUPS.items():
        previous = {}; rows = []
        for row in record[key]:
            if not isinstance(row, list) or len(row) != len(keys) + 1:
                raise ValueError('invalid compact solar row width')
            file, prefix, suffix, *values = row
            if type(file) is not int or not 0 <= file < len(files) or type(prefix) is not int or not isinstance(suffix, str):
                raise ValueError('invalid solar path reference')
            old = previous.get(file, '')
            if not 0 <= prefix <= len(old):
                raise ValueError('invalid solar path prefix')
            field = old[:prefix] + suffix
            rows.append(dict(zip(keys, [files[file], field, *values])))
            previous[file] = field
        result[key] = rows
    return result


def solar_record_text(record):
    """Plain JSON, with each compact row on its own line."""
    compact = compact_solar_record(record)
    def encoded(value):
        return json.dumps(value, separators=(',', ':'), allow_nan=False)
    fields = []
    for key, value in compact.items():
        body = '[\n' + ',\n'.join(encoded(row) for row in value) + '\n]' if key in SOLAR_GROUPS else encoded(value)
        fields.append(encoded(key) + ':' + body)
    return '{\n' + ',\n'.join(fields) + '\n}\n'


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
    extra = ['research/figures.json', 'tests/golden/seed7-snapshot.json', 'tests/golden/ui-seed7-snapshot.json']
    if args.part == 'SOLAR':
        extra += ['research/analysis/mass-budget.json', 'research/analysis/water-availability.json',
                  'research/analysis/delivery.json', 'research/validation/report.json']
    for rel in map(Path, extra):
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
    if args.part == 'SOLAR':
        complete = ROOT/'research/analysis/solar-input-changes.json'
        extra_changes=[]; exact=[]; membership=[]
        for before in sorted(args.before.rglob('*.json')):
            rel=before.relative_to(args.before);after=args.after/rel
            if after.exists():
                exact += [dict(file=rel.as_posix(), **r) for r in
                          changes(json.loads(before.read_text()), json.loads(after.read_text()), published_only=False)]
                extra_changes += [dict(file=rel.as_posix(), **r) for r in
                                  changed_text_and_flags(json.loads(before.read_text()), json.loads(after.read_text()))]
                membership += [dict(file=rel.as_posix(), **r) for r in
                               added_or_removed_numbers(json.loads(before.read_text()), json.loads(after.read_text()))]
        exact += [r for r in rows if r['file']==test.as_posix()]
        write_if_changed(complete, solar_record_text(dict(reason=REASONS['SOLAR'],
            comparison='Field paths compare publication positions. Candidate-pool changes alter array membership and order; match route and controls before treating a positional flag change as a verdict change for identical inputs.', changes=public_fields(exact),
            fieldEncoding='Field paths encode percent as %25 and at-sign as %40; percent-decode once to recover the source keys. Values are unchanged.',
            textAndFlagChanges=public_fields(extra_changes), addedOrRemovedNumericFields=public_fields(membership))))
        print(f'Recorded complete solar comparison: {len(exact)} changed numeric fields; '
              f'{len(membership)} added or removed numeric fields; {len(extra_changes)} text or flag changes.')
        summaries = {'research/figures.json', 'research/analysis/energy-documents.json',
                     'research/analysis/delivery.json', test.as_posix()}
        rows = [r for r in rows if r['file'] in summaries or
                (r['file'] == 'research/analysis/water-availability.json' and '.byFire[' not in r['field'])]
    data['parts'] = [p for p in data['parts'] if p['part'] != args.part]
    data['parts'].append(dict(part=args.part, reason=REASONS[args.part], changes=rows))
    data['parts'].sort(key=lambda p: p['part'])
    write_if_changed(output, json.dumps(data, indent=2)+'\n')
    print(f'Recorded part {args.part}: {len(rows)} moved generated numbers at published precision.')


if __name__ == '__main__':
    main()
