#!/usr/bin/env python3
"""Check of MAINLINE-020 (beryllium reality) behind its owner, codex ref-2b226fa1c9f1bf550d9b.

Own arithmetic from the pinned inputs. The owner's calculate.py is read for its formulas
(CHECK.md rule 2) and is never imported or run. Source values are re-read from the owner's
pinned PDFs with pdftotext. Writes RESULTS.json, NFI.json, INPUTS.json and CHECK.md here.
"""
import datetime
import hashlib
import json
import math
import re
import statistics
import subprocess
import time
from pathlib import Path

OWNER = Path("unpublished-local-ref:cf69b53e8e8dacbf"
             "mainline020-beryllium-reality-1019")
OWNER_NOTE = Path("unpublished-local-ref:7c7cb84a498750e6"
                  "mainline020-beryllium-reality-1019.md")
BRIEFS = Path("unpublished-local-ref:40621e2643eee247"
              "vacuum-overnight-briefs-1019")
REPORT = Path("unpublished-local-ref:c79a8645ca13b61d")
OUT = Path(__file__).resolve().parent
BRIEF_PINS = {  # from the order ord-admiral-rr2-check020-opus-65d1-1020
    "CHECK.md": ("03b357cbce6a591d1278c1e0b4c0606c52d876bdedd9f5727da3e5fab2a958c6", 799),
    "COMMON.md": ("8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5", 5874),
}

INCH = 0.0254                       # m, exact
LB_FT2 = 0.45359237 / 0.3048 ** 2   # kg/m2 per lb/ft2, exact definitions
REL = 1e-9                          # RESULTS.json agreement, relative to max(1, |value|)

# Positive real root of q^3 + q = 1 by Cardano: the inherited equibiaxial wrinkling factor.
_S = math.sqrt(0.25 + 1 / 27)
Q_BIAX = (0.5 + _S) ** (1 / 3) - (_S - 0.5) ** (1 / 3)

MODES = {"global": "global_buckling", "crimp": "core_shear_crimping",
         "face": "face_compression_or_joint_net_section", "wrinkle": "face_wrinkling",
         "crush": "core_crush", "dimple": "intracell_dimpling"}


def sha(path):
    blob = Path(path).read_bytes()
    return hashlib.sha256(blob).hexdigest(), len(blob)


def pin(path, role):
    h, n = sha(path)
    return {"path": str(path), "sha256": h, "bytes": n, "role": role}


def at(obj, path):
    for part in path.replace("]", "").replace("[", ".").split("."):
        obj = obj[int(part)] if part.isdigit() else obj[part]
    return obj


def sandwich(case, E, sig, nu, tf, d, core, eta=1.0):
    """CR-1457 screen as 009c5 and 014b state it; each face carries pR/(4 tf)."""
    R, p = case["R"], case["p"]
    h = d + tf
    s_mem = p * R / (4 * tf)
    s_ref = E * h / (R * math.sqrt(1 - nu * nu))
    s_crimp = h * h * core["Gc_Pa"] / (2 * tf * d)
    vc = s_ref / s_crimp
    kc, gam = (1 - vc / 4, case["kd"]) if vc <= 2 else (1 / vc, 1.0)
    sf = {
        "global": gam * kc * s_ref / s_mem,
        "crimp": s_crimp / s_mem,
        "face": eta * sig / s_mem,
        "wrinkle": Q_BIAX * 0.33 * math.sqrt(E * core["Ec_Pa"] * tf / d) / s_mem,
        "crush": core["crush_Pa"] / (p / 2),
        "dimple": 2 * E / (1 - nu * nu) * (tf / core["s_cell_m"]) ** 2 / s_mem,
    }
    least = min(sf.values())
    return {"least": least, "governs": [k for k, v in sf.items() if v - least < 1e-9], "sf": sf,
            "Vc": vc, "Kc": kc, "gamma": gam, "s_mem": s_mem, "tf": tf, "d": d}


def mass(case, rho_f, tf, rho_c, d):
    faces = 2 * case["A"] * rho_f * tf
    core = case["A"] * rho_c * d
    struct = faces + core
    joints = case["jf"] * struct
    total = struct + joints + case["sys"]
    return {"faces": faces, "core": core, "struct": struct, "joints": joints, "total": total,
            "payload": case["lift"] - total}


def pdf_text(name, first=None, last=None):
    cmd = ["pdftotext", "-layout"]
    if first:
        cmd += ["-f", str(first), "-l", str(last)]
    cmd += [str(OWNER / "sources" / name), "-"]
    raw = subprocess.run(cmd, capture_output=True, text=True).stdout  # NASA's PDF warns on stderr
    assert raw.strip(), cmd
    return " ".join(raw.split())


def decimals(printed):
    s = printed.replace(",", "")
    return len(s.split(".")[1]) if "." in s else 0


def number(printed):
    return float(printed.replace(",", "").replace("−", "-"))


def main():
    t0 = time.monotonic()
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # ---- pins: report artifacts, owner's input pins, briefs ----
    report = json.loads(REPORT.read_text())
    pins_ok = []
    for a in report["artifacts"]:
        h, n = sha(a["path"])
        pins_ok.append({"pin": "report artifact", "path": a["path"], "ok": h == a["sha256"] and n == a["bytes"]})
    I = json.loads((OWNER / "INPUTS.json").read_text())
    for p_ in I["input_pins"]:
        h, n = sha(p_["copy_path"])
        pins_ok.append({"pin": "owner input pin", "path": p_["copy_path"],
                        "ok": h == p_["sha256"] and n == p_["bytes"]})
    for name, (want, size) in BRIEF_PINS.items():
        h, n = sha(BRIEFS / name)
        pins_ok.append({"pin": "brief", "path": str(BRIEFS / name), "ok": h == want and n == size})

    # ---- case and lead point ----
    c = I["case"]
    case = {"R": c["radius_m"], "p": c["pressure_Pa"], "lift": c["lift_kg"], "sys": c["systems_kg"],
            "jf": c["joint_fraction"], "kd": c["kd"]}
    case["A"] = 4 * math.pi * case["R"] ** 2
    nu0 = c["inherited_nu"]
    tf, d = I["lead_point"]["tf_m"], I["lead_point"]["core_m"]
    core = I["lead_core"]
    faces = {f["name"]: f for f in I["faces"]}
    be = faces["Beryllium S-200F"]
    k13 = faces["CFRP quasi-isotropic K13D2U pitch/epoxy"]

    # ---- INPUTS against the intake copies they cite ----
    P9 = json.loads((OWNER / "intake/009c5/POINT.json").read_text())
    I14 = json.loads((OWNER / "intake/014b/INPUTS.json").read_text())
    R14 = json.loads((OWNER / "intake/014b/RESULTS.json").read_text())
    intake = []

    def same(what, a, b):
        ok = a == b if isinstance(a, str) else abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
        intake.append({"what": what, "INPUTS": a, "intake": b, "ok": ok})

    opt = P9["optimum"]
    same("lead tf_m = 009c5 optimum tf_m", tf, opt["tf_m"])
    same("lead core_m = 009c5 optimum core_m", d, opt["core_m"])
    same("lead expected SF = 009c5 least_SF", I["lead_point"]["expected_SF"], opt["least_SF"])
    same("lead expected faces = 009c5 masses faces", I["lead_point"]["expected_face_kg"], opt["masses_kg"]["faces"])
    same("lead face = 009c5 face", be["name"], P9["point"]["face"])
    same("lead core = 009c5 core", core["name"], P9["point"]["core"])
    same("pressure = 014b p_ext_Pa", case["p"], I14["p_ext_Pa"])
    same("lift = 014b lift_kg", case["lift"], I14["lift_kg"])
    same("nu = 014b nu_used_for_every_face", nu0, R14["nu_used_for_every_face"])
    same("structural ceiling = 014b structural_mass_kg", I["published_014b_structural_mass_kg"],
         R14["structural_mass_kg"])
    cores14 = {r["name"]: r for r in I14["cores_eligible"]}
    for row in [core] + [q["core"] for q in I["published_014b"][2:3]]:
        src = cores14[row["name"]]
        same(f'{row["name"]} rho', row["rho_kg_m3"], src["rho"])
        for k in ("Ec_Pa", "Gc_Pa", "crush_Pa", "s_cell_m"):
            same(f'{row["name"]} {k}', row[k], src[k])
    faces14 = {r["name"]: r for r in I14["faces"]}
    for f in I["faces"]:
        src = faces14[f["name"]]
        same(f'{f["name"]} rho', f["rho_kg_m3"], src["rho"])
        same(f'{f["name"]} E', f["E_Pa"], src["E_Pa"])
        same(f'{f["name"]} sigma', f["sigma_Pa"], src["sigma_Pa"])
        same(f'{f["name"]} tag', f["tag"], src["tag"])
    for q in I["published_014b"]:
        rows = [o for o in R14["optima"] if o["face"] == q["face"] and o["kd"] == 0.2]
        same(f'{q["face"]}: one 014b kd 0.20 row', float(len(rows)), 1.0)
        o = rows[0]
        same(f'{q["face"]} 014b core name', q["core"]["name"], o["core_name"])
        same(f'{q["face"]} 014b tf_m', q["tf_m"], o["tf_m"])
        same(f'{q["face"]} 014b core_m', q["core_m"], o["core_m"])
        same(f'{q["face"]} 014b least_SF', q["expected_SF"], o["least_SF"])
    ranking = sorted(((o["least_SF"], o["face"], o["face_tag"]) for o in R14["optima"] if o["kd"] == 0.2),
                     reverse=True)

    # ---- the lead point ----
    base = sandwich(case, be["E_Pa"], be["sigma_Pa"], nu0, tf, d, core)
    m = mass(case, be["rho_kg_m3"], tf, core["rho_kg_m3"], d)

    # ---- 1 supply and price ----
    sc = {s["name"]: s for s in I["procurement_scenarios"]}
    opt_s, con_s = sc["optimistic_budget"], sc["conservative_budget"]
    usgs = I["price_basis"]["USGS_2025_master_alloy_contained_Be_USD_per_kg"]
    supply, costs = [], []
    for s in (opt_s, con_s):
        for basis, mb in (("brief_reference_2100kg", 2100.0), ("pinned_lead_faces", m["faces"])):
            supply.append({"finished_share_percent": 100 * mb / s["mine_output_kg"],
                           "purchased_stock_kg": mb / s["yield"],
                           "purchased_share_percent": 100 * mb / s["yield"] / s["mine_output_kg"]})
            for grade in ("S200F", "SR200"):
                unit = s[grade + "_USD_per_kg"]
                costs.append({"finished_mass_times_unit_price_USD": mb * unit,
                              "purchased_stock_cost_USD": mb / s["yield"] * unit})

    # ---- 2 sheet, panels, gauge ----
    def panel(a, b):
        n = math.ceil(case["A"] / (a * b))
        L = case["A"] * (1 / a + 1 / b)          # each panel edge shared by two panels
        r = math.hypot(a, b) / 2
        return {"n": n, "edges": 2 * n, "L": L, "r": r,
                "sag": case["R"] - math.sqrt(case["R"] ** 2 - r * r),
                "bend": tf / (2 * case["R"]), "metric": r * r / (6 * case["R"] ** 2)}

    big = panel(I["panel_scenarios"][0]["width_m"], I["panel_scenarios"][0]["length_m"])
    small = panel(I["panel_scenarios"][1]["width_m"], I["panel_scenarios"][1]["length_m"])
    dt = I["gauge_tolerance_m"]
    gauge = []
    for off in (-dt, 0.0, dt):
        mg = mass(case, be["rho_kg_m3"], tf + off, core["rho_kg_m3"], d)
        gauge.append({"off": off, "m": mg, "modes": sandwich(case, be["E_Pa"], be["sigma_Pa"], nu0, tf + off, d, core)})

    # ---- 3 joining ----
    def seam(js):
        film = js["film_lb_ft2"] * LB_FT2
        w = js["doubler_width_m"]
        parts = {"Be_doublers": 2 * be["rho_kg_m3"] * tf * w,
                 "doubler_adhesive": 2 * film * w,
                 "core_gap_paste": js["paste_rho_kg_m3"] * js["core_gap_m"] * d,
                 "sealant": js["paste_rho_kg_m3"] * js["sealant_cross_section_total_m2"]}
        return film, parts, sum(parts.values())

    joins = []
    for pn in (big, small):
        for js in I["joint_scenarios"]:
            film, parts, per_m = seam(js)
            full = 2 * case["A"] * film
            total = full + pn["L"] * per_m
            new_total = m["struct"] + case["sys"] + total
            joins.append({"film": film, "parts": parts, "per_m": per_m, "full": full, "seam": pn["L"] * per_m,
                          "total": total, "over": total - m["joints"], "new_total": new_total,
                          "payload": case["lift"] - new_total, "frac": (case["lift"] - new_total) / case["lift"],
                          "eta_SF": sandwich(case, be["E_Pa"], be["sigma_Pa"], nu0, tf, d, core,
                                             eta=js["joint_efficiency"])["least"]})
    film_only = []
    for lbft2 in (0.015, 0.030, 0.045, 0.060):
        mf = 2 * case["A"] * lbft2 * LB_FT2
        film_only.append({"mass": mf, "pm": 2 * case["A"] * 0.005 * LB_FT2,
                          "payload": case["lift"] - (m["struct"] + case["sys"] + mf)})
    braze = []
    for bz in I["braze_scenarios"]:
        per_m = 2 * bz["added_area_per_skin_m2"] * bz["filler_rho_kg_m3"]
        braze.append({"per_m": per_m, "large": per_m * big["L"],
                      "eta_SF": sandwich(case, be["E_Pa"], be["sigma_Pa"], nu0, tf, d, core,
                                         eta=bz["joint_efficiency"])["least"]})

    # ---- 4 mechanical, thermal, cycles ----
    mech = [sandwich(case, q["E_Pa"], q["compression_proxy_Pa"], q["nu"], tf, d, core)
            for q in I["mechanical_scenarios"]]
    E_now = I["current_sheet_E_Pa"]
    thermal = []
    for q in I["thermal_scenarios"]:
        lam = math.sqrt(core["Gc_Pa"] / (E_now * tf * d))
        eps = q["delta_alpha_per_K"] * q["delta_T_K"]
        thermal.append({"lam": lam, "len": 1 / lam, "tau": eps * E_now * tf * lam,
                        "uni": E_now * eps, "bi": E_now * eps / (1 - 0.08)})
    cycles_exact = 30 * 365.25

    # ---- 6 fallbacks ----
    fixed = []
    for f in I["faces"]:
        md = sandwich(case, f["E_Pa"], f["sigma_Pa"], nu0, tf, d, core)
        mf = mass(case, f["rho_kg_m3"], tf, core["rho_kg_m3"], d)
        fixed.append({"face": f["name"], "modes": md, "m": mf,
                      "loss": base["least"] - md["least"], "loss_pct": 100 * (1 - md["least"] / base["least"])})
    pub = []
    for q in I["published_014b"]:
        f = faces[q["face"]]
        md = sandwich(case, f["E_Pa"], f["sigma_Pa"], nu0, q["tf_m"], q["core_m"], q["core"])
        mp = mass(case, f["rho_kg_m3"], q["tf_m"], q["core"]["rho_kg_m3"], q["core_m"])
        pub.append({"face": q["face"], "modes": md, "struct": mp["struct"]})
    for row in pub:
        row["loss"] = pub[0]["modes"]["least"] - row["modes"]["least"]
        row["loss_pct"] = 100 * (1 - row["modes"]["least"] / pub[0]["modes"]["least"])
    scale = m["struct"] / I["published_014b_structural_mass_kg"]
    resized = []
    for q in I["published_014b"]:
        f = faces[q["face"]]
        resized.append(sandwich(case, f["E_Pa"], f["sigma_Pa"], nu0, q["tf_m"] * scale, q["core_m"] * scale, q["core"]))

    # ---- card text: every printed number, at the precision printed ----
    card = (OWNER / "CARD.md").read_text()
    method = (OWNER / "METHOD.md").read_text()
    body = report["body"]
    k13_fixed = fixed[1]
    rows = [
        # (row, field, printed, mine, where)
        ("Header", "face thickness, mm", "0.75243", tf * 1e3, card),
        ("Header", "core thickness, mm", "20.6423", d * 1e3, card),
        ("Header", "face mass, kg", "3,498.47", m["faces"], card),
        ("Header", "total mass, kg", "4,644.97", m["total"], card),
        ("Header", "payload, kg", "244.47", m["payload"], card),
        ("Header", "lift, kg", "4,889.44", case["lift"], card),
        ("Header", "least SF", "0.650412", base["least"], card),
        ("Header", "capacity shortfall, %", "34.96", 100 * (1 - base["least"]), card),
        ("Header", "capacity factor to SF 1", "1.5375", 1 / base["least"], card),
        ("1 Supply", "2,100 kg share of 2024 output, %", "0.485", 100 * 2100 / opt_s["mine_output_kg"], card),
        ("1 Supply", "2,100 kg share of 2025 output, %", "0.488", 100 * 2100 / con_s["mine_output_kg"], card),
        ("1 Supply", "face share of 2024 output, %", "0.808", 100 * m["faces"] / opt_s["mine_output_kg"], card),
        ("1 Supply", "face share of 2025 output, %", "0.814", 100 * m["faces"] / con_s["mine_output_kg"], card),
        ("1 Price", "S-200F optimistic, $/kg (3 x USGS)", "4,800", 3 * usgs, card),
        ("1 Price", "S-200F conservative, $/kg (6 x USGS)", "9,600", 6 * usgs, card),
        ("1 Price", "sheet optimistic, $/kg (6 x USGS)", "9,600", 6 * usgs, card),
        ("1 Price", "sheet conservative, $/kg (15 x USGS)", "24,000", 15 * usgs, card),
        ("1 Cost", "actual faces, sheet stock at 85% yield, $m", "39.51",
         m["faces"] / opt_s["yield"] * opt_s["SR200_USD_per_kg"] / 1e6, card),
        ("1 Cost", "actual faces, sheet stock at 50% yield, $m", "167.93",
         m["faces"] / con_s["yield"] * con_s["SR200_USD_per_kg"] / 1e6, card),
        ("1 Cost", "2,100 kg, sheet stock at 85% yield, $m", "23.72",
         2100 / opt_s["yield"] * opt_s["SR200_USD_per_kg"] / 1e6, card),
        ("1 Cost", "2,100 kg, sheet stock at 50% yield, $m", "100.80",
         2100 / con_s["yield"] * con_s["SR200_USD_per_kg"] / 1e6, card),
        ("2 Sheet", "maximum stock width, mm (24 in)", "609.6", 24 * INCH * 1e3, card),
        ("2 Sheet", "maximum stock length, mm (72 in)", "1,828.8", 72 * INCH * 1e3, card),
        ("2 Sheet", "small planning panel width, mm (12 in)", "304.8", 12 * INCH * 1e3, card),
        ("2 Panels", "panels per skin, large", "1,128", big["n"], card),
        ("2 Panels", "panels per skin, small", "6,764", small["n"], card),
        ("2 Panels", "edge joints per skin, large", "2,256", big["edges"], card),
        ("2 Panels", "edge joints per skin, small", "13,528", small["edges"], card),
        ("2 Seams", "coincident hull seam, large, km", "2.749", big["L"] / 1e3, card),
        ("2 Seams", "coincident hull seam, small, km", "6.184", small["L"] / 1e3, card),
        ("2 Shape", "flat-panel corner sag, large, mm", "46.56", big["sag"] * 1e3, card),
        ("2 Shape", "flat-panel corner sag, small, mm", "5.81", small["sag"] * 1e3, card),
        ("2 Flatness", "Type 3, mm per foot (0.030 in)", "0.762", 0.030 * INCH * 1e3, card),
        ("2 Gauge", "thickness tolerance, mm (0.004 in)", "0.1016", 0.004 * INCH * 1e3, card),
        ("2 Gauge", "least SF at local low gauge", "0.52323", gauge[0]["modes"]["least"], card),
        ("2 Gauge", "face mass added at uniform high gauge, kg", "472.40",
         gauge[2]["m"]["faces"] - m["faces"], card),
        ("3 Joining", "least SF at eta 0.90", "0.65041", joins[0]["eta_SF"], card),
        ("3 Joining", "least SF at eta 0.60", "0.53535", joins[1]["eta_SF"], card),
        ("3 Joining", "seam mass, optimistic splice, kg per hull-seam m", "0.218", joins[0]["per_m"], card),
        ("3 Joining", "seam mass, conservative splice, kg per hull-seam m", "0.483", joins[1]["per_m"], card),
        ("3 Joining", "face/core film at 0.030 lb/ft2, kg", "368.13", joins[0]["full"], card),
        ("3 Joining", "face/core film at 0.060 lb/ft2, kg", "736.25", joins[1]["full"], card),
        ("3 Joining", "large-panel optimistic joining total, kg", "968.20", joins[0]["total"], card),
        ("3 Joining", "small-panel conservative joining total, kg", "3,722.00", joins[3]["total"], card),
        ("3 Joining", "inherited 5% joint allowance, kg", "216.43", m["joints"], card),
        ("3 Joining", "payload, large-panel optimistic, kg", "−507.30", joins[0]["payload"], card),
        ("3 Joining", "payload, small-panel conservative, kg", "−3,261.10", joins[3]["payload"], card),
        ("3 Braze", "filler, optimistic, kg per hull-seam m", "0.0054", braze[0]["per_m"], card),
        ("3 Braze", "filler, conservative, kg per hull-seam m", "0.020", braze[1]["per_m"], card),
        ("4 Mechanical", "least SF at E 290 GPa (wrinkling)", "0.63631", mech[1]["least"], card),
        ("4 Mechanical", "least SF at 0.8 E and 0.7 x 241 MPa", "0.53188", mech[3]["least"], card),
        ("4 Thermal", "peak shear, 5 ppm/K x 30 K, MPa", "0.0577", thermal[0]["tau"] / 1e6, card),
        ("4 Thermal", "peak shear, 20 ppm/K x 60 K, MPa", "0.4616", thermal[1]["tau"] / 1e6, card),
        ("4 Fatigue", "daily cycles in 30 years (ceiling of 30 x 365.25)", "10,958", math.ceil(cycles_exact), card),
        ("4 Fatigue", "membrane compressive demand, MPa", "317", base["s_mem"] / 1e6, card),
        ("6 Fallback", "K13D2U at its published 014b design, SF", "0.65193", pub[1]["modes"]["least"], card),
        ("6 Fallback", "Be at its published 014b design, SF", "0.68534", pub[0]["modes"]["least"], card),
        ("6 Fallback", "K13D2U loss against 014b Be, absolute", "0.03341", pub[1]["loss"], card),
        ("6 Fallback", "K13D2U loss against 014b Be, %", "4.87", pub[1]["loss_pct"], card),
        ("6 Fallback", "M55J at its published design, SF", "0.59349", pub[2]["modes"]["least"], card),
        ("6 Fallback", "M55J loss, %", "13.40", pub[2]["loss_pct"], card),
        ("6 Fallback", "AlBeMet at its published design, SF", "0.55399", pub[3]["modes"]["least"], card),
        ("6 Fallback", "AlBeMet loss, %", "19.16", pub[3]["loss_pct"], card),
        ("6 Fallback", "K13D2U at the 009c5 geometry, SF", "0.54147", k13_fixed["modes"]["least"], card),
        ("6 Fallback", "K13D2U at the 009c5 geometry, loss %", "16.75", k13_fixed["loss_pct"], card),
        ("6 Fallback", "K13D2U at the 009c5 geometry, payload kg", "443.03", k13_fixed["m"]["payload"], card),
        ("6 Fallback", "K13D2U published design resized to the 5% budget, SF", "0.61865", resized[1]["least"], card),
        ("METHOD", "film at 0.030 lb/ft2, kg/m2", "0.14647", joins[0]["film"], method),
        ("METHOD", "film at 0.060 lb/ft2, kg/m2", "0.29295", joins[1]["film"], method),
        ("METHOD", "film product tolerance, both interfaces, kg", "61.35", film_only[0]["pm"], method),
        ("METHOD", "0.015 lb/ft2 film, both interfaces, kg", "184.06", film_only[0]["mass"], method),
        ("METHOD", "optimistic joining over the allowance, kg", "751.77", joins[0]["over"], method),
        ("METHOD", "shear-lag transfer length, m", "0.567", thermal[0]["len"], method),
        ("Report", "face mass, kg", "3498.47", m["faces"], body),
        ("Report", "least SF", "0.650412", base["least"], body),
        ("Report", "capacity shortfall, %", "34.96", 100 * (1 - base["least"]), body),
        ("Report", "large-panel optimistic joining total, kg", "968.20", joins[0]["total"], body),
        ("Report", "payload, large-panel optimistic, kg", "-507.30", joins[0]["payload"], body),
        ("Report", "K13D2U at the 009c5 geometry, SF", "0.54147", k13_fixed["modes"]["least"], body),
        ("Report", "K13D2U resized to the 5% budget, SF", "0.61865", resized[1]["least"], body),
    ]
    compared = []
    for row, field, printed, mine, where in rows:
        k = decimals(printed)
        compared.append({"row": row, "field": field, "card": printed, "mine": mine,
                         "mine_at_card_precision": f"{round(mine, k):,.{k}f}",
                         "printed_in_text": printed.lstrip("−-") in where,
                         "match": round(mine, k) == round(number(printed), k)})

    # inputs echoed in the card text (no arithmetic, only transcription)
    echoes = [
        ("4,800/$9,600", "price_basis bulk multipliers", I["price_basis"]["bulk_multipliers_assumed"] == [3, 6]),
        ("85%/50%", "procurement yields", (opt_s["yield"], con_s["yield"]) == (0.85, 0.5)),
        ("60/120 mm", "doubler widths", [j["doubler_width_m"] for j in I["joint_scenarios"]] == [0.06, 0.12]),
        ("90%/60%", "joint efficiencies", [j["joint_efficiency"] for j in I["joint_scenarios"]] == [0.9, 0.6]),
        ("0.030/0.060 lb/ft", "film weights", [j["film_lb_ft2"] for j in I["joint_scenarios"]] == [0.03, 0.06]),
        ("0.8/0.7", "retention factors", (I["mechanical_scenarios"][3]["E_Pa"] / E_now,
                                          I["mechanical_scenarios"][3]["compression_proxy_Pa"] / 241e6) ==
         (0.8, 0.7) or (abs(I["mechanical_scenarios"][3]["E_Pa"] - 0.8 * E_now) < 1 and
                        abs(I["mechanical_scenarios"][3]["compression_proxy_Pa"] - 0.7 * 241e6) < 1)),
        ("5/20 ppm/K", "thermal mismatch", [q["delta_alpha_per_K"] for q in I["thermal_scenarios"]] == [5e-6, 2e-5]),
        ("30/60 K", "thermal excursion", [q["delta_T_K"] for q in I["thermal_scenarios"]] == [30, 60]),
        ("283 MPa", "inherited compression", be["sigma_Pa"] == 283e6),
        ("241 MPa", "conservative proxy", I["mechanical_scenarios"][2]["compression_proxy_Pa"] == 241e6),
        ("303 GPa", "inherited E", be["E_Pa"] == 303e9),
        ("290 GPa", "current E", E_now == 290e9),
    ]
    echo_rows = [{"card_text": t, "input": w, "in_card": t in card, "matches_INPUTS": bool(ok)} for t, w, ok in echoes]

    # ---- RESULTS.json at full precision ----
    R = json.loads((OWNER / "RESULTS.json").read_text())
    pairs = []

    def modes_pairs(prefix, md):
        pairs.append((prefix + ".least_SF", md["least"]))
        for mine_key, key in MODES.items():
            pairs.append((f"{prefix}.sfs.{key}", md["sf"][mine_key]))
        for key, val in (("Vc", md["Vc"]), ("Kc", md["Kc"]), ("gamma", md["gamma"]),
                         ("membrane_compression_Pa", md["s_mem"]), ("tf_m", md["tf"]), ("core_m", md["d"])):
            pairs.append((f"{prefix}.{key}", val))

    for key, val in (("face_mass_kg", m["faces"]), ("core_mass_kg", m["core"]), ("structural_mass_kg", m["struct"]),
                     ("joint_allowance_kg", m["joints"]), ("total_kg", m["total"]), ("payload_kg", m["payload"]),
                     ("capacity_gap_to_SF1_fraction", 1 - base["least"]),
                     ("capacity_factor_needed_for_SF1", 1 / base["least"]),
                     ("brief_mass_error_kg", m["faces"] - 2100),
                     ("brief_mass_understatement_percent_of_reference", 100 * (m["faces"] - 2100) / 2100),
                     ("area_one_skin_m2", case["A"])):
        pairs.append(("baseline." + key, val))
    modes_pairs("baseline.modes", base)
    for i, s in enumerate(supply):
        for key, val in s.items():
            pairs.append((f"annual_supply[{i}].{key}", val))
    for i, s in enumerate(costs):
        for key, val in s.items():
            pairs.append((f"cost_scenarios[{i}].{key}", val))
    for i, pn in enumerate((big, small)):
        for key, val in (("panels_per_skin_area_lower_bound", pn["n"]), ("panel_pieces_both_skins_lower_bound", 2 * pn["n"]),
                         ("mean_field_edge_joints_per_skin", pn["edges"]),
                         ("mean_field_edge_joints_both_skins", 2 * pn["edges"]),
                         ("coincident_hull_seam_m", pn["L"]), ("skin_seam_m_both_skins", 2 * pn["L"]),
                         ("corner_sag_from_tangent_plane_m", pn["sag"]),
                         ("through_thickness_bending_strain", pn["bend"]),
                         ("double_curvature_metric_strain_scale", pn["metric"])):
            pairs.append((f"panel_scenarios[{i}].{key}", val))
    for i, j in enumerate(joins):
        for key, val in (("film_kg_m2_per_interface", j["film"]), ("full_area_face_core_film_kg", j["full"]),
                         ("kg_per_hull_seam_m", j["per_m"]), ("seam_mass_kg", j["seam"]),
                         ("total_joining_mass_kg", j["total"]), ("replaces_joint_allowance_kg", m["joints"]),
                         ("additional_mass_over_allowance_kg", j["over"]),
                         ("total_with_replacement_joining_kg", j["new_total"]),
                         ("remaining_payload_kg", j["payload"]), ("payload_fraction", j["frac"]),
                         ("joint_efficiency_only_SF", j["eta_SF"])):
            pairs.append((f"joining_scenarios[{i}].{key}", val))
        for key, val in j["parts"].items():
            pairs.append((f"joining_scenarios[{i}].per_hull_seam_m_kg_breakdown.{key}", val))
    for i, f_ in enumerate(film_only):
        for key, val in (("both_interfaces_kg", f_["mass"]), ("mass_plus_minus_kg", f_["pm"]),
                         ("remaining_payload_if_only_film_replaces_5pct_joints_kg", f_["payload"])):
            pairs.append((f"film_only_scenarios[{i}].{key}", val))
    for i, b in enumerate(braze):
        for key, val in (("kg_per_hull_seam_m_filler_only", b["per_m"]), ("filler_mass_large_panel_kg", b["large"]),
                         ("joint_efficiency_only_SF", b["eta_SF"])):
            pairs.append((f"braze_scenarios[{i}].{key}", val))
    for i, g in enumerate(gauge):
        for key, val in (("face_mass_kg", g["m"]["faces"]), ("face_mass_change_kg", g["m"]["faces"] - m["faces"]),
                         ("remaining_payload_if_uniform_kg", g["m"]["payload"])):
            pairs.append((f"thickness_tolerance[{i}].{key}", val))
        modes_pairs(f"thickness_tolerance[{i}].modes_at_local_gauge", g["modes"])
    for i, md in enumerate(mech):
        modes_pairs(f"mechanical_sensitivities[{i}].modes", md)
    for i, t in enumerate(thermal):
        for key, val in (("shear_lag_lambda_per_m", t["lam"]), ("transfer_length_m", t["len"]),
                         ("long_joint_peak_shear_Pa", t["tau"]),
                         ("fully_restrained_uniaxial_thermal_stress_Pa", t["uni"]),
                         ("fully_restrained_biaxial_proxy_Pa", t["bi"])):
            pairs.append((f"thermal_sensitivities[{i}].{key}", val))
    pairs.append(("daily_cycles_assumed_30_years", math.ceil(cycles_exact)))
    for i, f_ in enumerate(fixed):
        modes_pairs(f"fixed_geometry_alternatives[{i}].modes", f_["modes"])
        for key, val in (("face_mass_kg", f_["m"]["faces"]), ("remaining_payload_kg", f_["m"]["payload"]),
                         ("SF_lost_absolute_vs_lead", f_["loss"]), ("SF_lost_percent_vs_lead", f_["loss_pct"])):
            pairs.append((f"fixed_geometry_alternatives[{i}].{key}", val))
    for i, p_ in enumerate(pub):
        for key, val in (("recomputed_SF", p_["modes"]["least"]), ("loss_absolute_vs_014b_Be", p_["loss"]),
                         ("loss_percent_vs_014b_Be", p_["loss_pct"])):
            pairs.append((f"published_equal_ceiling_alternatives[{i}].{key}", val))
    for i, md in enumerate(resized):
        modes_pairs(f"resized_5pct_margin_alternatives[{i}].modes", md)
        pairs.append((f"resized_5pct_margin_alternatives[{i}].scale", scale))
    results_rows = []
    for path, mine in pairs:
        theirs = at(R, path)
        diff = abs(theirs - mine) / max(1.0, abs(theirs), abs(mine))
        results_rows.append({"path": path, "RESULTS": theirs, "mine": mine, "rel_diff": diff, "ok": diff <= REL})

    # ---- tags: card sections, INPUTS rows, RESULTS rows ----
    sections = re.findall(r"\*\*(\d)\. ([^*]*)\*\*(.*?)(?=\n\n|\Z)", card, flags=re.S)
    tag_rows = [{"where": f"CARD section {n}", "heading": h.strip(),
                 "tagged": ("QUESTIONABLE" in h or "PROJECTION" in h), "has_source_link": "](" in rest}
                for n, h, rest in sections]
    for blk in ("case", "lead_point", "lead_core", "price_basis", "process_cost_row"):
        tag_rows.append({"where": f"INPUTS {blk}", "tag": I[blk].get("tag"), "tagged": bool(I[blk].get("tag"))})
    for blk in ("faces", "panel_scenarios", "joint_scenarios", "braze_scenarios", "procurement_scenarios",
                "mechanical_scenarios", "thermal_scenarios"):
        for r_ in I[blk]:
            tag_rows.append({"where": f'INPUTS {blk}: {r_["name"]}', "tag": r_.get("tag"), "tagged": bool(r_.get("tag"))})
    for blk in ("annual_supply", "cost_scenarios", "panel_scenarios", "joining_scenarios", "film_only_scenarios",
                "braze_scenarios", "thickness_tolerance", "mechanical_sensitivities", "thermal_sensitivities",
                "fixed_geometry_alternatives", "published_equal_ceiling_alternatives",
                "resized_5pct_margin_alternatives"):
        tag_rows.append({"where": f"RESULTS {blk}", "tag": sorted({r_.get("tag") for r_ in R[blk]}),
                         "tagged": all(r_.get("tag") for r_ in R[blk])})
    sources_in_inputs = {s_["id"]: bool(s_.get("url")) for s_ in I["sources"]}

    # ---- sources: re-read from the pinned PDFs ----
    usgs_t = pdf_text("USGS-2026-Be.pdf")
    s200 = pdf_text("S200F-2024.pdf")
    sr200 = pdf_text("SR200-2024.pdf")
    af163 = pdf_text("3M-AF163.pdf")
    nasa = pdf_text("NASA-19690025590.pdf")
    iaea44 = pdf_text("IAEA-Be-1995.pdf", 44, 44)
    iaea63 = pdf_text("IAEA-Be-1995.pdf", 63, 63)
    table7 = iaea44.split("Table 7")[1].split("modern grade")[0]
    nus = [float(x) for x in re.findall(r"\b0\.\d{3}\b", table7)]
    sources = []

    def found(sid, value, text, pattern, where):
        sources.append({"source": sid, "card_value": value, "where": where,
                        "pattern": pattern, "found": re.search(pattern, text) is not None})

    found("S01 USGS", "433 t (2024, revised) and 430 t (2025e) world mine output, Be content", usgs_t,
          r"World total \(rounded\) 433 430", "p. 2, world mine production table")
    found("S01 USGS", "data in metric tons of Be content", usgs_t,
          r"Data in metric tons, beryllium content", "p. 1 header")
    found("S01 USGS", "$1,600/kg contained Be, Be-Cu master alloy, 2025e", usgs_t,
          r"master alloy,5 680 660 1,400 1,500 1,600 dollars per kilogram of contained beryllium", "p. 1 salient table")
    found("S01 USGS", "master alloy Be content taken as 4%", usgs_t,
          r"beryllium content estimated to be 4%", "footnote 5")
    found("S02 S-200F", "E 290 GPa typical", s200, r"1\.85 g/cm3 290 GPa", "p. 1 physical properties")
    found("S02 S-200F", "241 MPa minimum tensile yield", s200,
          r"Yield Strength \(0\.2% offset\), MPa \(ksi\), min 241 \(35\)", "p. 2 mechanical properties")
    found("S02 S-200F", "2% minimum elongation", s200, r"Elongation \(% in 4 diameters\), min 2\.0", "p. 2")
    found("S02 S-200F", "below 6.3 mm the product is SR-200 sheet or PS-200 foil", s200,
          r"less than 6\.3 mm \(\.25.{0,2}\) thick, SR-200 sheet and PS-200 foil", "p. 2 tolerance note")
    found("S03 SR-200", "E 290 GPa typical", sr200, r"1\.85 g/cm3 290 GPa", "p. 1")
    found("S03 SR-200", "345 MPa minimum tensile yield", sr200,
          r"Yield Strength \(0\.2% offset\), MPa \(ksi\), min 345 \(50\)", "p. 1 mechanical properties")
    found("S03 SR-200", "10% elongation in 1 inch", sr200, r"min 10\.0 \(% in 1", "p. 1")
    found("S03 SR-200", "+/-0.004 in for 0.025-0.034 in (0.75 mm = 0.0296 in)", sr200,
          r"Over 0\.025.{0,2} to 0\.034.{0,2} \(0\.63 to 0\.86 mm\) 0\.004.{0,2}/0\.004", "p. 2 thickness table")
    found("S03 SR-200", "flatness at 0.040 in and under: Type 1 2%, Type 3 0.030 in/ft", sr200,
          r"0\.030.{0,2}/ft\. 0\.040 and under 2% 1% N/A \(0\.762/304 mm\)", "p. 2 flatness table")
    found("S03 SR-200", "flatness may be measured restrained", sr200,
          r"Flatness measurements may be made with the sheet restrained", "p. 2")
    found("S03 SR-200", "24 x 72 in maximum for 0.059-0.250 in", sr200,
          r"0\.059.{0,2} to 0\.250.{0,2} \(0\.5 to 6\.25 mm\) with maximum dimensions of 24.{0,2} x 72", "p. 3")
    found("S03 SR-200", "0.020-0.058 in sheet at narrower widths and shorter lengths", sr200,
          r"Sheets 0\.020.{0,2} to 0\.058.{0,2} thick are available at narrower widths and shorter lengths", "p. 3")
    found("S03 SR-200", "hot forming is a documented route", sr200, r"as a hot-formed material", "p. 1")
    found("S05 3M AF163", "film weights +/-0.005 lb/ft2", af163, r"\(± \.005\) Lb/ft", "p. 1 table")
    found("S05 3M AF163", "0.015 lb/ft2 only as unsupported 2U", af163, r"AF 163-2U Film 0\.015", "p. 1 table")
    found("S05 3M AF163", "0.030 and 0.060 lb/ft2 products", af163,
          r"AF 163-2U Film 0\.030 .{0,40}AF 163-2U Film 0\.060", "p. 1 table")
    found("S06 NASA", "FM-1000, 4 in lap: 112.5% efficiency", nasa,
          r"BL3 4\.0 5760 Tension 1400 62,000 112\.5", "printed p. 17")
    found("S06 NASA", "FM-1000, 1 in lap: 85% efficiency", nasa, r"BL7 1\.0 4520 Tension 4520 46,800 85", "printed p. 17")
    found("S06 NASA", "efficiency based on cross-rolled sheet Ftu 55 ksi", nasa,
          r"Ftu = 55,000 psi for beryllium cross-rolled sheet", "printed p. 17")
    found("S07 IAEA", "S-200F rotating-beam R = -1: 262/266 MPa at 10^7 cycles", iaea63,
          r"Fatigue life \(107 cycles\) is 262 MPa and 266 MPa", "PDF p. 63")
    sources.append({"source": "S07 IAEA", "card_value": "VHP Poisson ratio 0.08 as a representative value",
                    "where": "PDF p. 44, Table 7", "found": len(nus) == 12 and min(nus) == 0.058 and max(nus) == 0.108,
                    "values": nus, "mean": statistics.mean(nus)})
    for page, value, note in (
            (13, "adhesive bonding and brazing are established", "adhesive bonding 'a very desirable way to join "
             "beryllium'; brazing 'the most reliable method of metallurgically joining beryllium'"),
            (14, "published average Be joint strengths", "lap-shear and peel table, brazed shear table"),
            (8, "cross-rolling balances SR-200 in-plane properties; SR-200 is the 0.020-0.220 in sheet grade",
             "'properties of SR-200 sheet are balanced by cross rolling'; in-plane minimum 483 MPa UTS, 345 MPa "
             "yield, 10% elongation; wrought products stronger than hot-pressed block in the working direction"),
            (4, "compression: 'typically 10% higher' than tension, yet S-200F both 'about 37 ksi (255 MPa)'",
             "the internal inconsistency METHOD.md reports"),
            (5, "E 44.0 msi (303 GPa), the inherited value", "the 2024 datasheets give 290 GPa"),
            (11, "machining damage 0.002-0.010 in deep; etch 0.004 in (102 um) per side",
             "not used by the card; relevant only to faces machined rather than rolled")):
        sources.append({"source": "S04 Materion guide", "card_value": value, "found": True, "note": note,
                        "where": f"p. {page} (image-only PDF; read visually by the checker at 60-70 dpi)"})
    sources.append({"source": "S08 OSHA", "card_value": "0.2 ug/m3 8-h and 2.0 ug/m3 15-min",
                    "where": "no local copy (owner: HTTP 403)", "found": None,
                    "note": "Agrees with the checker's knowledge of 29 CFR 1910.1024(c); not hash-verifiable."})
    sources.append({"source": "S09 AlBeMet", "card_value": "AM162 is 62 wt% Be",
                    "where": "no local copy (owner: HTTP 403)", "found": None,
                    "note": "Agrees with the checker's knowledge of AlBeMet AM162 (Al-62Be); not hash-verifiable."})

    # ---- objections (NFI rows): own numbers ----
    sr_E, sr_sig, sr_nu = 290e9, 345e6, 0.08     # S03 typical E and minimum tensile yield; nu as the card's current rows
    grade = {
        "face_SF_at_lead_345": sr_sig / base["s_mem"],
        "face_SF_at_lead_card": [be["sigma_Pa"] / base["s_mem"], 241e6 / base["s_mem"]],
        "eta_least_card_basis_345": [sandwich(case, be["E_Pa"], sr_sig, nu0, tf, d, core, eta=e)["least"]
                                     for e in (0.9, 0.6)],
        "eta_least_card": [joins[0]["eta_SF"], joins[1]["eta_SF"]],
        "eta_least_current_E_345": [sandwich(case, sr_E, sr_sig, sr_nu, tf, d, core, eta=e)["least"]
                                    for e in (0.9, 0.6)],
        "eta_least_current_E_283": [sandwich(case, sr_E, be["sigma_Pa"], sr_nu, tf, d, core, eta=e)["least"]
                                    for e in (0.9, 0.6)],
        "retention_least_345": sandwich(case, 0.8 * sr_E, 0.7 * sr_sig, sr_nu, tf, d, core)["least"],
        "retention_governs_345": sandwich(case, 0.8 * sr_E, 0.7 * sr_sig, sr_nu, tf, d, core)["governs"],
        "retention_least_card": mech[3]["least"],
        "eta_breakeven_card_basis_283": base["least"] / (be["sigma_Pa"] / base["s_mem"]),
        "eta_breakeven_card_basis_345": base["least"] / (sr_sig / base["s_mem"]),
        "guide_p11_etch_fraction_of_gauge": 2 * 0.004 * INCH / tf,
    }
    be_pub = I["published_014b"][0]
    be290_pub = sandwich(case, sr_E, be["sigma_Pa"], sr_nu, be_pub["tf_m"], be_pub["core_m"], be_pub["core"])
    be290_pub_nu33 = sandwich(case, sr_E, be["sigma_Pa"], nu0, be_pub["tf_m"], be_pub["core_m"], be_pub["core"])
    be290_lead = mech[1]
    ebasis = {
        "Be_published_at_303": pub[0]["modes"]["least"],
        "Be_published_at_290": be290_pub["least"],
        "Be_published_at_290_nu033": be290_pub_nu33["least"],
        "Be_published_at_290_governs": be290_pub["governs"],
        "K13D2U_published": pub[1]["modes"]["least"],
        "loss_published_pct_303": pub[1]["loss_pct"],
        "loss_published_pct_290": 100 * (1 - pub[1]["modes"]["least"] / be290_pub["least"]),
        "Be_lead_at_290": be290_lead["least"],
        "K13D2U_exact": k13_fixed["modes"]["least"],
        "loss_exact_pct_303": k13_fixed["loss_pct"],
        "loss_exact_pct_290": 100 * (1 - k13_fixed["modes"]["least"] / be290_lead["least"]),
        "K13D2U_resized": resized[1]["least"],
        "loss_resized_pct_303": 100 * (1 - resized[1]["least"] / base["least"]),
        "loss_resized_pct_290": 100 * (1 - resized[1]["least"] / be290_lead["least"]),
    }
    dbl_opt = big["L"] * joins[0]["parts"]["Be_doublers"]
    dbl_con = small["L"] * joins[3]["parts"]["Be_doublers"]
    doublers = {
        "Be_doubler_kg": [dbl_opt, dbl_con],
        "Be_total_kg": [m["faces"] + dbl_opt, m["faces"] + dbl_con],
        "share_percent": [100 * (m["faces"] + dbl_opt) / opt_s["mine_output_kg"],
                          100 * (m["faces"] + dbl_con) / con_s["mine_output_kg"]],
        "sheet_stock_cost_USDm": [(m["faces"] + dbl_opt) / opt_s["yield"] * opt_s["SR200_USD_per_kg"] / 1e6,
                                  (m["faces"] + dbl_con) / con_s["yield"] * con_s["SR200_USD_per_kg"] / 1e6],
        "card_cost_USDm": [m["faces"] / opt_s["yield"] * opt_s["SR200_USD_per_kg"] / 1e6,
                           m["faces"] / con_s["yield"] * con_s["SR200_USD_per_kg"] / 1e6],
    }
    doublers["cost_increase_percent"] = [100 * (a / b - 1) for a, b in zip(doublers["sheet_stock_cost_USDm"],
                                                                           doublers["card_cost_USDm"])]
    observations = {
        "dimpling_biaxial_straight_line_SF": base["sf"]["dimple"] / 2,
        "dimpling_card_uniaxial_SF": base["sf"]["dimple"],
        "published_structural_masses_kg": [p_["struct"] for p_ in pub],
        "resize_scale": scale,
        "cycles_exact": cycles_exact,
        "brief_2100kg_vs_009c5_other_branch_faces_kg": P9["other_branch"]["masses_kg"]["faces"],
        "kd_0_20_ranking_014b": [{"face": f_, "tag": t_, "SF": s_} for s_, f_, t_ in ranking[:6]],
    }

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    inputs = {"schema": 1, "check_of": "MAINLINE-020", "unit": "vacuum-mainline020-check-1020", "pins": [
        pin(REPORT, "the filed report (artifacts and body)"),
        *[pin(OWNER / n, "owner file checked") for n in ("CARD.md", "RESULTS.json", "INPUTS.json", "NFI.json",
                                                          "METHOD.md", "MANIFEST.json")],
        pin(OWNER / "calculate.py", "owner script: read for formulas, not run"),
        pin(OWNER_NOTE, "owner note"),
        *[pin(OWNER / n, "intake read by this check") for n in ("intake/009c5/POINT.json", "intake/014b/INPUTS.json",
                                                                 "intake/014b/RESULTS.json", "intake/016/compute.py")],
        *[pin(OWNER / "sources" / n, "source re-read by this check") for n in (
            "USGS-2026-Be.pdf", "S200F-2024.pdf", "SR200-2024.pdf", "Materion-design-fabrication.pdf",
            "3M-AF163.pdf", "NASA-19690025590.pdf", "IAEA-Be-1995.pdf")],
        *[pin(BRIEFS / n, "brief") for n in ("CHECK.md", "COMMON.md", "CARD-020-BERYLLIUM-REALITY.md")],
    ]}
    (OUT / "INPUTS.json").write_text(json.dumps(inputs, indent=1) + "\n")

    g, e, dd = grade, ebasis, doublers
    nfi = {"schema": 1, "check_of": "MAINLINE-020", "unit": "vacuum-mainline020-check-1020", "tag": "QUESTIONABLE",
           "status": "OPEN", "items": [
        {"id": "NFI-020C-GRADE-BASIS", "rank": 1, "kind": "proposed fix", "tag": "QUESTIONABLE",
         "against": "CARD.md sections 3 and 4; RESULTS mechanical_sensitivities and joining eta",
         "claim": "The faces are bought as SR-200 sheet (sections 1-2), but every strength screen uses S-200F block "
                  "values: 283 MPa inherited as 'optimistic', 241 MPa block tensile minimum, and 0.7 x 241. SR-200's "
                  "own sourced minimum tensile yield is 345 MPa (S03; guide p. 8), above the card's optimistic value.",
         "support": "S02 lists S-200-F in rod and bar and points to SR-200 sheet and PS-200 foil below 6.3 mm. Guide "
                    "p. 8: wrought products are stronger than hot-pressed block in the working direction, and "
                    "SR-200's in-plane properties are balanced by cross rolling. Guide p. 11: machined beryllium "
                    "needs a 0.004 in etch on each side, together " +
                    f"{100 * g['guide_p11_etch_fraction_of_gauge']:.0f}" +
                    "% of a 0.752 mm face, which points to rolled sheet for faces this thin.",
         "numbers": {"face_SF_at_lead": {"card_283": g["face_SF_at_lead_card"][0], "card_241": g["face_SF_at_lead_card"][1],
                                          "SR200_345": g["face_SF_at_lead_345"]},
                     "least_SF_eta_0.9_0.6": {"card": g["eta_least_card"], "SR200_345_same_E": g["eta_least_card_basis_345"]},
                     "least_SF_retention_0.8E_0.7sigma": {"card": g["retention_least_card"],
                                                          "SR200_345": g["retention_least_345"]},
                     "eta_at_which_net_section_governs": {"283": g["eta_breakeven_card_basis_283"],
                                                          "345": g["eta_breakeven_card_basis_345"]}},
         "proposed_fix": "Add an SR-200 row (E 290 GPa, 345 MPa minimum tensile yield used as the compression proxy, "
                         "the card's own transfer convention, QUESTIONABLE, S03) to the eta and retention screens, "
                         "and keep 241 MPa only as an explicitly block-grade lower screen.",
         "effect_on_lead": "None on the least SF at eta 1. The conservative joint screen (eta 0.6) no longer lowers it "
                           "(0.65041 instead of 0.53535), and the retention screen becomes wrinkling-governed at "
                           f"{g['retention_least_345']:.5f} instead of {g['retention_least_card']:.5f}. Rolled-sheet "
                           "compression data are still needed (owner's NFI-020-GRADE-ORIENTATION-COMPRESSION)."},
        {"id": "NFI-020C-FALLBACK-E-BASIS", "rank": 2, "kind": "proposed fix", "tag": "QUESTIONABLE",
         "against": "CARD.md section 6",
         "claim": "Section 4 takes 290 GPa as Be's current modulus, but section 6 prices the K13D2U trade against "
                  "Be at the inherited 303 GPa. At 290 GPa, the SF given up by choosing K13D2U is smaller.",
         "numbers": {"published_designs": {"Be_303": e["Be_published_at_303"], "Be_290": e["Be_published_at_290"],
                                           "K13D2U": e["K13D2U_published"], "loss_pct_303": e["loss_published_pct_303"],
                                           "loss_pct_290": e["loss_published_pct_290"]},
                     "009c5_geometry": {"Be_303": base["least"], "Be_290": e["Be_lead_at_290"],
                                        "K13D2U": e["K13D2U_exact"], "loss_pct_303": e["loss_exact_pct_303"],
                                        "loss_pct_290": e["loss_exact_pct_290"]},
                     "5pct_budget_resized": {"Be_lead_303": base["least"], "Be_lead_290": e["Be_lead_at_290"],
                                             "K13D2U": e["K13D2U_resized"], "loss_pct_303": e["loss_resized_pct_303"],
                                             "loss_pct_290": e["loss_resized_pct_290"]}},
         "proposed_fix": "State section 6's SF given up at both Be moduli; K13D2U's 210 GPa stays the 014b QI value.",
         "effect_on_lead": "The Be-free fallback costs less SF than the card shows; the ranking does not change."},
        {"id": "NFI-020C-DOUBLER-BERYLLIUM", "rank": 3, "kind": "NFI row", "tag": "PROJECTION",
         "against": "CARD.md sections 1 and 3",
         "claim": "Section 3's splice doublers are full-gauge Be, but section 1 buys and prices only the faces.",
         "numbers": {"Be_doubler_kg_opt_con": dd["Be_doubler_kg"], "Be_total_kg": dd["Be_total_kg"],
                     "share_of_mine_output_percent": dd["share_percent"],
                     "sheet_stock_cost_USDm": dd["sheet_stock_cost_USDm"], "card_cost_USDm": dd["card_cost_USDm"],
                     "cost_increase_percent": dd["cost_increase_percent"]},
         "proposed_fix": "Count the doubler Be in the section 1 supply share and sheet cost, paired the way section 3 "
                         "pairs panels and joints.",
         "effect_on_lead": "No SF effect; procurement and cost rise."},
    ]}
    (OUT / "NFI.json").write_text(json.dumps(nfi, indent=1) + "\n")

    # ---- CHECK.md, from the numbers above ----
    summ = results["summary"]
    pc = summ["pin_counts"]
    n_card = sum(1 for r_ in compared if r_["row"] not in ("METHOD", "Report"))
    n_meth = sum(1 for r_ in compared if r_["row"] == "METHOD")
    n_rep = sum(1 for r_ in compared if r_["row"] == "Report")
    pdf_rows = [s_ for s_ in sources if s_["found"] is not None]
    untagged_blocks = sorted({t_["where"].split(": ")[0].replace("INPUTS ", "") for t_ in tag_rows if not t_["tagged"]})
    sec = [t_ for t_ in tag_rows if t_["where"].startswith("CARD section")]
    mis_text = "None." if not mism else " ".join(
        f'{r_["row"]}, {r_["field"]}: card {r_["card"]}, mine {r_["mine_at_card_precision"]}.' for r_ in mism)
    table = "\n".join(
        f'| {r_["row"]} | {r_["field"]} | {r_["card"]} | {r_["mine_at_card_precision"]} | {r_["mine"]:.10g} |'
        for r_ in compared)
    doc = f"""# MAINLINE-020 check: beryllium reality, checked behind its owner

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

**Result: no arithmetic mismatches.** My own script, check020.py, re-derived each number from the pinned inputs: {n_card} in CARD.md, {n_meth} in METHOD.md and {n_rep} in the report body. Each agrees at the precision printed. The {summ["results_values_compared"]} values in RESULTS.json agree with mine to {summ["results_max_rel_diff"]:.1e} relative or better. I read the owner's calculate.py only to compare its equations with METHOD.md. I did not import or run it.

**Mismatches (row, field, card value, my value).** {mis_text}

**Pins and intake.** These all match sha256 and size:
- the report's {pc["report artifact"]} artifacts;
- the owner's {pc["owner input pin"]} input pins;
- the {pc["brief"]} brief pins.

All {summ["intake_checks"]} intake checks match the 009c5 and 014b copies: the lead point, the HRH-10 and HRH-49 cores, the four faces with their tags, the four 014b designs, ν, pressure, lift and the 4,561.37 kg ceiling. Each 014b design is that face's only kd 0.20 row there. All four sit on that ceiling, so one scale, {scale:.6f}, resizes every design to the 5% budget. Among QUESTIONABLE faces in 014b, K13D2U is the best that is free of beryllium. CNT yarn and graphene rank above it but are PROJECTION.

**Formulas.** METHOD.md states the equations that calculate.py uses: the masses, the CR-1457 modes with the Vc branch rule, panel count and seam length, sag, seam mass, the film conversion, braze, gauge, shear lag and the resize. I wrote each one independently and they agree. My q comes from Cardano's formula ({Q_BIAX:.10f}), and my wrinkling is q·0.33·√(E·Ec·tf/d).

**Sources and tags.** Each of the card's {len(sec)} numbered sections carries a QUESTIONABLE or PROJECTION tag and at least one source link. INPUTS leaves its {" and ".join(b_.replace("_scenarios", "") for b_ in untagged_blocks) if untagged_blocks else "(no)"} scenario rows untagged, but RESULTS tags every one of those rows. I re-read the owner's pinned PDFs myself and found all {sum(1 for s_ in pdf_rows if s_["found"])} of {len(pdf_rows)} sourced values:
- USGS: 433 t (2024) and 430 t (2025e); $1,600/kg contained beryllium in 4% master alloy.
- S-200F: 290 GPa, a 241 MPa minimum yield and 2% elongation.
- SR-200: 24 × 72 in only for stock 0.059 in thick and over; ±0.004 in at this gauge; flatness 2% and 0.030 in/ft; a 345 MPa minimum yield and 10% elongation.
- AF163: films of 0.015 to 0.060 lb/ft², ±0.005.
- NASA: FM-1000 laps at 85% to 112.5%.
- IAEA: ν from {min(nus):.3f} to {max(nus):.3f} (mean {statistics.mean(nus):.3f}), and 262/266 MPa at 10⁷ cycles.
- The Materion guide, pages 4, 5, 8, 11, 13 and 14, read as images.

The OSHA limits (0.2 and 2.0 µg/m³) and AlBeMet's 62 wt% beryllium have no local copy, as the card says. Both agree with what I know of those sources, but I could not hash them.

**Objections.** Each is a row in NFI.json, and none stops anything.

1. NFI-020C-GRADE-BASIS, a proposed fix. Sections 1 and 2 buy SR-200 sheet, but sections 3 and 4 screen strength with S-200F block values. The S-200F datasheet lists S-200F in rod and bar, and points to SR-200 sheet and PS-200 foil for beryllium under 6.3 mm. SR-200's minimum tensile yield is 345 MPa (S03, and guide page 8), above the card's "optimistic" 283 MPa. I transferred it to compression the way the card transfers 241 MPa. Face compression at the lead is then {g["face_SF_at_lead_345"]:.4f}, against the card's {g["face_SF_at_lead_card"][0]:.4f} and {g["face_SF_at_lead_card"][1]:.4f}. Two screens change:
   - at η = 0.6 the least SF stays {g["eta_least_card_basis_345"][1]:.5f}, not {g["eta_least_card"][1]:.5f};
   - the 0.8E/0.7σ screen gives {g["retention_least_345"]:.5f} (wrinkling), not {g["retention_least_card"]:.5f}.

   The fix is to add an SR-200 row and keep 241 MPa as an explicitly block-grade lower screen. Whether SR-200 reaches 345 MPa in in-plane compression stays open under the owner's NFI-020-GRADE-ORIENTATION-COMPRESSION.
2. NFI-020C-FALLBACK-E-BASIS, a proposed fix. Section 4 takes 290 GPa as beryllium's current modulus, but section 6 compares K13D2U with beryllium at 303 GPa. At 290 GPa, beryllium's published 014b design drops to {e["Be_published_at_290"]:.5f}, governed by wrinkling. The SF given up by choosing K13D2U is then smaller:

   | Basis | Card, at 303 GPa | At 290 GPa |
   |---|---|---|
   | Published designs | {e["loss_published_pct_303"]:.2f}% | {e["loss_published_pct_290"]:.2f}% |
   | 009c5 geometry | {e["loss_exact_pct_303"]:.2f}% | {e["loss_exact_pct_290"]:.2f}% |
   | 5% budget | {e["loss_resized_pct_303"]:.2f}% (not printed) | {e["loss_resized_pct_290"]:.2f}% |

   The fix is to state section 6 at both moduli. The ranking does not change.
3. NFI-020C-DOUBLER-BERYLLIUM. Section 3's splice doublers are full-gauge beryllium: {dd["Be_doubler_kg"][0]:,.1f} kg optimistic and {dd["Be_doubler_kg"][1]:,.1f} kg conservative. Section 1 counts only the faces. With the doublers, beryllium is {dd["share_percent"][0]:.3f}% and {dd["share_percent"][1]:.3f}% of mine output. Sheet stock then costs ${dd["sheet_stock_cost_USDm"][0]:.2f}m and ${dd["sheet_stock_cost_USDm"][1]:.2f}m, which is {dd["cost_increase_percent"][0]:+.0f}% and {dd["cost_increase_percent"][1]:+.0f}%.

**Seen, not raised.**
- Dimpling is screened uniaxially, as 014b does. The biaxial straight-line rule halves it to {observations["dimpling_biaxial_straight_line_SF"]:.1f}, which still does not bind.
- The 10,958 cycles is 30 × 365.25 = {observations["cycles_exact"]:,.1f}, rounded up.
- SR-200's datasheet converts 0.059 in to "0.5 mm"; it is 1.50 mm. The owner already notes this.
- The brief's 2,100 kg is not the lead's face mass, and the card's correction to 3,498.47 kg stands.

## Every number compared

| Row | Field | Card | Mine at card precision | Mine |
|---|---|---|---|---|
{table}

Files: check020.py, RESULTS.json (all {summ["results_values_compared"]} RESULTS.json comparisons, the {summ["intake_checks"]} intake checks, sources, tags and pins), NFI.json, INPUTS.json (pins) and this CHECK.md.
"""
    (OUT / "CHECK.md").write_text(doc)

    print(json.dumps(results["summary"], indent=1))
    print("grade", json.dumps(grade, indent=1))
    print("ebasis", json.dumps(ebasis, indent=1))
    print("doublers", json.dumps(doublers, indent=1))
    print("observations", json.dumps(observations, indent=1))
    for r in compared:
        print(f'{r["row"]:12s} | {r["field"][:52]:52s} | {r["card"]:>10s} | {r["mine_at_card_precision"]:>10s} | '
              f'{"ok" if r["match"] else "MISMATCH"} | {"" if r["printed_in_text"] else "NOT IN TEXT"}')


if __name__ == "__main__":
    main()
