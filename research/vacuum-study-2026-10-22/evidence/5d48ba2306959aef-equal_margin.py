#!/usr/bin/env python3
"""MAINLINE-012: radius and altitude at equal float margin.

Own arithmetic. Does not execute predecessor scripts.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

UNIT = "vacuum-mainline012-equal-margin-1019"
ROOT = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs"
) / UNIT
R006 = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline006-float-margin-1019/RESULTS.json"
)
BRIEF = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/CARD-006-FLOAT-MARGIN.md"
)
ZONE = ZoneInfo("America/Los_Angeles")

E = 68.9e9
RHO_AL = 2700.0
NU = 0.33
SIGMA = 276e6
KD = 0.2
J2 = 0.05
SYS2 = 100.0
CORE_FIXED = 0.1
RHO_C = 16.0
T0 = 288.15
P0 = 101325.0
LAPSE = 0.0065
G0 = 9.80665
RSPEC = 287.053
P_EXT_500 = 95460.83791390515
LIFT_10 = 4889.442150186961
RADII = (5.0, 10.0, 20.0, 40.0)
ALTS = (0.0, 500.0, 2000.0, 5000.0, 11000.0)
MARGINS = (0.0, 0.05)


def g(x: float) -> str:
    return format(x, ".12g")


def pin(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8")


def stamp():
    return datetime.now(ZONE).isoformat(timespec="microseconds"), time.monotonic()


def rel(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0)


def atmosphere(h: float, radius: float) -> dict:
    t = T0 - LAPSE * h
    if t <= 0:
        raise SystemExit(f"temperature {t} at {h}")
    p = P0 * (t / T0) ** (G0 / (LAPSE * RSPEC))
    rho = p / (RSPEC * t)
    area = 4.0 * math.pi * radius * radius
    volume = (4.0 / 3.0) * math.pi * radius**3
    lift = rho * volume
    return {"h_m": h, "R_m": radius, "T_K": t, "p_ext_Pa": p, "rho_kg_m3": rho, "area_m2": area, "lift_kg": lift}


def sandwich_sf(tf: float, d: float, radius: float, p_ext: float) -> tuple[float, float]:
    p_b = KD * 4.0 * E * tf * d / (radius**2 * math.sqrt(1.0 - NU**2))
    p_y = 4.0 * SIGMA * tf / radius
    return p_b / p_ext, p_y / p_ext


def solve(family: str, atm: dict, margin: float, systems: float, core_mode: str) -> dict:
    budget = atm["lift_kg"] * (1.0 - margin)
    area = atm["area_m2"]
    if family == "P2-A":
        core_t = CORE_FIXED
        core_m = RHO_C * area * core_t
        faces = (budget - systems) / (1.0 + J2) - core_m
    else:
        faces = (budget - systems) / (2.0 * (1.0 + J2))
        core_m = faces
        core_t = faces / (RHO_C * area) if faces > 0 else -1.0
    if faces <= 0 or core_t <= 0 or budget <= systems:
        return {
            "family": family,
            "status": "INFEASIBLE",
            "margin_requested": margin,
            "systems_kg": systems,
            "lift_kg": atm["lift_kg"],
            "p_ext_Pa": atm["p_ext_Pa"],
            "T_K": atm["T_K"],
            "R_m": atm["R_m"],
            "h_m": atm["h_m"],
            "tag": "QUESTIONABLE",
            "reason": "fixed core or systems exceed the mass budget",
        }
    tf = faces / (2.0 * RHO_AL * area)
    d = core_t + tf
    sf_b, sf_y = sandwich_sf(tf, d, atm["R_m"], atm["p_ext_Pa"])
    total = (1.0 + J2) * (faces + core_m) + systems
    achieved = (atm["lift_kg"] - total) / atm["lift_kg"]
    if abs(achieved - margin) > 1e-9:
        raise SystemExit(f"margin drift {family} {achieved} {margin}")
    return {
        "family": family,
        "status": "OK",
        "margin_requested": margin,
        "float_margin": achieved,
        "systems_kg": systems,
        "lift_kg": atm["lift_kg"],
        "payload_kg": atm["lift_kg"] - total,
        "structural_mass_kg": total,
        "p_ext_Pa": atm["p_ext_Pa"],
        "T_K": atm["T_K"],
        "R_m": atm["R_m"],
        "h_m": atm["h_m"],
        "tf_m": tf,
        "core_m": core_t,
        "d_m": d,
        "buckling_SF": sf_b,
        "yield_SF": sf_y,
        "least_SF": min(sf_b, sf_y),
        "tag": "QUESTIONABLE",
    }


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    origin_path = ROOT / "ORIGIN.json"
    if origin_path.exists():
        origin = json.loads(origin_path.read_text(encoding="utf-8"))
        origin_utc = origin["origin_utc"]
        origin_mono = origin["origin_monotonic_s"]
    else:
        origin_utc, origin_mono = stamp()
        dump(
            origin_path,
            {
                "schema": 1,
                "unit": UNIT,
                "named_by": "CARD-006-FLOAT-MARGIN.md next job",
                "origin_utc": origin_utc,
                "origin_monotonic_s": origin_mono,
                "status": "ESTIMATE_PENDING_UNA",
                "caps": "measured_not_limits",
            },
        )
    base = atmosphere(500.0, 10.0)
    if abs(base["p_ext_Pa"] - P_EXT_500) > 0.1:
        raise SystemExit(f"pressure drift {base['p_ext_Pa']}")
    if rel(base["lift_kg"], LIFT_10) > 1e-12:
        raise SystemExit(f"lift drift {base['lift_kg']}")
    sealed = json.loads(R006.read_text(encoding="utf-8"))
    for family, key in (("P2-A", "P2-A"), ("P2-E", "P2-E")):
        row = solve(family, base, 0.0, SYS2, "fixed" if family == "P2-A" else "equal")
        want = next(r for r in sealed["families"][key]["rows"] if r["label"] == "0")
        if rel(row["buckling_SF"], want["buckling_SF"]) > 1e-9:
            raise SystemExit(f"{family} sf {row['buckling_SF']} {want['buckling_SF']}")
        if rel(row["yield_SF"], want["yield_SF"]) > 1e-9:
            raise SystemExit(f"{family} yield")

    radius_rows = []
    for radius in RADII:
        atm = atmosphere(500.0, radius)
        for family in ("P2-A", "P2-E"):
            for margin in MARGINS:
                row = solve(family, atm, margin, SYS2, "x")
                scaled_sys = SYS2 * (radius / 10.0) ** 2
                twin = solve(family, atm, margin, scaled_sys, "x")
                if row["status"] == "OK" and twin["status"] == "OK":
                    row["scaled_systems_buckling_SF"] = twin["buckling_SF"]
                    row["allowance_SF_spread"] = row["buckling_SF"] - twin["buckling_SF"]
                radius_rows.append(row)

    alt_rows = []
    ref = {}
    for h in ALTS:
        atm = atmosphere(h, 10.0)
        for family in ("P2-A", "P2-E"):
            for margin in MARGINS:
                row = solve(family, atm, margin, SYS2, "x")
                alt_rows.append(row)
                if h == 500.0 and row["status"] == "OK":
                    ref[(family, margin)] = row
    for row in alt_rows:
        if row["status"] != "OK":
            continue
        base_row = ref[(row["family"], row["margin_requested"])]
        t_ratio = base_row["T_K"] / row["T_K"]
        sf_ratio = row["buckling_SF"] / base_row["buckling_SF"]
        row["lift_per_pressure_vs_500m"] = t_ratio
        row["buckling_SF_vs_500m"] = sf_ratio
        row["cold_air_fraction_in_SF"] = sf_ratio / t_ratio

    end_utc, end_mono = stamp()
    results = {
        "schema": 1,
        "status": "ESTIMATE_PENDING_UNA",
        "card": "MAINLINE-012",
        "tag": "QUESTIONABLE",
        "certification": False,
        "kd": KD,
        "isa": {"T0_K": T0, "p0_Pa": P0, "lapse_K_per_m": LAPSE, "g0": G0, "Rspec": RSPEC},
        "checks": ["atmosphere_500m_PASS", "matches_006_margin0_PASS"],
        "radius_rows": radius_rows,
        "altitude_rows": alt_rows,
        "measurements": {
            "origin_utc": origin_utc,
            "origin_monotonic_s": origin_mono,
            "end_utc": end_utc,
            "end_monotonic_s": end_mono,
            "elapsed_s": end_mono - origin_mono,
            "role": "measurements_only_not_limits",
        },
    }
    dump(ROOT / "RESULTS.json", results)
    dump(
        ROOT / "NFI.json",
        [
            {
                "NFI_id": "NFI-KD-020",
                "gap": "Buckling uses kd 0.2. The 004b optimistic carry is 0.90. Buckling SF scales linearly with kd.",
                "direction": "Multiply buckling SF by kd/0.2 if a later card adopts the carry.",
                "effect": "Yield SF does not move with kd.",
            },
            {
                "NFI_id": "NFI-CORE-FIXED",
                "gap": "P2-A keeps the 0.1 m core while radius and altitude change. That fixed core can exhaust the mass budget.",
                "direction": "A core thickness that scales with radius.",
                "effect": "An infeasible row has no safety factor.",
            },
            {
                "NFI_id": "NFI-TROPOPAUSE",
                "gap": "11000 m is evaluated on the tropospheric lapse at the tropopause boundary. The isothermal stratosphere is not used.",
                "direction": "Hold T at 216.65 K above 11000 m if a later card climbs further.",
                "effect": "None inside this grid. 11000 m is the top row.",
            },
        ],
    )
    dump(
        ROOT / "INPUTS.json",
        {
            "schema": 1,
            "card": "MAINLINE-012",
            "pins": {"brief_006": pin(BRIEF), "results_006": pin(R006)},
            "radii_m": list(RADII),
            "altitudes_m": list(ALTS),
            "margins": list(MARGINS),
            "kd": KD,
        },
    )
    (ROOT / "CARD.md").write_text(render(results), encoding="utf-8")
    print("elapsed", results["measurements"]["elapsed_s"])
    for row in radius_rows:
        if row["margin_requested"] != 0.0:
            continue
        if row["status"] != "OK":
            print("R", row["family"], row["R_m"], "INFEASIBLE")
            continue
        print(
            "R",
            row["family"],
            row["R_m"],
            "SFb",
            g(row["buckling_SF"]),
            "SFy",
            g(row["yield_SF"]),
            "spread",
            g(row.get("allowance_SF_spread", float("nan"))),
        )
    for row in alt_rows:
        if row["margin_requested"] != 0.0 or row["family"] != "P2-E":
            continue
        if row["status"] != "OK":
            print("H", row["h_m"], "INFEASIBLE")
            continue
        print(
            "H",
            row["h_m"],
            "SFb",
            g(row["buckling_SF"]),
            "vs500",
            g(row["buckling_SF_vs_500m"]),
            "one_over_T",
            g(row["lift_per_pressure_vs_500m"]),
            "fraction",
            g(row["cold_air_fraction_in_SF"]),
        )


def render(results: dict) -> str:
    meas = results["measurements"]
    lines = [
        "# MAINLINE-012 geometry at equal float margin — ESTIMATE_PENDING_UNA",
        "",
        "Everything is QUESTIONABLE. Nothing is a certification. "
        "P2-A and P2-E are rescaled so the float margin is 0 or 5 percent. "
        "P2-A keeps the 0.1 m core and varies the face. P2-E keeps equal face mass and core mass. "
        "Joints stay 5 percent of the sandwich. Systems stay 100 kg unless the allowance comparison says otherwise. "
        "Buckling uses knockdown 0.2 and scales linearly with knockdown. "
        "The ISA troposphere matches the sealed 500 m pressure within 0.1 Pa and the sealed lift.",
        "",
        "The fixed-allowance twin scales the 100 kg systems with area, as (R/10)^2. "
        "The spread is this card's buckling safety factor minus that twin. "
        "Lift per unit pressure goes as 1/T. The cold-air fraction is the buckling-SF ratio versus 500 m, divided by T_500/T.",
        "",
        "## Radius at 500 m",
        "",
    ]
    for row in results["radius_rows"]:
        if row["status"] != "OK":
            lines.append(
                f"{row['family']} R {g(row['R_m'])} m, margin {g(row['margin_requested'])}. "
                "Infeasible. The fixed core or the systems exceed the mass budget."
            )
        else:
            lines.append(
                f"{row['family']} R {g(row['R_m'])} m, margin {g(row['float_margin'])}. "
                f"Face {g(row['tf_m'])} m, core {g(row['core_m'])} m. "
                f"Buckling SF {g(row['buckling_SF'])}. Yield SF {g(row['yield_SF'])}. "
                f"Least SF {g(row['least_SF'])}. Allowance spread {g(row['allowance_SF_spread'])}."
            )
        lines.append("")
    lines.append("## Altitude at R = 10 m")
    lines.append("")
    for row in results["altitude_rows"]:
        if row["status"] != "OK":
            lines.append(
                f"{row['family']} altitude {g(row['h_m'])} m, margin {g(row['margin_requested'])}. Infeasible."
            )
        else:
            lines.append(
                f"{row['family']} altitude {g(row['h_m'])} m, margin {g(row['float_margin'])}. "
                f"T {g(row['T_K'])} K. Pressure {g(row['p_ext_Pa'])} Pa. Lift {g(row['lift_kg'])} kg. "
                f"Buckling SF {g(row['buckling_SF'])}. Yield SF {g(row['yield_SF'])}. "
                f"Least SF {g(row['least_SF'])}. "
                f"Lift-per-pressure versus 500 m is {g(row['lift_per_pressure_vs_500m'])}. "
                f"Buckling SF versus 500 m is {g(row['buckling_SF_vs_500m'])}. "
                f"Cold-air fraction left in the safety factor is {g(row['cold_air_fraction_in_SF'])}."
            )
        lines.append("")
    lines.append("## Measurements")
    lines.append("")
    lines.append(
        f"Start {meas['origin_utc']}. End {meas['end_utc']}. Elapsed {meas['elapsed_s']} s. "
        "These times are measurements only."
    )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
