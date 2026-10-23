"""Core admissibility from native local Green strain, independently checked by Cauchy invariants.

Orthotropic StVK, zero Poisson ratios. C=I+2E. Choose F*=chol(C).T;
F* differs from the actual F only by a rigid rotation. Its first column
is the current material tangent. Thus F*S*F.T/J in this frame gives the
current tangent/normal Cauchy shear without assuming small rotations.
"""
import csv,gzip,json,math,pathlib
PSI=.006894757293168361
def collect_core(d):
    m=json.loads((d/"MODEL.json").read_text())
    assert m["core_kind"]=="orthotropic"
    ei,en,g=m["E_inplane_MPa"],m["E_core_MPa"],m["G_meridian_MPa"]
    strengths={"minimum_average":PSI*(25 if m["meridian_direction"]=="W" else 45),
               "typical":PSI*(35 if m["meridian_direction"]=="W" else 55)}
    hoop_strengths={"minimum_average":PSI*(45 if m["meridian_direction"]=="W" else 25),
                    "typical":PSI*(55 if m["meridian_direction"]=="W" else 35)}
    native={};rows={};state=None;t=None
    def pressure(t):
        for (t0,p0),(t1,p1) in zip(m.get("pressure_schedule_kPa",[[0,0],[1,m["pressure_reference_MPa"]*1000]]),
                                  m.get("pressure_schedule_kPa",[[0,0],[1,m["pressure_reference_MPa"]*1000]])[1:]):
            if t<=t1+1e-12:return p0+(p1-p0)*(t-t0)/(t1-t0)
        raise ValueError(t)
    raw=d/"model.dat"
    handle=raw.open("rt") if raw.exists() else gzip.open(d/"model.dat.gz","rt")
    max_invariant_abs=0.;max_outplane=0.
    with handle as f:
        for line in f:
            if "and time" in line:
                t=float(line.rsplit("and time",1)[1])
                if "set COREALL" not in line:
                    state=None;continue
                state="S" if line.lstrip().startswith("stresses (") else "E" if line.lstrip().startswith("strains (") else None
                if state=="S":native.clear()
                row=rows.setdefault(t,dict(time=t,p_kPa=pressure(t),max_core_shear_MPa=0.,
                    max_core_compression_MPa=0.,max_core_reference_shear_MPa=0.,
                    max_invariant_abs_MPa=0.,max_core_hoop_shear_MPa=0.,
                    minimum_average_index=0.,typical_index=0.,
                    min_acoustic_lower_bound_MPa=math.inf,points=0))
                continue
            v=line.split()
            if state not in ["S","E"] or len(v)<8 or not v[0].isdigit():continue
            eid,ip=map(int,v[:2]);a,b,c,ab,ac,bc=map(float,v[2:8])
            if state=="S":
                native[t,eid,ip]=(a,b,c,ab,ac,bc)
                row["max_core_reference_shear_MPa"]=max(row["max_core_reference_shear_MPa"],abs(ab))
                continue
            c11,c22,c33,c12,c13,c23=1+2*a,1+2*b,1+2*c,2*ab,2*ac,2*bc
            assert min(c11,c22,c33)>0 and c11*c22>c12*c12
            max_outplane=max(max_outplane,abs(ac),abs(bc))
            f11=math.sqrt(c11);f12=c12/f11;f13=c13/f11
            f22=math.sqrt(c22-f12*f12);f23=(c23-f12*f13)/f22
            f33=math.sqrt(c33-f13*f13-f23*f23)
            j=f11*f22*f33
            s11,s22,s33,s12=ei*a,en*b,ei*c,2*g*ab
            s13=2*m["G_inplane_MPa"]*ac;s23=2*m["G_hoop_MPa"]*bc
            # Exact sufficient Legendre-Hadamard bound for StVK at this state.
            # d2W[a*N,a*N]=|a|^2 N.S.N + sym(F.T*a*N):C:sym(...).
            # cmin is the smallest elasticity eigenvalue on symmetric tensors.
            # Gershgorin supplies conservative eigenvalue bounds on S and C.
            cmin=min(ei,en,2*g,2*m["G_inplane_MPa"],2*m["G_hoop_MPa"])
            strain_metric_lower=min(c11-abs(c12)-abs(c13),
                c22-abs(c12)-abs(c23),c33-abs(c13)-abs(c23))
            pk2_lower=min(s11-abs(s12)-abs(s13),s22-abs(s12)-abs(s23),
                          s33-abs(s13)-abs(s23))
            acoustic_bound=pk2_lower+.5*cmin*strain_metric_lower
            row["min_acoustic_lower_bound_MPa"]=min(row["min_acoustic_lower_bound_MPa"],acoustic_bound)
            xx=(f11*f11*s11+f12*f12*s22+f13*f13*s33+
                2*f11*f12*s12+2*f11*f13*s13+2*f12*f13*s23)/j
            yy=(f22*f22*s22+f23*f23*s33+2*f22*f23*s23)/j
            zz=f33*f33*s33/j
            xy=(f11*f22*s12+f11*f23*s13+f12*f22*s22+
                (f12*f23+f13*f22)*s23+f13*f23*s33)/j
            xz=f33*(f11*s13+f12*s23+f13*s33)/j
            yz=f33*(f22*s23+f23*s33)/j
            norm=math.hypot(f23,f33);ny,nz=f33/norm,-f23/norm
            tau=xy*ny+xz*nz
            tau_hoop=(-nz)*(yy*ny+yz*nz)+ny*(yz*ny+zz*nz)
            normal=ny*ny*yy+2*ny*nz*yz+nz*nz*zz
            sx,sy,sz,sxy,sxz,syz=native[t,eid,ip]
            inv=[abs((xx+yy+zz)-(sx+sy+sz)),
                 abs(math.sqrt(xx*xx+yy*yy+zz*zz+2*(xy*xy+xz*xz+yz*yz))-
                     math.sqrt(sx*sx+sy*sy+sz*sz+2*(sxy*sxy+sxz*sxz+syz*syz)))]
            err=max(inv);max_invariant_abs=max(max_invariant_abs,err)
            row["max_invariant_abs_MPa"]=max(row["max_invariant_abs_MPa"],err)
            row["points"]+=1
            row["max_core_hoop_shear_MPa"]=max(row["max_core_hoop_shear_MPa"],abs(tau_hoop))
            for label,strength in strengths.items():
                index=math.hypot(tau/strength,tau_hoop/hoop_strengths[label])
                row[label+"_index"]=max(row[label+"_index"],index)
            if abs(tau)>row["max_core_shear_MPa"]:
                row.update(max_core_shear_MPa=abs(tau),core_shear_eid=eid,core_shear_ip=ip,
                           shear_at_peak_signed_MPa=tau,
                           peak_E11=a,peak_E22=b,peak_E33=c,peak_E12=ab,peak_E13=ac,peak_E23=bc)
            row["max_core_compression_MPa"]=max(row["max_core_compression_MPa"],-normal)
    path=sorted(rows.values(),key=lambda r:r["time"])
    assert path and all(r["points"]>0 for r in path),"Missing core strain output"
    assert max_invariant_abs<2e-5,("Native strain/stress reconstruction mismatch",max_invariant_abs)
    cols=sorted(set().union(*(r.keys() for r in path)))
    with (d/"CORE-PATH.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(path)
    crossings={}
    for label,strength in strengths.items():
        field=label+"_index";prev=dict(p_kPa=0,**{field:0})
        for row in path:
            if row[field]>=1:
                crossings[label]=dict(strength_MPa=strength,
                    bracket_kPa=[prev["p_kPa"],row["p_kPa"]],
                    estimate_kPa=prev["p_kPa"]+(1-prev[field])*
                    (row["p_kPa"]-prev["p_kPa"])/(row[field]-prev[field]))
                break
            prev=row
        else:crossings[label]=dict(strength_MPa=strength,bracket_kPa=None,
                                   not_reached_through_kPa=path[-1]["p_kPa"])
    out=dict(name=m["name"],E_inplane_MPa=ei,G_inplane_MPa=m["G_inplane_MPa"],
        law="orthotropic StVK, zero Poisson coupling; transverse shear stop, not damage evolution",
        stress_frame="current material tangent and perpendicular normal; reconstructed from local Green strain",
        max_invariant_error_MPa=max_invariant_abs,max_outplane_strain=max_outplane,
        endpoint=path[-1],strength_crossings=crossings,
        crush_typical_MPa=35*PSI,tag="QUESTIONABLE/PROJECTION")
    (d/"CORE-SUMMARY.json").write_text(json.dumps(out,indent=2)+"\n")
    return out
if __name__=="__main__":
    import sys
    for p in sys.argv[1:]:print(json.dumps(collect_core(pathlib.Path(p))))
