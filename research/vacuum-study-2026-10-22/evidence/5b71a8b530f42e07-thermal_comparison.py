"""A declared alternative P2 thermal problem, not guessed owner inputs."""
from pathlib import Path
import json
import math
import numpy as np
from numpy.polynomial import legendre
from scipy.optimize import root, brentq

ROOT = Path(__file__).resolve().parent
D = json.loads((ROOT / "INPUTS.json").read_text())
X = D["explicit_check_assumptions"]["thermal_countermodel"]
P = D["P2_028b_selected"]["point"]
U = 130 * P["core"]["rho"] / 2640 / P["tc_m"]
SB, Ta, ei = X["sigma_SB"], X["Tair_K"], X["interior_emissivity"]
results, tests = [], []


def solve_day(absorptance, emissivity, h, n):
    # Split at the solar terminator, where max(mu,0) has a derivative jump.
    g, gw = legendre.leggauss(n // 2)
    mu = np.r_[(g - 1) / 2, (g + 1) / 2]
    weights = np.r_[gw, gw] / 4
    Q = absorptance * X["solar_W_m2"] * np.maximum(mu, 0)
    env4 = .5 * (X["Tsky_day_K"]**4 + X["ground_K"]**4)

    def residual(z):
        To, Ti, B = z[:n], z[n:2*n], z[-1]
        return np.r_[
            Q - h * (To - Ta) - emissivity * SB * (To**4 - env4) - U * (To - Ti),
            U * (To - Ti) - ei * (SB * Ti**4 - B),
            B - np.dot(weights, SB * Ti**4)
        ]

    def jacobian(z):
        To, Ti = z[:n], z[n:2*n]
        J = np.zeros((2*n + 1, 2*n + 1))
        idx = np.arange(n)
        J[idx, idx] = -h - 4 * emissivity * SB * To**3 - U
        J[idx, n + idx] = U
        J[n + idx, idx] = U
        J[n + idx, n + idx] = -U - 4 * ei * SB * Ti**3
        J[n:2*n, -1] = ei
        J[-1, n:2*n] = -weights * 4 * SB * Ti**3
        J[-1, -1] = 1
        return J

    guess = np.r_[np.full(2*n, Ta + 10), SB * (Ta + 10)**4]
    sol = root(residual, guess, jac=jacobian, tol=1e-10)
    err = float(np.max(abs(residual(sol.x))))
    assert err < 1e-7, (sol.message, err)
    To, Ti, B = sol.x[:n], sol.x[n:2*n], sol.x[-1]

    def pole(m):
        def f(t):
            a, b = t
            return [
                absorptance * 970 * max(m, 0) - h * (a - Ta)
                - emissivity * SB * (a**4 - env4) - U * (a - b),
                U * (a - b) - ei * (SB * b**4 - B)
            ]
        answer = root(f, [To[-1 if m > 0 else 0], Ti[-1 if m > 0 else 0]], tol=1e-11)
        assert max(abs(np.array(f(answer.x)))) < 1e-7
        return [float(v) for v in answer.x]

    sun, anti = pole(1), pole(-1)
    night_env4 = .5 * (X["Tsky_night_K"]**4 + X["ground_K"]**4)
    night = brentq(lambda T: h * (T - Ta) + emissivity * SB * (T**4 - night_env4), 200, 350)
    mean_face = (To + Ti) / 2
    coeff = [(2*k + 1) * float(np.dot(weights, mean_face * legendre.Legendre.basis(k)(mu)))
             for k in range(7)]
    average_external_residual = float(np.dot(weights,
        Q - h * (To - Ta) - emissivity * SB * (To**4 - env4)))
    average_interior_radiation = float(np.dot(weights, ei * (SB * Ti**4 - B)))
    return {
        "tag": "PROJECTION; independent specified thermal model",
        "h_W_m2K": h, "quadrature_points": n, "absorptance": absorptance,
        "emissivity": emissivity, "To_subsolar_K": sun[0], "Ti_subsolar_K": sun[1],
        "To_antisolar_K": anti[0], "Ti_antisolar_K": anti[1],
        "night_both_faces_K": night, "day_night_subsolar_swing_K": sun[0] - night,
        "subsolar_gradient_K": sun[0] - sun[1], "legendre_mean_face_K": coeff,
        "mean_face_K": float(np.dot(weights, mean_face)),
        "max_equation_residual_W_m2": err,
        "mean_external_energy_residual_W_m2": average_external_residual,
        "mean_interior_net_radiation_W_m2": average_interior_radiation,
        "profile": {"mu": mu.tolist(), "outer_K": To.tolist(), "inner_K": Ti.tolist()}
    }


for label, a, e in [("coated_outer", .2, .9), ("bare_Be", .4, .05)]:
    for h in X["h_cases_W_m2K"]:
        low, high = solve_day(a, e, h, 64), solve_day(a, e, h, 128)
        high["surface"] = label
        delta = max(abs(high[k] - low[k]) for k in [
            "To_subsolar_K", "Ti_subsolar_K", "To_antisolar_K", "Ti_antisolar_K"])
        tests.append({"name": f"{label} h={h} angular convergence",
                      "max_temperature_change_K": delta, "limit_K": .002,
                      "passed": delta < .002})
        tests.append({"name": f"{label} h={h} whole-sphere energy",
                      "residual_W_m2": high["mean_external_energy_residual_W_m2"],
                      "passed": abs(high["mean_external_energy_residual_W_m2"]) < 1e-7})
        tests.append({"name": f"{label} h={h} closed cavity radiation",
                      "residual_W_m2": high["mean_interior_net_radiation_W_m2"],
                      "passed": abs(high["mean_interior_net_radiation_W_m2"]) < 1e-7})
        results.append(high)

# Quadrature must not manufacture higher harmonics from uniform temperature.
mu, w = legendre.leggauss(128)
for k in range(1, 7):
    c = float((2*k + 1) / 2 * np.dot(w, 300 * legendre.Legendre.basis(k)(mu)))
    tests.append({"name": f"constant-temperature coefficient n={k}",
                  "actual_K": c, "expected_K": 0, "passed": abs(c) < 1e-9})
assert all(t["passed"] for t in tests), [t for t in tests if not t["passed"]]
record = {"assumptions": X, "core_conductance_W_m2K": U, "cases": results,
          "validation": tests}
(ROOT / "THERMAL-COMPARISON.json").write_text(json.dumps(record, indent=2) + "\n")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharex=True)
for ax, (label, title) in zip(axes, [("coated_outer", "Coated Be"), ("bare_Be", "Bare Be")]):
    for item in results:
        if item["surface"] != label:
            continue
        phi = np.degrees(np.arccos(item["profile"]["mu"]))
        ax.plot(phi, item["profile"]["outer_K"], label=f"h = {item['h_W_m2K']:g} W/m²K")
    owner = D["owner_results"]["p2_thermal"][label]
    ax.scatter([0, 180], [owner["T_outer_subsolar_K"], owner["T_outer_antisolar_K"]],
               color="black", marker="x", s=55, label="Filed endpoints")
    ax.axhline(Ta, color="gray", ls=":", lw=1)
    ax.set(title=title, xlabel="Angle from sun (degrees)", ylabel="Outer face temperature (K)",
           xlim=(0, 180))
    ax.grid(alpha=.2)
axes[0].legend(fontsize=8)
fig.suptitle("Independent boundary-condition sensitivity — PROJECTION", fontsize=13)
fig.text(.5, .01, "Equal sky/ground views; closed radiative cavity. Filed heat-transfer inputs are incomplete.",
         ha="center", fontsize=9)
fig.tight_layout(rect=[0, .04, 1, .93])
fig.savefig(ROOT / "thermal-boundary-sensitivity.png", dpi=150)
fig.savefig(ROOT / "thermal-boundary-sensitivity.svg")
print(json.dumps({"cases": len(results), "checks": len(tests),
                  "checks_passed": sum(t["passed"] for t in tests),
                  "max_64_to_128_change_K": max(t.get("max_temperature_change_K", 0) for t in tests)}))
