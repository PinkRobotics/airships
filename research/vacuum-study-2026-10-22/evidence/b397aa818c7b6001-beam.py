"""Independent 3D frame / conservative film-pressure model for MAINLINE-041.

No peer calculation program is imported. All quantities are QUESTIONABLE.
Initial member curves are stress-free chains of circular-section corotational beams.
"""
import os
import sys

for _key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_key] = "1"
sys.dont_write_bytecode = True
# Explicit installed scientific-library location; -I excludes implicit user startup.
sys.path.insert(0, "unpublished-local-ref:e2218733e161c504")

import json
import math
from pathlib import Path
import time
import numpy as np
import scipy
from scipy.spatial import ConvexHull
from scipy.sparse import coo_matrix, csc_matrix, bmat
from scipy.sparse.linalg import splu, LinearOperator, eigsh

ROOT = Path(__file__).resolve().parent
R = 10.0
P = 95460.8379139
E = 410e9
NU = 0.14
SELECTED = json.loads((ROOT / "intake/022d/RESULTS.json").read_text())["best_equilateral_screened"]
RO = SELECTED["r_o_m"]
TW = SELECTED["wall_m"]
RHO = 3100.0
AREA = math.pi * (RO**2 - (RO - TW)**2)
INERTIA = math.pi / 4 * (RO**4 - (RO - TW)**4)
EA, EI = E * AREA, E * INERTIA
GJ = E / (2 * (1 + NU)) * 2 * INERTIA
PARAMS = np.array([EA, EI, GJ])

CASE = {"r_o_m":RO,"wall_m":TW,"nominal_s_m":SELECTED["s_m"],
        "film_mass_kg":SELECTED["mass_kg"]["film"],"systems_kg":100.,
        "source_sag_debit_kg":SELECTED["mass_kg"]["sag_lift_loss"],
        "source_payload_kg":SELECTED["mass_kg"]["reserve"],
        "joint_rule":"041 explicit end moments; old metadata allowance not scored"}

def configure(frequency):
    """One explicit section per fresh process; call before importing symbols."""
    global CASE, RO, TW, AREA, INERTIA, EA, EI, GJ, PARAMS
    CASE = dict(CASE)
    RO, TW = CASE["r_o_m"], CASE["wall_m"]
    AREA = math.pi * (RO**2 - (RO-TW)**2)
    INERTIA = math.pi/4 * (RO**4 - (RO-TW)**4)
    EA, EI, GJ = E*AREA, E*INERTIA, E*INERTIA/(1+NU)
    PARAMS = np.array([EA, EI, GJ])


def skew(x):
    result = np.zeros(x.shape[:-1] + (3, 3))
    result[..., 0, 1], result[..., 0, 2] = -x[..., 2], x[..., 1]
    result[..., 1, 0], result[..., 1, 2] = x[..., 2], -x[..., 0]
    result[..., 2, 0], result[..., 2, 1] = -x[..., 1], x[..., 0]
    return result


def geodesic(frequency):
    phi = (1 + math.sqrt(5)) / 2
    v = np.array([(0, a, b * phi) for a in (-1, 1) for b in (-1, 1)]
                 + [(a, b * phi, 0) for a in (-1, 1) for b in (-1, 1)]
                 + [(b * phi, 0, a) for a in (-1, 1) for b in (-1, 1)], float)
    v /= np.linalg.norm(v, axis=1)[:, None]
    base_faces = ConvexHull(v).simplices
    points, triangles, registry = [], [], {}

    def vertex(x):
        x = x / np.linalg.norm(x)
        key = tuple(np.round(x, 12))
        if key not in registry:
            registry[key] = len(points)
            points.append(R * x)
        return registry[key]

    f = frequency
    for face in base_faces:
        a, b, c = v[face]
        local = {}
        for i in range(f + 1):
            for j in range(f + 1 - i):
                local[i, j] = vertex((f - i - j) * a + i * b + j * c)
        for i in range(f):
            for j in range(f - i):
                triangles.append([local[i, j], local[i + 1, j], local[i, j + 1]])
                if i + j < f - 1:
                    triangles.append([local[i + 1, j], local[i + 1, j + 1], local[i, j + 1]])
    points, triangles = np.array(points), np.array(triangles, dtype=np.int32)
    for tri in triangles:
        a, b, c = points[tri]
        if np.dot(np.cross(b - a, c - a), a + b + c) < 0:
            tri[1], tri[2] = tri[2], tri[1]
    edges = sorted({tuple(sorted((int(a), int(b)))) for tri in triangles
                    for a, b in zip(tri, np.roll(tri, -1))})
    assert len(points) == 10 * f * f + 2
    assert len(triangles) == 20 * f * f and len(edges) == 30 * f * f
    return points, triangles, np.array(edges, dtype=np.int32)


class Frame:
    def __init__(self, frequency=6, segments=3, pinned=False, reference=None, rise_factor=1.):
        self.frequency, self.segments, self.pinned = frequency, segments, pinned
        self.rise_factor = rise_factor
        self.true_member_lengths = []
        main, self.faces, self.edges = geodesic(frequency)
        self.nmain = len(main)
        nodes = list(main)
        chains = []
        for a, b in self.edges:
            va, vb = main[a] / R, main[b] / R
            angle = math.acos(np.clip(va @ vb, -1, 1))
            chord = main[b]-main[a]
            chord_length = np.linalg.norm(chord)
            normal = (main[a]+main[b])/np.linalg.norm(main[a]+main[b])
            sagitta = R*(1-math.cos(angle/2))
            h = rise_factor*sagitta
            radius = chord_length**2/(8*h)+h/2
            half_angle = 2*math.atan2(2*h,chord_length)
            center = (main[a]+main[b])/2+(h-radius)*normal
            self.true_member_lengths.append(2*radius*half_angle)
            ids = [int(a)]
            for k in range(1, segments):
                s = k / segments
                x = R * (math.sin((1 - s) * angle) * va + math.sin(s * angle) * vb) / math.sin(angle)
                if rise_factor != 1.:
                    theta = (2*s-1)*half_angle
                    x = center+radius*(math.cos(theta)*normal+math.sin(theta)*chord/chord_length)
                ids.append(len(nodes))
                nodes.append(x)
            ids.append(int(b))
            chains.append(ids)
        self.chains = np.array(chains, dtype=np.int32)
        self.x = np.array(nodes) if reference is None else np.asarray(reference).copy()
        assert self.x.shape == (len(nodes), 3)
        self.nn = len(nodes)
        self.beams = np.concatenate([self.chains[:, k:k + 2] for k in range(segments)])
        self.member_of_beam = np.tile(np.arange(len(chains)), segments)
        edge_lookup = {tuple(edge): i for i, edge in enumerate(self.edges)}
        boundary = []
        for face in self.faces:
            ids = []
            for a, b in zip(face, np.roll(face, -1)):
                chain = self.chains[edge_lookup[tuple(sorted((a, b)))]]
                if chain[0] != a:
                    chain = chain[::-1]
                ids.extend(chain[:-1])
            boundary.append(ids)
        self.boundary = np.array(boundary, dtype=np.int32)
        self.nrot = self.nn if not pinned else self.nn - self.nmain + 2 * len(chains)
        self.ndof = 3 * self.nn + 3 * self.nrot
        rdofs = []
        for member, (a, b) in zip(self.member_of_beam, self.beams):
            pair = []
            for node in (a, b):
                if not pinned:
                    pair.append(int(node))
                elif node >= self.nmain:
                    pair.append(int(node) - self.nmain)
                else:
                    side = 0 if node == self.chains[member, 0] else 1
                    pair.append(self.nn - self.nmain + 2 * int(member) + side)
            rdofs.append(pair)
        self.rotation_nodes = np.array(rdofs)
        parts = []
        for end in (0, 1):
            parts += [3 * self.beams[:, end, None] + np.arange(3),
                      3 * self.nn + 3 * self.rotation_nodes[:, end, None] + np.arange(3)]
        self.dofs = np.concatenate(parts, axis=1).astype(np.int32)
        self.krows = np.repeat(self.dofs, 12, axis=1).ravel()
        self.kcols = np.tile(self.dofs, (1, 12)).ravel()
        self.xpair = self.x[self.beams]
        chord = self.xpair[:, 1] - self.xpair[:, 0]
        self.length = np.linalg.norm(chord, axis=1)
        ex = chord / self.length[:, None]
        helper = np.tile([0., 0., 1.], (len(ex), 1))
        helper[np.abs(ex[:, 2]) > 0.8] = [0., 1., 0.]
        ey = np.cross(helper, ex)
        ey /= np.linalg.norm(ey, axis=1)[:, None]
        ez = np.cross(ex, ey)
        self.q0 = np.stack([ex, ey, ez], axis=2)
        self.pressure_dofs = (3 * self.boundary[..., None] + np.arange(3)).reshape(len(self.faces), -1)
        n = self.pressure_dofs.shape[1]
        self.prows = np.repeat(self.pressure_dofs, n, axis=1).ravel()
        self.pcols = np.tile(self.pressure_dofs, (1, n)).ravel()
        self._torch_data = None

    def assemble(self, local):
        return coo_matrix((local.ravel(), (self.krows, self.kcols)),
                          shape=(self.ndof, self.ndof)).tocsc()

    def linear_stiffness(self):
        n, lengths = len(self.beams), self.length
        k = np.zeros((n, 12, 12))

        def add(indices, matrix):
            for a, ia in enumerate(indices):
                for b, ib in enumerate(indices):
                    k[:, ia, ib] += matrix[:, a, b]

        pair = np.array([[1, -1], [-1, 1]])
        add([0, 6], EA / lengths[:, None, None] * pair)
        add([3, 9], GJ / lengths[:, None, None] * pair)
        for indices, sign in [([1, 5, 7, 11], 1), ([2, 4, 8, 10], -1)]:
            for e, L in enumerate(lengths):
                mat = EI / L**3 * np.array([
                    [12, 6 * L, -12, 6 * L],
                    [6 * L, 4 * L**2, -6 * L, 2 * L**2],
                    [-12, -6 * L, 12, -6 * L],
                    [6 * L, 2 * L**2, -6 * L, 4 * L**2]])
                signs = np.array([1, sign, 1, sign])
                k[e][np.ix_(indices, indices)] += mat * signs[:, None] * signs[None, :]
        T = np.zeros_like(k)
        for off in (0, 3, 6, 9):
            T[:, off:off + 3, off:off + 3] = self.q0.transpose(0, 2, 1)
        self.local_linear = k
        self.transforms = T
        global_k = np.einsum("eji,ejk,ekl->eil", T, k, T)
        return self.assemble(global_k)

    def pressure(self, q=None, tangent=True):
        """V of closed centroid-fan film; pV is conservative external potential.

        Centroid = mean boundary points. In an equal triangular cell this transfers
        one-third of its pressure resultant to each edge, distributed along it.
        """
        x = self.x if q is None else self.x + q[:3 * self.nn].reshape(-1, 3)
        b = x[self.boundary]
        n = b.shape[1]
        c = b.mean(axis=1)
        nxt, prev = np.roll(b, -1, axis=1), np.roll(b, 1, axis=1)
        S = np.cross(b, nxt).sum(axis=1)
        volume = np.einsum("fi,fi->", c, S) / 6
        diff = nxt - prev
        local_g = S[:, None, :] / (6 * n) + np.cross(diff, c[:, None, :]) / 6
        grad = np.bincount(self.pressure_dofs.ravel(), weights=local_g.ravel(), minlength=self.ndof)
        if not tangent:
            return volume, grad, None
        sd, sc = skew(diff), skew(c)
        h = (sd[:, :, None] - sd[:, None, :]) / (6 * n)
        for i in range(n):
            h[:, i, (i + 1) % n] -= sc / 6
            h[:, i, (i - 1) % n] += sc / 6
        # axes face, boundary row, boundary col, xyz row, xyz col.
        h = h.transpose(0, 1, 3, 2, 4).reshape(len(self.faces), 3 * n, 3 * n)
        H = coo_matrix((h.ravel(), (self.prows, self.pcols)),
                       shape=(self.ndof, self.ndof)).tocsc()
        return volume, grad, H

    def rigid_basis(self):
        Z = np.zeros((self.ndof, 6))
        for a in range(3):
            Z[a:3 * self.nn:3, a] = 1
            Z[:3 * self.nn, 3 + a] = np.cross(np.eye(3)[a], self.x).ravel()
            Z[3 * self.nn + a::3, 3 + a] = 1
        return np.linalg.qr(Z)[0]

    def strains_forces(self, q):
        local_q = np.einsum("eij,ej->ei", self.transforms, q[self.dofs])
        force = np.einsum("eij,ej->ei", self.local_linear, local_q)
        return force, -EA / self.length * (local_q[:, 6] - local_q[:, 0])

    def nonlinear(self, q, tangent=True, batch=96):
        import torch
        from corot import energy, gradient, hessian
        if self._torch_data is None:
            torch.set_num_threads(1)
            self._torch_data = (
                torch.tensor(self.xpair, dtype=torch.float64),
                torch.tensor(self.q0, dtype=torch.float64),
                torch.tensor(self.length, dtype=torch.float64),
                torch.tensor(PARAMS, dtype=torch.float64))
        xp, q0, length, params = self._torch_data
        ql = torch.tensor(q[self.dofs], dtype=torch.float64)
        forces, matrices, energies = [], [], []
        for start in range(0, len(self.beams), batch):
            stop = min(start + batch, len(self.beams))
            args = (ql[start:stop], xp[start:stop], q0[start:stop], length[start:stop], params)
            energies.append(energy(*args).detach().numpy())
            forces.append(gradient(*args).detach().numpy())
            if tangent:
                matrices.append(hessian(*args).detach().numpy())
        f = np.bincount(self.dofs.ravel(), weights=np.concatenate(forces).ravel(), minlength=self.ndof)
        H = self.assemble(np.concatenate(matrices)) if tangent else None
        return float(np.concatenate(energies).sum()), f, H

    def metadata(self):
        angles = np.arccos(np.clip(np.einsum("ei,ei->e", self.x[self.edges[:, 0]],
                                                  self.x[self.edges[:, 1]]) / R**2, -1, 1))
        arcs = R * angles
        total_length = float(np.sum(self.true_member_lengths))
        tube_mass = total_length * AREA * RHO
        film, systems = CASE["film_mass_kg"], CASE["systems_kg"]
        nodes = .02*self.nmain
        joints = .05*(tube_mass if CASE["joint_rule"]=="0.05*tubes" else tube_mass+film+nodes)
        mass = tube_mass+joints+nodes+film+systems
        lift = 4889.442150189999
        continuum = 4*math.sqrt(1.5)*E*math.sqrt(AREA*INERTIA)/(CASE["nominal_s_m"]*R**2*P)
        halfwave = math.pi*math.sqrt(math.sqrt(1.125)*math.sqrt(INERTIA/AREA)*R)
        return {
            "case": CASE, "rise_factor": self.rise_factor,
            "continuum_perfect_lambda_nominal_s": continuum,
            "continuum_perfect_lambda_actual_mean_arc": continuum*CASE["nominal_s_m"]/float(arcs.mean()),
            "continuum_halfwave_m": halfwave,
            "halfwave_over_nominal_s": halfwave/CASE["nominal_s_m"],
            "halfwave_over_mean_arc": halfwave/float(arcs.mean()),
            "gross_inherited_lift_kg": lift,
            "payload_before_sag_kg": lift-mass,
            "payload_after_source_sag_kg": lift-mass-CASE["source_sag_debit_kg"],
            "headroom_after_source_sag_and_source_payload_kg": lift-mass-CASE["source_sag_debit_kg"]-CASE["source_payload_kg"],
            "frequency": self.frequency, "segments_per_arc": self.segments,
            "main_nodes": self.nmain, "members": len(self.edges), "film_cells": len(self.faces),
            "beam_nodes": self.nn, "beam_elements": len(self.beams), "rotational_nodes": self.nrot,
            "DOF": self.ndof, "joint_type": "ball_pinned" if self.pinned else "rigid",
            "arc_length_m": {"min": float(arcs.min()), "mean": float(arcs.mean()), "max": float(arcs.max())},
            "arc_total_length_m": total_length, "straight_subelement_total_length_m": float(self.length.sum()),
            "tube_mass_kg": tube_mass, "joints_5pct_kg": joints,
            "node_mass_kg": 0.02 * self.nmain, "film_mass_inherited_kg": film,
            "systems_inherited_kg": systems,
            "total_mass_with_inherited_allowances_kg": mass,
            "radius_m": R, "E_Pa": E, "nu": NU, "r_o_m": RO, "wall_m": TW,
            "A_m2": AREA, "I_m4": INERTIA, "GJ_Nm2": GJ,
            "tag": "QUESTIONABLE", "certification": "none",
        }


class GaugeInverse:
    """Sparse constrained solve with six orthogonality conditions, no support pins."""
    def __init__(self, K, Q):
        self.n, self.Q = K.shape[0], Q
        self.scale = float(np.median(np.abs(K.diagonal())))
        constraint_scale = math.sqrt(max(self.scale, 1.))
        C = csc_matrix(Q * constraint_scale)
        self.lu = splu(bmat([[K, C], [C.T, None]], format="csc"), permc_spec="COLAMD")

    def projected(self, f):
        b = np.zeros(self.n + self.Q.shape[1])
        b[:self.n] = f
        return self.lu.solve(b)[:self.n]

    def positive_inverse(self, f):
        return self.projected(f) + self.Q @ (self.Q.T @ f) / self.scale


def eigen_buckling(K, destabilizing, Q, number=8):
    inv = GaugeInverse(K, Q)

    def project(x):
        return x - Q @ (Q.T @ x)

    M = LinearOperator(K.shape, matvec=lambda x: K @ x + inv.scale * Q @ (Q.T @ x))
    B = LinearOperator(K.shape, matvec=lambda x: project(destabilizing @ project(x)))
    Mi = LinearOperator(K.shape, matvec=inv.positive_inverse)
    v0 = project(np.random.default_rng(26020).normal(size=K.shape[0]))
    mu, modes = eigsh(B, k=number, M=M, Minv=Mi, which="LA", tol=2e-8,
                     maxiter=2500, ncv=max(36, 3 * number), v0=v0)
    order = np.argsort(1 / mu)
    values, modes = 1 / mu[order], modes[:, order]
    residuals = []
    for val, v in zip(values, modes.T):
        a, b = project(K @ v), val * project(destabilizing @ v)
        residuals.append(float(np.linalg.norm(a - b) / max(np.linalg.norm(a), np.linalg.norm(b), 1e-30)))
    return values, modes, residuals
