#!/usr/bin/env python3
"""MAINLINE-049 fold: orders ord-admiral-rr2-mainline049-fold-048-1020 and ord-admiral-rr2-mainline049-fold-chk040-1020.

048's finish and water account replaces 040's coating and water. The finish is multilayer CCAg/ITO at 7.5752 g/m2 plus
10% (classical CCAg is the alternative), with its optics in the thermal table and 048's larger-of-day-and-night gradient
and curvature. It adds 10 g/m2 structural primer and keeps the 0.1 kg/m2 exterior film aboard. Each construction's own
material water is charged: 048's bake route is primary (90% removed); the dry-gas route keeps all of it.

CHECK-040's rows are also run: 1 mm exterior water, cure compression in the global and crimp demand, and edge/scarf
coincidence. The script also rescores the finish's thermal factors on each beryllium-free face, finds the face-modulus
multiplier to float and the CFRP edge factor against cure, and checks itself against 048's and CHECK-040's own rows.
Writes FOLD.json."""
import csv
import datetime
import json
import math
import os
import sys
import time
import multiprocessing

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import acct49 as A  # noqa: E402
import extra49 as X  # noqa: E402
import model49 as M  # noqa: E402
import run49 as RUN  # noqa: E402
import src49 as S  # noqa: E402
import thermal49 as TH  # noqa: E402

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def finishes():
    prof = {x["id"]: x for x in json.load(open(f"{D048}/COATINGS.json"))}
    out = {"reference040": dict(alpha=prof["reference040"]["alpha"], epsilon=prof["reference040"]["epsilon"],
                                installed=prof["reference040"]["areal_mass_kg_m2"], finish_water=0., primer=0.,
                                name=prof["reference040"]["name"], use="040's assumed paint and primer; comparison only")}
    for fid in ("MLCCAg", "CCAg"):
        p = prof[fid]
        inst = p["areal_mass_kg_m2"] * 1.10                  # 048's 10% application allowance
        out[fid] = dict(alpha=p["alpha"], epsilon=p["epsilon"], areal=p["areal_mass_kg_m2"], installed=inst,
                        finish_water=inst * .01, primer=.01, name=p["name"], source=p["source"],
                        optical_source=p.get("optical_source"), mass_basis=p["mass_basis"],
                        mass_band_kg_m2=p.get("mass_band_kg_m2"))
    assert abs(out["MLCCAg"]["areal"] - .0075752) < 1e-12 and (out["MLCCAg"]["alpha"], out["MLCCAg"]["epsilon"]) == (.09, .8)
    return out


def constructions():
    B = RUN.build(F0, C0)
    faces, cores, seam = B["faces"], B["cores"], B["seam_cfrp"]
    K = X.k60_face(faces)
    # material water (each construction's own uptake; 048's fractions for the 5056 core, AF163-2U, primer and finish)
    w_face = S.val("w_cfrp", "water", "cfrp_moisture", "P75S/954-3 quasi-isotropic laminate at 55% RH", 0.18) / 100
    S.val("w_xn50", "water", "cfrp_moisture", "XN50/RS-3", 0.14)
    S.val("w_ex1515", "water", "cfrp_moisture", "Moisture absorption of EX-1515", 0.04)
    S.val("w_9543_hi", "water", "cfrp_moisture", "954-3 cyanate laminate (column 2)", 0.704)
    S.val("w_t300", "water", "cfrp_moisture", "T300/5208 graphite/epoxy composite at 322 K", 0.92)
    w_h10 = S.val("w_h10", "cores", "nomex_moisture", "Moisture pickup of HRH-10", 4.4) / 100
    S.val("w_nomex", "cores", "nomex_moisture", "Equilibrium moisture content of Nomex paper", 5.0)
    w_h49 = S.val("w_h36", "water", "aramid_moisture", "Moisture pickup of HexWeb HRH-36", 3.4) / 100
    S.val("w_kev49", "water", "aramid_moisture", "Equilibrium moisture of Kevlar 49 yarn from bone-dry", 3.5)
    w_fm300 = S.val("w_fm300", "water", "adhesive_moisture", "FM-300 film adhesive at 49 C, 70% RH", 1.67) / 100
    S.val("w_fm300_hot", "water", "adhesive_moisture", "FM-300 film adhesive at 49 C, 90% RH", 2.99)
    core_water = {"CR-III 5056 3/8-1.0": .001, "HRH-10-3/8-1.5": w_h10, "HRH-49-1/4-2.1": w_h49}
    cons = [dict(key="Be | CR-III 5056 3/8-1.0 | AF163-2U 200 F", label="Be SR-200 on CR-III 5056, AF163-2U 200 F (040)",
                 fface="Be SR-200", face=F0, nu=.0768, core_key="CR-III 5056 3/8-1.0", cure=CURE200, mat=dict(MAT0))]

    def add(fk, ck, cure, tag, face=None, nu=None, fface=None):
        f = faces[fk]
        face = face or f["face"]
        mat = dict(MAT0)
        mat.update(cores[ck]["mat"])
        mat.update(dict(rho_f=face["rho"], alpha_f=f["alpha"], tf_min=f["tf_min"]))
        if fk != "AlBeMet AM162":
            mat.update(seam)
            mat["seam_water_fraction"] = w_fm300
            mat["face_water_fraction"] = w_face
        mat["core_outgas_fraction"] = .001                   # 040's nominal volatile allowance; water is charged below
        mat["core_water_fraction"] = core_water[ck]
        fface = fface or fk
        cons.append(dict(key=f"{fface} | {ck} | {tag}", label=f"{fface} on {ck}, {tag}", fface=fface, face=face,
                         nu=nu or f["nu"], core_key=ck, cure=cure, mat=mat))
    add("AlBeMet AM162", "CR-III 5056 3/8-1.0", CURE200, "040's Be scarf and stock")
    for fk in ("M55J QI", "K13D2U QI"):
        add(fk, "CR-III 5056 3/8-1.0", CURE200, "AF163-2U 200 F")
        add(fk, "CR-III 5056 3/8-1.0", ROOM, "room-temperature cure (PROJECTION)")
        add(fk, "HRH-10-3/8-1.5", CURE200, "AF163-2U 200 F")
        add(fk, "HRH-49-1/4-2.1", CURE200, "AF163-2U 200 F")
    for cure, tag in ((ROOM, "room-temperature cure (PROJECTION)"), (C50, "50 C cure (PROJECTION)")):
        add("K13D2U QI", "CR-III 5056 3/8-1.0", cure, tag, face=K["face"], nu=K["qi"]["nu"],
            fface="K13D2U QI at 60% Vf (PROJECTION)")
    water = dict(face_cfrp=w_face, core=core_water, seam_cfrp=w_fm300, seam_metal=.01, face_core_film=.002,
                 primer=.01, finish=.01, basis={
                     "face_cfrp": "P75S/954-3 quasi-isotropic pitch/cyanate laminate, 55% RH saturation (Brand and Derby); "
                                  "the highest of three pitch/cyanate laminates; transferred to K13D2U and M55J (PROJECTION)",
                     "HRH-10": "Hexcel HRH-10 3/16-4.0 pickup after 95% RH, 120 F, 120 h",
                     "HRH-49": "Hexcel HRH-36 (para-aramid paper) pickup after the same exposure; Kevlar 49 yarn 3.5% at 55% "
                               "RH (PROJECTION for HRH-49)",
                     "5056": "048's assumed .001",
                     "seam_cfrp": "FM-300 film adhesive at 49 C, 70% RH (NASA CR-3387 estimate; FM 300-2M at ambient PROJECTION)",
                     "seam_metal": "048's assumed .01", "face_core_film": "048's AF163-2U WVR .002",
                     "primer": "048's assumed .01", "finish": "048's assumed .01 of the applied finish"})
    return B, K, cons, water


def configure(con, fid, face=None):
    M.set_material(face=face or con["face"], core=G["cores"][con["core_key"]]["core"],
                   thermal=G["tables"][(fid, con["core_key"])], **con["mat"])


def settings(con, fid, variant, weather, floor, cure=None):
    fin = G["fins"][fid]
    kw = dict(weather=weather, floor=floor, pad="heavy70", vented=True, nu=con["nu"],
              cure_temperature_K=con["cure"] if cure is None else cure,
              coating=fin["installed"], finish_id=fid, external_water_kg_m2=.1, structural_primer_kg_m2=fin["primer"],
              moisture_scale=.1, finish_water_kg_m2=fin["finish_water"])
    if variant == "water_1mm":
        kw["external_water_kg_m2"] = 1.0
    elif variant == "cure_in_global":
        kw["cure_in_global"] = True
    elif variant == "edge_scarf":
        kw["edge_scarf_interaction"] = True
    elif variant == "dry_gas":
        kw["moisture_scale"] = 1.0
    else:
        assert variant == "primary", variant
    return M.Settings(**kw)


def job(args):
    kind = args[0]
    if kind == "row":
        _, i, fid, variant, r, w, fl = args
        con = G["cons"][i]
        configure(con, fid)
        row = A.row(con["label"], r, w, fl, settings(con, fid, variant, w, fl), A.today_values(con["face"]))
        row.update(construction=con["key"], finish=fid, variant=variant)
        return kind, row
    if kind == "emult":
        _, i, r = args
        con = G["cons"][i]

        def f(k):
            face = dict(con["face"])
            face["E_today_Pa"] *= k
            face["E_full_Pa"] *= k
            configure(con, "MLCCAg", face=face)
            p = M.optimize(r, 15, 1.0, settings(con, "MLCCAg", "primary", "ISA", False))
            return -1e9 if p is None else p["signed_payload_kg"]
        lo, hi = 1.0, 1.0
        while f(hi) < 0 and hi < 8:
            hi *= 1.25
        if f(hi) < 0:
            return kind, {"construction": con["key"], "R_m": r, "k_E": None}
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if f(mid) >= 0:
                hi = mid
            else:
                lo = mid
        return kind, {"construction": con["key"], "R_m": r, "k_E": hi, "E_need_Pa": con["face"]["E_today_Pa"] * hi}
    if kind == "chk048":
        _, rid = args
        name, rest = rid.split("-R", 1)
        r, weather, fl, route, water = rest.split("-")
        M.set_material(face=F0, core=C0, thermal=G["t048"][name], **MAT0)
        inst = G["prof048"][name]["areal_mass_kg_m2"] * 1.10
        s = M.Settings(weather=weather, floor=(fl == "floor"), coating=inst, finish_id=name,
                       external_water_kg_m2=.1 if water == "retained_water" else 0., structural_primer_kg_m2=.01,
                       moisture_scale=.1 if route == "bake70" else 1., finish_water_kg_m2=inst * .01,
                       desiccant=(route == "desiccant"))
        res = M.least(int(r), s)
        ep = next(t["solution"] for t in res["endpoint_trials"] if t["mask"] == 11)
        ref = G["rows048"][rid]
        mine_u = None if res["least"] is None else res["least"]["usage"]
        theirs_u = None if ref["least_usage"] == "" else float(ref["least_usage"])
        mine_e, theirs_e = ep["signed_payload_kg"], float(ref["endpoint_payload_kg"])
        ok = abs(mine_e - theirs_e) < 1e-6 and ((mine_u is None and theirs_u is None) or abs(mine_u - theirs_u) < 1e-9)
        return kind, {"check": f"048 {rid}", "mine_endpoint": mine_e, "theirs_endpoint": theirs_e,
                      "mine_usage": mine_u, "theirs_usage": theirs_u, "ok": bool(ok)}
    if kind == "chk040":
        _, rid, case, theirs = args
        r, weather, fl = rid.split("-")[:3]
        M.set_material(face=F0, core=C0, thermal=BASE_T, **MAT0)
        kw = dict(weather=weather, floor=(fl == "floor"))
        mask = 15
        if case == "cure_in_global":
            kw["cure_in_global"] = True
        elif case == "edge_scarf_coincidence":
            kw["edge_scarf_interaction"] = True
        elif case == "water_1mm_all":
            kw["external_water_kg_m2"] = 1.0
        elif case == "water_1mm_028b":
            kw["external_water_kg_m2"] = 1.0
            mask = 11
        p = M.optimize(int(r[1:]), mask, 1., M.Settings(**kw))
        mine = None if p is None else p["signed_payload_kg"]
        ok = mine is not None and abs(mine - theirs) < 1e-3
        return kind, {"check": f"CHECK-040 {rid} {case}", "mine_kg": mine, "theirs_kg": theirs, "ok": bool(ok)}
    raise ValueError(kind)


def thermal_factors():
    """048's finish screen (037 day and full-cycle factors at 037's source geometry; the current edge factor) rescored
    with each construction's own face modulus, expansion mismatch, core and cure temperature."""
    out, cache = [], {}
    for fid in ("reference040", "CCAg", "MLCCAg"):
        fin = G["fins"][fid]
        kw = dict(alpha_out=fin["alpha"], epsilon_out=fin["epsilon"])
        for con in G["cons"]:
            ck = con["core_key"]
            c = G["cores"][ck]
            core = c["core"]
            if (fid, ck) not in cache:
                if c["k"] is None:
                    legacy = TH.evaluate(10, [TC0], n=37, midpoint=True, fixed_iterations=25, legacy_project=True,
                                         solid_density=2640, **kw)
                else:
                    legacy = TH.evaluate(10, [TC0], n=37, midpoint=True, fixed_iterations=25, legacy_project=True,
                                         k_core=c["k"], **kw)
                common = TH.evaluate(10, [TC0], n=128, k_core=c["k"], night=True, **kw)
                cache[(fid, ck)] = (legacy, common)
            legacy, common = cache[(fid, ck)]
            mat = con["mat"]
            dalpha = mat["alpha_c"] - mat["alpha_f"]
            E = con["face"]["E_today_Pa"]
            fpk = abs(dalpha) * math.sqrt(E * TF0 * core["Gc_Pa"] / TC0)
            wtyp = core["shear_strength_W_Pa"]
            day = wtyp / (fpk * abs(legacy["rise_K"][0]))
            cycle = wtyp / (fpk * abs(legacy["swing_K"][0]))
            kb = .5 * mat["wall_E"] * core["rho"] / mat["wall_rho"]
            dT = 1.002 * max(abs(con["cure"] - common["min_outer_K"][0]), abs(con["cure"] - common["max_outer_K"][0]))
            edge = mat["edge_allow"] / (abs(dalpha) * dT * math.sqrt(2 * kb * core["Gc_Pa"]))
            out.append(dict(finish=fid, construction=con["key"], face=con["fface"], core=ck, cure_K=con["cure"],
                            dalpha=dalpha, E_Pa=E, legacy_037_day_SF=day, legacy_037_full_cycle_SF=cycle,
                            day_at_least_1_6775=bool(day >= 1.6775), cycle_at_least_1=bool(cycle >= 1),
                            current_edge_SF=edge, rise_K=legacy["rise_K"][0], swing_K=legacy["swing_K"][0],
                            min_outer_K=common["min_outer_K"][0], max_outer_K=common["max_outer_K"][0]))
    return out


def own_geometry_and_pressure(cons, cores, tables, rows):
    # 037's rigid-face day and full-cycle factors at each construction's own all-four endpoint geometry (the
    # converged MLCCAg table at that core), beside 048's source-geometry values; and the dry-gas service pressure
    own_tf, dry_p = [], []
    for con in cons:
        mat, core = con["mat"], cores[con["core_key"]]["core"]
        dalpha = mat["alpha_c"] - mat["alpha_f"]
        for r in R3:
            row = next(x for x in rows if x["construction"] == con["key"] and x["variant"] == "primary"
                       and x["finish"] == "MLCCAg" and x["R_m"] == r and x["weather"] == "ISA" and not x["floor"])
            g = row["endpoint_all_geometry"]
            if g is None:
                continue
            tab = tables[("MLCCAg", con["core_key"])][str(r)]
            lt = [math.log(x) for x in tab["tc_m"]]
            rise = M.np.interp(math.log(g["tc_m"]), lt, tab["rise_K"])
            swing = M.np.interp(math.log(g["tc_m"]), lt, tab["swing_K"])
            fpk = abs(dalpha) * math.sqrt(con["face"]["E_today_Pa"] * g["tf_m"] * core["Gc_Pa"] / g["tc_m"])
            own_tf.append({"construction": con["key"], "R_m": r, "tf_m": g["tf_m"], "tc_m": g["tc_m"], "rise_K": float(rise),
                           "swing_K": float(swing), "day_SF": float(core["shear_strength_W_Pa"] / (fpk * rise)),
                           "full_cycle_SF": float(core["shear_strength_W_Pa"] / (fpk * swing)),
                           "account_edge_SF": row["endpoint_all_modes"]["thermal_core_interface_screen"]})
            configure(con, "MLCCAg")
            s = settings(con, "MLCCAg", "dry_gas", "ISA", False)
            joint = M.joining(r, g["tf_m"], g["tc_m"], M.coefficients(15, 1.0)[3], s)
            vac = M.vacuum(r, g["tf_m"], g["tc_m"], joint, s)
            dry_p.append({"construction": con["key"], "R_m": r, "bake_pressure_SF": row["endpoint_all_vacuum"]["pressure_SF"],
                          "dry_gas_pressure_SF_same_geometry": float(vac["pressure_SF"]),
                          "dry_gas_material_water_kg": float(vac["added_material_water_kg"])})
    return own_tf, dry_p


def main():
    t0 = time.monotonic()
    out = {"started": datetime.datetime.now().astimezone().isoformat(), "pins": {}}
    for k, (p, want) in PIN_FILES.items():
        out["pins"][k] = RUN.pin(p, want)
    for name in ("cfrp", "albemet", "cores", "water"):
        for ext in ("json", "md"):
            out["pins"][f"src_{name}_{ext}"] = RUN.pin(f"{S.SRC}/{name}.{ext}", None)
    for name in ("model49.py", "thermal49.py", "acct49.py", "laminate.py", "src49.py", "run49.py", "extra49.py", "fold49.py"):
        out["pins"][f"own_{name}"] = RUN.pin(os.path.join(HERE, name), None)
    assert all(v["ok"] for v in out["pins"].values()), [k for k, v in out["pins"].items() if not v["ok"]]
    out["common_amendment"] = RUN.common_amendment()
    assert out["common_amendment"]["current_minus_added_is_dispatched"], out["common_amendment"]

    fins = finishes()
    B, K, cons, water = constructions()
    cores = B["cores"]
    # thermal tables: each finish's optics on each core, 048's day-or-night convention
    tables = {}
    for fid in ("MLCCAg", "CCAg"):
        for ck, c in cores.items():
            tables[(fid, ck)] = TH.table(list(R3), k_core=c["k"], alpha_out=fins[fid]["alpha"],
                                         epsilon_out=fins[fid]["epsilon"], night=True)
    t048 = json.load(open(f"{D048}/THERMAL-TABLES.json"))
    # check: this code's MLCCAg and CCAg tables on 5056 at R15 equal 048's, and the 040 default equals 040's
    tcheck = {}
    for fid in ("MLCCAg", "CCAg"):
        mine, theirs = tables[(fid, "CR-III 5056 3/8-1.0")]["15"], t048[fid]["15"]
        tcheck[f"048 {fid} R15"] = max(max(abs(a - b) for a, b in zip(mine[k], theirs[k])) for k in (
            "tc_m", "gradient_K", "swing_K", "rise_K", "curvature_temperature_K", "max_outer_K", "min_outer_K"))
    d040 = TH.table([30])["30"]
    tcheck["040 R30"] = max(max(abs(a - b) for a, b in zip(d040[k], BASE_T["30"][k])) for k in (
        "gradient_K", "swing_K", "curvature_temperature_K", "max_outer_K", "min_outer_K"))
    assert all(v == 0.0 for v in tcheck.values()), tcheck
    out["thermal_table_checks_max_abs_K"] = tcheck

    G.update(fins=fins, cons=cons, cores=cores, tables=tables, t048=t048,
             prof048={x["id"]: x for x in json.load(open(f"{D048}/COATINGS.json"))},
             rows048={r["id"]: r for r in csv.DictReader(open(f"{D048}/ROWS.csv"))})
    mm = json.load(open(f"{DCHK}/MARGINAL-MODELS.json"))

    jobs = []
    floating_first = sorted(range(len(cons)), key=lambda i: 0 if ("Be SR-200" in cons[i]["key"] or "60% Vf" in cons[i]["key"]) else 1)
    for i in floating_first:
        for fid, variant in VARIANTS:
            for r in R3:
                for w in ("ISA", "optimistic"):
                    for fl in ((False, True) if variant == "primary" and fid == "MLCCAg" else (False,)):
                        jobs.append(("row", i, fid, variant, r, w, fl))
    emult = [i for i, c in enumerate(cons) if c["key"] in (
        "M55J QI | CR-III 5056 3/8-1.0 | room-temperature cure (PROJECTION)",
        "K13D2U QI | CR-III 5056 3/8-1.0 | room-temperature cure (PROJECTION)",
        "AlBeMet AM162 | CR-III 5056 3/8-1.0 | 040's Be scarf and stock",
        "M55J QI | HRH-49-1/4-2.1 | AF163-2U 200 F", "K13D2U QI | HRH-49-1/4-2.1 | AF163-2U 200 F")]
    assert len(emult) == 5
    jobs += [("emult", i, r) for i in emult for r in R3]
    jobs += [("chk048", rid) for rid in (
        "MLCCAg-R15-ISA-actual-dry_gas-retained_water", "MLCCAg-R15-ISA-actual-bake70-retained_water",
        "MLCCAg-R15-ISA-floor-bake70-retained_water", "MLCCAg-R15-optimistic-actual-bake70-retained_water",
        "MLCCAg-R12-ISA-floor-desiccant-retained_water", "MLCCAg-R10-ISA-floor-bake70-retained_water",
        "CCAg-R15-ISA-actual-bake70-retained_water", "MLCCAg-R15-optimistic-floor-dry_gas-dry_exterior")]
    jobs += [("chk040", x["id"], c, x["cases"][c]["signed_payload_kg"]) for x in mm
             for c in ("cure_in_global", "edge_scarf_coincidence")]
    jobs += [("chk040", "R30-ISA-actual", "water_1mm_all", -594.989), ("chk040", "R30-ISA-actual", "water_1mm_028b", -820.787)]
    print(len(jobs), "jobs", flush=True)
    results = {"row": [], "emult": [], "chk048": [], "chk040": []}
    with multiprocessing.get_context("fork").Pool(8) as pool:      # workers inherit G; simjob --cores 8
        for n, (kind, res) in enumerate(pool.imap_unordered(job, jobs, chunksize=1), 1):
            results[kind].append(res)
            if n % 50 == 0:
                print(n, "done", round(time.monotonic() - t0), "s", flush=True)
    assert all(c["ok"] for c in results["chk048"]), [c for c in results["chk048"] if not c["ok"]]
    assert all(c["ok"] for c in results["chk040"]), [c for c in results["chk040"] if not c["ok"]]
    order = {c["key"]: i for i, c in enumerate(cons)}
    vorder = {v: i for i, v in enumerate(VARIANTS)}
    rows = sorted(results["row"], key=lambda x: (order[x["construction"]], vorder[(x["finish"], x["variant"])], x["R_m"],
                                                 x["weather"], x["floor"]))

    # the CFRP edge factor against cure, under the new optics, at each construction's R20 all-endpoint geometry
    G_local = []
    for key in ("M55J QI | CR-III 5056 3/8-1.0 | room-temperature cure (PROJECTION)",
                "K13D2U QI at 60% Vf (PROJECTION) | CR-III 5056 3/8-1.0 | room-temperature cure (PROJECTION)"):
        con = cons[order[key]]
        row = next(x for x in rows if x["construction"] == key and x["variant"] == "primary" and x["finish"] == "MLCCAg"
                   and x["R_m"] == 20 and x["weather"] == "ISA" and not x["floor"])
        g = row["endpoint_all_geometry"]
        if g is None:
            continue
        for cure in (298.15, 310.0, 323.15, 338.15, CURE200, 394.26):
            configure(con, "MLCCAg")
            s = settings(con, "MLCCAg", "primary", "ISA", False, cure=cure)
            modes, th, props = M.mechanical(20, g["tf_m"], g["tc_m"], 15, 1.0, s)
            G_local.append({"construction": key, "cure_K": cure, "tf_m": g["tf_m"], "tc_m": g["tc_m"], "edge_SF": float(th),
                            "tau_Pa": float(props["thermal_interface_shear_Pa"]),
                            "cure_compression_Pa": float(props["added_cure_compression_Pa"]),
                            "wall_SF": float(modes["core_cell_wall_yield_screen"])})
    tf = thermal_factors()
    be = next(x for x in tf if x["finish"] == "MLCCAg" and x["face"] == "Be SR-200")
    ref = {x["id"]: x for x in json.load(open(f"{D048}/THERMAL-SCREEN.json"))}["MLCCAg"]
    tf_check = {"day": (be["legacy_037_day_SF"], ref["legacy_037_day_SF"]),
                "cycle": (be["legacy_037_full_cycle_SF"], ref["legacy_037_full_swing_SF"]),
                "edge": (be["current_edge_SF"], ref["current_200F_minimum_edge_SF"])}
    assert all(abs(a - b) < 1e-9 * max(1, abs(b)) for a, b in tf_check.values()), tf_check
    own_tf, dry_p = own_geometry_and_pressure(cons, cores, tables, rows)
    M.set_material(face=F0, core=C0, thermal=BASE_T, **MAT0)

    out.update({
        "finishes": fins, "water_fractions": water, "variants": [list(v) for v in VARIANTS],
        "constructions": [{"key": c["key"], "label": c["label"], "face": c["fface"], "core": c["core_key"], "cure_K": c["cure"],
                           "nu": c["nu"], "E_today_Pa": c["face"]["E_today_Pa"], "rho_f": c["mat"]["rho_f"],
                           "alpha_f": c["mat"]["alpha_f"], "alpha_c": c["mat"]["alpha_c"], "tf_min": c["mat"]["tf_min"],
                           "core_water_fraction": c["mat"]["core_water_fraction"],
                           "face_water_fraction": c["mat"]["face_water_fraction"],
                           "seam_water_fraction": c["mat"]["seam_water_fraction"],
                           "seam_film": c["mat"]["seam_film"], "seam_screen": c["mat"]["seam_screen"]} for c in cons],
        "k60": {"E1_Pa": K["E1_Pa"], "translation": K["eff"], "E_QI_Pa": K["qi"]["E_Pa"], "nu_QI": K["qi"]["nu"]},
        "checks_048": sorted(results["chk048"], key=lambda x: x["check"]),
        "checks_040": sorted(results["chk040"], key=lambda x: x["check"]),
        "thermal_screen_check_Be_MLCCAg": tf_check,
        "rows": rows,
        "E_multiplier_to_float": sorted(results["emult"], key=lambda x: (order[x["construction"]], x["R_m"])),
        "edge_vs_cure": G_local, "thermal_factors": tf, "thermal_factors_own_geometry": own_tf,
        "dry_gas_pressure_at_primary_geometry": dry_p,
        "supply_inputs": {"face_fibre_fraction": {k: v.get("fibre_mass_fraction") for k, v in B["faces"].items()},
                          "albemet_be_fraction": B["faces"]["AlBeMet AM162"]["be_mass_fraction"]},
        "ended": datetime.datetime.now().astimezone().isoformat(), "elapsed_s": time.monotonic() - t0,
        "sources_used": S.USED})
    with open(os.path.join(HERE, "FOLD.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "FOLD.json.tmp"), os.path.join(HERE, "FOLD.json"))
    print("elapsed", round(out["elapsed_s"], 1), "rows", len(rows))


if __name__ == "__main__":
    main()
