#!/usr/bin/env python3
"""049 sensitivity: the face-modulus multiplier (today and full scaled together) at which each beryllium-free
construction floats with all four of 040's optimisms at their endpoints, and the edge factor of CFRP on 5056 against
cure temperature (037b's method). Writes SENS.json."""
import json
import math
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model49 as M  # noqa: E402

C = json.load(open(os.path.join(HERE, "COMPUTE.json")))
MAT0 = dict(M.MAT)                     # 040's defaults, captured before any configure() changes the module state
BASE_T = json.load(open(os.path.join(HERE, "base040/THERMAL-TABLE.json")))
import thermal49 as TH  # noqa: E402


def configure(fk, ck, k_E=1.0):
    f = C["faces"][fk]
    c = C["cores"][ck]
    face = dict(f["face"])
    face["E_today_Pa"] *= k_E
    face["E_full_Pa"] *= k_E
    mat = dict(MAT0)
    mat.update(c["mat"])
    mat.update(dict(rho_f=face["rho"], alpha_f=f["alpha"], tf_min=f["tf_min"]))
    if fk != "AlBeMet AM162":
        mat.update(dict(joint="co-cured scarf", seam_film=C["seam_cfrp"]["seam_film"], seam_screen=C["seam_cfrp"]["seam_screen"]))
    thermal = BASE_T if c["k_W_mK"] is None else TH.table([15, 20, 30], k_core=c["k_W_mK"])
    M.set_material(face=face, core=c["core"], thermal=thermal, **mat)
    return f["nu"]


def payload_all(r, nu, cure, weather="ISA"):
    s = M.Settings(weather=weather, floor=False, pad="heavy70", vented=True, nu=nu, cure_temperature_K=cure)
    p = M.optimize(r, 15, 1.0, s)
    return None if p is None else p["signed_payload_kg"]


def main():
    t0 = time.monotonic()
    out = {"E_multiplier_to_float": [], "edge_vs_cure": []}
    cases = [("K13D2U QI", "CR-III 5056 3/8-1.0", 298.15), ("M55J QI", "CR-III 5056 3/8-1.0", 298.15),
             ("M55J QI", "HRH-49-1/4-2.1", 366.4833333333333), ("K13D2U QI", "HRH-49-1/4-2.1", 366.4833333333333),
             ("AlBeMet AM162", "CR-III 5056 3/8-1.0", 366.4833333333333)]
    for fk, ck, cure in cases:
        for r in (15, 20, 30):
            def f(k):
                nu = configure(fk, ck, k)
                v = payload_all(r, nu, cure)
                return -1e9 if v is None else v
            lo, hi = 1.0, 1.0
            while f(hi) < 0 and hi < 8:
                hi *= 1.25
            if f(hi) < 0:
                out["E_multiplier_to_float"].append({"face": fk, "core": ck, "cure_K": cure, "R_m": r, "k_E": None})
                continue
            for _ in range(40):
                mid = 0.5 * (lo + hi)
                if f(mid) >= 0:
                    hi = mid
                else:
                    lo = mid
            E_need = C["faces"][fk]["face"]["E_today_Pa"] * hi
            out["E_multiplier_to_float"].append({"face": fk, "core": ck, "cure_K": cure, "R_m": r, "k_E": hi, "E_need_Pa": E_need})
            print(fk, ck, r, "k_E", round(hi, 4), "E", round(E_need / 1e9, 1), "GPa", round(time.monotonic() - t0), "s", flush=True)
    # the CFRP-on-5056 edge factor against cure temperature, at R20's all-endpoint geometry from the RT-cure run
    row = next(x for x in C["rows"] if x["case"].startswith("M55J QI on CR-III 5056 3/8-1.0, room") and x["R_m"] == 20
               and x["weather"] == "ISA" and not x["floor"])
    g = row["endpoint_all_geometry"]
    for cure in (298.15, 310.0, 323.15, 338.15, 366.4833333333333, 394.26):
        configure("M55J QI", "CR-III 5056 3/8-1.0", 1.0)
        s = M.Settings(weather="ISA", floor=False, pad="heavy70", vented=True, nu=C["faces"]["M55J QI"]["nu"],
                       cure_temperature_K=cure)
        modes, th, props = M.mechanical(20, g["tf_m"], g["tc_m"], 15, 1.0, s)
        out["edge_vs_cure"].append({"cure_K": cure, "edge_SF": float(th), "tau_Pa": float(props["thermal_interface_shear_Pa"]),
                                    "cure_compression_Pa": float(props["added_cure_compression_Pa"]),
                                    "wall_SF": float(modes["core_cell_wall_yield_screen"])})
    out["elapsed_s"] = time.monotonic() - t0
    with open(os.path.join(HERE, "SENS.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "SENS.json.tmp"), os.path.join(HERE, "SENS.json"))
    print(json.dumps(out["edge_vs_cure"], indent=0))


if __name__ == "__main__":
    main()
