#!/usr/bin/env python3
"""MAINLINE-017b: write CARD.md, RESULTS.json, NFI.json and INPUTS.json from COMPUTE.json and TRENDS.json."""
import datetime
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "COMPUTE.json")))
T = {t["id"]: t for t in json.load(open(os.path.join(HERE, "TRENDS.json")))["trends"]}
SRC = "unpublished-local-ref:6e94df3272e3fba2"
JOB_STARTED = "2026-10-20T01:25:38-07:00"   # order read; a measurement, never a limit
P2, P3 = C["p2"], C["p3"]
MODE = {"global_buckling": "global buckling", "face_compression": "face compression",
        "core_shear_crimping": "core shear crimping", "core_crush": "core crush", "face_wrinkling": "face wrinkling",
        "intracell_dimpling": "intracell dimpling", "yield": "tube yield", "euler": "member Euler", "local": "tube local",
        "film": "film", "perry": "Perry beam-column", "global": "lattice global"}


def g(x, n=4):
    return f"{x:.{n}g}"


def fx(x, n=3):
    return f"{x:.{n}f}"


# ---------------------------------------------------------------- P2 single-property rows
P2_ROWS = [
    ("face_density", "Face specific stiffness and strength (density at beryllium's E and strength)",
     lambda f: f"face density {1850 / f:.0f} kg/m3, E/rho {290e3 / 1850 * f:.0f} MPa per kg/m3"),
    ("face_modulus", "Face modulus at beryllium's density", lambda f: f"{290 * f:.0f} GPa, only by stepping onto the "
                                                                     f"crimp branch at Vc 2 (see the gamma rule)"),
    ("gamma", "ANALYSIS: global knockdown gamma (handbook 0.20)", lambda f: f"gamma {min(1.0, 0.2 * f):.3f}"),
    ("core_shear_modulus", "Core W shear modulus per density (the brief's translation of gamma)",
     lambda f: f"{46.884 * f:.1f} MPa"),
    ("core_density", "Core density at today's core properties", lambda f: f"{16.018 / f:.2f} kg/m3"),
    ("core_tt_modulus", "Core through-thickness modulus (Q's translation, route b)", lambda f: f"{103.42 * f:.1f} MPa"),
    ("face_flatness", "Face flatness, CR-1457 waviness parameter K_delta (Q's translation, route a)",
     lambda f: f"K_delta {2.3201 / f:.3f}"),
    ("wrinkle_Q", "ANALYSIS: wrinkle coefficient Q (0.33)", lambda f: f"Q {0.33 * f:.3f}"),
    ("face_strength", "Face compressive strength (SR-200 345 MPa)", lambda f: f"{345 * f:.0f} MPa"),
    ("core_crush", "Core crush strength", lambda f: f"{241.3 * f:.0f} kPa"),
    ("cell_size", "Core cell size", lambda f: f"{9.525 / f:.2f} mm"),
    ("sheet_size", "Sheet size (stock 609.6 x 1828.8 mm)", lambda f: f"{0.6096 * f:.2f} x {1.8288 * f:.2f} m"),
    ("film_mass", "Bond-film areal mass (AF 163-2U, 73.2 g/m2 per line)", lambda f: f"{73.24 / f:.1f} g/m2"),
    ("seam_mass", "Seam mass per metre (028 scarf, splice, seal)", lambda f: "seams 1/f as heavy"),
]
FILM_DESIGN = {"today": ("Kapton HN", 115.5, 1420), "projection": ("Zylon 0/90", 3480.0, 1560)}
P3_ROWS = [
    ("sic_density", "Tube density (SiC 3100 kg/m3)", lambda f, row: f"{3100 / f:.0f} kg/m3"),
    ("sic_modulus", "Tube modulus (SiC 410 GPa)", lambda f, row: f"{410 * f:.0f} GPa"),
    ("film_specific_strength", "Film specific strength (design allowable over density)",
     lambda f, row: f"{FILM_DESIGN[row][0]} design {FILM_DESIGN[row][1] * f:.0f} MPa at {FILM_DESIGN[row][2]} kg/m3"),
    ("lattice_knockdown", "ANALYSIS: lattice global knockdown k (0.2)", lambda f, row: f"k {0.2 * f:.3f}"),
    ("sic_strength", "SiC design compressive strength (3900 MPa carried)", lambda f, row: f"{3900 * f:.0f} MPa"),
    ("joint_mass", "End-joint mass (023's C)",
     lambda f, row: (f"joints {1 / f:.0f} times as heavy" if f < 1 else f"joints {f:.2f} times lighter")),
    ("node_mass", "Node mass (20 g)", lambda f, row: (f"{0.02 / f:.1f} kg per node" if f < 0.02 else f"{20 / f:.1f} g per node")),
    ("local_knockdown", "ANALYSIS: tube local knockdown (SP-8007, capped at 1)", lambda f, row: f"local gamma x{f:.3f}"),
    ("straightness", "Member straightness (Perry L/1000)", lambda f, row: f"a bow of L/{1000 * f:.0f}"),
]
NICE = {"face_density": "lighter face", "face_modulus": "face modulus", "gamma": "gamma",
        "core_shear_modulus": "core shear modulus", "core_density": "core density",
        "core_tt_modulus": "core through-thickness modulus", "face_flatness": "face flatness (K_delta)",
        "sic_density": "tube density", "sic_modulus": "tube modulus", "film_specific_strength": "film specific strength",
        "lattice_knockdown": "lattice knockdown", "local_knockdown": "local knockdown", "sic_strength": "SiC strength",
        "joint_mass": "joint mass", "node_mass": "node mass", "straightness": "straightness"}


def p2_cell(rec, prop, fn):
    r = rec["alone"][prop]
    if r["alone"] and r.get("factor"):
        return f"x{r['factor']:.3f}: {fn(r['factor'])}"
    return f"not alone: saturates at {r['saturates_at']:.3f}, then {MODE[r['next_mode']]} binds"


def p3_cell(rec, prop, fn):
    r = rec["alone"][prop]
    if r["alone"] and r.get("factor"):
        return f"x{r['factor']:.3f}: {fn(r['factor'], rec['row'])}"
    if r["alone"]:
        return "floats at any value"
    return f"not alone: saturates at {r['saturates_at']:.3f}, then {MODE[r['next_mode']]} binds"


def combo_text(b):
    if not b:
        return "none floats"
    parts = [f"{NICE.get(k, k)} x{v:.3f}" for k, v in b["factors"].items() if v > 1 + 1e-5]
    return f"product {b['product']:.3f}: " + ", ".join(parts)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    def yrs(v):
        return "It does not close: there is no rising trend" if v is None else f"{v:.0f} years"
    w("**P2.**")
    w(f"- **Face specific stiffness (thin isotropic face):**")
    w(f"  - History: beryllium 164 (1966), 158 (1971), 164 (1990s), 157 (2024). Carbon fibre reached 387 (1992) and "
      f"423 (2007) along the fibre only. A quasi-isotropic laminate is 51 (P75, 1994) to about 100 (K13D2U, an "
      f"estimate).")
    w(f"  - Rate {TF['rate']['per_year'] * 100:+.2f} percent a year. Needed 293 / 272. {yrs(None)}.")
    w(f"  - Limit: 423 along the best fibre. No quasi-isotropic carbon face reaches beryllium.")
    w(f"- **Face modulus:** 299 (1967), 293 (1971), 297 (1991), 303 (2001, 2020), 290 (2024) GPa; rate "
      f"{TM['rate']['per_year'] * 100:+.2f} percent a year. The limit is the ideal polycrystal, 306.9 GPa, so the "
      f"element sits at its limit.")
    w(f"- **Gamma (large-shell precision), best tests found:**")
    w(f"  - Sphere tests: 0.85 (1954), 0.86 (1966, electroformed nickel), 0.69 (2016, elastomer).")
    w(f"  - Design: 0.14 (SP-8032, 1969), and 0.20 for sandwich hemispheres (CR-1457, 1969, from two 1964 tests).")
    w(f"  - Sandwich cylinders reached 0.87 (2018) and 0.72 (2024) of perfect, against SP-8007's 0.56-0.61.")
    w(f"  - No rising trend for spheres in 60 years. The limit is 1; the R 10 need is 94 percent of the best sphere "
      f"test found.")
    w(f"- **Core W shear stiffness per density (aluminium):** 2.93 MPa per kg/m3 in Hexcel's tables of 1998, 2004, "
      f"2016 and 2017. The 5052 1/4-1.6 row of today's sheet also equals a 1986 NASA quotation. The rate is "
      f"{TCS['rate']['per_year'] * 100:.1f} percent a year. The mean of L and W sits at the Gibson-Ashby regular "
      f"hexagon (4.63). The best existing core is carbon (Ultracor, 6.46 W, from a secondary source).")
    w(f"- **Core through-thickness stiffness per density:** 6.46 in every edition since 1998, so "
      f"{TCE['rate']['per_year'] * 100:.1f} percent a year. The limit is Es/rho_s = 24.8 for 5056. The best aluminium "
      f"is 13.5 (1/8-3.1).")
    w(f"- **Face flatness and wrinkling:** the design 0.33 and classical 0.82 are unchanged since 1969. Measured "
      f"coefficients run 0.125-0.82. No waviness history was found.")
    w(f"- **Sheet size:** 2438 mm (1966), 2032 (1972), 1829 (1990s, 2024). Rate "
      f"{TSH['rate']['per_year'] * 100:+.2f} percent a year.")
    w(f"- **Bond film:** 244 g/m2 (1954), 147 (1975), 73 (2006-2009), then flat. Lab edge deposition reached 8 "
      f"(2008). It improved {TBF['rate']['per_year'] * 100:.1f} percent a year (1975-2009).")
    w(f"- **Face strength:** SR-200's 345 MPa minimum has been unchanged since 1966. One 1967 lot reached 379 MPa in "
      f"compression.")
    w("")
    w("**P3.**")
    w(f"- **Tube specific stiffness (SiC):** 135 (1988), 131 (1997), 144 (2003, hot-pressed), 139 (2012, 2024) and 145 "
      f"(CVD, 2019).")
    w(f"  - Rate {TTUBE['rate']['per_year'] * 100:.2f} percent a year.")
    w(f"  - Needed {TTUBE['needed']:.0f}, which is x{TTUBE['gap_over_best']:.2f} over the best SiC.")
    w(f"  - About {TTUBE['years_to_close']:.0f} years at that rate (PROJECTION): in practice a different tube "
      f"material.")
    w(f"- **Film specific strength**, best real film each year:")
    w(f"  - History: Kapton H 126 kN m/kg (1975), Mylar 141 (1999), Teonex 228 (2013), Upilex-S 354 (2022).")
    w(f"  - Rate {TFILM['rate_long']['per_year'] * 100:.1f} percent a year since 1975 and "
      f"{TFILM['rate_recent']['per_year'] * 100:.1f} since 1999.")
    w(f"  - Needed {TFILM['needed_raw']:.0f} at 024's half-strength rule, which is x{TFILM['gap_over_best']:.2f} over "
      f"Upilex-S.")
    w(f"  - {TFILM['years_to_close']['at_recent_rate']:.0f}-{TFILM['years_to_close']['at_long_rate']:.0f} years "
      f"(PROJECTION).")
    w(f"  - Zylon fibre is {TFILM['fibre_reference']['value']:.0f}, as fibre, not film.")
    w(f"- **SiC design compressive strength:** flexure 402 (1988), 395 (1995), 380 (2004-2026) MPa; vendor compression "
      f"3900 MPa since 2004.")
    w(f"  - Rate {TSIC['rate']['per_year'] * 100:+.2f} percent a year.")
    w(f"  - No design allowable exists; NASA's CARES/Life leaves compression to other methods.")
    w(f"  - The ideal strength is 50.8 GPa.")
    w(f"- **Lattice knockdown:** perfect-geometry and FE values are 0.65 (2001) and 0.70 (2020). The design 0.2 and "
      f"Wright's 0.4 were not confirmed from a page. No trend.")
    w(f"- **End-fitting compression (CFRP):** 1470 MPa (T300, 2002) to 1870 (T1100G, 2025), "
      f"{T['end_joint_mass']['rate']['per_year'] * 100:.1f} percent a year. Ti-6Al-4V is 827 MPa annealed.")
    w(f"- **Local knockdown:** the SP-8007 rule has been unchanged since 1968, while modern cylinder tests reach "
      f"0.7-0.9. Straightness is L/1000 (steel), and 1 mm per m on CFRP tubes.")
    w("")
    w("## 4. Rank")
    w("")
    w("**By gap (single properties that reach SF 1, smallest first):**")
    w(f"1. P3 today, tube specific stiffness, x{TTUBE['factor']['sic_density']:.2f}.")
    w(f"2. P2 R 20, lighter face, x{TF['factor']['R20']:.2f}.")
    w(f"3. P2 R 10, lighter face, x{TF['factor']['R10']:.2f}.")
    w(f"4. P2 R 20, face modulus, x{TM['factor']['R20']:.2f} (Vc 2 step only).")
    w(f"5. P3 today, lattice knockdown, x{TLK['factor']:.2f}.")
    w(f"6. P2 R 10, face modulus, x{TM['factor']['R10']:.2f} (Vc 2 step only).")
    w(f"7. P2 R 20, gamma, x{TG['factor']['R20']:.2f}.")
    w(f"8. P3 today, film specific strength, x{TFILM['factor']:.2f}.")
    w(f"9. P2 R 10, gamma, x{TG['factor']['R10']:.2f}.")
    w("")
    w(f"**By trend.** Only film specific strength is rising fast enough to matter:")
    w(f"- It closes P3's film gap beyond Upilex-S in {TFILM['years_to_close']['at_recent_rate']:.0f}-"
      f"{TFILM['years_to_close']['at_long_rate']:.0f} years (PROJECTION).")
    w(f"- Upilex-S already covers x{up_over_kapton:.2f} of the x{TFILM['factor']:.2f}.")
    w("")
    w("Bond film and CFRP compression rise about 1-2 percent a year but are not levers. Everything else is flat, and "
      "three are at or near a physical limit: beryllium's modulus, an isotropic face's specific stiffness, and a "
      "sphere's knockdown against its best test.")
    w("")
    w("**Closest.** P3 through film specific strength is the only direction a 30-year trend reaches. That P3 also "
      "needs its SiC compression qualified at about 1.2 GPa, which is a test campaign rather than new material. The "
      "projection row already floats if its three projections hold: the Zylon membrane, the CFRP wrap, and a "
      "qualified 0.9 GPa allowable.")
    w("")
    w("**Step changes.** Each of these has no supporting trend:")
    w(f"- **P2's lighter face**, x{TF['factor']['R20']:.2f}-{TF['factor']['R10']:.2f}: a new face material class. "
      f"Nano-carbon films are lab only.")
    w(f"- **P3's tube specific stiffness**, x{TTUBE['factor']['sic_density']:.2f}: beyond SiC. A carbon-fibre tube "
      f"needs a sourced compressive strength near 0.8-1.2 GPa.")
    w(f"- **A test-validated knockdown for large sandwich spheres**, gamma {TG['needed']['R20']:.2f}-"
      f"{TG['needed']['R10']:.2f}. The cylinder programme is the one precedent for moving a knockdown.")
    w(f"- **A core stiffer through the thickness than aluminium can be**, if beryllium and the handbook values both "
      f"stay.")
    w(f"- **Lattice-dome knockdown tests** for P3's k {TLK['needed']:.2f}.")
    w("")
    w("Size helps P2 everywhere. R 20 lowers every factor and loosens the precision ask five-fold, from a 2.5 mm "
      "dimple to 13 mm. It changes no trend.")
    w("")
    w("## Method and checks")
    w("")
    w("model17b.py, scan17b.py, combo17b.py, run17b.py, trend17b.py and card17b.py are this seat's own code.")
    w("")
    w("**Models.**")
    w("- **P2:** 021 rev1's modes, which are CR-1457 as 009d/014b state them, with biaxial dimpling. 028's joining "
      "formulas run on 019's reserve.")
    w("- **P3:** 022c's equilateral frame:")
    w("  - 022b's member force pRs/(2 sqrt 3);")
    w("  - SP-8007 local gamma;")
    w("  - Perry at L/1000;")
    w("  - k 0.2 global;")
    w("  - 023's sized end joints;")
    w("  - 024's cap sag charged as lift.")
    w("")
    w(f"**Reproduction checks.** {len(C['checks'])} checks pass before anything new:")
    w("- 028's reoptimised AF 163/scarf stock case, 1.000640757 against 1.000640757;")
    w("- 021b's floating point, all six modes, and its today value 0.42714182;")
    w("- 022c's ti_kapton_019 (0.70174591) and cfrp_zylon_019 (1.41704657), on 022c's own grid, every mode and the "
      "sag.")
    w("")
    w("**Optimisers.**")
    w("- **P2:** a log-spaced grid of 6001 core-mass fractions, then golden refinement.")
    w("- **P3:** 022c's band with a 40-point film grid, then Nelder-Mead.")
    w("- **Factors:** bisection on the log factor, to 1e-9 for P2 and 1e-6 for P3.")
    w("")
    w("**Trends** come from trend17b.py, which pulls each value from the sourcing files by property, year and product, "
      "and asserts it.")
    w("")
    w("## Then")
    w("")
    w("Stop and file. The robotics seat sends the next job. NFI.json carries the open rows. A checker runs behind this "
      "card.")
    text = "\n".join(L) + "\n"
    with open(os.path.join(HERE, "CARD.md.tmp"), "w") as fh:
        fh.write(text)
    os.replace(os.path.join(HERE, "CARD.md.tmp"), os.path.join(HERE, "CARD.md"))
    print(len(text), "bytes")


if __name__ == "__main__":
    main()
