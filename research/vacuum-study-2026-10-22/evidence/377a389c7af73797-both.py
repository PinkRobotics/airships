#!/usr/bin/env python3
"""MAINLINE-009d ordered carry. Both 5 percent points.

Aramid numbers are the filed 009c-5 row. The aluminium point is re-optimised
on the 5 percent mass line with the 014b formulas. The 014b script is not
executed. Nothing here is a certification.
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
K_HONEY = 0.33
K_THEORY = 0.82
BIAX_FILED = 0.6823278038280194
CEILING_LEAST = 0.668649769509

R008 = Path(
    "unpublished-local-ref:b5eced3bc27be18f"
    "/.ship/work/outputs/vacuum-mainline008-material-gap-1019/RESULTS.json"
)
POINT = Path(
    "unpublished-local-ref:7f7c51a246885c2d"
    "/.ship/work/outputs/vacuum-mainline009c5-margin-five-percent-1019/POINT.json"
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


def modes(face: dict, core: dict, tf: float, tc: float, kd: float, biax: float) -> dict:
    h = tc + tf
    root = math.sqrt(1.0 - NU * NU)
    young = face["E_Pa"]
    sigma_0 = young * h / (R * root)
    sigma_crimp = h * h * core["Gc_Pa"] / (2.0 * tf * tc)
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
    uni = K_HONEY * young * math.sqrt(core["Ec_Pa"] * tf / (young * tc))
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
    if branch == "shear_crimping":
        if abs(sfs["global_buckling"] - sfs["core_shear_crimping"]) <= 1e-9 * max(sfs["core_shear_crimping"], 1e-30):
            ordered = [item for item in ordered if item[0] != "global_buckling"]
    theo = K_THEORY * young * math.sqrt(core["Ec_Pa"] * tf / (young * tc))
    return {
        "tf_m": tf,
        "core_m": tc,
        "h_m": h,
        "Vc": vc,
        "Kc": kc,
        "gamma": gamma,
        "branch": branch,
        "sfs": sfs,
        "governing": ordered[0][0],
        "least_SF": ordered[0][1],
        "second_mode": ordered[1][0],
        "second_SF": ordered[1][1],
        "wrinkle_SF_coefficient_0.82": biax * theo / membrane,
    }


def geometry(face: dict, core: dict, fraction: float, mass: float) -> tuple[float, float]:
    tc = (fraction * mass) / (AREA * core["rho"])
    tf = ((1.0 - fraction) * mass) / (2.0 * AREA * face["rho"])
    return tf, tc


def optimize(face: dict, core: dict, mass: float, kd: float, biax: float) -> dict:
    best = None
    for step in range(1, GRID):
        fraction = step / GRID
        tf, tc = geometry(face, core, fraction, mass)
        ev = modes(face, core, tf, tc, kd, biax)
        key = (ev["least_SF"], ev["second_SF"])
        if best is None or key > best["key"]:
            best = {"key": key, "fraction": fraction, "ev": ev}
    ev = best["ev"]
    ev["core_mass_fraction"] = best["fraction"]
    ev["core_name"] = core["name"]
    return ev


def kd_to_one(ev: dict) -> dict:
    """Global scales with kd only on the stiff branch. Other modes do not."""
    if ev["branch"] != "stiff_or_moderate_core":
        raise SystemExit("aluminium point left the stiff branch")
    global_sf = ev["sfs"]["global_buckling"]
    kd = ev["gamma"]
    others = {name: value for name, value in ev["sfs"].items() if name != "global_buckling"}
    blocking = min(others.items(), key=lambda item: (item[1], item[0]))
    kd_global = kd * (1.0 / global_sf)
    if blocking[1] >= 1.0:
        reached = True
        kd_least = kd_global
        blocker = None
    else:
        reached = False
        kd_least = None
        blocker = {"mode": blocking[0], "SF": blocking[1]}
    return {
        "kd_that_brings_global_to_1": kd_global,
        "least_reaches_1": reached,
        "kd_that_brings_least_to_1": kd_least,
        "mode_that_stays_below_1": blocker,
    }


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
        "tag": face_row["tag"],
    }
    if face["rho"] != 1850.0 or face["E_Pa"] != 303.0e9 or face["sigma_Pa"] != 283.0e6:
        raise SystemExit("beryllium properties moved")
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
            "tag": "QUESTIONABLE",
        })
    ceiling = [optimize(face, core, M_CEILING, 0.20, biax) for core in cores]
    for row in ceiling:
        if abs(row["least_SF"] - CEILING_LEAST) > 5e-10:
            raise SystemExit(f"ceiling miss {row['core_name']} {row['least_SF']}")
        if row["branch"] != "stiff_or_moderate_core" or row["governing"] != "global_buckling":
            raise SystemExit(f"ceiling branch {row['core_name']} {row['branch']} {row['governing']}")
    five = [optimize(face, core, M_FIVE, 0.20, biax) for core in cores]
    if five[0]["branch"] != "stiff_or_moderate_core":
        raise SystemExit("5 percent aluminium left the stiff branch")
    # Modes other than dimpling must tie. Cell size is the only difference.
    for key in ("global_buckling", "face_yield", "core_shear_crimping", "core_crush", "face_wrinkling"):
        if abs(five[0]["sfs"][key] - five[1]["sfs"][key]) > 1e-9:
            raise SystemExit(f"cells diverged on {key}")
    aramid = json.loads(POINT.read_text())
    ended = datetime.now(ZONE).isoformat(timespec="seconds")
    out = {
        "schema": 1,
        "card": "MAINLINE-009d",
        "unit": "vacuum-mainline009-combined-point-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": ended,
        "mass": {
            "margin": 0.05,
            "structural_kg": M_FIVE,
            "total_kg": (1.0 - 0.05) * LIFT,
            "payload_kg": LIFT - (1.0 - 0.05) * LIFT,
        },
        "aramid_crimp_branch": {
            "source": "rpt-ref-656730310661fdf86af6",
            "face": "Beryllium S-200F",
            "core": "Hexcel HRH-10-4.8-32",
            "tf_m": aramid["optimum"]["tf_m"],
            "core_m": aramid["optimum"]["core_m"],
            "Vc": aramid["optimum"]["Vc"],
            "Kc": aramid["optimum"]["Kc"],
            "gamma": aramid["optimum"]["gamma_d"],
            "branch": aramid["optimum"]["branch"],
            "modes": aramid["optimum"]["modes_at_0.20_design_wrinkle"],
            "least_SF": aramid["optimum"]["least_SF"],
            "governing": aramid["optimum"]["governing"],
            "note": "Handbook gamma is 1 on this branch. The 018 conservative curve is not this carry.",
        },
        "aluminium_stiff_branch": {
            "source": "014b formulas, re-optimised at 5 percent. Ceiling check reproduced 0.668649769509.",
            "face": "Beryllium S-200F",
            "cores": five,
            "kd_statement": kd_to_one(five[0]),
            "Gc": "W shear, 10.5 ksi, the lower modulus",
            "density_kg_m3": rho,
        },
    }
    (ROOT / "POINT.json").write_text(json.dumps(out, indent=1) + "\n")
    row = five[0]
    print(ended)
    print("rho", g(rho), "tf", g(row["tf_m"]), "tc", g(row["core_m"]), "fraction", g(row["core_mass_fraction"]))
    print("Vc", g(row["Vc"]), "Kc", g(row["Kc"]), "gamma", g(row["gamma"]), row["branch"])
    print("least", g(row["least_SF"]), row["governing"], "second", row["second_mode"], g(row["second_SF"]))
    for name, value in sorted(row["sfs"].items()):
        print(" ", name, g(value))
    print("dimple 3/8", g(five[1]["sfs"]["intracell_dimpling"]))
    print("wrinkle 0.82", g(row["wrinkle_SF_coefficient_0.82"]))
    statement = out["aluminium_stiff_branch"]["kd_statement"]
    print("kd_global_1", g(statement["kd_that_brings_global_to_1"]), "least_reaches", statement["least_reaches_1"])
    if statement["mode_that_stays_below_1"]:
        print("blocker", statement["mode_that_stays_below_1"]["mode"], g(statement["mode_that_stays_below_1"]["SF"]))


if __name__ == "__main__":
    main()
