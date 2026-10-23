#!/usr/bin/env python3
"""MAINLINE-022: P3 SiC frame-and-film at 5 percent margin.

Own arithmetic. 011b is not rewritten. RESULTS.json is the measured run.
"""
import datetime
import hashlib
import json
import math
import os
import time
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(ROOT, "RESULTS.json")
ORIGIN_PATH = os.path.join(ROOT, "ORIGIN.json")
ZONE = ZoneInfo("America/Los_Angeles")

R = 10.0
P_EXT = 95460.8379139
L_MASS = 4889.44215019
RHO = 3100.0
E_MOD = 410e9
SIG_CRUSH = 3900e6
SIG_FLEX = 380e6
M_WEIBULL = 10.0
# Same-volume two-parameter Weibull stress at P_f=1e-3, sigma_0 = 380 MPa typical.
SIG_WEIBULL = SIG_FLEX * (0.001 ** (1.0 / M_WEIBULL))
C_LOCAL = 0.6
C_TWO = 4.0
C_TRI = 4.0 * math.sqrt(1.5)
M_NODE = 0.02
JOINT_FRAC = 0.05
N_RO = 700
S_BAND = [round(0.40 + 0.02 * i, 3) for i in range(131)]

PINS = (
    (
        "unpublished-local-ref:bd9fce59fab05f7f",
        "0cc874af6424e3db79a364b2fb9b444a22e9a2f365d897d44680b685c6f48306",
        2897,
    ),
    (
        "withheld-source:b528d6a62c81ce0b",
        "8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5",
        5874,
    ),
    (
        "unpublished-local-ref:b40693bc2fdb6bdf",
        "14983c85c3495169b1bd4ab340f776ad6d4e93737b19623a7b483f440c5ff6ed",
        2021,
    ),
    (
        "unpublished-local-ref:2bf170d37c993460",
        "98c8d5b2988600fcaed430704fba2d16a25e165e5aad1998ef07550437165a3f",
        2063,
    ),
)

# 011b equilateral SiC, k=0.2, joints on, margin 0. Regression target.
PUB = {
    "s": 2.04,
    "r_o": 0.123688362374,
    "t_w": 0.000880299093685,
    "SF": 1.22552794688,
    "governing": "global",
    "m_tube": 4509.44160085,
    "m_joint": 225.472080043,
    "m_nodes": 7.01346929732,
}

FILMS = (
    {
        "name": "Mylar-850H",
        "rho": 1400.0,
        "sigma": 22.0 * 6894757.293178,
        "tag": "QUESTIONABLE",
        "state": "exists today",
        "t_catalog_m": 48.0 * 2.54e-7,  # 48 gauge = 0.48 mil
        "o2_cc_per_100in2_day": 6.0,
    },
    {
        "name": "011-film",
        "rho": 970.0,
        "sigma": 1.5e9,
        "tag": "PROJECTION",
        "state": "PROJECTION",
        "t_catalog_m": 8.0e-5,
        "o2_cc_per_100in2_day": None,
    },
)

SIGMAS = (
    ("flexural_380", SIG_FLEX, "exists today"),
    ("weibull_Pf1e-3_m10", SIG_WEIBULL, "calculated"),
    ("crush_3900", SIG_CRUSH, "exists as crush"),
)


def g(x):
    return format(x, ".12g")


def atomic_write(path, text):
    tmp = path + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    try:
        os.write(fd, text.encode())
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, path)
    dirfd = os.open(os.path.dirname(path), os.O_RDONLY)
    try:
        os.fsync(dirfd)
    finally:
        os.close(dirfd)


def pin_check():
    rows = []
    ok = True
    for path, sha, nbytes in PINS:
        data = open(path, "rb").read()
        got = hashlib.sha256(data).hexdigest()
        match = got == sha and len(data) == nbytes
        ok = ok and match
        rows.append({"path": path, "sha256": got, "bytes": len(data), "match": match})
        if not match:
            print("PIN DRIFT", path, got, len(data))
    return ok, rows


def node_count(s):
    return 8.0 * math.pi * R * R / (math.sqrt(3.0) * s * s) + 2.0


def sagitta(s):
    return R - math.sqrt(R * R - (s * 0.5) ** 2)


def arc_geom(s, h):
    # Circular arc through the chord s with midspan rise h.
    rad = ((s * 0.5) ** 2 + h * h) / (2.0 * h)
    theta = 2.0 * math.asin(min(1.0, (s * 0.5) / rad))
    return rad, rad * theta


def masses(s, t_f, rho_f, mode):
    V = node_count(s)
    members = 3.0 * V - 6.0
    m_nodes = M_NODE * V
    m_film = 4.0 * math.pi * R * R * t_f * rho_f
    if mode == "011b":
        m_sys = 50.0
        vehicle = L_MASS
        remain = vehicle - m_sys - m_nodes - m_film
        m_tube = remain / (1.0 + JOINT_FRAC)
        m_joint = remain - m_tube
    else:
        m_sys = 100.0
        vehicle = 0.95 * L_MASS
        assembly = (vehicle - m_sys) / (1.0 + JOINT_FRAC)
        m_joint = (vehicle - m_sys) - assembly
        m_tube = assembly - m_film - m_nodes
    payload = L_MASS - vehicle
    return {
        "V": V,
        "members": members,
        "m_nodes": m_nodes,
        "m_film": m_film,
        "m_tube": m_tube,
        "m_joint": m_joint,
        "m_sys": m_sys,
        "vehicle": vehicle,
        "payload": payload,
        "total_accounted": m_film + m_nodes + m_tube + m_joint + m_sys + payload,
    }


def perry(sig, E, s_len, r_o, I, A, n_force):
    rg2 = I / A
    eta = (s_len / 1000.0) * r_o / rg2
    sig_E = math.pi ** 2 * E * rg2 / (s_len * s_len)
    phi = (sig + (eta + 1.0) * sig_E) * 0.5
    disc = phi * phi - sig * sig_E
    if disc < 0.0:
        return None
    sig_cr = phi - math.sqrt(disc)
    sig_app = n_force / A
    return sig_cr / sig_app, eta, sig_app, sig_E


def legacy_point():
    """011b mass rules, chord length, N = p*R*s/2, at the published SiC point."""
    s = PUB["s"]
    r_o = PUB["r_o"]
    pack = masses(s, 8.0e-5, 970.0, "011b")
    A = pack["m_tube"] / (pack["members"] * s * RHO)
    disc = r_o * r_o - A / math.pi
    r_i = math.sqrt(disc)
    t_w = r_o - r_i
    I = math.pi / 4.0 * (r_o ** 4 - r_i ** 4)
    g_unit = E_MOD * math.sqrt(I * A) / (s * R * R)
    p_g = 0.2 * C_TRI * g_unit
    n_force = P_EXT * R * s / 2.0
    sig_ax = n_force / A
    return {
        "pack": pack,
        "A": A,
        "t_w": t_w,
        "I": I,
        "SF_global": p_g / P_EXT,
        "p_global": p_g,
        "N": n_force,
        "sigma_axial": sig_ax,
        "rt": r_o / t_w,
    }


def scan(mode, film, t_values, h_mults, n_ro, s_values):
    """Best least-SF row for each (grid, k, sigma) over s, t, h, r_o.

    least is the minimum of yield, Euler, local, film, Perry and global.
    """
    rho_f = film["rho"]
    sig_f = film["sigma"]
    best = {}
    for s in s_values:
        h_sph = sagitta(s)
        for t_f in t_values:
            pack0 = masses(s, t_f, rho_f, mode)
            if pack0["m_tube"] <= 0.0 or pack0["m_film"] < 0.0:
                continue
            for mult in h_mults:
                h = min(h_sph * mult, s / 5.0)
                if h <= 1e-6:
                    continue
                if mode == "011b":
                    length = s
                    n_coef = R * s / 2.0  # N = p * n_coef
                else:
                    _rad, length = arc_geom(s, h)
                    n_coef = (s ** 3) / (16.0 * h)  # N = p * n_coef
                A = pack0["m_tube"] / (pack0["members"] * length * RHO)
                if A <= 0.0:
                    continue
                r_min = math.sqrt(A / math.pi) * 1.0001
                r_max = min(0.25, s / 3.0)
                if r_max <= r_min:
                    continue
                span = r_max - r_min
                p_film = 2.0 * sig_f * t_f / s
                sf_film = p_film / P_EXT
                for i in range(n_ro):
                    r_o = r_min + span * i / (n_ro - 1)
                    disc = r_o * r_o - A / math.pi
                    if disc <= 0.0:
                        continue
                    r_i = math.sqrt(disc)
                    t_w = r_o - r_i
                    I = math.pi * 0.25 * (r_o ** 4 - r_i ** 4)
                    n_at_ext = P_EXT * n_coef
                    p_euler = (math.pi ** 2 * E_MOD * I / (length ** 2)) / n_coef
                    sig_loc = C_LOCAL * E_MOD * t_w / r_o
                    p_local = (sig_loc * A) / n_coef
                    sf_e = p_euler / P_EXT
                    sf_l = p_local / P_EXT
                    g_unit = E_MOD * math.sqrt(I * A) / (s * R * R)
                    base_name = "euler"
                    base_sf = sf_e
                    if sf_l < base_sf:
                        base_name, base_sf = "local", sf_l
                    if sf_film < base_sf:
                        base_name, base_sf = "film", sf_film
                    for sig_name, sig, _state in SIGMAS:
                        p_yield = (sig * A) / n_coef
                        sf_y = p_yield / P_EXT
                        got = perry(sig, E_MOD, length, r_o, I, A, n_at_ext)
                        if got is None:
                            continue
                        sf_p, eta, sig_app, sig_E = got
                        yname, ysf = base_name, base_sf
                        if sf_y < ysf:
                            yname, ysf = "yield", sf_y
                        if sf_p < ysf:
                            yname, ysf = "perry", sf_p
                        for grid, coeff in (("equilateral_triangular", C_TRI), ("two_way", C_TWO)):
                            for k in (0.2, 0.4):
                                sf_g = k * coeff * g_unit / P_EXT
                                if sf_g < ysf:
                                    gov, least = "global", sf_g
                                else:
                                    gov, least = yname, ysf
                                key = (grid, k, sig_name)
                                prev = best.get(key)
                                if prev is not None and least <= prev["SF_least"]:
                                    continue
                                best[key] = {
                                    "grid": grid,
                                    "k": k,
                                    "sigma_name": sig_name,
                                    "sigma_Pa": sig,
                                    "film": film["name"],
                                    "film_tag": film["tag"],
                                    "s_m": s,
                                    "h_m": h,
                                    "h_over_sagitta": h / h_sph,
                                    "arc_length_m": length,
                                    "t_film_m": t_f,
                                    "r_o_m": r_o,
                                    "t_w_m": t_w,
                                    "rt": r_o / t_w,
                                    "A_m2": A,
                                    "I_m4": I,
                                    "nodes": pack0["V"],
                                    "members": pack0["members"],
                                    "m_film_kg": pack0["m_film"],
                                    "m_nodes_kg": pack0["m_nodes"],
                                    "m_joint_kg": pack0["m_joint"],
                                    "m_tube_kg": pack0["m_tube"],
                                    "m_systems_kg": pack0["m_sys"],
                                    "m_payload_kg": pack0["payload"],
                                    "m_vehicle_kg": pack0["vehicle"],
                                    "SF_yield": sf_y,
                                    "SF_euler": sf_e,
                                    "SF_local": sf_l,
                                    "SF_film": sf_film,
                                    "SF_perry": sf_p,
                                    "SF_global": sf_g,
                                    "SF_least": least,
                                    "governing": gov,
                                    "N_N": n_at_ext,
                                    "sigma_axial_Pa": sig_app,
                                    "eta": eta,
                                    "N_over_Ne": sig_app / sig_E,
                                    "questionable": True,
                                }
    return best


def t_grid(film, mode):
    # Log grid from the catalog gauge up to the thickness that spends 75% of assembly on film.
    if mode == "011b":
        return [8.0e-5]
    assembly = (0.95 * L_MASS - 100.0) / 1.05
    t_hi = 0.75 * assembly / (4.0 * math.pi * R * R * film["rho"])
    t_lo = film["t_catalog_m"]
    if t_hi <= t_lo:
        return [t_lo]
    return [t_lo * (t_hi / t_lo) ** (i / 11.0) for i in range(12)]


def fitting_mass(row):
    """Lower and upper bounds on SiC bearing fittings at 380 MPa."""
    a_req = row["N_N"] / SIG_FLEX
    extra = max(0.0, a_req - row["A_m2"])
    sleeve = 2.0 * row["r_o_m"]
    per_end = RHO * extra * sleeve
    return {
        "A_bearing_for_380_m2": a_req,
        "tube_area_m2": row["A_m2"],
        "area_ratio_tube_over_need": row["A_m2"] / a_req if a_req else None,
        "lower_bound_one_per_node_kg": row["nodes"] * per_end,
        "upper_bound_per_member_end_kg": 2.0 * row["members"] * per_end,
        "allowance_kg": row["m_joint_kg"],
    }


def permeance_mylar(t_f):
    """016 method. Mylar 850H O2 transmission at 48 gauge, scaled as 1/t."""
    t48 = 48.0 * 2.54e-7
    # 6.0 cc / 100 in^2 / day at 1 atm.
    area_100 = 100.0 * 0.0254 ** 2
    scc_per_m2_s = 6.0 / area_100 / 86400.0
    scc_per_m2_s *= t48 / t_f
    mol = scc_per_m2_s * (1.0 / 22414.0) / 101325.0
    A = 4.0 * math.pi * R * R
    kg_day = mol * A * P_EXT * 0.02897 * 86400.0
    budget = 0.01 * L_MASS
    return {"kg_per_day": kg_day, "pct_of_1pct_budget": 100.0 * kg_day / budget}


def second_mode(row):
    pairs = [
        ("yield", row["SF_yield"]),
        ("euler", row["SF_euler"]),
        ("local", row["SF_local"]),
        ("film", row["SF_film"]),
        ("perry", row["SF_perry"]),
        ("global", row["SF_global"]),
    ]
    rest = sorted((p for p in pairs if p[0] != row["governing"]), key=lambda t: (t[1], t[0]))
    return rest[0]


def run_checks():
    bucket = []

    def check(name, computed, expected, tol):
        ok = abs(computed - expected) <= tol
        bucket.append({"name": name, "computed": computed, "expected": expected, "tol": tol, "pass": ok})
        if not ok:
            print("FAIL", name, computed, expected)
        return ok

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def build(origin, elapsed, bucket):
    cases = {}
    # Common-rules spherical arcs, both films. h multiplier 1 only.
    for film in FILMS:
        ts = t_grid(film, "common")
        cases[film["name"] + "|spherical"] = scan("common", film, ts, [1.0], N_RO, S_BAND)
    # Free rise on both films. Four rise multiples.
    for film in FILMS:
        ts = t_grid(film, "common")
        cases[film["name"] + "|rise"] = scan("common", film, ts, [1.0, 2.0, 4.0, 8.0], N_RO, S_BAND)

    def pick(case, grid, k, sigma):
        return cases[case][(grid, k, sigma)]

    # Least optimism set on the equilateral grid.
    # Baseline: flexural 380, k 0.2, Mylar, spherical rise.
    # Flags: crush, k 0.4, projection film, free rise.
    catalog = []
    flag_sets = []
    for crush in (0, 1):
        for k04 in (0, 1):
            for proj in (0, 1):
                for rise in (0, 1):
                    flag_sets.append((crush, k04, proj, rise))
    for flags in flag_sets:
        crush, k04, proj, rise = flags
        film_name = "011-film" if proj else "Mylar-850H"
        case = film_name + ("|rise" if rise else "|spherical")
        sigma = "crush_3900" if crush else "flexural_380"
        k = 0.4 if k04 else 0.2
        row = pick(case, "equilateral_triangular", k, sigma)
        two = pick(case, "two_way", k, sigma)
        names = []
        if crush:
            names.append("crush_3900_MPa")
        if k04:
            names.append("k_0.4")
        if proj:
            names.append("film_1.5_GPa")
        if rise:
            names.append("arc_rise_above_sphere")
        # The free-rise scan includes the sphere. A row that stays there is not an optimism.
        if row["h_over_sagitta"] <= 1.0 + 1e-9:
            names = [n for n in names if n != "arc_rise_above_sphere"]
        catalog.append({
            "flags": names,
            "n_flags": len(names),
            "equilateral": row,
            "two_way": two,
            "reaches": row["SF_least"] >= 1.0,
        })
    reaching = [c for c in catalog if c["reaches"]]
    reaching.sort(key=lambda c: (c["n_flags"], -c["equilateral"]["SF_least"]))
    least = reaching[0] if reaching else None
    baseline = next(c for c in catalog if c["n_flags"] == 0)

    def flagged(names):
        want = tuple(names)
        for c in catalog:
            if tuple(c["flags"]) == want:
                return c
        raise KeyError(names)

    # Integrator point: 011b film and 011b crush, spherical arcs, 5 percent joints.
    # 023, 024 and 025 had not filed. Those three values stay PENDING.
    carried_k02 = flagged(("crush_3900_MPa", "film_1.5_GPa"))
    carried_k04 = flagged(("crush_3900_MPa", "k_0.4", "film_1.5_GPa"))

    def decorate(row):
        sec_name, sec_sf = second_mode(row)
        out = dict(row)
        out["second"] = sec_name
        out["SF_second"] = sec_sf
        out["fittings"] = fitting_mass(row)
        if row["film"] == "Mylar-850H":
            out["permeation"] = permeance_mylar(row["t_film_m"])
        else:
            out["permeation"] = {"note": "011 film has no measured permeance. Monolithic SiC on the 016 method is a barrier. This polymer allowable is a PROJECTION."}
        out["manufacture"] = {
            "hexoloy_process_OD_max_mm": 381.0,
            "hexoloy_single_length_m": 1.4,
            "hexoloy_bonded_length_m": 4.9,
            "seal_tube_length_m": 0.3048,
            "silit_OD_max_mm": 300.0,
            "silit_length_m": 3.5,
            "silit_wall_min_mm": 4.0,
            "amasic_wall_min_mm": 2.0,
            "this_OD_mm": 2.0 * row["r_o_m"] * 1e3,
            "this_length_m": row["s_m"],
            "this_wall_mm": row["t_w_m"] * 1e3,
            "length_over_hexoloy_single": row["s_m"] / 1.4,
            "wall_over_amasic_min": (row["t_w_m"] * 1e3) / 2.0,
        }
        return out

    # Compact catalog for the file: drop full duplicates, keep SF and flags.
    catalog_out = []
    for c in catalog:
        catalog_out.append({
            "flags": c["flags"],
            "n_flags": c["n_flags"],
            "reaches_SF_1": c["reaches"],
            "equilateral_SF": c["equilateral"]["SF_least"],
            "equilateral_governing": c["equilateral"]["governing"],
            "equilateral_s_m": c["equilateral"]["s_m"],
            "two_way_SF": c["two_way"]["SF_least"],
            "two_way_governing": c["two_way"]["governing"],
        })

    # Weibull row on the baseline geometry's film and rise, for the named allowable.
    weibull_row = pick("Mylar-850H|spherical", "equilateral_triangular", 0.2, "weibull_Pf1e-3_m10")

    results = {
        "schema": 1,
        "card": "MAINLINE-022",
        "unit": "vacuum-mainline022-p3-optimistic-floating-point-1020",
        "seat": "ref-2543c559b19ffce7dfdd",
        "questionable": True,
        "certification": False,
        "origin": origin,
        "elapsed_s": elapsed,
        "mass_rules": {
            "payload_margin": 0.05,
            "vehicle_kg": 0.95 * L_MASS,
            "payload_kg": 0.05 * L_MASS,
            "systems_kg": 100.0,
            "joints": "5 percent of film+nodes+tubes, PENDING-023",
            "joint_allowance_kg": (0.95 * L_MASS - 100.0) * JOINT_FRAC / (1.0 + JOINT_FRAC),
        },
        "cross_checks": bucket,
        "parallel": {
            "023": "PENDING-023",
            "024": "PENDING-024",
            "025": "PENDING-025",
            "note": "No report for MAINLINE-023, 024 or 025 was in queue/submissions when this run started. Joints stay at 5 percent. The film stays the 011b film. The allowable stays the 011b crush.",
        },
        "baseline_today": decorate(baseline["equilateral"]),
        "baseline_two_way": decorate(baseline["two_way"]),
        "carried_011b_k02": {
            "flags": carried_k02["flags"],
            "equilateral": decorate(carried_k02["equilateral"]),
            "two_way": decorate(carried_k02["two_way"]),
            "pending": ["PENDING-023", "PENDING-024", "PENDING-025"],
        },
        "carried_011b_k04": {
            "flags": carried_k04["flags"],
            "equilateral": decorate(carried_k04["equilateral"]),
            "two_way": decorate(carried_k04["two_way"]),
        },
        "weibull_equilateral_k02": decorate(weibull_row),
        "least_optimism_set": None if least is None else {
            "flags": least["flags"],
            "equilateral": decorate(least["equilateral"]),
            "two_way": decorate(least["two_way"]),
        },
        "catalog": catalog_out,
        "recommendation_k": 0.2,
        "mainline_021": {
            "report": "rpt-ref-fe49179fb6a8ad8c986e",
            "ingested": "2026-10-20T00:31:15-07:00",
            "family": "P2 Be faces on aluminium honeycomb",
            "named_optimisms": 2,
            "gamma": 0.579,
            "gamma_factor_over_0.20": 2.90,
            "wrinkling_coefficient": 0.363,
            "wrinkling_factor_over_0.33": 1.10,
            "face_allowable_MPa": 283.0,
            "least_SF": 1.0,
            "full_set_least_SF": 1.111,
        },
    }
    return results


def row_sentence(row):
    edges = []
    if row["s_m"] >= 2.999:
        edges.append("s is on the 3 m band edge")
    if row["r_o_m"] >= 0.249:
        edges.append("r_o is on the 0.25 m cap")
    if row["h_m"] >= row["s_m"] / 5.0 - 1e-9 and row["h_over_sagitta"] > 1.01:
        edges.append("the rise is on the s/5 cap")
    edge = (" " + " ".join(edges) + ".") if edges else ""
    return (
        "Least SF {sf} by {gov}. s {s} m, rise {h} m ({hr} times the sagitta), r_o {ro} mm, wall {tw} mm, r/t {rt}, film {tf} mm ({film}). "
        "Yield {y}, Euler {e}, local {loc}, film {f}, Perry {p}, global {gl}. "
        "Tubes {tu} kg, nodes {nd} kg, joints {jt} kg, film {fm} kg, systems 100 kg, payload 244.47210751 kg.{edge}"
    ).format(
        sf=g(row["SF_least"]), gov=row["governing"], s=g(row["s_m"]), h=g(row["h_m"]),
        hr=g(row["h_over_sagitta"]), ro=g(row["r_o_m"] * 1e3), tw=g(row["t_w_m"] * 1e3),
        rt=g(row["rt"]), tf=g(row["t_film_m"] * 1e3), film=row["film"],
        y=g(row["SF_yield"]), e=g(row["SF_euler"]), loc=g(row["SF_local"]),
        f=g(row["SF_film"]), p=g(row["SF_perry"]), gl=g(row["SF_global"]),
        tu=g(row["m_tube_kg"]), nd=g(row["m_nodes_kg"]), jt=g(row["m_joint_kg"]),
        fm=g(row["m_film_kg"]), edge=edge,
    )


def p3_factors(flags, row):
    found = []
    if "crush_3900_MPa" in flags:
        found.append(("3900 MPa crush over the 380 MPa flexural bar", SIG_CRUSH / SIG_FLEX))
    if "film_1.5_GPa" in flags:
        found.append(("1.5 GPa film over Mylar 850H machine-direction 22 kpsi", 1.5e9 / (22.0 * 6894757.293178)))
    if "k_0.4" in flags:
        found.append(("k 0.4 over the ceramic floor 0.2", 2.0))
    if "arc_rise_above_sphere" in flags:
        found.append(("arc rise over the spherical sagitta", row["h_over_sagitta"]))
    return found


def comparison_sentence(results):
    """Which family needs less optimism. Factor size first, then the count."""
    least = results["least_optimism_set"]
    p2 = results["mainline_021"]
    if least is None:
        return (
            "MAINLINE-021 has filed. Its P2 sandwich, beryllium faces at 283 MPa on aluminium honeycomb, "
            "reaches SF 1 on two named optimisms: gamma 0.579, which is 2.90 times CR-1457's 0.20, and a "
            "wrinkling coefficient 0.363, which is 1.10 times 0.33. Its least mode is 1.000, and the full named "
            "set is 1.111. No catalog point on this P3 frame reaches SF 1, so the P2 sandwich needs less optimism."
        )
    factors = p3_factors(least["flags"], least["equilateral"])
    if not factors:
        largest = 1.0
        named = "no departure from the sourced-today row"
    else:
        named, largest = max(factors, key=lambda item: item[1])
        named = named + ", factor " + g(largest)
    if largest > 2.90:
        who = "The P2 sandwich needs less optimism. Its largest named factor is 2.90, and this frame's largest is " + g(largest) + " (" + named + ")."
    elif largest < 2.90:
        who = "This P3 frame needs less optimism. Its largest factor is " + g(largest) + ", under P2's 2.90."
    else:
        who = "The largest named factors match at 2.90."
    flags = ", ".join(least["flags"]) if least["flags"] else "none"
    return (
        "MAINLINE-021 has filed ({rid}). Its P2 sandwich reaches SF 1 on gamma 2.90 times 0.20 and a wrinkling "
        "coefficient 1.10 times 0.33, at a face allowable of 283 MPa. Least mode 1.000. Full named set 1.111. "
        "This frame's least equilateral set is {flags}, least SF {sf}. {who} Both are QUESTIONABLE."
    ).format(
        rid=p2["report"], flags=flags, sf=g(least["equilateral"]["SF_least"]), who=who,
    )

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def write_nfi(results):
    b = results["baseline_today"]
    fit = b["fittings"]
    perm = b["permeation"]
    man = b["manufacture"]
    w = results["weibull_equilateral_k02"]
    rows = [
        {
            "id": "NFI-022-SIC-ALLOWABLE",
            "value_scored_today_Pa": SIG_FLEX,
            "sourced_today": "Saint-Gobain Hexoloy SA 4-point flexural strength 380 MPa on a 3 x 4 x 45 mm bar. Compressive strength on the same sheets is 3900 MPa.",
            "weibull_Pa": SIG_WEIBULL,
            "weibull_note": "Two-parameter Weibull at P_f = 0.001, m = 10, sigma_0 taken as 380 MPa, same volume as the bar. m = 10 is the seal-tube and structural-tile page. Sheet B-1003-2 lists 8 for standard SA and 12 for enhanced SA. This is not a volume-scaled tube allowable, and it is not a compression test.",
            "crush_Pa": SIG_CRUSH,
            "factor_crush_over_flexural": SIG_CRUSH / SIG_FLEX,
            "factor_flexural_over_weibull": SIG_FLEX / SIG_WEIBULL,
            "state": "PENDING-025. 380 and 3900 exist on the datasheet. The 190 MPa figure is a calculation. This card carries 3900 MPa as 011b did. Using it as a tube allowable is an optimism. MAINLINE-025 owns the row.",
            "scored_baseline_SF": b["SF_least"],
            "weibull_case_SF": w["SF_least"],
            "source": "https://www.ceramicsrefractories.saint-gobain.com/hexoloy-enhanced-sa-sic-technical-data-sheet and the Hexoloy seal-tube page",
        },
        {
            "id": "NFI-022-BENDING-CONTACT",
            "service_axial_Pa": b["sigma_axial_Pa"],
            "flexural_Pa": SIG_FLEX,
            "SF_axial_over_flexural": SIG_FLEX / b["sigma_axial_Pa"] if b["sigma_axial_Pa"] else None,
            "bearing_area_for_380_m2": fit["A_bearing_for_380_m2"],
            "tube_area_m2": fit["tube_area_m2"],
            "note": "PENDING-025. At the sourced-today point the axial stress is the contact stress if the tube section bears the member force. Perry is the scored bending-imperfection mode. MAINLINE-025 owns the allowable.",
        },
        {
            "id": "NFI-022-TUBE",
            "design_OD_mm": man["this_OD_mm"],
            "design_length_m": man["this_length_m"],
            "design_wall_mm": man["this_wall_mm"],
            "exists": "Hexoloy SA process tubes: OD 25 to 381 mm, single piece to 1.4 m, bonded assemblies to 4.9 m. Seal tubes are about 0.30 m long. Silit SiSiC radiant tubes reach OD 300 mm, length 3.5 m, thinnest published wall about 4 mm, Amasic-3D about 2 mm.",
            "factor_length_over_hexoloy_single": man["length_over_hexoloy_single"],
            "factor_wall_vs_2mm": man["wall_over_amasic_min"],
            "state": "PENDING-025. A 250 mm class diameter exists. A 2 m single Hexoloy piece does not. A wall near 0.9 mm is below the 2 mm SiSiC floor and is a PROJECTION for alpha-SiC. MAINLINE-025 owns the manufacture row. These factors are context at the sourced-today geometry, not a closed finding.",
            "source": "https://www.ceramicsrefractories.saint-gobain.com/products/shapes/tubes/hexoloy-sic-process-tubes and the ceramic radiant tube page",
        },
        {
            "id": "NFI-022-JOINTS",
            "allowance_kg": fit["allowance_kg"],
            "lower_bound_kg": fit["lower_bound_one_per_node_kg"],
            "upper_bound_kg": fit["upper_bound_per_member_end_kg"],
            "member_force_N": b["N_N"],
            "factor_lower_over_allowance": fit["lower_bound_one_per_node_kg"] / fit["allowance_kg"],
            "state": "PENDING-023. This card carries joints at 5 percent of film, nodes and tubes, 216.427144889 kg. The bounds are context only: a SiC pad at 380 MPa over one tube diameter of engagement. MAINLINE-023 owns the joint mass. A 1 MN ceramic load introduction is not a catalog fitting.",
            "tag": "PENDING-023",
        },
        {
            "id": "NFI-022-FILM",
            "today": "Mylar 850H, tensile MD 22 kpsi, density 1.40 g/cc, O2 transmission 6.0 cc/100 in2/day at 48 gauge and 1 atm.",
            "scored_thickness_m": b["t_film_m"],
            "scored_sigma_Pa": 22.0 * 6894757.293178,
            "permeation_kg_per_day": perm.get("kg_per_day"),
            "permeation_pct_of_1pct_budget": perm.get("pct_of_1pct_budget"),
            "method": "MAINLINE-016: 1 percent of lift per day is 48.894 kg, and permeance is converted as scc to mol to kg at p_ext. Mylar transmission is scaled as 1/thickness from the 48-gauge line.",
            "projection": "The 011 film, 1.5 GPa at 970 kg/m3, has no datasheet. It is the film optimism.",
            "source": "https://polymerfilms.com/wp-content/uploads/2023/09/Mylar850H-Datasheets.pdf",
            "state": "PENDING-024. This card carries the 011b film: 1.5 GPa, 970 kg/m3. Mylar exists and is the sourced-today comparison. The 1.5 GPa film is a PROJECTION. MAINLINE-024 owns the film, its thickness and the vacuum permeation. Seams are not in the Mylar figure.",
        },
        {
            "id": "NFI-022-KNOCKDOWN",
            "scored_design": 0.2,
            "wright": 0.4,
            "factor": 2.0,
            "recommendation": "Use k 0.2 for ceramic arcs. A brittle member does not shed load after first crack. Wright 1965 used a modified k of 0.4 for a reticulated-shell table. That factor is an optimism here.",
            "state": "Both values are in the catalog. k 0.2 is the brief's band floor.",
        },
        {
            "id": "NFI-022-021",
            "note": comparison_sentence(results),
        },
        {
            "id": "NFI-022-DATASHEET-SPREAD",
            "note": "This card keeps 011b's E of 410 GPa and density 3100 kg/m3 so the regression is the same material. Hexoloy pages also print E 430 GPa, density 3.10 to 3.15 g/cm3, and Poisson's ratio 0.14. The local-buckling coefficient stays 0.6.",
        },
    ]
    return {"schema": 1, "card": "MAINLINE-022", "unit": "vacuum-mainline022-p3-optimistic-floating-point-1020", "rows": rows}


def write_inputs(pins):
    return {
        "schema": 1,
        "pins": pins,
        "mass": "payload = 0.05*L, systems = 100 kg, joints = 0.05*(film+nodes+tubes)",
        "sic": {"rho": RHO, "E_Pa": E_MOD, "flexural_Pa": SIG_FLEX, "crush_Pa": SIG_CRUSH, "weibull_Pa": SIG_WEIBULL, "m": M_WEIBULL},
        "films": list(FILMS),
        "global": {"C_triangular": C_TRI, "C_two_way": C_TWO},
        "arch": "N = p*s^3/(16*h) with h the sagitta. At h = s^2/(8R) this is N = p*R*s/2.",
        "sources": [
            "https://www.ceramicsrefractories.saint-gobain.com/hexoloy-enhanced-sa-sic-technical-data-sheet",
            "https://www.ceramicsrefractories.saint-gobain.com/products/shapes/tubes/hexoloy-sic-process-tubes",
            "https://www.ceramicsrefractories.saint-gobain.com/products/shapes/tubes/hexoloy-seal-tubes",
            "https://www.ceramicsrefractories.saint-gobain.com/products/products-application/heating-systems/ceramic-radiant-tube",
            "https://polymerfilms.com/wp-content/uploads/2023/09/Mylar850H-Datasheets.pdf",
        ],
    }


def main():
    if os.path.exists(RESULTS_PATH):
        raise SystemExit("RESULTS.json is the measured run. Not recomputing.")
    passed, bucket = run_checks()
    if not passed:
        raise SystemExit(3)
    if "--checks-only" in os.sys.argv:
        print("CHECKS_ONLY pass")
        return
    mono0 = time.monotonic()
    wall0 = datetime.datetime.now(ZONE)
    origin = {"origin_local": wall0.isoformat(timespec="microseconds"), "origin_monotonic_s": mono0}
    if os.path.exists(ORIGIN_PATH):
        origin = json.loads(open(ORIGIN_PATH, encoding="utf-8").read())
        print("ORIGIN exists; not restamping")
    else:
        atomic_write(ORIGIN_PATH, json.dumps(origin, indent=1) + "\n")
        print("ORIGIN", origin["origin_local"])
    results = build(origin, None, bucket)
    wall1 = datetime.datetime.now(ZONE)
    results["elapsed_s"] = time.monotonic() - origin["origin_monotonic_s"]
    results["ended_local"] = wall1.isoformat(timespec="microseconds")
    pins = next(item["pins"] for item in bucket if "pins" in item)
    atomic_write(RESULTS_PATH, json.dumps(results, indent=1) + "\n")
    atomic_write(os.path.join(ROOT, "NFI.json"), json.dumps(write_nfi(results), indent=1) + "\n")
    atomic_write(os.path.join(ROOT, "INPUTS.json"), json.dumps(write_inputs(pins), indent=1) + "\n")
    atomic_write(os.path.join(ROOT, "CARD.md"), write_card(results))
    b = results["baseline_today"]
    print("elapsed", g(results["elapsed_s"]))
    print("BASE", g(b["SF_least"]), b["governing"], "s", g(b["s_m"]), "ro", g(b["r_o_m"]), "tw", g(b["t_w_m"]),
          "tf", g(b["t_film_m"]), "y", g(b["SF_yield"]), "p", g(b["SF_perry"]), "g", g(b["SF_global"]), "f", g(b["SF_film"]))
    least = results["least_optimism_set"]
    if least:
        er = least["equilateral"]
        print("LEAST", least["flags"], g(er["SF_least"]), er["governing"], "s", g(er["s_m"]),
              "hmult", g(er["h_over_sagitta"]), "ro", g(er["r_o_m"]), "tw", g(er["t_w_m"]),
              "film", er["film"], "tf", g(er["t_film_m"]))
        print("LEAST2", g(least["two_way"]["SF_least"]), least["two_way"]["governing"])
    else:
        print("NO POINT AT SF 1")
    car = results["carried_011b_k02"]["equilateral"]
    print("CARRIED", g(car["SF_least"]), car["governing"], "s", g(car["s_m"]), "ro", g(car["r_o_m"]),
          "tw", g(car["t_w_m"]), "tf", g(car["t_film_m"]), "hr", g(car["h_over_sagitta"]),
          "y", g(car["SF_yield"]), "e", g(car["SF_euler"]), "l", g(car["SF_local"]),
          "f", g(car["SF_film"]), "p", g(car["SF_perry"]), "g", g(car["SF_global"]))
    print("CARRIED2", g(results["carried_011b_k02"]["two_way"]["SF_least"]), results["carried_011b_k02"]["two_way"]["governing"])
    c4 = results["carried_011b_k04"]["equilateral"]
    print("CARRIED04", g(c4["SF_least"]), c4["governing"], "s", g(c4["s_m"]))
    print("WEIBULL", g(results["weibull_equilateral_k02"]["SF_least"]), results["weibull_equilateral_k02"]["governing"])
    reachers = [c for c in results["catalog"] if c["reaches_SF_1"]]
    print("reachers", len(reachers))
    for c in reachers[:8]:
        print(" ", c["n_flags"], c["flags"], g(c["equilateral_SF"]), c["equilateral_governing"])


if __name__ == "__main__":
    import sys
    main()
