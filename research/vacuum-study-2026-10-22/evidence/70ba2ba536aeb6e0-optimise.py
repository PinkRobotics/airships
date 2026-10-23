#!/usr/bin/env python3
"""MAINLINE-009e. Aluminium point at 5 percent under the 018 optimistic curve.

gamma(Vc) = 0.20 + 0.40 * min(Vc, 2), recomputed at every geometry.
Wrinkle coefficients 0.33 and 0.82 are separate searches.
The 014b script is not executed. Nothing here is a certification.
"""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
STARTED = sys.argv[1]

R = 10.0
NU = 0.33
SYSTEMS = 100.0
JOINT = 0.05
P_EXT = 95460.83791390515
LIFT = 4889.442150186961
AREA = 4.0 * math.pi * R * R
M_CEILING = (LIFT - SYSTEMS) / (1.0 + JOINT)
M_FIVE = ((1.0 - 0.05) * LIFT - SYSTEMS) / (1.0 + JOINT)
GRID = 8000
PSI = 6894.757293168361
KSI = PSI * 1000.0
PCF_TO_KG = 0.45359237 / (0.3048**3)
BIAX_FILED = 0.6823278038280194
CEILING_LEAST = 0.668649769509

R008 = Path(
    "unpublished-local-ref:b5eced3bc27be18f"
    "/.ship/work/outputs/vacuum-mainline008-material-gap-1019/RESULTS.json"
)


def g(x: float) -> str:
    return format(x, ".12g")


def biaxial_factor() -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if mid**3 + mid > 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def gamma_optimistic(vc: float) -> float:
    return 0.20 + 0.40 * min(vc, 2.0)


def modes(face, core, tf, tc, biax, k_wrinkle, gamma_of) -> dict:
    h = tc + tf
    root = math.sqrt(1.0 - NU * NU)
    young = face["E_Pa"]
    sigma_0 = young * h / (R * root)
    sigma_crimp = h * h * core["Gc_Pa"] / (2.0 * tf * tc)
    vc = sigma_0 / sigma_crimp
    if vc <= 2.0:
        kc = 1.0 - vc / 4.0
        branch = "stiff_or_moderate_core"
    else:
        kc = 1.0 / vc
        branch = "shear_crimping"
    gamma = gamma_of(vc)
    membrane = P_EXT * R / (4.0 * tf)
    uni = k_wrinkle * young * math.sqrt(core["Ec_Pa"] * tf / (young * tc))
    sigma_d = 2.0 * young / (1.0 - NU * NU) * (tf / core["s_cell_m"]) ** 2
    sfs = {
        "global_buckling": (4.0 * gamma * kc * sigma_0 * tf / R) / P_EXT,
        "face_yield": (4.0 * face["sigma_Pa"] * tf / R) / P_EXT,
        "core_shear_crimping": (4.0 * sigma_crimp * tf / R) / P_EXT,
        "core_crush": core["crush_Pa"] / (P_EXT / 2.0),
        "face_wrinkling": biax * uni / membrane,
        "intracell_dimpling": sigma_d / membrane,
    }
    ordered = sorted(sfs.items(), key=lambda item: (item[1], item[0]))
    if branch == "shear_crimping" and abs(sfs["global_buckling"] - sfs["core_shear_crimping"]) <= 1e-9 * max(
        sfs["core_shear_crimping"], 1e-30
    ):
        ordered = [item for item in ordered if item[0] != "global_buckling"]
    return {
        "tf_m": tf,
        "core_m": tc,
        "h_m": h,
        "Vc": vc,
        "Kc": kc,
        "gamma": gamma,
        "branch": branch,
        "k_wrinkle": k_wrinkle,
        "sfs": sfs,
        "governing": ordered[0][0],
        "least_SF": ordered[0][1],
        "second_mode": ordered[1][0],
        "second_SF": ordered[1][1],
    }


def geometry(face, core, fraction, mass):
    tc = (fraction * mass) / (AREA * core["rho"])
    tf = ((1.0 - fraction) * mass) / (2.0 * AREA * face["rho"])
    return tf, tc


def optimize(face, core, mass, biax, k_wrinkle, gamma_of) -> dict:
    best = None
    for step in range(1, GRID):
        fraction = step / GRID
        tf, tc = geometry(face, core, fraction, mass)
        ev = modes(face, core, tf, tc, biax, k_wrinkle, gamma_of)
        key = (ev["least_SF"], ev["second_SF"])
        if best is None or key > best["key"]:
            best = {"key": key, "fraction": fraction, "ev": ev}
    ev = best["ev"]
    ev["core_mass_fraction"] = best["fraction"]
    ev["core_name"] = core["name"]
    return ev


def main() -> None:
    biax = biaxial_factor()
    if abs(biax - BIAX_FILED) > 1e-12:
        raise SystemExit(f"biaxial {biax}")
    doc = json.loads(R008.read_text())
    face_row = next(row for row in doc["candidates_ranked_by_least_SF_P2E"] if row["name"] == "Beryllium S-200F")
    face = {
        "name": face_row["name"],
        "rho": float(face_row["rho"]),
        "E_Pa": float(face_row["E_GPa"]) * 1.0e9,
        "sigma_Pa": float(face_row["sigma_c_MPa"]) * 1.0e6,
    }
    rho = 1.6 * PCF_TO_KG
    cores = []
    for cell, size in (("1/4", 0.0254 / 4.0), ("3/8", 0.0254 * 3.0 / 8.0)):
        cores.append({
            "name": f"Hexcel CR-III 5056 {cell}-1.6",
            "rho": rho,
            "Ec_Pa": 30.0 * KSI,
            "Gc_Pa": 10.5 * KSI,
            "crush_Pa": 50.0 * PSI,
            "s_cell_m": size,
        })
    # Handbook gamma = 0.20 on the stiff branch, the 014b ceiling, as a formula check only.
    ceiling = optimize(face, cores[0], M_CEILING, biax, 0.33, lambda vc: 0.20 if vc <= 2.0 else 1.0)
    if abs(ceiling["least_SF"] - CEILING_LEAST) > 5e-10:
        raise SystemExit(f"ceiling miss {ceiling['least_SF']}")
    if ceiling["branch"] != "stiff_or_moderate_core":
        raise SystemExit("ceiling left the stiff branch")
    rows = []
    for k_wrinkle in (0.33, 0.82):
        for core in cores:
            ev = optimize(face, core, M_FIVE, biax, k_wrinkle, gamma_optimistic)
            rows.append(ev)
    ended = datetime.now(ZONE).isoformat(timespec="seconds")
    out = {
        "schema": 1,
        "card": "MAINLINE-009e",
        "unit": "vacuum-mainline009-combined-point-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": ended,
        "curve": "optimistic gamma(Vc) = 0.20 + 0.40 * min(Vc, 2), recomputed at every geometry",
        "margin": 0.05,
        "structural_kg": M_FIVE,
        "payload_kg": 0.05 * LIFT,
        "total_kg": 0.95 * LIFT,
        "ceiling_check_least_SF": ceiling["least_SF"],
        "density_kg_m3": rho,
        "optima": rows,
    }
    (ROOT / "POINT.json").write_text(json.dumps(out, indent=1) + "\n")
    print(ended)
    for ev in rows:
        print(
            ev["core_name"],
            "Q",
            ev["k_wrinkle"],
            "frac",
            g(ev["core_mass_fraction"]),
            "tf",
            g(ev["tf_m"]),
            "tc",
            g(ev["core_m"]),
            "Vc",
            g(ev["Vc"]),
            "Kc",
            g(ev["Kc"]),
            "gamma",
            g(ev["gamma"]),
            ev["branch"],
            "least",
            g(ev["least_SF"]),
            ev["governing"],
            "second",
            ev["second_mode"],
            g(ev["second_SF"]),
        )
        for name, value in sorted(ev["sfs"].items()):
            print(" ", name, g(value))


if __name__ == "__main__":
    main()
