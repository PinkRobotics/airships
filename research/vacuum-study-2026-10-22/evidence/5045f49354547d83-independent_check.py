"""Independent reconstruction from pinned JSON data and downloaded source tables.

No owner code is imported, read, or executed. CR-1457 equations were transcribed
from the page images listed in SOURCE-REVIEW.md. The 1/8000 search is our own
grid; its agreement with the filed optima is a measured result, not a proof of
the owner's implementation. A separate continuous search checks resolution.
"""
import json
import math
import re
from pathlib import Path
from fractions import Fraction

import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT / "inputs/014b/INPUTS.json").read_text())
O = json.loads((ROOT / "inputs/014b/RESULTS.json").read_text())
P = json.loads((ROOT / "inputs/009c5/POINT.json").read_text())
F = I["faces"]
C = I["cores_eligible"]
byface = {f["name"]: f for f in F}
bycore = {c["name"]: c for c in C}
R = 10.0
AREA = 4 * math.pi * R**2
PRESSURE = I["p_ext_Pa"]
LIFT = I["lift_kg"]
NU = 0.33
POISSON = 1 - NU**2
BIAXIAL = brentq(lambda b: b**3 + b - 1, 0, 1, xtol=5e-15)
PSI = 0.45359237 * 9.80665 / 0.0254**2
PCF = 0.45359237 / 0.3048**3
checks = {"014b": [], "009c5": [], "sources": [], "primary_face_provenance": []}


def check(card, path, reported, value, rtol=2e-10, atol=2e-13):
    if isinstance(reported, (int, float)) and not isinstance(reported, bool):
        ok = math.isclose(reported, float(value), rel_tol=rtol, abs_tol=atol)
        value = float(value)
        delta = value - reported
    else:
        ok, delta = reported == value, None
    checks[card].append(dict(path=path, reported=reported, independent=value,
                             passed=bool(ok), difference=delta))


def mass_limit(margin):
    return ((1 - margin) * LIFT - 100) / 1.05


def arrays(face, core, fraction, kd, margin=0.0, coefficient=None):
    """Equal-area thin-shell mass model; stress equations first, then SF."""
    x = np.asarray(fraction)
    m = mass_limit(margin)
    tf = m * (1 - x) / (2 * AREA * face["rho"])
    d = m * x / (AREA * core["rho"])
    h = d + tf
    membrane = PRESSURE * R / (4 * tf)
    stress0 = face["E_Pa"] * h / (math.sqrt(POISSON) * R)
    crimp = h**2 * core["Gc_Pa"] / (2 * tf * d)
    vc = stress0 / crimp
    kc = np.where(vc <= 2, 1 - vc / 4, 1 / vc)
    # Filed convention reproduced, with the source's equality handled in NFI.
    gamma = np.where(vc > 2, 1, kd)
    if core["form"] == "honeycomb":
        q = 0.33 if coefficient is None else coefficient
        wrinkle = q * np.sqrt(face["E_Pa"] * core["Ec_Pa"] * tf / d)
    else:
        q = 0.50 if coefficient is None else coefficient
        wrinkle = q * (face["E_Pa"] * core["Ec_Pa"] * core["Gc_Pa"]
                       / POISSON)**(1 / 3)
    sfs = {
        "global_buckling": gamma * kc * stress0 / membrane,
        "face_yield": face["sigma_Pa"] / membrane,
        "core_shear_crimping": crimp / membrane,
        "core_crush": np.ones_like(x) * core["crush_Pa"] / (PRESSURE / 2),
        "face_wrinkling": BIAXIAL * wrinkle / membrane,
    }
    if "s_cell_m" in core:
        sfs["intracell_dimpling"] = (
            2 * face["E_Pa"] / POISSON * (tf / core["s_cell_m"])**2 / membrane
        )
    return tf, d, h, vc, kc, gamma, sfs


def point(face, core, x, kd, margin=0, coefficient=None):
    tf, d, h, vc, kc, gamma, raw = arrays(face, core, x, kd, margin, coefficient)
    sfs = {k: float(v) for k, v in raw.items()}
    modes = dict(sfs)
    if vc > 2:  # The two names denote the same pressure here.
        del modes["global_buckling"]
    modes = sorted(modes.items(), key=lambda kv: kv[1])
    balance = face["sigma_Pa"] * R * math.sqrt(POISSON) / (kd * face["E_Pa"])
    return dict(core_mass_fraction=float(x), tf_m=float(tf), core_m=float(d),
                h_m=float(h), Vc=float(vc), Kc=float(kc), gamma=float(gamma),
                branch="shear_crimping" if vc > 2 else "stiff_or_moderate_core",
                sfs=sfs, governing=modes[0][0], least_SF=modes[0][1],
                second_mode=modes[1][0], second_SF=modes[1][1],
                factor_to_SF_1=1 / modes[0][1], d_balance_m=balance,
                h_over_d_balance=float(h) / balance)


GRID = np.arange(1, 8000, dtype=float) / 8000


def search(face, core, kd, margin=0, grid=GRID):
    values = arrays(face, core, grid, kd, margin)[-1]
    least = np.min(np.array(list(values.values())), axis=0)
    return point(face, core, grid[int(np.argmax(least))], kd, margin)


def compare_point(card, path, owner, ours, nine=False):
    for k in ["core_mass_fraction", "tf_m", "core_m", "h_m", "Vc", "Kc",
              "branch", "least_SF", "second_SF", "d_balance_m",
              "h_over_d_balance", "factor_to_SF_1"]:
        if k in owner:
            check(card, path + "." + k, owner[k], ours[k])
    gamma_key = "gamma_d" if nine else "gamma"
    check(card, path + "." + gamma_key, owner[gamma_key], ours["gamma"])
    for k in ["governing", "second_mode"]:
        value = ours[k].replace("face_yield", "face_compression") if nine else ours[k]
        check(card, path + "." + k, owner[k], value)
    skey = "modes_at_0.20_design_wrinkle" if nine else "sfs"
    for k, v in owner[skey].items():
        check(card, path + "." + skey + "." + k, v,
              ours["sfs"][k.replace("face_compression", "face_yield")])


def source_tables():
    """Parse independent vendor text, after visually checking table headings."""
    criii = {}
    pages = (ROOT / "sources/criii.txt").read_text().split("\f")
    for alloy, page in [(5052, pages[3]), (5056, pages[4])]:
        for line in page.splitlines():
            a = line.split()
            if len(a) == 14 and re.fullmatch(r"\d+/\d+", a[0]) and float(a[1]) <= 4:
                vals = list(map(float, a[1:]))
                criii[(alloy, a[0], vals[0])] = dict(
                    rho=vals[0]*PCF, Ec_Pa=vals[5]*1000*PSI,
                    Gc_Pa=vals[12]*1000*PSI, Gl_Pa=vals[9]*1000*PSI,
                    crush_Pa=vals[6]*PSI, shear_strength_L_Pa=vals[7]*PSI,
                    shear_strength_W_Pa=vals[10]*PSI,
                    s_cell_m=float(Fraction(a[0]))*0.0254)
    plas = {}
    for line in (ROOT / "sources/plascore.txt").read_text().splitlines():
        a = line.split()
        if len(a) == 20 and re.fullmatch(r"\d+/\d+", a[0]) and float(a[3]) <= 64:
            v = list(map(float, a[1:]))
            trans = criii[(5052, a[0], v[1])]
            plas[(a[0], v[1])] = dict(rho=v[2], Ec_Pa=trans["Ec_Pa"],
                Gc_Pa=v[17]*1000*PSI, Gl_Pa=v[11]*1000*PSI,
                crush_Pa=v[3]*PSI, shear_strength_L_Pa=v[7]*PSI,
                shear_strength_W_Pa=v[13]*PSI,
                s_cell_m=float(Fraction(a[0]))*0.0254)
    attr = {}
    pattern = re.compile(r"^\s*(HFT|HRH-49)\s*[–-]\s*(\d+/\d+)\s*[–-]\s*(\d+\.\d+)\s+(.*)")
    for line in (ROOT / "sources/attributes.txt").read_text().splitlines():
        match = pattern.match(line)
        if match and float(match[3]) <= 4 and "-" not in match[4]:
            a = list(map(float, match[4].split()))
            if len(a) == 9:
                attr[(match[1], match[2], float(match[3]))] = dict(
                    rho=float(match[3])*PCF, Ec_Pa=a[2]*1000*PSI,
                    Gc_Pa=a[8]*1000*PSI, Gl_Pa=a[5]*1000*PSI,
                    crush_Pa=a[0]*PSI, shear_strength_L_Pa=a[3]*PSI,
                    shear_strength_W_Pa=a[6]*PSI,
                    s_cell_m=float(Fraction(match[2]))*0.0254)
    for i, c in enumerate(C):
        if i < 2:
            source = (dict(rho=32, Ec_Pa=17e6, Gc_Pa=13e6, crush_Pa=.4e6)
                      if i == 0 else
                      dict(rho=32, Ec_Pa=76e6, Gc_Pa=14e6,
                           crush_Pa=1e6, s_cell_m=.0048))
        elif i < 8:
            parent = C[0] if c["form"] == "foam" else C[1]
            ratio = c["rho"]/parent["rho"]
            source = dict(Ec_Pa=parent["Ec_Pa"]*ratio**2,
                          Gc_Pa=parent["Gc_Pa"]*ratio**2,
                          crush_Pa=parent["crush_Pa"]*ratio**1.5)
            check("sources", c["name"]+".tag", c["tag"], "PROJECTION")
        elif c["name"].startswith("Hexcel CR-III"):
            source = criii[(int(c["name"].split()[2]), c["cell"], c["pcf"])]
        elif c["name"].startswith("Plascore"):
            source = plas[(c["cell"], c["pcf"])]
        else:
            family = "HFT" if "HFT" in c["name"] else "HRH-49"
            source = attr[(family, c["cell"], c["pcf"])]
        for k, v in source.items():
            check("sources", f"cores[{i}].{k}", c[k], v)
        if "Gl_Pa" in c:
            check("sources", f"cores[{i}].W_is_lower", c["Gc_Pa"] <= c["Gl_Pa"], True)
        check("sources", f"cores[{i}].source_present", bool(c.get("source")), True)
        if i < 2 or i >= 8:
            check("sources", f"cores[{i}].tag", c["tag"], "QUESTIONABLE")
    check("sources", "pcf_to_kg_m3", I["pcf_to_kg_m3"], PCF)
    return {"CRIII_rows": len(criii), "Plascore_rows": len(plas),
            "HFT_HRH49_rows": len(attr)}


def run():
    table_counts = source_tables()
    inherited = json.loads((ROOT / "inputs/inherited/vacuum-mainline008-material-gap-1019-RESULTS.json").read_text())
    old = {v["name"]: v for v in inherited["candidates_ranked_by_least_SF_P2E"]}
    for i, f in enumerate(F):
        src = old[f["name"]]
        for key, val in dict(rho=src["rho"], E_Pa=src["E_GPa"]*1e9,
                             sigma_Pa=src["sigma_c_MPa"]*1e6, tag=src["tag"]).items():
            check("sources", f"faces[{i}].{key}", f[key], val)
        check("sources", f"faces[{i}].source_present", bool(src.get("source")), True)
    winners = []
    all_core = []
    for i, row in enumerate(O["optima"]):
        f = byface[row["face"]]
        kd = row["kd"]
        check("014b", f"optima[{i}].kd", kd, [.2, .1407][i % 2])
        check("014b", f"optima[{i}].theoretical.k", row["theoretical"]["k"], .82)
        points = [search(f, c, kd) for c in C]
        bestidx = int(np.argmax([v["least_SF"] for v in points]))
        best = points[bestidx]
        winner = dict(best, face=f["name"], core_name=C[bestidx]["name"],
                      kd=kd, face_tag=f["tag"])
        winners.append(winner)
        check("014b", f"optima[{i}].core_name", row["core_name"], winner["core_name"])
        compare_point("014b", f"optima[{i}]", row, best)
        core = C[bestidx]
        for key, val in dict(core_density_kg_m3=core["rho"], s_cell_m=core.get("s_cell_m"),
                             core_tag=core["tag"], face_tag=f["tag"]).items():
            if key in row:
                check("014b", f"optima[{i}].{key}", row[key], val)
        theor = point(f, core, best["core_mass_fraction"], kd, coefficient=.82)
        for k in ["governing", "least_SF", "second_mode", "second_SF", "factor_to_SF_1"]:
            check("014b", f"optima[{i}].theoretical.{k}", row["theoretical"][k], theor[k])
        check("014b", f"optima[{i}].theoretical.face_wrinkling",
              row["theoretical"]["face_wrinkling"], theor["sfs"]["face_wrinkling"])
        baseline = old[f["name"]]["rows"]["P2-E"]["least_SF"]
        check("014b", f"optima[{i}].p2e_least_SF_008", row["p2e_least_SF_008"], baseline)
        check("014b", f"optima[{i}].gain_vs_008_P2E", row["gain_vs_008_P2E"],
              best["least_SF"]/baseline)
        for j, (record, p, core) in enumerate(zip(row["per_density"], points, C)):
            for key, value in dict(core=core["name"], density=core["rho"],
                                   family=core["family"], tag=core["tag"],
                                   least_SF=p["least_SF"], governing=p["governing"]).items():
                check("014b", f"optima[{i}].per_density[{j}].{key}", record[key], value)
            all_core.append(dict(face=f["name"], core=core["name"], kd=kd, **p))
    for key, kd, questionable in [
            ("best_three_kd_0_20", .2, False),
            ("best_three_questionable_kd_0_20", .2, True),
            ("best_three_kd_0_1407", .1407, False)]:
        ranked = sorted([w for w in winners if w["kd"] == kd and
                         (not questionable or w["face_tag"] == "QUESTIONABLE")],
                        key=lambda v: v["least_SF"], reverse=True)[:3]
        for i, (row, calc) in enumerate(zip(O[key], ranked)):
            for k in ["face", "core_name", "least_SF", "governing", "tf_m", "core_m"]:
                if k in row:
                    check("014b", f"{key}[{i}].{k}", row[k], calc[k])
    check("014b", "crush_target_Pa", O["crush_target_Pa"], PRESSURE/2)
    check("014b", "structural_mass_kg", O["structural_mass_kg"], mass_limit(0))
    check("014b", "checks.biaxial_factor", O["checks"]["biaxial_factor"], BIAXIAL)
    tf0 = mass_limit(0)/(4*AREA*2700)
    d0 = mass_limit(0)/(2*AREA*16)
    classic = .2*4*tf0*(d0+tf0)*68.9e9/(R**2*math.sqrt(POISSON)*PRESSURE)
    check("014b", "checks.classical_SF", O["checks"]["classical_SF"], classic)
    for key, val in dict(schema=1, kd_handbook=.2, kd_brief=.1407,
                         nu_used_for_every_face=.33).items():
        check("014b", key, O[key], val)
    for key, val in dict(foam_design=.5, honeycomb_design=.33, theoretical=.82).items():
        check("014b", "wrinkling_coefficients."+key, O["wrinkling_coefficients"][key], val)
    face, core = byface["Beryllium S-200F"], bycore["Hexcel HRH-10-4.8-32"]
    nine = {}
    for key in ["optimum", "other_branch"]:
        row = P[key]
        a = point(face, core, row["core_mass_fraction"], .2, .05)
        nine[key] = a
        compare_point("009c5", key, row, a, nine=True)
        mass = mass_limit(.05)
        m = dict(structural=mass, faces=2*AREA*a["tf_m"]*face["rho"],
                 core=AREA*a["core_m"]*core["rho"], joints=.05*mass, systems=100,
                 total=.95*LIFT, payload=.05*LIFT, float_margin=.05)
        for k, val in m.items():
            check("009c5", key+".masses_kg."+k, row["masses_kg"][k], val)
        nine[key]["masses_kg"] = m
    for k, row in P["levels"].items():
        calc = point(face, core, P["optimum"]["core_mass_fraction"], float(k), .05)
        for name in ["Vc", "Kc", "least_SF", "second_SF", "gamma_d"]:
            check("009c5", f"levels.{k}.{name}", row[name],
                  calc[name.replace("gamma_d", "gamma")])
        for name, val in row["modes"].items():
            check("009c5", f"levels.{k}.modes.{name}", val,
                  calc["sfs"][name.replace("face_compression", "face_yield")])
    theory = point(face, core, P["optimum"]["core_mass_fraction"], .2, .05, .82)
    check("009c5", "wrinkle_coefficient_0.82.SF_wrinkle",
          P["wrinkle_coefficient_0.82"]["SF_wrinkle"], theory["sfs"]["face_wrinkling"])
    check("009c5", "wrinkle_coefficient_0.82.least_SF",
          P["wrinkle_coefficient_0.82"]["least_SF"], theory["least_SF"])
    ceiling = search(face, core, .2)
    check("009c5", "ceiling_check.fraction", P["ceiling_check"]["fraction"], ceiling["core_mass_fraction"])
    check("009c5", "ceiling_check.least_SF", P["ceiling_check"]["least_SF"], ceiling["least_SF"])
    check("009c5", "nfi[4].factor_on_Ec", P["nfi"][4]["factor_on_Ec"], (.82/.33)**2)
    check("009c5", "nfi[4].design", P["nfi"][4]["design"], .33)
    check("009c5", "nfi[4].theoretical", P["nfi"][4]["theoretical"], .82)
    check("009c5", "schema", P["schema"], 1)
    check("009c5", "point.payload_margin", P["point"]["payload_margin"], .05)
    for key in ["Vc", "Kc", "gamma_d"]:
        check("009c5", "branch."+key, P["branch"][key],
              nine["optimum"][key.replace("gamma_d", "gamma")])
    check("009c5", "sources.RESULTS.json.bytes", P["sources"]["RESULTS.json"]["bytes"],
          (ROOT / "inputs/inherited/vacuum-mainline007-core-trade-1019-RESULTS.json").stat().st_size)
    # Independent analytic balance search: refine each branch and check endpoints.
    def difference(x):
        s = point(face, core, x, .2, .05)["sfs"]
        return s["core_shear_crimping"]-s["face_wrinkling"]
    balance = brentq(difference, .18, .21, xtol=5e-15)
    exact_balance = point(face, core, balance, .2, .05)
    # Vc can have two roots: a very thin core and the ordinary moderate-core side.
    critical = []
    previous_x = 1e-10
    previous_y = point(face, core, previous_x, .2, .05)["Vc"]-2
    for x in np.linspace(1e-6, 1-1e-6, 10001):
        y = point(face, core, x, .2, .05)["Vc"]-2
        if previous_y*y < 0:
            critical.append(brentq(lambda q: point(face, core, q, .2, .05)["Vc"]-2,
                                  previous_x, x, xtol=5e-15))
        previous_x, previous_y = x, y
    fine = search(face, core, .2, .05, np.linspace(1e-6, 1-1e-6, 1000001))
    nine["independent_fine_grid"] = fine
    nine["continuous_crimp_wrinkle_balance"] = exact_balance
    nine["Vc_2_core_mass_fractions"] = critical
    nine["face_strength_37_over_41_SF"] = nine["optimum"]["sfs"]["face_yield"]*37/41
    nine["crimp_allowable_gap"] = 1/nine["optimum"]["least_SF"]
    nine["limit_other_branch"] = point(face, core, critical[-1]+1e-12, .2, .05)
    # Primary citation contradicts the inherited S200F modulus, independently
    # of the perfectly reproducible arithmetic above.
    check("primary_face_provenance", "Beryllium S-200F.E_Pa", face["E_Pa"], 290e9)
    check("primary_face_provenance", "Beryllium S-200F.rho", face["rho"], 1850)
    corrected = dict(face, E_Pa=290e9)
    sensitivity = {}
    for margin, name in [(0, "014b"), (.05, "009c5")]:
        filed_x = ceiling["core_mass_fraction"] if margin == 0 else P["optimum"]["core_mass_fraction"]
        fixed = point(corrected, core, filed_x, .2, margin)
        def balance_eq(x):
            sf = point(corrected, core, x, .2, margin)["sfs"]
            return sf["core_shear_crimping"] - sf["face_wrinkling"]
        x = brentq(balance_eq, .15, .25, xtol=5e-15)
        sensitivity[name] = dict(
            fixed_geometry=fixed,
            continuous_balance=point(corrected, core, x, .2, margin),
            grid_balance=search(corrected, core, .2, margin))
    for kd in [.2, .1407]:
        scored = [(c["name"], search(corrected, c, kd)) for c in C]
        key, best = max(scored, key=lambda v: v[1]["least_SF"])
        sensitivity["014b_best_core_"+str(kd)] = dict(core_name=key, **best)
    def numeric_leaves(v, path=""):
        if isinstance(v, dict):
            for k, x in v.items():
                yield from numeric_leaves(x, path+"."+k if path else k)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                yield from numeric_leaves(x, path+f"[{i}]")
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            yield path, v
    coverage = {}
    for card, obj in [("014b", O), ("009c5", P)]:
        done = {v["path"] for v in checks[card]}
        leaves = list(numeric_leaves(obj))
        coverage[card] = dict(numeric_leaves=len(leaves),
            checked_leaves=sum(k in done for k, v in leaves),
            exclusions=[dict(path=k, value=v,
                reason="Owner elapsed time is historical instrumentation, not independently observable.")
                for k, v in leaves if k not in done])
    assert coverage["009c5"]["checked_leaves"] == coverage["009c5"]["numeric_leaves"]
    assert coverage["014b"]["exclusions"][0]["path"] == "measurements.elapsed_s"
    assert len(coverage["014b"]["exclusions"]) == 1
    summary = {card: {"checks": len(a), "passed": sum(c["passed"] for c in a),
                     "mismatches": [c for c in a if not c["passed"]]}
               for card, a in checks.items()}
    (ROOT / "CALCULATIONS.json").write_text(json.dumps(dict(
        constants=dict(R_m=R, area_m2=AREA, pressure_Pa=PRESSURE, lift_kg=LIFT,
                       biaxial_factor=BIAXIAL, psi_to_Pa=PSI, pcf_to_kg_m3=PCF),
        source_table_counts=table_counts, numeric_coverage=coverage,
        summary=summary, checks=checks, s200f_290GPa_sensitivity=sensitivity,
        reconstructed_winners=winners, reconstructed_per_core_optima=all_core,
        nine=nine), indent=2)+"\n")
    print(json.dumps(summary, indent=2))
    print("009c5 independent balance", balance, exact_balance["least_SF"])
    print("009c5 Vc2 roots", critical)


if __name__ == "__main__":
    run()
