"""Independent radiative/conductive sphere calculation from the written 037/040 model."""
import csv
import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial import legendre as lg
from numpy.polynomial import polynomial as poly

R = Path(__file__).resolve().parent
SIGMA = 5.670374419e-8
TA = 284.9
RHO = 1.1672683307461802
CORE_RHO = 16.018463373960138
GC = 46884349.59354485


def convection(radius):
    diameter = 2 * radius
    reynolds = RHO * 2 * diameter / 1.79e-5
    nu = 2 + (.4 * math.sqrt(reynolds) + .06 * reynolds**(2/3)) * .71**.4
    return nu * .0257 / diameter


def solve_state(radius, thickness, alpha, epsilon, day=True, nodes=128, legacy=False):
    tc = np.atleast_1d(np.asarray(thickness, dtype=float))
    if legacy:
        mu = -1 + (np.arange(37) + .5) * 2 / 37
        weights = np.full(37, 2 / 37)
    else:
        mu, weights = lg.leggauss(nodes)
    wm = weights / 2
    k = 130 * CORE_RHO / (2640 if legacy else 2700)
    conductance = k / tc[:, None]
    h = convection(radius)
    solar = alpha * (970 if day else 0) * np.maximum(mu, 0)
    sky = 275 if day else 260
    radiation = (1 + mu) / 2 * sky**4 + (1 - mu) / 2 * TA**4
    outer = np.full((len(tc), len(mu)), TA)
    inner = outer.copy()
    mean4 = np.full(len(tc), TA**4)
    # Newton elimination of the two local temperatures and the cavity mean.
    for iteration in range(30):
        fo = solar + h*(TA-outer) + epsilon*SIGMA*(radiation-outer**4) + conductance*(inner-outer)
        fi = conductance*(outer-inner) + .2*SIGMA*(mean4[:, None]-inner**4)
        a = -h - 4*epsilon*SIGMA*outer**3 - conductance
        d = -conductance - 4*.2*SIGMA*inner**3
        det = a*d-conductance**2
        inner0 = (conductance*fo-a*fi)/det
        inner_mean = -a*.2*SIGMA/det
        constraint = mean4 - (inner**4) @ wm
        linear = 4*inner**3
        dm = (-constraint+(linear*inner0)@wm)/(1-(linear*inner_mean)@wm)
        di = inner0+inner_mean*dm[:, None]
        do = (-fo-conductance*di)/a
        outer += do
        inner += di
        mean4 += dm
        if max(np.max(np.abs(di)), np.max(np.abs(do))) < 2e-12:
            break
    fo = solar + h*(TA-outer) + epsilon*SIGMA*(radiation-outer**4) + conductance*(inner-outer)
    fi = conductance*(outer-inner) + .2*SIGMA*(mean4[:, None]-inner**4)
    average = (inner+outer)/2
    projected = average if legacy else average-(average@wm)[:, None]
    coef = np.stack([(2*n+1)*(projected*lg.legval(mu, [0]*n+[1]))@wm for n in range(7)], axis=1)
    coef[:, :2] = 0
    # Exact extrema of d²T/dphi², via roots of the derivative polynomial.
    curvatures = []
    for row in coef:
        p = lg.leg2poly(row)
        d1, d2 = poly.polyder(p), poly.polyder(p, 2)
        curv = poly.polysub(poly.polymul([1, 0, -1], d2), poly.polymul([0, 1], d1))
        roots = poly.polyroots(poly.polyder(curv))
        points = [-1., 1.] + [float(z.real) for z in roots if abs(z.imag) < 1e-9 and abs(z.real) <= 1]
        curvatures.append(float(np.max(np.abs(poly.polyval(points, curv)))))
    return dict(
        outer=outer, inner=inner, curvature=np.asarray(curvatures),
        max_residual=float(max(np.abs(fo).max(), np.abs(fi).max())),
        cavity_constraint_relative=float(np.max(np.abs(mean4-(inner**4)@wm)/mean4)),
        iterations=iteration+1,
    )


def thermal(radius, tc, alpha, epsilon, nodes=128, legacy=False):
    day = solve_state(radius, tc, alpha, epsilon, True, nodes, legacy)
    night = solve_state(radius, tc, alpha, epsilon, False, nodes, legacy)
    dg = np.max(np.abs(day["outer"]-day["inner"]), axis=1)
    ng = np.max(np.abs(night["outer"]-night["inner"]), axis=1)
    hi, lo = day["outer"].max(axis=1), night["outer"].min(axis=1)
    return dict(
        tc_m=np.atleast_1d(tc), day_gradient_K=dg, night_gradient_K=ng,
        day_curvature_temperature_K=day["curvature"],
        night_curvature_temperature_K=night["curvature"],
        gradient_K=np.maximum(dg, ng), swing_K=hi-lo, rise_K=hi-TA,
        curvature_temperature_K=np.maximum(day["curvature"], night["curvature"]),
        max_outer_K=hi, min_outer_K=lo,
        energy_residual_W_m2=max(day["max_residual"], night["max_residual"]),
        cavity_constraint_relative=max(day["cavity_constraint_relative"], night["cavity_constraint_relative"]),
    )


def main():
    coatings = json.loads((R/"intake/owner/COATINGS.json").read_text())
    owner = json.loads((R/"intake/owner/THERMAL-SCREEN.json").read_text())
    by_id = {x["id"]: x for x in owner}
    point = next(x for x in json.loads((R/"intake/base040/inputs/028b/PROPERTY-CHECKS.json").read_text())
                 ["full_named_maxima"] if x["route"] == "af015_scarf" and x["material"] == "SR200")["point"]
    tc, tf = point["tc_m"], point["tf_m"]
    rows, results = [], []

    def compare(field, old, new, rtol=2e-6, atol=2e-8):
        rows.append(dict(field=field, owner=old, independent=float(new), delta=float(new-old),
                         agrees=math.isclose(old, new, rel_tol=rtol, abs_tol=atol),
                         rtol=rtol, atol=atol))

    for c in coatings:
        if c["alpha"] is None:
            continue
        modes = {}
        for name, legacy in [("legacy", True), ("common", False)]:
            own = thermal(10, [tc], c["alpha"], c["epsilon"], legacy=legacy)
            modes[name] = {k:(v.tolist() if isinstance(v, np.ndarray) else v) for k, v in own.items()}
            for key, value in own.items():
                if key in by_id[c["id"]][name]:
                    compare(c["id"]+"."+name+"."+key, by_id[c["id"]][name][key][0], value[0])
        mismatch = (23.6e-6-11.3e-6)
        lag = mismatch*math.sqrt(290e9*tf*GC/tc)
        day_sf = 241316.50526089262/(lag*modes["legacy"]["rise_K"][0])
        cycle_sf = 241316.50526089262/(lag*modes["legacy"]["swing_K"][0])
        kb = .5*67e9*CORE_RHO/2700
        cure_delta = max(abs(366.4833333333333-modes["common"]["min_outer_K"][0]),
                         abs(366.4833333333333-modes["common"]["max_outer_K"][0]))
        edge_sf = 172368.93232920903/(1.002*mismatch*cure_delta*math.sqrt(2*kb*GC))
        factors = dict(legacy_037_day_SF=day_sf, legacy_037_full_swing_SF=cycle_sf,
                       current_200F_minimum_edge_SF=edge_sf)
        for key, value in factors.items():
            compare(c["id"]+"."+key, by_id[c["id"]][key], value)
        results.append(dict(id=c["id"], **factors, states=modes))
    with (R/"THERMAL-COMPARISONS.csv").open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    bad = [x for x in rows if not x["agrees"]]
    (R/"THERMAL-RESULTS.json").write_text(json.dumps(dict(
        method="Independent coupled Newton balances, analytic polynomial curvature extrema",
        convection_h_W_m2K=convection(10), results=results, comparisons=len(rows), mismatches=bad
    ), indent=2)+"\n")
    print(json.dumps(dict(comparisons=len(rows), mismatches=len(bad), first_mismatches=bad[:12])))


if __name__ == "__main__":
    main()
