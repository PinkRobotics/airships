#!/usr/bin/env python3
"""Independent MAINLINE-005 check. Formulas from COMMON.md. Geometry from pinned 002/003 RESULTS. Not the owner's script."""
import hashlib
import json
import math
from pathlib import Path

R = 10.0
KD = 0.2
E = 68.9e9
NU = 0.33
SIG = 276e6
RHO = 2700.0
P = 95460.83791390515  # pinned 002 atmosphere; COMMON prints 95460.8379139
S = 1.0
RO = 0.02
SIG_FILM = 1.5e9
T_FILM = 8e-5

def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-30)

def p1_buckling(t, e=E, kd=KD):
    return kd * 2 * (t / R) ** 2 * e / math.sqrt(3 * (1 - NU ** 2))

def p1_yield(t, sigma=SIG):
    return 2 * sigma * t / R

def p2_buckling(tf, sep, e=E, kd=KD):
    return kd * 4 * tf * sep * e / (R ** 2 * math.sqrt(1 - NU ** 2))

def p2_yield(tf, sigma=SIG):
    return 4 * sigma * tf / R

def p3_euler(inertia, e=E):
    return 2 * math.pi ** 2 * e * inertia / (R * S ** 3)

def p3_yield(area, sigma=SIG):
    return 2 * sigma * area / (R * S)

def film_pressure(sigma_f=SIG_FILM):
    return 2 * sigma_f * T_FILM / S

def load(path):
    return json.loads(Path(path).read_text())

base = Path("unpublished-local-ref:768b7b34f9cac6c4")
card = Path("unpublished-local-ref:0025f202a635b894")
r2 = load(base / "vacuum-mainline002-strength-owner1200-1019/RESULTS.json")
r3 = load(base / "vacuum-mainline003-p2-targets-owner1200-1019/RESULTS.json")
r5 = load(card / "RESULTS.json")
by2 = {row["point_id"]: row for row in r2["rows"]}
by3 = {row["point_id"]: row for row in r3["rows"]}
by5 = {row["point_id"]: row for row in r5["rows"]}

def geometry(pid):
    src = by2[pid] if pid in by2 else by3[pid]
    extra = src.get("extra") or {}
    geom = src["geometry"] if isinstance(src["geometry"], dict) else {}
    if pid.startswith("P1"):
        return {"t": extra["t_m"]}
    if pid.startswith("P2"):
        if "tf_m" in extra:
            return {"tf": extra["tf_m"], "sep": extra["d_m"]}
        return {"tf": geom["tf_m"], "sep": geom["d_m"]}
    return {"tw": extra["tw_m"], "A": extra["area_m2"], "I": extra["I_m4"]}

def derive(pid):
    g = geometry(pid)
    if pid.startswith("P1"):
        t = g["t"]
        pb, py = p1_buckling(t), p1_yield(t)
        e_req = P * math.sqrt(3 * (1 - NU * NU)) / (KD * 2 * (t / R) ** 2)
        s_req = P * R / (2 * t)
        figs = {"E_over_rho2": e_req / RHO ** 2, "sig_over_rho": s_req / RHO}
    elif pid.startswith("P2"):
        tf, sep = g["tf"], g["sep"]
        pb, py = p2_buckling(tf, sep), p2_yield(tf)
        e_req = P * R * R * math.sqrt(1 - NU * NU) / (KD * 4 * tf * sep)
        s_req = P * R / (4 * tf)
        figs = {"E_over_rho": e_req / RHO, "sig_over_rho": s_req / RHO}
    else:
        pb, py = p3_euler(g["I"]), p3_yield(g["A"])
        e_req = P * R * S ** 3 / (2 * math.pi ** 2 * g["I"])
        s_req = P * R * S / (2 * g["A"])
        figs = {"E_over_rho": e_req / RHO, "sig_over_rho": s_req / RHO}
    return {"pb": pb, "py": py, "E": e_req, "sigma": s_req, "xE": e_req / E, "xS": s_req / SIG,
            "sfb": pb / P, "sfy": py / P, "figs": figs, "geom": g}

worst = 0.0
n = 0
order = ["P1", "P1-A", "P2", "P2-A", "P2-C", "P2-K", "P2-E", "P3", "P3-A"]
for pid in order:
    m = derive(pid)
    src = by2[pid] if pid in by2 else by3[pid]
    lim = src["limits_Pa"]
    pb_pin = lim["knocked_down_buckling"] if not pid.startswith("P3") else lim["pinned_euler"]
    c = by5[pid]
    pairs = [
        ("pin_buckling_Pa", m["pb"], pb_pin),
        ("pin_yield_Pa", m["py"], lim["aluminum_yield"]),
        ("buckling_pressure_Pa", m["pb"], c["buckling_pressure_Pa_at_6061_kd0p2"]),
        ("yield_pressure_Pa", m["py"], c["yield_pressure_Pa_at_6061"]),
        ("E_required_Pa", m["E"], c["E_required_Pa"]),
        ("E_x_68p9GPa", m["xE"], c["E_required_x_68p9GPa"]),
        ("sigma_required_Pa", m["sigma"], c["sigma_required_Pa"]),
        ("sigma_x_276MPa", m["xS"], c["sigma_required_x_276MPa"]),
        ("buckling_SF", m["sfb"], c["buckling_SF"]),
        ("yield_SF", m["sfy"], c["yield_SF_QUESTIONABLE"]),
        ("both_E_Pa", m["E"], c["both_modes_at_once"]["E_Pa"]),
        ("both_sigma_Pa", m["sigma"], c["both_modes_at_once"]["sigma_Pa"]),
    ]
    fr, fb = c["figures_required"], c["both_modes_at_once"]["figures"]
    if pid.startswith("P1"):
        pairs += [
            ("E_over_rho2", m["figs"]["E_over_rho2"], fr["E_over_rho2"]),
            ("sig_over_rho", m["figs"]["sig_over_rho"], fr["sig_over_rho"]),
            ("both_E_over_rho2", m["figs"]["E_over_rho2"], fb["E_over_rho2"]),
            ("both_sig_over_rho", m["figs"]["sig_over_rho"], fb["sig_over_rho"]),
            ("6061_E_over_rho2", E / RHO ** 2, c["figures_6061"]["E_over_rho2"]),
            ("6061_sig_over_rho", SIG / RHO, c["figures_6061"]["sig_over_rho"]),
        ]
    elif pid.startswith("P2"):
        pairs += [
            ("E_over_rho", m["figs"]["E_over_rho"], fr["E_over_rho_faces"]),
            ("sig_over_rho", m["figs"]["sig_over_rho"], fr["sig_over_rho_faces"]),
            ("both_E_over_rho", m["figs"]["E_over_rho"], fb["E_over_rho_faces"]),
            ("both_sig_over_rho", m["figs"]["sig_over_rho"], fb["sig_over_rho_faces"]),
            ("6061_E_over_rho", E / RHO, c["figures_6061"]["E_over_rho"]),
            ("6061_sig_over_rho", SIG / RHO, c["figures_6061"]["sig_over_rho"]),
        ]
    else:
        pf, sf, sfilm = film_pressure(), film_pressure() / P, P * S / (2 * T_FILM)
        pairs += [
            ("E_over_rho", m["figs"]["E_over_rho"], fr["E_over_rho_members"]),
            ("sig_over_rho", m["figs"]["sig_over_rho"], fr["sig_over_rho_members"]),
            ("both_E_over_rho", m["figs"]["E_over_rho"], fb["E_over_rho_members"]),
            ("both_sig_over_rho", m["figs"]["sig_over_rho"], fb["sig_over_rho_members"]),
            ("film_pressure_Pa", pf, c["film_pressure_Pa"]),
            ("film_SF", sf, c["film_SF"]),
            ("sigma_film_required_Pa", sfilm, c["sigma_film_required_Pa"]),
            ("6061_E_over_rho", E / RHO, c["figures_6061"]["E_over_rho"]),
            ("6061_sig_over_rho", SIG / RHO, c["figures_6061"]["sig_over_rho"]),
        ]
    for name, mine, card_v in pairs:
        n += 1
        rr = rel(mine, card_v)
        worst = max(worst, rr)
        if rr > 1e-12:
            print(f"MISMATCH {pid} {name} card={card_v!r} mine={mine!r} rel={rr:.3e}")

# Scaling demonstration. P1 and P2 carry kd; P3 Euler does not.
p1 = derive("P1")
e_p1_kd04 = P * math.sqrt(3 * (1 - NU * NU)) / (0.4 * 2 * (0.0007 / R) ** 2)
p3 = derive("P3")
e_p3_kd04 = P * R * S ** 3 / (2 * math.pi ** 2 * geometry("P3")["I"])
print(f"comparisons {n} worst_rel {worst:.3e}")
print(f"P1 E(kd=0.4)/E(kd=0.2) = {e_p1_kd04 / p1['E']:.6f} (1/kd scaling expects 0.5)")
print(f"P3 E(kd=0.4)/E(kd=0.2) = {e_p3_kd04 / p3['E']:.6f} (formula has no kd; card scaling expects 0.5)")
# Sigma independence: membrane requirement ignores the 276 MPa assumption.
s_double = P * R / (2 * 0.0007)
print(f"P1 sigma_req at doubled baseline sigma / original = {s_double / p1['sigma']:.6f}")
# Exact annulus versus the pinned section.
for pid in ("P3", "P3-A"):
    tw = geometry(pid)["tw"]
    ri = RO - tw
    area = math.pi * (RO ** 2 - ri ** 2)
    inertia = math.pi / 4 * (RO ** 4 - ri ** 4)
    print(f"{pid} annulus/pin A rel {rel(area, geometry(pid)['A']):.3e} I rel {rel(inertia, geometry(pid)['I']):.3e} tw/ro {tw / RO:.6f}")
print(f"6061 E/rho2 {E / RHO ** 2:.6f} E/rho {E / RHO:.6f} sig/rho {SIG / RHO:.6f}")
print(f"film SF {film_pressure() / P:.6f} allowable_req {P * S / (2 * T_FILM):.6f}")
