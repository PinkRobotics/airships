#!/usr/bin/env python3
"""MAINLINE-059: how much exterior water the P2 lead can carry. Uses this seat's model49/thermal49 (MAINLINE-049's port
of 040, which reproduces 048 bit for bit) on 048's account with CHECK-040's cure compression: multilayer CCAg/ITO, the
bake route and 10 g/m2 primer. Beryllium on 5056 is run at R 10, 12, 15, 20 and 30, ISA and optimistic, actual joining.

Exterior water is a bill line, so the endpoint geometry does not depend on it. The carried water at zero payload is
0.1 kg/m2 + payload / area at each endpoint. The least set is also searched at higher exterior water loads. Writes
CAP.json."""
import json
import math
import multiprocessing
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "unpublished-local-ref:5eec519919d3414d")
import model49 as M  # noqa: E402
import thermal49 as TH  # noqa: E402

D048 = "unpublished-local-ref:2c491d684a140b5c"
PROF = {x["id"]: x for x in json.load(open(f"{D048}/COATINGS.json"))}
F0, C0, MAT0 = dict(M.F), dict(M.C), dict(M.MAT)
RADII = (10, 12, 15, 20, 30)
G = {}


def settings(weather, water, floor=False):
    inst = PROF["MLCCAg"]["areal_mass_kg_m2"] * 1.10
    return M.Settings(weather=weather, floor=floor, coating=inst, finish_id="MLCCAg", external_water_kg_m2=water,
                      structural_primer_kg_m2=.01, moisture_scale=.1, finish_water_kg_m2=inst * .01, cure_in_global=True)


def job(args):
    r, w, water = args
    M.set_material(face=F0, core=C0, thermal=G["table"], **MAT0)
    res = M.least(r, settings(w, water))
    ep = {t["mask"]: t["solution"] for t in res["endpoint_trials"]}
    lp = res["least"]
    return {"R_m": r, "weather": w, "external_water": water,
            "least_axes": None if lp is None else lp["selected_axes"], "least_usage": None if lp is None else lp["usage"],
            "endpoint_named_kg": None if ep[11] is None else ep[11]["signed_payload_kg"],
            "endpoint_all_kg": None if ep[15] is None else ep[15]["signed_payload_kg"],
            "endpoint_today_kg": None if ep[0] is None else ep[0]["signed_payload_kg"]}


def main():
    t0 = time.monotonic()
    G["table"] = TH.table(list(RADII), alpha_out=PROF["MLCCAg"]["alpha"], epsilon_out=PROF["MLCCAg"]["epsilon"], night=True)
    jobs = [(r, w, .1) for r in RADII for w in ("ISA", "optimistic")]
    jobs += [(r, "ISA", x) for r in RADII for x in (.15, .2, .3, .5, 1.0)]
    jobs += [(r, "optimistic", 1.0) for r in (20, 30)]
    with multiprocessing.get_context("fork").Pool(8) as pool:
        rows = pool.map(job, jobs, chunksize=1)
    for x in rows:
        area = 4 * math.pi * x["R_m"] ** 2
        for k in ("named", "all"):
            p = x[f"endpoint_{k}_kg"]
            x[f"water_capacity_{k}_kg_m2"] = None if p is None else x["external_water"] + p / area
    out = {"basis": __doc__, "elapsed_s": time.monotonic() - t0, "rows": rows}
    with open(os.path.join(HERE, "CAP.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1)
    os.replace(os.path.join(HERE, "CAP.json.tmp"), os.path.join(HERE, "CAP.json"))
    for x in rows:
        print(x["R_m"], x["weather"], x["external_water"], x["least_axes"], None if x["least_usage"] is None else round(x["least_usage"], 4),
              round(x["endpoint_named_kg"], 1) if x["endpoint_named_kg"] is not None else None,
              round(x["water_capacity_named_kg_m2"], 4) if x["water_capacity_named_kg_m2"] is not None else None,
              round(x["water_capacity_all_kg_m2"], 4) if x["water_capacity_all_kg_m2"] is not None else None)


if __name__ == "__main__":
    main()
