#!/usr/bin/env python3
"""Fill the nominal/three-cycle floor sentence from the generator's budget records."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]

def outputs():
    j=json.loads((ROOT/'research/analysis/mass-budget.json').read_text())['classes']['P100']
    base=j['cases']['floor'];sized=j['rightSized']['floor']
    sentence=(f"Sizing the battery to three prescribed cycles raises the floor from "
              f"**{base['totalT']:.1f} t, {base['overBy']:.2f}×**, to "
              f"**{sized['totalT']:.1f} t, {sized['overBy']:.2f}×**.\n")
    file='research/analysis/mass-budget.md';text=(ROOT/file).read_text()
    start='<!-- mass-budget:floor:start -->';end='<!-- mass-budget:floor:end -->'
    if text.count(start)!=1 or text.count(end)!=1:raise ValueError('missing unique floor sentence markers')
    text=text[:text.index(start)]+start+'\n'+sentence+end+text[text.index(end)+len(end):]
    all_classes=json.loads((ROOT/'research/analysis/mass-budget.json').read_text())['classes']
    ref=all_classes['P100']['plantComparisons'];s=ref['source']
    body=(f"The [ground StirLIN specification](https://www.criotecnica.com.br/wp-content/uploads/2017/06/stirlin2_specification.pdf) "
          f"gives {s['inputKW']:.0f} kW input, {s['massKg']:.0f} kg equipment and "
          f"{s['usableLitresHour']:.0f} usable atmospheric litres/hour. Its supplied cooling is excluded "
          "(the cooling interface and specification table); the [family datasheet](https://stirlingcryogenics.com/wp-content/uploads/2023/06/DS-StirLIN-family-ENG-28-06-2023.pdf) "
          "also excludes optional chiller power.\n\n"
          f"The exact input-matched ground ratio is {ref['inputTPerMW']:.6f} t/MW; the unchanged "
          f"rounded budget allowance is {json.loads((ROOT/'research/analysis/mass-budget.json').read_text())['evidence']['cryo_t_per_mw']['demonstrated']['value']:.1f} t/MW. "
          f"The stipulated liquid-density conversion is {ref['densityKgL']:.3f} kg/L. The output-matched ground ratio is "
          f"{ref['massPerOutputTph']:.6f} t of ground equipment per tonne/hour of usable liquid.\n\n"
          +ref['scope']+" No optional cooling unit quantity is established here; no cooling-option variant is used.\n\n"
          "| Class | Ground comparison | Plant t | Total nominal equipment t | Exceeds dry allowance |\n"
          "|---|---|---:|---:|---|\n")
    for cid,c in all_classes.items():
        for key,label in [('baselineFloor','Existing nominal floor'),('inputMatched','Supplied cooling; input matched'),('outputMatched','Supplied cooling; output matched')]:
            q=c['plantComparisons'][key]
            body+=f"| {cid} | {label} | {q['plantT']:.2f} | {q['totalT']:.2f} | {'yes' if q['exceedsAllowance'] else 'no'} |\n"
    start='<!-- mass-budget:plant-comparators:start -->';end='<!-- mass-budget:plant-comparators:end -->'
    if text.count(start)!=1 or text.count(end)!=1:raise ValueError('missing unique plant comparator markers')
    text=text[:text.index(start)]+start+'\n'+body+end+text[text.index(end)+len(end):]
    return {file:text}

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--emit',action='store_true');args=p.parse_args()
    out=outputs()
    if args.emit:print(json.dumps(out));return 0
    stale=[file for file,body in out.items() if (ROOT/file).read_text()!=body]
    if args.check and stale:print('floor prose RED: '+', '.join(stale));return 1
    if not args.check:
        for file,body in out.items():(ROOT/file).write_text(body)
    print('floor prose: nominal and three-cycle numbers match mass-budget.json');return 0
if __name__=='__main__':sys.exit(main())
