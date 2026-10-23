#!/usr/bin/env python3
"""MAINLINE-006: safety factor against float margin.

Own arithmetic from sealed 002 and 003 rows. Does not execute predecessor scripts.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SEAT = "ref-2543c559b19ffce7dfdd"
ref-4dd78496f9ad9abb5344 = "ref-44b53f348e892521e60b"
UNIT = "vacuum-mainline006-float-margin-1019"
ROOT = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline006-float-margin-1019"
)
STATE = Path(
    "unpublished-local-ref:89cd363716acb8e4"
)
R002 = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline002-strength-owner1200-1019/RESULTS.json"
)
R003 = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline003-p2-targets-owner1200-1019/RESULTS.json"
)
BRIEF = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/CARD-006-FLOAT-MARGIN.md"
)
COMMON = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/COMMON.md"
)
ZONE = ZoneInfo("America/Los_Angeles")
TOL = 1e-9

E = 68.9e9
RHO_AL = 2700.0
NU = 0.33
R = 10.0
SIGMA = 276e6
KD = 0.2
J1 = 0.1
SYS1 = 200.0
J2 = 0.05
SYS2 = 100.0
CORE0 = 0.1
RHO_C = 16.0
S = 1.0
RO = 0.02
SIG_F = 1.5e9
T_FILM = 8e-5
RHO_F = 970.0
NODE = 0.02
SYS3 = 50.0
P_EXT = 95460.83791390515
LIFT = 4889.442150186961

ASKED = (0.0, 0.05, 0.10, 0.20, 0.30)


def g(x: float) -> str:
    return format(x, ".12g")


def sha_bytes(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def pin(path: Path) -> dict:
    digest, nbytes = sha_bytes(path)
    return {"path": str(path), "sha256": digest, "bytes": nbytes}


def rel(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0)


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8")


def stamp():
    return datetime.now(ZONE).isoformat(timespec="microseconds"), time.monotonic()


def zoelly(t: float) -> float:
    return KD * 2.0 * E * (t / R) ** 2 / math.sqrt(3.0 * (1.0 - NU**2))


def sand(tf: float, d: float) -> float:
    return KD * 4.0 * E * tf * d / (R**2 * math.sqrt(1.0 - NU**2))


def mesh(area: float):
    tri = math.sqrt(3.0) / 4.0 * S * S
    n_tri = area / tri
    n_edge = 1.5 * n_tri
    n_node = n_edge - n_tri + 2.0
    return n_edge, n_node


def point(family, label, margin, geom, masses, p_buck, p_yield, extra, p_film=None):
    total = sum(masses.values())
    achieved = (LIFT - total) / LIFT
    if rel(achieved, margin) > 1e-9 and abs(achieved - margin) > 1e-9:
        raise SystemExit(f"margin drift {family} {label} {achieved} {margin}")
    sf_b = p_buck / P_EXT
    sf_y = p_yield / P_EXT
    least = min(sf_b, sf_y)
    payload = LIFT - total
    row = {
        "family": family,
        "label": label,
        "margin_requested": margin,
        "float_margin": achieved,
        "payload_kg": payload,
        "structural_mass_kg": total,
        "masses_kg": masses,
        "buckling_SF": sf_b,
        "yield_SF": sf_y,
        "least_SF": least,
        "buckling_pressure_Pa": p_buck,
        "yield_pressure_Pa": p_yield,
        "geometry": geom,
        "extra": extra,
        "tag": "QUESTIONABLE",
    }
    if p_film is not None:
        row["film_SF"] = p_film / P_EXT
        row["film_pressure_Pa"] = p_film
    return row


def shell_at(margin: float, label: str):
    total = LIFT * (1.0 - margin)
    t = (total - SYS1) / ((1.0 + J1) * RHO_AL * AREA)
    if t <= 0:
        raise SystemExit(f"P1 thickness not positive at {margin}")
    masses = {
        "shell": RHO_AL * AREA * t,
        "joints": J1 * RHO_AL * AREA * t,
        "systems_payload": SYS1,
        "residual_gas": 0.0,
    }
    return point(
        "P1",
        label,
        margin,
        {"t_m": t},
        masses,
        zoelly(t),
        2.0 * SIGMA * t / R,
        {"t_m": t},
    )


def p2a_at(margin: float, label: str):
    total = LIFT * (1.0 - margin)
    core_m = RHO_C * AREA * CORE0
    faces = (total - SYS2) / (1.0 + J2) - core_m
    tf = faces / (2.0 * RHO_AL * AREA)
    if tf <= 0:
        raise SystemExit(f"P2-A face not positive at {margin}")
    d = CORE0 + tf
    sand_m = faces + core_m
    masses = {
        "faces": faces,
        "core": core_m,
        "joints": J2 * sand_m,
        "systems_payload": SYS2,
        "residual_gas": 0.0,
    }
    return point(
        "P2-A",
        label,
        margin,
        {"tf_m": tf, "core_m": CORE0, "d_m": d},
        masses,
        sand(tf, d),
        4.0 * SIGMA * tf / R,
        {"tf_m": tf, "core_m": CORE0, "d_m": d},
    )


def p2e_at(margin: float, label: str):
    total = LIFT * (1.0 - margin)
    faces = (total - SYS2) / (2.0 * (1.0 + J2))
    tf = faces / (2.0 * RHO_AL * AREA)
    core_t = faces / (RHO_C * AREA)
    if tf <= 0 or core_t <= 0:
        raise SystemExit(f"P2-E thickness not positive at {margin}")
    d = core_t + tf
    sand_m = faces + faces
    masses = {
        "faces": faces,
        "core": faces,
        "joints": J2 * sand_m,
        "systems_payload": SYS2,
        "residual_gas": 0.0,
    }
    return point(
        "P2-E",
        label,
        margin,
        {"tf_m": tf, "core_m": core_t, "d_m": d},
        masses,
        sand(tf, d),
        4.0 * SIGMA * tf / R,
        {"tf_m": tf, "core_m": core_t, "d_m": d},
    )


def frame_at(margin: float, label: str):
    total = LIFT * (1.0 - margin)
    a_target = (total - M_FILM - M_NODES - SYS3) / (N_EDGE * RHO_AL * S)
    disc = RO**2 - a_target / math.pi
    if disc <= 0:
        raise SystemExit(f"P3 wall not inside the tube at {margin}")
    tw = RO - math.sqrt(disc)
    if tw <= 0 or tw >= RO:
        raise SystemExit(f"P3 wall out of range {tw}")
    ri = RO - tw
    area_t = math.pi * (RO**2 - ri**2)
    inertia = math.pi / 4.0 * (RO**4 - ri**4)
    p_e = 2.0 * math.pi**2 * E * inertia / (R * S**3)
    p_y = 2.0 * SIGMA * area_t / (R * S)
    p_f = 2.0 * SIG_F * T_FILM / S
    masses = {
        "frame": N_EDGE * RHO_AL * area_t * S,
        "film": M_FILM,
        "nodes": M_NODES,
        "systems_payload": SYS3,
        "residual_gas": 0.0,
    }
    return point(
        "P3",
        label,
        margin,
        {"tw_m": tw, "ro_m": RO, "s_m": S, "film_m": T_FILM},
        masses,
        p_e,
        p_y,
        {"tw_m": tw, "area_m2": area_t, "I_m4": inertia, "n_edges": N_EDGE},
        p_film=p_f,
    )


def rates(rows):
    ordered = sorted(rows, key=lambda r: r["payload_kg"])
    segs = []
    for a, b in zip(ordered, ordered[1:]):
        dpay = b["payload_kg"] - a["payload_kg"]
        loss = (a["least_SF"] - b["least_SF"]) / (dpay / 100.0)
        segs.append(
            {
                "from_label": a["label"],
                "to_label": b["label"],
                "from_margin": a["float_margin"],
                "to_margin": b["float_margin"],
                "payload_from_kg": a["payload_kg"],
                "payload_to_kg": b["payload_kg"],
                "least_SF_from": a["least_SF"],
                "least_SF_to": b["least_SF"],
                "SF_lost_per_100kg": loss,
            }
        )
    knee = max(segs, key=lambda s: s["SF_lost_per_100kg"])
    ends = {r["label"]: r for r in rows}
    secant = None
    if "0" in ends and "30pct" in ends:
        a, b = ends["0"], ends["30pct"]
        dpay = b["payload_kg"] - a["payload_kg"]
        secant = (a["least_SF"] - b["least_SF"]) / (dpay / 100.0)
    return segs, knee, secant


def expect(row, pressure_name, pressure, mass_name, mass):
    if rel(row["buckling_pressure_Pa"] if pressure_name != "yield" else row["yield_pressure_Pa"], pressure) > TOL:
        raise SystemExit(f"pressure {row['family']} {row['label']} {pressure}")
    got = row["masses_kg"][mass_name]
    if rel(got, mass) > TOL:
        raise SystemExit(f"mass {row['family']} {row['label']} {got} {mass}")


def main():
    global AREA, N_EDGE, M_FILM, M_NODES
    brief_pin = pin(BRIEF)
    common_pin = pin(COMMON)
    if brief_pin["sha256"] != "52b5ed16a27c3c3ce3d5739c4e8daf83a618c4ebb2a09269c874162018ad469a":
        raise SystemExit("brief pin")
    if common_pin["sha256"] != "8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5":
        raise SystemExit("common pin")
    AREA = 4.0 * math.pi * R * R
    N_EDGE, n_node = mesh(AREA)
    M_FILM = RHO_F * AREA * T_FILM
    M_NODES = n_node * NODE

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    r002 = json.loads(R002.read_text(encoding="utf-8"))
    by_id = {row["point_id"]: row for row in r002["rows"]}
    if rel(r002["atmosphere"]["lift_kg"], LIFT) > 0 or rel(r002["atmosphere"]["p_ext_Pa"], P_EXT) > 0:
        raise SystemExit("atmosphere pin")

    # Reproduce sealed rows from their own thicknesses, then from the margin solve.
    checks = []
    p1 = shell_at(by_id["P1"]["float_margin"], "baseline")
    if rel(p1["extra"]["t_m"], 0.0007) > 1e-12:
        raise SystemExit(f"P1 t {p1['extra']['t_m']}")
    if rel(p1["buckling_pressure_Pa"], by_id["P1"]["limits_Pa"]["knocked_down_buckling"]) > TOL:
        raise SystemExit("P1 buckling")
    if rel(p1["yield_pressure_Pa"], by_id["P1"]["limits_Pa"]["aluminum_yield"]) > TOL:
        raise SystemExit("P1 yield")
    if rel(p1["structural_mass_kg"], by_id["P1"]["all_mass_kg"]) > TOL:
        raise SystemExit("P1 mass")
    p1a = shell_at(0.0, "0")
    if rel(p1a["buckling_pressure_Pa"], by_id["P1-A"]["limits_Pa"]["knocked_down_buckling"]) > TOL:
        raise SystemExit("P1-A buckling")
    if rel(p1a["structural_mass_kg"], by_id["P1-A"]["all_mass_kg"]) > TOL:
        raise SystemExit("P1-A mass")
    p2 = p2a_at(by_id["P2"]["float_margin"], "baseline")
    if rel(p2["buckling_pressure_Pa"], by_id["P2"]["limits_Pa"]["knocked_down_buckling"]) > TOL:
        raise SystemExit(f"P2 buckling {p2['buckling_pressure_Pa']}")
    if rel(p2["structural_mass_kg"], by_id["P2"]["all_mass_kg"]) > TOL:
        raise SystemExit("P2 mass")
    p2a = p2a_at(0.0, "0")
    if rel(p2a["buckling_pressure_Pa"], by_id["P2-A"]["limits_Pa"]["knocked_down_buckling"]) > TOL:
        raise SystemExit("P2-A buckling")
    if rel(p2a["extra"]["tf_m"], by_id["P2-A"]["extra"]["tf_m"]) > TOL:
        raise SystemExit("P2-A tf")
    p3 = frame_at(by_id["P3"]["float_margin"], "baseline")
    if rel(p3["buckling_pressure_Pa"], by_id["P3"]["limits_Pa"]["pinned_euler"]) > TOL:
        raise SystemExit(f"P3 euler {p3['buckling_pressure_Pa']}")
    if rel(p3["yield_pressure_Pa"], by_id["P3"]["limits_Pa"]["aluminum_yield"]) > TOL:
        raise SystemExit("P3 yield")
    if rel(p3["film_pressure_Pa"], by_id["P3"]["limits_Pa"]["film_membrane"]) > TOL:
        raise SystemExit("P3 film")
    if rel(p3["structural_mass_kg"], by_id["P3"]["all_mass_kg"]) > TOL:
        raise SystemExit("P3 mass")
    p3a = frame_at(0.0, "0")
    if rel(p3a["buckling_pressure_Pa"], by_id["P3-A"]["limits_Pa"]["pinned_euler"]) > TOL:
        raise SystemExit("P3-A euler")
    if rel(p3a["extra"]["tw_m"], by_id["P3-A"]["extra"]["tw_m"]) > TOL:
        raise SystemExit("P3-A tw")

    r003 = json.loads(R003.read_text(encoding="utf-8"))
    e003 = next(row for row in r003["rows"] if row["point_id"] == "P2-E")
    p2e0 = p2e_at(0.0, "0")
    if rel(p2e0["extra"]["tf_m"], e003["geometry"]["tf_m"]) > TOL:
        raise SystemExit(f"P2-E tf {p2e0['extra']['tf_m']} {e003['geometry']['tf_m']}")
    if rel(p2e0["extra"]["core_m"], e003["geometry"]["core_m"]) > TOL:
        raise SystemExit("P2-E core")
    if rel(p2e0["buckling_SF"], e003["buckling_SF"]) > TOL:
        raise SystemExit(f"P2-E sf {p2e0['buckling_SF']} {e003['buckling_SF']}")
    checks.append("sealed_002_and_003_P2E_PASS")

    families = {}
    specs = [
        ("P1", by_id["P1"]["float_margin"], shell_at),
        ("P2-A", by_id["P2"]["float_margin"], p2a_at),
        ("P2-E", by_id["P2"]["float_margin"], p2e_at),
        ("P3", by_id["P3"]["float_margin"], frame_at),
    ]
    summary = []
    for name, base, fn in specs:
        rows = []
        for m in margins(base):
            label = "baseline" if abs(m - base) < 1e-15 else label_of(m)
            rows.append(fn(m, label))
        segs, knee, secant = rates(rows)
        families[name] = {"rows": rows, "segments": segs, "knee": knee, "secant_0_to_30_SF_per_100kg": secant}
        summary.append((name, knee, secant, rows))

    end_utc, end_mono = stamp()
    elapsed = end_mono - origin_mono
    results = {
        "schema": 1,
        "status": "ESTIMATE_PENDING_UNA",
        "dependency": "DEPENDENCY002_AND_003_ESTIMATE_PENDING_UNA",
        "card": "MAINLINE-006",
        "tag": "QUESTIONABLE",
        "certification": False,
        "map_point": False,
        "kd": KD,
        "kd_note": "Buckling SF scales linearly with kd. This card uses the MAINLINE-002 value 0.2.",
        "lift_kg": LIFT,
        "p_ext_Pa": P_EXT,
        "families": families,
        "checks": checks,
        "measurements": {
            "origin_utc": origin_utc,
            "origin_monotonic_s": origin_mono,
            "end_utc": end_utc,
            "end_monotonic_s": end_mono,
            "elapsed_s": elapsed,
            "role": "measurements_only_not_limits",
        },
    }
    dump(ROOT / "RESULTS.json", results)
    dump(
        ROOT / "NFI.json",
        [
            {
                "NFI_id": "NFI-KD-020",
                "gap": "Buckling uses kd 0.2 from MAINLINE-002. MAINLINE-004b carries 0.90 as a QUESTIONABLE optimistic factor. Buckling SF on this card scales linearly with kd.",
                "direction": "Multiply buckling SF by kd/0.2 when a later card adopts another knockdown.",
                "effect": "Yield SF does not move with kd.",
            },
            {
                "NFI_id": "NFI-KNEE",
                "gap": "The knee is the tabulated interval with the largest drop in least SF per 100 kg of payload. It is a finite difference on these margins, not a fitted optimum.",
                "direction": "A denser margin grid if a later card needs a smoother knee.",
                "effect": "The named knee can move if margins are added between 0 and 5 percent.",
            },
            {
                "NFI_id": "NFI-YIELD",
                "gap": "Yield uses 276 MPa tensile yield transferred to compression. QUESTIONABLE.",
                "direction": "A compression allowable.",
                "effect": "Yield SF scales linearly with that allowable.",
            },
            {
                "NFI_id": "NFI-SHEAR",
                "gap": "Sandwich buckling omits core shear. The 002 formula is used.",
                "direction": "A sandwich formula with shear.",
                "effect": "Buckling SF would move if the pressure formula moved.",
            },
        ],
    )
    dump(
        ROOT / "INPUTS.json",
        {
            "schema": 1,
            "card": "MAINLINE-006",
            "status": "ESTIMATE_PENDING_UNA",
            "kd": KD,
            "lift_kg": LIFT,
            "p_ext_Pa": P_EXT,
            "pins": {
                "brief": brief_pin,
                "common": common_pin,
                "results_002": pin(R002),
                "results_003": pin(R003),
            },
            "allocation": {
                "P1": "shell thickness; joints 10 percent of shell; systems 200 kg",
                "P2-A": "face thickness; core thickness fixed at 0.1 m; joints 5 percent of sandwich; systems 100 kg",
                "P2-E": "equal face mass and core mass; core density 16 kg/m3; joints 5 percent; systems 100 kg",
                "P3": "tube wall; outer radius 0.02 m fixed; film, nodes and 50 kg systems fixed",
            },
        },
    )
    (ROOT / "CARD.md").write_text(render(summary, origin_utc, end_utc, elapsed), encoding="utf-8")
    for name, knee, secant, rows in summary:
        print("---", name, "knee", knee["from_label"], "->", knee["to_label"], g(knee["SF_lost_per_100kg"]), "secant", g(secant))
        for row in rows:
            print(
                row["label"],
                "m",
                g(row["float_margin"]),
                "pay",
                g(row["payload_kg"]),
                "mass",
                g(row["structural_mass_kg"]),
                "SFb",
                g(row["buckling_SF"]),
                "SFy",
                g(row["yield_SF"]),
                "least",
                g(row["least_SF"]),
            )
    print("elapsed", elapsed)


def label_of(m: float) -> str:
    if abs(m) < 1e-15:
        return "0"
    return f"{int(round(m * 100))}pct"


def margins(baseline: float):
    vals = list(ASKED)
    if all(abs(baseline - m) > 1e-12 for m in vals):
        vals.append(baseline)
    return vals


def render(summary, origin_utc, end_utc, elapsed) -> str:
    lines = []
    lines.append("# MAINLINE-006 float margin against safety factor — ESTIMATE_PENDING_UNA")
    lines.append("")
    lines.append(
        "Dependency label DEPENDENCY002_AND_003_ESTIMATE_PENDING_UNA. No map point. "
        "Nothing here is a certification. Every factor is QUESTIONABLE. "
        "Float margin is the share of lift kept as payload. Payload in kilograms is margin times lift. "
        "Lift is 4889.44215019 kg and external pressure is 95460.83791390515 Pa, the sealed 002 atmosphere. "
        "Buckling uses knockdown 0.2, the MAINLINE-002 value. Buckling safety factor scales linearly with knockdown. "
        "Yield uses 276 MPa transferred from tensile data."
    )
    lines.append("")
    lines.append(
        "P1 varies shell thickness. Joints are 10 percent of the shell and systems are 200 kg. "
        "P2-A varies face thickness with the core held at 0.1 m. Joints are 5 percent of the sandwich and systems are 100 kg. "
        "P2-E uses MAINLINE-003's equal face-mass and core-mass split at core density 16 kg/m3. "
        "P3 varies tube wall thickness with outer radius held at 0.02 m. Film, nodes and 50 kg of systems stay fixed. "
        "The least safety factor is the lesser of buckling and yield. "
        f"On P3 the film safety factor stays {g(2.0 * SIG_F * T_FILM / S / P_EXT)} and does not govern."
    )
    lines.append("")
    lines.append(
        "The safety factor lost per 100 kg is the drop in the least safety factor across a payload step, divided by that step in units of 100 kg. "
        "The knee of a curve is the step with the largest drop. It is a finite difference on these margins."
    )
    lines.append("")
    for name, knee, secant, rows in summary:
        lines.append(f"## {name}")
        lines.append("")
        for row in rows:
            geo = row["geometry"]
            if "t_m" in geo and "tf_m" not in geo:
                size = f"thickness {g(geo['t_m'])} m"
            elif "tf_m" in geo:
                size = f"face {g(geo['tf_m'])} m, core {g(geo['core_m'])} m"
            else:
                size = f"wall {g(geo['tw_m'])} m"
            lines.append(
                f"{row['label']} margin {g(row['float_margin'])}. {size}. "
                f"Mass {g(row['structural_mass_kg'])} kg. Payload {g(row['payload_kg'])} kg. "
                f"Buckling SF {g(row['buckling_SF'])}. Yield SF {g(row['yield_SF'])}. "
                f"Least SF {g(row['least_SF'])}."
            )
            lines.append("")
        lines.append(
            f"From margin 0 to 30 percent, the least safety factor falls {g(secant)} per 100 kg of payload. "
            f"The knee is {knee['from_label']} to {knee['to_label']}, "
            f"where the least safety factor falls {g(knee['SF_lost_per_100kg'])} per 100 kg."
        )
        lines.append("")
    lines.append("## Measurements")
    lines.append("")
    lines.append(
        f"Start {origin_utc}. End {end_utc}. Elapsed {elapsed} s. "
        "These times are measurements only. The order deadline 2026-10-20T07:00:00-07:00 is a door check-in, not a work limit."
    )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
