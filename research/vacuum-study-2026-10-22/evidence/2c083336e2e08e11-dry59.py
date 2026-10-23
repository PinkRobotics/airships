#!/usr/bin/env python3
"""MAINLINE-059: evaporation and condensation on the hull's outer face (this seat's own energy balance).

Each surface element of the sphere balances absorbed sun, long-wave exchange and convection against latent heat:
    alpha G max(n.s, 0) + eps sigma (T_env^4 - T^4) + h (T_a - T) = L E(T)
- Long-wave environment: 040's thermal model's T_env^4 = 0.5 (1 + mu) T_sky^4 + 0.5 (1 - mu) T_a^4, with mu the
  element's vertical direction cosine.
- Convection: the larger of 040's forced sphere correlation (Whitaker form, generalised to wind U) and its natural term
  1.32 |dT|^0.25.
- Evaporation: E = h_m (rho_v,sat(T) - rho_v,a), with h_m = h / (rho_a c_p Le^(2/3)) by the Chilton-Colburn analogy
  (Le = 0.845, PROJECTION) and saturation from the Magnus form (Alduchov and Eskridge 1996).
- E < 0 is condensation. The inner face is treated as adiabatic (the vacuum side carries little heat; PROJECTION).
- Latent heat 2.45 MJ/kg is FAO-56's value at 20 C.

Conditions are named in CONDITIONS. Writes DRY.json."""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIG = 5.670374419e-8
L_V = 2.45e6               # FAO-56, J/kg
CP, RHO_A, LE = 1005.0, 1.2, 0.845
RV = 461.5
CONDITIONS = {
    "night_050_reference": dict(Ta=284.9, Td=280.0, Tsky=260.0, U=0.2, G=0.0, sun_el=None,
                                note="050's clear reference night: air 284.9 K, dewpoint 280 K, sky 260 K, 0.2 m/s"),
    "night_050_saturated": dict(Ta=284.9, Td=284.9, Tsky=260.0, U=0.2, G=0.0, sun_el=None,
                                note="050's saturated-clear sensitivity"),
    "morning_fair": dict(Ta=288.15, Td=283.15, Tsky=268.0, U=2.0, G=600.0, sun_el=30.0,
                         note="fair morning: 15 C, dewpoint 10 C (RH 72%), 2 m/s, 600 W/m2 direct at 30 deg elevation (PROJECTION)"),
    "midday_fair": dict(Ta=293.15, Td=282.15, Tsky=270.0, U=3.0, G=850.0, sun_el=60.0,
                        note="fair midday: 20 C, dewpoint 9 C (RH 49%), 3 m/s, 850 W/m2 at 60 deg (PROJECTION)"),
    "overcast_day": dict(Ta=285.15, Td=283.65, Tsky=283.15, U=2.0, G=150.0, sun_el=90.0,
                         note="overcast day: 12 C, RH 90%, 2 m/s, 150 W/m2 diffuse treated as overhead (PROJECTION)"),
    "fao_peak_check": dict(Ta=311.15, Td=300.0, Tsky=290.0, U=3.3, G=680.0, sun_el=75.0,
                           note="check against FAO-56's hourly example: 38 C, RH 52%, 3.3 m/s, 2.45 MJ/m2/h (680 W/m2)"),
}
FINISH_OPTICS = {"paint_040": (0.20, 0.90), "MLCCAg": (0.09, 0.80), "CCAg": (0.09, 0.65),
                 "grass_check": (0.77, 0.95)}     # albedo 0.23 (FAO-56's reference surface), for the check only
H_MODELS = ("sphere040", "flatplate")      # 040's sphere correlation; McAdams' wind flat-plate h = 5.7 + 3.8 U (PROJECTION)


def esat(T):
    tc = T - 273.15
    return 610.94 * math.exp(17.625 * tc / (tc + 243.04))


def rho_v(T, e=None):
    return (esat(T) if e is None else e) / (RV * T)


def h_forced(R, U):
    """040's sphere correlation (Whitaker form) with wind U; air properties as 040's thermal.py."""
    re = RHO_A * U * 2 * R / 1.79e-5
    return (2 + (0.4 * math.sqrt(re) + 0.06 * re ** (2 / 3)) * 0.71 ** 0.4) * 0.0257 / (2 * R)


def element_rate(mu, cos_sun, cond, alpha, eps, R, wet=True, hmodel="sphere040"):
    """Evaporation rate (kg/m2/s, + evaporating) and surface temperature for one element."""
    Ta, Tsky, G = cond["Ta"], cond["Tsky"], cond["G"]
    rva = rho_v(Ta, esat(cond["Td"]))
    hf = h_forced(R, cond["U"]) if hmodel == "sphere040" else 5.7 + 3.8 * cond["U"]
    env4 = 0.5 * (1 + mu) * Tsky ** 4 + 0.5 * (1 - mu) * Ta ** 4
    absorbed = alpha * G * max(cos_sun, 0.0)

    def resid(T):
        h = max(hf, 1.32 * max(abs(T - Ta), 0.05) ** 0.25)
        E = h / (RHO_A * CP * LE ** (2 / 3)) * (rho_v(T) - rva) if wet else 0.0
        return absorbed + eps * SIG * (env4 - T ** 4) + h * (Ta - T) - L_V * E, E
    lo, hi = Ta - 40, Ta + 60
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if resid(mid)[0] > 0:
            lo = mid
        else:
            hi = mid
    T = 0.5 * (lo + hi)
    return resid(T)[1], T


def field(cond, alpha, eps, R, n_pol=36, n_az=72, hmodel="sphere040"):
    """Rates over the sphere: polar angle phi from the top (0..pi) and azimuth lam (sun at lam = 0)."""
    phis = (np.arange(n_pol) + 0.5) * math.pi / n_pol
    lams = (np.arange(n_az) + 0.5) * 2 * math.pi / n_az
    el = cond["sun_el"]
    sdir = None if el is None else np.array([math.cos(math.radians(el)), 0.0, math.sin(math.radians(el))])
    E = np.zeros((n_pol, n_az))
    T = np.zeros((n_pol, n_az))
    for i, ph in enumerate(phis):
        for j, la in enumerate(lams):
            n = np.array([math.sin(ph) * math.cos(la), math.sin(ph) * math.sin(la), math.cos(ph)])
            cs = 0.0 if sdir is None else float(n @ sdir)
            E[i, j], T[i, j] = element_rate(math.cos(ph), cs, cond, alpha, eps, R, hmodel=hmodel)
    dA = (np.sin(phis)[:, None] * (math.pi / n_pol) * (2 * math.pi / n_az)) * R * R * np.ones((1, n_az))
    return phis, lams, E, T, dA


def main():
    out = {"basis": __doc__, "conditions": CONDITIONS, "finish_optics": FINISH_OPTICS, "results": {}}
    for R in (10, 30):
      for hm in H_MODELS:
        for fin, (alpha, eps) in FINISH_OPTICS.items():
            for cname, cond in CONDITIONS.items():
                if fin == "grass_check" and cname != "fao_peak_check":
                    continue
                phis, lams, E, T, dA = field(cond, alpha, eps, R, hmodel=hm)
                tot = float((E * dA).sum())
                area = float(dA.sum())
                by_phi = (E * dA).sum(axis=1) / dA.sum(axis=1)
                key = f"R{R}|{hm}|{fin}|{cname}"
                out["results"][key] = {"mean_rate_kg_m2_h": tot / area * 3600, "hull_rate_kg_h": tot * 3600,
                                       "min_rate_kg_m2_h": float(E.min() * 3600), "max_rate_kg_m2_h": float(E.max() * 3600),
                                       "rate_by_polar_deg": {f"{math.degrees(p):.1f}": float(r * 3600) for p, r in zip(phis, by_phi)},
                                       "T_min_K": float(T.min()), "T_max_K": float(T.max())}
                if R == 10 and (fin in ("MLCCAg", "grass_check") or cname == "fao_peak_check"):
                    print(f"{key:40s} mean {tot / area * 3600:+.4f} kg/m2/h  (12 h: {tot / area * 43200:+.3f} kg/m2)  "
                          f"min {E.min() * 3600:+.4f} max {E.max() * 3600:+.4f}  T {T.min():.1f}-{T.max():.1f} K")
    with open(os.path.join(HERE, "DRY.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1)
    os.replace(os.path.join(HERE, "DRY.json.tmp"), os.path.join(HERE, "DRY.json"))


if __name__ == "__main__":
    main()
