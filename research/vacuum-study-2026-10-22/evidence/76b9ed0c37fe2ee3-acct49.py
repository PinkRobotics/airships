#!/usr/bin/env python3
"""049: run 040's whole bill (model49, 040's model generalised) for one face, core, bond and joint at R 15, 20, 30,
ISA and optimistic weather, actual joining and 040's retained 5 percent floor."""
import math

import model49 as M

AXES = {"gamma": "gamma", "Q": "Q", "face_compression_and_E": "face tuple", "film": "film"}


def summary(point, today):
    """The coefficients at the least point and their multipliers on today's values."""
    if point is None:
        return None
    pr = point["properties"]
    return {"gamma": pr["gamma"], "gamma_x": pr["gamma"] / today["gamma"],
            "Q": pr["Q"], "Q_x": pr["Q"] / today["Q"],
            "E_Pa": pr["E_Pa"], "E_x": pr["E_Pa"] / today["E"],
            "Fcy_Pa": pr["Fcy_Pa"], "Fcy_x": pr["Fcy_Pa"] / today["Fcy"],
            "film_kg_m2": pr["film_kg_m2_interface"], "film_x": today["film"] / pr["film_kg_m2_interface"],
            "Vc": pr["Vc"], "tf_m": point["geometry"]["tf_m"], "tc_m": point["geometry"]["tc_m"],
            "faces_kg": point["bill_kg"]["faces"], "core_kg": point["bill_kg"]["core"],
            "payload_kg": point["signed_payload_kg"], "least_SF": point["least_shell_and_thermal_SF"],
            "binding": sorted(k for k, v in point["modes"].items() if v < 1 + 2e-6),
            "bill_kg": point["bill_kg"]}


def today_values(face):
    return {"gamma": .2, "Q": .33, "E": face["E_today_Pa"], "Fcy": face["strength_today_Pa"],
            "film": M.I["film"]["baseline_kg_m2_interface"]}


def row(label, r, w, fl, s, today):
    """One account row: the least set and the mask 11, 15 and 0 endpoints (and the mask 15 endpoint's bill)."""
    res = M.least(r, s)
    ep = {t["mask"]: t["solution"] for t in res["endpoint_trials"]}
    lp = res["least"]
    e15 = ep[15]
    return {"case": label, "R_m": r, "weather": w, "floor": fl,
            "least_axes": None if lp is None else [AXES[a] for a in lp["selected_axes"]],
            "least_usage": None if lp is None else lp["usage"],
            "least": summary(lp, today),
            "endpoint_028b_kg": None if ep[11] is None else ep[11]["signed_payload_kg"],
            "endpoint_all_kg": None if e15 is None else e15["signed_payload_kg"],
            "endpoint_today_kg": None if ep[0] is None else ep[0]["signed_payload_kg"],
            "faces_at_028b_endpoint_kg": None if ep[11] is None else ep[11]["bill_kg"]["faces"],
            "faces_at_all_endpoint_kg": None if e15 is None else e15["bill_kg"]["faces"],
            "endpoint_028b_binding": None if ep[11] is None else sorted(
                k for k, v in ep[11]["modes"].items() if v < 1 + 2e-6),
            "endpoint_all_binding": None if e15 is None else sorted(
                k for k, v in e15["modes"].items() if v < 1 + 2e-6),
            "endpoint_all_geometry": None if e15 is None else e15["geometry"],
            "endpoint_all_bill_kg": None if e15 is None else e15["bill_kg"],
            "endpoint_all_joining": None if e15 is None else e15["actual_joining"],
            "endpoint_all_modes": None if e15 is None else e15["modes"],
            "endpoint_all_vacuum": None if e15 is None else {k: e15["vacuum"][k] for k in (
                "added_material_water_kg", "desorbed_24h_kg", "pressure_SF")},
            "lift_kg": M.L0 * (r / 10) ** 3}


def account(label, face, core, nu, mat, thermal=None, radii=(15, 20, 30), weathers=("ISA", "optimistic"),
            floors=(False, True), cure_K=None, extra=None):
    M.set_material(face=face, core=core, thermal=thermal, **mat)
    today = today_values(face)
    rows = []
    for r in radii:
        for w in weathers:
            for fl in floors:
                kw = dict(weather=w, floor=fl, pad="heavy70", vented=True, nu=nu)
                if cure_K is not None:
                    kw["cure_temperature_K"] = cure_K
                if extra:
                    kw.update(extra)
                rows.append(row(label, r, w, fl, M.Settings(**kw), today))
    return rows
