#!/usr/bin/env python3
"""Why vacuum and not helium (or hydrogen)? The honest ledger, generated.

    python3 research/analysis/helium.py [--json OUT]

The project never wrote this answer down, and the draft answers it kept implying were wrong
in the concept's favour. The generated truth: **a vacuum cell can never beat a gas envelope
on net lift** — a perfect massless vacuum shell out-lifts pure hydrogen by 7.5%, so any
structure heavier than 0.067 kg/m3 loses the lift argument outright, and even the fourth
hierarchy level is six times heavier than that. The case for vacuum is OPERATIONAL AND
STRATEGIC: fleet-scale supply independence, no gas logistics tail at remote fire bases,
crush-safe fixed displacement over a fire, and the array being the airframe. Those are real,
they describe this project's mission — and for a single ship, a demonstrator, or anything
crewed, helium is simply better and this file says so.

Structure numbers come from vacuum-cell.json (this file does not re-derive them); gas
densities are ideal-gas at the working altitude; market numbers are constants carried with
their source below, USGS Mineral Commodity Summaries being public-domain primary data.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
CELL_JSON = ROOT / "research" / "analysis" / "vacuum-cell.json"
FIGURES = ROOT / "research" / "figures.json"

# Ideal-gas constants, J/(kg K).
R_AIR, R_HE, R_H2 = 287.05, 2077.1, 4124.2

# The reference hull (right-sized P-100, the same one vacuum-cell.py uses).
HULL_VOLUME_M3 = 220000.0
HULL_ENVELOPE_M2 = 22592.0

# ---- market constants, each with its source -----------------------------------------------
# USGS Mineral Commodity Summaries, Helium chapters (public domain, read 2026-08-10):
HE_PRICE_2021_USD_M3 = 7.57     # MCS 2022: Grade-A base price, $210/Mcf
HE_PRICE_2024_USD_M3 = 14.0     # MCS 2024 & 2025: $390/Mcf, "producers posting surcharges"
US_HE_CONSUMPTION_M3 = 56e6     # MCS 2025: US apparent consumption 2024
WORLD_HE_PRODUCTION_M3 = 180e6  # MCS 2025: world production 2024
US_HE_LIFTING_SHARE = 0.18      # MCS 2025: lifting gas share of US use
# Industry envelope permeability design spec, ~1 L/m2/day. Attributed to Liao & Pasternak
# 2009 (Prog. Aero. Sci. 45:83-96) — PAYWALLED, quoted secondhand, order-of-magnitude only.
ENVELOPE_LOSS_L_M2_DAY = 1.0
# Hydrogen price band, grey-to-green, USD/kg. Order-of-magnitude; pin to IEA GHR before
# leaning on it harder than "20-150x cheaper than helium".
H2_PRICE_USD_KG = (1.0, 7.0)
# Demonstrated dead-weight ledger (airships.net flight statistics, curated secondary):
HINDENBURG_VOLUME_M3 = 200000.0
HINDENBURG_DEAD_T = 118.0       # empty weight; useful/gross 49% on hydrogen
ZR3_USEFUL_FRACTION = 0.41      # the same LZ-126 hull on helium


def isa(alt_m: float) -> tuple[float, float, float]:
    t = 288.15 - 0.0065 * alt_m
    p = 101325.0 * (t / 288.15) ** (9.80665 / (R_AIR * 0.0065))
    rho = p / (R_AIR * t)
    return t, p, rho


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="OUT")
    args = ap.parse_args()
    cell = json.loads(CELL_JSON.read_text())
    wall = cell["theWall"]["rhoAirAtWorkAltKgPerM3"]
    ladder = cell["hierarchy"]["ladder"]

    t, p, rho_air = isa(2500.0)
    rho_he = p / (R_HE * t)
    rho_h2 = p / (R_H2 * t)
    # 97% He / 3% air by volume — the practical operating purity.
    rho_he97 = 0.97 * rho_he + 0.03 * rho_air

    def net(gas: float, structure: float) -> float:
        return rho_air - gas - structure

    ledger = {
        "vacuumIdeal": {"gas": 0.0, "structure": 0.0, "net": round(rho_air, 4)},
        "vacuumLevel1": {"gas": 0.0, "structure": ladder["1"]["totalKgPerM3"],
                         "net": round(net(0, ladder["1"]["totalKgPerM3"]), 4)},
        "vacuumLevel2": {"gas": 0.0, "structure": ladder["2"]["totalKgPerM3"],
                         "net": round(net(0, ladder["2"]["totalKgPerM3"]), 4)},
        "vacuumLevel3": {"gas": 0.0, "structure": ladder["3"]["totalKgPerM3"],
                         "net": round(net(0, ladder["3"]["totalKgPerM3"]), 4)},
        "hydrogen": {"gas": round(rho_h2, 4), "structure": None,
                     "net": round(rho_air - rho_h2, 4),
                     "note": "before envelope and frame"},
        "helium": {"gas": round(rho_he, 4), "structure": None,
                   "net": round(rho_air - rho_he, 4),
                   "note": "before envelope and frame"},
        "helium97": {"gas": round(rho_he97, 4), "structure": None,
                     "net": round(rho_air - rho_he97, 4),
                     "note": "97% purity, the practical operating point"},
    }

    # The one-line impossibility: the structure mass at which vacuum ties hydrogen.
    breakeven_h2 = rho_h2
    breakeven_he = rho_he

    # Per-ship helium economics.
    t0, p0 = 288.15, 101325.0
    fill_std_m3 = HULL_VOLUME_M3 * (p / p0) * (t0 / t)
    fill_usd = fill_std_m3 * HE_PRICE_2024_USD_M3
    loss_m3_day = ENVELOPE_LOSS_L_M2_DAY * HULL_ENVELOPE_M2 / 1000.0
    makeup_frac_yr = loss_m3_day * 365.0 / HULL_VOLUME_M3
    makeup_usd_yr = loss_m3_day * 365.0 * (p / p0) * (t0 / t) * HE_PRICE_2024_USD_M3

    # Fleet scale.
    fleet = 100
    fleet_m3 = fleet * fill_std_m3
    fleet_vs_us = fleet_m3 / US_HE_CONSUMPTION_M3
    fleet_vs_world = fleet_m3 / WORLD_HE_PRODUCTION_M3

    # Hydrogen fill.
    h2_fill_t = rho_h2 * HULL_VOLUME_M3 / 1000.0
    h2_fill_usd = tuple(round(h2_fill_t * 1000.0 * c) for c in H2_PRICE_USD_KG)

    # Useful fractions: structure-included lift per gross, vacuum vs the demonstrated rigids.
    useful = {
        "vacuumLevel2Pct": round(100.0 * (wall - ladder["2"]["totalKgPerM3"]) / wall, 1),
        "hindenburgH2Pct": 49.0,
        "hindenburgDeadKgPerM3": round(HINDENBURG_DEAD_T * 1000.0 / HINDENBURG_VOLUME_M3, 3),
        "zr3HeliumPct": round(100.0 * ZR3_USEFUL_FRACTION, 1),
    }

    out = {
        "generated": {"by": "research/analysis/helium.py",
                      "structureFrom": "research/analysis/vacuum-cell.json"},
        "atmosphere": {"altM": 2500, "tK": round(t, 1), "pPa": round(p),
                       "rhoAirKgPerM3": round(rho_air, 4)},
        "ledger": ledger,
        "breakeven": {
            "structureToTieHydrogenKgPerM3": round(breakeven_h2, 4),
            "structureToTieHeliumKgPerM3": round(breakeven_he, 4),
            "verdict": "Vacuum never wins on lift: the break-even structure against "
                       "hydrogen is ~6x below even the fourth hierarchy level. The case "
                       "for vacuum is operational and strategic, not aerostatic.",
        },
        "heliumMarket": {
            "price2021UsdPerM3": HE_PRICE_2021_USD_M3,
            "price2024UsdPerM3": HE_PRICE_2024_USD_M3,
            "priceRisePct": round(100.0 * (HE_PRICE_2024_USD_M3 / HE_PRICE_2021_USD_M3 - 1)),
            "federalReserve": "sold 2024-01-25, transferred to a single private buyer "
                              "2024-06-27; the 90-year public buffer no longer exists "
                              "(USGS MCS 2025)",
            "usConsumptionM3": US_HE_CONSUMPTION_M3,
            "worldProductionM3": WORLD_HE_PRODUCTION_M3,
            "usLiftingSharePct": round(100 * US_HE_LIFTING_SHARE),
        },
        "perShip": {
            "fillStdM3": round(fill_std_m3),
            "fillUsdM": round(fill_usd / 1e6, 1),
            "makeupPctPerYr": round(100.0 * makeup_frac_yr, 1),
            "makeupUsdPerYr": round(makeup_usd_yr / 1000.0) * 1000,
            "honest": "Helium logistics do not hurt one ship: the fill is a rounding error "
                      "against the airframe and make-up is ~$115k/yr. The argument only "
                      "becomes real at fleet scale and in the logistics tail.",
        },
        "fleet": {
            "ships": fleet,
            "inventoryStdM3": round(fleet_m3),
            "pctOfUsAnnualConsumption": round(100.0 * fleet_vs_us),
            "pctOfWorldAnnualProduction": round(100.0 * fleet_vs_world),
        },
        "hydrogen": {
            "fillT": round(h2_fill_t, 1),
            "fillUsdRange": h2_fill_usd,
            "cheaperThanHeliumX": [round(fill_usd / h2_fill_usd[1]),
                                   round(fill_usd / h2_fill_usd[0])],
            "flank": "An uncrewed compartmentalised hydrogen ship shares most of the vacuum "
                     "ship's strategic advantages at fabric-ship TRL. The project must cost "
                     "it explicitly; a wildfire is the hardest place to argue flammability "
                     "away, and that argument is currently made from memory, not from a "
                     "read regulation.",
        },
        "usefulFraction": useful,
    }

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(out, indent=1))

    print(f"\nTHE GAS LEDGER at 2,500 m (air {rho_air:.4f} kg/m3):\n")
    for k, r in ledger.items():
        s = "" if r["structure"] is None else f"  structure {r['structure']:.3f}"
        print(f"  {k:<14} gas {r['gas']:.3f}{s}  net {r['net']:+.3f}")
    print(f"\nBreak-even structure to tie hydrogen: {breakeven_h2:.3f} kg/m3 "
          f"(level-4 hierarchy is {ladder['4']['totalKgPerM3']:.3f}). Vacuum never wins "
          f"on lift.")
    print(f"\nPER SHIP: fill {fill_std_m3:,.0f} std m3 = ${fill_usd / 1e6:.1f}M; make-up "
          f"{100 * makeup_frac_yr:.1f}%/yr = ${makeup_usd_yr / 1000:.0f}k/yr.")
    print(f"FLEET OF {fleet}: {fleet_m3 / 1e6:.0f} Mm3 held as inventory — "
          f"{100 * fleet_vs_us:.0f}% of US annual consumption, "
          f"{100 * fleet_vs_world:.0f}% of world production.")
    print(f"\nUseful fraction, structure included: vacuum level-2 "
          f"{useful['vacuumLevel2Pct']}% vs Hindenburg 49% (H2) and ZR-3 41% (He).")


if __name__ == "__main__":
    main()
