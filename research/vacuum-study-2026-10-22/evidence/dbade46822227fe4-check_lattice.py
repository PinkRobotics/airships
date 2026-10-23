#!/usr/bin/env python3
"""Independent arithmetic check of the MAINLINE-026 rigid-joint lattice.

Does not import or execute the owner model. Closed-form mass, line load and
wall screen are ordinary arithmetic. The frequency-6 linear eigenproblem is a
numerical simulation and is the part admitted through simjob.
"""

from __future__ import annotations

import argparse
import json
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import numpy as np
from scipy.sparse import bmat, coo_matrix, csc_matrix
from scipy.sparse.linalg import splu

# Pinned physical inputs. QUESTIONABLE. Not allowables.
R_M = 10.0
P_PA = 95460.8379139
LIFT_KG = 4889.44215019
E_PA = 410.0e9
NU = 0.14
RHO = 3100.0
R_O = 0.12368836237368608
WALL = 0.0008802990936851718
S_REQ = 2.04
FILM_KG = 97.515
NODE_EACH_KG = 0.02
JOINT_FRAC = 0.05
SYSTEMS_KG = 50.0
C_LOCAL = 0.6
SIGMA_TYPICAL_PA = 3.9e9
FREQ = 6

# Owner machine figures, used only after this script's own arithmetic, to name
# differences. They are not inputs to the geometry, stiffness or eigen solve.
CARD = {
    "arc_min_m": 1.6274677754191222,
    "arc_mean_m": 2.0013435607236976,
    "arc_max_m": 2.170540448058861,
    "arc_total_m": 2161.4510455815935,
    "A_m2": 0.0006816960123390163,
    "I_m4": 5.177588818283229e-06,
    "GJ_Nm2": 1862115.2767509858,
    "tube_mass_kg": 4567.702931780806,
    "joints_5pct_kg": 228.3851465890403,
    "node_mass_kg": 7.24,
    "total_mass_kg": 4950.843078369846,
    "payload_kg": -61.40092817984714,
    "width_m": 0.5888972745734183,
    "w_Npm": 56216.62727599055,
    "N_wR_mean_N": 551513.6519823915,
    "old_over_new_share": 1.7320508075688772,
    "discrete_mean_N": 550543.522936495,
    "fan_volume_m3": 4167.275913727444,
    "lambda_m3": 6.472319662311285,
    "lambda_m6": 6.4662751985742855,
    "lambda_m12": 6.465400189710405,
    "lambda_m24": 6.465222443853006,
    "dead_lambda": 6.571963275671537,
    "continuum_card": 6.127639734402722,
    "euler_min": 7.571721534683924,
    "euler_mean": 9.789080392494736,
    "euler_max": 17.17209281550514,
    "euler_011b_two_way": 5.170415097855431,
    "euler_011b_triangular": 8.955421645706814,
    "sigma_axial_Pa": 863586316.6401045,
    "sigma_wall_Pa": 1750799936.9601378,
    "wall_lambda": 2.027359516037556,
    "strength_lambda": 4.516051175027251,
    "sf_global_k02": 1.2255279468805444,
    "nl12": {
        "perfect": 5.107400587927113,
        "joint_offset": 4.950376047460733,
        "crooked": 5.082613207915408,
        "eigenmode": 4.539579837323961,
    },
    "nl6": {
        "perfect": 5.140679594069376,
        "joint_offset": 4.983930742116369,
        "crooked": 5.116337662216148,
        "eigenmode": 4.567958873052904,
    },
}


def scrub(obj):
    if isinstance(obj, dict):
        return {str(k): scrub(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [scrub(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return scrub(obj.tolist())
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, float):
        return obj
    return obj


def base_icosahedron():
    phi = (1.0 + np.sqrt(5.0)) / 2.0
    verts = []
    for axis in range(3):
        for s1 in (-1.0, 1.0):
            for s2 in (-1.0, 1.0):
                p = np.zeros(3)
                p[axis] = s1
                p[(axis + 1) % 3] = s2 * phi
                verts.append(p)
    v = np.asarray(verts, dtype=float)
    n = len(v)
    adj = [[] for _ in range(n)]
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(v[i] - v[j]) < 2.1:
                adj[i].append(j)
                adj[j].append(i)
                edges.add((i, j))
    faces = []
    for i, j in edges:
        for k in adj[i]:
            if k <= j:
                continue
            a, b = (j, k) if j < k else (k, j)
            if (a, b) in edges and (min(i, k), max(i, k)) in edges:
                faces.append((i, j, k))
    out = []
    for i, j, k in faces:
        a, b, c = v[i], v[j], v[k]
        if np.dot(np.cross(b - a, c - a), a + b + c) < 0.0:
            out.append((i, k, j))
        else:
            out.append((i, j, k))
    return v, out


def geodesic(freq, radius):
    base, faces0 = base_icosahedron()
    index = {}
    pts = []

    def add(p):
        u = p / np.linalg.norm(p)
        key = tuple(np.round(u, 12))
        slot = index.get(key)
        if slot is None:
            slot = len(pts)
            index[key] = slot
            pts.append(u)
        return slot

    small = []
    for ia, ib, ic in faces0:
        A, B, C = base[ia], base[ib], base[ic]
        grid = {}
        for i in range(freq + 1):
            for j in range(freq + 1 - i):
                kk = freq - i - j
                grid[(i, j)] = add((i * A + j * B + kk * C) / freq)
        for i in range(freq):
            for j in range(freq - i):
                small.append((grid[(i, j)], grid[(i + 1, j)], grid[(i, j + 1)]))
                if i + j <= freq - 2:
                    small.append(
                        (grid[(i + 1, j)], grid[(i + 1, j + 1)], grid[(i, j + 1)])
                    )
    pts = np.asarray(pts, dtype=float) * radius
    faces = [tuple(t) for t in small]
    flipped = 0
    fixed = []
    for i, j, k in faces:
        a, b, c = pts[i], pts[j], pts[k]
        if np.dot(np.cross(b - a, c - a), a + b + c) < 0.0:
            fixed.append((i, k, j))
            flipped += 1
        else:
            fixed.append((i, j, k))
    return pts, fixed, flipped, len(faces0), len(base)


def volume(pts, faces):
    v = 0.0
    for i, j, k in faces:
        v += float(np.dot(pts[i], np.cross(pts[j], pts[k])))
    return v / 6.0


def grad_volume(pts, faces):
    g = np.zeros_like(pts)
    for i, j, k in faces:
        a, b, c = pts[i], pts[j], pts[k]
        g[i] += np.cross(b, c)
        g[j] += np.cross(c, a)
        g[k] += np.cross(a, b)
    g /= 6.0
    return g


def skew(w):
    x, y, z = w
    return np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]], dtype=float)


def slerp_mids(p, q, segs):
    if segs <= 1:
        return []
    u = p / np.linalg.norm(p)
    v = q / np.linalg.norm(q)
    omega = float(np.arccos(float(np.clip(np.dot(u, v), -1.0, 1.0))))
    sine = np.sin(omega)
    mids = []
    for step in range(1, segs):
        t = step / segs
        if sine < 1e-14:
            w = (1.0 - t) * u + t * v
        else:
            w = (np.sin((1.0 - t) * omega) * u + np.sin(t * omega) * v) / sine
        mids.append(w * R_M)
    return mids


def subdivide(pts, faces, members, segs):
    coords = [np.array(p, dtype=float, copy=True) for p in pts]
    interiors = {}
    for i, j in members:
        ids = []
        for mid in slerp_mids(pts[i], pts[j], segs):
            ids.append(len(coords))
            coords.append(mid)
        interiors[(i, j)] = ids

    def directed(i, j):
        if i < j:
            return interiors[(i, j)]
        return list(reversed(interiors[(j, i)]))

    elements = []
    owner = []
    for m_i, (i, j) in enumerate(members):
        chain = [i] + interiors[(i, j)] + [j]
        for a, b in zip(chain[:-1], chain[1:]):
            elements.append((a, b))
            owner.append(m_i)
    polygons = []
    for i, j, k in faces:
        polygons.append(
            [i] + directed(i, j) + [j] + directed(j, k) + [k] + directed(k, i)
        )
    return np.asarray(coords, dtype=float), elements, owner, polygons


def polygon_grad(coords):
    """Centroid-fan gradient. c = mean(b), V = c · sum(b_i × b_{i+1}) / 6."""
    count = coords.shape[0]
    center = np.mean(coords, axis=0)
    cross_sum = np.zeros(3)
    for a in range(count):
        cross_sum += np.cross(coords[a], coords[(a + 1) % count])
    grad = np.zeros_like(coords)
    inv = 1.0 / count
    for a in range(count):
        prev = coords[(a - 1) % count]
        nxt = coords[(a + 1) % count]
        grad[a] = cross_sum * inv + np.cross(nxt, center) + np.cross(center, prev)
    grad /= 6.0
    vol = float(np.dot(center, cross_sum) / 6.0)
    return grad, vol


def polygon_loads(coords, polygons):
    grad = np.zeros_like(coords)
    vol = 0.0
    for bound in polygons:
        local, piece = polygon_grad(coords[bound])
        vol += piece
        for slot, node in enumerate(bound):
            grad[node] += local[slot]
    return grad, vol


def polygon_hessian(coords, polygons, nd, eps=1e-4):
    rows, cols, vals = [], [], []
    for bound in polygons:
        xy = coords[list(bound)]
        count = len(bound)
        for b in range(count):
            for axis in range(3):
                plus = xy.copy()
                minus = xy.copy()
                plus[b, axis] += eps
                minus[b, axis] -= eps
                gp, _ = polygon_grad(plus)
                gm, _ = polygon_grad(minus)
                deriv = (gp - gm) / (2.0 * eps)
                col = bound[b] * 6 + axis
                for a in range(count):
                    for ax2 in range(3):
                        val = float(deriv[a, ax2])
                        if val != 0.0:
                            rows.append(bound[a] * 6 + ax2)
                            cols.append(col)
                            vals.append(val)
    raw = coo_matrix((vals, (rows, cols)), shape=(nd, nd)).tocsc()
    anti = raw - raw.T
    anti_max = float(np.max(np.abs(anti.data))) if anti.nnz else 0.0
    sym = 0.5 * (raw + raw.T)
    return sym.tocsc(), anti_max


def edges_of(faces):
    count = {}
    for i, j, k in faces:
        for a, b in ((i, j), (j, k), (k, i)):
            key = (a, b) if a < b else (b, a)
            count[key] = count.get(key, 0) + 1
    return count


def section():
    ri = R_O - WALL
    area = np.pi * (R_O * R_O - ri * ri)
    inertia = 0.25 * np.pi * (R_O**4 - ri**4)
    gmod = E_PA / (2.0 * (1.0 + NU))
    polar = 2.0 * inertia
    return {
        "r_i_m": ri,
        "A_m2": area,
        "I_m4": inertia,
        "J_m4": polar,
        "G_Pa": gmod,
        "EA": E_PA * area,
        "EI": E_PA * inertia,
        "GJ": gmod * polar,
    }


def beam_ke(ea, ei, gj, length):
    k = np.zeros((12, 12))
    ax = ea / length
    k[0, 0] = ax
    k[0, 6] = -ax
    k[6, 0] = -ax
    k[6, 6] = ax
    tor = gj / length
    k[3, 3] = tor
    k[3, 9] = -tor
    k[9, 3] = -tor
    k[9, 9] = tor
    a = 12.0 * ei / length**3
    b = 6.0 * ei / length**2
    c = 4.0 * ei / length
    d = 2.0 * ei / length
    # v, theta_z with theta_z = dv/dx
    iv = [1, 5, 7, 11]
    kb = np.array(
        [[a, b, -a, b], [b, c, -b, d], [-a, -b, a, -b], [b, d, -b, c]],
        dtype=float,
    )
    for ii in range(4):
        for jj in range(4):
            k[iv[ii], iv[jj]] = kb[ii, jj]
    # w, theta_y with theta_y = -dw/dx
    iw = [2, 4, 8, 10]
    kb = np.array(
        [[a, -b, -a, -b], [-b, c, b, d], [-a, b, a, b], [-b, d, b, c]],
        dtype=float,
    )
    for ii in range(4):
        for jj in range(4):
            k[iw[ii], iw[jj]] = kb[ii, jj]
    return k


def beam_kg(compression, length):
    """Initial-stress G for compression positive. Card Hermite matrix."""
    g = np.zeros((12, 12))
    s = compression / (30.0 * length)
    ll = length
    ll2 = length * length
    iv = [1, 5, 7, 11]
    mv = np.array(
        [
            [36.0, 3.0 * ll, -36.0, 3.0 * ll],
            [3.0 * ll, 4.0 * ll2, -3.0 * ll, -ll2],
            [-36.0, -3.0 * ll, 36.0, -3.0 * ll],
            [3.0 * ll, -ll2, -3.0 * ll, 4.0 * ll2],
        ],
        dtype=float,
    )
    for ii in range(4):
        for jj in range(4):
            g[iv[ii], iv[jj]] = s * mv[ii, jj]
    iw = [2, 4, 8, 10]
    mw = np.array(
        [
            [36.0, -3.0 * ll, -36.0, -3.0 * ll],
            [-3.0 * ll, 4.0 * ll2, 3.0 * ll, -ll2],
            [-36.0, 3.0 * ll, 36.0, 3.0 * ll],
            [-3.0 * ll, -ll2, 3.0 * ll, 4.0 * ll2],
        ],
        dtype=float,
    )
    for ii in range(4):
        for jj in range(4):
            g[iw[ii], iw[jj]] = s * mw[ii, jj]
    return g


def frame_of(pi, pj):
    diff = pj - pi
    length = float(np.linalg.norm(diff))
    ex = diff / length
    tmp = np.array([0.0, 0.0, 1.0]) if abs(ex[2]) < 0.9 else np.array([0.0, 1.0, 0.0])
    ey = np.cross(tmp, ex)
    ey = ey / np.linalg.norm(ey)
    ez = np.cross(ex, ey)
    rot = np.column_stack((ex, ey, ez))
    return rot, length


def to_global(local, rot):
    trans = np.zeros((12, 12))
    rt = rot.T
    for block in range(4):
        trans[block * 3 : (block + 1) * 3, block * 3 : (block + 1) * 3] = rt
    return trans.T @ local @ trans, trans


def pin_pin_factor(sec, n_elem):
    """Lowest pin-pin factor P L^2 / EI. One element of this G is 12."""
    length = 2.0
    ei = sec["EI"]
    n_nodes = n_elem + 1
    nd = n_nodes * 6
    ke_rows = []
    kg_rows = []
    step = length / n_elem
    for e in range(n_elem):
        i0 = e
        i1 = e + 1
        pi = np.array([i0 * step, 0.0, 0.0])
        pj = np.array([i1 * step, 0.0, 0.0])
        rot, le = frame_of(pi, pj)
        ke, trans = to_global(beam_ke(sec["EA"], ei, sec["GJ"], le), rot)
        kg, _ = to_global(beam_kg(1.0, le), rot)
        dofs = [i0 * 6 + a for a in range(6)] + [i1 * 6 + a for a in range(6)]
        ke_rows.append((ke, trans, dofs, le))
        kg_rows.append((kg, dofs))
    k = np.zeros((nd, nd))
    g = np.zeros((nd, nd))
    for ke, _, dofs, _le in ke_rows:
        for a in range(12):
            for b in range(12):
                k[dofs[a], dofs[b]] += ke[a, b]
    for kg, dofs in kg_rows:
        for a in range(12):
            for b in range(12):
                g[dofs[a], dofs[b]] += kg[a, b]
    # Fix translations, torsion and theta_y. Leave v and theta_z free,
    # except v at the two pins.
    fixed = set()
    for n in range(n_nodes):
        fixed.update({n * 6 + 0, n * 6 + 2, n * 6 + 3, n * 6 + 4})
    fixed.add(0)
    fixed.add(1)  # v at start, already; node 0 v is dof 1
    fixed.add((n_nodes - 1) * 6 + 1)
    # node 0 dof 1 was added; the line fixed.add(0) fixed axial. Good.
    free = [i for i in range(nd) if i not in fixed]
    kk = k[np.ix_(free, free)]
    gg = g[np.ix_(free, free)]
    ev = np.linalg.eigvals(np.linalg.solve(gg, kk))
    ev = sorted(float(x.real) for x in ev if abs(x.imag) < 1e-8 and x.real > 0.0)
    factor = ev[0] * length * length / ei
    return factor, ev[0]


def rotated_pin_factor(sec):
    length = np.sqrt(3.0)
    pi = np.zeros(3)
    pj = np.array([1.0, 1.0, 1.0])
    rot, le = frame_of(pi, pj)
    ke, trans = to_global(beam_ke(sec["EA"], sec["EI"], sec["GJ"], le), rot)
    kg, _ = to_global(beam_kg(1.0, le), rot)
    # Fix all translations and torsion. Both bending planes remain.
    fixed = {0, 1, 2, 3, 6, 7, 8, 9}
    free = [i for i in range(12) if i not in fixed]
    kk = ke[np.ix_(free, free)]
    gg = kg[np.ix_(free, free)]
    ev = np.linalg.eigvals(np.linalg.solve(gg, kk))
    ev = sorted(float(x.real) for x in ev if abs(x.imag) < 1e-8 and x.real > 0.0)
    return ev[0] * le * le / sec["EI"]


def rigid_basis(pts):
    n = len(pts)
    basis = np.zeros((n * 6, 6))
    for i, x in enumerate(pts):
        b = 6 * i
        basis[b : b + 3, 0:3] = np.eye(3)
        xx, yy, zz = (float(x[0]), float(x[1]), float(x[2]))
        basis[b + 1, 3] = -zz
        basis[b + 2, 3] = yy
        basis[b + 3, 3] = 1.0
        basis[b + 0, 4] = zz
        basis[b + 2, 4] = -xx
        basis[b + 4, 4] = 1.0
        basis[b + 0, 5] = -yy
        basis[b + 1, 5] = xx
        basis[b + 5, 5] = 1.0
    q, _ = np.linalg.qr(basis, mode="reduced")
    return basis, q


def assemble(pts, members, sec):
    n = len(pts)
    nd = n * 6
    kr, kc, kv = [], [], []
    cache = []
    for i, j in members:
        rot, le = frame_of(pts[i], pts[j])
        ke, trans = to_global(beam_ke(sec["EA"], sec["EI"], sec["GJ"], le), rot)
        dofs = [i * 6 + a for a in range(6)] + [j * 6 + a for a in range(6)]
        for a in range(12):
            for b in range(12):
                val = ke[a, b]
                if val != 0.0:
                    kr.append(dofs[a])
                    kc.append(dofs[b])
                    kv.append(val)
        cache.append((i, j, rot, le, trans, dofs))
    k = coo_matrix((kv, (kr, kc)), shape=(nd, nd)).tocsc()
    return k, cache


def assemble_hessian(pts, faces, nd):
    hr, hc, hv = [], [], []
    blocks = (
        (0, 1, lambda a, b, c: -skew(c) / 6.0),
        (0, 2, lambda a, b, c: skew(b) / 6.0),
        (1, 0, lambda a, b, c: skew(c) / 6.0),
        (1, 2, lambda a, b, c: -skew(a) / 6.0),
        (2, 0, lambda a, b, c: -skew(b) / 6.0),
        (2, 1, lambda a, b, c: skew(a) / 6.0),
    )
    for i, j, k in faces:
        ids = (i, j, k)
        pos = (pts[i], pts[j], pts[k])
        for ia, ib, fn in blocks:
            mat = fn(*pos)
            di = ids[ia] * 6
            dj = ids[ib] * 6
            for a in range(3):
                for b in range(3):
                    val = mat[a, b]
                    if val != 0.0:
                        hr.append(di + a)
                        hc.append(dj + b)
                        hv.append(val)
    h = coo_matrix((hv, (hr, hc)), shape=(nd, nd)).tocsc()
    return h


def assemble_geo(cache, axial):
    nd = None
    gr, gc, gv = [], [], []
    for n_i, (_i, _j, rot, le, _trans, dofs) in zip(axial, cache):
        kg, _ = to_global(beam_kg(float(n_i), le), rot)
        if nd is None:
            nd = max(dofs) + 1
        for a in range(12):
            for b in range(12):
                val = kg[a, b]
                if val != 0.0:
                    gr.append(dofs[a])
                    gc.append(dofs[b])
                    gv.append(val)
    # nd from the last element is not the matrix order if the last node
    # is not the highest index. Caller passes the true order via cache dofs.
    order = 0
    for _item in cache:
        order = max(order, max(_item[5]) + 1)
    return coo_matrix((gv, (gr, gc)), shape=(order, order)).tocsc()


def kkt_factor(k, basis):
    c = csc_matrix(basis)
    zero = csc_matrix((basis.shape[1], basis.shape[1]))
    kkt = bmat([[k, c], [c.T, zero]], format="csc")
    return splu(kkt.tocsc())


def kkt_solve(lu, rhs, n_basis):
    full = np.zeros(rhs.shape[0] + n_basis)
    full[: rhs.shape[0]] = rhs
    sol = lu.solve(full)
    return sol[: rhs.shape[0]], sol[rhs.shape[0] :]


def subspace_buckling(k, bmat_op, basis, rq, shift, n_modes=12, n_iter=20):
    """Shift-invert subspace iteration for K v = lambda B v, R.T v = 0."""
    nd = k.shape[0]
    n_basis = basis.shape[1]
    shifted = (k - shift * bmat_op).tocsc()
    lu = kkt_factor(shifted, basis)
    rng = np.random.default_rng(20261020)
    q = rng.normal(size=(nd, n_modes))
    q -= rq @ (rq.T @ q)
    q, _ = np.linalg.qr(q, mode="reduced")
    history = []
    for step in range(n_iter):
        bq = bmat_op @ q
        y = np.zeros_like(q)
        for col in range(n_modes):
            y[:, col], _ = kkt_solve(lu, np.asarray(bq[:, col]).ravel(), n_basis)
        y -= rq @ (rq.T @ y)
        q, _ = np.linalg.qr(y, mode="reduced")
        if (step + 1) % 5 == 0 or step + 1 == n_iter:
            lam = ritz_lambdas(k, bmat_op, q)
            history.append({"iteration": step + 1, "shift": shift, "lowest_positive": lam[:6]})
            print("shift", shift, "iter", step + 1, lam[:4], flush=True)
    lam, vecs, residuals = ritz_report(k, bmat_op, q)
    return lam, vecs, residuals, history


def ritz_lambdas(k, bop, q):
    kr = q.T @ (k @ q)
    br = q.T @ (bop @ q)
    ev = np.linalg.eigvals(np.linalg.solve(br, kr)) if False else None
    ev, _ = _small_eigs(kr, br)
    pos = sorted(x for x in ev if x > 0.0)
    return pos


def _small_eigs(kr, br):
    ev, evec = np.linalg.eig(np.linalg.solve(0.5 * (br + br.T), 0.5 * (kr + kr.T)))
    real = []
    vecs = []
    for value, vector in zip(ev, evec.T):
        if abs(value.imag) > 1e-7 * max(1.0, abs(value.real)):
            continue
        real.append(float(value.real))
        vecs.append(np.real(vector))
    order = np.argsort(np.array(real))
    return [real[i] for i in order], [vecs[i] for i in order]


def ritz_report(k, bop, q):
    kr = q.T @ (k @ q)
    kr = 0.5 * (kr + kr.T)
    br = q.T @ (bop @ q)
    br = 0.5 * (br + br.T)
    ev, evec = np.linalg.eig(np.linalg.solve(br, kr))
    rows = []
    for value, vector in zip(ev, evec.T):
        if abs(value.imag) > 1e-6 * max(1.0, abs(value.real)):
            continue
        lam = float(value.real)
        if lam <= 0.0:
            continue
        coeff = np.real(vector)
        coeff = coeff / np.linalg.norm(coeff)
        full = q @ coeff
        kv = k @ full
        bv = bop @ full
        scale = np.linalg.norm(kv)
        residual = float(np.linalg.norm(kv - lam * bv) / max(scale, 1e-30))
        ray = float((full @ kv) / (full @ bv))
        rows.append((lam, ray, residual, full))
    rows.sort(key=lambda item: item[0])
    return (
        [r[0] for r in rows],
        [r[3] for r in rows],
        [{"lambda": r[0], "rayleigh": r[1], "residual": r[2]} for r in rows],
    )


def rel_diff(card, mine):
    return abs(mine - card) / max(abs(card), 1e-30)


def compare(row, field, card, mine, kind):
    difference = mine - card
    relative = rel_diff(card, mine)
    if relative < 1e-9 or abs(difference) < 1e-9:
        status = "match"
    elif relative < 5e-4:
        status = "rounding"
    else:
        status = kind
    return {
        "row": row,
        "field": field,
        "card": card,
        "mine": mine,
        "difference": difference,
        "relative": relative,
        "status": status,
    }


def cited_ratios(continuum):
    finest = CARD["lambda_m24"]
    out = []
    for name in ("perfect", "joint_offset", "crooked", "eigenmode"):
        a = CARD["nl6"][name]
        b = CARD["nl12"][name]
        out.append(
            {
                "case": name,
                "source": "owner published critical lambdas; this check did not rerun the nonlinear paths",
                "lambda_6seg": a,
                "lambda_12seg": b,
                "k_over_published_finest_linear": b / finest,
                "k_over_011b_continuum": b / continuum,
                "mesh_change_m6_to_m12": (b - a) / a,
            }
        )
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("closed", "all"), default="all")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    sec = section()
    one = pin_pin_factor(sec, 1)[0]
    two = pin_pin_factor(sec, 2)[0]
    eight = pin_pin_factor(sec, 8)[0]
    rotated = rotated_pin_factor(sec)
    column = {
        "one_element_PL2_over_EI": one,
        "two_element_PL2_over_EI": two,
        "eight_element_PL2_over_EI": eight,
        "rotated_one_element_PL2_over_EI": rotated,
        "target_one_element": 12.0,
        "target_refined_pi_squared": float(np.pi**2),
    }
    print("column", column, flush=True)
    if abs(one - 12.0) > 1e-6 or abs(rotated - 12.0) > 1e-5:
        raise SystemExit("column Hermite check failed")

    raw, raw_faces = base_icosahedron()
    raw = raw * (R_M / np.linalg.norm(raw[0]))
    # Rebuild unit-sphere icosahedron faces already oriented, then scale.
    base_v, base_f = base_icosahedron()
    scale = R_M / np.linalg.norm(base_v[0])
    base_scaled = base_v * scale
    # Orient is already outward in the raw frame; scaling preserves it.
    v_ico = volume(base_scaled, base_f)
    edge = float(np.linalg.norm(base_scaled[base_f[0][0]] - base_scaled[base_f[0][1]]))
    v_formula = 5.0 / 12.0 * (3.0 + np.sqrt(5.0)) * edge**3
    ico_check = {
        "vertices": len(base_v),
        "faces": len(base_f),
        "volume_m3": v_ico,
        "formula_volume_m3": v_formula,
        "relative": abs(v_ico - v_formula) / v_formula,
    }
    print("icosahedron", ico_check, flush=True)
    if len(base_v) != 12 or len(base_f) != 20 or ico_check["relative"] > 1e-8:
        raise SystemExit("icosahedron volume check failed")

    pts, faces, flipped, n_base_faces, n_base_verts = geodesic(FREQ, R_M)
    edge_count = edges_of(faces)
    bad_edges = {e: c for e, c in edge_count.items() if c != 2}
    members = list(edge_count.keys())
    arcs = []
    chords = []
    for i, j in members:
        cosang = float(np.dot(pts[i], pts[j]) / (R_M * R_M))
        cosang = min(1.0, max(-1.0, cosang))
        arcs.append(R_M * float(np.arccos(cosang)))
        chords.append(float(np.linalg.norm(pts[j] - pts[i])))
    arcs = np.asarray(arcs)
    chords = np.asarray(chords)
    vol = volume(pts, faces)
    sphere = 4.0 / 3.0 * np.pi * R_M**3
    grad = grad_volume(pts, faces)
    unit = pts / R_M
    radial_sum = float(np.sum(grad * unit))
    radial_expect = 3.0 * vol / R_M
    # Central difference on one coordinate.
    eps = 1e-5
    pts_p = pts.copy()
    pts_m = pts.copy()
    pts_p[4, 0] += eps
    pts_m[4, 0] -= eps
    fd = (volume(pts_p, faces) - volume(pts_m, faces)) / (2.0 * eps)
    fd_err = abs(fd - grad[4, 0])

    sec_out = section()
    area = sec_out["A_m2"]
    inertia = sec_out["I_m4"]
    tube = area * RHO * float(np.sum(arcs))
    joints = JOINT_FRAC * tube
    nodes = len(pts) * NODE_EACH_KG
    total = tube + joints + nodes + FILM_KG + SYSTEMS_KG
    payload = LIFT_KG - total
    overrun = total - LIFT_KG
    width = S_REQ / (2.0 * np.sqrt(3.0))
    w_line = P_PA * width
    mean_arc = float(np.mean(arcs))
    n_wr = P_PA * mean_arc / (2.0 * np.sqrt(3.0)) * R_M
    share = np.sqrt(3.0)
    sigma_wall = C_LOCAL * E_PA * WALL / R_O
    # 011b continuum from this seat's published SF_global at k=0.2.
    continuum = CARD["sf_global_k02"] / 0.2
    euler_two = (np.pi**2 * sec_out["EI"]) / (S_REQ**2) / (P_PA * S_REQ / 2.0 * R_M)
    euler_tri = (np.pi**2 * sec_out["EI"]) / (S_REQ**2) / (w_line * R_M)

    geometry = {
        "frequency": FREQ,
        "joints": len(pts),
        "members": len(members),
        "faces": len(faces),
        "faces_flipped_to_outward": flipped,
        "edges_not_shared_by_two_faces": len(bad_edges),
        "base_vertices": n_base_verts,
        "base_faces": n_base_faces,
        "arc_min_m": float(np.min(arcs)),
        "arc_mean_m": mean_arc,
        "arc_max_m": float(np.max(arcs)),
        "arc_total_m": float(np.sum(arcs)),
        "chord_total_m": float(np.sum(chords)),
        "volume_m3": vol,
        "sphere_volume_m3": sphere,
        "radial_gradient_sum": radial_sum,
        "radial_gradient_expect_3V_over_R": radial_expect,
        "radial_relative": abs(radial_sum - radial_expect) / abs(radial_expect),
        "gradient_fd_abs_error": fd_err,
        "icosahedron_check": ico_check,
    }
    print("geometry", {k: geometry[k] for k in ("joints", "members", "faces", "volume_m3", "arc_mean_m", "radial_relative", "gradient_fd_abs_error")}, flush=True)
    if len(pts) != 362 or len(members) != 1080 or len(faces) != 720 or bad_edges:
        raise SystemExit("geodesic counts failed")
    if geometry["radial_relative"] > 1e-8 or fd_err > 1e-6:
        raise SystemExit("volume gradient check failed")

    mass = {
        "tube_mass_kg": tube,
        "joints_5pct_kg": joints,
        "node_mass_kg": nodes,
        "film_mass_kg": FILM_KG,
        "systems_kg": SYSTEMS_KG,
        "total_kg": total,
        "lift_kg": LIFT_KG,
        "payload_kg": payload,
        "overrun_kg": overrun,
        "mass_over_lift_percent": 100.0 * total / LIFT_KG - 100.0,
        "tube_uses": "A * density * great-circle arc total",
        "tag": "QUESTIONABLE",
    }
    line = {
        "width_at_2p04_m": width,
        "w_at_2p04_N_per_m": w_line,
        "N_equals_wR_at_mean_arc_N": n_wr,
        "old_ps_over_2_divided_by_this_share": share,
        "formula": "width=s/(2*sqrt(3)); w=p*width; N=w*R with s=mean arc",
        "tag": "QUESTIONABLE",
    }
    wall = {
        "formula": "0.6 * E * wall / r_o",
        "sigma_wall_Pa": sigma_wall,
        "sigma_wall_GPa": sigma_wall / 1e9,
        "tag": "QUESTIONABLE",
    }
    print("mass_overrun_kg", overrun, "w", w_line, "wall_GPa", sigma_wall / 1e9, flush=True)

    result = {
        "schema": 1,
        "unit": "vacuum-mainline026-check-1020",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "phase": args.phase,
        "formulation": {
            "segments_per_arc": 3,
            "member_shape": "three straight chords on the great-circle arc",
            "beam": "Euler-Bernoulli 12-DOF, no shear, J=2I",
            "rigid_modes": "orthogonality constraints, no support pins",
            "load": "inward -p grad V, centroid fan on the 3-segment cell boundary",
            "hessian": "p Hessian(V) of that fan, central-difference of the quadratic gradient",
            "geometric_stiffness": "card cubic Hermite G with compression positive; initial moment, shear and axial initial-stress omitted",
            "eigen": "K v = lambda (G - p Hessian) v",
            "nonlinear": "not rerun; owner paths are hundreds of seconds each",
        },
        "column_check": column,
        "section": {
            "r_o_m": R_O,
            "wall_m": WALL,
            "r_i_m": sec_out["r_i_m"],
            "A_m2": area,
            "I_m4": inertia,
            "GJ_Nm2": sec_out["GJ"],
            "E_Pa": E_PA,
            "nu": NU,
            "density_kg_m3": RHO,
            "tag": "QUESTIONABLE",
        },
        "geometry": geometry,
        "mass": mass,
        "line_load": line,
        "wall_screen_closed_form": wall,
        "continuum_from_011b": {
            "sf_global_k_0p2": CARD["sf_global_k02"],
            "perfect_lambda": continuum,
            "source": "this seat 011b RESULTS SiC k=0.2 SF_global / 0.2",
            "tag": "QUESTIONABLE",
        },
        "euler_at_requested_spacing": {
            "two_way_share": euler_two,
            "equal_triangular_share": euler_tri,
        },
    }

    if args.phase == "all":
        # The one-segment polygon fan must reproduce the joint-triangle calculus.
        c1, _e1, _o1, p1 = subdivide(pts, faces, members, 1)
        g1, v1 = polygon_loads(c1, p1)
        grad_err = float(np.max(np.abs(g1 - grad)))
        print("polygon_matches_tet", grad_err, abs(v1 - vol), flush=True)
        if grad_err > 1e-8 or abs(v1 - vol) > 1e-6:
            raise SystemExit("polygon fan does not match the triangle volume")
        h_analytic = assemble_hessian(pts, faces, len(pts) * 6)
        h_poly, anti_1 = polygon_hessian(c1, p1, len(pts) * 6)
        h_gap = h_poly - h_analytic
        h_err = float(np.max(np.abs(h_gap.data))) if h_gap.nnz else 0.0
        print("polygon_hessian_gap", h_err, "antisym", anti_1, flush=True)
        if h_err > 1e-6 or anti_1 > 1e-6:
            raise SystemExit("polygon Hessian does not match the triangle Hessian")

        segs = 3
        coords, elements, owners, polygons = subdivide(pts, faces, members, segs)
        n_joints = len(pts)
        k, cache = assemble(coords, elements, sec_out)
        nd = len(coords) * 6
        basis, rq = rigid_basis(coords)
        kernel = [float(np.linalg.norm(k @ basis[:, col])) for col in range(6)]
        grad_s, vol_s = polygon_loads(coords, polygons)
        h, antisym_max = polygon_hessian(coords, polygons, nd)
        print(
            "subdivided",
            len(coords),
            len(elements),
            vol_s,
            "kernel",
            max(kernel),
            "antisym",
            antisym_max,
            flush=True,
        )
        if max(kernel) > 1e-3 or antisym_max > 1e-6:
            raise SystemExit("subdivided stiffness or Hessian failed its check")
        force = np.zeros(nd)
        force[0::6] = -P_PA * grad_s[:, 0]
        force[1::6] = -P_PA * grad_s[:, 1]
        force[2::6] = -P_PA * grad_s[:, 2]
        ft = force.reshape(-1, 6)[:, :3]
        net_f = ft.sum(axis=0)
        net_m = np.cross(coords, ft).sum(axis=0)
        print("net_force", net_f, "net_moment", net_m, flush=True)
        if np.linalg.norm(net_f) > 10.0 or np.linalg.norm(net_m) > 100.0:
            raise SystemExit("pressure load is not in equilibrium")
        lu = kkt_factor(k, basis)
        displacement, reactions = kkt_solve(lu, force, 6)
        static_res = float(
            np.linalg.norm(k @ displacement + basis @ reactions - force) / np.linalg.norm(force)
        )
        axial = []
        for (_i, _j, _rot, le, trans, dofs) in cache:
            ul = trans @ displacement[dofs]
            axial.append(-sec_out["EA"] / le * (ul[6] - ul[0]))
        axial = np.asarray(axial)
        member_n = np.zeros(len(members))
        member_c = np.zeros(len(members))
        for n_val, m_i in zip(axial, owners):
            member_n[m_i] += n_val
            member_c[m_i] += 1.0
        member_n /= member_c
        g = assemble_geo(cache, axial)
        b_follow = (g - P_PA * h).tocsc()
        b_dead = g.tocsc()
        print(
            "mean_segment_N",
            float(np.mean(axial)),
            "mean_member_N",
            float(np.mean(member_n)),
            "static_res",
            static_res,
            flush=True,
        )
        unit_s = coords / R_M

        def solve_case(op, label):
            _lam, vectors, residuals, history = subspace_buckling(
                k, op, basis, rq, shift=6.0, n_modes=10, n_iter=40
            )
            packed = []
            for item, vec in zip(residuals, vectors):
                trans = vec.reshape(-1, 6)[:, :3]
                energy = float(np.sum(trans * trans))
                radial = float(np.sum(np.sum(trans * unit_s, axis=1) ** 2) / max(energy, 1e-30))
                joint_energy = float(np.sum(trans[:n_joints] ** 2) / max(energy, 1e-30))
                item = dict(item)
                item["radial_fraction"] = radial
                item["joint_participation_fraction"] = joint_energy
                packed.append(item)
                if len(packed) >= 6:
                    break
            return {"label": label, "modes": packed, "history": history}

        follow = solve_case(b_follow, "follower")
        dead = solve_case(b_dead, "fixed_pressure_direction")
        if follow["modes"][0]["residual"] > 1e-4:
            raise SystemExit("follower eigen residual is too large")
        sigma_axial = float(np.max(axial) / area)
        euler_member = (np.pi**2 * sec_out["EI"]) / (arcs**2) / member_n
        result["linear"] = {
            "segments_per_arc": segs,
            "nodes": len(coords),
            "elements": len(elements),
            "physical_DOF": nd,
            "fan_volume_m3": vol_s,
            "kernel_abs_norms": kernel,
            "hessian_antisymmetry_max": antisym_max,
            "triangle_hessian_gap": h_err,
            "net_force_N": net_f.tolist(),
            "net_moment_Nm": net_m.tolist(),
            "static_relative_residual": static_res,
            "reaction_norm": float(np.linalg.norm(reactions)),
            "compression_N": {
                "segment_min": float(np.min(axial)),
                "segment_mean": float(np.mean(axial)),
                "segment_max": float(np.max(axial)),
                "member_mean": float(np.mean(member_n)),
                "member_max": float(np.max(member_n)),
            },
            "follower": follow,
            "fixed_direction": dead,
            "max_axial_stress_Pa": sigma_axial,
            "wall_lambda_from_this_axial_stress": sigma_wall / sigma_axial,
            "strength_lambda_from_this_axial_stress": SIGMA_TYPICAL_PA / sigma_axial,
            "member_euler_using_this_compression": {
                "min": float(np.min(euler_member)),
                "mean": float(np.mean(euler_member)),
                "max": float(np.max(euler_member)),
                "formula": "pi^2 EI / full_arc^2 / mean_segment_N",
            },
            "tag": "QUESTIONABLE",
            "projection": "rigid joints and fan load transfer",
        }
        my_lambda = follow["modes"][0]["rayleigh"]
        result["continuum_gap"] = {
            "my_lambda": my_lambda,
            "continuum": continuum,
            "relative_above_continuum": (my_lambda - continuum) / continuum,
        }

    comparisons = [
        compare("geometry", "joints", 362, len(pts), "mismatch"),
        compare("geometry", "members", 1080, len(members), "mismatch"),
        compare("geometry", "faces", 720, len(faces), "mismatch"),
        compare("geometry", "arc_min_m", CARD["arc_min_m"], float(np.min(arcs)), "mismatch"),
        compare("geometry", "arc_mean_m", CARD["arc_mean_m"], mean_arc, "mismatch"),
        compare("geometry", "arc_max_m", CARD["arc_max_m"], float(np.max(arcs)), "mismatch"),
        compare("geometry", "arc_total_m", CARD["arc_total_m"], float(np.sum(arcs)), "mismatch"),
        compare("section", "A_m2", CARD["A_m2"], area, "mismatch"),
        compare("section", "I_m4", CARD["I_m4"], inertia, "mismatch"),
        compare("section", "GJ_Nm2", CARD["GJ_Nm2"], sec_out["GJ"], "mismatch"),
        compare("mass", "tube_mass_kg", CARD["tube_mass_kg"], tube, "mismatch"),
        compare("mass", "joints_5pct_kg", CARD["joints_5pct_kg"], joints, "mismatch"),
        compare("mass", "node_mass_kg", CARD["node_mass_kg"], nodes, "mismatch"),
        compare("mass", "total_kg", CARD["total_mass_kg"], total, "mismatch"),
        compare("mass", "payload_kg", CARD["payload_kg"], payload, "mismatch"),
        compare("line_load", "width_m", CARD["width_m"], width, "mismatch"),
        compare("line_load", "w_N_per_m", CARD["w_Npm"], w_line, "mismatch"),
        compare("line_load", "N_wR_mean_N", CARD["N_wR_mean_N"], n_wr, "mismatch"),
        compare("line_load", "old_share_over_new", CARD["old_over_new_share"], share, "mismatch"),
        compare("wall", "sigma_Pa", CARD["sigma_wall_Pa"], sigma_wall, "mismatch"),
        compare("011b", "continuum_perfect", CARD["continuum_card"], continuum, "mismatch"),
        compare("011b", "euler_two_way", CARD["euler_011b_two_way"], euler_two, "mismatch"),
        compare("011b", "euler_triangular_s_2p04", CARD["euler_011b_triangular"], euler_tri, "mismatch"),
    ]
    gap_card = (CARD["lambda_m24"] - continuum) / continuum
    comparisons.append(
        compare(
            "linear",
            "published_finest_above_continuum",
            0.0550918010983863,
            gap_card,
            "mismatch",
        )
    )
    # The card text says 5.51%. 0.0550918 is 5.509%.
    comparisons.append(
        compare("card_text", "percent_above_continuum_rounded", 0.0551, gap_card, "rounding")
    )
    result["cited_nonlinear_ratios"] = cited_ratios(continuum)
    for row in result["cited_nonlinear_ratios"]:
        comparisons.append(
            compare(
                "nonlinear_cited:" + row["case"],
                "k_over_finest_linear",
                {
                    "perfect": 0.7899806437105842,
                    "joint_offset": 4.950376047460733 / CARD["lambda_m24"],
                    "crooked": 5.082613207915408 / CARD["lambda_m24"],
                    "eigenmode": 4.539579837323961 / CARD["lambda_m24"],
                }[row["case"]],
                row["k_over_published_finest_linear"],
                "mismatch",
            )
        )
    if args.phase == "all":
        my_lambda = result["linear"]["follower"]["modes"][0]["rayleigh"]
        my_dead = result["linear"]["fixed_direction"]["modes"][0]["rayleigh"]
        comparisons.append(
            compare("linear", "lambda_vs_card_m24", CARD["lambda_m24"], my_lambda, "mesh")
        )
        comparisons.append(
            compare("linear", "lambda_vs_card_m3", CARD["lambda_m3"], my_lambda, "mesh")
        )
        comparisons.append(
            compare("linear", "dead_lambda", CARD["dead_lambda"], my_dead, "mesh")
        )
        comparisons.append(
            compare(
                "linear",
                "discrete_mean_compression_N",
                CARD["discrete_mean_N"],
                result["linear"]["compression_N"]["member_mean"],
                "mesh",
            )
        )
        comparisons.append(
            compare(
                "wall",
                "unit_axial_stress_Pa",
                CARD["sigma_axial_Pa"],
                result["linear"]["max_axial_stress_Pa"],
                "mesh",
            )
        )
        comparisons.append(
            compare(
                "wall",
                "nominal_wall_lambda",
                CARD["wall_lambda"],
                result["linear"]["wall_lambda_from_this_axial_stress"],
                "mesh",
            )
        )
        comparisons.append(
            compare(
                "linear",
                "member_euler_min",
                CARD["euler_min"],
                result["linear"]["member_euler_using_this_compression"]["min"],
                "mesh",
            )
        )
        comparisons.append(
            compare(
                "load",
                "fan_volume_m3",
                CARD["fan_volume_m3"],
                result["linear"]["fan_volume_m3"],
                "mesh",
            )
        )
    result["comparisons"] = comparisons
    result["mismatches"] = [row for row in comparisons if row["status"] not in ("match", "rounding")]
    text = json.dumps(scrub(result), indent=1)
    tmp = args.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.write("\n")
    os.replace(tmp, args.out)
    print("wrote", args.out, flush=True)


if __name__ == "__main__":
    main()
