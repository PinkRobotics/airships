#!/usr/bin/env python3
"""Optional P3 continuation: same 011b continuum and arc-member model.

Physical bay and radius bounds are held, while members/nodes are counted anew.
This imports only this card's environment function, never predecessor code.
"""
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from compute import I, P, L0, A0, environment

ROOT = Path(__file__).resolve().parent
FMODES = ("compression", "Euler", "local_tube_buckling", "film",
          "Perry", "global_lattice")
E, RHO, SIG, TFILM, RHOFILM = 410e9, 3100., 3900e6, 8e-5, 970.


def modes(radius, s, ro, cross, pressure, sig=SIG):
    ri2 = ro*ro-cross/math.pi
    ri = np.sqrt(np.maximum(ri2, 0.))
    tw = cross/(math.pi*(ro+ri))  # stable equivalent of ro-ri
    inertia = cross*(ro*ro+ri2)/4
    rg2 = inertia/cross
    stress = pressure*radius*s/(2*cross)+np.zeros_like(ro)
    sig_e = math.pi**2*E*rg2/(s*s)
    eta = s/1000.*ro/rg2
    phi = .5*(sig+(1+eta)*sig_e)
    # Rationalised Perry root avoids subtracting nearly equal terms.
    perry = sig*sig_e/(phi+np.sqrt(np.maximum(0.,phi*phi-sig*sig_e)))
    film = np.broadcast_to(2*1.5e9*TFILM/(s*pressure), np.shape(stress))
    vals = np.stack([
        np.broadcast_to(sig/stress, np.shape(stress)),
        sig_e/stress,
        .6*E*tw/ro/stress,
        film,
        perry/stress,
        .2*4*math.sqrt(1.5)*E*np.sqrt(inertia*cross)/(s*radius*radius*pressure),
    ])
    return dict(values=vals, tw=tw, inertia=inertia, stress=stress, ri=ri)


def evaluate(s, u, radius, scenario, pump_scaled=False, payload=0., sig=SIG, node_scale=0):
    s, u = np.asarray(s), np.asarray(u)
    env = environment(radius, scenario, pump_scaled, system_floor=50.)
    nodes = 8*math.pi*radius**2/(math.sqrt(3)*s*s)+2
    members = 3*nodes-6
    # Optional load-linked node mass: pressure-resultant scale R*s versus 10*2.04.
    unit_node = .02 if node_scale==0 else .02*(radius*s)/(10*2.04)
    node_mass = nodes*unit_node
    film_mass = env["area_m2"]*TFILM*RHOFILM
    tube = (env["lift_kg"]-50-env["other_reserve_kg"]-payload-film_mass-node_mass)/1.05
    cross = np.maximum(tube,1e-12)/(members*s*RHO)
    rmin = np.sqrt(cross/math.pi)*1.0001
    rmax = np.minimum(.25,s/3)
    ro = rmin+u*(rmax-rmin)
    valid = (tube>0)&(rmax>rmin)&(u>=0)&(u<=1)&(s>=.4)&(s<=3)
    m = modes(radius,s,ro,cross,env["high_pressure_Pa"],sig)
    least = np.where(valid, m["values"].min(axis=0), -1.)
    return dict(**m,least=least,ro=ro,cross=cross,tube=tube,nodes=nodes,members=members,
                node_mass=node_mass,film_mass=film_mass,env=env,valid=valid)


def optimum(radius, scenario, pump_scaled=False, payload=0., sig=SIG,
            node_scale=0, dense=False):
    ns, nu = (801,1001) if dense else (131,401)
    ss=np.linspace(.4,3,ns)[:,None]
    us=np.linspace(0,1,nu)[None,:]
    def ev(s,u):
        return evaluate(s,u,radius,scenario,pump_scaled,payload,sig,node_scale)
    g=ev(ss,us)
    y=g["least"]
    if y.max()<0:
        return dict(feasible=False,radius_m=radius,scenario=scenario,pump_scaled=pump_scaled,
                    reason="No positive feasible tube section in held geometry bounds.")
    if dense:
        return float(y.max())
    candidates=[]
    rowbest=y.max(axis=1)
    peaks=np.r_[0,np.where((rowbest[1:-1]>=rowbest[:-2])&(rowbest[1:-1]>=rowbest[2:]))[0]+1,ns-1]
    for j in sorted(peaks,key=lambda j:-rowbest[j])[:8]:
        k=int(y[j].argmax())
        seed=[float(ss[j,0]),float(us[0,k])]
        candidates.append(seed)
        refined=minimize(lambda v:-float(ev(v[0],v[1])["least"]),seed,
                         method="Nelder-Mead",bounds=[(.4,3),(0,1)],
                         options={"xatol":1e-11,"fatol":1e-12,"maxiter":2000})
        candidates.append(refined.x.tolist())
    s,u=max(candidates,key=lambda v:float(ev(*v)["least"]))
    q=ev(s,u)
    vals=dict(zip(FMODES,map(float,q["values"])))
    sf=min(vals.values())
    env=q["env"]
    return dict(feasible=True,tag="PROJECTION",material="SiC-alpha-Hexoloy-SA",
                radius_m=radius,scenario=scenario,pump_scaled=pump_scaled,
                sigma_Pa=sig,node_mass_law="fixed 20g/node" if node_scale==0 else "20g scaled by R*s/(10*2.04)",
                s_m=s,ro_m=float(q["ro"]),wall_m=float(q["tw"]),
                A_m2=float(q["cross"]),I_m4=float(q["inertia"]),r_i_m=float(q["ri"]),
                modes=vals,least_SF=sf,governs=[k for k,v in vals.items() if abs(v-sf)<1e-6*sf],
                nodes=float(q["nodes"]),members=float(q["members"]),
                masses_kg=dict(film=q["film_mass"],nodes=float(q["node_mass"]),
                               tubes=float(q["tube"]),joints=.05*float(q["tube"]),
                               systems_floor=50.,
                               design_envelope_total=q["film_mass"]+float(q["node_mass"])+
                               1.05*float(q["tube"])+50+env["other_reserve_kg"]+payload),
                reserve_kg=env["other_reserve_kg"],reserve_fraction=env["other_reserve_kg"]/env["lift_kg"],
                payload_kg=payload,environment=env,
                limits="0.4<=s<=3m, ro<=min(0.25m,s/3), film80um, 1.5GPa film, k0.2, a0=s/1000; arc members.")


def payload_at_one(radius,scenario,pump_scaled=False):
    z=optimum(radius,scenario,pump_scaled)
    if not z["feasible"] or z["least_SF"]<1:
        return dict(reaches_SF1=False,maximum_payload_kg=None)
    lo,hi=0.,L0*(radius/10)**3
    for _ in range(32):
        mid=(lo+hi)/2
        p=optimum(radius,scenario,pump_scaled,payload=mid)
        if p["feasible"] and p["least_SF"]>=1:lo=mid
        else:hi=mid
    p=optimum(radius,scenario,pump_scaled,payload=lo)
    return dict(reaches_SF1=True,maximum_payload_kg=lo,point=p,
                tag="PROJECTION",condition="011b's unrealised joints/nodes/curved ceramic tubes, film and brittle-member model.")


def main():
    source=next(r for r in I["reference_011b"]["RESULTS.json"]["primary_joints_on"]["SiC-alpha-Hexoloy-SA"]
                if r["grid"]=="equilateral_triangular" and r["k"]==.2)
    ref=modes(10.,source["s_m"],source["r_o_m"],source["A_m2"],95460.8379139)
    expected=[source[k] for k in ("SF_yield","SF_euler","SF_local","SF_film","SF_perry","SF_global")]
    err=max(abs(float(x)-y) for x,y in zip(ref["values"],expected))
    assert err<1e-10
    similar=[]
    for r in I["radii_m"]:
        x=r/10.
        mo=modes(r,source["s_m"]*x,source["r_o_m"]*x,source["A_m2"]*x*x,P)
        vals=dict(zip(FMODES,map(float,mo["values"])))
        similar.append(dict(radius_m=r,s_m=source["s_m"]*x,ro_m=source["r_o_m"]*x,
                            wall_m=source["t_w_m"]*x,film_m=TFILM,
                            nodes=source["nodes"],node_mass_kg=source["m_nodes_kg"],
                            tube_mass_kg=source["m_tube_kg"]*x**3,
                            joint_mass_kg=source["m_joint_kg"]*x**3,
                            film_mass_kg=A0*x*x*TFILM*RHOFILM,
                            modes=vals,least_SF=min(vals.values()),
                            note="Shape scaling demonstration only; not a closed environmental budget or an optimised payload."))
    rows=[];checks=[]
    for pump_scaled in (False,True):
        for label in I["scenarios"]:
            if pump_scaled and label=="optimistic":continue
            for r in I["radii_m"]:
                pt=optimum(r,label,pump_scaled)
                pt["payload_at_SF1"]=payload_at_one(r,label,pump_scaled)
                if pt["feasible"]:
                    dense=optimum(r,label,pump_scaled,dense=True)
                    assert pt["least_SF"]>=dense-1e-7,(pt,dense)
                    assert abs(pt["masses_kg"]["design_envelope_total"]-pt["environment"]["lift_kg"])<1e-7
                    checks.append(dict(radius_m=r,scenario=label,pump_scaled=pump_scaled,
                                       dense_best=dense,refined_best=pt["least_SF"]))
                rows.append(pt)
    sensitivity=[]
    for r in I["radii_m"]:
        sensitivity.append(optimum(r,"optimistic",sig=380e6))
        sensitivity.append(optimum(r,"optimistic",node_scale=1))
    data=dict(schema=1,tag="PROJECTION",reproduction_max_error=err,similarity=similar,
              P3=rows,sensitivities=sensitivity,dense_checks=checks,
              film_limited_similarity_radius_at_SF1_m=10*source["SF_film"],
              scope="No Be-face/core bond films charged to P3. Frame joints remain 5% of tubes; film seam/attachment qualification and extra mass are NFI.")
    (ROOT/"FRAME.json").write_text(json.dumps(data,indent=2)+"\n")
    print("P3 reproduction max error",err,"rows",len(rows),"checks",len(checks))
    for p in rows:
        print(p["scenario"],p["radius_m"],p["pump_scaled"],p.get("least_SF"),p["payload_at_SF1"].get("maximum_payload_kg"))


if __name__=="__main__":
    main()
