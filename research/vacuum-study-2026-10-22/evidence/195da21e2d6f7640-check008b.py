#!/usr/bin/env python3
"""MAINLINE-008b check. Own arithmetic. Does not call the owner's script.

P2 buckling and yield from COMMON.md. Equal face mass is the 008 first-order
rule: tf scales as 1/rho, SF_b as E/rho, SF_y as sigma/rho, SF_b linear in kd.
P1 and P3 safety factors are the candidate figure divided by the requirement
recomputed from the 005 geometry. Wrinkling is the brief's flat-panel form
sigma_wr = 0.5*(E_f*Ec*Gc)**(1/3), so Ec*Gc required is (2*sigma_f)**3/E_f
and the stress factor is (available/required)**(1/3).
"""

import hashlib
import json
import math
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

P = 95460.83791390515
R = 10.0
KD = 0.2
E_AL = 68.9e9
NU = 0.33
SIG_AL = 276e6
RHO_AL = 2700.0
SQRT1 = math.sqrt(1.0 - NU * NU)
SQRT3 = math.sqrt(3.0 * (1.0 - NU * NU))
KD_CARD = 0.140725695373
KD_FULL = 0.14072569537344654
KD_OPT = 0.9

ROOT8 = Path("unpublished-local-ref:6c407fc7aea92414")
ROOT5 = Path("unpublished-local-ref:0025f202a635b894")
ROOT7 = Path("unpublished-local-ref:f0239e03debd3e9c")
ROOT4 = Path("unpublished-local-ref:9b8e74a5330a363b")
OWN = Path("unpublished-local-ref:50eb1bf0371bd1e5")

TOL = 1e-9
mismatches = []
ncomp = 0
worst = 0.0


def rel(a, b):
    den = max(abs(a), abs(b), 1e-30)
    return abs(a - b) / den


def check(row, field, card, mine, tol=TOL):
    global ncomp, worst
    ncomp += 1
    d = rel(float(card), float(mine))
    worst = max(worst, d)
    if d > tol:
        mismatches.append((row, field, float(card), float(mine), d))


def half_up(value, nd):
    q = Decimal(1).scaleb(-nd)
    return Decimal(format(value, ".20f")).quantize(q, rounding=ROUND_HALF_UP)


def display_equal(token, value):
    nd = len(token.split(".")[1]) if "." in token else 0
    rounded = half_up(value, nd)
    if nd == 0:
        text = format(rounded, "f").split(".")[0]
    else:
        text = format(rounded, f".{nd}f")
    return text == token


def sci_equal(token, value):
    m = re.fullmatch(r"([0-9]+\.[0-9]+|[0-9]+)e([+-]?\d+)", token.replace(" ", ""))
    if not m:
        return False
    mant, exp = m.group(1), int(m.group(2))
    return display_equal(mant, value / (10 ** exp))


def token_equal(token, value):
    [credential]
    if re.fullmatch(r"[0-9.]+e[+-]?\d+", token):
        return sci_equal(token, value)
    if re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", token):
        return display_equal(token, value)
    return False


def sf_sandwich(tf, sep, E, sigma, kd):
    buckling = kd * 4.0 * tf * sep * E / (R * R * SQRT1)
    yield_p = 4.0 * SIG_AL * tf / R if sigma is None else 4.0 * sigma * tf / R
    return buckling / P, yield_p / P


def sf_p1(t, E, sigma):
    buckling = KD * 2.0 * (t / R) ** 2 * E / SQRT3
    yield_p = 2.0 * sigma * t / R
    return buckling / P, yield_p / P


def section_p3(tw):
    """Exact annular section used by MAINLINE-005 RESULTS, outer radius 0.02 m."""
    ro = 0.02
    ri = ro - tw
    area = math.pi * (ro * ro - ri * ri)
    inertia = math.pi / 4.0 * (ro ** 4 - ri ** 4)
    return area, inertia


def sf_p3(tw, E, sigma):
    area, inertia = section_p3(tw)
    euler = 2.0 * math.pi ** 2 * E * inertia / (R * 1.0 ** 3)
    member = 2.0 * sigma * area / (R * 1.0)
    return euler / P, member / P


def req_product(sigma_f, E):
    return (2.0 * sigma_f) ** 3 / E


def main():
    d8 = json.loads((ROOT8 / "RESULTS.json").read_text())
    d5 = json.loads((ROOT5 / "RESULTS.json").read_text())
    d7 = json.loads((ROOT7 / "RESULTS.json").read_text())
    d4 = json.loads((ROOT4 / "RESULTS.json").read_text())
    own = json.loads((OWN / "RESULTS.json").read_text())
    card = (OWN / "CARD.md").read_text()

    rows5 = {row["point_id"]: row for row in d5["rows"]}
    # Re-derive 005 requirements from the stated geometry, then compare.
    for pid, tkey in (("P1", "t"), ("P1-A", "t")):
        t = rows5[pid]["geometry"][tkey]
        sb, sy = sf_p1(t, E_AL, SIG_AL)
        check(pid, "005 SF_b", rows5[pid]["buckling_SF"], sb)
        check(pid, "005 SF_y", rows5[pid]["yield_SF_QUESTIONABLE"], sy)
        er2 = (E_AL / RHO_AL ** 2) / sb
        sr = (SIG_AL / RHO_AL) / sy
        check(pid, "005 E/rho2", rows5[pid]["figures_required"]["E_over_rho2"], er2)
        check(pid, "005 sigma/rho", rows5[pid]["figures_required"]["sig_over_rho"], sr)
    for pid in ("P3", "P3-A"):
        tw = rows5[pid]["geometry"]["tw"]
        area, inertia = section_p3(tw)
        check(pid, "005 A", rows5[pid]["geometry"]["A"], area)
        check(pid, "005 I", rows5[pid]["geometry"]["I"], inertia)
        sb, sy = sf_p3(tw, E_AL, SIG_AL)
        check(pid, "005 SF_b", rows5[pid]["buckling_SF"], sb)
        check(pid, "005 SF_y", rows5[pid]["yield_SF_QUESTIONABLE"], sy)
        er = (E_AL / RHO_AL) / sb
        sr = (SIG_AL / RHO_AL) / sy
        check(pid, "005 E/rho", rows5[pid]["figures_required"]["E_over_rho_members"], er)
        check(pid, "005 sigma/rho", rows5[pid]["figures_required"]["sig_over_rho_members"], sr)

    p2e = d8["case"]["rows_from"]["P2-E"]
    sb_al, sy_al = sf_sandwich(p2e["tf_Al_m"], p2e["d_m"], E_AL, SIG_AL, KD)
    check("P2-E Al", "SF_b", p2e["SF_b_Al"], sb_al)
    check("P2-E Al", "SF_y", p2e["SF_y_Al"], sy_al)
    p4 = next(row for row in d4["rows"] if row["point_id"] == "P2-E")
    check("004b", "kd full", p4["sealed_sp8032_kd"], KD_FULL, tol=0)
    check("004b", "SF_b conservative", p4["factors"]["conservative"]["buckling_SF"], sb_al * KD_FULL / KD)
    check("004b", "SF_b central", p4["factors"]["central"]["buckling_SF"], sb_al)
    check("004b", "SF_b optimistic", p4["factors"]["optimistic"]["buckling_SF"], sb_al * KD_OPT / KD)

    # 007 geometry, recomputed, then used as the light-core aluminium baseline.
    light = {}
    for rho, key in ((4.0, "4.0"), (1.0, "1.0")):
        block = d7["rows"][key]
        for split, label in (("max_least_SF", "leastfactor"), ("max_buckling_SF", "bucklingmax")):
            g = block[split]
            sb, sy = sf_sandwich(g["tf_m"], g["separation_m"], E_AL, SIG_AL, KD)
            check(f"007 {rho} {label}", "SF_b", g["SF_b"], sb)
            check(f"007 {rho} {label}", "SF_y", g["SF_y"], sy)
            light[f"007-{int(rho)}kg-{label}"] = {
                "tf": g["tf_m"],
                "sep": g["separation_m"],
                "sb": sb,
                "sy": sy,
            }

    products = []
    for mat in d7["materials"]:
        ec = mat.get("Ec_Pa")
        gc = mat.get("Gc_used_for_compare_Pa", mat.get("Gc_Pa"))
        if ec is None or gc is None:
            continue
        prod = ec * gc
        products.append((prod, mat["name"], mat["density_kg_m3"], ec, gc))
        published = next(
            row["Ec_Gc_Pa2"]
            for row in d7["material_comparison"]
            if row["material"] == mat["name"]
        )
        check(mat["name"], "Ec*Gc", published, prod)
    products.sort(reverse=True)
    best_prod, best_name, best_rho, best_ec, best_gc = products[0]

    req = {
        "P1": (E_AL / RHO_AL ** 2) / sf_p1(rows5["P1"]["geometry"]["t"], E_AL, SIG_AL)[0],
        "P1s": (SIG_AL / RHO_AL) / sf_p1(rows5["P1"]["geometry"]["t"], E_AL, SIG_AL)[1],
        "P1A": (E_AL / RHO_AL ** 2) / sf_p1(rows5["P1-A"]["geometry"]["t"], E_AL, SIG_AL)[0],
        "P1As": (SIG_AL / RHO_AL) / sf_p1(rows5["P1-A"]["geometry"]["t"], E_AL, SIG_AL)[1],
        "P3": (E_AL / RHO_AL) / sf_p3(rows5["P3"]["geometry"]["tw"], E_AL, SIG_AL)[0],
        "P3s": (SIG_AL / RHO_AL) / sf_p3(rows5["P3"]["geometry"]["tw"], E_AL, SIG_AL)[1],
        "P3A": (E_AL / RHO_AL) / sf_p3(rows5["P3-A"]["geometry"]["tw"], E_AL, SIG_AL)[0],
        "P3As": (SIG_AL / RHO_AL) / sf_p3(rows5["P3-A"]["geometry"]["tw"], E_AL, SIG_AL)[1],
    }
    # What the owner stored, the five-significant-figure card print.
    stored_req = own["inputs"]["005_required_figures"]
    print("005 printed vs recomputed requirement relative differences:")
    for label, stored, mine in (
        ("P1 E/rho2", stored_req["P1"]["E_over_rho2_Pa_m6_kg2"], req["P1"]),
        ("P1 sigma/rho", stored_req["P1"]["sigma_over_rho_Pa_m3_kg"], req["P1s"]),
        ("P1A E/rho2", stored_req["P1-A"]["E_over_rho2_Pa_m6_kg2"], req["P1A"]),
        ("P1A sigma/rho", stored_req["P1-A"]["sigma_over_rho_Pa_m3_kg"], req["P1As"]),
        ("P3 E/rho", stored_req["P3"]["E_over_rho_Pa_m3_kg"], req["P3"]),
        ("P3 sigma/rho", stored_req["P3"]["sigma_over_rho_Pa_m3_kg"], req["P3s"]),
        ("P3A E/rho", stored_req["P3-A"]["E_over_rho_Pa_m3_kg"], req["P3A"]),
        ("P3A sigma/rho", stored_req["P3-A"]["sigma_over_rho_Pa_m3_kg"], req["P3As"]),
    ):
        print(f"  {label}: stored {stored:.8g} mine {mine:.8g} rel {rel(stored, mine):.3e}")

    er_al = E_AL / RHO_AL
    sr_al = SIG_AL / RHO_AL
    by_name = {c["name"]: c for c in own["candidates"]}
    derived = []
    for src in d8["candidates_ranked_by_least_SF_P2E"]:
        name = src["name"]
        rho = float(src["rho"])
        E = float(src["E_GPa"]) * 1e9
        sigma = float(src["sigma_c_MPa"]) * 1e6
        er = E / rho
        sr = sigma / rho
        er2 = E / rho ** 2
        tf = p2e["tf_Al_m"] * RHO_AL / rho
        sb = sb_al * er / er_al
        sy = sy_al * sr / sr_al
        sigma_f = P * R / (4.0 * tf)
        need = req_product(sigma_f, E)
        sf_wr = (best_prod / need) ** (1.0 / 3.0)
        miss = need / best_prod
        row = {
            "name": name,
            "tag": src["tag"],
            "source": src["source"],
            "rho": rho,
            "E": E,
            "sigma": sigma,
            "er_gcc": (E / 1e9) / (rho / 1000.0),
            "sr_gcc": (sigma / 1e6) / (rho / 1000.0),
            "er": er,
            "sr": sr,
            "er2": er2,
            "tf": tf,
            "sb_c": sb * KD_CARD / KD,
            "sb_full": sb * KD_FULL / KD,
            "sb": sb,
            "sb_90": sb * KD_OPT / KD,
            "sy": sy,
            "sigma_f": sigma_f,
            "need": need,
            "sf_wr": sf_wr,
            "miss": miss,
            "p1b": er2 / req["P1"],
            "p1y": sr / req["P1s"],
            "p1ab": er2 / req["P1A"],
            "p1ay": sr / req["P1As"],
            "p3b": er / req["P3"],
            "p3y": sr / req["P3s"],
            "p3ab": er / req["P3A"],
            "p3ay": sr / req["P3As"],
            "light": {},
        }
        own_c = by_name[name]
        check(name, "tag present", 1, 1 if src["tag"] in ("QUESTIONABLE", "PROJECTION") else 0)
        check(name, "source present", 1, 1 if src.get("source") else 0)
        check(name, "E/rho", own_c["E_over_rho_Pa_per_kg_m3"], er)
        check(name, "sigma/rho", own_c["sigma_over_rho_Pa_per_kg_m3"], sr)
        check(name, "E/rho2", own_c["E_over_rho2_Pa_m6_kg2"], er2)
        check(name, "P2E tf", own_c["P2E"]["tf_at_equal_face_mass_m"], tf)
        check(name, "P2E SFb kd card", own_c["P2E"]["SF_b_kd_conservative_SP8032"], row["sb_c"])
        check(name, "P2E SFb 0.20", own_c["P2E"]["SF_b_kd_020"], sb)
        check(name, "P2E SFb 0.90", own_c["P2E"]["SF_b_kd_090"], row["sb_90"])
        check(name, "P2E SFy", own_c["P2E"]["SF_y"], sy)
        # P1/P3: owner divided by the printed 005 figures. Compare both.
        check(name, "P1 SFb vs exact req", own_c["P1_base"]["SF_b"], row["p1b"], tol=5e-5)
        check(name, "P1 SFy vs exact req", own_c["P1_base"]["SF_y"], row["p1y"], tol=5e-5)
        check(name, "P1A SFb vs exact req", own_c["P1A"]["SF_b"], row["p1ab"], tol=5e-5)
        check(name, "P1A SFy vs exact req", own_c["P1A"]["SF_y"], row["p1ay"], tol=5e-5)
        check(name, "P3 SFb vs exact req", own_c["P3_base"]["SF_b"], row["p3b"], tol=5e-5)
        check(name, "P3 SFy vs exact req", own_c["P3_base"]["SF_y"], row["p3y"], tol=5e-5)
        check(name, "P3A SFb vs exact req", own_c["P3A"]["SF_b"], row["p3ab"], tol=5e-5)
        check(name, "P3A SFy vs exact req", own_c["P3A"]["SF_y"], row["p3ay"], tol=5e-5)
        # And against the printed denominators, which is what RESULTS stored.
        check(name, "P1 SFb printed denom", own_c["P1_base"]["SF_b"], er2 / stored_req["P1"]["E_over_rho2_Pa_m6_kg2"])
        check(name, "P1 SFy printed denom", own_c["P1_base"]["SF_y"], sr / stored_req["P1"]["sigma_over_rho_Pa_m3_kg"])
        check(name, "P3 SFb printed denom", own_c["P3_base"]["SF_b"], er / stored_req["P3"]["E_over_rho_Pa_m3_kg"])
        check(name, "P3 SFy printed denom", own_c["P3_base"]["SF_y"], sr / stored_req["P3"]["sigma_over_rho_Pa_m3_kg"])
        w = own_c["WRINKLING_P2E"]
        check(name, "sigma_f", w["sigma_f_Pa"], sigma_f)
        check(name, "EcGc required", w["req_EcGc_Pa2"], need)
        check(name, "SWr", w["SF_wr_best_catalog"], sf_wr)
        check(name, "Wmis", w["wrinkle_miss_vs_best_catalog"], miss)
        check(name, "overall least", own_c["overall_P2E_kd020"]["least_SF"], min(sb, sy, sf_wr))
        check(name, "overall factor is 1/SF", own_c["overall_P2E_kd020"]["factor_needed"], 1.0 / min(sb, sy, sf_wr))
        for key, g in light.items():
            tf_l = g["tf"] * RHO_AL / rho
            sb_l = g["sb"] * er / er_al
            sy_l = g["sy"] * sr / sr_al
            sig_l = P * R / (4.0 * tf_l)
            need_l = req_product(sig_l, E)
            wr_l = (best_prod / need_l) ** (1.0 / 3.0)
            own_l = own_c["rows_007"][key]
            check(name + " " + key, "tf", own_l["tf_c_m"], tf_l)
            check(name + " " + key, "SFb", own_l["SF_b_at_020"], sb_l)
            check(name + " " + key, "SFy", own_l["SF_y"], sy_l)
            check(name + " " + key, "sigma_f", own_l["sigma_f_Pa"], sig_l)
            check(name + " " + key, "need", own_l["req_EcGc_Pa2"], need_l)
            check(name + " " + key, "SWr", own_l["SF_wr_best_catalog"], wr_l)
            check(name + " " + key, "Wmis", own_l["wrinkle_miss_vs_best_catalog"], need_l / best_prod)
            row["light"][key] = {
                "tf": tf_l,
                "sb": sb_l,
                "sy": sy_l,
                "need": need_l,
                "wr": wr_l,
                "miss": need_l / best_prod,
                "face": min(sb_l, sy_l),
                "overall": min(sb_l, sy_l, wr_l),
            }
        face = min(sb, sy)
        overall = min(sb, sy, sf_wr)
        limit = "buckling" if sb <= sy and sb <= sf_wr else "yield" if sy <= sf_wr else "wrinkling"
        row["face"] = face
        row["overall"] = overall
        row["limit"] = limit
        derived.append(row)

    print(f"\nbest catalog {best_name} rho {best_rho} Ec {best_ec} Gc {best_gc} product {best_prod:.6e}")
    print(f"comparisons {ncomp} worst rel {worst:.3e} numeric mismatches {len(mismatches)}")
    for item in mismatches:
        print("MISMATCH", item[0], item[1], item[2], item[3], f"rel {item[4]:.3e}")

    # CARD table digits.
    display_bad = []
    shorts = [
        "SiC", "CNT-yarn", "Graphene", "M55J", "Beryllium", "K13D2U", "Boron",
        "AlBeMet", "T700", "Al-Li", "Ti-6Al-4V", "6061", "7075", "AZ31B", "Vitreloy",
    ]
    for line in card.splitlines():
        if not line.startswith("| ") or line.startswith("| candidate") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 13:
            continue
        label = cells[0]
        row = None
        for s in shorts:
            if s in label:
                row = next(r for r in derived if s in r["name"])
                break
        vals = [
            row["er_gcc"], row["sr_gcc"], row["sb_c"], row["sb"], row["sb_90"], row["sy"],
            row["miss"], row["sf_wr"], row["p1b"], row["p1y"], row["p3b"], row["p3y"],
        ]
        for field, token, value in zip(
            ["E/r", "s/r", "SFb c", "SFb .20", "SFb .90", "SFy", "Wmis", "SWr", "P1b", "P1y", "P3b", "P3y"],
            cells[1:],
            vals,
        ):
            if not token_equal(token, value):
                display_bad.append((row["name"], field, token, value))
    print(f"\nCARD table display mismatches {len(display_bad)}")
    for item in display_bad:
        print("DISPLAY", item)

    # Prose claims.
    def show(value, nd):
        return format(half_up(value, nd), f".{nd}f")

    prose = []

    def add(label, token, value):
        ok = token_equal(token, value)
        prose.append((ok, label, token, value))
        if not ok:
            print(f"PROSE FAIL {label}: card {token} value {value}")

    # Headline passes.
    buck_pass = [r["name"] for r in derived if r["sb"] >= 1.0]
    buck_fail_c = [r for r in derived if r["sb_c"] >= 1.0]
    print("\nbuckling pass at 0.20:", buck_pass)
    print("buckling pass at card kd:", [r["name"] for r in buck_fail_c])
    add("SiC SFb .20 prose 1.212", "1.212", next(r["sb"] for r in derived if "SiC" in r["name"]))
    add("CNT SFb", "1.178", next(r["sb"] for r in derived if "CNT" in r["name"]))
    add("Be SFb", "1.501", next(r["sb"] for r in derived if "Beryllium" in r["name"]))
    add("K13 SFb", "1.100", next(r["sb"] for r in derived if "K13" in r["name"]))
    add("SiC conservative", "0.8529", next(r["sb_c"] for r in derived if "SiC" in r["name"]))

    # Best three overall and the factor the prose calls a core-product factor.
    ranked = sorted(derived, key=lambda r: -r["overall"])
    print("\noverall rank P2-E:")
    for r in ranked[:6]:
        print(f"  {r['name'][:28]:28} SF {r['overall']:.6f} limit {r['limit']} 1/SF {1/r['overall']:.4f} product x {r['miss']:.4f}")
    today = sorted((r for r in derived if r["tag"] == "QUESTIONABLE"), key=lambda r: -r["overall"])
    print("available today:")
    for r in today[:4]:
        print(f"  {r['name'][:28]:28} SF {r['overall']:.6f} limit {r['limit']} miss {r['miss']:.4f} sy {r['sy']:.4f}")

    one = "007-1kg-leastfactor"
    four = "007-4kg-leastfactor"
    print("\n1 kg face rank (min SFb, SFy):")
    for r in sorted(derived, key=lambda r: -r["light"][one]["face"])[:8]:
        L = r["light"][one]
        mode = "yield" if L["sy"] < L["sb"] else "buckling"
        print(f"  {r['name'][:28]:28} face {L['face']:.6f} {mode} wr {L['wr']:.4f} miss {L['miss']:.4f} overall {L['overall']:.4f}")
    print("4 kg face rank:")
    for r in sorted(derived, key=lambda r: -r["light"][four]["face"])[:8]:
        L = r["light"][four]
        mode = "yield" if L["sy"] < L["sb"] else "buckling"
        print(f"  {r['name'][:28]:28} face {L['face']:.6f} {mode}")

    print("\n1 kg at conservative kd, face least >= 1:")
    for r in derived:
        L = r["light"][one]
        sb_c = L["sb"] * KD_CARD / KD
        least = min(sb_c, L["sy"])
        if least >= 1.0:
            mode = "yield" if L["sy"] <= sb_c else "buckling"
            print(f"  {r['name'][:32]:32} least {least:.4f} {mode} tag {r['tag']}")

    print("\n1 kg overall rank:")
    for r in sorted(derived, key=lambda r: -r["light"][one]["overall"])[:6]:
        L = r["light"][one]
        print(f"  {r['name'][:28]:28} {L['overall']:.4f} miss {L['miss']:.4f}")

    # Specific prose tokens from the best-three paragraph.
    cnt = next(r for r in derived if "CNT" in r["name"])
    gra = next(r for r in derived if "Graphene" in r["name"])
    m55 = next(r for r in derived if "M55J" in r["name"])
    be = next(r for r in derived if "Beryllium" in r["name"])
    k13 = next(r for r in derived if "K13" in r["name"])
    sic = next(r for r in derived if r["name"].startswith("SiC"))
    al = next(r for r in derived if "6061" in r["name"])
    add("CNT overall SF", "0.783", cnt["overall"])
    add("graphene overall SF", "0.688", gra["overall"])
    add("M55J overall SF", "0.607", m55["overall"])
    add("CNT product factor", "2.1", cnt["miss"])
    add("CNT 1/SF mislabeled", "1.28", 1.0 / cnt["overall"])
    add("graphene 1/SF", "1.45", 1.0 / gra["overall"])
    add("M55J 1/SF", "1.65", 1.0 / m55["overall"])
    add("Be yield", "0.5817", be["sy"])
    add("Be strength factor", "1.72", 1.0 / be["sy"])
    add("Be wrinkle miss", "2.9", be["miss"])
    add("K13 yield", "0.4780", k13["sy"])
    add("K13 strength factor", "2.09", 1.0 / k13["sy"])
    add("SiC need", "1.057e16", sic["need"])
    add("CNT need", "2.22e15", cnt["need"])
    add("SiC tf mm", "0.2927", sic["tf"] * 1000)
    add("CNT tf mm", "0.6482", cnt["tf"] * 1000)
    add("1kg SiC face", "3.820", sic["light"][one]["face"])
    add("1kg CNT face", "3.713", cnt["light"][one]["face"])
    add("1kg graphene face", "2.888", gra["light"][one]["face"])
    add("1kg M55J face", "1.539", m55["light"][one]["face"])
    add("1kg Be face", "1.103", be["light"][one]["face"])
    add("1kg SiC need", "1.55e15", sic["light"][one]["need"])
    add("1kg CNT need", "3.25e14", cnt["light"][one]["need"])
    add("1kg CNT product x", "0.31", cnt["light"][one]["miss"])
    add("1kg graphene product x", "0.45", gra["light"][one]["miss"])
    add("4kg SiC face", "3.192", sic["light"][four]["face"])
    add("4kg CNT face", "3.103", cnt["light"][four]["face"])
    add("4kg graphene face", "2.413", gra["light"][four]["face"])
    add("4kg M55J face", "1.286", m55["light"][four]["face"])
    add("4kg Be face", "0.9216", be["light"][four]["face"])
    boron = next(r for r in derived if "Boron" in r["name"])
    add("4kg boron face", "1.038", boron["light"][four]["face"])
    add("Al P2E miss", "39.1", al["miss"])
    add("Al 1kg miss", "5.7", al["light"][one]["miss"])
    add("CNT 1kg tf mm", "1.229", cnt["light"][one]["tf"] * 1000)
    add("1kg CNT overall", "1.484", cnt["light"][one]["overall"])
    add("1kg graphene overall", "1.304", gra["light"][one]["overall"])
    add("1kg M55J overall", "1.151", m55["light"][one]["overall"])
    add("1kg Be overall today", "1.103", be["light"][one]["overall"])
    add("1kg K13 overall", "0.906", k13["light"][one]["overall"])
    sb_c = sic["light"][one]["sb"] * KD_CARD / KD
    add("1kg SiC conservative face", "2.688", min(sb_c, sic["light"][one]["sy"]))
    sb_c = cnt["light"][one]["sb"] * KD_CARD / KD
    add("1kg CNT conservative face", "2.613", min(sb_c, cnt["light"][one]["sy"]))
    sb_c = be["light"][one]["sb"] * KD_CARD / KD
    add("1kg Be conservative face", "1.103", min(sb_c, be["light"][one]["sy"]))
    add("P1 CNT short", "119", 1.0 / cnt["p1b"])
    add("P1 SiC short", "256", 1.0 / sic["p1b"])
    add("P3 Be", "0.2131", be["p3b"])
    add("P3 SiC", "0.1721", sic["p3b"])
    add("P3 CNT", "0.1673", cnt["p3b"])
    add("P3 best factor", "4.7", 1.0 / be["p3b"])

    print(f"\nprose checks {sum(1 for ok, *_ in prose if ok)}/{len(prose)} passed")
    print("\nFINDING buckling at kd 0.140725695373 on P2-E:")
    for r in sorted(derived, key=lambda r: -r["sb_c"]):
        print(f"  {r['name'][:40]:40} {r['sb_c']:.6f}")
    print("FINDING product factor vs 1/SF for wrinkling-limited best three:")
    for r in (cnt, gra, m55):
        print(
            f"  {r['name'][:28]:28} SF {r['overall']:.6f} 1/SF {1/r['overall']:.4f} "
            f"product {r['miss']:.4f}"
        )
    print("FINDING 1 kg face clearers at conservative kd were printed above.")
    print("DONE")


if __name__ == "__main__":
    main()
