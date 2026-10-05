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
    return {file:text[:text.index(start)]+start+'\n'+sentence+end+text[text.index(end)+len(end):]}

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
