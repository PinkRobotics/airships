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
  * every member lying in a face must also beat the film's transverse bending load, using
    film_edge_loads' membrane construction at the lattice pitch and the same 1.5 factor
  * joints are counted by the model and priced by the od^3 law measured on the real 51-node
    set after the sunken-frame correction (0.715 kg at a 10 mm bore)

The film check covers all four even-n face-member geometries: hexagon-hexagon and
hexagon-square cell edges, and coplanar members inside hexagon and square faces. The moment
falls as the CUBE of bracing pitch; the self-check proves both that law and exact n=1 parity
with film_edge_loads before any subdivided result is printed.

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
NODE_G_AT_10MM = 715.0 / 51    # measured sunken-frame set: 0.715 kg at a 10 mm bore

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


def section(od_mm, wall_mm):
    """Tube section properties in SI units."""
    ro, ri = od_mm / 2000, (od_mm - 2 * wall_mm) / 2000
    area = math.pi * (ro ** 2 - ri ** 2)
    inertia = math.pi / 4 * (ro ** 4 - ri ** 4)
    return {"ro": ro, "area": area, "inertia": inertia, "z": inertia / ro}


def face_panels(span, n):
    """The two even-n panel shapes, both derived from the octet pitch."""
    pitch = strut_length(span, n)
    return {"pitch": pitch,
            "hexInradius": vc.PANEL["hexSpoked"] * pitch,
            # In a square face the two <110> directions are perpendicular. Their pitch-sided
            # diamond is therefore a square, not the four-triangle apparatus used at n=1.
            "squareInradius": pitch / 2.0}


def dihedral_load(t1, t2, sin_a, theta):
    """Resultant of unequal membrane pulls across an interior dihedral."""
    beta = theta / 2.0 - math.asin(sin_a)
    return math.hypot((t1 + t2) * math.cos(beta),
                      (t1 - t2) * math.sin(beta))


def film_line_loads(span, n):
    """Unfactored one-atmosphere film line loads on every even-n face-member type."""
    panels = face_panels(span, n)
    t_hex, sin_a = vc.panel_tension(panels["hexInradius"])
    t_square, sin_square = vc.panel_tension(panels["squareInradius"])
    if not math.isclose(sin_a, sin_square, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("panel tilt changed with panel size; the shared-alpha model moved")
    th_hh = math.acos(-1.0 / 3.0)
    th_hs = math.pi - math.acos(1.0 / math.sqrt(3.0))
    return {
        "hexagon-hexagon edge": dihedral_load(t_hex, t_hex, sin_a, th_hh),
        "hexagon-square edge": dihedral_load(t_hex, t_square, sin_a, th_hs),
        "coplanar hexagon": 2.0 * t_hex * sin_a,
        "coplanar square": 2.0 * t_square * sin_a,
    }


def film_bending(span, n, sec):
    """Pinned, one-pitch bending envelope at the model's unchanged safety factor."""
    length = strut_length(span, n)
    cases = {}
    for name, line_load in film_line_loads(span, n).items():
        moment = line_load * length ** 2 / 8.0
        stress = moment / sec["z"]
        fails_at_atm = MAT["sigma"] / stress
        cases[name] = {"lineLoadNPerM": line_load, "momentNm": moment,
                       "stressMPa": stress / 1e6,
                       "marginAtSF": fails_at_atm / vc.LATTICE_SF,
                       "failsAtAtm": fails_at_atm}
    name = max(cases, key=lambda k: cases[k]["momentNm"])
    return {"case": name, **cases[name], "cases": cases}


def film_kg(span, n):
    """Film mass at the panel geometry actually present on an even-n article."""
    f = vc.kelvin_faces(span)
    panels = face_panels(span, n)
    return (8.0 * f["hexM2"] * vc.barrier_kg_per_m2(2.0 * panels["hexInradius"])
            + 6.0 * f["sqM2"] * vc.barrier_kg_per_m2(
                2.0 * panels["squareInradius"]))


def article_tube_length(span, n):
    """Total purchased cut length in standalone article A."""
    return vc.kelvin_lattice_counts(n)["struts"] * strut_length(span, n)


def article_tube_kg(span, n, area_m2):
    """Purchased tube in standalone article A: every physical cut, not an array share."""
    return article_tube_length(span, n) * area_m2 * MAT["rho"]


def face_edge_topology():
    """Enumerate the truncated octahedron's face pairs directly from its vertices."""
    import itertools

    vertices = sorted({tuple(s * x for s, x in zip(signs, perm))
                       for perm in itertools.permutations((0, 1, 2))
                       for signs in itertools.product((-1, 1), repeat=3)})

    def faces(v):
        out = []
        for axis in range(3):
            if abs(v[axis]) == 2:
                normal = tuple((1 if v[axis] > 0 else -1) if i == axis else 0
                               for i in range(3))
                out.append(("square", normal))
        for signs in itertools.product((-1, 1), repeat=3):
            if sum(s * x for s, x in zip(signs, v)) == 3:
                out.append(("hexagon", signs))
        return set(out)

    pairs = []
    for i, u in enumerate(vertices):
        for v in vertices[i + 1:]:
            if sum((a - b) ** 2 for a, b in zip(u, v)) != 2:
                continue
            common = sorted(faces(u) & faces(v))
            if len(common) != 2:
                raise ValueError(f"edge {u}-{v} belongs to {len(common)} faces")
            pairs.append(common)
    return pairs


def self_check():
    """Reproduce published crush and bending before trusting any subdivided result."""
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

    # Shared n=1 primitives must reproduce film_edge_loads' published rim and spoke rows.
    published = vc.film_edge_loads(span)["rows"]
    rim = film_bending(span, 1, section(14, 1))["cases"]["hexagon-hexagon edge"]
    spoke = film_bending(span, 1, section(10, 1))["cases"]["coplanar hexagon"]
    for label, got, row in (("film rim", rim, published[2]),
                            ("film spoke", spoke, published[3])):
        ok += [
            (label + " load", got["lineLoadNPerM"], row["lineLoadNPerM"], 0.5),
            (label + " moment", got["momentNm"], row["momentPinnedNm"], 0.05),
            (label + " stress", got["stressMPa"], row["stressPinnedMPa"], 0.5),
            (label + " margin SF", got["marginAtSF"], row["marginPinnedAtSF"], 0.005),
            (label + " fails atm", got["failsAtAtm"], row["failsAtAtm"], 0.005),
            (label + " SF identity", got["marginAtSF"],
             got["failsAtAtm"] / vc.LATTICE_SF, 1e-12),
        ]

    # Independent face enumeration: 12 HH and 24 HS edges, with the dihedral angles derived
    # from their outward normals rather than copied from the load helper.
    pairs = face_edge_topology()
    kinds = [tuple(sorted(face[0] for face in pair)) for pair in pairs]
    ok += [("whole edges enumerated", len(pairs), 36, 0),
           ("hexagon-hexagon edges", kinds.count(("hexagon", "hexagon")), 12, 0),
           ("hexagon-square edges", kinds.count(("hexagon", "square")), 24, 0)]
    hs_pair = next(pair for pair in pairs if tuple(sorted(x[0] for x in pair))
                   == ("hexagon", "square"))
    normals = [x[1] for x in hs_pair]
    cos_normals = sum(a * b for a, b in zip(*normals)) / math.sqrt(
        sum(a * a for a in normals[0]) * sum(b * b for b in normals[1]))
    theta_hs = math.pi - math.acos(cos_normals)
    ok.append(("HS interior angle deg", math.degrees(theta_hs), 125.2643897, 1e-6))

    panels = face_panels(1.0, 2)
    pitch = panels["pitch"]
    # Two <110> directions within x=constant are perpendicular pitch-long sides.
    d1, d2 = (0, 1, 1), (0, 1, -1)
    ok += [("square face directions", sum(a * b for a, b in zip(d1, d2)), 0, 0),
           ("square panel inradius", panels["squareInradius"], pitch / 2.0, 1e-12)]
    loads = film_line_loads(1.0, 2)
    ok.append(("square load equilibrium", loads["coplanar square"],
               vc.P_ATM * pitch / 2.0, 1e-9))

    t_hex, sin_a = vc.panel_tension(panels["hexInradius"])
    t_square, _ = vc.panel_tension(panels["squareInradius"])
    delta = theta_hs - 2.0 * math.asin(sin_a)
    vector_hs = math.hypot(t_hex + t_square * math.cos(delta),
                           t_square * math.sin(delta))
    cosine_hs = math.sqrt(t_hex ** 2 + t_square ** 2
                          + 2.0 * t_hex * t_square * math.cos(delta))
    ok += [("HS vector equilibrium", loads["hexagon-square edge"], vector_hs, 1e-9),
           ("HS cosine identity", loads["hexagon-square edge"], cosine_hs, 1e-9)]

    m2 = film_bending(1.0, 2, section(10, 1))["cases"]["hexagon-square edge"]["momentNm"]
    m4 = film_bending(1.0, 4, section(10, 1))["cases"]["hexagon-square edge"]["momentNm"]
    ok += [("film moment cube law", m2 / m4, 8.0, 1e-10),
           ("film mass pitch law", film_kg(1.0, 2) / film_kg(1.0, 4), 2.0, 1e-10)]

    # Keep finite-article purchasing separate from the 96*n^3 periodic crush identity.
    # Hard-coded enumerated counts and the expanded pitch formula independently gate both
    # total cut length and mass for a fixed reference section.
    reference_area = section(10, 1)["area"]
    for n, expected_struts in ((2, 948), (4, 6840)):
        expected_length = expected_struts / (2.0 * math.sqrt(2.0) * n)
        ok += [(f"physical struts at n={n}",
                vc.kelvin_lattice_counts(n)["struts"], expected_struts, 0),
               (f"article cut length n={n}", article_tube_length(1.0, n),
                expected_length, 1e-12),
               (f"article tube mass n={n}", article_tube_kg(1.0, n, reference_area),
                expected_length * reference_area * MAT["rho"], 1e-12)]
    print("SELF-CHECK against the model's own arithmetic")
    good = True
    for name, got, want, tol in ok:
        hit = abs(got - want) <= tol
        good &= hit
        print(f"  {'ok ' if hit else 'BAD'} {name:24s} {got:12.3f}  expected {want:10.3f}")
    print(f"  => {'consistent with the model' if good else 'DOES NOT RECONCILE — stop'}\n")
    if good:
        print("  n=1 film bending reproduces film_edge_loads' rim/spoke rows")
        print("  general-n moment ratio M(n)/M(2n) = 8.000 (cube of pitch)\n")
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
    axial_best = None
    for od in ODS_MM:
        for w in WALLS_MM:
            if od - 2 * w < 0.8:
                continue
            sec = section(od, w)
            euler = math.pi ** 2 * MAT["E"] * sec["inertia"] / length ** 2
            local = (vc.K_LOCAL * vc.ORTHO_PENALTY * 0.605 * MAT["E"]
                     * (w / 1000) / sec["ro"]) * sec["area"]
            axial = MAT["sigma"] * sec["area"]
            if min(euler, local, axial) < force:
                continue
            bend = film_bending(span, n, sec)
            phi = phi_of(span, n, sec["area"])
            tube = article_tube_kg(span, n, sec["area"])
            joint = nodes * NODE_G_AT_10MM / 1000 * (od / 10) ** 3
            film = film_kg(span, n)
            total = tube + joint + film
            candidate = dict(totalKg=total, tubeKg=tube, jointKg=joint, filmKg=film,
                             odMm=od, wallMm=w, strutMm=length * 1000, nodes=nodes,
                             struts=c["struts"], phi=phi, kgPerM3=total / volume,
                             overWall=total / volume / WALL_KG_M3,
                             eulerMargin=euler / force, localMargin=local / force,
                             yieldMargin=axial / force, filmBending=bend)
            if axial_best is None or total < axial_best["totalKg"]:
                axial_best = candidate
            if bend["marginAtSF"] < 1.0:
                continue
            if best is None or total < best["totalKg"]:
                best = candidate
    if best:
        best["axialOnly"] = axial_best
        best["filmSafe"] = True
        return best
    if axial_best:
        return {"axialOnly": axial_best, "filmSafe": False}
    return None


def main():
    if not self_check():
        return 1
    print("ARTICLE A — EVEN SUBDIVISION ONLY. Odd n keeps the separately sized boundary frame.")
    print("Each even-n tube holds independent Euler, local, yield and film-bending checks at")
    print("SF 1.5; combined axial-bending interaction and joint bearing remain unmodelled.\n")
    print(f"{'span':>5} {'n':>2} {'nodes':>6} {'strut':>8} {'OD x wall':>15} {'phi':>9} "
          f"{'tube':>6} {'joint':>6} {'film':>5} {'kg/m3':>7} {'Euler':>6} {'local':>6} "
          f"{'yield':>6} {'film@SF1.5':>11}")
    results = {}
    missing = []
    for span in (1.0, 2.0, 3.0, 4.0, 6.0):
        for n in (2, 4):
            b = best_article(span, n)
            if not b:
                print(f"{span:5.1f} {n:2d}   no tube in the catalogue holds the axial checks")
                missing.append((span, n))
                continue
            if not b["filmSafe"]:
                old = b["axialOnly"]
                fb = old["filmBending"]
                print(f"{span:5.1f} {n:2d}   NO FILM-SAFE SKU; axial winner "
                      f"{old['odMm']:.1f}x{old['wallMm']:.2f} mm has film margin "
                      f"{fb['marginAtSF']:.2f} at SF 1.5 and fails at "
                      f"{fb['failsAtAtm']:.2f} atm ({fb['case']})")
                missing.append((span, n))
                continue
            results[(span, n)] = b
            print(f"{span:5.1f} {n:2d} {b['nodes']:6d} {b['strutMm']:7.0f}mm "
                  f"{b['odMm']:7.1f} x {b['wallMm']:4.2f}mm {b['phi']:9.6f} "
                  f"{b['tubeKg'] / (span ** 3 / 2):6.2f} {b['jointKg'] / (span ** 3 / 2):6.2f} "
                  f"{b['filmKg'] / (span ** 3 / 2):5.2f} {b['kgPerM3']:7.2f} "
                  f"{b['eulerMargin']:6.2f} {b['localMargin']:6.2f} {b['yieldMargin']:6.2f} "
                  f"{b['filmBending']['marginAtSF']:11.2f}")
        print()

    if missing:
        rows = ", ".join(f"span {span:.1f}/n={n}" for span, n in missing)
        print(f"STOP: no complete film-safe publication set ({rows}).")
        return 2

    print("FILM-DRIVEN RESIZING (the axial-only winner fails; both margins are shown)")
    for (span, n), b in results.items():
        old = b["axialOnly"]
        fb = old["filmBending"]
        if (old["odMm"], old["wallMm"]) == (b["odMm"], b["wallMm"]):
            print(f"  article A, span {span:.1f}, n={n}: survives on "
                  f"{b['odMm']:.1f}x{b['wallMm']:.2f} mm; film margin {fb['marginAtSF']:.2f}")
        else:
            print(f"  article A, span {span:.1f}, n={n}: {fb['case']}, axial-only "
                  f"{old['odMm']:.1f}x{old['wallMm']:.2f} mm has film margin "
                  f"{fb['marginAtSF']:.2f} at SF 1.5 and fails at {fb['failsAtAtm']:.2f} atm; "
                  f"resized to {b['odMm']:.1f}x{b['wallMm']:.2f} mm -> "
                  f"{b['kgPerM3']:.2f} kg/m3")

    published_rows = ((1.0, 2), (2.0, 2), (4.0, 2), (3.0, 4), (6.0, 4))
    print("\nPUBLICATION SUMMARY — article A, values copied to FLOAT.md")
    print("  span n nodes strut_mm OD_mm wall_mm tube_kgm3 joint_kgm3 film_kgm3 "
          "total_kgm3 over_wall Euler local yield film_SF1.5 governor")
    for key in published_rows:
        span, n = key
        b = results[key]
        vol = span ** 3 / 2
        print(f"  {span:.1f} {n} {b['nodes']} {b['strutMm']:.0f} {b['odMm']:.1f} "
              f"{b['wallMm']:.2f} {b['tubeKg']/vol:.2f} {b['jointKg']/vol:.2f} "
              f"{b['filmKg']/vol:.2f} {b['kgPerM3']:.2f} {b['overWall']:.2f} "
              f"{b['eulerMargin']:.2f} {b['localMargin']:.2f} {b['yieldMargin']:.2f} "
              f"{b['filmBending']['marginAtSF']:.2f} {b['filmBending']['case']}")
    best_key = min(published_rows, key=lambda k: results[k]["overWall"])
    best = results[best_key]
    print(f"  best documented row: span {best_key[0]:.1f}, n={best_key[1]}, "
          f"{best['kgPerM3']:.2f} kg/m3 = {best['overWall']:.2f}x wall")
    print(f"\nthe wall is {WALL_KG_M3:.4f} kg/m3. None of the checked rows floats.")
    print("R1 tube sizing is no longer an axial-only floor: film bending is included at SF 1.5.")
    print("The totals remain lower bounds because these positive mass lines are NOT YET COUNTED:")
    print("  bond adhesive; seam tape; aluminium barrier coating; fasteners; jig-induced overlength")
    print("Estimate/source uncertainties (not zero-mass lines):")
    print("  even-n joint valence/geometry is unvalidated; tube catalogue is invented")
    return 0


if __name__ == "__main__":
    sys.exit(main())
