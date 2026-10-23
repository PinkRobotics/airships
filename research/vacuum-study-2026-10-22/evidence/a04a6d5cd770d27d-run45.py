#!/usr/bin/env python3
"""MAINLINE-045 driver: pins, the threat ladder, P2's and P3's responses, puncture and landing, detection, and the
requirement each lead needs with its cost. Reads DET.json (det45.py) and the sourcing files; writes COMPUTE.json."""
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
import dt45 as d  # noqa: E402
import p3_022d as q  # noqa: E402
import price45 as pr  # noqa: E402
import src45 as S  # noqa: E402

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def pin(path, want):
    data = open(path, "rb").read()
    h = hashlib.sha256(data).hexdigest()
    return {"path": path, "sha256": h, "bytes": len(data), "ok": (want is None or h.startswith(want))}


def main():
    t0 = time.monotonic()
    out = {"started": datetime.datetime.now().astimezone().isoformat(), "pins": {}}
    for k, (p, want) in PIN_FILES.items():
        out["pins"][k] = pin(p, want)
    for name in ("threats", "sandwich", "p3damage", "leak"):
        for ext in ("json", "md"):
            out["pins"][f"src_{name}_{ext}"] = pin(f"{S.SRC}/{name}.{ext}", None)
    for name in ("dt45.py", "det45.py", "p3_022d.py", "price45.py", "src45.py", "DET.json"):
        out["pins"][f"own_{name}"] = pin(os.path.join(HERE, name), None)
    assert all(v["ok"] for v in out["pins"].values()), [k for k, v in out["pins"].items() if not v["ok"]]
    DET = json.load(open(os.path.join(HERE, "DET.json")))
    p2, p3 = DET["p2"], DET["p3"]

    # ---------------------------------------------------------------- 1. the threats
    v25 = S.val("iec_v25", "threats", "hail_test_iec61215", "velocity, 25 mm", 23.0)
    v35 = S.val("iec_v35", "threats", "hail_test_iec61215", "velocity, 35 mm", 27.2)
    v45 = S.val("iec_v45", "threats", "hail_test_iec61215", "velocity, 45 mm", 30.7)
    v55 = S.val("iec_v55", "threats", "hail_test_iec61215", "velocity, 55 mm", 33.9)
    v65 = S.val("iec_v65", "threats", "hail_test_iec61215", "velocity, 65 mm", 36.7)
    v75 = S.val("iec_v75", "threats", "hail_test_iec61215", "velocity, 75 mm", 39.5)
    m25 = S.val("iec_m25", "threats", "hail_test_iec61215", "mass, 25 mm", 7.53) / 1e3
    m45 = S.val("iec_m45", "threats", "hail_test_iec61215", "mass, 45 mm", 43.9) / 1e3
    m75 = S.val("iec_m75", "threats", "hail_test_iec61215", "mass, 75 mm", 203.0) / 1e3
    rho_ice = m25 / (math.pi * 0.025 ** 3 / 6.0)                 # the IEC ball's own density, from its mass
    hail = []
    for D, v, m in ((0.025, v25, m25), (0.035, v35, None), (0.045, v45, m45), (0.055, v55, None), (0.065, v65, None),
                    (0.075, v75, m75)):
        mm = m if m is not None else rho_ice * math.pi * D ** 3 / 6.0
        hail.append({"D_m": D, "v_m_s": v, "m_kg": mm, "mass_basis": "IEC table" if m else "IEC 25 mm density",
                     "E_J": 0.5 * mm * v * v, "rho_v2_Pa": rho_ice * v * v})
    v2in = S.val("nbs_v2", "threats", "hail_nbs_ice_ball", "Terminal velocity of a 2 in", 32.004)
    e2in = S.val("nbs_e2", "threats", "hail_nbs_ice_ball", "Kinetic energy of a 2 in", 32.1193)
    v25w = S.val("nbs_v25wind", "threats", "hail_nbs_ice_ball", "Resultant impact velocity", 40.8432)
    design_hail = {"D_m": 0.0508, "v_m_s": v2in, "E_J": e2in, "basis": "NBSIR 82-2487 2 in ice ball at terminal velocity",
                   "rho_v2_Pa": rho_ice * v2in ** 2}
    bird_m4 = S.val("bird4", "threats", "bird_cfr25", "25.571(e)(1)", 1.81437)
    bird_m8 = S.val("bird8", "threats", "bird_cfr25", "25.631", 3.62874)
    bird_v = S.val("bird_v", "threats", "bird_flight_speed", "pigeons, swans, geese and ducks", 20.0)
    bird_rho = S.val("bird_rho", "threats", "bird_substitute", "gelatine", 0.944) * 1000.0
    vb = DET.get("vb_m_s", 18.00554)                                  # 037's VB, 35 kn
    birds = []
    for m in (bird_m4, bird_m8):
        for label, vrel in (("moored, bird's own speed", bird_v), ("flying at 037's VB into the bird", bird_v + vb)):
            birds.append({"m_kg": m, "case": label, "v_m_s": vrel, "E_J": 0.5 * m * vrel ** 2,
                          "D_m": (6.0 * m / (math.pi * bird_rho)) ** (1.0 / 3.0)})
    tools = [{"case": "Boeing small tool drop", "E_J": S.val("tool_small", "threats", "tooldrop_boeing787", "small tool drop", 5.42327)},
             {"case": "civil impact survey upper energy (CMH-17, via Airbus)", "E_J": S.val("tool_civil", "threats", "tooldrop_survey", "civil", 30.0)},
             {"case": "Airbus typical area", "E_J": S.val("tool_airbus", "threats", "tooldrop_airbus", "typical-area", 35.0)},
             {"case": "Boeing large tool drop (BVID cut-off)", "E_J": S.val("tool_bvid", "threats", "tooldrop_boeing787", "large tool drop (BVID)", 135.582)}]
    debris = [{"case": "ASTM E1996 level A, 2 g steel ball", "m_kg": 0.002,
               "v_m_s": S.val("deb_a", "threats", "debris_astm_e1996", "level A", 39.624)},
              {"case": "ASTM E1996 level D, 9 lb 2x4", "m_kg": 9.0 * 0.45359237,
               "v_m_s": S.val("deb_d", "threats", "debris_astm_e1996", "level D", 15.24)},
              {"case": "ASTM E1996 level E, 9 lb 2x4", "m_kg": 9.0 * 0.45359237,
               "v_m_s": S.val("deb_e", "threats", "debris_astm_e1996", "level E", 24.384)}]
    for r in debris:
        r["E_J"] = 0.5 * r["m_kg"] * r["v_m_s"] ** 2
    T5, p5, rho5 = d.isa(500.0)
    V = 4.0 / 3.0 * math.pi * 1000.0
    m_eff = rho5 * V * 1.5                                            # hull plus 0.5 rho V added mass
    S.val("added_mass", "leak", "added_mass", "Added (virtual) mass of a sphere", 0.5)
    moor = []
    for label, vc in (("TAR 473 landing floor", S.val("tar473", "leak", "airship_landing", "minimum limit vertical descent", 0.914)),
                      ("14 CFR 25.473 descent velocity (analogy)", S.val("cfr25473", "threats", "landing_cfr25", "Limit descent velocity", 3.048))):
        moor.append({"case": label, "v_m_s": vc, "m_eff_kg": m_eff, "E_J": 0.5 * m_eff * vc * vc})
    out["threats"] = {"hail_iec": hail, "rho_ice": rho_ice, "design_hail": design_hail, "hail_wind_resultant_m_s": v25w,
                      "birds": birds, "tools": tools, "debris": debris, "mooring": moor}

    # ---------------------------------------------------------------- 2. P2: the dent, its growth, its knockdown
    be_y = S.val("be_yield", "sandwich", "be_sr200_tensile", "0.2% offset yield", 345.0) * 1e6
    S.val("be_uts", "sandwich", "be_sr200_tensile", "ultimate tensile", 483.0)
    S.val("be_elong", "sandwich", "be_ductility", "SR-200 minimum tensile elongation", 10.0)
    be_E = S.val("be_E", "sandwich", "be_properties", "elastic modulus", 290.0) * 1e9
    S.note("be_brittle", "sandwich", "be_fracture", "low impact resistance")
    S.val("be_kic", "sandwich", "be_fracture", "Plane-strain crack toughness", 11.0)
    crush = S.val("cr3_crush", "sandwich", "core_crush_cr3", "crush strength (typical)", 0.241) * 1e6
    bare = S.val("cr3_bare", "sandwich", "core_crush_cr3", "bare compressive strength", 0.379) * 1e6
    scat = S.val("cr3_scatter", "sandwich", "core_crush_cr3", "Scatter statement", 20.0) / 100.0
    nu_be = 0.0752
    tf, sig_m = p2["tf_m"], p2["sigma_m_Pa"]
    N = sig_m * tf
    Dp = be_E * tf ** 3 / (12.0 * (1.0 - nu_be ** 2))
    q0 = q.P - 2.0 * N / 10.0                                         # the core's share on the undamaged shell
    lam2 = {"clamped": d.special.jn_zeros(1, 1)[0] ** 2, "ss": d.ss_root(nu_be) ** 2}
    growth = []
    for b_mm in (10, 15, 20, 25, 27.5, 30, 35, 40, 50, 60, 80, 100, 150):
        bb = b_mm / 1e3
        row = {"b_m": bb}
        for k, l2 in lam2.items():
            for tag, scr in (("typ", crush), ("min", crush * (1.0 - scat))):
                g = d.growth_depth(bb, N, Dp, scr, q0, l2)
                row[f"{k}_{tag}_m"] = None if math.isinf(g) else g
        growth.append(row)
    # calibration of the dent model against the sourced tests
    cal = {"pach": {"test_depth_m": S.val("pach_depth", "sandwich", "dent_vs_energy_al_honeycomb", "Residual dent depth from the Pach", 1.1),
                    "test_E_J": S.val("pach_E", "sandwich", "dent_vs_energy_al_honeycomb", "Impact energy used to create a 1.2 mm", 1.57),
                    "test_face_m": S.val("pach_tf", "sandwich", "dent_vs_energy_al_honeycomb", "Panel construction used in the Pach", 0.508) / 1e3}}
    for scr in (0.4e6, 0.9e6):
        dd, bb, xi = d.dent_energy(cal["pach"]["test_E_J"], cal["pach"]["test_face_m"], 345e6, scr, R_ind=0.0127)
        cal["pach"][f"model_crush_{scr/1e6:.1f}MPa"] = {"depth_m": dd, "diameter_m": 2 * bb}
    S.val("clarke_disp", "sandwich", "dent_vs_core_density", "Maximum impactor displacement", 2.37)
    S.val("clarke_16", "sandwich", "core_crush_depth", "Least-dense core", 16.0)
    dd, bb, xi = d.dent_energy(1.07 * 0.8, 0.301e-3, 503e6, crush, R_ind=0.0127)
    cal["clarke"] = {"fe_max_displacement_m": 2.37e-3, "model_depth_m": dd, "model_diameter_m": 2 * bb,
                     "ratio_fe_over_model": 2.37e-3 / dd}
    S.val("clarke_slope", "sandwich", "core_crush_depth", "Core damage width versus dent width", 1.05)
    # Shi et al.: the ice's effective contact pressure on a plate, from its own plastic work and dent
    shi_ke = 64.84
    shi_v = 46.88
    shi_dent = S.val("shi_dent", "sandwich", "hail_ice_impact", "3 mm aluminium plate, 50.8 mm ice at 46.88", 0.48) / 1e3
    shi_frac = S.val("shi_frac", "sandwich", "hail_ice_impact", "Plastic work as a fraction", 6.55) / 100.0
    q_shi = shi_frac * shi_ke / shi_dent / (math.pi * 0.0254 ** 2)
    k_shi = q_shi / (rho_ice * shi_v ** 2)
    cal["shi"] = {"q_eff_Pa": q_shi, "k_over_rho_v2": k_shi}
    S.val("stac", "sandwich", "hail_ice_impact", "dent threshold between 30 and 40", 40.0)

    def verdict(b, dep):
        """stable / grows, on the clamped and simply supported patch readings; and the dent's membrane strain."""
        out_ = {"face_membrane_strain": 0.5 * (dep / b) ** 2 if b > 0 else 0.0}
        for k, l2 in lam2.items():
            g = d.growth_depth(b, N, Dp, crush, q0, l2)
            out_[k] = "stable" if dep < g else "grows"
            out_[k + "_threshold_m"] = None if math.isinf(g) else g
        return out_
    p2_threats = []
    for h in hail + [dict(design_hail, m_kg=None)]:
        a = h["D_m"] / 2.0
        rows_ = {}
        for tag, qq in (("fluid rho v2", h["rho_v2_Pa"]), ("Shi-calibrated k rho v2", k_shi * h["rho_v2_Pa"])):
            dep, bb = d.dent_pressure(qq, a, tf, be_y, crush)
            rows_[tag] = {"q_Pa": qq, "depth_m": dep, "crushed_diameter_m": 2 * bb if dep > 0 else 0.0,
                          **(verdict(bb, dep) if dep > 0 else {"clamped": "no crush", "ss": "no crush"})}
        dep, bb, xi = d.dent_energy(h["E_J"], tf, be_y, crush, footprint=a)
        rows_["all energy to the panel"] = {"E_J": h["E_J"], "depth_m": dep, "crushed_diameter_m": 2 * bb, **verdict(bb, dep)}
        p2_threats.append({"threat": f"hail {h['D_m']*1e3:.1f} mm at {h['v_m_s']:.1f} m/s", "lambda": bb / p2["width_lambda1_m"],
                           "readings": rows_})
    for t in tools:
        dep, bb, xi = d.dent_energy(0.8 * t["E_J"], tf, be_y, crush, R_ind=0.0127)
        p2_threats.append({"threat": f"{t['case']}, {t['E_J']:.1f} J, 25.4 mm hemisphere", "lambda": bb / p2["width_lambda1_m"],
                           "readings": {"80 percent absorbed": {"depth_m": dep, "crushed_diameter_m": 2 * bb, **verdict(bb, dep)},
                                        "depth x2 (Clarke band)": {"depth_m": 2 * dep, "crushed_diameter_m": 2 * bb,
                                                                   **verdict(bb, 2 * dep)}}})
    for bd in birds:
        a = bd["D_m"] / 2.0
        dep, bb = d.dent_pressure(bird_rho * bd["v_m_s"] ** 2, a, tf, be_y, crush)
        dep2, bb2, _ = d.dent_energy(bd["E_J"], tf, be_y, crush, footprint=a)
        p2_threats.append({"threat": f"bird {bd['m_kg']:.2f} kg at {bd['v_m_s']:.1f} m/s ({bd['case']})", "lambda": bb2 / p2["width_lambda1_m"],
                           "readings": {"fluid rho v2": {"depth_m": dep, "crushed_diameter_m": 2 * bb, **verdict(bb, dep)},
                                        "all energy to the panel": {"E_J": bd["E_J"], "depth_m": min(dep2, tc_lim := p2["tc_m"]),
                                                                    "bottoms_out": dep2 >= tc_lim,
                                                                    "crushed_diameter_m": 2 * bb2, **verdict(bb2, dep2)}}})
    for m_ in moor:
        bb = 0.25                                                       # a fendered contact 0.5 m across (PROJECTION)
        dep = m_["E_J"] / (crush * math.pi * bb * bb)
        p2_threats.append({"threat": f"mooring contact at {m_['v_m_s']:.3f} m/s ({m_['case']}), 0.5 m contact",
                           "lambda": bb / p2["width_lambda1_m"],
                           "readings": {"core crush only": {"E_J": m_["E_J"], "depth_m": dep, "bottoms_out": dep >= p2["tc_m"],
                                                            "crushed_diameter_m": 2 * bb, **verdict(bb, dep),
                                                            "global_allowed_m": d.depth_allowed(p2["gamma_need"], bb / p2["width_lambda1_m"], p2["teq_m"])}}})
    # the largest undetected dent that keeps SF 1: global (015) and local (growth), by width
    undetected = []
    for D_mm in (20, 27.1, 40, 54.8, 60, 80, 100, 160, 300, 450, 700, 1000):
        bb = D_mm / 2e3
        lam = bb / p2["width_lambda1_m"]
        glob = d.depth_allowed(p2["gamma_need"], lam, p2["teq_m"]) if lam <= 5 else None
        row = {"diameter_m": D_mm / 1e3, "lambda_if_r0_is_half_width": lam,
               "global_allowed_m": None if glob is None or math.isinf(glob) else glob}
        for k, l2 in lam2.items():
            g = d.growth_depth(bb, N, Dp, crush, q0, l2)
            row[f"growth_{k}_m"] = None if math.isinf(g) else g
        undetected.append(row)
    bvid = {"nasa_1p27mm": S.val("bvid_nasa", "sandwich", "bvid_threshold", "Generally accepted BVID", 1.27),
            "boeing_0p25mm": S.val("bvid_boeing", "sandwich", "bvid_threshold", "Boeing BVID dent-depth range", 0.25),
            "npl_0p5mm": S.val("bvid_npl", "sandwich", "bvid_threshold", "BVID dent-depth values compiled by Boctor", 0.5)}
    tap = {"manual_a9095_m": S.val("tap_manual", "sandwich", "ndi_detection", "Manual tap test a90/95", 41.8) / 1e3,
           "automated_a9095_m": S.val("tap_auto", "sandwich", "ndi_detection", "Automated tap test a90/95", 29.0) / 1e3,
           "best_inspector_m": S.val("tap_best", "sandwich", "ndi_detection", "Best-inspector manual tap", 25.4) / 1e3}
    S.note("tap_thick", "sandwich", "ndi_detection", "Tap-test sensitivity falls")
    S.note("ndi_limits", "sandwich", "ndi_detection", "Limits of NDT methods")
    S.note("sensor_net", "sandwich", "ndi_detection", "Impact detection by sensor network")
    S.note("hidden_crush", "sandwich", "dent_relaxation", "Shallow residual print can hide")
    S.note("disbond_hide", "sandwich", "dent_relaxation", "Disbond lets the face relax")
    S.note("cai_wrinkle", "sandwich", "cai_honeycomb", "Dented-panel failure mode in CAI")
    S.note("cai_abrupt", "sandwich", "cai_honeycomb", "Dent grows abruptly")
    S.note("preload", "sandwich", "cai_preloaded_impact", "Threshold of compressive strain")
    S.val("gilioli_fail", "sandwich", "face_rupture_threshold", "Impact energy above which the 1 mm", 200.0)
    S.val("clarke_rupture", "sandwich", "face_rupture_threshold", "Impact energy per dent area", 1.62)
    # pricing the P2 options on 028b's own least set
    pricing2 = {"patch": [], "extra_mass": [], "denser_core": []}
    for edge in ("clamped", "ss"):
        for Dm in ((0.03, 0.045, 0.0548, 0.059) if edge == "clamped" else (0.02, 0.0271, 0.0293)):
            u = pr.usage_with_patch(Dm, edge)
            pricing2["patch"].append({"edge": edge, "D_m": Dm, "usage": u["max_usage"], "feasible": u["feasible"],
                                      "gamma": u["gamma_need"], "tf_m": u["tf"], "tc_m": u["tc"]})
    for m in (13.0, 25.0, 50.0, 100.0, 200.0):
        u = pr.usage_extra_mass(m)
        pricing2["extra_mass"].append({"kg": m, "kg_per_m2": m / (4 * math.pi * 100), "usage": u["max_usage"],
                                       "gamma": u["gamma_need"]})
    lo, hi = 0.0, 25.0
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        if pr.usage_extra_mass(mid)["max_usage"] <= 1.0:
            lo = mid
        else:
            hi = mid
    pricing2["mass_margin_kg"] = lo
    for k in (1.25, 1.5, 2.0, 3.0):
        u = pr.usage_denser_core(k)
        pricing2["denser_core"].append({"k": k, "crush_Pa": crush * k ** (5 / 3), "usage": u["max_usage"],
                                        "gamma": u["gamma_need"], "feasible": u["feasible"]})
    # the crush strength the design hail's dent needs to stop growing, and the venting that does it instead
    dh = next(r for r in p2_threats if r["threat"].startswith("hail 50.8"))
    need = {}
    for tag in ("Shi-calibrated k rho v2", "all energy to the panel"):
        rr = dh["readings"][tag]
        bb, dep = rr["crushed_diameter_m"] / 2, rr["depth_m"]
        ncr = lam2["clamped"] * Dp / (bb * bb)
        need[tag] = {"b_m": bb, "depth_m": dep,
                     "crush_needed_Pa": q0 + dep * 4.0 * (N - ncr) / (bb * bb) if N > ncr else None,
                     "vent_fraction_dp": ncr / N, "air_admitted_kg": (1.0 - min(ncr / N, 1.0)) * rho5 * V}
    pricing2["design_hail_needs"] = need
    out["p2"] = {"N_N_per_m": N, "D_face_Nm": Dp, "q0_Pa": q0, "crush_Pa": crush, "bare_Pa": bare, "crush_scatter": scat,
                 "growth": growth, "calibration": cal, "threats": p2_threats, "undetected": undetected, "bvid": bvid,
                 "tap": tap, "pricing": pricing2, "patch": p2["patch"], "hole_edge": p2["hole_edge"]}

    # ---------------------------------------------------------------- 3. P3: tubes, film, one lost member
    E_sic = S.val("sic_E", "p3damage", "sic_modulus", "Modulus of elasticity", 430.0, "Hexoloy") * 1e9
    nu_sic = 0.16                                                   # assumed; no Poisson row was sourced
    weib = {"tube C-ring flexure": (S.val("tube_cring", "p3damage", "sic_tube_strength", "C-ring", 299.0) * 1e6, 4.6),
            "tube sectored flexure": (S.val("tube_sector", "p3damage", "sic_tube_strength", "Sectored flexure", 192.0) * 1e6, 5.5),
            "Hexoloy SA 4-pt bars": (S.val("hex_4pt", "p3damage", "sic_flexure", "4-point bending, room", 380.0) * 1e6
                                     / math.gamma(1.0 + 1.0 / 10.0), 10.0)}
    S.val("hex_m", "p3damage", "sic_weibull", "Weibull modulus (2 parameter)", 10.0, "Hexoloy SA sintered alpha")
    S.note("cr134990", "p3damage", "sic_impact", "fracture / catastrophic damage")
    ro, tw = p3["ro"], p3["t"]
    tube = []
    for h in hail + [dict(design_hail, m_kg=None)]:
        q_flow = h["rho_v2_Pa"]
        best = (0.0, None)
        for c_mm in (2, 4, 6, 8, 10, 12, 15, 20):
            c = c_mm / 1e3
            if c > h["D_m"] / 2:
                continue
            M, lch = d.disc_moment(q_flow * math.pi * c * c, c, E_sic, tw, ro, nu_sic)
            s = 6.0 * M / tw ** 2
            if s > best[0]:
                best = (s, c)
        sig_per_MPa = best[0] / (q_flow / 1e6)                       # bending stress per MPa of contact pressure
        s_shi = best[0] * k_shi
        pf_shi = {k: 1.0 - math.exp(-(s_shi / s0) ** m) for k, (s0, m) in weib.items()}
        row = {"D_m": h["D_m"], "v_m_s": h["v_m_s"], "q_flow_Pa": q_flow, "sigma_flow_Pa": best[0], "c_m": best[1],
               "sigma_per_MPa_contact": sig_per_MPa,
               "Pf_flow": {k: 1.0 - math.exp(-(best[0] / s0) ** m) for k, (s0, m) in weib.items()},
               "sigma_shi_Pa": s_shi, "Pf_shi": pf_shi,
               "strikes_to_half_shi": {k: (math.log(2.0) / v if v > 0 else None) for k, v in pf_shi.items()},
               "q_to_fracture_Pa": {k: s0 / sig_per_MPa * 1e6 for k, (s0, m) in weib.items()}}
        tube.append(row)
    film = {"stress_Pa": p3["film_stress_Pa"], "ply_fibre_stress_Pa": p3["ply_fibre_stress_Pa"],
            "fibre_strength_Pa": S.val("zylon_uts", "p3damage", "zylon_tear", "Tensile strength of ZYLON", 5.8) * 1e9,
            "knot_fraction": S.val("zylon_knot", "p3damage", "zylon_tear", "Knot strength", 32.0) / 100.0,
            "daylight_residual": S.val("zylon_uv", "p3damage", "zylon_tear", "daylight", 35.0) / 100.0}
    film["fibre_utilisation"] = film["ply_fibre_stress_Pa"] / film["fibre_strength_Pa"]
    gcs = {"StratoFilm 420 J_c low": S.val("strato_jc", "p3damage", "balloon_film_tear", "Critical J-integral", 500.0),
           "Mylar EWF 10 mm/min": S.val("mylar_ewf", "p3damage", "pet_tear", "10 mm/min", 40.2) * 1e3,
           "Mylar EWF 1 m/s": S.val("mylar_ewf_fast", "p3damage", "pet_tear", "1 m/s", 63.7) * 1e3}
    k_el = S.val("kapton_elm25", "p3damage", "kapton_tear", "Propagating tear strength (Elmendorf", 0.07, "25 um")
    gcs["Kapton HN Elmendorf, 2F/t"] = 2.0 * k_el / 25e-6
    film["tear"] = {}
    for E_f in (81e9, 180e9):                                      # PROJECTION: no Zylon film modulus was sourced
        film["tear"][f"E_{E_f/1e9:.0f}GPa"] = {k: E_f * g / (math.pi * film["stress_Pa"] ** 2) for k, g in gcs.items()}
    film["merged_bay"] = DET["film_merged_bay"]
    film["stop_25mm_slit"] = {}
    for E_f in (81e9, 180e9):
        sig_t = math.sqrt(E_f * gcs["Mylar EWF 10 mm/min"] / (math.pi * 0.025))
        pt = q.best(film_sig=sig_t)
        film["stop_25mm_slit"][f"E_{E_f/1e9:.0f}GPa"] = {"film_stress_Pa": sig_t, "SF": pt["lam"] if pt else None,
                                                         "film_kg": pt["m_film"] if pt else None}
    S.note("ripstop", "p3damage", "kapton_tear", "Ripstop requirement")
    S.note("kapton_weak", "p3damage", "kapton_tear", "Qualitative: resistance of Kapton")
    # tear-stopping film: the stress at which a slit of half-length a does not run, against the film allowable
    pricing3 = {"film_allowable": [], "wall_min": [], "extra_mass": []}
    for sig in (1740e6, 1000e6, 600e6, 400e6, 300e6, 200e6):
        pt = q.best(film_sig=sig)
        pricing3["film_allowable"].append({"film_allowable_Pa": sig, "SF": pt["lam"], "s": pt["s"], "OD": 2 * pt["ro"],
                                           "wall": pt["t"], "film_kg": pt["m_film"], "tube_kg": pt["m_tube"]})
    for tmin in (1.5e-3, 2.0e-3, 3.0e-3):
        pt = q.best(wall_min=tmin)
        pricing3["wall_min"].append({"wall_min_m": tmin, "SF": (pt["lam"] if pt else None),
                                     "OD": (2 * pt["ro"] if pt else None), "s": (pt["s"] if pt else None)})
    for em in (50.0, 100.0, 200.0, 400.0):
        pt = q.best(extra_mass=em)
        pricing3["extra_mass"].append({"extra_kg": em, "SF": pt["lam"]})
    out["p3"] = {"tube_hail": tube, "weibull": {k: {"sigma0_Pa": s0, "m": m} for k, (s0, m) in weib.items()},
                 "film": film, "frame": DET["frame"], "pricing": pricing3,
                 "cover_fraction": p3["projected_tube_cover_fraction"]}

    # ---------------------------------------------------------------- 4. puncture, descent and landing
    cd_hole = S.val("cd_sharp", "leak", "orifice_cd", "sharp-edged orifice", 0.6)
    S.val("cd_crit", "leak", "orifice_choked", "Critical (choking) pressure ratio", 0.528)
    S.val("sphere_cd", "leak", "sphere_drag", "turbulent flow", 0.47)
    S.val("sphere_cd_crisis", "leak", "sphere_drag", "Drag crisis", 0.2)
    regs = {"cfr101_19": S.note("cfr101_19", "leak", "cfr101_deflation", "rapidly deflates"),
            "cfr101_13": S.val("cfr101_13", "leak", "cfr101_limits", "maximum operating height", 152.4),
            "tar_887c": S.val("tar887c", "leak", "airship_valve", "Ballonet air-induction", 7.5),
            "tar_473": S.val("tar473b", "leak", "airship_landing", "minimum limit vertical descent", 0.914),
            "tar_883g": S.note("tar883g", "leak", "aerostat_deflation", "Rapid envelope deflation"),
            "tar_895": S.note("tar895", "leak", "airship_ballast", "Disposable ballast capacity"),
            "cfr31_27c_in": S.val("cfr3127", "leak", "cfr31_balloon", "drop test", 36.0)}
    S.note("vac_rough", "leak", "vacuum_airship", "small leaks in face skins")
    out["leak"] = {"holes": DET["holes"], "big": DET["big_holes"], "touchdown_thresholds_hole_m": DET["touchdown_thresholds_hole_m"],
                   "landing_valve": DET["landing_valve"], "neutral_dp": DET["neutral_dp_note"], "cd_hole": cd_hole,
                   "regs": regs, "drop_test_speed_m_s": math.sqrt(2 * 9.80665 * 36 * 0.0254)}
    # internal-pressure leak detection: the hole a gauge finds in an hour at a given resolution
    det = []
    for res in (1.0, 0.1):
        md = res * V / (d.R_AIR * T5 * 3600.0)
        A = md / d.mdot_hole(1.0, cd_hole, p5, T5, 0.0)
        det.append({"resolution_Pa_per_h": res, "mdot_kg_s": md, "hole_m": 2 * math.sqrt(A / math.pi)})
    out["leak"]["pressure_detection"] = det
    out["DET"] = {"p2": p2, "p3": p3}
    out["ended"] = datetime.datetime.now().astimezone().isoformat()
    out["elapsed_s"] = time.monotonic() - t0
    out["sources_used"] = S.USED
    with open(os.path.join(HERE, "COMPUTE.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "COMPUTE.json.tmp"), os.path.join(HERE, "COMPUTE.json"))
    print("elapsed", round(out["elapsed_s"], 1))


if __name__ == "__main__":
    main()
