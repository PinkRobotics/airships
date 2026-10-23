#!/usr/bin/env python3
"""Independent MAINLINE-008 check. First-order formulas from the card brief. Not the owner's script."""
import hashlib
import json
import math
import re
from pathlib import Path

R = 10.0
KD = 0.2
NU = 0.33
E_AL = 68.9e9
SIG_AL = 276e6
RHO_AL = 2700.0
P = 95460.83791390515

def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-30)

def p2_buckling(tf, sep, e=E_AL, kd=KD):
    return kd * 4 * tf * sep * e / (R * R * math.sqrt(1 - NU * NU))

def p2_yield(tf, sigma=SIG_AL):
    return 4 * sigma * tf / R

def load(path):
    return json.loads(Path(path).read_text())

card = Path("unpublished-local-ref:6c407fc7aea92414")
base = Path("unpublished-local-ref:768b7b34f9cac6c4")
inp = load(card / "INPUTS.json")
res = load(card / "RESULTS.json")
r2 = load(base / "vacuum-mainline002-strength-owner1200-1019/RESULTS.json")
r3 = load(base / "vacuum-mainline003-p2-targets-owner1200-1019/RESULTS.json")
by2 = {row["point_id"]: row for row in r2["rows"]}
by3 = {row["point_id"]: row for row in r3["rows"]}

def geom(pid):
    src = by2[pid] if pid in by2 else by3[pid]
    extra = src.get("extra") or {}
    g = src["geometry"] if isinstance(src["geometry"], dict) else {}
    if "tf_m" in extra:
        return extra["tf_m"], extra["d_m"]
    return g["tf_m"], g["d_m"]

print("== aluminium safety factors from the sandwich formulas ==")
al = {}
for pid in ("P2-A", "P2-C", "P2-K", "P2-E"):
    tf, sep = geom(pid)
    pb, py = p2_buckling(tf, sep), p2_yield(tf)
    al[pid] = {"tf": tf, "d": sep, "SF_b": pb / P, "SF_y": py / P}
    given = inp["case"]["rows_from"][pid]
    for key, mine, card_v in (
        ("SF_b", al[pid]["SF_b"], given["SF_b_Al"]),
        ("SF_y", al[pid]["SF_y"], given["SF_y_Al"]),
        ("tf", tf, given["tf_Al_m"]),
        ("d", sep, given["d_m"]),
    ):
        rr = rel(mine, card_v)
        if rr > 1e-12:
            print(f"MISMATCH baseline {pid} {key} card={card_v!r} mine={mine!r} rel={rr:.3e}")
        else:
            print(f"  {pid} {key} rel {rr:.3e}")

e_over_rho_al = E_AL / RHO_AL
s_over_rho_al = SIG_AL / RHO_AL
print(f"6061 E/rho {e_over_rho_al:.6f} sig/rho {s_over_rho_al:.6f}")
print(f"  vs RESULTS {res['baseline_figures_6061']}")

ranked = {c["name"]: c for c in res["candidates_ranked_by_least_SF_P2E"]}
worst = 0.0
n = 0
max_tfd = 0.0
max_sep_err = 0.0
order_check = []
for cand in inp["candidates_input"]:
    rho = cand["rho"]
    e = cand["E_GPa"] * 1e9
    sig = cand["sigma_c_MPa"] * 1e6
    er = e / rho
    sr = sig / rho
    got = ranked[cand["name"]]
    pairs = [
        ("E_over_rho", er, got["E_over_rho_Pa_per_kg_m3"]),
        ("sig_over_rho", sr, got["sigma_c_over_rho_Pa_per_kg_m3"]),
        ("E_over_rho_GPa_per_g_cc", er * 1e-6, got["E_over_rho_GPa_per_g_cc"]),
        ("sig_over_rho_MPa_per_g_cc", sr * 1e-3, got["sigma_c_over_rho_MPa_per_g_cc"]),
        ("tag", None, None),
    ]
    if cand["tag"] not in ("QUESTIONABLE", "PROJECTION") or not cand.get("source"):
        print("MISSING TAG OR SOURCE", cand["name"], cand.get("tag"))
    rows = {}
    for pid in ("P2-A", "P2-C", "P2-K", "P2-E"):
        tf = al[pid]["tf"] * RHO_AL / rho
        d = al[pid]["d"]
        sfb = al[pid]["SF_b"] * (er / e_over_rho_al)
        sfy = al[pid]["SF_y"] * (sr / s_over_rho_al)
        least = min(sfb, sfy)
        gap = 1 / least
        limit = "E/rho" if sfb <= sfy else "sigma_c/rho"
        # exact separation correction, core held: sep_new = d - tf_al + tf
        sep_new = d - al[pid]["tf"] + tf
        sep_ratio = sep_new / d
        max_tfd = max(max_tfd, tf / d)
        max_sep_err = max(max_sep_err, abs(sep_ratio - 1))
        rows[pid] = {"tf": tf, "tfd": tf / d, "SF_b": sfb, "SF_y": sfy, "least": least,
                     "gap": gap, "limit": limit, "fE": 1 / sfb, "fS": 1 / sfy}
        crow = got["rows"][pid]
        for name, mine, card_v in (
            ("tf", tf, crow["tf_at_equal_face_mass_m"]),
            ("tfd", tf / d, crow["tf_over_d"]),
            ("SF_b", sfb, crow["SF_b"]),
            ("SF_y", sfy, crow["SF_y"]),
            ("least", least, crow["least_SF"]),
            ("gap", gap, crow["gap_1_over_least_SF"]),
            ("fE", 1 / sfb, crow["factor_E_over_rho_for_its_SF1"]),
            ("fS", 1 / sfy, crow["factor_sigma_c_over_rho_for_its_SF1"]),
        ):
            n += 1
            rr = rel(mine, card_v)
            worst = max(worst, rr)
            if rr > 1e-12:
                print(f"MISMATCH {cand['name']} {pid} {name} card={card_v!r} mine={mine!r} rel={rr:.3e}")
        if crow["limiting_figure"] != limit:
            print(f"MISMATCH limit {cand['name']} {pid} card={crow['limiting_figure']} mine={limit}")
    order_check.append((rows["P2-E"]["least"], cand["name"], rows["P2-E"]))

order_check.sort(key=lambda item: -item[0])
print(f"derived comparisons {n} worst_rel {worst:.3e}")
print(f"max tf/d {max_tfd:.6e} card check {res['checks']['tf_much_smaller_than_d_all_candidates_rows']}")
print(f"max |sep_new/sep_al - 1| {max_sep_err:.6e}")
print("rank by least SF P2-E:")
card_order = [c["name"] for c in res["candidates_ranked_by_least_SF_P2E"]]
for i, (least, name, row) in enumerate(order_check, 1):
    flag = "" if card_order[i - 1] == name else " ORDER"
    print(f"  {i} {least:.6f} {name} limit {row['limit']} gap {row['gap']:.6f}{flag}")

# Basis products the prose states with a number on both sides.
print("== stated QI / projection products vs the E used ==")
products = [
    ("CFRP quasi-isotropic T700/epoxy", 0.40 * 134, 54.0),
    ("CFRP quasi-isotropic M55J/epoxy", 0.42 * 325, 135.0),
    ("CFRP quasi-isotropic K13D2U pitch/epoxy", 0.41 * 515, 210.0),
    ("Boron/epoxy quasi-isotropic", 0.42 * 204, 86.0),
    ("Boron sigma", 0.34 * 2500, 850.0),
    ("CNT E from 50% of 256 GPa per g/cc at 1.40 g/cc", 0.50 * 256 * 1.40, 180.0),
    ("Be 41 ksi in MPa", 41 * 6.894757293168361, 283.0),
]
for name, mine, card_v in products:
    print(f"  {name}: stated_product {mine:.4f} card {card_v} rel {rel(mine, card_v):.3e}")

# Pins
pin_bad = 0
for pin in inp["pins"]:
    data = Path(pin["path"]).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != pin["sha256"] or len(data) != pin["bytes"]:
        pin_bad += 1
        print("PIN FAIL", pin["path"])
print(f"pins {len(inp['pins']) - pin_bad}/{len(inp['pins'])}")

claimed = {
    "CARD.md": "f9fad1e9a6e26f1026cc4c59d2838424f48aac8c48325c45f2c3af1e945757ee",
    "RESULTS.json": "b84f229e5f0e7f47af4788c15f0a75794ddfe3bb0d9a64723031815a49dca88d",
    "NFI.json": "6284193a78be0578dfc39462b1f7834a859055e537e83ab3780bd7f600c424c6",
    "INPUTS.json": "6e11b29ae71fe0b3a1b4dd39e74f91290d91a8eb7cde28a9731178283c2ea18f",
}
for name, exp in claimed.items():
    data = (card / name).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    print(name, "MATCH" if digest == exp else "FAIL", len(data))

# CARD.md displayed tokens
text = (card / "CARD.md").read_text()
sections = re.split(r"\n## Rank \d+ - ", text)[1:]
print(f"card rank sections {len(sections)}")
display_miss = 0

def near(token, value):
    if "e" in token.lower():
        shown = float(token)
        return rel(shown, value) < 5e-4
    if "." not in [credential] abs(float(token) - value) <= 0.5
    half = 0.5 * 10 ** (-len(token.split(".")[1]))
    return abs(float(token) - value) <= half + 1e-12

for section, cand in zip(sections, order_check):
    least, name, _ = cand
    # rebuild rows for this candidate
    src = next(c for c in inp["candidates_input"] if c["name"] == name)
    rho, e, sig = src["rho"], src["E_GPa"] * 1e9, src["sigma_c_MPa"] * 1e6
    er, sr = e / rho, sig / rho
    num = r"([0-9]+\.[0-9]+|[0-9]+)"
    fig = re.search(rf"Figures: E/rho {num}.*sigma_c/rho {num}", section)
    if not fig or not near(fig.group(1), er * 1e-6) or not near(fig.group(2), sr * 1e-3):
        display_miss += 1
        print("DISPLAY figures", name, fig.groups() if fig else None, er * 1e-6, sr * 1e-3)
    line = re.search(r"At equal face mass: (.+)", section).group(1)
    for pid in ("P2-A", "P2-C", "P2-K", "P2-E"):
        chunk = re.search(rf"{pid}: SF_b {num}, SF_y {num}, least {num}, gap {num}", line)
        tf = al[pid]["tf"] * RHO_AL / rho
        sfb = al[pid]["SF_b"] * (er / e_over_rho_al)
        sfy = al[pid]["SF_y"] * (sr / s_over_rho_al)
        gap = 1 / min(sfb, sfy)
        vals = (sfb, sfy, min(sfb, sfy), gap)
        if not chunk or any(not near(tok, val) for tok, val in zip(chunk.groups(), vals)):
            display_miss += 1
            print("DISPLAY", name, pid, None if not chunk else chunk.groups(), vals)
    thick = re.search(rf"Face thickness in P2-E at equal mass: {num} mm", section)
    tf_mm = al["P2-E"]["tf"] * RHO_AL / rho * 1000
    if not thick or not near(thick.group(1), tf_mm):
        display_miss += 1
        print("DISPLAY tf", name, None if not thick else thick.group(1), tf_mm)
# The direction list repeats P2-E for the best three overall and the best three available.
direction = [
    ("SiC (monolithic alpha SiC, Hexoloy SA type)", "0.825", "0.209"),
    ("CNT-yarn composite quasi-isotropic", "0.8486", "0.3068"),
    ("Graphene composite quasi-isotropic", "1.091", "0.4383"),
    ("CFRP quasi-isotropic M55J/epoxy", "1.325", "1.232"),
    ("Beryllium S-200F", "0.6662", "1.719"),
]
by_name = {name: row for _, name, row in order_check}
for name, fe, fs in direction:
    row = by_name[name]
    if not near(fe, row["fE"]) or not near(fs, row["fS"]):
        display_miss += 1
        print("DISPLAY direction", name, fe, fs, row["fE"], row["fS"])
print(f"display mismatches {display_miss}")
