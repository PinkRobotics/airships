"""Resolve search differences without changing the predeclared tolerances."""
import json
import math
import re
from collections import Counter
from scipy.optimize import brentq, minimize_scalar
import numpy as np
from independent import (
    ROOT, BY_NAME, DEFAULT, INPUT, P0, BETA, direct, reserves, at_fraction,
    thickness_bounds, _mass_from_bounds, grid_fractions, optimize_ideal,
    face_properties,
)

owner=json.loads((ROOT/"owner/RESULTS.json").read_text())
search=json.loads((ROOT/"SEARCH.json").read_text())


def fetch(path):
    obj=owner
    path=re.sub(r"\[(\d+)\]",r".\1",path.removeprefix("$."))
    for key in path.split("."):
        obj=obj[int(key)] if isinstance(obj,list) else obj[key]
    return obj


def best_core(radius,core,mask,settings,fmin):
    fractions=grid_fractions(8193,fmin)
    b,d,y,c=thickness_bounds(fractions,mask,1.,settings,core)
    val,_,_=_mass_from_bounds(radius,b,d,y,c,settings)
    ix=int(np.argmax(val))
    if not np.isfinite(val[ix]):
        return dict(payload_kg=None,f=None,point=None)
    candidates=[(float(val[ix]),float(fractions[ix]))]
    peaks=np.flatnonzero((val[1:-1]>=val[:-2])&(val[1:-1]>=val[2:])&np.isfinite(val[1:-1]))+1
    for j in peaks:
        opt=minimize_scalar(lambda z:-float(at_fraction(radius,z,core,mask,1.,settings)[0]),
                            bounds=(fractions[j-1],fractions[j+1]),method="bounded",
                            options={"xatol":2e-13})
        candidates.append((-float(opt.fun),float(opt.x)))
    payload,f=max(candidates)
    _,tf,tc=at_fraction(radius,f,core,mask,1.,settings)
    point=direct(radius,core,float(tf),float(tc),mask,1.,settings)
    guard=0.
    if point["scored_least_SF"]<1-1e-8 and abs(point["geometry"]["Vc"]-2)<1e-12:
        # Direct recomputation can round the exact branch point to its lower
        # side. Exhibit a strictly upper-sided feasible witness instead.
        guard=4e-12
        point=direct(radius,core,float(tf)*(1+guard),float(tc)*(1+guard),mask,1.,settings)
    return dict(payload_kg=point["masses_kg"]["payload"],raw_search_payload_kg=payload,
                f=f,one_sided_branch_guard=guard,point=point)


core_cache={}
ideal_cache={}
resolved=[]
for failure in search["failures"]:
    row=failure.copy()
    path=row["path"]
    if row["kind"]=="all_core_optimization":
        context=fetch(path.split(".per_core_optima")[0])
        pc=fetch(path.rsplit(".",1)[0])
        key=json.dumps([context["R_m"],pc["core"],context["mask"],context["settings"]],sort_keys=True)
        if key not in core_cache:
            core_cache[key]=best_core(context["R_m"],pc["core"],context["mask"],
                                      context["settings"],.00025)
        bounded=core_cache[key]
        delta=(bounded["payload_kg"]-row["reported"] if
               bounded["payload_kg"] is not None and row["reported"] is not None else None)
        matches=(abs(delta)<=row["tolerance"] if delta is not None else
                 bounded["payload_kg"]==row["reported"])
        row.update(disposition="fraction_domain_extension",core=pc["core"],
                   R_m=context["R_m"],restricted_fraction_range=[.00025,.99975],
                   restricted_payload_kg=bounded["payload_kg"],
                   restricted_difference_kg=delta,
                   agrees_on_restricted_domain=matches,
                   restricted_f=bounded["f"])
        # Preserve a direct physical-score witness for the wider-domain alternative.
        extended=best_core(context["R_m"],pc["core"],context["mask"],context["settings"],None)
        row["extended_witness"]=extended
        if not matches and bounded["point"] is not None:
            # These remaining rows are the same low-density, flat-gamma kink.
            c=BY_NAME[pc["core"]]
            settings=context["settings"]
            E,_=face_properties(context["mask"],1.)
            q=.82 if context["mask"]&2 else .33
            p=P0*settings["pressure_factor"]
            y0=bounded["point"]["geometry"]["tc_m"]/bounded["point"]["geometry"]["tf_m"]
            def kink(logy):
                y=math.exp(logy)
                lam=p/(4*BETA*q*math.sqrt(E*c["Ec_Pa"]/y))
                out=direct(1,c,lam,y*lam,context["mask"],1.,settings)
                return out["modes"]["global_buckling"]-1,lam,y
            z=brentq(lambda z:kink(z)[0],math.log(y0)-.15,math.log(y0)+.15,xtol=2e-14)
            _,lam,y=kink(z)
            polished=direct(context["R_m"],c,context["R_m"]*lam,
                            context["R_m"]*lam*y,context["mask"],1.,settings)
            row["polished_restricted_point"]=polished
            row["polished_restricted_difference_kg"]=polished["masses_kg"]["payload"]-row["reported"]
            row["additional_finding"]="Nonwinning same-domain active-mode-intersection precision; the residual is retained, not waived."
    elif ".ideal[" in path:
        track=path.split(".tracks.",1)[1].split(".ideal",1)[0]
        bi=int(re.search(r"\.ideal\[(\d+)\]",path).group(1))
        ci=int(re.search(r"\.per_core\[(\d+)\]",path).group(1))
        t=owner["tracks"][track]
        bound=(t["ideal_upper_bounds"]+[t["handbook_flat_gamma_ideal_bound"]])[bi]
        settings=t["settings"]|{"flat_gamma":bi==8}
        core=bound["per_core"][ci]["core"]
        key=json.dumps([bound["mask"],settings],sort_keys=True)
        if key not in ideal_cache:
            ideal_cache[key]=optimize_ideal(bound["mask"],settings,n=8193,fraction_min=.00025)
        bounded=next(x for x in ideal_cache[key]["per_core"] if x["core"]==core)
        delta=bounded["largest_least_SF"]-row["reported"]
        row.update(disposition="fraction_domain_extension",core=core,
                   restricted_fraction_range=[.00025,.99975],
                   restricted_least_SF=bounded["largest_least_SF"],
                   restricted_difference=delta,
                   agrees_on_restricted_domain=abs(delta)<=row["tolerance"],
                   restricted_f=bounded["f"])
    elif row["kind"]=="radius_sample":
        track=path.split(".tracks.",1)[1].split(".thresholds",1)[0]
        ti=int(re.search(r"\.thresholds\[(\d+)\]",path).group(1))
        si=int(re.search(r"\.samples\[(\d+)\]",path).group(1))
        threshold=owner["tracks"][track]["thresholds"][ti]
        radius=threshold["samples"][si][0]
        mask=threshold["mask"]
        settings=owner["tracks"][track]["settings"]
        # Exact cache key used in audit_search; read data, never executable code.
        key=json.dumps([float(radius).hex(),mask,float(1).hex(),settings,2049],sort_keys=True)
        got=None
        for line in (ROOT/"SEARCH-LEDGER.jsonl").open():
            record=json.loads(line)
            if record["key"]==key:
                got=record["point"];break
        assert got is not None
        tf,tc=got["geometry"]["tf_m"],got["geometry"]["tc_m"]
        # A declared numerical sensitivity, not a claim about unseen owner code.
        guard=3e-13
        guarded=direct(radius,got["core"],tf*(1+guard),tc*(1+guard),mask,1.,settings)
        guarded_fraction=guarded["masses_kg"]["payload"]/reserves(radius)[0]
        width=INPUT["stock_panel"]["a_m"]-30*tf
        row.update(disposition="near_overlap_endpoint_sensitivity",R_m=radius,
                   radius_to_geometric_ceiling=radius/threshold["geometric_radius_ceiling_m"],
                   remaining_short_panel_coverage_m=width,
                   independent_tf_m=tf,independent_tc_m=tc,
                   thickness_relative_perturbation=guard,
                   perturbed_payload_fraction=guarded_fraction,
                   perturbed_difference=guarded_fraction-row["reported"],
                   perturbation_matches_reported_tolerance=abs(guarded_fraction-row["reported"])<=row["tolerance"],
                   interpretation="A 3e-13 relative thickness sensitivity reproduces the scale of the discrepancy. This is an inference about numerical conditioning, not inspection of the owner's code. Both values are enormously negative.")
    elif row["kind"]=="radius_root":
        row["disposition"]="formal_crossing_precision"
    else:
        row["disposition"]="unresolved"
    resolved.append(row)
print("Difference classifications:",dict(Counter(r["disposition"] for r in resolved)),flush=True)

# Independent active-constraint roots remove the outer optimizer from each
# finite crossing. Brackets use this check's search, not the owner's radius.
active=[]
for t in search["thresholds"]:
    if t["first_R_m"] is None:
        continue
    own=t["witness"]
    mask=t["mask"]
    settings=owner["tracks"][t["track"]]["settings"]
    c=BY_NAME[own["core"]]
    E,strength=face_properties(mask,1.)
    pressure=P0*settings["pressure_factor"]
    q=.82 if mask&2 else .33
    y0=own["geometry"]["tc_m"]/own["geometry"]["tf_m"]
    def shape(logy):
        y=math.exp(logy)
        if mask in [5,6]:
            lam=pressure/(4*BETA*q*math.sqrt(E*c["Ec_Pa"]/y))
            equation="crimp" if mask==6 else "global"
        else:
            cap=10e6*901/30 if settings["scarf_screen"] else strength
            lam=pressure/(4*cap)
            equation="global"
        point=direct(1,c,lam,y*lam,mask,1.,settings)
        mode="core_shear_crimping" if equation=="crimp" else "global_buckling"
        return point["modes"][mode]-1,lam,y
    z=brentq(lambda z:shape(z)[0],math.log(y0)-.15,math.log(y0)+.15,xtol=2e-14)
    _,lam,y=shape(z)
    def mass(radius):
        return direct(radius,c,radius*lam,radius*lam*y,mask,1.,settings)["masses_kg"]["payload"]
    radius=brentq(mass,t["first_R_m"]-.05,t["first_R_m"]+.05,xtol=2e-11)
    witness=direct(radius,c,radius*lam,radius*lam*y,mask,1.,settings)
    local=[]
    for delta in [-1e-5,-1e-6,-1e-7,1e-7,1e-6,1e-5]:
        f=witness["f"]+delta
        value=float(at_fraction(radius,f,c,mask,1.,settings)[0])
        local.append(dict(f_offset=delta,payload_kg=value,
                          no_better_than_active_witness=value<=witness["masses_kg"]["payload"]+1e-7))
    active.append(dict(track=t["track"],mask=mask,core=c["name"],
                       reported_R_m=t["reported_first_R_m"],searched_R_m=t["first_R_m"],
                       active_constraint_R_m=radius,
                       delta_reported_m=radius-t["reported_first_R_m"],
                       delta_search_m=radius-t["first_R_m"],
                       tolerance_m=2e-5,
                       matches_reported_radius=abs(radius-t["reported_first_R_m"])<=2e-5,
                       local_shape_checks=local,witness=witness))

stock=4*INPUT["face"]["strength_full_Pa"]*.00635/(P0*1.01)
result=dict(schema=1,raw_search_difference_count=len(resolved),
            disposition_counts=dict(Counter(r["disposition"] for r in resolved)),
            restricted_domain_all_reproduced=all(r.get("agrees_on_restricted_domain",True) for r in resolved),
            residual_same_domain_differences=[r for r in resolved if
                        not r.get("agrees_on_restricted_domain",True)],
            unclassified=[r for r in resolved if r["disposition"]=="unresolved"],
            differences=resolved,active_constraint_crossings=active,
            stock_compression_radius_ceiling_m=stock,
            restricted_domain_note="The 3999 interior-fraction search has first grid point .00025; this restricted-domain diagnostic distinguishes that numerical scope from the extended search down to 1e-8. No fabrication validity is assigned to tiny-core alternatives.")
(ROOT/"DIFFERENCES.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
print(json.dumps({'restricted_domain_all_reproduced':result["restricted_domain_all_reproduced"],
                  'residual_same_domain_count':len(result["residual_same_domain_differences"]),
                  'active_crossings':[{k:v for k,v in a.items() if k not in ['witness','local_shape_checks']} for a in active]},
                 indent=2),flush=True)
