"""Independent CHECK-037b arithmetic. No owner code imported or executed.

The comparison side reads only JSON numerical claims. The calculation side uses
the equations derived in METHOD.md and primary/reference input data.
"""
from pathlib import Path
import json
import math
import datetime
import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parent
C = json.loads((ROOT / "owner/COMPUTE.json").read_text())
P = json.loads((ROOT / "upstream/vacuum-mainline028b-joining-into-021b-1020/PROPERTY-CHECKS.json").read_text())
X37 = json.loads((ROOT / "upstream/vacuum-mainline037-loads-beyond-pressure-1020/RESULTS.json").read_text())
POINT37 = next(r for r in P["full_named_maxima"] if r["route"] == "af015_scarf" and r["material"] == "SR200")["point"]
TF37, TC37 = POINT37["tf_m"], POINT37["tc_m"]
CORE = POINT37["core"]
R = 10.0
A = 4 * math.pi * R**2
P0 = 95460.83791390515
LIFT = 4889.442150186961
RESERVE = 411.2989440716474
SYSTEMS = 100.0
BUDGET = LIFT - RESERVE - SYSTEMS
EF, NU, RHOF = 290e9, 0.0752, 1850.0
ALPHA_F, ALPHA_C = 11.3e-6, 23.6e-6
DA = ALPHA_C - ALPHA_F
ES, RHOS, YS = 67e9, 2700.0, 227.53e6
PSI = 0.45359237 * 9.80665 / 0.0254**2
RHO = 0.45359237 / 0.3048**3
GC, GL, EC = 6800 * PSI, 15000 * PSI, 15000 * PSI
SW, SL, SWMIN, SLMIN = 35 * PSI, 55 * PSI, 25 * PSI, 45 * PSI
REL = RHO / RHOS
KB = ES * REL / 2
K2 = KB / 2
GSI, RHOSI = 0.635e6, 1490.0
AF = 0.015 * 0.45359237 / 0.09290304
BETA = brentq(lambda z: z**3 + z - 1, 0, 1, xtol=1e-15)
HOT = X37["p2_thermal"]["coated_outer"]["T_outer_subsolar_K"]
COLD = HOT - X37["p2_thermal"]["coated_outer"]["day_night_outer_swing_K"]
SWING = HOT - COLD
MID = (HOT + COLD) / 2
T250 = (250 - 32) * 5 / 9 + 273.15
T200 = (200 - 32) * 5 / 9 + 273.15

CHECKS = []
DERIVED = {}


def clean(v):
    if isinstance(v, (float, np.floating)):
        if not math.isfinite(v):
            return str(v)
        return float(v)
    if isinstance(v, dict):
        return {k: clean(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [clean(x) for x in v]
    if isinstance(v, np.bool_):
        return bool(v)
    if isinstance(v, np.integer):
        return int(v)
    return v


def check(path, claimed, derived, *, rtol=2e-9, atol=2e-10, kind="arithmetic"):
    if isinstance(claimed, bool) or isinstance(claimed, str) or claimed is None:
        ok = claimed == derived
        delta = None
    else:
        if not math.isfinite(claimed) or not math.isfinite(derived):
            ok = ((math.isnan(claimed) and math.isnan(derived)) or claimed == derived)
            delta = None
        else:
            delta = derived - claimed
            ok = abs(delta) <= atol + rtol * max(abs(derived), abs(claimed))
    CHECKS.append(dict(path=path, owner=clean(claimed), independent=clean(derived),
                       independent_minus_owner=delta, match=bool(ok), kind=kind,
                       relative_tolerance=rtol, absolute_tolerance=atol))


def compare(path, claimed, derived, **kw):
    for k, value in derived.items():
        if k not in claimed:
            continue
        if isinstance(value, dict):
            compare(path + "/" + k, claimed[k], value, **kw)
        else:
            check(path + "/" + k, claimed[k], value, **kw)


def joining(tf, tc, ratio=30, bond=AF):
    seam = A * (1 / (0.6096 - ratio * tf) + 1 / (1.8288 - ratio * tf))
    return 2*A*bond + seam*(2*tf*math.hypot(ratio, 1)*0.070 + 0.25*tc + 0.002)


def core_params(rho=RHO, gc=GC, ec=EC, crush=SW, cell=0.009525):
    return dict(rho=rho, gc=gc, ec=ec, crush=crush, cell=cell)


BASE = core_params()


def geometry(tf, core=BASE, ratio=30, bond=AF, ti=0):
    """Analytic piecewise mass balance, independent of owner's fraction solver.

    Two RTV layers are charged to physical joining. The inactive joint-allowance
    branch is also enforced. At all scored RTV points physical joining dominates.
    """
    seam = A*(1/(0.6096-ratio*tf) + 1/(1.8288-ratio*tf))
    face_mass = 2*A*RHOF*tf
    extra = 2*A*RHOSI*ti
    fixed_joint = 2*A*bond + seam*(2*tf*math.hypot(ratio, 1)*0.07 + 0.002) + extra
    tc_joint = (BUDGET-face_mass-fixed_joint)/(A*core["rho"]+0.25*seam)
    tc_floor = (BUDGET/1.05-face_mass)/(A*core["rho"])
    return min(tc_joint, tc_floor)


def evaluation(tf, tc, core=BASE, ratio=30, bond=AF, ti=0, dt=0, nu=NU):
    if tf <= 0 or tc <= 0:
        return None
    stress = P0*R/(4*tf)
    residual = KB*DA*dt*tc/(2*tf)
    local = stress + residual
    geff = tc/(tc/core["gc"] + 2*ti/GSI)
    h = tf + tc
    s0 = EF*h/(R*math.sqrt(1-nu**2))
    scr = geff*h*h/(2*tf*tc)
    vc = s0/scr
    kc = 1-vc/4 if vc <= 2 else 1/vc
    gn = stress/(kc*s0)
    gf = .2+.4*min(vc, 2)
    qn = local/(BETA*math.sqrt(EF*core["ec"]*tf/tc))
    if vc < 2:
        ug = math.log(gn/.2)/math.log(gf/.2)
    else:
        ug = 0 if gn <= 1 else math.inf
    uq = math.log(qn/.33)/math.log(.82/.33)
    other = dict(face_345=345e6/local, crimp=scr/stress,
                 crush=2*core["crush"]/P0,
                 dimpling=EF*(tf/core["cell"])**2/((1-nu*nu)*local),
                 scarf_screen=10e6*math.hypot(ratio, 1)**2/(ratio*local))
    s = A*(2*RHOF*tf+core["rho"]*tc)
    j = joining(tf, tc, ratio, bond)+2*A*RHOSI*ti
    raw = max(0, ug, uq)
    feasible = min(other.values()) >= 1-2e-10
    return dict(F=A*core["rho"]*tc/s, tf=tf, tc=tc, S=s, J=j, Vc=vc,
                gamma_need=gn, gamma_full=gf, Q_need=qn, u_gamma=ug,
                u_Q=uq, u_raw=raw, sigma_res_MPa=residual/1e6,
                others_min=min(other.values()), others=other,
                max_usage=raw if feasible else math.inf, feasible=feasible,
                mass_residual_kg=s+max(.05*s,j)+RESERVE+SYSTEMS-LIFT,
                full_min=min(*other.values(), 1/gn, .82/qn),
                stress_Pa=stress, core_shear_effective_Pa=geff)


def search(core=BASE, ratio=30, bond=AF, ti=0, dt=0, nu=NU):
    """Search face thickness using a grid plus every mode-boundary root.

    Bounded local refinement and equality roots are separate from JSON claims.
    A full classical-envelope max-min search also establishes rejection cases.
    """
    if 2*A*(bond+RHOSI*ti) >= BUDGET:
        return dict(feasible=False, reason="bond/interlayer mass alone exceeds budget",
                    minimum_interface_mass_kg=2*A*(bond+RHOSI*ti))
    args = dict(core=core, ratio=ratio, bond=bond, ti=ti, dt=dt, nu=nu)
    hi0 = min(BUDGET/(1.05*2*A*RHOF), .6096/ratio*.999)
    hi = brentq(lambda t: geometry(t, core, ratio, bond, ti), 0, hi0, xtol=1e-18)
    lo = hi*1e-8
    grid = np.unique(np.r_[np.geomspace(lo, hi*(1-1e-10), 2049),
                           np.linspace(lo, hi*(1-1e-10), 4097)])
    cache = {}

    def at(t):
        t = float(t)
        if t not in cache:
            cache[t] = evaluation(t, geometry(t, core, ratio, bond, ti), **args)
        return cache[t]

    pts = [at(t) for t in grid]
    candidates = list(grid)
    for mode in ["face_345", "crimp", "crush", "dimpling", "scarf_screen"]:
        vals = [p["others"][mode]-1 for p in pts]
        for a, b, va, vb in zip(grid[:-1],grid[1:],vals[:-1],vals[1:]):
            if va*vb < 0:
                candidates.append(brentq(lambda t: at(t)["others"][mode]-1,
                                         a,b,xtol=1e-18))
    # All nondifferentiable intersections of the two searched usages.
    vals = [p["u_gamma"]-p["u_Q"] for p in pts]
    for a,b,va,vb in zip(grid[:-1],grid[1:],vals[:-1],vals[1:]):
        if math.isfinite(va) and math.isfinite(vb) and va*vb < 0:
            candidates.append(brentq(lambda t: at(t)["u_gamma"]-at(t)["u_Q"],
                                     a,b,xtol=1e-18))
    for key, sign in [("u_raw", 1), ("full_min", -1)]:
        vals = [sign*p[key] for p in pts]
        for i in range(1,len(grid)-1):
            if math.isfinite(vals[i]) and vals[i] < vals[i-1] and vals[i] <= vals[i+1]:
                fit = minimize_scalar(lambda t: (sign*at(t)[key]
                                      if math.isfinite(at(t)[key]) else 1e100),
                                      bounds=(grid[i-1],grid[i+1]),method="bounded",
                                      options={"xatol":1e-17})
                candidates.append(fit.x)
    feasible = [at(t) for t in candidates if at(t)["feasible"]]
    best = min(feasible,key=lambda p:p["u_raw"]) if feasible else None
    maximum = max((at(t) for t in candidates), key=lambda p:p["full_min"])
    return dict(best=best, full_envelope_max=maximum, evaluated=len(cache),
                grid_points=len(grid), feasible=best is not None)


def thermal(dt, sft):
    eps = DA*dt
    lam = math.sqrt(GC/(EF*TF37*TC37))
    tau0 = eps*EF*TF37*lam
    tau_edge = 2*eps*math.sqrt(K2*GC)
    tau_l = 2*eps*math.sqrt(K2*GL)
    tau_double = tau_edge*math.sqrt(.9)
    sr = KB*eps*TC37/(2*TF37)
    pressure = P0*R/(4*TF37)
    total = pressure+sr
    h = TF37+TC37
    ef_full = 293.6e9
    scr = GC*h*h/(2*TF37*TC37)
    s0_full = ef_full*h/(R*math.sqrt(1-NU*NU))
    vc_full = s0_full/scr
    kc_full = 1-vc_full/4 if vc_full <= 2 else 1/vc_full
    modes = dict(global_buckling=(.2+.4*min(vc_full,2))*kc_full*s0_full/pressure,
                 face_compression=379.2e6/total,
                 core_shear_crimping=scr/pressure, core_crush=2*SW/P0,
                 face_wrinkling=BETA*.82*math.sqrt(ef_full*EC*TF37/TC37)/total,
                 intracell_dimpling=ef_full*(TF37/.009525)**2/((1-NU*NU)*total),
                 scarf_mean_shear=10e6*(30+1/30)/total)
    least=min(modes,key=modes.get)
    return dict(sft_K=sft,sft_C=sft-273.15,worst_dT_K=dt,
                tau_037_kPa=tau0/1000,SF_037_typ=SW/tau0,SF_037_min=SWMIN/tau0,
                tau_free_edge_kPa=tau_edge/1000,SF_edge_typ=SW/tau_edge,
                SF_edge_min=SWMIN/tau_edge,SF_edge_L_typ=SL/tau_l,
                SF_edge_L_min=SLMIN/tau_l,SF_edge_doubled_typ=SW/tau_double,
                SF_edge_doubled_min=SWMIN/tau_double,
                transfer_length_mm=TC37/2*math.sqrt(K2/GC)*1000,
                wall_stress_MPa=ES*eps/1e6,wall_SF_on_5052H39_yield=YS/(ES*eps),
                wall_stress_doubled_single_MPa=1.2*ES*eps/1e6,
                wall_SF_doubled_single=YS/(1.2*ES*eps),
                face_compression_added_037_MPa=sr/1e6,
                p2_037_modes_with_residual=modes,p2_037_least=least,
                p2_037_least_SF=modes[least],p2_037_face_SF_on_345=345e6/total)


def main():
    started=datetime.datetime.now().astimezone().isoformat()
    for k,v in dict(t_cold_K=COLD,t_hot_K=HOT,t_air_K=284.9,swing_K=SWING).items():
        check("compute/service/"+k,C["service"][k],v)
    check("compute/k_biax_al_MPa",C["k_biax_al_MPa"],KB/1e6)
    # Derivation using spring energies of a periodic three-bond honeycomb node:
    # uniform: all strains=e; doubled: single=1.2e, double=.6e.
    # Wall-volume weights single:double = 1:1, giving energy ratio
    # .5*(1.2**2+.6**2)=.9 and yield-force ratio .9/1.2=.75.
    compare("compute/doubled_wall_cell",C["doubled_wall_cell"],
            dict(k_biax_ratio=.5*(1.2**2+.6**2),single_wall_stress_ratio=1.2))
    residuals=[]
    temperatures=[T250,108+273.15,T200,80+273.15,70+273.15,25+273.15,MID]
    for i,t in enumerate(temperatures):
        dt=max(abs(t-COLD),abs(t-HOT))
        v=thermal(dt,t);residuals.append(v)
        compare(f"compute/residual/{i}",C["residual"][i],v)
    DERIVED["residual"]=residuals
    eq={}
    for name,dt in [("cure_250F",T250-COLD),("swing_037",SWING)]:
        force=EF*TF37*DA*dt
        yield_force=REL*YS*TC37/2
        v=dict(face_force_N_per_m=force,core_force_needed_N_per_m=2*force,
               core_force_at_wall_yield_N_per_m=yield_force,
               ratio=2*force/yield_force,ratio_doubled_cell=2*force/(.75*yield_force))
        eq[name]=v;compare("compute/screen_equilibrium/"+name,C["screen_equilibrium"][name],v)
    DERIVED["screen_equilibrium"]=eq
    rigid_per_K=DA*math.sqrt(EF*TF37*GC/TC37)
    edge_per_K=2*DA*math.sqrt(K2*GC)
    windows={}
    for name,allow,coef in [("037_screen",SW,rigid_per_K),
                             ("037_screen_min",SWMIN,rigid_per_K),
                             ("free_edge_typ",SW,edge_per_K),
                             ("free_edge_min",SWMIN,edge_per_K)]:
        allowed=allow/coef
        v=dict(allowed_dT_K=allowed,lo_K=HOT-allowed,hi_K=COLD+allowed)
        windows[name]=v
        if name in C["sft_window"]:compare("compute/sft_window/"+name,C["sft_window"][name],v)
    DERIVED["windows"]=windows
    threshold=COLD+(10e6*(30+1/30)-P0*R/(4*TF37))/(KB*DA*TC37/(2*TF37))-273.15
    DERIVED["037_scarf_ceiling_C"]=threshold
    verdict=json.loads((ROOT/"owner/RESULTS.json").read_text())["verdict"]
    check("verdict/stress_free_ceiling_037_scarf_C",verdict["stress_free_ceiling_037_scarf_C"],threshold)
    basic=[math.sqrt(GC/(EF*TF37*TC37)),rigid_per_K*(HOT-284.9),
           rigid_per_K*SWING,SW/(rigid_per_K*SWING)]
    for i,v in enumerate(basic):
        check(f"compute/checks/{i}/mine",C["checks"][i]["mine"],v)
        check(f"compute/checks/{i}/theirs",C["checks"][i]["theirs"],v)
    baseline=search()["best"]
    DERIVED["baseline"]=baseline
    compare("compute/baseline_usage",C["baseline_usage"],baseline)
    vals=[baseline["max_usage"],baseline["gamma_need"],baseline["Q_need"],
          1000*baseline["tf"],1000*baseline["tc"],search(nu=.33)["best"]["max_usage"]]
    for i,v in enumerate(vals,4):
        check(f"compute/checks/{i}/mine",C["checks"][i]["mine"],v)
        check(f"compute/checks/{i}/theirs",C["checks"][i]["theirs"],v,
              atol=.0000005 if i!=8 else .00005,kind="rounded predecessor comparison")
    ratios=[]
    for i,t in enumerate([T250,T200]):
        sr=KB*DA*(t-COLD)*baseline["tc"]/(2*baseline["tf"])
        cap=(P0*R/(4*baseline["tf"])+sr)/10e6
        ratio=(cap+math.sqrt(cap*cap-4))/2
        dj=joining(baseline["tf"],baseline["tc"],ratio)-joining(baseline["tf"],baseline["tc"])
        ratios.append(ratio)
        compare(f"compute/scarf_fix/{i}",C["scarf_fix"][i],
                dict(r_need=ratio,sigma_res_lead_MPa=sr/1e6,dJ_kg=dj))
    needed=GSI*((DA*(T250-COLD))**2*EF*TF37/SW**2-TC37/GC)
    check("compute/interlayer_needed_um/037_screen",C["interlayer_needed_um"]["037_screen"],needed*1e6)
    check("compute/interlayer_needed_um/free_edge",C["interlayer_needed_um"]["free_edge"],0,atol=1e-12)
    # Cases are explicitly derived from published product inputs, not executable.
    cases=[
        dict(dt=T250-COLD),dict(dt=T200-COLD),dict(dt=80+273.15-COLD,bond=.25),
        dict(dt=25+273.15-COLD),dict(dt=MID-COLD),
        dict(dt=T250-COLD,ratio=ratios[0]),dict(dt=T200-COLD,ratio=ratios[1]),
        dict(dt=T250-COLD,ti=25e-6),dict(dt=T250-COLD,ti=100e-6),
        dict(dt=T250-COLD,ti=needed),
        dict(core=core_params(32.04,34.474e6,117.21e6,1172.1e3,.0047625)),
        dict(core=core_params(51.26,34.474e6,262e6,2689e3,.009525)),
        dict(core=core_params(33.64,8.9632e6,172.37e6,896.32e3,.00635)),
        dict(core=core_params(24.03,10.342e6,41.369e6,723.95e3,.009525)),
        dict(core=core_params(72,1e12,1e12,1e9,.001)),
        dict(core=core_params(81.694,1e12,1e12,1e9,.001)),
        dict(core=core_params(84.898,1e12,1e12,1e9,.001)),
    ]
    searches=[]
    for i,args in enumerate(cases):
        owner=C["fixes"][i]
        outcome=search(**args)
        nores=search(**{**args,"dt":0})
        row=dict(index=i,name=owner["fix"],inputs=args,search=outcome,without_residual=nores)
        searches.append(row)
        # Evaluating every published geometry checks numerical diagnostics even
        # where the search explicitly returned no feasible design.
        for prefix,claim,kwargs in [
            ("",owner,args),("/without_residual",owner["without_residual"],{**args,"dt":0})]:
            tf,tc=claim["tf_mm"]/1000,claim["tc_mm"]/1000
            p=evaluation(tf,tc,**kwargs) if tf>0 and tc>0 else None
            if p:
                compare(f"compute/fixes/{i}"+prefix,claim,p)
                check(f"compute/fixes/{i}{prefix}/mass_balance",0,p["mass_residual_kg"],atol=1e-7)
                check(f"compute/fixes/{i}{prefix}/tc_closed_mass",tc,
                      geometry(tf,kwargs.get("core",BASE),kwargs.get("ratio",30),
                               kwargs.get("bond",AF),kwargs.get("ti",0)),atol=1e-12)
        for prefix,claim,found in [("",owner,outcome),("/without_residual",owner["without_residual"],nores)]:
            if found.get("best"):
                best=found["best"]
                small={k:best[k] for k in ["max_usage","gamma_need","gamma_full","Q_need","sigma_res_MPa"]}
                small.update(tf_mm=best["tf"]*1000,tc_mm=best["tc"]*1000)
                compare(f"search/fixes/{i}"+prefix,claim,small,rtol=3e-7,atol=2e-8,kind="independent search")
        # Fixed-geometry mass deltas are explanatory and are not double-charged.
        if i in [5,6]:
            dm=joining(baseline["tf"],baseline["tc"],args["ratio"])-baseline["J"]
        elif i==2:
            dm=2*A*(.25-AF)
        elif 7<=i<=9:
            dm=2*A*RHOSI*args["ti"]
        elif i>=10:
            dm=A*baseline["tc"]*(args["core"]["rho"]-RHO)
        else:
            dm=0
        check(f"compute/fixes/{i}/mass_change_kg",owner["mass_change_kg"],dm)
        row["mass_change_at_original_lead_kg"]=dm
        if i<10:
            dt=args["dt"];ti=args.get("ti",0)
            tau=DA*dt*math.sqrt(EF*TF37/(TC37/GC+ti/GSI))
            ge_edge=TC37/(TC37/GC+2*ti/GSI)
            te=2*DA*dt*math.sqrt(K2*ge_edge)
            check(f"compute/fixes/{i}/SF_037",owner["SF_037"],SW/tau)
            check(f"compute/fixes/{i}/SF_free_edge",owner["SF_free_edge"],SW/te)
        elif i<14:
            cte=[14.76e-6,14.76e-6,4.86e-6,34.92e-6][i-10]
            allow=[413.69e3,758.42e3,275.79e3,241.32e3][i-10]
            tau=abs(cte-ALPHA_F)*(T250-COLD)*math.sqrt(EF*TF37*args["core"]["gc"]/TC37)
            check(f"compute/fixes/{i}/SF_037",owner["SF_037"],allow/tau)
        print("case",i,"u",outcome.get("best",{}).get("u_raw") if outcome.get("best") else "none",
              "classical max",outcome.get("full_envelope_max",{}).get("full_min"),flush=True)
    DERIVED["fix_searches"]=searches
    DERIVED["constants"]=dict(A=A,pressure=P0,lift=LIFT,face_thickness_037=TF37,
                              core_thickness_037=TC37,core_relative_density=REL,
                              k_biax_Pa=KB,k_transverse_constrained_Pa=K2,
                              beta=BETA,psi_Pa=PSI,AF_kg_per_m2=AF,
                              rigid_tau_Pa_per_K=rigid_per_K,edge_tau_Pa_per_K=edge_per_K,
                              inplane_bending_Young_Pa=1.5*ES*REL**3,
                              scarf_ratios=ratios,interlayer_rigid_required_m=needed)
    # Product-mass correction with an independent rerun.
    support_mass=2*A*.030
    DERIVED["hexbond_support_correction"]=dict(
        missing_mass_kg=support_mass,corrected_increment_kg=2*A*(.280-AF),
        corrected_search=search(bond=.280,dt=80+273.15-COLD))
    # Full finite face/core compatibility, as a sensitivity to the rigid-face
    # limit. This is independent analysis, not a claimed exact local-edge model.
    finite=[]
    for name,tf,tc in [("037",TF37,TC37),("028b",baseline["tf"],baseline["tc"])]:
        compliance_ratio=KB*tc/(2*EF*tf/(1-NU))
        eps=DA*(T250-COLD)/(1+compliance_ratio)
        finite.append(dict(geometry=name,core_to_faces_biaxial_rigidity=compliance_ratio,
                           wall_stress_MPa=ES*eps/1e6,
                           face_residual_MPa=KB*eps*tc/(2*tf)/1e6,
                           wall_force_per_width_N_m=KB*eps*tc))
    DERIVED["finite_face_compatibility"]=finite
    DERIVED["started_at"]=started
    DERIVED["ended_at"]=datetime.datetime.now().astimezone().isoformat()
    (ROOT/"DERIVED.json").write_text(json.dumps(clean(DERIVED),indent=2,allow_nan=False)+"\n")
    (ROOT/"ARITHMETIC.json").write_text(json.dumps(CHECKS,indent=2,allow_nan=False)+"\n")
    mismatches=[r for r in CHECKS if not r["match"]]
    (ROOT/"MISMATCHES.json").write_text(json.dumps(mismatches,indent=2,allow_nan=False)+"\n")
    print(json.dumps(dict(checks=len(CHECKS),matches=len(CHECKS)-len(mismatches),
                          mismatches=len(mismatches)),indent=2))


if __name__ == "__main__":
    main()
