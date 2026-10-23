#!/usr/bin/env python3
"""MAINLINE-022b. Corrected frame equilibrium. Does not rewrite the 022 run."""
import datetime
import hashlib
import json
import math
import os
import time
from zoneinfo import ZoneInfo

import floatpoint as fp

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN_PATH = os.path.join(ROOT, "EQUILIBRIUM_ORIGIN.json")
OUT_PATH = os.path.join(ROOT, "EQUILIBRIUM.json")
CARD_PATH = os.path.join(ROOT, "EQUILIBRIUM.md")
ZONE = ZoneInfo("America/Los_Angeles")

NOTE = (
    "unpublished-local-ref:40621e2643eee247"
    "vacuum-overnight-briefs-1019/NOTE-P3-EQUILIBRIUM.md",
    "dc65f9c0d7585fbf3e57e3423fe48896a96425fd9f3abdcf49ce3b7cadaf7d8e",
    3618,
)
RESERVE_OPT = 411.2989440716474
RESERVE_5 = 0.05 * fp.L_MASS
SQRT3 = math.sqrt(3.0)
N_RO = 480


def g(x):
    return format(x, ".12g")


def sagitta(s):
    return fp.R - math.sqrt(fp.R * fp.R - (0.5 * s) ** 2)


def arc_length(s):
    """Great-circle arc between nodes. The chord is s."""
    theta = 2.0 * math.asin(min(1.0, (0.5 * s) / fp.R))
    return fp.R * theta


def sag_loss_kg(s):
    """Lift lost by a film crown of about s/24. Mean sag is half the crown."""
    return fp.L_MASS * s / (16.0 * fp.R)


def grid_counts(s, grid):
    if grid == "equilateral":
        nodes = fp.node_count(s)
        members = 3.0 * nodes - 6.0
        n_coef = fp.R * s / (2.0 * SQRT3)  # N = p * n_coef
        coeff = fp.C_TRI
    elif grid == "two_way":
        nodes = 4.0 * math.pi * fp.R * fp.R / (s * s) + 2.0
        members = 2.0 * nodes - 4.0
        n_coef = fp.R * s / 2.0
        coeff = fp.C_TWO
    else:
        raise ValueError(grid)
    return nodes, members, n_coef, coeff


def pack(s, t_f, rho_f, grid, base_reserve):
    nodes, members, n_coef, coeff = grid_counts(s, grid)
    m_nodes = fp.M_NODE * nodes
    m_film = 4.0 * math.pi * fp.R * fp.R * t_f * rho_f
    reserve = base_reserve + sag_loss_kg(s)
    vehicle = fp.L_MASS - reserve
    assembly = (vehicle - 100.0) / 1.05
    m_joint = (vehicle - 100.0) - assembly
    m_tube = assembly - m_film - m_nodes
    return {
        "nodes": nodes,
        "members": members,
        "n_coef": n_coef,
        "coeff": coeff,
        "m_nodes": m_nodes,
        "m_film": m_film,
        "m_joint": m_joint,
        "m_tube": m_tube,
        "reserve": reserve,
        "sag_kg": sag_loss_kg(s),
        "vehicle": vehicle,
    }


def t_grid(film, base_reserve):
    assembly = (fp.L_MASS - 100.0 - base_reserve) / 1.05
    t_hi = 0.75 * assembly / (4.0 * math.pi * fp.R * fp.R * film["rho"])
    t_lo = film["t_catalog_m"]
    if t_hi <= t_lo:
        return [t_lo]
    return [t_lo * (t_hi / t_lo) ** (i / 11.0) for i in range(12)]


def section_row(s, t_f, rho_f, grid, base_reserve, r_o, sigma, film_sigma):
    """One section. Rise is the sagitta, so the crown moment is zero."""
    info = pack(s, t_f, rho_f, grid, base_reserve)
    if info["m_tube"] <= 0.0 or info["members"] <= 0.0:
        return None
    length = arc_length(s)
    area = info["m_tube"] / (info["members"] * length * fp.RHO)
    if area <= 0.0 or r_o * r_o <= area / math.pi:
        return None
    r_i = math.sqrt(r_o * r_o - area / math.pi)
    t_w = r_o - r_i
    inertia = 0.25 * math.pi * (r_o ** 4 - r_i ** 4)
    n_force = fp.P_EXT * info["n_coef"]
    sf_y = (sigma * area / info["n_coef"]) / fp.P_EXT
    sf_e = (math.pi ** 2 * fp.E_MOD * inertia / (length ** 2) / info["n_coef"]) / fp.P_EXT
    sig_loc = fp.C_LOCAL * fp.E_MOD * t_w / r_o
    sf_l = (sig_loc * area / info["n_coef"]) / fp.P_EXT
    sf_f = (2.0 * film_sigma * t_f / s) / fp.P_EXT
    got = fp.perry(sigma, fp.E_MOD, length, r_o, inertia, area, n_force)
    if got is None:
        return None
    sf_p = got[0]
    sf_g = (0.2 * info["coeff"] * fp.E_MOD * math.sqrt(inertia * area) / (s * fp.R * fp.R)) / fp.P_EXT
    modes = {
        "yield": sf_y, "euler": sf_e, "local": sf_l, "film": sf_f, "perry": sf_p, "global": sf_g,
    }
    gov = min(modes, key=lambda name: (modes[name], name))
    row = dict(info)
    row.update({
        "s_m": s, "t_film_m": t_f, "r_o_m": r_o, "t_w_m": t_w, "rt": r_o / t_w,
        "A_m2": area, "I_m4": inertia, "length_m": length, "N_N": n_force,
        "sigma_axial_Pa": n_force / area, "SF_least": modes[gov], "governing": gov,
        "k": 0.2,
    })
    row.update({"SF_" + name: value for name, value in modes.items()})
    # k = 0.4 changes only the global mode.
    modes4 = dict(modes)
    modes4["global"] = 2.0 * sf_g
    gov4 = min(modes4, key=lambda name: (modes4[name], name))
    row["k04_SF_least"] = modes4[gov4]
    row["k04_governing"] = gov4
    row["k04_SF_global"] = modes4["global"]
    return row


def scan(film, sigma, base_reserve, s_values):
    best = {"equilateral": None, "two_way": None}
    ts = t_grid(film, base_reserve)
    for s in s_values:
        if s >= 2.0 * fp.R:
            continue
        for t_f in ts:
            for grid in ("equilateral", "two_way"):
                info = pack(s, t_f, film["rho"], grid, base_reserve)
                if info["m_tube"] <= 0.0:
                    continue
                length = arc_length(s)
                area = info["m_tube"] / (info["members"] * length * fp.RHO)
                r_min = math.sqrt(area / math.pi) * 1.0001
                r_max = min(0.25, s / 3.0)
                if r_max <= r_min:
                    continue
                span = r_max - r_min
                for i in range(N_RO):
                    r_o = r_min + span * (i / (N_RO - 1))
                    row = section_row(s, t_f, film["rho"], grid, base_reserve, r_o, sigma, film["sigma"])
                    if row is None:
                        continue
                    prev = best[grid]
                    if prev is None or row["SF_least"] > prev["SF_least"]:
                        best[grid] = row
    return best


def band():
    """Open past 3 m. Extend while the equilateral carried point sits on the top step."""
    top = 8.0
    values = None
    found = None
    film = fp.FILMS[1]
    while top <= 20.0:
        values = [round(0.40 + 0.05 * i, 3) for i in range(int(round((top - 0.40) / 0.05)) + 1)]
        found = scan(film, fp.SIG_CRUSH, RESERVE_5, values)
        s_best = found["equilateral"]["s_m"]
        print("band", top, "carried_s", s_best, "SF", g(found["equilateral"]["SF_least"]), found["equilateral"]["governing"])
        if s_best < top - 0.051:
            return values, found
        top += 4.0
    return values, found


def rebalance_fixed_mass():
    """Note's scaling: filed carried point, fixed tube mass, corrected N, retune r only."""
    s = 3.0
    # Filed 022 equilateral carried tube mass, 5 percent, no sag.
    m_tube = 4140.83666694
    nodes = fp.node_count(s)
    members = 3.0 * nodes - 6.0
    length = arc_length(s)
    area = m_tube / (members * length * fp.RHO)
    n_coef = fp.R * s / (2.0 * SQRT3)
    r_min = math.sqrt(area / math.pi) * 1.0001
    r_max = min(0.25, s / 3.0)
    best = None
    for i in range(4000):
        r_o = r_min + (r_max - r_min) * i / 3999.0
        r_i = math.sqrt(r_o * r_o - area / math.pi)
        t_w = r_o - r_i
        inertia = 0.25 * math.pi * (r_o ** 4 - r_i ** 4)
        sf_l = (fp.C_LOCAL * fp.E_MOD * t_w / r_o * area / n_coef) / fp.P_EXT
        sf_g = (0.2 * fp.C_TRI * fp.E_MOD * math.sqrt(inertia * area) / (s * fp.R * fp.R)) / fp.P_EXT
        least = min(sf_l, sf_g)
        if best is None or least > best[0]:
            best = (least, r_o, sf_l, sf_g)
    return {"SF": best[0], "r_o_m": best[1], "SF_local": best[2], "SF_global": best[3]}


def crown_example():
    """Note's rounded rise-8 geometry. N is the lattice value. Moment is N(h-sagitta)."""
    s, h, r_o, t_w = 1.1, 0.121, 0.1825, 0.000240
    h_sph = sagitta(s)
    r_i = r_o - t_w
    area = math.pi * (r_o * r_o - r_i * r_i)
    inertia = 0.25 * math.pi * (r_o ** 4 - r_i ** 4)
    n_force = fp.P_EXT * fp.R * s / (2.0 * SQRT3)
    moment = n_force * (h - h_sph)
    axial = n_force / area
    bending = moment * r_o / inertia
    return {
        "sagitta_m": h_sph,
        "N_N": n_force,
        "moment_Nm": moment,
        "sigma_axial_Pa": axial,
        "sigma_bending_Pa": bending,
        "yield_SF_before_bending": fp.SIG_FLEX / axial,
        "yield_SF_with_bending": fp.SIG_FLEX / (axial + bending),
    }


def check():
    path, sha, nbytes = NOTE
    data = open(path, "rb").read()
    got = hashlib.sha256(data).hexdigest()
    if got != sha or len(data) != nbytes:
        raise SystemExit("note pin drifted %s %s" % (got, len(data)))
    n_new = fp.P_EXT * fp.R * 2.04 / (2.0 * SQRT3)
    n_old = fp.P_EXT * fp.R * 2.04 / 2.0
    if abs(n_new / 1000.0 - 562.0) > 1.0:
        raise SystemExit("note N at 2.04 m is not 562 kN: %s" % n_new)
    if abs(n_old / 1000.0 - 974.0) > 1.0:
        raise SystemExit("old N at 2.04 m is not 974 kN: %s" % n_old)
    if abs(n_old / n_new - SQRT3) > 1e-12:
        raise SystemExit("force ratio is not sqrt(3)")
    crown = crown_example()
    if abs(crown["N_N"] / 1000.0 - 303.0) > 2.0:
        raise SystemExit("rise-8 N: %s" % crown["N_N"])
    if abs(crown["moment_Nm"] / 1000.0 - 32.0) > 1.0:
        raise SystemExit("rise-8 moment: %s" % crown["moment_Nm"])
    if abs(crown["sigma_axial_Pa"] / 1e9 - 1.10) > 0.03:
        raise SystemExit("rise-8 axial: %s" % crown["sigma_axial_Pa"])
    if abs(crown["sigma_bending_Pa"] / 1e9 - 1.28) > 0.05:
        raise SystemExit("rise-8 bending: %s" % crown["sigma_bending_Pa"])
    if abs(crown["yield_SF_before_bending"] - 0.34) > 0.02:
        raise SystemExit("rise-8 yield: %s" % crown["yield_SF_before_bending"])
    # s/24 against the spherical-cap sag over the triangle inradius.
    s = 2.04
    r_in = s / (2.0 * SQRT3)
    cap = s - math.sqrt(s * s - r_in * r_in)
    if abs(cap / (s / 24.0) - 1.0) > 0.05:
        raise SystemExit("sag is not s/24: %s" % cap)
    if abs(sag_loss_kg(2.04) - 64.0) > 4.0:
        raise SystemExit("sag mass at 2.04 m: %s" % sag_loss_kg(2.04))
    if abs((535.9459071525378 - 124.6469630808904) - RESERVE_OPT) > 1e-9:
        raise SystemExit("P3 reserve")
    nodes, members, _, _ = grid_counts(3.0, "two_way")
    if abs(members / nodes - 2.0) > 0.05:
        raise SystemExit("two-way count: %s / %s" % (members, nodes))
    print("checks pass", "N", g(n_new), "old", g(n_old), "sag2", g(sag_loss_kg(2.04)), "crownSF", g(crown["yield_SF_before_bending"]))
    return crown


S_BAND_MAX = None


def row_text(row):
    edge = ""
    if S_BAND_MAX is not None and row["s_m"] >= S_BAND_MAX - 0.051:
        edge += " s is on the open-band edge."
    if row["r_o_m"] >= 0.249:
        edge += " r_o is on the 0.25 m cap."
    return (
        "Least SF %s by %s. s %s m, r_o %s mm, wall %s mm, r/t %s, film %s mm. "
        "Yield %s, Euler %s, local %s, film %s, Perry %s, global %s. "
        "Tubes %s kg, nodes %s kg, joints %s kg, film %s kg, sag %s kg.%s"
        % (
            g(row["SF_least"]), row["governing"], g(row["s_m"]), g(row["r_o_m"] * 1e3),
            g(row["t_w_m"] * 1e3), g(row["rt"]), g(row["t_film_m"] * 1e3),
            g(row["SF_yield"]), g(row["SF_euler"]), g(row["SF_local"]), g(row["SF_film"]),
            g(row["SF_perry"]), g(row["SF_global"]), g(row["m_tube"]), g(row["m_nodes"]),
            g(row["m_joint"]), g(row["m_film"]), g(row["sag_kg"]), edge,
        )
    )


def main():
    if os.path.exists(OUT_PATH):
        raise SystemExit("EQUILIBRIUM.json is the measured 022b run. Not recomputing.")
    t0 = time.monotonic()
    crown = check()
    balance = rebalance_fixed_mass()
    print("rebalance", g(balance["SF"]), "local", g(balance["SF_local"]), "global", g(balance["SF_global"]))
    mono0 = time.monotonic()
    wall0 = datetime.datetime.now(ZONE)
    origin = {"origin_local": wall0.isoformat(timespec="microseconds"), "origin_monotonic_s": mono0}
    if os.path.exists(ORIGIN_PATH):
        origin = json.loads(open(ORIGIN_PATH, encoding="utf-8").read())
        print("EQUILIBRIUM_ORIGIN exists; not restamping")
    else:
        fp.atomic_write(ORIGIN_PATH, json.dumps(origin, indent=1) + "\n")
        print("EQUILIBRIUM_ORIGIN", origin["origin_local"])
    s_values, carried5 = band()
    film_proj = fp.FILMS[1]
    film_mylar = fp.FILMS[0]
    carried_opt = scan(film_proj, fp.SIG_CRUSH, RESERVE_OPT, s_values)
    mylar5 = scan(film_mylar, fp.SIG_FLEX, RESERVE_5, s_values)
    mylar_opt = scan(film_mylar, fp.SIG_FLEX, RESERVE_OPT, s_values)
    elapsed = time.monotonic() - t0
    ended = datetime.datetime.now(ZONE).isoformat(timespec="microseconds")

    def pack_row(row):
        keep = [k for k in row if k != "coeff"]
        return {k: row[k] for k in keep}

    cases = {
        "carried_5": {k: pack_row(v) for k, v in carried5.items()},
        "carried_optimistic": {k: pack_row(v) for k, v in carried_opt.items()},
        "mylar_380_5": {k: pack_row(v) for k, v in mylar5.items()},
        "mylar_380_optimistic": {k: pack_row(v) for k, v in mylar_opt.items()},
    }
    doc = {
        "schema": 1,
        "card": "MAINLINE-022b",
        "questionable": True,
        "origin_local": origin["origin_local"],
        "ended_local": ended,
        "elapsed_s": elapsed,
        "s_max_m": s_values[-1],
        "rise": "dropped. Node equilibrium fixes N. A rise above the sagitta adds a crown moment and is not a search variable.",
        "sag": "charged as L*s/(16*R), PENDING-024",
        "pending": ["PENDING-023", "PENDING-024", "PENDING-025"],
        "crown_example": crown,
        "fixed_mass_rebalance": balance,
        "cases": cases,
    }
    fp.atomic_write(OUT_PATH, json.dumps(doc, indent=1) + "\n")
    global S_BAND_MAX
    S_BAND_MAX = s_values[-1]
    c5 = carried5["equilateral"]
    lines = [
        "# MAINLINE-022b — corrected member force, rise dropped, band open",
        "",
        "QUESTIONABLE. This does not replace the measured 022 files. 023, 024 and 025 had not filed. Joints stay 5 percent (PENDING-023). The film material stays the carried 011b film or Mylar, and the sag formula is charged here and remains PENDING-024. The allowable stays the 3900 MPa crush or the 380 MPa bar (PENDING-025).",
        "",
        "The 022 code used N = pRs/2 on both grids. The note's equilateral force is pRs/(2√3). The ratio is √3. At s 2.04 m the note's force is %s N and the old force is %s N. Global buckling does not use N. On the filed carried geometry, local 1.242 times √3 is 2.15. Retuning radius at that fixed tube mass brings local and global together at SF %s. That is the note's rebalance, not the search below."
        % (g(fp.P_EXT * fp.R * 2.04 / (2.0 * SQRT3)), g(fp.P_EXT * fp.R * 2.04 / 2.0), g(balance["SF"])),
        "",
        "The rise is dropped. At the note's rounded rise-8 geometry the lattice force is %s N, the crown moment is %s N·m, the axial stress is %s GPa and the bending stress is %s GPa. Against 380 MPa the yield SF is %s before bending and %s with the crown moment. 022's rise lever had scored that point at 1.59 by cutting N. That cut is not equilibrium."
        % (g(crown["N_N"]), g(crown["moment_Nm"]), g(crown["sigma_axial_Pa"] / 1e9), g(crown["sigma_bending_Pa"] / 1e9), g(crown["yield_SF_before_bending"]), g(crown["yield_SF_with_bending"])),
        "",
        "A two-way grid has V = 4πR²/s²+2 and 2V−4 members. 022 used the triangulated 3V−6 count on both grids. The global coefficients are unchanged: 4√(3/2) equilateral and 4 two-way.",
        "",
        "Film sag is about s/24. The lift charged is L·s/(16R), added to the reserve. At s 2.04 m that is %s kg. 024 owns the film geometry."
        % g(sag_loss_kg(2.04)),
        "",
        "The spacing band runs from 0.40 m to %s m. A ceramic arc still takes k 0.2." % g(s_values[-1]),
        "",
        "## Carried film and crush, 5 percent, plus sag",
        "",
        "Equilateral, k 0.2. " + row_text(c5),
        "",
        "Two-way, k 0.2. " + row_text(carried5["two_way"]),
        "",
        "Equilateral k 0.4 at the same section: least SF %s by %s, global %s."
        % (g(c5["k04_SF_least"]), c5["k04_governing"], g(c5["k04_SF_global"])),
        "",
        "## Carried film and crush, 019 P3 reserve 411.298944072 kg, plus sag",
        "",
        "Equilateral, k 0.2. " + row_text(carried_opt["equilateral"]),
        "",
        "Two-way, k 0.2. " + row_text(carried_opt["two_way"]),
        "",
        "## Today: Mylar 850H and the 380 MPa bar, 5 percent, plus sag",
        "",
        "Equilateral, k 0.2. " + row_text(mylar5["equilateral"]),
        "",
        "Two-way, k 0.2. " + row_text(mylar5["two_way"]),
        "",
        "## Today, at the 019 P3 reserve, plus sag",
        "",
        "Equilateral, k 0.2. " + row_text(mylar_opt["equilateral"]),
        "",
        "Two-way, k 0.2. " + row_text(mylar_opt["two_way"]),
        "",
        "Elapsed time is a measurement. Nothing here is a certification.",
        "",
    ]
    fp.atomic_write(CARD_PATH, "\n".join(lines))
    print("elapsed", g(elapsed))
    for name, block in (
        ("C5", carried5), ("COPT", carried_opt), ("M5", mylar5), ("MOPT", mylar_opt),
    ):
        for grid in ("equilateral", "two_way"):
            row = block[grid]
            print(name, grid, g(row["SF_least"]), row["governing"], "s", g(row["s_m"]),
                  "ro", g(row["r_o_m"]), "tw", g(row["t_w_m"]), "tf", g(row["t_film_m"]),
                  "g", g(row["SF_global"]), "l", g(row["SF_local"]), "f", g(row["SF_film"]),
                  "y", g(row["SF_yield"]), "p", g(row["SF_perry"]))


if __name__ == "__main__":
    main()
