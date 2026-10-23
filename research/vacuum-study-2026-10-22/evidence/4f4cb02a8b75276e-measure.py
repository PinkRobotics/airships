#!/usr/bin/env python3
"""MAINLINE-018b. Measure gamma = p_collapse / p_crimp for the Sim hemispheres.

Geometry and absolute pressures are the EUCASS 2023-367 reading.
Gc = 20 MPa is E/2 from the stated foam modulus and Poisson 0.
The H80 and H35 shear moduli are the opened Divinycell H sheet.
Nothing here is a certification.
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
NU_CORE = 0.0
GC_PAPER = E_CORE / (2.0 * (1.0 + NU_CORE))
R_OUTER = 42.80e-3
T_OUTER = 0.42e-3
T_CORE = 3.10e-3
LEAD_LEAST = 0.650411843681

# EUCASS 2023-367 sections 3.2-3.3. MPa, read from the PDF text.
PRESSURE = {
    "flat": {
        "linear_perfect_Pa": 27.53e6,
        "nonlinear_perfect_Pa": 12.45e6,
        "imperfect_Pa": 6.03e6,
        "figure_linear": "Figure 9",
        "figure_imperfect": "Figure 10",
        "published_kdf": 0.22,
    },
    "dimple": {
        "linear_perfect_Pa": 27.56e6,
        "nonlinear_perfect_Pa": 12.44e6,
        "imperfect_Pa": 5.63e6,
        "figure_linear": "Figure 12",
        "figure_imperfect": "Figure 13",
        "published_kdf": 0.20,
    },
}

# Divinycell H, H.ds-u/10_2012.rev7, ASTM C273, average values.
SHEAR = {
    "paper_E_over_2": GC_PAPER,
    "H80": 27.0e6,
    "H35": 12.0e6,
}


def g(x: float) -> str:
    return format(x, ".12g")


def shell(name: str, t_inner: float) -> dict:
    h = T_CORE + 0.5 * (T_OUTER + t_inner)
    t_sum = T_OUTER + t_inner
    r_mid = R_OUTER - 0.5 * (T_OUTER + T_CORE + t_inner)
    root = math.sqrt(1.0 - NU * NU)
    sigma_0 = E_FACE * h / (r_mid * root)
    # Facing stress. Equal or unequal faces, handbook 2.3-4 form.
    sigma_crimp = h * h * GC_PAPER / (t_sum * T_CORE)
    vc = sigma_0 / sigma_crimp
    # Sphere membrane: sigma = p * R / (2 * t_sum), so p = 2 * sigma * t_sum / R.
    # That is 2 * h^2 * Gc / (R * tc). Same factor as the lead's 4*tf form when faces match.
    p_crimp = 2.0 * sigma_crimp * t_sum / r_mid
    p_classical = 2.0 * sigma_0 * t_sum / r_mid
    # Flexural rigidity about the sandwich neutral axis, isotropic faces.
    # Own-face term is what CR-1457 section 4.7 item (e) neglects.
    y_na = (t_inner * h) / t_sum
    d_outer = y_na
    d_inner = h - y_na
    d_own = E_FACE / (12.0 * (1.0 - NU * NU)) * (T_OUTER**3 + t_inner**3)
    d_steiner = E_FACE / (1.0 - NU * NU) * (T_OUTER * d_outer**2 + t_inner * d_inner**2)
    share = d_own / (d_own + d_steiner)
    pressures = PRESSURE[name]
    gamma = pressures["imperfect_Pa"] / p_crimp
    return {
        "name": name,
        "t_outer_m": T_OUTER,
        "t_inner_m": t_inner,
        "t_core_m": T_CORE,
        "h_m": h,
        "R_outer_m": R_OUTER,
        "R_middle_m": r_mid,
        "R_over_tc": r_mid / T_CORE,
        "sigma_0_Pa": sigma_0,
        "sigma_crimp_Pa": sigma_crimp,
        "Vc": vc,
        "branch": "shear_crimping" if vc > 2.0 else "stiff_or_moderate_core",
        "p_crimp_Pa": p_crimp,
        "p_classical_Pa": p_classical,
        "linear_over_crimp": pressures["linear_perfect_Pa"] / p_crimp,
        "nonlinear_perfect_over_crimp": pressures["nonlinear_perfect_Pa"] / p_crimp,
        "gamma_imperfect_over_crimp": gamma,
        "published_kdf_check": pressures["imperfect_Pa"] / pressures["linear_perfect_Pa"],
        "face_bending_share_of_flexural_rigidity": share,
        "lead_least_times_gamma": LEAD_LEAST * gamma,
        "pressures": pressures,
    }


def at_gc(row: dict, gc: float) -> dict:
    scale = GC_PAPER / gc
    gamma = row["gamma_imperfect_over_crimp"] * scale
    return {
        "Gc_Pa": gc,
        "p_crimp_Pa": row["p_crimp_Pa"] / scale,
        "gamma": gamma,
        "lead_least_times_gamma": LEAD_LEAST * gamma,
    }


def main() -> None:
    rows = {
        "flat": shell("flat", 0.42e-3),
        "dimple": shell("dimple", 0.40e-3),
    }
    # Robotics quoted about 3.92, 3.89 and 789 MPa. A miss stops the card.
    expect = {
        "flat": (3.92e6, 789e6),
        "dimple": (3.89e6, None),
    }
    for name, (p_c, p_k) in expect.items():
        got = rows[name]["p_crimp_Pa"]
        if abs(got - p_c) / p_c > 0.01:
            raise SystemExit(f"p_crimp miss {name} {got} vs {p_c}")
        if p_k is not None and abs(rows[name]["p_classical_Pa"] - p_k) / p_k > 0.01:
            raise SystemExit(f"classical miss {name} {rows[name]['p_classical_Pa']}")
    sensitivity = {
        name: {label: at_gc(row, gc) for label, gc in SHEAR.items()}
        for name, row in rows.items()
    }
    ended = datetime.now(ZONE).isoformat(timespec="seconds")
    out = {
        "schema": 1,
        "card": "MAINLINE-018b",
        "unit": "vacuum-mainline018b-crimp-gamma-measured-1020",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": ended,
        "p_crimp_formula": "p = 2 * h^2 * Gc / (R_middle * tc)",
        "p_classical_formula": "p = 2 * sigma_0 * (t_outer + t_inner) / R_middle",
        "gamma_definition": "imperfect collapse pressure / p_crimp",
        "Gc_paper_Pa": GC_PAPER,
        "Gc_basis": "G = E / (2 * (1 + nu)) from the stated foam modulus 0.04 GPa and Poisson 0.",
        "shells": rows,
        "sensitivity": sensitivity,
        "design_credit_cap": 1.0,
        "carried_least_if_capped": LEAD_LEAST,
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=1) + "\n")
    for name, row in rows.items():
        print(
            name,
            "h", g(row["h_m"]),
            "R", g(row["R_middle_m"]),
            "Vc", g(row["Vc"]),
            "p_crimp_MPa", g(row["p_crimp_Pa"] / 1e6),
            "p_classical_MPa", g(row["p_classical_Pa"] / 1e6),
            "gamma", g(row["gamma_imperfect_over_crimp"]),
            "kdf", g(row["published_kdf_check"]),
            "lin_over", g(row["linear_over_crimp"]),
            "nl_over", g(row["nonlinear_perfect_over_crimp"]),
            "share", g(row["face_bending_share_of_flexural_rigidity"]),
            "product", g(row["lead_least_times_gamma"]),
        )
        for label, sens in sensitivity[name].items():
            print(" ", label, "p_crimp_MPa", g(sens["p_crimp_Pa"] / 1e6), "gamma", g(sens["gamma"]), "product", g(sens["lead_least_times_gamma"]))
    print("ended", ended)


if __name__ == "__main__":
    main()
