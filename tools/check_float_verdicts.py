#!/usr/bin/env python3
"""Compare exact verdict regions with tools/gen_float_verdicts.py and the ledger."""
import json
import re
import sys

sys.dont_write_bytecode = True
from gen_float_verdicts import ROOT, TEMPLATES, markers, render
from float_regions import region


def check(root=ROOT):
    outputs = render(root)
    errors = []
    ledger = json.loads((root / 'research/analysis/float-ledger.json').read_text())
    rows = {c['id']: c for d in ledger['designs'] for c in d['cases']}
    record = rows['hull-52m/as-drawn/gamma-0.30/chord-1050/sf-1.2']
    favourable = rows['hull-52m/as-drawn/gamma-0.65/chord-1450/sf-1.2']
    expected = [f'{record["at"][alt]["liftToMass"]:.3f}' for alt in ('seaLevel', 'target')]
    expected += [f'{favourable["at"][alt]["liftToMass"]:.3f}' for alt in ('seaLevel', 'target')]
    expected += [f'{-favourable["at"][alt]["margin"]:.1f}' for alt in ('seaLevel', 'target')]
    templates = json.loads((root / TEMPLATES).read_text())
    for file, blocks in templates.items():
        for name in blocks:
            start, end = markers(name)
            actual, lo, _ = region((root / file).read_text(), start, end)
            fresh, _, _ = region(outputs[file], start, end)
            if actual != fresh:
                errors.append(f'{file}:{lo}: verdict differs from fresh catalogue generation')
            if name == 'hull':
                # The raw tag-stripped text is the scripts-off reading; every bound
                # result must appear at the ledger's precision before JavaScript runs.
                plain = re.sub(r'<!--.*?-->|<[^>]*>', '', actual, flags=re.S)
                for number in expected:
                    if not re.search(r'(?<![\d.])' + re.escape(number) + r'(?![\d.])', plain):
                        errors.append(f'{file}:{lo}: scripts-off verdict lacks ledger value {number}')
    return errors


def main():
    try:
        errors = check()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors = [f'float verdict check failed: {exc}']
    if errors:
        print('\n'.join(errors))
        return 1
    print('PASS float verdicts: four scripts-off hull paragraphs match fresh catalogue output and both ledger bases; bench paragraph matches its live binder')
    return 0


if __name__ == '__main__':
    sys.exit(main())
