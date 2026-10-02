#!/usr/bin/env python3
"""Measure the actual drawing and current bill, without changing either model."""
from __future__ import annotations
import argparse
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
BASES = ('record', 'favourable')
REGIONS = {
    'rings': 'barrel', 'bars': 'barrel', 'capGrid': 'caps',
    'film': 'whole hull', 'clamps': 'whole hull', 'pads': 'whole hull',
    'longerons': 'barrel and shoulder overlap', 'innerRings': 'barrel and caps',
    'fanWebs': 'barrel and caps', 'thetaWebs': 'barrel and caps',
    'junctionShear': 'shoulders', 'spokes': 'barrel and caps above cutoff',
    'flangeDoubler': 'barrel', 'torsionStraps': 'whole hull', 'skins': 'whole hull',
    'tiJoints': 'whole hull, unallocated', 'stabilityReserve': 'whole hull, unallocated',
}
FAMILIES = {'hoops': ['rings', 'capGrid'], 'hoopsInner': ['innerRings'],
            'longs': ['longerons'], 'webs': ['fanWebs'], 'thetas': ['thetaWebs'],
            'junctions': ['junctionShear'], 'spokes': ['spokes'], 'bars': ['bars', 'capGrid']}
MEMBERS = ('rings', 'capGrid', 'bars', 'longerons', 'innerRings', 'fanWebs',
           'thetaWebs', 'flangeDoubler', 'junctionShear')


def model():
    spec = importlib.util.spec_from_file_location('vacuum_cell', ROOT / 'research/analysis/vacuum-cell.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def different(a, b, abs_tol=1e-3, rel_tol=1e-6):
    if a is None or b is None:
        return True
    return not (math.isfinite(a) and math.isfinite(b)) or abs(a-b) > max(abs_tol, rel_tol*max(abs(a), abs(b)))


def measure_basis(v, draw, key, kd, d, sf):
    loc={}
    def trace(frame,event,arg):
        if event=='return' and frame.f_code.co_name=='ship_skeleton':loc.update(frame.f_locals)
        return trace
    sys.settrace(trace)
    try:r=v.ship0(key,sf,d,kd)
    finally:sys.settrace(None)
    g,w,s=r['geom'],r['wall'],r['skeleton'];rho=v.MATERIALS['T700_LAM']['rho'];f=draw
    f=f['families'];barA=2*math.pi*g['R']*g['cylL'];capA=4*math.pi*g['R']**2
    quantities={
      'rings':{'quantity':barA/v.SHIP0['ringPitchM'],'unit':'m','count':w['counts']['rings'],'drawn':f['hoops']['barrelArcM'],'family':'hoops/barrel'},
      'capGrid':{'quantity':capA,'unit':'m2','count':None,'drawn':None,'family':'no explicit grid topology'},
      'bars':{'quantity':barA/v.SHIP0['barPitchM'],'unit':'m','count':w['counts']['bars'],'drawn':f['bars']['barrelArcM'],'family':'bars/barrel'},
      'film':{'quantity':g['areaM2'],'unit':'m2','count':w['counts']['panels'],'drawn':draw.get('film',{}).get('areaM2'),'family':'ShipFilm mesh'},
      'clamps':{'quantity':g['areaM2']/v.SHIP0['ringPitchM']/v.SHIP0['barPitchM']/v.SHIP0['clampEvery'],'unit':'count','count':w['counts']['clamps'],'drawn':None,'family':'GridClamps patch only'},
      'pads':{'quantity':g['areaM2']/v.SHIP0['ringPitchM']/v.SHIP0['barPitchM']*(v.SHIP0['clampEvery']-1)/v.SHIP0['clampEvery'],'unit':'count','count':None,'drawn':None,'family':'not drawn'},
      'longerons':{'quantity':loc['long_len']*g['nLong'],'unit':'m','count':g['nLong'],'drawn':f['longs']['arcM'],'family':'longs'},
      'innerRings':{'quantity':s['nInnerRings']*2*math.pi*g['rIn'],'unit':'m','count':s['nInnerRings'],'drawn':f['hoopsInner']['arcM'],'family':'hoopsInner'},
      'fanWebs':{'quantity':loc['web_len']*loc['webs_per_col']*g['nLong'],'unit':'m','count':loc['webs_per_col']*g['nLong'],'drawn':f['webs']['lengthM'],'family':'webs'},
      'thetaWebs':{'quantity':s['thetaWebLenM']*s['nThetaWebs'],'unit':'m','count':s['nThetaWebs'],'drawn':f['thetas']['lengthM'],'family':'thetas'},
      'junctionShear':{'quantity':loc['junction_len']*2*g['nLong'],'unit':'m','count':2*g['nLong'],'drawn':f['junctions']['lengthM'],'family':'junctions; section inferred from smeared bill'},
      'spokes':{'quantity':v.ship_spoke_net(g)['lengthM'],'unit':'m','count':v.ship_spoke_net(g)['cords'],'drawn':f['spokes']['lengthM'],'family':'spokes; diameter inferred from smeared bill'},
      'flangeDoubler':{'quantity':barA,'unit':'m2','count':None,'drawn':None,'family':'not independently drawn'},
      'torsionStraps':{'quantity':g['areaM2'],'unit':'m2','count':None,'drawn':None,'family':'helical straps not drawn; outfit circumferential straps are different'},
      'skins':{'quantity':g['areaM2'],'unit':'m2','count':2,'drawn':None,'family':'void skin retired; jacket no separate mesh'},
      'tiJoints':{'quantity':sum(r['ledgerT'][x] for x in ['rings','capGrid','bars','longerons','innerRings','fanWebs','thetaWebs','flangeDoubler','junctionShear']),'unit':'t members','count':None,'drawn':None,'family':'GridJoints patch only'},
      'stabilityReserve':{'quantity':r['ledgerT']['stabilityReserve'],'unit':'t allowance','count':None,'drawn':None,'family':'additional solved areas; no separate drawing'},
    }
    for k,q in quantities.items():
        q['massT']=r['ledgerT'][k]
        if q['drawn'] is not None:
            q['delta']=q['drawn']-q['quantity'];q['drawnMassT']=q['massT']*q['drawn']/q['quantity'];q['deltaT']=q['drawnMassT']-q['massT']
    reserve={}
    if loc.get('a_i_2') is not None:
        # Price each purchased increment, not an average fraction of unrelated masses.
        reserve={'innerRings':(loc['a_i_2']-loc['a_i_1'])*rho*quantities['innerRings']['quantity']/1000*(1+v.SHIP0['junctionAdder'])/v.SHIP0['etaMass'],
         'thetaWebs':(loc['a_th_2']-loc['a_th_1'])*rho*quantities['thetaWebs']['quantity']/1000*(1+v.SHIP0['junctionAdder'])/v.SHIP0['etaMass'],
         'flangeDoubler':(loc['a_oe_2']-loc['a_oe_1'])*rho*barA/1000*(1+v.SHIP0['junctionAdder'])/v.SHIP0['etaMass'],
         'spokes':(loc['a_sp_2']-loc['a_sp_1'])*g['R']*v.SHIP0['rhoSpoke']*v.SHIP0['spokeFitting']*g['areaM2']/1000*(1+v.SHIP0['junctionAdder'])/v.SHIP0['etaMass']}
        assert abs(sum(reserve.values())-r['ledgerT']['stabilityReserve'])<1e-8
    return {'model':r,'bill':quantities,'reserveComponentsT':reserve,'capHoopsT':f['hoops']['capArcM']*w['ring']['kgPerM']/1000,'capBarsT':f['bars']['capArcM']*w['bar']['kgPerM']/1000}


def disagreements(bases, drawing):
    """Retain the original comparison set; unknown identity stays unknown."""
    out = []
    def add(key, kind, region, quantity=None, drawn=None, unit=None, line=None):
        out.append(dict(id=key, kind=kind, region=region, billQuantity=quantity,
                        drawnQuantity=drawn, unit=unit,
                        drawnMinusBill=None if quantity is None or drawn is None else drawn-quantity,
                        sign='unknown' if quantity is None or drawn is None else ('positive' if drawn>quantity else 'negative' if drawn<quantity else 'zero'),
                        byBasis={b: bases[b]['bill'].get(line, {}) for b in BASES} if line else {}))
    r = bases['record']
    for line in ('rings','innerRings','longerons','fanWebs','thetaWebs','junctionShear','bars','film','spokes'):
        q = r['bill'][line]
        if different(q['quantity'], q['drawn']):
            add(line, 'quantity', REGIONS[line], q['quantity'], q['drawn'], q['unit'], line)
    for line in ('capGrid','pads','flangeDoubler','torsionStraps','skins','tiJoints','stabilityReserve'):
        if r['model']['ledgerT'][line] > 0:
            add(line+'-allocation', 'no complete drawn allocation', REGIONS[line], line=line)
    for family in ('hoops','bars'):
        add('cap-'+family, 'drawn family has no station-mapped bill line', 'caps',
            drawn=drawing['families'][family]['capArcM'], unit='m')
        out[-1]['byBasis'] = {b: {'unallocatedSectionPriceT': bases[b]['capHoopsT' if family=='hoops' else 'capBarsT']} for b in BASES}
    add('fittings', 'clamp and joint symbols are a close-up, not a whole-hull count', 'whole hull')
    add('sections', 'inner-ring, fan, theta and junction display sections are schematic', 'whole hull')
    for key, line, billed, drawn in (
        ('outer-stations','rings',r['model']['wall']['counts']['rings'],drawing['families']['hoops']['rings']),
        ('inner-stations','innerRings',r['model']['skeleton']['nInnerRings'],drawing['families']['hoopsInner']['rings']),
        ('theta-count','thetaWebs',r['model']['skeleton']['nThetaWebs'],drawing['families']['thetas']['count'])):
        if different(billed,drawn,0,0):
            add(key,'count','whole hull stations' if key=='outer-stations' else REGIONS[line],billed,drawn,'count',line)
    return out


def measure():
    v = model()
    drawing = json.loads(subprocess.check_output(['node', 'research/analysis/member-census.mjs'], cwd=ROOT, text=True))
    configs = (('record',v.SHIP0['sigmaMid'],v.SHIP0['giKnockdown']),
               ('favourable','s1450',v.SHIP0['giKnockdownFrame']))
    def bases(d, draw):
        out = {}
        for name,key,kd in configs:
            try:
                out[name] = measure_basis(v,draw,key,kd,d,v.SHIP0['sfDeclared'])
                for line,q in out[name]['bill'].items():
                    q['region'] = REGIONS[line]
            except RuntimeError as e:
                out[name] = {'refusal': str(e)}
        return out
    record = bases(v.SHIP0['diaM'],drawing['record'])
    if any('refusal' in x for x in record.values()):
        raise RuntimeError('record hull sizing refused')
    out = dict(schema=1, status='accounting record; no checked cap design',
        provenance='gpt-6-astra executed the census and regeneration. muse-spark-1.3 and a second gpt-6 run examined the float case. claude-opus-5-5 ruled the publication basis. A person directs the project; no person checked the arithmetic.',
        basis={name:dict(knockdown=kd,chordAllowableMPa=v.SHIP0['sigmaWorldsMPa'][key],
                        structuralSF=v.SHIP0['sfDeclared'],pressurePa=v.P_ATM,
                        status='unverified material and imperfection assumptions') for name,key,kd in configs},
        drawing=drawing, record=record,
        drawnToBill={name:dict(billLines=lines, geometry=drawing['record']['families'][name],
                              allocation='unresolved in caps' if name in ('hoops','bars') else 'conditional current-section price')
                     for name,lines in FAMILIES.items()},
        scaledModels={key:bases(float(key),draw) for key,draw in drawing['nominal'].items()})
    out['disagreements'] = disagreements(record,drawing['record'])
    out['disagreementCount'] = len(out['disagreements'])
    return out


def fmt(value, places=3):
    return 'unknown' if value is None else f'{value:,.{places}f}'


def markdown(data):
    out = ['# Member census', '',
        'The drawing and the bill disagree. This generated record preserves those disagreements; it does not approve a cap design.',
        'The checks use smeared areas at full radius and do not resolve station lengths, sections or connections.', '',
        data['provenance'], '',
        f"There are **{data['disagreementCount']} recorded comparisons with disagreements** for the hull of record.",
        'A passing `make censuscheck` means fresh measurements match this record, including unknown counterparts.',
        'It does not mean the drawing agrees with the bill.', '',
        'Generated with `python3 research/analysis/member-census.py`. JSON: [complete measurements](../research/analysis/member-census.json).', '',
        '## Both directions', '',
        'Quantities use analytic arcs for rings and meridians, and actual endpoints for straight members.',
        'Rendering segments are not physical member counts. Signed differences are drawn minus billed.',
        'Tonnes price unchanged model sections, including existing allowances; they do not resize or check those sections.',
        'All mass pairs below are record / favourable. Unknown mass is never zero.', '',
        '| Bill line | Drawing counterpart | Region | Billed quantity | Drawn quantity | Signed difference | Unit | Billed t | Drawn t | Signed t |',
        '| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |']
    for line,q in data['record']['record']['bill'].items():
        pair = lambda field: ' / '.join(fmt(data['record'][b]['bill'][line].get(field)) for b in BASES)
        out.append(f"| {line} | {q['family']} | {q['region']} | {fmt(q['quantity'])} | {fmt(q['drawn'])} | {fmt(q.get('delta'))} | {q['unit']} | {pair('massT')} | {pair('drawnMassT')} | {pair('deltaT')} |")
    out += ['', '| Drawn family | Bill lines or allowance | Barrel m | Caps m | Total m | Physical count or runs | Render segments |',
            '| --- | --- | ---: | ---: | ---: | ---: | ---: |']
    def family_rows(draw):
        rows=[]
        for family,q in draw['families'].items():
            count=q.get('rings',q.get('members',q.get('meridians',q['count'])))
            rows.append(f"| {family} | {', '.join(FAMILIES[family])} | {fmt(q.get('barrelArcM',q['barrelM']))} | {fmt(q.get('capArcM',q['capM']))} | {fmt(q.get('arcM',q['lengthM']))} | {fmt(count,0)} | {q['count']} |")
        return rows
    out += family_rows(data['drawing']['record'])
    out += ['', 'The outer cap hoops have no hoop bill line. The cap bars have only an area allowance without station identities.',
            'The cap grid has no explicit drawing topology. Partial fitting symbols do not establish whole-hull populations.',
            'Film is billed on projected capsule area; the executed mesh has a different area and volume.', '',
            '## Recorded disagreements', '',
            '| Comparison | Region | Kind | Billed | Drawn | Signed difference | Sign |',
            '| --- | --- | --- | ---: | ---: | ---: | --- |']
    for q in data['disagreements']:
        out.append(f"| {q['id']} | {q['region']} | {q['kind']} | {fmt(q['billQuantity'])} | {fmt(q['drawnQuantity'])} | {fmt(q['drawnMinusBill'])} | {q['sign']} |")
    out += ['', '## Film, close-up fittings and outfit', '',
            'These are separate representations, not additional copies of the hull. The film mesh is a schematic drape, not a measured membrane.',
            'The outfit is outside the bare-hull mass comparison; its mass is unknown. The person and wrap are context, not added members.', '']
    for group in ('film','grid','outfit'):
        out += [f'### {group}', '', '| Quantity or object | Value or count | Chord length m |', '| --- | ---: | ---: |']
        obj=data['drawing']['record'][group]
        if isinstance(obj,dict):
            out += [f'| {k} | {fmt(value)} | — |' for k,value in obj.items()]
        else:
            out += [f"| {q['id']} | {q['count']} | {fmt(q.get('lengthM'))} |" for q in obj]
        out.append('')
    out += ['## Nominal fleet sizes: scaled models', '',
            'These execute the existing hull model at configured nominal fleet diameters. They are scaled models, not the fleet renderer’s member design.',
            'The fleet simulation uses a dry-structure allowance. This census does not replace that allowance or establish payload capacity.', '']
    for key,bases in data['scaledModels'].items():
        draw=data['drawing']['nominal'][key]
        out += [f'### Nominal diameter {float(key):g} m', '',
                '| Drawn family | Bill lines or allowance | Barrel m | Caps m | Total m | Physical count or runs | Render segments |',
                '| --- | --- | ---: | ---: | ---: | ---: | ---: |'] + family_rows(draw) + ['']
        for name,r in bases.items():
            if 'refusal' in r:
                out += [f"{name}: sizing refused: `{r['refusal']}`.", ''];continue
            out += [f"{name}: current model bill {fmt(r['model']['totalT'])} t.", '',
                    '| Bill line | Billed | Drawn | Signed quantity | Unit | Billed t | Drawn t | Signed t |',
                    '| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |']
            for line,q in r['bill'].items():
                out.append(f"| {line} | {fmt(q['quantity'])} | {fmt(q['drawn'])} | {fmt(q.get('delta'))} | {q['unit']} | {fmt(q['massT'])} | {fmt(q.get('drawnMassT'))} | {fmt(q.get('deltaT'))} |")
            out += ['']
        python_count=bases['record'].get('bill',{}).get('spokes',{}).get('count')
        out += [f"Spoke counts: Python bill {python_count if python_count is not None else 'sizing refused'}; JavaScript formula {draw['spokeNet']['cords']}; drawn {draw['families']['spokes']['count']}.",
                'The odd-column anchor and formula-length questions remain open.', '']
    out += ['Section allocation, fittings, polar omissions, torsion straps and the retired skin remain [open questions](OPEN-QUESTIONS.md).', '']
    return '\n'.join(out)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--json',type=Path,default=ROOT/'research/analysis/member-census.json')
    ap.add_argument('--markdown',type=Path,default=ROOT/'docs/MEMBER-CENSUS.md')
    args=ap.parse_args()
    result=measure()
    args.json.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    args.markdown.write_text(markdown(result))
    print(f"member census: {result['disagreementCount']} disagreements recorded; no design chosen")

if __name__=='__main__':
    main()
