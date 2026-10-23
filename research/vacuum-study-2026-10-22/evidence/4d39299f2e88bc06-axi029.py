#!/usr/bin/env python3
"""Own axisymmetric 8-node solid model for CHECK MAINLINE-029 (seat ref-55cff924be25afe6f9dd).

Written from the card's stated model, not from the owner's code: total-Lagrangian St. Venant-Kirchhoff (PK2 linear in Green
strain), layered sphere or hemisphere, faces isotropic, core orthotropic in the local (tangent, normal, hoop) frame of the
reference geometry, external follower pressure on the outer surface, stress-free Gaussian inward offset of every layer.
Analyses: linear buckling (stress stiffness, with or without the pressure load stiffness) and nonlinear static with
Crisfield cylindrical arc-length continuation, which follows the path through limit points.
"""
import math

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

GP3 = np.array([-math.sqrt(0.6), 0.0, math.sqrt(0.6)])
GW3 = np.array([5 / 9, 8 / 9, 5 / 9])
CORNERS = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
MIDS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def q8(xi, eta):
    """Serendipity Q8: N, dN/dxi, dN/deta (node order: 4 corners ccw from (-1,-1), then mids (0,-1),(1,0),(0,1),(-1,0))."""
    N = np.zeros(8); dx = np.zeros(8); de = np.zeros(8)
    for a, (xa, ea) in enumerate(CORNERS):
        N[a] = 0.25 * (1 + xi * xa) * (1 + eta * ea) * (xi * xa + eta * ea - 1)
        dx[a] = 0.25 * xa * (1 + eta * ea) * (2 * xi * xa + eta * ea)
        de[a] = 0.25 * ea * (1 + xi * xa) * (xi * xa + 2 * eta * ea)
    for k, (xa, ea) in enumerate(MIDS):
        a = 4 + k
        if xa == 0:
            N[a] = 0.5 * (1 - xi ** 2) * (1 + eta * ea)
            dx[a] = -xi * (1 + eta * ea)
            de[a] = 0.5 * ea * (1 - xi ** 2)
        else:
            N[a] = 0.5 * (1 + xi * xa) * (1 - eta ** 2)
            dx[a] = 0.5 * xa * (1 - eta ** 2)
            de[a] = -eta * (1 + xi * xa)
    return N, dx, de


def edge3(xi):
    N = np.array([0.5 * xi * (xi - 1), 1 - xi ** 2, 0.5 * xi * (xi + 1)])
    d = np.array([xi - 0.5, -2 * xi, xi + 0.5])
    return N, d


def _det_sign(lu):
    """Sign of det of a SuperLU factorisation: sign(prod diag U) times the parities of the row and column permutations."""
    d = lu.U.diagonal()
    s = -1.0 if (np.count_nonzero(d < 0) % 2) else 1.0
    for perm in (lu.perm_r, lu.perm_c):
        p = np.asarray(perm).copy()
        seen = np.zeros(len(p), dtype=bool)
        parity = 0
        for i in range(len(p)):
            if not seen[i]:
                j = i; L = 0
                while not seen[j]:
                    seen[j] = True; j = p[j]; L += 1
                parity += L - 1
        if parity % 2:
            s = -s
    return s


class Model:
    """layers: list of dicts {t, n, mat} from inner to outer; mat: ('iso', E, nu) or ('core', En, Gtn, Ein, Gin)."""

    def __init__(self, R_outer, layers, phi_end, ntheta, grading=1.0, dimple=None, clamp_equator=False,
                 fix_south_inner_z=False):
        self.Ro = R_outer
        self.layers = layers
        T = sum(L["t"] for L in layers)
        self.T = T
        # meridional corner stations phi_i, graded towards the north pole: phi = phi_end * s**grading
        s = np.linspace(0, 1, ntheta + 1)
        phc = phi_end * s ** grading
        # node stations along the meridian (corners and mids)
        phn = np.empty(2 * ntheta + 1)
        phn[0::2] = phc
        phn[1::2] = 0.5 * (phc[:-1] + phc[1:])
        # radial stations (corners and mids) from inner to outer
        rho_c = [R_outer - T]
        mat_of_row = []
        for L in layers:
            for k in range(L["n"]):
                rho_c.append(rho_c[-1] + L["t"] / L["n"])
                mat_of_row.append(L["mat"])
        rho_c = np.array(rho_c)
        nt = len(rho_c) - 1
        rhn = np.empty(2 * nt + 1)
        rhn[0::2] = rho_c
        rhn[1::2] = 0.5 * (rho_c[:-1] + rho_c[1:])
        self.nt, self.nth = nt, ntheta
        # imperfection: stress-free inward radial offset w0(phi) of every layer, Gaussian in arc length R_outer*phi
        if dimple is not None:
            amp, width = dimple
            w0 = amp * np.exp(-((R_outer * phn) / width) ** 2)
        else:
            w0 = np.zeros_like(phn)
        # node numbering on a (2nth+1) x (2nt+1) grid, skipping element centres (odd, odd)
        nid = -np.ones((2 * ntheta + 1, 2 * nt + 1), dtype=int)
        X = []
        for i in range(2 * ntheta + 1):
            for j in range(2 * nt + 1):
                if i % 2 == 1 and j % 2 == 1:
                    continue
                nid[i, j] = len(X)
                rr = rhn[j] - w0[i]
                X.append((rr * math.sin(phn[i]), rr * math.cos(phn[i])))
        self.X = np.array(X)
        self.X[np.abs(self.X[:, 0]) < 1e-12 * R_outer, 0] = 0.0
        self.nid = nid
        self.nn = len(X)
        # elements: xi along the meridian (increasing phi), eta through thickness (increasing radius)
        conn, emat = [], []
        for i in range(ntheta):
            for j in range(nt):
                I, J = 2 * i, 2 * j
                # corners ccw in (xi, eta): (-1,-1)=(I,J), (1,-1)=(I+2,J), (1,1)=(I+2,J+2), (-1,1)=(I,J+2)
                c = [nid[I, J], nid[I + 2, J], nid[I + 2, J + 2], nid[I, J + 2],
                     nid[I + 1, J], nid[I + 2, J + 1], nid[I + 1, J + 2], nid[I, J + 1]]
                conn.append(c)
                emat.append(mat_of_row[j])
        self.conn = np.array(conn)
        self.emat = emat
        self.ne = len(conn)
        # outer surface edges (eta = +1): nodes 3, 6, 2 in local order -> along xi from -1 to 1: (-1,1),(0,1),(1,1)
        self.edges = np.array([[nid[2 * i, 2 * nt], nid[2 * i + 1, 2 * nt], nid[2 * i + 2, 2 * nt]] for i in range(ntheta)])
        # boundary conditions
        fixed = []
        for n in range(self.nn):
            if abs(self.X[n, 0]) == 0.0:
                fixed.append(2 * n)                       # u_r = 0 on the axis
        if clamp_equator:
            for j in range(2 * nt + 1):
                n = nid[2 * ntheta, j]
                if n >= 0:
                    fixed += [2 * n, 2 * n + 1]
        if fix_south_inner_z:
            fixed.append(2 * nid[2 * ntheta, 0] + 1)
        self.fixed = np.unique(np.array(fixed, dtype=int))
        self.ndof = 2 * self.nn
        self.free = np.setdiff1d(np.arange(self.ndof), self.fixed)
        self._precompute()

    def _cmat(self, mat, alpha):
        """4x4 constitutive matrix for Voigt [rr, zz, tt(hoop), rz(engineering)] in global axes."""
        if mat[0] == "iso":
            E, nu = mat[1], mat[2]
            lam = E * nu / ((1 + nu) * (1 - 2 * nu))
            mu = E / (2 * (1 + nu))
            C = np.array([[lam + 2 * mu, lam, lam, 0], [lam, lam + 2 * mu, lam, 0], [lam, lam, lam + 2 * mu, 0],
                          [0, 0, 0, mu]])
            return np.broadcast_to(C, alpha.shape + (4, 4)).copy()
        En, Gtn, Ein, Gin = mat[1], mat[2], mat[3], mat[4]
        # local (t, n, hoop) with zero Poisson coupling: diag(Ein, En, Ein, Gtn); rotate (t, n) -> (r, z)
        Cl = np.diag([Ein, En, Ein, Gtn])
        out = np.empty(alpha.shape + (4, 4))
        for k, a in np.ndenumerate(alpha):
            c, s = math.cos(a), math.sin(a)
            # strain transformation global -> local (engineering shear): eps_l = Te eps_g
            Te = np.array([[c * c, s * s, 0, c * s], [s * s, c * c, 0, -c * s], [0, 0, 1, 0],
                           [-2 * c * s, 2 * c * s, 0, c * c - s * s]])
            out[k] = Te.T @ Cl @ Te
        return out

    def _precompute(self):
        ne = self.ne
        Xe = self.X[self.conn]                                      # (ne, 8, 2)
        self.gp = []
        for i, xi in enumerate(GP3):
            for j, eta in enumerate(GP3):
                N, dx, de = q8(xi, eta)
                J11 = Xe[:, :, 0] @ dx; J12 = Xe[:, :, 0] @ de       # dr/dxi, dr/deta
                J21 = Xe[:, :, 1] @ dx; J22 = Xe[:, :, 1] @ de       # dz/dxi, dz/deta
                det = J11 * J22 - J12 * J21
                # dN/dr = (J22 dN/dxi - J21 dN/deta)/det ; dN/dz = (-J12 dN/dxi + J11 dN/deta)/det
                dNr = (np.outer(J22, dx) - np.outer(J21, de)) / det[:, None]
                dNz = (-np.outer(J12, dx) + np.outer(J11, de)) / det[:, None]
                r = Xe[:, :, 0] @ N
                w = GW3[i] * GW3[j] * det * 2 * math.pi * r
                alpha = np.arctan2(J21, J11)                          # meridional tangent angle (reference)
                C = np.empty((ne, 4, 4))
                for mkey in set(map(repr, self.emat)):
                    idx = np.array([k for k in range(ne) if repr(self.emat[k]) == mkey])
                    C[idx] = self._cmat(self.emat[idx[0]], alpha[idx])
                self.gp.append({"N": N, "dNr": dNr, "dNz": dNz, "r": r, "w": w, "C": C})
        dofs = np.empty((ne, 16), dtype=int)
        dofs[:, 0::2] = 2 * self.conn
        dofs[:, 1::2] = 2 * self.conn + 1
        self.edofs = dofs
        self.rows = np.repeat(dofs, 16, axis=1).ravel()
        self.cols = np.tile(dofs, (1, 16)).ravel()
        ed = np.empty((len(self.edges), 6), dtype=int)
        ed[:, 0::2] = 2 * self.edges
        ed[:, 1::2] = 2 * self.edges + 1
        self.edge_dofs = ed

    def _kin(self, g, ue):
        """Displacement-gradient terms at one Gauss point for all elements. ue: (ne, 8, 2)."""
        H11 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 0]); H12 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 0])
        H21 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 1]); H22 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 1])
        ur = ue[:, :, 0] @ g["N"]
        hr = ur / g["r"]
        E = np.stack([H11 + 0.5 * (H11 ** 2 + H21 ** 2), H22 + 0.5 * (H12 ** 2 + H22 ** 2), hr + 0.5 * hr ** 2,
                      H12 + H21 + H11 * H12 + H21 * H22], axis=1)
        ne = ue.shape[0]
        B = np.zeros((ne, 4, 16))
        Nr, Nz, N = g["dNr"], g["dNz"], g["N"]
        B[:, 0, 0::2] = (1 + H11)[:, None] * Nr; B[:, 0, 1::2] = H21[:, None] * Nr
        B[:, 1, 0::2] = H12[:, None] * Nz;       B[:, 1, 1::2] = (1 + H22)[:, None] * Nz
        B[:, 2, 0::2] = ((1 + hr) / g["r"])[:, None] * N[None, :]
        B[:, 3, 0::2] = (1 + H11)[:, None] * Nz + H12[:, None] * Nr
        B[:, 3, 1::2] = H21[:, None] * Nz + (1 + H22)[:, None] * Nr
        return E, B

    def internal(self, u, tangent=True, linear=False, stress_from=None):
        """f_int and tangent stiffness. linear=True: small-strain stiffness only. stress_from: (u1) gives geometric stiffness
        of the linear stress state S(u1) (for buckling)."""
        ue = u[self.edofs].reshape(self.ne, 8, 2)
        f = np.zeros(self.ndof)
        Kv = np.zeros((self.ne, 16, 16)) if tangent else None
        for g in self.gp:
            if linear or stress_from is not None:
                E, B = self._kin(g, np.zeros_like(ue))
                if stress_from is not None:
                    u1 = stress_from[self.edofs].reshape(self.ne, 8, 2)
                    _, B0 = self._kin(g, np.zeros_like(u1))
                    Elin = np.einsum("eij,ej->ei", B0, u1.reshape(self.ne, 16))
                    S = np.einsum("eij,ej->ei", g["C"], Elin)
                    Kv += self._geo(g, S) * g["w"][:, None, None]
                    continue
                S = np.einsum("eij,ej->ei", g["C"], np.einsum("eij,ej->ei", B, ue.reshape(self.ne, 16)))
            else:
                E, B = self._kin(g, ue)
                S = np.einsum("eij,ej->ei", g["C"], E)
            fe = np.einsum("eki,ek->ei", B, S) * g["w"][:, None]
            np.add.at(f, self.edofs, fe)
            if tangent:
                Km = np.einsum("eki,ekl,elj->eij", B, g["C"], B)
                if not linear:
                    Km = Km + self._geo(g, S)
                Kv += Km * g["w"][:, None, None]
        K = sp.coo_matrix((Kv.ravel(), (self.rows, self.cols)), shape=(self.ndof, self.ndof)).tocsr() if tangent else None
        return f, K

    def _geo(self, g, S):
        Nr, Nz, N = g["dNr"], g["dNz"], g["N"]
        a = (S[:, 0, None, None] * Nr[:, :, None] * Nr[:, None, :] + S[:, 1, None, None] * Nz[:, :, None] * Nz[:, None, :]
             + S[:, 3, None, None] * (Nr[:, :, None] * Nz[:, None, :] + Nz[:, :, None] * Nr[:, None, :]))
        hoop = (S[:, 2] / g["r"] ** 2)[:, None, None] * np.outer(N, N)[None]
        ne = S.shape[0]
        G = np.zeros((ne, 16, 16))
        G[:, 0::2, 0::2] = a + hoop
        G[:, 1::2, 1::2] = a
        return G

    def pressure(self, u, stiffness=True):
        """Follower load per unit external pressure on the outer surface, and dF/du (load stiffness, to be subtracted)."""
        x = self.X + u.reshape(-1, 2)
        f = np.zeros(self.ndof)
        rows, cols, vals = [], [], []
        xe = x[self.edges]                                         # (nedge, 3, 2)
        for xi, wq in zip(GP3, GW3):
            N, d = edge3(xi)
            r = xe[:, :, 0] @ N; rp = xe[:, :, 0] @ d; zp = xe[:, :, 1] @ d
            c = 2 * math.pi * wq
            fr = c * (N[None, :] * (r * zp)[:, None]); fz = c * (N[None, :] * (-r * rp)[:, None])
            fe = np.empty((len(self.edges), 6)); fe[:, 0::2] = fr; fe[:, 1::2] = fz
            np.add.at(f, self.edge_dofs, fe)
            if stiffness:
                # d fr_k / d r_m = c N_k N_m zp ; d fr_k / d z_m = c N_k r d_m
                # d fz_k / d r_m = c N_k (-N_m rp - r d_m) ; d fz_k / d z_m = 0
                Kd = np.zeros((len(self.edges), 6, 6))
                Kd[:, 0::2, 0::2] = c * N[None, :, None] * N[None, None, :] * zp[:, None, None]
                Kd[:, 0::2, 1::2] = c * N[None, :, None] * d[None, None, :] * r[:, None, None]
                Kd[:, 1::2, 0::2] = c * N[None, :, None] * (-N[None, None, :] * rp[:, None, None] - d[None, None, :] * r[:, None, None])
                rows.append(np.repeat(self.edge_dofs, 6, axis=1).ravel())
                cols.append(np.tile(self.edge_dofs, (1, 6)).ravel())
                vals.append(Kd.ravel())
        Kp = None
        if stiffness:
            Kp = sp.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                               shape=(self.ndof, self.ndof)).tocsr()
        return f, Kp

    # ---------------- analyses ----------------
    def linear_buckling(self, nev=6, load_stiffness=False, sigma=None):
        u0 = np.zeros(self.ndof)
        f0, K0 = self.internal(u0, linear=True)
        fp, Kp = self.pressure(u0)
        fr = self.free
        Kff = K0[fr][:, fr].tocsc()
        u1 = np.zeros(self.ndof)
        u1[fr] = spla.spsolve(Kff, fp[fr])
        _, Ks = self.internal(u1, stress_from=u1)
        Kg = Ks - (Kp if load_stiffness else 0 * Kp)
        Bm = -Kg[fr][:, fr].tocsc()
        # (K0 + lam Kg) phi = 0  <=>  K0^-1 Bm phi = (1/lam) phi: largest real mu = 1/lam gives the lowest buckling factor
        lu = spla.splu(Kff)
        op = spla.LinearOperator(Kff.shape, matvec=lambda x: lu.solve(Bm @ x), dtype=float)
        mu, vecs = spla.eigs(op, k=nev, which="LR", tol=1e-10, maxiter=20000)
        lam = 1.0 / mu.real
        order = np.argsort(np.where(lam > 0, lam, np.inf))
        return lam[order], vecs[:, order], u1

    def arc_length(self, p_ref, dl0, nsteps, lam_stop=None, tol=1e-8, maxit=25, dl_min=None, dl_max=None, verbose=False,
                   follower=True, stop_after_limit_drop=0.25, lam_max=1e9):
        fr = self.free
        if not hasattr(self, "grow"):
            self.grow = 1.2
        u = np.zeros(self.ndof); lam = 0.0
        hist = [(0.0, 0.0, 0.0)]
        du_prev = None
        dl = dl0
        dl_min = dl_min or dl0 / 1000
        dl_max = dl_max or dl0 * 20
        lam_peak, u_peak = 0.0, u.copy()
        for step in range(nsteps):
            ok = False
            for attempt in range(12):
                fp, Kp = self.pressure(u, stiffness=follower)
                fi, K = self.internal(u)
                KT = (K - lam * p_ref * Kp) if follower else K
                KTf = KT[fr][:, fr].tocsc()
                try:
                    lu = spla.splu(KTf)
                except RuntimeError:
                    dl *= 0.5
                    continue
                dut = lu.solve(p_ref * fp[fr])
                dsign = _det_sign(lu)
                if du_prev is None:
                    sgn = 1.0
                    self._dsign0 = dsign
                    self._lsign = 1.0
                else:
                    # reverse the load direction only when the tangent determinant changes sign (limit point passed)
                    if dsign != self._dsign_prev:
                        self._lsign = -self._lsign
                    sgn = self._lsign
                self._dsign_try = dsign
                dlam = sgn * dl / np.linalg.norm(dut)
                Du = dlam * dut; Dlam = dlam
                conv = False
                for it in range(maxit):
                    uu = u.copy(); uu[fr] += Du
                    ll = lam + Dlam
                    fp, Kp = self.pressure(uu, stiffness=follower)
                    fi, K = self.internal(uu)
                    res = fi[fr] - ll * p_ref * fp[fr]
                    ref = np.linalg.norm(ll * p_ref * fp[fr]) + 1e-30
                    if np.linalg.norm(res) / ref < tol and it > 0:
                        conv = True
                        break
                    KT = (K - ll * p_ref * Kp) if follower else K
                    try:
                        lu = spla.splu(KT[fr][:, fr].tocsc())
                    except RuntimeError:
                        break
                    dr = lu.solve(-res); dt = lu.solve(p_ref * fp[fr])
                    a = dt @ dt; b = 2 * (Du + dr) @ dt; c = (Du + dr) @ (Du + dr) - dl ** 2
                    disc = b * b - 4 * a * c
                    if disc < 0:
                        break
                    s1 = (-b + math.sqrt(disc)) / (2 * a); s2 = (-b - math.sqrt(disc)) / (2 * a)
                    c1 = (Du + dr + s1 * dt) @ Du; c2 = (Du + dr + s2 * dt) @ Du
                    dlm = s1 if c1 >= c2 else s2
                    Du = Du + dr + dlm * dt; Dlam = Dlam + dlm
                if conv:
                    ok = True
                    break
                dl *= 0.5
                if dl < dl_min:
                    break
            if not ok:
                hist.append((lam, np.nan, np.nan))
                break
            u[fr] += Du; lam += Dlam
            du_prev = Du.copy()
            self._dsign_prev = self._dsign_try
            hist.append((lam, float(u[self.probe]) if getattr(self, "probe", None) is not None else u[fr] @ u[fr], it))
            if lam > lam_peak:
                lam_peak, u_peak = lam, u.copy()
            if verbose:
                print(f"step {step} lam {lam:.6f} p {lam * p_ref:.6g} it {it} dl {dl:.4g}", flush=True)
            if it <= 4:
                dl = min(dl * self.grow, dl_max)
            elif it >= 10:
                dl = max(dl * 0.6, dl_min)
            if lam_stop is not None and lam >= lam_stop:
                break
            if lam_peak > 0 and lam < (1 - stop_after_limit_drop) * lam_peak:
                break
            if lam > lam_max:
                break
        return {"lam_peak": lam_peak, "p_peak": lam_peak * p_ref, "u_peak": u_peak, "hist": hist, "u_end": u, "lam_end": lam}

    def disp_control(self, probe, targets, p_ref, tol=1e-9, maxit=30, follower=True, u0=None, lam0=0.0):
        """Prescribe the probe DOF (e.g. the outer north-pole axial displacement) and solve for (u, lambda) with a bordered
        Newton system; traces the path through limit points while the probe value is monotonic."""
        fr = self.free
        pos = int(np.nonzero(fr == probe)[0][0])
        u = np.zeros(self.ndof) if u0 is None else u0.copy()
        lam = lam0
        out = []
        for tgt in targets:
            ok = False
            for it in range(maxit):
                fp, Kp = self.pressure(u, stiffness=follower)
                fi, K = self.internal(u)
                res = fi[fr] - lam * p_ref * fp[fr]
                g = u[probe] - tgt
                ref = np.linalg.norm(lam * p_ref * fp[fr]) + 1e-30
                if it > 0 and np.linalg.norm(res) / ref < tol and abs(g) < 1e-12 * max(1.0, abs(tgt)):
                    ok = True
                    break
                KT = ((K - lam * p_ref * Kp) if follower else K)[fr][:, fr].tocsr()
                n = KT.shape[0]
                col = sp.csr_matrix((-p_ref * fp[fr]).reshape(-1, 1))
                row = sp.csr_matrix(([1.0], ([0], [pos])), shape=(1, n))
                A = sp.bmat([[KT, col], [row, None]], format="csc")
                rhs = np.concatenate([-res, [-g]])
                try:
                    d = spla.spsolve(A, rhs)
                except Exception:
                    break
                if not np.all(np.isfinite(d)):
                    break
                u[fr] += d[:n]; lam += d[n]
            out.append((float(tgt), float(lam), bool(ok), it))
            if not ok:
                break
        return out, u, lam

    def face_von_mises(self, u, layer_rows):
        """Max Cauchy von Mises over Gauss points of elements in the given thickness rows (0 = innermost)."""
        ue = u[self.edofs].reshape(self.ne, 8, 2)
        rowj = np.arange(self.ne) % self.nt
        sel = np.isin(rowj, layer_rows)
        best = 0.0; where = None
        for g in self.gp:
            E, B = self._kin(g, ue)
            S = np.einsum("eij,ej->ei", g["C"], E)
            H11 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 0]); H12 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 0])
            H21 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 1]); H22 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 1])
            hr = (ue[:, :, 0] @ g["N"]) / g["r"]
            for e in np.nonzero(sel)[0]:
                F = np.array([[1 + H11[e], H12[e], 0], [H21[e], 1 + H22[e], 0], [0, 0, 1 + hr[e]]])
                Sm = np.array([[S[e, 0], S[e, 3], 0], [S[e, 3], S[e, 1], 0], [0, 0, S[e, 2]]])
                J = np.linalg.det(F)
                sig = F @ Sm @ F.T / J
                s = sig - np.trace(sig) / 3 * np.eye(3)
                vm = math.sqrt(1.5 * np.sum(s * s))
                if vm > best:
                    best = vm; where = (int(e), float(g["r"][e]))
        return best, where
