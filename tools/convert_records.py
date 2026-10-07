#!/usr/bin/env python3
"""Convert recognised generated records; optional proof against a saved input."""
import argparse
import hashlib
import json
from pathlib import Path
from record_energy_fix import compact_solar_record, expand_solar_record, solar_record_text, write_if_changed


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()



def convert_carry(args):
    from claims import compact_carry_run, carry_history_text, write_carry_history
    path = args.root / 'research/claims/carry-history.json'
    old = json.loads(path.read_text())
    text = carry_history_text(old)
    converted = json.loads(text)
    baseline = json.loads(args.baseline.read_text()) if args.baseline else old
    assert len(baseline['runs']) == len(converted['runs']), 'carry run count changed'
    totals = {}
    sizes = []
    for i, (before, after) in enumerate(zip(baseline['runs'], converted['runs'])):
        for key in ('files', 'headlines', 'retired', 'added', 'defect_changes'):
            assert canonical(before[key]) == canonical(after[key]), (i, key)
            totals[key] = totals.get(key, 0) + len(canonical(after[key]))
        expected = compact_carry_run(before)['revalidated']
        assert canonical(expected) == canonical(after['revalidated']), (i, 'changed fields')
        sizes.append(len(carry_history_text(dict(version=1, runs=[after])).encode()))
        print(f'run {i + 1}: {sizes[-1]} bytes; preserved files/headlines/retired/added/defect_changes and {len(expected)} changed entries')
    old_changes = [compact_carry_run(run)['revalidated'] for run in baseline['runs']]
    new_changes = [run['revalidated'] for run in converted['runs']]
    print('changed-fields old sha256:', hashlib.sha256(canonical(old_changes)).hexdigest())
    print('changed-fields new sha256:', hashlib.sha256(canonical(new_changes)).hexdigest())
    print('preserved key sizes:', json.dumps(totals, sort_keys=True))
    print(f'converted carry: {len(text.encode())} bytes; after twenty largest runs: {len(text.encode()) + 20 * max(sizes, default=0)} bytes')
    write_carry_history(path, old)



def convert_register(args):
    from claims import write_json
    path = args.root / 'research/claims/register.json'
    old = json.loads(path.read_text())
    baseline = json.loads(args.baseline.read_text()) if args.baseline else old
    assert canonical(old) == canonical(baseline), 'register content differs before conversion'
    write_json(path, old)
    new = json.loads(path.read_text())
    assert canonical(baseline) == canonical(new), 'register content changed'
    print('register old sha256:', hashlib.sha256(canonical(baseline)).hexdigest())
    print('register new sha256:', hashlib.sha256(canonical(new)).hexdigest())
    print(f'{path.relative_to(args.root)}: {path.stat().st_size} bytes; json.load values equal')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--part', choices=['solar', 'carry', 'register'], required=True)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--baseline', type=Path)
    args = ap.parse_args()
    if args.part == 'register':
        convert_register(args)
        return
    if args.part == 'carry':
        convert_carry(args)
        return
    path = args.root / 'research/analysis/solar-input-changes.json'
    old = json.loads(path.read_text())
    text = solar_record_text(old)
    expanded = expand_solar_record(json.loads(text))
    baseline = json.loads(args.baseline.read_text()) if args.baseline else expand_solar_record(old)
    assert canonical(baseline) == canonical(expanded), 'solar content changed'
    for key in ('changes', 'textAndFlagChanges', 'addedOrRemovedNumericFields'):
        print(f'{key}: {len(baseline[key])} -> {len(expanded[key])} rows; equal')
    print('canonical old sha256:', hashlib.sha256(canonical(baseline)).hexdigest())
    print('canonical new sha256:', hashlib.sha256(canonical(expanded)).hexdigest())
    write_if_changed(path, text)
    print(f'{path.relative_to(args.root)}: {len(text.encode())} bytes')


if __name__ == '__main__':
    main()
