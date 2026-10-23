"""Independent CHECK-039 reconstruction from filed dimensions, not owner code.

All material values and empirical transfers remain conditional. The scalar
two-group model here reproduces the declared model; it is not a validated hull
model. See METHOD.md and SOURCE-CHECK.md for physical limitations.
"""
import json
import math
from pathlib import Path
from scipy.optimize import brentq

OUT = Path(__file__).resolve().parent
OWNER = Path("unpublished-local-ref:c8462fc7c556096e")
R, P, LIFT, RESERVE = 10., 95460.83791390515, 4889.442150186961, 411.2989440716474
AREA = 4 * math.pi * R**2
E, NU, RHO = 290e9, .0752, 1850.
GC, EC, RC = 46884349.59354485, 103421359.3975254, 16.018463373960138
CRUSH, CELL = 241316.50526089262, .009525
BOND = .015 * .45359237 / .3048**2
BIAX = brentq(lambda b: b**3 + b - 1, 0, 1, xtol=1e-15)
PT, PF = 1 / 1.238, 1 / 1.0285
SCARF = 10e6 * 901 / 30


def skin_join(f, c):
    length = AREA * (1 / (.6096 - 30*f) + 1 / (1.8288 - 30*f))
    return dict(bond=2*AREA*BOND,
                scarf_film=length*2*f*math.sqrt(901)*.07,
                core_splice=length*c*.0005*500,
                seal=length*.002, seam_m=length)


def model(concept, a, f, c, ml=0., shape=None, gsmin=10.):
    """Geometric inputs in metres and kg. Reconstruct all derived quantities."""
    h = f+c
    nt = P*R/2
    af = E*f/(1-NU**2)
    ds0 = af*h*h/2
    s0 = GC*h*h/c
    sigma0 = E*h/(R*math.sqrt(1-NU**2))
    scrimp = s0/(2*f)
    vc = sigma0/scrimp
    kc = 1-vc/4 if vc < 2 else 1/vc
    nsph = 2*f*sigma0*kc
    al, ae, ei, zc, ell = 0., 0., 0., 0., 0.
    el, rho = (410e9, 3100.) if concept == "C2" else (E, RHO)
    section = {}
    if concept != "baseline":
        ell = AREA*2*math.sqrt(3)/a
        ae = ml/(rho*ell)
        if concept == "C1":
            foot = .025*.0005
            b = math.sqrt((ae-foot)/shape)
            d = shape*b
            zc = (foot*.00025+b*d*(.0005+d/2))/ae
            ei = .025*.0005**3/12+foot*(.00025-zc)**2+b*d**3/12+b*d*(.0005+d/2-zc)**2
            section = dict(A=ae, I=ei, zc=zc, b=b, d=d, kind="tee", shape_param=shape)
        else:
            ro = math.sqrt(ae/(math.pi*(2/shape-1/shape**2)))
            wall = ro/shape
            ei = math.pi/4*(ro**4-(ro-wall)**4)
            zc = ro
            section = dict(A=ae, I=ei, zc=zc, ro=ro, t=wall, kind="tube", shape_param=shape)
        al = .75*math.sqrt(3)*el*ae/a

    # In-plane isogrid homogenization: Q12=Q11/3; biaxial lattice EA=4Q11/3.
    a11, a12 = 2*af+al, 2*NU*af+al/3
    ebar = a11-a12*a12/a11
    eps = nt/(a11+a12)
    fr = (4*al/3)/(a11+a12)
    sfmem = E/(1-NU)*eps
    mismatch = (11.3e-6-4.02e-6)*25.1 if concept == "C2" else 0.
    thface = E/(1-NU)*fr*mismatch
    srib = el*(eps+(1-fr)*mismatch) if ae else 0.
    fmember = el*eps*ae

    # Inner group centroid relative to sandwich midplane, outer face at h/2.
    inner = af+al
    zin = (-af*h/2-al*(h/2+f/2+zc))/inner
    distance = h/2-zin
    di = (0.75*math.sqrt(3)*el*ei/a if a else 0.) + af*al/inner*(f/2+zc)**2
    dsep = af*inner/(af+inner)*distance**2
    dtot = di+dsep
    shear = GC*distance**2/c
    curv = ebar/R**2
    # In x=k², the stationarity equation is monotone after multiplying by x².
    if di == 0 and vc >= 2:
        x = math.inf
        ng, lg = shear, 0.
    else:
        logx = brentq(lambda q: di*math.exp(2*q)
                     +dsep*(math.exp(q)/(1+dsep*math.exp(q)/shear))**2-curv,
                     -40, 40, xtol=1e-13)
        x = math.exp(logx)
        ng = di*x+dsep*x/(1+dsep*x/shear)+curv/x
        lg = 2*math.pi/math.sqrt(x)
    xr = min(x, (math.pi/a)**2) if a else x
    ngr = di*xr+dsep*xr/(1+dsep*xr/shear)+curv/xr if math.isfinite(xr) else shear
    lgr = 2*math.pi/math.sqrt(xr) if math.isfinite(xr) else 0.
    psi = dtot/ds0
    gs = (psi-1)/(3*math.sqrt(3)/4)
    adequate = bool(a and gs >= gsmin)
    heavy = psi >= 28
    ns = (1-fr)*nt
    qb = fr*P
    sbend = (1+NU)*qb*a*a/(72*f*h) if a else 0.
    stress = sfmem+thface+sbend
    qline = fmember/R
    width = .025 if concept == "C1" else .03
    crushline = (1-fr)*P/2+qline/(width+2*h) if a else P/2
    tauline = qline/(2*h)
    gfull = .2+.4*min(vc, 2)
    if heavy:
        gfull = max(gfull, .377/.6125 if concept == "C1" else .702)
    g_today = .425 if heavy else .2
    p_today, p_full, po_today, po_full = PT, PF, PT, PF
    cap = False
    values = dict(concept=concept, a_m=a, shape=shape, tf_mm=f*1000, tc_mm=c*1000,
                  lattice_kg=ml, sig_face_MPa=stress/1e6, heavy=heavy, Vc=vc, Kc=kc,
                  psi=psi, teq=math.sqrt(12*dtot/ebar), lam_g=lg, lam_gr=lgr,
                  fr=fr, sig_f=sfmem, sig_r=srib, th_face=thface, eps=eps,
                  Ng=ng, Ngr=ngr, Nsph_skin=nsph, Ns=ns, sig_b=sbend,
                  crush_line=crushline, tau_line=tauline, adequate=adequate, gamma_s=gs)
    base = dict(global_unrestricted=ng/nt, face_per_Pa=1/stress,
                wrinkle_per_Q=BIAX*math.sqrt(E*EC*f/c)/stress,
                crimp=scrimp/stress, dimple=E*(f/CELL)**2/(1-NU**2)/stress,
                crush_uniform=CRUSH/((1+fr)*P/2), crush_rib_line=CRUSH/crushline,
                scarf_screen=SCARF/stress)
    base["global"] = ngr/nt
    if a:
        # Equal-area circular cap, shallow-angle lambda; this mapping is a projection.
        lp = (12*(1-NU**2))**.25*a*math.sqrt(math.sqrt(3)/(4*math.pi))/math.sqrt(R*math.sqrt(3)*h)
        xp = 16*math.pi**2/(3*a*a)
        nplate = ds0*xp/(1+ds0*xp/s0)
        npanel = max(nsph, nplate)
        cap = lp > 2
        if adequate:
            base["panel"] = npanel/ns
            if cap:
                p_today, p_full = .2, .2+.4*min(vc,2)
                po_today, po_full = min(PT, .14+3.2/lp**2), PF
        else:
            base["panel"] = nsph/ns if lp > 1.165 else 1e9
            p_today = po_today = .2
            p_full = po_full = .2+.4*min(vc,2)
        base["core_shear_rib_line"] = CRUSH/tauline if tauline else 1e9
        if concept == "C1":
            base["rib_crippling"] = .43*math.pi**2*E/(12*(1-NU**2))*(section["b"]/section["d"])**2/srib
            join = dict(rib_bond_film=ell*.025*BOND, rib_splices_nodes_5pct=.05*ml)
        else:
            gamma = 1-.901*(1-math.exp(-math.sqrt(shape)/16))
            base["tube_local"] = .6*el/shape*gamma/srib
            section["F"] = fmember
            # Paste density is inferred from the filed mass; absent in INPUTS.json.
            join = dict(frame_bond=ell*(.03*BOND+2*.5*.005**2*1250),
                        sleeves_023_scaled=157.7*fmember/562200, nodes_026=362*.02)
            if concept == "C2":
                base["sic_compression"] = 3.9e9/srib
        if concept != "C2":
            base["rib_per_Pa"] = 1/srib
        values.update(lam_panel=lp, N_plate=nplate, N_panel_cl=npanel,
                      q_line=qline, section=section, lattice_joining_parts=join)
    else:
        join = {}
    jp = skin_join(f, c)
    skinmass = sum(v for k,v in jp.items() if k != "seam_m")
    mf, mc = 2*AREA*f*RHO, AREA*c*RC
    s = mf+mc+ml
    physical = skinmass+sum(join.values())
    charged = max(physical, .05*s)
    masses = dict(faces=mf, core=mc, lattice=ml, skin_joining=skinmass,
                  skin_joining_parts=jp, lattice_joining=sum(join.values()),
                  joining_physical=physical, joint_allowance_5pct=.05*s,
                  joint_charged=charged, joint_excess=max(0,physical-.05*s),
                  systems=100., reserve_019_fixed=RESERVE,
                  total=s+charged+100+RESERVE)
    values.update(S_kg=s, f_lattice=ml/s, f_core=mc/(mf+mc), masses=masses, base=base,
                  today_full=dict(gamma_g=[g_today,gfull], gamma_p=[p_today,p_full],
                                  gamma_p_O5=[po_today,po_full], Q=[.33,.82],
                                  sigma=[345e6,379.2e6]), cap_regime=cap)
    return values


def score(v, seam=True, o5=False, over=None):
    b, t = v["base"], v["today_full"]
    over = over or {}
    sf = dict(global_=b["global"]*over.get("gamma_g",t["gamma_g"][0]),
              face=b["face_per_Pa"]*over.get("sigma",345e6),
              wrinkle=b["wrinkle_per_Q"]*over.get("Q",.33))
    sf["global"] = sf.pop("global_")
    if "panel" in b:
        gamma = t["gamma_p_O5" if o5 else "gamma_p"][0]
        if v["cap_regime"] or not v["adequate"]:
            gamma = over.get("panel_cap_sphere",gamma)
        sf["panel"] = b["panel"]*gamma
    if "rib_per_Pa" in b:
        sf["rib_yield"] = b["rib_per_Pa"]*over.get("sigma",345e6)
    for k,val in b.items():
        if k not in ["global","global_unrestricted","face_per_Pa","wrinkle_per_Q","panel","rib_per_Pa"]:
            if k != "scarf_screen" or seam:
                sf[k] = val
    return sf


def needs(v, subset):
    b, t = v["base"], v["today_full"]
    if "O5_frame_bay" in subset:
        t = dict(t, gamma_p=t["gamma_p_O5"])
    n = dict(gamma_g=1/b["global"],Q=1/b["wrinkle_per_Q"],
             sigma=max(1/b["face_per_Pa"],1/b["rib_per_Pa"] if "rib_per_Pa" in b else 0))
    if "panel" in b:
        n["gamma_p"] = 1/b["panel"]
    today = {k:t[k][0] for k in n}
    factors = {k:n[k]/today[k] for k in n}
    usage = max([0.]+[math.log(max(1,factors[k]))/math.log(t[k][1]/t[k][0])
                        for k in subset if k in n])
    return dict(needed=n, today_at_point=today, needed_over_today=factors, max_usage=usage)


def detailed_points(x, path=""):
    if isinstance(x,dict):
        if all(k in x for k in ["tf_mm","tc_mm","masses","base"]):
            yield path,x
        else:
            for k,v in x.items():
                yield from detailed_points(v,path+"/"+str(k))
    elif isinstance(x,list):
        for i,v in enumerate(x):
            yield from detailed_points(v,path+"/"+str(i))


def leaves(x,path=""):
    if isinstance(x,dict):
        for k,v in x.items():
            yield from leaves(v,path+"/"+str(k))
    elif isinstance(x,list):
        for i,v in enumerate(x):
            yield from leaves(v,path+"/"+str(i))
    else:
        yield path,x


def main():
    records, points, mismatches, unavailable = [], [], [], []
    unique = set()
    for fn, gs in [("RUNS.json",10.),("RUNS-gs5.json",5.)]:
        data=json.loads((OWNER/fn).read_text())
        for path,x in detailed_points(data):
            y=model(x["concept"],x["a_m"],x["tf_mm"]/1000,x["tc_mm"]/1000,
                    x["lattice_kg"],x.get("shape"),gs)
            if "SF" in x:
                y["SF"]=score(y,x.get("seam_screen",True),x.get("O5_frame_bay",False),x.get("over"))
                y["least_SF"]=min(y["SF"].values())
                y["governs"]=min(y["SF"],key=y["SF"].get)
            if "needed" in x:
                y.update(needs(y,x["subset"]))
            key=(gs,x["concept"],x["a_m"],x["tf_mm"],x["tc_mm"],x["lattice_kg"],x.get("shape"))
            unique.add(key)
            yd=dict(leaves(y))
            count=0
            for p,val in leaves(x):
                if isinstance(val,(int,float)) and not isinstance(val,bool):
                    if p in yd:
                        calc=yd[p]
                        # Wavelength outputs are bounded-optimizer coordinates, not exact roots.
                        tol=2e-6 if p in ["/lam_g","/lam_gr"] else 2e-9
                        delta=calc-val
                        ok=abs(delta)<=max(1e-10,tol*max(abs(val),abs(calc)))
                        row=dict(file=fn,path=path+p,filed=val,independent=calc,
                                 delta=delta,relative=delta/max(abs(val),1e-300),ok=ok)
                        records.append(row);count+=1
                        if not ok:mismatches.append(row)
                    elif p.split("/")[1] not in ["over","subset"]:
                        unavailable.append(dict(file=fn,path=path+p,value=val))
            points.append(dict(file=fn,path=path,comparison_count=count,independent=y))
    output=dict(method="Independent geometric/arithmetic reconstruction; no owner code read or run.",
                numeric_comparisons=len(records),point_records=len(points),unique_geometries=len(unique),
                mismatches=mismatches,uncovered_numeric_fields=unavailable,comparisons=records)
    (OUT/"ARITHMETIC.json").write_text(json.dumps(output,indent=2)+"\n")
    (OUT/"RECALCULATED.json").write_text(json.dumps(points,indent=2)+"\n")
    print(json.dumps({k:v for k,v in output.items() if k!="comparisons"},indent=2))


def extended():
    checks, missing, reconstructions = [], [], []
    geometry = {}
    datasets = {fn:json.loads((OWNER/fn).read_text())
                for fn in ["RUNS.json","RUNS-gs5.json","RESULTS.json"]}
    for fn,d in datasets.items():
        for ci,c in enumerate(d["concepts"]):
            for path,x in detailed_points(c):
                key=(ci,x["tf_mm"],x["tc_mm"],x["lattice_kg"],x["psi"])
                geometry[key]=x.get("shape")
            for cat,entry in c["lift_shift_kg"].items():
                if isinstance(entry,dict) and isinstance(entry.get("design"),dict):
                    x=entry["design"]
                    geometry[(ci,x["tf_mm"],x["tc_mm"],x["lattice_kg"],x["psi"])]=(x.get("section") or {}).get("shape_param")

    def compare(path,x,y,round_sf=False):
        yd=dict(leaves(y))
        for p,v in leaves(x):
            if isinstance(v,(int,float)) and not isinstance(v,bool):
                if p in yd:
                    w=yd[p]
                    tol=5.1e-7 if round_sf and p.startswith("/SF/") else max(1e-10,2e-9*max(abs(v),abs(w)))
                    if p in ["/lam_g","/lam_gr"]:tol=max(tol,2e-6*abs(v))
                    checks.append(dict(path=path+p,filed=v,independent=w,delta=w-v,ok=abs(w-v)<=tol))
                elif p.split("/")[1] not in ["over"]:
                    missing.append(dict(path=path+p,value=v))

    for fn,d in datasets.items():
        for ci,c in enumerate(d["concepts"]):
            roots=[("",c,5. if fn=="RUNS-gs5.json" else 10.)]
            if "gs5" in c: roots.append(("/gs5",c["gs5"],5.))
            for suffix,root,gs in roots:
                for cat,entry in root.get("lift_shift_kg",{}).items():
                    if not isinstance(entry,dict) or not isinstance(entry.get("design"),dict):continue
                    x=entry["design"];shape=(x.get("section") or {}).get("shape_param")
                    y=model(c["concept"],c["a_m"],x["tf_mm"]/1000,x["tc_mm"]/1000,x["lattice_kg"],shape,gs)
                    over=dict(gamma_g=.564164,Q=.434628,panel_cap_sphere=.564164) if cat=="at_028b_values" else None
                    y["SF"]=score(y,cat!="today_six_modes",cat=="today_O5",over)
                    y["least_SF"]=min(y["SF"].values())
                    path=f"{fn}/concepts/{ci}{suffix}/lift_shift_kg/{cat}"
                    compare(path+"/design",x,y)
                    compare(path,dict(shift_kg=entry["shift_kg"]),dict(shift_kg=y["masses"]["total"]-LIFT))
                    reconstructions.append(dict(path=path,independent=y))
                for cat in ["sets_seam","sets_six_modes"]:
                    for j,x in enumerate(root.get(cat,[])):
                        key=(ci,x["tf_mm"],x["tc_mm"],x["lattice_kg"],x["psi"])
                        shape=geometry.get(key)
                        shape_origin="matching full geometry"
                        if shape is None and c["concept"]!="baseline":
                            # Compact records omit shape. Recover it from psi, disclose this dependency.
                            shape_origin="inferred from filed psi; psi is input, not independent check"
                            def residual(sh):
                                return model(c["concept"],c["a_m"],x["tf_mm"]/1000,
                                             x["tc_mm"]/1000,x["lattice_kg"],sh,gs)["psi"]-x["psi"]
                            lo,hi=(3.,20.) if c["concept"]=="C1" else (30.,300.)
                            shape=lo if abs(residual(lo))<1e-10 else hi if abs(residual(hi))<1e-10 else brentq(residual,lo,hi)
                        y=model(c["concept"],c["a_m"],x["tf_mm"]/1000,x["tc_mm"]/1000,x["lattice_kg"],shape,gs)
                        y.update(needs(y,x["subset"]))
                        path=f"{fn}/concepts/{ci}{suffix}/{cat}/{j}"
                        if shape_origin.startswith("inferred"):
                            y.pop("psi")
                        compare(path,x,y)
                        reconstructions.append(dict(path=path,shape=shape,shape_origin=shape_origin,independent=y))
                if fn=="RESULTS.json":
                    for cat in ["best_today","best_today_six_modes","best_at_028b_values","best_today_O5","least_set_seam","least_set_six_modes"]:
                        x=root.get(cat)
                        if not isinstance(x,dict):continue
                        shape=x.get("shape",(x.get("section") or {}).get("shape_param"))
                        if shape is None:shape=geometry.get((ci,x["tf_mm"],x["tc_mm"],x["lattice_kg"],x["psi"]))
                        y=model(c["concept"],c["a_m"],x["tf_mm"]/1000,x["tc_mm"]/1000,x["lattice_kg"],shape,gs)
                        over=dict(gamma_g=.564164,Q=.434628,panel_cap_sphere=.564164) if cat=="best_at_028b_values" else None
                        y["SF"]=score(y,x.get("seam_screen",True),x.get("O5_frame_bay",False),over)
                        y["least_SF"]=min(y["SF"].values())
                        y["sig_r_MPa"]=y["sig_r"]/1e6
                        y["today_endpoints"]={k:v[0] for k,v in y["today_full"].items()}
                        if "needed" in x:y.update(needs(y,x["subset"]))
                        compare(f"{fn}/concepts/{ci}{suffix}/{cat}",x,y,True)
    summary=dict(comparisons=len(checks),mismatches=[x for x in checks if not x["ok"]],
                 unreconstructed_fields=missing)
    (OUT/"EXTENDED-ARITHMETIC.json").write_text(json.dumps(dict(summary=summary,checks=checks,reconstructions=reconstructions),indent=2)+"\n")
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
    extended()
