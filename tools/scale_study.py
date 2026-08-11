#!/usr/bin/env python3
"""What a 1 m cell costs, computed from the project's own model.

Loads research/analysis/vacuum-cell.py, reproduces the published 0.709 m figures as a
self-check, then re-evaluates every governing check at a larger span and sweeps real tube
SKUs for the lightest one that holds each margin.

Nothing here is a new physics model: every formula is the module's own, called with a
different span, or (for the two rows that hard-code a section) re-derived from the same
module constants and checked against the module's output at the current span first.
"""
import importlib.util, json, math, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("vc", ROOT / "research/analysis/vacuum-cell.py")
vc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vc)
PUB = json.load(open(ROOT / "research/analysis/vacuum-cell.json"))

# The TRUE span, not the published 0.709: span = 2 * the printer chain's design-point
# pitch. Every published figure is computed from this and then rounded, so the self-check
# below has to work from the same unrounded number or it fails on the rounding.
S0 = 2 * vc.printer_chain(vc.MATERIALS["PAHT_Z"])["rows"]["0.6 mm x 2"]["cellMRaw"]
RHO = vc.MATERIALS["T700_LAM"]["rho"]
E = vc.MATERIALS["T700_LAM"]["E"]
SIG = vc.MATERIALS["T700_LAM"]["sigma"]
SF = vc.LATTICE_SF
TH_HH = math.acos(-1.0 / 3.0)          # hexagon-hexagon dihedral

# counts, from the article graph
N_LONG, N_RIM, N_SHORT = 108, 36, 72


def sec(od, idd):
    ro, ri = od / 2.0, idd / 2.0
    I = math.pi / 4.0 * (ro ** 4 - ri ** 4)
    return {"od": od, "id": idd, "I": I, "Z": I / ro,
            "A": math.pi * (ro ** 2 - ri ** 2),
            "kgPerM": math.pi * (ro ** 2 - ri ** 2) * RHO}


def line_loads(span):
    """The three film line loads, from the module's own panel geometry."""
    a = vc.kelvin_faces(span)["edgeM"]
    t_tri, sa = vc.panel_tension(vc.PANEL["hexSpoked"] * a)
    t_sq, _ = vc.panel_tension(vc.PANEL["squareSpoked"] * a)
    ca = math.sqrt(1 - sa * sa)
    half = TH_HH / 2.0
    w_rim = 2 * t_tri * (math.cos(half) * ca + math.sin(half) * sa)   # dihedral, both panels
    return {"rim": w_rim, "spoke": 2 * t_tri * sa, "sqtie": 2 * t_sq * sa, "edge": a}


def bend(w, L, s, propped=False):
    Le = L / 2.0 if propped else L
    m_pin = w * Le * Le / 8.0
    return {"stressPinnedMPa": m_pin / s["Z"] / 1e6,
            "marginPinnedAtSF": SIG / (m_pin / s["Z"] * SF),
            "failsAtAtm": SIG / (m_pin / s["Z"])}


def euler(dem, L, s, k=1.0):
    return math.pi ** 2 * E * s["I"] / (k * L) ** 2 / dem


def design(span, main, rim):
    """Every governing check at one span with one pair of SKUs."""
    a = vc.kelvin_faces(span)["edgeM"]
    d = vc.member_demands(span)
    w = line_loads(span)
    f = vc.kelvin_faces(span)
    short = a / math.sqrt(2.0)
    tube_kg = ((N_LONG * a + N_SHORT * short) * main["kgPerM"] + N_RIM * a * rim["kgPerM"])
    return {
        "span": span, "edge": a, "shortCut": short,
        "volL": span ** 3 / 2 * 1000, "areaM2": f["areaM2"],
        "hexLoadTf": vc.P_ATM * f["hexM2"] / 9806.65,
        "surfaceTf": vc.P_ATM * f["areaM2"] / 9806.65,
        "octetN": d["families"]["octet"]["axialN"],
        "octetEuler": euler(d["families"]["octet"]["axialN"], a, main),
        "octetStress": SIG * main["A"] / d["families"]["octet"]["axialN"],
        "rimN": d["families"]["rim"]["axialN"],
        "rimEuler": euler(d["families"]["rim"]["axialN"], a, rim),
        "rimBend": bend(w["rim"], a, rim),
        "spokeN": d["families"]["spoke"]["axialN"],
        "spokeEuler": euler(d["families"]["spoke"]["axialN"], a, main),
        "spokeBend": bend(w["spoke"], a, main, propped=True),
        "tieN": d["governingShortMemberN"],
        "tieEuler": euler(d["governingShortMemberN"], short, main),
        "tieBend": bend(w["sqtie"], short, main),
        "tubeKg": tube_kg, "filmKg": vc.film_kg(span),
        "filmGPerM2": vc.barrier_kg_per_m2(2 * vc.PANEL["hexSpoked"] * a) * 1000,
    }


P10x8, P14x12 = sec(0.010, 0.008), sec(0.014, 0.012)
base = design(S0, P10x8, P14x12)

# ---------------------------------------------------------------- self-check
pub = PUB["stockBuild"]
gov = pub["governingCheck"]
checks = [
    # Tolerances are the PUBLISHED rounding, one half-unit of the last printed digit —
    # not a fudge factor. A figure quoted as an integer newton is checked to 0.5 N.
    ("edge mm", base["edge"] * 1000, pub["pipe"]["longCutM"] * 1000, 0.5),
    ("volume L", base["volL"], pub["enclosedL"], 0.5),
    ("octet demand N", base["octetN"], pub["pipe"]["perStrutDemandN"], 0.5),
    ("octet Euler", base["octetEuler"], pub["pipe"]["eulerMarginPinned"], 0.005),
    ("octet stress margin", base["octetStress"], pub["pipe"]["stressMargin"], 0.05),
    ("rim demand N", base["rimN"], pub["pipe"]["rimDemandN"], 0.5),
    ("rim Euler", base["rimEuler"], pub["pipe"]["rimEulerMargin"], 0.005),
    ("spoke Euler", base["spokeEuler"], pub["pipe"]["spokeEulerMargin"], 0.005),
    ("tie demand N", base["tieN"], pub["pipe"]["tieDemandN"], 0.5),
    ("tie Euler", base["tieEuler"], pub["pipe"]["tieEulerMargin"], 0.005),
    ("rim bending MPa", base["rimBend"]["stressPinnedMPa"], gov["stressPinnedMPa"], 0.5),
    ("rim fails at atm", base["rimBend"]["failsAtAtm"], gov["failsAtAtm"], 0.005),
    ("tube kg", base["tubeKg"], pub["pipe"]["kg"], 0.005),
    ("film kg", base["filmKg"], pub["skinKg"], 0.0005),
]
print("SELF-CHECK against research/analysis/vacuum-cell.json at span 0.709")
ok = True
for name, got, want, tol in checks:
    good = abs(got - want) <= tol
    ok &= good
    print(f"  {'ok ' if good else 'BAD'} {name:22s} {got:10.3f}  published {want:10.3f}")
print(f"  => {'reproduces the published article' if ok else 'DOES NOT REPRODUCE — stop'}\n")
if not ok:
    sys.exit(1)

# ---------------------------------------------------------------- scaling law
print("SCALING (geometric: tube diameter grows with span)")
for label, s in [("demand  crush/strut", "L^2"), ("demand  film line load", "L^1"),
                 ("moment  w L^2 / 8", "L^3")]:
    print(f"  {label:26s} ~ {s}")
print("  Euler margin at FIXED tube    ~ 1/L^4      (demand L^2, capacity 1/L^2)")
print("  bending stress at FIXED tube  ~ L^3        (moment L^3, Z fixed)")
print("  both are held CONSTANT by scaling the tube diameter with the span:")
print("    I ~ d^4 so Euler capacity ~ d^4/L^2;  Z ~ d^3 so bending stress ~ L^3/d^3\n")

# ---------------------------------------------------------------- 1 m, today's tube
for span in (1.0, 0.98):
    d = design(span, P10x8, P14x12)
    print(f"AT SPAN {span:.3f} ON TODAY'S TUBE (10x8 / 14x12)")
    print(f"  edge {d['edge']*1000:.1f} mm   short cut {d['shortCut']*1000:.1f} mm   "
          f"{d['volL']:.0f} L   {d['areaM2']:.3f} m2   surface {d['surfaceTf']:.1f} tf")
    print(f"  octet Euler {d['octetEuler']:.2f}   spoke Euler {d['spokeEuler']:.2f}   "
          f"tie Euler {d['tieEuler']:.2f}   rim Euler {d['rimEuler']:.2f}")
    print(f"  rim BENDING {d['rimBend']['stressPinnedMPa']:.0f} MPa, margin "
          f"{d['rimBend']['marginPinnedAtSF']:.2f}, fails at {d['rimBend']['failsAtAtm']:.2f} atm")
    print(f"  spoke bending margin {d['spokeBend']['marginPinnedAtSF']:.2f}   "
          f"sq-tie bending margin {d['tieBend']['marginPinnedAtSF']:.2f}\n")

# ---------------------------------------------------------------- SKU sweep
CATALOGUE = [(10, 8), (12, 10), (12, 9), (12, 8), (14, 12), (14, 11), (14, 10),
             (15, 13), (16, 14), (16, 13), (16, 12), (18, 16), (18, 15), (18, 14),
             (20, 18), (20, 17), (20, 16), (22, 20), (24, 22), (25, 23), (25, 21),
             (26, 24), (28, 26), (30, 28), (30, 26)]

TARGETS = {                      # what the 0.709 article achieves today
    "octetEuler": base["octetEuler"], "spokeEuler": base["spokeEuler"],
    "tieEuler": base["tieEuler"], "rimEuler": base["rimEuler"],
    "rimBendAtm": base["rimBend"]["failsAtAtm"],
    "spokeBendMargin": base["spokeBend"]["marginPinnedAtSF"],
    "tieBendMargin": base["tieBend"]["marginPinnedAtSF"],
}
print("TODAY'S MARGINS (the bar a 1 m cell has to clear)")
for k, v in TARGETS.items():
    print(f"  {k:18s} {v:6.2f}")
print()


def qualifies(span, main, rim, factor=1.0):
    d = design(span, main, rim)
    t = {k: v * factor for k, v in TARGETS.items()}
    return (d["octetEuler"] >= t["octetEuler"] and d["spokeEuler"] >= t["spokeEuler"]
            and d["tieEuler"] >= t["tieEuler"] and d["rimEuler"] >= t["rimEuler"]
            and d["rimBend"]["failsAtAtm"] >= t["rimBendAtm"]
            and d["spokeBend"]["marginPinnedAtSF"] >= t["spokeBendMargin"]
            and d["tieBend"]["marginPinnedAtSF"] >= t["tieBendMargin"]), d


for span in (1.0, 0.98):
    for factor, label in ((1.0, "PARITY with today"), (1.3, "+30% on every margin")):
        best, ranked = None, []
        for mo, mi in CATALOGUE:
            for ro, ri in CATALOGUE:
                if ro < mo:
                    continue
                main, rim = sec(mo / 1000, mi / 1000), sec(ro / 1000, ri / 1000)
                good, d = qualifies(span, main, rim, factor)
                if not good:
                    continue
                # TOTAL mass is the minimand, not tube mass: the joints grow as the cube of
                # the bore they socket, so a fatter pipe is paid for twice.
                d["nodesKg"] = pub["printed"]["nodesKg"] * (mo / 10.0) ** 3
                d["totalKg"] = d["tubeKg"] + d["nodesKg"] + d["filmKg"]
                ranked.append((d["totalKg"], d, (mo, mi), (ro, ri)))
                if best is None or d["totalKg"] < best[0]["totalKg"]:
                    best = (d, (mo, mi), (ro, ri))
        if not best:
            print(f"span {span}: nothing in the catalogue reaches {label}")
            continue
        d, m, r = best
        nodes, tot = d["nodesKg"], d["totalKg"]
        print(f"SPAN {span:.3f} — {label}: main {m[0]}x{m[1]}, rim {r[0]}x{r[1]}")
        print(f"  tube {d['tubeKg']:.2f} kg + joints ~{nodes:.2f} kg (od^3 estimate) "
              f"+ film {d['filmKg']*1000:.0f} g = {tot:.2f} kg")
        print(f"  {tot / (span**3/2):.2f} kg/m3   vs the wall 0.9569 -> "
              f"{tot / (span**3/2) / 0.9569:.1f}x   vs sea-level air "
              f"{tot / (1.225 * span**3/2):.1f}x")
        print(f"  octet {d['octetEuler']:.2f}  spoke {d['spokeEuler']:.2f}  "
              f"tie {d['tieEuler']:.2f}  rim {d['rimEuler']:.2f}  "
              f"rim bending fails at {d['rimBend']['failsAtAtm']:.2f} atm")
        print(f"  film {d['filmGPerM2']:.2f} g/m2 on the hexagons")
        for tk, dd, mm, rr in sorted(ranked)[1:4]:
            print(f"    next: {mm[0]}x{mm[1]} / {rr[0]}x{rr[1]}  {tk:.2f} kg "
                  f"(tube {dd['tubeKg']:.2f} + joints {dd['nodesKg']:.2f})")
        print()

# ---------------------------------------------------------------- pure geometric
print("PURE GEOMETRIC SCALE (what the law says, ignoring what is stocked)")
for span in (1.0, 0.98):
    k = span / S0
    main, rim = sec(0.010 * k, 0.008 * k), sec(0.014 * k, 0.012 * k)
    d = design(span, main, rim)
    nodes = pub["printed"]["nodesKg"] * k ** 3
    tot = d["tubeKg"] + nodes + d["filmKg"]
    print(f"  span {span}: main {10*k:.2f}x{8*k:.2f}, rim {14*k:.2f}x{12*k:.2f}  "
          f"({k:.4f}x)")
    print(f"    octet {d['octetEuler']:.2f}  spoke {d['spokeEuler']:.2f}  "
          f"tie {d['tieEuler']:.2f}  rim {d['rimEuler']:.2f}  "
          f"rim bending {d['rimBend']['failsAtAtm']:.2f} atm  (all unchanged)")
    print(f"    {tot:.2f} kg -> {tot/(span**3/2):.2f} kg/m3 (unchanged), "
          f"film {d['filmKg']*1000:.0f} g\n")

# ---------------------------------------------------------------- what a metre of array holds
print("WHAT THE SIZE BUYS")
for span in (0.709, 1.0):
    per_m3 = 2 / span ** 3           # BCC: two cells per span^3
    print(f"  span {span}: {per_m3:.2f} cells per m3, "
          f"{216 * per_m3:.0f} tube cuts and {51 * per_m3:.0f} printed joints per m3")

print("\nTHE BARRIER GETS EASIER (area per unit volume falls as 1/L)")
b0 = 2.90                                  # cm3/(m2 day), the 178 L article's budget
for span in (S0, 0.98, 1.0):
    f = vc.kelvin_faces(span)
    av = f["areaOverVolume"]
    print(f"  span {span:.4f}: {av:.4f} m2/m3, decade budget "
          f"{b0 * vc.kelvin_faces(S0)['areaOverVolume'] / av:.2f} cm3/(m2 day)")

print("\nPRINT AND ASSEMBLY PER CUBIC METRE OF SHIP")
for span, nodes_kg in ((S0, 0.465), (1.0, None)):
    per_m3 = 2 / span ** 3
    nk = nodes_kg if nodes_kg else 0.465 * (16 / 10.0) ** 3
    print(f"  span {span:.4f}: {51*per_m3:5.0f} joints/m3, {216*per_m3:5.0f} cuts/m3, "
          f"{nk*per_m3:5.2f} kg printed/m3, {nk/51*1000:4.1f} g per joint")
