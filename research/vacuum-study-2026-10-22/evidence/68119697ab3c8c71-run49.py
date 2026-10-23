#!/usr/bin/env python3
"""MAINLINE-049 driver: the beryllium-free P2 through 040's whole bill. Pins, the 040 reproduction (12 rows), the
faces (M55J and K13D2U quasi-isotropic CFRP, AlBeMet sheet, Be reference), the cores (CR-III 5056, HRH-10 Nomex,
HRH-49 Kevlar), 037b's mismatch screens for each pair, the CFRP seams, the account at R 15/20/30, ISA and optimistic,
actual joining and 040's retained floor, and the face mass against world supply. Writes COMPUTE.json."""
import csv
import datetime
import hashlib
import json
import math
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import acct49 as A  # noqa: E402
import laminate as LAM  # noqa: E402
import model49 as M  # noqa: E402
import src49 as S  # noqa: E402
import thermal49 as TH  # noqa: E402

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


COMMON_DISPATCHED = "8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5"
COMMON_ADDED = ("- **A simjob refusal is a wait, not a stop.**", "- **Heavy runs go through simjob,**")


def common_amendment():
    """COMMON.md as it stands against the dispatched pin: the lines added since dispatch, and whether removing exactly
    those lines gives back the dispatched file (if not, a new rule exists and must be read before running)."""
    data = open(f"{BRIEF}/COMMON.md", "rb").read()
    lines = data.decode().split("\n")
    added = [x for x in lines if x.startswith(COMMON_ADDED)]
    base = hashlib.sha256("\n".join(x for x in lines if not x.startswith(COMMON_ADDED)).encode()).hexdigest()
    return {"dispatched_sha256": COMMON_DISPATCHED, "current_sha256": hashlib.sha256(data).hexdigest(),
            "added_lines": added, "current_minus_added_is_dispatched": base == COMMON_DISPATCHED,
            "effect": "heavy runs go through simjob and a refusal is retried unchanged; this card's runs were moved "
                      "onto simjob when the order and amendments were read"}


def pin(path, want):
    data = open(path, "rb").read()
    h = hashlib.sha256(data).hexdigest()
    return {"path": path, "sha256": h, "bytes": len(data), "ok": (want is None or h.startswith(want))}


def build(F0, C0):
    """Sections 1-3: the faces, the cores (040 format with their 037b inputs) and the CFRP seam. Shared with fold49."""
    # ---------------------------------------------------------------- 1. the faces
    faces = {}
    # M55J quasi-isotropic (vendor-calculated laminate), Toray fibre and UD composite
    m_E = S.val("m55j_qi_E", "cfrp", "m55j_qi", "QI laminate in-plane modulus", 108.9) * 1e9
    m_nu = S.val("m55j_qi_nu", "cfrp", "m55j_qi", "QI laminate Poisson ratio", 0.308)
    m_Fc = S.val("m55j_qi_Fc", "cfrp", "m55j_qi", "QI laminate ultimate compressive strength", 313.0) * 1e6
    m_a = S.val("m55j_qi_cte", "cfrp", "m55j_qi", "QI laminate in-plane CTE", -0.365) * 1e-6
    m_fib_rho = S.val("m55j_rho", "cfrp", "m55j_fibre", "Fibre density", 1.91) * 1000
    S.val("m55j_Xc", "cfrp", "m55j_lamina", "UD composite 0 deg compressive strength X_c", 890.0)
    S.val("m55j_E1", "cfrp", "m55j_lamina", "UD composite 0 deg tensile modulus E1", 338.0)
    S.val("m55j_ilss", "cfrp", "m55j_lamina", "interlaminar shear strength ILSS", 73.2)
    vf, rho_resin = 0.60, 1200.0                                      # PROJECTION: 60% Vf (Toray's basis), resin 1.2 g/cm3
    m_rho = vf * m_fib_rho + (1 - vf) * rho_resin
    thin_gsm = S.val("m55j_thin", "cfrp", "thin_ply", "fibre areal weight reduction using M55J", 30.0)
    m_tmin = 6 * thin_gsm / 1000 / (m_fib_rho * vf)                  # [0/+-60]s of 30 g/m2 plies (PROJECTION)
    faces["M55J QI"] = {"face": dict(F0, name="M55J/epoxy quasi-isotropic", rho=m_rho, E_today_Pa=m_E, E_full_Pa=m_E,
                                     strength_today_Pa=m_Fc, strength_full_Pa=m_Fc / (1 - m_nu)),
                        "nu": m_nu, "alpha": m_a, "tf_min": m_tmin, "fibre_mass_fraction": vf * m_fib_rho / m_rho,
                        "supply": "M55J tonnage not printed; world carbon fibre demand 126,500-224,510 t/yr",
                        "basis": {"E": "Rock West calculated QI 108.9 GPa", "Fc_today": "Rock West calculated QI 313 MPa",
                                  "Fc_full": "313/(1-nu): equal-biaxial reading of a fibre-strain limit (PROJECTION)",
                                  "rho": f"60% Vf of 1.91 g/cm3 fibre in 1.2 g/cm3 resin = {m_rho:.0f} kg/m3 (PROJECTION)",
                                  "tf_min": f"six 30 g/m2 plies (ESA's intent for M55J) = {m_tmin * 1e3:.3f} mm (PROJECTION)"}}
    # K13D2U quasi-isotropic from the measured lamina (laminate theory), 014b's pinned QI strength
    k_E1 = S.val("k13_E1", "cfrp", "k13d2u_lamina", "Lamina longitudinal modulus E1", 410.2) * 1e9
    k_E2 = S.val("k13_E2", "cfrp", "k13d2u_lamina", "Lamina transverse modulus E2", 5.557) * 1e9
    k_G12 = S.val("k13_G12", "cfrp", "k13d2u_lamina", "Lamina in-plane shear modulus G12", 4.102) * 1e9
    k_nu12 = S.val("k13_nu12", "cfrp", "k13d2u_lamina", "Lamina major Poisson ratio", 0.39)
    k_ply = S.val("k13_ply", "cfrp", "k13d2u_lamina", "Nominal cured ply thickness", 0.061) / 1000
    k_fib_rho = S.val("k13_rho", "cfrp", "k13d2u_fibre", "Fibre density", 2.2) * 1000
    k_resin_w = S.val("k13_resin", "cfrp", "k13d2u_lamina", "Resin content of EX1515", 33.0) / 100
    S.val("k13_fibre_cte", "cfrp", "k13d2u_fibre", "Fibre axial CTE", -1.5)
    qi = LAM.quasi_iso(k_E1, k_E2, k_G12, k_nu12)
    d014 = json.load(open(f"{D014B}/INPUTS.json"))
    k014 = next(f for f in d014["faces"] if f["name"].startswith("CFRP quasi-isotropic K13D2U"))
    k_rho = 1.0 / ((1 - k_resin_w) / k_fib_rho + k_resin_w / rho_resin)
    faces["K13D2U QI"] = {"face": dict(F0, name="K13D2U/epoxy quasi-isotropic", rho=k_rho, E_today_Pa=qi["E_Pa"],
                                       E_full_Pa=qi["E_Pa"], strength_today_Pa=k014["sigma_Pa"],
                                       strength_full_Pa=k014["sigma_Pa"] / (1 - qi["nu"])),
                          "nu": qi["nu"], "alpha": m_a, "tf_min": 6 * k_ply,
                          "fibre_mass_fraction": 1 - k_resin_w,
                          "supply": "continuous pitch fibre capacity about 1,400 t/yr (three producers)",
                          "basis": {"E": f"[0/+-60] laminate theory on Tuttle's lamina = {qi['E_Pa'] / 1e9:.1f} GPa",
                                    "Fc_today": f"014b's pinned QI strength {k014['sigma_Pa'] / 1e6:.0f} MPa (no sourced Xc)",
                                    "Fc_full": "today/(1-nu), the equal-biaxial reading (PROJECTION)",
                                    "alpha": "M55J's QI value as a proxy (PROJECTION); fibre -1.5 ppm/K",
                                    "rho": f"33% resin by weight, 2.20 fibre, 1.2 resin = {k_rho:.0f} kg/m3 (PROJECTION resin)",
                                    "tf_min": f"six 0.061 mm plies = {6 * k_ply * 1e3:.3f} mm"}}
    # AlBeMet AM162 rolled sheet
    alb = dict(F0, name="AlBeMet AM162 rolled sheet",
               rho=S.val("am_rho", "albemet", "am162_physical", "density (product-form table)", 2.071) * 1000,
               E_today_Pa=S.val("am_E", "albemet", "am162_sheet", "typical elastic modulus, rolled sheet", 193.0) * 1e9,
               strength_today_Pa=S.val("am_ys_min", "albemet", "am162_sheet", "minimum 0.2% yield", 276.0) * 1e6,
               strength_full_Pa=S.val("am_ys_typ", "albemet", "am162_sheet", "typical 0.2% yield", 314.0) * 1e6)
    alb["E_full_Pa"] = alb["E_today_Pa"]
    be_frac = S.val("am_be", "albemet", "am162_physical", "beryllium content, nominal", 62.0) / 100
    faces["AlBeMet AM162"] = {"face": alb, "nu": S.val("am_nu", "albemet", "am162_physical", "Poisson's ratio", 0.17, "AlBeMet AM162"),
                              "alpha": S.val("am_cte", "albemet", "am162_physical", "coefficient of thermal expansion at 25 C", 13.9) * 1e-6,
                              "tf_min": 0.254e-3, "be_mass_fraction": be_frac,
                              "basis": {"Fc_today": "sheet minimum tensile yield used in compression",
                                        "Fc_full": "sheet typical tensile yield", "tf_min": "0.254 mm, the thinnest sheet supplied"}}
    # ---------------------------------------------------------------- 2. the cores (040 format) and their 037b inputs
    cores = {"CR-III 5056 3/8-1.0": {"core": C0, "mat": {}, "k": None,
                                     "basis": "040's core and its 037b inputs"}}
    h10 = dict(C0, name="Hexcel HRH-10-3/8-1.5 (Nomex/phenolic)", rho=24.03, s_cell_m=0.009525,
               Ec_Pa=S.val("h10_Ec", "cores", "hrh10", "stabilized compressive modulus", 41.4, "3/8 - 1.5") * 1e6,
               Gc_Pa=S.val("h10_GW", "cores", "hrh10", "W-direction plate shear modulus", 10.3, "3/8 - 1.5") * 1e6,
               Gl_Pa=S.val("h10_GL", "cores", "hrh10", "L-direction plate shear modulus", 20.7, "3/8 - 1.5") * 1e6,
               crush_Pa=S.val("h10_crush", "cores", "hrh10", "stabilized compressive strength", 0.724, "3/8 - 1.5") * 1e6,
               shear_strength_L_Pa=S.val("h10_tL", "cores", "hrh10", "L-direction plate shear strength", 0.483, "3/8 - 1.5") * 1e6,
               shear_strength_W_Pa=S.val("h10_tW", "cores", "hrh10", "W-direction plate shear strength", 0.241, "3/8 - 1.5") * 1e6)
    nomex_wall_E = S.val("nomex_Es", "cores", "nomex_honeycomb_inplane", "Cell-wall elastic modulus Es", 7.9) * 1e9
    nomex_rho = S.val("nomex_rho13", "cores", "nomex_paper", "Nomex Type 410 paper density", 0.87) * 1000
    nomex_str = S.val("nomex_ts05", "cores", "nomex_paper", "tensile strength per unit width, machine direction", 39.0, "0.05 mm") * 100 / 0.05e-3
    nomex_k = S.val("nomex_k05", "cores", "core_conductivity", "Nomex Type 410 paper thermal conductivity", 0.103, "0.05 mm")
    h10_cte = S.val("h10_cte", "cores", "core_cte_thickness", "HRH-10 / HRH-310", 34.9) * 1e-6
    nomex_moist = S.val("nomex_moist", "cores", "nomex_moisture", "Equilibrium moisture content of Nomex paper", 5.0) / 100
    min_over_typ = 25.0 / 35.0                                        # CR-III's minimum/typical W ratio (PROJECTION transfer)
    cores["HRH-10-3/8-1.5"] = {"core": h10, "k": nomex_k * h10["rho"] / nomex_rho,
                               "mat": dict(alpha_c=h10_cte, wall_E=nomex_wall_E, wall_rho=nomex_rho, wall_yield=nomex_str,
                                           edge_allow=min_over_typ * h10["shear_strength_W_Pa"], solid_rho=nomex_rho,
                                           core_outgas_fraction=nomex_moist),
                               "basis": "Hexcel HRH-10 sheet; in-plane CTE = thickness value (PROJECTION); wall E measured "
                                        "7.9 GPa; wall density 0.87 g/cm3 paper; wall strength 39 N/cm on 0.05 mm paper; "
                                        "edge allowable typical x 25/35 (PROJECTION); conductivity paper x solidity (PROJECTION)"}
    h49 = dict(C0, name="Hexcel HRH-49-1/4-2.1 (Kevlar 49 fabric/epoxy)", rho=33.64, s_cell_m=0.00635,
               Ec_Pa=S.val("h49_Ec", "cores", "hrh49", "stabilized compressive modulus", 172.0) * 1e6,
               Gc_Pa=S.val("h49_GW", "cores", "hrh49", "W-direction plate shear modulus", 8.96) * 1e6,
               Gl_Pa=S.val("h49_GL", "cores", "hrh49", "L-direction plate shear modulus", 18.6) * 1e6,
               crush_Pa=S.val("h49_crush", "cores", "hrh49", "stabilized compressive strength", 0.896) * 1e6)
    c037 = json.load(open(f"{SRC037B}/core.json"))["rows"]
    h49["shear_strength_L_Pa"] = next(r["value"] for r in c037 if r["product"].startswith("Hexcel HRH-49")
                                      and r["property"] == "L shear strength") * 1e3
    h49["shear_strength_W_Pa"] = next(r["value"] for r in c037 if r["product"].startswith("Hexcel HRH-49")
                                      and r["property"] == "W shear strength") * 1e3
    kev_E = S.val("kev_E", "cores", "kevlar_paper", "Kevlar 49 yarn tensile modulus", 112400.0) * 1e6
    kev_rho = S.val("kev_rho", "cores", "kevlar_paper", "Kevlar 29/49 fibre density", 1.44) * 1000
    kev_k = S.val("kev_k", "cores", "kevlar_paper", "Kevlar fibre thermal conductivity", 0.04)
    h49_cte = S.val("h49_cte", "cores", "core_cte_thickness", "HRH-49 (Kevlar", 4.86) * 1e-6
    h36_moist = S.val("h36_moist", "cores", "nomex_moisture", "Moisture pickup of HRH-36", 3.4) / 100
    wall49_E, wall49_rho = 0.25 * kev_E, 0.5 * kev_rho + 0.5 * rho_resin      # woven fabric/epoxy at 50% Vf (PROJECTION)
    cores["HRH-49-1/4-2.1"] = {"core": h49, "k": kev_k * h49["rho"] / wall49_rho,
                               "mat": dict(alpha_c=h49_cte, wall_E=wall49_E, wall_rho=wall49_rho, wall_yield=300e6,
                                           edge_allow=min_over_typ * h49["shear_strength_W_Pa"], solid_rho=wall49_rho,
                                           core_outgas_fraction=h36_moist),
                               "basis": "Hexcel HRH-49 sheet; in-plane CTE = thickness value (PROJECTION); wall a woven "
                                        "Kevlar/epoxy at 50% Vf, a quarter of the yarn modulus (PROJECTION); wall strength "
                                        "300 MPa (PROJECTION); edge allowable typical x 25/35; moisture HRH-36's 3.4%"}
    # ---------------------------------------------------------------- 3. bond and seams
    cure_200F = 366.4833333333333
    S.val("af163_cure", "cfrp", "cfrp_adhesive", "AF 163-2 designed cure schedule", 250.0)
    seam_cfrp = dict(joint="co-cured scarf", seam_film=S.val("fm300_146", "cfrp", "cfrp_adhesive", "FM 300M lightest supported film", 146.0) / 1000,
                     seam_screen=S.val("fm3002_cocure", "cfrp", "cfrp_joint", "Wide-area lap shear of co-cured FM 300-2M", 17.3) * 1e6)
    S.val("fm3002_lap", "cfrp", "cfrp_joint", "Lap shear of FM 300-2M film on precured CFRP", 23.7)
    return dict(faces=faces, cores=cores, seam_cfrp=seam_cfrp, cure_200F=cure_200F, rho_resin=rho_resin)


def config_list(cure_200F, seam_cfrp):
    """The nine beryllium-free constructions run through the account."""
    configs = [("AlBeMet AM162", "CR-III 5056 3/8-1.0", cure_200F, {}, "040's Be scarf and stock"),
               ("M55J QI", "CR-III 5056 3/8-1.0", cure_200F, seam_cfrp, "AF163-2U 200 F"),
               ("M55J QI", "CR-III 5056 3/8-1.0", 298.15, seam_cfrp, "room-temperature cure (PROJECTION)"),
               ("M55J QI", "HRH-10-3/8-1.5", cure_200F, seam_cfrp, "AF163-2U 200 F"),
               ("M55J QI", "HRH-49-1/4-2.1", cure_200F, seam_cfrp, "AF163-2U 200 F"),
               ("K13D2U QI", "CR-III 5056 3/8-1.0", cure_200F, seam_cfrp, "AF163-2U 200 F"),
               ("K13D2U QI", "CR-III 5056 3/8-1.0", 298.15, seam_cfrp, "room-temperature cure (PROJECTION)"),
               ("K13D2U QI", "HRH-10-3/8-1.5", cure_200F, seam_cfrp, "AF163-2U 200 F"),
               ("K13D2U QI", "HRH-49-1/4-2.1", cure_200F, seam_cfrp, "AF163-2U 200 F")]
    return configs


def main():
    t0 = time.monotonic()
    out = {"started": datetime.datetime.now().astimezone().isoformat(), "pins": {}}
    for k, (p, want) in PIN_FILES.items():
        out["pins"][k] = pin(p, want)
    for name in ("cfrp", "albemet", "cores"):
        for ext in ("json", "md"):
            out["pins"][f"src_{name}_{ext}"] = pin(f"{S.SRC}/{name}.{ext}", None)
    for name in ("model49.py", "thermal49.py", "acct49.py", "laminate.py", "src49.py"):
        out["pins"][f"own_{name}"] = pin(os.path.join(HERE, name), None)
    assert all(v["ok"] for v in out["pins"].values()), [k for k, v in out["pins"].items() if not v["ok"]]
    F0, C0 = dict(M.F), dict(M.C)
    out["common_amendment"] = common_amendment()
    assert out["common_amendment"]["current_minus_added_is_dispatched"], out["common_amendment"]
    MAT0 = dict(M.MAT)

    # ---------------------------------------------------------------- 0. the 040 reproduction
    checks = []
    ref = [r for r in csv.DictReader(open(f"{D040}/ALL-CASES.csv")) if r["pad"] == "heavy70" and r["vented"] == "True"
           and r["R_m"] in ("15", "20", "30") and r["weather"] in ("ISA", "optimistic")]
    be_rows = A.account("Be SR-200 on CR-III 5056, AF163-2U 200 F (040)", F0, C0, .0768, {})
    for r in ref:
        mine = next(x for x in be_rows if x["R_m"] == int(r["R_m"]) and x["weather"] == r["weather"]
                    and x["floor"] == (r["floor"] == "True"))
        ok_u = (r["least_usage"] == "" and mine["least_usage"] is None) or (
            mine["least_usage"] is not None and r["least_usage"] != "" and abs(mine["least_usage"] - float(r["least_usage"])) < 2e-8)
        ok_p = abs(mine["endpoint_028b_kg"] - float(r["endpoint_payload_kg"])) < 1e-3
        checks.append({"check": f"040 {r['id']}", "mine_usage": mine["least_usage"], "theirs_usage": r["least_usage"],
                       "mine_endpoint": mine["endpoint_028b_kg"], "theirs_endpoint": float(r["endpoint_payload_kg"]),
                       "ok": bool(ok_u and ok_p)})
    assert all(c["ok"] for c in checks), [c for c in checks if not c["ok"]]
    out["checks"] = checks

    B_ = build(F0, C0)
    faces, cores, seam_cfrp, cure_200F = B_["faces"], B_["cores"], B_["seam_cfrp"], B_["cure_200F"]
    # ---------------------------------------------------------------- 4. the thermal tables per core
    tables = {"CR-III 5056 3/8-1.0": None}
    for key in ("HRH-10-3/8-1.5", "HRH-49-1/4-2.1"):
        tables[key] = TH.table([15, 20, 30], k_core=cores[key]["k"])
    out["thermal_k_core"] = {k: (0.7713 if v["k"] is None else v["k"]) for k, v in cores.items()}
    # ---------------------------------------------------------------- 5. the account
    configs = config_list(cure_200F, seam_cfrp)
    rows = list(be_rows)
    for fk, ck, cure, seam, bond in configs:
        f, c = faces[fk], cores[ck]
        thermal = tables[ck] if tables[ck] is not None else json.load(open(f"{HERE}/base040/THERMAL-TABLE.json"))
        mat = dict(MAT0)
        mat.update(c["mat"])
        mat.update(dict(rho_f=f["face"]["rho"], alpha_f=f["alpha"], tf_min=f["tf_min"]))
        mat.update(seam)
        label = f"{fk} on {ck}, {bond}"
        rows += A.account(label, f["face"], c["core"], f["nu"], mat, thermal=thermal, cure_K=cure)
        print(label, "done", round(time.monotonic() - t0), "s", flush=True)
    M.set_material(face=F0, core=C0, thermal=json.load(open(f"{HERE}/base040/THERMAL-TABLE.json")), **MAT0)
    out["rows"] = rows
    out["faces"] = {k: {kk: vv for kk, vv in v.items() if kk != "face"} | {"face": v["face"]} for k, v in faces.items()}
    out["cores"] = {k: {"core": v["core"], "mat": v["mat"], "k_W_mK": v["k"], "basis": v["basis"]} for k, v in cores.items()}
    out["seam_cfrp"] = seam_cfrp
    out["supply"] = {"be_world_t_2024": S.val("be_2024", "albemet", "be_supply", "world beryllium mine production, total", 433.0),
                     "be_world_t_2025e": S.val("be_2025", "albemet", "be_supply", "world beryllium mine production, total", 430.0),
                     "pitch_capacity_t": S.val("pitch_cap", "cfrp", "cf_supply", "continuous pitch-based carbon fibre", 1400.0),
                     "cf_demand_2024_t": S.val("cf_2024", "cfrp", "cf_supply", "demand 2024 (Composites United)", 126500.0),
                     "cf_demand_2025_t": S.val("cf_2025", "cfrp", "cf_supply", "demand 2025 (ATA CFT)", 224510.0),
                     "cf_capacity_2025_t": S.val("cf_cap", "cfrp", "cf_supply", "operational carbon fibre capacity 2025", 326080.0),
                     "materion_be_2025_klb": S.val("materion", "albemet", "be_supply", "Materion beryllium produced at Utah", 391.0)}
    out["ended"] = datetime.datetime.now().astimezone().isoformat()
    out["elapsed_s"] = time.monotonic() - t0
    out["sources_used"] = S.USED
    with open(os.path.join(HERE, "COMPUTE.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "COMPUTE.json.tmp"), os.path.join(HERE, "COMPUTE.json"))
    print("elapsed", round(out["elapsed_s"], 1))


if __name__ == "__main__":
    main()
