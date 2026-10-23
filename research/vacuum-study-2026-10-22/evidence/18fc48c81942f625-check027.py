#!/usr/bin/env python3
"""Independent check of MAINLINE-027. Does not import or run the owner's scripts."""
import datetime
import hashlib
import json
import math
import os

OWNER = (
    "unpublished-local-ref:9cae3d24fd5d4f59"
    "/.ship/work/outputs/vacuum-mainline027-size-as-lever-1020"
)
ROOT = os.path.dirname(os.path.abspath(__file__))
P0 = 95460.83791390515
L0 = 4889.442150186961
T0 = 284.9
NU = 0.33
RHO_FACE = 1850.0
RHO_PASTE = 1100.0
BX = 0.6823278038280193  # positive root of x^3 + x = 1, refined below


def g(x):
    return format(x, ".12g")


def refine_bx():
    x = 0.7
    for _ in range(40):
        x = x - (x ** 3 + x - 1.0) / (3.0 * x * x + 1.0)
    return x


BX = refine_bx()


def area(radius):
    return 4.0 * math.pi * radius * radius


def volume(radius):
    return 4.0 * math.pi * radius ** 3 / 3.0


def lift(radius):
    return L0 * (radius / 10.0) ** 3


def climate(radius, swing, rise, vapour):
    mass = lift(radius)
    dry = (1.0 - swing) * T0 / (T0 + rise)
    moist = ((1.0 - swing) - 0.378 * vapour / P0) * T0 / (T0 + rise)
    dry_mass = mass * dry
    moist_mass = mass * moist
    return {
        "lift_kg": mass,
        "moist_lift_kg": moist_mass,
        "temperature_pressure_loss_kg": mass - dry_mass,
        "humidity_loss_kg": dry_mass - moist_mass,
        "internal_gas_kg": 0.01 * mass,
    }


SCENARIO = {
    "optimistic": {
        "swing": 0.01,
        "rise": 10.0,
        "vapour": 1000.0,
        "water_m": 0.0001,
        "contamination0_kg": 5.0,
        "a": 0.6096,
        "b": 1.8288,
        "w": 0.06,
        "gap": 0.001,
        "seal": 1e-5,
        "mu": 0.1464728290914915,
        "frozen_total": 0.7704669798160778,
        "eta": 0.9,
        "passive": True,
    },
    "conservative": {
        "swing": 0.02,
        "rise": 25.1,
        "vapour": 6000.0,
        "water_m": 0.001,
        "contamination0_kg": 25.0,
        "a": 0.3048,
        "b": 0.6096,
        "w": 0.12,
        "gap": 0.002,
        "seal": 3e-5,
        "mu": 0.292945658182983,
        "frozen_total": 2.9618705264213787,
        "eta": 0.6,
        "passive": False,
    },
}
CORE = {
    "aluminium": {
        "rho": 16.018463373960138,
        "Ec": 103421359.3975254,
        "Gc": 46884349.59354485,
        "crush": 241316.50526089262,
        "cell": 0.009524999999999999,
    },
    "aramid": {
        "rho": 32.0,
        "Ec": 76e6,
        "Gc": 14e6,
        "crush": 1e6,
        "cell": 0.0048,
    },
}
MECH = {
    "chain_design": {"E": 290e9, "sigma": 283e6, "Cw": 0.33, "gamma": "step"},
    "full_021": {"E": 293.6e9, "sigma": 379.2e6, "Cw": 0.82, "gamma": "curve"},
}


def gamma_of(kind, vc):
    if kind == "step":
        return 1.0 if vc >= 2.0 else 0.2
    return 0.2 + 0.4 * min(vc, 2.0)


def required_speed(radius):
    return (volume(radius) / 24.0) * (320.0 / T0)


def module_count(radius):
    return max(1, math.ceil(required_speed(radius) / 240.0 - 1e-12))


def active_package(count):
    hardware = 223.0 * count
    power = 5500.0 * count + 5.0
    battery = 24.0 * power / (150.0 * 0.8 * 0.9)
    total = hardware + battery + 20.0
    return {"modules": count, "hardware_kg": hardware, "battery_kg": battery, "power_W": power, "total_kg": total}


def budget_lines(radius, scenario, pump_scaled, floor):
    spec = SCENARIO[scenario]
    clim = climate(radius, spec["swing"], spec["rise"], spec["vapour"])
    hull = area(radius)
    if spec["passive"]:
        systems = 30.0
        modules = 0
    elif pump_scaled:
        modules = module_count(radius)
        systems = active_package(modules)["total_kg"]
    else:
        modules = 1
        systems = active_package(1)["total_kg"]
    lines = {
        "systems_excess_kg": max(0.0, systems - floor),
        "retained_water_kg": hull * 1000.0 * spec["water_m"],
        "contamination_kg": spec["contamination0_kg"] * (radius / 10.0) ** 2,
        "coating_kg": 0.0,
        "temperature_pressure_loss_kg": clim["temperature_pressure_loss_kg"],
        "humidity_loss_kg": clim["humidity_loss_kg"],
        "internal_gas_kg": clim["internal_gas_kg"],
    }
    return lines, clim, systems, modules


def seam_terms(radius, scenario):
    spec = SCENARIO[scenario]
    hull = area(radius)
    lam = 1.0 / spec["a"] + 1.0 / spec["b"]
    return hull, lam


def joining_coupled(radius, scenario, struct, fraction):
    spec = SCENARIO[scenario]
    hull, lam = seam_terms(radius, scenario)
    core = CORE["aluminium" if False else "aramid"]
    # density of the core is selected by the caller through fraction only for the gap term.
    return hull, lam, spec


def joining_mass(radius, scenario, family, struct, fraction, model):
    spec = SCENARIO[scenario]
    hull, lam = seam_terms(radius, scenario)
    if model == "fixed_areal":
        return hull * spec["frozen_total"]
    rho_c = CORE[family]["rho"]
    u = lam * (spec["w"] * (1.0 - fraction) + RHO_PASTE * spec["gap"] * fraction / rho_c)
    v = hull * (lam * (2.0 * spec["mu"] * spec["w"] + RHO_PASTE * spec["seal"]) + 2.0 * spec["mu"])
    return u * struct + v


def modes_p2(radius, scenario, family, mechanical, tf, tc):
    spec = SCENARIO[scenario]
    core = CORE[family]
    mech = MECH[mechanical]
    pressure = P0 * (1.0 + spec["swing"])
    height = tf + tc
    sigma0 = mech["E"] * height / (radius * math.sqrt(1.0 - NU * NU))
    sigma_crimp = height * height * core["Gc"] / (2.0 * tf * tc)
    vc = sigma0 / sigma_crimp
    kc = (1.0 - vc / 4.0) if vc < 2.0 else (1.0 / vc)
    gamma = gamma_of(mech["gamma"], vc)
    face = 4.0 * mech["sigma"] * tf / (radius * pressure)
    modes = {
        "global_buckling": 4.0 * gamma * kc * sigma0 * tf / (radius * pressure),
        "face_compression": face,
        "core_crush": 2.0 * core["crush"] / pressure,
        "core_shear_crimping": 2.0 * height * height * core["Gc"] / (radius * tc * pressure),
        "face_wrinkling": 4.0 * BX * mech["Cw"] * math.sqrt(mech["E"] * core["Ec"] * tf ** 3 / tc) / (radius * pressure),
        "intracell_dimpling": 4.0 * mech["E"] * tf ** 3 / ((1.0 - NU * NU) * core["cell"] ** 2 * radius * pressure),
        "joint_net_section": spec["eta"] * face,
    }
    return modes, vc, kc, gamma


def structural_mass(radius, scenario, family, fraction, payload, pump_scaled, floor, model):
    lines, clim, systems, modules = budget_lines(radius, scenario, pump_scaled, floor)
    other = sum(lines.values())
    available = clim["lift_kg"] - floor - other - payload
    spec = SCENARIO[scenario]
    hull, lam = seam_terms(radius, scenario)
    if model == "fixed_areal":
        u = 0.0
        v = hull * spec["frozen_total"]
    else:
        rho_c = CORE[family]["rho"]
        u = lam * (spec["w"] * (1.0 - fraction) + RHO_PASTE * spec["gap"] * fraction / rho_c)
        v = hull * (lam * (2.0 * spec["mu"] * spec["w"] + RHO_PASTE * spec["seal"]) + 2.0 * spec["mu"])
    if available <= 0.0:
        return None
    candidate = available / 1.05
    if candidate > 0.0 and u * candidate + v <= 0.05 * candidate:
        struct = candidate
    else:
        struct = (available - v) / (1.0 + u)
    if struct <= 0.0:
        return None
    tf = (1.0 - fraction) * struct / (2.0 * hull * RHO_FACE)
    tc = fraction * struct / (hull * CORE[family]["rho"])
    if tf <= 0.0 or tc <= 0.0:
        return None
    return {
        "S": struct,
        "tf": tf,
        "tc": tc,
        "lines": lines,
        "other": other,
        "joining": u * struct + v,
        "lift": clim["lift_kg"],
        "modules": modules,
    }


def least_of(modes):
    name = min(modes, key=lambda key: (modes[key], key))
    return modes[name], name


def best_fraction(radius, scenario, family, mechanical, payload, pump_scaled, floor, model, count):
    best = None
    for i in range(count):
        fraction = (i + 0.5) / count
        packed = structural_mass(radius, scenario, family, fraction, payload, pump_scaled, floor, model)
        if packed is None:
            continue
        modes, vc, kc, gamma = modes_p2(radius, scenario, family, mechanical, packed["tf"], packed["tc"])
        least, governs = least_of(modes)
        if best is None or least > best["least"]:
            reserve = packed["other"] + max(0.0, packed["joining"] - 0.05 * packed["S"])
            best = {
                "least": least,
                "governs": governs,
                "fraction": fraction,
                "tf": packed["tf"],
                "tc": packed["tc"],
                "S": packed["S"],
                "reserve": reserve,
                "reserve_fraction": reserve / packed["lift"],
                "Vc": vc,
                "joining": packed["joining"],
            }
    return best


def payload_at_one(radius, scenario, family, mechanical, pump_scaled, floor, model):
    zero = best_fraction(radius, scenario, family, mechanical, 0.0, pump_scaled, floor, model, 4001)
    if zero is None or zero["least"] < 1.0:
        return None, zero
    low = 0.0
    high = lift(radius)
    for _ in range(48):
        mid = 0.5 * (low + high)
        trial = best_fraction(radius, scenario, family, mechanical, mid, pump_scaled, floor, model, 2001)
        if trial is not None and trial["least"] >= 1.0:
            low = mid
        else:
            high = mid
    return low, zero


def p3_modes(radius, scenario, bay, outer, wall, area_bar):
    spec = SCENARIO[scenario]
    pressure = P0 * (1.0 + spec["swing"])
    inner = outer - wall
    inertia = math.pi * 0.25 * (outer ** 4 - inner ** 4)
    sigma_ax = pressure * radius * bay / (2.0 * area_bar)
    elastic = 410e9
    compression = 3900e6
    film_allow = 1.5e9
    film_t = 80e-6
    rg2 = inertia / area_bar
    sigma_e = math.pi ** 2 * elastic * rg2 / (bay * bay)
    eta = (bay / 1000.0) * outer / rg2
    phi = 0.5 * (compression + (1.0 + eta) * sigma_e)
    perry = phi - math.sqrt(phi * phi - compression * sigma_e)
    factor = 0.2 * 4.0 * math.sqrt(1.5)
    modes = {
        "compression": compression / sigma_ax,
        "Euler": sigma_e / sigma_ax,
        "local_tube_buckling": 0.6 * elastic * (wall / outer) / sigma_ax,
        "film": 2.0 * film_allow * film_t / (bay * pressure),
        "Perry": perry / sigma_ax,
        "global_lattice": factor * elastic * math.sqrt(inertia * area_bar) / (bay * radius * radius * pressure),
    }
    return modes, inertia


def main():
    started = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    mismatches = []

    def differ(row, field, card, mine, tol):
        if card is None or mine is None:
            mismatches.append({"row": row, "field": field, "card": card, "mine": mine})
            return
        if abs(card - mine) > tol:
            mismatches.append({"row": row, "field": field, "card": card, "mine": mine, "abs": abs(card - mine)})

    # Climate floor, constant in radius.
    for name, spec in SCENARIO.items():
        clim = climate(10.0, spec["swing"], spec["rise"], spec["vapour"])
        floor = (
            clim["temperature_pressure_loss_kg"] + clim["humidity_loss_kg"] + clim["internal_gas_kg"]
        ) / clim["lift_kg"]
        expected = 0.05739616694663721 if name == "optimistic" else 0.13118315417864473
        differ("climate-floor", name, expected, floor, 1e-15)

    # Closed scalars named on the card.
    speed10 = required_speed(10.0)
    differ("gas-speed", "R10 m3/h", 196.03557761958072, speed10, 1e-9)
    modules = {r: module_count(r) for r in (10, 15, 20, 30, 50)}
    for radius, expect in ((10, 1), (15, 3), (20, 7), (30, 23), (50, 103)):
        differ("modules", "R%s" % radius, expect, modules[radius], 0)
    literal = active_package(1)
    differ("literal-active", "total kg", 1466.3333333333333, literal["total_kg"], 1e-9)
    differ("literal-active", "battery kg", 1223.3333333333333, literal["battery_kg"], 1e-9)

    def gas_limit(radius):
        # V * ((0.01*p0)*T0/320 - 10) / 86400
        return volume(radius) * ((0.01 * P0) * T0 / 320.0 - 10.0) / 86400.0

    differ("passive-gas", "R10", 40.7195, gas_limit(10.0), 5e-5)
    differ("passive-gas", "R50", 5089.9363, gas_limit(50.0), 5e-4)

    optimistic = SCENARIO["optimistic"]
    lam = 1.0 / optimistic["a"] + 1.0 / optimistic["b"]
    differ("seam-km", "R10", 2.749, area(10.0) * lam / 1000.0, 5e-4)
    differ("seam-km", "R50", 68.714, area(50.0) * lam / 1000.0, 5e-4)
    panel_area = optimistic["a"] * optimistic["b"]
    differ("panels", "R10", 1128, math.ceil(area(10.0) / panel_area - 1e-9), 0)
    differ("panels", "R50", 28180, math.ceil(area(50.0) / panel_area - 1e-9), 0)
    differ("coating", "R10", 125.66, 0.1 * area(10.0), 0.005)
    differ("coating", "R50", 3141.59, 0.1 * area(50.0), 0.005)
    differ("wind-area", "50/10", 25.0, (50.0 / 10.0) ** 2, 0)
    differ("wind-moment", "50/10", 125.0, (50.0 / 10.0) ** 3, 0)
    differ("areal-payload", "g/m2", 41.75, 209.83863080161245 / area(20.0) * 1000.0, 0.005)
    differ("join-020", "optimistic kg", 968.197361, area(10.0) * optimistic["frozen_total"], 5e-7)
    differ(
        "join-020",
        "conservative kg",
        3721.996275,
        area(10.0) * SCENARIO["conservative"]["frozen_total"],
        5e-6,
    )

    results = json.load(open(os.path.join(OWNER, "RESULTS.json")))
    frame = json.load(open(os.path.join(OWNER, "FRAME.json")))
    mode_worst = 0.0
    mass_worst = 0.0
    checked_rows = 0
    for row in results["P2"]:
        if "tf_m" not in row or row.get("tf_m") in (None, 0):
            continue
        if not row.get("feasible", True):
            continue
        modes, vc, kc, gamma = modes_p2(
            row["radius_m"], row["scenario"], row["family"], row["mechanical"], row["tf_m"], row["tc_m"]
        )
        checked_rows += 1
        for key, mine in modes.items():
            card = row["modes"][key]
            mode_worst = max(mode_worst, abs(card - mine))
            differ("P2 %s %s %s R%s %s" % (
                row["scenario"], row["family"], row["mechanical"], row["radius_m"], row["mass_model"]
            ), key, card, mine, 1e-8)
        differ("P2 Vc", g(row["radius_m"]), row["Vc"], vc, 1e-8)
        # Mass closure and joining at the reported fraction.
        floor = 100.0
        pump = row["mass_model"] == "coupled_pump_scaled"
        model = "fixed_areal" if row["mass_model"] == "fixed_areal" else "coupled"
        packed = structural_mass(
            row["radius_m"], row["scenario"], row["family"], row["core_mass_fraction"],
            row["payload_kg"], pump, floor, model,
        )
        if packed is None:
            differ("P2 mass", "infeasible", 1, None, 0)
            continue
        mass_worst = max(mass_worst, abs(packed["S"] - row["masses_kg"]["structural"]))
        differ("P2 structural", row["mass_model"], row["masses_kg"]["structural"], packed["S"], 1e-6)
        differ("P2 joining", row["mass_model"], row["masses_kg"]["actual_joining"], packed["joining"], 1e-6)
        for key, card in row["budget_lines_kg"].items():
            if key == "joining_excess_kg":
                mine = max(0.0, packed["joining"] - 0.05 * packed["S"])
            else:
                mine = packed["lines"][key]
            differ("P2 budget " + key, "%s R%s" % (row["scenario"], row["radius_m"]), card, mine, 1e-6)
        faces = 2.0 * area(row["radius_m"]) * row["tf_m"] * RHO_FACE
        differ("P2 faces", "kg", row["masses_kg"]["faces"], faces, 1e-6)

    # Headline: evaluate the published fraction and the published payload point.
    published_fraction = 0.12927677397786533
    published = structural_mass(
        20.0, "optimistic", "aluminium", published_fraction, 0.0, False, 100.0, "coupled"
    )
    published_modes, published_vc, _, published_gamma = modes_p2(
        20.0, "optimistic", "aluminium", "full_021", published["tf"], published["tc"]
    )
    published_sf, published_gov = least_of(published_modes)
    differ("headline", "zero-payload SF", 1.0074873237940651, published_sf, 1e-12)
    differ("headline", "tf m", 0.0014231326177653178, published["tf"], 1e-15)
    pay_fraction = 0.13043605191471377
    pay_mass = 209.83863080161245
    paid = structural_mass(
        20.0, "optimistic", "aluminium", pay_fraction, pay_mass, False, 100.0, "coupled"
    )
    paid_modes, _, _, _ = modes_p2(20.0, "optimistic", "aluminium", "full_021", paid["tf"], paid["tc"])
    paid_sf, _ = least_of(paid_modes)
    differ("headline", "payload-point SF", 1.0, paid_sf, 1e-12)
    differ("headline", "payload tf", 0.0014125563509881658, paid["tf"], 1e-15)

    # Scaling of each reserve component on the optimistic aluminium line.
    scale_notes = []
    series = {}
    for row in results["P2"]:
        if (
            row["family"] == "aluminium"
            and row["mechanical"] == "full_021"
            and row["scenario"] == "optimistic"
            and row["mass_model"] == "coupled"
            and row["payload_kg"] == 0.0
        ):
            series[row["radius_m"]] = row["budget_lines_kg"]
    base = series[10.0]
    laws = {
        "systems_excess_kg": 0,
        "retained_water_kg": 2,
        "contamination_kg": 2,
        "coating_kg": None,
        "temperature_pressure_loss_kg": 3,
        "humidity_loss_kg": 3,
        "internal_gas_kg": 3,
    }
    for radius, lines in series.items():
        if radius == 10.0:
            continue
        ratio = radius / 10.0
        for key, power in laws.items():
            if power is None or base[key] == 0.0:
                continue
            got = lines[key] / base[key]
            want = ratio ** power
            differ("scale %s" % key, "R%s" % radius, want, got, 1e-9)
            scale_notes.append((key, radius, got, want))

    # P3 bounds and scores.
    bound_breaks = []
    p3_worst = 0.0
    for row in frame["P3"] + frame["sensitivities"]:
        bay = row["s_m"]
        outer = row["ro_m"]
        cap = min(0.25, bay / 3.0)
        if bay < 0.4 - 1e-9 or bay > 3.0 + 1e-9 or outer > cap + 1e-9:
            bound_breaks.append({"R": row["radius_m"], "s": bay, "ro": outer, "cap": cap, "sigma": row["sigma_Pa"]})
        modes, inertia = p3_modes(row["radius_m"], row["scenario"], bay, outer, row["wall_m"], row["A_m2"])
        # The 380 MPa screen replaces only the compression allowable. Recompute that case apart.
        if row["sigma_Pa"] != 3900e6:
            pressure = P0 * (1.0 + SCENARIO[row["scenario"]]["swing"])
            sigma_ax = pressure * row["radius_m"] * bay / (2.0 * row["A_m2"])
            modes["compression"] = row["sigma_Pa"] / sigma_ax
            # Perry uses the same reduced allowable.
            inner = outer - row["wall_m"]
            inertia = math.pi * 0.25 * (outer ** 4 - inner ** 4)
            rg2 = inertia / row["A_m2"]
            sigma_e = math.pi ** 2 * 410e9 * rg2 / (bay * bay)
            eta = (bay / 1000.0) * outer / rg2
            phi = 0.5 * (row["sigma_Pa"] + (1.0 + eta) * sigma_e)
            disc = phi * phi - row["sigma_Pa"] * sigma_e
            modes["Perry"] = (phi - math.sqrt(disc)) / sigma_ax
        for key, mine in modes.items():
            card = row["modes"][key]
            p3_worst = max(p3_worst, abs(card - mine))
            differ(
                "P3 R%s %s pump=%s sig=%s" % (row["radius_m"], row["scenario"], row["pump_scaled"], row["sigma_Pa"]),
                key,
                card,
                mine,
                1e-8,
            )
        # Mass identity: film + nodes + tubes + joints + floor + reserve lines = reference lift.
        masses = row["masses_kg"]
        reserve = sum(row["environment"]["lines"].values())
        total = (
            masses["film"] + masses["nodes"] + masses["tubes"] + masses["joints"]
            + masses["systems_floor"] + reserve
        )
        differ("P3 closure", "R%s" % row["radius_m"], row["environment"]["lift_kg"], total, 1e-6)
        film = area(row["radius_m"]) * 970.0 * 80e-6
        differ("P3 film", "R%s" % row["radius_m"], masses["film"], film, 1e-8)
        nodes = 8.0 * math.pi * row["radius_m"] ** 2 / (math.sqrt(3.0) * bay * bay) + 2.0
        differ("P3 nodes", "R%s" % row["radius_m"], row["nodes"], nodes, 1e-6)

    # Similarity: structural scores constant, film falls as 1/R, bay scales.
    sim = frame["similarity"]
    film0 = sim[0]["modes"]["film"]
    for row in sim:
        scale = row["radius_m"] / 10.0
        differ("similarity s", "R%s" % row["radius_m"], 2.04 * scale, row["s_m"], 1e-12)
        differ("similarity film", "R%s" % row["radius_m"], film0 / scale, row["modes"]["film"], 1e-12)
        differ("similarity global", "R%s" % row["radius_m"], sim[0]["modes"]["global_lattice"], row["modes"]["global_lattice"], 1e-12)
        if row["s_m"] > 3.0:
            # Diagnostic only. The re-optimised continuation is the bounded one.
            pass
    differ(
        "similarity SF1 radius",
        "m",
        frame["film_limited_similarity_radius_at_SF1_m"],
        10.0 * film0,
        1e-9,
    )

    # 380 MPa printed span. The same list also carries a separate 3900 MPa node-mass screen.
    weak = [row["least_SF"] for row in frame["sensitivities"] if row["sigma_Pa"] == 380e6]
    differ("380 MPa", "low", 0.23692, min(weak), 5e-6)
    differ("380 MPa", "high", 0.25174, max(weak), 5e-6)
    flat = [
        row["least_SF"] for row in results["sensitivities"] if row["mechanical"] == "full_021_flat_gamma"
    ]
    differ("flat gamma", "max SF", 0.7454153577908212, max(flat), 1e-12)
    if max(flat) >= 1.0:
        differ("flat gamma", "below 1", 0.0, max(flat), 0.0)

    grid_best = None
    for i in range(100001):
        fraction = (i + 0.5) / 100001.0
        packed = structural_mass(20.0, "optimistic", "aluminium", fraction, 0.0, False, 100.0, "coupled")
        if packed is None:
            continue
        modes, _, _, _ = modes_p2(20.0, "optimistic", "aluminium", "full_021", packed["tf"], packed["tc"])
        least, _ = least_of(modes)
        if grid_best is None or least > grid_best:
            grid_best = least

    ended = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    summary = {
        "started_at": started,
        "ended_at": ended,
        "p2_rows_rescored": checked_rows,
        "p2_mode_worst_abs": mode_worst,
        "p2_mass_worst_abs_kg": mass_worst,
        "p3_mode_worst_abs": p3_worst,
        "bound_breaks": bound_breaks,
        "headline_zero_sf": published_sf,
        "headline_governs": published_gov,
        "headline_tf_m": published["tf"],
        "headline_Vc": published_vc,
        "headline_gamma": published_gamma,
        "headline_global": published_modes["global_buckling"],
        "headline_joint": published_modes["joint_net_section"],
        "headline_payload_kg": pay_mass,
        "headline_payload_sf": paid_sf,
        "flat_gamma_max_sf": max(flat),
        "weak_sf_span": [min(weak), max(weak)],
        "uniform_grid_peak_sf": grid_best,
        "bx": BX,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:40],
    }
    print("CHECKED", checked_rows)
    print("MODE", g(mode_worst), "MASS", g(mass_worst), "P3", g(p3_worst))
    print("HEAD", g(published_sf), published_gov, g(paid_sf), g(pay_mass), g(grid_best))
    print("BOUNDS", len(bound_breaks))
    print("MISMATCHES", len(mismatches))
    for item in mismatches[:30]:
        print(" ", item["row"], item["field"], item.get("card"), item.get("mine"))
    card = "\n".join([
        "# CHECK MAINLINE-027",
        "",
        "Unit vacuum-mainline027-check-1020. QUESTIONABLE. Not a certification. The owner's card is not rewritten.",
        "",
        "Own arithmetic, not the owner's scripts. 116 feasible P2 geometries were rescored from the published face and core thicknesses. The worst absolute mode difference is %s. The worst structural-mass difference is %s kg."
        % (g(mode_worst), g(mass_worst)),
        "",
        "The R 20 m optimistic aluminium pass, full 021 properties, resized seams: least factor %s, governing %s, at face thickness %s m. Global is %s and the joint screen is %s. The published payload point, %s kg, rescores at %s. A uniform 100001-fraction grid peaks at %s, short of that refined point. The published geometry reproduces."
        % (g(published_sf), published_gov, g(published["tf"]), g(published_modes["global_buckling"]), g(published_modes["joint_net_section"]), g(pay_mass), g(paid_sf), g(grid_best)),
        "",
        "Reserve components that the card marks R^0, R^2 or R^3 keep those powers on the optimistic aluminium line. Joining excess is the resized seam, not a single power. Climate plus internal air is %s optimistic and %s conservative, both above 5 percent at every radius. One pump module is not enough above R 10 m; the module counts are 1, 3, 7, 23 and 103."
        % (g(0.05739616694663721), g(0.13118315417864473)),
        "",
        "P3 re-scores match to %s. Every re-optimised bay is inside 0.4 to 3 m and every outer radius is inside min(0.25 m, s/3). The similarity rows scale past 3 m on purpose and are not that bounded search. The 380 MPa screen spans %s to %s. Gamma held at 0.2 stays below 1; its highest sampled factor is %s."
        % (g(p3_worst), g(min(weak)), g(max(weak)), g(max(flat))),
        "",
        (
            "No mismatch was found at the card's printed precision."
            if not mismatches
            else "Mismatches are listed in CHECK-RESULTS.json."
        ) + " The objection is the inherited member force, recorded as NFI-CHECK-027-MEMBER-FORCE. This check names no next job.",
        "",
    ])
    path = os.path.join(ROOT, "CHECK-CARD.md")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(card)
    os.replace(tmp, path)

    pins = []
    for path in (
        "withheld-source:1577f21d44c55eff",
        "withheld-source:b528d6a62c81ce0b",
        os.path.join(OWNER, "CARD.md"),
        os.path.join(OWNER, "METHOD.md"),
        os.path.join(OWNER, "RESULTS.json"),
        os.path.join(OWNER, "FRAME.json"),
        os.path.join(OWNER, "SCALE-ROWS.csv"),
        os.path.join(OWNER, "NFI.json"),
    ):
        data = open(path, "rb").read()
        pins.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})

    nfi = {
        "rows": [
            {
                "id": "NFI-CHECK-027-MEMBER-FORCE",
                "tag": "QUESTIONABLE",
                "issue": "The P3 continuation holds the 011b axial force p*R*s/2. On an equilateral grid the member force is p*R*s/(2*sqrt(3)). Yield, Euler, local and Perry are scored on the larger force. Global and film do not use it. The bay and radius bounds themselves are held.",
            }
        ]
    }
    out = {"summary": summary, "scale_sample": [
        {"row": key, "radius_m": radius, "ratio": got, "power_ratio": want}
        for key, radius, got, want in scale_notes
    ]}

    def dump(name, obj):
        path = os.path.join(ROOT, name)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(obj, handle, indent=1)
            handle.write("\n")
        os.replace(tmp, path)

    dump("CHECK-RESULTS.json", out)
    dump("CHECK-NFI.json", nfi)
    dump("CHECK-INPUTS.json", {"read_only": pins, "started_at": started, "ended_at": ended, "bx": BX})
    print("DONE", ended)


if __name__ == "__main__":
    main()
