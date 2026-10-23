#!/usr/bin/env python3
"""Verify saved witnesses by direct force, moment, stiffness and mass equations.

Does not import the search model or execute any source-seat program.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path

from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
P, R, LIFT, E, RHO = 95460.8379139, 10., 4889.44215019, 410e9, 3100.
checks = []


def close(label, observed, expected, rtol=2e-9, atol=1e-9):
    ok = abs(observed - expected) <= atol + rtol * abs(expected)
    checks.append({"check": label, "observed": observed, "expected": expected,
                   "absolute_error": abs(observed - expected), "passed": ok})


def require(label, truth, observed=None):
    checks.append({"check": label, "observed": observed, "passed": bool(truth)})


def main():
    saved = json.loads((ROOT / "SCAN.json").read_text())
    rows = saved["rows"]
    require("scan complete", saved["complete"])
    expected = {"/".join(x) for x in itertools.product(
        ("cap", "membrane"), ("equilateral", "two_way"), ("5", "019"),
        ("projection", "mylar", "ti_kapton", "cfrp_zylon"), ("overall", "in_band"))}
    require("all 64 distinct combinations", {r["key"] for r in rows} == expected and len(rows) == 64)
    seed = {r["key"]: r for r in json.loads((ROOT / "SEED-SCAN.json").read_text())["rows"]}
    max_mass_error, max_strength_error, gauge_improvements = 0., 0., []
    for row in rows:
        key = row["key"]
        c, m = row["case"], row["mass_kg"]
        s, a, b, lam = row["s_m"], row["r_o_m"], row["r_i_m"], row["target_multiplier"]
        area = math.pi * (a*a - b*b)
        inertia = math.pi / 4 * (a**4 - b**4)
        L = 2 * R * math.asin(s / (2 * R))
        equilateral = c["grid"] == "equilateral"
        N = P * R * s / (2 * math.sqrt(3) if equilateral else 2)
        faces = (4 * math.pi * R*R) / (math.sqrt(3) * s*s / 4 if equilateral else s*s)
        members, nodes = (1.5 * faces, .5 * faces + 2) if equilateral else (2 * faces, faces + 2)
        Y = (2 / math.sqrt(3) if equilateral else 1) * E * area / s
        D = (3 * math.sqrt(3) / 4 if equilateral else 1) * E * inertia / s
        Ne = math.pi**2 * E * inertia / (L*L)
        local_stress = (.099 + .901 * math.exp(-math.sqrt(a / (a-b)) / 16)) * .6 * E * (a-b) / a
        Fc, Ft = row["Fc_assumed_Pa"], row["Ft_projection_Pa"]
        eccentricity = L / 1000

        def stresses(load):
            moment = load * eccentricity / (1 - load / Ne)
            axial, bend = load / area, moment * a / inertia
            return axial + bend, max(0., bend - axial)

        perry_force = brentq(lambda load: stresses(load)[0] / Fc - 1,
                            0., Ne * (1 - 1e-10), xtol=1e-7)
        tensile_force = brentq(lambda load: (stresses(load)[1] - Ft) / 1e9,
                              0., Ne * (1 - 1e-10), xtol=1e-7)
        expected_sf = {"compression": Fc * area / N, "euler": Ne / N,
                       "local": local_stress * area / N, "perry": perry_force / N,
                       "tension": tensile_force / N,
                       "global": .8 * math.sqrt(D * Y) / (R*R * P)}
        rho_f, sigma, directions = {
            "projection": (970., 1.5e9, 1),
            "mylar": (1400., 151684660.449916, 1),
            "ti_kapton": (1420., 231e6 * .5, 1),
            "cfrp_zylon": (1560., 5800e6 * .6, 2),
        }[c["family"]]
        tf = row["film_total_m"]
        expected_sf["film"] = 2 * sigma * (tf / directions) / (P * s)
        for mode, sf in expected_sf.items():
            close(key + "/SF/" + mode, row["SF"][mode], sf)
            max_strength_error = max(max_strength_error, abs(row["SF"][mode] - sf))
        require(key + "/strength constraints", min(expected_sf.values()) >= lam - 3e-9,
                min(expected_sf.values()) - lam)
        close(key + "/area", row["area_m2"], area)
        close(key + "/inertia", row["inertia_m4"], inertia)
        close(key + "/tube mass", m["tube"], RHO * area * members * L)
        close(key + "/film mass", m["film"], 4 * math.pi * R*R * rho_f * tf)
        close(key + "/node mass", m["nodes"], .02 * nodes)
        close(key + "/member count", row["members"], members)
        close(key + "/member force", row["force_at_pressure_1_N"], N)
        close(key + "/member length", row["member_length_m"], L)
        mass_sum = m["tube"] + m["film"] + m["joint"] + m["nodes"] + m["systems"] + m["reserve"] + m["sag_lift_loss"]
        close(key + "/mass balance", mass_sum, LIFT, rtol=0, atol=2e-8)
        max_mass_error = max(max_mass_error, abs(mass_sum - LIFT))
        half = math.pi * (1.125 * inertia / area * R*R)**.25
        close(key + "/030 half-wave", row["half_wave_m"], half)
        if c["band"] == "in_band":
            require(key + "/curved member screen", half >= L * (1 - 3e-9), half / L)
        if c["family"] in ("projection", "mylar"):
            close(key + "/joint percentage", m["joint"], .05 * (m["tube"] + m["film"] + m["nodes"]))
            require(key + "/joint capacity remains unknown", row["SF_least_with_sized_joint"] is None)
        else:
            rho_j, sig_j = (4430., 827e6) if c["family"] == "ti_kapton" else (1550., 1470e6)
            aj, overlap = lam * N / sig_j, lam * N / (2 * math.pi * a * 28.9e6)
            mj = 2 * members * rho_j * aj * overlap
            close(key + "/joint mass from area and overlap", m["joint"], mj)
            close(key + "/joint axial capacity", row["joint"]["axial_SF"], sig_j * aj / N)
            close(key + "/joint adhesive capacity", row["joint"]["bond_SF"], 28.9e6 * 2 * math.pi * a * overlap / N)
            close(key + "/lambda squared mass", m["joint"], row["joint"]["mass_at_multiplier_1_kg"] * lam*lam)
        cmp, ten = stresses(lam * N)
        close(key + "/direct limit compression", row["stresses"]["at_limit"]["max_compression_Pa"], cmp, atol=.05)
        close(key + "/direct limit tension", row["stresses"]["at_limit"]["max_tension_Pa"], ten, atol=.05)
        require(key + "/unclipped annulus", 0 < area < math.pi * a*a)
        require(key + "/film floor", tf >= row["film_floor_m"] - 1e-12)
        require(key + "/bound constraints", .4 <= s <= 8 and .003 <= a <= min(.25, s/3) and lam <= 5)
        delta = lam - seed[key]["target_multiplier"]
        gauge_improvements.append({"key": key, "four_dimensional_minus_seed_SF": delta})
        require(key + "/four variable search preserves seed", delta >= -3e-9, delta)

    index = {r["key"]: r for r in rows}
    for key, row in index.items():
        if row["case"]["band"] == "overall":
            band = index[key.rsplit("/", 1)[0] + "/in_band"]
            require(key + "/overall contains in-band", row["target_multiplier"] + 3e-9 >= band["target_multiplier"])

    # Reproduce 030's source values without running that seat's code.
    for row in json.loads((ROOT / "inputs/030/CONTINUUM.json").read_text()):
        if "buckle_half_wave_m" not in row:
            continue
        ro, ri = row["r_o_m"], row["r_o_m"] - row["wall_m"]
        half = math.pi * (1.125 * (ro*ro + ri*ri) / 4 * R*R)**.25
        close("030/" + row["point"], half, row["buckle_half_wave_m"], rtol=1e-13)

    # Independent linear membrane integral: w = 3*s²/(2*rho) * b1*b2*b3.
    # Uniform triangle mean(b1*b2*b3) = 2!*1!*1!*1!/5! = 1/60.
    mean_barycentric_product = math.factorial(2) / math.factorial(5)
    close("equilateral membrane coefficient", 1.5 * mean_barycentric_product, 1/40, rtol=0, atol=1e-16)
    crown = 1 - math.sqrt(11/12)
    cap_mean = crown*crown * (1 - crown/3) / (1/12)
    close("membrane over cap ratio", (1/40) / cap_mean, 1.1660029709329083, rtol=1e-13)
    for s, expected_loss in ((2., 62.90003892028683), (2.04, 64.15803969869263)):
        close("024 cap loss at " + str(s), LIFT * 3 * s * cap_mean / R, expected_loss)
    # Two distinct series for the square membrane's mean, for sensitivity only.
    one = 1/6 - 32/math.pi**5 * sum(math.tanh(k*math.pi/2)/k**5 for k in range(1, 2000, 2))
    double = 128/math.pi**6 * sum(
        1 / (m*m*n*n*(m*m+n*n)) for m in range(1, 480, 2) for n in range(1, 480, 2))
    close("square membrane two series", double, one, rtol=0, atol=3e-9)

    sensitivity_file = ROOT / "SENSITIVITIES.json"
    sensitivity_count = 0
    if sensitivity_file.exists():
        sensitivities = json.loads(sensitivity_file.read_text())
        require("sensitivity scan complete", sensitivities["complete"])
        for group, alternatives in sensitivities.items():
            if not isinstance(alternatives, list):
                continue
            for alternative in alternatives:
                if "result" not in alternative:
                    continue
                sensitivity_count += 1
                row = alternative["result"]
                c, masses = row["case"], row["mass_kg"]
                key = group + "/" + row["key"] + "/Ft=" + str(c["Ft"])
                ro, ri, L = row["r_o_m"], row["r_i_m"], row["member_length_m"]
                A, I = math.pi * (ro*ro-ri*ri), math.pi/4 * (ro**4-ri**4)
                Ne = math.pi**2 * E * I / (L*L)
                N = row["target_multiplier"] * row["force_at_pressure_1_N"]
                moment = N * L / 1000 / (1 - N / Ne)
                compression, tension = N / A + moment * ro / I, max(0., moment * ro / I - N / A)
                require(key + "/Euler", N < Ne)
                require(key + "/compression", compression <= row["Fc_assumed_Pa"] + .2, compression)
                require(key + "/tensile projection", tension <= c["Ft"] + .2, tension)
                close(key + "/tube mass", RHO*A*row["members"]*L, masses["tube"])
                close(key + "/mass closure", masses["vehicle"] + masses["reserve"] + masses["sag_lift_loss"], LIFT)
                ratio = 1.125 if c["wave_ratio_DY"] is None else c["wave_ratio_DY"]
                half = math.pi * (ratio * I/A * R*R)**.25
                close(key + "/half-wave", half, row["half_wave_m"])
                if c["band"] == "in_band":
                    denominator = row["s_m"] if c["spacing_screen"] else L
                    require(key + "/screen", half/denominator >= 1 - 3e-9, half/denominator)
                if c["square_geometry"] and c["grid"] == "two_way":
                    s = row["s_m"]
                    if c["branch"] == "membrane":
                        mean = one * s
                    else:
                        h = s * (1 - math.sqrt(.75))
                        mean = h*h * (s-h/3) / (s*s/4)
                    close(key + "/square sag", masses["sag_lift_loss"], 3*LIFT*mean/R, rtol=3e-8)
                require(key + "/recorded constraints", row["min_constraint"] >= -3e-9, row["min_constraint"])
        require("112 optimized sensitivity witnesses", sensitivity_count == 112, sensitivity_count)

    # Verify snapshots against original filed metadata and the earlier audit's manifest.
    pins = json.loads((ROOT / "INPUT-PINS.json").read_text())
    old_manifest = json.loads((ROOT / "inputs/check022bc/MANIFEST.json").read_text())
    old_index = {r["path"]: r for r in old_manifest["artifacts"]}
    pin_checks = []
    for pin in pins:
        b = (ROOT / pin["snapshot"]).read_bytes()
        observed = hashlib.sha256(b).hexdigest()
        require("snapshot/" + pin["snapshot"], observed == pin["sha256"] and len(b) == pin["bytes"])
        prior = old_index.get(pin["source_path"])
        if prior:
            require("prior filed pin/" + pin["snapshot"], observed == prior["sha256"] and len(b) == prior["bytes"])
        pin_checks.append({**pin, "observed_sha256": observed, "prior_manifest_checked": prior is not None})

    failures = [r for r in checks if not r["passed"]]
    report = {"status": "PASS" if not failures else "FAIL", "checks": len(checks),
              "failures": failures, "max_mass_closure_error_kg": max_mass_error,
              "max_direct_SF_difference": max_strength_error, "pins": pin_checks,
              "optimized_sensitivity_witnesses_checked": sensitivity_count,
              "gauge_search_comparison": gauge_improvements,
              "square_membrane_mean_coefficient": one, "rows": checks}
    (ROOT / "VERIFICATION.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("rows", "pins", "gauge_search_comparison")}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
