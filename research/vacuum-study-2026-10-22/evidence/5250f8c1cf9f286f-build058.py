#!/usr/bin/env python3
"""MAINLINE-058: assemble RESULTS.json, NFI.json and INPUTS.json from the run files; print the card's numbers.
Lever hardware charged to the widest band (all PROJECTION): relief valve and controls 5 kg; water-ballast bladder 2 % of
its capacity (pillow-tank listings give 0.35-0.93 % for the fabric alone); ballast capacity = excess lift at the band's
cold edge over its worst-corner hot edge (P2), or the Heathrow 99th-percentile excess (P3, no cold screen)."""
import datetime
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lev058 as L  # noqa: E402
import p2m058 as m  # noqa: E402
import p3m058 as p3  # noqa: E402

ME = Path("unpublished-local-ref:b4008749caf12a44")
O = ME / "work/outputs/vacuum-mainline058-flyable-band-1020"
RUNS = O / "runs"
S = ME / "work/scripts/band058"
W = Path("unpublished-local-ref:7a5bf1cec24b249e")
SUB = Path("unpublished-local-ref:ab52dba26d6cc3a7")
SCR = Path("unpublished-local-ref:328c3cdb361f38a6"
           "62008c44-5149-4121-bd7d-8db0f4ad70e6/scratchpad")
VALVE_KG, BLADDER = 5.0, 0.02
RADII = (10, 12, 15, 20, 30)
TARGETS = (0.50, 0.75, 0.90, 0.95, 0.99)
AXES2 = {1: "gamma", 2: "Q", 4: "E/face", 8: "film"}
AXES3 = {1: "S", 2: "F", 4: "L", 8: "J"}


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def names(mask, axes):
    return "/".join(v for k, v in axes.items() if mask & k) or "none"


def jl(name):
    return json.loads((RUNS / name).read_text())


def main():
    lev, d1, db, dc, p3r, ex, val = (jl(n) for n in ("levers058.json", "days058.json", "days058b.json", "days058c.json",
                                                      "p3_058.json", "extra058.json", "validate058.json"))
    site = jl("heathrow_summary058.json")

    def hull(R, mask, hid):
        return next(h for h in lev["hulls"] if h["R_m"] == R and h["mask"] == mask and h["id"] == hid)

    def band(R, mask, hid, mode, dp, rh=1.0):
        return next(b for b in lev["bands"] if b["R_m"] == R and b["mask"] == mask and b["hull"] == hid and b["mode"] == mode
                    and b["dp_hPa"] == dp and b["RH"] == rh)["hot_edge_offset_K"]

    def dB(R, mask, hid, fin, st, v="primary"):
        return next(r for r in db["P2"] if r["R_m"] == R and r["mask"] == mask and r["hull"] == hid and r["finish"] == fin
                    and r["set"] == st and r["variant"] == v)

    def d3(R, sel, hid, st):
        return next(r for r in db["P3"] if r["R_m"] == R and r["selection"] == sel and r["hull"] == hid and r["set"] == st)

    def dC(R, fin, mask, dp):
        return next(r for r in dc["rows"] if r["R_m"] == R and r["finish"] == fin and r["mask"] == mask and r["design_dp_hPa"] == dp)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
