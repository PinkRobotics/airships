"""Final core-field audit, run only inside the admitted postprocessing job."""
import csv,json,math
from core_collect import collect_core
from core_refine import core_at
from data_tools import ROOT,P0,summary,path
def read(name):return json.loads((ROOT/name).read_text())
def process(check):
    groups=read("CORE-BOUNDARIES.json");assert len(groups)==8
    cold=read("CORE-THERMAL.json");cal=read("CORE-CALIBRATION.json")
    sweep=read("CORE-SWEEP.json");assert len(sweep)==24
    passing_names={b["passing_run"] for g in groups+[cold] for b in g["boundaries"]}
    core_records={}
    for file in sorted((ROOT/"runs").glob("*/MODEL.json")):
        model=json.loads(file.read_text())
        if model.get("args",{}).get("core_output"):
            cached=file.parent/"CORE-SUMMARY.json"
            c=json.loads(cached.read_text()) if cached.exists() else None
            needs_bound=model["name"] in passing_names or model["name"].startswith("core-control-")
            needs_peak=model["name"]=="core-control-inherited"
            if (c is None or (needs_bound and "min_acoustic_lower_bound_MPa" not in c["endpoint"]) or
                (needs_peak and "peak_E11" not in c["endpoint"])):
                c=collect_core(file.parent)
            core_records[c["name"]]=c
            check("core-native-tensor-invariants:"+c["name"],c["max_invariant_error_MPa"]<2e-5,
                  dict(max_trace_or_frobenius_error_MPa=c["max_invariant_error_MPa"],
                       full_3d_outplane_strain=c["max_outplane_strain"]))
    governing={}
    for sf in [1.,1.05]:
        governing[str(sf)]=min((dict(label=g["label"],meridian=g["meridian"],width_mm=g["width_mm"],**b)
            for g in groups for b in g["boundaries"]
            if b["SF"]==sf and b["strength_basis"]=="minimum_average"),
            key=lambda b:b["amplitude_estimate_mm"])
    min_acoustic=math.inf;max_crush=0.
    for g in groups+[cold]:
        for b in g["boundaries"]:
            for side in ["passing","failing"]:
                n=b[side+"_run"];target=b["pressure_kPa"]
                core=core_at(n,target)
                faces=[r for r in path(n) if r["p_kPa"]<=target+1e-4]
                native=list(csv.DictReader((ROOT/"runs"/n/"CORE-PATH.csv").open()))
                native=[{k:float(v) for k,v in row.items() if v!=""} for row in native
                        if float(row["p_kPa"])<=target+1e-4]
                index=max(row[b["strength_basis"]+"_index"] for row in native)
                face=max(r["max_mises_MPa"] for r in faces)
                passed=face<=b["face_yield_MPa"] and index<=1
                check("core-final-boundary:"+str(b["face_yield_MPa"])+g["label"]+g["meridian"]+
                      str(b["SF"])+b["strength_basis"]+side,
                      core is not None and passed==(side=="passing"),
                      dict(run=n,face_MPa=face,core_index=index,target_kPa=target))
                if side=="passing":
                    bound=min(row["min_acoustic_lower_bound_MPa"] for row in native)
                    crush=max(row["max_core_compression_MPa"] for row in native)
                    min_acoustic=min(min_acoustic,bound);max_crush=max(max_crush,crush)
                    check("core-local-ellipticity:"+n,bound>0,
                          dict(sufficient_lower_bound_MPa=bound,
                               scope="all saved core points and increments through target; not global stability"))
    check("passing-core-typical-crush-screen",max_crush<35*.006894757293168361,
          dict(maximum_passing_compression_MPa=max_crush,
               catalog_typical_crush_MPa=35*.006894757293168361,
               scope="Comparison only; catalog typical strength is not an installed allowable."))
    confirmations=read("CORE-CHECKS.json")
    acoustic_probe=None
    for c in confirmations:
        check("core-confirmation:"+c["run"],c["passed"],c)
        if c["kind"].startswith("control_"):
            r=core_records[c["run"]]
            c["acoustic_lower_bound_MPa"]=r["endpoint"]["min_acoustic_lower_bound_MPa"]
            ref=summary(c["reference"])
            target=summary(c["run"])["endpoint_kPa"]
            ref_face=next(row["max_mises_MPa"] for row in path(ref["name"])
                          if abs(row["p_kPa"]-target)<1e-4)
            ref_core=core_at(c["reference"],target)
            c["face_difference_MPa"]=c["face_MPa"]-ref_face
            c["core_shear_difference_MPa"]=c["core_shear_MPa"]-ref_core["max_core_shear_MPa"]
            if c["kind"] in ["control_angular","control_layers"]:
                check("regularized-refined-control-passes:"+c["run"],
                      c["face_MPa"]<=345 and c["core_index"]<=1
                      and c["acoustic_lower_bound_MPa"]>0,c)
            if c["kind"]=="control_inherited":
                import numpy as np
                e=r["endpoint"];m=json.loads((ROOT/"runs"/c["run"]/"MODEL.json").read_text())
                E=np.array([[e["peak_E11"],e["peak_E12"],e["peak_E13"]],
                    [e["peak_E12"],e["peak_E22"],e["peak_E23"]],
                    [e["peak_E13"],e["peak_E23"],e["peak_E33"]]])
                E1,E2,E3=m["E_inplane_MPa"],m["E_core_MPa"],m["E_inplane_MPa"]
                G12,G13,G23=m["G_meridian_MPa"],m["G_inplane_MPa"],m["G_hoop_MPa"]
                S=E*np.array([[E1,2*G12,2*G13],[2*G12,E2,2*G23],[2*G13,2*G23,E3]])
                F=np.linalg.cholesky(np.eye(3)+2*E).T
                best=None
                directions=[np.array([np.sin(p)*np.cos(a),np.sin(p)*np.sin(a),np.cos(p)])
                    for p in np.linspace(0,np.pi,37) for a in np.linspace(0,2*np.pi,144,endpoint=False)]
                directions += [np.array([np.cos(a),np.sin(a),0.]) for a in np.linspace(0,np.pi,7201)]
                for n in directions:
                    x,y,z=n
                    A=np.array([[E1*x*x+G12*y*y+G13*z*z,G12*x*y,G13*x*z],
                        [G12*x*y,G12*x*x+E2*y*y+G23*z*z,G23*y*z],
                        [G13*x*z,G23*y*z,G13*x*x+G23*y*y+E3*z*z]])
                    Q=F@[address]+float(n@S@n)*np.eye(3)
                    eig,vec=np.linalg.eigh(Q)
                    if best is None or eig[0]<best[0]:best=(float(eig[0]),n.tolist(),vec[:,0].tolist())
                acoustic_probe=dict(run=c["run"],pressure_kPa=target,
                    core_element=e["core_shear_eid"],integration_point=e["core_shear_ip"],
                    minimum_sampled_acoustic_eigenvalue_MPa=best[0],reference_wave_direction=best[1],
                    polarization_in_cholesky_frame=best[2],green_strain=E.tolist(),
                    result="demonstrated_loss_of_strong_ellipticity" if best[0]<0 else "no_negative_direction_found; not proof of ellipticity",
                    scope="Exact rank-one second variation at one native state; directional search supplies a witness if negative.")
    for q in cal["common_passing_checks"]:
        s=summary(q["run"]);core=core_records[q["run"]]
        fy=s["first_yield_bracket_kPa"]
        cb=core["strength_crossings"]["minimum_average"]["bracket_kPa"]
        check("core-calibration-common-pass:"+q["run"],
            s["endpoint_kPa"]/1.1>=P0 and (fy is None or fy[0]>=P0)
            and (cb is None or cb[0]>=P0),q)
    check("core-calibration-failing-edge",cal["global_bracket"]["failing"]["capacity_kPa"]<P0,
          cal["global_bracket"]["failing"])
    perfect={}
    for m in ["W","L"]:
        for y in [255,300,345]:
            n=f"cfull-perfect-{m}-y{y}-a0.000000-nu0.0768"
            s=summary(n);perfect[f"{y}-{m}"]=s
            if y<345:
                check("regularized-perfect-fails:"+n,
                      s["endpoint_kPa"]<P0 and s["first_yield_bracket_kPa"][1]<P0,
                      dict(endpoint_kPa=s["endpoint_kPa"],first_yield=s["first_yield_bracket_kPa"]))
    perfect345=perfect["345-W"]
    check("regularized-biased-perfect-fails-SF105",perfect345["endpoint_kPa"]/1.1<P0*1.05,
          perfect345["endpoint_kPa"]/1.1)
    sweep_path_checks=[]
    for r in sweep:
        cs=r["first_core_shear"]["minimum_average"]["bracket_kPa"]
        lower=min(r["endpoint_kPa"],r["first_face_yield_bracket_kPa"][0],
                  cs[0] if cs else math.inf)
        native=list(csv.DictReader((ROOT/"runs"/r["run"]/"CORE-PATH.csv").open()))
        retained=[row for row in native if float(row["p_kPa"])<=lower+1e-4]
        bound=min(float(row["min_acoustic_lower_bound_MPa"]) for row in retained)
        detail=dict(run=r["run"],through_pressure_kPa=lower,
                    minimum_sufficient_acoustic_bound_MPa=bound,
                    scope="Saved points through the lower bracket of first material failure; no post-failure stability credit.")
        sweep_path_checks.append(detail)
        check("core-sweep-pre-failure-local-ellipticity:"+r["run"],bound>0,detail)
    out=dict(tag="QUESTIONABLE/PROJECTION",core_law=read("INPUTS.json")["core_fold"],
        regularized_boundaries=groups,governing_boundaries=governing,thermal_debit=cold,
        calibration=cal,sweep=sweep,perfect_cases=perfect,controls=confirmations,
        core_run_count=len(core_records),minimum_passing_acoustic_bound_MPa=min_acoustic,
        maximum_passing_core_compression_MPa=max_crush,
        maximum_native_invariant_error_MPa=max(r["max_invariant_error_MPa"] for r in core_records.values()),
        inherited_core_acoustic_probe=acoustic_probe,
        sweep_pre_failure_local_ellipticity=sweep_path_checks,
        strength_interaction="sqrt((tau_meridian/S_meridian)^2+(tau_hoop/S_hoop)^2) <= 1",
        inherited_law_status="No accepted tolerance: CHECK-029 demonstrated local ellipticity loss. Historical .01-MPa results remain separate.",
        installed_hull_allowable=None,physical_core_characterization=False)
    (ROOT/"CORE-RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
    table=[]
    for r in sweep:
        c=r["first_core_shear"]["minimum_average"];typ=r["first_core_shear"]["typical"]
        table.append(dict(run=r["run"],width_mm=r["width_mm"],meridian=r["meridian"],
            amplitude_mm=r["amplitude_mm"],face_yield_MPa=345,core_Einplane_MPa=1,
            endpoint_kPa=r["endpoint_kPa"],face_yield_lower_kPa=r["first_face_yield_bracket_kPa"][0],
            face_yield_upper_kPa=r["first_face_yield_bracket_kPa"][1],
            face_yield_estimate_kPa=r["first_face_yield_estimate_kPa"],
            core_minimum_average_shear_estimate_kPa=c.get("estimate_kPa"),
            core_minimum_average_shear_lower_kPa=c["bracket_kPa"][0] if c["bracket_kPa"] else None,
            core_minimum_average_shear_upper_kPa=c["bracket_kPa"][1] if c["bracket_kPa"] else None,
            core_typical_shear_estimate_kPa=typ.get("estimate_kPa"),
            core_shear_status="crossing_observed" if c["bracket_kPa"] else "not_reached_on_converged_path",
            three_limit_estimate_kPa=r["three_limit_estimate_kPa"],
            endpoint_core_shear_MPa=r["endpoint_core_shear_MPa"]))
    with (ROOT/"CORE-SWEEP.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(table[0]));w.writeheader();w.writerows(table)
    return out

def plots(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    groups=d["regularized_boundaries"]
    for ext in ["pdf","png"]:
        old=ROOT/f"TOLERANCE.{ext}"
        old.replace(ROOT/f"FACE-ONLY-TOLERANCE.{ext}")
    narrow=[g for g in groups if g["label"]!="fullwave"]
    fig,ax=plt.subplots(figsize=(10,5.5))
    for i,g in enumerate(narrow):
        for sf,dx,color in [(1.,-.15,"#28648b"),(1.05,.15,"#956b22")]:
            b=next(b for b in g["boundaries"] if b["SF"]==sf and b["strength_basis"]=="minimum_average")
            a,lo,hi=b["amplitude_estimate_mm"],b["passing_amplitude_mm"],b["failing_amplitude_mm"]
            ax.errorbar(i+dx,a,yerr=[[a-lo],[hi-a]],fmt="o",capsize=4,color=color,
                        label=f"SF {sf:g}" if i==0 else None)
    cal=d["calibration"]["global_bracket"]
    ax.axhspan(cal["passing"]["amplitude_mm"],cal["failing"]["amplitude_mm"],color="#a64632",alpha=.2,
               label="Common amplitude; endpoint / 1.10 (conditional)")
    ax.set_xticks(range(len(narrow)),[f"{g['width_mm']:.0f} mm\n{g['meridian']}" for g in narrow])
    ax.set_ylabel("Dimple amplitude (mm)");ax.set_ylim(bottom=0)
    ax.set_title("345 MPa faces: endpoint, first face yield and first core shear\nExplicit E-in-plane = 1 MPa core regularization")
    ax.legend(fontsize=9);ax.grid(axis="y",alpha=.2)
    fig.text(.5,.015,"QUESTIONABLE / PROJECTION · minimum-average core strengths · numerical brackets are not physical uncertainty bounds",ha="center",fontsize=8.5)
    fig.tight_layout(rect=[0,.04,1,1])
    for ext in ["pdf","png"]:fig.savefig(ROOT/f"TOLERANCE.{ext}",dpi=150)
    plt.close(fig)
    fig,axes=plt.subplots(2,4,figsize=(16,8),sharex=True,sharey=True)
    for j,label in enumerate(["old021","current","old021b","fullwave"]):
        for i,m in enumerate(["W","L"]):
            ax=axes[i,j];points=sorted((r for r in d["sweep"] if r["label"]==label and r["meridian"]==m),key=lambda r:r["amplitude_mm"])
            perfect=d["perfect_cases"]["345-"+m]
            pb=perfect["first_yield_bracket_kPa"]
            x=[0]+[r["amplitude_mm"] for r in points]
            fy=[sum(pb)/2]+[r["first_face_yield_estimate_kPa"] for r in points]
            endpoint=[perfect["endpoint_kPa"]]+[r["endpoint_kPa"] for r in points]
            cs=[math.nan]+[r["first_core_shear"]["minimum_average"].get("estimate_kPa",math.nan) for r in points]
            capacity=[min(endpoint[0],fy[0])]+[r["three_limit_estimate_kPa"] for r in points]
            ax.plot(x,endpoint,"--",c="#777777",label="Numerical endpoint")
            ax.plot(x,fy,"o-",c="#28648b",ms=3,label="First face yield")
            ax.plot(x,cs,"s-",c="#b55a27",ms=3,label="First core shear")
            ax.plot(x,capacity,":",c="#38744a",lw=2,label="Three-limit minimum")
            ax.axhline(P0,c="#555555",lw=.8);ax.axhline(P0*1.05,c="#555555",lw=.8,ls=":")
            ax.set_xscale("symlog",linthresh=1);ax.set_ylim(0,120);ax.grid(alpha=.15)
            ax.set_title(f"{m} · w={points[0]['width_mm']:.1f} mm")
            if j==0:ax.set_ylabel("Pressure (kPa)")
            if i==1:ax.set_xlabel("Dimple amplitude (mm)")
    axes[0,0].legend(fontsize=8)
    fig.suptitle("345 MPa faces with stated regularized core: large dimples encounter material limits before the endpoint")
    fig.text(.5,.015,"QUESTIONABLE / PROJECTION · missing core marker: strength not reached before numerical stop · lines join sampled amplitudes",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,.035,1,.95])
    for ext in ["pdf","png"]:fig.savefig(ROOT/f"CORE-PRESSURE-SWEEP.{ext}",dpi=150)
    plt.close(fig)
