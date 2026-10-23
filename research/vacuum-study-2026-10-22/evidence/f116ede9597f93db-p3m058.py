#!/usr/bin/env python3
"""MAINLINE-058 P3 account against design load, from 052's frozen RESULTS rows (data only, ground service).
For every radius and every one of the 16 endpoint subsets (plus the baseline), each pressure-dependent item is fitted
as ln(kg) = a + n ln(p) over 052's three applied loads (97172.3 / 98402.7 / 99707.1 Pa); the other items are fixed.
Sag volume = 052's ISA sag lift debit / 500 m ISA density, held fixed; lift = rho_local (V - V_sag); 052's weather
headroom is not charged (the local density replaces it, as in 050). P3 has no cold screen in its account.
Writes runs/p3_058.json."""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lev058 as L  # noqa: E402
import p2m058 as m  # noqa: E402

F052 = Path("unpublished-local-ref:9b9c35e476f00701"
            "vacuum-mainline052-p3-common-account-1020/RESULTS.json")
OUT = Path("unpublished-local-ref:3c8f53a40b5020e4"
           "vacuum-mainline058-flyable-band-1020/runs/p3_058.json")
VARIABLE = ("SiC_tubes", "joint_sleeves_and_allowance", "joint_bond_and_installation", "PBO_two_plies")
SKIP = ("sag_lift_debit", "weather_headroom")


class P3Hull:
    def __init__(self, radius, fits, fixed, v_sag):
        self.r = radius
        self.volume = 4 * math.pi * radius ** 3 / 3
        self.fits, self.fixed, self.v_sag = fits, fixed, v_sag

    def bill(self, p_design):
        b = dict(self.fixed)
        for k, (a, n) in self.fits.items():
            b[k] = math.exp(a + n * math.log(p_design))
        return b

    def mass(self, p_design):
        return sum(self.bill(p_design).values())


def load_hulls():
    rows = [r for r in json.loads(F052.read_text())["rows"] if r["service"] == "ground"]
    out = {}
    for R in sorted({r["R_m"] for r in rows}):
        sub = {r["weather"]: r for r in rows if r["R_m"] == R}
        for sel in ["baseline"] + [f"mask{k}" for k in range(16)]:
            recs = {}
            for w, r in sub.items():
                recs[w] = r["baseline"] if sel == "baseline" else next(e for e in r["endpoints"] if e["mask"] == int(sel[4:]))
            ps = np.array([recs[w]["applied_pressure_Pa"] for w in ("ISA", "both", "optimistic")])
            fits, resid = {}, {}
            for k in VARIABLE:
                y = np.log([recs[w]["bill_kg"][k] for w in ("ISA", "both", "optimistic")])
                n, a = np.polyfit(np.log(ps), y, 1)
                fits[k] = (float(a), float(n))
                resid[k] = float(np.max(np.abs(a + n * np.log(ps) - y)))
            isa = recs["ISA"]["bill_kg"]
            fixed = {k: v for k, v in isa.items() if k not in VARIABLE and k not in SKIP}
            for k in fixed:
                assert all(abs(recs[w]["bill_kg"][k] - fixed[k]) < 1e-6 for w in recs), (R, sel, k)
            v_sag = isa["sag_lift_debit"] / m.RHOREF
            out[(R, sel)] = {"hull": P3Hull(R, fits, fixed, v_sag), "fit_max_log_residual": resid,
                             "axes": recs["ISA"].get("axes", []), "isa_payload_052": recs["ISA"]["payload_kg"],
                             "isa_load_052": float(ps[0])}
    return out


def lift(h, z, offset, dp, rh, p_design, mode):
    """As lev058.lift_trim, with the sag volume removed from the buoyant volume."""
    vol = h.volume - h.v_sag
    return L.lift_trim(vol, z, offset, dp, rh, p_design, mode)


def hot_edge(h, mass, z, dp, rh, p_design, mode):
    return L.hot_edge(h.volume - h.v_sag, mass, z, dp, rh, p_design, mode)


def main():
    hulls = load_hulls()
    p_full = 103953.19780784745
    p_trim = L.design_load(100, -30)
    res = {"unit": "vacuum-mainline058-flyable-band-1020", "tag": "QUESTIONABLE / PROJECTION", "p_full_Pa": p_full,
           "p_trim_Pa": p_trim, "rows": []}
    for (R, sel), rec in sorted(hulls.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        h = rec["hull"]
        # reproduce 052's ISA payload at its own load and 500 m ISA density with V_sag charged
        check = m.RHOREF * (h.volume - h.v_sag) - h.mass(rec["isa_load_052"])
        row = {"R_m": R, "selection": sel, "axes": rec["axes"], "fits": h.fits, "fit_max_log_residual": rec["fit_max_log_residual"],
               "v_sag_m3": h.v_sag, "isa_payload_052_kg": rec["isa_payload_052"], "isa_payload_reproduced_kg": check,
               "mass_full_kg": h.mass(p_full), "mass_trim_kg": h.mass(p_trim), "bill_full": h.bill(p_full),
               "bill_trim": h.bill(p_trim), "edges": []}
        for hid, p_d in (("full", p_full), ("trim-30", p_trim)):
            mass = h.mass(p_d)
            for mode in (("none",) if hid == "full" else ("none", "trim", "climb")):
                for dp in L.DP:
                    for rh in L.RH:
                        he = hot_edge(h, mass, 100, dp, rh, p_d, mode)
                        row["edges"].append({"hull": hid, "mode": mode, "dp_hPa": float(dp), "RH": rh, "hot_edge_offset_K": he})
        res["rows"].append(row)
        if sel in ("baseline", "mask15", "mask11"):
            e = {(x["hull"], x["mode"], x["dp_hPa"], x["RH"]): x["hot_edge_offset_K"] for x in row["edges"]}
            print(R, sel, round(row["isa_payload_052_kg"], 3), round(check, 3), "full", round(row["mass_full_kg"], 1),
                  "trim", round(row["mass_trim_kg"], 1), "hot -30 RH100 full/trim:", e[("full", "none", -30.0, 1.0)],
                  e[("trim-30", "trim", -30.0, 1.0)], "n_tubes", round(h.fits["SiC_tubes"][1], 4), flush=True)
    OUT.write_text(json.dumps(res, indent=1, default=float))
    print("DONE")


if __name__ == "__main__":
    main()
