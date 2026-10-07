#!/usr/bin/env python3
"""Generate current editorial answers from repository records, with their bases."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
CONTRACTS={
 'current-hull':'docs/PHYSICS.md',
 'turbulence':'docs/PHYSICS.md',
 'certification':'docs/VERIFICATION-PLAN.md',
 'drop-hull':'research/reports/03-diligence.md',
 **{name:'docs/VERIFICATION-PLAN.md' for name in ('nitrogen-register','descent-register','disc-register','nitrogen-conclusion','descent-conclusion')},
}

def sections(root=ROOT):
    classes=json.loads((root/'research/analysis/energy-documents.json').read_text())['classes']
    ref=next(c for c in classes if c['class']=='P100');big=max(classes,key=lambda c:c['lengthM'])
    dims='; '.join(f"{c['class']}: {c['lengthM']:g} m long × {c['diameterM']:g} m diameter" for c in classes)
    result = {
      'current-hull': "**Current architecture.** The concept drawing uses one film on hoop rings over a two-walled "
        "truss, with machinery on an ambient-pressure raft outside the vacuum. Compartment membranes are intended "
        "to limit breach damage; their arrangement remains open. No drawn hull floats. The configured fleet is "
        +dims+". These are fleet-model assumptions, distinct from the drawn structural hull and any enlarged "
        "equipment-budget closure.\nThe dimensions come from `energy-documents.json`, generated from `sim/config.js`.",
      'turbulence': f"- **Turbulence and gust loading.** The largest configured hull is {big['lengthM']:g} m long. "
        "Its behaviour in a convective column is a structural and control problem the model does not represent. "
        "The configured release height is an assumption, not a gust-loading result.",
      'certification': f"4. **Certification and airspace.** No airworthiness basis is established for the configured "
        f"{ref['lengthM']:g} m reference hull, with an assumed dry allowance of {ref['payloadT']:g} t "
        f"and requested water load of {ref['payloadT']:g} t. These are model allowances, not a built aircraft's "
        "weighed mass. Canadian certification and airspace requirements remain an open work item.",
      'drop-hull': f"3. **A drop from a height a {big['lengthM']:g} m configured hull can safely use that still "
        "arrives as water.** The source guidance contradicts the current release premise. Needs droplet physics "
        "and, eventually, a drop test; no model quantity establishes ground deposition.",
    }
    replay=json.loads((root/'research/analysis/editorial-controls.json').read_text())
    budget=json.loads((root/'research/analysis/mass-budget.json').read_text())['classes']
    descent=json.loads((root/'research/analysis/descent.json').read_text())['classes']
    rows=replay['classes'];controls=replay['controls'];ids=list(rows)
    basis=f"Prescribed {controls['mode']}, {controls['km']:g} km, {controls['basis']}-basis controls"
    statuses='; '.join(f"{r['name']}: prescribedCloses={str(r['prescribedCloses']).lower()}" for r in rows.values())
    nitrogen=' / '.join(f"{budget[c]['descentWithoutNitrogen']['cycleSavingPct']:.1f}%" for c in ids)
    credits=' / '.join(f"{descent[c]['rotorsBlindToTheBag']['creditSavesPctOfCycle']:.1f}%" for c in ids)
    letdown=' / '.join(f"{descent[c]['letdown']['mwh']:.3f} MWh" for c in ids)
    margin=budget['P100']['descentWithoutNitrogen']['marginX']
    disc=rows['P100']['doubledDiscChangePct']
    result.update({
      'nitrogen-register': f"| — | Is nitrogen needed in the normal cycle? | {basis}: the budget's net routine-make fraction is "
        f"**{nitrogen}** for the configured classes. Its reference anchor/hold diagnostic is **{margin:.1f}×**. "
        f"{statuses}. This compares priced effort on nonclosing cycles; it does not establish that nitrogen can be omitted in operation. | `mass-budget.json`, `editorial-controls.json` |",
      'descent-register': f"| 3, 14, 15 | What does the letdown cost? | {basis}: the current descent ledger already prices "
        f"**{letdown}**. The record-basis bag-credit diagnostics are **{credits}** of cycle effort. "
        "These are diagnostic comparisons on cycles that do not close, not operational savings. | `descent.json` |",
      'disc-register': f"| 8 | Is `diskM2` inert? | **No.** On the same prescribed controls, doubling the reference disc "
        f"changes diagnostic supplied cycle effort by **{disc:.1f}%**. The prescribed cycle does not close; "
        "this is not a saving in operation. | `editorial-controls.json` |",
      'nitrogen-conclusion': f"On the {basis.lower()}, the reference net nitrogen-make fraction is "
        f"**{rows['P100']['netNitrogenPct']:.1f}%** of supplied cycle effort. The prescribed cycle does not close. "
        "The comparison is diagnostic and does not establish a routine nitrogen saving in operation.",
      'descent-conclusion': f"**Current letdown ledger.** {basis}: **{letdown}** for the configured classes, already "
        "included in `descent.json`. These are prescribed diagnostics on cycles that do not close; "
        "the earlier underpriced letdown calculation is superseded by this force-owner ledger.",
    })
    return result

def outputs(root=ROOT):
    result={}
    for name,body in sections(root).items():
        f=CONTRACTS[name];text=result.get(f,(root/f).read_text())
        start=f'<!-- editorial:{name}:start -->';end=f'<!-- editorial:{name}:end -->'
        if text.count(start)!=1 or text.count(end)!=1:raise ValueError('missing unique region '+name)
        lo=text.index(start);hi=text.index(end,lo)+len(end)
        result[f]=text[:lo]+start+'\n'+body+'\n'+end+text[hi:]
    return result

def cooling_errors(root=ROOT):
    bad=[]
    for f in ('docs/VERIFICATION-PLAN.md','research/analysis/mass-budget.md'):
        text=(root/f).read_text()
        for old in ('need to reject heat with no convection','inside a vacuum envelope with','thermal management with no convection'):
            if old in text:bad.append(f+': stale current cooling premise '+old)
        for word in ('ducting','coolant loops','ventilation'):
            if word not in text:bad.append(f+': missing cooling open item '+word)
    return bad

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--emit',action='store_true');p.add_argument('--root',type=Path,default=ROOT);args=p.parse_args()
    try:result=outputs(args.root)
    except (ValueError,KeyError) as exc:print('editorial prose RED: '+str(exc));return 1
    if args.emit:print(json.dumps(result));return 0
    bad=cooling_errors(args.root)
    stale=[f for f,body in result.items() if (args.root/f).read_text()!=body]
    if args.check and (stale or bad):print('editorial prose RED: '+', '.join(stale+bad));return 1
    if not args.check:
        for f,body in result.items():(args.root/f).write_text(body)
    if bad:print('editorial cooling RED: '+', '.join(bad));return 1
    print('editorial prose: current answers and bases match their producing records; cooling open items retained');return 0
if __name__=='__main__':sys.exit(main())
