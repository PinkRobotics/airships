#!/usr/bin/env python3
"""Compare the checker's own MAINLINE-019 numbers (check019.py) with the owner's filed RESULTS.json.

The owner's file is read here only, after the checker's numbers exist. Optimum LOCATIONS (tf, core, f, Vc) are graded
looser than optimum VALUES: a flat maximin optimum fixes its value far more tightly than its location.
"""
import json
from pathlib import Path

import check019 as c

OUT = c.OUT
OWNER = Path("unpublished-local-ref:faa5a9863ad10300"
             "vacuum-mainline019-margin-budget-1019")


def rel(a, b):
    if a == b:
        return 0.0
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def grade(a, b, loc=False):
    r = rel(a, b)
    tight, loose = (1e-9, 1e-6) if not loc else (1e-6, 1e-4)
    return "match_tight" if r <= tight else ("match_loose" if r <= loose else "MISMATCH")


def main():
    mine = json.loads((OUT / "RESULTS.json").read_text())
    own = json.loads((OWNER / "RESULTS.json").read_text())
    rows = []

    def add(name, card, me, loc=False):
        rows.append({"name": name, "card": card, "mine": me, "rel": rel(card, me), "grade": grade(card, me, loc)})

    # margin sweep 0..30 %
    for core in c.CORES:
        for frac_key, o in own["baseline_margin_sweep"][core].items():
            frac = float(frac_key)
            m = c.optimise(core, frac * c.L0)
            add(f"sweep {core} {frac:.2f} least_SF", o["least_SF"], m["least_SF"])
            add(f"sweep {core} {frac:.2f} tf_m", o["tf_m"], m["tf_m"], loc=True)
            add(f"sweep {core} {frac:.2f} core_m", o["core_m"], m["tc_m"], loc=True)
            add(f"sweep {core} {frac:.2f} Vc", o["Vc"], m["Vc"], loc=True)
            add(f"sweep {core} {frac:.2f} gamma", o["gamma_d"], m["gamma"])
    # scenarios: common reserve, line items, joints, climate, points
    keymap = {"systems_excess_kg": "systems_excess", "joints_and_bondfilm_excess_kg": "joints_excess",
              "retained_water_kg": "water", "contamination_kg": "contamination",
              "temperature_pressure_loss_kg": "climate_dry", "humidity_loss_kg": "humidity",
              "internal_gas_kg": "internal_air", "payload_kg": "payload"}
    for sc in ("optimistic", "conservative"):
        o, m = own["scenarios"][sc], mine["budgets"][sc]
        add(f"{sc} common reserve kg", o["margin_kg"], m["common_kg"])
        add(f"{sc} common reserve pct", o["margin_pct"], m["common_pct"])
        for core in c.CORES:
            ob, mb = o["budgets"][core], m["per_core"][core]
            for ok, mk in keymap.items():
                add(f"{sc} {core} item {mk}", ob["lines"][ok], mb["items_on_common_line"][mk])
            add(f"{sc} {core} total on common line", ob["total_margin_kg"], mb["total_on_common_line"])
            add(f"{sc} {core} seam kg", ob["joints"]["seam_kg"], mb["extra"]["seams"])
            add(f"{sc} {core} bond film kg", ob["joints"]["full_area_bondfilm_kg"], mb["extra"]["films"])
            op, mp = o["points"][core], mine["lines"][sc][core]
            add(f"{sc} {core} least_SF", op["least_SF"], mp["least_SF"])
            add(f"{sc} {core} worst-pressure least_SF", op["worst_pressure_least_SF"],
                mine["max_pressure"][sc][core])
            add(f"{sc} {core} tf_m", op["tf_m"], mp["tf_m"], loc=True)
            add(f"{sc} {core} core_m", op["core_m"], mp["tc_m"], loc=True)
            add(f"{sc} {core} Vc", op["Vc"], mp["Vc"], loc=True)
            add(f"{sc} {core} gamma", op["gamma_d"], mp["gamma"])
    # variants
    vmap = {"conservative_environment_passive_service": "conservative_sealed"}
    for ok, ov in own["variants"].items():
        mk = vmap.get(ok)
        if mk is None:
            mk = "conservative_8h" if "8" in ok else ("optimistic_payload100" if "payload" in ok else None)
        if mk is None:
            rows.append({"name": f"variant {ok}", "grade": "UNMAPPED"})
            continue
        add(f"variant {ok} reserve kg", ov["margin_kg"], mine["sensitivities"][mk]["common_kg"])
        for core in c.CORES:
            add(f"variant {ok} {core} least_SF", ov["points"][core]["least_SF"], mine["sensitivities"][mk]["SF"][core])
    # panel limits at the common 5 % line
    for core in c.CORES:
        for sc in ("optimistic", "conservative"):
            op = own["panel_limits_at_common_5pct"][core][sc]
            mp = mine["panel_limits_5pct"][f"{sc}|{core}"]
            add(f"panel {core} {sc} allowance kg", op["allowance_kg"], mp["allowance_kg"])
            add(f"panel {core} {sc} seams-only width m", op["seam_only_min_square_width_m"], mp["w_seams_only_m"])
            if op["all_joint_min_square_width_m"] is None or mp["w_with_films_m"] is None:
                rows.append({"name": f"panel {core} {sc} with-films width", "card": op["all_joint_min_square_width_m"],
                             "mine": mp["w_with_films_m"],
                             "grade": "match" if op["all_joint_min_square_width_m"] == mp["w_with_films_m"] else "MISMATCH"})
            else:
                add(f"panel {core} {sc} with-films width m", op["all_joint_min_square_width_m"], mp["w_with_films_m"])
    # vacuum route and systems
    sr, v = own["systems_routes"], mine["vacuum"]
    add("passive allowed gas load Pa m3/s", sr["passive"]["maximum_total_gas_throughput_at_T0_Pa_m3_s"],
        v["allowed_gas_load_ref_Pa_m3_s"])
    add("1%/day ingress Pa m3/s", sr["inherited_one_percent_day"]["Q_Pa_m3_s"], v["ingress_1pct_day_Pa_m3_s"])
    add("required speed m3/h at T0", sr["inherited_one_percent_day"]["required_pumping_m3_h_at_cap"], v["speed_ref_m3_h"])
    add("required speed m3/h at 320 K", sr["active_catalog"]["required_m3_h_at_320K"], v["speed_320K_m3_h"])
    add("reversible pump-down kWh", sr["commissioning"]["reversible_minimum_to_one_percent_kWh"], v["pumpdown_min_kWh"])
    # climate correction
    cc, mc = own["climate_correction"], mine["climate"]
    add("+25.1 K exact loss kg", cc["exact_loss_kg"], mc["dT_25.1_alone_exact"])
    add("+25.1 K linearised loss kg", cc["linearized_loss_kg"], mc["dT_25.1_alone_first_order"])
    add("old 5% remaining kg", -cc["margin_remaining_on_old_5pct_kg"], mc["old_5pct_short_by"])
    # 290 GPa
    for core in c.CORES:
        add(f"E 290 GPa optimistic {core} least_SF",
            own["material_modulus_sensitivity_290GPa_same_margins"]["optimistic"][core]["least_SF"],
            mine["E290"]["reoptimised"][core])
    # slopes
    for core in c.CORES:
        add(f"slope 0-5% {core}", own["slope_check"]["this_card"][core]["loss_per_100kg_0_to_5"],
            mine["slope_0_5_per100kg"][core])
        s30 = (c.optimise(core, 0.0)["least_SF"] - c.optimise(core, 0.3 * c.L0)["least_SF"]) / (0.3 * c.L0) * 100
        add(f"slope 0-30% {core}", own["slope_check"]["this_card"][core]["loss_per_100kg_0_to_30"], s30)
    # direct 009c-5
    add("009c-5 direct least_SF", own["reproduction"]["aramid009c5_direct"], mine["direct_009c5"]["least"])
    summary = {}
    for r in rows:
        summary[r["grade"]] = summary.get(r["grade"], 0) + 1
    out = {"rows": rows, "summary": summary,
           "max_rel_values": max(r["rel"] for r in rows if "rel" in r and "_m" not in r["name"][-5:]
                                 and "Vc" not in r["name"]),
           "max_rel_all": max(r["rel"] for r in rows if "rel" in r)}
    (OUT / "COMPARE.json").write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps(summary), "max rel (values)", out["max_rel_values"], "max rel (all)", out["max_rel_all"])
    for r in rows:
        if r["grade"] not in ("match_tight",):
            print(r["grade"], r["name"], r.get("card"), r.get("mine"), r.get("rel"))


if __name__ == "__main__":
    main()
