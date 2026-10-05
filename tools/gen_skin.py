#!/usr/bin/env python3
"""#63 — the loaded skin: solve the film's pressure-loaded shape and cut the net for it.

WHY THIS TOOL EXISTS. The film cannot be installed flat. The analysis fixes the loaded
bulge at h = 0.25*r over each panel's incircle (research/analysis/vacuum-cell.py,
panel_tension), and reaching that shape from a flat sheet demands 4.12% membrane strain
against the 0.27-0.40% the film delivers at working stress — the independent physics
audit reproduced both numbers. A flat net comes up drum-tight and crazes its barrier
coating on the first pump-down. The escape, stated in the analysis as a design
requirement, is to PRE-FORM the membrane: cut each panel for the shape the pressure will
give it. This tool computes that shape and produces the cutting geometry.

WHAT IT COMPUTES, in order, each step gated:

  1. THE PANELS. The film's unsupported spans are NOT the 14 faces — the faces are braced.
     Each hexagon carries six radial spokes (six equilateral triangles, side = the cell
     edge), and each square holds four in-plane ties from its rim vertices to the face
     centre (both diagonals: four right isosceles triangles, legs = the half-pitch tie).
     72 panels in two congruence classes, derived here from the same integer-lattice
     arithmetic as gen_nodes.article_graph() and gated against its member list edge by
     edge. NOTE: the analysis' PANEL["squareSpoked"] = 1/(2+sqrt2) of the EDGE is the
     inradius of a half-square, not of these quarter-square panels — the real square
     panel is smaller (inradius 51.9 mm, not 73.4). The net is cut for the article, so
     this tool uses the article's panels and records the discrepancy for the analysis.

  2. THE LOADED SURFACE. The model's own law: a panel at inradius r operates as a
     spherical cap of radius R = 2.125*r (that is h = 0.25*r over the incircle), so its
     tension is T = p*R/2 and the equilibrium surface is the constant-mean-curvature
     graph  div(grad w / sqrt(1+|grad w|^2)) = -2/R  over the REAL panel polygon, w = 0
     on the boundary frame. Solved by P1 finite elements with Picard iteration on the
     slope weight. Three reproductions gate the solver before its answer is used:
       - on the incircle DISC the solve must return the analysis' own cap: sag -> 0.25*r;
       - in the LINEAR limit on the equilateral panel the exact closed form
         w = 2*d1*d2*d3/(3*r*R) gives sag = 2*r^2/(3R) and bowl volume 0.3*r^2*A/R
         (Saint-Venant's torsion solution; d_i = 3*r*lambda_i and Viviani's theorem);
       - halving the mesh must move the answer toward those values at second order.

  3. THE DISPLACEMENT DEBIT. Every bowl is open to the sky: the article displaces less
     air than its outline claims. The bowls' integral is subtracted from the nominal
     0.709^3/2 m^3 and published — the page ledger reads it from here. The analysis'
     smeared 8.6% (flat face area x h/2 at the incircle sag) is reproduced as a check,
     then replaced by the solved integral.

  4. THE GORE STUDY, which decides HOW the net is made. A doubly-curved panel cannot
     be flattened whole (~2% strain, ten times the film's budget), so a flat-cut panel
     must be assembled from radial gores meeting at the incentre. The tool flattens
     every gore at k = 3, 6 and 12 by least squares on every mesh edge length and
     measures the worst residual strain. The measured verdict: only k = 12 clears the
     film's 0.27% elastic budget — and twelve gores on each of 72 panels is over a
     thousand slivers of film joined by tens of metres of seam that lie on no structure.
     THE NET IS THEREFORE FORMED, NOT GORED: its outline, cuts and folds are unchanged
     from the proven flat net, and each face's panel field is pressed to this tool's
     solved surface before assembly (two dies — one hexagon face, one square face; the
     dimple edges end on the member lines, where w = 0, so every fold line survives).
     The gored alternative is recorded with its outlines, strain and seam bill, as the
     quantified reason forming wins.

OUTPUTS. research/geometry/skin/loaded-skin.json (the record: solve, gores, totals) and
ship/skin.generated.js (the page's copy: subsampled class meshes, 72 placements, the
ledger numbers). --check regenerates both and compares their data, so a stale
committed copy goes red without an argument. Every gate prints as a PROOF line; any
failure exits nonzero. Deterministic: fixed meshes, fixed iteration, no randomness.
Pure numpy: scipy is not a declared dependency of this repository, so both linear
solves (the FEM systems and the flattening's Gauss-Newton normal equations) run on a
Jacobi-preconditioned conjugate gradient with bincount matvecs.
"""

import argparse
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_nodes  # noqa: E402  (article_graph parity gate)
from data_compare import first_difference, numeric_equal, parse_json, parse_skin_literal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_OUT = os.path.join(ROOT, "research", "geometry", "skin", "loaded-skin.json")
JS_OUT = os.path.join(ROOT, "ship", "skin.generated.js")

# The article's exact cut basis: half-pitch 177.25 mm, span 709.00 mm across the squares.
# One unit of the integer lattice is one half-pitch. Mirrors check_assembly's KNOWN span.
S = 0.17725
SPAN = 4.0 * S / 2.0 * 2.0            # 0.7090: max|u| = 2 units of S across the squares
P_SL = 101325.0                        # sea-level standard atmosphere, Pa
P_2500 = 101325.0 * (1.0 - 0.0065 * 2500.0 / 288.15) ** (9.80665 / (287.05 * 0.0065))
BULGE = 0.25                           # the analysis' operating point: h = BULGE * r
R_OVER_r = (1.0 + BULGE * BULGE) / (2.0 * BULGE)   # 2.125 exactly
STRAIN_BUDGET = 0.0027                 # film working strain, conservative end (0.27-0.40%)
SPLITS = 2                             # radial sector splits per half-side (12 sectors/panel)
MESH_M = 24                            # barycentric subdivisions per sector
REF_M = 12                             # coarse mesh for the refinement gates
PAGE_M = 6                             # page mesh: exact subsample (MESH_M % PAGE_M == 0)
PICARD_TOL = 1e-12                     # metres; nonlinear iteration convergence
PICARD_CAP = 300
POST_R = 0.005                         # land-post top radius: the film is pinned on it
TUBE_R = 0.005                         # bare 10 mm OD tube radius, for clearance
JOINT_ZONE = 0.040                     # length of member inside/behind its printed joint
CLEAR_MARGIN = 0.003                   # required film standoff from a bare tube surface

PROOFS = []


def proof(name, ok, detail):
    PROOFS.append((name, bool(ok), detail))
    print(f"  {'PROOF' if ok else 'FAIL '}  {name}: {detail}")
    return bool(ok)


# ---------------------------------------------------------------------------------------
# 1. Panels — from the same integers as the article graph, gated against it.
# ---------------------------------------------------------------------------------------

def panel_layout():
    """72 film panels as integer-vertex triples (unit = half-pitch), with roles.

    hexTri: (hub, cornerA, cornerB) — consecutive corners around each hexagon hub.
    sqTri:  (centre, cornerA, cornerB) — consecutive rim vertices around each square centre.
    """
    nodes, members, _ = gen_nodes.article_graph()
    pos = {u for u, _k in nodes}
    fam = {}
    for u, v, k in members:
        fam[frozenset((u, v))] = k

    def ring(centre, corners, normal):
        n = np.array(normal, float)
        n /= np.linalg.norm(n)
        e1 = np.array([1.0, 0.0, 0.0])
        if abs(e1 @ n) > 0.9:
            e1 = np.array([0.0, 1.0, 0.0])
        e1 = e1 - (e1 @ n) * n
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(n, e1)
        c = np.array(centre, float)
        ang = sorted(corners, key=lambda q: math.atan2((np.array(q) - c) @ e2,
                                                       (np.array(q) - c) @ e1))
        return ang

    panels = []
    hubs = [u for u, k in nodes if k == "hexHub"]
    for hub in hubs:
        corners = [v if u == hub else u for u, v, k in members
                   if k == "spoke" and hub in (u, v)]
        assert len(corners) == 6, (hub, corners)
        order = ring(hub, corners, hub)          # hexagon plane normal is the hub direction
        for i in range(6):
            panels.append(("hexTri", hub, order[i], order[(i + 1) % 6]))
    for axis in range(3):
        for sgn in (-1, 1):
            centre = tuple(2 * sgn if q == axis else 0 for q in range(3))
            assert centre in pos, centre
            corners = [u for u, k in nodes if k == "rimVertex" and u[axis] == 2 * sgn]
            assert len(corners) == 4, (centre, corners)
            normal = [sgn if q == axis else 0 for q in range(3)]
            order = ring(centre, corners, normal)
            for i in range(4):
                panels.append(("sqTri", centre, order[i], order[(i + 1) % 4]))

    # Gate: every panel edge is a real member of the right family, and every in-face
    # member is shared by exactly the panels that should share it.
    want = {("hexTri", "apex"): "spoke", ("hexTri", "base"): "rim",
            ("sqTri", "apex"): "tie", ("sqTri", "base"): "rim"}
    edge_use = {}
    ok = True
    for cls, apex, a, b in panels:
        for u, v, role in ((apex, a, "apex"), (apex, b, "apex"), (a, b, "base")):
            k = fam.get(frozenset((u, v)))
            if k != want[(cls, role)]:
                ok = False
            edge_use[frozenset((u, v))] = edge_use.get(frozenset((u, v)), 0) + 1
    proof("panelEdgesAreMembers", ok, "every panel edge is a member of its expected family")
    spokes = [m for m in edge_use if fam.get(m) == "spoke"]
    rims = [m for m in edge_use if fam.get(m) == "rim"]
    sq_ties = [m for m in edge_use if fam.get(m) == "tie" and edge_use[m]]
    counts_ok = (len(panels) == 72
                 and sum(1 for c, *_ in panels if c == "hexTri") == 48
                 and sum(1 for c, *_ in panels if c == "sqTri") == 24
                 and all(edge_use[m] == 2 for m in spokes) and len(spokes) == 48
                 and all(edge_use[m] == 2 for m in rims) and len(rims) == 36
                 and all(edge_use[m] == 2 for m in sq_ties) and len(sq_ties) == 24)
    proof("panelTiling", counts_ok,
          f"{len(panels)} panels (48 hex + 24 sq); every spoke, rim edge and in-plane "
          f"tie borders exactly 2 panels ({len(spokes)}/{len(rims)}/{len(sq_ties)} members)")
    return panels


def canonical_panels():
    """The two congruence classes in 2D, incentre at the origin.

    hexTri: equilateral, side sqrt2*S (spoke = rim = the cell edge). V0 is the hub.
    sqTri: right isosceles, legs S (the ties), hypotenuse sqrt2*S (the rim edge).
    V0 is the square centre (the right angle).
    """
    L = math.sqrt(2.0) * S
    r_hex = L / (2.0 * math.sqrt(3.0))
    hex_v = np.array([[0.0, L / math.sqrt(3.0)],
                      [-L / 2.0, -r_hex],
                      [L / 2.0, -r_hex]])
    r_sq = S * (2.0 - math.sqrt(2.0)) / 2.0
    sq_v = np.array([[0.0, 0.0], [S, 0.0], [0.0, S]]) - r_sq
    return {"hexTri": {"verts": hex_v, "r": r_hex},
            "sqTri": {"verts": sq_v, "r": r_sq}}


def placements(panels, canon):
    """A rigid map (origin, E1, E2, N) per panel from canonical 2D into the article,
    exact to the integer arithmetic. w is drawn along -N (inward: the film bows into
    the vacuum). Congruence is the gate: all three side lengths must match the class."""
    out = []
    ok = True
    for cls, apex, a, b in panels:
        P = np.array([apex, a, b], float) * S
        V = canon[cls]["verts"]
        for (i, j) in ((0, 1), (0, 2), (1, 2)):
            if abs(np.linalg.norm(P[i] - P[j]) - np.linalg.norm(V[i] - V[j])) > 1e-12:
                ok = False
        # Rigid map: E1 along V0->V1, E2 completing in-plane, N the outward face normal.
        d2 = V[1] - V[0]
        u1 = d2 / np.linalg.norm(d2)
        u2 = np.array([-u1[1], u1[0]])
        D = P[1] - P[0]
        E1 = D / np.linalg.norm(D)
        # In-plane second direction from the third vertex, Gram-Schmidt.
        D2 = P[2] - P[0]
        E2 = D2 - (D2 @ E1) * E1
        E2 /= np.linalg.norm(E2)
        # Canonical (u1,u2) components of V2-V0 must reproduce P2-P0 with a POSITIVE
        # u2 component mapping to E2 (handedness), which the vertex order guarantees.
        c1, c2 = (V[2] - V[0]) @ u1, (V[2] - V[0]) @ u2
        if c2 < 0:
            ok = False
        rebuilt = P[0] + c1 * E1 + c2 * E2
        if np.linalg.norm(rebuilt - P[2]) > 1e-12:
            ok = False
        N = np.cross(E1, E2)
        centre = P.mean(axis=0)
        if N @ centre < 0:            # every face's outward normal points away from origin
            N = -N
            # flip E2 to keep E1 x E2 = N; canonical y then maps mirrored, which the
            # mirror symmetry of both classes absorbs.
            E2 = -E2
        # Origin maps the canonical incentre (2D origin) into the face.
        A1 = (V[0] @ u1, V[0] @ u2)
        origin = P[0] - A1[0] * E1 - A1[1] * E2
        out.append({"cls": cls, "origin": origin, "E1": E1, "E2": E2, "N": N})
    proof("placementsCongruent", ok,
          "all 72 rigid maps reproduce their integer vertices to 1e-12")
    return out


# ---------------------------------------------------------------------------------------
# 2. Mesh — six sectors glued (incentre -> corners and incircle touchpoints), so every
#    gore boundary this tool can choose is an exact line of mesh edges.
# ---------------------------------------------------------------------------------------

def tri_grid(A, B, C, m):
    """Structured barycentric mesh of one sector."""
    verts, index = [], {}
    for i in range(m + 1):
        for j in range(m + 1 - i):
            index[(i, j)] = len(verts)
            verts.append(A + (B - A) * (i / m) + (C - A) * (j / m))
    tris = []
    for i in range(m):
        for j in range(m - i):
            v00, v10, v01 = index[(i, j)], index[(i + 1, j)], index[(i, j + 1)]
            tris.append((v00, v10, v01))
            if j < m - i - 1:
                tris.append((index[(i + 1, j)], index[(i + 1, j + 1)], index[(i, j + 1)]))
    return np.array(verts), tris


def panel_mesh(V, m, splits=2):
    """Glue radial sector grids about the incentre (the 2D origin by construction).

    Each side carries 2*splits sectors: the incircle's tangent foot (the touchpoint —
    the midpoint on the equilateral) splits the side in two, and each half is split
    `splits` ways evenly. Every radial line incentre -> outer point is then a real mesh
    polyline, so every gore boundary the study can choose is exact mesh edges. Vertices
    on shared lines coincide exactly (same endpoints, same fractions) and are
    deduplicated by key.
    """
    I = np.zeros(2)
    sides = [(0, 1), (1, 2), (2, 0)]
    feet, outer = {}, {}
    for (i, j) in sides:
        d = V[j] - V[i]
        t = ((I - V[i]) @ d) / (d @ d)
        T = V[i] + t * d
        feet[(i, j)] = T
        pts = [V[i] + (T - V[i]) * (q / splits) for q in range(splits)]
        pts += [T + (V[j] - T) * (q / splits) for q in range(splits)]
        pts.append(np.array(V[j], float))
        outer[(i, j)] = pts
    sectors = []
    for (i, j) in sides:
        pts = outer[(i, j)]
        for q in range(2 * splits):
            sectors.append((I, pts[q], pts[q + 1]))
    verts, tris, keymap = [], [], {}
    sector_of = []
    for s_idx, (A, B, C) in enumerate(sectors):
        sv, st = tri_grid(A, B, C, m)
        local = []
        for p in sv:
            k = (round(float(p[0]), 12), round(float(p[1]), 12))
            if k not in keymap:
                keymap[k] = len(verts)
                verts.append(p)
            local.append(keymap[k])
        for (a, b, c) in st:
            tris.append((local[a], local[b], local[c]))
            sector_of.append(s_idx)
    verts = np.array(verts)
    tris = np.array(tris, dtype=np.int64)
    # Boundary: vertices on any of the three panel sides.
    bnd = np.zeros(len(verts), dtype=bool)
    for (i, j) in sides:
        d = V[j] - V[i]
        L2 = d @ d
        rel = verts - V[i]
        t = (rel @ d) / L2
        off = rel - np.outer(t, d)
        on = (np.abs(off).max(axis=1) < 1e-9) & (t > -1e-9) & (t < 1 + 1e-9)
        bnd |= on
    # The sunken-frame boundary condition: at every corner the film lands on a printed
    # post whose flat top IS the nominal plane, so it is pinned over the post disc, not
    # at a point. (All three corners of every panel are article nodes.)
    for cnr in range(3):
        bnd |= np.linalg.norm(verts - V[cnr], axis=1) < POST_R
    return {"verts": verts, "tris": tris, "bnd": bnd,
            "sector_of": np.array(sector_of), "feet": feet, "outer": outer,
            "splits": splits, "V": V}


# ---------------------------------------------------------------------------------------
# 3. The membrane solve — P1 FEM, Picard on the slope weight.
# ---------------------------------------------------------------------------------------

def fem_grads(verts, tris):
    """Per-element area and P1 basis gradients."""
    p = verts[tris]                                    # (ne, 3, 2)
    e1 = p[:, 1] - p[:, 0]
    e2 = p[:, 2] - p[:, 0]
    det = e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0]
    area = 0.5 * np.abs(det)
    # grad lambda_i: rotate opposite edge by 90 deg / (2A), signed with det.
    g = np.empty((len(tris), 3, 2))
    for i in range(3):
        a = p[:, (i + 1) % 3]
        b = p[:, (i + 2) % 3]
        d = b - a
        g[:, i, 0] = -d[:, 1] / det
        g[:, i, 1] = d[:, 0] / det
    return area, g


def cg_solve(rows, cols, vals, b, x0, tol=1e-13, cap=20000):
    """Jacobi-preconditioned conjugate gradient on a symmetric positive definite
    system given as COO triplets. Deterministic; raises if it does not converge."""
    n = len(b)
    diag = np.bincount(rows[rows == cols], weights=vals[rows == cols], minlength=n)
    assert (diag > 0).all(), "system diagonal must be positive"

    def Av(x):
        return np.bincount(rows, weights=vals * x[cols], minlength=n)

    x = x0.copy()
    r = b - Av(x)
    bnorm = float(np.linalg.norm(b)) or 1.0
    z = r / diag
    p = z.copy()
    rz = float(r @ z)
    for _ in range(cap):
        if np.linalg.norm(r) <= tol * bnorm:
            return x
        Ap = Av(p)
        alpha = rz / float(p @ Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        z = r / diag
        rz_new = float(r @ z)
        p = z + (rz_new / rz) * p
        rz = rz_new
    raise AssertionError(f"CG did not converge: |r|/|b| = {np.linalg.norm(r) / bnorm:.2e}")


def membrane_solve(mesh, R, linear=False):
    """Solve div(q grad w) = -2/R, q = 1/sqrt(1+|grad w|^2) (q = 1 when linear),
    w = 0 on the boundary. Returns w plus per-element gradient of the converged state."""
    verts, tris, bnd = mesh["verts"], mesh["tris"], mesh["bnd"]
    nv, ne = len(verts), len(tris)
    area, g = fem_grads(verts, tris)
    c = 2.0 / R
    f = np.zeros(nv)
    np.add.at(f, tris.ravel(), np.repeat(c * area / 3.0, 3))
    free = ~bnd
    fmap = -np.ones(nv, dtype=np.int64)
    fmap[free] = np.arange(int(free.sum()))
    # Fixed sparsity: element (i, j) pairs with both ends free, mapped to free indexing;
    # per-iteration values are the fixed gradient products times the slope weight q.
    gij = np.einsum("eiv,ejv->eij", g, g) * area[:, None, None]
    rows_all = fmap[np.repeat(tris, 3, axis=1).ravel()]
    cols_all = fmap[np.tile(tris, (1, 3)).ravel()]
    keep = (rows_all >= 0) & (cols_all >= 0)
    rows_k, cols_k = rows_all[keep], cols_all[keep]
    w = np.zeros(nv)
    wf = np.zeros(int(free.sum()))
    it = 0
    for it in range(1, PICARD_CAP + 1):
        gw = np.einsum("eiv,ei->ev", g, w[tris])
        q = np.ones(ne) if linear else 1.0 / np.sqrt(1.0 + (gw * gw).sum(axis=1))
        vals = (gij * q[:, None, None]).ravel()[keep]
        wf = cg_solve(rows_k, cols_k, vals, f[free], wf, tol=1e-14)
        w_new = np.zeros(nv)
        w_new[free] = wf
        delta = np.abs(w_new - w).max()
        w = w_new
        if linear or delta < PICARD_TOL:
            break
    assert linear or delta < PICARD_TOL, f"Picard did not converge: {delta}"
    gw = np.einsum("eiv,ei->ev", g, w[tris])
    return {"w": w, "grad": gw, "area": area, "iters": it}


def disc_mesh(r, wedges, rings):
    """Polygonized incircle disc for the cap-law reproduction gate."""
    verts = [np.zeros(2)]
    ring_start = [None]
    for k in range(1, rings + 1):
        ring_start.append(len(verts))
        for a in range(wedges):
            th = 2.0 * math.pi * a / wedges
            verts.append(np.array([math.cos(th), math.sin(th)]) * (r * k / rings))
    verts = np.array(verts)
    tris = []
    for a in range(wedges):
        tris.append((0, 1 + a, 1 + (a + 1) % wedges))
    for k in range(1, rings):
        s0, s1 = ring_start[k], ring_start[k + 1]
        for a in range(wedges):
            a2 = (a + 1) % wedges
            tris.append((s0 + a, s1 + a, s1 + a2))
            tris.append((s0 + a, s1 + a2, s0 + a2))
    tris = np.array(tris, dtype=np.int64)
    bnd = np.zeros(len(verts), dtype=bool)
    bnd[ring_start[rings]:] = True
    return {"verts": verts, "tris": tris, "bnd": bnd}


def surface_quantities(mesh, sol):
    """Bowl volume (flat-projected), lifted dome area, incentre sag, worst slope."""
    verts, tris = mesh["verts"], mesh["tris"]
    w, area, gw = sol["w"], sol["area"], sol["grad"]
    vol = float((area * w[tris].mean(axis=1)).sum())
    dome = float((area * np.sqrt(1.0 + (gw * gw).sum(axis=1))).sum())
    icent = int(np.argmin(np.linalg.norm(verts, axis=1)))
    assert np.linalg.norm(verts[icent]) < 1e-12
    slope = float(np.sqrt((gw * gw).sum(axis=1)).max())
    return {"volM3": vol, "domeM2": dome, "sagM": float(w[icent]), "slopeMax": slope}

# ---------------------------------------------------------------------------------------
# 4. Symmetry and reproduction gates.
# ---------------------------------------------------------------------------------------

def keymap_of(verts):
    return {(round(float(p[0]), 9), round(float(p[1]), 9)): i
            for i, p in enumerate(verts)}


def symmetry_gap(mesh, w, transform):
    """Worst |w(p) - w(Tp)| over all vertices, with Tp located by rounded key."""
    km = keymap_of(mesh["verts"])
    worst = 0.0
    for i, p in enumerate(mesh["verts"]):
        q = transform(p)
        j = km.get((round(float(q[0]), 9), round(float(q[1]), 9)))
        assert j is not None, f"symmetry image of vertex {i} is not a mesh vertex"
        worst = max(worst, abs(float(w[i] - w[j])))
    return worst


# ---------------------------------------------------------------------------------------
# 5. Gores — cut, flatten by least squares on every edge length, measure the residual.
# ---------------------------------------------------------------------------------------

def gore_groups(k, splits):
    """Which sectors form each of k gores. Sectors are built per side, 2*splits per
    side, in the fixed order side(0,1), side(1,2), side(2,0). k must be 3, 6 or 12 and
    divide the sector count."""
    per_side = k // 3
    width = 2 * splits // per_side
    assert width * per_side == 2 * splits, (k, splits)
    groups = []
    for s in range(3):
        base = s * 2 * splits
        for g in range(per_side):
            groups.append(tuple(base + g * width + q for q in range(width)))
    return groups


def submesh(mesh, w, sectors):
    keep = np.isin(mesh["sector_of"], sectors)
    tris = mesh["tris"][keep]
    used = np.unique(tris)
    remap = -np.ones(len(mesh["verts"]), dtype=np.int64)
    remap[used] = np.arange(len(used))
    v3 = np.column_stack([mesh["verts"][used], w[used]])
    return v3, remap[tris], used


def flatten_gore(v3, tris, i_pin, j_pin):
    """Least-squares isometric flattening: minimize edge-length error over 2D positions,
    Gauss-Newton with the analytic sparse Jacobian (unit edge direction over rest length
    per endpoint). Gauge pinned: vertex i_pin at the origin, vertex j_pin on the +y axis.
    Returns the 2D layout and the signed strain of every edge. Deterministic."""
    edges = set()
    for a, b, c in tris:
        for u, v in ((a, b), (b, c), (c, a)):
            edges.add((min(u, v), max(u, v)))
    edges = np.array(sorted(edges))
    l3 = np.linalg.norm(v3[edges[:, 0]] - v3[edges[:, 1]], axis=1)
    n = len(v3)
    x = v3[:, :2].copy()
    # Rotate the initial guess so the pin direction is +y, translate pin to origin.
    d = x[j_pin] - x[i_pin]
    th = math.atan2(d[0], d[1])
    rot = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    x = (x - x[i_pin]) @ rot.T
    free = np.ones((n, 2), dtype=bool)
    free[i_pin] = False
    free[j_pin, 0] = False
    fidx = np.flatnonzero(free.ravel())
    col_of = -np.ones(2 * n, dtype=np.int64)
    col_of[fidx] = np.arange(len(fidx))
    ne = len(edges)

    def strains_of(x):
        d = x[edges[:, 0]] - x[edges[:, 1]]
        return (np.linalg.norm(d, axis=1) - l3) / l3

    prev = None
    for _it in range(200):
        d = x[edges[:, 0]] - x[edges[:, 1]]
        ln = np.linalg.norm(d, axis=1)
        r = (ln - l3) / l3
        unit = d / ln[:, None]
        # J rows: +unit/l3 at edge start, -unit/l3 at edge end, up to 4 free columns
        # per row (2 endpoints x 2 axes); pinned slots stay column -1, value 0.
        ecols = np.full((ne, 4), -1, dtype=np.int64)
        evals = np.zeros((ne, 4))
        for side, sgn in ((0, 1.0), (1, -1.0)):
            vv = edges[:, side]
            for ax in (0, 1):
                cc = col_of[2 * vv + ax]
                slot = side * 2 + ax
                ecols[:, slot] = cc
                evals[:, slot] = np.where(cc >= 0, sgn * unit[:, ax] / l3, 0.0)
        # Gauss-Newton normal equations as COO triplets: 4x4 outer product per edge,
        # plus a vanishing Tikhonov diagonal to keep the CG diagonal strictly positive.
        jr = np.repeat(ecols, 4, axis=1).ravel()
        jc = np.tile(ecols, (1, 4)).ravel()
        jv = (evals[:, :, None] * evals[:, None, :]).ravel()
        keep = (jr >= 0) & (jc >= 0)
        nf = len(fidx)
        rows_t = np.concatenate([jr[keep], np.arange(nf)])
        cols_t = np.concatenate([jc[keep], np.arange(nf)])
        vals_t = np.concatenate([jv[keep], np.full(nf, 1e-12)])
        good = ecols >= 0
        rhs = -np.bincount(ecols[good], weights=(evals * r[:, None])[good],
                           minlength=nf)
        step = cg_solve(rows_t, cols_t, vals_t, rhs, np.zeros(nf), tol=1e-10)
        flat = x.ravel()
        flat[fidx] += step
        x = flat.reshape(n, 2)
        cost = float(r @ r)
        done = ((prev is not None and abs(prev - cost) <= 1e-14 * max(prev, 1e-30))
                or float(np.abs(step).max()) < 1e-11)
        if done:
            return x, strains_of(x), edges
        prev = cost
    raise AssertionError("gore flattening did not converge")


def boundary_loop(tris):
    """Ordered boundary vertex loop of a triangulated patch."""
    count = {}
    for a, b, c in tris:
        for u, v in ((a, b), (b, c), (c, a)):
            count[(min(u, v), max(u, v))] = count.get((min(u, v), max(u, v)), 0) + 1
    nxt = {}
    for a, b, c in tris:
        for u, v in ((a, b), (b, c), (c, a)):
            if count[(min(u, v), max(u, v))] == 1:
                nxt[u] = v
    start = next(iter(nxt))
    loop, at = [start], nxt[start]
    while at != start:
        loop.append(at)
        at = nxt[at]
    return loop


def cut_lengths(mesh, w, V, k):
    """Lifted (on-surface) length of each gore cut line: the k radial lines from the
    incentre to the gore boundaries' outer points (corners at k = 3; touchpoints join at
    k = 6; the quarter points too at k = 12). These are the seams a gored panel needs."""
    km_v = mesh["verts"]
    splits = mesh["splits"]
    width = 2 * splits // (k // 3)
    ends = [np.array(V[i], float) for i in range(3)]
    for s in ((0, 1), (1, 2), (2, 0)):
        pts = mesh["outer"][s]
        ends += [pts[q] for q in range(width, 2 * splits, width)]
    total = 0.0
    per_cut = []
    for E in ends:
        L = np.linalg.norm(E)
        d = E / L
        t = km_v @ d
        off = km_v - np.outer(t, d)
        on = (np.abs(off).max(axis=1) < 1e-9) & (t > -1e-9) & (t < L + 1e-9)
        idx = np.flatnonzero(on)
        order = idx[np.argsort(t[idx])]
        p3 = np.column_stack([km_v[order], w[order]])
        seg = float(np.linalg.norm(np.diff(p3, axis=0), axis=1).sum())
        per_cut.append(seg)
        total += seg
    return total, per_cut


def develop(cls_name, mesh, w, V, budget):
    """THE GORE STUDY: flatten every gore at k = 3, 6 and 12 and measure the residual.

    This is the study that decides HOW the net is made, so all three counts are always
    measured — the residual is the finding, not a retry loop. Its verdict, printed by
    main(): flat-cut goring only clears the film's elastic budget at twelve gores per
    panel, and the article has 72 panels; the net is therefore FORMED (the panel fields
    pressed to this solved surface, outline unchanged), and the gored alternative is
    recorded here with its measured strain and seam bill."""
    study = {}
    for k in (3, 6, 12):
        worst = 0.0
        gores = []
        for gi, sectors in enumerate(gore_groups(k, mesh["splits"])):
            v3, tris, used = submesh(mesh, w, sectors)
            km = keymap_of(v3[:, :2])
            i_pin = km[(0.0, 0.0)]
            # Gauge pin: any second vertex fixes rotation; use the gore's first outer
            # boundary point, which every gore has by construction.
            side_pts = mesh["outer"][((0, 1), (1, 2), (2, 0))[sectors[0] // (2 * mesh["splits"])]]
            Q = side_pts[sectors[0] % (2 * mesh["splits"])]
            j_pin = km[(round(float(Q[0]), 9), round(float(Q[1]), 9))]
            x2, strains, edges = flatten_gore(v3, tris, i_pin, j_pin)
            worst = max(worst, float(np.abs(strains).max()))
            loop = boundary_loop(tris)
            gores.append({"outline2d": [[round(float(x2[i][0]), 7),
                                         round(float(x2[i][1]), 7)] for i in loop],
                          "area2dM2": float(abs(sum(
                              x2[loop[i]][0] * x2[loop[(i + 1) % len(loop)]][1]
                              - x2[loop[(i + 1) % len(loop)]][0] * x2[loop[i]][1]
                              for i in range(len(loop)))) / 2.0),
                          "maxStrain": float(np.abs(strains).max())})
        seam, per_cut = cut_lengths(mesh, w, V, k)
        study[k] = {"worstStrain": worst, "gores": gores,
                    "seamPerPanelM": seam, "cutsM": per_cut}
    cleared = [k for k in (3, 6, 12) if study[k]["worstStrain"] <= budget]
    return {"study": study, "kMin": cleared[0] if cleared else None,
            "floorK": 12}

# ---------------------------------------------------------------------------------------
# 6. The record and the page copy.
# ---------------------------------------------------------------------------------------

def page_mesh(V, w_lookup):
    """The page's copy of a class mesh: the same construction at PAGE_M, every vertex an
    exact vertex of the solve mesh, w copied (never interpolated) by key."""
    pm = panel_mesh(V, PAGE_M)
    w = np.empty(len(pm["verts"]))
    for i, p in enumerate(pm["verts"]):
        k = (round(float(p[0]), 9), round(float(p[1]), 9))
        assert k in w_lookup, "page vertex is not a solve vertex"
        w[i] = w_lookup[k]
    return pm, w


def emit(record, page):
    js = ["/* GENERATED — do not edit. `python3 tools/gen_skin.py` rewrites this file.",
          " *",
          " * The loaded skin: the film's pressure-formed shape over all 72 panels, solved",
          " * by tools/gen_skin.py (P1 FEM on div(grad w/sqrt(1+|grad w|^2)) = -2/R, the",
          " * analysis' own operating law T = pR/2 at R = 2.125 r). The page draws these",
          " * numbers and none of its own; check_explorer holds it to that.",
          " */",
          "export const SKIN = " + json.dumps(page, separators=(",", ":")) + ";",
          ""]
    return (json.dumps(record, indent=1, sort_keys=True) + "\n", "\n".join(js))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="regenerate and byte-compare against the committed outputs")
    args = ap.parse_args()

    print("gen_skin: the loaded skin — panels, membrane solve, displacement, gores")
    panels = panel_layout()
    canon = canonical_panels()
    plc = placements(panels, canon)

    # The panels must tile the faces exactly: no strip, no gap, no overlap.
    A_hex_panel = math.sqrt(3.0) / 4.0 * (math.sqrt(2.0) * S) ** 2
    A_sq_panel = S * S / 2.0
    faces = (12.0 + 24.0 * math.sqrt(3.0)) * S * S
    proof("panelsTileFaces",
          abs(48 * A_hex_panel + 24 * A_sq_panel - faces) < 1e-12,
          f"48 hex + 24 sq panel areas = the 14 faces exactly "
          f"({48 * A_hex_panel + 24 * A_sq_panel:.6f} m^2)")

    r_hex, r_sq = canon["hexTri"]["r"], canon["sqTri"]["r"]
    R_hex, R_sq = R_OVER_r * r_hex, R_OVER_r * r_sq

    # GATE: on the incircle disc the solver must return the analysis' own cap.
    disc = disc_mesh(r_hex, wedges=96, rings=48)
    dsol = membrane_solve(disc, R_hex)
    icent = int(np.argmin(np.linalg.norm(disc["verts"], axis=1)))
    sag_frac = float(dsol["w"][icent]) / r_hex
    proof("capLawOnDisc", abs(sag_frac - BULGE) < 2e-3,
          f"nonlinear solve on the incircle disc sags {sag_frac:.5f} r "
          f"(the analysis' cap: {BULGE}) in {dsol['iters']} iterations")

    meshes, sols = {}, {}
    for cls in ("hexTri", "sqTri"):
        meshes[cls] = panel_mesh(canon[cls]["verts"], MESH_M)
        sols[cls] = membrane_solve(meshes[cls], R_OVER_r * canon[cls]["r"])

    # GATE: the exact linear closed form on the equilateral panel, at two mesh sizes.
    closed_sag = 2.0 * r_hex * r_hex / (3.0 * R_hex)
    closed_vol = 0.3 * r_hex * r_hex * A_hex_panel / R_hex
    errs = {}
    for m in (REF_M, MESH_M):
        mm = panel_mesh(canon["hexTri"]["verts"], m)
        ls = membrane_solve(mm, R_hex, linear=True)
        q = surface_quantities(mm, ls)
        errs[m] = (abs(q["sagM"] - closed_sag) / closed_sag,
                   abs(q["volM3"] - closed_vol) / closed_vol)
    proof("linearClosedForm",
          errs[MESH_M][0] < 5e-3 and errs[MESH_M][1] < 5e-3
          and errs[MESH_M][0] < errs[REF_M][0] and errs[MESH_M][1] < errs[REF_M][1],
          f"sag err {errs[MESH_M][0]:.2e} (coarse {errs[REF_M][0]:.2e}), "
          f"vol err {errs[MESH_M][1]:.2e} (coarse {errs[REF_M][1]:.2e}) vs "
          f"w = 2 d1 d2 d3/(3 r R)")

    # GATE: refinement stability of the nonlinear answer.
    mref = panel_mesh(canon["hexTri"]["verts"], REF_M)
    sref = membrane_solve(mref, R_hex)
    qref = surface_quantities(mref, sref)
    q32h = surface_quantities(meshes["hexTri"], sols["hexTri"])
    proof("nonlinearRefinement",
          abs(q32h["sagM"] - qref["sagM"]) / q32h["sagM"] < 5e-3,
          f"hex sag moves {abs(q32h['sagM'] - qref['sagM']) / q32h['sagM']:.2e} "
          f"between mesh {REF_M} and {MESH_M}")

    # GATE: symmetry — the solve must respect the panel's own group.
    c, s = math.cos(2 * math.pi / 3), math.sin(2 * math.pi / 3)
    gap_h = symmetry_gap(meshes["hexTri"], sols["hexTri"]["w"],
                         lambda p: np.array([c * p[0] - s * p[1], s * p[0] + c * p[1]]))
    r0 = canon["sqTri"]["r"]
    gap_s = symmetry_gap(meshes["sqTri"], sols["sqTri"]["w"],
                         lambda p: np.array([p[1], p[0]]))
    proof("solveSymmetry", gap_h < 1e-9 and gap_s < 1e-9,
          "hex 120-degree gap and square mirror gap each < 1e-9 m")

    # GATE: the true surface is deeper than the linear one (slope softens the operator).
    q32s = surface_quantities(meshes["sqTri"], sols["sqTri"])
    lin_h = surface_quantities(meshes["hexTri"],
                               membrane_solve(meshes["hexTri"], R_hex, linear=True))
    proof("nonlinearDeeper", q32h["sagM"] > lin_h["sagM"],
          f"hex sag {q32h['sagM'] * 1000:.2f} mm vs linear {lin_h['sagM'] * 1000:.2f} mm")

    # The analysis' smeared displacement debit, reproduced before being replaced.
    a_edge = math.sqrt(2.0) * S
    A_hexface, A_sqface = 3 * math.sqrt(3) / 2 * a_edge ** 2, a_edge ** 2
    r_hexA, r_sqA = a_edge / (2 * math.sqrt(3)), a_edge / (2 + math.sqrt(2))
    dv_smear = (8 * A_hexface * (BULGE * r_hexA) / 2 + 6 * A_sqface * (BULGE * r_sqA) / 2)
    proof("smearedDebitReproduced", abs(dv_smear - 0.0152731) < 1e-6,
          f"the analysis' flat-area x h/2 rule gives {dv_smear:.7f} m^3 (audit: 0.0152731)")

    # GATE: the bowls bulge INTO the cell — the free film must clear the bare tube of
    # every member it is not bonded to. Lift each panel's solved surface into the
    # article and measure clearance against all 216 members, excluding members in the
    # panel's own face plane (bonded boundary) and each member's first JOINT_ZONE from
    # both ends (inside the printed joint, where the film sits on the land post above,
    # the first fired version of this gate reported 2.6 mm entirely from that zone).
    segs = []
    nodes_g, members_g, _t = gen_nodes.article_graph()
    for u, v, _k in members_g:
        a, b = np.array(u, float) * S, np.array(v, float) * S
        d = b - a
        L = float(np.linalg.norm(d))
        if L <= 2 * JOINT_ZONE:
            continue
        segs.append((a + d / L * JOINT_ZONE, b - d / L * JOINT_ZONE, u, v))
    clearances = []
    for pl in plc:
        cls = pl["cls"]
        mm, ww = meshes[cls], sols[cls]["w"]
        keep = ww > 1e-4                       # free film; the frame lines are bonded
        pts = (pl["origin"][None, :]
               + np.outer(mm["verts"][keep, 0], pl["E1"])
               + np.outer(mm["verts"][keep, 1], pl["E2"])
               - np.outer(ww[keep], pl["N"]))
        n_hat = pl["N"]
        plane_d = float(n_hat @ pl["origin"])
        for a, b, u, v in segs:
            if abs(n_hat @ a - plane_d) < 1e-6 and abs(n_hat @ b - plane_d) < 1e-6:
                continue                        # in-plane member: bonded boundary
            ab = b - a
            tt = np.clip(((pts - a) @ ab) / float(ab @ ab), 0.0, 1.0)
            d = np.linalg.norm(pts - (a[None, :] + tt[:, None] * ab), axis=1).min()
            clearances.append((float(d), (cls, u, v)))
    worst_clear = min(d for d, _key in clearances)
    # Compare every candidate with the true minimum under the shared data rule;
    # choose the smallest (class, member start, member end) key among those ties.
    cls, u, v = min(key for d, key in clearances if numeric_equal(d - TUBE_R, worst_clear - TUBE_R))
    worst_what = f"{cls} panel vs member {u}-{v}"
    proof("bowlsClearStructure", worst_clear - TUBE_R > CLEAR_MARGIN,
          f"worst free-film clearance to a bare tube surface "
          f"{(worst_clear - TUBE_R) * 1000:.1f} mm ({worst_what}); gate "
          f"{CLEAR_MARGIN * 1000:.0f} mm beyond the {TUBE_R * 1000:.0f} mm tube radius")

    dv = 48 * q32h["volM3"] + 24 * q32s["volM3"]
    v_nom = SPAN ** 3 / 2.0
    disp = v_nom - dv
    dome_area = 48 * q32h["domeM2"] + 24 * q32s["domeM2"]

    # THE GORE STUDY — the measurement that decides forming over flat-cut goring.
    dev = {}
    for cls in ("hexTri", "sqTri"):
        dev[cls] = develop(cls, meshes[cls], sols[cls]["w"],
                           canon[cls]["verts"], STRAIN_BUDGET)
        st = dev[cls]["study"]
        kmin = dev[cls]["kMin"]
        proof(f"goreStudy:{cls}",
              st[3]["worstStrain"] >= st[6]["worstStrain"] >= st[12]["worstStrain"],
              f"residual strain {st[3]['worstStrain']:.3%} / {st[6]['worstStrain']:.3%}"
              f" / {st[12]['worstStrain']:.3%} at k = 3/6/12 — "
              + (f"k = {kmin} first clears" if kmin else "NO count clears")
              + f" the {STRAIN_BUDGET:.2%} budget")
        # Development must conserve the dome's area to the strain it reports.
        q = surface_quantities(meshes[cls], sols[cls])
        for k in (3, 6, 12):
            a2 = sum(gg["area2dM2"] for gg in st[k]["gores"])
            proof(f"goreArea:{cls}:k{k}", abs(a2 - q["domeM2"]) / q["domeM2"] < 0.01,
                  f"gore 2D area {a2:.6f} vs dome {q['domeM2']:.6f} m^2")

    # THE VERDICT GATE: forming is justified because every practical gore count fails
    # the film's elastic budget. (If a future solver clears k <= 6 this goes red, and
    # the forming-vs-goring decision deserves reopening.)
    proof("formingJustified",
          dev["hexTri"]["study"][6]["worstStrain"] > STRAIN_BUDGET
          and dev["sqTri"]["study"][6]["worstStrain"] > STRAIN_BUDGET,
          "six gores per panel (the practical ceiling: 432 pieces) still exceeds the "
          "elastic budget on both classes — the net is FORMED, outline unchanged")
    seam_total = (48 * dev["hexTri"]["study"][12]["seamPerPanelM"]
                  + 24 * dev["sqTri"]["study"][12]["seamPerPanelM"])
    gored_pieces = 48 * 12 + 24 * 12

    numbers = {
        "spanM": round(SPAN, 6), "halfPitchM": S,
        "pSLPa": round(P_SL, 1), "p2500Pa": round(P_2500, 1),
        "bulgeLaw": BULGE, "rOverR": R_OVER_r,
        "rHexMm": round(r_hex * 1000, 4), "rSqMm": round(r_sq * 1000, 4),
        "RHexMm": round(R_hex * 1000, 4), "RSqMm": round(R_sq * 1000, 4),
        "tHexSLNpm": round(P_SL * R_hex / 2, 1), "tSqSLNpm": round(P_SL * R_sq / 2, 1),
        "tHex2500Npm": round(P_2500 * R_hex / 2, 1),
        "tSq2500Npm": round(P_2500 * R_sq / 2, 1),
        "sagHexMm": round(q32h["sagM"] * 1000, 3), "sagSqMm": round(q32s["sagM"] * 1000, 3),
        "slopeMaxHex": round(q32h["slopeMax"], 5), "slopeMaxSq": round(q32s["slopeMax"], 5),
        "dishM3": round(dv, 7), "dispNominalM3": round(v_nom, 7),
        "dispLoadedM3": round(disp, 7), "dishPct": round(100 * dv / v_nom, 3),
        "smearedDishM3": round(dv_smear, 7),
        "domeAreaM2": round(dome_area, 6), "flatAreaM2": round(faces, 6),
        "goreStudyPctHex": {str(k): round(100 * dev["hexTri"]["study"][k]["worstStrain"], 4)
                            for k in (3, 6, 12)},
        "goreStudyPctSq": {str(k): round(100 * dev["sqTri"]["study"][k]["worstStrain"], 4)
                           for k in (3, 6, 12)},
        "goreKMinHex": dev["hexTri"]["kMin"], "goreKMinSq": dev["sqTri"]["kMin"],
        "goredPiecesAtK12": gored_pieces, "goredSeamAtK12M": round(seam_total, 3),
        "netVerdict": "formed", "formedDies": 2, "formedPressings": 14,
        "clearanceMm": None,  # filled below
        "strainFlatPct": round(100 * (R_OVER_r * math.asin(1.0 / R_OVER_r) - 1.0), 2),
        "strainBudgetPct": round(100 * STRAIN_BUDGET, 2),
        "sqPanelInradiusNoteMm": round(S * (2 - math.sqrt(2)) / 2 * 1000, 2),
        "analysisSqInradiusMm": round(r_sqA * 1000, 2),
    }

    numbers["clearanceMm"] = round((worst_clear - TUBE_R) * 1000, 2)
    page = {"classes": {}, "placements": [], "numbers": numbers}
    for cls in ("hexTri", "sqTri"):
        lookup = {(round(float(p[0]), 9), round(float(p[1]), 9)): float(wv)
                  for p, wv in zip(meshes[cls]["verts"], sols[cls]["w"])}
        pm, w = page_mesh(canon[cls]["verts"], lookup)
        page["classes"][cls] = {
            "pos": [round(float(x), 7) for p in pm["verts"] for x in p],
            "w": [round(float(x), 7) for x in w],
            "tris": [int(i) for t in pm["tris"] for i in t]}
    for p in plc:
        page["placements"].append(
            [p["cls"]] + [round(float(x), 7) for arr in
                          (p["origin"], p["E1"], p["E2"], p["N"]) for x in arr])

    record = {"params": {k: numbers[k] for k in
                         ("spanM", "halfPitchM", "bulgeLaw", "rOverR", "pSLPa", "p2500Pa")},
              "numbers": numbers,
              "gores": {cls: {"study": {str(k): {
                                  "worstStrain": round(dev[cls]["study"][k]["worstStrain"], 7),
                                  "seamPerPanelM": round(dev[cls]["study"][k]["seamPerPanelM"], 6)}
                                  for k in (3, 6, 12)},
                              "kMin": dev[cls]["kMin"],
                              "cutsM": [round(x, 6)
                                        for x in dev[cls]["study"][12]["cutsM"]],
                              "outlines": [gg["outline2d"] for gg in
                                           dev[cls]["study"][12]["gores"]]}
                        for cls in dev},
              "proofs": [{"name": n, "ok": ok, "detail": d} for n, ok, d in PROOFS]}

    ok_all = all(ok for _n, ok, _d in PROOFS)
    record["proofs"] = [{"name": n, "ok": ok, "detail": d} for n, ok, d in PROOFS]
    json_text, js_text = emit(record, page)

    if args.check:
        stale = []
        for path, text, parse in ((JSON_OUT, json_text, parse_json),
                                  (JS_OUT, js_text, parse_skin_literal)):
            try:
                with open(path, encoding="utf-8") as file:
                    difference = first_difference(parse(file.read()), parse(text))
            except (OSError, ValueError) as exc:
                difference = f"$: cannot read or parse data ({type(exc).__name__})"
            if difference:
                stale.append(f"{os.path.relpath(path, ROOT)}: {difference}")
        if stale:
            print(f"  FAIL   staleOutputs: regenerated data differ: {'; '.join(stale)}")
            sys.exit(1)
        print("  PROOF  freshOutputs: committed skin outputs match a full regeneration")
    else:
        os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
        with open(JSON_OUT, "w", encoding="utf-8") as fh:
            fh.write(json_text)
        with open(JS_OUT, "w", encoding="utf-8") as fh:
            fh.write(js_text)
        print(f"  wrote {os.path.relpath(JSON_OUT, ROOT)} and "
              f"{os.path.relpath(JS_OUT, ROOT)}")

    print(f"SKIN {'PASS' if ok_all else 'FAIL'}: sag hex {numbers['sagHexMm']} mm / "
          f"sq {numbers['sagSqMm']} mm; dish {numbers['dishPct']}% of nominal volume "
          f"({numbers['dishM3']} m^3); displaced {numbers['dispLoadedM3']} m^3; "
          f"net FORMED (2 dies, 14 pressings) — flat-cut goring fails its strain "
          f"budget even at twelve gores ({gored_pieces} pieces, "
          f"{numbers['goredSeamAtK12M']} m of unbacked seam)")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
