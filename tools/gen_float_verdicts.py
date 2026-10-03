#!/usr/bin/env python3
"""Fill scripts-off verdicts from the same catalogue contexts as their page binders.

Templates own the prose; the catalogue owns every result. Exact markers let the float
gate compare a fresh emission without granting an allowance to the surrounding page.
"""
import argparse
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
import check_float_ledger as ledger_gate
from float_regions import region

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = 'tools/float_verdict_templates.json'
SPAN = re.compile(r'<span\s+([^>]*\bdata-(?:n|cat)="[^"]+"[^>]*)>[^<]*</span>')


def markers(name):
    return f'<!-- float-verdict:{name}:start -->', f'<!-- float-verdict:{name}:end -->'


def fill(template, contexts, file):
    def number(match):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', match[1]))
        key = 'data-cat' if 'data-cat' in attrs else 'data-n'
        values = contexts['__engineering' if key == 'data-cat' else '__ship']
        value = ledger_gate.dig(values, attrs[key])
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f'{file}: nonnumeric verdict route {attrs[key]}')
        value *= float(attrs.get('data-mul', '1'))
        shown = f'{value:,.{int(attrs.get("data-f", "0"))}f}'
        return f'<span {match[1]}>{shown}</span>'
    return SPAN.sub(number, template)


def render(root=ROOT):
    # Reuse the gate's execution of the engineering binder and viewer computeCtx().
    # Both contexts obtain hull results from ship/catalog.js; no duplicated equation.
    ledger_gate.ROOT = root
    contexts = ledger_gate.catalog_values()
    if contexts is None:
        raise ValueError('cannot execute the page catalogue contexts')
    templates = json.loads((root / TEMPLATES).read_text())
    outputs = {}
    for file, blocks in templates.items():
        body = (root / file).read_text()
        for name, template in blocks.items():
            start, end = markers(name)
            fragment = start + '\n' + fill(template, contexts, file) + '\n' + end
            actual, _, _ = region(body, start, end)
            body = body.replace(actual, fragment + ('\n' if actual.endswith('\n') else ''), 1)
        outputs[file] = body
    return outputs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group(required=True)
    modes.add_argument('--emit', action='store_true')
    modes.add_argument('--write', action='store_true')
    args = ap.parse_args()
    try:
        outputs = render()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'float verdict generation failed: {exc}', file=sys.stderr)
        return 1
    if args.emit:
        print(json.dumps(outputs, ensure_ascii=False))
        return 0
    changed = []
    for file, body in outputs.items():
        path = ROOT / file
        if path.read_text() != body:
            path.write_text(body)
            changed.append(file)
    print(f'float verdicts: {len(changed)} pages written; {len(outputs)} pages generated')
    return 0


if __name__ == '__main__':
    sys.exit(main())
