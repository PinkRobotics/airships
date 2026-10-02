#!/usr/bin/env python3
"""Record the before/after leaves of this ruling; run from the repository root."""
import json
from pathlib import Path
import subprocess


def git(*args):
    return subprocess.check_output(['git', *args], text=True)


def leaves(obj, prefix=''):
    if isinstance(obj, dict):
        return {p: v for key, value in obj.items() for p, v in leaves(value, prefix+'/'+key).items()}
    if isinstance(obj, list):
        return {p: v for i, value in enumerate(obj) for p, v in leaves(value, prefix+'/'+str(i)).items()}
    return {prefix: obj}


cause = ('The 2026-08-13 capsule change a32809fb5536e3dace98541cc6594820568c806c '
         'changed nominal fleet dimensions and cycle inputs in research/figures.json, while '
         'leaving the mass-budget generator and its spheroid area call unchanged. The three '
         'generated analyses were not refreshed then. This regeneration uses the existing '
         'capsule area function, as ruled on 2026-10-02. The old-formula regeneration is '
         'superseded: it reproduced stale-cache effects but still priced the wrong surface. '
         'The first-study film reference remains the dated 190 by 47 m spheroid. '
         'No energy model is changed; regenerated energy context is recorded here for its owner.')
inputs = []
for ref in ('a32809f^', 'a32809f', 'HEAD'):
    inputs.append(dict(ref=ref, commit=git('rev-parse', ref).strip(),
                       figuresBlob=git('rev-parse', ref+':research/figures.json').strip(),
                       budgetBlob=git('rev-parse', ref+':research/analysis/mass-budget.py').strip(),
                       figures=json.loads(git('show', ref+':research/figures.json'))))
changes=[]
for name in ('mass-budget', 'delivery', 'vacuum-cell', 'helium', 'water-availability', 'descent'):
    path=f'research/analysis/{name}.json'
    old=leaves(json.loads(git('show', 'HEAD:'+path)))
    new=leaves(json.loads(Path(path).read_text()))
    for pointer in sorted(old.keys() | new.keys()):
        a,b=old.get(pointer),new.get(pointer)
        if a==b: continue
        numeric=isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float))
        if numeric and any(k in pointer for k in ('hullArea','requiredKgPerM2')):
            direction='geometry/allowance denominator; not a structural result'
        elif numeric and name=='mass-budget' and any(k in pointer for k in ('massT','totalT','overBy','volumeM3','timesBaseline')):
            direction=('better' if b<a else 'worse')+' in this conditional equipment budget'
        else:
            direction='context or intermediate; no direct float verdict'
        changes.append(dict(file=path,pointer=pointer,old=a,new=b,numeric=numeric,
                            cause='capsule surface and refreshed capsule-era inputs' if name=='mass-budget' else
                            'dated-reference label' if name=='vacuum-cell' else 'refreshed capsule-era inputs',
                            floatEffect=direction))
record=dict(cause=cause,history=inputs,changes=changes)
base=Path('docs/audit/26-10-02-analysis-regeneration')
base.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
lines=['# Analysis regeneration, 2026-10-02','',cause,'',
       'Each pointer identifies its printed JSON location. The companion JSON preserves full values and historical inputs.', '',
       '| Printed at | Old | New | Cause | Float effect |', '|---|---:|---:|---|---|']
for row in changes:
    if row['numeric']:
        lines.append('| '+' | '.join(str(row[k]).replace('|','\\|') for k in ('file','old','new','cause','floatEffect')).replace(row['file'],row['file']+'#'+row['pointer'],1)+' |')
base.with_suffix('.md').write_text('\n'.join(lines)+'\n')
print(f"regeneration audit: {sum(r['numeric'] for r in changes)} numeric leaves, {sum(not r['numeric'] for r in changes)} other leaves")
