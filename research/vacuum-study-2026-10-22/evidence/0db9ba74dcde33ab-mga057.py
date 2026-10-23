#!/usr/bin/env python3
"""MAINLINE-057: concept-stage mass-growth allowance (MGA) on both leads' whole bills, the floating size with it, and the
payload sensitivity to a flat allowance. Own arithmetic on the owners' filed bills (read as data, no owner code run).

MGA table: NASA GSFC IDC Table VI-1 'Mass MGA %s' (Karpati, Hyde, Peabody, Garrison, Resource Management and Contingencies in
Aerospace Concurrent Engineering, NTRS 20120013284), adapted from Table 1 of AIAA S-120-2006. Maturity map used here:
estimated -> TRL 0-2 row; calculated -> TRL 3-5 row; measured -> TRL 8 row (weighed, not flown). Allocations and
environmental allowances get no MGA; an item carrying its own margin gets only the excess of the table value over it.
P2 bills: 048 fold (MLCCAg, bake70, cure in global, 0.1 kg/m2 retained water) at R10/12/15; 040 (200 F fix) at R10-R30 with
048's finish transferred (coating 0.2 kg/m2 replaced by 8.33272 g/m2 finish + 10 g/m2 primer + absorbed water), checked
against 048 at R10-15. P3 bills: 052 at R10-R30, ground service unless stated."""
import json
import math
from pathlib import Path

W = Path("unpublished-local-ref:7a5bf1cec24b249e")
OUT = W / "ref-55cff924be25afe6f9dd/.ship/work/outputs/vacuum-mainline057-mass-growth-1020"
F048 = W / "ref-3f7ec48b84b54a049007/.ship/work/outputs/vacuum-mainline048-fold-check040-1020/RESULTS-MLCCAg.json"
F040 = W / "ref-3f7ec48b84b54a049007/.ship/work/outputs/vacuum-mainline040-common-account-1020/RESULTS.json"
F052 = W / "ref-baa4584cf36c531365e7/.ship/work/outputs/vacuum-mainline052-p3-common-account-1020/RESULTS.json"
L0 = 4889.44215019

# GSFC Table VI-1 (percent) by TRL row and item type
GSFC = {"TRL 0-2": {"structure": 25, "hardware": 30, "thermal": 25, "mechanisms": 25, "electrical_gt15kg": 20},
        "TRL 3-5": {"structure": 15, "hardware": 20, "thermal": 20, "mechanisms": 15, "electrical_gt15kg": 15},
        "TRL 6": {"structure": 10, "hardware": 15, "thermal": 15, "mechanisms": 10, "electrical_gt15kg": 10},
        "TRL 7": {"structure": 5, "hardware": 6, "thermal": 5, "mechanisms": 5, "electrical_gt15kg": 5},
        "TRL 8": {"structure": 3, "hardware": 3, "thermal": 3, "mechanisms": 3, "electrical_gt15kg": 3},
        "TRL 9": {"structure": 0, "hardware": 0, "thermal": 0, "mechanisms": 0, "electrical_gt15kg": 0}}
ROW = {"estimated": "TRL 0-2", "calculated": "TRL 3-5", "measured": "TRL 8"}

# item -> (type, maturity, own margin as a fraction of the item, note); type None = allocation/environment, no MGA
P2_ITEMS = {
    "faces": ("structure", "calculated", 0.0, "SR-200 faces sized by the line's buckling/strength account; no hardware"),
    "core": ("structure", "calculated", 0.0, "CR III 5056 3/8-1.0, density x volume"),
    "charged_joining": ("hardware", "estimated", 0.0, "film, scarf, splice, seal from rules and catalog areal masses; process unqualified (038 T2)"),
    "coating": ("thermal", "calculated", 0.10, "MLCCAg recipe 7.5752 g/m2 plus its own +10% (048)"),
    "mooring_pad": ("structure", "calculated", 0.0, "sized for the 70 kn load"),
    "structural_primer": ("hardware", "estimated", 0.0, "assumed extra 10 g/m2 primer (048)"),
    "absorbed_water": ("thermal", "calculated", 0.0, "material water fractions (048)"),
    "gas": (None, "allocation", 0.0, "internal air allocation, 1% of L0 (COMMON)"),
    "systems": (None, "allocation", 0.0, "the 100 kg systems allowance (its own margin)"),
    "extra_service": (None, "allocation", 0.0, "service hardware charge"),
    "water": (None, "environment", 0.0, "assumed 0.1 kg/m2 retained exterior water (048); its own case"),
    "contamination": (None, "allocation", 0.0, "contamination allocation"),
    "weather_headroom": (None, "environment", 0.0, "weather headroom (its own case)"),
    "desiccant": ("hardware", "estimated", 0.0, "sorbent (zero at bake70)"),
}
P3_ITEMS = {
    "SiC_tubes": ("structure", "calculated", 0.0, "SiC members sized by the frame account; process unproven"),
    "joint_sleeves_and_allowance": ("hardware", "estimated", None, "sleeves; above the actual sleeves the item is its own allowance"),
    "joint_bond_and_installation": ("hardware", "estimated", 0.0, "bonds and installation"),
    "nodes": ("hardware", "estimated", 0.0, "nodes"),
    "PBO_two_plies": ("structure", "calculated", 0.0, "two-ply PBO film sized by stress"),
    "barrier_and_protection": ("thermal", "calculated", 0.0, "PET, Al, attachment, white finish, seams (052)"),
    "mooring_load_introduction": ("structure", "calculated", 0.0, "70 kn pad"),
    "systems": (None, "allocation", 0.0, "the 100 kg systems allowance"),
    "vacuum_service": (None, "allocation", 0.0, "additional 50 kg service charge (top of the 30-50 kg band)"),
    "gas": (None, "allocation", 0.0, "1% of L0"),
    "exterior_water": (None, "environment", 0.0, "0.1 kg/m2 retained exterior water"),
    "contamination": (None, "allocation", 0.0, "allocation"),
    "sag_lift_debit": (None, "lift debit", 0.0, "calculated buoyancy loss from film sag, not hardware mass"),
    "weather_headroom": (None, "environment", 0.0, "weather headroom"),
}


def item_mga(table, bill, extra=None, scheme="sourced"):
    """Added kg per item. scheme 'sourced': table value by type and maturity, less any own margin; 'estimated': every
    hardware item at the TRL 0-2 row."""
    add = {}
    for k, m in bill.items():
        typ, mat, own, _ = table.get(k, ("hardware", "estimated", 0.0, "unclassified"))
        if typ is None or m <= 0:
            add[k] = 0.0
            continue
        row = ROW[mat] if scheme == "sourced" else ("TRL 0-2" if scheme == "estimated" else scheme)
        pct = GSFC[row][typ] / 100.0
        if own is None:                                   # P3 joint allowance above the actual sleeves is its own margin
            actual = (extra or {}).get("actual_sleeves", m)
            add[k] = max(0.0, pct * actual - (m - actual))
        else:
            add[k] = max(0.0, (pct - own) * m)
    return add


def hardware(table, bill):
    return sum(m for k, m in bill.items() if table.get(k, ("hardware",))[0] is not None)


def transfer040(bill, area):
    """040 bill -> 048 finish: coating 0.2 kg/m2 -> 8.33272 g/m2 finish, plus 10 g/m2 primer and 1.0894e-4 kg/m2 absorbed water."""
    b = dict(bill)
    b["coating"] = 0.00833272 * area
    b["structural_primer"] = 0.01 * area
    b["absorbed_water"] = 0.13690315860808328 / 1256.6370614359173 * area
    return b


def main():
    res = {"schema": 1, "unit": "vacuum-mainline057-mass-growth-1020", "tag": "QUESTIONABLE / PROJECTION",
           "mga_table": {"source": "NASA GSFC IDC Table VI-1, NTRS 20120013284, adapted from AIAA S-120-2006 Table 1", "rows": GSFC,
                         "maturity_map": ROW, "system_margin_note": "the same source adds a system-level margin, typically 30% for "
                         "Pre-Phase-A concepts, above the itemized MGA; not applied in the itemized case"},
           "classification": {"P2": {k: {"type": v[0], "maturity": v[1], "own_margin": v[2], "note": v[3]} for k, v in P2_ITEMS.items()},
                              "P3": {k: {"type": v[0], "maturity": v[1], "own_margin": v[2], "note": v[3]} for k, v in P3_ITEMS.items()}}}
    # ---------------- P2 from 048 (R10/12/15)
    d48 = json.loads(F048.read_text())["rows"]
    p2 = []
    for r in d48:
        if r["drying"] != "bake70" or not r["cure_in_global"] or r["external_water_kg_m2"] != 0.1 or r["weather"] == "both":
            continue
        trials = r["least"].get("endpoint_trials") or []
        rec = {"source": "048", "R_m": r["R_m"], "weather": r["weather"], "floor": r["floor"], "id": r["id"], "masks": []}
        for t in trials:
            s = t.get("solution") or {}
            bill = s.get("bill_kg")
            if not bill:
                continue
            rec["masks"].append({"mask": t["mask"], "axes": t["axes"], "payload_kg": t["payload_kg"], "bill": bill,
                                 "lift_kg": s.get("lift_kg")})
        tfe = r.get("two_factor_endpoint")
        if tfe:
            rec["least_endpoint"] = {"mask": tfe["mask"], "axes": tfe["selected_axes"], "payload_kg": tfe["signed_payload_kg"],
                                     "bill": tfe["bill_kg"], "lift_kg": tfe["lift_kg"]}
        p2.append(rec)
    # ---------------- P2 from 040 with the finish transfer (R10-R30)
    d40 = json.loads(F040.read_text())["rows"]
    for r in d40:
        if r["pad"] != "heavy70" or not r["vented"] or r["weather"] == "both":
            continue
        L = r["least"]
        rec = {"source": "040 with 048 finish transfer", "R_m": r["R_m"], "weather": r["weather"], "floor": r["floor"], "id": r["id"],
               "masks": []}
        for t in L.get("endpoint_trials") or []:
            s = t.get("solution") or {}
            bill = s.get("bill_kg")
            if not bill:
                continue
            area = s["geometry"]["area_m2"]
            b2 = transfer040(bill, area)
            rec["masks"].append({"mask": t["mask"], "axes": t["axes"], "payload_kg": s["lift_kg"] - sum(b2.values()), "bill": b2,
                                 "lift_kg": s["lift_kg"], "payload_040_kg": t["payload_kg"]})
        p2.append(rec)
    # ---------------- P3 from 052
    d52 = json.loads(F052.read_text())["rows"]
    p3 = []
    for r in d52:
        rec = {"source": "052", "R_m": r["R_m"], "weather": r["weather"], "service": r["service"], "masks": []}
        for e in r.get("endpoints") or []:
            rec["masks"].append({"mask": e["mask"], "axes": e["axes"], "payload_kg": e["payload_kg"], "bill": e["bill_kg"],
                                 "lift_kg": e["lift_kg"], "actual_sleeves": e["joint_actual_sleeves_kg"]})
        p3.append(rec)

    def evaluate(rec, table, schemes=("sourced", "estimated")):
        out = []
        for m in rec["masks"]:
            row = {"mask": m["mask"], "axes": m["axes"], "payload_kg": m["payload_kg"], "hardware_kg": hardware(table, m["bill"])}
            for sch in schemes:
                add = item_mga(table, m["bill"], {"actual_sleeves": m.get("actual_sleeves", 0.0)}, sch)
                row[f"mga_{sch}_kg"] = sum(add.values())
                row[f"payload_{sch}_kg"] = m["payload_kg"] - sum(add.values())
                row[f"mga_{sch}_by_item"] = add
            row["flat_tolerable_on_hardware"] = m["payload_kg"] / row["hardware_kg"] if row["hardware_kg"] else None
            out.append(row)
        return out

    def least_set(rows, key):
        ok = [r for r in rows if r[key] >= 0]
        if not ok:
            return None
        n = min(len(r["axes"]) for r in ok)
        best = max((r for r in ok if len(r["axes"]) == n), key=lambda r: r[key])
        return {"axes": best["axes"], "count": n, "payload_kg": best[key]}

    summary = []
    for lead, recs, table in (("P2", p2, P2_ITEMS), ("P3", p3, P3_ITEMS)):
        for rec in recs:
            rows = evaluate(rec, table)
            rec["evaluated"] = rows
            allm = max(rows, key=lambda r: len(r["axes"])) if rows else None
            summary.append({"lead": lead, "source": rec["source"], "R_m": rec["R_m"], "weather": rec["weather"],
                            "floor": rec.get("floor"), "service": rec.get("service"),
                            "all_axes_payload_kg": allm["payload_kg"] if allm else None,
                            "all_axes_payload_sourced_mga_kg": allm["payload_sourced_kg"] if allm else None,
                            "all_axes_payload_estimated_mga_kg": allm["payload_estimated_kg"] if allm else None,
                            "all_axes_sourced_mga_kg": allm["mga_sourced_kg"] if allm else None,
                            "all_axes_hardware_kg": allm["hardware_kg"] if allm else None,
                            "flat_tolerable_on_hardware_at_all_axes": allm["flat_tolerable_on_hardware"] if allm else None,
                            "least_set_no_mga": least_set(rows, "payload_kg"),
                            "least_set_sourced_mga": least_set(rows, "payload_sourced_kg"),
                            "least_set_estimated_mga": least_set(rows, "payload_estimated_kg")})
    # flat sensitivity at all-axes endpoints (ISA and optimistic; P2 actual joining; P3 ground)
    flat = []
    for s, rec in zip(summary, p2 + p3):
        if (s["lead"] == "P2" and (s["floor"] or s["source"] != "040 with 048 finish transfer")) or \
           (s["lead"] == "P3" and s["service"] != "ground"):
            continue
        row = {"lead": s["lead"], "R_m": s["R_m"], "weather": s["weather"]}
        for f in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30):
            row[f"flat_{int(f * 100)}"] = s["all_axes_payload_kg"] - f * s["all_axes_hardware_kg"]
        row["tolerable_flat"] = s["flat_tolerable_on_hardware_at_all_axes"]
        flat.append(row)
    # transfer check at R10-15: 048 actual rows vs 040-transfer actual rows, same mask
    check = []
    for a in p2:
        if a["source"] != "048" or a["floor"]:
            continue
        b = next((x for x in p2 if x["source"].startswith("040") and x["R_m"] == a["R_m"] and x["weather"] == a["weather"]
                  and x["floor"] == a["floor"]), None)
        if not b:
            continue
        for m in a["masks"]:
            mb = next((x for x in b["masks"] if x["mask"] == m["mask"]), None)
            if mb:
                check.append({"R_m": a["R_m"], "weather": a["weather"], "mask": m["mask"], "payload_048_kg": m["payload_kg"],
                              "payload_040_transfer_kg": mb["payload_kg"], "diff_kg": mb["payload_kg"] - m["payload_kg"]})
    # maturity sweep: every hardware item at one TRL row (types as classified), all-axes endpoint, actual/ground, ISA and optimistic
    sweep = []
    for lead, recs, table in (("P2", p2, P2_ITEMS), ("P3", p3, P3_ITEMS)):
        for rec in recs:
            if (lead == "P2" and (rec["floor"] or not rec["source"].startswith("040"))) or (lead == "P3" and rec["service"] != "ground"):
                continue
            if rec["weather"] == "both" or not rec["masks"]:
                continue
            m = max(rec["masks"], key=lambda x: len(x["axes"]))
            row = {"lead": lead, "R_m": rec["R_m"], "weather": rec["weather"], "payload_no_mga_kg": m["payload_kg"]}
            for trl in GSFC:
                add = item_mga(table, m["bill"], {"actual_sleeves": m.get("actual_sleeves", 0.0)}, trl)
                row[trl] = m["payload_kg"] - sum(add.values())
            floats = [t for t in GSFC if row[t] >= 0]
            row["least_mature_row_that_floats"] = floats[0] if floats else None
            sweep.append(row)
    # optimism cost: linear extrapolation of payload in the least set's usage, from its zero-payload point to its endpoint
    cost = []
    for r in d48:
        if r["drying"] != "bake70" or not r["cure_in_global"] or r["external_water_kg_m2"] != 0.1 or r["floor"] or r["weather"] != "ISA":
            continue
        L = r["least"].get("least")
        if not L:
            continue
        T = next((t for t in r["least"].get("endpoint_trials") or [] if t["mask"] == L["mask"]), None)
        if not T or not T.get("solution"):
            continue
        u0, pay1 = L["usage"], T["payload_kg"]
        slope = pay1 / (1 - u0)
        mga = sum(item_mga(P2_ITEMS, T["solution"]["bill_kg"]).values())
        cost.append({"lead": "P2", "R_m": r["R_m"], "least_set": L["selected_axes"], "usage_at_zero_payload": u0,
                     "endpoint_payload_kg": pay1, "kg_per_unit_usage": slope, "sourced_mga_kg": mga,
                     "usage_needed_with_mga": u0 + mga / slope})
    for r in d52:
        if r["service"] != "ground" or r["weather"] != "ISA" or not r.get("least"):
            continue
        L = r["least"]
        E = next((e for e in r.get("endpoints") or [] if e["mask"] == L["mask"]), None)
        if not E:
            continue
        u0 = L["usage"]; pay1 = E["payload_kg"]
        if not (0 < u0 < 1):
            continue
        slope = pay1 / (1 - u0)
        mga = sum(item_mga(P3_ITEMS, E["bill_kg"], {"actual_sleeves": E["joint_actual_sleeves_kg"]}).values())
        cost.append({"lead": "P3", "R_m": r["R_m"], "least_set": L["axes"], "usage_at_zero_payload": u0, "endpoint_payload_kg": pay1,
                     "kg_per_unit_usage": slope, "sourced_mga_kg": mga, "usage_needed_with_mga": u0 + mga / slope})
    res.update({"P2_records": p2, "P3_records": p3, "summary": summary, "flat_sensitivity": flat, "transfer_check": check,
                "maturity_sweep": sweep, "optimism_cost": cost})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "mga057.json").write_text(json.dumps(res, indent=1))
    for s in summary:
        if s["lead"] == "P2" and s["floor"]:
            continue
        if s["lead"] == "P3" and s["service"] != "ground":
            continue
        ls0, ls1 = s["least_set_no_mga"], s["least_set_sourced_mga"]
        print(f"{s['lead']} {s['source'][:6]:6s} R{s['R_m']:<3} {s['weather']:10s} all-axes pay {s['all_axes_payload_kg']:9.1f}  "
              f"MGA {s['all_axes_sourced_mga_kg']:8.1f} -> {s['all_axes_payload_sourced_mga_kg']:9.1f} (est {s['all_axes_payload_estimated_mga_kg']:9.1f})  "
              f"flat-tol {100 * s['flat_tolerable_on_hardware_at_all_axes']:6.2f}%  least0 {ls0['axes'] if ls0 else None} least_mga {ls1['axes'] if ls1 else None}")
    for r in flat:
        print("FLAT", r["lead"], r["R_m"], r["weather"], {k: round(v, 1) for k, v in r.items() if k.startswith("flat_")}, round(100 * r["tolerable_flat"], 2))
    for r in sweep:
        print("TRL", r["lead"], r["R_m"], r["weather"], {k: round(v) for k, v in r.items() if k.startswith("TRL")}, r["least_mature_row_that_floats"])
    for c in cost:
        print("COST", c["lead"], c["R_m"], c["least_set"], round(c["usage_at_zero_payload"], 4), round(c["endpoint_payload_kg"], 1),
              round(c["kg_per_unit_usage"], 1), round(c["sourced_mga_kg"], 1), round(c["usage_needed_with_mga"], 3))
    print("transfer check:", [(c["R_m"], c["weather"], c["mask"], round(c["diff_kg"], 1)) for c in check if c["mask"] in (11, 15)])
    return res


if __name__ == "__main__":
    main()
