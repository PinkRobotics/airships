#!/usr/bin/env python3
"""CHECK-030d: re-derive 030d's P2 numbers on 048's account with cure compression, using this seat's own code.

The model is MAINLINE-049's model49.py and thermal49.py: this seat's port of 040, which reproduces 048's beryllium rows
bit for bit and CHECK-040's sensitivity rows within 0.0006 kg. None of 030d's or 048's code is read or run here. 048's
finish conventions are restated from its METHOD: deposited finishes take +10% and 1% of their applied mass as water; FEP
tapes take +5% overlap and 0.01% water on the film plus 1% on the rest. The routes are bake (90% of the added material
water removed), dry gas (none removed) and desiccant (bed added). Writes P2CHECK.json."""
import datetime
import json
import multiprocessing
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
M49 = "unpublished-local-ref:5eec519919d3414d"
sys.path.insert(0, M49)
import model49 as M  # noqa: E402
import thermal49 as TH  # noqa: E402

D048 = "unpublished-local-ref:2c491d684a140b5c"
PROF = {x["id"]: x for x in json.load(open(f"{D048}/COATINGS.json"))}      # data: areal masses and optics
FINS = ("MLCCAg", "CCAg", "AgFEP05", "AgFEP1")
F0, C0, MAT0 = dict(M.F), dict(M.C), dict(M.MAT)
G = {}


def finish(name):
    p = PROF[name]
    fep = "FEP" in name
    inst = p["areal_mass_kg_m2"] * (1.05 if fep else 1.10)
    film = .028 if name == "AgFEP05" else .054
    water = ((film * .0001 + (p["areal_mass_kg_m2"] - film) * .01) * 1.05) if fep else inst * .01
    return inst, water


def settings(name, weather, floor, route, ext_water=.1, cure=False):
    inst, fw = finish(name)
    return M.Settings(weather=weather, floor=floor, coating=inst, finish_id=name, external_water_kg_m2=ext_water,
                      structural_primer_kg_m2=.01, moisture_scale=.1 if route == "bake70" else 1.,
                      finish_water_kg_m2=fw, desiccant=(route == "desiccant"), cure_in_global=cure)


def job(args):
    kind = args[0]
    if kind == "least":
        _, name, r, w, fl, route, ext, cure = args
        M.set_material(face=F0, core=C0, thermal=G["tables"][name], **MAT0)
        res = M.least(r, settings(name, w, fl, route, ext, cure))
        ep = {t["mask"]: t["solution"] for t in res["endpoint_trials"]}
        lp = res["least"]
        out = {"finish": name, "R_m": r, "weather": w, "floor": fl, "route": route, "external_water": ext, "cure": cure,
               "least_axes": None if lp is None else lp["selected_axes"], "least_usage": None if lp is None else lp["usage"],
               "endpoint_named_kg": None if ep[11] is None else ep[11]["signed_payload_kg"],
               "endpoint_all_kg": None if ep[15] is None else ep[15]["signed_payload_kg"],
               "floats_any": any(t["solution"] is not None and t["solution"]["signed_payload_kg"] >= 0
                                 for t in res["endpoint_trials"])}
        if name == "MLCCAg" and r == 10 and w == "ISA" and route == "bake70" and ext == .1:
            out["named_bill"] = None if ep[11] is None else ep[11]["bill_kg"]
            out["named_lift"] = None if ep[11] is None else ep[11]["lift_kg"]
            out["named_geometry"] = None if ep[11] is None else ep[11]["geometry"]
            out["least_bill"] = None if lp is None else lp["bill_kg"]
            out["least_payload"] = None if lp is None else lp["signed_payload_kg"]
            out["least_properties"] = None if lp is None else {k: lp["properties"][k] for k in (
                "gamma", "Q", "film_kg_m2_interface", "E_Pa", "Fcy_Pa")}
            out["named_material_water_before_bake"] = None
        return out
    raise ValueError(kind)


def main():
    t0 = time.monotonic()
    G["tables"] = {n: TH.table([10, 12, 15], alpha_out=PROF[n]["alpha"], epsilon_out=PROF[n]["epsilon"], night=True)
                   for n in FINS}
    jobs = []
    # (a) the cure-included R10-15 table: multilayer finish, bake, 0.1 mm, both joining conventions
    for r in (10, 12, 15):
        for w in ("ISA", "optimistic", "both"):
            for fl in (False, True):
                jobs.append(("least", "MLCCAg", r, w, fl, "bake70", .1, True))
                jobs.append(("least", "MLCCAg", r, w, fl, "bake70", .1, False))
    # (b) the two marginal floats said to be lost with cure compression
    for name, route in (("AgFEP05", "desiccant"), ("AgFEP1", "dry_gas")):
        for cure in (False, True):
            jobs.append(("least", name, 15, "optimistic", True, route, .1, cure))
    # (c) 1 mm of exterior water: the best all-four candidates (R10 ISA, every finish and route, both cure treatments)
    for name in FINS:
        for route in ("bake70", "dry_gas", "desiccant"):
            for cure in (False, True):
                jobs.append(("least", name, 10, "ISA", False, route, 1.0, cure))
    print(len(jobs), "jobs", flush=True)
    with multiprocessing.get_context("fork").Pool(8) as pool:
        rows = pool.map(job, jobs, chunksize=1)
    out = {"started": datetime.datetime.now().astimezone().isoformat(), "elapsed_s": time.monotonic() - t0,
           "basis": __doc__, "rows": rows}
    # material water before the bake at the named R10 endpoint (bake removes 90%)
    named = next(x for x in rows if x["finish"] == "MLCCAg" and x["R_m"] == 10 and x["weather"] == "ISA" and x["floor"]
                 and x["route"] == "bake70" and x["external_water"] == .1 and x["cure"])
    out["r10_named_material_water_after_bake_kg"] = named["named_bill"]["absorbed_water"]
    out["r10_named_material_water_before_bake_kg"] = named["named_bill"]["absorbed_water"] / .1
    with open(os.path.join(HERE, "P2CHECK.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "P2CHECK.json.tmp"), os.path.join(HERE, "P2CHECK.json"))
    print("elapsed", round(out["elapsed_s"], 1), "rows", len(rows))


if __name__ == "__main__":
    main()
