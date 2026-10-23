#!/usr/bin/env python3
"""MAINLINE-058 P2 account: my own implementation of the equations 048/050 state (atmosphere, dry two-skin thermal
balance, Be / CR-III sandwich screens, complete bill, thin-face bisection and core scan). No owner module is imported or
run. Constants are the 040 INPUTS values (pinned) and the 050 METHOD / model50 equations read as text.
Every material value is QUESTIONABLE; every weather, finish and lever extension is a PROJECTION."""
import math

import numpy as np
from numpy.polynomial.legendre import Legendre, leggauss

# ---- case and atmosphere (COMMON / 040 INPUTS)
P0 = 95460.83791390515            # 500 m ISA pressure, Pa
TREF = 284.9                      # 500 m ISA temperature, K
RHOREF = 1.1672683307461802       # 500 m ISA density, kg/m3
LIFT0 = 4889.442150186961         # R 10 m lift at 500 m ISA, kg
RD, RV, GRAV, LAPSE = 287.053, 461.5, 9.80665, 0.0065
SIGMA = 5.670374419e-8
# ---- Be face (SR-200) and Hexcel CR-III 5056 3/8-1.0 core (040 INPUTS, QUESTIONABLE)
NU = 0.0768
ALPHAF, ALPHAC = 11.3e-6, 23.6e-6
RHOCORE = 16.018463373960138
GC = 46884349.59354485
EC = 103421359.3975254
CRUSH = 241316.50526089262
CELL = 0.009524999999999999
KBIAX = 0.5 * 67e9 * RHOCORE / 2700
COREMIN = 25 * 6894.757293168361      # W minimum strength, 037b
CURE = (200 - 32) * 5 / 9 + 273.15    # 200 F cure, 037b
SCARF = 30.34139731914874
FILM0 = 0.030 * 0.45359237 / 0.3048 ** 2
COATING = 0.0075752 * 1.10            # MLCCAg + 10 % application allowance (048)
PRIMER = 0.010
BETA = next(float(x.real) for x in np.roots([1, 0, 1, -1]) if abs(x.imag) < 1e-12)
KNOT = 0.514444
Q70 = 0.5 * RHOREF * (70 * KNOT) ** 2
QGUST = 0.5 * RHOREF * (35 * KNOT + 35 * 0.3048) ** 2
QWIND = max(Q70, QGUST)
PMIN = P0 * 1.01 + QWIND
# interface screen: night outer-skin minimum at which COREMIN / edge = 1
REQ_COLD = CURE - COREMIN / (1.002 * (ALPHAC - ALPHAF) * math.sqrt(2 * KBIAX * GC))

MU, WG = leggauss(128)
_X = np.cos(np.linspace(0, np.pi, 1441))
_ANG = np.stack([(1 - _X * _X) * Legendre.basis(j).deriv(2)(_X) - _X * Legendre.basis(j).deriv()(_X) for j in range(2, 7)])
_LEG = np.stack([Legendre.basis(j)(MU) for j in range(2, 7)])


def es_water(t):
    """Buck (1996) saturation vapour pressure over water, Pa (050's coefficients, NCAR-verified)."""
    c = np.asarray(t, dtype=float) - 273.15
    return 611.21 * np.exp((18.678 - c / 234.5) * c / (257.14 + c))


def atmosphere(z, offset, anomaly_hpa, rh):
    """050 convention: sea-level surface, T = 288.15 + offset - 0.0065 z, RH given at z (over water), constant e/p column."""
    z, offset, anomaly_hpa, rh = np.broadcast_arrays(*[np.asarray(v, dtype=float) for v in (z, offset, anomaly_hpa, rh)])
    ts = 288.15 + offset
    t = ts - LAPSE * z
    ps = 101325.0 + 100.0 * anomaly_hpa
    e = rh * es_water(t)
    p = ps * (t / ts) ** (GRAV / (RD * LAPSE))
    for _ in range(12):
        p = ps * (t / ts) ** (GRAV * (1 - 0.378 * e / p) / (RD * LAPSE))
    rho = (p - 0.378 * e) / (RD * t)
    return {"T_K": t, "p_Pa": p, "e_Pa": e, "x": e / p, "rho": rho, "load_Pa": np.maximum(1.01 * P0, p) + QWIND}


def column(z, offset, anomaly_hpa, x):
    """Same column with a given vapour mole fraction x = e/p (constant with height): explicit."""
    z, offset, anomaly_hpa, x = np.broadcast_arrays(*[np.asarray(v, dtype=float) for v in (z, offset, anomaly_hpa, x)])
    ts = 288.15 + offset
    t = ts - LAPSE * z
    ps = 101325.0 + 100.0 * anomaly_hpa
    p = ps * (t / ts) ** (GRAV * (1 - 0.378 * x) / (RD * LAPSE))
    rho = p * (1 - 0.378 * x) / (RD * t)
    return {"T_K": t, "p_Pa": p, "e_Pa": x * p, "x": x, "rho": rho, "load_Pa": np.maximum(1.01 * P0, p) + QWIND}


def forced_h(radius, wind):
    re = RHOREF * wind * 2 * radius / 1.79e-5
    return (2 + (0.4 * np.sqrt(re) + 0.06 * re ** (2 / 3)) * 0.71 ** 0.4) * 0.0257 / (2 * radius)


def skin(radius, tc, ta, sky, solar, wind=2.0, alpha=0.09, eps=0.80, heater=None):
    """Steady dry two-skin balance on 128 Gauss-Legendre zones (mu = cos of angle from zenith).
    Outer: eps*sigma*(To^4 - env) + h*(To - Ta) + qi - alpha*S*max(mu,0) - heater = 0, env = (1+mu)/2 sky^4 + (1-mu)/2 Ta^4,
    h = max(forced, 1.32|dT|^.25); core: To = Ti + qi/(us + .8 sigma <Ti>^3), us = 130 rho_c/(2700 tc);
    interior: qi = .2 sigma (Ti^4 - <Ti^4>). Returns outer, inner arrays (ntc, 128)."""
    tc = np.atleast_1d(np.asarray(tc, dtype=float))
    hf = forced_h(radius, wind)
    us = 130 * RHOCORE / 2700 / tc[:, None]
    env = 0.5 * (1 + MU) * sky ** 4 + 0.5 * (1 - MU) * ta ** 4
    sun = alpha * solar * np.maximum(MU, 0)
    extra = 0.0 if heater is None else heater
    inside = np.full((len(tc), len(MU)), float(ta))
    for _ in range(500):
        mean = (inside @ WG / 2)[:, None]
        mean4 = (inside ** 4 @ WG / 2)[:, None]
        conduct = us + 0.8 * SIGMA * mean ** 3
        new = inside.copy()
        for __ in range(20):
            qi = 0.2 * SIGMA * (new ** 4 - mean4)
            dqi = 0.8 * SIGMA * new ** 3
            out = new + qi / conduct
            d = out - ta
            hn = 1.32 * np.maximum(np.abs(d), 0.05) ** 0.25
            h = np.maximum(hf, hn)
            dh = np.where((hn > hf) & (np.abs(d) > 0.05), 0.25 * h, 0.0)
            res = eps * SIGMA * (out ** 4 - env) + h * d + qi - sun - extra
            der = (4 * eps * SIGMA * out ** 3 + h + dh) * (1 + dqi / conduct) + dqi
            step = res / der
            new = new - step
            if np.max(np.abs(step)) < 1e-10:
                break
        err = float(np.max(np.abs(new - inside)))
        inside = new
        if err < 2e-9:
            break
    else:
        raise ArithmeticError("skin balance did not converge")
    mean = (inside @ WG / 2)[:, None]
    mean4 = (inside ** 4 @ WG / 2)[:, None]
    out = inside + 0.2 * SIGMA * (inside ** 4 - mean4) / (us + 0.8 * SIGMA * mean ** 3)
    return out, inside


def curvature(out, inside):
    temp = (out + inside) / 2
    dev = temp - (temp @ WG / 2)[:, None]
    coeff = np.stack([(2 * j + 1) / 2 * ((dev * _LEG[j - 2]) @ WG) for j in range(2, 7)], axis=1)
    return np.max(np.abs(coeff @ _ANG), axis=1)


def thermal(radius, tc, ta, day_depr=9.9, night_depr=24.9, solar=970.0, wind=2.0, alpha=0.09, eps_day=0.80,
            eps_night=None):
    """050's coupled scenario: day sky = Ta - 9.9 K with 970 W/m2 overhead sun, night sky = Ta - 24.9 K, 2 m/s."""
    eps_night = eps_day if eps_night is None else eps_night
    od, idy = skin(radius, tc, ta, ta - day_depr, solar, wind, alpha, eps_day)
    on, ini = skin(radius, tc, ta, ta - night_depr, 0.0, wind, alpha, eps_night)
    return {"tc_m": np.atleast_1d(np.asarray(tc, dtype=float)),
            "gradient_K": np.maximum(np.max(np.abs(od - idy), axis=1), np.max(np.abs(on - ini), axis=1)),
            "curvature_temperature_K": np.maximum(curvature(od, idy), curvature(on, ini)),
            "max_outer_K": np.max(od, axis=1), "min_outer_K": np.min(on, axis=1),
            "min_outer_day_K": np.min(od, axis=1), "max_outer_night_K": np.max(on, axis=1)}


class P2:
    """Complete 048 bill and the nine screens of the 050 account for one radius."""

    def __init__(self, radius):
        self.r = float(radius)
        self.area = 4 * math.pi * self.r ** 2
        self.volume = 4 * math.pi * self.r ** 3 / 3
        self.lift = LIFT0 * (self.r / 10) ** 3
        force = 0.47 * Q70 * math.pi * self.r ** 2
        area = force / CRUSH
        a = math.sqrt(area / math.pi)
        thick = math.sqrt(3 * 1.33 * force * math.log(a / 0.025) / (2 * math.pi * 276e6))
        self.pad_kg = area * thick * 2700

    def evaluate(self, tf, tc, pressure, th, mask=11, usage=1.0):
        keys = ("gradient_K", "curvature_temperature_K", "min_outer_K", "max_outer_K")
        arrs = np.broadcast_arrays(*[np.asarray(v, dtype=float) for v in (tf, tc, pressure)],
                                   *[np.asarray(th[k], dtype=float) for k in keys])
        tf, tc, pressure = arrs[:3]
        th = dict(zip(keys, arrs[3:]))
        eu = usage if mask & 4 else 0.0
        e = 290e9 * (293.6 / 290) ** eu
        strength = 345e6 * (379.2 / 345) ** eu
        q = 0.33 * (0.82 / 0.33) ** (usage if mask & 2 else 0.0)
        film = FILM0 * 0.5 ** (usage if mask & 8 else 0.0)
        h = tf + tc
        sp = pressure * self.r / (4 * tf)
        s0 = e * h / (self.r * math.sqrt(1 - NU ** 2))
        scr = GC * h * h / (2 * tf * tc)
        vc = s0 / scr
        kc = np.where(vc <= 2, 1 - vc / 4, 1 / vc)
        g0 = np.where(vc < 2, 0.2, 1.0)
        gf = 0.2 + 0.4 * np.minimum(vc, 2)
        gamma = g0 * (gf / g0) ** (usage if mask & 1 else 0.0)
        grad = 1.002 * e * ALPHAF * th["gradient_K"] / (2 * (1 - NU))
        bend = 1.002 * e * h * ALPHAF * th["curvature_temperature_K"] / (2 * (1 - NU ** 2) * self.r)
        coldexc = np.maximum(CURE - th["min_outer_K"], 0)
        residual = 1.002 * KBIAX * (ALPHAC - ALPHAF) * coldexc * tc / (2 * tf)
        strain = 1.002 * abs(ALPHAC - ALPHAF) * np.maximum(np.abs(CURE - th["min_outer_K"]), np.abs(CURE - th["max_outer_K"]))
        edge = strain * math.sqrt(2 * KBIAX * GC)
        st = sp + grad + bend
        sd = st + residual
        modes = {"global_buckling": gamma * kc * s0 / sp, "face_compression": strength / sd,
                 "core_shear_crimping": scr / st, "core_crush": np.broadcast_to(2 * CRUSH / pressure, tf.shape),
                 "face_wrinkling": BETA * q * np.sqrt(e * EC * tf / tc) / sd,
                 "intracell_dimpling": e * (tf / CELL) ** 2 / (1 - NU ** 2) / sd,
                 "scarf_average_shear_screen": 10e6 * (SCARF + 1 / SCARF) / sd,
                 "core_cell_wall_yield_screen": np.broadcast_to(227.53e6 / (1.2 * 67e9 * strain), tf.shape),
                 "thermal_core_interface_screen": np.broadcast_to(COREMIN / edge, tf.shape)}
        lap = SCARF * tf
        length = self.area * (1 / (0.6096 - lap) + 1 / (1.8288 - lap))
        mface = 2 * self.area * tf * 1850
        mcore = self.area * tc * RHOCORE
        mfilm = np.full(tf.shape, 2 * self.area * film)
        mscarf = 2 * length * np.hypot(lap, tf) * 0.07
        msplice = length * tc * 0.0005 * 500
        mseal = length * 0.002
        actual = mfilm + mscarf + msplice + mseal
        mprimer = PRIMER * self.area
        mcoat = COATING * self.area
        addedwater = 0.1 * (0.002 * mfilm + 0.001 * mcore + 0.01 * mprimer + 0.01 * mcoat + 0.01 * (mscarf + msplice + mseal))
        bill = {"faces": mface, "core": mcore, "charged_joining": np.maximum(actual, 0.05 * (mface + mcore)),
                "coating": np.full(tf.shape, mcoat), "mooring_pad": np.full(tf.shape, self.pad_kg),
                "gas": np.full(tf.shape, 0.01 * self.lift), "systems": np.full(tf.shape, 100.0),
                "water": np.full(tf.shape, 0.1 * self.area), "contamination": np.full(tf.shape, 5 * (self.r / 10) ** 2),
                "absorbed_water": addedwater, "structural_primer": np.full(tf.shape, mprimer)}
        total = sum(bill.values())
        sf = np.minimum.reduce([np.asarray(v) for v in modes.values()])
        return {"modes": modes, "minimum_SF": sf, "mass_kg": total, "bill_kg": bill, "tf_m": tf, "tc_m": tc,
                "pressure_Pa": pressure}

    def thin_face(self, tc, pressure, th, mask=11, usage=1.0):
        tc, pressure = np.broadcast_arrays(np.asarray(tc, dtype=float), np.asarray(pressure, dtype=float))
        lo = np.full(tc.shape, 1e-7)
        hi = np.full(tc.shape, min(0.0195, 0.008 * self.r / 10))
        for _ in range(47):
            mid = (lo + hi) / 2
            ok = self.evaluate(mid, tc, pressure, th, mask, usage)["minimum_SF"] >= 1
            hi = np.where(ok, mid, hi)
            lo = np.where(ok, lo, mid)
        pt = self.evaluate(hi, tc, pressure, th, mask, usage)
        pt["mass_kg"] = np.where(pt["minimum_SF"] >= 1 - 1e-10, pt["mass_kg"], np.inf)
        return pt

    def optimum(self, pressure, table, mask=11, usage=1.0, grid=640):
        """Global log-core scan over [0.0012, 1.4] R/10 m, then golden refinement of the three best local minima.
        table: thermal dict over a core grid; interpolated in log(tc)."""
        lt = np.log(table["tc_m"])

        def th_at(tc):
            ltc = np.log(tc)
            return {k: np.interp(ltc, lt, table[k]) for k in ("gradient_K", "curvature_temperature_K", "max_outer_K",
                                                             "min_outer_K")}

        def mass(tc):
            return self.thin_face(tc, pressure, th_at(tc), mask, usage)["mass_kg"]

        logs = np.linspace(math.log(0.0012 * self.r / 10), math.log(1.4 * self.r / 10), grid)
        m = mass(np.exp(logs))
        local = np.r_[True, (m[1:-1] <= m[:-2]) & (m[1:-1] <= m[2:]), True] & np.isfinite(m)
        if not local.any():
            return None
        cand = np.argsort(np.where(local, m, np.inf))[:3]
        cand = [c for c in cand if np.isfinite(m[c])]
        golden = (math.sqrt(5) - 1) / 2
        best = None
        for c in cand:
            left, right = logs[max(c - 2, 0)], logs[min(c + 2, grid - 1)]
            a = right - golden * (right - left)
            b = left + golden * (right - left)
            fa, fb = mass(np.exp(np.array([a])))[0], mass(np.exp(np.array([b])))[0]
            for _ in range(32):
                if fa <= fb:
                    right, b, fb = b, a, fa
                    a = right - golden * (right - left)
                    fa = mass(np.exp(np.array([a])))[0]
                else:
                    left, a, fa = a, b, fb
                    b = left + golden * (right - left)
                    fb = mass(np.exp(np.array([b])))[0]
            tc = math.exp((left + right) / 2)
            mm = mass(np.array([tc]))[0]
            if best is None or mm < best[1]:
                best = (tc, mm)
        tc = best[0]
        pt = self.thin_face(np.array([tc]), pressure, th_at(np.array([tc])), mask, usage)
        out = {k: (float(v[0]) if isinstance(v, np.ndarray) else v) for k, v in pt.items() if k not in ("modes", "bill_kg")}
        out["modes"] = {k: float(np.asarray(v)[0]) for k, v in pt["modes"].items()}
        out["bill_kg"] = {k: float(np.asarray(v)[0]) for k, v in pt["bill_kg"].items()}
        out["grid_minimum_kg"] = float(np.min(m))
        out["mask"], out["usage"] = mask, usage
        return out
