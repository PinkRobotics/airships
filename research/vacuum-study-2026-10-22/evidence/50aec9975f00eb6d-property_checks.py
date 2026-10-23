"""SR-200 sheet Poisson-ratio correction and targeted numerical cross-checks.

Imports only this card's own arithmetic. Run after calculate.py. The 021b
replication stays in RESULTS.json; the sheet-based scalar approximation is here.
This is not a full orthotropic shell model.
"""
import json
import hashlib
from datetime import datetime, timezone
import numpy as np
from scipy.optimize import brentq
import calculate as m


def main():
    m.NU=m.I["nu_SR200_sheet_scalar"]
    out={"schema":1,"card":"MAINLINE-028b","nu":m.NU,
         "nu_basis":"NASA CR-194164 Table 2: SR-200 1.96 mm sheet nu21=0.0752; nu12=0.0768. Use the lower in-plane value in the inherited scalar model, not an orthotropic validation.",
         "started_at":datetime.now(timezone.utc).isoformat(),"searches":[],"full_named_maxima":[]}
    sr,sens=m.I["materials"]
    for route in m.I["routes"]:
        for enforce in ([False,True] if route["seam"]=="scarf" else [True]):
            r=m.search(route,sr,enforce)
            out["searches"].append(r)
            print(route["id"],enforce,None if not r["least_set"] else
                  (r["least_set"]["subset"],r["least_set"]["min_max_usage"]),flush=True)
        for material in (sr,sens):
            full=m.maximize_full(route,material)
            out["full_named_maxima"].append({"route":route["id"],"material":material["id"],**full})
            print("full",route["id"],material["id"],full["least_SF"],flush=True)
    # Dense all-core subset search at the smallest safety margin; this includes
    # the core choice, not merely a finer refinement of the previous winner.
    dense=[]
    for route in m.I["routes"][:2]:
        coarse=next(x for x in out["searches"] if x["route"]==route["id"] and x["joint_screen_enforced"])
        best=None
        for core in m.I["cores"]:
            pt=m.best_on_curve(core,route,sr,(0,1),True,24000)
            if pt is not None and (best is None or pt["usage"]<best["usage"]):
                best=pt
        old=next(x for x in coarse["subsets"] if x["subset"]==list(m.NAMES[:2]))
        err=abs(best["usage"]-old["min_max_usage"]) if best and old["point"] else None
        dense.append({"route":route["id"],"coarse":old["point"],"dense":best,
                      "usage_error":err,"pass":err is not None and err<1e-7})
    # Independent scalar Brent root of the mass balance, with a separately
    # expanded joining expression, against the vector bisection.
    roots=[]
    for r in out["searches"]:
        if "floating_point" not in r: continue
        pt=r["floating_point"]; route=next(x for x in m.I["routes"] if x["id"]==r["route"])
        f,core=pt["fraction"],pt["core"]
        def residual(s):
            tf=(1-f)*s/(2*m.A*1850); tc=f*s/(m.A*core["rho"])
            overlap=30*tf if route["seam"]=="scarf" else 0
            ell=m.A*(1/(.6096-overlap)+1/(1.8288-overlap))
            mu=(2*tf*(901**.5)*.07 if route["seam"]=="scarf" else 0)+.25*tc+.002
            j=2*m.A*(route["bond_kg_m2"]+route.get("primer_kg_m2",0))+ell*mu
            return s+max(.05*s,j)+m.FIXED+m.SYS-m.LIFT
        s=brentq(residual,1,m.BUDGET,xtol=1e-10)
        err=abs(s-pt["masses_kg"]["structural"])
        roots.append({"route":r["route"],"joint_screen":r["joint_screen_enforced"],
                      "mass_error_kg":err,"pass":err<1e-8})
    upper=255e6*m.BUDGET/(1+m.J)/(2*m.A*1850)/m.N
    out["S200F255_all_subsets_infeasible_proof"]={
        "face_SF_upper_bound_even_with_zero_core":upper,
        "reason":"Even putting the entire structural budget into faces gives SF<1; any core or joint excess reduces it. Independent of nu, gamma and wrinkling.",
        "face_strength_is_fixed_Pa":255e6}
    check={"dense_subsets_match":all(x["pass"] for x in dense),
           "independent_mass_roots_match":all(x["pass"] for x in roots),
           "S200F255_analytic_impossibility":upper<1,
           "all_conditional_points_meet_their_enforced_modes":all(
               x["floating_point"]["at_needed"]["least_seven_screen_SF" if x["joint_screen_enforced"]
                                              else "least_six_mode_SF"]>=1-1e-8
               for x in out["searches"] if "floating_point" in x)}
    out["validation"]={"all_passed":all(check.values()),"checks":check,
                       "dense_grid":dense,"independent_roots":roots}
    out["ended_at"]=datetime.now(timezone.utc).isoformat()
    (m.ROOT/"PROPERTY-CHECKS.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps(out["validation"],indent=2),flush=True)
    assert all(check.values()),check


if __name__=="__main__":
    main()
