#!/usr/bin/env python3
"""Compare the pre-solar sizing publication with fresh budget-generator records."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
def outputs():
 reference=json.loads((ROOT/'research/analysis/solar-budget-reference.json').read_text())
 budget=json.loads((ROOT/'research/analysis/mass-budget.json').read_text())
 start='<!-- solar:budget-comparison:start -->';end='<!-- solar:budget-comparison:end -->'
 rows=[]
 for cid,old in reference['classes'].items():
  now=budget['classes'][cid];sized=now['rightSized']['floor'];hull=sized['hullThatCloses']['0.508']
  pairs=[(old['nominalFloorT'],now['cases']['floor']['totalT'],'.1f'),
         (old['threeCycleFloorT'],sized['totalT'],'.1f'),
         (old['threeCycleFloorOverBy'],sized['overBy'],'.2f'),
         (old['enlargedVolumeM3'],hull.get('volumeM3') if isinstance(hull,dict) else None,',d'),
         (old['enlargedTimesBaseline'],hull.get('timesBaseline') if isinstance(hull,dict) else None,'.2f')]
  rows.append('| '+cid+' | '+' | '.join(f'{a:{fmt}} → '+(format(b,fmt) if b is not None else 'not closed') for a,b,fmt in pairs)+' |')
 body='''## Solar-input sensitivity of the existing budget diagnostic

This comparison preserves the pre-correction publication on the left and refreshes the
existing diagnostic on the right from `mass-budget.json`. The reason is the projected
solar-area correction; gross material area stays a separate assumption. Neither column
establishes a buildable hull or validates the enlarged-hull closure condition. If this
record is regenerated on an integrated tree, other model corrections can also contribute
to the differences; this comparison does not isolate their individual effects.

| Class | Nominal floor t | Three-cycle floor t | Three-cycle floor / dry | Existing 0.508 kg/m³ diagnostic volume m³ | Existing volume / baseline |
|---|---|---|---|---|---|
'''+ '\n'.join(rows)+'\n'
 p100=budget['classes']['P100']['rightSized']['floor']
 body+='\nP-100 density sweep of the same existing diagnostic; current values precede the preserved publication:\n\n'
 body+='| Shell kg/m³ | Current volume m³ | Current / baseline | Current length × diameter | Earlier volume m³ | Earlier / baseline | Earlier length × diameter |\n|---|---|---|---|---|---|---|\n'
 for density,old in reference['p100Hulls'].items():
  current=p100['hullThatCloses'].get(density)
  if not isinstance(current,dict) or 'volumeM3' not in current:
   body+=f"| {density} | not closed | | | {old['volumeM3']:,} | {old['timesBaseline']:.2f} | {old['lenM']} × {old['diaM']} m |\n"
   continue
  body+=f"| {density} | {current['volumeM3']:,} | {current['timesBaseline']:.2f} | {current['lenM']} × {current['diaM']} m | {old['volumeM3']:,} | {old['timesBaseline']:.2f} | {old['lenM']} × {old['diaM']} m |\n"
 body+='\nCurrent P-100 packing diagnostics (their earlier dimensions remain in the numeric reference):\n\n'
 body+='| Existing diagnostic | phi=0.74 | phi=0.85 | phi=1.0 |\n|---|---|---|---|\n'
 for density in ['0.264','0.508','0.750']:
  cells=[]
  for phi in ['phi=0.74','phi=0.85','phi=1.0']:
   value=p100['cellular'].get(phi,{}).get(density)
   cells.append(f"{value['volumeM3']:,} m³; {value['lenM']} × {value['diaM']} m" if isinstance(value,dict) and 'volumeM3' in value else 'not closed')
  body+='| hull at shell '+density+' | '+' | '.join(cells)+' |\n'
 intro='''The enlargement passages below retain the earlier sizing publication. The
[generated solar-input comparison](#solar-input-sensitivity-of-the-existing-budget-diagnostic)
records the changed power-input sensitivity separately; those earlier values are not
updated sizing claims. The closure condition itself remains unverified here.
'''
 file='research/analysis/mass-budget.md';text=(ROOT/file).read_text()
 baseline_volume=f"{reference['p100Hulls']['0.508']['volumeM3']:,}"
 if baseline_volume not in text.split('<!-- solar:budget-comparison:start -->')[0]:
  intro='''The [generated publication comparison](#solar-input-sensitivity-of-the-existing-budget-diagnostic)
records the preceding power-input publication beside the current integrated diagnostic.
It does not isolate each model correction or validate the enlarged-hull closure condition.
'''
 for key,content in [('budget-note',intro),('budget-comparison',body)]:
  s=f'<!-- solar:{key}:start -->';e=f'<!-- solar:{key}:end -->'
  if text.count(s)!=1 or text.count(e)!=1:raise ValueError('missing unique solar budget region')
  text=text[:text.index(s)]+s+'\n'+content+e+text[text.index(e)+len(e):]
 out={file:text}
 current=p100['hullThatCloses']['0.508']
 current_volume=f"{current['volumeM3']:,} m³" if isinstance(current,dict) and 'volumeM3' in current else 'no closing volume'
 old_volume=reference['p100Hulls']['0.508']['volumeM3']
 for file in ['docs/OPEN-QUESTIONS.md','docs/VERIFICATION-PLAN.md']:
  original=(ROOT/file).read_text();s='<!-- solar:budget-reference:start -->';e='<!-- solar:budget-reference:end -->'
  if original.count(s)!=1 or original.count(e)!=1:raise ValueError(file+': missing unique solar budget reference')
  qualification=("Earlier enlarged-hull figures on this page retain the preceding power-input publication. "
                 if baseline_volume in original[:original.index(s)] else
                 "The generated comparison preserves the preceding power-input publication beside the current integrated diagnostic. ")
  paragraph=(qualification+
             f"The existing P-100 0.508 kg/m³ sizing routine now returns {current_volume}, against the earlier {old_volume:,} m³, "
             "on the current model after the projected solar-area correction. Other integrated model corrections can also contribute. This is a diagnostic comparison, not validation of the closure condition. "
             "See the [generated before/after budget comparison](../research/analysis/mass-budget.md#solar-input-sensitivity-of-the-existing-budget-diagnostic).\n")
  out[file]=original[:original.index(s)]+s+'\n'+paragraph+e+original[original.index(e)+len(e):]
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--emit',action='store_true');a=p.parse_args();out=outputs()
 if a.emit:print(json.dumps(out));return 0
 if a.check and any((ROOT/f).read_text()!=b for f,b in out.items()):print('solar budget comparison RED: stale generated region');return 1
 if not a.check:
  for f,b in out.items():(ROOT/f).write_text(b)
 print('solar budget comparison: earlier publication and fresh power-input sensitivity match');return 0
if __name__=='__main__':sys.exit(main())
