#!/usr/bin/env python3
"""MAINLINE-030: does the smeared lattice (global) buckling formula apply at the P3 points the night scored?

Equilateral grid, member length s, tube r_o and wall t. Smeared plate: D = (3*sqrt3/4)*E*I/s, Y = (2/sqrt3)*E*A/s, so
D/Y = 1.125*I/A = 1.125*rg^2. The classical sphere buckle (Donnell) has k^4 = Y/(D*R^2), so the half-wavelength is
pi*sqrt(1.0607*rg*R). The smeared formula needs that half-wave to span several members; the ratio to s is reported.
Checker's own arithmetic; QUESTIONABLE.
"""
import json
import math
from pathlib import Path

R = 10.0
POINTS = [  # name, source report, s m, r_o m, wall m
    ("011b SiC equilateral k0.2", "rpt-mainline011b-grok-p3-global-arcs-1019", 2.04, 0.123688362374, 0.000880299093685),
    ("022 carried, 5%", "rpt-mainline022-grok-p3-optimistic-floating-point-1020", 3.0, 0.136709082896, 0.0010718489472),
    ("023 re-optimised 5%", "rpt-ref-a4768f77870336c8cdbb", 1.78, None, None),
    ("022b carried, 5%, gamma", "rpt-mainline022b-grok-equilibrium-1020", 6.15, 0.167645931148, 0.00162527464757),
    ("022b carried, 019 reserve, gamma", "rpt-mainline022b-grok-equilibrium-1020", 6.15, 0.165575346913, 0.00157870644521),
    ("022b CFRP + Zylon, 5%", "rpt-mainline022b-grok-equilibrium-1020", 5.5, 0.166128907123, 0.00160025181565),
    ("022b Ti + Kapton, 5%", "rpt-mainline022b-grok-equilibrium-1020", 1.85, 0.103026820155, 0.000696476333589),
    ("022b Mylar + 380 MPa, 5%", "rpt-mainline022b-grok-equilibrium-1020", 0.55, 0.085198517829, 0.000311428174832),
]
out = []
for name, src, s, ro, t in POINTS:
    V = 8 * math.pi * R ** 2 / (math.sqrt(3) * s ** 2) + 2
    row = {"point": name, "source": src, "s_m": s, "nodes": V}
    if ro is not None:
        ri = ro - t
        rg = math.sqrt((ro ** 2 + ri ** 2) / 4)
        half = math.pi * math.sqrt(1.125 ** 0.5 * rg * R)
        row.update({"r_o_m": ro, "wall_m": t, "rg_m": rg, "buckle_half_wave_m": half, "half_wave_over_s": half / s})
    out.append(row)
p = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline030-design-register-1020" / "CONTINUUM.json"
p.write_text(json.dumps(out, indent=1))
for r in out:
    print(f"{r['point']:36s} s {r['s_m']:5.2f} m  nodes {r['nodes']:7.1f}  " +
          (f"half-wave {r['buckle_half_wave_m']:.3f} m  half-wave/s {r['half_wave_over_s']:.2f}" if 'rg_m' in r else "(section not stated in the body)"))
