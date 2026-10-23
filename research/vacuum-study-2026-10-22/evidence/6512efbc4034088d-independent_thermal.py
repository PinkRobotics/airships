"""Spot-check the dry, no-sun, two-skin steady thermal roots, from equations."""
import datetime as dt
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

B = Path(__file__).resolve().parent
SIGMA = 5.670374419e-8
INNER_EPS = .2
REQ = 264.0346773614648
RHO_AIR = 4889.442150186961 / (4*math.pi*10**3/3)
mu, weights = np.polynomial.legendre.leggauss(128)
weights = weights / 2


def thermal(R, tc, eps, ta, depression):
    re = RHO_AIR * 2 * (2*R) / 1.79e-5
    nu = 2 + (.4*re**.5 + .06*re**(2/3)) * .71**.4
    h_forced = nu * .0257 / (2*R)
    conductance = 130 * (16.018463373960138 / 2700) / tc
    radiation_environment = .5*(1+mu)*(ta-depression)**4 + .5*(1-mu)*ta**4
    def local(mean_inner_fourth):
        ti = np.full(len(mu), mean_inner_fourth**.25)
        for _ in range(25):
            to = ti + INNER_EPS*SIGMA*(ti**4-mean_inner_fourth)/conductance
            derivative_to = 1 + 4*INNER_EPS*SIGMA*ti**3/conductance
            delta = np.maximum(np.abs(to-ta), .05)
            hn = 1.32*delta**.25
            h = np.maximum(h_forced, hn)
            dh = np.where((hn > h_forced) & (np.abs(to-ta) > .05), .33*delta**(-.75)*np.sign(to-ta), 0)
            residual = h*(ta-to) + eps*SIGMA*(radiation_environment-to**4) + conductance*(ti-to)
            derivative = (dh*(ta-to)-h)*derivative_to - 4*eps*SIGMA*to**3*derivative_to + conductance*(1-derivative_to)
            increment = residual/derivative
            ti -= increment
            if np.max(np.abs(increment)) < 1e-11:
                break
        to = ti + INNER_EPS*SIGMA*(ti**4-mean_inner_fourth)/conductance
        return ti, to
    mean4 = brentq(lambda j: np.dot(weights, local(j)[0]**4)-j,
                   (ta-depression)**4, ta**4, xtol=.0001)
    ti, to = local(mean4)
    h = np.maximum(h_forced, 1.32*np.maximum(np.abs(to-ta), .05)**.25)
    residual_outer = h*(ta-to) + eps*SIGMA*(radiation_environment-to**4) + conductance*(ti-to)
    residual_inner = conductance*(to-ti) + INNER_EPS*SIGMA*(mean4-ti**4)
    return {"minimum_outer_K": float(to.min()),
            "max_balance_residual_W_m2": float(max(np.max(np.abs(residual_outer)), np.max(np.abs(residual_inner)))),
            "h_forced_W_m2_K": h_forced, "h_min_W_m2_K": float(h.min()),
            "h_max_W_m2_K": float(h.max()), "Re": re}


if __name__ == "__main__":
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    hulls = json.loads((B/"sources/levers058.json").read_text())["hulls"]
    rows = []
    for radius in [10, 30]:
        for hid in ["trim-30", "finish_AlAOC"]:
            row = next(x for x in hulls if x["R_m"] == radius and x["mask"] == 11 and x["id"] == hid)
            root = brentq(lambda ta: thermal(radius, row["tc_m"], row["eps_night"], ta, 24.9)["minimum_outer_K"]-REQ, 264.1, 290, xtol=1e-8)
            diagnostic = thermal(radius, row["tc_m"], row["eps_night"], root, 24.9)
            rows.append({"R_m": radius, "hull": hid, "core_thickness_input_m": row["tc_m"],
                         "epsilon": row["eps_night"], "independent_cold_air_K": root,
                         "owner_cold_air_K": row["cold_threshold_K"]["clear_night"],
                         "difference_K": root-row["cold_threshold_K"]["clear_night"], **diagnostic})
    (B/"checks/058-THERMAL-MIXED-CONVECTION.json").write_text(json.dumps({
        "measured_start": start, "measured_end": dt.datetime.now(dt.timezone.utc).isoformat(),
        "equations": "Outer: h(Ta-To)+eps*sigma(Fsky*Tsky^4+Fground*Ta^4-To^4)+K(Ti-To)=0. Inner: K(To-Ti)+eps_i*sigma(<Ti^4>-Ti^4)=0.",
        "scope": "Inherited dry sphere with mixed forced/natural convection, no installation or wet-optics validation; independently solved, no source code imported.",
        "rows": rows}, indent=2)+"\n")
    print("Four independent cold-edge thermal roots completed.")
