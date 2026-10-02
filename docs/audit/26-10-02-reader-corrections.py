#!/usr/bin/env python3
"""Apply the permitted moved-number readers from the generated budget; keep an audit."""
import json
from pathlib import Path
import subprocess

ROOT=Path('.')
new=json.loads(Path('research/analysis/mass-budget.json').read_text())
old=json.loads(subprocess.check_output(['git','show','HEAD:research/analysis/mass-budget.json'],text=True))
p='research/analysis/mass-budget.md'
s=subprocess.check_output(['git','show','HEAD:'+p],text=True)
changes=[]
manifest=[]

def replace(before, after, pointer, fmt):
    global s
    assert before in s, before
    s=s.replace(before,after)
    changes.append(dict(file=p,old=before,new=after,pointer=pointer,cause='regenerated capsule budget'))
    if fmt: manifest.append((p.split('/')[-1], 'mass-budget', pointer, fmt))

root='classes/P100/'
a,b=old['classes']['P100'],new['classes']['P100']
replace('**4.426 kg per m²** of the 22,592 m² skin.',
        f"**{b['requiredKgPerM2']:.3f} kg per m²** of the {b['hullAreaM2']:,} m² capsule skin.",
        root+'requiredKgPerM2','.3f')
manifest.append(('mass-budget.md','mass-budget',root+'hullAreaM2',',d'))
for i,row in enumerate(a['cases']['floor']['lines']):
    label=row['item']
    printed='LN₂ tankage' if label=='LN2 tankage' else label
    if printed=='Cryogenic plant': continue
    oldvals=[a['cases'][c]['lines'][i]['tonnes'] for c in ('floor','credible','demonstrated')]
    newvals=[b['cases'][c]['lines'][i]['tonnes'] for c in ('floor','credible','demonstrated')]
    if oldvals==newvals: continue
    before='| '+printed+' | '+' | '.join(f'{v:.1f}' for v in oldvals)+' |'
    after='| '+printed+' | '+' | '.join(f'{v:.1f}' for v in newvals)+' |'
    replace(before,after,root+f'cases/floor/lines/{i}/tonnes','.1f')
    for c in ('credible','demonstrated'):
        manifest.append(('mass-budget.md','mass-budget',root+f'cases/{c}/lines/{i}/tonnes','.1f'))
replace('| **TOTAL** | **216.3** | 468.1 | 1123.1 |',
        '| **TOTAL** | **'+format(b['cases']['floor']['totalT'],'.1f')+'** | '+
        ' | '.join(format(b['cases'][c]['totalT'],'.1f') for c in ('credible','demonstrated'))+' |',root+'cases/floor/totalT','.1f')
replace('| × the 100 t allowance | **2.16×** | 4.68× | 11.23× |',
        '| × the 100 t allowance | **'+format(b['cases']['floor']['overBy'],'.2f')+'×** | '+
        ' | '.join(format(b['cases'][c]['overBy'],'.2f')+'×' for c in ('credible','demonstrated'))+' |',root+'cases/floor/overBy','.2f')
for c in ('credible','demonstrated'):
    for key,fmt in [('totalT','.1f'),('overBy','.2f')]:manifest.append(('mass-budget.md','mass-budget',root+f'cases/{c}/{key}',fmt))
replace('floor to **180.5 t, 1.81×**.',f"floor to **{b['rightSized']['floor']['totalT']:.1f} t, {b['rightSized']['floor']['overBy']:.2f}×**.",root+'rightSized/floor/totalT','.1f')
ca=a['rightSized']['floor']['hullThatCloses'];cb=b['rightSized']['floor']['hullThatCloses']
for key in ca:
    bold=key=='0.508'
    def cells(r):
        vals=[f"{r['volumeM3']:,} m³",f"{r['timesBaseline']:.2f}×",f"{r['lenM']} × {r['diaM']} m"]
        return ' | '.join('**'+v+'**' if bold else v for v in vals)
    replace(cells(ca[key]),cells(cb[key]),root+f'rightSized/floor/hullThatCloses/{key}/volumeM3',',d')
    for k,fmt in [('timesBaseline','.2f'),('lenM','d'),('diaM','d')]:manifest.append(('mass-budget.md','mass-budget',root+f'rightSized/floor/hullThatCloses/{key}/{k}',fmt))
replace('closes at 223 × 55 m',f"closes at {cb['0.508']['lenM']} × {cb['0.508']['diaM']} m",root+'rightSized/floor/hullThatCloses/0.508/lenM','d')
replace('closes at 1.61× the reference volume — a 223 m hull',f"closes at {cb['0.508']['timesBaseline']:.2f}× the reference volume, a {cb['0.508']['lenM']} m hull",root+'rightSized/floor/hullThatCloses/0.508/timesBaseline','.2f')
for phi in ('phi=0.74','phi=0.85','phi=1.0'):
    for key,r in a['rightSized']['floor']['cellular'][phi].items():
        nr=b['rightSized']['floor']['cellular'][phi][key]
        if not r['closes']:continue
        before=f"{r['volumeM3']:,} m³ — {r['lenM']} × {r['diaM']} m"
        after=f"{nr['volumeM3']:,} m³, {nr['lenM']} × {nr['diaM']} m"
        # A closure-table replacement may already have changed a duplicate cell.
        if before not in s:
            before=f"{nr['volumeM3']:,} m³ — {r['lenM']} × {r['diaM']} m"
        replace(before,after,root+f'rightSized/floor/cellular/{phi}/{key}/volumeM3',',d')
        for k in ('lenM','diaM'):manifest.append(('mass-budget.md','mass-budget',root+f'rightSized/floor/cellular/{phi}/{key}/{k}','d'))
s=s.replace('## The requirement, as the model states it', '**2026-10-02 correction:** nominal fleet areas now use the model’s capsule surface.\nThe [regeneration audit](../../docs/audit/26-10-02-analysis-regeneration.md) records every old and new number and its cause.\nThese conditional equipment budgets do not validate a drawn hull.\n\n## The requirement, as the model states it')
Path(p).write_text(s)
for file in ('docs/OPEN-QUESTIONS.md','docs/VERIFICATION-PLAN.md'):
    text=subprocess.check_output(['git','show','HEAD:'+file],text=True)
    if file.endswith('OPEN-QUESTIONS.md'):
        # The old row is explicitly dated; preserve it and add the correction beside it.
        target=next(line for line in text.splitlines() if '353,975' in line)
        correction=(f">\n> **2026-10-02 correction to #11:** the conditional capsule budget now gives {cb['0.508']['volumeM3']:,} m³ and {cb['0.508']['lenM']} m length. "
                    'This is equipment-budget closure under an assumed shell density, not a checked design.\n> See [the regeneration audit](audit/26-10-02-analysis-regeneration.md).')
        text=text.replace('> Regenerate all of it with `make analysis`.\n', '> Regenerate all of it with `make analysis`.\n'+correction+'\n')
    else:
        text=text.replace('353,975 m³, a 223 m ship',f"{cb['0.508']['volumeM3']:,} m³, a {cb['0.508']['lenM']} m ship")
    Path(file).write_text(text)
Path('docs/audit/26-10-02-reader-corrections.json').write_text(json.dumps(dict(changes=changes,manifest=manifest),indent=2)+'\n')
print(f'reader corrections: {len(changes)} replacements, {len(manifest)} bindings')
