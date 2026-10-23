#!/usr/bin/env python3
"""MAINLINE-059: water ponded in P3's sagged film bays (this seat's own geometry).

Under vacuum each P3 bay's film is pushed inward between members, so the outer surface is a dish. 024 charges that sag as
lift: equilateral bays of side s tile the sphere, with crown c = 0.0425737 s and mean depth 0.503625 c. 052's resized
f5-019 charges 73.10073 kg of sag lift at R10 ISA, scaling as R^3, which fixes s = 2.3244 m at R10 and s proportional to R.

The dish shape is PROJECTION: d = k c t (2 - t), t = 3 min(L1, L2, L3) in barycentric coordinates. It is zero on the
members and has its crown at the centroid; k = 1.00725 matches 024's mean depth. A bay tilted by beta (its polar angle on
the sphere) holds water up to its lowest rim point. The pond volume is averaged over the bay's azimuth. Bays below the
equator face down and hold nothing. Writes PONDS.json."""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RHO_AIR_ISA = 1.16726833075          # COMMON's 500 m ISA air density
RHO_W = 1000.0
SAG_R10_ISA = 73.10073311528532      # 052 MASS-ACCOUNT.csv, R10 ISA sag lift debit, kg
CROWN_PER_S = 1 - math.sqrt(1 - 1 / 12)    # 024: cap of radius s through the inradius circle -> c/s = 0.0425737
MEAN_PER_CROWN = 0.503624902308      # 024: mean depth over the bay / crown


def bay_size(R):
    """Side s from the sag volume: V = 4 pi R^2 x mean depth = 4 pi R^2 x 0.503625 x 0.0425737 s."""
    vol = SAG_R10_ISA / RHO_AIR_ISA * (R / 10) ** 3
    return vol / (4 * math.pi * R * R * MEAN_PER_CROWN * CROWN_PER_S)


def dish(n=301):
    """Barycentric grid on the unit-side equilateral triangle: points (x, y), weights and normalised depth t(2-t)."""
    v = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, math.sqrt(3) / 2]])
    pts, w, dep = [], [], []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            l1, l2 = i / n, j / n
            l3 = 1 - l1 - l2
            p = l1 * v[0] + l2 * v[1] + l3 * v[2]
            t = 3 * min(l1, l2, l3)
            pts.append(p)
            dep.append(t * (2 - t))
    pts, dep = np.array(pts), np.array(dep)
    area = math.sqrt(3) / 4
    w = np.full(len(pts), area / len(pts))
    k = MEAN_PER_CROWN / (dep @ w / area)            # scale so the mean depth is 024's 0.503625 crown
    return v, pts, w, dep * k, k


def pond_fraction(beta, psi, v, pts, w, dep, crown_over_s):
    """Pond volume / (s^3) for a bay tilted by beta, downslope direction at azimuth psi (unit side, depth c/s)."""
    n = np.array([math.cos(psi), math.sin(psi)])
    sb, cb = math.sin(beta), math.cos(beta)
    z = -(pts @ n) * sb - dep * crown_over_s * cb        # height of the film surface (world vertical)
    edge = []
    for a in range(3):
        p0, p1 = v[a], v[(a + 1) % 3]
        for u in np.linspace(0, 1, 201):
            edge.append(p0 + u * (p1 - p0))
    zrim = (-(np.array(edge) @ n) * sb).min()            # lowest point of the rim (members at depth 0)
    depth = np.maximum(0.0, zrim - z)
    return float(depth @ w) * cb                          # vertical columns over the horizontal projection


def pond_surface(beta, psi, v, pts, w, dep, crown_over_s):
    """Free-surface (horizontal) area / s^2 of the same pond: the wetted region projected on the horizontal."""
    n = np.array([math.cos(psi), math.sin(psi)])
    sb, cb = math.sin(beta), math.cos(beta)
    z = -(pts @ n) * sb - dep * crown_over_s * cb
    edge = []
    for a in range(3):
        p0, p1 = v[a], v[(a + 1) % 3]
        for u in np.linspace(0, 1, 201):
            edge.append(p0 + u * (p1 - p0))
    zrim = (-(np.array(edge) @ n) * sb).min()
    return float(w[(zrim - z) > 0].sum()) * cb


def lattice(s, R, centre, rings=6):
    """Bays of a planar equilateral triangular lattice (side s) around the top point, mapped onto the sphere: each
    bay's tilt is its centroid distance / R; its downslope azimuth is the direction away from the top, measured in the
    bay's own frame. centre = "face" (a bay centred on the top) or "vertex" (a node on the top)."""
    h = s * math.sqrt(3) / 2
    tri = []
    for i in range(-rings * 2, rings * 2 + 1):
        for j in range(-rings * 2, rings * 2 + 1):
            x0, y0 = i * s + j * s / 2, j * h
            up = [(x0, y0), (x0 + s, y0), (x0 + s / 2, y0 + h)]
            dn = [(x0 + s, y0), (x0 + s / 2, y0 + h), (x0 + 3 * s / 2, y0 + h)]
            tri += [up, dn]
    if centre == "face":
        off = (s / 2, h / 3)
    elif centre == "vertex":
        off = (0.0, 0.0)
    else:
        off = centre                         # an explicit (x, y) position of the top point in the lattice
    out = []
    for T in tri:
        T = [(x - off[0], y - off[1]) for x, y in T]
        cx, cy = sum(x for x, _ in T) / 3, sum(y for _, y in T) / 3
        r = math.hypot(cx, cy)
        if r / R > math.radians(20):
            continue
        # orientation of the downslope direction relative to the bay's first edge, in the bay's own frame
        ex, ey = T[1][0] - T[0][0], T[1][1] - T[0][1]
        downs = math.atan2(cy, cx) if r > 1e-9 else 0.0
        upward = T[2][1] > T[0][1]
        rel = downs - math.atan2(ey, ex)
        if not upward:
            rel = -rel                       # a pointing-down triangle is the unit triangle mirrored
        out.append((r / R, rel))
    return out


def main():
    v, pts, w, dep, k = dish()
    cs = CROWN_PER_S
    betas = np.radians(np.concatenate([np.linspace(0, 10, 41), np.linspace(10.5, 90, 160)]))
    psis = np.radians(np.linspace(0, 120, 25)[:-1])
    frac = np.array([np.mean([pond_fraction(b, p, v, pts, w, dep, cs) for p in psis]) for b in betas])
    area_unit = math.sqrt(3) / 4
    level = frac[0] / area_unit            # mean pond depth / s for a level bay (= mean dish depth / s)
    out = {"basis": __doc__, "k_shape": k, "crown_per_s": cs, "mean_per_crown": MEAN_PER_CROWN,
           "beta_deg": np.degrees(betas).tolist(), "pond_volume_per_s3": frac.tolist(),
           "level_mean_depth_per_s": level, "radii": {}}
    for R in (10, 12, 15, 20, 30):
        s = bay_size(R)
        A_bay = area_unit * s * s
        # bays per unit area 1/A_bay; pond mass per unit area at tilt beta = rho_w V(beta) / A_bay
        m_area = RHO_W * frac * s ** 3 / A_bay           # kg/m2 of hull surface at polar angle beta
        integrand = m_area * 2 * math.pi * R * R * np.sin(betas)
        total = float(np.trapezoid(integrand, betas))
        disc = {}
        for centre in ("face", "vertex"):
            lat = lattice(s, R, centre)
            vol = sum(pond_fraction(b, rel, v, pts, w, dep, cs) for b, rel in lat) * s ** 3
            disc[centre] = RHO_W * vol
            disc[centre + "_surface_m2"] = sum(pond_surface(b, rel, v, pts, w, dep, cs) for b, rel in lat) * s ** 2
        # the top point placed uniformly at random over one lattice cell (a rhombus of two bays): 200 placements
        rng = np.random.default_rng(59)
        samples = []
        for _ in range(200):
            a_, b_ = rng.random(2)
            off = (a_ * s + b_ * s / 2, b_ * s * math.sqrt(3) / 2)
            samples.append(RHO_W * s ** 3 * sum(pond_fraction(b, rel, v, pts, w, dep, cs) for b, rel in lattice(s, R, off)))
        samples = np.array(samples)
        disc["random_mean"], disc["random_p05"], disc["random_p95"] = float(samples.mean()), float(np.percentile(samples, 5)), float(np.percentile(samples, 95))
        disc["random_min"], disc["random_max"] = float(samples.min()), float(samples.max())
        out["radii"][str(R)] = {"s_m": s, "crown_m": cs * s, "bay_area_m2": A_bay, "bays": 4 * math.pi * R * R / A_bay,
                                "pond_random_top": {k: disc[k] for k in ("random_mean", "random_p05", "random_p95", "random_min", "random_max")},
                                "pond_face_up_kg": disc["face"], "pond_vertex_up_kg": disc["vertex"],
                                "pond_face_up_surface_m2": disc["face_surface_m2"], "pond_vertex_up_surface_m2": disc["vertex_surface_m2"],
                                "level_bay_capacity_kg": RHO_W * frac[0] * s ** 3,
                                "pond_capacity_kg": total, "pond_capacity_per_hull_area_kg_m2": total / (4 * math.pi * R * R),
                                "pond_kg_m2_by_beta": m_area.tolist()}
        print(f"R{R}: s {s:.4f} m, crown {cs * s * 100:.2f} cm, level bay {RHO_W * frac[0] * s ** 3:.1f} kg, "
              f"upper-hemisphere pond capacity {total:.0f} kg ({total / (4 * math.pi * R * R):.3f} kg/m2 of hull); "
              f"bay on top {disc['face']:.0f} kg, node on top {disc['vertex']:.0f} kg; random top point mean "
              f"{disc['random_mean']:.0f} kg (5-95% {disc['random_p05']:.0f}-{disc['random_p95']:.0f}, range "
              f"{disc['random_min']:.0f}-{disc['random_max']:.0f})")
    with open(os.path.join(HERE, "PONDS.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1)
    os.replace(os.path.join(HERE, "PONDS.json.tmp"), os.path.join(HERE, "PONDS.json"))
    for b, f in list(zip(np.degrees(betas), frac))[::12]:
        print(f"  beta {b:5.1f} deg: pond {f / area_unit:.5f} s (mean depth over the bay, per bay side)")


if __name__ == "__main__":
    main()
