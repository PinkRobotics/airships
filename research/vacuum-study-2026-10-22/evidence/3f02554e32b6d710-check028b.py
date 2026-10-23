#!/usr/bin/env python3
"""Independent check of MAINLINE-028b. Does not import or run the owner's scripts."""
import datetime
import hashlib
import json
import math
import os

OWNER = (
    "unpublished-local-ref:5c0646e1ee1e5966"
    "/.ship/work/outputs/vacuum-mainline028b-joining-into-021b-1020"
)
ROOT = os.path.dirname(os.path.abspath(__file__))
R = 10.0
P = 95460.83791390515
LIFT = 4889.442150186961
RESERVE = 411.2989440716474
SYSTEMS = 100.0
RHO_F = 1850.0
E = 290e9
E_LOT = 293.6e9
NU = 0.0752
FACE_TODAY = 345e6
FACE_FULL = 379.2e6
FACE_255 = 255e6
A = 4.0 * math.pi * R * R
H_BUDGET = LIFT - SYSTEMS - RESERVE
AF_AREAL = 0.015 * 0.45359237 / 0.09290304
LAB_AREAL = 0.008
SUBSETS = (
    (),
    ("O1_gamma",),
    ("O2_wrinkle",),
    ("O3_SR200_face_strength",),
    ("O1_gamma", "O2_wrinkle"),
    ("O1_gamma", "O3_SR200_face_strength"),
    ("O2_wrinkle", "O3_SR200_face_strength"),
    ("O1_gamma", "O2_wrinkle", "O3_SR200_face_strength"),
)


def g(x):
    return format(x, ".12g")


def bx_root():
    b = 0.7
    for _ in range(30):
        b -= (b * b * b + b - 1.0) / (3.0 * b * b + 1.0)
    return b


BX = bx_root()


def log_usage(required, today, full):
    if required <= today * (1.0 + 1e-12):
        return 0.0
    if full <= today * (1.0 + 1e-15):
        return math.inf
    return math.log(required / today) / math.log(full / today)


def load_cores():
    doc = json.load(open(os.path.join(OWNER, "intake", "014b_inputs.json")))
    found = []

    def walk(obj):
        if isinstance(obj, list) and obj and isinstance(obj[0], dict) and "Ec_Pa" in obj[0]:
            found.append(obj)
        elif isinstance(obj, dict):
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)

    walk(doc)
    cores = [core for core in max(found, key=len) if core.get("form") == "honeycomb"]
    if len(cores) != 47:
        raise SystemExit("expected 47 honeycomb cores, found %s" % len(cores))
    return cores


def joining(tf, tc, bond, primer, scarf):
    if scarf:
        gap_a = 0.6096 - 30.0 * tf
        gap_b = 1.8288 - 30.0 * tf
        if gap_a <= 1e-9 or gap_b <= 1e-9:
            return None
        length = A * (1.0 / gap_a + 1.0 / gap_b)
        film_per_m = 2.0 * tf * math.sqrt(901.0) * 0.070
    else:
        length = A * (1.0 / 0.6096 + 1.0 / 1.8288)
        film_per_m = 0.0
    splice_per_m = 0.0005 * tc * 500.0
    seal_per_m = 0.002
    physical = 2.0 * A * (bond + primer) + length * (film_per_m + splice_per_m + seal_per_m)
    return {
        "physical": physical,
        "length": length,
        "bond": 2.0 * A * bond,
        "primer": 2.0 * A * primer,
        "scarf_film": length * film_per_m,
        "splice": length * splice_per_m,
        "seal": length * seal_per_m,
    }


def solve_mass(fraction, rho_c, bond, primer, scarf):
    def at(structural):
        tf = (1.0 - fraction) * structural / (2.0 * A * RHO_F)
        tc = fraction * structural / (A * rho_c)
        if tf <= 0.0 or tc <= 0.0:
            return None
        bill = joining(tf, tc, bond, primer, scarf)
        if bill is None:
            return None
        return tf, tc, bill

    trial = H_BUDGET / 1.05
    got = at(trial)
    if got is None:
        return None
    if got[2]["physical"] <= 0.05 * trial + 1e-8:
        structural = trial
    else:
        lo, hi = 1e-6, trial
        structural = None
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            mid_got = at(mid)
            if mid_got is None or mid + mid_got[2]["physical"] > H_BUDGET:
                hi = mid
            else:
                lo = mid
                structural = mid
        if structural is None:
            return None
    tf, tc, bill = at(structural)
    allowance = 0.05 * structural
    charged = max(allowance, bill["physical"])
    total = structural + charged + SYSTEMS + RESERVE
    return {
        "tf": tf,
        "tc": tc,
        "structural": structural,
        "faces": (1.0 - fraction) * structural,
        "core": fraction * structural,
        "bill": bill,
        "allowance": allowance,
        "charged": charged,
        "excess": max(0.0, bill["physical"] - allowance),
        "total": total,
    }


def section_state(tf, tc, elastic, nu, core):
    h = tf + tc
    stress = P * R / (4.0 * tf)
    sigma0 = elastic * h / (R * math.sqrt(1.0 - nu * nu))
    sigma_crimp = h * h * core["Gc_Pa"] / (2.0 * tf * tc)
    vc = sigma0 / sigma_crimp
    kc = (1.0 - vc / 4.0) if vc <= 2.0 else (1.0 / vc)
    gamma_today = 0.2 if vc < 2.0 else 1.0
    gamma_full = 0.2 + 0.4 * min(vc, 2.0)
    root = math.sqrt(elastic * core["Ec_Pa"] * tf / tc)
    return {
        "stress": stress,
        "sigma0": sigma0,
        "sigma_crimp": sigma_crimp,
        "Vc": vc,
        "Kc": kc,
        "gamma_today": gamma_today,
        "gamma_full": gamma_full,
        "wrinkle_unit": BX * root,
        "crush": core["crush_Pa"] / (P / 2.0),
        "dimple_unit": elastic * (tf / core["s_cell_m"]) ** 2 / ((1.0 - nu * nu) * stress),
        "crimp": sigma_crimp / stress,
        "scarf": (10e6 * 901.0) / (stress * 30.0),
    }


def modes_at(state, gamma, k, face):
    stress = state["stress"]
    return {
        "global_buckling": gamma * state["Kc"] * state["sigma0"] / stress,
        "face_compression": face / stress,
        "core_shear_crimping": state["crimp"],
        "core_crush": state["crush"],
        "face_wrinkling": k * state["wrinkle_unit"] / stress,
        "intracell_dimpling": state["dimple_unit"],
    }


def subset_usage(state, subset, enforce_scarf, face_today, face_full):
    if state["crimp"] < 1.0 - 1e-8 or state["crush"] < 1.0 - 1e-8 or state["dimple_unit"] < 1.0 - 1e-8:
        return None
    if enforce_scarf and state["scarf"] < 1.0 - 1e-8:
        return None
    required = {
        "O1_gamma": (state["stress"] / (state["Kc"] * state["sigma0"]), state["gamma_today"], state["gamma_full"]),
        "O2_wrinkle": (state["stress"] / state["wrinkle_unit"], 0.33, 0.82),
        "O3_SR200_face_strength": (state["stress"], face_today, face_full),
    }
    held = []
    for name, (req, today, full) in required.items():
        usage = log_usage(req, today, full)
        if name not in subset:
            if usage > 1e-7:
                return None
        else:
            held.append(usage)
    if any(math.isinf(item) for item in held):
        return None
    return max(held) if held else 0.0


def least_screen(modes, scarf, weld, enforce):
    values = list(modes.values())
    if enforce and scarf:
        values.append(scarf)
    if weld:
        values.append(modes["face_compression"])
    return min(values)


def main():
    started = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    mismatches = []

    def differ(row, field, card, mine, tol):
        if mine is None or abs(card - mine) > tol:
            mismatches.append({
                "row": row, "field": field, "card": card, "mine": mine,
                "abs": None if mine is None else abs(card - mine),
            })

    cores = load_cores()
    by_name = {core["name"]: core for core in cores}
    lead = by_name["Hexcel CR-III 5056 3/8-1.0"]
    checks = json.load(open(os.path.join(OWNER, "PROPERTY-CHECKS.json")))
    results = json.load(open(os.path.join(OWNER, "RESULTS.json")))

    # Reserve parts named on the method page.
    parts = 125.663706 + 5.0 + 213.036427 + 18.704390 + 48.894422
    differ("reserve", "named parts kg", RESERVE, parts, 0.00001)

    # 255 MPa upper bound: entire structural budget in the faces, zero core.
    structural_cap = H_BUDGET / 1.05
    tf_cap = structural_cap / (2.0 * A * RHO_F)
    face_sf_cap = FACE_255 / (P * R / (4.0 * tf_cap))
    differ("255", "zero-core face SF", 0.9582172954756751, face_sf_cap, 1e-12)
    bound_note = {"zero_core_tf_m": tf_cap, "zero_core_face_SF": face_sf_cap, "structural_cap_kg": structural_cap}

    rescored = []
    for blob, nu in ((checks, NU), (results, 0.33)):
        for row in blob["searches"]:
            if abs(row["nu"] - nu) > 1e-12 or "floating_point" not in row:
                continue
            point = row["floating_point"]
            core = by_name[point["core"]["name"]]
            enforce = row["joint_screen_enforced"]
            scarf = point["at_needed"]["projected_seam_mode"] == "scarf_mean_shear"
            bond = point["joining"]["bond_kg"] / (2.0 * A)
            primer = point["joining"]["primer_kg"] / (2.0 * A)
            label = "%s nu=%s seam=%s" % (row["route"], nu, enforce)
            solved = solve_mass(point["fraction"], core["rho"], bond, primer, scarf)
            if solved is None:
                mismatches.append({"row": label, "field": "mass solve", "card": point["tf_m"], "mine": None})
                continue
            differ(label, "tf m", point["tf_m"], solved["tf"], 1e-12)
            differ(label, "tc m", point["tc_m"], solved["tc"], 1e-12)
            differ(label, "charged total kg", point["masses_kg"]["charged_total"], solved["total"], 1e-8)
            differ(label, "physical joining kg", point["joining"]["physical_total_kg"], solved["bill"]["physical"], 1e-8)
            differ(label, "bond kg", point["joining"]["bond_kg"], solved["bill"]["bond"], 1e-8)
            differ(label, "primer kg", point["joining"]["primer_kg"], solved["bill"]["primer"], 1e-8)
            differ(label, "scarf film kg", point["joining"]["scarf_film_kg"], solved["bill"]["scarf_film"], 1e-8)
            differ(label, "splice kg", point["joining"]["core_splice_kg"], solved["bill"]["splice"], 1e-8)
            differ(label, "seal kg", point["joining"]["seal_kg"], solved["bill"]["seal"], 1e-8)
            state = section_state(solved["tf"], solved["tc"], E, nu, core)
            differ(label, "Vc", point["Vc"], state["Vc"], 1e-9)
            needed = modes_at(state, point["needed"]["gamma"], point["needed"]["wrinkle"], FACE_TODAY)
            published = point["at_needed"]["six_modes"]
            for name, value in needed.items():
                differ(label, "needed " + name, published[name], value, 1e-9)
            seam = state["scarf"] if scarf else needed["face_compression"]
            differ(label, "needed seam", point["at_needed"]["projected_seam_SF"], seam, 1e-9)
            differ(label, "gamma usage", point["log_usage"]["O1_gamma"], log_usage(
                point["needed"]["gamma"], state["gamma_today"], state["gamma_full"]
            ), 1e-9)
            differ(label, "wrinkle usage", point["log_usage"]["O2_wrinkle"], log_usage(
                point["needed"]["wrinkle"], 0.33, 0.82
            ), 1e-9)
            full_modes = modes_at(state, state["gamma_full"], 0.82, FACE_FULL)
            # Full-endpoint column on the selected bay uses the lot modulus.
            state_lot = section_state(solved["tf"], solved["tc"], E_LOT, nu, core)
            lot_modes = modes_at(state_lot, state_lot["gamma_full"], 0.82, FACE_FULL)
            gamma_held = modes_at(state_lot, 0.2, 0.82, FACE_FULL)
            differ(label, "full gamma SF", point["at_full_named"]["six_modes"]["global_buckling"], lot_modes["global_buckling"], 1e-8)
            differ(label, "gamma 0.2 least", point["at_full_but_gamma_02"]["least_seven_screen_SF"], min(
                list(gamma_held.values()) + ([state_lot["scarf"]] if scarf else [gamma_held["face_compression"]])
            ), 1e-8)
            rescored.append({
                "label": label,
                "route": row["route"],
                "nu": nu,
                "seam_enforced": enforce,
                "usage": point["log_usage"]["O1_gamma"],
                "mine_usage": log_usage(point["needed"]["gamma"], state["gamma_today"], state["gamma_full"]),
                "least_needed": min(needed.values()),
                "seam": seam,
            })

    for row in checks["full_named_maxima"]:
        point = row["point"]
        core = by_name[point["core"]["name"]]
        scarf = point["at_full_named"]["projected_seam_mode"] == "scarf_mean_shear"
        bond = point["joining"]["bond_kg"] / (2.0 * A)
        primer = point["joining"]["primer_kg"] / (2.0 * A)
        solved = solve_mass(row["fraction"], core["rho"], bond, primer, scarf)
        label = "full %s %s" % (row["route"], row["material"])
        if solved is None:
            mismatches.append({"row": label, "field": "mass solve", "card": point["tf_m"], "mine": None})
            continue
        differ(label, "tf m", point["tf_m"], solved["tf"], 1e-12)
        if row["material"] == "SR200":
            state = section_state(solved["tf"], solved["tc"], E_LOT, NU, core)
            modes = modes_at(state, state["gamma_full"], 0.82, FACE_FULL)
            seam = state["scarf"] if scarf else modes["face_compression"]
        else:
            state = section_state(solved["tf"], solved["tc"], E, NU, core)
            modes = modes_at(state, state["gamma_full"], 0.82, FACE_255)
            seam = state["scarf"] if scarf else modes["face_compression"]
        published = point["at_full_named"]["six_modes"]
        for name, value in modes.items():
            differ(label, name, published[name], value, 1e-8)
        differ(label, "seam", point["at_full_named"]["projected_seam_SF"], seam, 1e-8)
        differ(label, "least", row["least_SF"], min(list(modes.values()) + [seam]), 1e-8)

    # Own search. Geometry does not depend on the subset, so each fraction is solved once.
    search_rows = []
    fractions = [0.004 + (0.96 - 0.004) * i / 1600.0 for i in range(1601)]
    for row in checks["searches"]:
        if abs(row["nu"] - NU) > 1e-12 or not row["joint_screen_enforced"]:
            continue
        point = row["floating_point"]
        scarf = point["at_needed"]["projected_seam_mode"] == "scarf_mean_shear"
        bond = point["joining"]["bond_kg"] / (2.0 * A)
        primer = point["joining"]["primer_kg"] / (2.0 * A)
        best = {subset: None for subset in SUBSETS}
        for core in cores:
            for fraction in fractions:
                solved = solve_mass(fraction, core["rho"], bond, primer, scarf)
                if solved is None:
                    continue
                state = section_state(solved["tf"], solved["tc"], E, NU, core)
                for subset in SUBSETS:
                    usage = subset_usage(state, subset, scarf, FACE_TODAY, FACE_FULL)
                    if usage is None:
                        continue
                    current = best[subset]
                    if current is None or usage < current["usage"]:
                        best[subset] = {"usage": usage, "core": core["name"], "fraction": fraction}
        for subset in SUBSETS:
            published = next(item for item in row["subsets"] if tuple(item["subset"]) == subset)
            found = best[subset]
            card_usage = published["min_max_usage"]
            mine = None if found is None else found["usage"]
            search_rows.append({
                "route": row["route"],
                "subset": list(subset),
                "published": card_usage,
                "published_feasible": published["feasible_within_named"],
                "mine": mine,
                "mine_core": None if found is None else found["core"],
            })
            # A coarser grid may sit above a refined minimum usage. That is not a miss.
            # A grid that beats the published usage, or makes an infeasible subset feasible, is.
            if mine is not None and card_usage is not None and mine + 5e-4 < card_usage:
                differ(row["route"], "search below published " + ",".join(subset), card_usage, mine, 5e-4)
            if not published["feasible_within_named"] and mine is not None and mine <= 1.0:
                differ(row["route"], "subset became feasible " + ",".join(subset), 1.0, mine, 0.0)

    # 255 MPa: full gamma and k=0.82, face fixed. Record the best least screen.
    sens_best = []
    for row in checks["full_named_maxima"]:
        if row["material"] != "S200F255_sensitivity":
            continue
        point = row["point"]
        scarf = point["at_full_named"]["projected_seam_mode"] == "scarf_mean_shear"
        bond = point["joining"]["bond_kg"] / (2.0 * A)
        primer = point["joining"]["primer_kg"] / (2.0 * A)
        winner = None
        for core in cores:
            for fraction in fractions:
                solved = solve_mass(fraction, core["rho"], bond, primer, scarf)
                if solved is None:
                    continue
                state = section_state(solved["tf"], solved["tc"], E, NU, core)
                modes = modes_at(state, state["gamma_full"], 0.82, FACE_255)
                seam = state["scarf"] if scarf else modes["face_compression"]
                least = min(list(modes.values()) + [seam])
                if winner is None or least > winner["least"]:
                    winner = {"least": least, "core": core["name"], "fraction": fraction}
        sens_best.append({
            "route": row["route"],
            "published": row["least_SF"],
            "mine": None if winner is None else winner["least"],
            "core": None if winner is None else winner["core"],
        })
        if winner is not None and winner["least"] > row["least_SF"] + 5e-4:
            differ(row["route"], "255 search above published", row["least_SF"], winner["least"], 5e-4)
        if winner is not None and winner["least"] >= 1.0:
            differ(row["route"], "255 set floats", 0.9582172954756751, winner["least"], 0.0)

    ended = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    summary = {
        "started_at": started,
        "ended_at": ended,
        "bx": BX,
        "zero_core_255": bound_note,
        "rows_rescored": len(rescored),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:40],
        "search": search_rows,
        "sensitivity_255": sens_best,
        "headline_usages": [
            {"label": item["label"], "published_usage": item["usage"], "rescored_usage": item["mine_usage"]}
            for item in rescored if "seam=True" in item["label"] and "0.0752" in item["label"]
        ],
    }
    print("BX", g(BX))
    print("BOUND", g(face_sf_cap))
    print("MISMATCHES", len(mismatches))
    for item in mismatches[:30]:
        print(" ", item["row"], item["field"], item.get("card"), item.get("mine"))
    for item in summary["headline_usages"]:
        print("USE", item["label"], g(item["published_usage"]), g(item["rescored_usage"]))
    for item in sens_best:
        print("S255", item["route"], g(item["published"]), g(item["mine"]))

    pins = []
    for path in (
        "withheld-source:1577f21d44c55eff",
        "withheld-source:b528d6a62c81ce0b",
        os.path.join(OWNER, "CARD.md"),
        os.path.join(OWNER, "METHOD.md"),
        os.path.join(OWNER, "PROPERTY-CHECKS.json"),
        os.path.join(OWNER, "RESULTS.json"),
        os.path.join(OWNER, "NFI.json"),
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
            "id": "NFI-CHECK-028B-SEAM-SCREEN",
            "status": "scope",
            "note": (
                "The 0.97197751743 and 0.996075 usages are set by the assumed 10 MPa "
                "scarf-shear screen, which caps face stress at 300.333333 MPa. "
                "That screen is not a measured beryllium scarf allowable. "
                "The laboratory 0.651468543105 usage is the same with the screen off, "
                "because the ideal weld is scored as parent face compression."
            ),
        },
        {
            "id": "NFI-CHECK-028B-255-BOUND",
            "status": "stands",
            "note": (
                "With the fixed reserve and systems removed, the largest face thickness "
                "at zero core is %s m and the 255 MPa compression factor is %s. "
                "Core mass or joint excess leaves less face thickness. "
                "No gamma or wrinkling value changes that face factor."
            ) % (g(tf_cap), g(face_sf_cap)),
        },
    ]})
    dump("CHECK-INPUTS.json", {"read_only": pins, "started_at": started, "ended_at": ended})
    lines = [
        "# CHECK MAINLINE-028b",
        "",
        "Unit vacuum-mainline028b-check-1020. QUESTIONABLE. Not a certification. The owner's card is not rewritten.",
        "",
        "Own arithmetic on the fixed 019 reserve, stock panels, and the published sections. Two factors, gamma and wrinkling, are the least set that reaches a usage of 1 or below. Empty, wrinkling-only and face-only sets stay infeasible. Gamma alone stays above 1.",
        "",
        "Scarf-screen usages at nu=0.0752: %s. The zero-core 255 MPa face factor is %s, so no set floats."
        % (
            "; ".join(
                "%s %s" % (item["route"], g(item["usage"]))
                for item in rescored
                if item["nu"] == NU and item["seam_enforced"]
            ),
            g(face_sf_cap),
        ),
        "",
        "No mismatch at the printed precision." if not mismatches else "Mismatches: %s." % len(mismatches),
        "",
    ]
    dump("CHECK-CARD.md", "\n".join(lines) + "\n")
    print("DONE", ended)


if __name__ == "__main__":
    main()
