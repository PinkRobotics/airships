#!/usr/bin/env python3
"""MAINLINE-059: CARD.md, RESULTS.json, NFI.json and INPUTS.json from WATER.json, RETAIN.json, PONDS.json, DRY.json and
CAP.json."""
import datetime
import hashlib
import json
import math
import os
import re

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def acct(lead, R, fin, w="ISA"):
    return next(x for x in W["account"] if x["lead"] == lead and x["R_m"] == R and x["finish"] == fin and x["weather"] == w)


def cap(R, w="ISA", water=.1):
    return next(x for x in CP["rows"] if x["R_m"] == R and x["weather"] == w and abs(x["external_water"] - water) < 1e-9)


def wait(lead, fin, R, cond):
    return next(x for x in W["waits"] if x["lead"] == lead and x["finish"] == fin and x["R_m"] == R and x["condition"] == cond)


def meth(R, name):
    return next(x for x in W["methods"] if x["R_m"] == R and x["method"].startswith(name))


def prof(kind, fin, R, extra):
    key = f"{fin}|R{R}|{extra}"
    p = RT[kind][key]["profile_deg_kg_m2"]
    return {float(k): v for k, v in p.items()}


def at(p, deg):
    k = min(p, key=lambda x: abs(x - deg))
    return p[k]


def main():
    s = W["sources"]
    up = W["rain_upper_factor"]
    a10 = 4 * math.pi * 100
    p2 = acct("P2", 10, "MLCCAg")
    p3 = acct("P3", 10, "paint_040")
    p3f = acct("P3", 10, "hydrophobic_FEP")
    pr = {R: PD["radii"][str(R)] for R in (10, 12, 15, 20, 30)}
    c10 = cap(10)
    mm = {R: cap(R, "ISA", 1.0) for R in (10, 12, 15, 20, 30)}
    fins = ["MLCCAg", "paint_040", "hydrophobic_FEP", "slippery_silicone", "superhydrophobic"]
    rain_lo = min(acct("P2", 10, f)["rain_10min_kg"] for f in fins) / a10
    rain_hi = max(acct("P2", 10, f)["rain_10min_kg"] for f in fins) / a10
    dew_lo = min(acct("P2", 10, f)["dew_reference_kg"] for f in fins) / a10
    dew_hi = max(acct("P2", 10, f)["dew_saturated_kg"] for f in fins) / a10
    wm, wd, wo = wait("P2", "MLCCAg", 10, "midday_fair"), wait("P2", "MLCCAg", 10, "morning_fair"), wait("P2", "MLCCAg", 10, "overcast_day")
    w3 = wait("P3", "paint_040", 10, "midday_fair")
    tc = meth(10, "superhydrophobic topcoat")
    ht = meth(10, "onboard heater film")
    gh = meth(10, "ground heating")
    sh = meth(10, "shelter")
    cv = meth(10, "ground-supported cover")
    ak = meth(10, "air knives")
    tilt = meth(10, "P3: orient")
    p3_bayup = p3["rain_10min_kg"] + pr[10]["pond_face_up_kg"]
    L = []
    a = L.append
    a("# MAINLINE-059: the water on the hull. ESTIMATE")
    a("")
    a(f"Unit vacuum-mainline059-retained-water-1020. Order {ORDER}. Status ESTIMATE. Values are QUESTIONABLE, and "
      "PROJECTION where named. Nothing here is a certification. Started 06:30:34 PDT when the order was read; the end time "
      "is in RESULTS.json. Times are measurements, not limits.")
    a("")
    a("## The answer")
    a("")
    a("**What water each lead should carry.**")
    a(f"- **P2 (smooth beryllium sandwich): keep 0.1 kg/m2.** After rain and 10 minutes of drainage the hull keeps "
      f"{rain_lo:.3f}-{rain_hi:.3f} kg/m2, depending on finish ({rain_lo * up:.3f}-{rain_hi * up:.3f} on the upper rain "
      f"reading). After a dew night it keeps {dew_lo:.3f}-{dew_hi:.3f} kg/m2. All of it fits inside 0.1. At R 10 ISA, P2's "
      f"cure-included named endpoint carries {c10['water_capacity_named_kg_m2']:.4f} kg/m2 in all: "
      f"{', '.join(f'R {R} {cap(R)['water_capacity_named_kg_m2']:.3f}' for R in (12, 15, 20, 30))}.")
    a(f"- **P2 at 1 mm:** it floats only at R 30 ISA, on {' + '.join(mm[30]['least_axes'])} (usage "
      f"{mm[30]['least_usage']:.3f}, +{mm[30]['endpoint_named_kg'] / 1000:.2f} t). R 10 to 20 sink.")
    a(f"- **P3 (frame and film): 0.1 kg/m2 only if its ponds are emptied.** Under vacuum each film bay is a dish "
      f"(024's sag: a {pr[10]['crown_m'] * 100:.1f} cm crown on a {pr[10]['s_m']:.2f} m bay at R 10), so the top bays pond "
      "rain.")
    a(f"  - **Pond mass at R 10:** {pr[10]['pond_random_top']['random_mean']:.0f} kg on average over frame orientations. "
      f"It ranges {pr[10]['pond_random_top']['random_min']:.0f}-{pr[10]['pond_face_up_kg']:.0f} kg: "
      f"{pr[10]['pond_vertex_up_kg']:.0f} kg with a node on top, {pr[10]['pond_face_up_kg']:.0f} kg with a bay on top. "
      f"It scales as R cubed: {pr[30]['pond_random_top']['random_mean']:.0f} kg on average at R 30.")
    a(f"  - **R 10 ISA:** P3 carries {p3['capacity_kg']:.0f} kg of water in all ({p3['capacity_kg_m2']:.4f} kg/m2). With a "
      f"bay on top, film plus pond is {p3_bayup:.0f} kg, so it sinks; with a node on top it floats.")
    a(f"  - **Waiting does not empty ponds:** {w3['pond_evaporation_h_node_up'][0]:.0f}-{w3['pond_evaporation_h_bay_up'][1]:.0f} "
      "hours of fair midday sun at R 10.")
    a("")
    a("**The cheapest way to hold it there.**")
    a(f"- **P2: wait.** It drains in about 10 minutes, then dries in {wm['dry_fully_h_rain_10min_kg'][0]:.1f}-"
      f"{wm['dry_fully_h_rain_10min_kg'][1]:.1f} h in fair midday sun ({wd['dry_fully_h_rain_10min_kg'][0]:.1f}-"
      f"{wd['dry_fully_h_rain_10min_kg'][1]:.1f} h on a fair morning, {wo['dry_fully_h_rain_10min_kg'][0]:.1f}-"
      f"{wo['dry_fully_h_rain_10min_kg'][1]:.1f} h overcast). It needs no hardware and no mass. Even undried, the retained "
      "water fits inside the allowance.")
    a(f"  - A superhydrophobic topcoat adds {tc['flying_mass_kg'][0]:.0f}-{tc['flying_mass_kg'][1]:.0f} kg at R 10 to save "
      f"{tc['water_saved_kg']['dew_saturated']:.0f}-{tc['water_saved_kg']['rain']:.0f} kg of water, and its optics over the "
      "mirror are unqualified.")
    a(f"  - Onboard heater film weighs {ht['flying_mass_kg']:.0f} kg at R 10.")
    a("- **P3: design the frame's orientation, then tilt after rain.**")
    a(f"  - Put a node, or the best placement, on top: {tilt['ponds_kg']['random_min']:.0f}-"
      f"{tilt['ponds_kg']['node_up']:.0f} kg of pond instead of {tilt['ponds_kg']['bay_up']:.0f} kg at R 10, at no mass.")
    a("  - Tip the moored hull past about 14 deg to spill the ponds. That needs ground handling (PROJECTION, not costed).")
    a(f"  - A night shelter keeps both rain and dew off at no flying mass. At R 10 it costs about {sh['cost_rub'] / 1e6:.1f}M "
      "RUB by the sourced inflatable-hangar price per floor area; height is not addressed.")
    a("")
    a("**The measurement that would ground it: weigh real panels.**")
    a("- **P2:** a full-scale curved panel (2 x 2 m at R 10 curvature) with the actual finish, on a tilting load-cell rig, "
      "after sprayed rain and after a dew night, at 0-90 deg and inverted.")
    a("- **P3:** a full-size sagged film bay (2.3 m) with its members, at 0-15 deg tilt, measuring pond mass and spill angle.")
    a("- **Drying:** an outdoor drying-rate run under named sun and wind.")
    a("")
    a("The retention model rests on one measured condensation plate and one modelled rain plate. The panel weighings "
      "replace both.")
    a("")
    # ---------------------------------------------------------------- 1
    a("## 1. What stays on")
    a("")
    a("**How retention is modelled.** A drop stays where the Furmidge pinning force exceeds its weight along the surface; the "
      "contact angles set the critical drop size.")
    a(f"- **Calibration:** the retained mass per area is calibrated so this seat's Furmidge size on a measured vertical "
      f"acrylic plate (advancing {s['acrylic_thA']:.0f}, receding {s['acrylic_thR']:.0f} deg) gives its measured "
      f"{s['acrylic_kg_m2'] * 1000:.0f} g/m2 after condensation.")
    a(f"- **Rain:** a modelled 0.3 m PVC rain-gauge plate holds {s['pvc_rain_mm']:.2f} mm per spell, so rain is also given "
      f"x{up:.2f} as an upper reading.")
    a("- **Hydrophilic finishes** also keep a draining film: Jeffreys' after rain, Nusselt's under dew.")
    a(f"- **Near the top** every finish is capped at the {s['leaf_horizontal_mm']:.1f} mm a horizontal leaf holds.")
    a("- **Below 135 deg** rain is not credited.")
    a("")
    a("Finish contact angles, advancing and receding:")
    a("- **048's mirror:** 30/10 deg (ITO 25 deg static, sourced).")
    a("- **040's paint:** 40/15 deg (unsourced).")
    a("- **FEP/PTFE:** 115/105 deg.")
    a("- **Slippery silicone:** 107.5/102.5 deg.")
    a("- **NeverWet class:** 164/159 deg.")
    a("")
    a("Retained water at R 10 by position, kg/m2 (polar angle from the top; 90 deg is the equator):")
    a("")
    angs = (0.25, 5.25, 10.25, 30.25, 45.25, 60.25, 90.25, 120.25, 135.25, 150.25)
    a("| Finish | Case | " + " | ".join(f"{x:.0f} deg" for x in angs) + " | Hull total, kg |")
    a("|---|---|" + "---|" * len(angs) + "---|")
    for f in fins:
        pr_ = prof("rain", f, 10, "wait600s")
        a(f"| {NAMES[f]} | rain, 10 min | " + " | ".join(f"{at(pr_, x):.3f}" for x in angs) + f" | {RT['rain'][f'{f}|R10|wait600s']['total_kg']:.0f} |")
        pd_ = prof("dew", f, 10, "night_050_saturated")
        a(f"| | dew, saturated night | " + " | ".join(f"{at(pd_, x):.3f}" for x in angs) + f" | {RT['dew'][f'{f}|R10|night_050_saturated']['retained_kg']:.0f} |")
    a("")
    a("**Dew.** The deposit is this seat's night energy balance on 050's nights. The excess over what the finish holds runs "
      "off. 050's reference night (clear, 0.2 m/s) and its saturated-clear night are used.")
    a(f"- **Checks against 050:** the balance gives {DR['results']['R10|sphere040|MLCCAg|night_050_reference']['mean_rate_kg_m2_h'] * -12:.3f} "
      f"kg/m2 net for the reference night against 050's 0.090, and "
      f"{DR['results']['R10|sphere040|MLCCAg|night_050_saturated']['mean_rate_kg_m2_h'] * -12:.3f} for the saturated "
      "night against 0.243.")
    a(f"- **Checks against sources:** passive condensers yield {s['grass_dew_mm']:.2f} mm a night on grassland, up to "
      f"{s['dew_jerusalem_L']:.1f} L/m2 at the observed high and {s['dew_max_L']:.1f} L/m2 at the physical limit. Dew stops "
      f"above about {s['dew_wind_ms']:.0f} m/s of wind.")
    a("")
    a("**P3's ponds.** 024 charges the film sag as a cap through each bay's inradius: crown 0.0426 s and mean 0.5036 crown. "
      "052's 73.10 kg of sag lift at R 10, scaling as R cubed, fixes the bay side s.")
    a("- **Dish shape (PROJECTION):** a quadratic dish with that crown and mean. A bay tilted by its polar angle holds water "
      "up to its lowest member.")
    a("- **Placement:** the totals sample 200 placements of the top point in the bay pattern.")
    a("")
    a("| R, m | Bay side, m | Crown, cm | Level bay holds, kg | Mean, kg | 5-95%, kg | Node on top, kg | Bay on top, kg |")
    a("|---|---|---|---|---|---|---|---|")
    for R in (10, 12, 15, 20, 30):
        p = pr[R]
        a(f"| {R} | {p['s_m']:.2f} | {p['crown_m'] * 100:.1f} | {p['level_bay_capacity_kg']:.0f} | "
          f"{p['pond_random_top']['random_mean']:.0f} | {p['pond_random_top']['random_p05']:.0f}-{p['pond_random_top']['random_p95']:.0f} | "
          f"{p['pond_vertex_up_kg']:.0f} | {p['pond_face_up_kg']:.0f} |")
    a("")
    a("A bay holds water only within about 9 deg of the top. A level bay holds the most, and none ponds beyond about 14 deg "
      "of tilt.")
    a("")
    # ---------------------------------------------------------------- 2
    a("## 2. How fast it goes")
    a("")
    a("**The drying model.** Each element of the hull balances absorbed sun, long-wave exchange (040's sky and ground "
      "split) and convection against latent heat (2.45 MJ/kg, FAO-56).")
    a("- **Transfer:** mass transfer follows heat transfer by the Chilton-Colburn analogy.")
    a("- **Convection bracket:** the low reading is 040's own sphere correlation; the high is a wind flat-plate "
      "h = 5.7 + 3.8 U.")
    a(f"- **Check:** a grass-albedo surface at FAO-56's hourly example reaches "
      f"{max(DR['results']['R10|flatplate|grass_check|fao_peak_check']['rate_by_polar_deg'].values()):.2f} kg/m2/h at its "
      f"sun-facing element against FAO's {s['fao_ETo_mm_h']:.2f} mm/h.")
    a("- **Mirror finishes** absorb only 9-20% of the sun, so they dry slowly.")
    a("")
    a("| Lead, finish | R, m | Condition | Hull evaporation, kg/h | Rain residue dries in, h | Saturated dew dries in, h |")
    a("|---|---|---|---|---|---|")
    for lead, f in (("P2", "MLCCAg"), ("P2", "paint_040"), ("P3", "paint_040")):
        for R in (10, 30):
            for cond, lab in (("morning_fair", "fair morning, 15 C, 2 m/s, 600 W/m2"), ("midday_fair", "fair midday, 20 C, 3 m/s, 850 W/m2"),
                              ("overcast_day", "overcast, 12 C, RH 90%, 2 m/s")):
                x = wait(lead, f, R, cond)
                a(f"| {lead}, {NAMES[f]} | {R} | {lab} | {x['hull_rate_kg_h'][0]:.0f}-{x['hull_rate_kg_h'][1]:.0f} | "
                  f"{x['dry_fully_h_rain_10min_kg'][0]:.1f}-{x['dry_fully_h_rain_10min_kg'][1]:.1f} | "
                  f"{x['dry_fully_h_dew_saturated_kg'][0]:.1f}-{x['dry_fully_h_dew_saturated_kg'][1]:.1f} |")
    a("")
    a(f"Sourced dew lasts {s['dew_duration_h']:.1f} h a night on grassland and is gone about {s['dew_gone_h']:.0f} h after "
      "sunrise on shrubs, inside the fair-morning range.")
    a("")
    a(f"P3's ponds evaporate only from their free surface ({pr[10]['pond_vertex_up_surface_m2']:.1f}-"
      f"{pr[10]['pond_face_up_surface_m2']:.1f} m2 at R 10). Emptying them by evaporation takes "
      f"{w3['pond_evaporation_h_node_up'][0]:.0f}-{w3['pond_evaporation_h_node_up'][1]:.0f} h (node on top) or "
      f"{w3['pond_evaporation_h_bay_up'][0]:.0f}-{w3['pond_evaporation_h_bay_up'][1]:.0f} h (bay on top) of fair midday sun.")
    a("")
    # ---------------------------------------------------------------- 3
    a("## 3. The ways to shed it")
    a("")
    a("| Way | Flying mass at R 10 / R 30 | Energy | Durability | Cost | What it removes |")
    a("|---|---|---|---|---|---|")
    tc30, gh30, sh30, cv30 = meth(30, "superhydrophobic topcoat"), meth(30, "ground heating"), meth(30, "shelter"), meth(30, "ground-supported cover")
    a(f"| Waiting (sun and wind) | 0 | none | n/a | availability: hours (section 2) | films and drops; not P3's ponds |")
    a(f"| Superhydrophobic topcoat | {tc['flying_mass_kg'][0]:.0f}-{tc['flying_mass_kg'][1]:.0f} / {tc30['flying_mass_kg'][0]:.0f}-{tc30['flying_mass_kg'][1]:.0f} kg | none | "
      f"about {s['ued_life_yr']:.0f} year outdoors; {s['ued_taber']:.0f} Taber cycles | about ${tc['cost_usd_per_application']:,.0f} / "
      f"${tc30['cost_usd_per_application']:,.0f} per coat | P2 rain {tc['water_saved_kg']['rain']:.0f} kg less at R 10; optics: \"{tc['optics'][:60]}\" |")
    a(f"| Onboard heater film | {ht['flying_mass_kg']:.0f} / {meth(30, 'onboard heater film')['flying_mass_kg']:.0f} kg | ground or battery | heater life | not costed | excluded: heavier than either margin |")
    a(f"| Ground heating | 0 | dew prevention {gh['dew_prevention_kWh_per_night']:.0f} / {gh30['dew_prevention_kWh_per_night']:.0f} kWh a night "
      f"(050); evaporating P2's rain residue {gh['evaporate_P2_rain_kWh_ideal']:.0f} kWh ideal | equipment | energy only, equipment not costed | dew; residues |")
    a(f"| Night shelter or hangar | 0 | none | structure | about {sh['cost_rub'] / 1e6:.1f}M / {sh30['cost_rub'] / 1e6:.0f}M RUB (floor-area scaling) | rain and dew while inside |")
    a(f"| Ground-supported cover | 0 ({cv['fabric_kg'][0]:.0f}-{cv['fabric_kg'][1]:.0f} kg of fabric handled at R 10) | none | fabric | fabric price not sourced | dew; rain if it sheds |")
    a(f"| Air knives on a gantry | 0 | {ak['energy_kWh_per_pass'][0]:.0f}-{ak['energy_kWh_per_pass'][1]:.0f} kWh a pass | equipment | gantry not costed | drops; residue not sourced |")
    a(f"| P3: orient the frame, tilt after rain | 0 | handling | n/a | handling hardware not costed | ponds ({tilt['ponds_kg']['bay_up']:.0f} kg to {tilt['ponds_kg']['random_min']:.0f}-{tilt['ponds_kg']['node_up']:.0f} kg; all above 14 deg) |")
    a("")
    a("**Notes:**")
    a(f"- **Anti-icing references:** {s['antiice_SH_kW_m2']:.1f} kW/m2 with a superhydrophobic coat and "
      f"{s['antiice_enamel_kW_m2']:.0f} kW/m2 on enamel. Ice protection runs at kilowatts per square metre, about two "
      "hundred times the 21 W/m2 that dew prevention needs (050).")
    a(f"- **Historic hangars:** ${s['airdock_usd1929'] / 1e6:.1f}M (Goodyear Airdock, 1929); a ${s['cargolifter_musd']:.0f}M estimate "
      f"(CargoLifter, 1998); {s['lindstrand_t']:.0f} t of fabric in an inflatable airship hangar.")
    a(f"- **Covers:** fabrics are {s['silnylon_gsm']:.0f}-{s['linen_gsm']:.0f} g/m2. A cover over 110% of the hull would weigh "
      f"{cv['fabric_kg'][0]:.0f}-{cv['fabric_kg'][1]:.0f} kg at R 10, so it can only stay on the ground.")
    a("")
    # ---------------------------------------------------------------- 4
    a("## 4. The leads' water account")
    a("")
    a("Capacity is the total exterior water at which the named endpoint's payload reaches zero.")
    a("- **P2:** this seat's model on 048's account with cure compression.")
    a("- **P3:** 0.1 kg/m2 plus 052's ground-service endpoint over the hull area.")
    a("")
    a("Retained water is after rain with 10 minutes of drainage (base / upper) and after the reference and saturated dew "
      "nights. P3 adds its ponds.")
    a("")
    a("| Lead | R, m | Weather | Finish | Capacity, kg (kg/m2) | Allowance 0.1 kg/m2, kg | Rain, kg | Dew, kg | Ponds (min / mean / node / bay on top), kg |")
    a("|---|---|---|---|---|---|---|---|---|")
    for x in W["account"]:
        if x["finish"] not in ("MLCCAg", "paint_040") or (x["lead"] == "P2" and x["finish"] != "MLCCAg"):
            continue
        pk = x.get("ponds_kg")
        ptxt = "-" if pk is None else f"{pk['min']:.0f} / {pk['mean']:.0f} / {pk['node_up']:.0f} / {pk['bay_up']:.0f}"
        a(f"| {x['lead']} | {x['R_m']} | {x['weather']} | {NAMES[x['finish']]} | {x['capacity_kg']:.0f} ({x['capacity_kg_m2']:.4f}) | "
          f"{x['allowance_kg']:.0f} | {x['rain_10min_kg']:.0f} / {x['rain_10min_upper_kg']:.0f} | {x['dew_reference_kg']:.0f} / "
          f"{x['dew_saturated_kg']:.0f} | {ptxt} |")
    a("")
    a("A capacity below 0.1 kg/m2 means the lead cannot carry even the allowance. That is so for P2 and P3 at R 10 in "
      "optimistic weather.")
    a("")
    a("**P2's least set as exterior water rises** (ISA, cure compression included):")
    for R in (10, 12, 15, 20, 30):
        cells = []
        for x in (.1, .15, .2, .3, .5, 1.0):
            r = cap(R, "ISA", x)
            ax = None if r["least_axes"] is None else ["face tuple" if q == "face_compression_and_E" else q for q in r["least_axes"]]
            cells.append(f"{x:g} kg/m2: " + ("none" if ax is None else f"{' + '.join(ax)} {r['least_usage']:.3f}"))
        a(f"- **R {R}:** " + "; ".join(cells) + ".")
    a("")
    # ---------------------------------------------------------------- method
    a("## Method and checks")
    a("")
    a("This seat's own code:")
    a("- **ponds59.py:** P3 bay ponds.")
    a("- **dry59.py:** the evaporation and dew energy balance.")
    a("- **retain59.py:** films and drops by finish and position.")
    a("- **cap59.py:** P2's capacity with MAINLINE-049's model49/thermal49, which reproduce 048 bit for bit. It ran "
      "through simjob.")
    a("- **water59.py, src59.py and card59.py.**")
    a("")
    a("Sourced values are drawn from the four sourcing files by property and product, and asserted.")
    a("")
    a("**Checks:**")
    a("- **Pond placement:** the pond random-placement mean equals the orientation-integral value at every radius.")
    a("- **Sag scaling:** 052's sag debit scales exactly as R cubed (73.10, 126.32 and 246.71 kg at R 10, 12 and 15).")
    a("- **Dew:** the energy balance reproduces 050's saturated dew to 2%, and its reference night is 25% low.")
    a("- **FAO-56:** the drying bracket contains FAO-56's hourly rate.")
    a("- **Capacity:** P2's R 10 capacity reproduces the 030d/048 cure-included +118.695 kg named endpoint.")
    a("")
    a("## Then")
    a("")
    a("Stop and file. The robotics seat sends the next job. NFI.json carries the open rows.")
    text = "\n".join(L) + "\n"
    with open(os.path.join(HERE, "CARD.md.tmp"), "w") as fh:
        fh.write(text)
    os.replace(os.path.join(HERE, "CARD.md.tmp"), os.path.join(HERE, "CARD.md"))

    now = datetime.datetime.now().astimezone().isoformat()
    results = {"schema": 1, "card": "MAINLINE-059", "unit": "vacuum-mainline059-retained-water-1020", "order": ORDER,
               "status": "ESTIMATE", "tag": "QUESTIONABLE / PROJECTION", "certification": "none",
               "job_started_at": JOB_STARTED, "job_ended_at": now, "times_are": "measurements only",
               "answer": {"P2_design_water_kg_m2": 0.1, "P2_retained_rain_kg_m2": [rain_lo, rain_hi], "P2_retained_rain_upper_kg_m2": [rain_lo * up, rain_hi * up],
                          "P2_retained_dew_kg_m2": [dew_lo, dew_hi], "P2_capacity_named_kg_m2": {R: cap(R)["water_capacity_named_kg_m2"] for R in (10, 12, 15, 20, 30)},
                          "P2_1mm": {R: {"axes": mm[R]["least_axes"], "usage": mm[R]["least_usage"], "named_kg": mm[R]["endpoint_named_kg"]} for R in mm},
                          "P3_capacity_kg_m2": {R: acct("P3", R, "paint_040")["capacity_kg_m2"] for R in (10, 12, 15, 20, 30)},
                          "P3_ponds_kg": {R: {"mean": pr[R]["pond_random_top"]["random_mean"], "min": pr[R]["pond_random_top"]["random_min"],
                                              "node_up": pr[R]["pond_vertex_up_kg"], "bay_up": pr[R]["pond_face_up_kg"]} for R in pr},
                          "P3_R10_bay_up_total_kg": p3_bayup, "cheapest": {"P2": "wait (drain 10 min; dry in sun)",
                                                                          "P3": "frame orientation (node or best placement on top), tilt past 14 deg after rain; shelter as the fallback"},
                          "measurement": "weigh a full-scale finished P2 panel and a full-size sagged P3 bay on a tilting load-cell rig after rain and dew; outdoor drying rate"},
               "water": W, "retain": RT, "ponds": {k: v for k, v in PD.items() if k != "basis"}, "dry_conditions": DR["conditions"],
               "capacity": CP}
    with open(os.path.join(HERE, "RESULTS.json.tmp"), "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "RESULTS.json.tmp"), os.path.join(HERE, "RESULTS.json"))
    items = [
        ("NFI-059-RETENTION-CALIBRATION", "PROJECTION", "Film and drop retention is calibrated on one measured condensation plate (acrylic, 54 g/m2) and one "
         "modelled rain plate (PVC, 0.08 mm, the upper reading), and transferred to each finish through Furmidge with assumed hysteresis.",
         "Weigh a full-scale curved panel with each finish after rain and dew at 0-90 deg and inverted."),
        ("NFI-059-PAINT", "QUESTIONABLE", "040's white silicate paint has no sourced wettability or water uptake; it is modelled as a hydrophilic oxide.",
         "Contact angles and uptake of the actual paint."),
        ("NFI-059-P3-PONDS", "PROJECTION", "P3's ponds use 024's sag crown and mean, 052's bay size through its sag debit, a quadratic dish and a "
         "planar bay pattern near the top. 052 does not fix the frame's orientation; the pond mass spans 5-171 kg at R 10 with it.",
         "A full-size sagged bay with members: pond mass against tilt, and the spill angle."),
        ("NFI-059-P3-FINISH", "QUESTIONABLE", "P3's OD4/white protection outer layer has no sourced wettability; paint-like and FEP-like bounds are used.",
         "Contact angles of the actual protection layer."),
        ("NFI-059-DRYING", "PROJECTION", "Drying is bracketed between 040's sphere correlation and a flat-plate wind correlation (a factor up to "
         "about 8); the inner face is taken as adiabatic; the low solar absorptance of the mirror finishes limits solar drying.",
         "An outdoor drying run on a finished panel under logged sun, wind, temperature and humidity."),
        ("NFI-059-DEW", "PROJECTION", "Dew is distributed by this seat's energy balance (050's saturated case within 2%, reference 25% low); "
         "frost and freezing of retained water are not modelled (no verified frost source).", "Night dew and frost weighing on a finished panel."),
        ("NFI-059-TOPCOAT", "QUESTIONABLE", "The superhydrophobic topcoat's dry areal mass assumes 1.0-1.5 g/cm3 on its 13-25 um film; it is "
         "'hazy translucent white' and unqualified over a silver mirror; it lasts about a year and 30 Taber cycles.",
         "Areal mass, optics and life of the coating on the finish."),
        ("NFI-059-SHELTER", "QUESTIONABLE", "Shelter cost scales one 30 x 15 m inflatable hangar price by floor area; height, wind and handling are "
         "not addressed; historic airship hangars are not comparable.", "A quotation for a shelter sized to the hull."),
        ("NFI-059-AIRKNIFE", "QUESTIONABLE", "Air-knife residual water and a gantry for a sphere are not sourced or costed.", "A blow-off test on a curved panel."),
        ("NFI-059-TILT", "PROJECTION", "Tipping a moored P3 sphere past 14 deg needs handling hardware that is not designed.", "A mooring and handling concept."),
        ("NFI-059-IN-FLIGHT", "QUESTIONABLE", "Rain met in flight adds water beyond the ground-retained film; not computed.", "A flight rain-exposure case."),
        ("NFI-059-WET-OPTICS", "QUESTIONABLE", "Retained water changes the finishes' absorptance and emittance (048's open item); dry optics are used.",
         "Wet optical measurements on each finish."),
    ]
    nfi = {"schema": 1, "card": "MAINLINE-059", "unit": "vacuum-mainline059-retained-water-1020", "tag": "QUESTIONABLE", "status": "OPEN",
           "items": [{"id": i, "tag": t, "claim": c, "needed_to_ground": n} for i, t, c, n in items]}
    with open(os.path.join(HERE, "NFI.json.tmp"), "w") as fh:
        json.dump(nfi, fh, indent=1)
    os.replace(os.path.join(HERE, "NFI.json.tmp"), os.path.join(HERE, "NFI.json"))

    def pin(p, role):
        data = open(p, "rb").read()
        return {"path": p, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "role": role}
    B = "unpublished-local-ref:792ada9d1fcd5e54"
    Q = "unpublished-local-ref:ab52dba26d6cc3a7"
    pins = [pin(f"{B}/CARD-059-RETAINED-WATER.md", "brief"), pin(f"{B}/COMMON.md", "brief"), pin(f"{Q}/{ORDER}.json", "order"),
            pin(W["p3_card"], "052 CARD.md (P3 endpoints)")]
    for rid in ("rpt-ref-2092a3e39c7141afde61", "rpt-ref-9a9a131b4ca724b68cc2",
                "rpt-1228-mainline050-flyable-weather-1020", "rpt-ref-d7b2450119f373b2d1db",
                "rpt-ref-2bb3c2b520a8e5f8c750", "rpt-ref-593068c3ed82fd458128"):
        pins.append(pin(f"{Q}/{rid}.json", "source report"))
    for n in ("retention", "dew", "drying", "shedding"):
        for e in ("json", "md"):
            pins.append(pin(f"{SRC}/{n}.{e}", "sourcing file"))
    M49 = "unpublished-local-ref:5eec519919d3414d"
    for n in ("model49.py", "thermal49.py"):
        pins.append(pin(f"{M49}/{n}", "own model (MAINLINE-049)"))
    for n in ("ponds59.py", "dry59.py", "retain59.py", "cap59.py", "water59.py", "src59.py", "card59.py", "simretry.sh",
              "PONDS.json", "DRY.json", "RETAIN.json", "CAP.json", "WATER.json"):
        pins.append(pin(os.path.join(HERE, n), "this card's own code or intermediate"))
    inputs = {"schema": 1, "card": "MAINLINE-059", "unit": "vacuum-mainline059-retained-water-1020", "pins": pins,
              "sources_used": W["sources_used"]}
    with open(os.path.join(HERE, "INPUTS.json.tmp"), "w") as fh:
        json.dump(inputs, fh, indent=1)
    os.replace(os.path.join(HERE, "INPUTS.json.tmp"), os.path.join(HERE, "INPUTS.json"))
    print(len(text), "bytes card;", len(items), "NFI;", len(pins), "pins")


if __name__ == "__main__":
    main()
