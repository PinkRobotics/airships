#!/usr/bin/env python3
"""MAINLINE-037b: cure residual face-core shear in the P2 Be / CR-III 5056 sandwich, its relief, and the fixes.

Two shear readings, both this seat's arithmetic:
- 037's screen (as filed): the core is a rigid in-plane substrate with aluminium's expansion,
  tau = d_eps E_f t_f lambda, lambda = sqrt(Gc / (E_f t_f t_c)).
- the core-compliance reading: CR-1457's premise that the facings carry the in-plane rigidity. In a continuous core the
  faces set the strain and the interface carries no mismatch shear; at a free core edge (an unbonded splice or a
  closeout) the core's in-plane force N = K_biax d_eps t_c is shed into the faces over a shear lag. Honeycomb resists
  an equal-biaxial strain by stretching its walls, K_biax = E_foil (rho*/rho_s) / 2 (this seat's wall mechanics), and
  resists the in-plane shear part almost not at all, so at the edge the core contracts across the edge while the face
  holds it along the edge. The edge shear is tau = 2 K2 d_eps sqrt(Gc_eff / (K2 + G2)), K2 = K_biax/2, G2 -> 0,
  with Gc_eff the shear stiffness between the core mid-depth and each face.
Plus a replica of 028b's least-set search (gamma and wrinkle usage) to price each fix in gamma and Q.
"""
import math
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

sys.path.insert(0, "unpublished-local-ref:d49761785f6805ea"
                   "vacuum-mainline017b-improvement-directions-1020")
import model17b as m  # noqa: E402

# ---------------------------------------------------------------- 037's lead point and thermal results (read, not retyped)
D037 = ("unpublished-local-ref:6274fe8df66f8d90"
        "vacuum-mainline037-loads-beyond-pressure-1020")
E_BE, ALPHA_BE, NU_SHEET = 290.0e9, 11.3e-6, 0.0752
ALPHA_AL = 23.6e-6
TF37, TC37 = 0.0007996763438767137, 0.022106790073497733
GC_W, SHEAR_W = 46884349.59354485, 241316.50526089262      # CR-III 5056 3/8-1.0, W modulus and W strength (typ)
T_AIR = 284.9


def lam_037(gc, tf, tc, e_f=E_BE, ti=0.0, gi=1.0):
    return math.sqrt(1.0 / (e_f * tf * (tc / gc + ti / gi)))


def tau_037(d_eps, gc=GC_W, tf=TF37, tc=TC37, e_f=E_BE, ti=0.0, gi=1.0):
    """037's screen: face bonded through the core to an in-plane-rigid substrate of the core's expansion."""
    return abs(d_eps) * e_f * tf * lam_037(gc, tf, tc, e_f, ti, gi)


def tau_edge(d_eps, k_biax, gc=GC_W, tc=TC37, ti=0.0, gi=1.0, g2=0.0):
    """Core-compliance reading: shear at a free core edge. Relative slip between core mid-depth and each face has
    compliance (tc/2)/gc + ti/gi per unit area (an interlayer of thickness ti and modulus gi adds in series)."""
    k2 = 0.5 * k_biax
    s = 1.0 / (tc / (2.0 * gc) + ti / gi)                # shear stiffness per area, mid-core to one face (Pa/m)
    lam = math.sqrt(2.0 * s / ((k2 + g2) * tc))           # dN/dx = 2 tau, tau = s u_rel, N = (K2+G2) tc u_rel'
    # far field N = 2 K2 d_eps tc; at the edge N = 0, so u_rel'(0) = -2 K2 d_eps / (K2 + G2)
    u0 = 2.0 * k2 * abs(d_eps) / ((k2 + g2) * lam)
    return s * u0, {"lambda_1_per_m": lam, "transfer_length_m": 1.0 / lam, "core_force_N_per_m": 2.0 * k2 * abs(d_eps) * tc}


def k_biax(e_foil, rho_core, rho_foil):
    """Equal-biaxial in-plane stiffness of a honeycomb: an affine dilation stretches every wall by the same strain, and
    the wall volume fraction is rho*/rho_s, so sigma = E_foil (rho*/rho_s) eps / 2 in each direction (2-D network)."""
    return 0.5 * e_foil * rho_core / rho_foil


def doubled_wall_cell():
    """Expanded honeycomb has its ribbon walls doubled (Hexcel's rho = (8/3)(t/d) rho_foil). On a 120-degree cell the
    stretch-only nodes carry one wall force f in all three walls. The wall elongations sum to f l (1/2 + 2)/(E t) and
    equal 1.5 l (eps_W + eps_L), so f = 0.6 E t (eps_W + eps_L). Single walls then carry 1.2 E d_eps under an equal
    biaxial d_eps (uniform cell: 1.0), and sigma = 1.5 f l / A with rho*/rho_s = 4 t l / A gives
    K_biax = 0.45 E rho*/rho_s (uniform cell: 0.5). Returns (K_biax ratio to the uniform cell, single-wall stress ratio)."""
    f_per_strain_sum = 1.5 / 2.5                     # f / (E t (eps_W + eps_L))
    k_ratio = (1.5 * f_per_strain_sum * 2.0 / 4.0) / 0.5
    wall_ratio = f_per_strain_sum * 2.0
    return k_ratio, wall_ratio


# ---------------------------------------------------------------- 028b replica: the least set {gamma, wrinkle} and its usage
RES019 = 411.2989440716474


def geom_028b(F, q):
    """028b's line: faces + core + max(0.05 S, joining) + 100 + 411.299 = lift; 028's joining with the 30:1 scarf."""
    A = 4.0 * math.pi * 100.0
    L = m.L10
    cap = L - m.SYS - RES019
    F = np.asarray(F, dtype=float)
    lo, hi = np.zeros_like(F), np.full_like(F, cap)
    for _ in range(60):
        S = 0.5 * (lo + hi)
        tf = (1.0 - F) * S / (2.0 * A * q["rho_f"])
        tc = F * S / (A * q["rho_c"]) + q.get("extra_tc", 0.0) * 0.0
        J, _ = m.p2_joining(10.0, tf, tc, q, fixed30=True)
        J = J + q.get("extra_mass", 0.0)                      # interlayer or other added bond mass
        over = S + np.maximum(0.05 * S, J) > cap
        hi = np.where(over, S, hi)
        lo = np.where(over, lo, S)
    S = lo
    tf = (1.0 - F) * S / (2.0 * A * q["rho_f"])
    tc = F * S / (A * q["rho_c"])
    J, parts = m.p2_joining(10.0, tf, tc, q, fixed30=True)
    J = J + q.get("extra_mass", 0.0)
    return S, tf, tc, J


def _point_028b(F, q, sigma_today):
    S, tf, tc, J = geom_028b(np.array([F]), q)
    root = math.sqrt(1.0 - q["nu"] ** 2)
    h = tc + tf
    s0 = q["E"] * h / (10.0 * root)
    ti, gi = q.get("interlayer", (0.0, 1.0))              # one layer on each face, in series with the core in shear
    gc_eff = tc / (tc / q["Gc"] + 2.0 * ti / gi)
    sc = h * h * gc_eff / (2.0 * tf * tc)
    vc = s0 / sc
    kc = np.where(vc < 2.0, 1.0 - vc / 4.0, 1.0 / vc)
    sm = m.P0 * 10.0 / (4.0 * tf)
    # cure residual: the core's in-plane pull K_biax d_eps tc, shared by the two faces as compression. It is
    # self-equilibrated through the wall, so it does not drive global buckling or crimping; it adds to the face-local
    # modes (yield, wrinkling, dimpling) and passes through the face scarf.
    kres, dres = q.get("res", (0.0, 0.0))
    sr = np.where(tf > 0.0, kres * dres * tc / (2.0 * np.where(tf > 0.0, tf, 1.0)), 0.0)   # no wall, no residual
    sl = sm + np.maximum(sr, 0.0)
    gn = float(np.where(vc < 2.0, sm / (kc * s0), 0.0)[0])
    gf = float((0.20 + 0.40 * np.minimum(vc, 2.0))[0])
    qn = float((sl / (m.Q_BIAX * math.sqrt(q["E"] * q["Ec"]) * np.sqrt(tf / tc) * q.get("wrinkle_factor", 1.0)))[0])
    modes = {"face_345": float(sigma_today / sl[0]), "crimp": float(sc[0] / sm[0]), "crush": q["crush"] / (m.P0 / 2.0),
             "dimpling": float(0.5 * 2.0 * q["E"] / (1.0 - q["nu"] ** 2) * (tf[0] / q["cell"]) ** 2 / sl[0]),
             "scarf_screen": float(q["scarf_tau"] * (1.0 + q["scarf_min"] ** 2) / (sl[0] * q["scarf_min"]))}
    ug = math.log(gn / 0.2) / math.log(gf / 0.2) if gn > 0.2 else 0.0
    uq = math.log(qn / 0.33) / math.log(0.82 / 0.33) if qn > 0.33 else 0.0
    return {"F": F, "tf": float(tf[0]), "tc": float(tc[0]), "S": float(S[0]), "J": float(J[0]), "Vc": float(vc[0]),
            "gamma_need": gn, "gamma_full": gf, "Q_need": qn, "u_gamma": ug, "u_Q": uq, "u_raw": max(ug, uq),
            "sigma_res_MPa": float(sr[0]) / 1e6, "others_min": min(modes.values()), "others": modes}


def usage_028b(q, n=4001, sigma_today=345e6):
    """Minimise the larger of the gamma and wrinkle usages over the core-mass fraction, with every other mode at
    SF >= 1 on today's values (face 345 MPa, crimp, crush, dimpling, 028's 10 MPa scarf screen). The optimum often
    sits on that boundary (028b's faces are pinned by the scarf screen), so boundaries are located by bisection."""
    X = np.linspace(math.log(1e-4), math.log(0.95), n)
    pts = [_point_028b(math.exp(x), q, sigma_today) for x in X]
    feas = [p["others_min"] >= 1.0 for p in pts]
    if not any(feas):
        best = min(pts, key=lambda p: -p["others_min"])
        return dict(best, max_usage=float("inf"), feasible=False)
    k = min((i for i in range(n) if feas[i]), key=lambda i: pts[i]["u_raw"])
    cands = [pts[k]]
    for j in (k - 1, k + 1):                       # the feasibility edge next to the best grid point
        if 0 <= j < n and not feas[j]:
            a, b = X[k], X[j]
            for _ in range(80):
                c = 0.5 * (a + b)
                if _point_028b(math.exp(c), q, sigma_today)["others_min"] >= 1.0:
                    a = c
                else:
                    b = c
            cands.append(_point_028b(math.exp(a), q, sigma_today))
    lo, hi = X[max(0, k - 1)], X[min(n - 1, k + 1)]     # interior minimum, if any
    for _ in range(100):
        a, b = lo + (hi - lo) * 0.381966, hi - (hi - lo) * 0.381966
        pa, pb = _point_028b(math.exp(a), q, sigma_today), _point_028b(math.exp(b), q, sigma_today)
        va = pa["u_raw"] if pa["others_min"] >= 1.0 else float("inf")
        vb = pb["u_raw"] if pb["others_min"] >= 1.0 else float("inf")
        if va < vb:
            hi = b
        else:
            lo = a
    pm = _point_028b(math.exp(0.5 * (lo + hi)), q, sigma_today)
    if pm["others_min"] >= 1.0:
        cands.append(pm)
    best = min(cands, key=lambda p: p["u_raw"])
    return dict(best, max_usage=best["u_raw"], feasible=True)


def base_q(core=None, nu=NU_SHEET):
    q = dict(m.P2_TODAY)
    q.update({"nu": nu, "E": 290e9, "sigma": 345e6, "rho_f": 1850.0, "film": 0.07323641454574575})
    if core:
        q.update(core)
    return q
