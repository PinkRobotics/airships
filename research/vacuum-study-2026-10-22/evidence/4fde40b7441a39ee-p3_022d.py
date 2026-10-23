#!/usr/bin/env python3
"""022d's equilateral cap-branch P3 point, re-implemented from its METHOD.md (Zylon 0/90 film, CFRP-wrap joints,
5% reserve), to price MAINLINE-045's P3 requirements. This seat's own code; 022d's scripts were not run."""
import math

R, P, LIFT = 10.0, 95460.8379139, 4889.44215019
E_SIC, RHO_SIC, SYSTEMS, NODE_KG = 410e9, 3100.0, 100.0, 0.02
RESERVE_5 = 244.4721075095
FILM_RHO, FILM_SIG = 1560.0, 1740e6          # Zylon 0/90: 1740 MPa acting on total gauge (022d, from 024)
C_CFRP = 5.806797113962e-15                  # kg m / N^2, sized CFRP wrap end, m_end = C (lam N)^2 / r_o
FC = 3.9e9
C_GLOBAL = 4.0 * math.sqrt(1.5)


def point(s, ro, tfilm, lam, reserve=RESERVE_5, extra_mass=0.0, film_sig=FILM_SIG, wall_min=0.0):
    S = 4.0 * math.pi * R * R
    L = 2.0 * R * math.asin(s / (2.0 * R))
    faces = S / (math.sqrt(3.0) * s * s / 4.0)
    members, nodes = 1.5 * faces, 0.5 * faces + 2.0
    N = P * R * s / (2.0 * math.sqrt(3.0))
    rho_c = s
    b = s / (2.0 * math.sqrt(3.0))
    h = rho_c - math.sqrt(rho_c * rho_c - b * b)
    mean = h * h * (rho_c - h / 3.0) / (b * b)
    sag = 3.0 * LIFT * mean / R
    m_film = S * FILM_RHO * tfilm
    m_nodes = NODE_KG * nodes
    m_joint = 2.0 * members * C_CFRP * (lam * N) ** 2 / ro
    avail = LIFT - reserve - sag - SYSTEMS - extra_mass
    m_tube = avail - m_film - m_nodes - m_joint
    A = m_tube / (RHO_SIC * members * L)
    if A <= 0 or A >= math.pi * ro * ro:
        return None
    ri = math.sqrt(ro * ro - A / math.pi)
    t = ro - ri
    if t < wall_min:
        return None
    I = math.pi * (ro ** 4 - ri ** 4) / 4.0
    NE = math.pi ** 2 * E_SIC * I / (L * L)
    gam = 0.099 + 0.901 * math.exp(-math.sqrt(ro / t) / 16.0)
    modes = {"compression": FC * A / N, "euler": NE / N, "local": gam * 0.6 * E_SIC * t / ro * A / N,
             "film": 2.0 * film_sig * tfilm / (P * s), "global": 0.2 * C_GLOBAL * E_SIC * math.sqrt(I * A) / (s * R * R * P)}
    e = L / 1000.0
    qN = lam * N
    if qN < NE:
        Mb = qN * e / (1.0 - qN / NE)
        modes["perry"] = FC / (qN / A + Mb * ro / I) * lam
    half = math.pi * math.sqrt(math.sqrt(9.0 / 8.0) * math.sqrt(I / A) * R)
    return {"s": s, "L": L, "ro": ro, "t": t, "A": A, "I": I, "N": N, "members": members, "nodes": nodes,
            "m_tube": m_tube, "m_film": m_film, "m_joint": m_joint, "m_nodes": m_nodes, "sag": sag,
            "modes": modes, "least": min(modes.values()), "half_over_L": half / L, "gamma_local": gam}


def lam_point(s, ro, tfilm, **kw):
    """The load multiplier at which the least mode equals the multiplier (joint mass depends on it)."""
    lam = 1.0
    for _ in range(60):
        pt = point(s, ro, tfilm, lam, **kw)
        if pt is None:
            return None
        new = min(v for k, v in pt["modes"].items() if k != "perry")
        if abs(new - lam) < 1e-13:
            break
        lam = new
    pt["lam"] = lam
    return pt


def best(screen=True, x0=(3.1707585691074884, 0.27508285638020646 / 2, 0.00010944022237810727), **kw):
    """Maximise the least factor over spacing, tube radius and film gauge, with 022d's half-wave screen."""
    from scipy import optimize

    def neg(x):
        s, ro, tf = x
        if s <= 0.4 or ro <= 0.003 or ro > min(0.25, s / 3.0) or tf <= 12e-6:
            return 10.0
        pt = lam_point(s, ro, tf, **kw)
        if pt is None:
            return 10.0
        pen = 0.0
        if screen and pt["half_over_L"] < 1.0:
            pen = 50.0 * (1.0 - pt["half_over_L"])
        return -pt["lam"] + pen
    starts = [x0, (x0[0] * 0.9, x0[1] * 0.9, x0[2] * 0.9), (x0[0] * 1.1, x0[1] * 1.05, x0[2] * 1.1)]
    wmin = kw.get("wall_min", 0.0)
    if wmin > 0.0:                                  # starts whose tube can carry the minimum wall
        for frac in (0.9, 0.75, 0.6):
            ro = frac * 9.79e-4 / (2.0 * math.pi * wmin)
            s0 = math.pi * math.sqrt(math.sqrt(9.0 / 8.0) * ro / math.sqrt(2.0) * R)
            starts.append((s0, ro, x0[2] * s0 / x0[0]))
    bestx, bestf = None, 1e9
    for st in starts:
        r = optimize.minimize(neg, st, method="Nelder-Mead",
                              options={"xatol": 1e-12, "fatol": 1e-14, "maxiter": 40000, "maxfev": 80000})
        if r.fun < bestf:
            bestx, bestf = r.x, r.fun
    if bestf >= 10.0:
        return None
    pt = lam_point(*bestx, **kw)
    return pt
