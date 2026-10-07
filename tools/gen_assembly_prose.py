#!/usr/bin/env python3
"""Keep assembly prose bound to the computed report and its frozen contract."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FILE = 'research/analysis/vacuum-cell.md'

def outputs(root=ROOT):
    report = json.loads((root/'research/geometry/nodes/assembly.json').read_text())
    cap = json.loads((root/'research/geometry/nodes/contract.json').read_text())
    proofs = report['proofs']
    passed = sum(p['passed'] for p in proofs)
    assert len({p['id'] for p in proofs}) == len(proofs)
    assert report['verdict']['proofsRun'] == len(proofs)
    assert report['verdict']['proofsPassed'] == passed
    assert {p['id']: p['passed'] for p in proofs} == {k: v['passed'] for k,v in cap['checks'].items()}
    failures = ', '.join(p['id'] for p in proofs if not p['passed'])
    demand = next(p for p in proofs if p['id']=='P12')
    closing=sum(e['isClosingMember'] for e in report['ends'])
    seat=max(e['bearingAreaAt20umMm2'] for e in report['ends'])
    slot=report['paramsMm']['slot_margin']
    sections = {
        'assembly-geometry': f"The computed assembly checks include every one of the **{closing} closing ends** "
            "against its own pilot bound. This does not mean the insertion sweep checked every end. "
            f"The seat is a real land of **{seat:.3f} mm²**. No slot starts closer than the declared "
            f"**{slot:.3f} mm** to the feature it would foul. The fast-mode sweep checks the representatives "
            "named in the result; its failing representative and every frozen failure remain below.",
        'assembly-status': f"**{passed} of the {len(proofs)} proofs pass** in the stored {report['sampling']['mode']}-mode assembly result. "
            "These are computational checks of geometry and load provenance, not physical tests.",
        'assembly-demand': f"The demand-provenance check {demand['id']} {'passes' if demand['passed'] else 'fails'}: "
            f"{demand['headline']}. A derived demand is not a demonstrated strength or equilibrium result.",
        'assembly-failures': f"The {len(proofs)-passed} failed proofs ({failures}) and all "
            f"{report['verdict']['frozen']} frozen defects remain visible in "
            "`research/geometry/nodes/assembly.json` and its frozen contract. Agreement with that contract "
            "does not mean a defect-free or physically proven article.\n\n"
            "| Proof | Computed result |\n|---|---|\n" +
            '\n'.join(f"| {p['id']} — {p['name']} | {p['headline']} |" for p in proofs if not p['passed'])
    }
    text=(root/FILE).read_text()
    for name, body in sections.items():
        start=f'<!-- editorial:{name}:start -->';end=f'<!-- editorial:{name}:end -->'
        if text.count(start)!=1 or text.count(end)!=1: raise ValueError('missing unique region '+name)
        lo=text.index(start);hi=text.index(end,lo)+len(end)
        text=text[:lo]+start+'\n'+body+'\n'+end+text[hi:]
    vp='docs/VERIFICATION-PLAN.md'
    plan=(root/vp).read_text()
    start='<!-- editorial:joint-bill:start -->';end='<!-- editorial:joint-bill:end -->'
    if start not in plan and end not in plan:
        if 'modelled printed joints' in plan:
            raise ValueError('missing joint-bill region on the modelled bill')
        return {FILE:text}
    assert plan.count(start)==plan.count(end)==1
    manifest=json.loads((root/'research/geometry/nodes/manifest.json').read_text())
    body=f"**{len(manifest['nodes'])} modelled printed joints** ({manifest['totalNodeMassKg']:.3f} kg, "
    body+="computed from geometry at the manifest's assumed print density)"
    lo=plan.index(start);hi=plan.index(end,lo)+len(end)
    plan=plan[:lo]+start+'\n  '+body+'\n  '+end+plan[hi:]
    return {FILE:text,vp:plan}

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--emit',action='store_true');p.add_argument('--root',type=Path,default=ROOT);args=p.parse_args()
    try: result=outputs(args.root)
    except (ValueError,AssertionError,KeyError) as exc: print('assembly prose RED: '+str(exc));return 1
    if args.emit: print(json.dumps(result));return 0
    stale=[f for f,body in result.items() if (args.root/f).read_text()!=body]
    if args.check and stale: print('assembly prose RED: '+', '.join(stale));return 1
    if not args.check:
        for f,body in result.items(): (args.root/f).write_text(body)
    print('assembly prose: counts, demand status and every frozen failure match the assembly result');return 0
if __name__=='__main__':sys.exit(main())
