#!/usr/bin/env python3
"""MAINLINE-024 added load: film sag and the lift it costs.

The filed film card is not rewritten. This script charges the note's sag.
arcs.py is not executed.
"""
import datetime
import hashlib
import json
import math
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
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
A_HULL = 4.0 * math.pi * R * R
SQRT3 = math.sqrt(3.0)
SIC = (3100.0, 410e9, 3900e6)

# Design rows from the filed card. Same allowables. Not re-sourced here.
CANDIDATES = (
    ("zylon_hm_crossply", "Zylon HM 0/90", 3.48e9, 1560.0, True),
    ("vectran_ht_crossply", "Vectran HT 0/90", 1.60e9, 1400.0, True),
    ("dyneema_sk78_crossply", "Dyneema SK78 0/90", 0.68e9, 968.660968661, True),
    ("dyneema_dm20_crossply", "Dyneema DM20 0/90", 0.62e9, 968.75, True),
    ("kapton_hn", "Kapton HN", 115.5e6, 1420.0, False),
    ("teonex_q51", "Teonex Q51", 105.0e6, 1360.0, False),
)


def g(x):
    return format(x, ".12g")


def crown(s, base_radius):
    disc = s * s - base_radius * base_radius
    return s - math.sqrt(disc)


def mean_of_cap(s, h):
    return h * (3.0 * s - h) / (3.0 * (2.0 * s - h))


def sag_pack(s):
    a_in = s / (2.0 * SQRT3)
    h = crown(s, a_in)
    mean = mean_of_cap(s, h)
    fraction = 3.0 * mean / R
    a_out = s / SQRT3
    h_vertex = crown(s, a_out)
    mean_vertex = mean_of_cap(s, h_vertex)
    return {
        "s_m": s,
        "inradius_m": a_in,
        "crown_m": h,
        "mean_m": mean,
        "s_over_24_m": s / 24.0,
        "lift_fraction": fraction,
        "lift_kg": fraction * L_MASS,
        "vertex_crown_m": h_vertex,
        "vertex_mean_m": mean_vertex,
        "vertex_lift_kg": (3.0 * mean_vertex / R) * L_MASS,
    }


def film_mass(s, sigma, rho, crossply):
    # One direction: t = p*s/(2*sigma). Crossply doubles it.
    t_dir = P_EXT * s / (2.0 * sigma)
    t = (2.0 * t_dir) if crossply else t_dir
    return t, A_HULL * t * rho


def mass_pack(s, charged):
    nodes = 8.0 * math.pi * R * R / (SQRT3 * s * s) + 2.0
    m_nodes = M_NODE_UNIT * nodes
    members = 3.0 * nodes - 6.0
    budget = L_MASS - charged - m_nodes - M_SYS
    if budget <= 0.0 or members <= 0.0:
        return None
    m_tube = budget / (1.0 + JOINT_FRAC)
    m_joint = budget - m_tube
    return nodes, members, m_nodes, m_tube, m_joint, budget


def score_s(s, charged):
    """SiC equilateral k=0.2 at one bay. Film is sized to factor 1."""
    rho, E, sig = SIC
    packed = mass_pack(s, charged)
    if packed is None:
        return None
    nodes, members, m_nodes, m_tube, m_joint, budget = packed
    area = m_tube / (members * s * rho)
    r_min = math.sqrt(area / math.pi) * 1.0001
    r_max = min(0.25, s / SLENDER)
    if r_max <= r_min:
        return None
    span = r_max - r_min
    factor = 0.2 * C_TRI
    sf_f = 1.0
    sf_y = (2.0 * sig * area / (R * s)) / P_EXT
    euler_coef = 2.0 * math.pi ** 2 * E / (R * s ** 3)
    inv = 1.0 / (R * s)
    best = None
    best_sf = -1.0
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
        modes = {
            "yield": sf_y,
            "euler": sf_e,
            "local": sf_l,
            "film": sf_f,
            "perry": sf_p,
            "global": sf_g,
        }
        gov = min(modes, key=lambda name: (modes[name], name))
        least = modes[gov]
        adjusted = {
            "yield": sf_y * SQRT3,
            "euler": sf_e * SQRT3,
            "local": sf_l * SQRT3,
            "perry": sf_p * SQRT3,
            "film": sf_f,
            "global": sf_g,
        }
        gov_n = min(adjusted, key=lambda name: (adjusted[name], name))
        if least > best_sf:
            best_sf = least
            best = {
                "s_m": s,
                "r_o_m": r_o,
                "t_w_m": t_w,
                "m_nodes_kg": m_nodes,
                "m_tube_kg": m_tube,
                "m_joint_kg": m_joint,
                "charged_kg": charged,
                "budget_kg": budget,
                "SF_least_011b_force": least,
                "governing_011b_force": gov,
                "SF_global": sf_g,
                "SF_film": sf_f,
                "SF_local_011b": sf_l,
                "SF_least_note_force": adjusted[gov_n],
                "governing_note_force": gov_n,
                "closure_kg": charged + m_nodes + m_joint + m_tube + M_SYS,
            }
    return best


def main():
    started = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    checks = [sag_pack(2.04), sag_pack(3.0), sag_pack(2.0), sag_pack(4.0)]
    # The note's about-figures. Tolerances are the note's own rounding.
    c204, c3 = checks[0], checks[1]
    ok_crown = abs(c204["crown_m"] - 0.087) < 0.001 and abs(c3["crown_m"] - 0.13) < 0.005
    ok_lift = abs(c204["lift_kg"] - 64.0) < 1.0 and abs(c3["lift_kg"] - 94.0) < 1.0
    if not (ok_crown and ok_lift):
        raise SystemExit("NOTE CHECK FAIL %s %s" % (c204, c3))

    s_values = [round(2.0 + 0.02 * i, 2) for i in range(101)]
    table = []
    light = None
    for key, name, sigma, rho, crossply in CANDIDATES:
        series = []
        for s in s_values:
            t, m_film = film_mass(s, sigma, rho, crossply)
            sag = sag_pack(s)
            system = m_film + sag["lift_kg"]
            row = {
                "s_m": s,
                "thickness_m": t,
                "film_kg": m_film,
                "crown_m": sag["crown_m"],
                "mean_m": sag["mean_m"],
                "sag_over_thickness": sag["crown_m"] / t,
                "lift_kg": sag["lift_kg"],
                "lift_fraction": sag["lift_fraction"],
                "system_kg": system,
            }
            series.append(row)
            if light is None or system < light["system_kg"]:
                light = {"key": key, "name": name, **row}
        ends = [series[0], series[s_values.index(2.04)] if 2.04 in s_values else None, series[s_values.index(3.0)], series[-1]]
        # 2.04 is not on a 0.02 grid from 2.00 (2.04 = 2.00+0.02*2). 0.02*2=0.04, yes 2.04 is in the grid.
        table.append({"key": key, "name": name, "crossply": crossply, "at": {
            "s2": series[0],
            "s2p04": next(item for item in series if abs(item["s_m"] - 2.04) < 1e-9),
            "s3": next(item for item in series if abs(item["s_m"] - 3.0) < 1e-9),
            "s4": series[-1],
        }})

    # Restate the frame at the lightest system, across s = 2 to 4, thickness and sag following s.
    key, name, sigma, rho, crossply = next(c for c in CANDIDATES if c[0] == light["key"])
    band = []
    for s in s_values:
        t, m_film = film_mass(s, sigma, rho, crossply)
        charged = m_film + sag_pack(s)["lift_kg"]
        scored = score_s(s, charged)
        if scored is None:
            continue
        scored["film_kg"] = m_film
        scored["thickness_m"] = t
        band.append(scored)
    best_band = max(band, key=lambda item: item["SF_least_011b_force"])
    at_light_s = next(item for item in band if abs(item["s_m"] - light["s_m"]) < 1e-9)
    ended = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

    note = "unpublished-local-ref:f1ad809d1efc520a"
    data = open(note, "rb").read()
    pins = [{"path": note, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}]
    filed = os.path.join(ROOT, "film.py")
    data = open(filed, "rb").read()
    pins.append({"path": filed, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})

    results = {
        "schema": 1,
        "card": "MAINLINE-024-sag",
        "unit": "vacuum-mainline024-p3-film-1020",
        "questionable": True,
        "certification": False,
        "started_at": started,
        "ended_at": ended,
        "definition": {
            "curvature_radius_m": "s",
            "base_radius_m": "inradius s/(2*sqrt(3))",
            "crown": "s - sqrt(s^2 - inradius^2)",
            "mean": "cap volume over the inradius circle",
            "lift_kg": "L * 3 * mean / R",
            "vertex_sphere_not_charged": "base radius s/sqrt(3), shown and not used",
            "member_force": "011b N=p*R*s/2 is kept in the briefed factor. The note's N=p*R*s/(2*sqrt(3)) multiplies yield, Euler, local and Perry by sqrt(3). Global and film are unchanged.",
        },
        "note_checks": checks,
        "candidates": table,
        "lightest": light,
        "frame_at_lightest_s": at_light_s,
        "frame_best_in_2_to_4": best_band,
    }
    nfi = {
        "rows": [
            {"id": "NFI-SAG-INRADIUS", "note": "The charged sag uses the inradius as a circular base. The triangle is not that circle."},
            {"id": "NFI-SAG-VERTEX", "note": "A sphere through the three vertices rises about four times as far. It is not charged."},
            {"id": "NFI-SAG-MEAN", "note": "Mean sag is the spherical-cap mean over that circle. It is 0.5036 of the crown, which is why 3*crown/R is about twice the note's percent."},
            {"id": "NFI-MEMBER-FORCE", "note": "The note's equilateral force is smaller than 011b by sqrt(3). This filing does not replace the briefed global or film factor. Yield, Euler, local and Perry are reported both ways."},
            {"id": "NFI-BARRIER-MASS", "note": "The metallised layer still has no opened density. The sag kilograms are added to the film only."},
            {"id": "NFI-FILM-RESIZED", "note": "Thickness follows s, so the film factor is 1 at every bay in this table. The filed card had held the 2.04 m thickness."},
        ]
    }
    inputs = {"read_only": pins, "started_at": started, "ended_at": ended}

    def dump(name, obj):
        path = os.path.join(ROOT, name)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(obj, indent=1) + "\n")
        os.replace(tmp, path)

    dump("SAG-RESULTS.json", results)
    dump("SAG-NFI.json", nfi)
    dump("SAG-INPUTS.json", inputs)

    lines = []
    lines.append("# MAINLINE-024 — film sag and lift")
    lines.append("")
    lines.append("Unit vacuum-mainline024-p3-film-1020. QUESTIONABLE. Not a certification. The filed film card is not rewritten.")
    lines.append("")
    lines.append(
        "The note takes a sphere of radius s on a base equal to the triangle's inradius, s/(2*sqrt(3)). "
        "The crown is %s m at s 2.04 m and %s m at s 3 m, against the note's about 0.087 m and 0.13 m. "
        "s/24 is %s m and %s m."
        % (g(c204["crown_m"]), g(c3["crown_m"]), g(c204["s_over_24_m"]), g(c3["s_over_24_m"]))
    )
    lines.append(
        "The mean over that circle is %s of the crown. The lift lost is 3*mean/R: %s kg at 2.04 m and %s kg at 3 m, "
        "against the note's about 64 kg and 94 kg. At s 2 m the loss is %s kg. At s 4 m it is %s kg."
        % (
            g(c204["mean_m"] / c204["crown_m"]),
            g(c204["lift_kg"]),
            g(c3["lift_kg"]),
            g(checks[2]["lift_kg"]),
            g(checks[3]["lift_kg"]),
        )
    )
    lines.append(
        "A sphere through the vertices, which this note does not charge, crowns at %s m at s 2.04 m and would cost %s kg."
        % (g(c204["vertex_crown_m"]), g(c204["vertex_lift_kg"]))
    )
    lines.append("")
    lines.append("Thickness is resized with s, so the film factor is 1 at each bay. Sag over thickness uses the crown.")
    lines.append("")
    for block in table:
        a = block["at"]
        lines.append(
            "%s. At s 2 / 2.04 / 3 / 4 m the film is %s / %s / %s / %s kg, the sag is %s / %s / %s / %s times the thickness, "
            "and the film plus lift loss is %s / %s / %s / %s kg."
            % (
                block["name"],
                g(a["s2"]["film_kg"]), g(a["s2p04"]["film_kg"]), g(a["s3"]["film_kg"]), g(a["s4"]["film_kg"]),
                g(a["s2"]["sag_over_thickness"]), g(a["s2p04"]["sag_over_thickness"]),
                g(a["s3"]["sag_over_thickness"]), g(a["s4"]["sag_over_thickness"]),
                g(a["s2"]["system_kg"]), g(a["s2p04"]["system_kg"]), g(a["s3"]["system_kg"]), g(a["s4"]["system_kg"]),
            )
        )
    lines.append("")
    lines.append(
        "The lightest system in s 2 to 4 m is %s at s %s m: film %s kg plus lift loss %s kg, together %s kg. "
        "Crown over thickness is %s. The metallised layer's mass is still not computed. The total is above 97.515 kg."
        % (
            light["name"], g(light["s_m"]), g(light["film_kg"]), g(light["lift_kg"]),
            g(light["system_kg"]), g(light["sag_over_thickness"]),
        )
    )
    lines.append(
        "At that bay, with the film and the lift loss both charged, the briefed least factor is %s, governing %s. "
        "Global is %s. After the note's sqrt(3) on yield, Euler, local and Perry, the least is %s, governing %s. "
        "Across s 2 to 4 m the highest briefed factor is %s at s %s m."
        % (
            g(at_light_s["SF_least_011b_force"]),
            at_light_s["governing_011b_force"],
            g(at_light_s["SF_global"]),
            g(at_light_s["SF_least_note_force"]),
            at_light_s["governing_note_force"],
            g(best_band["SF_least_011b_force"]),
            g(best_band["s_m"]),
        )
    )
    lines.append("")
    lines.append("The member-force correction is not a new scan of 011b. Global and the film factor do not use that force.")
    lines.append("")
    text = "\n".join(lines) + "\n"
    path = os.path.join(ROOT, "SAG-CARD.md")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp, path)
    print("CROWN", g(c204["crown_m"]), g(c3["crown_m"]))
    print("LIFT", g(c204["lift_kg"]), g(c3["lift_kg"]), g(checks[2]["lift_kg"]), g(checks[3]["lift_kg"]))
    print("VERTEX", g(c204["vertex_crown_m"]), g(c204["vertex_lift_kg"]))
    print("LIGHT", light["key"], g(light["s_m"]), g(light["system_kg"]), g(light["film_kg"]), g(light["lift_kg"]), g(light["sag_over_thickness"]))
    print("SF", g(at_light_s["SF_least_011b_force"]), at_light_s["governing_011b_force"], g(at_light_s["SF_global"]))
    print("SFNOTE", g(at_light_s["SF_least_note_force"]), at_light_s["governing_note_force"])
    print("BEST", g(best_band["s_m"]), g(best_band["SF_least_011b_force"]), best_band["governing_011b_force"])
    print("DONE", ended)


if __name__ == "__main__":
    main()
