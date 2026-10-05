#!/usr/bin/env python3
"""OPEN-QUESTIONS #12: does the water arrive, and is tonnage the right metric?

    python3 research/analysis/delivery.py [--json OUT]

`deliveredT` counts tonnes leaving the tank. The US Forest Service says a load released
1,000 ft above the vegetation "would completely dissipate", and `ALT.drop` is 450 m —
1,476 ft. This script works out what is actually happening between the tank and the fuel,
in the only two terms that matter: how far the water drifts on the way down, and what
coverage it lays when it gets there.

Vehicle quantities come from research/figures.json. Everything else is stated below.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
FIGURES = ROOT / "research" / "figures.json"

# Coverage level is the fire world's unit for how much liquid is on the ground: US gallons
# per 100 square feet. Everything in aerial suppression is specified in it.
GAL_PER_100FT2_IN_L_PER_M2 = 3.78541 / 9.2903        # 0.4074

# Terminal velocity of free water drops, Gunn & Kinzer (1949), sea level. Drops larger than
# about 5.5 mm are aerodynamically unstable and break up, so ~9 m/s is the ceiling on how
# fast released water can fall — not a modelling choice, a property of water.
TERMINAL_MS = {0.5: 2.1, 1.0: 4.0, 2.0: 6.5, 3.0: 8.1, 5.0: 9.1}
MAX_STABLE_DROP_MM = 5.5

# JETTISON heights, not operational drop heights: USFS 2022 airtanker-base biological
# assessment section 4 lists these for training jettisons over designated areas. Real
# operational VLAT drops are lower again (DC-10 practice is 150-300 ft AGL), so the
# VLAT row here is if anything high. Kept because it is the only published table.
REFERENCE_HEIGHTS_M = {
    "single-engine airtanker": 18,     # 60 ft
    "large airtanker": 53,             # 150-200 ft, midpoint
    "very large airtanker": 122,       # 300-500 ft, midpoint
    "USFS 'completely dissipates'": 305,   # 1,000 ft
    "P-series ALT.drop": 450,
    # The design answer: the hull stays high and the SPRAYERS come down on leads, the same
    # way the intake hose already goes down 300 m to the water. Release height is then the
    # hull's altitude minus the lead, and it is a control input rather than a compromise.
    "sprayer lead, hull 450 m - 300 m lead": 150,
    "sprayer lead, hull 450 m - 400 m lead": 50,
}

# Load capacities for the comparison, litres.
TANKER_L = {"SEAT": 3028, "LAT (BAe-146)": 11350, "VLAT (DC-10)": 45400}

# Wildfire convection columns. Values in the 10-30 m/s band are routinely reported over
# active crown fire; 5 m/s is a quiet flank. This is the number that decides whether water
# released above a fire can reach it at all.
UPDRAFT_MS = {"quiet flank": 5, "active flank": 10, "crown fire column": 25}


def coverage_level(litres: float, run_km: float, swath_m: float) -> float:
    l_per_m2 = litres / (run_km * 1000.0 * swath_m)
    return l_per_m2 / GAL_PER_100FT2_IN_L_PER_M2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="OUT")
    args = ap.parse_args()
    fig = json.loads(FIGURES.read_text())

    out = {"generated": {"by": "research/analysis/delivery.py",
                         "figures": fig["generated"]},
           "fall": {}, "classes": {}, "references": {
               "dropHeightsM": REFERENCE_HEIGHTS_M,
               "updraftMs": UPDRAFT_MS,
               "maxStableDropMm": MAX_STABLE_DROP_MM,
               "terminalMs": TERMINAL_MS}}

    # 1. THE FALL. How long, and how far downwind, from each candidate release height.
    for h_name, h in REFERENCE_HEIGHTS_M.items():
        rec = {}
        for d, v in TERMINAL_MS.items():
            t = h / v
            rec[f"{d} mm"] = {
                "fallSeconds": round(t, 1),
                "driftM": {f"{w} m/s": round(w * t) for w in (3, 5, 10, 15)},
            }
        out["fall"][h_name] = rec

    # 2. THE COLUMN. A drop cannot descend through an updraft faster than it falls.
    out["updraftVerdict"] = {
        k: {"updraftMs": u,
            "dropsThatStillDescendMm":
                [d for d, v in sorted(TERMINAL_MS.items()) if v > u] or "none"}
        for k, u in UPDRAFT_MS.items()}

    wa = ROOT / 'research/analysis/water-availability.json'
    water = json.loads(wa.read_text())
    # Replay the accepted controls for the release's actual duration (the route can
    # take longer than emptying the tank at the installed pump rate).
    script = """
import fs from 'node:fs';
import {CLASSES,MODES,planCycle} from './sim/index.js';
const water=JSON.parse(fs.readFileSync('research/analysis/water-availability.json'));
console.log(JSON.stringify(Object.fromEntries(Object.entries(water.classes).map(([cid,c])=>{
 const row=c.acceptedPlans.workedExample;
 if(row.state!=='ready')return [cid,null];
 const p=planCycle(CLASSES[cid],MODES[row.mode],row.km,null,row.options);
 if(!p.feasible)throw Error(cid+': accepted worked example no longer closes');
 return [cid,p.dur.WATER_RELEASE*60];
}))));
"""
    release_seconds = json.loads(subprocess.check_output(
        ['node','--input-type=module','-e',script],cwd=ROOT,text=True))

    # 3. WHAT ONE PASS LAYS, against what an airtanker lays.
    for cid, cd in fig["classes"].items():
        spec, cyc = cd["spec"], cd["cycle"]
        plan = water['classes'][cid]['acceptedPlans']['workedExample']
        worked_ready = plan['state'] == 'ready' and plan['feasible'] is True
        if not worked_ready and any(plan[k] is not None for k in ('tph', 'releasedT', 'retainedT', 'suppliedMWh')):
            raise ValueError(f'{cid}: inactive worked example supplies logistics terms')
        litres = plan['releasedT'] * 1000.0 if worked_ready else None
        run_km = spec["dropKm"]
        rec = {
            "payloadT": plan["releasedT"],
            "workedExamplePlan": plan,
            "runKm": run_km,
            "releaseSeconds": round(release_seconds[cid], 0) if worked_ready else None,
            "releaseRateM3s": plan["releasedT"] / release_seconds[cid] if worked_ready else None,
            "coverageLevelBySwath": {
                f"{s} m": round(coverage_level(litres, run_km, s), 1) if worked_ready else None
                for s in (20, 30, 50, 80)},
            "equivalentLoads": {k: round(litres / v, 1) if worked_ready else None for k, v in TANKER_L.items()},
            # The line a class could lay if it flew its payload at a chosen coverage level
            # instead of at its fixed dropKm. CL 4 is a normal timber prescription.
            "lineKmAtCL": {
                f"CL{cl}, {s_} m swath": round(
                    litres / (cl * GAL_PER_100FT2_IN_L_PER_M2 * s_) / 1000.0, 2) if worked_ready else None
                for cl in (2, 4, 8) for s_ in (30,)},
            "_lineKmAtCL4": {
                f"{s} m swath": round(
                    litres / (4 * GAL_PER_100FT2_IN_L_PER_M2 * s) / 1000.0, 2) if worked_ready else None
                for s in (20, 30, 50, 80)},
        }
        # Daily logistics, at the real median leg from the water-availability analysis
        # rather than at the 15 km worked example, if that file has been generated.
        w = water['classes'][cid]
        median = w['acceptedPlans']['medianByFire']
        ready = median['state'] == 'ready' and median['feasible'] is True
        tph = median['tph'] if ready else None
        if not ready and median['tph'] is not None:
            raise ValueError(f'{cid}: inactive median plan supplies a rate')
        rec['atRealMedianLeg'] = {
            'legKm': w['distanceKm']['byFire']['p50'], 'plan': median,
            'tph': tph,
            'tonnesPer24h': round(tph * 24) if ready else None,
            'suppliedMWhPer24h': median['suppliedMWh'] * 1440 / median['cycleMin'] if ready else None,
            'latLoadsPer24h': round(tph * 24 * 1000 / TANKER_L['LAT (BAe-146)']) if ready else None,
        }
        out["classes"][cid] = rec

    # 4. THE METRIC THAT MEANS SOMETHING. AFUE never counts tonnes; it counts whether a drop
    # achieved its objective, and the objective for most large-aircraft drops is line. So
    # convert the fleet's day into kilometres of line at a real prescription, and put it
    # against the perimeters of the fires it would be flown at.
    hist = ROOT / "data" / "fire-history-bc.json"
    if hist.exists():
        fires = json.loads(hist.read_text())["fires"]
        perims = []
        for f in fires:
            ring = f[5]
            if not ring:
                continue
            ky = 110.574
            kx = 111.320 * math.cos(math.radians(f[1]))
            p = sum(math.hypot((ring[i + 1][0] - ring[i][0]) * kx,
                               (ring[i + 1][1] - ring[i][1]) * ky)
                    for i in range(len(ring) - 1))
            perims.append((p, f[2]))
        perims.sort()
        n = len(perims)
        out["perimeters"] = {
            "firesWithRings": n,
            "note": ("Rings are Douglas-Peucker simplified at ~200 m, so these perimeters are "
                     "LOWER bounds; a convoluted fire edge is longer than its outline."),
            "km": {f"p{q}": round(perims[min(n - 1, int(q / 100 * n))][0], 1)
                   for q in (10, 50, 90, 99)},
            "maxKm": round(perims[-1][0], 1),
        }
        for cid, r in out["classes"].items():
            if r["atRealMedianLeg"]["tph"] is None:
                for cl in (2, 4, 6, 8):
                    r["atRealMedianLeg"][f"lineKmPer24hAtCL{cl}_30mSwath"] = None
                    r["atRealMedianLeg"][f"pctOfPerimetersLinedDailyAtCL{cl}"] = None
                continue
            t24 = r["atRealMedianLeg"]["tph"] * 24
            for swath, cl in ((30, 2), (30, 4), (30, 6), (30, 8)):
                km = t24 * 1000.0 / (cl * GAL_PER_100FT2_IN_L_PER_M2 * swath) / 1000.0
                r["atRealMedianLeg"][f"lineKmPer24hAtCL{cl}_{swath}mSwath"] = round(km, 1)
            for cl in (2, 4, 6, 8):
                kmc = t24 / (cl * GAL_PER_100FT2_IN_L_PER_M2 * 30)
                r["atRealMedianLeg"][f"pctOfPerimetersLinedDailyAtCL{cl}"] = round(
                    100.0 * sum(1 for p, _ in perims if p <= kmc) / n, 1)

    # 5. THE SHIP'S OWN UPWASH. A buoyant hull holds station by thrusting DOWNWARD, which
    # means its rotors accelerate air UPWARD — the opposite sign to a helicopter. Over the
    # drop that is an updraft of the ship's own making, in exactly the place the water is
    # released, and by this document's own criterion it competes with the drop's descent.
    RHO = 1.10
    for cid, cd in fig["classes"].items():
        spec = cd["spec"]
        rows = {}
        # From an empty hull's surplus up to a loaded one: what the rotors hold during release.
        for frac, label in ((0.25, "start of release"), (1.0, "end of release")):
            held_t = cd["lift"]["surplusAtSourceT"] * frac
            thrust = held_t * 1000.0 * 9.81
            vi = math.sqrt(thrust / (2.0 * RHO * spec["diskM2"]))
            rows[label] = {
                "heldT": round(held_t, 1),
                "inducedUpwashAtDiscMs": round(vi, 1),
                "wakeMs": round(2 * vi, 1),
                "airMassFlowKgS": round(RHO * spec["diskM2"] * vi),
            }
        # HOW FAR DOWN DO YOU HAVE TO GO TO ESCAPE IT? Below the disc the rotor is a sink:
        # the volume flow Q = A*vi spreads over a hemisphere of radius z, so the induced
        # velocity falls as 1/z^2. This is why hanging the sprayers on a lead works — a few
        # hundred metres of lead puts the release outside the ship's own flow field entirely.
        vi_end = math.sqrt(cd["lift"]["surplusAtSourceT"] * 1000.0 * 9.81
                           / (2.0 * RHO * spec["diskM2"]))
        q = spec["diskM2"] * vi_end
        rows["inflowBelowHullMs"] = {
            f"{z} m below": round(q / (2.0 * math.pi * z * z), 2)
            for z in (25, 50, 100, 200, 300, 400)}
        rows["waterReleaseKgS"] = spec["fillM3s"] * 1000.0
        rows["airToWaterMassRatio"] = round(
            rows["end of release"]["airMassFlowKgS"] / (spec["fillM3s"] * 1000.0))
        out["classes"][cid]["ownUpwash"] = rows

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(out, indent=1))

    print("\nFALL TIME AND DRIFT (2 mm drops, the modal size that survives)")
    print(f"{'release height':<32}{'fall s':>8}{'drift @3':>10}{'@5':>8}{'@10':>8}{'@15':>8}")
    for k, h in REFERENCE_HEIGHTS_M.items():
        f = out["fall"][k]["2.0 mm"]
        d = f["driftM"]
        print(f"{k + f' ({h} m)':<32}{f['fallSeconds']:>8.1f}"
              f"{d['3 m/s']:>10}{d['5 m/s']:>8}{d['10 m/s']:>8}{d['15 m/s']:>8}")

    print("\nCAN IT GET DOWN THROUGH THE COLUMN?")
    for k, v in out["updraftVerdict"].items():
        print(f"  {k:<20} {v['updraftMs']:>3} m/s -> drops that still descend: "
              f"{v['dropsThatStillDescendMm']}")

    print("\nWHAT ONE PASS LAYS")
    for cid, r in out["classes"].items():
        if r["workedExamplePlan"]["state"] != "ready":
            print(f"  {cid}: worked example not served; no release or coverage quotient")
            continue
        print(f"  {cid}: {r['payloadT']:,.0f} t over {r['runKm']} km in "
              f"{r['releaseSeconds']:.0f} s")
        print(f"     coverage level by swath: "
              + ", ".join(f"{k} -> CL {v}" for k, v in r["coverageLevelBySwath"].items()))
        print(f"     accepted {r['workedExamplePlan']['mode']}: released {r['payloadT']} t, "
              f"retained {r['workedExamplePlan']['retainedT']} t, supplied "
              f"{r['workedExamplePlan']['suppliedMWh']:.6f} MWh/cycle; "
              f"{r['equivalentLoads']['LAT (BAe-146)']} LAT loads of water"
              + (f"; at the real median leg {r['atRealMedianLeg']['tonnesPer24h']:,} t/24 h "
                 f"= {r['atRealMedianLeg']['latLoadsPer24h']:,} LAT loads/day"
                 if r["atRealMedianLeg"]["tph"] is not None else "; median leg not served"))


if __name__ == "__main__":
    main()
