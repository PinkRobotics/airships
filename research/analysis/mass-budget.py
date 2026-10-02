#!/usr/bin/env python3
"""OPEN-QUESTIONS #11: a bottom-up dry-mass budget, line by line, against sources.

    python3 research/analysis/mass-budget.py            # table to stdout
    python3 research/analysis/mass-budget.py --json OUT  # machine-readable

`dryT = payloadT` is the assumption the whole ledger stands on, and until now the argument
against it was two citations rather than a budget. Two citations can be waved away one at a
time. A budget cannot: it says what every part of the ship weighs, where that number comes
from, and how far the total is from the allowance.

Every model quantity is read from research/figures.json, which `make factsheet` regenerates
from the live model and `tools/check_figures_fresh.py` refuses to let drift. Nothing about
the vehicle is typed in here. What IS typed in here is the external evidence — the specific
masses — and each one carries its source in the table below.

THREE COLUMNS, and the leftmost is the point. `floor` takes the single most favourable
published or derivable number for every line simultaneously, which no real vehicle gets.
`credible` takes what an engineer would actually plan against. `demonstrated` takes what has
been built and flown. If the floor column does not close, nothing else needs discussing.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
FIGURES = ROOT / "research" / "figures.json"

P_ATM = 101325.0          # Pa, the load the shell carries
ATMOSPHERE: dict = {}     # filled from figures.json in main(); see air_ballast()


def capsule_area(len_m: float, dia_m: float) -> float:
    """Price the nominal fleet on the existing model's capsule surface."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "area_model", ROOT / "research/analysis/vacuum-cell.py")
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    geom = model.ship_geom(dia_m)
    if not math.isclose(geom["lenM"], len_m):
        raise ValueError("Fleet dimensions are not this capsule family")
    return geom["areaM2"]


# ---------------------------------------------------------------------------------------
# The external evidence. Everything below is a number from outside this project, with the
# source it came from. These are the only free parameters in the budget.
# ---------------------------------------------------------------------------------------
EVIDENCE = {
    # kg per m3 of ENCLOSED VOLUME. Jenett's design rules are ratios (R/t = 10, lattice
    # pitch t/10), so shell mass scales with volume for spheres and the fraction is
    # radius-independent. That is the most favourable scaling available to us and it is
    # still the floor, not an estimate: see shellNote.
    "shell_kg_per_m3": {
        "floor": (0.508, "Jenett et al. 2019 Table 2 — 2,126 t shell on a 4.19e6 m3 "
                         "lattice sphere. Bare lattice: no skin, joints, valves or plant."),
        "credible": (0.75, "Jenett's lattice plus a 50% allowance for the joints, panel "
                           "attachments and non-spherical geometry the paper excludes and "
                           "names as later work."),
        "demonstrated": (1.16, "Akhmeteli & Gavrilin 2021 — the only vacuum shell design "
                               "checked against a buckling FEA, at 0.9 x 1.29 kg/m3."),
    },
    # kg/m2 of hull surface for the gas barrier ALONE, with the load-carrying job left to
    # the lattice underneath it. Metlen's membrane is heavy because it is also structural;
    # separating the two functions is the only reason this line can be small. `floor` is not
    # a constant — barrier_floor() derives it from the hull's own geometry below.
    "barrier_kg_per_m2": {
        "floor": (None, "Derived by barrier_floor() from the hull's lattice pitch: a Zylon "
                        "film bulging into one cell at h/a = 0.25, safety factor 4, 50% "
                        "fibre efficiency."),
        "credible": (None, "Ten times the derived film floor, for seams, adhesive, handling "
                           "plies and repair patches. Nobody has made one."),
        "demonstrated": (3.45, "Metlen 2013 — Zylon-reinforced Mylar, the only real "
                               "membrane in the literature, at W/B += 0.37."),
    },
    # THE WRONG REFERENCE CLASS, corrected. An earlier version used building-integrated CIGS
    # roofing laminate at 2.0-3.0 kg/m2 — hardware sized to be walked on and to weather for
    # 25 years. The right comparison is flight-proven HALE array: MicroLink flexible sheet
    # (flying on AALTO Zephyr and BAE PHASA-35) publishes >700 W/kg at 250 W/m2, and Alta
    # Devices Gen4 GaAs ELO is 0.17 kg/m2 bare. This line falls from 12.0 t to about 2.2 t.
    "solar_kg_per_m2": {
        "floor": (0.36, "MicroLink flexible solar sheet, 250 W/m2 at >700 W/kg — flight "
                        "hardware on Zephyr and PHASA-35."),
        "credible": (0.65, "X Development HALE patent US 10,407,153 budgets ~500 g/m2 of "
                           "cells plus ~150 g/m2 of structure, installed."),
        "demonstrated": (1.20, "A conservative installed figure with encapsulation and "
                               "attachment for a hull that flies through smoke and hail."),
    },
    "battery_wh_per_kg": {
        "floor": (500.0, "Lvovich 2020 (NASA GRC) — 'no clear path' beyond 500 Wh/kg at "
                         "pack level. The best case anyone at NASA will name."),
        "credible": (300.0, "Lvovich 2020 — 'achievable within reasonable timeframe'."),
        "demonstrated": (149.0, "Chin et al. 2021 — the X-57 pack NASA actually flew, from "
                                "225 Wh/kg cells at a cell-to-pack factor of 0.66."),
    },
    "motor_kw_per_kg": {
        "floor": (16.0, "NASA HEMM target, 1.4 MW class. A target, not a delivery."),
        "credible": (13.2, "NASA electrified-aircraft metric goal for MW-class machines."),
        "demonstrated": (5.0, "Representative of MW-class machines actually run on a bench."),
    },
    # Includes inverters, cabling, protection and thermal. Chin et al. and the NASA circuit
    # protection work both put drives at roughly the machine's own mass at these ratings.
    "drive_frac_of_motor": {"floor": (1.0, "n/a"), "credible": (1.2, "n/a"),
                            "demonstrated": (1.5, "n/a")},
    # Rotor discs. A CH-47 rotor is 18.3 m and its blade set plus hub is about 1.4 t; blade
    # mass goes roughly as diameter^2 at constant disc loading and technology.
    "rotor_kg_per_m2_disc": {
        "floor": (5.3, "A CH-47 blade set plus hub is about 1.4 t on an 18.3 m rotor — "
                       "5.3 kg per m2 of disc, and radius-independent under the mass-goes-as-"
                       "diameter-squared scaling this line assumes. An earlier version used "
                       "1.5, which is the blades-only figure and contradicted this string."),
        "credible": (7.0, "The same, with a hub and pylon for a body of revolution."),
        "demonstrated": (9.0, "Heavy-lift rotorcraft practice."),
    },
    # THE LINE WITH NO SOURCE. A 6 MW airborne nitrogen liquefier does not exist and no
    # published figure prices one. The range spans skid-mounted industrial practice (about
    # 20 t/MW at the small end) down to a number nobody has any right to assume.
    # NO AIRBORNE FIGURE EXISTS, and the ground figures are far worse than an earlier version
    # of this table assumed. Stirling StirLIN-2: 34 kW in 2,200 kg = 64.7 t/MW. StirLIN-1
    # Compact: 71.4 t/MW. NASA's own MASS-OPTIMISED FLIGHT concept — Hauser, Johnson &
    # Sutherlin, in-situ oxygen liquefaction for Mars, AIAA SciTech 2016, reverse turbo-
    # Brayton, the most mass-efficient cryocooler class known — is 136.5 kg at 1,990 W =
    # 68.6 t/MW. So practice is ~65-70 t/MW, not 20, and the floor below is not "a tenfold
    # improvement on industry": it is 34x better than the best flight design NASA has
    # published. It is kept at that value so the reader can see exactly what the budget is
    # being given for free, and because the plant cannot be deleted — a sealed-cell hull has
    # no other ballast source.
    "cryo_t_per_mw": {
        "floor": (2.0, "NO SOURCE, and 34x better than NASA's best published flight-optimised "
                       "liquefier. Recorded as a stated gift to the budget, not an estimate."),
        "credible": (20.0, "NO SOURCE. A three-fold improvement on ground practice."),
        "demonstrated": (65.0, "Stirling StirLIN-2, 34 kW in 2,200 kg; corroborated by NASA "
                               "GRC's 68.6 t/MW reverse turbo-Brayton flight concept."),
    },
    "ln2_tank_frac": {
        "floor": (0.05, "Vacuum-jacketed cryogenic tank at large scale, LN2 (denser and "
                        "warmer than LH2, so lighter per tonne stored)."),
        "credible": (0.08, "The same with structure to react flight loads."),
        "demonstrated": (0.15, "Aerospace cryotank practice."),
    },
    "fabric_kg_per_m2": {
        "floor": (1.0, "Coated fabric for water bladders and the anchor bag."),
        "credible": (1.5, "The same, with wear plies at the fill and dump interfaces."),
        "demonstrated": (2.5, "Bambi-bucket-class reinforced fabric."),
    },
    # UHMWPE rope. Fibre tenacity 3.5-4.0 N/tex at 970 kg/m3; rope realisation about 60-70%
    # of fibre. 2.4 N/tex at rope level is the working figure, so a rope's break load is
    # 2.4e6 N per kg/m of linear density.
    "rope_n_per_kg_per_m": {
        "floor": (2.0e6, "UHMWPE at 2.0 N/tex — the optimistic end of realised rope tenacity."),
        "credible": (1.5e6, "Commercial 12-strand UHMWPE data sheets realise 1.4-1.6 N/tex, "
                            "well under the 3.5-4.0 N/tex of the bare fibre."),
        "demonstrated": (1.4e6, "The pessimistic end of the same data sheets."),
    },
    "rope_safety_factor": {"floor": (3.0, "n/a"), "credible": (5.0, "n/a"),
                           "demonstrated": (7.0, "n/a")},
    "hose_kg_per_m_per_m_bore": {
        "floor": (10.0, "Reinforced layflat discharge hose, mass per metre per metre of "
                        "bore, at the 30 bar this head needs."),
        "credible": (17.0, "The same in a wire-reinforced construction that survives "
                           "repeated deployment."),
        "demonstrated": (25.0, "Heavy suction hose."),
    },
    # Everything with no line of its own: avionics, sensors, flight control, mooring gear,
    # crew provision, lightning protection, ice protection, paint, fasteners.
    # Measured on a real airship rather than guessed: Sentinel 1000 weight statement (Pant &
    # Kale, IIT Bombay LTA Systems Lab, Table 5) gives electrics and instruments 438 kg plus
    # miscellaneous 128.7 kg on a 5,726 kg empty weight — 9.9%, or 14.3% counting controls.
    # ANSI/AIAA S-120 mass growth allowance at "Estimated" maturity is a further 20-30%.
    # An earlier version used 5% at the floor, which is below any published figure.
    "sundries_frac": {
        "floor": (0.10, "Sentinel 1000 actuals: electrics, instruments and miscellaneous are "
                        "9.9% of empty weight on a flown airship."),
        "credible": (0.15, "The same, counting flight controls (14.3%)."),
        "demonstrated": (0.20, "With an ANSI/AIAA S-120 mass growth allowance on top."),
    },
}

CASES = ("floor", "credible", "demonstrated")

# Zylon PBO-AS: tensile strength and density. The strongest commercially available fibre
# that has actually been woven into a membrane for this purpose (Metlen used it).
ZYLON_PA, ZYLON_RHO = 5.8e9, 1560.0
BULGE_RATIO = 0.25        # bulge depth over cell half-width; shallow, so the film is taut
BARRIER_SF = 4.0          # safety factor on a film under permanent load, in creep
FIBRE_EFF = 0.5           # realised fraction of fibre strength in a coated woven membrane


def barrier_floor(disp_m3: float) -> float:
    """kg/m2 for a gas barrier that only has to seal, spanning one lattice cell.

    Jenett's design rules are ratios: shell thickness is a tenth of the radius and the
    lattice pitch a tenth of that, so the cell a film must span is R/100 of the hull's
    equal-volume radius. The film bulges into the cell and carries the atmosphere as
    membrane tension: sigma = p R_bulge / 2t, and R_bulge follows from the bulge depth.

    This is a FLOOR and nothing more. It has no seams, no adhesive, no handling plies, no
    repair, no puncture margin, and it assumes a film in permanent creep at a quarter of
    its fibre strength holds for the life of the vehicle. Nobody has made one.
    """
    r_hull = (3.0 * disp_m3 / (4.0 * math.pi)) ** (1.0 / 3.0)
    a = (r_hull / 100.0) / 2.0                       # cell half-width, m
    h = BULGE_RATIO * a
    r_bulge = (a * a + h * h) / (2.0 * h)
    sigma = ZYLON_PA / BARRIER_SF * FIBRE_EFF
    t = P_ATM * r_bulge / (2.0 * sigma)
    return ZYLON_RHO * t


def ev(key: str, case: str, disp_m3: float | None = None) -> float:
    v = EVIDENCE[key][case][0]
    if v is None:
        if key != "barrier_kg_per_m2" or disp_m3 is None:
            raise ValueError(f"{key}/{case} is derived and needs a displacement")
        f = barrier_floor(disp_m3)
        return f if case == "floor" else f * 10.0
    return v


def shell_budget_t(base_ex_shell_ex_sundries: float, sundries_frac: float,
                   allowance_t: float) -> float:
    """How much shell the allowance can afford, solved rather than subtracted.

    The sundries line is a fraction of EVERYTHING, including the shell, so "allowance minus
    everything except the shell" double-counts the shell's own share of it. Let S be the
    shell and B the rest before sundries: (S + B)(1 + f) = allowance, so S = allowance/(1+f) - B.
    An earlier version subtracted instead and published a shell budget 2.6 t too small.
    """
    return allowance_t / (1.0 + sundries_frac) - base_ex_shell_ex_sundries


def closing_volume(shell_kg_m3: float, rho_work: float, spec: dict, base_t: float,
                   area_scaled_t: float, area0_m2: float, sundries_frac: float) -> dict:
    """THE QUESTION THE BUDGET DID NOT ASK: how big must the hull be?

    Displacement was treated as fixed and the shell was asked to fit inside it. But dispM3 is
    a design variable and the payload is the requirement, so the honest question is the other
    way round. Net lift per m3 is (rho_air - shell_kg_m3) and it is CONSTANT with size —
    Jenett's design rules are ratios, so the shell's mass per enclosed m3 does not change with
    radius. Fixed payload divided by a constant net lift per m3 therefore has a solution, and
    growing the hull closes the budget for any shell lighter than the air it displaces.

    Which makes the real wall a single number nobody in this project has written down:
    a shell denser than rho_air has no net lift at any size whatsoever.
    """
    if shell_kg_m3 >= rho_work:
        return {"closes": False, "why": "shell is denser than the air it displaces"}
    v = float(spec["dispM3"])
    for _ in range(300):
        area = area0_m2 * (v / spec["dispM3"]) ** (2.0 / 3.0)
        m_else = (base_t + area_scaled_t * area / area0_m2) * (1.0 + sundries_frac)
        vn = (spec["payloadT"] + m_else) / (rho_work - shell_kg_m3) * 1000.0
        if abs(vn - v) < 1.0:
            v = vn
            break
        v = vn
    scale = (v / spec["dispM3"]) ** (1.0 / 3.0)
    return {"closes": True, "volumeM3": round(v), "timesBaseline": round(v / spec["dispM3"], 2),
            "lenM": round(spec["lenM"] * scale), "diaM": round(spec["diaM"] * scale)}


def budget(spec: dict, lift: dict, energy: dict, cycle: dict, case: str,
           rightsize: bool = False) -> list[dict]:
    """One class, one evidence case, every line in tonnes.

    `rightsize` applies the one change that is a decision rather than physics: size the
    battery for the mission instead of for eighteen cycles of endurance.

    IT NO LONGER DELETES THE CRYOGENIC TRAIN. An earlier version did, on the argument that a
    vacuum hull can ballast by admitting air. It cannot: the hull is many PERMANENTLY SEALED
    vacuum cells, there is no valve, and a cell that is cracked open cannot be pumped out
    again in the field. The plant is the emergency ballast source and it stays in the budget.
    See research/analysis/air-ballast.md, which is kept as a retraction.
    """
    area = capsule_area(spec["lenM"], spec["diaM"])
    batt_mwh = cycle["eCycleMWh"] * 2.0 * 1.5 if rightsize else spec["battMWh"]
    lines = []

    def add(name, t, driver, note=""):
        lines.append({"item": name, "tonnes": round(t, 2), "driver": driver, "note": note})

    add("Vacuum shell (lattice)", ev("shell_kg_per_m3", case) * spec["dispM3"] / 1000.0,
        f"{spec['dispM3']:,.0f} m3 enclosed",
        "Volume basis, which is the favourable one. On a surface basis Jenett's own sphere "
        "is 16.9 kg/m2 and this line triples.")
    add("Gas barrier skin",
        ev("barrier_kg_per_m2", case, spec["dispM3"]) * area / 1000.0,
        f"{area:,.0f} m2 hull surface")
    add("Solar skin", ev("solar_kg_per_m2", case) * spec["solarM2"] / 1000.0,
        f"{spec['solarM2']:,.0f} m2 projected")
    add("Battery pack", batt_mwh * 1e6 / ev("battery_wh_per_kg", case) / 1000.0,
        f"{batt_mwh:,.2f} MWh",
        "Sized for endurance between recharges, not for a cycle. The ship as specified "
        "stores eighteen cycles of energy.")

    motor_t = spec["battMW"] * 1000.0 / ev("motor_kw_per_kg", case) / 1000.0
    add("Propulsion motors", motor_t, f"{spec['battMW']} MW peak bus")
    add("Drives, cabling, thermal", motor_t * ev("drive_frac_of_motor", case),
        "fraction of motor mass")
    add("Rotors and hubs", ev("rotor_kg_per_m2_disc", case) * spec["diskM2"] / 1000.0,
        f"{spec['diskM2']:,} m2 disc area")

    add("Cryogenic plant", ev("cryo_t_per_mw", case) * spec["cryoMW"],
        f"{spec['cryoMW']} MW rated",
        "NO PUBLISHED SOURCE EXISTS FOR THIS LINE, and it cannot be deleted: the sealed-cell "
        "hull has no way to ballast with air. It is the emergency ballast source.")
    add("LN2 tankage", ev("ln2_tank_frac", case) * spec["ln2CapT"],
        f"{spec['ln2CapT']} t capacity")

    # Water tanks: the payload volume as a bladder, plus manifolds and dump valves.
    water_area = 4.84 * (spec["payloadT"]) ** (2.0 / 3.0)      # sphere-equivalent, m2 per m3
    add("Water tanks and plumbing",
        ev("fabric_kg_per_m2", case) * water_area / 1000.0 + 0.02 * spec["payloadT"],
        f"{spec['payloadT']} m3 payload")

    # Pump and hose. The bore follows from the fill rate at a 5 m/s hose velocity.
    bore = math.sqrt(4.0 * spec["fillM3s"] / (math.pi * 5.0))
    add("Pump", energy["pumpMW"] * 1000.0 / ev("motor_kw_per_kg", case) / 1000.0 * 2.0,
        f"{energy['pumpMW']} MW hydraulic set", "Twice the motor mass, for the wet end.")
    add("Hose", ev("hose_kg_per_m_per_m_bore", case) * bore * spec["hoseM"] / 1000.0,
        f"{spec['hoseM']} m x {bore * 1000:.0f} mm bore")

    # Anchor: cable sized by the bag's pull, bag by its own wetted area, winch by the power
    # to haul the bag clear of the surface at the model's own 5 m/s.
    pull_n = spec["anchorBagT"] * 1000.0 * 9.81
    lin = pull_n * ev("rope_safety_factor", case) / ev("rope_n_per_kg_per_m", case)
    add("Anchor cable", lin * spec["anchorCableM"] / 1000.0,
        f"{pull_n / 1e6:.1f} MN at SF {ev('rope_safety_factor', case):.0f}")
    bag_area = 4.84 * (spec["anchorBagT"]) ** (2.0 / 3.0)
    add("Anchor bag", ev("fabric_kg_per_m2", case) * bag_area / 1000.0,
        f"{spec['anchorBagT']} m3 bag")
    add("Winch", pull_n * 5.0 / 1e3 / ev("motor_kw_per_kg", case) / 1000.0 * 2.0,
        "haul at 5 m/s")

    sub = sum(x["tonnes"] for x in lines)
    add("Sundries and margin", sub * ev("sundries_frac", case),
        "avionics, control, mooring, fasteners")
    return lines


# Blower trains are heavy machines next to flight motors; this is the number the air-ballast
# line is most sensitive to and it is an estimate, not a source.
BLOWER_KW_PER_KG = 1.0
PUMP_ISOTHERMAL_EFF = 0.30
CLEAR_HOURS = 6.0


R_AIR, ISA_T0, ISA_LAPSE = 287.05, 288.15, 0.0065


def choked_flux(p0: float, t0: float) -> float:
    """kg/s per m2 of orifice for air choking into vacuum. Sets the ballast valve area."""
    g = 1.4
    return (p0 * math.sqrt(g / (R_AIR * t0))
            * (2.0 / (g + 1.0)) ** ((g + 1.0) / (2.0 * (g - 1.0))))


def air_ballast(spec: dict, lift: dict, energy: dict | None = None,
                assumptions: dict | None = None, atmosphere: dict | None = None) -> dict:
    """Ballast by letting air INTO a vacuum hull, instead of by making liquid nitrogen.

    A vacuum airship's lift is the absence of air. Admitting air adds mass at exactly the
    density of the surrounding atmosphere, which is precisely what ballast has to do, and
    it is self-limiting: a fully flooded hull weighs its own structure and nothing else.
    Nothing is carried, nothing is manufactured, and there is no tank.

    The bill is deferred rather than avoided — the hull has to be pumped back down. Work is
    the isothermal minimum for clearing the flooded volume against the atmosphere.
    """
    rho_ground = lift["atGroundT"] * 1000.0 / spec["dispM3"]      # kg/m3 the model uses
    need_t = lift["ln2ToSinkEmptyAtGroundT"]                      # the ballast requirement
    flooded_m3 = need_t * 1000.0 / rho_ground
    # AT THE GROUND, NOT AT SEA LEVEL. The flooded volume is measured at the density the model
    # gives at TERRAIN_MSL, so the pressure the pump discharges against has to be the pressure
    # at the same place — 89.9 kPa, not 101.3. Using sea level here overstated the pumping
    # bill by 13% and understated the valve by the same.
    terrain_m = (atmosphere or {}).get("terrainMslM", 0.0)
    t_ground = ISA_T0 - ISA_LAPSE * terrain_m
    p_ground = rho_ground * R_AIR * t_ground
    # W = V[p0 - pf ln(p0/pf) - pf], which tends to p0.V as pf tends to zero: the reversible
    # isothermal minimum for emptying a vessel against ambient. Verified numerically.
    work_j = p_ground * flooded_m3
    mwh = work_j / 3.6e9
    elec_mwh = mwh / PUMP_ISOTHERMAL_EFF
    pump_mw = elec_mwh / CLEAR_HOURS
    flux = choked_flux(p_ground, t_ground)
    out = {
        "floodedM3": round(flooded_m3),
        "floodedPctOfHull": round(100.0 * flooded_m3 / spec["dispM3"], 1),
        "ballastNeededT": need_t,
        "energyToDescendMWh": 0.0,           # open a valve
        "idealWorkMWh": round(mwh, 2),
        "electricalMWhToReEvacuate": round(elec_mwh, 2),
        "clearHours": CLEAR_HOURS,
        "pumpMW": round(pump_mw, 2),
        "pumpT": round(pump_mw * 1000.0 / BLOWER_KW_PER_KG / 1000.0, 2),
        # Choked inflow sets the valve. This is the one dimension of the mechanism that is
        # not obviously small, and it is still buildable.
        "valveAreaM2For60s": round(need_t * 1000.0 / (flux * 60.0), 2),
        "valveAreaM2For300s": round(need_t * 1000.0 / (flux * 300.0), 2),
    }
    if energy and assumptions:
        # The route it replaces: liquefy a full ballast load, and — separately — the nitrogen
        # the model chooses to make on EVERY cycle even though the anchor already holds the
        # ship down.
        e_ln2_full = spec["ln2CapT"] * 1000.0 * assumptions["eLN2"] / 1000.0
        e_cryo_cycle = energy["ln2MakeT"] * 1000.0 * assumptions["eLN2"] / 1000.0
        solar_mw = energy["solarMW"]
        out.update({
            "ln2RouteMWhToFillTanks": round(e_ln2_full, 1),
            "ln2RouteDaysOnSolar": round(e_ln2_full / solar_mw / 24.0, 1),
            "airRouteDaysOnSolarToReEvacuate": round(elec_mwh / solar_mw / 24.0, 1),
            "energyRatioLn2OverAir": round(e_ln2_full / elec_mwh, 1),
            "cycleCryoMWh": round(e_cryo_cycle, 3),
            "cycleRecoveryMWh": energy["eBackMWh"],
            "cycleNetCryoMWh": round(e_cryo_cycle - energy["eBackMWh"], 3),
        })
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="OUT")
    args = ap.parse_args()

    fig = json.loads(FIGURES.read_text())
    global ATMOSPHERE
    ATMOSPHERE = fig["atmosphere"]
    out = {"generated": {"by": "research/analysis/mass-budget.py",
                         "figures": fig["generated"]},
           "evidence": {k: {c: {"value": v[c][0], "source": v[c][1]} for c in CASES}
                        for k, v in EVIDENCE.items()},
           "classes": {}}

    for cid, cd in fig["classes"].items():
        spec, lift, energy, cycle = cd["spec"], cd["lift"], cd["energy"], cd["cycle"]
        area = capsule_area(spec["lenM"], spec["diaM"])
        rec = {
            "allowanceT": spec["payloadT"],
            "hullAreaM2": round(area),
            "displacementM3": spec["dispM3"],
            "requiredKgPerM3": round(spec["payloadT"] * 1000.0 / spec["dispM3"], 4),
            "requiredKgPerM2": round(spec["payloadT"] * 1000.0 / area, 3),
            "liftAtWorkAltT": lift["atWorkAltT"],
            "cases": {},
            "rightSized": {},
            "airBallast": air_ballast(spec, lift, energy, fig["assumptions"],
                                      fig["atmosphere"]),
        }
        # What the descent needs from the rotors once the anchor has done its share, with no
        # nitrogen made at all. If this closes, the cryogenic train is redundant in the cycle
        # as well as in the emergency.
        resid = cd["lift"]["surplusAtSourceT"] - cd["descent"]["anchorT"]
        rec["descentWithoutNitrogen"] = {
            "surplusAtSourceT": cd["lift"]["surplusAtSourceT"],
            "anchorT": cd["descent"]["anchorT"],
            "residualForRotorsT": round(resid, 1),
            "rotorCapT": cd["descent"]["rotorCapT"],
            "marginX": round(cd["descent"]["rotorCapT"] / resid, 1) if resid > 0 else None,
            "cycleMWhAsBuilt": cd["cycle"]["eCycleMWh"],
            "cycleMWhWithoutCryo": round(
                cd["cycle"]["eCycleMWh"] - rec["airBallast"]["cycleNetCryoMWh"], 3),
            "cycleSavingPct": round(
                100.0 * rec["airBallast"]["cycleNetCryoMWh"] / cd["cycle"]["eCycleMWh"], 1),
        }
        for case in CASES:
            for tag, rs in (("cases", False), ("rightSized", True)):
                lines = budget(spec, lift, energy, cycle, case, rightsize=rs)
                tot = sum(x["tonnes"] for x in lines)
                rec[tag][case] = {
                    "lines": lines,
                    "totalT": round(tot, 1),
                    "overBy": round(tot / spec["payloadT"], 2),
                    "shellAloneOverBy": round(
                        next(x["tonnes"] for x in lines
                             if x["item"].startswith("Vacuum shell")) / spec["payloadT"], 2),
                    "everythingButShellT": round(
                        tot - next(x["tonnes"] for x in lines
                                   if x["item"].startswith("Vacuum shell")), 1),
                    "baseExShellExSundriesT": round(sum(
                        x["tonnes"] for x in lines
                        if not x["item"].startswith(("Vacuum shell", "Sundries"))), 2),
                }
        # HOW MUCH DOES THE BATTERY CHOICE MATTER? "Two cycles plus a reserve" is a choice,
        # not a derivation, and picking it without showing the trade would be the same sin
        # this budget is auditing. So: sweep endurance, and let the reader see whether the
        # conclusion turns on it. (It does not — the shell dominates at every point.)
        rec["batterySensitivity"] = {}
        for case in CASES:
            wh = ev("battery_wh_per_kg", case)
            # Everything except the shell AND except the battery, so the sweep moves one
            # thing and the shell budget is what is left after both.
            lines = rec["rightSized"][case]["lines"]
            f = ev("sundries_frac", case)
            # Excludes Sundries as well, because Sundries is a fraction of the battery too and
            # holding it fixed while the pack grows by 32 t was silently free margin.
            base = sum(x["tonnes"] for x in lines
                       if not x["item"].startswith(("Battery", "Vacuum shell", "Sundries")))
            rows = {}
            for cycles in (2, 4, 8, 16):
                mwh = cd["cycle"]["eCycleMWh"] * cycles
                t = mwh * 1e6 / wh / 1000.0
                left = shell_budget_t(base + t, f, spec["payloadT"])
                rows[f"{cycles} cycles"] = {
                    "batteryMWh": round(mwh, 2),
                    "batteryT": round(t, 1),
                    "totalT": round((base + t) * (1.0 + f), 1),
                    "leftForShellT": round(left, 1),
                    "requiredShellKgPerM3": round(max(0.0, left) * 1000.0
                                                  / spec["dispM3"], 4),
                }
            rec["batterySensitivity"][case] = rows

        # The one number that decides the vehicle: with everything else right-sized, what
        # must a m3 of enclosed vacuum cost for the budget to close at all?
        rho_work = fig["atmosphere"]["rhoAtWorkAlt"]
        rec["shellDensityWallKgPerM3"] = rho_work
        for case in CASES:
            f = ev("sundries_frac", case)
            base = rec["rightSized"][case]["baseExShellExSundriesT"]
            left = shell_budget_t(base, f, spec["payloadT"])
            rec["rightSized"][case]["shellBudgetLeftT"] = round(left, 1)
            rec["rightSized"][case]["requiredShellKgPerM3"] = round(
                max(0.0, left) * 1000.0 / spec["dispM3"], 4)
            # And the other way round: at each published shell density, how big a hull closes?
            lines = rec["rightSized"][case]["lines"]
            area_scaled = sum(x["tonnes"] for x in lines
                              if x["item"].startswith(("Gas barrier", "Solar")))
            rec["rightSized"][case]["hullThatCloses"] = {
                f"{k:.3f}": closing_volume(k, rho_work, spec, base - area_scaled,
                                           area_scaled, area, f)
                for k in (0.264, 0.35, 0.508, 0.60, 0.75, 0.90)
            }
            # CELLULAR: the vacuum is held in many permanently sealed cells, not one
            # envelope. That changes the structural problem twice over. The buckling radius
            # becomes the CELL's, not the hull's, so the hull's fineness ratio stops
            # mattering — the outer body is a fairing, not a pressure vessel. In exchange,
            # the space between cells is at ambient and contributes no lift, so displacement
            # is scaled by the packing fraction. phi = 0.74 is close-packed spheres; a
            # space-filling polyhedral cell approaches 1.0 but is a worse pressure shape.
            rec["rightSized"][case]["cellular"] = {
                f"phi={phi}": {
                    f"{k:.3f}": closing_volume(k, rho_work * phi, spec,
                                               base - area_scaled, area_scaled, area, f)
                    for k in (0.264, 0.508, 0.75)
                } for phi in (0.74, 0.85, 1.0)
            }
        out["classes"][cid] = rec

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(out, indent=1))

    ref = "P100"
    r = out["classes"][ref]
    print(f"\n{ref}: allowance {r['allowanceT']} t inside {r['displacementM3']:,} m3 "
          f"({r['requiredKgPerM3']} kg/m3, {r['requiredKgPerM2']} kg/m2 of hull)\n")
    w = 30
    print(f"{'line':<{w}} {'floor':>10} {'credible':>10} {'demonstr.':>10}")
    print("-" * (w + 33))
    names = [x["item"] for x in r["cases"]["floor"]["lines"]]
    for i, n in enumerate(names):
        vals = [r["cases"][c]["lines"][i]["tonnes"] for c in CASES]
        print(f"{n:<{w}} {vals[0]:>10.1f} {vals[1]:>10.1f} {vals[2]:>10.1f}")
    print("-" * (w + 33))
    print(f"{'TOTAL':<{w}} " + " ".join(f"{r['cases'][c]['totalT']:>10.1f}" for c in CASES))
    print(f"{'x allowance':<{w}} " + " ".join(f"{r['cases'][c]['overBy']:>10.2f}"
                                              for c in CASES))
    print(f"{'shell alone, x allowance':<{w}} "
          + " ".join(f"{r['cases'][c]['shellAloneOverBy']:>10.2f}" for c in CASES))
    print()
    print("RIGHT-SIZED (battery sized for the mission; the cryogenic plant STAYS —\n       a sealed-cell hull cannot ballast with air, see air-ballast.md)")
    print(f"{'TOTAL':<{w}} " + " ".join(f"{r['rightSized'][c]['totalT']:>10.1f}"
                                        for c in CASES))
    print(f"{'x allowance':<{w}} " + " ".join(f"{r['rightSized'][c]['overBy']:>10.2f}"
                                              for c in CASES))
    print(f"{'left for the shell, t':<{w}} "
          + " ".join(f"{r['rightSized'][c]['shellBudgetLeftT']:>10.1f}" for c in CASES))
    print(f"{'=> shell must cost, kg/m3':<{w}} "
          + " ".join(f"{r['rightSized'][c]['requiredShellKgPerM3']:>10.3f}" for c in CASES))
    print(f"{'best published shell, kg/m3':<{w}} {EVIDENCE['shell_kg_per_m3']['floor'][0]:>10.3f}")
    ab = r["airBallast"]
    print(f"\nAir ballast on the {ref}: flood {ab['floodedM3']:,} m3 "
          f"({ab['floodedPctOfHull']}% of the hull) for {ab['ballastNeededT']} t of ballast; "
          f"{ab['electricalMWhToReEvacuate']} MWh to pump back down.")
    print()
    for cid in ("P1000", "P10000"):
        c = out["classes"][cid]
        print(f"{cid}: over by "
              + ", ".join(f"{c['cases'][k]['overBy']:.2f}x ({k})" for k in CASES)
              + f"; right-sized floor {c['rightSized']['floor']['overBy']:.2f}x, "
              + f"shell must cost {c['rightSized']['floor']['requiredShellKgPerM3']:.3f} kg/m3")


if __name__ == "__main__":
    main()
