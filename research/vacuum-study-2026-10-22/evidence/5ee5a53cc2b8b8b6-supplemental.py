#!/usr/bin/env python3
"""Additional independent checks, exact active constraints and source sensitivities."""
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq, minimize_scalar
import check021b as c

HERE = Path(__file__).resolve().parent
OWNER = json.loads((HERE / "snapshots/RESULTS.json").read_text())
CALC = json.loads((HERE / "CALCULATIONS.json").read_text())
core = next(x for x in c.CORES if x["name"] == "Hexcel CR-III 5056 3/8-1.0")
out = {}


def exact_least_set():
    """The best three-member set activates compression and equal gamma/panel use."""
    def at(u):
        w = c.W0 * (c.W1 / c.W0)**u
        f = brentq(lambda f: float(c.raw(core, f, w)["stress"]) - 345e6,
                   1e-6, .99, xtol=5e-15)
        d = c.raw(core, f, w)
        return f, w, float(c.usages(d)[0])
    u = brentq(lambda u: at(u)[2] - u, .8, .9, xtol=5e-15)
    f, w, ug = at(u)
    return dict(max_usage=u, point=c.point(core, f, w, .03),
                compression_residual_Pa=float(c.raw(core, f, w)["stress"] - 345e6),
                gamma_panel_usage_residual=ug - u)


def fixed_mass_subsets(structural, strength_today=345e6, n=4000):
    f = np.arange(1, n)[None, :] / n
    d = c.raw(c.CARR, f, structural=structural)
    ug, uw, _ = c.usages(d)
    us = np.maximum(0, np.log(d["stress"] / strength_today) / math.log(379.2e6 / strength_today))
    values = [ug, uw, us]
    rows = []
    for mask in range(8):
        good = (d["crimp"] >= 1 - 1e-12) & (d["crush"] >= 1 - 1e-12) & (d["dimpling"] >= 1 - 1e-12)
        objective = np.zeros_like(d["stress"])
        for k in range(3):
            if mask & (1 << k):
                objective = np.maximum(objective, values[k])
            else:
                good &= values[k] <= 1e-12
        scores = np.where(good, objective, np.inf)
        ci, fi = np.unravel_index(np.argmin(scores), scores.shape)
        value = float(scores[ci, fi])
        rows.append(dict(mask=mask, max_usage=value if math.isfinite(value) else None,
                         core=c.CORES[ci]["name"] if math.isfinite(value) else None,
                         fraction=float(f[0, fi]) if math.isfinite(value) else None))
    return rows


def tolerance(gamma, h, nu=c.NU):
    t = math.sqrt(3) * h
    x = -math.log((gamma - .45) / .51) / 3.88
    amp = x * t
    beta1 = math.sqrt(t / c.R) / (12 * (1 - nu**2))**.25
    return dict(kd=gamma, nu_width=nu, t_eq_mm=t * 1000, R_over_t_eq=c.R / t,
                delta_over_t_eq=x, amplitude_mm=amp * 1000,
                rms_lambda1_mm=amp * 1000 * beta1 / math.sqrt(8),
                rms_worst_mm=amp * 1000 * beta1 * 2.625 / math.sqrt(8),
                width_note="Amplitude is from lambda_I=1; rms_worst changes only width to 2.625 and is not a coupled knockdown/tolerance pair.")


def direct_geometry(tf, tc, E=290e9, sigma=345e6, gamma=None, coefficient=None, nu=c.NU):
    """Independent scalar mode evaluation from actual gauges."""
    if gamma is None:
        gamma = CALC["declared_point"]["needed_values"]["gamma"]
    if coefficient is None:
        coefficient = CALC["declared_point"]["needed_values"]["wrinkle"]
    h = tf + tc
    stress = c.P * c.R / (4 * tf)
    s0 = E * h / (c.R * math.sqrt(1 - nu**2))
    sc = core["Gc_Pa"] * h*h / (2 * tf * tc)
    v = s0 / sc
    kc = 1 - v / 4 if v <= 2 else 1 / v
    return dict(zip(c.MODE_NAMES, [
        gamma * kc * s0 / stress, sigma / stress, sc / stress,
        2 * core["crush_Pa"] / c.P,
        c.BETA * coefficient * math.sqrt(E * core["Ec_Pa"] * tf / tc) / stress,
        E * (tf / core["s_cell_m"])**2 / ((1 - nu**2) * stress)]))


out["exact_continuous_least_set"] = exact_least_set()
out["constant_019_reserve_subsets"] = fixed_mass_subsets((c.LIFT - 100 - 535.9459071525378) / 1.05)
out["rev1_reference_subsets"] = fixed_mass_subsets((.95 * c.LIFT - 100) / 1.05, 283e6)
fp = CALC["declared_point"]
out["tolerance_at_needed"] = tolerance(fp["needed_values"]["gamma"], fp["h_m"])
out["tolerance_at_full_curve"] = tolerance(fp["gamma_full"], fp["h_m"])
out["tolerance_015_convention_needed"] = tolerance(fp["needed_values"]["gamma"], fp["h_m"], nu=.30)
out["tolerance_015_convention_full_curve"] = tolerance(fp["gamma_full"], fp["h_m"], nu=.30)
out["pressure_plus_1pct_at_needed"] = {k: v / 1.01 for k, v in fp["at_needed_values"].items()}
out["uniform_low_gauge_screen"] = direct_geometry(fp["tf_m"] - .0001016, fp["core_m"])
out["compression_at_historical_S200F_283MPa"] = 283e6 / fp["stress_Pa"]
out["nu_00768_same_geometry"] = direct_geometry(fp["tf_m"], fp["core_m"], nu=.0768)
out["nu_00768_needed"] = c.point(core, .1586, fp["panel_width_m"], .03, nu=.0768)
out["nu_00768_continuous_least_set"] = c.continuous_usage(11, nu=.0768)

# Reference 019 optimization is restricted to its two named lead cores.
saved = c.CORES
c.CORES = [x for x in saved if x["name"] in ["Hexcel HRH-10-4.8-32", "Hexcel CR-III 5056 1/4-1.6"]]
out["references_019"] = {}
structural = (c.LIFT - 100 - 535.9459071525378) / 1.05
for fam in ["aluminium", "aramid"]:
    row = c.maximize_minimum(0, structural=structural, group=fam, E_override=303e9, strength_today=283e6)[0]
    chosen = next(x for x in c.CORES if x["name"] == row["core"])
    d = c.raw(chosen, row["fraction"], structural=structural, E=303e9)
    # Joint takeoff evaluated at this frozen geometry; reserve not fed back.
    seam_length = 2 * c.AREA / 4
    seams = seam_length * (2 * .06 * float(d["tf"]) * c.RHO + 2 * .06 * .0002 * 1250
                           + float(d["tc"]) * .0015 * 1100)
    joint_excess = max(0, seams + 2 * c.AREA * .015 * c.FILM_CONV - .05 * structural)
    row.update(tf_m=float(d["tf"]), core_m=float(d["tc"]), joint_excess=joint_excess,
               rebuilt_reserve=c.FIXED + joint_excess)
    out["references_019"][fam] = row
c.CORES = saved

# The current-grade subset table and the alternate full-grade calculation use
# different E. Quantify the effect of explicitly coupling lot E to selecting O3.
out["grid_strength_E2936"] = c.grid_subsets(strength_E=293.6e9)
out["coupled_grade_full_bounds"] = []
for mask in range(32):
    if mask & 4:
        out["coupled_grade_full_bounds"].append(dict(
            mask=mask, best=c.maximize_minimum(mask, strength_E=293.6e9)[0]))

# Check each reported number against independently calculated values. Refined
# family optima are separate; compare the reported grid points at their own f.
checks = []
def compare(field, actual, reported, tolerance=2e-11):
    difference = actual - reported
    checks.append(dict(field=field, check=actual, card=reported, difference=difference,
                       relative_difference=difference / max(1., abs(reported)),
                       pass_=abs(difference) <= tolerance * max(1., abs(reported))))

for k, value in c.FIXED_LINES.items():
    compare("case.reserve_fixed_lines." + k, value, OWNER["case"]["reserve_fixed_lines"][k])
for k in ["tf_m", "core_m", "h_m", "Vc"]:
    compare("floating_point." + k, fp[k], OWNER["floating_point"][k])
for k, value in fp["masses_kg"].items():
    ownerkey = "joint_allowance_0.05S" if k == "joint_allowance_0_05S" else k
    compare("floating_point.masses_kg." + ownerkey, value, OWNER["floating_point"]["masses_kg"][ownerkey])
for block in ["today", "at_needed_values", "at_full_named_set", "at_full_set_conservative_gamma"]:
    for mode, value in fp[block].items():
        compare(f"floating_point.{block}.{mode}", value, OWNER["floating_point"][block]["sfs"][mode])
for block in ["needed_values", "usage"]:
    for k, value in fp[block].items():
        compare(f"floating_point.{block}.{k}", value, OWNER["floating_point"][block][k])
for key, block in [("tolerance_at_needed", "tolerance_015_at_needed_gamma"), ("tolerance_at_full_curve", "tolerance_015_at_018_curve")]:
    for k in ["kd", "t_eq_mm", "R_over_t_eq", "delta_over_t_eq", "amplitude_mm", "rms_worst_mm"]:
        compare(f"floating_point.{block}.{k}", out[key][k], OWNER["floating_point"][block][k])
for key, block in [("tolerance_015_convention_needed", "tolerance_015_at_needed_gamma"),
                   ("tolerance_015_convention_full_curve", "tolerance_015_at_018_curve")]:
    compare(f"{key}.rms_worst_mm", out[key]["rms_worst_mm"], OWNER["floating_point"][block]["rms_worst_mm"])
for row in CALC["grid_32"]:
    owner = next(x for x in OWNER["subsets"] if x["subset"] == row["subset"])
    assert row["feasible_within_named"] == owner["feasible_within_named"]
    if row["best"] is not None:
        compare(f"subsets.mask{row['mask']}", row["best"]["max_usage"], owner["min_max_usage"], tolerance=5e-8)
    else:
        assert owner["min_max_usage"] is None
for group, row in OWNER["families"].items():
    material = next(x for x in c.CORES if x["name"] == row["core"])
    today = group.endswith("_today")
    d = c.raw(material, row["fraction"], c.W0 if today else 4, .03 if today else .015,
              E=290e9 if today else 293.6e9)
    factors = c.modes(d, None if today else d["gamma_full"], .33 if today else .82, 345e6 if today else 379.2e6)
    # The declared grid mass solver leaves residuals around 1e-9 in these
    # factors. Retain the residual explicitly; use the same 5e-8 numerical
    # comparison tolerance as the grid's usage scores.
    compare(f"families.{group}.least", float(min(factors)), row["least"], tolerance=5e-8)
    if not today:
        calculated = c.point(material, row["fraction"], 4, .015)
        filed = row["point"]
        for key in ["tf_m", "core_m", "h_m", "Vc"]:
            compare(f"families.{group}.point.{key}", calculated[key], filed[key], tolerance=5e-8)
        for key, value in calculated["masses_kg"].items():
            ownerkey = "joint_allowance_0.05S" if key == "joint_allowance_0_05S" else key
            compare(f"families.{group}.point.masses_kg.{ownerkey}", value, filed["masses_kg"][ownerkey], tolerance=5e-8)
        for block in ["today", "at_needed_values", "at_full_named_set", "at_full_set_conservative_gamma"]:
            for mode, value in calculated[block].items():
                # Gamma is physically capped at one when the core is on the
                # crimp branch; raising it beyond one cannot cure hard crimp.
                if block == "at_needed_values" and mode == "global_buckling" and calculated["Vc"] >= 2:
                    value = calculated[block]["core_shear_crimping"]
                compare(f"families.{group}.point.{block}.{mode}", value, filed[block]["sfs"][mode], tolerance=5e-8)
    else:
        compare(f"families.{group}.reserve_kg", float(d["reserve"]), row["reserve_kg"], tolerance=5e-8)
for row in out["constant_019_reserve_subsets"]:
    owner = next(x for x in OWNER["reserve_taken_as_given_535_95"]
                 if x["subset"] == [n for k, n in enumerate(c.NAMES[:3]) if row["mask"] & (1 << k)])
    if row["max_usage"] is not None:
        compare(f"reserve_as_given.mask{row['mask']}", row["max_usage"], owner["min_max_usage"])
    else:
        assert owner["min_max_usage"] is None
compare("checks.021_rev1_least_set_usage", out["rev1_reference_subsets"][3]["max_usage"],
        OWNER["checks"]["021_rev1_least_set_usage"]["mine"])
for fam in ["aluminium", "aramid"]:
    compare(f"checks.019_{fam}_least", out["references_019"][fam]["least_SF"],
            OWNER["checks"][f"019_{fam}_least"]["mine"], tolerance=2e-8)
out["comparisons"] = checks
out["comparison_summary"] = dict(n=len(checks), passed=sum(x["pass_"] for x in checks),
                                  failed=[x for x in checks if not x["pass_"]])
(HERE / "SUPPLEMENTAL.json").write_text(json.dumps(c.clean(out), indent=2, allow_nan=False) + "\n")
print(json.dumps(c.clean({k: out[k] for k in ["exact_continuous_least_set", "references_019", "tolerance_at_needed", "comparison_summary"]}), indent=2))
