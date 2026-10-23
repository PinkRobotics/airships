#!/usr/bin/env python3
"""MAINLINE-028 independent check.

Own arithmetic from METHOD.md and the pinned inputs. The owner's
calculate.py is not read or executed. Nothing here is a certification.
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
T0 = datetime.now(ZONE).isoformat(timespec="seconds")

R = 10.0
P = 95460.83791390515
LIFT = 4889.442150186961
RHO_F = 1850.0
E = 290.0e9
NU = 0.33
SIG = 283.0e6
EC = 103421359.3975254
GC = 46884349.59354485
RHO_C = 16.018463373960138
CRUSH = 241316.50526089262
CELL = 0.009524999999999999
GAMMA = 0.5953179642995181
K_W = 0.37068071372338524
TF0 = 0.0008434480441930918
TC0 = 0.02021337638749162
ALLOWANCE = 216.4271448894101

# AF 163-2U, datasheet weight column headed (± .005) lb/ft².
LB = 0.45359237
FT = 0.3048
W_AF = 0.015 * LB / FT ** 2
W_SEAM = 0.07  # owner-selected 70 g/m² scarf film, not the bond-line weight
R_SCARF = 30.0
GAP = 0.0005
RHO_SPLICE = 500.0
SEAL = 0.002
TAU_SCREEN = 10.0e6
A_PANEL = 0.6096
B_PANEL = 1.8288
A4 = 4.0
B4 = 4.0

AREA = 4.0 * math.pi * R * R
N_F = P * R / 4.0
Q = math.sqrt(1.0 - NU * NU)


def half_up(value: float, places: int) -> str:
    quant = Decimal("1").scaleb(-places)
    return str(Decimal(format(value, ".20f")).quantize(quant, rounding=ROUND_HALF_UP))


def biaxial() -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if mid ** 3 + mid > 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


BIAX = biaxial()


def seam_length(tf: float, a: float, b: float) -> float:
    return AREA * (1.0 / (a - R_SCARF * tf) + 1.0 / (b - R_SCARF * tf))


def mu(tf: float, tc: float) -> dict:
    face = 2.0 * tf * math.sqrt(1.0 + R_SCARF ** 2) * W_SEAM
    core = GAP * tc * RHO_SPLICE
    return {
        "face_joint_adhesive": face,
        "core_splice": core,
        "sealing": SEAL,
        "total": face + core + SEAL,
    }


def joining(tf: float, tc: float, a: float, b: float, w_bond: float, primer: float = 0.0) -> dict:
    length = seam_length(tf, a, b)
    per = mu(tf, tc)
    seams = length * per["total"]
    bond = 2.0 * AREA * (w_bond + primer)
    return {
        "bond_kg": bond,
        "seams_kg": seams,
        "total_kg": bond + seams,
        "seam_length_m": length,
        "scarf_overlap_m": R_SCARF * tf,
        "mu": per,
    }


def modes(tf: float, tc: float, weld_retention: float = 1.0, joint_retention: float = 1.0) -> dict:
    h = tc + tf
    stress = N_F / tf
    sigma0 = E * h / (R * Q)
    sig_crimp = h * h * GC / (2.0 * tf * tc)
    vc = sigma0 / sig_crimp
    kc = 1.0 - vc / 4.0 if vc <= 2.0 else 1.0 / vc
    sfs = {
        "global_buckling": GAMMA * kc * sigma0 / stress,
        "face_compression": weld_retention * SIG / stress,
        "core_shear_crimping": sig_crimp / stress,
        "core_crush_inherited": CRUSH / (P / 2.0),
        "face_wrinkling": BIAX * K_W * math.sqrt(E * EC * tf / tc) / stress,
        "intracell_dimpling": E * (tf / CELL) ** 2 / ((1.0 - NU * NU) * stress),
    }
    shear = stress * R_SCARF / (1.0 + R_SCARF ** 2)
    normal = stress / (1.0 + R_SCARF ** 2)
    sfs["projected_scarf_average_shear"] = TAU_SCREEN / shear
    if joint_retention < 1.0:
        sfs["projected_joint_retention"] = joint_retention * SIG / stress
    ordered = sorted(
        (k, v)
        for k, v in sfs.items()
        if k not in ("projected_scarf_average_shear", "projected_braze_average_shear")
    )
    least = min(ordered, key=lambda item: (item[1], item[0]))
    return {
        "sfs": sfs,
        "least_known_mode_SF": least[1],
        "governing": least[0],
        "Vc": vc,
        "Kc": kc,
        "stress_Pa": stress,
        "scarf_shear_Pa": shear,
        "scarf_normal_Pa": normal,
    }


def seam_length_plain(a: float, b: float) -> float:
    return AREA * (1.0 / a + 1.0 / b)


def fixed_eb(tf: float, tc: float, a: float, b: float, w_bond: float) -> float:
    length = seam_length_plain(a, b)
    return 2.0 * AREA * w_bond + length * (GAP * tc * RHO_SPLICE + SEAL)


def fixed_strap(tf: float, tc: float, a: float, b: float, w_bond: float) -> float:
    length = seam_length_plain(a, b)
    width = 2.0 * N_F / TAU_SCREEN
    per = 2.0 * RHO_F * tf * width + 2.0 * W_SEAM * width + GAP * tc * RHO_SPLICE + SEAL
    return 2.0 * AREA * w_bond + length * per


def fixed_braze(tf: float, tc: float, a: float, b: float, w_bond: float) -> float:
    length = AREA * (1.0 / (a - 3.0 * tf) + 1.0 / (b - 3.0 * tf))
    slope = 2.0 * tf * math.sqrt(1.0 + 9.0)
    per = slope * 5.0e-5 * 2700.0 + GAP * tc * RHO_SPLICE + SEAL
    return 2.0 * AREA * w_bond + length * per


# MAINLINE-020 optimistic splice, resized to this geometry.
# 60 mm doubler, 1 mm paste gap, 10 mm² sealant, paste 1100 kg/m³.
# The doubler film is the route bond weight. It replaces the 0.5 mm / 500 kg splice.
W_LEGACY = 0.060
G_LEGACY = 0.001
AB_LEGACY = 1.0e-5
RHO_PASTE = 1100.0


def fixed_legacy(tf: float, tc: float, a: float, b: float, w_bond: float) -> float:
    length = seam_length_plain(a, b)
    per = (
        2.0 * RHO_F * tf * W_LEGACY
        + 2.0 * w_bond * W_LEGACY
        + RHO_PASTE * G_LEGACY * tc
        + RHO_PASTE * AB_LEGACY
    )
    return 2.0 * AREA * w_bond + length * per


def mass_of(kind: str, tf: float, tc: float, a: float, b: float, w_bond: float, primer: float) -> float:
    if kind == "scarf":
        return joining(tf, tc, a, b, w_bond, primer)["total_kg"]
    if kind == "eb":
        return fixed_eb(tf, tc, a, b, w_bond + primer)
    if kind == "strap":
        return fixed_strap(tf, tc, a, b, w_bond + primer)
    if kind == "braze":
        return fixed_braze(tf, tc, a, b, w_bond + primer)
    if kind == "legacy":
        return fixed_legacy(tf, tc, a, b, w_bond + primer)
    raise ValueError(kind)


def solve_s(fraction: float, a: float, b: float, w_bond: float, primer: float = 0.0, weld_retention: float = 1.0, kind: str = "scarf", joint_retention: float = 1.0) -> dict:
    target = 0.95 * LIFT - 100.0
    lo, hi = 2000.0, 4600.0
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        tf = (1.0 - fraction) * mid / (2.0 * AREA * RHO_F)
        tc = fraction * mid / (AREA * RHO_C)
        got = mid + mass_of(kind, tf, tc, a, b, w_bond, primer)
        if got > target:
            hi = mid
        else:
            lo = mid
    structural = 0.5 * (lo + hi)
    tf = (1.0 - fraction) * structural / (2.0 * AREA * RHO_F)
    tc = fraction * structural / (AREA * RHO_C)
    mass_kg = mass_of(kind, tf, tc, a, b, w_bond, primer)
    ev = modes(tf, tc, weld_retention, joint_retention)
    return {
        "core_mass_fraction": fraction,
        "tf_m": tf,
        "tc_m": tc,
        "structural_mass_kg": structural,
        "joining_kg": mass_kg,
        "residual_kg": structural + mass_kg - target,
        "least_SF": ev["least_known_mode_SF"],
        "governing": ev["governing"],
        "evaluation": ev,
    }


def optimise(a: float, b: float, w_bond: float, primer: float = 0.0, weld_retention: float = 1.0, kind: str = "scarf", joint_retention: float = 1.0) -> dict:
    best = None
    for step in range(1, 4001):
        fraction = step / 8000.0
        row = solve_s(fraction, a, b, w_bond, primer, weld_retention, kind, joint_retention)
        if best is None or row["least_SF"] > best["least_SF"]:
            best = row
    span = 3.0 / 8000.0
    lo = max(1.0 / 8000.0, best["core_mass_fraction"] - span)
    hi = min(0.5, best["core_mass_fraction"] + span)
    for _ in range(50):
        left = solve_s(lo + 0.5 * (hi - lo) * 0.5, a, b, w_bond, primer, weld_retention, kind, joint_retention)
        right = solve_s(lo + 0.5 * (hi - lo) * 1.5, a, b, w_bond, primer, weld_retention, kind, joint_retention)
        if left["least_SF"] >= right["least_SF"]:
            hi = lo + 0.5 * (hi - lo) * 1.5
            best = left if left["least_SF"] >= best["least_SF"] else best
        else:
            lo = lo + 0.5 * (hi - lo) * 0.5
            best = right if right["least_SF"] >= best["least_SF"] else best
    return best


def close(name: str, got: float, expect: float, tol: float) -> dict:
    return {
        "name": name,
        "got": got,
        "expect": expect,
        "abs_diff": got - expect,
        "pass": abs(got - expect) <= tol,
    }


def main() -> None:
    base = modes(TF0, TC0)
    stock = joining(TF0, TC0, A_PANEL, B_PANEL, W_AF)
    four = joining(TF0, TC0, A4, B4, W_AF)
    opt = optimise(A_PANEL, B_PANEL, W_AF)
    expect_modes = {
        "global_buckling": 1.0,
        "face_compression": 1.0001831189536448,
        "core_shear_crimping": 2.154663914751214,
        "core_crush_inherited": 5.0558220634629825,
        "face_wrinkling": 1.0,
        "intracell_dimpling": 9.018853684781929,
    }
    rows = []
    for key, expect in expect_modes.items():
        rows.append(close(f"baseline {key}", base["sfs"][key], expect, 1e-9))
    rows.append(close("AF 0.015 kg/m2", W_AF, 0.07323641454574575, 1e-15))
    rows.append(close("stock bond kg", stock["bond_kg"], 184.06318552973724, 1e-9))
    rows.append(close("stock seam m", stock["seam_length_m"], 2847.4618466307857, 1e-6))
    rows.append(close("scarf overlap m", stock["scarf_overlap_m"], 0.025303441325792753, 1e-12))
    rows.append(close("scarf adhesive kg/m", stock["mu"]["face_joint_adhesive"], 0.0035444492846716485, 1e-12))
    rows.append(close("core splice kg/m", stock["mu"]["core_splice"], 0.005053344096872905, 1e-12))
    rows.append(close("stock seams kg", stock["seams_kg"], 30.176812312424374, 1e-9))
    rows.append(close("stock total kg", stock["total_kg"], 214.2399978421616, 1e-9))
    rows.append(close("remaining vs 216.427 kg", ALLOWANCE - stock["total_kg"], 2.1871470472484873, 1e-9))
    rows.append(close("4 m total kg", four["total_kg"], 190.76, 0.006))
    low = 2.0 * AREA * (0.010 * LB / FT ** 2)
    high = 2.0 * AREA * (0.020 * LB / FT ** 2)
    rows.append(close("film tolerance low kg", low, 122.71, 0.006))
    rows.append(close("film tolerance high kg", high, 245.42, 0.006))
    rows.append(close("scarf shear MPa", base["scarf_shear_Pa"] / 1e6, 9.42, 0.005))
    rows.append(close("scarf normal MPa", base["scarf_normal_Pa"] / 1e6, 0.314, 0.0005))
    rows.append(close("reopt least SF", opt["least_SF"], 1.0006407572834681, 5e-6))
    rows.append(close("reopt fraction", opt["core_mass_fraction"], 0.09398025568605683, 2e-5))
    rows.append(close("reopt joining kg", opt["joining_kg"], 214.2500798137841, 1e-3))

    # Headlines that are not inside the 65 route rows.
    both = P * R / 2.0
    rows.append(close("both faces N/m", both, 477304.18956952577, 1e-6))
    rows.append(close("each face N/m", N_F, 238652.09478476288, 1e-6))
    rows.append(close("face stress Pa", N_F / TF0, 282948186.8240931, 1e-4))
    rows.append(close("radial kPa", (P / 2.0) / 1e3, 47.73041895695258, 1e-9))
    rows.append(close("kd 0.2 global", 0.2 / GAMMA, 0.335954921560834, 1e-12))
    rows.append(close("weld retention need", 1.0 / base["sfs"]["face_compression"], 0.9998169145727672, 1e-12))
    rows.append(close("bonds-only g/m2", ALLOWANCE / (2.0 * AREA) * 1000.0, 86.11362482103863, 1e-9))
    rows.append(close("local 0.10 mm normal MPa", (EC * 1.0e-4 / TC0) / 1e6, 0.5116481156583237, 5e-4))
    rows.append(close("local 0.10 mm shear MPa", (GC * 1.0e-4 / TC0) / 1e6, 0.23194714576510672, 5e-4))
    braze_shear = (N_F / TF0) * 3.0 / 10.0
    rows.append(close("braze shear MPa", braze_shear / 1e6, 84.88445604722793, 5e-3))
    strap_w = 2.0 * N_F / TAU_SCREEN
    rows.append(close("strap width m", strap_w, 0.047730418956952576, 1e-12))
    rows.append(close("braze face kg/m", 2.0 * TF0 * math.sqrt(10.0) * 5.0e-5 * 2700.0, 0.000720, 5e-7))
    rows.append(close("fillet 0.10 mm kg/m2", 2700.0 * (1.0e-4) ** 2 * (2.0 / CELL), 0.005669291338582677, 1e-12))
    rows.append(close("fillet 0.20 mm kg/m2", 2700.0 * (2.0e-4) ** 2 * (2.0 / CELL), 0.02267716535433071, 1e-12))

    panels = {
        "small_planning": (0.3048, 0.6096),
        "stock_envelope": (0.6096, 1.8288),
        "1m_projection": (1.0, 1.0),
        "2m_projection": (2.0, 2.0),
        "4m_projection": (4.0, 4.0),
    }
    routes = {
        "lab8_scarf": ("scarf", 0.008, 0.0, 1.0),
        "lab20_scarf": ("scarf", 0.02, 0.0, 1.0),
        "hex70_scarf": ("scarf", 0.07, 0.0, 1.0),
        "af015_scarf": ("scarf", W_AF, 0.0, 1.0),
        "hex100_scarf": ("scarf", 0.1, 0.0, 1.0),
        "af030_scarf": ("scarf", 0.030 * LB / FT ** 2, 0.0, 1.0),
        "af020_tolerance_scarf": ("scarf", 0.020 * LB / FT ** 2, 0.0, 1.0),
        "af015_scarf_primer5": ("scarf", W_AF, 0.005, 1.0),
        "lab8_braze_scarf": ("braze", 0.008, 0.0, 1.0),
        "lab8_eb_eta1": ("eb", 0.008, 0.0, 1.0),
        "lab8_eb_eta08": ("eb", 0.008, 0.0, 0.8),
        "hex70_strap": ("strap", 0.07, 0.0, 1.0),
        "legacy020_optimistic": ("legacy", 0.030 * LB / FT ** 2, 0.0, 1.0),
    }
    owner_path = Path(
        "unpublished-local-ref:5c0646e1ee1e5966"
        "/.ship/work/outputs/vacuum-mainline028-p2-joining-1020/RESULTS.json"
    )
    owner = json.loads(owner_path.read_text(encoding="utf-8"))
    mismatches = []
    legacy_with_screen = []
    compared = 0
    for case in owner["cases"]:
        kind, w_bond, primer, retention = routes[case["route"]]
        a, b = panels[case["panel"]]
        fixed = mass_of(kind, TF0, TC0, a, b, w_bond, primer)
        stored_fixed = case["fixed_geometry"]["total_kg"]
        compared += 1
        if abs(fixed - stored_fixed) > 1e-6:
            mismatches.append(
                {
                    "row": f"{case['panel']}/{case['route']}",
                    "field": "fixed_geometry.total_kg",
                    "card": stored_fixed,
                    "mine": fixed,
                }
            )
        got = optimise(a, b, w_bond, primer, retention, kind)
        stored = case["reoptimized_5pct_margin"]
        compared += 3
        if abs(got["least_SF"] - stored["evaluation"]["least_known_mode_SF"]) > 5e-6:
            mismatches.append(
                {
                    "row": f"{case['panel']}/{case['route']}",
                    "field": "reoptimized.least_known_mode_SF",
                    "card": stored["evaluation"]["least_known_mode_SF"],
                    "mine": got["least_SF"],
                }
            )
        if abs(got["joining_kg"] - stored["joining"]["total_kg"]) > 1e-3:
            mismatches.append(
                {
                    "row": f"{case['panel']}/{case['route']}",
                    "field": "reoptimized.joining.total_kg",
                    "card": stored["joining"]["total_kg"],
                    "mine": got["joining_kg"],
                }
            )
        if abs(got["core_mass_fraction"] - stored["core_mass_fraction"]) > 2e-5:
            mismatches.append(
                {
                    "row": f"{case['panel']}/{case['route']}",
                    "field": "reoptimized.core_mass_fraction",
                    "card": stored["core_mass_fraction"],
                    "mine": got["core_mass_fraction"],
                }
            )
        if case["route"] == "legacy020_optimistic":
            # calculate.py applies 0.9*sigma/stress. METHOD.md and CARD do not state 0.9.
            with_screen = optimise(a, b, w_bond, primer, retention, kind, 0.9)
            screen_gap = abs(with_screen["least_SF"] - stored["evaluation"]["least_known_mode_SF"])
            legacy_with_screen.append(
                {
                    "panel": case["panel"],
                    "stated_least_SF": got["least_SF"],
                    "with_0_9_least_SF": with_screen["least_SF"],
                    "stored_least_SF": stored["evaluation"]["least_known_mode_SF"],
                    "sf_gap_with_screen": screen_gap,
                    "joining_gap_with_screen": with_screen["joining_kg"] - stored["joining"]["total_kg"],
                    "fraction_gap_with_screen": with_screen["core_mass_fraction"] - stored["core_mass_fraction"],
                }
            )
    for bond in owner["bond_masses"]:
        mine = 2.0 * AREA * bond["kg_m2_per_line"]
        compared += 1
        if abs(mine - bond["two_bond_lines_kg"]) > 1e-9:
            mismatches.append(
                {
                    "row": bond["id"],
                    "field": "two_bond_lines_kg",
                    "card": bond["two_bond_lines_kg"],
                    "mine": mine,
                }
            )

    out = {
        "schema": 1,
        "card": "CHECK-028",
        "unit": "vacuum-mainline028-check-1020",
        "started_at": T0,
        "ended_at": datetime.now(ZONE).isoformat(timespec="seconds"),
        "owner_script_executed": False,
        "biaxial_factor": BIAX,
        "film_kg_m2": W_AF,
        "baseline": base,
        "stock_fixed": stock,
        "four_metre_fixed": four,
        "reoptimized_stock_af015": {
            "core_mass_fraction": opt["core_mass_fraction"],
            "tf_m": opt["tf_m"],
            "tc_m": opt["tc_m"],
            "structural_mass_kg": opt["structural_mass_kg"],
            "joining_kg": opt["joining_kg"],
            "least_SF": opt["least_SF"],
            "governing": opt["governing"],
            "residual_kg": opt["residual_kg"],
        },
        "tolerance_band_both_lines_kg": {"lb_0_010": low, "lb_0_020": high},
        "route_comparisons": compared,
        "mismatches": mismatches,
        "legacy_unstated_0_9_screen": legacy_with_screen,
        "checks": rows,
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    failed = [row for row in rows if not row["pass"]]
    print("checks", len(rows), "failed", len(failed))
    for row in rows:
        mark = "PASS " if row["pass"] else "FAIL "
        print(f"{mark}{row['name']}: got {row['got']:.12g} expect {row['expect']:.12g} diff {row['abs_diff']:.3g}")
    print("governing", opt["governing"], "tf", opt["tf_m"], "tc", opt["tc_m"])
    print("4m", four["total_kg"], "low", low, "high", high)
    print("shear SF", base["sfs"]["projected_scarf_average_shear"])
    print("route comparisons", compared, "mismatches", len(mismatches))
    for item in mismatches:
        print("MISMATCH", item["row"], item["field"], "card", item["card"], "mine", item["mine"])


if __name__ == "__main__":
    main()
