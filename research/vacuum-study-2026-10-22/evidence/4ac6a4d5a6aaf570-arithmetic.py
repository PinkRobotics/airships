#!/usr/bin/python3
"""MAINLINE-004 named knockdown. Reads sealed JSON. Does not execute predecessor scripts."""
from __future__ import annotations

import json
import math
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
SEALED = Path("unpublished-local-ref:827c7db7d9847d66")
PRIOR = Path("unpublished-local-ref:589528d32156350c")
ORIGIN = 2089283.285637928


def now():
    return datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="microseconds"), time.monotonic()


def get(rows, iid, point):
    for row in rows:
        if row["input_id"] == iid and row["point_id_or_common"] == point:
            return row["value"]
    raise SystemExit(f"missing {iid} {point}")


def g(x):
    return format(x, ".12g")


def main():
    origin = json.loads((ROOT / "ORIGIN.json").read_text())
    if origin["origin_monotonic_s"] != ORIGIN:
        raise SystemExit("origin moved")
    phase1 = json.loads((ROOT / "PHASE1.json").read_text())
    if phase1["status"] != "INSIDE":
        raise SystemExit("phase1")
    p1 = phase1["elapsed_s"]
    inputs = json.loads((SEALED / "INPUTS.json").read_text())
    prior = json.loads((PRIOR / "RESULTS.json").read_text())
    E = get(inputs, "I-E", "common")
    nu = get(inputs, "I-NU", "common")
    R = get(inputs, "I-R", "common")
    kd0 = get(inputs, "I-KD", "P2")
    if abs(kd0 - 0.2) > 1e-15:
        raise SystemExit(f"kd {kd0}")
    p_ext = prior["atmosphere"]["p_ext_Pa"]
    denom = R**2 * math.sqrt(1.0 - nu**2)
    lam_pre = (12.0 * (1.0 - nu**2)) ** 0.25 * 2.0 * math.sin(math.pi / 2.0)

    base = {r["point_id"]: r for r in prior["rows"]}
    comp = prior["comparison_P2A"]
    specs = {
        "P2-A": {
            "tf": comp["tf_m"],
            "core": comp["core_m"],
            "sf0": comp["buckling_SF"],
            "E0": E * comp["E_factor"],
            "strength_sf": comp["strength_SF_QUESTIONABLE"],
        },
        "P2-C": {
            "tf": base["P2-C"]["geometry"]["tf_m"],
            "core": base["P2-C"]["geometry"]["core_m"],
            "sf0": base["P2-C"]["buckling_SF"],
            "E0": base["P2-C"]["E_required_Pa"],
            "strength_sf": base["P2-C"]["strength_SF_QUESTIONABLE"],
        },
        "P2-K": {
            "tf": base["P2-K"]["geometry"]["tf_m"],
            "core": base["P2-K"]["geometry"]["core_m"],
            "sf0": base["P2-K"]["buckling_SF"],
            "E0": base["P2-K"]["E_required_Pa"],
            "strength_sf": base["P2-K"]["strength_SF_QUESTIONABLE"],
        },
        "P2-E": {
            "tf": base["P2-E"]["geometry"]["tf_m"],
            "core": base["P2-E"]["geometry"]["core_m"],
            "sf0": base["P2-E"]["buckling_SF"],
            "E0": base["P2-E"]["E_required_Pa"],
            "strength_sf": base["P2-E"]["strength_SF_QUESTIONABLE"],
        },
    }
    rows = []
    for pid in ("P2-A", "P2-C", "P2-K", "P2-E"):
        spec = specs[pid]
        tf, core = spec["tf"], spec["core"]
        d = core + tf
        p_cl = 4.0 * E * tf * d / denom
        p0 = kd0 * p_cl
        if abs(p0 / p_ext - spec["sf0"]) / spec["sf0"] > 1e-9:
            raise SystemExit(f"prior SF drift {pid}")
        t_eq = (6.0 * tf * d**2) ** (1.0 / 3.0)
        slenderness = R / t_eq
        lam = lam_pre * math.sqrt(slenderness)
        if lam <= 2.0:
            raise SystemExit(f"lambda out of quoted range {pid} {lam}")
        rho = 0.14 + 3.2 / lam**2
        sf = spec["sf0"] * (rho / kd0)
        e_req = spec["E0"] * (kd0 / rho)
        # Identity: new required E equals E * p_ext / (rho * p_cl)
        if abs(e_req - E * p_ext / (rho * p_cl)) / e_req > 1e-12:
            raise SystemExit(f"scaling {pid}")
        rows.append({
            "point_id": pid,
            "dependency": "DEPENDENCY003_ESTIMATE_PENDING_UNA",
            "tag": "QUESTIONABLE",
            "geometry": {"R_m": R, "tf_m": tf, "core_m": core, "d_m": d, "t_eq_m": t_eq},
            "prior_kd": kd0,
            "prior_buckling_SF": spec["sf0"],
            "prior_E_required_Pa": spec["E0"],
            "strength_SF_QUESTIONABLE_unchanged": spec["strength_sf"],
            "lambda": lam,
            "R_over_t_eq": slenderness,
            "knockdown": rho,
            "buckling_pressure_Pa": rho * p_cl,
            "buckling_SF": sf,
            "E_required_Pa": e_req,
            "E_ratio_to_prior": e_req / spec["E0"],
            "scaling": "E_required proportional to 1/knockdown; a larger knockdown lowers required E",
            "held_fixed": "geometry, mass, atmosphere, classical sandwich pressure, strength transfer, omitted core modes",
        })

    utc, mono = now()
    elapsed = mono - ORIGIN
    dur2 = elapsed - p1
    phase2 = {
        "schema": 1, "phase": 2,
        "name": "four_curve_evaluations_revised_sf_and_E",
        "end_utc": utc, "end_monotonic_s": mono, "end_elapsed_s": elapsed,
        "duration_s": dur2, "actual_max_s": 450, "cumulative_max_s": 600,
        "status": "INSIDE" if dur2 <= 450 and elapsed <= 600 else "OVER",
    }
    out = {
        "schema": 1,
        "status": "ESTIMATE_PENDING_UNA",
        "dependency": "DEPENDENCY003_ESTIMATE_PENDING_UNA",
        "card": "MAINLINE-004",
        "curve": phase1["curve"],
        "mapping": phase1["mapping"],
        "rows": rows,
        "checks": {"prior_sf_match": "PASS", "E_scales_as_inverse_knockdown": "PASS", "lambda_above_2": "PASS"},
    }
    if phase2["status"] != "INSIDE":
        (ROOT / "PHASE2.json").write_text(json.dumps(phase2, indent=1) + "\n")
        raise SystemExit(phase2)
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=1) + "\n")
    (ROOT / "PHASE2.json").write_text(json.dumps(phase2, indent=1) + "\n")
    nfis = [
        {"NFI_id": "NFI-KD", "gap": "The 0.14 plus 3.2 over lambda squared form is a text reproduction of NASA SP-8032, not the monograph page. The PDF was not retrieved.", "direction": "Pin the August 1969 page that prints the curve.", "effect": "A different reading of the curve would rescale buckling pressure and required modulus by the same factor."},
        {"NFI_id": "NFI-TRANSFER", "gap": "The curve is monolithic clamped-cap evidence. Phi equals pi and the equivalent thickness are transfers onto a complete sandwich sphere.", "direction": "A sandwich knockdown test or formula at these proportions.", "effect": "The stated buckling safety factor is not a validated sandwich knockdown."},
        {"NFI_id": "NFI-DENSITY", "gap": "Lower core density stays deferred. This unit adds no density point.", "direction": "Leave it to a later card.", "effect": "None inside these four rows."},
        {"NFI_id": "NFI-AL-YIELD-CARRY", "gap": "003 strength safety factors stay QUESTIONABLE and unchanged. Buckling knockdown does not cure yield, shear, wrinkling or crush.", "direction": "Keep the carry parallel.", "effect": "Strength safety factor is not rescaled."},
        {"NFI_id": "NFI-SAND", "gap": "Classical pressure remains the inherited sandwich extrapolation.", "direction": "A published sandwich formula with shear.", "effect": "Required modulus would move if the classical pressure moved."},
        {"NFI_id": "NFI-CRUSH", "gap": "Core crush still has no formula.", "direction": "Unchanged from 003.", "effect": "Crush stays out of the buckling safety factor."},
    ]
    (ROOT / "NFI.json").write_text(json.dumps(nfis, indent=1) + "\n")
    (ROOT / "INPUTS.json").write_text(json.dumps({
        "schema": 1,
        "card": "MAINLINE-004",
        "status": "ESTIMATE_PENDING_UNA",
        "dependency": "DEPENDENCY003_ESTIMATE_PENDING_UNA",
        "curve": phase1["curve"]["equation"],
        "mapping": phase1["mapping"]["thickness"],
        "prior_knockdown": kd0,
        "source_003_results": str(PRIOR / "RESULTS.json"),
    }, indent=1) + "\n")
    lines = [
        "# MAINLINE-004 knockdown card — ESTIMATE_PENDING_UNA",
        "",
        "Dependency label DEPENDENCY003_ESTIMATE_PENDING_UNA. This card does not add a map point and does not wait for Una 003.",
        "",
        "Curve: NASA SP-8032, Weingarten and Seide, August 1969, Buckling of Thin-Walled Doubly Curved Shells. Quoted text form rho = 0.14 + 3.2/lambda^2 for lambda > 2. Lambda uses [12(1-nu^2)]^(1/4) * sqrt(R/t) * 2*sin(phi/2). The monograph PDF was not retrieved. The equation is the text reproduced by Wagner, Huehne and Niemann (2018) equation 5 and by a 2022 comparative study equations 16 and 17.",
        "",
        "Mapping: complete-sphere half-angle pi, and thickness equal to the inherited sandwich bending equivalent (6*tf*d^2)^(1/3). This transfers monolithic cap evidence onto a sandwich. It is QUESTIONABLE and is not validated sandwich data.",
        "",
        "Required face modulus scales as 1/rho. A larger knockdown factor lowers required E. Geometry, mass, atmosphere and the QUESTIONABLE strength safety factors stay at the 003 values.",
        "",
    ]
    for row in rows:
        lines.append(f"## {row['point_id']}")
        lines.append("")
        geo = row["geometry"]
        lines.append(f"Face {g(geo['tf_m'])} m, core {g(geo['core_m'])} m, equivalent thickness {g(geo['t_eq_m'])} m, R/t {g(row['R_over_t_eq'])}, lambda {g(row['lambda'])}.")
        lines.append("")
        lines.append(f"Prior knockdown 0.2, buckling SF {g(row['prior_buckling_SF'])}, required modulus {g(row['prior_E_required_Pa'])} Pa.")
        lines.append("")
        lines.append(f"Curve knockdown {g(row['knockdown'])}. Buckling pressure {g(row['buckling_pressure_Pa'])} Pa. Buckling SF {g(row['buckling_SF'])}. Required modulus {g(row['E_required_Pa'])} Pa, ratio to the 0.2 result {g(row['E_ratio_to_prior'])}.")
        lines.append("")
        lines.append(f"QUESTIONABLE strength SF unchanged at {g(row['strength_SF_QUESTIONABLE_unchanged'])}.")
        lines.append("")
    lines.append("Lower density is not evaluated. Shear, wrinkling and crush stay omitted. Needs-further-investigation rows are in NFI.json.")
    (ROOT / "CARD.md").write_text("\n".join(lines) + "\n")
    utc3, mono3 = now()
    elapsed3 = mono3 - ORIGIN
    dur3 = elapsed3 - elapsed
    phase3 = {
        "schema": 1, "phase": 3, "name": "card_source_input_nfi_comparison",
        "end_utc": utc3, "end_monotonic_s": mono3, "end_elapsed_s": elapsed3,
        "duration_s": dur3, "actual_max_s": 200, "cumulative_max_s": 800,
        "status": "INSIDE" if dur3 <= 200 and elapsed3 <= 800 else "OVER",
    }
    (ROOT / "PHASE3.json").write_text(json.dumps(phase3, indent=1) + "\n")
    if phase3["status"] != "INSIDE":
        raise SystemExit(phase3)
    print(json.dumps({
        "elapsed2": elapsed, "elapsed3": elapsed3,
        "rows": [{k: r[k] for k in ("point_id", "lambda", "knockdown", "buckling_SF", "E_required_Pa", "E_ratio_to_prior")} for r in rows],
    }, indent=1))


if __name__ == "__main__":
    main()
