#!/usr/bin/env python3
"""MAINLINE-013: ultralight core properties against the P2 float-ceiling needs, at each core's own density.

Own arithmetic, from the pinned inputs named in INPUTS.json. Nothing here is a certification; every sourced value
is QUESTIONABLE and every scale-up or extrapolated value is PROJECTION.

Rows (MAINLINE-007's two splits, rebuilt at any core density):
  B  the split that maximises knocked-down buckling: tf = M/(2A(2*rho_f - rho_c))
  Q  the split that maximises the lesser of buckling and yield: on the equal-factor line h = h_eq when B's separation
     exceeds h_eq, otherwise the same point as B.
Needs on each row (the card's three checks):
  crush     core compressive strength >= p/2 (MAINLINE-005b's QUESTIONABLE model)
  crimp     CR-1457 shear-crimp pressure 2*h^2*Gc/(R*tc) >= p  (eqs 6.2-27 and 6.2-29 with gamma_d = 1 on that branch)
  wrinkle   CR-1457 equibiaxial face wrinkling stress >= the face membrane stress p*R/(4*tf)
            continuum (solid or foam) form eq 2.2-5, Q = 0.50, with eq 2.2-6 (Rx^3 + Ry = 1) at Rx = Ry
            honeycomb form eq 2.2-14 (0.33), with eq 2.2-15, the same interaction
Margins are provided/required; a margin below 1 is a gap of 1/margin on the stated quantity.

Run: python3 -I compute.py   (writes RESULTS.json and INPUTS.json beside this file; reads cores.json)
"""
import datetime
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STARTED = datetime.datetime.now().astimezone().isoformat()
JOB_STARTED = "2026-10-19T23:20:07-07:00"   # the order was read (date at that moment); a measurement, not a limit

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_pins():
    out = []
    for path, want in PINS:
        got = sha256(path)
        if got != want:
            sys.exit(f"PIN MISMATCH {path}: {got} != {want}")
        out.append({"path": path, "sha256": got, "bytes": os.path.getsize(path)})
    return out


PIN_RECORDS = verify_pins()
R001 = json.load(open(PINS[2][0]))
R007 = json.load(open(PINS[16][0]))
R007B = json.load(open(PINS[18][0]))

# ---------------------------------------------------------------- the case (COMMON.md; values read from 001 RESULTS)
R = 10.0                                         # m, external radius
P = R001["atmosphere"]["p_ext_Pa"]               # 95460.8379139 Pa at 500 m ISA, p_int = 0
LIFT = R001["atmosphere"]["lift_kg"]             # 4889.44215019 kg
SYSTEMS = 100.0                                  # kg, P2 rule (MAINLINE-002)
JOINT = 0.05                                     # joints as a fraction of the sandwich (MAINLINE-002)
E_F, NU_F, SIG_Y, RHO_F = 68.9e9, 0.33, 276e6, 2700.0   # 6061-T6; sigma is QUESTIONABLE (COMMON.md)
KD = 0.2                                         # knockdown; MAINLINE-004 replaces it
AREA = 4.0 * math.pi * R * R                     # faces and core both use the external area (MAINLINE-007)
M_STRUCT = (LIFT - SYSTEMS) / (1.0 + JOINT)      # float ceiling, margin 0
S1NU2 = math.sqrt(1.0 - NU_F ** 2)
H_EQ = SIG_Y * R * S1NU2 / (KD * E_F)            # separation where buckling SF equals yield SF (MAINLINE-007)

# ---------------------------------------------------------------- CR-1457 (NASA CR-1457, Sullins, Smith and Spier, 1969)
Q_FOAM_DESIGN = 0.50       # eq 2.2-5: "Q = 0.50 be used to obtain a lower-bound prediction" (p. 2-26)
HC_DESIGN = 0.33           # eq 2.2-14: lower-bound honeycomb wrinkling coefficient (p. 2-33)
HC_CLASSICAL = 0.82        # eq 2.2-12 with K_delta = 0: initially perfect facings, the upper-bound classical value (p. 2-33)
GAMMA_D = 0.20             # eq 6.2-13, hemispheres, "except where shear crimping occurs" (p. 6-10)
CRUSH_REQ = P / 2.0        # MAINLINE-005b, QUESTIONABLE
# The second level, carried as a column only: NASA/CR-1999-208994 (Ley, Lin and Mbanefo, 1999), Table 3 "Theory (upper
# bound)" k1 = 0.76 for sigma_wr = k1*(Ef*Ec*Gc)^(1/3) (Cox and Riddell, thick core); its Table 1 runs 0.76-0.96 (Hoff and
# Mautner 0.91). Used here in place of Q inside eq 2.2-5, so it keeps CR-1457's (1 - nu^2) factor (a 3.9% difference).
Q_FOAM_CLASSICAL = 0.76
DESIGN_SOURCE = PINS[20][0]
REVIEW_PDF = os.path.join(HERE, "NASA-CR-1999-208994.pdf")
REVIEW_SHA = "50251cdb5314d72abd0712dc559f6be5d1c39f33e99875ed0664115652bcaf3c"


def equibiaxial_factor():
    """R with R^3 + R = 1: eqs 2.2-6 and 2.2-15 at Rx = Ry (the sphere's membrane state is equibiaxial)."""
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid ** 3 + mid - 1.0 > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


EQB = equibiaxial_factor()


# ---------------------------------------------------------------- rows
def make_row(rho_c, tf, tc, split):
    h = tc + tf
    faces = 2.0 * AREA * tf * RHO_F
    core = AREA * tc * rho_c
    joints = JOINT * (faces + core)
    total = faces + core + joints + SYSTEMS
    p_b = KD * 4.0 * tf * h * E_F / (R * R * S1NU2)
    p_y = 4.0 * SIG_Y * tf / R
    sigma_face = P * R / (4.0 * tf)
    sigma0 = E_F * h / (R * S1NU2)                             # eq 6.2-26 (eta = 1)
    row = {
        "split": split, "rho_core_kg_m3": rho_c, "tf_m": tf, "tc_m": tc, "h_m": h,
        "tc_over_R": tc / R,
        "masses_kg": {"faces": faces, "core": core, "joints": joints, "systems": SYSTEMS},
        "all_mass_kg": total, "float_margin_kg": LIFT - total,
        "SF_b": p_b / P, "SF_y": p_y / P, "least_SF": min(p_b, p_y) / P,
        "face_stress_Pa": sigma_face,
        "sigma0_Pa": sigma0,
        # needs
        "crush_req_Pa": CRUSH_REQ,
        "Gc_req_crimp_Pa": P * R * tc / (2.0 * h * h),         # 2 h^2 Gc/(R tc) = p   (eqs 6.2-27, 6.2-29, gamma_d = 1)
        "Gc_req_crimp_advisory_Pa": P * R / (2.0 * h),         # MAINLINE-007's p = 2 Gc d / R
        "Gc_at_Vc_2_Pa": sigma0 * tf * tc / (h * h),           # crimping branch boundary (MAINLINE-007b)
        "EcGc_req_foam_design_Pa2": (1.0 - NU_F ** 2) / E_F * (sigma_face / (Q_FOAM_DESIGN * EQB)) ** 3,
        "EcGc_req_foam_classical_Pa2": (1.0 - NU_F ** 2) / E_F * (sigma_face / (Q_FOAM_CLASSICAL * EQB)) ** 3,
        "EcGc_req_advisory_Pa2": (2.0 * sigma_face) ** 3 / E_F,  # MAINLINE-007's uniaxial advisory product
        "Ec_req_honeycomb_design_Pa": E_F * tc / tf * (sigma_face / (EQB * HC_DESIGN * E_F)) ** 2,
        "Ec_req_honeycomb_classical_Pa": E_F * tc / tf * (sigma_face / (EQB * HC_CLASSICAL * E_F)) ** 2,
        # a fourth local mode, outside the card's three and reported beside them: intracell buckling (face dimpling),
        # CR-1457 eq 2.1-4 sigma_cr = 2.0*Ef/(1-nu^2)*(tf/s)^2 with the straight-line biaxial rule eq 2.1-6 (Rx + Ry = 1),
        # so each direction carries half: the largest cell (inscribed circle s) is tf*sqrt(Ef/((1-nu^2)*sigma_face))
        "cell_max_dimpling_m": tf * math.sqrt(E_F / ((1.0 - NU_F ** 2) * sigma_face)),
    }
    row["geometry_flag"] = ("INVALID: core thicker than the radius" if tc >= R else
                            "QUESTIONABLE: core over a tenth of the radius; external-area and thin-shell rules strained"
                            if tc > 0.1 * R else "ok")
    return row


def row_b(rho_c):
    tf = M_STRUCT / (2.0 * AREA * (2.0 * RHO_F - rho_c))
    tc = (M_STRUCT / AREA - 2.0 * tf * RHO_F) / rho_c
    return make_row(rho_c, tf, tc, "B")


def row_q(rho_c):
    b = row_b(rho_c)
    if b["h_m"] <= H_EQ:
        return dict(b, split="Q=B")
    tf = (M_STRUCT / AREA - H_EQ * rho_c) / (2.0 * RHO_F - rho_c)
    return make_row(rho_c, tf, H_EQ - tf, "Q")


def crossover_density():
    """Density where B's separation equals h_eq; below it the two splits differ."""
    lo, hi = 0.5, 64.0
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if row_b(mid)["h_m"] > H_EQ:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


# ---------------------------------------------------------------- one core on one row
def shear_trim(row, gc):
    """CR-1457 6.2: Vc, Kc and the general-instability SF with core shear (gamma_d 0.20, or 1 on the crimping branch)."""
    s_crimp = row["h_m"] ** 2 * gc / (2.0 * row["tf_m"] * row["tc_m"])
    vc = row["sigma0_Pa"] / s_crimp
    if vc <= 2.0:
        kc, gd, branch = 1.0 - vc / 4.0, GAMMA_D, "moderate"
    else:
        kc, gd, branch = 1.0 / vc, 1.0, "crimping"
    p_cr = 4.0 * gd * kc * row["sigma0_Pa"] * row["tf_m"] / R
    return {"Vc": vc, "Kc": kc, "gamma_d": gd, "branch": branch, "SF_general": p_cr / P,
            "SF_general_over_kd_buckling": (p_cr / P) / row["SF_b"]}


def evaluate(core, row):
    ec, gc, sc = core.get("E_c_Pa"), core.get("G_c_used_Pa"), core.get("sigma_c_Pa")
    out = {"split": row["split"], "geometry_flag": row["geometry_flag"]}
    out["crush_margin"] = sc / row["crush_req_Pa"] if sc else None
    # a large-strain, undefined-strain, indentation or tension strength can fail crush but cannot pass it
    out["crush_basis"] = core.get("sigma_c_class")
    out["crush_unproven"] = bool(sc and core.get("sigma_c_class") != "structural" and out["crush_margin"] >= 1.0)
    out["core_strain_at_p_over_2_linear"] = row["crush_req_Pa"] / ec if ec else None
    if gc:
        out["crimp_margin"] = gc / row["Gc_req_crimp_Pa"]
        out["shear"] = shear_trim(row, gc)
    else:
        out["crimp_margin"], out["shear"] = None, None
    form = "honeycomb" if core["wrinkle_form"] == "honeycomb" else "continuum"
    out["wrinkle_form"] = form
    if form == "honeycomb":
        if ec:
            s_wr = EQB * HC_DESIGN * E_F * math.sqrt(ec * row["tf_m"] / (E_F * row["tc_m"]))
            out["wrinkle_stress_margin"] = s_wr / row["face_stress_Pa"]
            out["wrinkle_quantity"] = "Ec"
            out["wrinkle_quantity_margin"] = ec / row["Ec_req_honeycomb_design_Pa"]
            out["wrinkle_quantity_margin_classical_0p82"] = ec / row["Ec_req_honeycomb_classical_Pa"]
        else:
            out["wrinkle_stress_margin"] = out["wrinkle_quantity_margin"] = None
    else:
        if ec and gc:
            s_wr = EQB * Q_FOAM_DESIGN * (E_F * ec * gc / (1.0 - NU_F ** 2)) ** (1.0 / 3.0)
            out["wrinkle_stress_margin"] = s_wr / row["face_stress_Pa"]
            out["wrinkle_quantity"] = "EcGc"
            out["wrinkle_quantity_margin"] = ec * gc / row["EcGc_req_foam_design_Pa2"]
            out["wrinkle_quantity_margin_classical_0p76"] = ec * gc / row["EcGc_req_foam_classical_Pa2"]
        else:
            out["wrinkle_stress_margin"] = out["wrinkle_quantity_margin"] = None
    cell = core.get("cell_size_m")
    out["dimpling_cell_margin"] = row["cell_max_dimpling_m"] / cell if cell else None   # beside the three, not in the verdict
    checks = [out["crush_margin"], out["crimp_margin"], out["wrinkle_quantity_margin"]]
    if any(m is not None and m < 1.0 for m in checks):
        out["verdict"] = "FAIL"
    elif out["crush_unproven"]:
        out["verdict"] = "INCOMPLETE"
    elif all(m is not None for m in checks):
        out["verdict"] = "PASS" if row["geometry_flag"] == "ok" else "PASS_GEOMETRY_QUESTIONABLE"
    else:
        out["verdict"] = "INCOMPLETE"
    gaps = []
    if out["crush_margin"] is not None and out["crush_margin"] < 1:
        gaps.append({"check": "crush", "property": "compressive strength", "factor": 1.0 / out["crush_margin"]})
    if out["crimp_margin"] is not None and out["crimp_margin"] < 1:
        gaps.append({"check": "crimp", "property": "transverse shear modulus Gc", "factor": 1.0 / out["crimp_margin"]})
    if out["wrinkle_quantity_margin"] is not None and out["wrinkle_quantity_margin"] < 1:
        q = "through-thickness modulus Ec" if form == "honeycomb" else "product Ec*Gc"
        gaps.append({"check": "wrinkle", "property": q, "factor": 1.0 / out["wrinkle_quantity_margin"],
                     "stress_factor": 1.0 / out["wrinkle_stress_margin"]})
    out["gaps"] = gaps
    return out


# ---------------------------------------------------------------- PROJECTION: the ideal stretch-dominated lattice
# Ashby, Phil. Trans. R. Soc. A 364 (2006) 15-30, doi 10.1098/rsta.2005.1678, eq 5.1: E/Es ~ (1/3)(rho/rho_s) for a
# stretch-dominated lattice, so Ec = rho*S/3 with S = Es/rho_s the strut material's specific stiffness. Gc = Ec/2 is
# the optimistic isotropic bound (G = E/(2(1+nu)) at nu = 0). Then EcGc = rho^2*S^2/18 and Gc = rho*S/6. Strength is
# not projected: eq 5.2's (1/3) rho_rel sigma_y is an upper bound, and the elastic strut-buckling constant of eq 5.3
# is not given there.
STRUT_REFERENCES = [
    # (name, S in m^2/s^2 = Pa per kg/m3, tag, where the E and density come from)
    ("6061-T6", 68.9e9 / 2700.0, "QUESTIONABLE", "COMMON.md: E 68.9 GPa, 2700 kg/m3"),
    ("ALD alumina (the Meza lattices' wall)", 165e9 / 2900.0, "QUESTIONABLE",
     "Meza et al. PNAS 2015 Table 1: Es 165 GPa (20 nm Al2O3); Meza et al. Science 2014 main text: rho_s 2900 kg/m3"),
    ("beryllium S-200F", 303e9 / 1850.0, "QUESTIONABLE", "008b RESULTS candidate (Materion sheet): E 303 GPa, 1850 kg/m3"),
    ("CNT yarn, unidirectional", 256e9 / 1000.0, "PROJECTION", "008b RESULTS candidate source text: specific modulus 256 GPa per g/cc, unidirectional"),
    ("K13D2U pitch fibre tow", 935e9 / 2200.0, "QUESTIONABLE", "008b RESULTS candidate source text: tow 935 GPa, 2.20 g/cc (fibre, not a strut composite)"),
]


def ideal_lattice_needs(row, q=Q_FOAM_DESIGN):
    """Strut specific stiffness an ideal stretch-dominated lattice core needs on this row, per check."""
    rho = row["rho_core_kg_m3"]
    need = (1.0 - NU_F ** 2) / E_F * (row["face_stress_Pa"] / (q * EQB)) ** 3
    return {"S_req_wrinkle": math.sqrt(18.0 * need) / rho, "S_req_crimp": 6.0 * row["Gc_req_crimp_Pa"] / rho}


def ideal_lattice_threshold(S, split, q=Q_FOAM_DESIGN):
    """Lightest density (0.1-200 kg/m3) at which an ideal lattice of specific stiffness S passes wrinkling and crimp
    on the named split; None if it never does in that range. Scanned on a fine geometric grid, then bisected."""
    rowf = row_q if split == "Q" else row_b
    def ok(r):
        n = ideal_lattice_needs(rowf(r), q)
        return S >= n["S_req_wrinkle"] and S >= n["S_req_crimp"]
    grid = [0.1 * (1.01 ** i) for i in range(int(math.log(2000) / math.log(1.01)) + 1)]
    prev = None
    for r in grid:
        if ok(r):
            if prev is None:
                return r
            lo, hi = prev, r
            for _ in range(100):
                mid = 0.5 * (lo + hi)
                if ok(mid):
                    hi = mid
                else:
                    lo = mid
            return hi
        prev = r
    return None


# ---------------------------------------------------------------- reproduction checks against the sealed cards
def close(a, b, rel=1e-9):
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-300)


def checks():
    res = {}
    # 007 rows, both splits, every named density
    n = bad = 0
    for key, pair in R007["rows"].items():
        rho = float(key)
        for rule, mine in (("max_buckling_SF", row_b(rho)), ("max_least_SF", row_q(rho))):
            ref = pair[rule]
            for a, b in ((mine["tf_m"], ref["tf_m"]), (mine["tc_m"], ref["core_m"]), (mine["h_m"], ref["separation_m"]),
                         (mine["SF_b"], ref["SF_b"]), (mine["SF_y"], ref["SF_y"]), (mine["face_stress_Pa"], ref["membrane_stress_Pa"]),
                         (mine["Gc_req_crimp_advisory_Pa"], ref["Gc_crimp_Pa"]), (mine["EcGc_req_advisory_Pa2"], ref["Ec_times_Gc_Pa2"]),
                         (mine["all_mass_kg"], ref["all_mass_kg"]), (mine["crush_req_Pa"], ref["crush_target_Pa"])):
                n += 1
                bad += 0 if close(a, b, 1e-9) else 1
    res["007_rows_fields"] = {"compared": n, "mismatched": bad, "result": "PASS" if bad == 0 else "FAIL"}
    # 007b: the biaxial factor, the Vc = 2 boundary on every row and at P2-E, and two core comparisons
    res["007b_biaxial_factor"] = "PASS" if close(EQB, R007B["biaxial_factor"], 1e-12) else "FAIL"
    m = 0
    for g in R007B["Gc_at_crimp_boundary"]:
        tf, tc = g["tf_m"], g["core_m"]
        h = tf + tc
        mine = (E_F * h / (R * S1NU2)) * tf * tc / (h * h)
        m += 0 if close(mine, g["Gc_for_Vc_equals_2_Pa"], 1e-9) else 1
    res["007b_Gc_at_Vc_2"] = {"compared": len(R007B["Gc_at_crimp_boundary"]), "mismatched": m,
                              "result": "PASS" if m == 0 else "FAIL"}
    for c in R007B["comparisons"]:
        if c.get("material") == "Hexcel HRH-10-4.8-32" and c.get("geometry") == "rho_32.0_max_buckling_SF":
            row = row_b(32.0)
            ev = evaluate({"E_c_Pa": c["Ec_Pa"], "G_c_used_Pa": c["Gc_Pa"], "sigma_c_Pa": None, "wrinkle_form": "honeycomb"}, row)
            ok = close(ev["wrinkle_stress_margin"], c["honeycomb_wrinkling"]["SF_wr_equibiaxial"], 1e-9) and \
                close(ev["shear"]["Vc"], c["Vc"], 1e-9) and close(ev["shear"]["SF_general"], c["SF_general"], 1e-9)
            res["007b_HRH10_32_honeycomb_wrinkle_and_shear"] = "PASS" if ok else "FAIL"
        if c.get("material") == "ROHACELL 31 IG-F" and c.get("geometry") == "rho_32.0_max_buckling_SF":
            row = row_b(32.0)
            ev = evaluate({"E_c_Pa": c["Ec_Pa"], "G_c_used_Pa": c["Gc_Pa"], "sigma_c_Pa": None, "wrinkle_form": "continuum"}, row)
            ok = close(ev["wrinkle_stress_margin"], c["foam_wrinkling"]["SF_wr_equibiaxial"], 1e-9) and \
                close(ev["shear"]["Kc"], c["Kc"], 1e-9)
            res["007b_Rohacell31_foam_wrinkle_and_shear"] = "PASS" if ok else "FAIL"
    # the 007 headline: buckling SF reaches 1 at 3.73369568197 kg/m3 on the buckling-optimal split
    lo, hi = 1.0, 8.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if row_b(mid)["SF_b"] > 1.0:
            lo = mid
        else:
            hi = mid
    res["007_SFb_1_density"] = {"mine": 0.5 * (lo + hi), "sealed": R007["sf_b_reaches_1"]["rho_core_kg_m3"]
                                if isinstance(R007.get("sf_b_reaches_1"), dict) and "rho_core_kg_m3" in R007["sf_b_reaches_1"] else None}
    return res


# ---------------------------------------------------------------- summaries
CHECK_KEYS = (("crush", "crush_margin"), ("crimp", "crimp_margin"), ("wrinkle", "wrinkle_quantity_margin"))


def band_summary(cores, lo, hi, split="Q", statuses=("MEASURED",)):
    """Best margin per check among the band's cores on one split. A crush margin from a non-structural strength
    counts only below 1 (it can show a failure, never a pass)."""
    sel = [c for c in cores if lo <= c["density_kg_m3"] <= hi and c.get("status") in statuses]
    best = {}
    for check, key in CHECK_KEYS + (("crush_large_strain_upper_bound", "crush_margin"),):
        top = None
        for c in sel:
            ev = c["rows"][split]
            m = ev.get(key)
            if m is None:
                continue
            if check == "crush" and ev.get("crush_basis") != "structural":
                continue           # ranked on structural strengths only
            if check == "crush_large_strain_upper_bound" and ev.get("crush_basis") == "structural":
                continue           # the other strengths: each an upper bound on its core's true crush margin
            if top is None or m > top[0]:
                top = (m, c)
        if top is None:
            best[check] = None
            continue
        m, c = top
        ev = c["rows"][split]
        entry = {"best_margin": m, "core_id": c["core_id"], "density_kg_m3": c["density_kg_m3"],
                 "family": c["family"], "passes": m >= 1.0}
        if m < 1.0:
            entry["gap_factor"] = 1.0 / m
        if check == "wrinkle":
            entry["quantity"] = ev.get("wrinkle_quantity")
            entry["stress_margin"] = ev.get("wrinkle_stress_margin")
        best[check] = entry
    passing = [c["core_id"] for c in sel if c["rows"][split]["verdict"] == "PASS"]
    return {"band_kg_m3": [lo, hi], "split": split, "statuses": list(statuses), "n_cores": len(sel),
            "best": best, "passing_all_three": passing}


def fmt(x, sig=3):
    if x is None:
        return "none"
    if isinstance(x, (int, float)):
        if x == 0:
            return "0"
        if abs(x) >= 1e5 or abs(x) < 1e-3:
            return f"{x:.{sig}g}"
        return f"{x:.{sig}g}"
    return str(x)


def card_block(c):
    """One short block per core, plain sentences, every number from RESULTS."""
    q, b = c["rows"]["Q"], c["rows"]["B"]
    src = c.get("source") or {}
    where = src.get("doi") and f"doi {src['doi']}" or src.get("url") or "no locator"
    lines = [f"**{c.get('name') or c['core_id']}** ({c['core_id']}), {fmt(c['density_kg_m3'])} kg/m3, {c['family']}, "
             f"{c.get('status')}, QUESTIONABLE."]
    props = []
    props.append(f"Ec {fmt(c.get('E_c_Pa'))} Pa" if c.get("E_c_Pa") else "no Ec")
    if c.get("G_c_used_Pa"):
        props.append(f"Gc {fmt(c['G_c_used_Pa'])} Pa ({'sourced' if c.get('G_c_used_basis') == 'sourced' else 'DERIVED as Ec/2'})")
    else:
        props.append("no Gc")
    if c.get("sigma_c_Pa"):
        props.append(f"strength {fmt(c['sigma_c_Pa'])} Pa ({'structural' if c.get('sigma_c_class') == 'structural' else 'large-strain or not uniaxial: can fail crush, cannot pass it'})")
    else:
        props.append("no strength")
    lines.append("; ".join(props) + ".")
    def row_sentence(tag, ev):
        parts = [f"crush {fmt(ev['crush_margin'])}" + (" (unproven: large-strain basis)" if ev.get("crush_unproven") else ""),
                 f"crimp {fmt(ev['crimp_margin'])}"]
        if ev.get("wrinkle_quantity_margin") is not None:
            parts.append(f"wrinkling {fmt(ev['wrinkle_quantity_margin'])} on {ev.get('wrinkle_quantity')} "
                         f"({fmt(ev.get('wrinkle_stress_margin'))} on stress)")
        else:
            parts.append("wrinkling not computable")
        if ev.get("dimpling_cell_margin") is not None:
            parts.append(f"dimpling cell {fmt(ev['dimpling_cell_margin'])}")
        worst = max(ev["gaps"], key=lambda g: g["factor"]) if ev["gaps"] else None
        binds = f" Binds: {worst['check']}, needs {fmt(worst['factor'])}x {worst['property']}." if worst else ""
        geo = "" if ev["geometry_flag"] == "ok" else f" Geometry {ev['geometry_flag'].split(':')[0]}."
        return f"{tag}: {ev['verdict']}; " + ", ".join(parts) + "." + binds + geo
    lines.append(row_sentence("Least-factor split" if q["split"] != "Q=B" else "One split point", q))
    if q["split"] != "Q=B":
        lines.append(row_sentence("Buckling split", b))
    cite = (src.get("citation") or "").strip()
    lines.append(f"Source: {cite[:110]}{'...' if len(cite) > 110 else ''}; {where}; {(src.get('location') or '')[:70]}; "
                 f"{c.get('reading') or ''}.")
    return " ".join(lines)


# ---------------------------------------------------------------- cores
def load_cores():
    path = os.path.join(HERE, "cores.json")
    if not os.path.exists(path):
        return {"cores": [], "derivation_rules": {}}, None
    return json.load(open(path)), {"path": path, "sha256": sha256(path), "bytes": os.path.getsize(path)}


def apply_shear_rule(core, rules):
    """G_c used: the sourced value when one exists, else the named rule applied to the sourced E_c (DERIVED)."""
    if core.get("G_c_Pa"):
        core["G_c_used_Pa"], core["G_c_used_basis"] = core["G_c_Pa"], "sourced"
    elif core.get("E_c_Pa") and core.get("G_rule") in rules:
        rule = rules[core["G_rule"]]
        core["G_c_used_Pa"] = rule["G_over_E"] * core["E_c_Pa"]
        core["G_c_used_basis"] = f"DERIVED: G = {rule['G_over_E']} * E ({rule['name']})"
    else:
        core["G_c_used_Pa"], core["G_c_used_basis"] = None, "none: no sourced Gc and no rule"
    return core

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
