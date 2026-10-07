#!/usr/bin/env python3
"""Write or check station and invented-exercise distances from the water study record."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
def render(d):
    text='| Class | Points with an in-radius station | No selected source | Nearest station median / p90, km | Selected station median / p90, km | Selections offering an out-of-radius station |\n'
    text+='|---|---:|---:|---:|---:|---:|\n'
    for cid,name in [('P100','P-100'),('P1000','P-1000'),('P10000','P-10000')]:
        s=d['stationGeometry'][cid];n=s['nearestDistanceKm']['byFire'];c=s['selectedStationKm']['byFire']
        text+=f"| {name} | {s['nearestWithinClassSearchKm']} | {s['noSelectedSource']} | {n['p50']:.2f} / {n['p90']:.2f} | {c['p50']:.2f} / {c['p90']:.2f} | {s['selectionsOfferingOutOfRadiusStation']} |\n"
    text+='\n| Class | Selection farther than nearest station, % | p90 station detour, km |\n|---|---:|---:|\n'
    for cid,name in [('P100','P-100'),('P1000','P-1000'),('P10000','P-10000')]:
        c=d['crossCheck'][cid];text+=f"| {name} | {c['pctModelFlewFurther']:.2f} | {c['detourKm']['p90']:.2f} |\n"
    text+='\nInvented exercise geometry (empty when this study is run on another view):\n\n'
    text+='| Hull | Invented incident | Class | Nearest station, km | Mean planned leg, km | Plan state |\n|---|---|---|---:|---:|---|\n'
    for r in d['plannedExercise']['rows']:
        text+=f"| {r['hull']} | {r['incident']} | {r['class']} | {r['nearestStationKm']:.2f} | {r['meanPlannedLegKm']:.2f} | {r['state']} |\n"
    return text

def outputs():
    p=ROOT/'research/analysis/water-availability.md';s=p.read_text()
    start='<!-- water-stations:start -->';end='<!-- water-stations:end -->'
    assert s.count(start)==s.count(end)==1
    body=render(json.loads((ROOT/'research/analysis/water-availability.json').read_text()))
    old=s.split(start,1)[1].split(end,1)[0];new='\n'+body
    return {'research/analysis/water-availability.md':s.replace(start+old+end,start+new+end)}

def main():
    if '--emit' in sys.argv:
        print(json.dumps(outputs()));return 0
    for name,text in outputs().items():
        p=ROOT/name
        if '--check' in sys.argv:
            if p.read_text()!=text:
                print('FAIL water station note: differs from generated record');return 1
        else:p.write_text(text)
    print('PASS water station note: station distributions and invented-exercise legs match' if '--check' in sys.argv else 'Generated water station note');return 0
if __name__=='__main__':sys.exit(main())
