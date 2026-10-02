#!/usr/bin/env python3
"""A fixed, invented exercise on bundled BC land and lakes. Never reads the network.

Only aggregate count quantiles, size quantiles and control-stage proportions inform the
invented fires. No incident row, name, location, date, cause or URL becomes an exercise fire.
The geography record is used only to reject candidates. --check writes nothing.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import random
import re

ROOT = Path(__file__).resolve().parents[1]
SEED = 7
REGION = {"name": "Northern interior of British Columbia", "bbox": [-125.5, 57.0, -121.5, 59.8]}
LIMITS = {"guardKm": 150, "seasonNoteKm": 150, "communityKm": 25}
MODE = "Exercise: every fire on this map is invented. The terrain, the lakes and the distances are real."
assert LIMITS["guardKm"] == LIMITS["seasonNoteKm"], "the note states one distance for both limits"
NOTE = ("No fire shown here happened. No aircraft flew. The exercise shows how the simulated fleet chooses "
        f"under load. Its ground was chosen at least {LIMITS['guardKm']} km from every 2026 fire on the guard "
        "list and from every wildfire of note in the season record.")


def read(path):
    return json.loads((ROOT / path).read_text())


def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def hav(a, b):
    x, y = map(math.radians, a); u, v = map(math.radians, b)
    return 12742 * math.asin(min(1, math.sqrt(math.sin((v-y)/2)**2 + math.cos(y)*math.cos(v)*math.sin((u-x)/2)**2)))


def inside(p, ring):
    yes = False
    for a, b in zip(ring, ring[1:] + ring[:1]):
        if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < (b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]:
            yes = not yes
    return yes


def edge_km(p, ring):
    # Local equirectangular segment distance; a 2% safety subtraction below covers its
    # approximation at these sub-100 km scales and this latitude range.
    kx = 111.195 * math.cos(math.radians(p[1])); ky = 111.195
    best = math.inf
    for a, b in zip(ring, ring[1:] + ring[:1]):
        ax, ay = (a[0]-p[0])*kx, (a[1]-p[1])*ky
        bx, by = (b[0]-p[0])*kx, (b[1]-p[1])*ky
        dx, dy = bx-ax, by-ay
        t = max(0, min(1, -(ax*dx+ay*dy)/(dx*dx+dy*dy))) if dx or dy else 0
        best = min(best, math.hypot(ax+t*dx, ay+t*dy))
    return best * .98


def quantile(vals, p):
    vals = sorted(vals); pos = (len(vals)-1)*p; lo = int(pos); hi = min(lo+1, len(vals)-1)
    return vals[lo] + (vals[hi]-vals[lo])*(pos-lo)


def context():
    idx = read('data/season/2026.days.json')
    season = read('data/season/2026.json')['fires']
    guard = read('data/season/2026.guard.json')
    guarded = {f['fire'] for f in guard['fires']}
    noted = {f['fire'] for f in season if f['fireOfNote'] or f['wasFireOfNote']}
    # Centres and enclosing discs for EVERY captured outline, not just the latest view.
    # The conservative bound keeps the entire invented footprint 150 km away.
    discs = {n: [] for n in guarded | noted}
    for f in season:
        if f['fire'] in discs:
            discs[f['fire']].append(([f['lon'], f['lat']], math.sqrt(max(f['hindsightSizeHa'] or 0, 10)/math.pi)/10))
    days = []
    paths = ['data/season/2026.days.json','data/season/2026.json','data/season/2026.guard.json',
             'data/bc-outline.json','data/water-bc.json','sim/communities.js','data/terrain-bc.jpg']
    for d in idx['days']:
        fp = 'data/season/' + d['fires']['file']; pp = 'data/season/' + d['perims']['file']
        paths += [fp, pp]
        fires = read(fp)['data']['features']; perims = read(pp)['data']['features']
        days.append((d['date'], fires))
        for f in fires:
            p = f['properties']; n = p['FIRE_NUMBER']
            if n in discs:
                discs[n].append((f['geometry']['coordinates'][:2], math.sqrt(max(p['CURRENT_SIZE'] or 0, 10)/math.pi)/10))
        for f in perims:
            n = f['properties']['FIRE_NUMBER']; g = f['geometry']
            if n not in discs or not g: continue
            polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            for poly in polys:
                ring = poly[0]; ll = ring[0]
                discs[n].append((ll, max(hav(ll,p) for p in ring)))
    assert all(discs[n] for n in guarded | noted), 'unresolved exclusion entry'
    communities = json.loads(re.sub(r',\s*]', ']', re.search(r'export const CITIES = (\[.*?\]);', (ROOT/'sim/communities.js').read_text(), re.S)[1]))
    water = read('data/water-bc.json')['water']
    return dict(days=days, guard=[d for n in sorted(guarded) for d in discs[n]] + [(p['ll'],0) for p in guard['places']],
                note=[d for n in sorted(noted) for d in discs[n]], communities=[c[:2] for c in communities],
                outline=read('data/bc-outline.json'), water=water,
                sources={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(paths)})


def distances(c, ll, radius=0):
    return {"guardKm": min(hav(ll,p)-r-radius for p,r in c['guard']),
            "seasonNoteKm": min(hav(ll,p)-r-radius for p,r in c['note']),
            "communityKm": min(hav(ll,p)-radius for p in c['communities'])}


def on_land(c, ll, radius):
    land = [r for r in c['outline'] if inside(ll,r)]
    if not land or max(edge_km(ll,r) for r in land) <= radius + .1: return False
    for w in c['water']:
        # A bounding disc around each water polygon cheaply excludes distant bodies.
        if hav(ll,w[:2]) > w[-1] + radius + .1: continue
        ring = w[5] if len(w) > 7 else None
        if ring:
            if inside(ll,ring) or edge_km(ll,ring) <= radius + .1: return False
        elif hav(ll,w[:2]) <= w[-1] + radius + .1: return False
    return True


def prepare_water(c):
    for w in c['water']:
        ring = w[5] if len(w)>5 else None
        # Appended internal bounds never enter the generated document.
        radius = max(hav(w[:2],p) for p in ring) if ring else math.sqrt(w[2]/math.pi)/10
        w.extend([None, radius])


def fit(c):
    threshold = quantile([len(fs) for _,fs in c['days']], .75)
    busy = [(d,fs) for d,fs in c['days'] if len(fs) >= threshold]
    rows = [f['properties'] for _,fs in busy for f in fs]
    stages = Counter(p['FIRE_STATUS'] for p in rows if p['FIRE_STATUS'] in ('Out of Control','Being Held','Under Control'))
    qs = [0,.1,.25,.5,.75,.9,.95,1]
    return {"days": [d for d,_ in busy], "busyThresholdCount": threshold,
            "countQuantiles": {str(q): quantile([len(fs) for _,fs in busy],q) for q in qs},
            "sizeHaQuantiles": {str(q): quantile([p['CURRENT_SIZE'] or 0 for p in rows],q) for q in qs},
            "stageCounts": dict(sorted(stages.items())),
            "stageProportions": {k:v/sum(stages.values()) for k,v in sorted(stages.items())},
            "omittedStageRows": len(rows)-sum(stages.values()),
            "method": "Top quartile by captured active count, inclusive; type-7 quantiles. Inverse-CDF interpolation of count and log1p(size) quantiles; seeded categorical control-stage draws. Fire of Note is not a control stage, so those rows inform count and size but not stage proportions. No incident is sampled or relocated."}


def draw_quantiles(rng, qs, log=False):
    u = rng.random(); points = sorted((float(k),v) for k,v in qs.items())
    for (p,a),(q,b) in zip(points,points[1:]):
        if u<=q:
            if log: a,b = math.log1p(a),math.log1p(b)
            v = a+(b-a)*(u-p)/(q-p)
            return math.expm1(v) if log else v


def generate():
    c=context(); prepare_water(c); fitted=fit(c); rng=random.Random(SEED)
    count=round(draw_quantiles(rng,fitted['countQuantiles']))
    bbox=REGION['bbox']; fires=[]; perims=[]; minima={k:math.inf for k in LIMITS}; attempts=0
    while len(fires)<count:
        # Size and stage are drawn once per fire; geography rejection does not bias their mix.
        size=round(draw_quantiles(rng,fitted['sizeHaQuantiles'],True),3)
        status=rng.choices(list(fitted['stageProportions']),list(fitted['stageProportions'].values()))[0]
        angles=[2*math.pi*k/32 for k in range(32)]
        phase=rng.random()*2*math.pi
        unit=[((1+.12*math.sin(3*a+phase))*math.cos(a),(1+.12*math.sin(3*a+phase))*math.sin(a)) for a in angles]
        area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(unit,unit[1:]+unit[:1])))/2
        scale=math.sqrt(size/100/area); radius=max(math.hypot(*p) for p in unit)*scale if size>=80 else math.sqrt(max(size,10)/math.pi)/10
        for _ in range(20000):
            attempts+=1
            ll=[round(rng.uniform(bbox[0],bbox[2]),6),round(rng.uniform(bbox[1],bbox[3]),6)]
            ds=distances(c,ll,radius+.002)
            if any(ds[k]<LIMITS[k] for k in LIMITS) or ds['communityKm'] < 45 or not on_land(c,ll,radius+.002): continue
            if any(hav(ll,f['geometry']['coordinates'])<radius+2 for f in fires): continue
            break
        else: raise ValueError('No permissible draw: the constraints remain unchanged')
        for k in minima: minima[k]=min(minima[k],ds[k])
        i=len(fires)+1; number=f'EX{i:03d}'; name=f'Exercise {i:03d}'
        props={'FIRE_NUMBER':number,'INCIDENT_NAME':name,'FIRE_STATUS':status,'CURRENT_SIZE':size,'EXERCISE':True}
        fires.append({'type':'Feature','geometry':{'type':'Point','coordinates':ll},'properties':props})
        if size>=80:
            ring=[[round(ll[0]+x*scale/(111.195*math.cos(math.radians(ll[1]))),6),round(ll[1]+y*scale/111.195,6)] for x,y in unit]
            ring.append(ring[0])
            perims.append({'type':'Feature','geometry':{'type':'Polygon','coordinates':[ring]},
                           'properties':{'FIRE_NUMBER':number,'INCIDENT_NAME':name,'EXERCISE':True,'FIRE_SIZE_HECTARES':size}})
    doc={'kind':'exercise','seed':SEED,'label':MODE,'note':NOTE,'region':REGION,
         'fires':{'type':'FeatureCollection','features':fires},'perimeters':{'type':'FeatureCollection','features':perims}}
    prov={'file':'exercise.json','kind':'file','dataKind':'exercise','generator':'tools/gen_exercise.py','seed':SEED,'region':REGION,'count':count,
          'label':MODE,'note':NOTE,'fit':fitted,'minimumDistancesKm':{k:round(v,3) for k,v in minima.items()},
          'limitsKm':LIMITS,'placementCommunityClearanceKm':45,'attempts':attempts,'sourcesSha256':c['sources'],
          'geometry':'32-vertex radial polygons at >=80 ha, a seeded sinusoidal perturbation scaled to the drawn area in a local kilometre plane; otherwise the model uses its area-equivalent circle. Rounded to six decimal degrees. All footprints are inside the bundled BC outline and outside bundled water (unoutlined lakes conservatively use area-equivalent discs). Terrain is the bundled hillshade, not a measured height field.',
          'distanceBasis':'Conservative minimum clearances from the whole exercise footprint to enclosing discs of every guard and season-note observation and captured perimeter, on every captured date; guard places on all dates. Communities are exactly sim/communities.js, not a complete settlement inventory.',
          'wind':'Still air; no invented forecast.','authorship':'Project-generated synthetic data; source licences remain in data/README.md and DATA-SOURCES.md.'}
    prov.update(source=list(c['sources']), publisher='Pink Robotics',
                licence='Apache-2.0', licenceUrl='LICENSE',
                licenceStatement='Apache License, Version 2.0',
                licenceEvidence='LICENSE; invented scene produced by the project generator.',
                licenceReason='Project-authored synthetic data, describing no real fire.',
                attribution='Pink Robotics. Licensed under Apache-2.0.',
                notes='This invented scene describes no real fire. ' + prov['geometry'] + ' ' + prov['distanceBasis'] + ' ' + prov['wind'],
                decision='redistributed', sha256=hashlib.sha256(encoded(doc)).hexdigest(),
                measurements={'bytes': len(encoded(doc))},
                documentation=json.loads((ROOT/'tools/exercise-notes.json').read_text()))
    return doc,prov


def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    doc,prov=generate()
    for name,obj in [('exercise.json',doc),('exercise.prov.json',prov)]:
        p=ROOT/'data/exercise'/name; raw=encoded(obj)
        if args.check:
            if not p.exists() or p.read_bytes()!=raw: raise SystemExit(f'exercise: {p.relative_to(ROOT)} differs from regeneration')
        else: p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(raw)
    print(f"exercise: {'byte-identical' if args.check else 'generated'}; {prov['count']} invented fires; minima km {prov['minimumDistancesKm']}")

if __name__=='__main__': main()
