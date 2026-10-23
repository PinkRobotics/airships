#!/usr/bin/env python3
"""MAINLINE-018b narrowed. Confirm Figure 15 pressures, face-bending share, lead, run size.

The 018b script is not re-executed. Nothing here is a certification.
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

E_FACE = 210.0e9
NU = 0.33
E_CORE = 0.04e9
GC = E_CORE / 2.0
T_CORE = 3.10e-3
T_OUTER = 0.42e-3
R_OUTER_PAPER = 42.80e-3
LEAD_LEAST = 0.650411843681
LEAD_CORE = 0.0206423058669
LEAD_R = 10.0

# Printed on EUCASS 2023-367 Figure 15 bars, page 10.
FIGURE_15 = {
    "flat": {"linear_perfect_Pa": 27.53e6, "imperfect_Pa": 6.03e6},
    "dimple": {"linear_perfect_Pa": 27.56e6, "imperfect_Pa": 5.63e6},
}
# Section text beside Figures 9 and 12. Not printed on Figure 15.
NONLINEAR_PERFECT = {"flat": 12.45e6, "dimple": 12.44e6}

# Published mesh, section 2.2.
FOAM_ELEMENT_M = 1.54e-3
SHEET_ELEMENT_M = 1.04e-3
# Allowance for an implicit buckle plus one arc-length step. Not a measured ABAQUS footprint.
BYTES_PER_DOF = 10_000
FREE_RAM_BYTES = 44 * (1024**3)


def g(x: float) -> str:
    return format(x, ".12g")


def shell(name: str, t_inner: float) -> dict:
    h = T_CORE + 0.5 * (T_OUTER + t_inner)
    t_sum = T_OUTER + t_inner
    r_mid = R_OUTER_PAPER - 0.5 * (T_OUTER + T_CORE + t_inner)
    root = math.sqrt(1.0 - NU * NU)
    sigma_0 = E_FACE * h / (r_mid * root)
    sigma_crimp = h * h * GC / (t_sum * T_CORE)
    p_crimp = 2.0 * h * h * GC / (r_mid * T_CORE)
    p_classical = 2.0 * sigma_0 * t_sum / r_mid
    # Distance between face middle surfaces is h. Neutral axis from the outer-face middle.
    y_na = t_inner * h / t_sum
    d_outer = y_na
    d_inner = h - y_na
    factor = E_FACE / (1.0 - NU * NU)
    d_own = factor / 12.0 * (T_OUTER**3 + t_inner**3)
    d_steiner = factor * (T_OUTER * d_outer**2 + t_inner * d_inner**2)
    share = d_own / (d_own + d_steiner)
    linear = FIGURE_15[name]["linear_perfect_Pa"]
    imperfect = FIGURE_15[name]["imperfect_Pa"]
    gamma = imperfect / p_crimp
    return {
        "name": name,
        "t_inner_m": t_inner,
        "h_m": h,
        "R_middle_m": r_mid,
        "R_over_tc": r_mid / T_CORE,
        "Vc": sigma_0 / sigma_crimp,
        "p_crimp_Pa": p_crimp,
        "p_classical_Pa": p_classical,
        "gamma": gamma,
        "lead_times_gamma": LEAD_LEAST * gamma,
        "face_bending_share_of_flexural_rigidity": share,
        "linear_over_crimp": linear / p_crimp,
        "nonlinear_perfect_over_crimp": NONLINEAR_PERFECT[name] / p_crimp,
        "rigidity_share_times_crimp_pressure_Pa": share * p_crimp,
    }


def mesh(r_mid: float, t_inner: float) -> dict:
    t_sum = T_OUTER + t_inner
    r_outer = r_mid + 0.5 * (t_sum + T_CORE)
    r_foam = r_outer - T_OUTER - 0.5 * T_CORE
    r_sheet = r_outer - 0.5 * T_OUTER
    foam_volume = 2.0 * math.pi * r_foam**2 * T_CORE
    sheet_area = 2.0 * math.pi * r_sheet**2
    n_solid = foam_volume / FOAM_ELEMENT_M**3
    n_sheet = sheet_area / SHEET_ELEMENT_M**2
    # One node per solid element, two node layers per continuum shell, 3 dof.
    dof = 3.0 * (n_solid + 4.0 * n_sheet)
    ram = dof * BYTES_PER_DOF
    return {
        "R_middle_m": r_mid,
        "R_over_tc": r_mid / T_CORE,
        "Vc_flat_thicknesses_held": shell("flat", T_OUTER)["Vc"] * (shell("flat", T_OUTER)["R_middle_m"] / r_mid),
        "solid_elements": n_solid,
        "sheet_elements_one_face": n_sheet,
        "sheet_elements_two_faces": 2.0 * n_sheet,
        "elements": n_solid + 2.0 * n_sheet,
        "dof_allowance": dof,
        "ram_bytes_at_10kB_per_dof": ram,
        "fits_free_ram": ram < FREE_RAM_BYTES,
    }


def main() -> None:
    rows = {
        "flat": shell("flat", 0.42e-3),
        "dimple": shell("dimple", 0.40e-3),
    }
    paper = mesh(rows["flat"]["R_middle_m"], T_OUTER)
    rt40 = mesh(40.0 * T_CORE, T_OUTER)
    rt100 = mesh(100.0 * T_CORE, T_OUTER)
    ended = datetime.now(ZONE).isoformat(timespec="seconds")
    out = {
        "schema": 1,
        "card": "MAINLINE-018b-narrowed",
        "unit": "vacuum-mainline018b-crimp-gamma-measured-1020",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": ended,
        "figure_15": "EUCASS 2023-367 page 10 prints 27.53, 27.56, 6.03 and 5.63 MPa on the bars.",
        "shells": rows,
        "lead_R_over_tc": LEAD_R / LEAD_CORE,
        "mesh_paper_flat": paper,
        "mesh_Rtc_40": rt40,
        "mesh_Rtc_100": rt100,
        "bytes_per_dof_allowance": BYTES_PER_DOF,
        "free_ram_bytes_observed": FREE_RAM_BYTES,
    }
    (ROOT / "NARROW-RESULTS.json").write_text(json.dumps(out, indent=1) + "\n")
    for name, row in rows.items():
        print(
            name,
            "Rtc", g(row["R_over_tc"]),
            "Vc", g(row["Vc"]),
            "p_crimp_MPa", g(row["p_crimp_Pa"] / 1e6),
            "gamma", g(row["gamma"]),
            "product", g(row["lead_times_gamma"]),
            "share", g(row["face_bending_share_of_flexural_rigidity"]),
            "lin_over", g(row["linear_over_crimp"]),
            "nl_over", g(row["nonlinear_perfect_over_crimp"]),
        )
    for label, block in (("paper", paper), ("rt40", rt40), ("rt100", rt100)):
        print(
            label,
            "Rtc", g(block["R_over_tc"]),
            "Vc", g(block["Vc_flat_thicknesses_held"]),
            "elements", g(block["elements"]),
            "dof", g(block["dof_allowance"]),
            "ram_GiB", g(block["ram_bytes_at_10kB_per_dof"] / (1024**3)),
            "fits", block["fits_free_ram"],
        )
    print("lead_Rtc", g(LEAD_R / LEAD_CORE))
    print("ended", ended)


if __name__ == "__main__":
    main()
