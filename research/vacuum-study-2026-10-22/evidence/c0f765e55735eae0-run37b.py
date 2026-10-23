#!/usr/bin/env python3
"""MAINLINE-037b driver: pins, reproduction checks, the cure residual in both readings, relief, fixes priced in the
face-core shear factor, in mass, and in 028b's gamma and wrinkle usage. Writes COMPUTE.json."""
import datetime
import hashlib
import json
import math
import os
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import bond37b as b  # noqa: E402

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def pin(path, want):
    data = open(path, "rb").read()
    h = hashlib.sha256(data).hexdigest()
    return {"path": path, "sha256": h, "bytes": len(data), "ok": (want is None or h.startswith(want))}


def val(f, pid, prop_text, prod_text, value, tol=1e-3):
    """The sourced row with this property id, property text and product text; its value is asserted."""
    hits = [(i, r) for i, r in enumerate(FILES[f]["rows"]) if r["property_id"] == pid and prop_text in r["property"]
            and prod_text in str(r.get("product"))]
    if len(hits) > 1:
        hits = [(i, r) for i, r in hits if r["value"] is not None and abs(r["value"] - value) <= tol * max(1, abs(value))]
    assert len(hits) == 1, (f, pid, prop_text, prod_text, len(hits))
    i, r = hits[0]
    assert r["value"] is not None and abs(r["value"] - value) <= tol * max(1.0, abs(value)), (f, pid, r["value"], value)
    return r["value"], {"file": f"{f}.json", "index": i}


def dens(f, pid, prop_text, prod_text):
    """The density printed on that sourced row."""
    hits = [(i, r) for i, r in enumerate(FILES[f]["rows"]) if r["property_id"] == pid and prop_text in r["property"]
            and prod_text in str(r.get("product"))]
    assert len(hits) >= 1 and hits[0][1].get("density_kg_m3"), (f, pid, prop_text, prod_text)
    return hits[0][1]["density_kg_m3"], {"file": f"{f}.json", "index": hits[0][0], "field": "density_kg_m3"}


def main():
    t0 = time.monotonic()
    out = {"started": datetime.datetime.now().astimezone().isoformat(), "pins": {}, "sources_used": {}}
    for k, (p, want) in PIN_FILES.items():
        out["pins"][k] = pin(p, want)
    for name in ("adhesive", "core", "interlayer"):
        for ext in ("json", "md"):
            out["pins"][f"src_{name}_{ext}"] = pin(f"{SRC}/{name}.{ext}", None)
    assert all(v["ok"] for v in out["pins"].values()), [k for k, v in out["pins"].items() if not v["ok"]]

    def use(key, *args, **kw):
        v, ref = val(*args, **kw)
        out["sources_used"][key] = {"value": v, **ref}
        return v

    # ---------------------------------------------------------------- sourced inputs
    T = lambda f: (f - 32.0) * 5.0 / 9.0 + 273.15  # noqa: E731
    af_cure_F = use("af163_cure_low_F", "adhesive", "af163_cure", "Alternative low-temperature cure", "AF 163-2 family", 200.0)
    af_tg_dry_C = use("af163_tg_dry_C", "adhesive", "af163_cure", "Glass transition temperature, dry", "AF 163-2U", 108.0)
    af_creep_in = use("af163_creep_in", "adhesive", "af163_cure", "Creep, 180 F", "AF 163-2U", 0.0002, tol=1e-6)
    hb679_C = use("hexbond679_cure_C", "adhesive", "rt_cure_adhesive", "Typical cure temperature", "HexBond 679", 80.0)
    hb679_aw = use("hexbond679_areal_g_m2", "adhesive", "rt_cure_adhesive", "Areal weight", "HexBond 679", 250.0)
    hb679_min_C = 70.0   # 8 h at 70 C, the row 'Isothermal cure time to 95 % conversion' at 70 C
    use("hexbond679_70C_min", "adhesive", "rt_cure_adhesive", "Isothermal cure time", "HexBond 679", 480.0)
    ea9394_lap = use("ea9394_lap_psi", "adhesive", "rt_cure_adhesive", "Lap shear strength at 77 F", "EA 9394", 4200.0)
    ea9394_rho = use("ea9394_density", "adhesive", "rt_cure_adhesive", "Mixed density", "EA 9394", 1.36)
    rtv_g = use("rtv566_G_MPa", "interlayer", "silicone_adhesive", "Shear modulus (measured, thin layers)", "RTV 566", 0.635)
    rtv_sg = use("rtv566_sg", "interlayer", "silicone_adhesive", "Specific gravity of parts", "RTV566", 1.49)
    rtv_lap = use("rtv566_lap_MPa", "interlayer", "silicone_adhesive", "Lap shear strength, primed on aluminium", "RTV566", 3.2)
    foil_e_5052 = use("foil_5052_E_GPa", "core", "foil_properties", "Young's modulus, 5052-H39 foil", "5052-H39", 56.537)
    foil_y_5052 = use("foil_5052_yield_MPa", "core", "foil_properties", "0.2 percent yield strength, 5052-H39", "5052-H39", 227.53)
    foil_e_5056 = use("foil_5056_E_GPa", "core", "foil_properties", "Young's modulus, 5056-H14", "5056-H14", 67.0)
    foil_rho_5056, ref = dens("core", "foil_properties", "Young's modulus, 5056-H14", "5056-H14")
    out["sources_used"]["foil_5056_rho"] = {"value": foil_rho_5056, **ref}

    def cdens(key, pid, prop_text, prod_text):
        v, r = dens("core", pid, prop_text, prod_text)
        out["sources_used"][key] = {"value": v, **r}
        return v
    al_cte = use("al_core_cte_thickness", "core", "core_aluminium_ref", "coefficient of thermal expansion", "CR III", 2.376e-5, tol=1e-3)
    ti_cte = use("ti325_cte", "core", "foil_properties", "CTE, Ti-3Al-2.5V", "TIMETAL", 9.61e-6, tol=1e-3)
    ph157_cte = use("ph157_cte", "core", "foil_properties", "CTE, PH 15-7 Mo", "PH 15-7", 1.1e-5, tol=1e-3)
    ph177_cte = use("ph177_cte", "core", "foil_properties", "CTE, 17-7 PH", "17-7 PH", 1.53e-5, tol=1e-3)
    def min_psi(prop_text):
        """The minimum-average strength printed beside the typical value on the CR-III Table II row."""
        hits = [r for r in FILES["core"]["rows"] if r["property_id"] == "core_aluminium_ref" and r["property"] == prop_text]
        assert len(hits) == 1, prop_text
        printed = hits[0]["value_as_printed"]
        lo = float(printed.split("(min ")[1].split(" psi")[0])
        out["sources_used"][f"cr3_{prop_text.split()[0]}_min_psi"] = {"value": lo, "file": "core.json",
                                                                       "field": "value_as_printed", "printed": printed}
        return lo
    s_min_psi = min_psi("W shear strength")     # 25 psi, Table II minimum average
    s_l_min_psi = min_psi("L shear strength")   # 45 psi
    s_l_typ = use("cr3_L_strength_kPa", "core", "core_aluminium_ref", "L shear strength", "CR-III-3/8-5056-1.0N", 379.21) * 1e3
    g_l = use("cr3_L_modulus_MPa", "core", "core_aluminium_ref", "L shear modulus", "CR-III-3/8-5056-1.0N", 103.42) * 1e6
    use("cr3_W_strength_kPa", "core", "core_aluminium_ref", "W shear strength", "CR-III-3/8-5056-1.0N", 241.32)
    use("cr3_W_modulus_MPa", "core", "core_aluminium_ref", "W shear modulus", "CR-III-3/8-5056-1.0N", 46.884)

    # ---------------------------------------------------------------- 037 reproduction and the 028b replica
    R037 = json.load(open(f"{b.D037}/RESULTS.json"))
    th = R037["p2_thermal"]["coated_outer"]
    t_hot, swing = th["T_outer_subsolar_K"], th["day_night_outer_swing_K"]
    t_cold = t_hot - swing
    da_al = b.ALPHA_AL - b.ALPHA_BE
    checks = []

    def rec(name, mine, theirs, tol):
        checks.append({"check": name, "mine": mine, "theirs": theirs,
                       "ok": abs(mine - theirs) <= tol * max(1.0, abs(theirs))})
    rec("037 lambda", b.lam_037(b.GC_W, b.TF37, b.TC37), th["shear_lag_from_day_rise"]["lambda_1_per_m"], 1e-12)
    rec("037 day-rise tau", b.tau_037(da_al * (t_hot - b.T_AIR)), th["shear_lag_from_day_rise"]["tau_Pa"], 1e-9)
    rec("037 swing tau", b.tau_037(da_al * swing), th["shear_lag_from_swing"]["tau_Pa"], 1e-9)
    rec("037 swing SF", b.SHEAR_W / b.tau_037(da_al * swing), th["shear_lag_from_swing"]["SF_vs_shear_W"], 1e-9)
    u_lead = b.usage_028b(b.base_q())
    rec("028b nominal AF/scarf max usage (nu 0.0752)", u_lead["max_usage"], 0.971978, 2e-6)
    rec("028b gamma needed", u_lead["gamma_need"], 0.564164, 2e-6)
    rec("028b wrinkle needed", u_lead["Q_need"], 0.434628, 2e-6)
    rec("028b face mm", u_lead["tf"] * 1e3, 0.794624, 2e-6)
    rec("028b core mm", u_lead["tc"] * 1e3, 23.2372, 2e-6)
    rec("028b nu 0.33 max usage", b.usage_028b(b.base_q(nu=0.33))["max_usage"], 0.906439, 2e-6)
    out["checks"] = checks
    assert all(c["ok"] for c in checks), [c for c in checks if not c["ok"]]

    # ---------------------------------------------------------------- the residual state, aluminium core
    kb_al = b.k_biax(foil_e_5056 * 1e9, 16.018463373960138, foil_rho_5056)   # 5056 at its sourced 67 GPa, 2700 kg/m3
    s_typ, s_min = b.SHEAR_W, s_min_psi * 6894.757293168
    sft_cases = [
        ("AF 163-2U, datasheet 250 F cure, stress-free at cure", T(250.0)),
        ("AF 163-2U, stress-free at its dry Tg (108 C), the lower bound of the cure-or-Tg rule", af_tg_dry_C + 273.15),
        ("AF 163-2U, datasheet 200 F alternative cure (2-6 h)", T(af_cure_F)),
        ("HexBond 679 low-temperature film, 80 C cure", hb679_C + 273.15),
        ("HexBond 679, 70 C minimum (8 h)", hb679_min_C + 273.15),
        ("Room-temperature cure (EA 9394 class), 25 C", 298.15),
        ("Cure at the middle of the day-night swing", 0.5 * (t_hot + t_cold)),
    ]
    s_l_min = s_l_min_psi * 6894.757293168
    k_dw, wall_dw = b.doubled_wall_cell()
    sig37 = R037["face_working_stress_Pa"]
    m37 = R037["p2"]["uniform"]["modes"]
    local37 = ("face_compression", "face_wrinkling", "intracell_dimpling", "scarf_mean_shear")
    residual = []
    for label, sft in sft_cases:
        worst = max(abs(sft - t_cold), abs(sft - t_hot))
        d = da_al * worst
        t37 = b.tau_037(d)
        te, aux = b.tau_edge(d, kb_al)
        te_l, _ = b.tau_edge(d, kb_al, gc=g_l)                       # an edge across the ribbon: L shear
        te_dw, _ = b.tau_edge(d, kb_al * k_dw)                       # doubled ribbon walls
        # the face compression the core's pull adds at 037's point, and 037's face-local factors with it
        sr37 = kb_al * d * b.TC37 / (2.0 * b.TF37)
        scale = sig37 / (sig37 + sr37)
        modes = {k: (v * scale if k in local37 else v) for k, v in m37.items()}
        least = min(modes, key=modes.get)
        residual.append({"case": label, "sft_K": sft, "sft_C": sft - 273.15, "worst_dT_K": worst,
                         "worst_at": "cold night" if abs(sft - t_cold) >= abs(sft - t_hot) else "hot day",
                         "tau_037_kPa": t37 / 1e3, "SF_037_typ": s_typ / t37, "SF_037_min": s_min / t37,
                         "tau_free_edge_kPa": te / 1e3, "SF_edge_typ": s_typ / te, "SF_edge_min": s_min / te,
                         "SF_edge_L_typ": s_l_typ / te_l, "SF_edge_L_min": s_l_min / te_l,
                         "SF_edge_doubled_typ": s_typ / te_dw, "SF_edge_doubled_min": s_min / te_dw,
                         "transfer_length_mm": aux["transfer_length_m"] * 1e3,
                         "wall_stress_MPa": foil_e_5056 * 1e3 * d,
                         "wall_SF_on_5052H39_yield": foil_y_5052 / (foil_e_5056 * 1e3 * d),
                         "wall_stress_doubled_single_MPa": wall_dw * foil_e_5056 * 1e3 * d,
                         "wall_SF_doubled_single": foil_y_5052 / (wall_dw * foil_e_5056 * 1e3 * d),
                         "face_compression_added_037_MPa": sr37 / 1e6,
                         "p2_037_modes_with_residual": modes, "p2_037_least": least, "p2_037_least_SF": modes[least],
                         "p2_037_face_SF_on_345": R037["face_SF_on_345_uniform"] * scale})
    out["residual"] = residual
    # 037's screen asks the core to hold each face at the core's own expansion: a face force E_f t_f d_eps, which the
    # core must carry back in its own plane. Its walls yield at (yield/E_foil); the core's force there is K_biax that tc.
    eps_y = foil_y_5052 / (foil_e_5056 * 1e3)
    n_cap = kb_al * eps_y * b.TC37
    eq = {}
    w250 = max(abs(T(250.0) - t_cold), abs(T(250.0) - t_hot))
    for tag, dT in (("cure_250F", w250), ("swing_037", swing)):
        n_face = b.E_BE * b.TF37 * da_al * dT
        eq[tag] = {"face_force_N_per_m": n_face, "core_force_needed_N_per_m": 2.0 * n_face,
                   "core_force_at_wall_yield_N_per_m": n_cap, "ratio": 2.0 * n_face / n_cap,
                   "ratio_doubled_cell": 2.0 * n_face / (kb_al * k_dw * (foil_y_5052 / (wall_dw * foil_e_5056 * 1e3)) * b.TC37)}
    out["screen_equilibrium"] = eq
    out["doubled_wall_cell"] = {"k_biax_ratio": k_dw, "single_wall_stress_ratio": wall_dw}
    one_k = da_al * 1.0
    out["sft_window"] = {
        "037_screen": {"allowed_dT_K": s_typ / b.tau_037(one_k), "lo_K": t_hot - s_typ / b.tau_037(one_k),
                       "hi_K": t_cold + s_typ / b.tau_037(one_k)},
        "free_edge_typ": {"allowed_dT_K": s_typ / b.tau_edge(one_k, kb_al)[0],
                          "lo_K": t_hot - s_typ / b.tau_edge(one_k, kb_al)[0], "hi_K": t_cold + s_typ / b.tau_edge(one_k, kb_al)[0]},
        "free_edge_min": {"allowed_dT_K": s_min / b.tau_edge(one_k, kb_al)[0],
                          "hi_K": t_cold + s_min / b.tau_edge(one_k, kb_al)[0]},
        "service_K": [t_cold, t_hot], "swing_K": swing}
    out["k_biax_al_MPa"] = kb_al / 1e6
    out["service"] = {"t_cold_K": t_cold, "t_hot_K": t_hot, "t_air_K": b.T_AIR, "swing_K": swing}

    # ---------------------------------------------------------------- fixes
    fixes = []
    base_u = u_lead

    def price(label, q, residual_037=None, residual_edge=None, mass=0.0, note="", res=None):
        """028b's least set for this fix; with res = (K_biax, d_eps) it is re-found with the cure's face compression
        on the face-local modes, and the verdict is read from that."""
        u0 = b.usage_028b(q)
        u = b.usage_028b(dict(q, res=res)) if res else u0
        if u["feasible"] and u["max_usage"] <= 1.0:
            verdict = "floats inside the named stretch (usage <= 1)"
        elif u["feasible"] and u["gamma_need"] <= 1.0 and u["Q_need"] <= 0.82:
            verdict = "floats only beyond the named stretch (usage > 1, gamma and Q still below their classical limits)"
        else:
            verdict = "cannot float: the gamma or wrinkle coefficient needed exceeds its classical limit (1, 0.82)"
        fixes.append({"fix": label, "float": verdict, "mass_change_kg": mass, "SF_037": residual_037, "SF_free_edge": residual_edge,
                      "residual_included": bool(res), "max_usage": u["max_usage"], "feasible": u["feasible"],
                      "gamma_need": u["gamma_need"], "gamma_full": u["gamma_full"], "Q_need": u["Q_need"],
                      "tf_mm": u["tf"] * 1e3, "tc_mm": u["tc"] * 1e3, "sigma_res_MPa": u["sigma_res_MPa"],
                      "binding_other": min(u["others"], key=u["others"].get), "others": u["others"],
                      "without_residual": {"max_usage": u0["max_usage"], "feasible": u0["feasible"],
                                           "gamma_need": u0["gamma_need"], "Q_need": u0["Q_need"],
                                           "tf_mm": u0["tf"] * 1e3, "tc_mm": u0["tc"] * 1e3},
                      "note": note})
        return u
    sft_af = T(250.0)
    w_af = max(abs(sft_af - t_cold), abs(sft_af - t_hot))
    price("As designed: AF 163-2U at its 250 F cure on CR-III 5056 3/8-1.0", b.base_q(),
          s_typ / b.tau_037(da_al * w_af), s_typ / b.tau_edge(da_al * w_af, kb_al)[0], 0.0, "028b's nominal point",
          res=(kb_al, da_al * w_af))
    for label, sft, aw in (("AF 163-2U at its 200 F datasheet cure", T(af_cure_F), 0.07323641454574575),
                           ("HexBond 679 at 80 C (250 g/m2 resin per line)", hb679_C + 273.15, hb679_aw / 1e3),
                           ("Room-temperature cure at 25 C (EA 9394 class), at AF's areal weight (PROJECTION)", 298.15,
                            0.07323641454574575),
                           ("Cure at mid-swing, at AF's areal weight (PROJECTION)", 0.5 * (t_hot + t_cold), 0.07323641454574575)):
        w = max(abs(sft - t_cold), abs(sft - t_hot))
        q = b.base_q()
        q["film"] = aw
        price(label, q, s_typ / b.tau_037(da_al * w), s_typ / b.tau_edge(da_al * w, kb_al)[0],
              2.0 * A * (aw - 0.07323641454574575), res=(kb_al, da_al * w))
    # a longer face scarf: 028b fixes 30:1, so its 10 MPa screen caps the face at 300.33 MPa; the cure's face compression
    # then thickens the faces at the core's expense. 028's own rule sizes r to the screen: r (1 + 1/r^2) = sigma / tau.
    def scarf_r(sigma):
        x = sigma / 10e6
        return 0.5 * (x + math.sqrt(x * x - 4.0))
    scarf_rows = []
    for label, sft in (("AF 163-2U at its 250 F cure", T(250.0)), ("AF 163-2U at its 200 F datasheet cure", T(af_cure_F))):
        w = max(abs(sft - t_cold), abs(sft - t_hot))
        sr_lead = kb_al * da_al * w * u_lead["tc"] / (2.0 * u_lead["tf"])
        r_need = scarf_r(b.m.P0 * 10.0 / (4.0 * u_lead["tf"]) + sr_lead)
        q = b.base_q()
        q["scarf_min"] = r_need
        dj = (b.m.p2_joining(10.0, b.np.array([u_lead["tf"]]), b.np.array([u_lead["tc"]]), q, fixed30=True)[0][0]
              - u_lead["J"])
        price(f"{label} with a {r_need:.2f}:1 face scarf (028's own sizing rule)", q,
              s_typ / b.tau_037(da_al * w), s_typ / b.tau_edge(da_al * w, kb_al)[0], float(dj),
              f"scarf ratio set so the 10 MPa screen holds at 028b's lead with {sr_lead / 1e6:.3f} MPa of cure "
              f"compression; joint mass change at the lead geometry", res=(kb_al, da_al * w))
        scarf_rows.append({"cure": label, "r_need": r_need, "sigma_res_lead_MPa": sr_lead / 1e6, "dJ_kg": float(dj)})
    out["scarf_fix"] = scarf_rows
    # compliant interlayer, RTV 566, at the AF cure; thickness each reading needs for SF 1
    g_i, rho_i = rtv_g * 1e6, rtv_sg * 1000.0
    d_af = da_al * w_af

    def need_thickness(fn):
        lo, hi = 0.0, 0.05
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if fn(mid) >= 1.0:
                hi = mid
            else:
                lo = mid
        return hi
    t37_need = need_thickness(lambda ti: s_typ / b.tau_037(d_af, ti=ti, gi=g_i))
    tedge_need = need_thickness(lambda ti: s_typ / b.tau_edge(d_af, kb_al, ti=ti, gi=g_i)[0])
    for ti in sorted({25e-6, 100e-6, t37_need} | ({tedge_need} if tedge_need > 1e-9 else set())):
        q = b.base_q()
        q["interlayer"] = (ti, g_i)
        q["extra_mass"] = 2.0 * A * rho_i * ti
        price(f"RTV 566 interlayer {ti * 1e6:.0f} um each face, AF cure", q,
              s_typ / b.tau_037(d_af, ti=ti, gi=g_i), s_typ / b.tau_edge(d_af, kb_al, ti=ti, gi=g_i)[0],
              2.0 * A * rho_i * ti, f"interlayer shear stress {b.tau_037(d_af, ti=ti, gi=g_i) / 1e6:.3f} MPa (037 screen) "
              f"against {rtv_lap:.1f} MPa primed lap shear", res=(kb_al, d_af))
    out["interlayer_needed_um"] = {"037_screen": t37_need * 1e6, "free_edge": tedge_need * 1e6}

    # cores: sourced sets; non-metallic in-plane CTE is unsourced, so the thickness-direction value is a stated proxy
    cores = {
        "Hexcel HFT-3/16-2.0 (glass, +/-45)": dict(
            rho_c=cdens("hft_rho", "core_glass", "W shear modulus", "HFT-3/16-2.0"),
            Gc=use("hft_gw", "core", "core_glass", "W shear modulus", "HFT-3/16-2.0", 34.474) * 1e6,
            Ec=use("hft_ec", "core", "core_glass", "stabilised compressive modulus", "HFT-3/16-2.0", 117.21) * 1e6,
            crush=use("hft_stab", "core", "core_glass", "stabilised compressive strength", "HFT-3/16-2.0", 1172.1) * 1e3,
            cell=0.0047625, shear_w=use("hft_sw", "core", "core_glass", "W shear strength", "HFT-3/16-2.0", 413.69) * 1e3,
            cte=use("glass_cte", "core", "core_glass", "coefficient of thermal expansion, THICKNESS", "HRP, HFT", 1.476e-5, tol=1e-3),
            cte_basis="thickness-direction CTE used as an in-plane proxy (PROJECTION)"),
        "Hexcel HRP-3/8-3.2 (glass/phenolic)": dict(
            rho_c=cdens("hrp_rho", "core_glass", "W shear modulus", "HRP-3/8-3.2"), Gc=use("hrp_gw", "core", "core_glass", "W shear modulus", "HRP-3/8-3.2", 34.474) * 1e6,
            Ec=use("hrp_ec", "core", "core_glass", "stabilised compressive modulus", "HRP-3/8-3.2", 262.0) * 1e6,
            crush=use("hrp_stab", "core", "core_glass", "stabilised compressive strength", "HRP-3/8-3.2", 2689.0) * 1e3,
            cell=0.009525, shear_w=use("hrp_sw", "core", "core_glass", "W shear strength", "HRP-3/8-3.2", 758.42) * 1e3,
            cte=1.476e-5, cte_basis="thickness-direction CTE used as an in-plane proxy (PROJECTION)"),
        "Hexcel HRH-49-1/4-2.1 (Kevlar)": dict(
            rho_c=cdens("hrh49_rho", "core_aramid", "W shear modulus", "HRH-49-1/4-2.1"), Gc=use("hrh49_gw", "core", "core_aramid", "W shear modulus", "HRH-49-1/4-2.1", 8.9632) * 1e6,
            Ec=use("hrh49_ec", "core", "core_aramid", "stabilised compressive modulus", "HRH-49-1/4-2.1", 172.37) * 1e6,
            crush=use("hrh49_stab", "core", "core_aramid", "stabilised compressive strength", "HRH-49-1/4-2.1", 896.32) * 1e3,
            cell=0.00635, shear_w=use("hrh49_sw", "core", "core_aramid", "W shear strength", "HRH-49-1/4-2.1", 275.79) * 1e3,
            cte=use("hrh49_cte", "core", "core_aramid", "coefficient of thermal expansion, THICKNESS", "HRH-49", 4.86e-6, tol=1e-3),
            cte_basis="thickness-direction CTE used as an in-plane proxy (PROJECTION)"),
        "Hexcel HRH-10-3/8-1.5 (Nomex)": dict(
            rho_c=cdens("hrh10_rho", "core_aramid", "W shear modulus", "HRH-10-3/8-1.5"), Gc=use("hrh10_gw", "core", "core_aramid", "W shear modulus", "HRH-10-3/8-1.5", 10.342) * 1e6,
            Ec=use("hrh10_ec", "core", "core_aramid", "stabilised compressive modulus", "HRH-10-3/8-1.5", 41.369) * 1e6,
            crush=use("hrh10_stab", "core", "core_aramid", "stabilised compressive strength", "HRH-10-3/8-1.5", 723.95) * 1e3,
            cell=0.009525, shear_w=use("hrh10_sw", "core", "core_aramid", "W shear strength", "HRH-10-3/8-1.5", 241.32) * 1e3,
            cte=use("hrh10_cte", "core", "core_aramid", "coefficient of thermal expansion, THICKNESS", "HRH-10, HRH-310", 3.492e-5, tol=1e-3),
            cte_basis="thickness-direction CTE used as an in-plane proxy (PROJECTION)"),
    }
    for name, c in cores.items():
        q = b.base_q({k: c[k] for k in ("rho_c", "Gc", "Ec", "crush", "cell")})
        d = (c["cte"] - b.ALPHA_BE) * w_af
        t37 = b.tau_037(d, gc=c["Gc"]) if abs(d) > 0 else 0.0
        price(f"Core {name}, AF cure", q, (c["shear_w"] / t37) if t37 else None, None,
              (c["rho_c"] - 16.018463373960138) * A * u_lead["tc"],
              c["cte_basis"] + f"; core CTE {c['cte']:.3g}/K; W strength {c['shear_w'] / 1e3:.0f} kPa; mass change at the "
              "lead's core depth")
    # metal cores matched to beryllium: mass bound (other properties taken as perfect)
    metal = {"Ti-3Al-2.5V honeycomb (72 kg/m3)": (use("ti_rho", "core", "core_titanium", "core density, Ti-3Al-2.5V corrugated", "Ti-3Al-2.5V", 72.0), ti_cte),
             "17-7 PH hexagonal honeycomb (81.7 kg/m3)": (use("ph_rho", "core", "core_stainless", "core density, brazed 17-7 PH", "17-7 PH", 81.694), ph177_cte),
             "Beryllium honeycomb (84.9 kg/m3)": (use("be_rho", "core", "core_beryllium", "core density, Be ingot-foil", "Beryllium", 84.898), b.ALPHA_BE)}
    for name, (rho, cte) in metal.items():
        q = b.base_q({"rho_c": rho, "Gc": 1e12, "Ec": 1e12, "crush": 1e9, "cell": 0.001})
        u = price(f"Core {name}, every other core property perfect (a mass bound)", q, None, None,
                  (rho - 16.018463373960138) * A * u_lead["tc"],
                  f"foil CTE {cte:.3g}/K against beryllium {b.ALPHA_BE:.3g}/K; mass change at the lead's core depth")
    out["fixes"] = fixes
    out["baseline_usage"] = base_u
    out["ended"] = datetime.datetime.now().astimezone().isoformat()
    out["elapsed_s"] = time.monotonic() - t0
    tmp = os.path.join(HERE, "COMPUTE.json.tmp")
    with open(tmp, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(tmp, os.path.join(HERE, "COMPUTE.json"))
    print("elapsed", round(out["elapsed_s"], 1))


if __name__ == "__main__":
    main()
