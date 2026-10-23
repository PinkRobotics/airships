"""Una600 MAINLINE-002: my own ordinary arithmetic from the stated inputs (the pinned baseline INPUTS.json + the current 276 MPa premise) and
the card's stated models; never the owner's arithmetic.py. Compares every number in RESULTS.json (rel 1e-12) and the card's 12-digit print,
and checks tags/sources/NFI presence. usage: mycheck2.py <current outputs> <baseline outputs>"""
import json, math, re, sys
O, Bd = sys.argv[1], sys.argv[2]
rows = json.load(open(f"{Bd}/INPUTS.json")); RES = json.load(open(f"{O}/RESULTS.json")); CUR = json.load(open(f"{O}/INPUTS.json"))
card = open(f"{O}/CARD.md").read(); nfi = json.load(open(f"{O}/NFI.json")); bnfi = json.load(open(f"{Bd}/NFI.json"))
def v(iid, point=None):
    hits = [r for r in rows if r["input_id"] == iid and (point is None or r["point_id_or_common"] in (point, "common"))]
    assert hits, (iid, point); return float(hits[0]["value"])
TOL = 1e-12; bad = []; n = [0]; printed = []
def cmp(label, mine, theirs):
    n[0] += 1; rel = abs(mine - theirs) / max(abs(theirs), 1e-300)
    if rel > TOL and not (abs(theirs) < 1e-12 and abs(mine) < 1e-12): bad.append((label, mine, theirs, rel))
h, T0, P0, L, g, Rs = v("I-H"), v("I-T0"), v("I-P0"), v("I-LAPSE"), v("I-G"), v("I-RSPEC")
T = T0 - L * h; p = P0 * (T / T0) ** (g / (L * Rs)); rho = p / (Rs * T)
R = v("I-R"); V = 4 / 3 * math.pi * R ** 3; lift = rho * V; A = 4 * math.pi * R ** 2
E, rAl, nu = v("I-E"), v("I-RHO-AL"), v("I-NU"); sig = float(CUR["sigma_Pa"])
at = RES["atmosphere"]
for k, mine in (("T_K", T), ("p_ext_Pa", p), ("rho_kg_m3", rho), ("volume_m3", V), ("lift_kg", lift)): cmp(f"atmosphere {k}", mine, at[k])
def check(pid, masses, limits, stiff_key):
    r = next(x for x in RES["rows"] if x["point_id"] == pid); tot = sum(masses.values()); margin = (lift - tot) / lift
    for k, m in masses.items(): cmp(f"{pid} mass {k}", m, r["masses_kg"][k])
    cmp(f"{pid} all mass", tot, r["all_mass_kg"]); cmp(f"{pid} lift", lift, r["lift_equivalent_mass_kg"])
    if abs(r["float_margin"]) < 1e-12: assert abs(margin) < 1e-12, (pid, margin)
    else: cmp(f"{pid} float margin", margin, r["float_margin"])
    for k, pl in limits.items(): cmp(f"{pid} limit {k}", pl, r["limits_Pa"][k]); cmp(f"{pid} factor {k} = p_ext/limit", p / pl, r["factors"][k]["factor"])
    assert set(limits) == set(r["limits_Pa"]), (pid, set(limits), set(r["limits_Pa"]))
    gov = min(limits, key=limits.get); assert gov == r["governing_limit"], (pid, gov, r["governing_limit"])
    coll = limits[gov]; cmp(f"{pid} collapse = least limit", coll, r["collapse_pressure_Pa"]); cmp(f"{pid} crush SF", coll / p, r["crush_safety_factor"])
    others = [pl for k, pl in limits.items() if k != stiff_key]; ceil = min([p] + others) / p
    cmp(f"{pid} stiffness-only ceiling SF", ceil, r["stiffness_only_ceiling_SF"])
    for x in [coll, coll / p, tot, margin, ceil] + list(masses.values()) + list(limits.values()) + [p / pl for pl in limits.values()]:
        if abs(x) > 1e-12 and x != 0: printed.append((pid, f"{x:.12g}"))
    print(f"{pid}: total {tot!r} margin {margin!r} limits { {k: round(x, 6) for k, x in limits.items()} } gov {gov} SF {coll/p!r} ceiling {ceil!r}")
    return r
# P1 / P1-A: thin shell
J1, S1, G1, kd1 = v("I-J1", "P1"), v("I-SYS1", "P1"), v("I-GAS1", "P1"), v("I-KD", "P1")
def p1(t):
    m = {"shell": rAl * A * t}; m["joints"] = J1 * m["shell"]; m["systems_payload"] = S1; m["residual_gas"] = G1
    return m, {"knocked_down_buckling": kd1 * 2 * E * (t / R) ** 2 / math.sqrt(3 * (1 - nu ** 2)), "aluminum_yield": 2 * sig * t / R}
t1 = v("I-T1", "P1"); check("P1", *p1(t1), "knocked_down_buckling")
t1a = (lift - S1 - G1) / ((1 + J1) * rAl * A); r = check("P1-A", *p1(t1a), "knocked_down_buckling"); cmp("P1-A t", t1a, r["extra"].get("t_m") or float(re.search(r"t=([0-9.e-]+)", r["geometry"]).group(1)))
# P2 / P2-A: sandwich, two faces + core, joints on faces+core, d = core + tf
tf, c, rc, kd2, J2, S2, G2 = v("I-TF", "P2"), v("I-CORE-T", "P2"), v("I-RHO-CORE", "P2"), v("I-KD", "P2"), v("I-J2", "P2"), v("I-SYS2", "P2"), v("I-GAS2", "P2")
def p2(f):
    m = {"faces": 2 * rAl * A * f, "core": rc * A * c}; m["joints"] = J2 * (m["faces"] + m["core"]); m["systems_payload"] = S2; m["residual_gas"] = G2
    d = c + f; return m, {"knocked_down_buckling": kd2 * 4 * f * d / (R ** 2 * math.sqrt(1 - nu ** 2)) * E, "aluminum_yield": 4 * sig * f / R}
check("P2", *p2(tf), "knocked_down_buckling")
tfa = ((lift - S2 - G2) / (1 + J2) - rc * A * c) / (2 * rAl * A); r = check("P2-A", *p2(tfa), "knocked_down_buckling"); cmp("P2-A tf", tfa, float(re.search(r"tf=([0-9.e-]+)", r["geometry"]).group(1)))
# P3 / P3-A: equal-triangle frame on 4piR^2, tubes at fixed ro, nodes, film; pinned Euler, member yield 2*sig*A/(R*s), film 2*sig_film*t/s
s, ro, tw, sgf, tfi, rfi, mn, S3, G3 = (v("I-S", "P3"), v("I-RO", "P3"), v("I-TW", "P3"), v("I-SIG", "P3"), v("I-TFILM", "P3"), v("I-RHO-FILM", "P3"), v("I-NODE", "P3"), v("I-SYS3", "P3"), v("I-GAS3", "P3"))
Ftri = A / (math.sqrt(3) / 4 * s ** 2); Edg = 1.5 * Ftri; Vn = Edg - Ftri + 2
def p3(w):
    ri = ro - w; Aa = math.pi * (ro ** 2 - ri ** 2); I = math.pi / 4 * (ro ** 4 - ri ** 4)
    m = {"frame": rAl * Aa * Edg * s, "film": rfi * A * tfi, "nodes": mn * Vn, "systems_payload": S3, "residual_gas": G3}
    return m, {"pinned_euler": 2 * math.pi ** 2 * E * I / (R * s ** 3), "aluminum_yield": 2 * sig * Aa / (R * s), "film_membrane": 2 * sgf * tfi / s}
check("P3", *p3(tw), "pinned_euler")
Aa = (lift - rfi * A * tfi - mn * Vn - S3 - G3) / (rAl * Edg * s); twa = ro - math.sqrt(ro ** 2 - Aa / math.pi)
r = check("P3-A", *p3(twa), "pinned_euler"); cmp("P3-A tw", twa, float(re.search(r"tw=([0-9.e-]+)", r["geometry"]).group(1)))
# the card's 12-significant-digit print of my values
missing = sorted({(pid, x) for pid, x in printed if x not in card})
print(f"compared {n[0]} RESULTS numbers at rel {TOL}: MISMATCHES {len(bad)}"); [print("  MISMATCH", b) for b in bad]
print(f"card print: {len(set(printed))} of my values formatted %.12g; absent from CARD.md: {len(missing)} {missing[:12]}")
# tags, sources, NFI
print("current premise: tag", CUR.get("tag"), "| source present", bool(str(CUR.get("source") or "").strip()), "| sigma_kind", CUR.get("sigma_kind"), "| transfer", CUR.get("sigma_transfer"), "| admitted", CUR.get("admitted"))
untag = [r_["input_id"] + "/" + r_["point_id_or_common"] for r_ in rows if r_.get("QUESTIONABLE_tag") != "QUESTIONABLE"]
unsrc = [r_["input_id"] + "/" + r_["point_id_or_common"] for r_ in rows if not str(r_.get("source_reference_or_explicit_assumption_basis") or "").strip()]
print(f"baseline input rows {len(rows)}: untagged {untag}; unsourced {unsrc}")
inc = [x.get("NFI_id") for x in nfi if not all(str(x.get(k) or "").strip() for k in ("gap", "direction", "effect"))]
print(f"current NFI rows {len(nfi)}: incomplete {inc}; ids {[x.get('NFI_id') for x in nfi]}")
binc = [x["NFI_id"] for x in bnfi if not all(str(x.get(k) or "").strip() for k in ("questionable_assumption_or_gap", "direction_of_further_investigation", "how_it_affects_margin_or_SF"))]
print(f"baseline NFI rows {len(bnfi)}: incomplete {binc}; ids {[x['NFI_id'] for x in bnfi]}")
