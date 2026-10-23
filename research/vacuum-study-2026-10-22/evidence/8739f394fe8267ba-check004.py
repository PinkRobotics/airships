#!/usr/bin/env python3
"""Independent check of MAINLINE-004 (knockdown card) and MAINLINE-004b (kd range)
arithmetic. glm lead-sciences-73a25445. Own arithmetic; the owner's scripts are NOT read.

Restated model from the pins:
  Sealed base (003/006): R=10, p_ext=95460.83791390515 Pa, E=68.9e9, nu=0.33,
  sigma=276e6, rho_Al=2700, rho_core=16, lift=4889.442150186961 kg, systems=100,
  joints=5% of (faces+core).
  Sealed rows re-derived here from the mass ceiling (float margin 0):
    P2-A: core fixed 0.1 m, face solves.
    P2-C: face fixed 0.0002 m, core takes the ceiling.
    P2-K: one factor scales baseline face 0.0002 / core 0.1.
    P2-E: equal face mass and core mass.
  Classical sandwich pressure p_cl = 4*E*tf*d/(R^2*sqrt(1-nu^2)), d = face
  separation = core + tf (COMMON.md: reproduces 11701.558 Pa at the P2 baseline).
  SP-8032 text form: kd = 0.14 + 3.2/lambda^2 (lambda > 2),
  lambda = [12(1-nu^2)]^(1/4) * sqrt(R/t) * 2*sin(phi/2), phi = pi, t = t_eq.
  t_eq = (6*tf*d^2)^(1/3)  [hypothesis tested: d = face separation vs core].
  SF = kd*p_cl/p; E_req = E*p/(kd*p_cl) = E/SF; ratio = 0.2/kd_curve.
  004b rows: kd in {sp8032, 0.2, 0.9, 1.0, 0.22, 0.2-dimple}; opt/cons = 0.9/kd_sp.
"""
import json, math, re, sys

E, NU, SIGMA = 68.9e9, 0.33, 276e6
RHO_AL, RHO_CORE = 2700.0, 16.0
R = 10.0
P_EXT = 95460.83791390515
LIFT = 4889.442150186961
A = 4.0*math.pi*R*R

def masses(tf, c):
    faces = 2.0*A*tf*RHO_AL
    core = A*c*RHO_CORE
    joints = 0.05*(faces+core)
    return faces, core, joints

def p_cl(tf, c):
    d = c + tf
    return 4.0*E*tf*d/(R*R*math.sqrt(1.0-NU*NU))

def p_yield(tf):
    return 4.0*SIGMA*tf/R

# ---- sealed rows re-derived from the mass ceiling ----
rows = {}
# P2-A: core fixed 0.1
core = 0.1
coremass = A*core*RHO_CORE
faces = (LIFT - 100.0 - 1.05*coremass)/1.05
rows['P2-A'] = (faces/(2.0*A*RHO_AL), core)
# P2-C: face fixed 0.0002
tf = 0.0002
faces = 2.0*A*tf*RHO_AL
coremass = (LIFT - 100.0 - 1.05*faces)/1.05
rows['P2-C'] = (tf, coremass/(A*RHO_CORE))
# P2-K: one factor k scales baseline (0.0002, 0.1)
base_faces = 2.0*A*0.0002*RHO_AL
base_core = A*0.1*RHO_CORE
k = (LIFT - 100.0)/(1.05*(base_faces + base_core))
rows['P2-K'] = (0.0002*k, 0.1*k)
# P2-E: equal split
X = (LIFT - 100.0)/2.10
rows['P2-E'] = (X/(2.0*A*RHO_AL), X/(A*RHO_CORE))

# ---- card-stated values (regex from the two CARD.md files) ----
card4 = open(sys.argv[1]).read()
card4b = open(sys.argv[2]).read()

c4 = {}
for m in re.finditer(r"(P2-[ACKE])\n\nFace ([\d.e+-]+) m, core ([\d.e+-]+) m, equivalent thickness ([\d.e+-]+) m, "
                     r"R/t ([\d.e+-]+), lambda ([\d.e+-]+)\.\n\nPrior knockdown 0\.2, buckling SF ([\d.e+-]+), "
                     r"required modulus ([\d.e+-]+) Pa\.\n\nCurve knockdown ([\d.e+-]+)\. Buckling pressure ([\d.e+-]+) Pa\. "
                     r"Buckling SF ([\d.e+-]+)\. Required modulus ([\d.e+-]+) Pa, ratio to the 0\.2 result ([\d.e+-]+)\.\n\n"
                     r"QUESTIONABLE strength SF unchanged at ([\d.e+-]+)\.", card4):
    c4[m.group(1)] = dict(tf=float(m.group(2)), core=float(m.group(3)), teq=float(m.group(4)),
        rt=float(m.group(5)), lam=float(m.group(6)), sf02=float(m.group(7)), ereq02=float(m.group(8)),
        kd=float(m.group(9)), pb=float(m.group(10)), sf=float(m.group(11)), ereq=float(m.group(12)),
        ratio=float(m.group(13)), ysf=float(m.group(14)))

c4b = {}
for m in re.finditer(r"(P2-[ACKE])\n\nFace ([\d.e+-]+) m, core ([\d.e+-]+) m, face separation ([\d.e+-]+) m, "
                     r"lambda ([\d.e+-]+)\. QUESTIONABLE strength SF stays ([\d.e+-]+)\.\n\n"
                     r"Conservative knockdown ([\d.e+-]+)\. Buckling SF ([\d.e+-]+)\. Required face modulus ([\d.e+-]+) Pa, "
                     r"(above|below) the QUESTIONABLE alloy modulus 68\.9 GPa\.\n\n"
                     r"Central knockdown 0\.2\. Buckling SF ([\d.e+-]+)\. Required face modulus ([\d.e+-]+) Pa, "
                     r"(above|below) the QUESTIONABLE alloy modulus 68\.9 GPa\.\n\n"
                     r"Optimistic carry knockdown 0\.9\. Buckling SF ([\d.e+-]+)\. Required face modulus ([\d.e+-]+) Pa, "
                     r"(above|below) the QUESTIONABLE alloy modulus 68\.9 GPa\.\n\n"
                     r"Classical reference knockdown 1\. Buckling SF ([\d.e+-]+)\. Required face modulus ([\d.e+-]+) Pa, "
                     r"(above|below) the QUESTIONABLE alloy modulus 68\.9 GPa\.\n\n"
                     r"Sandwich flat knockdown 0\.22\. Buckling SF ([\d.e+-]+)\. Required face modulus ([\d.e+-]+) Pa, "
                     r"(above|below) the QUESTIONABLE alloy modulus 68\.9 GPa\.\n\n"
                     r"Sandwich dimle.*?Optimistic over conservative is ([\d.e+-]+)\.", card4b, re.S):
    c4b[m.group(1)] = dict(tf=float(m.group(2)), core=float(m.group(3)), d=float(m.group(4)),
        lam=float(m.group(5)), ysf=float(m.group(6)), kd_sp=float(m.group(7)),
        sf_sp=float(m.group(8)), ereq_sp=float(m.group(9)), sp_side=m.group(10),
        sf_02=float(m.group(11)), ereq_02=float(m.group(12)), c_side=m.group(13),
        sf_09=float(m.group(14)), ereq_09=float(m.group(15)), o_side=m.group(16),
        sf_10=float(m.group(17)), ereq_10=float(m.group(18)), cl_side=m.group(19),
        sf_22=float(m.group(20)), ereq_22=float(m.group(21)), f_side=m.group(22),
        ratio=float(m.group(23)))

report = {'schema': 1, 'card': 'MAINLINE-004+004b-check', 'checker': 'ref-c713c40ee838487ac6d3 (glm)',
          'tolerance_rel': 5e-9, 'mismatches': [], 'notes': [], 'derived_rows': {}}

def close(a, b, tol=5e-9):
    return abs(a-b) <= tol*max(1.0, abs(a), abs(b))

def side(v):  # "above/below the QUESTIONABLE alloy modulus 68.9 GPa"
    return 'below' if v < E else 'above'

lam_factor = (12.0*(1.0-NU*NU))**0.25 * 2.0*math.sin(math.pi/2.0)

for fam, (tf, c) in rows.items():
    faces, corem, joints = masses(tf, c)
    total = faces + corem + joints + 100.0
    d = c + tf
    pcl = p_cl(tf, c)
    py = p_yield(tf)
    # t_eq hypotheses
    teq_sep = (6.0*tf*d*d)**(1.0/3.0)
    teq_core = (6.0*tf*c*c)**(1.0/3.0)
    lam = lam_factor*math.sqrt(R/teq_sep)
    kd = 0.14 + 3.2/lam**2
    sf02 = 0.2*pcl/P_EXT
    sfcurve = kd*pcl/P_EXT
    report['derived_rows'][fam] = {
        'tf': tf, 'core': c, 'd': d, 'mass_total': total, 'faces': faces, 'core': corem,
        'teq_sep': teq_sep, 'teq_core': teq_core, 'lambda': lam, 'kd_sp8032': kd,
        'p_cl': pcl, 'p_yield': py, 'SF_kd02': sf02, 'SF_kdcurve': sfcurve,
        'Ereq02': E/sf02, 'Ereqcurve': E/sfcurve, 'yield_SF': py/P_EXT}

    r4 = c4.get(fam)
    if r4:
        fields = {
          'tf': (r4['tf'], tf), 'core': (r4['core'], c), 'teq': (r4['teq'], teq_sep),
          'R/t': (r4['rt'], R/teq_sep), 'lambda': (r4['lam'], lam), 'kd': (r4['kd'], kd),
          'pbuck': (r4['pb'], kd*pcl), 'SF': (r4['sf'], sfcurve),
          'Ereq': (r4['ereq'], E/sfcurve), 'ratio': (r4['ratio'], 0.2/kd),
          'SF02': (r4['sf02'], sf02), 'Ereq02': (r4['ereq02'], E/sf02),
          'yield_SF': (r4['ysf'], py/P_EXT)}
        for kk, (theirs, mine) in fields.items():
            if not close(theirs, mine):
                report['mismatches'].append({'card': '004', 'row': fam, 'field': kk, 'card': theirs, 'mine': mine})
        if not close(r4['teq'], teq_core):
            report['notes'].append(f"{fam}: card teq matches d=separation hypothesis ({teq_sep:.12g}); core-only hypothesis gives {teq_core:.12g} (excluded)")

    r4b = c4b.get(fam)
    if r4b:
        # 004b: SF_new = SF_sp*(kd_new/kd_sp) must equal fresh kd*p_cl/p within 1e-12
        for label, kdx, sf_card, ereq_card, side_card in (
            ('conservative', kd, r4b['sf_sp'], r4b['ereq_sp'], r4b['sp_side']),
            ('central', 0.2, r4b['sf_02'], r4b['ereq_02'], r4b['c_side']),
            ('optimistic', 0.9, r4b['sf_09'], r4b['ereq_09'], r4b['o_side']),
            ('classical', 1.0, r4b['sf_10'], r4b['ereq_10'], r4b['cl_side']),
            ('flat', 0.22, r4b['sf_22'], r4b['ereq_22'], r4b['f_side'])):
            sf_fresh = kdx*pcl/P_EXT
            sf_scaled = sfcurve*(kdx/kd)
            if abs(sf_fresh/sf_scaled - 1.0) > 1e-12:
                report['mismatches'].append({'card': '004b', 'row': fam, 'field': label+'_form_agreement', 'card': '1e-12', 'mine': abs(sf_fresh/sf_scaled-1.0)})
            if not close(sf_card, sf_fresh):
                report['mismatches'].append({'card': '004b', 'row': fam, 'field': label+'_SF', 'card': sf_card, 'mine': sf_fresh})
            if not close(ereq_card, E/sf_fresh):
                report['mismatches'].append({'card': '004b', 'row': fam, 'field': label+'_Ereq', 'card': ereq_card, 'mine': E/sf_fresh})
            if side(sf_fresh*E/1.0) if False else side_card != side(ereq_card if False else E/sf_fresh):
                report['mismatches'].append({'card': '004b', 'row': fam, 'field': label+'_side', 'card': side_card, 'mine': side(E/sf_fresh)})
        for kk, (theirs, mine) in {'tf': (r4b['tf'], tf), 'core': (r4b['core'], c), 'd': (r4b['d'], d),
                                   'lambda': (r4b['lam'], lam), 'kd_sp': (r4b['kd_sp'], kd),
                                   'yield_SF': (r4b['ysf'], py/P_EXT),
                                   'ratio_opt_cons': (r4b['ratio'], 0.9/kd)}.items():
            if not close(theirs, mine):
                report['mismatches'].append({'card': '004b', 'row': fam, 'field': kk, 'card': theirs, 'mine': mine})

# COMMON.md invariant: p_cl reproduces 11701.558 Pa at the P2 baseline tf=0.0002, core=0.1
base_pcl = p_cl(0.0002, 0.1)
report['notes'].append(f"COMMON.md invariant: my p_cl(tf=0.0002, core=0.1) = {base_pcl!r} Pa (006 sealed: 11701.558395327309)")
# mass-ceiling closure of re-derived rows
for fam, (tf, c) in rows.items():
    faces, corem, joints = masses(tf, c)
    report['notes'].append(f"{fam}: my total mass {faces+corem+joints+100.0!r} vs sealed lift {LIFT!r}")

print(json.dumps(report, indent=1, default=float))
