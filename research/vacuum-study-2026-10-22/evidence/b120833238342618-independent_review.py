"""Independent arithmetic spot checks. No owner code imported or executed."""
from pathlib import Path
import csv
import datetime as dt
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import brentq

B = Path(__file__).resolve().parent
S = B / "sources"
OUT = B / "checks"
OUT.mkdir(exist_ok=True)


def read(p):
    return json.loads(p.read_text())


def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


R_D = 287.053
G = 9.80665
LAPSE = .0065
P0 = 95460.83791390515
RHO_REF = 4889.442150186961 / (4 * math.pi * 10**3 / 3)
Q = .5 * RHO_REF * (70 * .514444)**2
P_FLOOR = 1.01 * P0


def es(t):
    c = np.asarray(t) - 273.15
    return 611.21 * np.exp((18.678 - c / 234.5) * c / (257.14 + c))


def atmosphere(t, dp, rh, z=100.0):
    """050 local-RH column, independently solved to convergence."""
    ps = 101325 + 100 * dp
    e = rh * es(t)
    p = ps * (t / (t + LAPSE * z))**(G / (R_D * LAPSE))
    for _ in range(40):
        p = ps * (t / (t + LAPSE * z))**(G * (1 - .378 * e / p) / (R_D * LAPSE))
    return float(p), float((p - .378 * e) / (R_D * t))


def hot_edge(mass, radius, volume_debit=0):
    volume = 4 * math.pi * radius**3 / 3 - volume_debit
    return brentq(lambda t: atmosphere(t, -30, 1)[1] * volume - mass, 220, 360) - 287.5


def growth2(bill, maturity):
    growth = {}
    for k, m in bill.items():
        if maturity == "concept":
            rate = (.15 if k in {"faces", "core", "mooring_pad"}
                    else .30 if k in {"charged_joining", "structural_primer"}
                    else .20 if k == "absorbed_water" else 0)
            growth[k] = m * rate
            if k == "coating":
                growth[k] = m / 1.1 * (.20 - .10)
        elif maturity == "TRL7":
            growth[k] = .05 * m if k in {
                "faces", "core", "mooring_pad", "charged_joining",
                "structural_primer", "absorbed_water"
            } else 0
        else:
            growth[k] = 0
    return growth


def review061():
    data = read(B / "inputs/061/RESULTS.json")
    density = []
    for row in data["p2"]:
        if row["basis"] != "endpoint" and row["R_m"] != 30:
            continue
        single = next(x for x in row["single"] if x["property"] == "face_density")
        witness = single["solution"]
        radius = row["R_m"]
        area = 4 * math.pi * radius**2
        bill = witness["bill_kg"]
        face_volume = 2 * area * witness["geometry"]["tf_m"]
        nominal_faces = face_volume * 1850
        nonface = {k: v for k, v in bill.items() if k != "faces"}
        nonface_charged = sum(nonface.values()) + sum(growth2(nonface, "concept").values())
        factor = 1.15 * nominal_faces / (witness["lift_kg"] - nonface_charged)
        calculated_bill = dict(bill, faces=nominal_faces / factor)
        payload = witness["lift_kg"] - sum(calculated_bill.values()) - sum(growth2(calculated_bill, "concept").values())
        combo = row["combination"]
        density.append({
            "R_m": radius, "weather": row["weather"], "basis": row["basis"],
            "maturity": "concept", "geometry_input": witness["geometry"],
            "joining_floor_active_input": witness["floor"],
            "owner_factor": single["factor"], "independent_factor": factor,
            "difference": factor - single["factor"], "payload_at_independent_factor_kg": payload,
            "nominal_faces_kg": nominal_faces, "nonface_with_growth_kg": nonface_charged,
            "combo_product": combo["factor_product"], "combo_factors": combo["factors"],
            "combo_vs_density_factor": combo["factor_product"] - factor,
            "scope": "Independent mass closure at supplied geometry; does not certify geometry or global optimality."
        })
    trl = []
    for row in data["p2"]:
        if row["basis"] != "endpoint" or (row["R_m"], row["weather"]) not in [(12, "ISA"), (20, "optimistic")]:
            continue
        w = row["deficit"]["TRL7"]
        growth = growth2(w["bill_kg"], "TRL7")
        payload = w["lift_kg"] - sum(w["bill_kg"].values()) - sum(growth.values())
        trl.append({
            "R_m": row["R_m"], "weather": row["weather"], "growth_kg": growth,
            "growth_total_kg": sum(growth.values()), "independent_payload_kg": payload,
            "owner_payload_kg": w["payload_kg"], "difference_kg": payload - w["payload_kg"],
            "geometry_input": w["geometry"], "global_mode_input": w["modes"].get("global")
        })
    p3 = []
    retain = {"SiC_tubes", "systems", "vacuum_service", "gas", "exterior_water",
              "contamination", "mooring_load_introduction", "sag_lift_debit", "weather_headroom"}
    for row in data["p3"]:
        w = row["deficit"]["none"]
        bill = {k: v for k, v in w["bill_kg"].items() if k in retain}
        growth = .15 * (bill["SiC_tubes"] + bill["mooring_load_introduction"])
        mass = sum(bill.values()) + growth
        upper = w["lift_kg"] - mass
        relief = row["combination"]["058_full_relief_fraction_given_for_free"]
        generous_upper = upper + 1.15 * bill["SiC_tubes"] * relief
        p3.append({
            "R_m": row["R_m"], "weather": row["weather"], "retained_bill_kg": bill,
            "growth_kg": growth, "independent_irreducible_mass_kg": mass,
            "independent_payload_upper_bound_kg": upper,
            "owner_payload_upper_bound_kg": row["combination"]["irreducible_payload_upper_bound_kg"],
            "difference_kg": upper - row["combination"]["irreducible_payload_upper_bound_kg"],
            "free_relief_fraction_input": relief, "generous_upper_bound_kg": generous_upper,
            "owner_generous_bound_kg": row["combination"]["relief_generous_payload_upper_bound_kg"],
            "scope": "Fixed g/R family and fixed tube lower bound; deleted all favorable-lever reducible items."
        })
    beryllium = []
    for row in data["beryllium"]:
        if row["R_m"] != 30:
            continue
        case = next(x for x in data["p2"] if x["R_m"] == 30 and x["basis"] == "endpoint" and x["weather"] == row["weather"])
        geom = case["deficit"]["none"]["geometry"]
        mass = 2 * 4 * math.pi * 30**2 * geom["tf_m"] * 1850
        beryllium.append({
            "weather": row["weather"], "face_volume_times_density_kg": mass,
            "USGS_2025_world_mine_Be_content_kg": 430000,
            "independent_percent": 100 * mass / 430000,
            "owner_percent": row["nominal_share_percent"],
            "difference_percentage_points": 100 * mass / 430000 - row["nominal_share_percent"],
            "excludes": "Fabrication yield, spares and conversion from mine Be content to sheet capacity."
        })
    frozen = []
    for row in data["frozen_check057"]:
        if row["R_m"] == 20 and row["weather"] == "optimistic":
            lift = 4889.442150186961 * (20 / 10)**3
            payload = lift - sum(row["bill_kg"].values()) - sum(growth2(row["bill_kg"], "TRL7").values())
            frozen.append({"R_m": 20, "weather": "optimistic", "independent_payload_kg": payload,
                           "owner_payload_kg": row["payloads_kg"]["TRL7"],
                           "scope": "Frozen earlier geometry, corrected 5% hardware rate, no silent replacement by 061 geometry."})
    return {"density": density, "TRL7": trl, "P3_certificate": p3,
            "beryllium": beryllium, "frozen_R20_optimistic": frozen}


def review058_edges():
    data = read(B / "inputs/058/RESULTS.json")
    hulls = read(S / "levers058.json")
    p3data = read(S / "p3_058.json")
    # Maximum pressure of the stated rectangular grid is the hot, saturated,
    # lowest-altitude corner; compare the two named sea pressures.
    loads = []
    for dp in [30, -30]:
        p, rho = atmosphere(307.5, dp, 1)
        own = max(P_FLOOR, p) + Q
        owner = hulls["design_loads_Pa"][f"z100_dp{dp}"]
        loads.append({"dp_hPa": dp, "T_K": 307.5, "RH": 1, "Q_Pa": Q,
                      "independent_design_Pa": own, "owner_Pa": owner, "difference_Pa": own - owner})
    edges = []
    bands = []
    for radius in [10, 30]:
        reference = next(x for x in data["levers"]["P2"] if x["R_m"] == radius)
        full = next(x for x in hulls["hulls"] if x["R_m"] == radius and x["mask"] == 11 and x["id"] == "full")
        trim = next(x for x in hulls["hulls"] if x["R_m"] == radius and x["mask"] == 11 and x["id"] == "trim-30")
        e_full = hot_edge(full["mass_kg"], radius)
        e_trim = hot_edge(trim["mass_kg"], radius)
        edges.append({"lead": "P2", "R_m": radius, "independent_full_K": e_full,
                      "owner_full_K": reference["baseline_050"]["hot_edge_K"]["-30"],
                      "independent_trim_K": e_trim,
                      "owner_trim_K": reference["relief_trim"]["hot_edge_K"]["-30"],
                      "independent_gain_K": e_trim - e_full,
                      "scope": "Fixed saved hull masses, saturated low-pressure corner, before added relief hardware."})
        prow = next(x for x in p3data["rows"] if x["R_m"] == radius and x["selection"] == "mask15")
        pfull = hot_edge(prow["mass_full_kg"], radius, prow["v_sag_m3"])
        ptrim = hot_edge(prow["mass_trim_kg"], radius, prow["v_sag_m3"])
        edges.append({"lead": "P3", "R_m": radius, "independent_full_K": pfull,
                      "independent_trim_K": ptrim, "independent_gain_K": ptrim - pfull,
                      "owner_full_K": next(x["hot_edge_offset_K"] for x in prow["edges"] if x["hull"] == "full" and x["dp_hPa"] == -30 and x["RH"] == 1),
                      "owner_trim_K": next(x["hot_edge_offset_K"] for x in prow["edges"] if x["hull"] == "trim-30" and x["mode"] == "trim" and x["dp_hPa"] == -30 and x["RH"] == 1)})
        w = next(x for x in data["widest_band"]["P2"] if x["R_m"] == radius and x["mask"] == 11 and x["finish"] == "AlAOC")
        hardware = 5 + .02 * w["ballast_capacity_kg"]
        mass = w["hull_kg"] + hardware
        hot = hot_edge(mass, radius)
        cold = w["cold_edge_air_K"] - 287.5
        bands.append({"R_m": radius, "independent_hardware_kg": hardware, "whole_mass_kg": mass,
                      "independent_hot_K": hot, "cold_input_K": cold,
                      "independent_width_K": hot - cold, "owner_width_K": w["width_at_worst_corner_K"],
                      "baseline_width_K": e_full - (full["cold_threshold_K"]["clear_night"] - 287.5),
                      "cold_shift_K": trim["cold_threshold_K"]["clear_night"] - w["cold_edge_air_K"],
                      "scope": "Independent mass, EOS/root and subtraction; cold thermal roots are supplied boundary inputs."})
    return {"pressure_loads": loads, "edges": edges, "bands": bands}


def weather058(station_height=0, humidity_height=False):
    arr = np.load(S / "heathrow_hourly058.npz", allow_pickle=False)
    t_surface = arr["T_K"] + LAPSE * station_height
    ps = arr["SLP_hPa"] * 100
    f_vapor = es(arr["Td_K"]) / ps
    if humidity_height:
        for _ in range(30):
            p_station = ps * (arr["T_K"] / t_surface)**(G * (1-.378*f_vapor)/(R_D*LAPSE))
            f_vapor = es(arr["Td_K"]) / p_station
    exponent = G * (1 - .378 * f_vapor) / (R_D * LAPSE)
    t_floor = t_surface - LAPSE * 100
    p_floor = ps * (t_floor / t_surface)**exponent
    density_floor = p_floor * (1 - .378 * f_vapor) / (R_D * t_floor)
    valid = np.isfinite(t_surface) & np.isfinite(arr["Td_K"]) & np.isfinite(ps)
    days_valid = valid.reshape(-1, 24).all(axis=1)
    daylight = arr["sun_elevation_deg"] > 0
    source = read(S / "days058b.json")
    thermal = read(S / "days058.json")
    levers = read(S / "levers058.json")
    report = read(B / "inputs/058/RESULTS.json")
    p3hulls = read(S / "p3_058.json")

    def score(ok):
        ok = valid & ok
        day = ok.reshape(-1, 24).all(axis=1) & days_valid
        return {"hours_count": int(ok.sum()), "hours_fraction": float(ok.sum()/valid.sum()),
                "days_count": int(day.sum()), "full_day_fraction": float(day.sum()/days_valid.sum())}

    def projected(r, added_mass=0):
        R = r["R_m"]
        mass = r["mass_kg"] + added_mass
        pcap = r["design_load_Pa"] - Q
        t_climb = np.where(p_floor > pcap, t_surface * (pcap / ps)**(1 / exponent), t_floor)
        p_climb = np.minimum(p_floor, pcap)
        rho_climb = p_climb * (1 - .378 * f_vapor) / (R_D * t_climb)
        # Admitted ambient air gives the pressure relief its own onboard mass.
        rho_net_trim = np.minimum(p_floor, pcap) * (1 - .378 * f_vapor) / (R_D * t_floor)
        volume = 4 * math.pi * R**3 / 3
        if "selection" in r:
            ph = next(x for x in p3hulls["rows"] if x["R_m"] == R and x["selection"] == r["selection"])
            volume -= ph["v_sag_m3"]
            cold_floor = cold_climb = np.ones(len(valid), dtype=bool)
        else:
            # Independently recompute the counts, holding the declared thermal
            # boundary data fixed. Do not claim an independent thermal solution.
            hid = "full" if r["hull"] == "full" else ("trim-30" if r["finish"] == "MLCCAg" else "finish_" + r["finish"])
            th = next(x for x in thermal["rows"] if x["lead"] == "P2" and x["R_m"] == R
                      and x["mask"] == r["mask"] and x["hull"] == hid and x["variant"] == "primary")
            grid = thermal["D_grid_K"]
            night = np.interp(24.9, grid, th["thresholds_K"]["night"])
            day = np.interp(9.9, grid, th["thresholds_K"]["day_no_sun"])
            threshold = np.where(daylight, day, night)
            cold_floor = t_floor >= threshold
            cold_climb = t_climb >= threshold
        none = (p_floor + Q <= r["design_load_Pa"] + 1e-6) & (density_floor * volume >= mass) & cold_floor
        trim = (rho_net_trim * volume >= mass) & cold_floor
        climb = (rho_climb * volume >= mass) & cold_climb
        ok = {"none": none, "trim": trim, "climb": climb, "best": trim | climb}[r["set"]]
        return score(ok)

    samples = []
    for R, finish, hull, op in [(10, "MLCCAg", "full", "none"),
                                (10, "MLCCAg", "trim-30", "best"),
                                (10, "AlAOC", "trim-30", "best"),
                                (12, "AlAOC", "trim-30", "best"),
                                (20, "AlAOC", "trim-30", "best")]:
        r = next(x for x in source["P2"] if x["R_m"] == R and x["mask"] == 11 and
                 x["finish"] == finish and x["hull"] == hull and x["set"] == op and x["variant"] == "primary")
        own = projected(r)
        hardware = 0
        if hull != "full":
            whole = next(x for x in report["widest_band"]["P2"] if x["R_m"] == R and x["mask"] == 11 and x["finish"] == finish)
            hardware = 5 + .02 * whole["ballast_capacity_kg"]
        samples.append({"lead": "P2", "R_m": R, "finish": finish, "hull": hull, "operation": op,
                        "owner_mass_kg": r["mass_kg"], "owner_day_fraction": r["full_day_fraction"],
                        "owner_hour_fraction": r["hours_fraction"], "independent_at_owner_mass": own,
                        "added_hardware_kg": hardware, "independent_with_hardware": projected(r, hardware)})
    for R in [10, 12, 15]:
        r = next(x for x in source["P3"] if x["R_m"] == R and x["selection"] == "mask15" and
                 x["hull"] == "design+0" and x["set"] == "climb" and x["variant"] == "primary")
        own = projected(r)
        samples.append({"lead": "P3", "R_m": R, "hull": "design+0", "operation": "climb",
                        "owner_mass_kg": r["mass_kg"], "owner_day_fraction": r["full_day_fraction"],
                        "owner_hour_fraction": r["hours_fraction"], "independent_at_owner_mass": own,
                        "independent_with_valve_only": projected(r, 5),
                        "scope": "5 kg valve is a lower hardware bound; no matched standard-pressure bladder specification in the whole-band table."})
    # Raw observation spot check independent of the NPZ conversion; one day's
    # on-the-hour FM-12 observations. Denominator check below covers every NPZ hour.
    raw = []
    with (S / "2014-03772099999.csv").open(newline="") as handle:
        for row in csv.DictReader(handle):
            if not row["DATE"].startswith("2014-01-01") or row["REPORT_TYPE"].strip() != "FM-12":
                continue
            at = dt.datetime.fromisoformat(row["DATE"])
            if at.minute:
                continue
            j = at.hour
            ours = {"T_K": int(row["TMP"].split(",")[0])/10 + 273.15,
                    "Td_K": int(row["DEW"].split(",")[0])/10 + 273.15,
                    "SLP_hPa": int(row["SLP"].split(",")[0])/10}
            raw.append({"UTC": row["DATE"], "parsed": ours,
                        "NPZ": {k: float(arr[k][j]) for k in ours},
                        "max_absolute_difference": max(abs(ours[k] - arr[k][j]) for k in ours)})
    return {
        "mapping": {"Tsea": "observed T + lapse*station_height",
                    "station_height_m": station_height,
                    "dewpoint_pressure_corrected_to_station": humidity_height},
        "coverage_scope": "Independent EOS, pressure-relief and all-24-hour reduction on pinned weather arrays; thermal thresholds supplied as data.",
        "calendar_hours": len(valid), "complete_hours": int(valid.sum()), "calendar_days": len(days_valid),
        "complete_24h_UTC_days": int(days_valid.sum()), "excluded_days": int((~days_valid).sum()),
        "selected_cases": samples, "raw_NOAA_spot_checks": raw
    }


if __name__ == "__main__":
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    t0 = time.monotonic()
    if len(sys.argv) == 1:
        save("061-ARITHMETIC.json", review061())
        save("058-EDGES.json", review058_edges())
        save("058-COVERAGE.json", weather058())
        label = "EXECUTION.json"
    elif sys.argv[1] == "mapping":
        for height, humidity in [(2, False), (25.29, False), (27.29, False), (25.29, True)]:
            save(f"058-COVERAGE-height{height}-humidity{humidity}.json", weather058(height, humidity))
        label = "MAPPING-EXECUTION.json"
    else:
        save("058-COVERAGE-height27.29-humidityTrue.json", weather058(27.29, True))
        label = "CANONICAL-MAPPING-EXECUTION.json"
    save(label, {"measured_start": start,
                            "measured_end": dt.datetime.now(dt.timezone.utc).isoformat(),
                            "elapsed_seconds": time.monotonic() - t0,
                            "owner_code_read_imported_or_executed": False})
    print("Independent mass, EOS, pressure-relief, weather aggregation and source-data spot checks completed.")
