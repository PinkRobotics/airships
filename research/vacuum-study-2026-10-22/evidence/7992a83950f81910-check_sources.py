"""Recompute the ancillary numbers quoted in the 022b/022c report bodies."""

import json
import math
from pathlib import Path
import re

import check_model as cm


def main():
    checks = []

    def check(label, owner, own, rel=2e-9):
        passed = math.isclose(owner, own, rel_tol=rel, abs_tol=1e-9)
        checks.append({"field": label, "owner": owner, "checker": own,
                       "delta": own - owner, "passed": passed})

    j = json.loads((cm.ROOT / "inputs/023/RESULTS.json").read_text())
    coeff = {}
    for name, rho, strength in (("ti_sleeve", 4430., 827e6),
                                ("invar_sleeve", 8050., 276e6),
                                ("cfrp_wrap", 1550., 1470e6)):
        value = rho / (strength * 2 * math.pi * 28.9e6)
        coeff[name] = value
        check(name + "/coefficient", j["mass_coefficients"][name]["C_end_kg_m_per_N2"], value)
    s, ro, wall = 2.04, .12368836237368608, .0008802990936851718
    count, nodes, force, _, _ = cm.geometry(s, "equilateral")
    rounded = {"ti_sleeve": cm.JOINTS["ti"], "cfrp_wrap": cm.JOINTS["cfrp"]}
    round_deltas = {}
    for name, val in rounded.items():
        round_deltas[name] = {
            "source_coefficient": coeff[name], "used_coefficient": val,
            "fractional_difference": val / coeff[name] - 1,
            "source_exact_total_mass_kg": 2 * count * coeff[name] * force**2 / ro,
            "scan_total_mass_kg": 2 * count * val * force**2 / ro,
            "interpretation": "Rounding of supplied coefficient, not a mismatched formula",
        }
    # Braze row is a new closed mass budget at the held radius, not old tube area.
    budget = cm.LIFT - 50 - 97.515 - cm.NODE * nodes
    braze_fraction = force / (math.pi * 25e6 * s * ro)
    tube_mass = budget / (1 + braze_fraction)
    braze_mass = tube_mass * braze_fraction
    check("023/braze_frozen_mass_kg",
          j["joints"]["sic_braze"]["frozen_k0.2"]["m_joint_kg"], braze_mass)
    diameter = math.sqrt(2 * force / (math.pi * (.6 * 827e6)))
    pin_mass = 4430 * math.pi * diameter**2 / 4 * (3 * diameter)
    bearing = force / (2 * wall * diameter)
    check("023/pin_diameter_m", j["pin_clevis_reference"]["d_m"], diameter)
    check("023/pin_mass_kg", j["pin_clevis_reference"]["mass_kg"], pin_mass)
    check("023/pin_bearing_Pa", j["pin_through_wall_bearing_Pa"], bearing)

    film = json.loads((cm.ROOT / "inputs/024/RESULTS.json").read_text())
    for row in film["candidates"]:
        if row["design_allowable_Pa"] is None:
            continue
        factor = 2 if row["form"] == "filament_crossply" else 1
        t = factor * cm.P * s / (2 * row["design_allowable_Pa"])
        mass = cm.SURFACE * row["density_kg_m3"] * t
        check("024/" + row["key"] + "/thickness_m", row["thickness_m"], t)
        check("024/" + row["key"] + "/mass_kg", row["mass_kg"], mass)

    # Two specific inherited-check rows quoted as 1.205 and 1.130 in 022b.
    inherited = json.loads((cm.ROOT / "inputs/011b-check/RESULTS-EXTRA.json").read_text())
    quoted = []
    for row in inherited["restatements"]:
        if not (row["material"].startswith("SiC") and row["grid"] == "equilateral_triangular"
                and row["k"] == .2 and row["local_sp8007"] and row["force_factor"] < .6):
            continue
        s, ro = row["s_m"], row["r_o_m"]
        count, nodes, force, coeff_g, _ = cm.geometry(s, "equilateral")
        tube = (cm.LIFT - row["systems_kg"] - row["margin_kg"] - 97.515 - cm.NODE * nodes) / 1.05
        area = tube / (count * s * cm.RHO)  # this quoted 011b model uses chord length
        ri = math.sqrt(ro**2 - area / math.pi)
        wall = area / (math.pi * (ro + ri))
        inertia = area * (ro**2 + ri**2) / 4
        mean = force / area
        euler = math.pi**2 * cm.E * inertia / (area * s**2)
        eta = .001 * s * ro * area / inertia
        phi = (3900e6 + (1 + eta) * euler) / 2
        perry = 3900e6 * euler / (phi + math.sqrt(phi**2 - 3900e6 * euler))
        gamma = .099 + .901 * math.exp(-math.sqrt(ro / wall) / 16)
        modes = {
            "yield": 3900e6 / mean, "euler": euler / mean,
            "local": gamma * .6 * cm.E * wall / ro / mean,
            "film": 2 * 1.5e9 * 80e-6 / (cm.P * s),
            "perry": perry / mean,
            "global": .2 * coeff_g * cm.E * math.sqrt(inertia * area) / (s * cm.R**2 * cm.P),
        }
        label = "quoted011b/sys" + str(row["systems_kg"])
        for key, value in modes.items():
            check(label + "/" + key, row["SF"][key], value)
        check(label + "/least", row["SF_least"], min(modes.values()))
        quoted.append({"owner": row["SF_least"], "checker": min(modes.values()),
                       "systems_kg": row["systems_kg"], "margin_kg": row["margin_kg"]})

    # NASA gamma uses the caller's radius convention in 022b; show its effect.
    r = json.loads((cm.ROOT / "inputs/GAMMA.json").read_text())["cases"]["percent_crush_5"]["equilateral"]
    outer_gamma = .099 + .901 * math.exp(-math.sqrt(r["r_o_m"] / r["t_w_m"]) / 16)
    mid_gamma = .099 + .901 * math.exp(-math.sqrt(r["r_o_m"] / r["t_w_m"] - .5) / 16)
    arithmetic_check_count = len(checks)

    number = re.compile(r"(?<![\w])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")

    def printed_check(label, text, expected, marker="least "):
        printed = [float(v) for v in number.findall(text.split(marker, 1)[1])]
        if len(printed) != len(expected):
            raise ValueError((label, len(printed), len(expected), text))
        for index, (value, reference) in enumerate(zip(printed, expected)):
            check(label + "/printed_" + str(index), value, reference, rel=5e-11)

    for stage in ("GAMMA", "FOLD"):
        doc = json.loads((cm.ROOT / "inputs" / (stage + ".json")).read_text())
        lines = (cm.ROOT / "inputs" / (stage + ".md")).read_text().splitlines()
        for name, block in doc["cases"].items():
            for grid, row in block.items():
                label = name + " " + grid
                line = next(line for line in lines if line.startswith(label + " least "))
                numbers = [row[k] for k in ("SF_least", "s_m")]
                numbers += [row["r_o_m"] * 1e3, row["t_w_m"] * 1e3, row["rt"],
                            row["gamma"], row["t_film_m"] * 1e3]
                numbers += [row["SF_" + mode] for mode in cm.MODES]
                numbers += [row["m_tube"], row["m_joint"]]
                if stage == "FOLD":
                    numbers += [row["m_film"]]
                numbers += [row["sag_kg"], row["k04_SF_least"]]
                printed_check(stage + "/" + label, line, numbers)
    eq = json.loads((cm.ROOT / "inputs/EQUILIBRIUM.json").read_text())
    lines = [line for line in (cm.ROOT / "inputs/EQUILIBRIUM.md").read_text().splitlines()
             if ". Least SF " in line]
    rows = [r for block in eq["cases"].values() for r in block.values()]
    if len(lines) != len(rows):
        raise ValueError("EQUILIBRIUM prose row count differs")
    for index, (line, row) in enumerate(zip(lines, rows)):
        numbers = [row["SF_least"], row["s_m"], row["r_o_m"] * 1e3,
                   row["t_w_m"] * 1e3, row["rt"], row["t_film_m"] * 1e3]
        numbers += [row["SF_" + mode] for mode in cm.MODES]
        numbers += [row[k] for k in ("m_tube", "m_nodes", "m_joint", "m_film", "sag_kg")]
        printed_check("EQUILIBRIUM/row" + str(index), line, numbers, marker="Least SF ")
    sagdoc = json.loads((cm.ROOT / "inputs/022c/SAG.json").read_text())
    lines = [line for line in (cm.ROOT / "inputs/022c/SAG.md").read_text().splitlines()
             if " equilateral least " in line]
    rows = [block["equilateral"] for kind in ("cap", "membrane")
            for block in sagdoc[kind].values()]
    if len(lines) != len(rows):
        raise ValueError("SAG prose row count differs")
    for index, (line, row) in enumerate(zip(lines, rows)):
        numbers = [row["SF_least"], row["s_m"], row["r_o_m"] * 1e3, .25,
                   row["t_w_m"] * 1e3, row["rt"], row["gamma"],
                   row["t_film_m"] * 1e3, row["sag_kg"]]
        numbers += [row["SF_" + mode] for mode in cm.MODES]
        printed_check("SAG/row" + str(index), line, numbers)
    result = {
        "classification": "QUESTIONABLE values retained with their source limitations",
        "checks": checks, "all_passed": all(c["passed"] for c in checks),
        "independent_ancillary_arithmetic_count": arithmetic_check_count,
        "printed_row_comparison_count": len(checks) - arithmetic_check_count,
        "quoted_011b_reference_rows": quoted,
        "coefficient_rounding": round_deltas,
        "braze_mass_kg": braze_mass,
        "pin_bearing_Pa": bearing,
        "gamma_radius_convention": {
            "outer_gamma": outer_gamma, "mid_surface_gamma": mid_gamma,
            "relative_change": mid_gamma / outer_gamma - 1,
            "interpretation": "Document radius choice; this small convention change does not establish long-ceramic-strut validity",
        },
        "Zylon_source_contract": {
            "source": "inputs/024/INPUTS.json formulae.crossply and inputs/024/RESULTS.json",
            "t_total": "2*p*s/(2*sigma_fiber)",
            "source_effective_biaxial_strength_Pa": 3.48e9 / 2,
            "scan_effective_strength_Pa": 3.48e9,
            "scan_film_capacity_over_source": 2.,
        },
        "NASA_source": {
            "url": "https://ntrs.nasa.gov/api/citations/20205011530/downloads/20205011530%20Rev%202FINALa%201-2023.pdf",
            "locator": "printed pp.23-25, equations9-10 and L/r caution",
            "retrieved_on": "2026-10-20",
        },
    }
    (cm.ROOT / "SOURCE-CHECKS.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"comparisons": len(checks), "mismatches": sum(not c["passed"] for c in checks),
                      "quoted_011b": quoted}, indent=2))


if __name__ == "__main__":
    main()
