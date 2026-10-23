#!/usr/bin/env python3
"""MAINLINE-008b: the 008 material gap table updated with every filed card.

Own arithmetic from pinned inputs (COMMON.md case + filed cards 008, 004b, 005, 007).
Every number traces to an input and a stated formula. Nothing is a certification.
"""
import json, math, datetime, os

W = os.path.dirname(os.path.abspath(__file__))
R008 = "evidence/b84f229e5f0e7f47-RESULTS.json"

# --- pinned case (COMMON.md, pinned by MAINLINE-001/002/003; sha256 8f359d6c...) ---
R = 10.0                      # m, external radius
p = 95460.83791390515         # Pa, 500 m ISA external pressure
E_al = 68.9e9                 # Pa
nu = 0.33
sigma_al = 276e6              # Pa, QUESTIONABLE tensile yield transferred to compression
rho_al = 2700.0               # kg/m3

# --- pinned P2-E row (004b/005/007 agree; 008 rows_from) ---
tf_al_P2E = 0.000336094970395        # m
sep_P2E = 0.113768147479             # m, face separation (d+tf form)
SF_b_al_P2E_020_sealed = 0.233885578993
SF_y_al_P2E_sealed = 0.388692217064

# --- pinned knockdown levels (004b CARD.md, sha256 a97d2d3c...) ---
KD = {
    "conservative_SP-8032": 0.140725695373,  # per-row sealed SP-8032 for P2-E
    "central_0.20": 0.20,                    # Wagner 2020 eq(7) ~0.2; Sim 2024 dimple 0.20
    "optimistic_0.90": 0.90,                 # Wagner 2020 Table 3 row 12 (Krenzke&Kiernan)
}
SF_b_al_P2E_sealed = {   # 004b sealed aluminium P2-E buckling SF per level (cross-check)
    "conservative_SP-8032": 0.164568553708,
    "central_0.20": 0.233885578993,
    "optimistic_0.90": 1.05248510547,
}

# --- pinned required figures, 005 CARD.md (sha256 2c4ebdd5...), all kd 0.2 ---
REQ_P1 = {"E_over_rho2_Pa_m6_kg2": 1.0924e7, "sigma_over_rho_Pa_m3_kg": 2.5254e5}          # row P1, t=0.7 mm
REQ_P1A = {"E_over_rho2_Pa_m6_kg2": 3.3904e6, "sigma_over_rho_Pa_m3_kg": 1.4069e5}        # row P1-A
REQ_P3 = {"E_over_rho_Pa_m3_kg": 7.6841e8, "sigma_over_rho_Pa_m3_kg": 1.4428e6}           # row P3, tw=1 mm
REQ_P3A = {"E_over_rho_Pa_m3_kg": 2.6575e8, "sigma_over_rho_Pa_m3_kg": 4.4087e5}          # row P3-A

# --- pinned 007 light-core rows (007 CARD.md, sha256 bbff5c7a...), Al faces, kd 0.2 ---
ROWS_007 = {
    "007-4kg-leastfactor": {"rho_core": 4.0, "tf_al": 0.000532532408361, "sep": 0.189070201186,
                             "SF_b_al": 0.615871169453, "SF_y_al": 0.615871169453},
    "007-4kg-bucklingmax": {"rho_core": 4.0, "tf_al": 0.000336344114183, "sep": 0.453728210033,
                             "SF_b_al": 0.933469986989, "SF_y_al": 0.388980350657},
    "007-1kg-leastfactor": {"rho_core": 1.0, "tf_al": 0.000637294958154, "sep": 0.189070201186,
                             "SF_b_al": 0.737028554512, "SF_y_al": 0.737028554512},
    "007-1kg-bucklingmax": {"rho_core": 1.0, "tf_al": 0.000336157221732, "sep": 1.81491284013,
                             "SF_b_al": 3.73180518599, "SF_y_al": 0.388764210437},
}

# --- pinned catalog cores (007), QUESTIONABLE Ec*Gc products, Pa^2 ---
CORES = [
    {"name": "Hexcel HRH-10-4.8-32", "rho": 32, "EcGc": 1.064e15,
     "src": "Hexcel HexWeb HRH-10 datasheet"},
    {"name": "Divinycell H35", "rho": 38, "EcGc": 4.8e14,
     "src": "DIAB Divinycell H rev9 SI"},
    {"name": "Hexcel HRH-10-6.4-24", "rho": 24, "EcGc": 3.69e14,
     "src": "Hexcel HexWeb HRH-10 datasheet"},
    {"name": "ROHACELL 31 IG-F", "rho": 32, "EcGc": 2.21e14,
     "src": "Evonik ROHACELL IG-F Apr 2022"},
]
BEST_CORE = max(CORES, key=lambda c: c["EcGc"])

checks = []
def chk(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})

# --- reproduce the P2-E aluminium row from the COMMON formulas ---
def pb_sandwich(kd, tf, sep, E): return kd * 4.0 * tf * sep * E / (R * R * math.sqrt(1 - nu * nu))
def SF_y_sandwich(tf, sigma): return 4.0 * sigma * tf / R / p

sf_b_repro = pb_sandwich(0.2, tf_al_P2E, sep_P2E, E_al) / p
sf_y_repro = SF_y_sandwich(tf_al_P2E, sigma_al)
chk("reproduce SF_b_al P2-E kd0.2 from formula", abs(sf_b_repro - SF_b_al_P2E_020_sealed) < 1e-11,
    f"{sf_b_repro:.12f} vs sealed {SF_b_al_P2E_020_sealed}")
chk("reproduce SF_y_al P2-E from formula", abs(sf_y_repro - SF_y_al_P2E_sealed) < 1e-11,
    f"{sf_y_repro:.12f} vs sealed {SF_y_al_P2E_sealed}")

# --- reproduce 004b's Al buckling SF at each kd level (SF scales linearly with kd) ---
for lvl, kd in KD.items():
    v = SF_b_al_P2E_020_sealed * kd / 0.2
    chk(f"Al P2-E SF_b at kd={kd}", abs(v - SF_b_al_P2E_sealed[lvl]) < 1e-9,
        f"{v:.12f} vs 004b {SF_b_al_P2E_sealed[lvl]}")

# --- reproduce 007 least-factor row SF_y from formula (spot check both rows) ---
for k in ("007-4kg-leastfactor", "007-1kg-leastfactor"):
    r = ROWS_007[k]
    v = SF_y_sandwich(r["tf_al"], sigma_al)
    chk(f"reproduce {k} SF_y_al", abs(v - r["SF_y_al"]) / r["SF_y_al"] < 1e-5,
        f"{v:.12f} vs 007 {r['SF_y_al']}")

# --- reproduce 005 P1 required figures from the P1 formula (t = 0.7 mm, kd 0.2) ---
t_P1 = 0.0007
E_req_P1 = p * math.sqrt(3 * (1 - nu * nu)) / (0.2 * 2.0 * (t_P1 / R) ** 2)
sig_req_P1 = p * R / (2 * t_P1)
chk("reproduce 005 P1 E required", abs(E_req_P1 / rho_al**2 - REQ_P1["E_over_rho2_Pa_m6_kg2"]) / REQ_P1["E_over_rho2_Pa_m6_kg2"] < 5e-4,
    f"E/ho^2 {E_req_P1/rho_al**2:.4e} vs {REQ_P1['E_over_rho2_Pa_m6_kg2']:.4e}")
chk("reproduce 005 P1 sigma required", abs(sig_req_P1 / rho_al - REQ_P1["sigma_over_rho_Pa_m3_kg"]) / REQ_P1["sigma_over_rho_Pa_m3_kg"] < 5e-4,
    f"sigma/rho {sig_req_P1/rho_al:.4e} vs {REQ_P1['sigma_over_rho_Pa_m3_kg']:.4e}")

# --- load the 15 filed candidates (008 RESULTS.json, pinned read-only) ---
d008 = json.load(open(R008))
cands = d008["candidates_ranked_by_least_SF_P2E"]
chk("candidate count", len(cands) == 15, f"{len(cands)}")

er_al = E_al / rho_al
sr_al = sigma_al / rho_al
er2_al = E_al / rho_al**2

def wrinkling(tf_c, E_f, sigma_f=None):
    """req Ec*Gc = (2 sigma_f)^3 / E_f, sigma_f = pR/(4 tf)."""
    if sigma_f is None:
        sigma_f = p * R / (4.0 * tf_c)
    return sigma_f, (2.0 * sigma_f) ** 3 / E_f

rows_out = []
for c in cands:
    rho, E, sig = float(c["rho"]), float(c["E_GPa"]) * 1e9, float(c["sigma_c_MPa"]) * 1e6
    er, sr, er2 = E / rho, sig / rho, E / rho**2
    rE, rS, rE2 = er / er_al, sr / sr_al, er2 / er2_al
    # P2-E at the three kd levels (item 1) + yield (kd-independent)
    p2e = {lvl: SF_b_al_P2E_020_sealed * (kd / 0.2) * rE for lvl, kd in KD.items()}
    sf_y_p2e = SF_y_al_P2E_sealed * rS
    tf_c_P2E = tf_al_P2E * rho_al / rho
    # cross-check against 008's own filed P2-E numbers (kd 0.2)
    filed = c["rows"]["P2-E"]
    chk(f"008 P2-E agreement {c['name'][:24]}",
        abs(p2e["central_0.20"] - filed["SF_b"]) < 1e-9 and abs(sf_y_p2e - filed["SF_y"]) < 1e-9,
        f"SF_b {p2e['central_0.20']:.10f}/{filed['SF_b']:.10f} SF_y {sf_y_p2e:.10f}/{filed['SF_y']:.10f}")
    # P1 and P3 columns (item 2), base rows; -A variants carried beside
    sf_b_P1 = er2 / REQ_P1["E_over_rho2_Pa_m6_kg2"]
    sf_y_P1 = sr / REQ_P1["sigma_over_rho_Pa_m3_kg"]
    sf_b_P1A = er2 / REQ_P1A["E_over_rho2_Pa_m6_kg2"]
    sf_y_P1A = sr / REQ_P1A["sigma_over_rho_Pa_m3_kg"]
    sf_b_P3 = er / REQ_P3["E_over_rho_Pa_m3_kg"]
    sf_y_P3 = sr / REQ_P3["sigma_over_rho_Pa_m3_kg"]
    sf_b_P3A = er / REQ_P3A["E_over_rho_Pa_m3_kg"]
    sf_y_P3A = sr / REQ_P3A["sigma_over_rho_Pa_m3_kg"]
    # wrinkling on P2-E (item 4)
    sf_f_p2e, req_p2e = wrinkling(tf_c_P2E, E)
    # 007 light-core rows (item 3), both splits, with wrinkling on each row's tf
    r007 = {}
    for k, r in ROWS_007.items():
        tf_c = r["tf_al"] * rho_al / rho
        sf_f, req = wrinkling(tf_c, E)
        r007[k] = {
            "tf_c_m": tf_c, "SF_b_at_020": r["SF_b_al"] * rE, "SF_y": r["SF_y_al"] * rS,
            "sigma_f_Pa": sf_f, "req_EcGc_Pa2": req,
            "SF_wr_best_catalog": (BEST_CORE["EcGc"] / req) ** (1.0 / 3.0),
            "wrinkle_miss_vs_best_catalog": req / BEST_CORE["EcGc"],
        }
    row = {
        "name": c["name"], "tag": c["tag"], "rho": rho, "E_GPa": c["E_GPa"], "sigma_c_MPa": c["sigma_c_MPa"],
        "source": c["source"],
        "E_over_rho_Pa_per_kg_m3": er, "sigma_over_rho_Pa_per_kg_m3": sr, "E_over_rho2_Pa_m6_kg2": er2,
        "P2E": {
            "tf_at_equal_face_mass_m": tf_c_P2E,
            "SF_b_kd_conservative_SP8032": p2e["conservative_SP-8032"],
            "SF_b_kd_020": p2e["central_0.20"],
            "SF_b_kd_090": p2e["optimistic_0.90"],
            "SF_y": sf_y_p2e,
        },
        "P1_base": {"SF_b": sf_b_P1, "SF_y": sf_y_P1},
        "P1A": {"SF_b": sf_b_P1A, "SF_y": sf_y_P1A},
        "P3_base": {"SF_b": sf_b_P3, "SF_y": sf_y_P3},
        "P3A": {"SF_b": sf_b_P3A, "SF_y": sf_y_P3A},
        "WRINKLING_P2E": {
            "sigma_f_Pa": sf_f_p2e, "req_EcGc_Pa2": req_p2e,
            "SF_wr_best_catalog": (BEST_CORE["EcGc"] / req_p2e) ** (1.0 / 3.0),
            "wrinkle_miss_vs_best_catalog": req_p2e / BEST_CORE["EcGc"],
            "margins_vs_each_catalog": {cc["name"]: cc["EcGc"] / req_p2e for cc in CORES},
        },
        "rows_007": r007,
    }
    # overall at kd 0.20 on P2-E, wrinkling against the best catalog core
    least_p2e = min(p2e["central_0.20"], sf_y_p2e, row["WRINKLING_P2E"]["SF_wr_best_catalog"])
    lim = ("buckling E/rho (kd 0.20)" if least_p2e == p2e["central_0.20"]
           else "yield sigma_c/rho" if least_p2e == sf_y_p2e
           else "face wrinkling vs best catalog core Ec*Gc")
    row["overall_P2E_kd020"] = {
        "least_SF": least_p2e, "limiting_property": lim, "factor_needed": 1.0 / least_p2e,
    }
    # overall at kd 0.20 on each 007 least-factor row
    for k in ("007-4kg-leastfactor", "007-1kg-leastfactor"):
        rr = row["rows_007"][k]
        least = min(rr["SF_b_at_020"], rr["SF_y"], rr["SF_wr_best_catalog"])
        lim = ("buckling E/rho (kd 0.20)" if least == rr["SF_b_at_020"]
               else "yield sigma_c/rho" if least == rr["SF_y"]
               else "face wrinkling vs best catalog core Ec*Gc")
        rr["overall_kd020"] = {"least_SF": least, "limiting_property": lim, "factor_needed": 1.0 / least}
    rows_out.append(row)

def top3(rows, key):
    rs = sorted(rows, key=lambda r: r[key]["least_SF"], reverse=True)
    return [{ "name": r["name"], "tag": r["tag"], "least_SF": r[key]["least_SF"],
              "limiting_property": r[key]["limiting_property"], "factor_needed": r[key]["factor_needed"],
              "SF_b_kd020": (r["P2E"]["SF_b_kd_020"] if key == "overall_P2E_kd020" else r["rows_007"][key]["SF_b_at_020"]),
              "SF_y": r["P2E"]["SF_y"] if key == "overall_P2E_kd020" else r["rows_007"][key]["SF_y"],
              "SF_wr": r["WRINKLING_P2E"]["SF_wr_best_catalog"] if key == "overall_P2E_kd020" else r["rows_007"][key]["SF_wr_best_catalog"],
            } for r in rs]

best = {
    "P2E_kd020_all": top3(rows_out, "overall_P2E_kd020"),
    "P2E_kd020_available_today": [t for t in top3(rows_out, "overall_P2E_kd020") if t["tag"] != "PROJECTION"],
    "row_007_1kg_leastfactor_all": top3(rows_out, "rows_007") if False else [
        { "name": r["name"], "tag": r["tag"], **r["rows_007"]["007-1kg-leastfactor"]["overall_kd020"],
          "SF_b_kd020": r["rows_007"]["007-1kg-leastfactor"]["SF_b_at_020"],
          "SF_y": r["rows_007"]["007-1kg-leastfactor"]["SF_y"],
          "SF_wr": r["rows_007"]["007-1kg-leastfactor"]["SF_wr_best_catalog"]}
        for r in sorted(rows_out, key=lambda r: r["rows_007"]["007-1kg-leastfactor"]["overall_kd020"]["least_SF"], reverse=True)],
    "row_007_4kg_leastfactor_all": [
        { "name": r["name"], "tag": r["tag"], **r["rows_007"]["007-4kg-leastfactor"]["overall_kd020"],
          "SF_b_kd020": r["rows_007"]["007-4kg-leastfactor"]["SF_b_at_020"],
          "SF_y": r["rows_007"]["007-4kg-leastfactor"]["SF_y"],
          "SF_wr": r["rows_007"]["007-4kg-leastfactor"]["SF_wr_best_catalog"]}
        for r in sorted(rows_out, key=lambda r: r["rows_007"]["007-4kg-leastfactor"]["overall_kd020"]["least_SF"], reverse=True)],
}
best["row_007_1kg_leastfactor_available_today"] = [t for t in best["row_007_1kg_leastfactor_all"] if t["tag"] != "PROJECTION"][:3]
best["row_007_4kg_leastfactor_available_today"] = [t for t in best["row_007_4kg_leastfactor_all"] if t["tag"] != "PROJECTION"][:3]
best["P2E_kd020_all"] = best["P2E_kd020_all"][:3]
best["P2E_kd020_available_today"] = best["P2E_kd020_available_today"][:3]
best["row_007_1kg_leastfactor_all"] = best["row_007_1kg_leastfactor_all"][:3]
best["row_007_4kg_leastfactor_all"] = best["row_007_4kg_leastfactor_all"][:3]

now = datetime.datetime.now().astimezone().isoformat()
out = {
    "schema": 1, "card": "MAINLINE-008b", "unit": "vacuum-mainline008b-table-update-1019",
    "status": "ESTIMATE",
    "started_at": "2026-10-19T23:08:47-07:00", "ended_at": now,
    "measurements_note": "Times are measurements only; no budget, no cap. Source reading preceded the start stamp.",
    "case": {"R_m": R, "p_external_Pa": p, "kd_levels": KD, "E_al_Pa": E_al, "nu": nu,
             "sigma_al_Pa": sigma_al, "rho_al": rho_al,
             "P2E_tf_al_m": tf_al_P2E, "P2E_sep_m": sep_P2E},
    "inputs": {
        "005_required_figures": {"P1": REQ_P1, "P1-A": REQ_P1A, "P3": REQ_P3, "P3-A": REQ_P3A},
        "007_rows": ROWS_007, "catalog_cores_EcGc_Pa2": CORES, "best_catalog_core": BEST_CORE["name"],
    },
    "formulas": {
        "SF_b_sandwich": "kd*4*tf*(d+tf)*E/(R^2*sqrt(1-nu^2))/p; at equal face mass scales as (E/rho)",
        "SF_y_sandwich": "4*sigma*tf/R/p; at equal face mass scales as (sigma_c/rho)",
        "kd_scaling": "SF_b(kd) = SF_b(0.2)*kd/0.2 (linear in kd; required E as 1/kd)",
        "P1_equal_mass": "at fixed shell mass t follows 1/rho: SF_b follows E/rho^2, SF_y follows sigma/rho (005)",
        "P3_equal_mass": "at fixed member mass and outer radius the wall follows 1/rho: SF_b follows E/rho, SF_y follows sigma/rho (005)",
        "wrinkling": "sigma_f = pR/(4*tf); sigma_wr = 0.5*(E_f*Ec*Gc)^(1/3); require Ec*Gc >= (2*sigma_f)^3/E_f; SF_wr = (avail/req)^(1/3)",
        "tf_equal_mass": "tf_c = tf_al * 2700/rho_c",
    },
    "checks": checks,
    "candidates": rows_out,
    "best_three": best,
    "catalog_cores_note": "All catalog Ec*Gc products QUESTIONABLE (007); HRH-10 sheets have no continuum Ec on the datasheets (007); no catalog structural core exists at 1-4 kg/m3 (007).",
}
json.dump(out, open(os.path.join(W, "RESULTS.json"), "w"), indent=1)
nfail = sum(1 for c in checks if not c["pass"])
print(f"checks: {len(checks)} total, {nfail} failed")
print("unit rows:", len(rows_out))
for k, v in best.items():
    print(f"== {k}")
    for t in v:
        print(f"   {t['least_SF']:.4f}  {t['name'][:44]:46s} lim={t['limiting_property']}")
