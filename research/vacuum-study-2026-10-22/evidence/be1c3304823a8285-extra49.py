#!/usr/bin/env python3
"""049 extras: (1) K13D2U at Toray's 60% Vf translation (PROJECTION) through the whole bill on 5056 at a room-temperature
and a 50 C cure; (2) the endpoint bill of every construction at R 15/20/30 ISA, actual joining, all four optimisms.
Writes EXTRA.json."""
import json
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

C = json.load(open(os.path.join(HERE, "COMPUTE.json")))
BASE_T = json.load(open(os.path.join(HERE, "base040/THERMAL-TABLE.json")))
MAT0 = dict(M.MAT)
F0, C0 = dict(M.F), dict(M.C)


def mat_for(fk, ck, face):
    f, c = C["faces"][fk], C["cores"][ck]
    mat = dict(MAT0)
    mat.update(c["mat"])
    mat.update(dict(rho_f=face["rho"], alpha_f=f["alpha"], tf_min=f["tf_min"]))
    if fk != "AlBeMet AM162":
        mat.update(dict(joint="co-cured scarf", seam_film=C["seam_cfrp"]["seam_film"], seam_screen=C["seam_cfrp"]["seam_screen"]))
    return mat


def k60_face(faces):
    """K13D2U at Toray's 60% Vf translation (PROJECTION): E1 = fibre modulus x M55J's UD E1 / fibre modulus, with
    Tuttle's E2, G12 and nu12 kept. Shared with fold49."""
    k_fib = S.val("k13_fibE", "cfrp", "k13d2u_fibre", "Fibre tensile modulus", 935.0) * 1e9
    m_fib = S.val("m55j_fibE", "cfrp", "m55j_fibre", "Fibre tensile modulus", 540.0) * 1e9
    m_E1 = S.val("m55j_E1", "cfrp", "m55j_lamina", "UD composite 0 deg tensile modulus E1", 338.0) * 1e9
    eff = m_E1 / m_fib
    k_E1 = k_fib * eff
    E2 = S.val("k13_E2", "cfrp", "k13d2u_lamina", "Lamina transverse modulus E2", 5.557) * 1e9
    G12 = S.val("k13_G12", "cfrp", "k13d2u_lamina", "Lamina in-plane shear modulus G12", 4.102) * 1e9
    nu12 = S.val("k13_nu12", "cfrp", "k13d2u_lamina", "Lamina major Poisson ratio", 0.39)
    qi = LAM.quasi_iso(k_E1, E2, G12, nu12)
    f = faces["K13D2U QI"]
    face = dict(f["face"], name="K13D2U/epoxy QI at 60% Vf (PROJECTION)", E_today_Pa=qi["E_Pa"], E_full_Pa=qi["E_Pa"])
    face["strength_full_Pa"] = face["strength_today_Pa"] / (1 - qi["nu"])
    return {"face": face, "qi": qi, "eff": eff, "E1_Pa": k_E1}


def main():
    t0 = time.monotonic()
    out = {}
    # (1) K13D2U at 60% Vf: E1 = fibre modulus x (M55J's UD E1 / fibre E at 60% Vf), the rest of Tuttle's lamina kept
    K = k60_face(C["faces"])
    face, qi, eff, k_E1 = K["face"], K["qi"], K["eff"], K["E1_Pa"]
    out["k13_60"] = {"E1_Pa": k_E1, "translation": eff, "E_QI_Pa": qi["E_Pa"], "nu_QI": qi["nu"], "rows": []}
    for cure, tag in ((298.15, "room-temperature cure (PROJECTION)"), (323.15, "50 C cure (PROJECTION)")):
        mat = mat_for("K13D2U QI", "CR-III 5056 3/8-1.0", face)
        rows = A.account(f"K13D2U QI at 60% Vf (PROJECTION) on CR-III 5056 3/8-1.0, {tag}", face, C0, qi["nu"], mat,
                         thermal=BASE_T, cure_K=cure)
        out["k13_60"]["rows"] += rows
        print(tag, "done", round(time.monotonic() - t0), "s", flush=True)
    # (2) the endpoint bills, all four optimisms at their endpoints, R 15/20/30 ISA actual
    bills = []
    combos = [("Be", None, None, 366.4833333333333), ("AlBeMet AM162", "CR-III 5056 3/8-1.0", None, 366.4833333333333),
              ("M55J QI", "CR-III 5056 3/8-1.0", None, 298.15), ("M55J QI", "HRH-10-3/8-1.5", None, 366.4833333333333),
              ("M55J QI", "HRH-49-1/4-2.1", None, 366.4833333333333), ("K13D2U QI", "CR-III 5056 3/8-1.0", None, 298.15),
              ("K13D2U QI", "HRH-10-3/8-1.5", None, 366.4833333333333), ("K13D2U QI", "HRH-49-1/4-2.1", None, 366.4833333333333),
              ("K13D2U QI 60% Vf", "CR-III 5056 3/8-1.0", face, 298.15)]
    for fk, ck, fface, cure in combos:
        for r in (15, 20, 30):
            if fk == "Be":
                M.set_material(face=F0, core=C0, thermal=BASE_T, **MAT0)
                nu = .0768
            else:
                base_fk = "K13D2U QI" if fk.startswith("K13D2U QI 60") else fk
                ff = fface or C["faces"][base_fk]["face"]
                c = C["cores"][ck]
                M.set_material(face=ff, core=c["core"], thermal=BASE_T if c["k_W_mK"] is None else TH.table([r], k_core=c["k_W_mK"]),
                               **mat_for(base_fk, ck, ff))
                nu = qi["nu"] if fk.startswith("K13D2U QI 60") else C["faces"][base_fk]["nu"]
            s = M.Settings(weather="ISA", floor=False, pad="heavy70", vented=True, nu=nu, cure_temperature_K=cure)
            p = M.optimize(r, 15, 1.0, s)
            bills.append({"face": fk, "core": ck or "CR-III 5056 3/8-1.0", "R_m": r, "cure_K": cure,
                          "payload_kg": None if p is None else p["signed_payload_kg"],
                          "bill_kg": None if p is None else p["bill_kg"], "lift_kg": None if p is None else p["lift_kg"],
                          "joining": None if p is None else p["actual_joining"],
                          "geometry": None if p is None else p["geometry"],
                          "modes": None if p is None else p["modes"]})
    M.set_material(face=F0, core=C0, thermal=BASE_T, **MAT0)
    out["endpoint_bills"] = bills
    out["sources_used"] = S.USED
    out["elapsed_s"] = time.monotonic() - t0
    with open(os.path.join(HERE, "EXTRA.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "EXTRA.json.tmp"), os.path.join(HERE, "EXTRA.json"))
    print("elapsed", round(out["elapsed_s"], 1))


if __name__ == "__main__":
    main()
