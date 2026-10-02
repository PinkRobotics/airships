#!/usr/bin/env python3
"""Render the outside-structures questions from the published measurements."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
START='<!-- structure-questions:start -->'
END='<!-- structure-questions:end -->'


def render():
    m=json.loads((ROOT/'research/analysis/member-census.json').read_text())
    c=json.loads((ROOT/'research/analysis/cap-readings.json').read_text())
    f=json.loads((ROOT/'docs/audit/26-10-02-stiffness-sensitivity.json').read_text())
    r=m['record']['record'];b=m['record']['favourable'];d=m['drawing']['record']
    inner=r['bill']['innerRings'];j=r['bill']['junctionShear']
    scaled=m['scaledModels']['119']['record']['bill']['spokes']
    spokes=m['drawing']['nominal']['119']['families']['spokes']
    lines=[START, '## Questions for an outside structures engineer', '',
       '**Recorded 2026-10-02. Open.** These questions do not select a cap, a laminate or a new vehicle.',
       'The [member census](MEMBER-CENSUS.md) and [cap readings](../research/analysis/cap-readings.md) preserve the measured disagreement.', '',
       '### Cap members, directions and connections', '',
       f"What physical members, sections and connections make up the {d['dia']:g} m hull’s caps?",
       f"The drawing contains {d['families']['hoops']['capArcM']:,.3f} m of cap hoops without a hoop bill line.",
       f"The grid is charged by {r['bill']['capGrid']['quantity']:,.3f} m² of area: {r['bill']['capGrid']['massT']:.3f} t record and {b['bill']['capGrid']['massT']:.3f} t favourable.",
       'Do its membrane directions coincide with the drawn hoops or bars, and which sections and connections carry each load?',
       f"The drawn cap bars total {d['families']['bars']['capArcM']:,.3f} m; the grid also includes a bending-bar allowance.", '',
       '### Station-aware cap and shoulder checks', '',
       'What check would resolve station radius, member length, connection stiffness and the load transfer across each shoulder?',
       f"Inner rings total {inner['quantity']:,.3f} m in the bill and {inner['drawn']:,.3f} m in the drawing.",
       f"Shoulder diagonals total {j['quantity']:,.3f} m billed and {j['drawn']:,.3f} m drawn.",
       f"Their unchanged-section price increases by {j['deltaT']:.6f} t record and {b['bill']['junctionShear']['deltaT']:.6f} t favourable, before the separate joint allowance.",
       f"Removing the grid stiffness returns cap margin {c['controls']['record']['noGridStiffnessCapMargin']:g} on both bases.",
       'Which analysis and physical measurements would establish the applicability of a replacement check?', '',
       '### Conditional laminate-stiffness sensitivity', '',
       'What measured axial, hoop and shear properties, layup, coupling terms and compression allowables should describe the discrete tubes?',
       f"The code’s co-critical effective-modulus factor is {f['coCriticalFactor']:.12f}; the stated fibre-only 75/25 fixed-tube idealisation gives {f['fixedTubeFactor']:.12f}.",
       f"Their local-capacity ratio is {f['capacityRatio']:.9f}.",
       'The executed sensitivity also uses consistent axial and global moduli under that same idealisation.',
       '**This is conditional arithmetic, not measured laminate data or a corrected prediction.**', '',
       '| Basis | Original mass t | Conditional mass t | Original sea-level / 2,500 m ratios | Conditional sea-level / 2,500 m ratios |',
       '| --- | ---: | ---: | --- | --- |']
    for name,row in f['byBasis'].items():
        lines.append(f"| {name} | {row['oldMassT']:.6f} | {row['conditionalMassT']:.6f} | {row['oldRatios'][0]:.3f} / {row['oldRatios'][1]:.3f} | {row['conditionalRatios'][0]:.3f} / {row['conditionalRatios'][1]:.3f} |")
    lines += ['', 'Which laminate measurements would settle this difference before those moduli are used in a physical member check?',
       'Execution record: [conditional sensitivity](audit/26-10-02-stiffness-sensitivity.json).', '',
       '### Odd-column spoke anchors and polar stations', '',
       f"How should diametral spokes attach when the scaled model has {m['scaledModels']['119']['record']['model']['geom']['nLong']} columns at 119 m diameter?",
       f"The Python bill counts {scaled['count']:,} cords and the drawing contains {spokes['count']:,}.",
       f"The formula length is {scaled['quantity']:,.3f} m against {scaled['drawn']:,.3f} m drawn.",
       f"Which polar stations are physical members when {r['model']['skeleton']['nInnerRings']} inner stations are billed but {d['families']['hoopsInner']['rings']} rings are drawn?",
       'What sections, anchors and terminations belong at those stations?', '',
       '### Fittings, torsion straps and retired skin', '',
       f"What whole-hull fitting manifest replaces the area-derived {r['bill']['clamps']['quantity']:,.3f} clamps and {r['bill']['pads']['quantity']:,.3f} pads?",
       f"Which physical joints support the {r['bill']['tiJoints']['massT']:.3f} t record allowance and {b['bill']['tiJoints']['massT']:.3f} t favourable allowance?",
       f"Where are the helical torsion straps charged at {r['bill']['torsionStraps']['massT']:.3f} t, distinct from the outfit’s circumferential straps?",
       f"What does the {r['bill']['skins']['massT']:.3f} t skin line represent after the inner void skin was retired from the drawing?",
       'Which seals, coatings, bonds, seams and equipment attachments belong in a complete bill?', '',
       '<a id="breach-hand-figures"></a>',
       '### Breach hand figures without a generator', '',
       'What calculation, load case and material basis support the physics note’s 0.162 kg/m³ tension and 3.59 kg/m³ compression figures?',
       'They are hand figures without a generator. What would make that breach comparison reproducible and applicable to the proposed cellular architecture?',
       END, '']
    return '\n'.join(lines)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    path=ROOT/'docs/OPEN-QUESTIONS.md';text=path.read_text();block=render()
    if START in text:
        before,rest=text.split(START,1);_,after=rest.split(END,1)
        new=before+block.rstrip()+after
    else:
        new=text.replace('## What is not on this list',block+'\n---\n\n## What is not on this list')
    if args.check:
        if new!=text:raise SystemExit('structure questions differ from their measured records')
        print('structure questions: current measured figures and recorded conditional sensitivity match')
    else:
        path.write_text(new);print('structure questions generated')

if __name__=='__main__':main()
