"""Una600 MAINLINE-003: my own ordinary arithmetic from the pinned MAINLINE-001 INPUTS (P2 rows), the current sigma premise and the
card's declared formulas; never the owner's arithmetic.py, the advisory redistribute.py or a predecessor checker. Compares RESULTS
(rel 1e-12), the P2-A comparison against sealed MAINLINE-002 RESULTS, the card's 12-digit print, tags/sources/NFI presence, and prints
the NFI rows' dependency text for the dependency check. usage: mycheck3.py <current outputs> <M001 outputs> <M002 outputs>"""
import json, math, re, sys
O, B1, B2 = sys.argv[1:4]
rows = json.load(open(f"{B1}/INPUTS.json")); RES = json.load(open(f"{O}/RESULTS.json")); CUR = json.load(open(f"{O}/INPUTS.json"))
card = open(f"{O}/CARD.md").read(); nfi = json.load(open(f"{O}/NFI.json")); R2 = json.load(open(f"{B2}/RESULTS.json"))
def v(iid, point=None):
    hits = [r for r in rows if r["input_id"] == iid and (point is None or r["point_id_or_common"] in (point, "common"))]
    assert hits, (iid, point); return float(hits[0]["value"])
TOL = 1e-12; bad = []; n = [0]; printed = []
def cmp(label, mine, theirs):
    n[0] += 1; rel = abs(mine - theirs) / max(abs(theirs), 1e-300)
    if rel > TOL and not (abs(theirs) < 1e-12 and abs(mine) < 1e-12): bad.append((label, mine, theirs, rel))
    if abs(mine) > 1e-12: printed.append(f"{mine:.12g}")
h, T0, P0, L, g, Rs = v("I-H"), v("I-T0"), v("I-P0"), v("I-LAPSE"), v("I-G"), v("I-RSPEC")
T = T0 - L * h; p = P0 * (T / T0) ** (g / (L * Rs)); rho = p / (Rs * T)
R = v("I-R"); V = 4 / 3 * math.pi * R ** 3; lift = rho * V; A = 4 * math.pi * R ** 2
E, rAl, nu = v("I-E"), v("I-RHO-AL"), v("I-NU"); sig = float(CUR["sigma_Pa"])
for k, mine in (("T_K", T), ("p_ext_Pa", p), ("rho_kg_m3", rho), ("volume_m3", V), ("lift_kg", lift)): cmp(f"atm {k}", mine, RES["atmosphere"][k])
tf0, c0, rc, kd, J2, S2, G2 = v("I-TF", "P2"), v("I-CORE-T", "P2"), v("I-RHO-CORE", "P2"), v("I-KD", "P2"), v("I-J2", "P2"), v("I-SYS2", "P2"), v("I-GAS2", "P2")
cmp("core density", rc, RES["core_density_kg_m3"])
M = (lift - S2 - G2) / (1 + J2)                       # faces + core mass at the ceiling
def row(f, c):
    m = {"faces": 2 * rAl * A * f, "core": rc * A * c}; m["joints"] = J2 * (m["faces"] + m["core"]); m["systems_payload"] = S2; m["residual_gas"] = G2
    d = c + f; pb = kd * 4 * f * d * E / (R ** 2 * math.sqrt(1 - nu ** 2)); py = 4 * sig * f / R
    sm = p * R / (4 * f)                               # membrane stress at external pressure
    return {"f": f, "c": c, "d": d, "m": m, "tot": sum(m.values()), "pb": pb, "py": py, "sm": sm,
            "Ereq": E * p / pb, "sreq": sig * p / py, "Gc": p * R / (2 * d), "EcGc": (2 * sm) ** 3 / E}
k = M / (2 * rAl * A * tf0 + rc * A * c0)
pts = {"P2-C": row(tf0, (M - 2 * rAl * A * tf0) / (rc * A)), "P2-K": row(k * tf0, k * c0), "P2-E": row(M / 2 / (2 * rAl * A), M / 2 / (rc * A))}
for pid, x in pts.items():
    r = next(y for y in RES["rows"] if y["point_id"] == pid); gm = r["geometry"]
    cmp(f"{pid} tf", x["f"], gm["tf_m"]); cmp(f"{pid} core", x["c"], gm["core_m"]); cmp(f"{pid} d", x["d"], gm["d_m"])
    for kk, mm in x["m"].items(): cmp(f"{pid} mass {kk}", mm, r["masses_kg"][kk])
    cmp(f"{pid} all mass", x["tot"], r["all_mass_kg"]); cmp(f"{pid} lift", lift, r["lift_equivalent_mass_kg"])
    mg = (lift - x["tot"]) / lift; assert abs(mg) < 1e-12 and abs(r["float_margin"]) < 1e-12, (pid, mg, r["float_margin"])
    cmp(f"{pid} buckling limit", x["pb"], r["limits_Pa"]["knocked_down_buckling"]); cmp(f"{pid} yield limit", x["py"], r["limits_Pa"]["aluminum_yield"])
    gov = "knocked_down_buckling" if x["pb"] < x["py"] else "aluminum_yield"; assert gov == r["governing_limit"], (pid, gov)
    cmp(f"{pid} collapse", min(x["pb"], x["py"]), r["collapse_pressure_Pa"]); cmp(f"{pid} p_ext", p, r["external_pressure_Pa"])
    cmp(f"{pid} buckling SF", x["pb"] / p, r["buckling_SF"]); cmp(f"{pid} strength SF", x["py"] / p, r["strength_SF_QUESTIONABLE"])
    cmp(f"{pid} least SF", min(x["pb"], x["py"]) / p, r["least_stated_modeled_SF"])
    cmp(f"{pid} E required", x["Ereq"], r["E_required_Pa"]); cmp(f"{pid} sigma required", x["sreq"], r["sigma_required_Pa"])
    cmp(f"{pid} membrane stress", x["sm"], r["membrane_stress_at_external_Pa"])
    cmp(f"{pid} E factor", p / x["pb"], r["factors"]["knocked_down_buckling"]["factor"]); cmp(f"{pid} yield factor", p / x["py"], r["factors"]["aluminum_yield"]["factor"])
    t = r["omitted_targets_QUESTIONABLE"]
    cmp(f"{pid} Gc crimp", x["Gc"], t["Gc_for_crimp_at_external_Pa"]); cmp(f"{pid} EcGc", x["EcGc"], t["Ec_times_Gc_Pa2"]); cmp(f"{pid} equal sqrt", math.sqrt(x["EcGc"]), t["equal_Ec_Gc_assumption_Pa"])
    assert t.get("core_crush") == "NO_FORMULA_IN_BRIEF"; assert r.get("tag") == "QUESTIONABLE"
    assert "core_shear" in CUR["omitted_from_stated_SF"] and "face_wrinkling" in CUR["omitted_from_stated_SF"] and "core_crush" in CUR["omitted_from_stated_SF"]
    print(f"{pid}: tf {x['f']!r} core {x['c']!r} buckSF {x['pb']/p!r} strSF {x['py']/p!r} Ereq {x['Ereq']:.6g} sreq {x['sreq']:.6g} Gc {x['Gc']:.6g} EcGc {x['EcGc']:.6g}")
# the P2-A comparison: MAINLINE-002's closed form, against sealed MAINLINE-002 RESULTS and against this card's comparison block
tfa = (M - rc * A * c0) / (2 * rAl * A); a = row(tfa, c0); ca = RES["comparison_P2A"]; r2 = next(y for y in R2["rows"] if y["point_id"] == "P2-A")
cmp("P2-A tf vs card", tfa, ca["tf_m"]); cmp("P2-A core vs card", c0, ca["core_m"])
cmp("P2-A buckling SF vs card", a["pb"] / p, ca["buckling_SF"]); cmp("P2-A strength SF vs card", a["py"] / p, ca["strength_SF_QUESTIONABLE"])
cmp("P2-A E factor vs card", p / a["pb"], ca["E_factor"]); cmp("P2-A strength factor vs card", p / a["py"], ca["strength_factor"])
cmp("P2-A buckling limit vs sealed 002", a["pb"], r2["limits_Pa"]["knocked_down_buckling"]); cmp("P2-A yield limit vs sealed 002", a["py"], r2["limits_Pa"]["aluminum_yield"])
cmp("P2-A all mass vs sealed 002", a["tot"], r2["all_mass_kg"])
print(f"compared {n[0]} numbers at rel {TOL}: MISMATCHES {len(bad)}"); [print("  MISMATCH", b) for b in bad]
miss = sorted({x for x in printed if x not in card}); print(f"card print: {len(set(printed))} of my values at %.12g; absent from CARD.md: {len(miss)} {miss[:15]}")
print("premise:", CUR.get("sigma_tag"), CUR.get("sigma_transfer"), "| baseline rows", len(rows), "untagged", [r_["input_id"] for r_ in rows if r_.get("QUESTIONABLE_tag") != "QUESTIONABLE"], "unsourced", [r_["input_id"] for r_ in rows if not str(r_.get("source_reference_or_explicit_assumption_basis") or "").strip()])
print("NFI rows", len(nfi), [x.get("NFI_id") for x in nfi])
for x in nfi:
    if x.get("NFI_id") in ("NFI-AL-YIELD-CARRY", "NFI-KD") or re.search(r"scale", json.dumps(x)): print("  NFI", json.dumps(x)[:900])
