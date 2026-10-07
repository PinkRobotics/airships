#!/usr/bin/env python3
"""Convert recognised generated records; optional proof against a saved input."""
import argparse
import hashlib
import json
from pathlib import Path
from record_energy_fix import compact_solar_record, expand_solar_record, solar_record_text, write_if_changed


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--part', choices=['solar'], required=True)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--baseline', type=Path)
    args = ap.parse_args()
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
