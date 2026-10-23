#!/usr/bin/env python3
"""MAINLINE-024: P3 film load, sourced candidates, barrier, mass, restated SF.

Own arithmetic. arcs.py and the 016 script are read and not executed.
Every design thickness uses a creep-rupture fraction or a stated knockdown
on an opened ultimate. The 011b film allowable of 1.5 GPa is not a candidate.
"""
import datetime
import hashlib
import json
import math
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ZONE = datetime.datetime.now().astimezone()


def g(x):
    return format(x, ".12g")


def sha_file(path):
    data = open(path, "rb").read()
    return hashlib.sha256(data).hexdigest(), len(data)


# Case. COMMON.md decimals, and 011b's arc constants.
R = 10.0
P_EXT = 95460.8379139
L_MASS = 4889.44215019
M_NODE_UNIT = 0.02
M_SYS = 50.0
JOINT_FRAC = 0.05
C_LOCAL = 0.6
C_TRI = 4.0 * math.sqrt(1.5)
N_RO = 4000
SLENDER = 3.0
S_BAY = 2.04
# 016 compute.py lift, used only for that card's 1% per day allowance.
LIFT_016 = 4889.442150186961
ALLOW_KG_DAY = 0.01 * LIFT_016
M_AIR = 0.02897
M_O2 = 0.031998
M_N2 = 0.028014
V_STP = 0.022414  # m3/mol
X_O2 = 0.20946
X_N2 = 0.78084
ATM = 101325.0
PUMP_KG = (150.0, 400.0)

# 011b pin, reproduced, not used as a candidate allowable.
M_FILM_PIN = 97.515
SIGMA_PIN = 1.5e9
T_PIN = 8e-5
RHO_PIN = 970.0

SIC = (3100.0, 410e9, 3900e6)
S_ALL = [round(0.4 + 0.02 * i, 3) for i in range(301)]
S_BAND = [s for s in S_ALL if s <= 3.0 + 1e-12]

# Stated where no creep-rupture fraction was opened. Not a test.
KNOCK_ASSUMED = 0.5

A_HULL = 4.0 * math.pi * R * R
P_O2 = X_O2 * P_EXT
P_N2 = X_N2 * P_EXT
# 011b curvature: p = 2*sigma*t/s, so the pillow radius is the bay side.
R_CURVE = S_BAY
R_TRI = S_BAY / math.sqrt(3.0)
CAP_RISE = R_CURVE - math.sqrt(R_CURVE * R_CURVE - R_TRI * R_TRI)
W_ARC = P_EXT * S_BAY / 2.0
W_TRI = P_EXT * S_BAY * math.sqrt(3.0) / 6.0
SIGMA_PIN_AT_T = P_EXT * R_CURVE / (2.0 * T_PIN)


def mass_pack(s, m_film):
    nodes = 8.0 * math.pi * R * R / (math.sqrt(3.0) * s * s) + 2.0
    m_nodes = M_NODE_UNIT * nodes
    members = 3.0 * nodes - 6.0
    budget = L_MASS - m_film - m_nodes - M_SYS
    if budget <= 0.0:
        return None
    m_tube = budget / (1.0 + JOINT_FRAC)
    m_joint = budget - m_tube
    return nodes, members, m_nodes, m_tube, m_joint, budget


def scan_sic(m_film, sigma_t):
    """SiC, joints on, Perry on, equilateral grid, k=0.2. sigma_t is sigma*t."""
    rho, E, sig = SIC
    factor = 0.2 * C_TRI
    best = None
    best_sf = -1.0
    for s in S_BAND:
        packed = mass_pack(s, m_film)
        if packed is None:
            continue
        nodes, members, m_nodes, m_tube, m_joint, budget = packed
        area = m_tube / (members * s * rho)
        r_min = math.sqrt(area / math.pi) * 1.0001
        r_max = min(0.25, s / SLENDER)
        if r_max <= r_min:
            continue
        span = r_max - r_min
        sf_f = (2.0 * sigma_t / s) / P_EXT
        sf_y = (2.0 * sig * area / (R * s)) / P_EXT
        euler_coef = 2.0 * math.pi ** 2 * E / (R * s ** 3)
        inv = 1.0 / (R * s)
        local_best = None
        local_sf = -1.0
        for i in range(N_RO):
            r_o = r_min + span * i / (N_RO - 1)
            disc = r_o * r_o - area / math.pi
            if disc <= 0.0:
                continue
            r_i = math.sqrt(disc)
            t_w = r_o - r_i
            inertia = math.pi * 0.25 * (r_o ** 4 - r_i ** 4)
            sf_e = euler_coef * inertia / P_EXT
            sig_loc = C_LOCAL * E * t_w / r_o
            sf_l = 2.0 * sig_loc * area * inv / P_EXT
            rg2 = inertia / area
            eta = (s * 0.001) * r_o / rg2
            sig_e = math.pi * math.pi * E * rg2 / (s * s)
            phi = (sig + (eta + 1.0) * sig_e) * 0.5
            discp = phi * phi - sig * sig_e
            if discp < 0.0:
                continue
            sig_cr = phi - math.sqrt(discp)
            sig_app = P_EXT * R * s / (2.0 * area)
            sf_p = sig_cr / sig_app
            g_unit = E * math.sqrt(inertia * area) / (s * R * R)
            sf_g = factor * g_unit / P_EXT
            name, base = "yield", sf_y
            for cand, val in (
                ("euler", sf_e),
                ("local", sf_l),
                ("film", sf_f),
                ("perry", sf_p),
            ):
                if val < base:
                    name, base = cand, val
            if sf_g < base:
                gov, least = "global", sf_g
            else:
                gov, least = name, base
            if least > local_sf:
                local_sf = least
                pairs = [
                    ("yield", sf_y),
                    ("euler", sf_e),
                    ("local", sf_l),
                    ("film", sf_f),
                    ("perry", sf_p),
                    ("global", sf_g),
                ]
                rest = sorted((p for p in pairs if p[0] != gov), key=lambda t: (t[1], t[0]))
                local_best = {
                    "s_m": s,
                    "r_o_m": r_o,
                    "t_w_m": t_w,
                    "m_nodes_kg": m_nodes,
                    "m_joint_kg": m_joint,
                    "m_tube_kg": m_tube,
                    "m_film_kg": m_film,
                    "budget_kg": budget,
                    "SF_least": least,
                    "governing": gov,
                    "second": rest[0][0],
                    "SF_second": rest[0][1],
                    "SF_global": sf_g,
                    "SF_film": sf_f,
                    "SF_yield": sf_y,
                    "SF_euler": sf_e,
                    "SF_local": sf_l,
                    "SF_perry": sf_p,
                    "closure_kg": m_film + m_nodes + m_joint + m_tube + M_SYS,
                }
        if local_best is not None and local_best["SF_least"] > best_sf:
            best_sf = local_best["SF_least"]
            best = local_best
    return best


def thickness_isotropic(sigma):
    return P_EXT * R_CURVE / (2.0 * sigma)


def mass_of(t, rho):
    return A_HULL * t * rho


def gas_from_permeance(permeance_mol, partial_pa, molar_mass):
    """permeance mol/(m2 s Pa) -> kg/day over the hull."""
    return permeance_mol * A_HULL * partial_pa * molar_mass * 86400.0


def cc_day_to_kg(cc_per_m2_day, molar_mass):
    m3 = cc_per_m2_day * 1e-6
    mol = m3 / V_STP
    return mol * molar_mass * A_HULL


def pump_sentence(kg_day_known, missing):
    if missing:
        held = "not shown"
    elif kg_day_known <= ALLOW_KG_DAY:
        held = "holds the sourced load"
    else:
        held = "does not hold the sourced load"
    return {
        "sourced_kg_per_day": kg_day_known,
        "allowance_kg_per_day": ALLOW_KG_DAY,
        "pump_kg_band": list(PUMP_KG),
        "pump": held,
        "getter": "016 gives no getter capacity",
        "missing": missing,
    }


def main():
    started = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    pin = scan_sic(M_FILM_PIN, SIGMA_PIN * T_PIN)
    target = 1.22552794688
    if pin is None or abs(pin["SF_least"] - target) > 1e-9:
        raise SystemExit("PIN SCAN MISMATCH %s" % (None if pin is None else repr(pin["SF_least"])))
    if abs(pin["s_m"] - 2.04) > 1e-12:
        raise SystemExit("PIN S MISMATCH %s" % pin["s_m"])
    if abs(pin["r_o_m"] * 1e3 - 123.688362374) > 1e-6:
        raise SystemExit("PIN RO MISMATCH %s" % (pin["r_o_m"] * 1e3))
    if abs(pin["t_w_m"] * 1e3 - 0.880299093685) > 1e-6:
        raise SystemExit("PIN TW MISMATCH %s" % (pin["t_w_m"] * 1e3))

    # Opened numbers. Units SI. Comments name the file in sources/.
    # Kapton HN, all listed gauges: 231 MPa, 2.76 GPa, 1.42 g/cm3.
    # Summary Table 10, 25 um: O2 3800, N2 910 mL/(m2 day MPa); water 54 g/(m2 day).
    kapton_ult = 231e6
    kapton_rho = 1420.0
    kapton_e = 2.76e9
    kapton_sig = KNOCK_ASSUMED * kapton_ult
    kapton_t = thickness_isotropic(kapton_sig)
    # Teonex Q51. IEC sheet, 25 um: TD 265 MPa, E 6080 MPa, rho 1.36.
    # Hongrun gauge table: 250 um row is 210 MPa both ways. Required thickness
    # is above that row, so the opened thick-gauge ultimate is the one used.
    # O2 permeability 0.8e-12 cc cm/(cm2 s cmHg). Water 6.7 g/m2/day at 25 um.
    pen_ult = 210e6
    pen_rho = 1360.0
    pen_e = 6.08e9
    pen_sig = KNOCK_ASSUMED * pen_ult
    pen_t = thickness_isotropic(pen_sig)
    # Zylon HM filament. 5.8 GPa, 270 GPa, 1.56 g/cm3.
    # Toyobo: at 60% of break, extrapolated rupture life 1e7 min (19 years).
    zylon_ult = 5.8e9
    zylon_rho = 1560.0
    zylon_e = 270e9
    zylon_frac = 0.60
    zylon_sig = zylon_frac * zylon_ult
    zylon_t_dir = thickness_isotropic(zylon_sig)
    zylon_t = 2.0 * zylon_t_dir
    # Vectran HT filament. ~3.2 GPa, ~75 GPa, 1.40 g/cm3. No creep fraction.
    vec_ult = 3.2e9
    vec_rho = 1400.0
    vec_e = 75e9
    vec_sig = KNOCK_ASSUMED * vec_ult
    vec_t = 2.0 * thickness_isotropic(vec_sig)
    # Dyneema. FibrXL: DM20 3.1 GPa at 32.0 cN/dtex; SK78 3.4 GPa at 35.1 cN/dtex.
    # Density is GPa divided by N/tex from that same row.
    # CIS YA104: 200 kN on a 1000 kN rope is 20% of break, 16 C.
    # DM20 250 years, SK78 15 years. Indicative rope numbers.
    dm_ult = 3.1e9
    dm_tex = 3.20  # N/tex
    # 1 GPa per (N/tex) is 1 g/cm3. The sheet prints both and not the density.
    dm_rho = (dm_ult / 1e9) / dm_tex * 1000.0
    dm_e = 94e9
    dm_sig = 0.20 * dm_ult
    dm_t = 2.0 * thickness_isotropic(dm_sig)
    sk_ult = 3.4e9
    sk_tex = 3.51
    sk_rho = (sk_ult / 1e9) / sk_tex * 1000.0
    sk_e = 113e9
    sk_sig = 0.20 * sk_ult
    sk_t = 2.0 * thickness_isotropic(sk_sig)

    rows = []

    def add_film(key, name, form, state, ult, knock, sig, e_mod, rho, t, creep, barrier_kind):
        areal = t * rho
        mass = mass_of(t, rho)
        rows.append({
            "key": key,
            "name": name,
            "form": form,
            "state": state,
            "tag": "QUESTIONABLE",
            "ultimate_Pa": ult,
            "knockdown": knock,
            "knockdown_basis": creep,
            "design_allowable_Pa": sig,
            "modulus_Pa": e_mod,
            "density_kg_m3": rho,
            "thickness_m": t,
            "pillow_stress_Pa": sig,
            "curvature_radius_m": R_CURVE,
            "areal_kg_m2": areal,
            "mass_kg": mass,
            "against_pin_kg": mass - M_FILM_PIN,
            "barrier": barrier_kind,
        })

    add_film(
        "kapton_hn",
        "Kapton HN polyimide film",
        "biaxial_film",
        "exists today",
        kapton_ult,
        KNOCK_ASSUMED,
        kapton_sig,
        kapton_e,
        kapton_rho,
        kapton_t,
        "no creep-rupture stress in the opened Kapton sheets; knockdown is an assumption",
        "the film itself, scaled from the 25 um table",
    )
    add_film(
        "teonex_q51",
        "Teonex Q51 PEN film",
        "biaxial_film",
        "exists today",
        pen_ult,
        KNOCK_ASSUMED,
        pen_sig,
        pen_e,
        pen_rho,
        pen_t,
        "IEC sheet says the 25 um values are not design data; no creep-rupture stress; knockdown is an assumption on the 250 um ultimate",
        "the film itself, from the 25 um permeability coefficient",
    )
    add_film(
        "zylon_hm_crossply",
        "Zylon HM filament as a 0/90 membrane",
        "filament_crossply",
        "filament exists today; the 0/90 membrane was not sourced",
        zylon_ult,
        zylon_frac,
        zylon_sig,
        zylon_e,
        zylon_rho,
        zylon_t,
        "Toyobo extrapolation: 60 percent of break, 1e7 minutes, about 19 years, on HM filament",
        "not the filament; a separate metallised Mylar layer",
    )
    add_film(
        "vectran_ht_crossply",
        "Vectran HT filament as a 0/90 membrane",
        "filament_crossply",
        "filament exists today; the 0/90 membrane was not sourced",
        vec_ult,
        KNOCK_ASSUMED,
        vec_sig,
        vec_e,
        vec_rho,
        vec_t,
        "no creep-rupture fraction in the opened Vectran sheet; knockdown is an assumption",
        "not the filament; a separate metallised Mylar layer",
    )
    add_film(
        "dyneema_dm20_crossply",
        "Dyneema DM20 filament as a 0/90 membrane",
        "filament_crossply",
        "filament exists today; the 0/90 membrane was not sourced",
        dm_ult,
        0.20,
        dm_sig,
        dm_e,
        dm_rho,
        dm_t,
        "CIS YA104 indicative rope: 20 percent of a 1000 kN break, 16 C, 250 years",
        "not the filament; a separate metallised Mylar layer",
    )
    add_film(
        "dyneema_sk78_crossply",
        "Dyneema SK78 filament as a 0/90 membrane",
        "filament_crossply",
        "filament exists today; the 0/90 membrane was not sourced",
        sk_ult,
        0.20,
        sk_sig,
        sk_e,
        sk_rho,
        sk_t,
        "CIS YA104 indicative rope: 20 percent of a 1000 kN break, 16 C, 15 years, 0.5 percent per year",
        "not the filament; a separate metallised Mylar layer",
    )

    # PET is the barrier sheet. No strength was in it. Stress at the printed gauge.
    pet_t = 12e-6
    pet_stress = P_EXT * R_CURVE / (2.0 * pet_t)
    rows.append({
        "key": "mylar_12um_barrier_only",
        "name": "Mylar polyester 12 um, plain and metallised",
        "form": "barrier_gauge",
        "state": "exists today as a packaging film",
        "tag": "QUESTIONABLE",
        "ultimate_Pa": None,
        "knockdown": None,
        "knockdown_basis": "the opened brochure has transmission, not a strength, modulus, density or creep",
        "design_allowable_Pa": None,
        "modulus_Pa": None,
        "density_kg_m3": None,
        "thickness_m": pet_t,
        "pillow_stress_Pa": pet_stress,
        "curvature_radius_m": R_CURVE,
        "areal_kg_m2": None,
        "mass_kg": None,
        "against_pin_kg": None,
        "barrier": "this gauge is the barrier layer, not the pillow structure",
    })
    for key, name in (
        ("cnt_sheet", "CNT sheet"),
        ("graphene_laminate", "graphene laminate"),
    ):
        rows.append({
            "key": key,
            "name": name,
            "form": "none_opened",
            "state": "PROJECTION",
            "tag": "PROJECTION",
            "ultimate_Pa": None,
            "knockdown": None,
            "knockdown_basis": "no production allowable was opened",
            "design_allowable_Pa": None,
            "modulus_Pa": None,
            "density_kg_m3": None,
            "thickness_m": None,
            "pillow_stress_Pa": None,
            "curvature_radius_m": R_CURVE,
            "areal_kg_m2": None,
            "mass_kg": None,
            "against_pin_kg": None,
            "barrier": "not opened",
        })

    # Gas. Kapton permeance is for 25 um. Scale by 25 um / t.
    kapton_row = next(r for r in rows if r["key"] == "kapton_hn")
    scale_k = 25e-6 / kapton_row["thickness_m"]
    # mL/(m2 day MPa) -> mol/(m2 s Pa)
    def ml_per_mpa_to_perm(ml):
        # ml = 1e-6 m3; per day; per MPa = per 1e6 Pa
        m3 = ml * 1e-6
        mol = m3 / V_STP
        return mol / 86400.0 / 1e6

    k_o2 = gas_from_permeance(ml_per_mpa_to_perm(3800.0) * scale_k, P_O2, M_O2)
    k_n2 = gas_from_permeance(ml_per_mpa_to_perm(910.0) * scale_k, P_N2, M_N2)
    k_h2o = 54.0 * scale_k * A_HULL / 1000.0
    kapton_gas = {
        "o2_kg_day": k_o2,
        "n2_kg_day": k_n2,
        "h2o_kg_day_at_table": k_h2o,
        "h2o_note": "54 g/(m2 day) is the 25 um ASTM E-96 row. The sheet does not print a humidity on that row. Scaled by 25 um over the design thickness.",
        "sum_o2_n2_kg_day": k_o2 + k_n2,
        "pump": pump_sentence(k_o2 + k_n2 + k_h2o, missing=[]),
    }

    # PEN. P = 0.8e-12 cm3 cm / (cm2 s cmHg). Use the design thickness.
    pen_row = next(r for r in rows if r["key"] == "teonex_q51")
    t_cm = pen_row["thickness_m"] * 100.0
    p_coef = 0.8e-12  # cm3 cm / (cm2 s cmHg)
    dp_cmhg = P_O2 * 76.0 / ATM
    cc_per_cm2_s = p_coef / t_cm * dp_cmhg
    cc_per_m2_day = cc_per_cm2_s * 1e4 * 86400.0
    pen_o2 = cc_day_to_kg(cc_per_m2_day, M_O2)
    pen_h2o = 6.7 * (25e-6 / pen_row["thickness_m"]) * A_HULL / 1000.0
    pen_gas = {
        "o2_kg_day": pen_o2,
        "n2_kg_day": None,
        "h2o_kg_day_at_table": pen_h2o,
        "h2o_note": "6.7 g/(m2 day) at 25 um, JIS Z0208. The sheet does not print the humidity. Scaled by thickness. N2 is not on the sheet.",
        "o2_cc_m2_day": cc_per_m2_day,
        "pump": pump_sentence(pen_o2 + pen_h2o, missing=["n2"]),
    }

    # Metallised Mylar 12 um. Brochure rate at 100% oxygen. Read as 1 atm.
    # Hull O2 is the partial pressure over that 1 atm.
    mylar_scale = P_O2 / ATM
    my_o2 = cc_day_to_kg(0.5 * mylar_scale, M_O2)
    my_h2o = 1.0 * A_HULL / 1000.0  # upper bound, <1 g/m2/day
    plain_o2 = cc_day_to_kg(140.0 * mylar_scale, M_O2)
    plain_h2o = 40.0 * A_HULL / 1000.0
    mylar_gas = {
        "metallised_od3_12um": {
            "o2_kg_day": my_o2,
            "n2_kg_day": None,
            "h2o_kg_day_upper_at_38C_90RH": my_h2o,
            "condition": "O2 column is 100% oxygen, 25 C, 45% RH. Water column is 38 C, 90% RH. Pressure is not printed; 1 atm of oxygen is the reading used for the scale.",
        },
        "plain_12um": {
            "o2_kg_day": plain_o2,
            "h2o_kg_day_at_38C_90RH": plain_h2o,
        },
        "pump_metallised": pump_sentence(my_o2 + my_h2o, missing=["n2"]),
    }

    # ALD. Groner 2006: O2 below 5e-3 cc/m2/day for >=5 nm; water ~1e-3 g/m2/day at 26 nm.
    ald_o2_upper = cc_day_to_kg(5e-3, M_O2)
    ald_h2o = 1e-3 * A_HULL / 1000.0
    ald = {
        "thickness_m": 26e-9,
        "state": "in the lab, on coupon PEN and Kapton, not a hull",
        "tag": "PROJECTION",
        "o2_kg_day_upper": ald_o2_upper,
        "h2o_kg_day": ald_h2o,
        "n2_kg_day": None,
        "mass_note": "26 nm. A mass of 1 kg on this hull would need a density above 30550 kg/m3. The layer does not move the 98 kg comparison.",
        "pump": pump_sentence(ald_o2_upper + ald_h2o, missing=["n2"]),
    }

    ranked = sorted((r for r in rows if r["mass_kg"] is not None), key=lambda r: r["mass_kg"])
    lightest = ranked[0]
    films_only = sorted(
        (r for r in rows if r["form"] == "biaxial_film"),
        key=lambda r: r["mass_kg"],
    )
    light_film = films_only[0]

    def restate(row):
        # sigma*t product: isotropic uses sigma*t; crossply uses sigma_fiber * t_dir = p*Rc/2.
        product = P_EXT * R_CURVE / 2.0
        found = scan_sic(row["mass_kg"], product)
        frozen = None
        # r_o search is inside scan; also record that s=2.04 film SF is 1 by sizing.
        return {
            "key": row["key"],
            "mass_kg": row["mass_kg"],
            "areal_kg_m2": row["areal_kg_m2"],
            "scan": found,
            "film_sf_at_2p04": 1.0,
            "closure_matches_lift": found is not None and abs(found["closure_kg"] - L_MASS) < 1e-6,
        }

    rest_light = restate(lightest)
    rest_film = restate(light_film)
    if rest_light["scan"] is None or rest_film["scan"] is None:
        raise SystemExit("RESCAN FAILED")

    m_film_check = 4.0 * math.pi * R * R * T_PIN * RHO_PIN
    ended = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

    sources = []
    src_dir = os.path.join(ROOT, "sources")
    for name in sorted(os.listdir(src_dir)):
        if name.lower().endswith(".pdf"):
            path = os.path.join(src_dir, name)
            digest, nbytes = sha_file(path)
            sources.append({"path": path, "sha256": digest, "bytes": nbytes})

    read_only = [
        "unpublished-local-ref:16ecc0c012565c0a",
        "withheld-source:b528d6a62c81ce0b",
        "evidence/3386d33e97dda171-arcs.py",
        "evidence/8d1c42afdeb216fd-CARD.md",
        "evidence/9bfdcd6086870cbc-compute.py",
    ]
    pins = []
    for path in read_only:
        digest, nbytes = sha_file(path)
        pins.append({"path": path, "sha256": digest, "bytes": nbytes})

    results = {
        "schema": 1,
        "card": "MAINLINE-024",
        "unit": "vacuum-mainline024-p3-film-1020",
        "seat": "ref-1a533823b6613bf7ff73",
        "questionable": True,
        "certification": False,
        "started_at": started,
        "ended_at": ended,
        "geometry": {
            "bay_m": S_BAY,
            "curvature_radius_m": R_CURVE,
            "curvature_basis": "011b film pressure is 2*sigma*t/s, so the pillow radius is the bay side",
            "triangle_circumradius_m": R_TRI,
            "cap_rise_m": CAP_RISE,
            "hemisphere_not_used_m": R_TRI,
            "line_load_011b_N_per_m": W_ARC,
            "line_load_triangle_share_N_per_m": W_TRI,
            "line_load_used": "011b w=p*s/2",
            "pin_stress_at_80um_Pa": SIGMA_PIN_AT_T,
            "pin_film_mass_check_kg": m_film_check,
            "hull_area_m2": A_HULL,
        },
        "pin_reproduction": pin,
        "candidates": rows,
        "gas": {"kapton_design": kapton_gas, "pen_design": pen_gas, "mylar": mylar_gas, "ald_26nm": ald},
        "lightest_design_row": rest_light,
        "lightest_biaxial_film": rest_film,
        "allowance_kg_day": ALLOW_KG_DAY,
        "pump_kg_band": list(PUMP_KG),
    }

    nfi = {
        "tag": "QUESTIONABLE",
        "rows": [
            {"id": "NFI-FILM-ALLOWABLE-011B", "state": "unsourced", "note": "1.5 GPa and 80 um at 970 kg/m3 are the 011b pin. They are not a candidate allowable."},
            {"id": "NFI-CURVATURE", "state": "assumption", "note": "Pillow radius is set to the bay side, 2.04 m, because that is the 011b film formula. It is not a measured cap."},
            {"id": "NFI-KNOCK-HALF", "state": "assumption", "note": "Where no creep-rupture fraction was opened, the design stress is half the opened ultimate. Kapton, Teonex and Vectran use it."},
            {"id": "NFI-ZYLON-EXTRAPOLATION", "state": "exists as a filament test note", "note": "The 19 year life is Toyobo's extrapolation of an HM filament at 60 percent of break, not a laminate test."},
            {"id": "NFI-CROSSPLY", "state": "assumption", "note": "A uniaxial filament needs a 0/90 build to carry both pillow directions. Total thickness is twice the one-direction thickness. No resin is included, so a real laminate is heavier."},
            {"id": "NFI-DYNEEMA-ROPE", "state": "exists as a rope example", "note": "The 20 percent fraction and the 15 and 250 year lives are indicative rope numbers at 16 C, not a film."},
            {"id": "NFI-DYNEEMA-DENSITY", "state": "derived from the same row", "note": "Density is the printed GPa divided by the printed N/tex. The sheet does not print density."},
            {"id": "NFI-PEN-THICKNESS", "state": "exists today", "note": "The design thickness is above the 250 um row. The 210 MPa ultimate is the thickest opened gauge, not a measurement at the design thickness."},
            {"id": "NFI-PEN-NOT-DESIGN-DATA", "state": "exists today", "note": "The IEC Teonex sheet says its typical values are not design data."},
            {"id": "NFI-MYLAR-STRENGTH", "state": "not opened", "note": "The barrier brochure has no PET strength, modulus, density or creep. The 12 um mass is not computed."},
            {"id": "NFI-MYLAR-PRESSURE", "state": "assumption", "note": "The oxygen column does not print the test pressure. The scale uses 1 atm of oxygen."},
            {"id": "NFI-N2-MISSING", "state": "not opened", "note": "N2 is opened for Kapton only. PEN, Mylar and the ALD paper do not give N2."},
            {"id": "NFI-HULL-HUMIDITY", "state": "not in the case", "note": "The case has no exterior humidity. Water loads stay at the sheet condition and are not a hull rate."},
            {"id": "NFI-ALD-SCALE", "state": "in the lab", "note": "The alumina numbers are coupon measurements. A 1257 m2 hull coating was not opened. Tagged PROJECTION at hull scale."},
            {"id": "NFI-GETTER", "state": "not in the 016 method", "note": "No getter capacity is stated. The pump band is the 150 to 400 kg catalog class, not scaled to the gas load."},
            {"id": "NFI-CNT-GRAPHENE", "state": "PROJECTION", "note": "No production allowable was opened. Thickness is not stated."},
            {"id": "NFI-FABRIC-POROUS", "state": "assumption", "note": "A filament crossply is not taken as gas-tight. The barrier is a separate layer."},
            {"id": "NFI-AIR-FRACTIONS", "state": "assumption", "note": "Dry-air mole fractions 0.20946 and 0.78084 are not in the vacuum case."},
        ],
    }

    inputs = {
        "started_at": started,
        "ended_at": ended,
        "read_only": pins,
        "sources": sources,
        "formulae": {
            "pillow": "sigma = p*R_c/(2*t), R_c = s = 2.04 m",
            "line_load": "w = p*s/2",
            "triangle_share": "w = p*s*sqrt(3)/6",
            "crossply": "t_total = 2*p*R_c/(2*sigma)",
            "scan": "011b SiC equilateral, k=0.2, joints on, Perry on, s from 0.40 to 3.00 m",
            "gas": "permeance * area * partial pressure * molar mass * 86400",
            "pump": "150 to 400 kg holds 48.8944215019 kg/day; it is not scaled",
        },
    }

    def dump(name, obj):
        path = os.path.join(ROOT, name)
        text = json.dumps(obj, indent=1) + "\n"
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(tmp, path)

    dump("RESULTS.json", results)
    dump("NFI.json", nfi)
    dump("INPUTS.json", inputs)

    def sentence(row):
        return (
            "%s. Form %s. State %s. Design stress %s Pa from knockdown %s. "
            "Thickness %s m. Mass %s kg, %s kg/m2. %s"
            % (
                row["name"],
                row["form"],
                row["state"],
                g(row["design_allowable_Pa"]),
                g(row["knockdown"]),
                g(row["thickness_m"]),
                g(row["mass_kg"]),
                g(row["areal_kg_m2"]),
                row["knockdown_basis"],
            )
        )

    card = []
    card.append("# MAINLINE-024 — the P3 film")
    card.append("")
    card.append("Unit vacuum-mainline024-p3-film-1020. Every row is QUESTIONABLE or PROJECTION. Nothing here is a certification.")
    card.append("")
    card.append("## Load")
    card.append("")
    card.append(
        "The 011b film formula is p = 2*sigma*t/s, so this card sets the pillow radius to the 2.04 m bay. "
        "The triangle's circumradius is %s m. The cap rise on that radius is %s m. A hemisphere of radius %s m is not used."
        % (g(R_TRI), g(CAP_RISE), g(R_TRI))
    )
    card.append(
        "The line load used by the arcs is p*s/2 = %s N/m. The triangular tributary is %s N/m and is not the load in the scan."
        % (g(W_ARC), g(W_TRI))
    )
    card.append(
        "At the pinned 80 um film the biaxial stress is %s Pa. The pin mass check is %s kg against 97.515 kg. "
        "That 1.5 GPa allowable is not used for a candidate."
        % (g(SIGMA_PIN_AT_T), g(m_film_check))
    )
    card.append("")
    card.append("## Candidates")
    card.append("")
    card.append(
        "A candidate that is a filament is built as 0/90, so the mass is twice a one-direction membrane. No resin is included. "
        "Where no creep-rupture fraction was opened, the design stress is half the opened ultimate."
    )
    card.append("")
    for row in rows:
        if row["mass_kg"] is None:
            card.append(
                "%s. %s Thickness is not computed. %s"
                % (row["name"], row["state"], row["knockdown_basis"])
            )
        else:
            card.append(sentence(row))
    card.append("")
    card.append(
        "At the printed 12 um Mylar gauge the pillow stress would be %s Pa. That gauge does not carry the bay."
        % g(pet_stress)
    )
    card.append("")
    card.append("## Barrier and the pump")
    card.append("")
    card.append(
        "Kapton at its design thickness passes %s kg/day of oxygen and %s kg/day of nitrogen at the hull partial pressures. "
        "The water row, scaled and still at the sheet's unprinted humidity, is %s kg/day. "
        "The 016 allowance is %s kg/day. The 150 to 400 kg pump holds that sourced load. No getter mass is computed."
        % (g(k_o2), g(k_n2), g(k_h2o), g(ALLOW_KG_DAY))
    )
    card.append(
        "Teonex at its design thickness passes %s kg/day of oxygen. Nitrogen is not on the sheet. "
        "Scaled water at the JIS Z0208 row is %s kg/day."
        % (g(pen_o2), g(pen_h2o))
    )
    card.append(
        "Metallised Mylar at 12 um, scaled from pure oxygen to the hull oxygen pressure, passes %s kg/day of oxygen. "
        "Water at 38 C and 90 percent RH is under %s kg/day. Nitrogen is not on the brochure. "
        "Plain 12 um Mylar water at that climate is %s kg/day, which is above the allowance."
        % (g(my_o2), g(my_h2o), g(plain_h2o))
    )
    card.append(
        "ALD alumina at 26 nm, in the lab, is under %s kg/day of oxygen and about %s kg/day of water. "
        "That is a coupon result. It is PROJECTION on this hull. Its mass does not move the 98 kg comparison."
        % (g(ald_o2_upper), g(ald_h2o))
    )
    card.append("")
    card.append("## Lightest system and the restated factor")
    card.append("")
    card.append(
        "The lightest design row is %s at %s kg, %s kg/m2. It is a filament crossply, not a sourced film, and it still needs the metallised layer. "
        "The metallised layer's kilograms are not computed because the brochure has no density. The structure alone is already above 97.515 kg."
        % (lightest["name"], g(lightest["mass_kg"]), g(lightest["areal_kg_m2"]))
    )
    card.append(
        "The lightest film that exists as a film is %s at %s kg. It is its own barrier."
        % (light_film["name"], g(light_film["mass_kg"]))
    )
    sl = rest_light["scan"]
    sf = rest_film["scan"]
    card.append(
        "The pin scan reproduces least factor %s, global, at s %s m, outer radius %s mm, wall %s mm."
        % (g(pin["SF_least"]), g(pin["s_m"]), g(pin["r_o_m"] * 1e3), g(pin["t_w_m"] * 1e3))
    )
    card.append(
        "With the lightest design mass held, and the film sized so its factor is 1 at 2.04 m, the scan's least factor is %s, governing %s, second %s, at s %s m. "
        "Closure is %s kg against lift %s kg."
        % (g(sl["SF_least"]), sl["governing"], sl["second"], g(sl["s_m"]), g(sl["closure_kg"]), g(L_MASS))
    )
    card.append(
        "With the lightest real film, the least factor is %s, governing %s, at s %s m."
        % (g(sf["SF_least"]), sf["governing"], g(sf["s_m"]))
    )
    card.append("")
    card.append("Stop. The robotics seat sends the next job.")
    card.append("")
    text = "\n".join(card) + "\n"
    path = os.path.join(ROOT, "CARD.md")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp, path)

    print("PIN", g(pin["SF_least"]), pin["governing"], g(pin["s_m"]), g(pin["r_o_m"] * 1e3), g(pin["t_w_m"] * 1e3))
    print("NODES", g(pin["m_nodes_kg"]), "JOINTS", g(pin["m_joint_kg"]))
    for row in ranked:
        print("ROW", row["key"], g(row["mass_kg"]), g(row["thickness_m"]), g(row["design_allowable_Pa"]))
    print("LIGHTEST", lightest["key"], g(rest_light["scan"]["SF_least"]), rest_light["scan"]["governing"], g(rest_light["scan"]["s_m"]))
    print("FILM", light_film["key"], g(rest_film["scan"]["SF_least"]), rest_film["scan"]["governing"], g(rest_film["scan"]["s_m"]))
    print("KAPTON GAS", g(k_o2), g(k_n2), g(k_h2o))
    print("PEN GAS", g(pen_o2), g(pen_h2o))
    print("MYLAR", g(my_o2), g(my_h2o), g(plain_o2), g(plain_h2o))
    print("ALD", g(ald_o2_upper), g(ald_h2o))
    print("STRESS12", g(pet_stress))
    print("W", g(W_ARC), g(W_TRI), "RISE", g(CAP_RISE))
    print("DONE", ended)


if __name__ == "__main__":
    main()
