#!/usr/bin/env python3
"""Price five readings of the drawing–bill disagreement without patching the model."""
from __future__ import annotations
import argparse
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('member_census', Path(__file__).with_name('member-census.py'))
census = importlib.util.module_from_spec(spec)
spec.loader.exec_module(census)
NAMES = {
    'R': 'As billed',
    'A': 'Cap grid kept by area; matching members at drawn length',
    'B': 'Drawn hoops and bars billed; grid removed',
    'C': 'Grid and drawn hoops both charged',
    'D': 'Both charged; identifiable cap-bar double charge removed',
}


def readings(measured=None):
    measured = census.measure() if measured is None else measured
    v = census.model()
    f = measured['drawing']['record']['families']
    cap_hoops_length = f['hoops']['capArcM']
    cap_bars_length = f['bars']['capArcM']
    result = dict(schema=1, status='readings of a disagreement; no checked design',
                  basis=measured['basis'], geometry=measured['record']['record']['model']['geom'],
                  disagreementCount=measured['disagreementCount'], readings={}, ranges={}, controls={})
    for code,name in NAMES.items():
        result['readings'][code] = dict(name=name, byBasis={})
        for basis,meas in measured['record'].items():
            original=meas['model']; q=meas['bill']; wall=original['wall']
            lines=copy.deepcopy(original['ledgerT'])
            if code!='R':
                for line in ('innerRings','thetaWebs','fanWebs','longerons','junctionShear','bars'):
                    lines[line] *= q[line]['drawn']/q[line]['quantity']
                lines['stabilityReserve'] = sum(t * (q[k]['drawn']/q[k]['quantity'] if q[k]['drawn'] is not None else 1)
                                                for k,t in meas['reserveComponentsT'].items())
                if code in ('B','C','D'):
                    lines['rings'] += cap_hoops_length*wall['ring']['kgPerM']/1000
                    lines['bars'] += cap_bars_length*wall['bar']['kgPerM']/1000
                if code=='B':
                    lines['capGrid']=0
                if code=='D':
                    lines['capGrid'] -= wall['barKgM2']*q['capGrid']['quantity']/1000
                lines['tiJoints']=sum(lines[k] for k in census.MEMBERS)*(1/v.SHIP0['etaMass']-1)
            mass=sum(lines.values())
            result['readings'][code]['byBasis'][basis]=dict(
                massT=mass, deltaMassT=mass-original['totalT'], massByLineT=lines,
                at={alt:dict(altitudeM=height,liftT=original[lift],liftToMass=original[lift]/mass,marginT=original[lift]-mass)
                    for alt,height,lift in [('seaLevel',0,'liftSLT'),('target',2500,'lift2500T')]})
    for basis in census.BASES:
        result['ranges'][basis]={}
        for altitude in ('seaLevel','target'):
            vals={code:row['byBasis'][basis]['at'][altitude]['liftToMass'] for code,row in result['readings'].items()}
            lo,hi=min(vals,key=vals.get),max(vals,key=vals.get)
            result['ranges'][basis][altitude]=dict(min=vals[lo],max=vals[hi],minReading=lo,maxReading=hi)
        r=measured['record'][basis]; original=r['model']; wall=copy.deepcopy(original['wall'])
        wall['capGridKgM2']=wall['barKgM2']
        b=measured['basis'][basis]
        no_grid=v.ship_skeleton(original['geom'],b['chordAllowableMPa']*1e6,b['structuralSF'],wall,b['knockdown'])
        result['controls'][basis]=dict(
            originalReserveT=original['ledgerT']['stabilityReserve'],
            repricedReserveT=result['readings']['A']['byBasis'][basis]['massByLineT']['stabilityReserve'],
            reserveComponentsT=r['reserveComponentsT'],
            noGridStiffnessCapMargin=no_grid['capBuckle']['marginAtSF'],
            junctionBillM=r['bill']['junctionShear']['quantity'],junctionDrawnM=r['bill']['junctionShear']['drawn'],
            longeronBillM=r['bill']['longerons']['quantity'],longeronDrawnM=r['bill']['longerons']['drawn'])
    result['noneReachesOne']=all(q['max']<1 for basis in result['ranges'].values() for q in basis.values())
    return result


def markdown(data):
    g=data['geometry']
    rec,best=data['basis']['record'],data['basis']['favourable']
    out=['# End-cap readings', '',
         'These are readings of a disagreement between the bill and the drawing. None is a checked design.',
         'The sizing checks take smeared areas at full radius; they do not see each station’s length or resolve its connections.',
         'Removing the cap-grid stiffness gives zero cap margin on both bases.', '',
         f"The {g['diaM']:g} m diameter, {g['lenM']:g} m long hull of record retains its current bill.",
         'No model copy is patched. The drawing functions supply quantities; the current model supplies sections and purchased reserve increments.',
         'Matching skeleton lines and integer barrel bars are repriced in every alternative. Projected film area and the existing sag debit remain.',
         'The area-grid reading does not charge outer cap hoops as a second system. None of these readings changes the drawing.', '',
         'Generated by `python3 research/analysis/cap-readings.py`; [JSON](cap-readings.json) and [member census](../../docs/MEMBER-CENSUS.md).', '',
         f"Structural safety factor is {rec['structuralSF']:g} against full sea-level pressure. Altitude changes lift only.",
         f"The record basis assumes knockdown {rec['knockdown']:.2f} and a {rec['chordAllowableMPa']:,.0f} MPa chord allowable.",
         f"The favourable basis assumes knockdown {best['knockdown']:.2f} and a {best['chordAllowableMPa']:,.0f} MPa carbon-laminate compressive ceiling; both remain unverified.", '',
         '| Reading | Basis | Mass t | Change t | Sea-level lift/mass | Sea-level margin t | Lift/mass at 2,500 m | Margin t at 2,500 m |',
         '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for row in data['readings'].values():
        for basis,q in row['byBasis'].items():
            a,b=q['at']['seaLevel'],q['at']['target']
            out.append(f"| {row['name']} | {basis} | {q['massT']:.6f} | {q['deltaMassT']:+.6f} | {a['liftToMass']:.3f} | {a['marginT']:+.6f} | {b['liftToMass']:.3f} | {b['marginT']:+.6f} |")
    out+=['', '## Ranges', '']
    for basis,alts in data['ranges'].items():
        a,b=alts['seaLevel'],alts['target']
        out += [f"{basis.capitalize()}: {a['min']:.3f} to {a['max']:.3f} at sea level; {b['min']:.3f} to {b['max']:.3f} at 2,500 m."]
    if data['noneReachesOne']:
        out+=['No reading reaches 1 on either basis at either altitude.']
    else:
        out+=['At least one arithmetic reading reaches 1; no reading establishes a checked design.']
    out+=['', '## Mass by line', '']
    for basis in census.BASES:
        out += [f'### {basis}', '', '| Line | '+' | '.join(NAMES.values())+' |', '| --- | '+' | '.join(['---:']*len(NAMES))+' |']
        for line in data['readings']['R']['byBasis'][basis]['massByLineT']:
            out.append('| '+line+' | '+' | '.join(f"{data['readings'][code]['byBasis'][basis]['massByLineT'][line]:.6f}" for code in NAMES)+' |')
        out+=['']
    out+=['## What changed the earlier sensitivity', '',
          'The shoulder diagonals are measured at their drawn endpoints. The reserve is repriced by each purchased increment, not by a blended mass fraction.',
          'Longeron arcs cover the complete interval between the drawn endpoints. The earlier numerical integration omitted its last subinterval.', '']
    for basis,q in data['controls'].items():
        out+=[f"{basis.capitalize()}: shoulder diagonals {q['junctionBillM']:.3f} m billed, {q['junctionDrawnM']:.3f} m drawn; reserve {q['originalReserveT']:.6f} t becomes {q['repricedReserveT']:.6f} t."]
    out+=['', 'These accounting changes do not prove the capacity of shorter rings or longer braces. An outside structures assessment must settle their load paths and sections.', '']
    return '\n'.join(out)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--json',type=Path,default=Path(__file__).with_suffix('.json'))
    ap.add_argument('--markdown',type=Path,default=Path(__file__).with_suffix('.md'))
    args=ap.parse_args(); data=readings()
    args.json.write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    args.markdown.write_text(markdown(data))
    print('cap readings: five readings on two bases at two altitudes; no design chosen')

if __name__=='__main__':
    main()
