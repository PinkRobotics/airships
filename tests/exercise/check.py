#!/usr/bin/env python3
"""Exercise gate: regenerate, read the actual file, then drive three browser viewports.

No remote data is fetched. Optional test-name substrings select a mutation probe.
The guard's refused-words function is reused verbatim on this fourth kind of view.
"""
import importlib.util
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


gen = module('exercise_generator', 'tools/gen_exercise.py')
guard = module('guard_gate', 'tests/guard/check.py')
TESTS = []


def test(fn):
    TESTS.append(fn); return fn


def doc():
    return gen.read('data/exercise/exercise.json')


@test
def regenerated_bytes_and_seed():
    exercise, prov = gen.generate()
    for name, obj in [('exercise.json',exercise),('exercise.prov.json',prov)]:
        assert (ROOT/'data/exercise'/name).read_bytes() == gen.encoded(obj), f'{name}: differs from seeded regeneration'
    return f"seed {exercise['seed']}; both files byte-identical"


@test
def invented_identity_and_no_calendar():
    d=doc(); fs=d['fires']['features']; seen=set()
    assert d['kind']=='exercise' and d['label']==gen.MODE and d['note']==gen.NOTE
    for i,f in enumerate(fs,1):
        p=f['properties']; n=p['FIRE_NUMBER']
        assert re.fullmatch(r'EX\d{3}',n), f'exercise number {n!r} is not EX followed by three digits'
        assert n==f'EX{i:03d}' and n not in seen; seen.add(n)
        assert p['INCIDENT_NAME']==f'Exercise {i:03d}' and p['EXERCISE'] is True
        assert set(p)=={'FIRE_NUMBER','INCIDENT_NAME','EXERCISE','FIRE_STATUS','CURRENT_SIZE'}, 'unapproved incident field'
        assert p['FIRE_STATUS'] in {'Out of Control','Being Held','Under Control'}
        assert math.isfinite(p['CURRENT_SIZE']) and p['CURRENT_SIZE']>0
    for f in d['perimeters']['features']:
        p=f['properties']; assert p['FIRE_NUMBER'] in seen and p['EXERCISE'] is True
        assert p['INCIDENT_NAME']=='Exercise '+p['FIRE_NUMBER'][2:]
    assert not re.search(r'\d{4}-\d{2}-\d{2}',json.dumps(d)), 'an exercise is not a calendar day'
    idx=gen.read('data/season/2026.days.json')
    assert 'exercise' not in json.dumps(idx).lower(), 'exercise leaked into the season index'
    return f'{len(fs)} EX-numbered, named and labelled invented fires; no dates'


@test
def geography_from_the_committed_file():
    c=gen.context();gen.prepare_water(c); d=doc(); minima={k:math.inf for k in gen.LIMITS}
    rings={f['properties']['FIRE_NUMBER']:f['geometry']['coordinates'][0] for f in d['perimeters']['features']}
    for f in d['fires']['features']:
        p=f['properties']; ll=f['geometry']['coordinates']; ring=rings.get(p['FIRE_NUMBER'])
        radius=max(gen.hav(ll,q) for q in ring) if ring else math.sqrt(max(p['CURRENT_SIZE'],10)/math.pi)/10
        for k,v in gen.distances(c,ll,radius).items():
            assert v>=gen.LIMITS[k], f"{p['FIRE_NUMBER']}: {k} {v:.3f} < {gen.LIMITS[k]}"
            minima[k]=min(minima[k],v)
        assert -125.5<=ll[0]<=-121.5 and 57<=ll[1]<=59.8, 'outside stated region'
        assert gen.on_land(c,ll,radius), f"{p['FIRE_NUMBER']}: footprint crosses the outline or bundled water"
    # The record says in words that fires on neither list reject nothing, and how near the
    # nearest one is. Held here: that fire really is on neither list, and the sentence
    # carries the recorded distance (--check holds the distance itself to the generator).
    prov=gen.read('data/exercise/exercise.prov.json'); near=prov['nearestOtherFire']
    assert near['fire'] not in c['excluded'], f"{near['fire']} is on an exclusion list, so it is not 'another fire'"
    assert f"is {near['km']:.1f} km from an exercise footprint" in prov['distanceBasis'], 'the stated distance is not the recorded one'
    assert 'Fires on neither list reject nothing' in prov['notes'], 'the notice lost the sentence about other fires'
    return '; '.join(f'{k} >= {v:.3f}' for k,v in minima.items())+f" km; every footprint on bundled land; nearest fire on neither list {near['km']:.3f} km"


EXTRA = r"""
  out.exercise = S.exercise;
  out.title = document.title;
  out.meta = ['meta[name="description"]','meta[property="og:title"]','meta[property="og:description"]'].map(s=>document.querySelector(s).content);
  out.heading = txt('firesH');
  out.choice = document.getElementById('daySel').value;
  out.exerciseOption = [...document.getElementById('daySel').options].find(o => o.value==='exercise')?.textContent;
  out.wind = S.missions.filter(m=>m.wind).length;
  out.heat = S.heat.length;
  out.sourceIndices = S.missions.filter(m=>!m.idle).map(m=>m.waterIdx);
  out.namedCommunities = S.missions.filter(m=>m.protect).length;
  // Check the allocator's envelope against the original union, on ALL dates, including
  // places whose date has no captured fire file. S.regions cannot be quietly emptied.
  out.missingGuardEntries = S.guard.fires.filter(f=>f.keepOutKm>0 && !S.regions.some(r=>r.who===f.fire)).length;
  out.historicalCount = S.exerciseHistoricalRegions.length;
  out.envelopeFailures = S.exerciseHistoricalRegions.filter(r => {
    const envelope = S.regions.find(e=>e.who===r.who && e.kind===r.kind);
    return !envelope || (r.edge || [r.ll]).some(p=>sim.havKm(p,envelope.ll)+r.rKm>envelope.rKm+1e-8);
  }).length;
  const {select} = await import('/app/map/interact.js?v=eae942b2');
  out.drawerFailures=[];
  for (const f of S.fires) {
    select({type:'fire',f,m:null});
    const s=txt('cpOps');
    if (!s.includes(f.name) || !s.toLowerCase().includes('exercise') || s.includes('BC Wildfire Service') || /\d{4}-\d{2}-\d{2}/.test(s))
      out.drawerFailures.push(f.id);
  }
  out.tableNames=[...document.querySelectorAll('#firesTop tr td:first-child')].map(e=>e.textContent);
  out.rosterNames=[...document.querySelectorAll('#roster tr.r-ship td:nth-child(2)')].map(e=>e.textContent);
  const modeRect=document.getElementById('modeNote').getBoundingClientRect();
  out.chipOverlap=[...document.querySelectorAll('.hud .chip')].some(e=>{
    const r=e.getBoundingClientRect();
    return Math.min(r.right,modeRect.right)>Math.max(r.left,modeRect.left)+1 && Math.min(r.bottom,modeRect.bottom)>Math.max(r.top,modeRect.top)+1;
  });
  out.width=innerWidth;
  out.overflow=document.documentElement.scrollWidth-innerWidth;
  out.visibleDates=[];
  for (const e of document.body.querySelectorAll('*')) {
    if (e.closest('select,script,style,noscript') || !e.getClientRects().length) continue;
    for (const n of e.childNodes) if(n.nodeType===3 && /\d{4}-\d{2}-\d{2}/.test(n.textContent)) out.visibleDates.push(n.textContent);
  }
  // The canvas is its own channel: capture the text actually painted, including its
  // exercise watermark and labelled fire markers (there is no separate hover tooltip).
  document.getElementById('btnFitFires').click(); S.layers.labels=true;
  const {draw}=await import('/app/map/render.js?v=eae942b2');
  const ctx=document.getElementById('map').getContext('2d'), original=ctx.fillText;
  const painted=[]; ctx.fillText=function(s,...args){painted.push(s);return original.call(this,s,...args);};
  try {draw();} finally {ctx.fillText=original;}
  out.mapLabels=painted.filter(s=>/EX\d{3}|Exercise \d{3}|EXERCISE/.test(s));
"""
PROBE=guard.PROBE.replace('  return JSON.stringify(out);',EXTRA+'\n  return JSON.stringify(out);')
VIEWS={}


def pages(routes=False):
    keys=['precedence','default','sample'] if routes else [1440,834,390]
    if all(k in VIEWS for k in keys): return VIEWS
    with guard.serve() as base:
        if routes:
            # X7: explicit exercise wins over an old day query; default still tries live.
            for name,query in [('precedence','?view=exercise&day=2026-08-08'),('default',''),('sample','?data=snapshot')]:
                VIEWS[name]=guard.probe_once(base,query,guard.PROBE,5)
        else:
            for w,h in [(1440,900),(834,1112),(390,844)]:
                VIEWS[w]=guard.probe_once(base,'?view=exercise',PROBE,5,f'{w}x{h}')
    return VIEWS


@test
def page_labels_and_guard_at_three_widths():
    water=gen.read('data/water-bc.json')['water']
    for w in (1440,834,390):
        v=pages()[w]; p=v['panels']
        assert v['exercise'] and v['day'] is None and v['daySource']=='exercise' and not v['recordOnly'], v['standDown']
        assert 'EXERCISE' in p['hud'], f'{w}: missing EXERCISE status chip'
        assert 'exercise' in v['heading'].lower(), f'{w}: fires heading lost exercise'
        assert 'exercise' in v['title'].lower() and all('exercise' in s.lower() for s in v['meta'])
        guard.refuse_words(f'exercise metadata {w}',v['meta'])
        assert p['mode']==gen.MODE and p['guardNote']==gen.NOTE, f'{w}: ruled sentences moved'
        assert v['choice']=='exercise' and v['exerciseOption']=='Exercise: invented fires'
        assert not v['drawerFailures'] and all(re.fullmatch(r'Exercise \d{3}',n) for n in v['tableNames']+v['rosterNames'])
        assert 'EXERCISE · INVENTED FIRES' in v['mapLabels'] and len(v['mapLabels'])>1
        assert not any(re.fullmatch(r'EX\d{3}',s) for s in v['mapLabels']), 'unlabelled map marker'
        assert v['width']==w and v['overflow']<=1 and not v['chipOverlap'] and not v['visibleDates'], f'{w}: layout or date leak {v["visibleDates"]}'
        assert v['flying']==16 and v['uncovered']>0, 'exercise must commit all ships and leave a queue'
        assert v['wind']==v['heat']==v['namedCommunities']==0
        assert all(0<=i<len(water) and water[i][3]==0 for i in v['sourceIndices']), 'exercise uses only bundled lakes'
        assert v['historicalCount']>0 and v['envelopeFailures']==0 and v['missingGuardEntries']==0
        assert v['sweep']['samples']>100 and not v['sweep']['violations'], 'all-date guard sweep failed'
        guard.refuse_words(f'exercise {w}',v['visible'])
    v=VIEWS[1440]
    return f"1440/834/390: labels, all fire drawers and map labels; {v['flying']} ships, {v['uncovered']} queued; {v['sweep']['samples']} positions per view across three cycles, no violations"


@test
def exercise_is_explicit_and_never_the_failure_fallback():
    vs=pages(routes=True); v=vs['precedence']
    assert v['daySource']=='exercise' and v['day'] is None
    for k in ['default','sample']:
        v=vs[k]; assert v['daySource']=='sample' and v['day']==guard.SAMPLE_DAY and v['panels']['mode'].startswith('Replay of ')
    return f'default mirror failure and explicit snapshot remain replay of {guard.SAMPLE_DAY}'


@test
def static_reference_is_labelled():
    regs=dict(guard.fallback_regions()); html=regs['FALLBACK']
    assert re.search(r'<section[^>]*>\s*<p[^>]*>'+re.escape(gen.MODE)+r'</p>',html)
    assert gen.NOTE in html and '<b>EXERCISE</b>' in regs['FALLBACK-HUD']
    assert 'real fires' not in html and 'The fires are real' not in html
    assert not re.search(r'\d{4}-\d{2}-\d{2}', ''.join(regs.values()))
    guard.refuse_words('static exercise',list(regs.values()))
    # Pin the visually audited poster, including the label legible at 390 px.
    # A deliberate recapture requires another visual audit and this pin to move.
    assert hashlib.sha256((ROOT/'media/map-snapshot.jpg').read_bytes()).hexdigest() == 'c4e076ce60d800debca48be85416faf9a7e82b1bcd7f64ddef922296495f7463', 'poster differs from the labelled, visually audited image'
    assert '?view=exercise' in (ROOT/'tests/golden/check.py').read_text()
    assert '?view=exercise' in (ROOT/'tools/gen_fallback.py').read_text()
    return 'fallback opens with exact exercise sentence; poster exists; both reference generators use exercise'


def main():
    failed=0; selected=[f for f in TESTS if len(sys.argv)==1 or any(a in f.__name__ for a in sys.argv[1:])]
    for fn in selected:
        try: print('  ok   '+fn.__name__+': '+str(fn()),flush=True)
        except Exception as e:
            failed+=1;print('  FAIL '+fn.__name__+': '+type(e).__name__+': '+str(e),flush=True)
    print(f'exercise: {len(selected)-failed} passed, {failed} failed')
    return bool(failed)

if __name__=='__main__': sys.exit(main())
