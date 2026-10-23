#!/usr/bin/env python3
"""CHECK-047 part B: this checker's own axisymmetric CalculiX model of MAINLINE-047's stated P2 point.

It is built from the card's and METHOD.md's stated definitions only; the owner's decks and code are not read.
- Geometry: full sphere, R_outer = 10,000 mm, two 0.794624066985892 mm Be faces, a 23.23721790601544 mm core. Every
  layer is offset inward by d(theta) = a exp[-(R theta / w)^2], stress-free.
- Elements: CAX8 (full integration), shared nodes. The angular mesh is this checker's own: uniform h_fine at the outer
  surface out to S_fine, a geometric growth, then h_far. Faces have nf elements each and the core nc.
- Restraint: axis nodes radial, one south-pole node axial.
- Faces: E = 290 GPa, nu = 0.0768, *PLASTIC with NLGEOM (finite-strain J2, hyperelastic elastic part), perfectly
  plastic at the stated yield. 10,000 MPa reproduces the identical pre-yield branch, as the card does.
- Core: orthotropic StVK (*ELASTIC, ENGINEERING CONSTANTS with NLGEOM), zero Poisson. It uses a cylindrical
  orientation about the global z axis through the sphere centre: local 1 = sphere radial, 2 = meridian, 3 = hoop.
  W puts G_W = 6.8 ksi on the radial-meridian pair; L interchanges.
- Load: follower pressure on the outer surface, ramped in steps that end exactly at the requested pressures. An
  optional last step runs on until the solver stops (the numerical endpoint).

Usage: fe047.py build NAME a_mm w_mm W|L yield_MPa [--p kPa,kPa,...] [--endpoint kPa] [--hfine 4] [--sfine 1300]
       [--hfar 60] [--nf 2] [--nc 6] [--ein 1] [--gin 0.5]
       fe047.py parse NAME
Runs live under fe/NAME/; the solver is run by the caller through simjob."""
import gzip
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FE = os.path.join(HERE, "fe")
PSI = 0.006894757293168361
RO, TF, TC = 10000.0, 0.794624066985892, 23.23721790601544
P_SERVICE = 95.46083791390515


def theta_edges(hfine, sfine, hfar, growth=1.06):
    s = [0.0]
    h = hfine
    while s[-1] < sfine - 1e-9:
        s.append(min(s[-1] + hfine, sfine))
    while h < hfar:
        h = min(h * growth, hfar)
        s.append(s[-1] + h)
    total = math.pi * RO
    rest = total - s[-1]
    n = max(1, round(rest / hfar))
    s += [s[-1] + rest * (k + 1) / n for k in range(n)]
    th = np.array(s) / RO
    th[-1] = math.pi
    return th


def build(name, a, w, mer, ys, pressures, endpoint=None, hfine=4.0, sfine=1300.0, hfar=60.0, nf=2, nc=6, ein=1.0, gin=0.5, ef=290000.0):
    d = os.path.join(FE, name)
    os.makedirs(d, exist_ok=True)
    th_e = theta_edges(hfine, sfine, hfar)
    n = len(th_e) - 1
    th_n = np.empty(2 * n + 1)
    th_n[0::2] = th_e
    th_n[1::2] = 0.5 * (th_e[:-1] + th_e[1:])
    Ri = RO - 2 * TF - TC
    layers = [TF / nf] * nf + [TC / nc] * nc + [TF / nf] * nf          # inner face, core, outer face
    L = len(layers)
    rho = [Ri]
    for t in layers:
        rho += [rho[-1] + t / 2, rho[-1] + t]
    rho = np.array(rho)
    nr = len(rho)                                                      # 2L + 1 node rows

    def nid(i, j):
        return 1 + i * nr + j
    used = set()
    elems = []
    for i in range(n):
        for jl in range(L):
            I, J = 2 * i, 2 * jl
            con = [nid(I, J), nid(I + 2, J), nid(I + 2, J + 2), nid(I, J + 2), nid(I + 1, J), nid(I + 2, J + 1), nid(I + 1, J + 2), nid(I, J + 1)]
            used.update(con)
            elems.append((1 + i * L + jl, i, jl, con))
    lines = ["*HEADING", f"CHECK-047 own model {name}: a={a} mm w={w} mm {mer} yield={ys} MPa", "*NODE"]
    axis, spole = [], None
    for i in range(2 * n + 1):
        th = th_n[i]
        dd = a * math.exp(-(RO * th / w) ** 2) if a else 0.0
        for j in range(nr):
            k = nid(i, j)
            if k not in used:
                continue
            r = rho[j] - dd
            x = 0.0 if i in (0, 2 * n) else r * math.sin(th)
            y = r * math.cos(th)
            lines.append(f"{k},{x:.12e},{y:.12e}")
            if i in (0, 2 * n):
                axis.append(k)
            if i == 2 * n and j == nr - 1:
                spole = k
    face_el = [e for e, i, jl, c in elems if jl < nf or jl >= nf + nc]
    core_el = [e for e, i, jl, c in elems if nf <= jl < nf + nc]
    smax_face, smax_core = min(4000.0, 6 * w), min(3000.0, 5 * w)
    face_out = [e for e, i, jl, c in elems if (jl < nf or jl >= nf + nc) and th_e[i] * RO < smax_face]
    core_out = [e for e, i, jl, c in elems if nf <= jl < nf + nc and th_e[i] * RO < smax_core]
    outer = [e for e, i, jl, c in elems if jl == L - 1]
    lines.append("*ELEMENT, TYPE=CAX8, ELSET=ALL")
    for e, i, jl, c in elems:
        lines.append(f"{e}," + ",".join(map(str, c)))

    def elset(nm, ids):
        lines.append(f"*ELSET, ELSET={nm}")
        for k in range(0, len(ids), 12):
            lines.append(",".join(map(str, ids[k:k + 12])))
    elset("FACES", face_el)
    elset("CORE", core_el)
    elset("FACEOUT", face_out)
    elset("COREOUT", core_out)
    lines.append("*NSET, NSET=AXIS")
    for k in range(0, len(axis), 12):
        lines.append(",".join(map(str, axis[k:k + 12])))
    gm, gh = (6800 * PSI, 15000 * PSI) if mer == "W" else (15000 * PSI, 6800 * PSI)
    lines += ["*MATERIAL, NAME=BE", "*ELASTIC", f"{ef:.1f}, 0.0768", "*PLASTIC", f"{ys:.6f}, 0.",
              "*MATERIAL, NAME=CORE", "*ELASTIC, TYPE=ENGINEERING CONSTANTS",
              f"{15000 * PSI:.10f}, {ein:.10f}, {ein:.10f}, 0., 0., 0., {gm:.10f}, {gh:.10f}", f"{gin:.10f}, 0.",
              "*ORIENTATION, NAME=SPH, SYSTEM=CYLINDRICAL", "0., 0., 0., 0., 0., 1.",
              "*SOLID SECTION, ELSET=FACES, MATERIAL=BE", "*SOLID SECTION, ELSET=CORE, MATERIAL=CORE, ORIENTATION=SPH",
              "*BOUNDARY", "AXIS, 1, 1", f"{spole}, 2, 2"]
    prev = 0.0
    for k, p in enumerate(pressures):
        first = k == 0
        lines += ["*STEP, NLGEOM, INC=10000", "*STATIC", ("0.1, 1., 1e-7, 0.2" if first else "0.25, 1., 1e-7, 0.5"), "*DLOAD"]
        lines.append(f"OUTERS, P3, {p / 1000:.12e}")          # CalculiX reads at most 20 characters a field
        lines += ["*EL PRINT, ELSET=FACEOUT, FREQUENCY=1000000", "S, PEEQ", "*EL PRINT, ELSET=COREOUT, FREQUENCY=1000000", "S, E",
                  "*END STEP"]
        prev = p
    if endpoint:
        lines += ["*STEP, NLGEOM, INC=100000", "*STATIC", "0.002, 1., 1e-7, 0.01", "*DLOAD", f"OUTERS, P3, {endpoint / 1000:.12e}",
                  "*EL PRINT, ELSET=FACEOUT, FREQUENCY=1000000", "PEEQ", "*END STEP"]
    # the outer-surface element set is defined before the steps
    k0 = lines.index("*BOUNDARY")
    blk = ["*ELSET, ELSET=OUTERS"] + [",".join(map(str, outer[k:k + 12])) for k in range(0, len(outer), 12)]
    lines[k0:k0] = blk
    with open(os.path.join(d, "job.inp"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    meta = {"name": name, "a_mm": a, "w_mm": w, "meridian": mer, "yield_MPa": ys, "pressures_kPa": pressures, "endpoint_to_kPa": endpoint,
            "mesh": {"n_theta": n, "h_fine_mm": hfine, "s_fine_mm": sfine, "h_far_mm": hfar, "growth": 1.06, "nface": nf, "ncore": nc,
                     "elements": len(elems), "nodes": len(used)},
            "core": {"E_normal": 15000 * PSI, "E_in": ein, "G_in": gin, "G_meridian": gm, "G_hoop": gh}, "face_E_MPa": ef,
            "out_regions_mm": {"faces": smax_face, "core": smax_core},
            "theta_elem_mid": [float(0.5 * (th_e[i] + th_e[i + 1])) for i in range(n)], "nf": nf, "nc": nc, "L": L}
    json.dump(meta, open(os.path.join(d, "meta.json"), "w"))
    return d


def blocks(path):
    """Yield (kind, set, time, rows) for every *EL PRINT block in a .dat file."""
    op = gzip.open if path.endswith(".gz") else open
    kind = None
    rows = []
    with op(path, "rt") as fh:
        for line in fh:
            m = re.search(r"^\s*(stresses|strains|equivalent plastic strain)\b.*?set\s*(\S+)\s+and time\s+(\S+)", line)
            if m:
                if kind:
                    yield kind, st, tm, rows
                kind, st, tm, rows = m.group(1), m.group(2), float(m.group(3)), []
                continue
            if kind:
                t = line.split()
                if len(t) >= 3 and t[0].isdigit():
                    rows.append([int(t[0]), int(t[1])] + [float(x) for x in t[2:8] if re.match(r"^[-+0-9.Ee]+$", x)])
    if kind:
        yield kind, st, tm, rows


def mises(s):
    sxx, syy, szz, sxy, sxz, syz = s
    return math.sqrt(0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2) + 3 * (sxy ** 2 + sxz ** 2 + syz ** 2))


def core_eval(E_loc, mer, ein=1.0, gin=0.5):
    """The card's stated current-frame shear: material axes 1 = meridian, 2 = normal, 3 = hoop; StVK S = C:E;
    F* = Cholesky factor (F*^T F* = C); sigma* = F* S F*^T / det F*; tangent F*e1, normal perpendicular to F*e1 and F*e3."""
    p = [1, 0, 2]                                   # card axes from this model's local axes (radial, meridian, hoop)
    E = np.array([[E_loc[p[i]][p[j]] for j in range(3)] for i in range(3)])
    gm, gh = (6800 * PSI, 15000 * PSI) if mer == "W" else (15000 * PSI, 6800 * PSI)
    Dv = np.diag([ein, 15000 * PSI, ein, gm, gin, gh])        # (11, 22, 33, 2E12, 2E13, 2E23) with 12 = meridian-normal
    v = np.array([E[0, 0], E[1, 1], E[2, 2], 2 * E[0, 1], 2 * E[0, 2], 2 * E[1, 2]])
    s = Dv @ v
    S = np.array([[s[0], s[3], s[4]], [s[3], s[1], s[5]], [s[4], s[5], s[2]]])
    C = np.eye(3) + 2 * E
    Fs = np.linalg.cholesky(C).T
    J = np.linalg.det(Fs)
    sig = Fs @ S @ Fs.T / J
    t = Fs[:, 0] / np.linalg.norm(Fs[:, 0])
    nrm = np.cross(Fs[:, 0], Fs[:, 2])
    nrm = nrm / np.linalg.norm(nrm)
    b = np.cross(nrm, t)
    tau_m = float(t @ sig @ nrm)
    tau_h = float(b @ sig @ nrm)
    comp = -float(nrm @ sig @ nrm)
    Sm, Sh = (25 * PSI, 45 * PSI) if mer == "W" else (45 * PSI, 25 * PSI)
    Smt, Sht = (35 * PSI, 55 * PSI) if mer == "W" else (55 * PSI, 35 * PSI)
    lam_S = float(np.linalg.eigvalsh(S)[0])
    lam_C = float(np.linalg.eigvalsh(C)[0])
    cmin = min(ein, 15000 * PSI, 2 * gm, 2 * gin, 2 * gh)
    return {"tau_m": tau_m, "tau_h": tau_h, "index_min": math.hypot(tau_m / Sm, tau_h / Sh), "index_typ": math.hypot(tau_m / Smt, tau_h / Sht),
            "compression": comp, "bound": lam_S + 0.5 * cmin * lam_C, "sigma_star": sig, "S": S, "E": E}


def parse(name):
    d = os.path.join(FE, name)
    meta = json.load(open(os.path.join(d, "meta.json")))
    dat = os.path.join(d, "job.dat") if os.path.exists(os.path.join(d, "job.dat")) else os.path.join(d, "job.dat.gz")
    frames = {}
    for kind, st, tm, rows in blocks(dat):
        frames.setdefault(round(tm, 9), {})[(kind, st)] = rows
    nf, nc, L = meta["nf"], meta["nc"], meta["L"]
    thm = meta["theta_elem_mid"]
    out = []
    for k, tm in enumerate(sorted(frames)):
        fr = frames[tm]
        rec = {"time": tm}
        if ("stresses", "FACEOUT") in fr:
            best = max(fr[("stresses", "FACEOUT")], key=lambda r: mises(r[2:8]))
            e = best[0] - 1
            rec.update({"face_mises_max": mises(best[2:8]), "face_max_elem": best[0], "face_max_ip": best[1],
                        "face_max_s_mm": thm[e // L] * RO, "face_max_layer": "inner" if e % L < nf else "outer"})
        if ("equivalent plastic strain", "FACEOUT") in fr:
            rec["peeq_max"] = max(r[2] for r in fr[("equivalent plastic strain", "FACEOUT")])
        if ("strains", "COREOUT") in fr:
            strains = fr[("strains", "COREOUT")]
            stresses = {(r[0], r[1]): r[2:8] for r in fr.get(("stresses", "COREOUT"), [])}
            worst, wc, minb, inv_err, maxcomp = None, None, None, 0.0, 0.0
            mer = meta["meridian"]
            for r in strains:
                exx, eyy, ezz, exy, exz, eyz = r[2:8]
                El = [[exx, exy, exz], [exy, eyy, eyz], [exz, eyz, ezz]]
                ce = core_eval(El, mer, meta["core"]["E_in"], meta["core"]["G_in"])
                if worst is None or ce["index_min"] > worst[1]["index_min"]:
                    worst = ((r[0], r[1]), ce)
                maxcomp = max(maxcomp, ce["compression"])
                minb = ce["bound"] if minb is None else min(minb, ce["bound"])
                sn = stresses.get((r[0], r[1]))
                if sn is not None:
                    sx, sy, sz, sxy, sxz, syz = sn
                    Sn = np.array([[sx, sxy, sxz], [sxy, sy, syz], [sxz, syz, sz]])
                    ss = ce["sigma_star"]
                    inv_err = max(inv_err, abs(np.trace(Sn) - np.trace(ss)), abs(np.linalg.norm(Sn) - np.linalg.norm(ss)))
            (e, ip), ce = worst
            rec.update({"core_index_min_avg": ce["index_min"], "core_index_typical": ce["index_typ"], "core_tau_meridian": ce["tau_m"],
                        "core_tau_hoop": ce["tau_h"], "core_worst_elem": e, "core_worst_ip": ip, "core_worst_s_mm": thm[(e - 1) // L] * RO,
                        "core_max_compression": maxcomp, "core_min_sufficient_bound": minb, "core_invariant_error": inv_err,
                        "core_worst_E": ce["E"].tolist()})
        out.append(rec)
    # step pressures: frames are step ends, in order
    ps = meta["pressures_kPa"]
    for k, rec in enumerate(out[:len(ps)]):
        rec["pressure_kPa"] = ps[k]
    res = {"meta": {k: v for k, v in meta.items() if k != "theta_elem_mid"}, "frames": out}
    sta = os.path.join(d, "job.sta")
    if os.path.exists(sta) and meta.get("endpoint_to_kPa"):
        last = None
        for line in open(sta):
            t = line.split()
            # STEP INC ATT ITRS TOT-TIME STEP-TIME INC-TIME; an attempt marked U did not converge
            if len(t) >= 7 and t[0].isdigit() and not t[2].endswith("U"):
                last = (int(t[0]), float(t[5]))             # step, step time of the last converged increment
        nps = len(ps)
        if last and last[0] == nps + 1:
            p0 = ps[-1]
            res["endpoint_kPa"] = p0 + (meta["endpoint_to_kPa"] - p0) * last[1]
        elif last:
            res["endpoint_kPa"] = None
            res["endpoint_note"] = f"last converged step {last[0]} time {last[1]}"
    json.dump(res, open(os.path.join(d, "result.json"), "w"), indent=1)
    return res


def main():
    cmd = sys.argv[1]
    if cmd == "build":
        name, a, w, mer, ys = sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5], float(sys.argv[6])
        kw = {}
        args = sys.argv[7:]
        pressures = [P_SERVICE, 1.05 * P_SERVICE]
        endpoint = None
        for k in range(0, len(args), 2):
            key, val = args[k], args[k + 1]
            if key == "--p":
                pressures = [float(x) if x not in ("SF1", "SF105") else (P_SERVICE if x == "SF1" else 1.05 * P_SERVICE) for x in val.split(",")]
            elif key == "--endpoint":
                endpoint = float(val)
            elif key in ("--hfine", "--sfine", "--hfar", "--ein", "--gin"):
                kw[key[2:]] = float(val)
            elif key in ("--nf", "--nc"):
                kw[key[2:]] = int(val)
        d = build(name, a, w, mer, ys, pressures, endpoint, **kw)
        print(d, json.load(open(os.path.join(d, "meta.json")))["mesh"])
    elif cmd == "parse":
        res = parse(sys.argv[2])
        for f in res["frames"]:
            print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in f.items() if k != "core_worst_E"})
        if "endpoint_kPa" in res:
            print("endpoint", res["endpoint_kPa"], res.get("endpoint_note", ""))


if __name__ == "__main__":
    main()
