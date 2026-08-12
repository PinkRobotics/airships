#!/usr/bin/env python3
"""The vacuum cell, designed from first principles.

    python3 research/analysis/vacuum-cell.py [--json OUT]

The hull is an array of permanently sealed vacuum cells, with machinery in ambient bays
between them. An interior wall in such an array has vacuum on BOTH sides and carries no
pressure differential — the atmosphere is held only at the boundary. That is what this file
is about, because it changes which physics governs.

WHAT THE ARRAY BUYS. A monolithic vacuum balloon fails by global shell buckling, and for a
SINGLE-LAYER shell that is an impossibility result no material escapes (Akhmeteli & Gavrilin:
a perfect diamond sphere collapses at ~0.2 atm). Fill the volume instead and there is no thin
shell: the array is a cellular solid in hydrostatic compression, and what governs is its
crushing strength. (A reviewer derives that the filled array also beats an
optimally-proportioned lattice SHELL by about 25%, because strength is superlinear in relative
density so concentrating material into a shell wastes it. That is a better argument than "no
shell left to buckle" and it is NOT reproduced here — an attempt at it produced nonsense and
was removed rather than published.)

WHAT IT DOES NOT BUY. The material requirement. One atmosphere still crosses a solid fraction
of a few parts in ten thousand.

THE DESIGN RESULT. At floating densities struts buckle rather than yield, so strength goes as
phi^2 for solid rods and the arithmetic collapses. Hollow struts, proportioned so Euler and
local wall buckling fail together, restore phi^1.5. Jenett et al. use hollow tubes too, at a
FIXED R/t = 10 — which puts local buckling far out of reach, so their tubes recover the phi^2
law. The optimum R/t is an order of magnitude higher, and that proportion is what the mass
turns on. That, and not "they assumed away buckling", is the contribution: Jenett explicitly
discusses the strength-exponent shift and bounds his claim to relative densities above 1e-3.

WHERE IT LANDS. Corrected for laminate rather than fibre properties, for the orthotropic tube
wall, for node mass, for a lattice safety factor and for the interior sealing film, the
reference design sits AT the wall rather than comfortably inside it. Which side it falls on is
decided by choices this analysis has not yet made. It is published that way on purpose.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
FIGURES = ROOT / "research" / "figures.json"

P_ATM = 101325.0

# Octet truss (Deshpande, Fleck & Ashby 2001): phi = 6*sqrt(2)*pi*(r/l)^2.
C_PHI = 6.0 * math.sqrt(2.0) * math.pi

# UNDER HYDROSTATIC LOAD THIS IS EXACT, not an estimate, and it does not depend on topology:
# every strut in any stretch-dominated truss takes the same affine strain, so the stress in
# the solid is 3p/phi. An earlier version apologised for it as an approximation.
ALIGN = 1.0 / 3.0

# Local buckling of a thin cylinder in axial compression, as a fraction of the classical
# 0.605*E*t/R. NASA SP-8007 at these proportions gives about 0.33, so 0.3 is mildly
# conservative for an ISOTROPIC wall. See ORTHO_PENALTY for what a composite wall does.
K_LOCAL = 0.3

# Imperfection knockdown for a monolithic shell under external pressure.
K_SHELL = 0.2

# THE CORRECTION THAT DECIDED THE ANSWER. Local buckling of an ORTHOTROPIC tube depends on
# sqrt(E_axial * E_hoop), not the axial modulus alone — bending stiffness along the tube
# combines with hoop membrane stiffness. Through the co-critical optimisation the governing
# modulus becomes E_x^(3/4) * E_theta^(1/4). For a [0/90] laminate putting a fraction f of the
# fibre axially that is E_1 * f^(3/4) * (1-f)^(1/4), maximised at f = 3/4:
ORTHO_PENALTY = 0.75 ** 0.75 * 0.25 ** 0.25          # 0.5699

# Internal surface of a space-filling cell array, per m3, times cell size. 3.0 for cubes.
CELL_AREA_COEFF = 3.0

# Nodes join twelve tubes and carry no load themselves, so their solid raises phi without
# raising capacity. 10-30% is the usual range; 15% is the working figure.
NODE_MASS_FRAC = 0.15

# Every strut sits exactly at its Euler load, all of them at once, so the buckling mode is
# near-degenerate — the worst case for imperfection sensitivity, and the direct analogue of
# the knockdown the monolithic branch already gets. An earlier version applied none at all.
LATTICE_SF = 1.5


MATERIALS = {
    "M60J_LAM": dict(
        name="M60J UD laminate, Vf 0.6", E=354e9, sigma=2.29e9, rho=1658,
        orthotropic=True, printable=False,
        source="Toray M60JB FIBRE is 588 GPa / 3.82 GPa / 1930 kg/m3. A laminate at 60% fibre "
               "volume is roughly 354 GPa / 2.29 GPa / 1658. Jenett et al. quote the fibre "
               "figures as though they were composite figures and this project inherited that; "
               "the laminate numbers are what a part is actually made of."),
    "T700_LAM": dict(
        name="T700 UD laminate, Vf 0.6", E=135e9, sigma=2.50e9, rho=1600,
        orthotropic=True, printable=False,
        source="Standard-modulus aerospace prepreg, laminate values."),
    "CFF": dict(
        name="Continuous carbon fibre, printed (Markforged-class)", E=60e9, sigma=800e6,
        rho=1400, orthotropic=True, printable=True,
        source="Representative published values. NOT vendor-verified in this session."),
    "PAHT_XY": dict(
        name="Bambu PAHT-CF, in-plane (X-Y)", E=3.86e9, sigma=92e6, rho=1060,
        orthotropic=True, printable=True,
        source="Bambu Lab PAHT-CF TDS, ISO 527: 3860 +/- 230 MPa, 92 +/- 7 MPa, 1.06 g/cm3."),
    "PAHT_Z": dict(
        name="Bambu PAHT-CF, interlayer (Z)", E=2.18e9, sigma=47e6, rho=1060,
        orthotropic=True, printable=True,
        source="Same TDS, Z direction: 2180 +/- 130 MPa, 47 +/- 5 MPa. THE DIRECTION THAT "
               "GOVERNS a printed pressure vessel."),
    "TI64": dict(
        name="Ti-6Al-4V, laser powder-bed sintered", E=114e9, sigma=1.10e9, rho=4430,
        orthotropic=False, printable=True,
        source="Representative LPBF values, stress-relieved. Isotropic, so it takes no "
               "orthotropic penalty — the one advantage metal has here."),
    "AEROGEL": dict(
        name="Silica aerogel, monolithic", E=10e6, sigma=0.5e6, rho=120,
        orthotropic=False, printable=True,
        source="Order-of-magnitude literature values. Included to test the internal-support "
               "idea, not as a shell candidate; its numbers fall outside the thin-wall "
               "assumptions every relation here makes."),
}


def isa_temperature(alt_m: float) -> float:
    return 288.15 - 0.0065 * alt_m


def isa_pressure(alt_m: float) -> float:
    return 101325.0 * (isa_temperature(alt_m) / 288.15) ** (9.80665 / (287.05 * 0.0065))


def rho_air(alt_m: float) -> float:
    """ISA troposphere density: rho_SL * (T/T0)^(g/(L*R) - 1)."""
    return (101325.0 / (287.05 * 288.15)) * \
        (isa_temperature(alt_m) / 288.15) ** (9.80665 / (287.05 * 0.0065) - 1.0)


def e_eff(m: dict) -> float:
    """The modulus that governs local buckling of this material's tube wall."""
    return m["E"] * (ORTHO_PENALTY if m["orthotropic"] else 1.0)


def material_index(m: dict) -> float:
    """E_eff^(2/3)/rho — the property that decides every buckling-governed row.

    NOT specific strength: rho_shell is exactly inversely proportional to this.
    """
    return e_eff(m) ** (2.0 / 3.0) / m["rho"]


def arch_monolithic(m: dict, p: float = P_ATM) -> dict:
    nu = 0.3
    t_over_r = math.sqrt(p * math.sqrt(3 * (1 - nu * nu)) / (2 * K_SHELL * m["E"]))
    return {"architecture": "monolithic shell", "latticeKgPerM3": 3.0 * m["rho"] * t_over_r,
            "governs": "shell buckling"}


def arch_solid_strut(m: dict, p: float = P_ATM) -> dict:
    k = ALIGN * math.pi ** 2 / (4.0 * C_PHI)
    pd = p * LATTICE_SF
    phi_b = math.sqrt(pd / (k * m["E"]))
    phi_y = pd / (ALIGN * m["sigma"])
    phi = max(phi_b, phi_y)
    return {"architecture": "solid-strut lattice", "phi": phi,
            "latticeKgPerM3": phi * m["rho"],
            "governs": "strut buckling" if phi_b > phi_y else "material yield"}


# THE BUILT ARTICLE'S GEOMETRY, PINNED (2026-08-12). Every article-A row used to re-read
# the live co-critical chain on each run — fine while the chain's physics was frozen.
# Landing the classical 0.605 local-buckling coefficient (audit O1) moves the chain's
# optimum to ~0.55 m span, but the demonstrator is BUILT at the pre-correction point:
# sawn, printed, frozen in the manifest and the contract. A built object's size is a
# measurement, not a derivation — same doctrine as the weighed joints and the sawn cut
# table — so the exact chain outputs it was cut from are pinned here, and the corrected
# chain's own optimum is a finding about FUTURE articles, not this one's identity.
DEMO_STRUT_PINNED_M = 0.2505065525376105     # the 0.6 mm x 2 design-point strut
DEMO_PITCH_PINNED_M = 0.35426976406201705    # sub-cell pitch; span = 2x = 708.53953 mm
DEMO_TUBE_R_PINNED_M = 0.016604417467399196  # the printed tube radius it was drawn at


def arch_tube_strut(m: dict, p: float = P_ATM) -> dict:
    """Hollow struts, each tube proportioned so Euler and local wall buckling coincide."""
    ee = e_eff(m)
    a = 2.0 * K_LOCAL / math.pi ** 2
    c = 2.0 * C_PHI * a
    k = ALIGN * K_LOCAL / math.sqrt(c)
    pd = p * LATTICE_SF
    phi_b = (pd / (k * ee)) ** (2.0 / 3.0)
    phi_y = pd / (ALIGN * m["sigma"])
    phi = max(phi_b, phi_y)
    psi = math.sqrt(phi / c)
    lam = math.sqrt(a * psi)
    return {"architecture": "tubular-strut lattice", "phi": phi,
            "latticeKgPerM3": phi * m["rho"],
            "governs": "strut buckling" if phi_b > phi_y else "material yield",
            "wallOverTubeRadius": psi, "tubeRadiusOverStrutLength": lam,
            "wallThicknessPerStrutLength": psi * lam, "tubeROverT": 1.0 / psi,
            "eEffPa": ee}


ARCHS = {"monolithic": arch_monolithic, "solidStrut": arch_solid_strut,
         "tubeStrut": arch_tube_strut}


def barrier_kg_per_m2(cell_span_m: float, sigma_f: float = 5.8e9, rho_f: float = 1560,
                      sf: float = 4.0, eff: float = 0.5, bulge: float = 0.25) -> float:
    a = cell_span_m / 2.0
    h = bulge * a
    r_bulge = (a * a + h * h) / (2.0 * h)
    return rho_f * (P_ATM * r_bulge / (2.0 * (sigma_f / sf * eff)))


def kelvin_faces(span: float) -> dict:
    """A truncated octahedron's edge and areas, from its span across the square faces.

    THE EDGE IS span/(2*sqrt2), NOT span/4. Two functions wrote span/4 and understated
    every film area by exactly a factor of two — a review and the designer's own geometry
    question caught it on the same afternoon. The tell is decisive: the wrong area,
    0.8415 m2 at the demonstrator's span, is LESS than the equal-volume sphere's 1.531 m2,
    which no shape can be. The project's own cell_shapes() coefficient (2.6574) already
    encoded the right value, so the two halves of the model disagreed with each other.
    """
    a = span / (2.0 * math.sqrt(2.0))
    return {"edgeM": a,
            "hexM2": 3.0 * math.sqrt(3.0) / 2.0 * a * a,
            "sqM2": a * a,
            "areaM2": (6.0 + 12.0 * math.sqrt(3.0)) * a * a,
            "areaOverVolume": (6.0 + 12.0 * math.sqrt(3.0)) * a * a / (span ** 3 / 2.0)}


# Panel inradius as a fraction of the cell EDGE, per bracing scheme. The barrier function
# wants a panel "span" of twice the inradius — the same convention the unbraced hexagon
# always used (it was handed the across-flats, i.e. twice the apothem).
PANEL = {
    "hexUnbraced": math.sqrt(3.0) / 2.0,          # apothem of the hexagon
    "hexSpoked": 1.0 / (2.0 * math.sqrt(3.0)),    # 6 equilateral triangles, side = edge
    "squareSpoked": 1.0 / (2.0 + math.sqrt(2.0)),  # 4 triangles: the in-plane ties already
}                                                  # brace every square face — see below


def film_kg(span: float, hex_scheme: str = "hexSpoked") -> float:
    """Film mass for one article, priced PER FACE TYPE at the panel each face actually has.

    The old single-span pricing charged every square metre at the hexagon's span. Squares
    are smaller and — the discovery that made the hexagon question sharp — they are ALREADY
    braced: 24 of the 48 vertex ties lie exactly in the square face planes, dividing each
    square into four triangles. The hexagons had nothing, which is precisely what the
    designer saw.
    """
    f = kelvin_faces(span)
    a = f["edgeM"]
    return (8.0 * f["hexM2"] * barrier_kg_per_m2(2.0 * PANEL[hex_scheme] * a)
            + 6.0 * f["sqM2"] * barrier_kg_per_m2(2.0 * PANEL["squareSpoked"] * a))


def panel_tension(panel_inradius: float, p: float = P_ATM) -> tuple[float, float]:
    """Membrane tension in one bulged panel, and the sine of its tilt off the face plane.

    A bulge of h = 0.25 a on a panel of inradius a is a spherical cap of radius
    (a^2 + h^2)/2h, so T = p*R/2 and the film meets its own boundary tilted below the face
    by alpha with sin(alpha) = a/R — 0.4707 here, and INDEPENDENT of panel size because R
    scales with a. Both callers need the pair: film_edge_loads resolves the out-of-plane
    part into bending, member_demands resolves the in-plane part into axial. It is one
    function because it was nearly two, and two copies of the bulge geometry is exactly the
    failure this file's parity gate exists to catch.
    """
    r_bulge = (panel_inradius ** 2 + (0.25 * panel_inradius) ** 2) / (
        2.0 * 0.25 * panel_inradius)
    return p * r_bulge / 2.0, panel_inradius / r_bulge


def face_shares(span: float, p: float = P_ATM) -> dict:
    """Each panel's pressure resultant, split equally among the corners that carry it.

    A bulged panel hands its frame exactly p * (flat panel area) along the inward face
    normal, whatever shape the bulge takes — the in-plane parts of the membrane pull are
    self-equilibrated within the panel and are member_demands' other load set. The hexagons
    are cut into six triangles by their spokes and the squares into four by their in-plane
    ties, so a corner takes a third of each triangle it belongs to: the hub is a corner of
    all six triangles (H/3) and each hexagon vertex of two (H/9); the square centre of all
    four (Q/3) and each square vertex of two (Q/6).
    """
    f = kelvin_faces(span)
    h, q = p * f["hexM2"], p * f["sqM2"]
    return {"hexFaceN": h, "sqFaceN": q,
            "hexToHubN": h / 3.0, "hexToVertexN": h / 9.0,
            "sqToCentreN": q / 3.0, "sqToVertexN": q / 6.0}


def member_demands(span: float, sf: float = LATTICE_SF, p: float = P_ATM) -> dict:
    """WHAT EACH FAMILY REACTS. Every axial demand in the article, from its own load path.

    THE BUG THIS REPLACES, and WHY IT SURVIVED SO LONG. One number, 3*p*SF*V/(96*L), was
    published as "perStrutDemandN" and handed to every member in the article. The comment
    beside it read "96 = 60 octet + 36 rim" — and that IS a true member count: before the
    spokes existed the article held exactly 96 long members. But it is not what the divisor
    means, and the two 96s are unrelated. Read as a member count it sent the crush demand to
    the rim, which cannot carry crush, and it made the 48 spokes look like an omission to be
    corrected by writing 144. check_assembly called the spokes' inherited number fabricating
    a numerator, and it was; the rim's was fabricated the same way and nobody had noticed,
    because the arithmetic came out right for the wrong reason.

    DO NOT "FIX" THE 96 TO 144. The divisor is the phi in sigma = 3p/phi, so it counts the
    octet lattice's own strut-lengths per Kelvin-cell VOLUME, and that is exactly 96: the
    lattice is FCC at half-pitch, so it runs 3 struts per cubic half-pitch, and a cell of
    span 4 half-pitches encloses 32 of them. (Clip the infinite lattice against the cell and
    the measure is 102 strut-lengths, of which the 6 lying IN the six square faces belong
    equally to the cell above — 96 again.) weightless_article's boundary surcharge counts
    against the same 96. Putting 144 there would dilute the octet's stress with members that
    are not in the octet, and this article's numbers would stop agreeing with the array's,
    which is the one thing the demonstrator exists to prove.

    WHAT THE ARTICLE ACTUALLY CARRIES, in two load sets that do not mix:

    1. CRUSH, the hydrostatic field of the array. Carried by the octet, and only by the
       octet: the rim, spokes and ties are the odd-n boundary apparatus, which does not
       exist at even n where the same octet carries the same crush (see
       kelvin_lattice_counts on why the hexagon planes are bare only at odd n). The 24 rim
       vertices are dual-lattice sites, so not one rim member is an octet strut — the rim
       could never have had a share of this.

    2. THE FILM, which only a standalone article has. Each panel's pull splits into a
       normal resultant (face_shares) and a self-equilibrated in-plane pull q = T*cos(alpha)
       along each of its edges. The normal set has an exact reaction, node by node:
         - the hexagon hub's H/3 goes out through 3 <100> props at 54.74 deg, so each takes
           H/(3*sqrt(3)) = p*a^2/2;
         - a rim vertex takes H/9 from each of two hexagons plus Q/6 from one square, and
           its two ties span that vector exactly — the <100> prop takes p*a^2/2 (the same
           number again, reached independently) and the in-plane square tie p*a^2/3;
         - the square centre IS an octet node and its Q/3 enters through 4 struts at 45 deg
           at p*a^2/(6*sqrt(2)) each. That is the only crush an octet strut sees in the
           STANDALONE article, and it is a third of the array's demand — worth knowing
           before strain gauges go on a single cell expecting the array's number.
       The in-plane set is reacted inside each face, and here the path is INDETERMINATE:
       a vertex's radial tributary can go inward along that face's spoke (or in-plane tie)
       or around the ring as hoop in the rim. Both are sized for the whole of it, which is
       the standard envelope and the only honest thing to do without solving the frame.

    WHAT IS NOT IN HERE. Bending — film_edge_loads owns that and it governs the rim.
    Redistribution by stiffness: these are statically admissible envelopes, checked once
    against a linear pin-jointed solve of all 216 members under the same two load sets. The
    tripod prop is exact, the spoke and the ties sit just above the solve, the rim
    comfortably above it, and the octet's array crush is far above what a standalone
    article puts through it.
    """
    f = kelvin_faces(span)
    a = f["edgeM"]                        # the cell edge IS the strut length, by construction
    vol = span ** 3 / 2.0
    t_tri, sin_a = panel_tension(PANEL["hexSpoked"] * a, p)
    t_sq, _ = panel_tension(PANEL["squareSpoked"] * a, p)
    cos_a = math.sqrt(1.0 - sin_a ** 2)
    q_hex, q_sq = t_tri * cos_a, t_sq * cos_a      # in-plane pull per metre of edge

    crush = 3.0 * p * sf * vol / (96.0 * a)        # sigma = 3p/phi, phi = 96*A*a/V
    pa2 = p * sf * a * a
    prop = pa2 / 2.0                               # hub tripod AND rim-vertex inward tie
    tie_in_plane_normal = pa2 / 3.0                # the square's share at a rim vertex
    octet_entry = pa2 / (6.0 * math.sqrt(2.0))     # Q/3 through 4 struts at 45 deg
    # A vertex's radial tributary is the two half-edges either side of it, resolved along
    # the radius: sqrt(3)/2 * q * a in a hexagon (the two edges 30 deg off radial), q*a/sqrt2
    # in a square (45 deg off). Hoop is the same load taken the other way round the ring,
    # where the kink at a vertex turns 2N*cos(60) = N loose in a hexagon and 2N*cos(45) in a
    # square, so a hexagon ring's hoop equals its spoke's thrust and a square's is smaller.
    spoke = sf * math.sqrt(3.0) / 2.0 * q_hex * a
    sq_radial = sf * q_sq * a / math.sqrt(2.0)
    hex_hoop, sq_hoop = spoke, sf * q_sq * a / 2.0
    # A rim edge belongs to two faces and both rings can want their hoop in it. Twelve of the
    # 36 edges are hexagon-hexagon and take two hexagon rings; the other 24 are square-hexagon.
    rim_hh, rim_sh = 2.0 * hex_hoop, hex_hoop + sq_hoop
    vertex_tie_in_plane = tie_in_plane_normal + sq_radial

    fam = {
        "octet": (crush, "crush: 3*p*SF*V/(96*L), the octet's own hydrostatic share. The "
                         "standalone article only puts %.0f N through it (Q/3 at a square "
                         "centre through 4 struts at 45 deg); this is the array's load, "
                         "which is what the demonstrator exists to prove."
                  % round(octet_entry)),
        "rim": (rim_hh, "film, in-plane: hoop for the two hexagon rings a hexagon-hexagon "
                        "edge belongs to. A square-hexagon edge takes %.0f N. No crush "
                        "share: the rim vertices are dual sites and no rim member is an "
                        "octet strut." % round(rim_sh)),
        "spoke": (spoke, "film, in-plane: the hexagon's radial tributary, sqrt(3)/2 * q * a "
                         "with q = T*cos(alpha) = %.0f N/m. Bending governs it, not this "
                         "(film_edge_loads rows 3 and 4)." % round(q_hex)),
        "tripodProp": (prop, "film, normal: the hub's H/3 through 3 <100> props at 54.74 "
                             "deg = p*a^2/2. Exact — nothing else at a hub can take it."),
        "vertexTieInward": (prop, "film, normal: a rim vertex's 2*H/9 + Q/6 resolves onto "
                                  "its <100> prop as p*a^2/2, the same value as the hub's "
                                  "tripod reached independently."),
        "vertexTieInPlane": (vertex_tie_in_plane,
                             "film: the square's share of a rim vertex, p*a^2/3, plus the "
                             "square panel's in-plane radial tributary q*a/sqrt(2). The "
                             "largest short-member demand in the article."),
    }
    short = max(fam[k][0] for k in ("tripodProp", "vertexTieInward", "vertexTieInPlane"))
    return {
        "note": "one demand per family, each from the load it reacts. 96 is the octet's "
                "strut count per Kelvin-cell volume, not a member count of this article.",
        "safetyFactor": sf,
        "crushDivisor": 96,
        # RAW newtons, never rounded here. stock_build divides capacities by these to get
        # its margins and cell/model.js does the same arithmetic on its own side; rounding
        # on one side only is the divergence the parity gate has already caught twice.
        "families": {k: {"axialN": v, "from": why} for k, (v, why) in fam.items()},
        "crushPerOctetStrutN": crush,
        "octetStandaloneEntryN": octet_entry,
        "rimSquareHexEdgeN": rim_sh,
        "hexRingHoopN": hex_hoop, "sqRingHoopN": sq_hoop,
        "inPlanePullHexNPerM": q_hex, "inPlanePullSqNPerM": q_sq,
        "governingShortMemberN": short,
        # The other half of a node-equilibrium check: what the film hands each node
        # DIRECTLY, at the same safety factor as the member demands. check_assembly
        # modelled the hexagon hubs only and had to say so; these are the rest.
        "externalFilmShareAtSF": {k: v * sf for k, v in face_shares(span, p).items()},
    }


def film_edge_loads(span: float, sf: float = LATTICE_SF,
                    scheme: str = "hexSpoked") -> dict:
    """THE CHECK THIS MODEL DID NOT HAVE — boundary members in BENDING, and it governs.

    Every strength claim in this project was axial: 96 struts at 3,372 N, 119 MPa in a
    10x8 pipe, x21 on stress. But the film does not push on the lattice, it pulls on the
    BOUNDARY FRAME, transversely, and a review computed the consequence: the rim reaches
    ultimate somewhere around one atmosphere. The article's governing stress was sixteen
    times the one being published.

    The load needs no membrane theory, only equilibrium: a boundary member carries
    w = p * (tributary width), the pressure on the panel area that drains to it. Panels
    are split equally among their edges — crude, transparent, and conservative for the
    long edge of a non-equilateral panel.

    Bending is why bracing works so well: M ~ w L^2 with w ~ panel size and L ~ panel size,
    so the moment falls as the CUBE of the bracing pitch. It is also why an in-plane spoke
    is only half an answer — it collects the membrane beautifully and then has to carry
    the load in bending itself. Propping the midspan out of plane, into the octet behind,
    is what actually converts the problem back into compression.
    """
    f = kelvin_faces(span)
    a = f["edgeM"]
    p = P_ATM

    def tube(od, idd):
        ro, ri = od / 2.0, idd / 2.0
        return {"od": od, "idd": idd,
                "Z": (math.pi / 4.0 * (ro ** 4 - ri ** 4)) / ro,
                "I": math.pi / 4.0 * (ro ** 4 - ri ** 4),
                "kgPerM": math.pi * (ro ** 2 - ri ** 2) * MATERIALS["T700_LAM"]["rho"]}

    pipe = tube(0.010, 0.008)
    sigma_u = MATERIALS["T700_LAM"]["sigma"]

    def row(name, w, length, sec, propped=False):
        span_eff = length / 2.0 if propped else length
        m_pin = w * span_eff ** 2 / 8.0
        m_cl = w * span_eff ** 2 / 12.0
        s_pin, s_cl = m_pin / sec["Z"], m_cl / sec["Z"]
        return {"member": name, "lineLoadNPerM": round(w),
                "spanM": round(span_eff, 4),
                "momentPinnedNm": round(m_pin, 1), "momentClampedNm": round(m_cl, 1),
                "stressPinnedMPa": round(s_pin / 1e6), "stressClampedMPa": round(s_cl / 1e6),
                "marginPinnedAtSF": round(sigma_u / (s_pin * sf), 2),
                "marginClampedAtSF": round(sigma_u / (s_cl * sf), 2),
                "failsAtAtm": round(sigma_u / s_pin, 2)}

    # THE LINE LOAD, and the geometry of the corner matters. Each panel's film pulls on a
    # boundary member along its own surface tangent, tilted below the face plane by alpha,
    # with sin(alpha) = a_panel/R — which is 0.4707 at the model's bulge, INDEPENDENT of
    # panel size. For two COPLANAR panels (a spoke inside a face) the in-plane components
    # cancel and only 2*T*sin(alpha) is left. At a DIHEDRAL edge they do not cancel: they
    # sum along the inward bisector, and the rim load is roughly twice what a tributary-
    # area estimate gives. Getting this wrong is what let the rim look survivable.
    def tension(panel_inradius):
        return panel_tension(panel_inradius, p)                 # T, sin(alpha)

    def dihedral(t1, t2, sin_a, theta):
        """Vector sum of two membrane pulls across a dihedral of interior angle theta."""
        cos_a = math.sqrt(1.0 - sin_a ** 2)
        half = theta / 2.0
        return math.hypot((t1 + t2) * math.cos(half - math.asin(sin_a)),
                          (t1 - t2) * math.sin(half - math.asin(sin_a))) if False else \
            math.hypot((t1 + t2) * math.cos(half) * cos_a + (t1 + t2) * math.sin(half) * sin_a,
                       0.0)

    th_hh = math.acos(-1.0 / 3.0)             # hexagon-hexagon dihedral, 109.47 deg
    t_bare, sa = tension(PANEL["hexUnbraced"] * a)
    t_tri, _ = tension(PANEL["hexSpoked"] * a)
    t_sq, _ = tension(PANEL["squareSpoked"] * a)
    w_bare = dihedral(t_bare, t_bare, sa, th_hh)
    w_rim = dihedral(t_tri, t_tri, sa, th_hh)
    w_spoke = 2.0 * t_tri * sa                # coplanar: only the out-of-plane part
    w_sqtie = 2.0 * t_sq * sa

    rows = [
        row("rim edge, hexagons UNBRACED (the design as it stood)", w_bare, a, pipe),
        row("rim edge, hexagons spoked, 10x8", w_rim, a, pipe),
        row("rim edge, hexagons spoked, 14x12", w_rim, a, tube(0.014, 0.012)),
        row("hexagon spoke, 10x8 (two coplanar panels)", w_spoke, a, pipe),
        row("hexagon spoke, midspan-propped", w_spoke, a, pipe, True),
        row("in-plane square tie (two coplanar panels)", w_sqtie, a / math.sqrt(2.0), pipe),
    ]
    hub = face_shares(span, p)["hexToHubN"]       # the hub's share, through its 6 spokes
    return {
        "note": "w = p * tributary width; bending governs the boundary, axial governs the "
                "interior. The unbraced rim is the article's true first failure.",
        "hexFaceLoadN": round(p * f["hexM2"]),
        "squareFaceLoadN": round(p * f["sqM2"]),
        # Summed over the whole surface — eight hexagons AND six squares. The page once
        # quoted the squares' subtotal as the article's, which the designer caught.
        "hexFaces": 8, "squareFaces": 6,
        "totalSurfaceLoadN": round(p * f["areaM2"]),
        "totalSurfaceLoadTf": round(p * f["areaM2"] / 9806.65, 1),
        "rows": rows,
        "hubShareN": round(hub),
        # Three <100> props at 54.74 deg to the face normal: sum of axial components is
        # 3*cos(54.74) = sqrt(3), so each carries F/sqrt(3) — NOT F/3.
        "tripodPropN": round(hub / math.sqrt(3.0)),
        "tripodPropNAtSF": round(hub / math.sqrt(3.0) * sf),
        # WHAT A FLAT PAD CAN AND CANNOT DO. The designer asked for a pad so the film is
        # carried over an area instead of a point, and he is right about the failure it
        # prevents — a point in a 16-micron film is a puncture. But a pad can only collect
        # what the film's tension hands it around its own perimeter, 2*pi*r*T*sin(theta),
        # and at any buildable size that is a small fraction of the hub's share. The pad is
        # therefore LOCAL PROTECTION, not a load path: the spokes carry the hub's load.
        "padDiaMm": round(2000.0 * PAD_R_M),
        "padCollectsN": round(2.0 * math.pi * PAD_R_M
                              * (barrier_kg_per_m2(2.0 * PANEL["hexSpoked"] * a) / 1560.0)
                              * (5.8e9 / 4.0 * 0.5) * 0.4707),
        "padWouldNeedDiaMmForHubShare": round(2000.0 * hub / (
            2.0 * math.pi * (barrier_kg_per_m2(2.0 * PANEL["hexSpoked"] * a) / 1560.0)
            * (5.8e9 / 4.0 * 0.5) * 0.4707)),
        # THE BUOYANCY TAX NOBODY WAS COUNTING. Every panel bulges INWARD by h = 0.25a,
        # and that dimple is open to the atmosphere: the article displaces less air than
        # its outline suggests. On the bench it is cosmetic; on a flight article, where
        # mass and displaced air are equal by construction, it is a direct cut in lift —
        # and it is the strongest argument for bracing there is, stronger than film mass.
        "bulgeVolumeLostL": round(1000.0 * (
            8.0 * f["hexM2"] * 0.25 * PANEL[scheme] * a / 2.0
            + 6.0 * f["sqM2"] * 0.25 * PANEL["squareSpoked"] * a / 2.0), 1),
        "bulgeVolumeLostPct": round(100.0 * (
            8.0 * f["hexM2"] * 0.25 * PANEL[scheme] * a / 2.0
            + 6.0 * f["sqM2"] * 0.25 * PANEL["squareSpoked"] * a / 2.0)
            / (span ** 3 / 2.0), 1),
        "bulgeVolumeLostUnbracedPct": round(100.0 * (
            8.0 * f["hexM2"] * 0.25 * PANEL["hexUnbraced"] * a / 2.0
            + 6.0 * f["sqM2"] * 0.25 * PANEL["squareSpoked"] * a / 2.0)
            / (span ** 3 / 2.0), 1),
    }


PAD_R_M = 0.035          # the printed film pad on each hexagon hub — local protection


def barrier_kg_per_m3(cell_span_m: float) -> float:
    """THE TERM THIS MODEL COMPUTED AND DID NOT COUNT, until a review caught it.

    Individually sealed cells mean the film is the array's INTERNAL surface, about 3/l m2 per
    m3. Its areal mass grows with the span it bulges across exactly as fast as area-per-volume
    falls, so the product is SCALE-FREE — the same at every cell size, if every partition is
    sized to hold an atmosphere. It is comparable to the lattice itself, and it is Metlen's
    0.37 W/B membrane penalty arriving by another road.

    There is an escape and it has a price: partitions at minimum gauge cost almost nothing and
    do NOT contain a breach, because the neighbour's film is not sized for the atmosphere a
    flooded cell puts against it. That trade is the sharpest open question in the design.
    """
    return barrier_kg_per_m2(cell_span_m) * CELL_AREA_COEFF / cell_span_m


def total_shell(m: dict, cell_span_m: float, p: float = P_ATM,
                film: bool = True, nodes: float = NODE_MASS_FRAC) -> dict:
    t = arch_tube_strut(m, p)
    bar = barrier_kg_per_m3(cell_span_m) if film else 0.0
    return {"latticeKgPerM3": t["latticeKgPerM3"],
            "nodesKgPerM3": t["latticeKgPerM3"] * nodes,
            "filmKgPerM3": bar,
            "totalKgPerM3": t["latticeKgPerM3"] * (1.0 + nodes) + bar,
            "detail": t}


def hierarchy_ladder(m: dict, levels: int = 5, film: float | None = None,
                     nodes: float = NODE_MASS_FRAC) -> dict:
    """STRUCTURE INSIDE STRUCTURE, which is the path rather than a curiosity.

    Each level of self-similar hierarchy improves the strength-versus-density EXPONENT, and
    the exponent is what everything here turns on. A solid rod gives sigma* ~ phi^2. Make the
    rod a tube and it is phi^1.5. Make the tube's wall itself a lattice and it is phi^4/3.
    With n levels the exponent is (n+2)/(n+1), and the limit is LINEAR — which is exactly the
    scaling Jenett et al. assume. Hierarchy is therefore the MECHANISM by which their
    assumption becomes true, not a contradiction of it.

    Reference for the ladder: Lakes, "Materials with structural hierarchy", Nature 361 (1993).

    The practical news is that it converges fast. The second level is the one that matters:
    it takes the reference design from under the wall to comfortably over it.
    """
    ee = e_eff(m)
    a = 2.0 * K_LOCAL / math.pi ** 2
    c = 2.0 * C_PHI * a
    k = ALIGN * K_LOCAL / math.sqrt(c)
    pd = P_ATM * LATTICE_SF
    x = pd / (k * ee)
    # The yield cap a review caught this ladder omitting: whatever buckling permits, the
    # SOLID still has to carry 3p/phi without breaking, so phi can never fall below
    # pd/(ALIGN*sigma) — the same cap arch_tube_strut applies. Levels 3 and 4 hit it for
    # every material here: hierarchy's returns end where the material's strength begins.
    phi_yield = pd / (ALIGN * m["sigma"])
    if film is None:
        film = envelope_film_kg_per_m3()
    names = ["solid rod", "hollow tube", "tube of tubes", "third order", "fourth order"]
    out = {}
    for n in range(levels):
        alpha = (n + 2) / (n + 1)
        phi_b = x ** (1.0 / alpha)
        phi = max(phi_b, phi_yield)
        lat = phi * m["rho"]
        tot = lat * (1.0 + nodes) + film
        out[str(n)] = {"levels": n, "exponent": round(alpha, 4), "phi": phi,
                       "latticeKgPerM3": round(lat, 4),
                       "totalKgPerM3": round(tot, 4),
                       "yieldCapped": phi_yield > phi_b,
                       "solidStressOverStrength": round(3.0 * pd / phi / m["sigma"], 3),
                       "name": names[n] if n < len(names) else f"order {n}",
                       "note": "each level costs joints, tolerance and inspection; the "
                               "coefficient degrades even as the exponent improves"}
    return out


# The reference hull the film arithmetic uses throughout: the right-sized P-100 from
# mass-budget.py. 220,000 m3 of enclosed volume behind 22,592 m2 of outer envelope.
HULL_VOLUME_M3 = 220000.0
HULL_ENVELOPE_M2 = 22592.0


def envelope_film_kg_per_m3(span_m: float = 2.0, datm: float = 1.0) -> float:
    """The outer envelope's film, priced for the job it actually has.

    An earlier version charged 0.0171 kg/m2 here — a number with no source that a review
    traced to nothing, for a surface that must hold a FULL ATMOSPHERE over unsupported cell
    spans. Priced by the model's own membrane function, an atmosphere-rated boundary film
    over 2 m spans costs 0.232 kg/m2 = 0.0238 kg/m3 of hull — twelve times what was charged,
    and as-was, NOTHING in the 'envelope only' option was holding the atmosphere at all.

    Two honest levers remain, and both are design choices rather than corrections:
    finer boundary cells (film mass is span-proportional), and the graded band, which
    divides `datm` by the number of steps — that is where grading genuinely earns its keep.
    """
    return barrier_kg_per_m2(span_m) * datm * HULL_ENVELOPE_M2 / HULL_VOLUME_M3


def shared_wall(cell_span_m: float) -> dict:
    """How much of the array's wall area is interior — vacuum on both sides, carrying nothing.

    This is the number the whole architecture stands on, and it was quoted on the page before
    it was generated anywhere. Interior area is CELL_AREA_COEFF/span per m3; the envelope is
    fixed by the hull. At 2 m cells, 93.6% of all wall area carries no pressure differential.
    """
    interior = CELL_AREA_COEFF / cell_span_m * HULL_VOLUME_M3
    return {"cellSpanM": cell_span_m,
            "interiorM2": round(interior),
            "envelopeM2": HULL_ENVELOPE_M2,
            "interiorOverEnvelope": round(interior / HULL_ENVELOPE_M2, 1),
            "sharedFractionPct": round(100.0 * interior / (interior + HULL_ENVELOPE_M2), 1)}


# Space-filling cell shapes: shared-wall area per m3 of array, normalised by cell volume^(1/3)
# so shapes are compared at equal enclosed volume. The cube's 3.0 is what CELL_AREA_COEFF uses
# everywhere — deliberately conservative. The interlocking "sphere-like" block the design
# intends is the truncated octahedron (the Kelvin cell), and it is 11.4% better: Kelvin posed
# equal-volume space partition as a minimum-area problem in 1887 and this shape held the record
# until Weaire & Phelan improved it by 0.3% in 1994. The design gets that saving for free,
# because minimum film area and "as close to a sphere as tessellation allows" are the same ask.
def cell_shapes() -> dict:
    out = {}
    def entry(name, vol_coeff, area_coeff, note):
        # coeff = (shared area / volume) * volume^(1/3), with shared = total face area / 2.
        c = (area_coeff / 2.0) / vol_coeff * vol_coeff ** (1.0 / 3.0)
        out[name] = {"coeff": round(c, 4),
                     "filmSavingVsCubePct": round(100.0 * (1.0 - c / 3.0), 1),
                     "note": note}
    entry("cube", 1.0, 6.0, "the analysis baseline: CELL_AREA_COEFF = 3.0")
    entry("rhombicDodecahedron", 16.0 * math.sqrt(3.0) / 9.0, 8.0 * math.sqrt(2.0),
          "FCC Voronoi cell — the natural partition around octet-truss nodes")
    entry("truncatedOctahedron", 8.0 * math.sqrt(2.0), 6.0 + 12.0 * math.sqrt(3.0),
          "the Kelvin cell: BCC Voronoi, 8 hexagons + 6 squares, the interlocking "
          "near-sphere the design describes")
    wp = out["truncatedOctahedron"]["coeff"] * (1.0 - 0.003)
    out["weairePhelan"] = {"coeff": round(wp, 4),
                           "filmSavingVsCubePct": round(100.0 * (1.0 - wp / 3.0), 1),
                           "note": "0.3% below Kelvin (Weaire & Phelan 1994) — the known "
                                   "record; two cell shapes, harder to print for 0.3%"}
    return out


def printer_chain(m: dict) -> dict:
    """Nozzle -> extrusion width -> wall -> strut -> cell, for the printed demonstrator.

    The optimum tube wall is a FIXED FRACTION of the strut length (the co-critical
    proportion), so the thinnest wall a printer lays reliably sets the smallest cell that is
    at the right proportions. Wall = perimeters x nozzle width, taking extrusion width equal
    to the nozzle bore — the conservative floor of the usual 100-120% practice.

    Chopped carbon abrades brass and bridges a 0.4 mm orifice, so 0.6 mm hardened steel is
    the reliable choice for a shop running many machines, and two perimeters is the thinnest
    wall that closes into a leak-checkable surface. That row is the design point. The octet
    cell edge is sqrt(2) x strut.
    """
    t = arch_tube_strut(m)
    wps = t["wallThicknessPerStrutLength"]
    rows = {}
    for nozzle_mm, perims in ((0.4, 2), (0.6, 2), (0.6, 3), (1.0, 2)):
        wall_mm = nozzle_mm * perims
        strut = wall_mm / 1000.0 / wps
        cell = strut * math.sqrt(2.0)
        rows[f"{nozzle_mm:.1f} mm x {perims}"] = {
            "nozzleMm": nozzle_mm, "perimeters": perims,
            "wallMm": round(wall_mm, 2),
            "strutM": round(strut, 3),
            "cellM": round(cell, 3),
            # Unrounded, for downstream arithmetic — the parity gate caught the
            # demonstrator priced from ROUNDED struts on this side and raw on the JS side.
            "cellMRaw": cell,
            "strutMRaw": strut,
            "tubeRadiusMRaw": t["tubeRadiusOverStrutLength"] * strut,
            "enclosedL": round(cell ** 3 * 1000.0),
            "tubeRadiusMm": round(t["tubeRadiusOverStrutLength"] * strut * 1000.0, 1),
        }
    return {"material": m["name"], "rows": rows,
            "designPoint": "0.6 mm x 2",
            "bedFitNote": "251 mm struts fit a 256 mm consumer bed with no splicing.",
            "tubeROverT": round(t["tubeROverT"], 1)}


def kelvin_lattice_counts(n: int = 1) -> dict:
    """The Kelvin demonstrator's lattice, counted exactly (mirrored in cell/model.js).

    Fill a Kelvin cell of span 2p with the octet grid at pitch p: every coordinate is a
    multiple of p/2, so in those units the nodes are the integer triples with
    max|u| <= 2 and |ux|+|uy|+|uz| <= 3, and the struts are the <110>-step pairs inside.
    Boundary nodes (either bound met with equality) are where the skin is bonded — the
    half-pitch grid contains the BCC points, so they land exactly in the faces.
    """
    lim = 2 * n

    # FCC ONLY: coordinate sum EVEN. The first version admitted every integer triple,
    # which is TWO interleaved octet lattices — twice the design density. The parity gate's
    # ratio test caught it converging to 2.0 instead of 1.0, and the "heavy-looking
    # lattice" a viewer complained about was partly this phantom twin.
    def inside(u):
        a, b, c = abs(u[0]), abs(u[1]), abs(u[2])
        return max(a, b, c) <= lim and a + b + c <= 3 * n and (u[0] + u[1] + u[2]) % 2 == 0

    nodes = [(x, y, z) for x in range(-lim, lim + 1) for y in range(-lim, lim + 1)
             for z in range(-lim, lim + 1) if inside((x, y, z))]
    steps = []
    for a, b in ((1, 1), (1, -1)):
        steps += [(a, b, 0), (a, 0, b), (0, a, b)]
    struts = sum(1 for u in nodes for s in steps
                 if inside((u[0] + s[0], u[1] + s[1], u[2] + s[2])))
    boundary = sum(1 for u in nodes
                   if max(abs(u[0]), abs(u[1]), abs(u[2])) == lim
                   or abs(u[0]) + abs(u[1]) + abs(u[2]) == 3 * n)
    # The RIM FRAME: the octet has no nodes in the hexagon faces (their centres are the
    # dual lattice's sites), so the article's skin is framed by printed members along its
    # own 36 edges — and a Kelvin edge at span 2np is exactly n strut-lengths long, so the
    # rim prints as the same struts. 24 rim vertices join them.
    #
    # VERTEX TIES — a load path the DESIGNER caught missing (2026-08-10). The 24 rim
    # vertices are permutations of (0, +-n, +-2n): coordinate sum ODD, every one — dual
    # sites, like the hexagon centres. The rim cage therefore never touched the octet;
    # the two structures shared only the 6 square-centre nodes ("only touches the face
    # on the points of a cube", verbatim). A standalone article's skin pulls on the rim
    # with p*R/2-scale line loads, so the rim MUST tie inward: 2 ties per vertex to its
    # nearest even-parity sites. At n=1 those are the <100> half-steps (length p/2,
    # e.g. (0,1,2)->(0,0,2) and (0,1,2)->(0,1,1)); at n>=2 the half-steps land on odd
    # sites and the nearest even sites are <110> steps (full strut length). Equivalents
    # are length-weighted at the same section — a fixed 48-member cost per article,
    # vanishing as 1/n^3 in the array but real money at N=1.
    tie_equiv = 48.0 / math.sqrt(2.0) if n == 1 else 48.0
    # HEXAGON SUPPORT — the designer's second catch, same day: after the vertex ties the
    # eight hexagon faces were still bare membrane spans. Their centres, permutations of
    # (+-n,+-n,+-n), have coordinate sum 3n: at EVEN n they are real lattice sites and the
    # face is node-centred for free; at ODD n (the demonstrator's n=1) they are dual sites
    # and the face gets a deliberate dual-site node plus a TRIPOD of three <100> half-step
    # ties to its even neighbours ((n-1,n,n)-class, sum 3n-1, even exactly when n is odd).
    # The tripod also halves the skin's unsupported span (film prices at half across-flats
    # now) and gives mating cells a shared bond point at every hexagon centre.
    #
    # PARITY DECIDES WHETHER A BOUNDARY FRAME IS NEEDED AT ALL, and this is the single most
    # useful thing the counting knows. A hexagon face lies in the plane sum(s*u) = 3n. At
    # ODD n that sum is odd, so the plane contains NO even-parity site whatsoever: the face
    # is bare, and the article must carry its own rim, hub, spokes and ties. At EVEN n the
    # plane is full of lattice sites — face centres, edge midpoints, a triangular grid at
    # the lattice's own pitch — so the film bonds straight onto the octet and the whole
    # boundary apparatus disappears. The floater should therefore be an EVEN-n article;
    # n = 1 is the awkward case, and it is the one we are building on the bench.
    odd = (n % 2 == 1)
    hex_nodes = 8 if odd else 0
    hex_ties = 24 if odd else 0
    hex_equiv = (hex_ties / math.sqrt(2.0)) if odd else 0.0
    # HEXAGON SPOKES — the designer's third catch: the square faces were already braced
    # in plane (24 of the 48 vertex ties lie exactly in the square face planes, cutting
    # each square into four triangles) while the eight hexagons had nothing at all. Six
    # radial spokes per face fix that, and they are the same cut as every primary: the
    # hexagon's circumradius IS the lattice's strut length.
    hex_spokes = 48 if odd else 0
    hex_spoke_equiv = float(48 * n) if odd else 0.0
    return {"struts": struts, "nodes": len(nodes), "boundaryNodes": boundary,
            "rimStrutEquivalents": (36 * n) if odd else 0, "rimNodes": 24 if odd else 0,
            "tieStruts": 48 if odd else 0,
            "tieStrutEquivalents": tie_equiv if odd else 0.0,
            "hexNodes": hex_nodes, "hexTieStruts": hex_ties,
            "hexTieStrutEquivalents": hex_equiv,
            "hexSpokeStruts": hex_spokes, "hexSpokeStrutEquivalents": hex_spoke_equiv,
            "boundaryFrameNeeded": odd}


def demonstrator(m: dict) -> dict:
    """The printable proof-of-concept cell: one octet unit cell at the 0.6 mm x 2 design point.

    WHAT IT DEMONSTRATES AND WHAT IT DOES NOT. A PAHT-CF lattice is ~22x the buoyancy wall at
    ANY size — relative density is scale-free, so no printed-nylon cell floats, ever. What the
    demonstrator proves is everything else the architecture claims: that struts and nodes
    print on stock consumer hardware at the co-critical proportions, assemble into a cell,
    take a barrier, pump down, SEAL, hold vacuum against permeation for months, and carry a
    full atmosphere with the margin the model predicts (the sizing already carries
    LATTICE_SF = 1.5, so at sea level the crush margin IS the safety factor). Strain gauges
    on the struts against the model's predicted stress is the experiment; buoyancy is not.
    Buoyancy needs the flight material (wound or pultruded aerospace CF) and level-2
    hierarchy — the demonstrator is the architecture at arm's length, not the vehicle.
    """
    t = arch_tube_strut(m)
    chain = printer_chain(m)["rows"]["0.6 mm x 2"]
    p = DEMO_PITCH_PINNED_M              # the built article's pitch, pinned — see above
    # THE ARTICLE IS NOT A CUBE. The design's cell is the interlocking near-sphere, and
    # the half-pitch meshing makes it buildable from the exact same parts: a Kelvin cell
    # of span 2p, filled with the SAME co-critical struts at pitch p, boundary nodes
    # landing exactly in the faces, skin bonded on them. An earlier version printed one
    # cubic octet cell — the analyst's convenience, not the design — and the designer
    # asked "why is it a cube" within a day of seeing it.
    span = 2.0 * p
    vol = span ** 3 / 2.0                # BCC packs two Kelvin cells per span^3
    counts = kelvin_lattice_counts()
    r_m = DEMO_TUBE_R_PINNED_M
    wall_m = chain["wallMm"] / 1000.0
    strut_kg = 2.0 * math.pi * r_m * wall_m * DEMO_STRUT_PINNED_M * m["rho"]
    # Octet interior + the rim frame along the article's 36 edges (each exactly one strut
    # long at N = 1 — the Kelvin edge IS the lattice spacing) + the 48 vertex ties and
    # 24 hexagon-tripod ties the designer caught missing: without the first the rim is a
    # structural island, without the second the big faces are bare membrane spans.
    n_struts = counts["struts"] + counts["rimStrutEquivalents"]
    lat_kg = (n_struts + counts["tieStrutEquivalents"]
              + counts["hexTieStrutEquivalents"]
              + counts["hexSpokeStrutEquivalents"]) * strut_kg
    nodes_kg = lat_kg * NODE_MASS_FRAC
    area_m2 = kelvin_faces(span)["areaM2"]
    # Priced per face type, at the panel each face actually has now that the hexagons are
    # spoked. The old single-span pricing also used an area that was exactly half the
    # truth — see kelvin_faces.
    film_kg_ = film_kg(span)
    displaced = 1.225 * vol              # sea level, where the demonstrator lives
    total_kg = lat_kg + nodes_kg + film_kg_
    return {
        "material": m["name"],
        "strutM": round(DEMO_STRUT_PINNED_M, 3), "cellM": round(DEMO_PITCH_PINNED_M, 3),
        "spanM": round(span, 3), "enclosedL": round(vol * 1000.0),
        "wallMm": chain["wallMm"],
        "tubeRadiusMm": round(DEMO_TUBE_R_PINNED_M * 1000.0, 1),
        # The BUILT article's proportion, from its own pinned radius and wall — not the
        # live optimum's, which the 0.605 correction is free to move.
        "tubeROverT": round(DEMO_TUBE_R_PINNED_M / wall_m, 1),
        "printedStruts": (n_struts + counts["tieStruts"] + counts["hexTieStruts"]
                          + counts["hexSpokeStruts"]),
        "printedNodes": counts["nodes"] + counts["rimNodes"] + counts["hexNodes"],
        "octetStruts": counts["struts"], "rimStruts": counts["rimStrutEquivalents"],
        "tieStruts": counts["tieStruts"], "hexTieStruts": counts["hexTieStruts"],
        "hexNodes": counts["hexNodes"],
        "boundaryNodes": counts["boundaryNodes"],
        "inArrayShareKg": round(t["phi"] * m["rho"] * vol * (1.0 + NODE_MASS_FRAC)
                                + film_kg_, 3),
        "latticeKg": round(lat_kg, 3),
        "nodesKg": round(nodes_kg, 3),
        "filmKg": round(film_kg_, 3),
        "totalKg": round(total_kg, 3),
        "displacedAirKg": round(displaced, 3),
        "massOverDisplaced": round(total_kg / displaced, 1),
        # WHY THIS SIZE, AND WHY IT IS NOT "THE WEIGHTLESS SIZE": weightlessness is a
        # DENSITY property, not a size — a printed-nylon lattice is ~20x air at every
        # size, and the level-2 flight article is lighter than air at every size its
        # walls can be made. Size here is set by the nozzle chain alone; the article's
        # job is proportions, assembly, seal and margin. The weightless prototype is the
        # same geometry in flight-grade material at level 2, and E5 is its gate.
        "crushMarginAtSeaLevelAtLeast": LATTICE_SF,
        "floats": False,
        "measures": ["print yield and dimensional tolerance at 251 mm",
                     "assembly and joint integrity at the 12-tube nodes",
                     "skin bonding at the boundary-node grid",
                     "vacuum retention: pump-down, seal, months-long pressure log",
                     "strut strain under full atmosphere against the model's 3p/phi",
                     "creep at permanent load in the matrix-dominated directions",
                     "breach behaviour of an instrumented sub-volume"],
    }


def article_film_kg_per_m3(n: int, pitch: float = 0.3545) -> float:
    """The standalone article's film, per cubic metre, and PARITY DECIDES THE SCALING.

    The old term was wrong twice over. It carried the span/4 area error (a factor of two),
    and then divided by n a second time although the quantity it computed was already
    scale-free — the docstring argued that panels stay one pitch wide while the code
    priced them at a fraction of the whole article's span. Both cannot be true.

    Which one IS true depends on parity, and that is the useful part. At EVEN n the
    hexagon faces are full of lattice sites, so the film bonds to the octet at the
    lattice's own pitch: the panel stays one cell wide however big the article grows, and
    the film term falls as 1/n exactly as area-per-volume does. At ODD n the faces are
    bare and the only bracing is the six spokes per face, so the panels grow WITH the
    article and the film term is scale-free — no reward at all for building bigger.
    """
    span = 2.0 * n * pitch
    f = kelvin_faces(span)
    if n % 2 == 0:
        # lattice-braced: the panel is a cell-sized triangle whatever the article's size
        a1 = 2.0 * pitch / (2.0 * math.sqrt(2.0))
        return (f["areaM2"] * barrier_kg_per_m2(2.0 * PANEL["hexSpoked"] * a1)
                / (span ** 3 / 2.0))
    return film_kg(span) / (span ** 3 / 2.0)


def weightless_article(wall: float) -> dict:
    """Could a sealed article of this design actually weigh ZERO? Yes — sized here.

    The designer's question, asked verbatim of the demonstrator: "if evacuated and sealed
    somehow, in theory could be of zero weight?" The ladder's kg/m3 figures are IN-ARRAY
    densities; a standalone sealed article pays a boundary surcharge — its skin struts and
    nodes are shared with nobody — of about 2.1x at one cell, falling toward 1 as the
    article grows. So each rung has a MINIMUM WEIGHTLESS SIZE, counted here exactly from
    the same integer lattice the demonstrator uses, at N sub-cells of half-span per side.

    The outer film term is SCALE-FREE per N (a film's areal mass grows with the panel span
    exactly as fast as area-per-volume falls): barrier(p) * (A/V) = 1.674 * barrier(1 m) / N,
    about 0.19/N kg/m3, independent of the material's pitch.

    Sea level is the natural demo condition — air is 1.225 kg/m3 there, 28% more buoyant
    than the 2,500 m wall — and the demo is a bench, not a ship.
    """
    net_per_n3 = 96.0                    # net strut-equivalents per article at N=1 is 96*N^3
    rungs = [("PAHT_Z", 4, "all-printed nylon"),
             ("CFF", 3, "continuous fibre, printed"),
             ("T700_LAM", 2, "T700, wound"),
             ("M60J_LAM", 2, "M60J-class, wound")]
    out = {"filmAtN1KgPerM3": round(article_film_kg_per_m3(1), 4),
           "filmAtN2KgPerM3": round(article_film_kg_per_m3(2), 4),
           "rows": {}}
    for key, level, label in rungs:
        lad = hierarchy_ladder(MATERIALS[key], film=0.0)
        # phi is carried raw; latticeKgPerM3 is rounded for display — the parity gate
        # caught this side computing from the rounded copy.
        lat = lad[str(level)]["phi"] * MATERIALS[key]["rho"] * (1.0 + NODE_MASS_FRAC)
        found_sl, found_alt = None, None
        table = {}
        for n in range(1, 13):
            c = kelvin_lattice_counts(n)
            ratio = (c["struts"] + c["rimStrutEquivalents"] + c["tieStrutEquivalents"]
                     + c["hexTieStrutEquivalents"]
                     + c["hexSpokeStrutEquivalents"]) / (net_per_n3 * n ** 3)
            rho = lat * ratio + article_film_kg_per_m3(n)
            table[str(n)] = round(rho, 3)
            if found_sl is None and rho < 1.225:
                found_sl = n
            if found_alt is None and rho < wall:
                found_alt = n
        out["rows"][key] = {
            "label": label, "level": level,
            "densityAtN1": table["1"],
            "minNSeaLevel": found_sl, "minNAt2500m": found_alt,
            "note": "N is sub-cells of half-span per side; the article spans 2N pitches "
                    "across its squares. Pitch depends on the material's thinnest wall, "
                    "so size in metres is set by that wall, not by this table.",
        }
    return out


# THE SAW SCHEDULE, measured. Nine seat-to-seat cut lengths from the frozen joint
# manifest (research/geometry/nodes/manifest.json cutList, sunken-frame freeze of
# 2026-08-11) — the tube the article actually saws. Centre-to-centre stays the physics
# length (Euler spans, demands); BILLING at it was P14's standing finding: 48.8 m billed
# where the saw table says 39.8. Like NODE_MASS_MEASURED_KG this is a measured constant,
# and check_assembly's P14 holds every row to the live manifest, so a regrow that moves
# one cut goes red there instead of going stale here.
CUT_SCHEDULE_MEASURED = (
    ("octet", 211.183, 24), ("octet", 216.846, 24), ("octet", 221.500, 12),
    ("rim", 202.778, 24), ("rim", 203.877, 12),
    ("spoke", 206.142, 48),
    ("tie", 129.770, 24), ("tie", 134.376, 24), ("tie", 139.025, 24),
)


def stock_build() -> dict:
    """The HYBRID article: purchased carbon pipe mains, printed everything else.

    The designer's question that reframed the build (2026-08-10): "could this be
    assembled mainly from CF stock and 3d printed connectors??" Yes — and the design had
    already converged on it without saying so: 144 of the article's 216 members are the same
    251 mm cut, the nodes are already printed sockets that a pipe end seats
    into, and catalogue tube IS the T700_LAM row — stock delivers real laminate properties,
    which no chopped-fibre print does. ROLL-WRAPPED, not pultruded: a pultrusion is
    all-axial fibre, and this model has assumed a cross-plied wall from the day
    ORTHO_PENALTY was written (0.75^0.75 * 0.25^0.25 is the value for 3/4 axial, 1/4
    hoop). Specifying pultruded tube would have contradicted our own physics by 0.65x
    on the local-buckling capacity the co-critical proportion depends on — and would
    split at the socket, where the spigot presses outward on a wall with no hoop fibre. Same span as the printed article, so one
    geometry serves both.

    TWO SKUs, TWO CUTS — and the designer was right for the wrong reason. He proposed
    replacing the printed ties with a SMALLER carbon pipe. Carbon yes; smaller no. Sized
    against the load they actually carry — the film's inward pull, which member_demands
    resolves onto them node by node — the ties come out ABOVE the octet's own crush demand:
    they are the most heavily loaded members in the article, and a 6 x 4 pipe Euler-buckles
    at half their demand. So it is 10 x 8 roll-wrapped tube everywhere except the 36 rim
    edges, which the film's dihedral pull puts in bending and which take 14 x 12, cut to
    251 mm (60 octet + 36 rim + 48 hexagon spokes) or 177 mm (72 ties). 1.69 kg of printed
    plastic becomes 0.58 kg of carbon and gets stronger doing it.

    Node mass is now MEASURED, not budgeted: gen_nodes.py integrates each printed joint
    from its own SDF and the manifest is read here. The 15% NODE_MASS_FRAC survives only
    where it belongs, in the in-array kg/m3 rows, labelled as the assertion it is.
    """
    m = MATERIALS["T700_LAM"]
    p = DEMO_PITCH_PINNED_M              # the built article's pitch, pinned
    span = 2.0 * p
    vol = span ** 3 / 2.0
    L = DEMO_STRUT_PINNED_M
    counts = kelvin_lattice_counts()
    # ONE DEMAND PER FAMILY, each from the load path that puts it there. This used to be a
    # single 3*pd*vol/(96*L) handed to all 216 members; see member_demands for why 96 is
    # right for the octet and wrong for everyone else.
    dem = member_demands(span)
    fam = dem["families"]
    f_demand = fam["octet"]["axialN"]
    ro, ri = 0.010 / 2.0, 0.008 / 2.0               # 10 x 8 mm roll-wrapped, catalogue
    area = math.pi * (ro ** 2 - ri ** 2)
    inertia = math.pi / 4.0 * (ro ** 4 - ri ** 4)
    pcr_pinned = math.pi ** 2 * m["E"] * inertia / L ** 2
    pcr_socketed = pcr_pinned / 0.65 ** 2
    kg_per_m = area * m["rho"]
    # TWO SKUs, and the second one is the rim. The film's pull at a dihedral edge is
    # roughly twice what it is along a spoke inside a flat face — the two panels' in-plane
    # tensions add across the corner instead of cancelling — so the 36 cell edges carry
    # 13.9 kN/m and a 10 x 8 tube is only good to 1.33 atmospheres there. 14 x 12 takes it
    # to 2.84. Everything else stays on the single 10 x 8 SKU.
    rim_ro, rim_ri = 0.014 / 2.0, 0.012 / 2.0
    rim_kg_per_m = math.pi * (rim_ro ** 2 - rim_ri ** 2) * m["rho"]
    rim_cuts = counts["rimStrutEquivalents"]
    # 251 mm on the 10 x 8 SKU: the octet interior and the hexagon spokes. Written as
    # "96 - rim_cuts + spokes" until 2026-08-11, which reached the right 108 by subtracting
    # the rim frame from a number that never contained it (see member_demands on the 96).
    long_cuts = counts["struts"] + counts["hexSpokeStruts"]
    short_cuts = counts["tieStruts"] + counts["hexTieStruts"]        # 177 mm: every tie
    # BILL THE SAW TABLE, NOT THE SPANS. The article buys 39.8 m of tube, not 48.8:
    # every cut is shorter than its centre-to-centre span by both joints' seats, which
    # the prover measures. The spans keep doing the physics below; the bill is the saw's.
    sawn_main_m = sum(mm * n for f, mm, n in CUT_SCHEDULE_MEASURED if f != "rim") / 1000.0
    sawn_rim_m = sum(mm * n for f, mm, n in CUT_SCHEDULE_MEASURED if f == "rim") / 1000.0
    pipe_kg = kg_per_m * sawn_main_m + rim_kg_per_m * sawn_rim_m
    nodes_kg = measured_node_mass_kg()
    skin_kg = film_kg(span)
    total = pipe_kg + nodes_kg + skin_kg
    displaced = 1.225 * vol
    loads = film_edge_loads(span)
    # ALL 72 SHORT MEMBERS ARE SIZED AT THE WORST OF THEM, which is no longer the hexagon
    # tripod prop. The 24 in-plane square ties carry the square's share of a rim vertex AND
    # that panel's in-plane radial pull, and the sum is above the prop's p*a^2/2.
    tie_demand = dem["governingShortMemberN"]
    rim_demand = fam["rim"]["axialN"]
    spoke_demand = fam["spoke"]["axialN"]
    pcr_tie = math.pi ** 2 * m["E"] * inertia / (L / math.sqrt(2.0)) ** 2
    rim_inertia = math.pi / 4.0 * (rim_ro ** 4 - rim_ri ** 4)
    pcr_rim = math.pi ** 2 * m["E"] * rim_inertia / L ** 2
    return {
        "spanM": round(span, 3), "enclosedL": round(vol * 1000.0),
        "pipe": {"sku": "10 x 8 mm ROLL-WRAPPED CF tube, [0/+-45/90], T700-class — 180 members",
                 "odM": 2.0 * ro, "idM": 2.0 * ri, "rimOdM": 2.0 * rim_ro,
                 "count": long_cuts + rim_cuts + short_cuts,
                 "longCuts": long_cuts, "memberLongM": round(L, 3),
                 "rimCuts": rim_cuts, "rimSku": "14 x 12 mm roll-wrapped — the film's dihedral edge",
                 "shortCuts": short_cuts, "memberShortM": round(L / math.sqrt(2.0), 3),
                 # Two lengths, two jobs: the spans do physics, the saw table gets billed.
                 "memberLengthM": round((long_cuts + rim_cuts) * L
                                        + short_cuts * L / math.sqrt(2.0), 1),
                 "sawnM": round(sawn_main_m + sawn_rim_m, 3),
                 "sawnRows": len(CUT_SCHEDULE_MEASURED),
                 "kg": round(pipe_kg, 3),
                 # perStrutDemandN is the OCTET's demand and nothing else's. Every family's
                 # own number is in demands below; reading this one for a rim or a spoke is
                 # the defect that made the article's margins agree by accident.
                 "perStrutDemandN": round(f_demand),
                 "eulerMarginPinned": round(pcr_pinned / f_demand, 2),
                 "eulerMarginSocketed": round(pcr_socketed / f_demand, 2),
                 "stressMargin": round(m["sigma"] * area / f_demand, 1),
                 "rimDemandN": round(rim_demand),
                 "rimEulerMargin": round(pcr_rim / rim_demand, 2),
                 "spokeDemandN": round(spoke_demand),
                 "spokeEulerMargin": round(pcr_pinned / spoke_demand, 2),
                 "tieDemandN": round(tie_demand),
                 "tieEulerMargin": round(pcr_tie / tie_demand, 2)},
        "printed": {"nodes": counts["nodes"] + counts["rimNodes"] + counts["hexNodes"],
                    "nodesKg": round(nodes_kg, 3),
                    "nodesMeasured": nodes_kg != round(pipe_kg * NODE_MASS_FRAC, 6)},
        "skinKg": round(skin_kg, 3),
        "totalKg": round(total, 3),
        # THE ARTICLE IN THE UNIT THE WALL IS WRITTEN IN, generated rather than typed. The note
        # quoted this cell at 16.06 kg/m3 for a fortnight after the per-arm SKU fix moved the
        # joints from 0.444 to 0.465 kg, because it was hand-arithmetic with nothing holding it
        # to the build. It is the only figure in the stock build that says whether the article
        # is anywhere near floating, so it is the last one that should have been typed.
        "kgPerM3": round(total / vol, 2),
        "displacedAirKg": round(displaced, 3),
        "massOverDisplaced": round(total / displaced, 1),
        "governingCheck": loads["rows"][2],       # the rim at its own SKU
        "floats": False,
        "note": "the crush-test pathfinder, and the article whose boundary is now sized "
                "for the film load that governs it rather than for crush alone",
    }


def measured_node_mass_kg() -> float:
    """The printed joints, weighed by the generator that draws them.

    NODE_MASS_FRAC = 0.15 was the largest unsourced number left in the project. It is a
    fraction of STRUT mass, which is dimensionally the wrong parameterisation — a node's
    mass is set by how many arms it has, not by how much pipe hangs off it. gen_nodes.py
    integrates every joint from its own signed distance field, so the article can quote a
    measurement. Falls back to the budget, loudly, when the geometry has not been built.
    """
    path = (pathlib.Path(__file__).resolve().parent.parent.parent
            / "research" / "geometry" / "nodes" / "manifest.json")
    try:
        return float(json.loads(path.read_text())["totalNodeMassKg"])
    except Exception:
        return float("nan")


def graded_pressure(m: dict, wall: float) -> dict:
    """Can pressure be staged across cells so no partition sees a full atmosphere?

    THE FIRST TWO VERSIONS OF THIS TABLE WERE WRONG, and both corrections are recorded here
    rather than erased. Version one charged nested-shell structure AND the full staged-gas
    mass at once — double-counting the load path. Version two swung the other way: "the gas
    columns transmit the compression, so the lattice sees only its local step". A reviewer's
    force balance killed that in a line: gas can transmit compression only UP TO ITS OWN
    PRESSURE, so across any cut the solid must carry P_atm minus the local gas pressure —
    the load ACCUMULATES inward, and the vacuum core carries the full atmosphere exactly as
    if the grading were not there.

    The statics-correct model of the graded-cells proposal: N pressure levels from ambient
    to hard vacuum in equal volume fractions; the lattice in the zone with gas at
    (N-j)/N atm carries j/N atm of hydrostatic compression on its solid; level-2 struts
    throughout (mass ~ p^0.75). Gas mass averages (N-1)/(2N) of ambient density. Films
    between zones hold one step over a cell span in normal operation — a lost zone doubles
    that, which is the same containment trade the main design carries, unresolved here too.
    The outer envelope's film is priced for the differential it actually sees: the full
    atmosphere ungraded, one step behind a graded band.

    The answer: IN BULK, grading surrenders over half the net lift — the gas costs lift
    everywhere while the deep lattice still carries almost the full atmosphere — and it
    hands the array's rigidity and trim to trapped gas and its temperature. AT THE BOUNDARY
    the corrected envelope price changes the verdict for the better: a thin graded band
    cuts the envelope film's differential tenfold, and that saving covers the band's gas.
    The band is roughly free in mass and buys the surface everything else wants — a tenth
    of the membrane strain, of the crazing risk, and of the consequence of an outer-face
    breach.
    """
    lad = hierarchy_ladder(m, film=0.0)
    lat2 = lad["2"]["phi"] * m["rho"]        # level-2 lattice density at the full atmosphere
    film_atm = barrier_kg_per_m3(2.0)        # atmosphere-rated interior films at 2 m cells

    def stack_factor(n: int) -> float:
        """Mean of (j/n)^0.75 over zones j = 1..n: the cumulative-load structure factor."""
        return sum((j / n) ** 0.75 for j in range(1, n + 1)) / n

    bulk = {}
    for n in (1, 2, 5, 10):
        gas = wall * (n - 1) / (2.0 * n)
        struct = lat2 * stack_factor(n) * (1.0 + NODE_MASS_FRAC)
        films = (film_atm / n if n > 1 else 0.0) + envelope_film_kg_per_m3(2.0, 1.0 / n)
        bulk[str(n)] = {"levels": n,
                        "structureKgPerM3": round(struct, 4),
                        "gasKgPerM3": round(gas, 4),
                        "filmsKgPerM3": round(films, 4),
                        "netLiftKgPerM3": round(wall - struct - gas - films, 4)}

    f, nb = 0.05, 10
    ref = bulk["1"]
    gas_cost = f * wall * (nb - 1) / (2.0 * nb)
    struct_delta = f * lat2 * (stack_factor(nb) - 1.0) * (1.0 + NODE_MASS_FRAC)
    film_delta = f * film_atm / nb
    envelope_delta = envelope_film_kg_per_m3(2.0, 1.0 / nb) - envelope_film_kg_per_m3(2.0, 1.0)
    net_cost = gas_cost + struct_delta + film_delta + envelope_delta
    band = {"bandVolumeFraction": f, "levels": nb,
            "outerSurfaceDifferentialAtm": round(1.0 / nb, 2),
            "gasCostKgPerM3": round(gas_cost, 4),
            "structureDeltaKgPerM3": round(struct_delta, 4),
            "filmsDeltaKgPerM3": round(film_delta, 4),
            "envelopeDeltaKgPerM3": round(envelope_delta, 4),
            "netCostKgPerM3": round(net_cost, 4),
            "costPctOfNetLift": round(100.0 * net_cost / ref["netLiftKgPerM3"], 1),
            "geometryNote": "5% of this hull behind 22,592 m2 of envelope is a band about "
                            "half a metre deep, so its ten steps are sub-cell-scale layers "
                            "— which is the seal-at-every-scale doctrine anyway, and film "
                            "mass is span-proportional so thinner layers cost no more.",
            "note": "The corrected envelope price is what turns the band from cheap to "
                    "roughly free: dropping the outer film's differential tenfold saves "
                    "about as much as the band's gas weighs. The band's own lattice still "
                    "carries its cumulative load — a third more than the vacuum it "
                    "replaces would need at the same depth — and the trapped gas ties trim "
                    "to temperature, which is a real operational price even when the mass "
                    "is a wash."}
    return {"assumptions": "level-2 struts (mass ~ p^0.75); zone lattice sized for its "
                           "CUMULATIVE load j/N atm (statics), the core for the full "
                           "atmosphere; films hold one step over a 2 m cell span; envelope "
                           "film priced for the differential it sees; equal volume per "
                           "level",
            "bulk": bulk, "band": band}


def pumped_plenum() -> dict:
    """A soft outer shell holding a LOSSY, ACTIVELY PUMPED partial vacuum around the array.

    Tyler's proposal, 2026-08-11, and it is the ACTIVE member of the family the graded band
    and seal-at-every-scale belong to: put the sealed cells inside a plenum the ship keeps
    at reduced pressure, and no cell operates against a full atmosphere.

    Statics is not fooled — force balance still delivers one atmosphere to the array
    through the shell's mounts, so this buys NO lattice mass in normal operation. What it
    buys is everything else, and each scales directly with the plenum pressure:

      - OPERATING MARGIN. Cells are designed (and the demonstrator is proven) at a full
        atmosphere; operated at p_plenum their crush margin multiplies by 1/p_plenum.
      - PERMEATION. The pressure difference driving gas into a sealed-for-life cell drops
        to p_plenum of its no-plenum value — the service-life budget stretches accordingly.
      - BREACH. A holed cell floods to p_plenum, not to ambient; every contingency in the
        breach ladder softens by the same factor.
      - REDUNDANCY. Pump failure is a slow drift back to the 1 atm case the cells were
        designed for — margin erodes toward the design point, nothing breaks.

    The price is a pump fighting the shell's leak rate for the life of the ship, and that
    power is NOT quantified here: it needs a shell leak-rate assumption nobody has made
    yet, and it is named in OPEN-QUESTIONS rather than invented. The prototype requirement
    is unchanged on purpose: one cell, zero net weight, against a FULL atmosphere, outside
    any ship — the plenum is what the ship then adds around it.
    """
    rows = {}
    for p in (1.0, 0.5, 0.25, 0.1):
        rows[f"{p:.2f}"] = {
            "plenumAtm": p,
            "cellOperatingMarginX": round(LATTICE_SF / p, 2),
            "permeationDriveX": round(p, 2),
            "breachFloodsToAtm": round(p, 2),
        }
    return {
        "rows": rows,
        "staticsCaveat": "No lattice saving: the shell's mounts deliver the withheld "
                         "fraction of the atmosphere into the array as structure load, "
                         "so the cumulative-load ledger is unchanged.",
        "openInput": "Shell leak rate, which sets pump power and its energy line. "
                     "Unchosen; do not quote a pump mass until it is.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="OUT")
    args = ap.parse_args()
    fig = json.loads(FIGURES.read_text())
    wall = fig["atmosphere"]["rhoAtWorkAlt"]
    cell = 2.0                     # m, the working cell size

    out = {
        "generated": {"by": "research/analysis/vacuum-cell.py", "figures": fig["generated"]},
        "constants": {"octetPhiCoeff": round(C_PHI, 3), "alignFraction": ALIGN,
                      "kLocalTubeBuckling": K_LOCAL, "kShellKnockdown": K_SHELL,
                      "orthotropicPenalty": round(ORTHO_PENALTY, 4),
                      "nodeMassFraction": NODE_MASS_FRAC, "latticeSafetyFactor": LATTICE_SF,
                      "cellSpanM": cell},
        "theWall": {"rhoAirAtWorkAltKgPerM3": wall,
                    "meaning": "A shell heavier than this per m3 of enclosed volume has no "
                               "net lift at any size. It is the whole go/no-go."},
        "materials": {}, "designPoint": {}, "nullResults": {}, "verdict": {},
        "hierarchy": {
            "why": "Each level of self-similar structure improves the strength-density "
                   "EXPONENT, which is the only thing that matters here. (n+2)/(n+1), "
                   "tending to linear — which is Jenett's assumption, reached rather than "
                   "assumed. Lakes, Nature 361 (1993).",
            "ladder": None,
        },
    }

    for key, m in MATERIALS.items():
        tot = total_shell(m, cell)
        t = tot["detail"]
        out["materials"][key] = {
            "name": m["name"], "printable": m["printable"], "source": m["source"],
            "orthotropic": m["orthotropic"],
            "materialIndex": round(material_index(m), 4),
            "specificStrengthMNmPerKg": round(m["sigma"] / m["rho"] / 1e6, 4),
            "monolithicKgPerM3": round(arch_monolithic(m)["latticeKgPerM3"], 3),
            "solidStrutKgPerM3": round(arch_solid_strut(m)["latticeKgPerM3"], 3),
            "tubeLatticeKgPerM3": round(t["latticeKgPerM3"], 4),
            "nodesKgPerM3": round(tot["nodesKgPerM3"], 4),
            "filmKgPerM3": round(tot["filmKgPerM3"], 4),
            "totalKgPerM3": round(tot["totalKgPerM3"], 4),
            "marginX": round(wall / tot["totalKgPerM3"], 3),
            "floats": tot["totalKgPerM3"] < wall,
            "tubeROverT": round(t["tubeROverT"], 1),
            "governs": t["governs"],
        }

    ref = MATERIALS["M60J_LAM"]
    t = arch_tube_strut(ref)
    tot = total_shell(ref, cell)
    net = wall - tot["totalKgPerM3"]
    out["designPoint"] = {
        "material": ref["name"],
        "phi": t["phi"],
        "tubeROverT": round(t["tubeROverT"], 1),
        "jenettFixedROverT": 10,
        "wallThicknessPerStrutLength": t["wallThicknessPerStrutLength"],
        "minimumStrutLengthM": {
            f"{w} mm wall": round((w / 1000.0) / t["wallThicknessPerStrutLength"], 3)
            for w in (0.03, 0.125, 0.2, 0.4)},
        "buildUp": {"lattice": round(tot["latticeKgPerM3"], 4),
                    "nodes": round(tot["nodesKgPerM3"], 4),
                    "interiorFilm": round(tot["filmKgPerM3"], 4),
                    "total": round(tot["totalKgPerM3"], 4),
                    "wall": wall,
                    "netLiftKgPerM3": round(net, 4),
                    "floats": tot["totalKgPerM3"] < wall},
        "floodableFractionOfHull": round(max(0.0, min(1.0, net / wall)), 3),
        "filmIsAChoiceAndTheModelPickedOneIncoherently": {
            "problem": "This model charged 0.347 kg/m3 for atmosphere-rated partitions on "
                       "every interior face, and its own note said they do NOT contain a "
                       "breach. That is paying for a component and claiming it does nothing. "
                       "Either size it for containment and claim the function, or delete it "
                       "and accept that one breach floods the hull.",
            "permeationNote": "An interior partition has vacuum on BOTH sides, so there is no "
                              "partial-pressure gradient and no permeation driving force at "
                              "all. A permeation barrier is only needed where vacuum meets "
                              "atmosphere — the outer envelope, which is 22,592 m2 against "
                              "660,000 m2 of interior wall at 1 m cells, a factor of 29.",
            "outerEnvelopeOnlyKgPerM3": round(envelope_film_kg_per_m3(2.0), 5),
            "containingPartitionsKgPerM3": round(barrier_kg_per_m3(2.0), 4),
            "totalIfOuterEnvelopeOnly": round(
                arch_tube_strut(MATERIALS["M60J_LAM"])["latticeKgPerM3"]
                * (1 + NODE_MASS_FRAC) + envelope_film_kg_per_m3(2.0), 4),
            "bulgeStrainProblem": {
                "assumedBulgeHOverA": 0.25,
                "membraneStrainRequiredPct": 4.12,
                "zylonStrainAtWorkingStressPct": [0.27, 0.40],
                "note": "The assumed bulge needs 10-15x the strain the fibre can deliver at "
                        "the model's own working stress. Either the film is PRE-FORMED to its "
                        "loaded dome shape, or the reachable bulge is h/a ~ 0.07 and the film "
                        "is about 3.7x heavier — which sinks it outright. Independently "
                        "verified. A 4% strain would also craze any inorganic barrier "
                        "coating on first pump-down.",
            },
        },
        "film": {
            "sizedToHoldAnAtmosphere": {
                f"{c:.1f} m cells": round(barrier_kg_per_m3(c), 4)
                for c in (0.5, 1.0, 2.0, 4.0)},
            "scaleInvarianceNote":
                "Identical at every cell size, because a film's areal mass grows with the "
                "span it bulges across exactly as fast as area-per-volume falls. That is the "
                "finding: you cannot make this term go away by choosing a cell size.",
            "minimumGaugeAlternative": {
                f"{c:.1f} m cells": round(0.05 * CELL_AREA_COEFF / c, 4)
                for c in (0.5, 1.0, 2.0, 4.0)},
            "minimumGaugeNote":
                "A 50 g/m2 foil laminate — enough to stop permeation for a service life, not "
                "enough to hold an atmosphere. It is 0.075 kg/m3 at 2 m cells instead of "
                "0.347, and it does NOT contain a breach: the neighbour's partition is not "
                "sized for the atmosphere a flooded cell puts against it, so flooding "
                "cascades. THIS IS THE SHARPEST UNRESOLVED TRADE IN THE DESIGN.",
        },
    }

    # Both "null results" were wrong, and in the same way: they assumed shell mass scales with
    # pressure, which is the YIELD case. Everything here is buckling-governed, where it scales
    # as p^(2/3) — so full vacuum is strictly optimal and altitude is mildly unfavourable.
    pv = {}
    for frac in (1.0, 0.75, 0.5, 0.25):
        dp = P_ATM * frac
        lat = arch_tube_strut(ref, dp)["latticeKgPerM3"] * (1 + NODE_MASS_FRAC)
        lift = wall * frac
        pv[f"{frac:.2f}"] = {"deltaPFraction": frac, "grossLiftKgPerM3": round(lift, 4),
                             "shellKgPerM3": round(lat, 4),
                             "shellPerLift": round(lat / lift, 4)}
    base = arch_tube_strut(ref, P_ATM)["latticeKgPerM3"] * (1 + NODE_MASS_FRAC)
    alt = {}
    for h in (0, 2500, 5000):
        lat = arch_tube_strut(ref, isa_pressure(h))["latticeKgPerM3"] * (1 + NODE_MASS_FRAC)
        alt[f"{h} m"] = {"pressurePa": round(isa_pressure(h)),
                         "rhoAirKgPerM3": round(rho_air(h), 4),
                         "shellSizedLocallyKgPerM3": round(lat, 4),
                         "marginIfSizedLocally": round(rho_air(h) / lat, 3),
                         "marginIfSizedAtSeaLevel": round(rho_air(h) / base, 3)}
    out["nullResults"] = {
        "partialVacuum": {
            "retracted": "Earlier text said partial vacuum is exactly neutral. That is the "
                         "yield-governed answer. Buckling governs, so shell mass goes as "
                         "deltaP^(2/3) while lift goes as deltaP — full vacuum is STRICTLY "
                         "OPTIMAL and partial vacuum degrades as deltaP^(-1/3). The "
                         "corrected result favours the concept.",
            "sweep": pv},
        "altitude": {
            "retracted": "Earlier text said altitude is exactly neutral. For a "
                         "buckling-governed hull the requirement goes as T*p^(-1/3), so it "
                         "gets HARDER with altitude, not easier — and a ship that lands has "
                         "to survive sea level anyway, which is the convention used here.",
            "sweep": alt},
        "materialIndex": "Specific strength is NOT the criterion — every row is "
                         "buckling-governed. The index is E_eff^(2/3)/rho.",
    }

    out["verdict"] = {
        "floatingMaterials": [k for k, v in out["materials"].items() if v["floats"]],
        "referenceTotalKgPerM3": out["designPoint"]["buildUp"]["total"],
        "wall": wall,
        "summary": ("Corrected for laminate rather than fibre properties, the orthotropic "
                    "tube wall, node mass, a lattice safety factor and the interior sealing "
                    "film, the reference design sits AT the wall rather than inside it. "
                    "Which side it falls on is decided by choices not yet made: cell size, "
                    "whether interior films are sized to contain a breach, and packing "
                    "fraction."),
    }

    out["hierarchy"]["ladder"] = hierarchy_ladder(ref)
    first_float = next((v for v in out["hierarchy"]["ladder"].values()
                        if v["totalKgPerM3"] < wall), None)
    out["hierarchy"]["floatsFromLevel"] = first_float["levels"] if first_float else None
    out["hierarchy"]["headline"] = (
        f"One more level of hierarchy than the current design carries takes it from "
        f"{out['hierarchy']['ladder']['1']['totalKgPerM3']} to "
        f"{out['hierarchy']['ladder']['2']['totalKgPerM3']} kg/m3 — from under the wall to "
        f"{round(wall / out['hierarchy']['ladder']['2']['totalKgPerM3'], 2)}x over it.")
    # Ladders for the printable materials too, because the demonstrator page asks the obvious
    # next question: what would a PRINTED cell need? (Answer: even Markforged-class continuous
    # fibre never floats on this ladder — the flight article is wound or pultruded.)
    out["hierarchy"]["ladders"] = {k: hierarchy_ladder(MATERIALS[k])
                                   for k in ("M60J_LAM", "T700_LAM", "CFF", "PAHT_Z")}

    out["sharedWall"] = {f"{c:.1f} m cells": shared_wall(c) for c in (0.5, 1.0, 2.0, 4.0)}
    out["cellShapes"] = cell_shapes()
    out["printerChain"] = printer_chain(MATERIALS["PAHT_Z"])
    out["demonstrator"] = demonstrator(MATERIALS["PAHT_Z"])
    out["stockBuild"] = stock_build()
    # RAW span, not the rounded display value: the parity gate has caught this exact
    # rounded-vs-raw divergence twice now, once on strut mass and once here.
    out["filmEdgeLoads"] = film_edge_loads(2.0 * DEMO_PITCH_PINNED_M)
    out["memberDemands"] = member_demands(2.0 * DEMO_PITCH_PINNED_M)
    out["kelvinFaces"] = {str(n): kelvin_lattice_counts(n) for n in (1, 2, 3)}
    out["gradedPressure"] = graded_pressure(ref, wall)
    out["pumpedPlenum"] = pumped_plenum()
    out["weightlessArticle"] = weightless_article(wall)

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(out, indent=1))

    w = 34
    print(f"\nTHE WALL: {wall:.4f} kg per m3 enclosed. Cell {cell:.0f} m, "
          f"nodes {NODE_MASS_FRAC:.0%}, SF {LATTICE_SF}.\n")
    print(f"{'material':<{w}}{'index':>8}{'lattice':>9}{'+nodes':>8}{'+film':>8}"
          f"{'TOTAL':>9}{'margin':>8}")
    print("-" * (w + 50))
    for r in out["materials"].values():
        print(f"{r['name'][:w - 1]:<{w}}{r['materialIndex']:>8.3f}"
              f"{r['tubeLatticeKgPerM3']:>9.3f}{r['nodesKgPerM3']:>8.3f}"
              f"{r['filmKgPerM3']:>8.3f}{r['totalKgPerM3']:>9.3f}{r['marginX']:>7.2f}x"
              + ("  FLOATS" if r["floats"] else ""))
    d = out["designPoint"]
    print(f"\nDESIGN POINT: R/t = {d['tubeROverT']} (Jenett fixes it at "
          f"{d['jenettFixedROverT']}), phi = {d['phi']:.3e}")
    print(f"  {d['floodableFractionOfHull']:.0%} of the hull could flood before it sinks")
    print("\nHIERARCHY — structure inside structure, which is the path:")
    for v in out["hierarchy"]["ladder"].values():
        print(f"  {v['levels']} levels  exponent {v['exponent']:.3f}  "
              f"{v['totalKgPerM3']:>8.3f} kg/m3  {wall / v['totalKgPerM3']:>5.2f}x  "
              f"{v['name']}" + ("   FLOATS" if v["totalKgPerM3"] < wall else ""))
    print(f"\n{out['hierarchy']['headline']}")

    print("\nPRINTER CHAIN (PAHT-CF, interlayer): nozzle -> wall -> strut -> cell")
    for label, r in out["printerChain"]["rows"].items():
        mark = "  <-- design point" if label == out["printerChain"]["designPoint"] else ""
        print(f"  {label:<12} wall {r['wallMm']:.2f} mm  strut {r['strutM']:.3f} m  "
              f"cell {r['cellM']:.3f} m  {r['enclosedL']:>4} L{mark}")
    d = out["demonstrator"]
    print(f"\nDEMONSTRATOR (standalone article): {d['printedStruts']} struts + "
          f"{d['printedNodes']} nodes, {d['totalKg']:.2f} kg against "
          f"{d['displacedAirKg']:.3f} kg displaced ({d['massOverDisplaced']:.0f}x — it does "
          f"not float; it holds vacuum with margin >= {d['crushMarginAtSeaLevelAtLeast']} "
          f"and proves the proportions). In-array share: {d['inArrayShareKg']:.2f} kg.")

    print("\nGRADED PRESSURE — bulk (net lift, kg/m3):")
    for r in out["gradedPressure"]["bulk"].values():
        print(f"  N={r['levels']:<3} structure {r['structureKgPerM3']:.3f}  "
              f"gas {r['gasKgPerM3']:.3f}  films {r['filmsKgPerM3']:.3f}  "
              f"net {r['netLiftKgPerM3']:+.3f}")
    b = out["gradedPressure"]["band"]
    print(f"  band: outer {b['bandVolumeFraction']:.0%} graded in {b['levels']} steps costs "
          f"{b['costPctOfNetLift']:.1f}% of net lift; the envelope sees "
          f"{b['outerSurfaceDifferentialAtm']:.1f} atm instead of 1.")

    print("\nCELL SHAPES — shared-wall area coefficient (cube = 3.0):")
    for name, s in out["cellShapes"].items():
        print(f"  {name:<22} {s['coeff']:.3f}  ({s['filmSavingVsCubePct']:+.1f}% film "
              f"vs cube)")
    sw = out["sharedWall"]["2.0 m cells"]
    print(f"\nSHARED WALL at 2 m cells: {sw['interiorM2']:,} m2 interior against "
          f"{sw['envelopeM2']:,.0f} m2 envelope — {sw['sharedFractionPct']}% of all wall "
          f"area carries no pressure differential.")


if __name__ == "__main__":
    main()
