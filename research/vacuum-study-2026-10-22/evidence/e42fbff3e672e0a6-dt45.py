#!/usr/bin/env python3
"""MAINLINE-045 models: damage tolerance of the two leads. This seat's own arithmetic.

- map015: 015/015b's knockdown-against-dimple map (Baizhikova 2026 Eq 3, Lee 2016 Eq 23, the Jimenez 2017 plateau
  fit), as 015b states it, with its width convention R beta0 = lambda sqrt(R t_eq) / [12(1-nu^2)]^(1/4).
- face over a damaged zone: a circular face patch that has lost its core under in-plane compression.
- leak: choked and subsonic inflow, ISA, and the descent of a rigid hull that takes air in.
- frame: a rigid-jointed geodesic tube frame (3-D beams) under external pressure, intact and with one member gone.
- tube impact: a thin shell under a local disc load (shallow shell taken as a plate on its own membrane foundation).
"""
import math

import numpy as np
from scipy import integrate, optimize, special

# ---------------------------------------------------------------- 015's map
NU_MAP = 0.33                                   # 015b: the live map carries nu 0.33 only


def teq_sandwich(tf, tc):
    return math.sqrt(3.0) * (tc + tf)           # 015: matches the sandwich radius of gyration to a monocoque


def width_lambda1(R, teq, nu=NU_MAP):
    """R beta0 at lambda = 1: the 1/e radius of a Gaussian dimple, w0 = -delta exp(-(beta/beta0)^2)."""
    return math.sqrt(R * teq) / (12.0 * (1.0 - nu * nu)) ** 0.25


def kd_eq3(x):
    """Baizhikova 2026 Eq 3 at lambda 1 (015b): fitted R/t 100-1550, excludes delta/t below about 0.07."""
    return 0.45 + 0.51 * math.exp(-3.88 * x)


def x_eq3(kd):
    return math.inf if kd <= 0.45 else -math.log((kd - 0.45) / 0.51) / 3.88


def kd_lee(x):
    """Lee et al. 2016 Eq 23 (015b): lower envelope over widths k = 1-5, at R/t 100 and 200; no FEM below 0.15."""
    return 0.068 + 0.25 / (0.28 + x)


def x_lee(kd):
    return 0.25 / (kd - 0.068) - 0.28


def plateau(lam):
    """Jimenez 2017 large-amplitude plateau against width, as 015 filed it: 0.4470 at lambda 1, 0.2338 at 2.625."""
    return (1.0 - 0.036) * (1.0 + lam) ** -1.23 + 0.036


def lam_plateau(kd):
    """The width below which no amplitude takes the plateau down to kd."""
    return ((kd - 0.036) / 0.964) ** (-1.0 / 1.23) - 1.0


def kd_dent(x, lam):
    """A conservative knockdown for one dimple of amplitude x = delta/t_eq and width lam.
    lam <= 1: no worse than the lambda-1 curve (narrower dimples are milder below the worst width, about 2-2.6),
    and no lower than the plateau at that width. 1 < lam <= 5: Lee's envelope, and no lower than the plateau."""
    if lam <= 1.0:
        return max(kd_eq3(x), plateau(lam))
    return max(kd_lee(x), plateau(lam))


def depth_allowed(kd_need, lam, teq):
    """The largest dimple depth (m) of width lam whose knockdown stays at or above kd_need (inf if none limits)."""
    if plateau(lam) >= kd_need:
        return math.inf
    x = x_eq3(kd_need) if lam <= 1.0 else x_lee(kd_need)
    return x * teq


# ---------------------------------------------------------------- a face patch that has lost its core
def ss_root(nu):
    """First root of x J0(x) - (1 - nu) J1(x) = 0: a simply supported circular plate in radial compression."""
    f = lambda x: x * special.j0(x) - (1.0 - nu) * special.j1(x)  # noqa: E731
    return optimize.brentq(f, 1.0, 3.0)


def patch_stress(tf, a, E, nu, edge):
    """Radial-compression buckling stress of a circular face patch of radius a, clamped or simply supported."""
    lam2 = special.jn_zeros(1, 1)[0] ** 2 if edge == "clamped" else ss_root(nu) ** 2
    D = E * tf ** 3 / (12.0 * (1.0 - nu * nu))
    return lam2 * D / (a * a * tf)


def patch_diameter(tf, sigma, E, nu, edge):
    """The patch diameter that buckles at the working stress sigma."""
    lam2 = special.jn_zeros(1, 1)[0] ** 2 if edge == "clamped" else ss_root(nu) ** 2
    return 2.0 * tf * math.sqrt(lam2 * E / (12.0 * (1.0 - nu * nu) * sigma))


# ---------------------------------------------------------------- air, holes and descent
R_AIR, GAMMA, G0 = 287.05287, 1.4, 9.80665


def isa(z):
    T = 288.15 - 0.0065 * z
    p = 101325.0 * (T / 288.15) ** (G0 / (R_AIR * 0.0065))
    return T, p, p / (R_AIR * T)


def mdot_hole(area, cd, p0, T0, p_in):
    """Mass flow into the hull through a hole: choked below the critical ratio, isentropic subsonic above it."""
    pr = max(p_in / p0, 0.0)
    crit = (2.0 / (GAMMA + 1.0)) ** (GAMMA / (GAMMA - 1.0))
    if pr <= crit:
        return cd * area * p0 * math.sqrt(GAMMA / (R_AIR * T0)) * (2.0 / (GAMMA + 1.0)) ** (
            (GAMMA + 1.0) / (2.0 * (GAMMA - 1.0)))
    if pr >= 1.0:
        return 0.0
    return cd * area * p0 * math.sqrt(2.0 * GAMMA / ((GAMMA - 1.0) * R_AIR * T0)
                                      * (pr ** (2.0 / GAMMA) - pr ** ((GAMMA + 1.0) / GAMMA)))


def descent(area, cd_hole, *, R=10.0, wall=0.0, m_hull, z0=500.0, m_free=0.0, cd_drag=0.47, added=0.5,
            t_end=4.0e6, vent=None):
    """A sealed rigid hull, neutral at z0 with m_free kg of air already allowed for, takes air in through a hole.
    It moves vertically under buoyancy, weight and drag (with added mass). The air inside is taken at the ambient
    temperature of the hull's altitude (isothermal fill, the higher-pressure-difference reading).
    vent: optional (area, cd) of a valve that opens to hold p_inside >= p_outside - dp0.
    Returns the history and its extremes: dp / dp0, touchdown speed and times."""
    V_ext = 4.0 / 3.0 * math.pi * R ** 3
    V_in = 4.0 / 3.0 * math.pi * (R - wall) ** 3
    T0, p0, rho0 = isa(z0)
    m_in0 = m_free
    M = rho0 * V_ext - m_in0                                   # everything that is not inside air
    dp0 = p0 - m_in0 * R_AIR * T0 / V_in
    A_ref = math.pi * R * R

    def rhs(t, y):
        z, v, m_in = y
        T, p, rho = isa(max(z, 0.0))
        p_in = m_in * R_AIR * T / V_in
        md = mdot_hole(area, cd_hole, p, T, p_in)
        if vent is not None and p - p_in > dp0:
            md += mdot_hole(vent[0], vent[1], p, T, p_in)
        mass = M + m_in + added * rho * V_ext
        force = (rho * V_ext - M - m_in) * G0 - 0.5 * rho * cd_drag * A_ref * v * abs(v)
        return [v, force / mass, md]

    def ground(t, y):
        return y[0]
    ground.terminal, ground.direction = True, -1
    sol = integrate.solve_ivp(rhs, (0.0, t_end), [z0, 0.0, m_in0], events=ground, max_step=t_end / 2000.0,
                              rtol=1e-8, atol=[1e-6, 1e-9, 1e-9], dense_output=False)
    z, v, m_in = sol.y
    T = 288.15 - 0.0065 * np.maximum(z, 0.0)
    p = 101325.0 * (T / 288.15) ** (G0 / (R_AIR * 0.0065))
    dp = p - m_in * R_AIR * T / V_in
    i = int(np.argmax(dp))
    out = {"dp0_Pa": dp0, "dp_max_ratio": float(dp[i] / dp0), "z_at_dp_max_m": float(z[i]),
           "t_end_s": float(sol.t[-1]), "z_end_m": float(z[-1]), "v_end_m_s": float(v[-1]),
           "m_in_end_kg": float(m_in[-1]), "reached_ground": bool(sol.t_events[0].size), "M_not_air_kg": M}
    t_heavy = None
    for tt, mm in zip(sol.t, m_in):
        if mm - m_in0 > 0.5:
            t_heavy = float(tt)
            break
    out["t_first_half_kg_s"] = t_heavy
    return out


# ---------------------------------------------------------------- the geodesic frame
def geodesic(freq, R):
    """Class-I icosahedral geodesic sphere: nodes on radius R, unique edges."""
    phi = (1.0 + 5 ** 0.5) / 2.0
    v = np.array([[-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0], [0, -1, phi], [0, 1, phi],
                  [0, -1, -phi], [0, 1, -phi], [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]], float)
    f = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6),
         (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10),
         (8, 6, 7), (9, 8, 1)]
    nodes, index, tris = [], {}, []

    def key(p):
        q = p / np.linalg.norm(p)
        return tuple(np.round(q, 9))

    def add(p):
        k = key(p)
        if k not in index:
            index[k] = len(nodes)
            nodes.append(np.array(k) * R)
        return index[k]
    for a, b, c in f:
        A, B, C = v[a], v[b], v[c]
        grid = {}
        for i in range(freq + 1):
            for j in range(freq + 1 - i):
                p = A + (B - A) * i / freq + (C - A) * j / freq
                grid[(i, j)] = add(p)
        for i in range(freq):
            for j in range(freq - i):
                tris.append((grid[(i, j)], grid[(i + 1, j)], grid[(i, j + 1)]))
                if i + j < freq - 1:
                    tris.append((grid[(i + 1, j)], grid[(i + 1, j + 1)], grid[(i, j + 1)]))
    X = np.array(nodes)
    edges = set()
    for a, b, c in tris:
        for e in ((a, b), (b, c), (c, a)):
            edges.add(tuple(sorted(e)))
    return X, sorted(edges), tris


def frame_solve(X, edges, tris, p, A, I, E, nu, removed=(), pinned=False):
    """Linear static 3-D frame (12-DOF Euler-Bernoulli beams, rigid joints) under external pressure lumped to the
    nodes (one third of each triangle's area, along the inward normal). Returns member axial force (+ tension)
    and end moments. 3-2-1 supports; the pressure load is self-equilibrated, so they carry nothing."""
    n = len(X)
    G = E / (2.0 * (1.0 + nu))
    J = 2.0 * I
    keep = [e for k, e in enumerate(edges) if k not in set(removed)]
    ndof = 6 * n
    K = np.zeros((ndof, ndof))
    F = np.zeros(ndof)
    for a, b, c in tris:
        P, Q, S = X[a], X[b], X[c]
        area = 0.5 * np.linalg.norm(np.cross(Q - P, S - P))
        for i in (a, b, c):
            F[6 * i:6 * i + 3] += -p * area / 3.0 * X[i] / np.linalg.norm(X[i])
    Ts = []
    for (i, j) in keep:
        d = X[j] - X[i]
        L = np.linalg.norm(d)
        ex = d / L
        ref = X[i] + X[j]
        ref = ref / np.linalg.norm(ref)                          # local z: outward, near the shell normal
        ez = ref - ex * (ref @ ex)
        ez /= np.linalg.norm(ez)
        ey = np.cross(ez, ex)
        R3 = np.vstack([ex, ey, ez])
        T = np.zeros((12, 12))
        for k in range(4):
            T[3 * k:3 * k + 3, 3 * k:3 * k + 3] = R3
        k = np.zeros((12, 12))
        EA, GJ, EIy, EIz = E * A / L, G * J / L, E * I, E * I
        k[0, 0] = k[6, 6] = EA
        k[0, 6] = k[6, 0] = -EA
        k[3, 3] = k[9, 9] = GJ
        k[3, 9] = k[9, 3] = -GJ
        if not pinned:
            for (v1, t1, v2, t2, EIb, s) in ((1, 5, 7, 11, EIz, 1.0), (2, 4, 8, 10, EIy, -1.0)):
                c1, c2, c3 = 12 * EIb / L ** 3, 6 * EIb / L ** 2, EIb / L
                k[v1, v1] = k[v2, v2] = c1
                k[v1, v2] = k[v2, v1] = -c1
                k[v1, t1] = k[t1, v1] = s * c2
                k[v1, t2] = k[t2, v1] = s * c2
                k[v2, t1] = k[t1, v2] = -s * c2
                k[v2, t2] = k[t2, v2] = -s * c2
                k[t1, t1] = k[t2, t2] = 4 * c3
                k[t1, t2] = k[t2, t1] = 2 * c3
        kg = T.T @ k @ T
        dofs = np.r_[6 * i:6 * i + 6, 6 * j:6 * j + 6]
        K[np.ix_(dofs, dofs)] += kg
        Ts.append((i, j, T, k, dofs, L))
    fixed = [0, 1, 2]
    far = int(np.argmax(np.linalg.norm(X - X[0], axis=1)))
    fixed += [6 * far + 1, 6 * far + 2]
    third = int(np.argmax(np.abs(np.cross(X - X[0], X[far] - X[0]) @ np.array([0, 0, 1.0]))))
    fixed += [6 * third + 2]
    if pinned:
        for i in range(n):
            fixed += [6 * i + 3, 6 * i + 4, 6 * i + 5]
    free = np.setdiff1d(np.arange(ndof), fixed)
    Kff = K[np.ix_(free, free)]
    cond = np.linalg.cond(Kff)
    U = np.zeros(ndof)
    U[free] = np.linalg.solve(Kff, F[free])
    res = []
    for (i, j, T, k, dofs, L) in Ts:
        fl = k @ (T @ U[dofs])
        N = fl[6]                                  # + tension at end j
        M1 = math.hypot(fl[4], fl[5])
        M2 = math.hypot(fl[10], fl[11])
        res.append({"edge": (i, j), "L": L, "N": N, "M": max(M1, M2)})
    return res, cond, U


# ---------------------------------------------------------------- a thin shell under a local disc load
def disc_moment(F, c, E, t, Rs, nu):
    """Centre bending moment per width under a load F spread uniformly over radius c on a thin shell of radius Rs,
    taken as a plate on the membrane foundation k = E t / Rs^2 (the shallow-sphere analogy)."""
    D = E * t ** 3 / (12.0 * (1.0 - nu * nu))
    k = E * t / Rs ** 2
    lchar = (D / k) ** 0.25
    q = F / (math.pi * c * c)
    f = lambda s: special.j1(s * c / lchar) * s ** 2 / (s ** 4 + 1.0)  # noqa: E731  (xi = s / lchar)
    val, _ = integrate.quad(f, 0.0, 200.0, limit=800)
    tail, _ = integrate.quad(f, 200.0, 4000.0, limit=4000)
    # M = D (1+nu)/2 * q c * int J1(xi c) xi^2 / (D xi^4 + k) dxi, with xi = s / l: = (1+nu)/2 q c l * I(s)
    return 0.5 * (1.0 + nu) * q * c * lchar * (val + tail), lchar


# ---------------------------------------------------------------- a dented face on a crushable core, under load
def growth_depth(b, N, D, sigma_c, q0, edge_lam2):
    """Depth above which a dent of radius b keeps crushing the core under the face's membrane force N.
    The face over a paraboloid dent of depth d pushes on the core with q0 + 4 (N - N_cr(b)) d / b^2, where q0 is the
    core's share of the pressure on the undamaged shell (p - 2N/R) and N_cr(b) = lam2 D / b^2 is the patch's own
    buckling force. Crushing resumes when that exceeds the crush strength. Returns inf when N <= N_cr(b)."""
    ncr = edge_lam2 * D / (b * b)
    if N <= ncr:
        return math.inf
    return (sigma_c - q0) * b * b / (4.0 * (N - ncr))


def dent_energy(E_abs, tf, sigma0, sigma_c, footprint=None, R_ind=None, n=400):
    """Dent depth under an absorbed energy E_abs: the face membrane (2 pi sigma0 tf d) plus core crush over
    radius b = a + xi, a the contact radius (a rigid sphere's sqrt(2 R d), or a flattened ice footprint), and
    xi = (tf/2) sqrt(sigma0/sigma_c) the plastic spread of the face. Returns (depth, crushed radius, spread)."""
    xi = 0.5 * tf * math.sqrt(sigma0 / sigma_c)

    def a_of(dd):
        if footprint is not None:
            return footprint
        return math.sqrt(max(2.0 * R_ind * dd - dd * dd, 0.0)) if dd < R_ind else R_ind

    def work(dmax):
        xs = np.linspace(0.0, dmax, n)
        P = sigma_c * math.pi * (np.array([a_of(x) for x in xs]) + xi) ** 2 + 2.0 * math.pi * sigma0 * tf * xs
        return float(np.trapezoid(P, xs))
    lo, hi = 0.0, 0.05
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if work(mid) < E_abs:
            lo = mid
        else:
            hi = mid
    dd = 0.5 * (lo + hi)
    return dd, a_of(dd) + xi, xi


def dent_pressure(q, a, tf, sigma0, sigma_c):
    """Quasi-static dent under a contact pressure q over a footprint of radius a: the depth at which the face
    membrane and the crushing core balance q pi a^2 (zero when the core does not crush)."""
    xi = 0.5 * tf * math.sqrt(sigma0 / sigma_c)
    b = a + xi
    force = q * math.pi * a * a
    crush = sigma_c * math.pi * b * b
    return max(force - crush, 0.0) / (2.0 * math.pi * sigma0 * tf), b
