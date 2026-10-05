#!/usr/bin/env python3
"""Keep the few ungenerated solar statements tied to the new collecting-area record."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
def outputs():
 solar=json.loads((ROOT/'research/analysis/solar-area.json').read_text())
 energy=json.loads((ROOT/'research/analysis/energy-documents.json').read_text())
 delivery=json.loads((ROOT/'research/analysis/delivery.json').read_text())
 p=next(r['asDrawn'] for r in energy['records'] if r['class']=='P100' and r['km']==15 and r['basis']=='record')
 solar_mw=solar['classes']['P100']['creditedSolarMW']
 average=p['cycleMWh']*60/p['cycleMin']
 fraction=100*solar['coverage']['fraction']
 daily=delivery['classes']['P100']['atRealMedianLeg']
 daily_supply=(f"{daily['suppliedMWhPer24h']:.1f} MWh of supplied effort per P-100 per day at the accepted median-leg rate,"
               if daily['suppliedMWhPer24h'] is not None else
               "The median-leg P-100 plan is not served, so it supplies no daily energy or delivery quotient,")
 bodies={
  ('research/reports/02-paper.md','area'):
   f"`solarM2` is {fraction:.0f}% of each current capsule's projected footprint, a named design assumption\n"
   "rather than a validated panel layout. See the [generated areas](../analysis/solar-area.json).\n",
  ('research/reports/03-diligence.md','supply'):
   f"- **Continuous supplied effort, reference ship, unsupported prescribed profile:** 1.391 → 8.042 → {p['cycleMWh']:.3f} MWh<!--f:P100.cycle.eCycleMWh--> per\n"
   f"  {p['cycleMin']:.1f}-minute<!--f:P100.cycle.cycleMin--> cycle = **{average:.2f} MW average**, or **{average-solar_mw:.2f} MW imported** net\n"
   f"  of the assumed projected solar ({solar_mw:.2f} MW<!--f:P100.energy.solarMW-->). These quotients establish no delivery or endurance.\n",
  ('docs/VERIFICATION-PLAN.md','daily'):
   f"3. **The energy supply chain.** {daily_supply}\n"
   f"   against {solar_mw*24:.2f} MWh/day of assumed solar. The tender fleet is named in the README and deliberately never\n"
   "   modelled. **Every 24-hour figure in this folder is a claim about the aircraft, not about a\n"
   "   system shown to supply it.**\n",
 }
 out={}
 for (file,key),body in bodies.items():
  text=(ROOT/file).read_text();start=f'<!-- solar:{key}:start -->';end=f'<!-- solar:{key}:end -->'
  if text.count(start)!=1 or text.count(end)!=1:raise ValueError(file+': missing unique solar prose markers')
  out[file]=text[:text.index(start)]+start+'\n'+body+end+text[text.index(end)+len(end):]
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--emit',action='store_true');a=p.parse_args();out=outputs()
 if a.emit:print(json.dumps(out));return 0
 stale=[f for f,b in out.items() if (ROOT/f).read_text()!=b]
 if a.check and stale:print('solar prose RED: '+', '.join(stale));return 1
 if not a.check:
  for f,b in out.items():(ROOT/f).write_text(b)
 print('solar prose: three current statements match their collecting-area and energy records');return 0
if __name__=='__main__':sys.exit(main())
