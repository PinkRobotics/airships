#!/usr/bin/env python3
"""MAINLINE-009c. Take MAINLINE-014's beryllium / HRH-10 row as the P2 point.

The thicknesses stay where 014 left them. This script does not search again
and does not score the P3 frame. On the shear-crimping branch gamma_d is 1,
so the same Kc applies at every knockdown and the global factor does not scale.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STARTED = datetime.now().astimezone().isoformat(timespec="seconds")

SEAT = Path("unpublished-local-ref:7a5bf1cec24b249e")
R014 = (
    SEAT
    / "ref-2543c559b19ffce7dfdd/.ship/work/outputs"
    / "vacuum-mainline014-balanced-sandwich-1019/RESULTS.json"
)
R008 = (
    SEAT
    / "ref-454ea8a33cb537f77738/.ship/work/outputs"
    / "vacuum-mainline008-material-gap-1019/RESULTS.json"
)
R007 = (
    SEAT
    / "ref-1a533823b6613bf7ff73/.ship/work/outputs"
    / "vacuum-mainline007-core-trade-1019/RESULTS.json"
)
P3 = (
    SEAT
    / "ref-1a533823b6613bf7ff73/.ship/work/outputs"
    / "vacuum-mainline009-combined-point-1019/P3-PENDING.json"
)

R = 10.0
NU = 0.33
P_EXT = 95460.83791390515
LIFT = 4889.442150186961
SYSTEMS = 100.0
JOINT = 0.05
KD = (0.20, 0.90, 0.1407)


def sha256(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def assert_close(name: str, got: float, expect: float, rel: float = 1e-12) -> None:
    scale = max(abs(expect), 1e-30)
    err = abs(got - expect) / scale
    if err > rel:
        raise SystemExit(f"{name} rel {err:.3e}: got {got!r} expect {expect!r}")


def g(x: float) -> str:
    return format(float(x), ".12g")


def biaxial_factor() -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if mid**3 + mid > 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def main() -> None:
    filed = load(R014)
    faces = load(R008)
    prior = load(R007)
    pending = load(P3)
    be = next(row for row in faces["candidates_ranked_by_least_SF_P2E"] if row["name"] == "Beryllium S-200F")
    hexcel = next(m for m in prior["materials"] if m["name"] == "Hexcel HRH-10-4.8-32")
    point = next(
        row for row in filed["optima"]
        if row["face"] == "Beryllium S-200F" and row["kd"] == 0.2 and row["core_name"] == "Hexcel HRH-10-4.8-32"
    )
    twin = next(
        row for row in filed["optima"]
        if row["face"] == "Beryllium S-200F" and row["kd"] == 0.1407 and row["core_name"] == "Hexcel HRH-10-4.8-32"
    )
    cnt = next(
        row for row in filed["optima"]
        if row["face"].startswith("CNT") and row["kd"] == 0.2
    )

    tf = point["tf_m"]
    tc = point["core_m"]
    h = tc + tf
    E = be["E_GPa"] * 1e9
    sigma = be["sigma_c_MPa"] * 1e6
    rho_f = float(be["rho"])
    ec = hexcel["Ec_Pa"]
    gc = hexcel["Gc_used_for_compare_Pa"]
    crush = hexcel["compressive_strength_Pa"]
    if ec != 76.0e6 or gc != 14.0e6 or crush != 1.0e6:
        raise SystemExit("Hexcel sourced constants moved")
    root = math.sqrt(1.0 - NU * NU)
    sigma_0 = E * h / (R * root)
    sigma_crimp = h * h * gc / (2.0 * tf * tc)
    vc = sigma_0 / sigma_crimp
    if vc <= 2.0:
        raise SystemExit("014's beryllium row is not on the crimp branch")
    kc = 1.0 / vc
    gamma = 1.0
    assert_close("Vc", vc, point["Vc"])
    assert_close("Kc", kc, point["Kc"])
    assert_close("h", h, point["h_m"])

    def classical(kd: float) -> float:
        return (kd * 4.0 * tf * h * E / (R * R * root)) / P_EXT

    # gamma_d is 1 on this branch at every knockdown. Kc is already 1/Vc.
    # Stated global = crimp, and it does not scale with kd.
    stated = gamma * kc * (4.0 * sigma_0 * tf / R) / P_EXT
    crimp_sf = (4.0 * sigma_crimp * tf / R) / P_EXT
    face = (4.0 * sigma * tf / R) / P_EXT
    crush_sf = crush / (P_EXT / 2.0)
    membrane = P_EXT * R / (4.0 * tf)
    bx = biaxial_factor()
    wrinkle_033 = bx * (0.33 * E * math.sqrt(ec * tf / (E * tc))) / membrane
    wrinkle_082 = bx * (0.82 * E * math.sqrt(ec * tf / (E * tc))) / membrane
    assert_close("global", stated, point["sfs"]["global_buckling"])
    assert_close("crimp", crimp_sf, point["sfs"]["core_shear_crimping"])
    assert_close("global equals crimp", stated, crimp_sf, 1e-12)
    assert_close("face", face, point["sfs"]["face_yield"])
    assert_close("crush", crush_sf, point["sfs"]["core_crush"])
    assert_close("wrinkle 0.33", wrinkle_033, point["sfs"]["face_wrinkling"])
    assert_close("wrinkle 0.82", wrinkle_082, point["wrinkle_SF_theoretical"])
    assert_close("twin least", twin["least_SF"], point["least_SF"])
    if round(stated, 3) != 0.685:
        raise SystemExit(f"least does not round to 0.685: {stated}")

    area = 4.0 * math.pi * R * R
    faces_kg = 2.0 * area * tf * rho_f
    core_kg = area * tc * hexcel["density_kg_m3"]
    joints = JOINT * (faces_kg + core_kg)
    total = faces_kg + core_kg + joints + SYSTEMS
    payload = LIFT - total
    margin = payload / LIFT
    ceiling = (LIFT - SYSTEMS) / (1.0 + JOINT)
    assert_close("014 structural mass", ceiling, filed["structural_mass_kg"])

    modes = {
        "global_buckling": stated,
        "face_compression": face,
        "core_crush": crush_sf,
        "core_shear_crimping": crimp_sf,
        "face_wrinkling": wrinkle_033,
    }
    # Global and crimp are the same pressure. Wrinkling is the next one.
    least = min(modes.values())
    levels = {}
    for kd in KD:
        row = dict(modes)
        levels[format(kd, ".4g")] = {
            "gamma_d": gamma,
            "Kc": kc,
            "modes": row,
            "least_SF": least,
            "governing": "core_shear_crimping",
            "tied_with": "global_buckling",
            "note": "Vc>2 sets gamma_d to 1. The knockdown does not enter.",
        }
    levels_082 = dict(modes)
    levels_082["face_wrinkling"] = wrinkle_082
    least_082 = min(levels_082.values())

    out = {
        "schema": 1,
        "card": "MAINLINE-009c",
        "unit": "vacuum-mainline009-combined-point-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "point": {
            "family": "P2",
            "face": be["name"],
            "face_tag": be["tag"],
            "face_source": be["source"],
            "core": "Hexcel HRH-10-4.8-32",
            "core_tag": "QUESTIONABLE",
            "core_source": hexcel["source"],
            "taken_from": "rpt-mainline014-grok-balanced-sandwich-1019",
            "why_this_row": "The order names this QUESTIONABLE row. CNT-yarn is higher and is PROJECTION.",
            "cnt_not_the_point": {
                "face": cnt["face"],
                "tag": cnt["face_tag"],
                "least_SF": cnt["least_SF"],
                "core": cnt["core_name"],
            },
        },
        "branch": {
            "name": "shear_crimping",
            "Vc": vc,
            "Kc": kc,
            "gamma_d": gamma,
            "rule": "Vc>2 gives Kc=1/Vc and gamma_d=1. Stated global equals crimp at every knockdown. Do not scale it by kd/0.20.",
            "sigma_0_Pa": sigma_0,
            "sigma_crimp_Pa": sigma_crimp,
        },
        "geometry": {"tf_m": tf, "core_m": tc, "separation_m": h, "R_m": R},
        "float": {
            "lift_kg": LIFT,
            "faces_kg": faces_kg,
            "core_kg": core_kg,
            "joints_kg": joints,
            "systems_kg": SYSTEMS,
            "total_kg": total,
            "payload_kg": payload,
            "float_margin": margin,
            "ceiling": "014's structural mass is (lift-100)/1.05. This row spends that ceiling. MAINLINE-009's 5 percent margin is not this point.",
        },
        "stated_modes_every_knockdown": levels,
        "honeycomb_coefficient": {
            "design": 0.33,
            "design_source": "NASA CR-1457 equation 2.2-14",
            "theoretical": 0.82,
            "theoretical_source": "MAINLINE-014 names 0.82 from Hemp, as quoted for anti-plane cores in NASA/CR-1999-208994. Those works were not opened here.",
            "SF_wrinkle_design": wrinkle_033,
            "SF_wrinkle_theoretical": wrinkle_082,
            "least_SF_design": least,
            "least_SF_theoretical": least_082,
            "governing_theoretical": "core_shear_crimping",
            "Ec_scale_factor": (0.82 / 0.33) ** 2,
        },
        "reaches_SF_1_in_every_mode": least >= 1.0,
        "factor_to_SF_1": 1.0 / least,
        "nfi": [
            {
                "id": "NFI-CRIMP-BRANCH",
                "note": "Vc is above 2, so Kc is 1/Vc and gamma_d is 1 at every knockdown. Stated global equals crimp. The factor does not scale with kd.",
            },
            {
                "id": "NFI-NU",
                "note": "nu is the aluminium case value 0.33. MAINLINE-008 published no beryllium Poisson ratio.",
            },
            {
                "id": "NFI-FACE-STRENGTH",
                "note": "The stated face mode uses compressive yield 283 MPa, which MAINLINE-008 takes from 41 ksi. The same line prints tensile yield 37 ksi. Scaling the face factor by 37/41 leaves it above the crimp pair. QUESTIONABLE.",
            },
            {
                "id": "NFI-STABILISED-EC",
                "note": "Hexcel Ec of 76 MPa is the stabilised compressive modulus. MAINLINE-007 says that column is not the continuum modulus of the wrinkling formula. Equation 2.2-14 uses it here because 014 did.",
            },
            {
                "id": "NFI-WRINKLE-Q",
                "optimistic": 0.82,
                "design": 0.33,
                "factor_on_Ec": (0.82 / 0.33) ** 2,
                "note": "Honeycomb design coefficient 0.33 is CR-1457 equation 2.2-14. The theoretical 0.82 is the value 014 names from Hemp via NASA/CR-1999-208994. Those works were not opened. The least factor does not move, because crimp governs.",
            },
            {
                "id": "NFI-CRUSH",
                "note": "Core crush is compressive strength over p/2. Thickness does not enter.",
            },
            {
                "id": "NFI-MASS",
                "note": "This row uses 014's ceiling, (lift-100)/1.05. Float margin is 0. MAINLINE-009's 5 percent margin is a different point.",
            },
            {
                "id": "NFI-CNT",
                "note": "CNT-yarn's least factor is higher and the face tag is PROJECTION. It is not this point.",
            },
            {
                "id": "NFI-013",
                "note": "MAINLINE-013 has not filed. Scaled cores are not this row.",
            },
            {
                "id": "NFI-ALHC",
                "note": "Plascore aluminium honeycomb has no Ec. Wrinkling is unscored, so those rows stay out.",
            },
        ],
        "sic_divinycell_009b_least_SF": 0.23515931324953654,
        "p3": {"mark": "PENDING-011b", "scored": False, "rows": pending["rows"]},
        "later": {"014b_report": None, "009d": "when 014b files"},
        "sources": {
            path.name: {"path": str(path), "sha256": sha256(path)[0], "bytes": sha256(path)[1]}
            for path in (R014, R008, R007, P3)
        },
    }
    (ROOT / "POINT.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({
        "Vc": g(vc),
        "Kc": g(kc),
        "tf_mm": g(tf * 1e3),
        "core_mm": g(tc * 1e3),
        "global": g(stated),
        "face": g(face),
        "crush": g(crush_sf),
        "wrinkle_033": g(wrinkle_033),
        "wrinkle_082": g(wrinkle_082),
        "least_082": g(least_082),
        "margin": g(margin),
        "payload": g(payload),
        "total": g(total),
        "factor": g(1.0 / least),
        "Ec_scale": g((0.82 / 0.33) ** 2),
        "cnt": g(cnt["least_SF"]),
        "classical_0.20": g(classical(0.20)),
        "wrong_scale_0.90": g(stated * 0.90 / 0.20),
    }, indent=1))


if __name__ == "__main__":
    main()
