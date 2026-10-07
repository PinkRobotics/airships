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
 **{name:'research/analysis/delivery.md' for name in ('release-illustration','release-inflow')},
 **{name:'docs/VERIFICATION-PLAN.md' for name in ('release-register','release-conclusion')},
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
    reference_state=("The prescribed reference cycle does not close." if not rows['P100']['prescribedCloses'] else
        "The prescribed reference cycle closes in this model; that is not operational validation.")
    all_states=("The prescribed cycles do not close." if not any(r['prescribedCloses'] for r in rows.values()) else
        "Prescribed closure status: "+statuses+".")
    result.update({
      'nitrogen-register': f"| — | Is nitrogen needed in the normal cycle? | {basis}: the budget's net routine-make fraction is "
        f"**{nitrogen}** for the configured classes. Its reference anchor/hold diagnostic is **{margin:.1f}×**. "
        f"{statuses}. {all_states} This compares priced effort on the prescribed records; it does not establish that nitrogen can be omitted in operation. | `mass-budget.json`, `editorial-controls.json` |",
      'descent-register': f"| 3, 14, 15 | What does the letdown cost? | {basis}: the current descent ledger already prices "
        f"**{letdown}**. The record-basis bag-credit diagnostics are **{credits}** of cycle effort. "
        f"{all_states} These are diagnostic effort comparisons, not operational savings. | `descent.json` |",
      'disc-register': f"| 8 | Is `diskM2` inert? | **No.** On the same prescribed controls, doubling the reference disc "
        f"changes diagnostic supplied cycle effort by **{disc:.1f}%**. {reference_state} "
        "this is not a saving in operation. | `editorial-controls.json` |",
      'nitrogen-conclusion': f"On the {basis.lower()}, the reference net nitrogen-make fraction is "
        f"**{rows['P100']['netNitrogenPct']:.1f}%** of supplied cycle effort. {reference_state} "
        "The comparison is diagnostic and does not establish a routine nitrogen saving in operation.",
      'descent-conclusion': f"**Current letdown ledger.** {basis}: **{letdown}** for the configured classes, already "
        f"included in `descent.json`. {all_states} These are prescribed diagnostics; "
        "the earlier underpriced letdown calculation is superseded by this force-owner ledger.",
    })
    release_record=json.loads((root/'research/analysis/release-states.json').read_text())
    release=release_record['classes']['P100']
    if release['state']!='ready':
        for name in ('release-illustration','release-inflow','release-register','release-conclusion'):
            result[name]='Accepted reference release unavailable; no ideal-disc release estimate is published.'
    else:
        plan=release['plan'];start=release['states']['start of release'];end=release['states']['end of release']
        state_rows='\n'.join(f"| {label} | {s['altitudeAglM']:.0f} m | {s['densityKgM3']:.6f} kg/m³ | "
            f"{s['waterAboardT']:.1f} t | {s['heldT']:.3f} tf | {s['inducedUpwashAtDiscMs']:.1f} m/s | "
            f"{s['wakeMs']:.1f} m/s | {s['airMassFlowKgS']:,.0f} kg/s |" for label,s in release['states'].items())
        basis=f"the accepted {plan['km']:g} km {plan['mode']} reference plan ({plan['options']['basis']} basis), releasing {plan['releasedT']:g} t and retaining {plan['retainedT']:g} t"
        ratio=f"{release['airToWaterBenchmarkRatio']:.1f}"
        comparison=f"The endpoint ideal-disc air-flow estimate is **{end['airMassFlowKgS']:,.0f} kg/s**, "
        comparison+=f"**{ratio} times** the nominal **{release['waterBenchmarkKgS']:g} kg/s** water-rate benchmark from configured intake capacity. "
        comparison+=f"The accepted plan's mean tank release rate is {release['acceptedMeanWaterReleaseKgS']:,.1f} kg/s. "
        comparison+="Neither quantity measures outlet flow, a wake, drift or where water lands."
        speed=release_record['dropComparison']['largestTabulatedReleaseSpeedMs']
        relation='exceeds' if end['inducedUpwashAtDiscMs']>speed else 'does not exceed'
        comparison+=(f" At the end of release, the ideal induced upward velocity of {end['inducedUpwashAtDiscMs']:.1f} m/s "
            f"{relation} the largest tabulated density-corrected release-level fall speed, {speed:.3f} m/s. "
            "This compares the named endpoint with fixed-diameter drop speeds in the model air; it does not represent every drop or a ground pattern.")
        result.update({
          'release-illustration': "The producer replays "+basis+". The release endpoints use local air density, water aboard and rotor force ownership:\n\n"
            "| State | AGL altitude | Local density | Water aboard | Rotor hold | Ideal induced velocity upward | Ideal far-wake velocity | Ideal air flow |\n"
            "|---|---|---|---|---|---|---|---|\n"+state_rows+"\n\n"+comparison+
            " The upward-flow sign motivates further investigation; ideal-disc arithmetic alone does not establish deposition or suppression.",
          'release-inflow': "Point-sink heuristic using the accepted release endpoint's ideal-disc volume flow; this is not a measured wake:\n\n"
            "| Distance below hull | Reference heuristic inflow |\n|---|---|\n"+
            '\n'.join(f"| {z} | {v:.2f} m/s |" for z,v in release['inflowBelowHullMs'].items() if z!='25 m below'),
          'release-register': "| 12 | What does the release illustration represent? | Ideal-disc estimates at "+basis+". "+comparison+" | `release-states.json`, `delivery.json` |",
          'release-conclusion': "**Release basis.** The illustration follows "+basis+". "+comparison+
            " The release-height assumption and ground deposition remain open; no fire outcome is inferred.",
        })
    # Standalone region fences end a Markdown table. Each produced answer therefore
    # carries its own table header rather than leaving pipe text outside a table.
    header='| # | Question | Answer | Record |\n|---|---|---|---|\n'
    for name in ('nitrogen-register','descent-register','disc-register','release-register'):
        if result[name].startswith('|'):result[name]=header+result[name]
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
    except (OSError,ValueError,KeyError) as exc:print('editorial prose RED: '+str(exc));return 1
    if args.emit:print(json.dumps(result));return 0
    bad=cooling_errors(args.root)
    stale=[f for f,body in result.items() if (args.root/f).read_text()!=body]
    if args.check and (stale or bad):print('editorial prose RED: '+', '.join(stale+bad));return 1
    if not args.check:
        for f,body in result.items():(args.root/f).write_text(body)
    if bad:print('editorial cooling RED: '+', '.join(bad));return 1
    print('editorial prose: current answers and bases match their producing records; cooling open items retained');return 0
if __name__=='__main__':sys.exit(main())
