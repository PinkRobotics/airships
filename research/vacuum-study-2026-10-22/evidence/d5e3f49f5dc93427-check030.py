#!/usr/bin/env python3
"""MAINLINE-030 independent check. Owner scripts are not executed."""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
OWNER = Path(
    "unpublished-local-ref:3810915cf17e47f1"
    "/.ship/work/outputs/vacuum-mainline030-design-register-1020"
)
EXTRA = Path(
    "unpublished-local-ref:3810915cf17e47f1"
    "/.ship/work/outputs/vacuum-mainline011b-check-1019/RESULTS-EXTRA.json"
)
R = 10.0
P = 95460.83791390515
SIGMA_FILM = 1.5e9
T_FILM = 80e-6


def tube_rg(ro: float, wall: float) -> float:
    ri = ro - wall
    return math.sqrt((ro * ro + ri * ri) / 2.0)


def half_wave(rg: float) -> float:
    return math.pi * math.sqrt(0.75 * rg * R)


def nodes(s: float) -> float:
    return 2.0 + 8.0 * math.pi * R * R / (math.sqrt(3.0) * s * s)


def member_force(s: float) -> float:
    return P * R * s / (2.0 * math.sqrt(3.0))


def main() -> None:
    continuum = json.loads((OWNER / "CONTINUUM.json").read_text(encoding="utf-8"))
    waves = []
    for row in continuum:
        if "r_o_m" not in row:
            continue
        rg = tube_rg(row["r_o_m"], row["wall_m"])
        wave = half_wave(rg)
        stated = math.pi * math.sqrt(1.06 * row["rg_m"] * R)
        waves.append(
            {
                "point": row["point"],
                "s_m": row["s_m"],
                "stored_wave_m": row["buckle_half_wave_m"],
                "mine_wave_m": wave,
                "wave_diff_m": wave - row["buckle_half_wave_m"],
                "stored_ratio": row["half_wave_over_s"],
                "mine_ratio": wave / row["s_m"],
                "stated_1_06_wave_m": stated,
                "stated_1_06_shortfall_m": stated - row["buckle_half_wave_m"],
            }
        )
    film_s = 2.224
    film = SIGMA_FILM * T_FILM / ((P / 2.0) * film_s)
    extra = json.loads(EXTRA.read_text(encoding="utf-8"))
    found = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("s_m") == 2.224 and node.get("systems_kg") == 100.0 and "SF" in node:
                found.append(node["SF"]["film"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(extra)
    source_film = found[0]
    register = json.loads((OWNER / "REGISTER.json").read_text(encoding="utf-8"))
    want = ["R007", "R010", "R013", "R018", "R033", "R038", "R055", "R057", "R059", "R067"]
    picked = [row for row in register["rows"] if row["rid"] in want]
    have = {row["rid"] for row in picked}
    for row in register["rows"]:
        if len(picked) >= 20:
            break
        if row["rid"] not in have and len(row["sources"]) >= 2:
            picked.append(row)
            have.add(row["rid"])
    misses = []
    checked = 0
    for row in picked:
        for source in row["sources"]:
            checked += 1
            path = Path(source["file"])
            if not path.exists() or source["row_id"] not in path.read_text(encoding="utf-8", errors="replace"):
                misses.append({"rid": row["rid"], "row_id": source["row_id"], "file": source["file"]})
    uids = [source["uid"] for row in register["rows"] for source in row["sources"]]
    out = {
        "schema": 1,
        "card": "CHECK-030",
        "unit": "vacuum-mainline030-check-1020",
        "started_at": datetime.now(ZONE).isoformat(timespec="seconds"),
        "owner_script_executed": False,
        "half_waves": waves,
        "today": {
            "021": 0.2 / 0.59532,
            "021b": 0.2 / 0.46823,
        },
        "member_force_N": {"s_6_15": member_force(6.15), "s_2_224": member_force(film_s)},
        "nodes": {"s_6_15": nodes(6.15), "s_2_224": nodes(film_s), "s_2_04": nodes(2.04)},
        "inband_film_SF": film,
        "source_film_SF": source_film,
        "film_diff": film - source_film,
        "merged_rows_checked": [row["rid"] for row in picked],
        "source_pointers_checked": checked,
        "source_id_misses": misses,
        "source_pointers": len(uids),
        "unique_source_uids": len(set(uids)),
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("film", film, "source", source_film, "diff", film - source_film)
    print("rows", len(picked), "pointers", checked, "misses", len(misses))
    print("uids", len(uids), "unique", len(set(uids)))
    for row in waves:
        if "6.15" in str(row["s_m"]) or abs(row["s_m"] - 2.04) < 1e-9:
            print(row["point"], "ratio", row["mine_ratio"], "stated short", row["stated_1_06_shortfall_m"])


if __name__ == "__main__":
    main()
