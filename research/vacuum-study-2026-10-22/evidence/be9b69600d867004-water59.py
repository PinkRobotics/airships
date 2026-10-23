#!/usr/bin/env python3
"""MAINLINE-059: the water account. Combines RETAIN.json (films and drops by finish and position), PONDS.json (P3's bay
ponds), DRY.json (evaporation and dew), CAP.json (P2's carrying capacity, this seat's model) and 052's P3 endpoints with
the sourced method data. Gives each lead's retained water after rain and dew, its carrying capacity, the wait to fly, and
the mass, energy, durability and cost of each way to shed water. Writes WATER.json."""
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import retain59 as RT  # noqa: E402
import src59 as S  # noqa: E402

RADII = (10, 12, 15, 20, 30)
Q052 = "evidence/3c66e9fa3523cc5a-report.json"
RAIN_UPPER = None          # set from the PVC rain-gauge estimate / the acrylic calibration (sourced)


def area(R):
    return 4 * math.pi * R * R


def p3_endpoints():
    """052's ground-service full endpoints (CARD.md table), kg."""
    card = next(a["path"] for a in json.load(open(Q052))["artifacts"] if a["path"].endswith("/CARD.md"))
    out = {}
    for line in open(card):
        m = re.match(r"\| (\d+) \| (ISA|optimistic|both) \| (-?[\d,]+\.\d+) \|", line)
        if m:
            out.setdefault(int(m.group(1)), {})[m.group(2)] = float(m.group(3).replace(",", ""))
    return out, card


def main():
    global RAIN_UPPER
    src = {}
    # retention and dew sources
    src["acrylic_kg_m2"] = S.val("acrylic", "retention", "retained_water", "steady-state retained condensed water per unit area", 54.0) / 1000
    src["acrylic_thA"] = S.val("acr_thA", "retention", "contact_angle", "static advancing water contact angle", 78.0, "acrylic")
    src["acrylic_thR"] = S.val("acr_thR", "retention", "contact_angle", "receding water contact angle", 48.0, "acrylic")
    S.val("acr_rc", "retention", "drop_retention", "theoretical critical drop radius", 1.8)
    src["pvc_rain_mm"] = S.val("pvc_rain", "retention", "retained_water", "adhered rain water on a 0.3 x 0.3 m PVC", 0.08)
    S.val("ito", "retention", "contact_angle", "water contact angle on ITO film on soda-lime glass", 25.0)
    S.val("ptfe", "retention", "contact_angle", "advancing water contact angle on native PTFE", 115.0)
    S.val("fep", "retention", "contact_angle", "water contact angle on FEP topcoat", 105.0)
    S.val("nw_a", "retention", "contact_angle", "advancing water contact angle on NeverWet", 164.0)
    S.val("nw_r", "retention", "contact_angle", "receding water contact angle on NeverWet", 159.0)
    S.val("sil_sl", "retention", "sliding_angle", "water sliding angle", 5.0)
    S.val("sil_ca", "retention", "contact_angle", "water contact angle (CA) with contact-angle hysteresis", 105.0)
    src["roof_flat_in"] = S.val("roof_flat", "retention", "retained_water", "typical depression (retention) loss, flat roofs", 0.1)
    src["roof_sloped_in"] = S.val("roof_sloped", "retention", "retained_water", "typical depression (retention) loss, sloped roofs", 0.05)
    src["pitched_roof_mm"] = S.val("roof_pitched", "retention", "retained_water", "initial loss (water held before runoff starts) on pitched roofs", 0.4)
    src["leaf_horizontal_mm"] = S.val("leaf", "dew", "dew_retention", "Maximum dew depth held on a horizontal leaf", 0.8)
    S.val("slide_1mm", "dew", "dew_runoff", "Drop size at which dew drops slide off", 1.0)
    src["grass_dew_mm"] = S.val("grass_dew", "dew", "dew_yield", "Mean dew yield on 9 US grassland sites", 0.14)
    src["dew_duration_h"] = S.val("dew_dur", "dew", "dew_duration", "Dew duration per night: grasslands", 3.4)
    src["dew_gone_h"] = S.val("dew_gone", "dew", "dew_duration", "Time for dew to disappear after sunrise", 4.0)
    src["dew_max_L"] = S.val("dew_max", "dew", "dew_physics", "Theoretical upper limit of dew yield", 800.0) / 1000
    src["dew_jerusalem_L"] = S.val("dew_jer", "dew", "dew_yield", "Highest dew collection amount known", 0.6)
    src["dew_wind_ms"] = S.val("dew_wind", "dew", "dew_physics", "Wind speed above which dew condensation stops", 3.0)
    # drying sources
    src["latent_MJ_kg"] = S.val("latent", "drying", "latent_heat", "latent heat of vaporization of water at 20 C", 2.45)
    src["fao_ETo_mm_h"] = S.val("eto", "drying", "potential_evaporation", "grass reference evapotranspiration, hourly", 0.63)
    S.note("paved", "drying", "drying_rate", "evaporation rate from moist paved surface")
    # shedding sources
    src["ued_m2_per_3p8L"] = S.val("ued_cov", "shedding", "coating_mass", "coverage of two-coat system per gallon", 23.0)
    src["ued_thickness"] = S.note("ued_dft", "shedding", "coating_mass", "dry film thickness of finished system")
    src["ued_price_usd_per_50gal"] = S.val("ued_price", "shedding", "coating_cost", "list price, bottom coat, 50 gallon drum", 7685.9)
    src["ued_life_yr"] = S.val("ued_life", "shedding", "coating_durability", "outdoor life before top-coat recoat", 1.0)
    src["ued_taber"] = S.val("ued_taber", "shedding", "coating_durability", "abrasion resistance, Taber cycles", 30.0)
    src["rainx_months"] = S.val("rainx", "shedding", "coating_durability", "application life", 3.0)
    src["ued_optics"] = S.note("ued_optics", "shedding", "coating_optics", "coating appearance / transparency")
    src["heater_g_cm2"] = S.val("minco", "shedding", "heater", "areal mass of polyimide (Kapton) etched-foil heater", 0.04)
    src["heater_max_W_cm2"] = S.val("freek", "shedding", "heater", "recommended maximum surface load", 0.8)
    src["antiice_SH_kW_m2"] = S.val("ai_sh", "shedding", "anti_icing_power", "superhydrophobic-coated airfoil", 4.5)
    src["antiice_enamel_kW_m2"] = S.val("ai_en", "shedding", "anti_icing_power", "uncoated hydrophilic ename", 25.0)
    src["hangar_rub"] = S.val("hangar", "shedding", "shelter_cost", "inflatable PVC pneumatic-frame hangar, 30 x 15 m", 3848256.0)
    src["airdock_usd1929"] = S.val("airdock", "shedding", "shelter_cost", "Goodyear Airdock", 2200000.0)
    src["cargolifter_musd"] = S.val("cargolifter", "shedding", "shelter_cost", "estimated cost of column-free airship hangar", 67.0, "CargoLifter")
    src["lindstrand_t"] = S.val("lindstrand", "shedding", "cover_fabric", "all-fabric inflatable airship hangar", 22.0)
    src["blower_kW"] = S.val("blower", "shedding", "air_knife", "regenerative blower motor sizes", 4.0)
    src["carwash_hp"] = S.val("carwash", "shedding", "air_knife", "car-wash dryer carousel motor power", 180.0)
    src["silnylon_gsm"] = S.val("silnylon", "shedding", "cover_fabric", "silicone/PU coated nylon ripstop", 42.0)
    src["linen_gsm"] = S.val("linen", "shedding", "cover_fabric", "airship outer-cover fabric (linen)", 90.0)

    RAIN_UPPER = src["pvc_rain_mm"] / src["acrylic_kg_m2"]           # 0.08 kg/m2 (PVC, rain) over 0.054 (acrylic, dew)
    ret = json.load(open(os.path.join(HERE, "RETAIN.json")))
    ponds = json.load(open(os.path.join(HERE, "PONDS.json")))
    dry = json.load(open(os.path.join(HERE, "DRY.json")))
    cap = json.load(open(os.path.join(HERE, "CAP.json")))
    p3ep, p3card = p3_endpoints()

    def p2cap(R, w="ISA"):
        x = next(r for r in cap["rows"] if r["R_m"] == R and r["weather"] == w and abs(r["external_water"] - .1) < 1e-9)
        return x["water_capacity_named_kg_m2"], x["endpoint_named_kg"]

    def p3cap(R, w="ISA"):
        p = p3ep[R][w]
        return .1 + p / area(R), p

    # P3's extra dew: the dew that falls on the pond bays (tilt below 14 deg) stays there whatever the drop capacity
    def p3_dew_extra(R, night, fin):
        phis, dep, kept = RT.dew_profile(fin, R, night)
        sel = phis <= math.radians(14)
        dphi = phis[1] - phis[0]
        return float(((dep - kept)[sel] * 2 * math.pi * R * R * np.sin(phis[sel]) * dphi).sum())

    leads = {"P2": {"finishes": ["MLCCAg", "paint_040", "hydrophobic_FEP", "slippery_silicone", "superhydrophobic"],
                    "primary": "MLCCAg"},
             "P3": {"finishes": ["paint_040", "hydrophobic_FEP"], "primary": "paint_040"}}
    acct = []
    for lead, L in leads.items():
        for R in RADII:
            A = area(R)
            for w in ("ISA", "optimistic"):
                capw, pay = (p2cap if lead == "P2" else p3cap)(R, w)
                for fin in L["finishes"]:
                    rain = ret["rain"][f"{fin}|R{R}|wait600s"]["total_kg"]
                    rain1h = ret["rain"][f"{fin}|R{R}|wait3600s"]["total_kg"]
                    dref = ret["dew"][f"{fin}|R{R}|night_050_reference"]["retained_kg"]
                    dsat = ret["dew"][f"{fin}|R{R}|night_050_saturated"]["retained_kg"]
                    row = {"lead": lead, "R_m": R, "weather": w, "finish": fin, "capacity_kg_m2": capw, "endpoint_payload_kg": pay,
                           "allowance_kg": .1 * A, "capacity_kg": capw * A,
                           "rain_10min_kg": rain, "rain_10min_upper_kg": rain * RAIN_UPPER, "rain_1h_kg": rain1h,
                           "dew_reference_kg": dref, "dew_saturated_kg": dsat}
                    if lead == "P3":
                        pr = ponds["radii"][str(R)]
                        row["ponds_kg"] = {"mean": pr["pond_random_top"]["random_mean"], "p05": pr["pond_random_top"]["random_p05"],
                                           "p95": pr["pond_random_top"]["random_p95"], "min": pr["pond_random_top"]["random_min"],
                                           "node_up": pr["pond_vertex_up_kg"], "bay_up": pr["pond_face_up_kg"]}
                        row["dew_reference_kg"] += p3_dew_extra(R, "night_050_reference", fin)
                        row["dew_saturated_kg"] += p3_dew_extra(R, "night_050_saturated", fin)
                    acct.append(row)

    def rates(R, fin, cond):
        k = lambda hm: dry["results"][f"R{R}|{hm}|{fin}|{cond}"]
        lo, hi = k("sphere040"), k("flatplate")
        return lo, hi
    waits = []
    for lead, fin in (("P2", "MLCCAg"), ("P2", "paint_040"), ("P3", "paint_040")):
        for R in (10, 30):
            for cond in ("morning_fair", "midday_fair", "overcast_day"):
                lo, hi = rates(R, fin, cond)
                rlo, rhi = lo["hull_rate_kg_h"], hi["hull_rate_kg_h"]
                row = next(x for x in acct if x["lead"] == lead and x["R_m"] == R and x["weather"] == "ISA" and x["finish"] == fin)
                item = {"lead": lead, "finish": fin, "R_m": R, "condition": cond, "hull_rate_kg_h": [rlo, rhi]}
                for lab in ("rain_10min_kg", "dew_saturated_kg"):
                    m = row[lab]
                    item[f"dry_fully_h_{lab}"] = [m / rhi if rhi > 0 else None, m / rlo if rlo > 0 else None]
                if lead == "P3":
                    top_lo, top_hi = max(lo["rate_by_polar_deg"].values()), max(hi["rate_by_polar_deg"].values())
                    pr = ponds["radii"][str(R)]
                    for lab, mass, surf in (("bay_up", pr["pond_face_up_kg"], pr["pond_face_up_surface_m2"]),
                                            ("node_up", pr["pond_vertex_up_kg"], pr["pond_vertex_up_surface_m2"])):
                        item[f"pond_evaporation_h_{lab}"] = [mass / (surf * top_hi) if top_hi > 0 else None,
                                                             mass / (surf * top_lo) if top_lo > 0 else None]
                waits.append(item)

    # the ways to shed water, at R10 and R30 (PROJECTION where a value is not sourced)
    ued_L_m2 = 3.8 / src["ued_m2_per_3p8L"]
    usd_L = src["ued_price_usd_per_50gal"] / (50 * 3.785411784)
    methods = []
    for R in (10, 30):
        A = area(R)
        mlc = next(x for x in acct if x["lead"] == "P2" and x["R_m"] == R and x["weather"] == "ISA" and x["finish"] == "MLCCAg")
        sh = next(x for x in acct if x["lead"] == "P2" and x["R_m"] == R and x["weather"] == "ISA" and x["finish"] == "superhydrophobic")
        methods.append({"R_m": R, "method": "superhydrophobic topcoat (Ultra-Ever Dry class)",
                        "flying_mass_kg": [0.013 * A, 0.0375 * A],
                        "mass_basis": "13-25 um dry film (sourced) x 1.0-1.5 g/cm3 (PROJECTION, density not printed)",
                        "water_saved_kg": {"rain": mlc["rain_10min_kg"] - sh["rain_10min_kg"], "dew_saturated": mlc["dew_saturated_kg"] - sh["dew_saturated_kg"]},
                        "durability": f"about {src['ued_life_yr']:.0f} year outdoors; {src['ued_taber']:.0f} Taber cycles; Rain-X class {src['rainx_months']:.0f} months",
                        "cost_usd_per_application": ued_L_m2 * usd_L * A, "cost_basis": "bottom-coat drum price applied to both coats (PROJECTION)",
                        "optics": src["ued_optics"], "energy_kWh": 0.0, "P3_ponds": "no effect: ponds are geometric"})
        methods.append({"R_m": R, "method": "onboard heater film", "flying_mass_kg": src["heater_g_cm2"] * 10 * A,
                        "mass_basis": "polyimide etched-foil heater 0.04 g/cm2 (sourced)", "verdict": "excluded: heavier than either lead's margin"})
        lat = src["latent_MJ_kg"]
        methods.append({"R_m": R, "method": "ground heating", "flying_mass_kg": 0.0,
                        "dew_prevention_kWh_per_night": 319.0 * (R / 10) ** 2, "dew_prevention_kW": 26.6 * (R / 10) ** 2,
                        "dew_basis": "050: 21.1 W/m2, 26.6 kW and 319 kWh per 12 h at R10 (area-scaled)",
                        "evaporate_P2_rain_kWh_ideal": mlc["rain_10min_kg"] * lat / 3.6,
                        "evaporate_P3_ponds_kWh_ideal": [ponds["radii"][str(R)]["pond_random_top"]["random_mean"] * lat / 3.6,
                                                         ponds["radii"][str(R)]["pond_face_up_kg"] * lat / 3.6],
                        "anti_icing_reference_kW_m2": [src["antiice_SH_kW_m2"], src["antiice_enamel_kW_m2"]]})
        floor_m2 = (2 * R + 4) ** 2
        methods.append({"R_m": R, "method": "shelter or hangar for the night", "flying_mass_kg": 0.0,
                        "floor_m2": floor_m2, "cost_rub": src["hangar_rub"] / (30 * 15) * floor_m2,
                        "cost_basis": "30 x 15 m inflatable PVC hangar price per floor area (sourced) scaled to the hull footprint plus 2 m (PROJECTION; height not addressed)",
                        "historic_large_hangars": {"Goodyear Airdock 1929 USD": src["airdock_usd1929"], "CargoLifter 1998 MUSD": src["cargolifter_musd"],
                                                   "Lindstrand inflatable fabric t": src["lindstrand_t"]},
                        "water_avoided": "rain and dew while inside"})
        methods.append({"R_m": R, "method": "ground-supported cover", "flying_mass_kg": 0.0,
                        "fabric_kg": [src["silnylon_gsm"] / 1000 * A * 1.1, src["linen_gsm"] / 1000 * A * 1.1],
                        "fabric_basis": "42-90 g/m2 fabric over 110% of the hull area (PROJECTION overlap)",
                        "water_avoided": "dew (blocks sky cooling) and rain if it sheds off the cover"})
        methods.append({"R_m": R, "method": "air knives on a gantry", "flying_mass_kg": 0.0,
                        "power_kW": [src["blower_kW"], src["carwash_hp"] * 0.7457], "energy_kWh_per_pass": [src["blower_kW"] * 0.5, src["carwash_hp"] * 0.7457 * 0.5],
                        "basis": "one blower to a car-wash carousel; 0.5 h pass (PROJECTION); residual water after blow-off not sourced"})
        methods.append({"R_m": R, "method": "waiting (sun and wind)", "flying_mass_kg": 0.0, "energy_kWh": 0.0, "see": "waits"})
        methods.append({"R_m": R, "method": "P3: orient the frame and tilt after rain", "flying_mass_kg": 0.0,
                        "ponds_kg": {k: ponds["radii"][str(R)]["pond_random_top"][k] for k in ("random_min", "random_mean", "random_max")}
                                    | {"node_up": ponds["radii"][str(R)]["pond_vertex_up_kg"], "bay_up": ponds["radii"][str(R)]["pond_face_up_kg"]},
                        "tilt_to_spill_deg": 14.0, "basis": "ponds vanish above about 14 deg bay tilt (PONDS.json); handling hardware not sourced"})
    out = {"basis": __doc__, "sources": src, "rain_upper_factor": RAIN_UPPER, "p3_endpoints_052": p3ep, "p3_card": p3card,
           "account": acct, "waits": waits, "methods": methods, "sources_used": S.USED}
    with open(os.path.join(HERE, "WATER.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1)
    os.replace(os.path.join(HERE, "WATER.json.tmp"), os.path.join(HERE, "WATER.json"))
    for x in acct:
        if x["weather"] == "ISA" and x["R_m"] in (10, 30):
            extra = "" if x["lead"] == "P2" else f" ponds mean {x['ponds_kg']['mean']:.0f} (min {x['ponds_kg']['min']:.0f}, bay-up {x['ponds_kg']['bay_up']:.0f})"
            print(f"{x['lead']} R{x['R_m']} {x['finish']:18s} cap {x['capacity_kg_m2']:.4f} kg/m2 ({x['capacity_kg']:.0f} kg) | rain {x['rain_10min_kg']:.0f}/{x['rain_10min_upper_kg']:.0f} kg, dew {x['dew_reference_kg']:.0f}/{x['dew_saturated_kg']:.0f} kg{extra}")
    for x in waits:
        print(x["lead"], x["finish"], x["R_m"], x["condition"], [round(v, 1) for v in x["hull_rate_kg_h"]], {k: [None if v is None else round(v, 2) for v in vv] for k, vv in x.items() if k.startswith(("dry_", "pond_"))})


if __name__ == "__main__":
    main()
