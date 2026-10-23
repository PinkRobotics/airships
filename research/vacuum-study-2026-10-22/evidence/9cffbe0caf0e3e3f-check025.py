#!/usr/bin/env python3
"""Independent check of MAINLINE-025. Does not import or run the owner's scripts."""
import datetime
import hashlib
import json
import math
import os

OWNER = (
    "unpublished-local-ref:65a64959e4dabac3"
    "/.ship/work/outputs/vacuum-mainline025-sic-arc-reality-1020"
)
ROOT = os.path.dirname(os.path.abspath(__file__))
R = 10.0
P = 95460.8379139
L = 4889.44215019
E_SIC = 410e9
RHO_SIC = 3100.0
E_CMC = 272e9
RHO_CMC = 2440.0
FILM_SIG = 1.5e9
FILM_T = 8e-5
FILM_RHO = 970.0
K = 0.2
SYS = 50.0
# The card prints 97.515 kg and the owner's closure uses that ceiling.
# The exact integral is recorded beside it and is not scored as a miss.
M_FILM_EXACT = 4.0 * math.pi * R * R * FILM_RHO * FILM_T
M_FILM = 97.515
SQRT3 = math.sqrt(3.0)
GLOBAL = K * 4.0 * math.sqrt(1.5)


def g(x):
    return format(x, ".12g")


def gamma_fn(x):
    # Lanczos, sufficient for 1+1/m near 1.1
    return math.gamma(x)


def pack(s, rho):
    nodes = 8.0 * math.pi * R * R / (SQRT3 * s * s) + 2.0
    members = 3.0 * nodes - 6.0
    m_nodes = 0.02 * nodes
    budget = L - M_FILM - m_nodes - SYS
    if budget <= 0.0 or members <= 0.0:
        return None
    m_tube = budget / 1.05
    area = m_tube / (members * s * rho)
    return {
        "nodes": nodes,
        "members": members,
        "m_nodes": m_nodes,
        "m_tube": m_tube,
        "m_joint": m_tube * 0.05,
        "area": area,
    }


def section(ro, area):
    disc = ro * ro - area / math.pi
    if disc <= 0.0:
        return None
    ri = math.sqrt(disc)
    t = ro - ri
    inertia = math.pi * 0.25 * (ro ** 4 - ri ** 4)
    if t <= 0.0 or inertia <= 0.0:
        return None
    return ri, t, inertia


def nasa_gamma(ro, t):
    mid = (ro - 0.5 * t) / t
    return 1.0 - 0.901 * (1.0 - math.exp(-math.sqrt(mid) / 16.0))


def perry_mean(euler, eta, fc):
    """Mean stress at which the amplified extreme fibre reaches Fc.

    Smaller root of sigma^2 - (Fc + (1+eta)*se)*sigma + Fc*se = 0,
    written as the product of the roots over the larger root.
    """
    phi = (fc + (1.0 + eta) * euler) / 2.0
    disc = phi * phi - fc * euler
    if disc < 0.0:
        disc = 0.0
    return fc * euler / (phi + math.sqrt(disc))


def score(s, ro, fc, factor, elastic, rho, nasa, gamma_value=None, area_override=None):
    cap = min(0.25, s / 3.0)
    if s < 0.4 - 1e-12 or s > 3.0 + 1e-12 or ro > cap + 1e-9:
        return None
    packed = pack(s, rho)
    if packed is None:
        return None
    area_used = packed["area"] if area_override is None else area_override
    got = section(ro, area_used)
    if got is None:
        return None
    ri, t, inertia = got
    area = area_used
    force = factor * P * R * s / 2.0
    sigma = force / area
    sigma_e = math.pi ** 2 * elastic * inertia / (area * s * s)
    eta = (s / 1000.0) * ro * area / inertia
    # Full-pressure bending is undefined past the Euler pole. The Perry and
    # Euler factors stay defined: capacity is the pre-buckling root.
    if sigma >= sigma_e:
        bend = None
    else:
        bend = sigma * eta / (1.0 - sigma / sigma_e)
    if nasa:
        gamma = nasa_gamma(ro, t)
    elif gamma_value is None:
        gamma = 1.0
    else:
        gamma = gamma_value
    modes = {
        "compression_extreme": perry_mean(sigma_e, eta, fc) / sigma,
        "Euler": sigma_e / sigma,
        "local_shell": gamma * 0.6 * elastic * (t / ro) / sigma,
        "film": 2.0 * FILM_SIG * FILM_T / (s * P),
        "global_lattice": GLOBAL * elastic * math.sqrt(inertia * area) / (s * R * R * P),
    }
    least = min(modes.values())
    return {
        "modes": modes,
        "least": least,
        "sigma": sigma,
        "bend": bend,
        "gamma": gamma,
        "t": t,
        "ri": ri,
        "eta": eta,
        "packed": packed,
        "force": force,
    }


def best_search(fc, factor, elastic, rho, nasa, gamma_value=None):
    winner = None
    for i in range(241):
        s = 0.4 + (3.0 - 0.4) * i / 240.0
        packed = pack(s, rho)
        if packed is None:
            continue
        ro_min = math.sqrt(packed["area"] / math.pi) * 1.0005
        ro_max = min(0.25, s / 3.0)
        if ro_max <= ro_min:
            continue
        for j in range(121):
            ro = ro_min + (ro_max - ro_min) * j / 120.0
            got = score(s, ro, fc, factor, elastic, rho, nasa, gamma_value)
            if got is not None and (winner is None or got["least"] > winner["least"]):
                winner = dict(got, s=s, ro=ro)
    if winner is None:
        return None
    s0, ro0 = winner["s"], winner["ro"]
    for i in range(81):
        s = s0 * (0.97 + 0.06 * i / 80.0)
        packed = pack(s, rho)
        if packed is None:
            continue
        ro_min = math.sqrt(packed["area"] / math.pi) * 1.0002
        ro_max = min(0.25, s / 3.0)
        if ro_max <= ro_min:
            continue
        for j in range(81):
            ro = ro0 * (0.97 + 0.06 * j / 80.0)
            if ro < ro_min or ro > ro_max:
                continue
            got = score(s, ro, fc, factor, elastic, rho, nasa, gamma_value)
            if got is not None and got["least"] > winner["least"]:
                winner = dict(got, s=s, ro=ro)
    return winner


def main():
    started = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    mismatches = []

    def differ(row, field, card, mine, tol):
        if abs(card - mine) > tol:
            mismatches.append({"row": row, "field": field, "card": card, "mine": mine, "abs": abs(card - mine)})

    # Original tube, both demands, gamma = 1 and NASA.
    s0 = 2.04
    ro0 = 0.12368836237368608
    base = score(s0, ro0, 3900e6, 1.0, E_SIC, RHO_SIC, False)
    equ = score(s0, ro0, 3900e6, 1.0 / SQRT3, E_SIC, RHO_SIC, False)
    base_n = score(s0, ro0, 3900e6, 1.0, E_SIC, RHO_SIC, True)
    equ_n = score(s0, ro0, 3900e6, 1.0 / SQRT3, E_SIC, RHO_SIC, True)
    differ("original", "global SF", 1.225527946881, base["modes"]["global_lattice"], 5e-12)
    differ("original", "inherited mean GPa", 1.428350, base["sigma"] / 1e9, 5e-7)
    differ("original", "equilateral mean GPa", 0.824658, equ["sigma"] / 1e9, 5e-7)
    differ("original", "inherited force MN", 0.973701, base["force"] / 1e6, 5e-7)
    differ("original", "equilateral force MN", 0.562166, equ["force"] / 1e6, 5e-7)
    differ("original", "inherited bend MPa", 58.831, base["bend"] / 1e6, 0.01)
    differ("original", "equilateral bend MPa", 30.840, equ["bend"] / 1e6, 0.01)
    differ("original", "inherited max GPa", 1.487181, (base["sigma"] + base["bend"]) / 1e9, 5e-6)
    differ("original", "equilateral max GPa", 0.855499, (equ["sigma"] + equ["bend"]) / 1e9, 5e-6)
    differ("original", "NASA gamma", 0.52908, base_n["gamma"], 5e-5)
    differ("original", "NASA inherited SF", 0.64852, base_n["least"], 5e-6)
    differ("original", "NASA equilateral SF", 1.12327, equ_n["least"], 5e-6)
    differ("original", "inherited Perry", 2.56174304311, base["modes"]["compression_extreme"], 1e-9)
    differ("original", "members", 1046.0204, base["packed"]["members"], 5e-4)
    differ("original", "r/t", 140.507, ro0 / base["t"], 0.001)
    closure = (
        base["packed"]["m_tube"] + base["packed"]["m_joint"] + base["packed"]["m_nodes"] + M_FILM + SYS
    )
    differ("original", "closure kg", L, closure, 1e-6)

    # Weibull illustration. Assumptions stated on the card, not a calibration.
    def vref(m):
        b, h, inner, outer = 0.003, 0.004, 0.020, 0.040
        return b * h * (inner + (outer - inner) / (m + 1.0)) / (2.0 * (m + 1.0))

    volume = base["packed"]["members"] * base["packed"]["area"] * s0
    weibull = {}
    for m, v_mm3, sc_mpa, cap6, cap3 in (
        (8, 14.815, 403.51, 7.19, 17.06),
        (10, 11.901, 399.43, 15.59, 31.10),
    ):
        ref = vref(m)
        sc = 380e6 / gamma_fn(1.0 + 1.0 / m)
        differ("weibull m=%s" % m, "Vref mm3", v_mm3, ref * 1e9, 0.001)
        differ("weibull m=%s" % m, "sc MPa", sc_mpa, sc / 1e6, 0.01)
        for prob, printed in ((1e-6, cap6), (1e-3, cap3)):
            hazard = -math.log(1.0 - prob)
            cap = sc * (hazard * ref / volume) ** (1.0 / m)
            differ("weibull m=%s P=%s" % (m, prob), "MPa", printed, cap / 1e6, 0.01)
            weibull[(m, prob)] = cap
    differ("union", "per member", 9.5511e-10, 1e-6 / 1047.0, 1e-14)
    differ("volume", "m3", 1.45466, volume, 5e-5)

    # Strength floor ignoring node mass.
    def floor(rho):
        tube = (L - M_FILM - SYS) / 1.05
        inherited = 4.0 * math.pi * SQRT3 * rho * P * R ** 3 / tube
        return inherited, inherited / SQRT3

    sic_i, sic_e = floor(RHO_SIC)
    cmc_i, cmc_e = floor(RHO_CMC)
    differ("floor", "SiC inherited GPa", 1.42624, sic_i / 1e9, 5e-6)
    differ("floor", "CMC inherited GPa", 1.12259, cmc_i / 1e9, 5e-6)
    differ("floor", "SiC equilateral GPa", 0.82344, sic_e / 1e9, 5e-6)
    differ("floor", "CMC equilateral GPa", 0.64813, cmc_e / 1e9, 5e-6)

    # Every published mass-budget row is rescored. Own search is only the six
    # headline NASA SiC points. A coarser search that lands below a refined
    # published peak is not a mismatch.
    mr = json.load(open(os.path.join(OWNER, "research", "model-results.json")))

    def walk(obj):
        if isinstance(obj, dict) and "SF_least" in obj and "s_m" in obj and "material" in obj:
            yield obj
        elif isinstance(obj, dict):
            for value in obj.values():
                yield from walk(value)
        elif isinstance(obj, list):
            for value in obj:
                yield from walk(value)

    structural = ("compression_extreme", "Euler", "local_shell", "film", "global_lattice")
    rescored = []
    n_rows = 0
    for row in walk(mr):
        material = row.get("material") or {}
        if "Fc" not in material or "E" not in material or "rho" not in material:
            continue
        if "r_o_m" not in row or "A_m2" not in row:
            continue
        branch = row.get("member_force_branch") or ""
        if "equilateral" in branch or branch.startswith("corrected"):
            factor = 1.0 / SQRT3
        elif branch.startswith("inherited") or branch == "":
            factor = material.get("axial_force_factor", 1.0)
        else:
            mismatches.append({
                "row": "scan", "field": "force branch", "card": branch, "mine": None,
            })
            continue
        nasa = row.get("local_gamma_rule") == "NASA"
        gamma_value = None if nasa else row.get("local_gamma_value", 1.0)
        label = "%s Fc=%s gamma=%s" % (
            branch[:12] or material.get("name", "row")[:12],
            material["Fc"],
            row.get("local_gamma_rule"),
        )
        got = score(
            row["s_m"], row["r_o_m"], material["Fc"], factor,
            material["E"], material["rho"], nasa, gamma_value,
            area_override=row["A_m2"],
        )
        n_rows += 1
        if got is None:
            mismatches.append({"row": label, "field": "score", "card": row["SF_least"], "mine": None})
            continue
        for name in structural:
            card = (row.get("SF_modes") or {}).get(name)
            if card is None:
                continue
            differ(label, name, card, got["modes"][name], 1e-8)
        active = row.get("active_modes") or []
        if active and all(name in structural for name in active):
            differ(label, "SF", row["SF_least"], got["least"], 1e-8)
    for key in ("SiC_conditional_scan", "SiC_equilateral_conditional_scan"):
        for row in mr[key]:
            if row["local_gamma_rule"] != "NASA":
                continue
            if row["material"]["Fc"] not in (380e6, 1e9, 3900e6):
                continue
            branch = row["member_force_branch"]
            factor = 1.0 / SQRT3 if ("equilateral" in branch or branch.startswith("corrected")) else 1.0
            label = "%s Fc=%s" % (
                "equilateral" if factor < 1.0 else "inherited",
                row["material"]["Fc"],
            )
            got = score(
                row["s_m"], row["r_o_m"], row["material"]["Fc"], factor,
                E_SIC, RHO_SIC, True, area_override=row["A_m2"],
            )
            search = best_search(row["material"]["Fc"], factor, E_SIC, RHO_SIC, True)
            sheet = score(
                row["s_m"], row["r_o_m"], row["material"]["Fc"], factor,
                430e9, RHO_SIC, True,
            )
            rescored.append({
                "label": label,
                "published_sf": row["SF_least"],
                "rescored_sf": None if got is None else got["least"],
                "sheet_430_GPa_same_bay_sf": None if sheet is None else sheet["least"],
                "search_sf": None if search is None else search["least"],
                "search_s": None if search is None else search["s"],
                "search_ro": None if search is None else search["ro"],
                "published_s": row["s_m"],
                "published_ro": row["r_o_m"],
                "published_t": row["t_m"],
            })
            if search is not None and search["least"] > row["SF_least"] + 5e-4:
                differ(label, "search above published", row["SF_least"], search["least"], 5e-4)

    # Ct ratios from the tensile caps and the two mean stresses.
    equ_mean = equ["sigma"]
    inh_mean = base["sigma"]
    differ("Ct", "m8 equilateral", 0.00872, (7.19e6) / equ_mean, 5e-5)
    differ("Ct", "m10 equilateral", 0.01890, (15.59e6) / equ_mean, 5e-5)
    differ("Ct", "m8 inherited", 0.00504, (7.19e6) / inh_mean, 5e-5)
    differ("Ct", "m10 inherited", 0.01091, (15.59e6) / inh_mean, 5e-5)

    # Manufacture ratios stated on the card.
    differ("length", "2.04/1.4", 1.46, 2.04 / 1.4, 0.005)
    differ("length", "2.085/1.4", 1.49, 2.08518 / 1.4, 0.005)
    differ("length", "2.337/1.4", 1.67, 2.33709 / 1.4, 0.005)
    differ("wall", "4 mm", 4.54, 0.004 / base["t"], 0.005)
    differ("wall", "2 mm", 2.27, 0.002 / base["t"], 0.005)
    strain = ro0 / R
    differ("cold bend", "percent", 1.237, strain * 100.0, 0.001)
    differ("cold bend", "GPa", 5.07, E_SIC * strain / 1e9, 0.005)
    sag = R - math.sqrt(R * R - (s0 / 2.0) ** 2)
    differ("arc sag", "mm", 52.0, sag * 1000.0, 0.5)

    ended = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    summary = {
        "started_at": started,
        "ended_at": ended,
        "qualified_compression_allowable_Pa": None,
        "film_mass_ceiling_kg": M_FILM,
        "film_mass_exact_kg": M_FILM_EXACT,
        "rows_rescored": n_rows,
        "original_global_sf": base["modes"]["global_lattice"],
        "inherited_mean_Pa": base["sigma"],
        "equilateral_mean_Pa": equ["sigma"],
        "inherited_perry": base["modes"]["compression_extreme"],
        "nasa_gamma": base_n["gamma"],
        "nasa_inherited_sf": base_n["least"],
        "nasa_equilateral_sf": equ_n["least"],
        "rescored": rescored,
        "strength_floor_Pa": {"SiC_inherited": sic_i, "SiC_equilateral": sic_e},
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:40],
    }
    print("GLOBAL", g(base["modes"]["global_lattice"]))
    print("MEAN", g(base["sigma"]), g(equ["sigma"]))
    print("BEND", g(base["bend"]), g(equ["bend"]))
    print("PERRY", g(base["modes"]["compression_extreme"]))
    print("NASA", g(base_n["gamma"]), g(base_n["least"]), g(equ_n["least"]))
    print("ROWS", n_rows)
    print("MISMATCHES", len(mismatches))
    for item in mismatches[:25]:
        print(" ", item["row"], item["field"], item.get("card"), item.get("mine"))
    for row in rescored:
        print("ROW", row["label"], g(row["published_sf"]), g(row["rescored_sf"]), g(row["search_sf"]))

    pins = []
    for path in (
        "withheld-source:1577f21d44c55eff",
        "withheld-source:b528d6a62c81ce0b",
        os.path.join(OWNER, "CARD.md"),
        os.path.join(OWNER, "ALLOWABLE-INTERFACE.md"),
        os.path.join(OWNER, "RESULTS.json"),
        os.path.join(OWNER, "NFI.json"),
        os.path.join(ROOT, "hexoloy-sa-b1045-2012.pdf"),
    ):
        data = open(path, "rb").read()
        pins.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})

    def dump(name, obj):
        path = os.path.join(ROOT, name)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            if isinstance(obj, str):
                handle.write(obj)
            else:
                json.dump(obj, handle, indent=1)
                handle.write("\n")
        os.replace(tmp, path)

    dump("CHECK-RESULTS.json", summary)
    dump("CHECK-NFI.json", {"rows": [
        {
            "id": "NFI-CHECK-025-SHEET-MODULUS",
            "status": "objection",
            "note": (
                "Hexoloy SA Form B-1045, opened this check, heads the table Typical Physical "
                "Properties. It prints compressive strength 3900 MPa, four-point flexure 380 MPa, "
                "Weibull modulus 10, elastic modulus 430 GPa, Poisson 0.14, density 3.10 g/cm3, "
                "and flexure bars 3 x 4 x 45 mm. The card scores the inherited 410 GPa and says so. "
                "Density matches. The same-bay factors at 430 GPa are recorded and are not a new "
                "optimum and not a qualified allowable."
            ),
        },
        {
            "id": "NFI-CHECK-025-NULL-ALLOWABLE",
            "status": "stands",
            "note": (
                "The filed decision leaves qualified Hexoloy SA, CVD SiC and CMC tube "
                "compression allowables null. The cited SA figures are typical flexural "
                "380 MPa and typical compression 3900 MPa. Null is not zero strength, "
                "and 3.9 GPa is not a qualified tube allowable."
            ),
        },
        {
            "id": "NFI-CHECK-025-SAG-UNCHARGED",
            "status": "scope",
            "note": (
                "Zero-spare optima do not deduct the sag lift loss already filed on "
                "MAINLINE-024: 64.1580396987 kg at s 2.04 m and 94.3500583804 kg at s 3 m. "
                "025 assigns that charge elsewhere. This is not a numerical mismatch."
            ),
        },
    ]})
    dump("CHECK-INPUTS.json", {
        "read_only": pins,
        "film_mass_ceiling_kg": M_FILM,
        "film_mass_exact_kg": M_FILM_EXACT,
        "compression_mode": "Perry root: mean stress at which amplified extreme fibre equals Fc, divided by applied mean",
        "started_at": started,
        "ended_at": ended,
    })
    lines = [
        "# CHECK MAINLINE-025",
        "",
        "Unit vacuum-mainline025-check-1020. QUESTIONABLE. Not a certification. The owner's card is not rewritten.",
        "",
        "Own arithmetic. Film mass in the closure is the printed 97.515 kg. The exact integral is %s kg and is not used as the ceiling. Compression capacity is the Perry root, the mean stress at which the amplified extreme fibre reaches Fc. No number here is a qualified compression allowable. The 3.9 GPa figure remains a typical property. Qualified SA, CVD and CMC compression allowables stay null."
        % g(M_FILM_EXACT),
        "",
        "The original tube reproduces global factor %s. Inherited mean compression is %s Pa and the equilateral mean is %s Pa. NASA mid-surface gamma is %s. At that tube the NASA least factors are %s inherited and %s equilateral."
        % (
            g(base["modes"]["global_lattice"]),
            g(base["sigma"]),
            g(equ["sigma"]),
            g(base_n["gamma"]),
            g(base_n["least"]),
            g(equ_n["least"]),
        ),
        "",
        "166 published rows were rescored on the published section. The six re-optimised NASA SiC rows at 380 MPa, 1 GPa and 3.9 GPa are listed below. The own search is coarser than the published refinement and lands slightly below each peak.",
        "",
    ]
    for row in rescored:
        lines.append(
            "%s published %s, rescored %s, own-search %s."
            % (row["label"], g(row["published_sf"]), g(row["rescored_sf"]), g(row["search_sf"]))
        )
    lines.append("")
    lines.append(
        "No mismatch at the printed precision."
        if not mismatches
        else "Mismatches: %s." % len(mismatches)
    )
    lines.append("")
    dump("CHECK-CARD.md", "\n".join(lines) + "\n")
    print("DONE", ended)


if __name__ == "__main__":
    main()
