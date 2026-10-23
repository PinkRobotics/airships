#!/usr/bin/env python3
"""Independent check of MAINLINE-012 (equal float margin). glm lead-sciences-73a25445.

Own arithmetic from the pinned inputs (COMMON.md pins + CARD-006 brief + sealed 006
RESULTS model + sealed 001/003 atmosphere constants). The owner's script is NOT read.

Model, restated from the pins:
  ISA troposphere, sealed at 500 m: p500=95460.83791390515 Pa, rho500=1.1672683307461802,
  T500=284.9 K, lift at R=10 m: 4889.442150186961 kg.
  Sphere: V=(4/3)pi R^3, A=4 pi R^2.
  P2 sandwich: faces=2*A*tf*rho_Al (rho_Al=2700), core=A*c*rho_core (16),
  joints=0.05*(faces+core), systems=100 kg.
  Buckling pressure = kd*4*tf*(c+tf)*E/(R^2*sqrt(1-nu^2)), kd=0.2, E=68.9e9, nu=0.33.
  Yield pressure = 4*sigma*tf/R, sigma=276e6.
  SF = pressure limit / p_ext.
  P2-A: core fixed 0.1 m, face solves the mass ceiling.
  P2-E: faces mass = core mass, both solved from the ceiling.
  Ceiling: faces+core+joints+systems = (1-margin)*lift.
  Allowance twin: systems = 100*(R/10)^2 instead of 100, same ceiling; spread =
  card buckling SF - twin buckling SF.
Outputs my values for every CARD.md row; diffs against the card's stated numbers.
"""
import json, math, re, sys

# pinned constants (COMMON.md; sealed 003 RESULTS atmosphere block)
E = 68.9e9
NU = 0.33
SIGMA = 276e6
RHO_AL = 2700.0
RHO_CORE = 16.0
KD = 0.2
P500 = 95460.83791390515
RHO500 = 1.1672683307461802
T500 = 284.9
LIFT10 = 4889.442150186961  # sealed lift at R=10, 500 m

V10 = (4.0/3.0)*math.pi*10.0**3

def isa(h):
    """ISA troposphere. Return (T, p, rho). Constants: T0=288.15, p0=101325,
    lapse 0.0065 K/m, g=9.80665, R_spec from the sealed 500 m state."""
    T0, P0, LAPSE, G = 288.15, 101325.0, 0.0065, 9.80665
    T = T0 - LAPSE*h
    R_spec = P500/(RHO500*T500)
    p = P0*(1.0 - LAPSE*h/T0)**(G/(R_spec*LAPSE))
    rho = p/(R_spec*T)
    return T, p, rho

def sphere(R):
    return (4.0/3.0)*math.pi*R**3, 4.0*math.pi*R**2

def sandwich_pressures(tf, c, R):
    sep = c + tf                      # face separation d+tf per COMMON.md
    pb = KD*4.0*tf*sep*E/(R**2*math.sqrt(1.0-NU**2))
    py = 4.0*SIGMA*tf/R
    return pb, py

def masses(tf, c, R):
    V, A = sphere(R)
    faces = 2.0*A*tf*RHO_AL
    core = A*c*RHO_CORE
    joints = 0.05*(faces+core)
    return faces, core, joints

def solve_P2A(R, margin, systems=100.0):
    """core fixed 0.1 m; face thickness solves the ceiling."""
    V, A = sphere(R)
    lift = RHO500*V
    core = A*0.1*RHO_CORE
    budget = (1.0-margin)*lift
    # 1.05*faces + 1.05*core + systems = budget
    faces = (budget - systems - 1.05*core)/1.05
    if faces <= 0:
        return None
    tf = faces/(2.0*A*RHO_AL)
    return tf, 0.1, lift

def solve_P2E(R, margin, systems=100.0):
    """faces mass = core mass = X; 1.05*2X + systems = budget."""
    V, A = sphere(R)
    lift = RHO500*V
    budget = (1.0-margin)*lift
    X = (budget - systems)/2.10
    if X <= 0:
        return None
    tf = X/(2.0*A*RHO_AL)
    c = X/(A*RHO_CORE)
    return tf, c, lift

def solve_alt(family, h, margin):
    """Altitude row: R=10, atmosphere from ISA (lift from ISA rho)."""
    T, p, rho = isa(h)
    lift = rho*V10
    if family == 'P2-A':
        core = 4.0*math.pi*100.0*0.1*RHO_CORE
        budget = (1.0-margin)*lift
        faces = (budget - 100.0 - 1.05*core)/1.05
        if faces <= 0:
            return {'infeasible': True, 'T': T, 'p': p, 'lift': lift}
        tf = faces/(2.0*4.0*math.pi*100.0*RHO_AL); c = 0.1
    else:
        X = ((1.0-margin)*lift - 100.0)/2.10
        if X <= 0:
            return {'infeasible': True, 'T': T, 'p': p, 'lift': lift}
        tf = X/(2.0*4.0*math.pi*100.0*RHO_AL)
        c = X/(4.0*math.pi*100.0*RHO_CORE)
    pb, py = sandwich_pressures(tf, c, 10.0)
    return {'tf': tf, 'c': c, 'T': T, 'p': p, 'lift': lift,
            'buck_SF': pb/p, 'yield_SF': py/p}

def twin_spread(family, R, margin):
    """Rescale with systems = 100*(R/10)^2; spread = SF_card - SF_twin."""
    main = (solve_P2A if family == 'P2-A' else solve_P2E)(R, margin, systems=100.0)
    twin = (solve_P2A if family == 'P2-A' else solve_P2E)(R, margin, systems=100.0*(R/10.0)**2)
    if main is None or twin is None:
        return None
    tfm, cm, lift = main
    tft, ct, _ = twin
    pbm, _ = sandwich_pressures(tfm, cm, R)
    pbt, _ = sandwich_pressures(tft, ct, R)
    _, p, _ = isa(500.0)
    return pbm/p - pbt/p

# ---- transcribe the card's stated numbers (regex from CARD.md) ----
CARD = open(sys.argv[1]).read()

radius_rows = []
for m in re.finditer(r"(P2-[AE]) R (\d+) m, margin ([\d.]+)\. Face ([\d.e+-]+) m, core ([\d.e+-]+) m\. "
                     r"Buckling SF ([\d.e+-]+)\. Yield SF ([\d.e+-]+)\. Least SF ([\d.e+-]+)\. "
                     r"Allowance spread ([\d.e+-]+)\.", CARD):
    radius_rows.append(dict(family=m.group(1), R=float(m.group(2)), margin=float(m.group(3)),
        tf=float(m.group(4)), core=float(m.group(5)), buck=float(m.group(6)),
        yield_=float(m.group(7)), least=float(m.group(8)), spread=float(m.group(9))))

alt_rows = []
for m in re.finditer(r"(P2-[AE]) altitude (\d+) m, margin ([\d.]+)\. T ([\d.]+) K\. Pressure ([\d.]+) Pa\. "
                     r"Lift ([\d.]+) kg\. Buckling SF ([\d.e+-]+)\. Yield SF ([\d.e+-]+)\. Least SF ([\d.e+-]+)\. "
                     r"Lift-per-pressure versus 500 m is ([\d.e+-]+)\. Buckling SF versus 500 m is ([\d.e+-]+)\. "
                     r"Cold-air fraction left in the safety factor is ([\d.e+-]+)\.", CARD):
    alt_rows.append(dict(family=m.group(1), h=float(m.group(2)), margin=float(m.group(3)),
        T=float(m.group(4)), p=float(m.group(5)), lift=float(m.group(6)), buck=float(m.group(7)),
        yield_=float(m.group(8)), least=float(m.group(9)), lpp=float(m.group(10)),
        sfr=float(m.group(11)), cold=float(m.group(12))))

report = {'schema': 1, 'card': 'MAINLINE-012-check', 'checker': 'ref-c713c40ee838487ac6d3 (glm)',
          'tolerance_abs': 5e-9, 'mismatches': [], 'notes': []}

def close(a, b, tol=5e-9):
    return abs(a-b) <= tol*max(1.0, abs(a), abs(b))

# ---- radius rows ----
for row in radius_rows:
    fam, R, margin = row['family'], row['R'], row['margin']
    solver = solve_P2A if fam == 'P2-A' else solve_P2E
    got = solver(R, margin)
    if got is None:
        report['notes'].append(f"{fam} R={R} m={margin}: card 'Infeasible'; my solve also infeasible (faces<=0)" if 'Infeasible' in CARD else f"{fam} R={R} m={margin}: my solve infeasible but card has numbers")
        continue
    tf, c, lift = got
    pb, py = sandwich_pressures(tf, c, R)
    T500_, p500, _ = isa(500.0)
    buck, yld = pb/p500, py/p500
    spread = twin_spread(fam, R, margin)
    fields = {'tf': (row['tf'], tf), 'core': (row['core'], c),
              'buck_SF': (row['buck'], buck), 'yield_SF': (row['yield_'], yld),
              'least_SF': (row['least'], min(buck, yld)), 'spread': (row['spread'], spread)}
    for k, (theirs, mine) in fields.items():
        if not close(theirs, mine):
            report['mismatches'].append({'row': f'{fam} R={R} m={margin}', 'field': k,
                                         'card': theirs, 'mine': mine})

# infeasibility checks the card asserts
for fam, R, margin in [('P2-A', 5.0, 0.0), ('P2-A', 5.0, 0.05)]:
    got = solve_P2A(R, margin)
    report['notes'].append(f"{fam} R={R} m={margin}: card Infeasible; my solve {'infeasible' if got is None else 'FEASIBLE tf=%.6g' % got[0]}")

# ---- altitude rows ----
base = {}
for fam in ('P2-A', 'P2-E'):
    for margin in (0.0, 0.05):
        got = solve_alt(fam, 500.0, margin)
        if not got.get('infeasible'):
            base[(fam, margin)] = got
for row in alt_rows:
    fam, h, margin = row['family'], row['h'], row['margin']
    mine = solve_alt(fam, h, margin)
    if mine.get('infeasible'):
        report['notes'].append(f"{fam} h={h} m={margin}: card {'Infeasible' if ('%s altitude %d m, margin %.2f. Infeasible' % (fam, h, margin)) in CARD else 'HAS NUMBERS'}; my solve infeasible (faces<=0: core alone exceeds budget)")
        continue
    lpp = (mine['lift']/mine['p'])/(LIFT10/P500)
    sfr = mine['buck_SF']/base[(fam, margin)]['buck_SF'] if h != 500.0 else 1.0
    cold = sfr/(T500/mine['T'])
    fields = {'T': (row['T'], mine['T']), 'p': (row['p'], mine['p']), 'lift': (row['lift'], mine['lift']),
              'buck_SF': (row['buck'], mine['buck_SF']), 'yield_SF': (row['yield_'], mine['yield_SF']),
              'least_SF': (row['least'], min(mine['buck_SF'], mine['yield_SF'])),
              'lpp': (row['lpp'], lpp), 'sfr': (row['sfr'], sfr), 'cold': (row['cold'], cold)}
    for k, (theirs, mn) in fields.items():
        if not close(theirs, mn):
            report['mismatches'].append({'row': f'{fam} h={h} m={margin}', 'field': k,
                                         'card': theirs, 'mine': mn})

# P2-A 11 km infeasibility the card asserts
for margin in (0.0, 0.05):
    got = solve_alt('P2-A', 11000.0, margin)
    report['notes'].append(f"P2-A h=11000 m={margin}: card Infeasible; my solve {'infeasible' if got.get('infeasible') else 'FEASIBLE'}")

# ---- ISA sanity ----
T500_, p_isa_500, rho_isa = isa(500.0)
report['notes'].append(f"ISA check at 500 m: my p={p_isa_500!r} vs sealed {P500!r} (diff {p_isa_500-P500:+.6f} Pa); card claims within 0.1 Pa")
report['notes'].append(f"ISA rho500 mine={rho_isa!r} vs sealed {RHO500!r}")

print(json.dumps(report, indent=1, default=float))
