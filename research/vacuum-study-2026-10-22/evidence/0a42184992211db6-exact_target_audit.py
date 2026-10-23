#!/usr/bin/env python3
"""Refine again only where a final boundary used an interpolated target stress."""
import json,pathlib
from data_tools import ROOT,P0,at_pressure
from refine import refine_group

def main():
    groups=json.loads((ROOT/"BOUNDARIES.json").read_text())
    assert len(groups)==8
    audit=[]
    for i,g in enumerate(groups):
        interpolated=[]
        for b in g["boundaries"]:
            for side in ["passing","failing"]:
                value=at_pressure(b[side+"_run"],P0*b["SF"])
                if value and not value["interpolation"].startswith("native"):
                    interpolated.append(dict(SF=b["SF"],side=side,run=b[side+"_run"]))
        if interpolated:
            file=ROOT/f"boundary-{g['label']}-{g['meridian']}.json"
            previous=ROOT/"code-versions"/"before-exact-target-fallback"/file.name
            if not previous.exists():
                file.rename(previous)
            g=refine_group(g["label"],g["meridian"],g["config"])
            groups[i]=g
            (ROOT/"BOUNDARIES.json").write_text(json.dumps(groups,indent=2)+"\n")
        audit.append(dict(group=g["label"]+"-"+g["meridian"],
                          interpolated_initial_edges=interpolated,
                          recalculated=bool(interpolated)))
        for b in g["boundaries"]:
            for side in ["passing","failing"]:
                value=at_pressure(b[side+"_run"],P0*b["SF"])
                assert value is None or value["interpolation"].startswith("native")
    (ROOT/"BOUNDARIES.json").write_text(json.dumps(groups,indent=2)+"\n")
    (ROOT/"EXACT-TARGET-AUDIT.json").write_text(json.dumps(
        dict(passed=True,groups=audit,
             method="Every final pass/fail edge uses a native target-pressure increment. Where adaptive cutbacks skipped service, an additional linear-ramp service cap replaces interpolation."),indent=2)+"\n")
    print(json.dumps(audit))
if __name__=="__main__":main()
