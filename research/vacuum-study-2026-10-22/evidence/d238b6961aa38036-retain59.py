#!/usr/bin/env python3
"""MAINLINE-059: water a sphere keeps after rain and after dew, by finish and position (this seat's own model).

Drops. A drop of base radius a and contact angle theta is a spherical cap. It stays where gravity along the surface is
below the Furmidge pinning force:
    rho g V(a, theta_m) sin(beta) <= 2 a gamma (cos theta_R - cos theta_A),    theta_m = (theta_A + theta_R) / 2.
That fixes a critical size a_c(beta); smaller drops stay. The retained mass per area is
    m = kappa rho h_eff(a_c),    h_eff = V / (pi rho_p^2),
with rho_p the drop's projected radius. kappa is calibrated so that this seat's Furmidge size on the measured acrylic
plate (78/48 deg, vertical) gives its measured 54 g/m2 (Leonard and Vandewalle 2025): kappa absorbs the real drop-size
distribution and coverage (PROJECTION transfer to other finishes).

Films. On a hydrophilic finish (receding angle at most 15 deg) rain leaves a draining film. Jeffreys' thickness
h = sqrt(mu x / (rho g sin(beta) t)) at distance x = R phi from the top is used when larger than the drop value.

Caps and coverage.
- Near the top every finish is capped at 0.8 kg/m2, the dew a horizontal leaf holds (Ali et al. leaf-chamber data,
  dew.json).
- Rain wets the upper hemisphere and the band down to 135 deg; below that only wind-driven rain reaches (none
  credited, PROJECTION).
- Dew deposits by the local night condensation of dry59's 050 reference and saturated nights. Retention is
  min(deposited, drop capacity); the excess runs off.

Hydrophilic finishes also keep their condensate as a draining Nusselt film where that is thicker than the drops.

Writes RETAIN.json."""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
G, GAMMA, RHO, MU = 9.81, 0.072, 1000.0, 1.0e-3
CAP = 0.80                     # kg/m2: dew held by a horizontal leaf (dew.json, Ali et al.)
ACRYLIC = (78.0, 48.0, 0.054)  # advancing, receding, retained kg/m2 on the vertical plate (retention.json)
FINISHES = {
    "paint_040": {"thA": 40.0, "thR": 15.0, "basis": "white silicate paint: no sourced wettability; hydrophilic oxide assumed (PROJECTION)"},
    "MLCCAg": {"thA": 30.0, "thR": 10.0, "basis": "ITO top layer: static 25 deg sourced on glass; 30/10 hysteresis assumed (PROJECTION)"},
    "hydrophobic_FEP": {"thA": 115.0, "thR": 105.0, "basis": "PTFE advancing 115 deg with 5-15 deg hysteresis; FEP topcoat 105-108 deg (sourced)"},
    "slippery_silicone": {"thA": 107.5, "thR": 102.5, "basis": "silicone slippery coating: CA 105 deg, sliding 5 +- 2 deg (sourced); 5 deg hysteresis assumed"},
    "superhydrophobic": {"thA": 164.0, "thR": 159.0, "basis": "NeverWet on glass/PMMA: advancing 164, receding 159 deg (sourced, secondary)"},
}


def cap_volume(a, th):
    t = math.radians(th)
    return math.pi * a ** 3 * (2 - 3 * math.cos(t) + math.cos(t) ** 3) / (3 * math.sin(t) ** 3)


def h_eff(a, th):
    t = math.radians(th)
    rp = a if th <= 90 else a / math.sin(t)
    return cap_volume(a, th) / (math.pi * rp * rp)


def a_crit(beta, thA, thR):
    """Critical base radius from Furmidge (beta in radians); infinite on a level surface."""
    if beta <= 1e-9:
        return math.inf
    thm = 0.5 * (thA + thR)
    k = cap_volume(1.0, thm)
    dcos = math.cos(math.radians(thR)) - math.cos(math.radians(thA))
    return math.sqrt(2 * GAMMA * dcos / (RHO * G * k * math.sin(beta)))


def kappa():
    thA, thR, m = ACRYLIC
    a = a_crit(math.pi / 2, thA, thR)
    return m / (RHO * h_eff(a, 0.5 * (thA + thR))), a


KAPPA, A_ACRYLIC = kappa()


def drop_capacity(beta, fin):
    f = FINISHES[fin]
    a = a_crit(beta, f["thA"], f["thR"])
    if not math.isfinite(a):
        return CAP
    return min(CAP, KAPPA * RHO * h_eff(a, 0.5 * (f["thA"] + f["thR"])))


def film(beta, x, t):
    if beta <= 1e-9 or t <= 0:
        return CAP
    return min(CAP, RHO * math.sqrt(MU * x / (RHO * G * math.sin(beta) * t)))


def rain_profile(fin, R, t_wait):
    """Retained kg/m2 by polar angle phi (0 = top) after rain and a drainage wait t_wait (s)."""
    f = FINISHES[fin]
    phis = np.radians(np.linspace(0.25, 179.75, 360))
    m = []
    for ph in phis:
        if ph > math.radians(135):
            m.append(0.0)
            continue
        beta = ph if ph <= math.pi / 2 else math.pi - ph       # slope from horizontal; underside faces down
        val = drop_capacity(beta, fin)
        if f["thR"] <= 15 and ph <= math.pi / 2:
            val = max(val, film(beta, R * ph, t_wait))
        m.append(val)
    return phis, np.array(m)


def integrate(phis, m, R):
    dphi = phis[1] - phis[0]
    return float((m * 2 * math.pi * R * R * np.sin(phis) * dphi).sum())


def dew_profile(fin, R, night):
    """Retained dew kg/m2 by polar angle: dry59's 12 h night condensation, capped by the finish's drop capacity."""
    d = json.load(open(os.path.join(HERE, "DRY.json")))
    key = f"R{R}|sphere040|MLCCAg|{night}" if f"R{R}|sphere040|MLCCAg|{night}" in d["results"] else f"R10|sphere040|MLCCAg|{night}"
    by = d["results"][key]["rate_by_polar_deg"]
    pol = np.array([float(k) for k in by])
    dep = np.array([max(0.0, -v) * 12 for v in by.values()])       # kg/m2 over 12 h where condensing
    phis = np.radians(np.linspace(0.25, 179.75, 360))
    deposit = np.interp(np.degrees(phis), pol, dep)
    cap = np.array([drop_capacity(ph if ph <= math.pi / 2 else math.pi - ph, fin) for ph in phis])
    if FINISHES[fin]["thR"] <= 15:
        # hydrophilic: the condensate drains as a Nusselt film, h = (3 mu q x / (rho^2 g sin beta))^(1/3), with q the mean
        # 12 h condensation rate and x = R phi; it stays where it is thicker than the drop capacity (upper hemisphere)
        q = deposit / 43200.0
        nus = np.array([min(CAP, RHO * (3 * MU * qq * R * ph / (RHO ** 2 * G * max(math.sin(ph), 1e-6))) ** (1 / 3))
                        if ph <= math.pi / 2 and qq > 0 else 0.0 for ph, qq in zip(phis, q)])
        cap = np.maximum(cap, nus)
    return phis, deposit, np.minimum(deposit, cap)


def main():
    out = {"basis": __doc__, "kappa": KAPPA, "acrylic_critical_base_radius_m": A_ACRYLIC, "cap_kg_m2": CAP,
           "finishes": FINISHES, "rain": {}, "dew": {}}
    for fin in FINISHES:
        for R in (10, 12, 15, 20, 30):
            area = 4 * math.pi * R * R
            for t_wait in (600, 3600):
                phis, m = rain_profile(fin, R, t_wait)
                tot = integrate(phis, m, R)
                out["rain"][f"{fin}|R{R}|wait{t_wait}s"] = {"total_kg": tot, "mean_kg_m2": tot / area,
                                                            "profile_deg_kg_m2": {f"{math.degrees(p):.2f}": float(v) for p, v in list(zip(phis, m))[::10]}}
            for night in ("night_050_reference", "night_050_saturated"):
                phis, dep, ret = dew_profile(fin, R, night)
                out["dew"][f"{fin}|R{R}|{night}"] = {"deposited_kg": integrate(phis, dep, R), "retained_kg": integrate(phis, ret, R),
                                                     "retained_mean_kg_m2": integrate(phis, ret, R) / area,
                                                     "deposited_mean_kg_m2": integrate(phis, dep, R) / area,
                                                     "profile_deg_kg_m2": {f"{math.degrees(p):.2f}": float(v) for p, v in list(zip(phis, ret))[::10]}}
        r10 = out["rain"][f"{fin}|R10|wait600s"]
        r10h = out["rain"][f"{fin}|R10|wait3600s"]
        d10 = out["dew"][f"{fin}|R10|night_050_reference"]
        d10s = out["dew"][f"{fin}|R10|night_050_saturated"]
        print(f"{fin:18s} R10 rain: {r10['total_kg']:6.1f} kg after 10 min ({r10['mean_kg_m2']:.4f} kg/m2), {r10h['total_kg']:6.1f} kg "
              f"after 1 h | dew kept: reference {d10['retained_kg']:5.1f} of {d10['deposited_kg']:5.1f} kg, saturated "
              f"{d10s['retained_kg']:5.1f} of {d10s['deposited_kg']:5.1f} kg")
    print("kappa", round(KAPPA, 4), "acrylic a_c mm", round(A_ACRYLIC * 1e3, 3))
    for fin in FINISHES:
        f = FINISHES[fin]
        print(f"  {fin:18s} vertical capacity {drop_capacity(math.pi / 2, fin):.4f} kg/m2; at 10 deg {drop_capacity(math.radians(10), fin):.4f}; "
              f"at 2 deg {drop_capacity(math.radians(2), fin):.4f}; a_c(vertical) {a_crit(math.pi / 2, f['thA'], f['thR']) * 1e3:.3f} mm")
    with open(os.path.join(HERE, "RETAIN.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1)
    os.replace(os.path.join(HERE, "RETAIN.json.tmp"), os.path.join(HERE, "RETAIN.json"))


if __name__ == "__main__":
    main()
