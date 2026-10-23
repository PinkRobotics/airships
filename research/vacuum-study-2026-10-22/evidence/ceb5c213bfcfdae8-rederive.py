#!/usr/bin/env python3
"""MAINLINE-009c-5. Be S-200F / HRH-10-32 on the 5 percent mass line.

Formulas are MAINLINE-014's. The search is new because the mass is not the
float ceiling. Nothing here is a certification.
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

R = 10.0
NU = 0.33
P_EXT = 95460.83791390515
LIFT = 4889.442150186961
SYSTEMS = 100.0
JOINT = 0.05
MARGIN = 0.05
AREA = 4.0 * math.pi * R * R
KD_DESIGN = 0.20
KNOCKDOWNS = (0.20, 0.90, 0.1407)


def sha256(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def assert_close(name: str, got: float, expect: float, rel: float = 1e-9) -> None:
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


def modes(young: float, sigma: float, gc: float, ec: float, crush: float, tf: float, tc: float, kd: float, biax: float, coeff: float) -> dict:
    h = tc + tf
    root = math.sqrt(1.0 - NU * NU)
    sigma_0 = young * h / (R * root)
    sigma_crimp = h * h * gc / (2.0 * tf * tc)
    vc = sigma_0 / sigma_crimp
    if vc <= 2.0:
        kc = 1.0 - vc / 4.0
        gamma = kd
        branch = "stiff_or_moderate_core"
    else:
        kc = 1.0 / vc
        gamma = 1.0
        branch = "shear_crimping"
    membrane = P_EXT * R / (4.0 * tf)
    sfs = {
        "global_buckling": (4.0 * gamma * kc * sigma_0 * tf / R) / P_EXT,
        "face_compression": (4.0 * sigma * tf / R) / P_EXT,
        "core_shear_crimping": (4.0 * sigma_crimp * tf / R) / P_EXT,
        "core_crush": crush / (P_EXT / 2.0),
        "face_wrinkling": biax * (coeff * young * math.sqrt(ec * tf / (young * tc))) / membrane,
    }
    ordered = sorted(sfs.items(), key=lambda item: (item[1], item[0]))
    governing = ordered[0][0]
    if branch == "shear_crimping" and abs(sfs["global_buckling"] - sfs["core_shear_crimping"]) <= 1e-9 * max(sfs["core_shear_crimping"], 1e-30):
        governing = "core_shear_crimping"
        ordered = [item for item in ordered if item[0] != "global_buckling"]
    return {
        "tf_m": tf,
        "core_m": tc,
        "h_m": h,
        "Vc": vc,
        "Kc": kc,
        "gamma_d": gamma,
        "branch": branch,
        "sfs": sfs,
        "governing": governing,
        "least_SF": ordered[0][1],
        "second_mode": ordered[1][0],
        "second_SF": ordered[1][1],
    }


def geometry(fraction: float, m_struct: float, rho_f: float, rho_c: float) -> tuple[float, float]:
    tc = (fraction * m_struct) / (AREA * rho_c)
    tf = ((1.0 - fraction) * m_struct) / (2.0 * AREA * rho_f)
    return tf, tc


def search(m_struct: float, young: float, sigma: float, gc: float, ec: float, crush: float, rho_f: float, rho_c: float, biax: float, grid: int, branch_limit: str | None) -> dict:
    best = None
    for step in range(1, grid):
        fraction = step / grid
        tf, tc = geometry(fraction, m_struct, rho_f, rho_c)
        if tf <= 0.0 or tc <= 0.0:
            continue
        ev = modes(young, sigma, gc, ec, crush, tf, tc, KD_DESIGN, biax, 0.33)
        if branch_limit is not None and ev["branch"] != branch_limit:
            continue
        key = (ev["least_SF"], ev["second_SF"])
        if best is None or key > best["key"]:
            best = {"key": key, "fraction": fraction, "ev": ev}
    if best is None:
        raise SystemExit(f"no geometry for {branch_limit}")
    return best


def pack(ev: dict, fraction: float, m_struct: float) -> dict:
    faces = 2.0 * AREA * ev["tf_m"] * 1850.0
    core = AREA * ev["core_m"] * 32.0
    joints = JOINT * (faces + core)
    total = faces + core + joints + SYSTEMS
    return {
        "core_mass_fraction": fraction,
        "tf_m": ev["tf_m"],
        "core_m": ev["core_m"],
        "h_m": ev["h_m"],
        "Vc": ev["Vc"],
        "Kc": ev["Kc"],
        "gamma_d": ev["gamma_d"],
        "branch": ev["branch"],
        "modes_at_0.20_design_wrinkle": ev["sfs"],
        "governing": ev["governing"],
        "least_SF": ev["least_SF"],
        "second_mode": ev["second_mode"],
        "second_SF": ev["second_SF"],
        "masses_kg": {
            "structural": m_struct,
            "faces": faces,
            "core": core,
            "joints": joints,
            "systems": SYSTEMS,
            "total": total,
            "payload": LIFT - total,
            "float_margin": (LIFT - total) / LIFT,
        },
    }


def main() -> None:
    filed = load(R014)
    faces = load(R008)
    prior = load(R007)
    be = next(row for row in faces["candidates_ranked_by_least_SF_P2E"] if row["name"] == "Beryllium S-200F")
    hexcel = next(m for m in prior["materials"] if m["name"] == "Hexcel HRH-10-4.8-32")
    ceiling_row = next(
        row for row in filed["optima"]
        if row["face"] == "Beryllium S-200F" and row["kd"] == 0.2 and row["core_name"] == "Hexcel HRH-10-4.8-32"
    )
    young = be["E_GPa"] * 1e9
    sigma = be["sigma_c_MPa"] * 1e6
    rho_f = float(be["rho"])
    ec = hexcel["Ec_Pa"]
    gc = hexcel["Gc_used_for_compare_Pa"]
    crush = hexcel["compressive_strength_Pa"]
    rho_c = hexcel["density_kg_m3"]
    if (young, sigma, rho_f, ec, gc, crush, rho_c) != (303e9, 283e6, 1850.0, 76e6, 14e6, 1e6, 32.0):
        raise SystemExit("sourced face or core constants moved")
    biax = biaxial_factor()
    assert_close("biaxial", biax, filed["checks"]["biaxial_factor"], 1e-15)

    ceiling = (LIFT - SYSTEMS) / (1.0 + JOINT)
    assert_close("014 structural mass", ceiling, filed["structural_mass_kg"])
    # 014's grid was 8000. Reproduce that row before trusting the 5 percent search.
    reproduced = search(ceiling, young, sigma, gc, ec, crush, rho_f, rho_c, biax, 8000, None)
    assert_close("014 fraction", reproduced["fraction"], ceiling_row["core_mass_fraction"], 1e-12)
    assert_close("014 tf", reproduced["ev"]["tf_m"], ceiling_row["tf_m"], 1e-12)
    assert_close("014 least", reproduced["ev"]["least_SF"], ceiling_row["least_SF"], 1e-12)
    assert_close("014 Vc", reproduced["ev"]["Vc"], ceiling_row["Vc"], 1e-12)

    m_struct = ((1.0 - MARGIN) * LIFT - SYSTEMS) / (1.0 + JOINT)
    either = search(m_struct, young, sigma, gc, ec, crush, rho_f, rho_c, biax, 100001, None)
    moderate = search(m_struct, young, sigma, gc, ec, crush, rho_f, rho_c, biax, 100001, "stiff_or_moderate_core")
    crimp = search(m_struct, young, sigma, gc, ec, crush, rho_f, rho_c, biax, 100001, "shear_crimping")
    winner = either["ev"]
    if winner["branch"] == "shear_crimping":
        other = moderate
    else:
        other = crimp

    levels = {}
    for kd in KNOCKDOWNS:
        ev = modes(young, sigma, gc, ec, crush, winner["tf_m"], winner["core_m"], kd, biax, 0.33)
        if ev["branch"] != winner["branch"]:
            raise SystemExit("branch changed with knockdown")
        levels[format(kd, ".4g")] = {
            "gamma_d": ev["gamma_d"],
            "Kc": ev["Kc"],
            "Vc": ev["Vc"],
            "modes": ev["sfs"],
            "least_SF": ev["least_SF"],
            "governing": ev["governing"],
            "second_mode": ev["second_mode"],
            "second_SF": ev["second_SF"],
        }
    wrinkle_082 = modes(young, sigma, gc, ec, crush, winner["tf_m"], winner["core_m"], KD_DESIGN, biax, 0.82)

    point = pack(winner, either["fraction"], m_struct)
    out = {
        "schema": 1,
        "card": "MAINLINE-009c-5",
        "unit": "vacuum-mainline009-combined-point-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "point": {
            "family": "P2",
            "face": "Beryllium S-200F",
            "core": "Hexcel HRH-10-4.8-32",
            "payload_margin": MARGIN,
            "taken_from": "rpt-mainline014-grok-balanced-sandwich-1019",
            "replaces_margin": "MAINLINE-009c spent the float ceiling. This row is the same face and core on the 5 percent line.",
        },
        "branch": {
            "name": winner["branch"],
            "Vc": winner["Vc"],
            "Kc": winner["Kc"],
            "gamma_d": winner["gamma_d"],
        },
        "optimum": point,
        "levels": levels,
        "wrinkle_coefficient_0.82": {
            "SF_wrinkle": wrinkle_082["sfs"]["face_wrinkling"],
            "least_SF": wrinkle_082["least_SF"],
            "governing": wrinkle_082["governing"],
            "source": "014's theoretical honeycomb coefficient. Hemp and NASA/CR-1999-208994 were not opened.",
        },
        "other_branch": pack(other["ev"], other["fraction"], m_struct),
        "ceiling_check": {
            "fraction": reproduced["fraction"],
            "least_SF": reproduced["ev"]["least_SF"],
            "matches_014": True,
        },
        "nfi": [
            {
                "id": "NFI-CRIMP-STEP",
                "first": True,
                "note": "gamma_d = 1 on the crimp branch is the handbook's step at Vc = 2. At or below 2, gamma_d is the knockdown and Kc is 1 - Vc/4. Above 2, Kc is 1/Vc and gamma_d steps to 1. MAINLINE-018 is testing whether a knockdown applies on the crimp branch. This card does not move the step.",
            },
            {
                "id": "NFI-NU",
                "note": "nu is the aluminium case value 0.33. MAINLINE-008 published no beryllium Poisson ratio.",
            },
            {
                "id": "NFI-FACE-STRENGTH",
                "note": "Face compression uses compressive yield 283 MPa, from 41 ksi. The same 008 line prints tensile yield 37 ksi. Scaling the face factor by 37/41 is the tensile reading.",
            },
            {
                "id": "NFI-STABILISED-EC",
                "note": "Hexcel Ec of 76 MPa is the stabilised compressive modulus. MAINLINE-007 says that column is not the continuum modulus of the wrinkling formula.",
            },
            {
                "id": "NFI-WRINKLE-Q",
                "design": 0.33,
                "theoretical": 0.82,
                "factor_on_Ec": (0.82 / 0.33) ** 2,
                "note": "Design coefficient 0.33 is CR-1457 equation 2.2-14. Theoretical 0.82 is 014's Hemp figure. Those works were not opened here.",
            },
            {
                "id": "NFI-P3",
                "note": "P3 stays PENDING-011b. The SiC frame is not scored.",
            },
        ],
        "later": {"014b_report": None, "018_report": None, "009d": "when 014b or 018 files"},
        "sources": {
            path.name: {"path": str(path), "sha256": sha256(path)[0], "bytes": sha256(path)[1]}
            for path in (R014, R008, R007)
        },
    }
    (ROOT / "POINT.json").write_text(json.dumps(out, indent=1) + "\n")
    ev = winner
    print(json.dumps({
        "branch": ev["branch"],
        "Vc": g(ev["Vc"]),
        "Kc": g(ev["Kc"]),
        "gamma": g(ev["gamma_d"]),
        "tf_m": g(ev["tf_m"]),
        "core_m": g(ev["core_m"]),
        "fraction": g(either["fraction"]),
        "least": g(ev["least_SF"]),
        "governing": ev["governing"],
        "second": ev["second_mode"],
        "second_SF": g(ev["second_SF"]),
        "modes": {k: g(v) for k, v in ev["sfs"].items()},
        "levels_gamma": {k: levels[k]["gamma_d"] for k in levels},
        "levels_global": {k: g(levels[k]["modes"]["global_buckling"]) for k in levels},
        "levels_least": {k: g(levels[k]["least_SF"]) for k in levels},
        "wrinkle_082": g(wrinkle_082["sfs"]["face_wrinkling"]),
        "least_082": g(wrinkle_082["least_SF"]),
        "gov_082": wrinkle_082["governing"],
        "other_branch": other["ev"]["branch"],
        "other_least": g(other["ev"]["least_SF"]),
        "other_Vc": g(other["ev"]["Vc"]),
        "other_gov": other["ev"]["governing"],
        "margin": g(point["masses_kg"]["float_margin"]),
        "payload": g(point["masses_kg"]["payload"]),
        "total": g(point["masses_kg"]["total"]),
        "face_if_37_over_41": g(ev["sfs"]["face_compression"] * 37.0 / 41.0),
    }, indent=1))


if __name__ == "__main__":
    main()
