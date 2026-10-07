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

# Gunn–Kinzer free-drop speeds in sea-level reference air. Local terminal speeds
# are density-adjusted below; this table is not a density-independent fall ceiling.
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
    # The design answer: the hull stays high and the SPRAYERS come down on leads, the same
    # way the intake hose already goes down 300 m to the water. Release height is then the
    # hull's altitude minus the lead, and it is a control input rather than a compromise.
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


# Beard density adjustment as printed in Ghiggi et al., Appendix B1 Eq. B1.
# The source's reference density is retained; the local column comes from sim/.
CORRECTION_RHO0 = 1.225
WARM_SENSITIVITY_K = 15  # Stipulated fixed-pressure sensitivity, not observed weather.
DRIFT_WINDS_MS = (3, 5, 10, 15)  # Stipulated uniform drift inputs.


def terminal_speed(diameter_mm, reference_ms, rho):
    return reference_ms * (CORRECTION_RHO0 / rho) ** (0.375 + 0.025 * diameter_mm)


def model_air():
    script = """
import {ALT,CFG,TERRAIN_MSL,airDensity,isaTemperatureK} from './sim/index.js';
const rho=z=>airDensity(TERRAIN_MSL+z,CFG.rhoSL);
const heights={'single-engine airtanker':18,'large airtanker':53,'very large airtanker':122,
 "USFS 'completely dissipates'":305,'P-series ALT.drop':ALT.drop,
 [`sprayer lead, hull ${ALT.drop} m - 300 m lead`]:Math.max(0,ALT.drop-300),
 [`sprayer lead, hull ${ALT.drop} m - 400 m lead`]:Math.max(0,ALT.drop-400)};
const columns=Object.fromEntries(Object.entries(heights).map(([name,h])=>{
 const count=Math.max(1,Math.ceil(h)),dz=h/count;
 return [name,{heightM:h,releaseRho:rho(h),groundRho:rho(0),temperatureK:isaTemperatureK(TERRAIN_MSL+h),
  dz,samples:Array.from({length:count},(_,i)=>rho((i+.5)*dz))}];
}));
console.log(JSON.stringify({terrainMslM:TERRAIN_MSL,releaseAglM:ALT.drop,
 releaseMslM:TERRAIN_MSL+ALT.drop,rhoAtRelease:rho(ALT.drop),rhoAtGround:rho(0),
 temperatureAtReleaseK:isaTemperatureK(TERRAIN_MSL+ALT.drop),columns}));
"""
    return json.loads(subprocess.check_output(['node', '--input-type=module', '-e', script], cwd=ROOT, text=True))


def fall_record(diameter, reference_ms, column):
    seconds = math.fsum(column['dz'] / terminal_speed(diameter, reference_ms, rho)
                        for rho in column['samples'])
    return {'fallSeconds': round(seconds, 1), 'fallSecondsExact': seconds,
            'seaLevelTableFallSeconds': column['heightM'] / reference_ms,
            'terminalAtReleaseMs': terminal_speed(diameter, reference_ms, column['releaseRho']),
            'terminalAtGroundMs': terminal_speed(diameter, reference_ms, column['groundRho']),
            'driftM': {f'{w} m/s': round(w * seconds) for w in DRIFT_WINDS_MS},
            'driftExactM': {f'{w} m/s': w * seconds for w in DRIFT_WINDS_MS}}


def table(head, rows):
    return '| ' + ' | '.join(head) + ' |\n|' + '|'.join('---' for _ in head) + '|\n' + ''.join(
        '| ' + ' | '.join(map(str, row)) + ' |\n' for row in rows)


def weather_prose(out):
    a = out['atmosphere']; fall = out['fall']['P-series ALT.drop']; ref = out['references']
    source = next(s for s in json.loads((ROOT/'research/sources.json').read_text())['sources']
                  if s['id'] == 'ghiggi-2026-disdrodb')
    link = f"[Ghiggi et al.]({source['url']})"
    release = (f"The model release is {a['releaseAglM']:g} m above terrain at "
               f"{a['terrainMslM']:g} m MSL, hence {a['releaseMslM']:g} m MSL; "
               f"its reference-atmosphere density is {a['rhoAtRelease']:.6f} kg/m³. "
               'These are model inputs, not sampled fire weather.\n')
    two = fall['2.0 mm']
    reference = (f"For 2 mm drops, terminal speed is {TERMINAL_MS[2.0]:.1f} m/s in the sea-level reference table; "
                 f"at the model release it is {two['terminalAtReleaseMs']:.3f} m/s.\n\n"
                 'The retained Gunn–Kinzer table describes free drops in sea-level reference air, '
                 'rather than a density-independent property of water. Drops near and above '
                 f"{MAX_STABLE_DROP_MM:g} mm can break up. The density adjustment in {link}, "
                 f"{source['locator']}, is applied to that table through the model's dry standard-atmosphere column.\n\n")
    reference += table(['Diameter mm','Sea-level reference m/s','At release m/s','At ground m/s','Fall time s'],
                       [[f'{d:g}', f'{v:.1f}', f"{fall[f'{d} mm']['terminalAtReleaseMs']:.3f}",
                         f"{fall[f'{d} mm']['terminalAtGroundMs']:.3f}", f"{fall[f'{d} mm']['fallSecondsExact']:.3f}"]
                        for d,v in TERMINAL_MS.items()])
    reference += ('\nThis empirical correction holds diameter fixed and integrates inverse terminal speed '
                  'down to the ground. It does not solve break-up, evaporation, entrainment, initial '
                  'acceleration, humidity or a separate viscosity correction. No deposition or flight envelope follows.\n')
    small = fall['0.5 mm']; large = fall['5.0 mm']; wind = 10
    smear = (f"**The pattern smears, and the smear is worse than the drift.** A stipulated uniform "
             f"{wind:g} m/s wind translates the pattern, while the spread of fall times stretches it. "
             f"At the model release height, {min(TERMINAL_MS):g} mm drops fall for {small['fallSecondsExact']:.3f} s "
             f"and {max(TERMINAL_MS):g} mm drops for {large['fallSecondsExact']:.3f} s. The resulting "
             f"along-wind spread is {wind*(small['fallSecondsExact']-large['fallSecondsExact']):.3f} m, "
             f"against the {out['classes']['P100']['runKm']:g} km planned release run. "
             'This is a fixed-diameter, no-updraft sensitivity, not a ground pattern.\n\n'
             '**The mean drift is also conditional:**\n\n')
    smear += table(['Release example / height AGL m','Fall time, 2 mm s']+[f'Drift at {w} m/s, m' for w in DRIFT_WINDS_MS],
                   [[name+f" / {h:g}", f"{out['fall'][name]['2.0 mm']['fallSecondsExact']:.3f}"]+
                    [str(out['fall'][name]['2.0 mm']['driftM'][f'{w} m/s']) for w in DRIFT_WINDS_MS]
                    for name,h in ref['dropHeightsM'].items()])
    smear += ('\nEach wind is a stipulated uniform horizontal input; the reference jettison heights '
              'are comparisons, and every row uses the same model terrain and atmospheric column.\n')
    updraft = ('**Free drops descend only where their downward speed relative to the air exceeds '
               'the local upward air motion.** The following updrafts are stipulated screens, '
               'not observed weather or operating limits. Diameter is held fixed.\n\n')
    updraft += table(['Stipulated case','Updraft m/s','Diameters descending throughout the reference column, mm'],
                     [[k, f"{r['updraftMs']:g}", ', '.join(f'{d:g}' for d in r['dropsThatStillDescendMm'])
                       if isinstance(r['dropsThatStillDescendMm'],list) else 'none in reference air']
                      for k,r in out['updraftVerdict'].items()])
    warm = out['warmSensitivity']
    updraft += (f"\nA stipulated {warm['deltaK']:g} K warming at unchanged pressure raises the "
                f"{max(TERMINAL_MS):g} mm release speed from {large['terminalAtReleaseMs']:.3f} "
                f"to {warm['fiveMmAtReleaseMs']:.3f} m/s, near the "
                f"{UPDRAFT_MS['active flank']:g} m/s screen. This is a threshold case: "
                'reference-speed precision and empirical/model uncertainty do not establish a robust '
                'crossing, and release-level speed does not establish descent through the full column. '
                'No quantitative confidence interval is supplied by this calculation.\n')
    return {'release-air':release, 'drop-reference':reference, 'drop-drift':smear, 'drop-updraft':updraft}


def render_weather(out):
    text = (ROOT/'research/analysis/delivery.md').read_text()
    for key,body in weather_prose(out).items():
        start=f'<!-- logistics:{key}:start -->'; end=f'<!-- logistics:{key}:end -->'
        if text.count(start)!=1 or text.count(end)!=1:
            raise ValueError(f'delivery.md: missing unique {key} region')
        left,rest=text.split(start); _,right=rest.split(end)
        text=left+start+'\n'+body+end+right
    return text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="OUT")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--emit", action="store_true")
    args = ap.parse_args()
    fig = json.loads(FIGURES.read_text())

    air = model_air()
    heights = {name: c['heightM'] for name,c in air['columns'].items()}
    out = {"generated": {"by": "research/analysis/delivery.py", "figures": fig["generated"]},
           "fall": {}, "classes": {}, "atmosphere": {k:v for k,v in air.items() if k != 'columns'},
           "references": {"dropHeightsM": heights, "updraftMs": UPDRAFT_MS,
                          "maxStableDropMm": MAX_STABLE_DROP_MM, "terminalMs": TERMINAL_MS,
                          "densityCorrection": {"rho0KgM3": CORRECTION_RHO0,
                              "source": "ghiggi-2026-disdrodb", "exponentIntercept": .375,
                              "exponentPerMm": .025}}}
    for name,column in air['columns'].items():
        out['fall'][name] = {f'{d} mm': fall_record(d, v, column) for d,v in TERMINAL_MS.items()}
    out['updraftVerdict'] = {
        name: {'updraftMs': u,
               'dropsThatStillDescendMm': [d for d in TERMINAL_MS
                    if min(out['fall']['P-series ALT.drop'][f'{d} mm']['terminalAtReleaseMs'],
                           out['fall']['P-series ALT.drop'][f'{d} mm']['terminalAtGroundMs']) > u] or 'none',
               'uncertainty': 'Threshold screens only; empirical and atmosphere uncertainty is not quantified. A warm release near the threshold establishes no robust full-column descent.'}
        for name,u in UPDRAFT_MS.items()}
    warm_rho = air['rhoAtRelease'] * air['temperatureAtReleaseK'] / (air['temperatureAtReleaseK'] + WARM_SENSITIVITY_K)
    out['warmSensitivity'] = {'kind': 'stipulated fixed-pressure sensitivity', 'deltaK': WARM_SENSITIVITY_K,
                             'rhoAtRelease': warm_rho,
                             'fiveMmAtReleaseMs': terminal_speed(5.0, TERMINAL_MS[5.0], warm_rho),
                             'verdict': 'near threshold; no robust full-column descent established'}

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
    # convert the fleet's day into geometric line kilometres at a coverage level, and put it
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
    release = json.loads(subprocess.check_output(
        ["node", "tools/gen_release_states.mjs", "--record", "--release-only"], cwd=ROOT, text=True))["classes"]
    for cid, r in release.items():
        if r["state"] != "ready":
            out["classes"][cid]["ownUpwash"] = {"state": r["state"], "basis": r["reason"]}
            continue
        rows = {label: {
            "heldT": round(state["heldT"], 1),
            "altitudeAglM": state["altitudeAglM"],
            "densityKgM3": state["densityKgM3"],
            "waterAboardT": state["waterAboardT"],
            "inducedUpwashAtDiscMs": round(state["inducedUpwashAtDiscMs"], 1),
            "wakeMs": round(state["wakeMs"], 1),
            "airMassFlowKgS": round(state["airMassFlowKgS"]),
        } for label, state in r["states"].items()}
        rows.update(state="ready", basis=r["basis"], acceptedPlan=r["plan"],
                    inflowBelowHullMs={z: round(v, 2) for z,v in r["inflowBelowHullMs"].items()},
                    waterReleaseKgS=r["waterBenchmarkKgS"], waterBenchmarkBasis=r["benchmarkBasis"],
                    acceptedMeanWaterReleaseKgS=r["acceptedMeanWaterReleaseKgS"],
                    airToWaterMassRatio=round(r["airToWaterBenchmarkRatio"], 1))
        out["classes"][cid]["ownUpwash"] = rows

    encoded = json.dumps(out, indent=1)
    fresh_note = render_weather(out)
    if args.emit:
        print(json.dumps({'research/analysis/delivery.md': fresh_note}))
        return
    if args.check:
        stale = []
        if (ROOT/'research/analysis/delivery.json').read_text() != encoded:
            stale.append('delivery.json')
        if (ROOT/'research/analysis/delivery.md').read_text() != fresh_note:
            stale.append('delivery.md weather regions')
        if stale:
            raise SystemExit('delivery weather RED: ' + ', '.join(stale))
        print('delivery weather: record and four regions match model atmosphere')
        return
    if args.json:
        output = pathlib.Path(args.json)
        output.write_text(encoded)
        if output.resolve() == (ROOT/'research/analysis/delivery.json').resolve():
            (ROOT/'research/analysis/delivery.md').write_text(fresh_note)

    print("\nFALL TIME AND DRIFT (2 mm drops, the modal size that survives)")
    print(f"{'release height':<32}{'fall s':>8}{'drift @3':>10}{'@5':>8}{'@10':>8}{'@15':>8}")
    for k, h in heights.items():
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
