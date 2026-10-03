#!/usr/bin/env python3
"""Append the dated regeneration correction; leave the earlier account intact.

Uses the commits named in the audit, compares all JSON leaves, and independently reruns
both surface formulas. No model or generated analysis file is written.
"""
import contextlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
AUDIT = 'docs/audit/26-10-02-analysis-regeneration.md'
MARK = '## Correction, 2026-10-03 — separate causes and omitted strings'


def blob(ref, file):
    return subprocess.check_output(['git','show',f'{ref}:{file}'],cwd=ROOT,text=True)


def leaves(value, prefix=''):
    if isinstance(value,dict):
        for k,v in value.items():
            yield from leaves(v,prefix+'/'+k.replace('~','~0').replace('/','~1'))
    elif isinstance(value,list):
        for i,v in enumerate(value):yield from leaves(v,prefix+'/'+str(i))
    else:
        yield prefix,value


def spheroid(length,diameter):
    a,b = length/2,diameter/2
    e = math.sqrt(1-b*b/(a*a))
    return 2*math.pi*b*b*(1+a/(b*e)*math.asin(e))


def model():
    spec = importlib.util.spec_from_file_location('correction_budget',ROOT/'research/analysis/mass-budget.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def budget(mod, figures, formula, scratch):
    fig = scratch/'figures.json'
    out = scratch/'budget.json'
    fig.write_text(json.dumps(figures))
    mod.FIGURES,mod.capsule_area = fig,formula
    prior = sys.argv
    try:
        sys.argv = ['mass-budget.py','--json',str(out)]
        with contextlib.redirect_stdout(io.StringIO()):mod.main()
    finally:sys.argv=prior
    return dict(leaves(json.loads(out.read_text())))


def correction():
    audit = json.loads((ROOT/'docs/audit/26-10-02-analysis-regeneration.json').read_text())
    before,_,after = audit['history']
    oldref,newref = before['commit'],after['commit']
    artifact_ref = subprocess.check_output(['git','log','--diff-filter=A','-1','--format=%H','--',AUDIT],cwd=ROOT,text=True).strip()
    oldfig = json.loads(blob(oldref,'research/figures.json'))
    newfig = json.loads(blob(newref,'research/figures.json'))
    mod = model()
    capsule = mod.capsule_area
    oldspec,new = oldfig['classes']['P100']['spec'],newfig['classes']['P100']['spec']
    areas = [spheroid(oldspec['lenM'],oldspec['diaM']),spheroid(new['lenM'],new['diaM']),capsule(new['lenM'],new['diaM'])]
    scratch = Path(os.environ['TMPDIR'])
    with tempfile.TemporaryDirectory(prefix='audit-correction-',dir=scratch) as tmp:
        work = Path(tmp)
        stages = [budget(mod,oldfig,spheroid,work),budget(mod,newfig,spheroid,work),budget(mod,newfig,capsule,work)]
    rows = ['',MARK,'',
        'This dated correction adds to the earlier table; it does not replace that account. '
        'The float results and energy model are unchanged. Current float results are in '
        '[the ledger](../FLOAT-LEDGER.md).','',
        '| Surface computation for P100 | Area m² | Cause |', '|---|---:|---|',
        f'| Old spheroid formula, pre-August {oldspec["lenM"]} × {oldspec["diaM"]} m | {areas[0]:,.0f} | cached pre-August geometry |',
        f'| Same formula, capsule-era {new["lenM"]} × {new["diaM"]} m | {areas[1]:,.0f} | changed dimensions, formula held fixed |',
        f'| Capsule formula, same capsule-era dimensions | {areas[2]:,.0f} | changed surface formula, inputs held fixed |','',
        'Verified with `python3 tools/correct_analysis_audit.py --check`; the script evaluates the '
        'old formula and the current capsule function, then runs the mass-budget generator on '
        'both historical input snapshots. A cache refresh exposes changed dimensions and cycle '
        'inputs together; changing the area formula is a separate effect. Battery and cycle '
        'rows move with refreshed cycle inputs. Barrier mass and area-normalised allowance move '
        'with the surface area. Totals, sundries and closing-hull rows can inherit both. '
        'The table below identifies the actual stages affecting each originally reported mass-budget row.','',
        '| Printed at | Refreshed inputs (old formula) | Surface formula (same inputs) |', '|---|---|---|']
    for change in audit['changes']:
        if change['file']!='research/analysis/mass-budget.json':continue
        ptr=change['pointer']
        a,b,c=(s.get(ptr) for s in stages)
        # Include the stage values; a reader can see a zero effect without inferred causality.
        rows.append(f'| mass-budget.json#{ptr} | {a} → {b} | {b} → {c} |')
    rows += ['',f'The omitted strings below were compared at `{oldref}` and `{artifact_ref}`. '
             f'The companion JSON names `{newref}` as its latest input snapshot, before the refreshed '
             'artifacts were committed; the latter comparison uses the commit that first added this audit. The earlier numeric-leaf '
             'table omitted text containing numbers and two reworded vacuum-cell notes.','',
             '| Printed at | Earlier text | Later text |', '|---|---|---|']
    counts={}
    def esc(v):return str(v).replace('|','&#124;').replace('\n',' ').replace('<','&lt;').replace('>','&gt;')
    for file in ['research/analysis/mass-budget.json','research/analysis/vacuum-cell.json']:
        left=dict(leaves(json.loads(blob(oldref,file))))
        right=dict(leaves(json.loads(blob(artifact_ref,file))))
        n=0
        for ptr,a in sorted(left.items()):
            b=right.get(ptr)
            if not isinstance(a,str) or not isinstance(b,str) or a==b:continue
            if file.endswith('mass-budget.json') and not any(c.isdigit() for c in a+b):continue
            rows.append(f'| {file}#{ptr} | {esc(a)} | {esc(b)} |');n+=1
        counts[file]=n
    print('areas m²: '+', '.join(f'{v:,.0f}' for v in areas)+'; omitted strings: '+json.dumps(counts,sort_keys=True))
    return '\n'.join(rows)+'\n'


def main():
    text=correction()
    path=ROOT/AUDIT
    current=path.read_text()
    old=current.split('\n'+MARK,1)[0].rstrip()+'\n'
    expected=old+text
    if '--check' in sys.argv:
        if current!=expected:print('analysis audit correction is missing or stale');return 1
        print('analysis audit correction matches its historical comparisons');return 0
    path.write_text(expected)
    print('Appended dated correction to '+AUDIT)
    return 0

if __name__=='__main__':sys.exit(main())
