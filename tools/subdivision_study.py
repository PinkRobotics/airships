#!/usr/bin/env python3
"""What the article weighs when the octet grid is subdivided finer inside the same cell.

    python3 tools/subdivision_study.py

The article as built is n = 1: the octet grid at one pitch per half-span. At that
subdivision a hexagon face contains no lattice point of its own, so the film has to be
carried by a separate apparatus — 36 rim edges, 48 spokes, 72 ties — which is 156 of the
216 members and 69% of the tube by length. `kelvin_lattice_counts` reports
`boundaryFrameNeeded: False` at every EVEN n: the lattice reaches the faces itself and the
whole apparatus goes away.

This prices that. Nothing here is a new physics model:

  * relative density phi is volume-normalised the way the model does it — 96 octet struts
    per Kelvin-cell volume at n = 1, and 96*n^3 at subdivision n
  * the stress in the solid is 3*p*SF/phi, which the model notes is EXACT for any
    stretch-dominated truss under hydrostatic load and independent of topology
  * the strut must beat that stress in Euler AND in local wall buckling, the latter with
    the repo's own NASA SP-8007 knockdown (K_LOCAL) and orthotropy penalty
  * joints are counted by the model and priced by the od^3 law measured on the real 51-node
    set (11.7 g -> 49.8 g when the bore went 10 -> 16 mm, against 4.10x predicted)

WHAT THIS DOES NOT CHECK, and it is the first thing to add: the FILM's bending load on the
members lying in the cell faces. At n = 1 that load is what governs the whole boundary and
it is why the rim is a 14x12. The moment falls as the CUBE of the bracing pitch, so at
n = 2 it is 1/8 and at n = 4 it is 1/64 of the n = 1 value — which is the reason to expect
these numbers to survive the check, not a reason to skip it. Until it is added, every
figure below is a floor, not an answer.

ODD n is refused. At odd n the boundary apparatus exists and its members are sized by film
bending, not by crush, so a phi-based sizing would silently under-price them — which is
exactly the error this docstring exists to prevent.
"""
import importlib.util
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "vc", ROOT / "research" / "analysis" / "vacuum-cell.py")
vc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vc)

MAT = vc.MATERIALS["T700_LAM"]
WALL_KG_M3 = 0.956859          # the air at 2,500 m: what a cubic metre has to beat
PD = vc.P_ATM * vc.LATTICE_SF  # every demand here carries the model's 1.5 already
OCTET_PER_CELL = 96            # struts per Kelvin-cell volume at n = 1; the model's divisor
NODE_G_AT_10MM = 465.0 / 51    # measured: the real 51-joint set at a 10 mm bore

# Real tube, as walls you can ask a supplier for against outside diameters in 0.5 mm steps.
# Replace with research/data/tube-catalogue.json the moment that file exists — see FLOAT.md.
WALLS_MM = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0]
ODS_MM = [x / 2 for x in range(8, 261)]


def strut_length(span, n):
    """The octet pitch at subdivision n. At n = 1 this is the cell edge."""
    return span / (2 * math.sqrt(2) * n)


def strut_force(span, n):
    """One strut's share of the array's hydrostatic crush, factored."""
    return 3 * PD * (span ** 3 / 2) / (OCTET_PER_CELL * n ** 3 * strut_length(span, n))


def phi_of(span, n, area_m2):
    """Relative density, volume-normalised — the same 96-per-cell convention as the model."""
    return (OCTET_PER_CELL * n ** 3 * strut_length(span, n) * area_m2) / (span ** 3 / 2)


def self_check():
    """Reproduce the published article's own crush figures before trusting anything else."""
    span = 2 * vc.printer_chain(vc.MATERIALS["PAHT_Z"])["rows"]["0.6 mm x 2"]["cellMRaw"]
    ro, ri = 0.005, 0.004
    area = math.pi * (ro ** 2 - ri ** 2)
    force = strut_force(span, 1)
    model = vc.member_demands(span)["families"]["octet"]["axialN"]
    phi = phi_of(span, 1, area)
    # The two ways of saying the same thing must agree: force/area, and the topology-free
    # 3p/phi. They are different arithmetic over the same lattice.
    ok = [("octet strut force", force, model, 0.5),
          ("stress via force/area", force / area / 1e6, 119.3, 0.5),
          ("stress via 3*p*SF/phi", 3 * PD / phi / 1e6, 119.3, 0.5)]
    c = vc.kelvin_lattice_counts(1)
    counts = (c["struts"] + c["rimStrutEquivalents"] + c["tieStruts"]
              + c["hexTieStruts"] + c["hexSpokeStruts"])
    ok.append(("members at n=1", counts, 216, 0))
    ok.append(("nodes at n=1", c["nodes"] + c["rimNodes"] + c["hexNodes"], 51, 0))
    ok.append(("boundary frame at n=2",
               0 if vc.kelvin_lattice_counts(2)["boundaryFrameNeeded"] else 1, 1, 0))
    print("SELF-CHECK against the model's own arithmetic")
    good = True
    for name, got, want, tol in ok:
        hit = abs(got - want) <= tol
        good &= hit
        print(f"  {'ok ' if hit else 'BAD'} {name:24s} {got:12.3f}  expected {want:10.3f}")
    print(f"  => {'consistent with the model' if good else 'DOES NOT RECONCILE — stop'}\n")
    return good


def best_article(span, n):
    """Lightest tube in the catalogue that holds this subdivision, with its mass split."""
    if n % 2:
        raise ValueError("odd n has a boundary frame sized by film bending; see the docstring")
    c = vc.kelvin_lattice_counts(n)
    nodes = c["nodes"] + c["rimNodes"] + c["hexNodes"]
    length = strut_length(span, n)
    force = strut_force(span, n)
    volume = span ** 3 / 2
    best = None
    for od in ODS_MM:
        for w in WALLS_MM:
            if od - 2 * w < 0.8:
                continue
            ro, ri = od / 2000, (od - 2 * w) / 2000
            area = math.pi * (ro ** 2 - ri ** 2)
            inertia = math.pi / 4 * (ro ** 4 - ri ** 4)
            euler = math.pi ** 2 * MAT["E"] * inertia / length ** 2
            local = (vc.K_LOCAL * vc.ORTHO_PENALTY * 0.605 * MAT["E"] * (w / 1000) / ro) * area
            if min(euler, local, MAT["sigma"] * area) < force:
                continue
            phi = phi_of(span, n, area)
            tube = phi * MAT["rho"] * volume
            joint = nodes * NODE_G_AT_10MM / 1000 * (od / 10) ** 3
            film = vc.film_kg(span) / n          # panels shrink with the pitch
            total = tube + joint + film
            if best is None or total < best["totalKg"]:
                best = dict(totalKg=total, tubeKg=tube, jointKg=joint, filmKg=film,
                            odMm=od, wallMm=w, strutMm=length * 1000, nodes=nodes,
                            phi=phi, kgPerM3=total / volume,
                            overWall=total / volume / WALL_KG_M3)
    return best


def main():
    if not self_check():
        return 1
    print("EVEN SUBDIVISION ONLY — at odd n a boundary frame exists and is sized by film")
    print("bending, which this tool does not model. n=1 is the article as built; its real")
    print("figure is 9.3-9.7x the wall from the fully-checked sizing in FLOAT.md.\n")
    print(f"{'span':>5} {'n':>2} {'nodes':>6} {'strut':>8} {'OD x wall':>15} {'phi':>9} "
          f"{'tube':>6} {'joint':>6} {'film':>5} {'kg/m3':>7} {'x wall':>7}")
    for span in (1.0, 2.0, 3.0, 4.0, 6.0):
        for n in (2, 4):
            b = best_article(span, n)
            if not b:
                print(f"{span:5.1f} {n:2d}   no tube in the catalogue holds it")
                continue
            print(f"{span:5.1f} {n:2d} {b['nodes']:6d} {b['strutMm']:7.0f}mm "
                  f"{b['odMm']:7.1f} x {b['wallMm']:4.2f}mm {b['phi']:9.6f} "
                  f"{b['tubeKg'] / (span ** 3 / 2):6.2f} {b['jointKg'] / (span ** 3 / 2):6.2f} "
                  f"{b['filmKg'] / (span ** 3 / 2):5.2f} {b['kgPerM3']:7.2f} {b['overWall']:7.2f}")
        print()
    print(f"the wall is {WALL_KG_M3:.4f} kg/m3. A row under 1.00 in the last column floats.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
