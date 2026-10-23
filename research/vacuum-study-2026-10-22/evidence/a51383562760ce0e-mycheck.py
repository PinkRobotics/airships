"""Una600: my own ordinary arithmetic from the owner's stated inputs (INPUTS.json) and the card's stated equations; never the owner's
arithmetic.py. Compares every stated number in POINTS.json and the card's sensitivities, and checks every input row's QUESTIONABLE tag and
source. usage: mycheck.py <owner outputs dir>"""
import json, math, sys
O = sys.argv[1]
rows = json.load(open(f"{O}/INPUTS.json")); pts = {p["point_id"]: p for p in json.load(open(f"{O}/POINTS.json"))}
nfi = json.load(open(f"{O}/NFI.json"))
def v(iid, point=None):
    hits = [r for r in rows if r["input_id"] == iid and (point is None or r["point_id_or_common"] in (point, "common"))]
    assert len(hits) >= 1, (iid, point); return float(hits[0]["value"])
TOL = 1e-12; bad = []; n = 0
def cmp(label, mine, theirs):
    global n; n += 1
    rel = abs(mine - theirs) / max(abs(theirs), 1e-300)
    if rel > TOL: bad.append((label, mine, theirs, rel))
    return rel
# atmosphere (ISA troposphere, the owner's stated constants)
h, T0, P0, L, g, Rs = v("I-H"), v("I-T0"), v("I-P0"), v("I-LAPSE"), v("I-G"), v("I-RSPEC")
T = T0 - L * h; p = P0 * (T / T0) ** (g / (L * Rs)); rho = p / (Rs * T)
R = v("I-R"); V = 4 / 3 * math.pi * R ** 3; lift = rho * V; A = 4 * math.pi * R ** 2
print(f"T {T!r}  p_ext {p!r}  rho {rho!r}  V {V!r}  lift {lift!r}")
cmp("card T 284.9", T, 284.9); cmp("card p_ext", p, 95460.8379139); cmp("card rho", rho, 1.16726833075)
E, rAl, nu = v("I-E"), v("I-RHO-AL"), v("I-NU")
def check_point(pid, masses, p_coll, extra=None):
    P = pts[pid]; tot = sum(masses.values()); margin = (lift - tot) / lift; sf = p_coll / p
    cmp(f"{pid} V", V, P["displaced_volume_m3"]); cmp(f"{pid} lift", lift, P["lift_equivalent_mass_kg"])
    for k, m in masses.items(): cmp(f"{pid} mass {k}", m, P["all_mass_breakdown_kg"][k])
    cmp(f"{pid} all mass", tot, P["all_mass_kg"]); cmp(f"{pid} float margin", margin, P["float_margin"])
    cmp(f"{pid} collapse", p_coll, P["collapse_pressure_estimate_Pa"])
    sfk = next(k for k in P if "safety" in k.lower() and "factor" in k.lower() and isinstance(P[k], (int, float)))
    cmp(f"{pid} SF ({sfk})", sf, P[sfk])
    fk = [k for k in P if "factor" in k.lower() and k != sfk and isinstance(P[k], (int, float))]
    for k in fk: cmp(f"{pid} improvement ({k}) = 1/SF (linear in E)", 1 / sf, P[k])
    for k, (mine, key) in (extra or {}).items(): cmp(f"{pid} {k}", mine, P[key])
    print(f"{pid}: masses {masses} total {tot!r} margin {margin!r} p_collapse {p_coll!r} SF {sf!r} factor {1/sf!r}")
    return tot, margin, sf
# P1 simple shell: thin-shell mass rho*4piR^2*t; Zoelly with knockdown
t1, kd1 = v("I-T1", "P1"), v("I-KD", "P1")
m1 = {"shell": rAl * A * t1}; m1["joints"] = v("I-J1", "P1") * m1["shell"]; m1["systems_payload"] = v("I-SYS1", "P1"); m1["residual_gas"] = v("I-GAS1", "P1")
pcl1 = 2 * E * (t1 / R) ** 2 / math.sqrt(3 * (1 - nu ** 2)); D1 = E * t1 ** 3 / (12 * (1 - nu ** 2)); S1 = E * t1
cmp("P1 identity 4/R^2 sqrt(D S) = Zoelly", 4 / R ** 2 * math.sqrt(D1 * S1), pcl1)
check_point("P1", m1, kd1 * pcl1, {"classical": (pcl1, "classical_or_mode_pressure_Pa")})
# P2 sandwich: two faces, core rho*A*c, joints on faces+core; owner extrapolation
tf, c, rc, kd2 = v("I-TF", "P2"), v("I-CORE-T", "P2"), v("I-RHO-CORE", "P2"), v("I-KD", "P2")
def p2(core):
    m = {"faces": 2 * rAl * A * tf, "core": rc * A * core}; m["joints"] = v("I-J2", "P2") * (m["faces"] + m["core"])
    m["systems_payload"] = v("I-SYS2", "P2"); m["residual_gas"] = v("I-GAS2", "P2"); d = core + tf
    D = E * tf * d ** 2 / (2 * (1 - nu ** 2)); S = E * 2 * tf; pcl = 4 / R ** 2 * math.sqrt(D * S)
    return m, pcl
m2, pcl2 = p2(c); check_point("P2", m2, kd2 * pcl2, {"classical": (pcl2, "classical_or_mode_pressure_Pa")})
# P3 frame/membrane: equal-triangle continuum on 4piR^2, tubes and nodes, pinned Euler vs film
s, ro, tw, sig, tfi, rfi, mn = (v("I-S", "P3"), v("I-RO", "P3"), v("I-TW", "P3"), v("I-SIG", "P3"), v("I-TFILM", "P3"), v("I-RHO-FILM", "P3"), v("I-NODE", "P3"))
ri = ro - tw; Ftri = A / (math.sqrt(3) / 4 * s ** 2); Edg = 1.5 * Ftri; Vn = Edg - Ftri + 2
m3 = {"frame": rAl * math.pi * (ro ** 2 - ri ** 2) * Edg * s, "film": rfi * A * tfi, "nodes": mn * Vn, "systems_payload": v("I-SYS3", "P3"), "residual_gas": v("I-GAS3", "P3")}
I = math.pi / 4 * (ro ** 4 - ri ** 4); pe = 2 * math.pi ** 2 * E * I / (R * s ** 3); pf = 2 * sig * tfi / s
check_point("P3", m3, min(pe, pf))
print(f"P3 p_euler {pe!r} p_film {pf!r} (collapse = the lesser); triangles {Ftri!r} edges {Edg!r} nodes {Vn!r}")
# the card's sensitivities
rc_ = v("I-RHO-CHARTER"); psl = v("I-P-SL")
for pid, (m, pc) in {"P1": (m1, kd1 * pcl1), "P2": (m2, kd2 * pcl2), "P3": (m3, min(pe, pf))}.items():
    tot = sum(m.values()); l2 = rc_ * V
    print(f"S-RHO-{pid} margin {(l2 - tot) / l2!r}   S-SL-{pid} SF {pc / psl!r}")
card = {"S-RHO-P1": 0.42463883211, "S-RHO-P2": 0.256149750245, "S-RHO-P3": 0.669287142454, "S-SL-P1": 0.000815144929939, "S-SL-P2": 0.115485402372, "S-SL-P3": 0.0312875456094}
for pid, (m, pc) in {"P1": (m1, kd1 * pcl1), "P2": (m2, kd2 * pcl2), "P3": (m3, min(pe, pf))}.items():
    tot = sum(m.values()); TOLc = 5e-11   # the card prints 12 significant digits
    for key, mine in ((f"S-RHO-{pid}", (rc_ * V - tot) / (rc_ * V)), (f"S-SL-{pid}", pc / psl)):
        r_ = abs(mine - card[key]) / abs(card[key]); n_ = 1
        if r_ > TOLc: bad.append((key, mine, card[key], r_))
mA, pclA = p2(v("I-CORE-ALT", "P2")); totA = sum(mA.values())
alt = {"float_margin": ((lift - totA) / lift, -0.00274565036435), "crush_SF": (kd2 * pclA / p, 0.195980676463), "collapse_Pa": (kd2 * pclA, 18708.4795901), "all_mass_kg": (totA, 4902.86684881)}
for k, (mine, theirs) in alt.items():
    r_ = abs(mine - theirs) / abs(theirs); print(f"S-P2-CORE-0.16m {k} mine {mine!r} card {theirs!r} rel {r_:.2e}")
    if r_ > 5e-11: bad.append((f"S-P2-CORE-0.16m {k}", mine, theirs, r_))
# tags and sources: every input row and every NFI row
untagged = [r["input_id"] + "/" + r["point_id_or_common"] for r in rows if r.get("QUESTIONABLE_tag") != "QUESTIONABLE"]
unsourced = [r["input_id"] + "/" + r["point_id_or_common"] for r in rows if not str(r.get("source_reference_or_explicit_assumption_basis") or "").strip()]
nfi_ids = {x["NFI_id"] for x in nfi}; dangling = [r["input_id"] for r in rows if r.get("NFI_id") and r["NFI_id"] not in nfi_ids]
nfi_empty = [x["NFI_id"] for x in nfi if not all(str(x.get(k) or "").strip() for k in ("questionable_assumption_or_gap", "direction_of_further_investigation", "how_it_affects_margin_or_SF"))]
used = sorted({i for P in pts.values() for i in P.get("material_and_other_input_ids", [])}); missing_rows = [i for i in used if not any(r["input_id"] == i for r in rows)]
print(f"input rows {len(rows)}: untagged {untagged}; unsourced {unsourced}; NFI rows {len(nfi)}; dangling NFI refs {dangling}; incomplete NFI rows {nfi_empty}; point inputs without a row {missing_rows}")
print(f"compared {n} POINTS/card numbers at rel {TOL} (+ sensitivities at 5e-11, the card's printed precision): MISMATCHES {len(bad)}")
for b in bad: print("  MISMATCH", b)
