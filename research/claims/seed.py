#!/usr/bin/env python3
"""Initial register construction only. Never refresh an existing register with this tool.

Covered entries come from the rules exercised by tools/tests/test_claims.py. Everything else
is explicitly unowned or awaiting the float inventory, never silently granted a citation.
"""
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import claims

HEADLINES = {
    'stale': 'Handwritten energy figures and hull dimensions lag the model.',
    'water': 'Released water is described as delivered water.',
    'float': 'Float figures await a ledger that records their physical basis.',
    'generated': 'Static defaults and diagrams still need a generating check.',
    'review': 'Source and historical figures still need occurrence-level review.',
    'unowned': 'Other public numbers still need an accountable owner or an explicit label.',
}

# These are row meanings, not value matches. Equal digits never establish ownership.
README_ROWS = {
    'Payload': ('spec.payloadT', 't'), 'Cycle': ('cycle.cycleMin', 'min'),
    'Delivered': ('cycle.tph', 't/h'), 'Descent anchor': ('descent.anchorT', 't'),
    'Retained as ballast': ('descent.retainedT', 't'), 'Energy': ('cycle.eCycleMWh', 'MWh/cycle'),
    'Per tonne': ('cycle.kwhPerTonne', 'kWh per released tonne'),
}
FLOAT_WORDS = re.compile(r'\b(float\w*|sink\w*|buoyan\w*|displace\w*|lift|mass|deficit|shell|crush)\b', re.I)


def model(occ, key, unit, scenario):
    return dict(kind='model', key=key, precision=len(occ['raw'].split('.')[1]) if '.' in occ['raw'] else 0,
                unit=unit, scenario=scenario)


def choose(occ):
    """Conservative, tested bootstrapping rules; not an ongoing auto-registration pass."""
    rule = claims.nonclaim_rule(occ)
    if rule:
        return dict(kind='nonclaim', rule=rule), 'claimscheck'
    if occ['file'] == 'README.md' and occ['surface'] == 'cell':
        row = occ['context'].split(' | ')
        if row[0] in README_ROWS and row[1] in {'1', '2', '3'}:
            cls = ['P100', 'P1000', 'P10000'][int(row[1]) - 1]
            suffix, unit = README_ROWS[row[0]]
            return model(occ, f'classes.{cls}.{suffix}', unit, dict(
                vehicle_class=cls, mode='balanced', one_way_km=15, wind='still air',
                water='released from aircraft, not arrived at fire', altitude='model defaults')), 'claimscheck'
    if occ['file'] == 'README.md' and occ['raw'] == '190' and occ['text'].startswith('The P-100 is the reference vehicle'):
        return model(occ, 'classes.P100.spec.lenM', 'm', dict(vehicle_class='P100', geometry='current reference hull')), 'claimscheck'
    if occ['file'] == 'concept/index.html' and occ['surface'] == 'aria-label' and occ['text'].startswith('All three conceptual airships'):
        cls = {'190': 'P100', '404': 'P1000', '876': 'P10000'}.get(occ['raw'])
        if cls:
            return model(occ, f'classes.{cls}.spec.lenM', 'm', dict(vehicle_class=cls, geometry='current hull length')), 'claimscheck'
    if occ['file'] == 'concept/index.html' and occ['raw'] == '0.45' and ('configured 0.45 kWh/kg' in occ['text'] or '0.45 kWh/kg dial' in occ['text']):
        return model(occ, 'assumptions.eLN2', 'kWh/kg', dict(basis='default nitrogen liquefaction assumption')), 'claimscheck'
    if occ['marker']:
        key = occ['marker']
        if '.lift.' in key or key.endswith('.spec.dispM3'):
            arithmetic = model(occ, 'classes.' + key, 'as printed in the marked report', dict(
                basis='marker quantity; complete float basis awaits ledger'))
            return dict(kind='delegated', inventory='floatcheck', arithmetic=arithmetic), 'floatcheck'
        return dict(kind='generated', generator='figure-marker', region=key), 'figcheck'
    if occ['file'] == 'index.html' and occ['region'] in claims.FALLBACK:
        return dict(kind='generated', generator='tools/gen_fallback.py', region=occ['region']), 'fallbackcheck'
    # Only a literal leading label: mentions of a target elsewhere are not a label.
    label = re.match(r'^(Vision|Assumption|Target|Historical)\s*[:—–]', occ['block'], re.I)
    if label:
        return dict(kind='labelled', label=label[1].lower()), 'claimscheck'
    if FLOAT_WORDS.search(occ['block'] + ' ' + occ['context']):
        return dict(kind='delegated', inventory='floatcheck'), 'floatcheck'
    return None, 'claimscheck'


def main():
    out = ROOT / 'research/claims'
    if (out / 'register.json').exists() or (out / 'accepted-defects.json').exists():
        raise SystemExit('Refusing to overwrite the register or ratchet. Review the extraction diff instead.')
    data = claims.extract(ROOT, ROOT / 'dist.manifest')
    flat = claims.flatten(claims.read_json(ROOT / 'research/figures.json'))
    entries, defects = [], []
    for occ in data['occurrences']:
        owner, gate = choose(occ)
        entry = claims.entry_for(occ, owner, gate)
        entries.append(entry)
        problem = claims.failure(occ, entry, flat, ROOT, {}, {})
        if problem:
            kind = problem['kind']
            if kind == 'stale-model':
                group = 'stale'
                description = 'The displayed value disagrees with the named model key at its printed precision.'
                closes = 'Correct the displayed value and its scenario, publish old and new, then update the occurrence binding and retire this defect.'
            elif kind == 'water-basis':
                group = 'water'
                description = 'The bound key computes release from the aircraft; the surrounding wording says delivered without an arrival model.'
                closes = 'Label the quantity as released water, or bind an independently computed arrived-water quantity; update the register and retire this defect.'
            elif kind == 'delegation-miss':
                group = 'float'
                description = 'Awaiting the float ledger: a float-related block has no occurrence inventory that owns this number and its basis.'
                closes = 'Land the float inventory, state quantity, hull or cell, altitude, safety factor, knockdown and evidence class on the page, then rebind the corrected occurrence.'
            elif occ['surface'].startswith('script-default') or occ['surface'] == 'default' or occ['surface'] in {'text', 'aria-label', 'desc'}:
                group = 'generated'
                description = 'This static default or diagram number has no verified generating region or arithmetic binding.'
                closes = 'Bind this exact output to a checked generator or model, with its units and scenario, and correct or label the page before retiring this defect.'
            elif occ['file'].startswith('research/reports/'):
                group = 'review'
                description = 'Unowned occurrence: source entailment or historical scope has not been reviewed for this exact sentence.'
                closes = 'Review the local source and locator or label the historical/assumed basis on the page; record the dated reviewer and new occurrence binding.'
            else:
                group = 'unowned'
                description = 'Unowned occurrence: neither a tested nonclaim rule nor a checked owner currently answers for it. This does not assert that the number is false.'
                closes = 'Correct or explicitly label this sentence and bind its quantity to a check, or remove the claim; update the register and retire this defect.'
            defects.append(dict(occurrences=[occ['id']], headline=group, problem=description,
                                failure=problem, closes=closes))
    claims.write_json(out / 'register.json', dict(version=1, delegations={
        'floatcheck': dict(command=['python3', '-B', 'tools/check_float_ledger.py', '--inventory'],
                           optional_until_present='tools/check_float_ledger.py')}, entries=entries))
    claims.write_json(out / 'known-defects.json', dict(version=1, headlines=HEADLINES, defects=defects))
    print(f'Prepared {len(entries)} occurrences and {len(defects)} defects; check --accept-new must accept them explicitly.')


if __name__ == '__main__':
    main()
