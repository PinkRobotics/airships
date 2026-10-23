#!/usr/bin/env python3
"""MAINLINE-021: the optimistic floating point, every mode at SF 1 or above on the fewest and smallest named optimisms.

Own arithmetic from pinned inputs (INPUTS.json lists them). The mode formulas are 009d's (both.py) and 014b's reading of
NASA CR-1457, re-implemented here and checked against their sealed numbers before anything new is computed. One change,
stated: intracell dimpling uses CR-1457's own biaxial rule (eq 2.1-6, straight line, so each direction carries half);
009d and 014b score the uniaxial eq 2.1-4. Both columns are reported.

THE OPTIMISMS, each moved from today's sourced value toward its named full value:
  O1 gamma: today the CR-1457 rule (0.20 below Vc 2, 1 at Vc >= 2); full the MAINLINE-018 optimistic curve
     gamma(Vc) = 0.20 + 0.40*min(Vc, 2), PROJECTION. It replaces kd on the stiff branch and is not stacked.
  O2 honeycomb wrinkling coefficient: today 0.33 (CR-1457 eq 2.2-14, design); full 0.82 (eq 2.2-12, K_delta 0).
     Foam cores carry 014's foam pair, 0.50 and 0.82.
  O3 beryllium face strength: today S-200F 283 MPa (MAINLINE-008 row); full the strongest sourced grade
     (sources/beryllium.json, chosen in BE_GRADE below with its basis).
USAGE of optimism i at a geometry: u_i = ln(needed/today)/ln(full/today), where needed brings its mode to SF 1;
0 means not needed, 1 means the whole named stretch. For every subset S of {O1, O2, O3} the search minimises
max_{i in S} u_i over core choice and core-mass fraction on the 5 percent mass line, with every mode outside S at SF >= 1
on today's value and crimp, crush and dimpling at SF >= 1 (no optimism touches them). The fewest-member S that reaches
max u <= 1 is the least set; its argmin is the floating point.

Run: python3 -I float021.py   (writes RESULTS.json and INPUTS.json beside this file)
"""
import datetime
import hashlib
import itertools
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STARTED = datetime.datetime.now().astimezone().isoformat()
JOB_STARTED = "2026-10-20T00:15:12-07:00"   # order read; a measurement, never a limit
WS = "unpublished-local-ref:7a5bf1cec24b249e"
OWN = f"{WS}/ref-4189c1615990eb515921/.ship/work"

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_pins():
    out = {}
    for key, (path, want) in PINS.items():
        got = sha256(path)
        if want and got != want:
            sys.exit(f"PIN MISMATCH {key} {got}")
        if key in REPORT_PINS and not got.startswith(REPORT_PINS[key]):
            sys.exit(f"REPORT PIN MISMATCH {key} {got}")
        out[key] = {"path": path, "sha256": got, "bytes": os.path.getsize(path)}
    return out


PIN_RECORDS = verify_pins()
P009D = json.load(open(PINS["p009d_point"][0]))
P009C5 = json.load(open(PINS["p009c5_point"][0]))
I014B = json.load(open(PINS["p014b_inputs"][0]))

# ---------------------------------------------------------------- the case (COMMON.md; 009d's constants)
R, NU, SYSTEMS, JOINT = 10.0, 0.33, 100.0, 0.05
P_EXT = 95460.83791390515
LIFT = 4889.442150186961
MARGIN = 0.05                                         # stands until MAINLINE-019 files
AREA = 4.0 * math.pi * R * R
M_FIVE = ((1.0 - MARGIN) * LIFT - SYSTEMS) / (1.0 + JOINT)
ROOT = math.sqrt(1.0 - NU * NU)


def biaxial_factor():
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid ** 3 + mid > 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


BIAX = biaxial_factor()                               # R^3 + R = 1 at Rx = Ry (CR-1457 eqs 2.2-6, 2.2-15)
K_HONEY_TODAY, K_HONEY_FULL = 0.33, 0.82              # CR-1457 eq 2.2-14 and eq 2.2-12 (K_delta = 0)
K_FOAM_TODAY, K_FOAM_FULL = 0.50, 0.82                # 014's foam pair
S200F = next(f for f in I014B["faces"] if f["name"] == "Beryllium S-200F")
SIGMA_TODAY_INHERITED = S200F["sigma_Pa"]              # 283 MPa, MAINLINE-008's S-200F row
SIGMA_TODAY = SIGMA_TODAY_INHERITED                   # a scenario may change it (run_scenario)

# O3's full value comes from this seat's own sourcing (sources/beryllium.json), chosen below with its basis
BE_SOURCES = os.path.join(OWN, "sources", "beryllium.json")
_BE = json.load(open(BE_SOURCES))
E_CHAIN = S200F["E_Pa"]          # 303 GPa as 008/014b/009d/009e carried it (S-200FH's value per the 021 checker); reproduction only
# ord-admiral-rr2-mainline021-be-modulus-290-1020: each grade's own E. S-200-F typical E, Materion DS-HPP-610 (sources file)
E_TODAY = next(g["E_Pa"] for g in _BE["grades"] if g.get("grade") == "S-200-F" and g.get("E_Pa"))
_LOT = [g for g in _BE["grades"] if (g.get("grade") or "").startswith("SR-200 (cross-rolled sheet, 1.96 mm") and g.get("E_Pa")]
E_O3 = min(g["E_Pa"] for g in _LOT)   # the lot's own in-plane moduli (298.7 L, 293.6 LT GPa): the lower, with the lower strength
FACE = dict(S200F, E_Pa=E_TODAY)                       # the face as scored; a scenario may change E
BE_GRADE = None                                        # set by choose_be_grade()


def choose_be_grade():
    """O3's full value: the strongest sourced compressive yield for the product a sub-millimetre face would be. Materion's
    S-200-F datasheet says S-200-F under 6.3 mm thick is supplied as SR-200 sheet; the strongest compressive yield found
    is the SR-200 cross-rolled 1.96 mm sheet lot of NASA CR-194164 Table 3 (after Fenn 1967): 379.2 MPa longitudinal and
    382.7 MPa long-transverse. An equibiaxial face is held to the LOWER direction, 379.2 MPa. Read from the sources file."""
    if not os.path.exists(BE_SOURCES):
        return None, None
    d = json.load(open(BE_SOURCES))
    lots = [g for g in d.get("grades", []) if (g.get("grade") or "").startswith("SR-200 (cross-rolled sheet, 1.96 mm")
            and g.get("compressive_yield_Pa")]
    if not lots:
        return None, None
    v = min(g["compressive_yield_Pa"] for g in lots)
    gr = next(g for g in lots if g["compressive_yield_Pa"] == v)
    return v, {"grade": gr.get("grade"), "product_form": gr.get("product_form"), "property": "compressive yield",
               "basis": gr.get("compressive_yield_basis"), "value_Pa": v, "directions_Pa": sorted(g["compressive_yield_Pa"] for g in lots),
               "source": gr.get("source"), "E_Pa": gr.get("E_Pa")}


def be_alternatives():
    """Other sourced face strengths, carried as scenarios for 'today' (each from the sources file, none retyped)."""
    d = json.load(open(BE_SOURCES))
    def find(prefix, key):
        g = next(g for g in d["grades"] if (g.get("grade") or "") == prefix and g.get(key))
        return g[key], g
    sr_min, sr = find("SR-200", "tensile_yield_Pa")
    s200f_guide, guide = find("S-200-F", "compressive_yield_Pa")
    return {
        "S-200-F inherited (MAINLINE-008, compressive yield 41 ksi)": (SIGMA_TODAY_INHERITED, "008 row; MB-001 note as 008 recorded it"),
        "S-200-F, Materion design guide compressive yield 'about 37 ksi'": (s200f_guide, guide["source"]["url"]),
        "SR-200 sheet, Materion datasheet minimum tensile yield (compressive about equal per the 1967 lot)": (sr_min, sr["source"]["url"]),
    }


def gamma_handbook(vc):
    return 0.20 if vc < 2.0 else 1.0                   # CR-1457 p. 6-12: Yd 0.20 below Vc 2, 1 at Vc >= 2


def gamma_optimistic(vc):
    return 0.20 + 0.40 * min(vc, 2.0)                  # MAINLINE-018 optimistic curve, PROJECTION


def gamma_conservative(vc):
    return 0.20                                        # MAINLINE-018 conservative curve (the downside column)


def geometry(core, fraction):
    tc = fraction * M_FIVE / (AREA * core["rho"])
    tf = (1.0 - fraction) * M_FIVE / (2.0 * AREA * S200F["rho"])
    return tf, tc


def modes(core, tf, tc, gamma_fn, k_wr, sigma_f):
    young = FACE["E_Pa"]
    h = tc + tf
    sigma_0 = young * h / (R * ROOT)                   # eq 6.2-26
    sigma_crimp = h * h * core["Gc_Pa"] / (2.0 * tf * tc)   # eq 6.2-27
    vc = sigma_0 / sigma_crimp
    if vc <= 2.0:
        kc, branch = 1.0 - vc / 4.0, "stiff_or_moderate_core"
    else:
        kc, branch = 1.0 / vc, "shear_crimping"
    gamma = gamma_fn(vc)
    membrane = P_EXT * R / (4.0 * tf)
    if core["form"] == "foam":
        uni = k_wr * (young * core["Ec_Pa"] * core["Gc_Pa"] / (1.0 - NU * NU)) ** (1.0 / 3.0)
    else:
        uni = k_wr * young * math.sqrt(core["Ec_Pa"] * tf / (young * tc))
    sfs = {
        "global_buckling": (4.0 * gamma * kc * sigma_0 * tf / R) / P_EXT,
        "face_compression": (4.0 * sigma_f * tf / R) / P_EXT,
        "core_shear_crimping": (4.0 * sigma_crimp * tf / R) / P_EXT,
        "core_crush": core["crush_Pa"] / (P_EXT / 2.0),
        "face_wrinkling": BIAX * uni / membrane,
    }
    extra = {}
    if core.get("s_cell_m"):
        sigma_d = 2.0 * young / (1.0 - NU * NU) * (tf / core["s_cell_m"]) ** 2     # eq 2.1-4
        sfs["intracell_dimpling"] = 0.5 * sigma_d / membrane                        # eq 2.1-6, equibiaxial
        extra["intracell_dimpling_uniaxial_009d_form"] = sigma_d / membrane
    least_mode = min(sfs, key=lambda k: sfs[k])
    return {"tf_m": tf, "core_m": tc, "h_m": h, "Vc": vc, "Kc": kc, "gamma": gamma, "branch": branch,
            "sfs": sfs, "least_SF": sfs[least_mode], "governing": least_mode, **extra}


# ---------------------------------------------------------------- reproduction checks (009d aluminium, 009c-5 aramid)
def optimize_fixed(core, gamma_fn, k_wr, sigma_f, dimpling_uniaxial=False, grid=8000):
    """Max of the least SF over the core-mass fraction: 009d's 8000-step grid, then golden refinement."""
    def least(f):
        ev = modes(core, *geometry(core, f), gamma_fn, k_wr, sigma_f)
        s = dict(ev["sfs"])
        if dimpling_uniaxial and "intracell_dimpling_uniaxial_009d_form" in ev:
            s["intracell_dimpling"] = ev["intracell_dimpling_uniaxial_009d_form"]
        return min(s.values())
    best_f = max((i / grid for i in range(1, grid)), key=least)
    lo, hi = max(best_f - 1.0 / grid, 1e-9), min(best_f + 1.0 / grid, 1 - 1e-9)
    gr = (math.sqrt(5) - 1) / 2
    for _ in range(200):
        a, b = hi - gr * (hi - lo), lo + gr * (hi - lo)
        if least(a) < least(b):
            lo = a
        else:
            hi = b
    f = 0.5 * (lo + hi)
    if least(best_f) > least(f):
        f = best_f
    return f, modes(core, *geometry(core, f), gamma_fn, k_wr, sigma_f)


def checks():
    out = {}
    FACE["E_Pa"] = E_CHAIN
    try:
        return _checks(out)
    finally:
        FACE["E_Pa"] = E_TODAY


def _checks(out):
    al = next(c for c in I014B["cores_eligible"] if c["name"] == "Hexcel CR-III 5056 1/4-1.6")
    sealed = P009D["aluminium_stiff_branch"]["cores"][0]
    # 009d's grid optimum, re-derived on its own 8000-step grid (no refinement), uniaxial dimpling as 009d scores it
    grid = 8000
    def least_grid(f):
        ev = modes(al, *geometry(al, f), lambda v: 0.20 if v <= 2.0 else 1.0, K_HONEY_TODAY, SIGMA_TODAY)
        s = dict(ev["sfs"]); s["intracell_dimpling"] = ev["intracell_dimpling_uniaxial_009d_form"]
        return (min(s.values()), sorted(s.values())[1])
    f = max((i / grid for i in range(1, grid)), key=least_grid)
    ev = modes(al, *geometry(al, f), lambda v: 0.20 if v <= 2.0 else 1.0, K_HONEY_TODAY, SIGMA_TODAY)
    same = (abs(f - sealed["core_mass_fraction"]) < 1e-12 and abs(ev["tf_m"] - sealed["tf_m"]) < 1e-15 and
            all(abs(ev["sfs"][k] - sealed["sfs"][{"face_compression": "face_yield"}.get(k, k)]) < 1e-12
                for k in ("global_buckling", "face_compression", "core_shear_crimping", "core_crush", "face_wrinkling")) and
            abs(ev["intracell_dimpling_uniaxial_009d_form"] - sealed["sfs"]["intracell_dimpling"]) < 1e-9 and
            abs(ev["Vc"] - sealed["Vc"]) < 1e-12)
    out["009d_aluminium_point"] = {"result": "PASS" if same else "FAIL", "least": ev["least_SF"], "sealed": sealed["least_SF"]}
    # 009c-5 aramid point, geometry held, every mode
    ar = next(c for c in I014B["cores_eligible"] if c["name"] == "Hexcel HRH-10-4.8-32")
    opt = P009C5["optimum"]
    ev = modes(ar, opt["tf_m"], opt["core_m"], gamma_handbook, K_HONEY_TODAY, SIGMA_TODAY)
    ref = opt["modes_at_0.20_design_wrinkle"]
    ok = all(abs(ev["sfs"][k] - ref[k]) < 1e-12 for k in ("global_buckling", "face_compression", "core_shear_crimping",
                                                           "core_crush", "face_wrinkling"))
    out["009c5_aramid_point_held"] = {"result": "PASS" if ok else "FAIL", "least": ev["least_SF"], "sealed": opt["least_SF"]}
    # the aramid optimum re-derived on today's values (handbook gamma) from scratch
    f, ev = optimize_fixed(ar, gamma_handbook, K_HONEY_TODAY, SIGMA_TODAY)
    # a finer optimiser may land a hair above a sealed optimum; it must never land below it
    out["009c5_aramid_reoptimised"] = {"least": ev["least_SF"], "sealed": opt["least_SF"],
                                       "result": "PASS" if -1e-9 <= ev["least_SF"] - opt["least_SF"] < 1e-5 else "FAIL",
                                       "rule": "reproduced or bettered by less than 1e-5 (golden refinement past the sealed grid)",
                                       "tf_m": ev["tf_m"], "sealed_tf_m": opt["tf_m"]}
    # 009d's statement: the kd that brings the aluminium global mode to 1
    out["009d_kd_global_1"] = {"mine": 0.20 / P009D["aluminium_stiff_branch"]["cores"][0]["sfs"]["global_buckling"],
                               "sealed": P009D["aluminium_stiff_branch"]["kd_statement"]["kd_that_brings_global_to_1"]}
    out["biaxial_factor"] = BIAX
    # 009e: the 1.6 pcf CR-III 5056 point at 5 percent under the 018 optimistic curve, k 0.33, 283 MPa, re-derived here
    # on 009e's own 8000-step grid, keyed on (least, second) as its optimise.py does
    def key009e(fr):
        e = modes(al, *geometry(al, fr), gamma_optimistic, K_HONEY_TODAY, SIGMA_TODAY_INHERITED)
        s_ = dict(e["sfs"]); s_["intracell_dimpling"] = e["intracell_dimpling_uniaxial_009d_form"]
        v = sorted(s_.values())
        return (v[0], v[1])
    fg = max((i / 8000 for i in range(1, 8000)), key=key009e)
    eg = modes(al, *geometry(al, fg), gamma_optimistic, K_HONEY_TODAY, SIGMA_TODAY_INHERITED)
    fr, er = optimize_fixed(al, gamma_optimistic, K_HONEY_TODAY, SIGMA_TODAY_INHERITED)
    out["009e_aluminium_optimistic"] = {"least_on_009e_grid": eg["least_SF"], "sealed": 0.92414822677, "tf_m": eg["tf_m"],
                                        "sealed_tf_m": 0.00077932830463, "Vc": eg["Vc"], "gamma": eg["gamma"],
                                        "refined_least": er["least_SF"], "refined_tf_m": er["tf_m"],
                                        "result": "PASS" if abs(eg["least_SF"] - 0.92414822677) < 5e-12
                                        and abs(eg["tf_m"] - 0.00077932830463) < 5e-15 else "FAIL",
                                        "rule": "009e's own grid reproduces its sealed least and face to the printed digits"}
    # 015's tolerance map: the 014b beryllium point (h 42.2429 mm) at kd 0.5 gives 43.79 mm and RMS 1.91 mm
    t = tolerance(0.04224293688916936, 0.5)
    out["015_tolerance_kd_0p5"] = {"amplitude_mm": t["amplitude_mm"], "sealed_mm": 43.79, "rms_worst_mm": t["rms_worst_mm"],
                                   "sealed_rms_mm": 1.91,
                                   "result": "PASS" if abs(t["amplitude_mm"] - 43.79) < 0.005 and abs(t["rms_worst_mm"] - 1.91) < 0.005 else "FAIL"}
    return out


# ---------------------------------------------------------------- MAINLINE-015's tolerance map, re-implemented
K0_EQ3, A_EQ3, B_EQ3, K_WORST = 0.45, 0.51, 3.88, 2.625


def tolerance(h, kd):
    """015: t_eq = sqrt(3)*h; kappa = 0.45 + 0.51*exp(-3.88*delta/t_eq) inverted at kappa = kd (fit R/t 100-1550, floor
    0.45); single Gaussian dimple RMS = delta*beta0/sqrt(8), beta0 from the Koga-Hoff width with nu 0.3 (015's choice)."""
    t_eq = math.sqrt(3.0) * h
    root = (12.0 * (1.0 - 0.3 ** 2)) ** 0.25 * math.sqrt(R / t_eq)
    beta_l1, beta_w = 1.0 / root, K_WORST / root
    out = {"kd": kd, "t_eq_mm": t_eq * 1000.0, "R_over_t_eq": R / t_eq, "in_fit_range": 100.0 <= R / t_eq <= 1550.0,
           "wavelength_m": math.sqrt(R * t_eq)}
    ratio = (kd - K0_EQ3) / A_EQ3
    if ratio <= 0.0 or ratio >= 1.0:
        out.update({"status": "outside the Eq 3 inversion (floor 0.45)", "amplitude_mm": None, "rms_worst_mm": None})
        return out
    dbar = -math.log(ratio) / B_EQ3
    delta = dbar * t_eq
    out.update({"status": "lambda_I_1 inversion", "delta_over_t_eq": dbar, "amplitude_mm": delta * 1000.0,
                "rms_worst_mm": delta * beta_w / math.sqrt(8.0) * 1000.0,
                "rms_narrow_mm": delta * beta_l1 / math.sqrt(8.0) * 1000.0})
    return out


# ---------------------------------------------------------------- the search
FAMILY = {"aluminium_honeycomb": "aluminium", "aramid_honeycomb": "aramid"}


def family_of(core):
    if core["family"] in FAMILY:
        return FAMILY[core["family"]]
    if "HRH-49" in core["name"]:
        return "aramid"
    return "other"


def usage(needed, today, full):
    """Share of the named stretch an optimism must use: 0 when today's value already suffices, 1 at the full value."""
    if needed <= today * (1 + 1e-12):
        return 0.0
    if full <= today * (1 + 1e-12):
        return math.inf
    return math.log(needed / today) / math.log(full / today)


def point_usage(core, f, sigma_full):
    tf, tc = geometry(core, f)
    k_today, k_full = (K_FOAM_TODAY, K_FOAM_FULL) if core["form"] == "foam" else (K_HONEY_TODAY, K_HONEY_FULL)
    ev = modes(core, tf, tc, gamma_handbook, k_today, SIGMA_TODAY)
    vc = ev["Vc"]
    g_today, g_full = gamma_handbook(vc), gamma_optimistic(vc)
    need = {
        "O1_gamma": g_today / ev["sfs"]["global_buckling"],
        "O2_wrinkle": k_today / ev["sfs"]["face_wrinkling"],
        "O3_be_strength": SIGMA_TODAY / ev["sfs"]["face_compression"],
    }
    u = {"O1_gamma": usage(need["O1_gamma"], g_today, g_full),
         "O2_wrinkle": usage(need["O2_wrinkle"], k_today, k_full),
         "O3_be_strength": usage(need["O3_be_strength"], SIGMA_TODAY, sigma_full) if sigma_full else
         (0.0 if need["O3_be_strength"] <= SIGMA_TODAY else math.inf)}
    hard = {k: ev["sfs"][k] for k in ("core_shear_crimping", "core_crush", "intracell_dimpling") if k in ev["sfs"]}
    return ev, need, u, hard, (g_today, g_full), (k_today, k_full)


def search(cores, sigma_full, grid=4000):
    """For every subset S: min over cores and fractions of max_{i in S} u_i, with u_j = 0 for j outside S and the
    untouched modes (crimp, crush, dimpling) at SF >= 1. Also the shortfall table when nothing is feasible."""
    names = ("O1_gamma", "O2_wrinkle", "O3_be_strength")
    subsets = [s for n in range(0, 4) for s in itertools.combinations(names, n)]
    best = {s: None for s in subsets}
    fam_best = {}
    for core in cores:
        fam = family_of(core)
        for i in range(1, grid):
            f = i / grid
            ev, need, u, hard, gpair, kpair = point_usage(core, f, sigma_full)
            hard_ok = all(v >= 1.0 for v in hard.values())
            for s in subsets:
                if not hard_ok or any(u[j] > 0.0 for j in names if j not in s):
                    continue
                score = max((u[j] for j in s), default=0.0)
                if best[s] is None or score < best[s][0]:
                    best[s] = (score, core["name"], f)
            # per family: the least set point AND the max-least point under the full named set
            full = modes(core, *geometry(core, f), gamma_optimistic,
                         K_FOAM_FULL if core["form"] == "foam" else K_HONEY_FULL, sigma_full or SIGMA_TODAY)
            key = (fam, "full_set_max_least")
            if key not in fam_best or full["least_SF"] > fam_best[key][0]:
                fam_best[key] = (full["least_SF"], core["name"], f)
            score_all = max(u.values()) if hard_ok else math.inf
            key2 = (fam, "all_three_min_max_usage")
            if key2 not in fam_best or score_all < fam_best[key2][0]:
                fam_best[key2] = (score_all, core["name"], f)
    return subsets, best, fam_best


def family_max_least(cores, gamma_fn, k_honey, k_foam, sigma_f, scale=None, grid=4000):   # the search's own grid
    """Max over the family's cores and fractions of the least SF, with an optional multiplier on one property."""
    best = (-1.0, None, None, None)
    for core in cores:
        c = dict(core)
        g_fn, kh, kf, sf = gamma_fn, k_honey, k_foam, sigma_f
        if scale:
            prop, m = scale
            if prop in ("Gc_Pa", "crush_Pa", "Ec_Pa"):
                c[prop] = c[prop] * m
            elif prop == "gamma":
                g_fn = (lambda base, mm: (lambda v: min(1.0, base(v) * mm)))(gamma_fn, m)
            elif prop == "wrinkle":
                kh, kf = kh * m, kf * m
            elif prop == "be_strength":
                sf = sf * m
        for i in range(1, grid):
            f = i / grid
            ev = modes(c, *geometry(c, f), g_fn, kf if c["form"] == "foam" else kh, sf)
            if ev["least_SF"] > best[0]:
                best = (ev["least_SF"], core["name"], f, ev)
    return best


def added_optimism(cores, sigma_full):
    """When a family stays below 1 on the full named set: for each single further property, the smallest multiplier
    that brings the family's best least SF to 1 (re-optimised), by bisection. gamma is capped at 1."""
    base = family_max_least(cores, gamma_optimistic, K_HONEY_FULL, K_FOAM_FULL, sigma_full or SIGMA_TODAY)
    out = {"full_set_least": base[0], "core": base[1], "fraction": base[2],
           "governing": base[3]["governing"] if base[3] else None, "single_property_multipliers": {}}
    if base[0] >= 1.0:
        return out
    for prop in ("Gc_Pa", "crush_Pa", "Ec_Pa", "gamma", "wrinkle", "be_strength"):
        lo, hi = 1.0, 64.0
        if family_max_least(cores, gamma_optimistic, K_HONEY_FULL, K_FOAM_FULL, sigma_full or SIGMA_TODAY, (prop, hi))[0] < 1.0:
            out["single_property_multipliers"][prop] = None      # not enough alone, even at 64x
            continue
        for _ in range(40):
            mid = math.sqrt(lo * hi)
            if family_max_least(cores, gamma_optimistic, K_HONEY_FULL, K_FOAM_FULL, sigma_full or SIGMA_TODAY, (prop, mid))[0] >= 1.0:
                hi = mid
            else:
                lo = mid
        b = family_max_least(cores, gamma_optimistic, K_HONEY_FULL, K_FOAM_FULL, sigma_full or SIGMA_TODAY, (prop, hi))
        out["single_property_multipliers"][prop] = {"multiplier": hi, "core": b[1], "fraction": b[2]}
    return out


def describe(core, f, sigma_full):
    """The point at today's values, at the needed values, and at the full named set, with the masses."""
    ev_today, need, u, hard, (g_today, g_full), (k_today, k_full) = point_usage(core, f, sigma_full)
    tf, tc = ev_today["tf_m"], ev_today["core_m"]
    faces = 2.0 * AREA * tf * S200F["rho"]
    core_mass = AREA * tc * core["rho"]
    joints = JOINT * (faces + core_mass)
    gamma_needed = max(need["O1_gamma"], g_today)
    k_needed = max(need["O2_wrinkle"], k_today)
    sig_needed = max(need["O3_be_strength"], SIGMA_TODAY)
    ev_needed = modes(core, tf, tc, lambda v: gamma_needed, k_needed, sig_needed)
    e_was = FACE["E_Pa"]
    FACE["E_Pa"] = E_O3                                  # all three optimisms at full: the face IS the SR-200 lot
    try:
        ev_full = modes(core, tf, tc, gamma_optimistic, k_full, sigma_full or SIGMA_TODAY)
        ev_cons = modes(core, tf, tc, gamma_conservative, k_full, sigma_full or SIGMA_TODAY)
    finally:
        FACE["E_Pa"] = e_was
    return {
        "core": core["name"], "core_tag": core["tag"], "family": family_of(core), "core_rho_kg_m3": core["rho"],
        "core_Ec_Pa": core["Ec_Pa"], "core_Gc_Pa": core["Gc_Pa"], "core_crush_Pa": core["crush_Pa"],
        "core_cell_m": core.get("s_cell_m"), "core_mass_fraction": f,
        "R_m": R, "tf_m": tf, "core_m": tc, "h_m": tf + tc, "d_m_face_separation": tf + tc,
        "masses_kg": {"faces": faces, "core": core_mass, "joints": joints, "systems": SYSTEMS,
                      "margin": MARGIN * LIFT, "total": faces + core_mass + joints + SYSTEMS + MARGIN * LIFT,
                      "lift": LIFT},
        "Vc": ev_today["Vc"], "Kc": ev_today["Kc"], "branch": ev_today["branch"],
        "today": ev_today,
        "needed_values": {"gamma": gamma_needed, "gamma_today": g_today, "gamma_full_018": g_full,
                          "wrinkle_coefficient": k_needed, "wrinkle_today": k_today, "wrinkle_full": k_full,
                          "be_strength_Pa": sig_needed, "be_today_Pa": SIGMA_TODAY, "be_full_Pa": sigma_full},
        "improvement_factors_over_today": {"gamma": gamma_needed / g_today, "wrinkle_coefficient": k_needed / k_today,
                                           "be_strength": sig_needed / SIGMA_TODAY},
        "usage": u,
        "at_needed_values": ev_needed,
        "at_full_named_set": ev_full,
        "face_E_Pa_scored": FACE["E_Pa"], "face_E_Pa_at_full_set": E_O3,
        "tolerance_015_at_needed_gamma": tolerance(ev_today["h_m"], gamma_needed) if ev_today["branch"] != "shear_crimping" else
        {"status": "crimp branch: kd does not enter (015)"},
        "tolerance_015_at_018_curve": tolerance(ev_today["h_m"], g_full) if ev_today["branch"] != "shear_crimping" else
        {"status": "crimp branch: kd does not enter (015)"},
        "at_full_set_but_conservative_gamma": ev_cons,
    }


def run_scenario(label, sigma_today, sigma_full, young, cores, full_detail):
    """One reading of 'today': the least set, its floating point, and (in full detail) both families' results."""
    global SIGMA_TODAY
    SIGMA_TODAY = sigma_today
    FACE["E_Pa"] = young
    try:
        subsets, best, fam_best = search(cores, sigma_full)
        rows = []
        for sub in subsets:
            b = best[sub]
            rows.append({"subset": list(sub), "min_max_usage": None if b is None else (None if math.isinf(b[0]) else b[0]),
                         "feasible_within_named": b is not None and b[0] <= 1.0,
                         "core": None if b is None else b[1], "fraction": None if b is None else b[2]})
        out = {"label": label, "sigma_today_Pa": sigma_today, "sigma_full_Pa": sigma_full, "E_Pa": young, "subsets": rows}
        feasible = [r for r in rows if r["feasible_within_named"]]
        out["least_set"] = None
        if feasible:
            n = min(len(r["subset"]) for r in feasible)
            out["least_set"] = min((r for r in feasible if len(r["subset"]) == n), key=lambda r: r["min_max_usage"])
            core = next(c for c in cores if c["name"] == out["least_set"]["core"])
            out["floating_point"] = describe(core, out["least_set"]["fraction"], sigma_full)
        if full_detail:
            out["families"] = {}
            for (fam, kind), (score, name, f) in sorted(fam_best.items()):
                core = next(c for c in cores if c["name"] == name)
                out["families"].setdefault(fam, {})[kind] = {"score": None if math.isinf(score) else score,
                                                             "point": describe(core, f, sigma_full)}
            for fam in ("aluminium", "aramid", "other"):
                fam_cores = [c for c in cores if family_of(c) == fam]
                today = family_max_least(fam_cores, gamma_handbook, K_HONEY_TODAY, K_FOAM_TODAY, SIGMA_TODAY)
                out["families"].setdefault(fam, {})["today_max_least"] = {
                    "least": today[0], "core": today[1], "fraction": today[2], "governing": today[3]["governing"]}
                cons = family_max_least(fam_cores, gamma_conservative, K_HONEY_FULL, K_FOAM_FULL, sigma_full)
                out["families"][fam]["full_set_conservative_gamma_max_least"] = {
                    "least": cons[0], "core": cons[1], "governing": cons[3]["governing"]}
                out["families"][fam]["added_optimism"] = added_optimism(fam_cores, sigma_full)
        return out
    finally:
        SIGMA_TODAY = SIGMA_TODAY_INHERITED
        FACE["E_Pa"] = E_TODAY

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
