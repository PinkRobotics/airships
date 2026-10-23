#!/usr/bin/env python3
"""Streaming integration-point audit, with brackets rather than invented collapse loads."""
import csv, gzip, hashlib, json, math, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parent
def collect(name, compress=True):
    d=ROOT/"runs"/name
    m=json.loads((d/"MODEL.json").read_text())
    pref=m["pressure_reference_MPa"]*1000
    raw=d/"model.dat"; packed=d/"model.dat.gz"
    if not raw.exists() and not packed.exists():
        r=dict(name=name,status="no_native_data")
        (d/"SUMMARY.json").write_text(json.dumps(r,indent=2)+"\n");return r
    opener=raw.open if raw.exists() else lambda mode:gzip.open(packed,mode)
    paths={};state=None;t=None
    nr=2*m["nface"]+m["ncore"]
    with opener("rt") as f:
        for line in f:
            if "and time" in line:
                t=float(line.rsplit("and time",1)[1])
                row=paths.setdefault(t,dict(time=t,p_kPa=t*pref,max_mises_MPa=0.,
                    max_peeq=0.,inner_mises_MPa=0.,outer_mises_MPa=0.))
                state="stress" if line.lstrip().startswith("stresses (") else "peeq" if "equivalent plastic strain (" in line else "displacement" if line.lstrip().startswith("displacements (") else None
                continue
            fields=line.split()
            if state=="stress" and len(fields)==8 and fields[0].isdigit():
                eid,ip=map(int,fields[:2]);xx,yy,zz,xy,xz,yz=map(float,fields[2:])
                vm=math.sqrt(.5*((xx-yy)**2+(yy-zz)**2+(zz-xx)**2)+3*(xy*xy+xz*xz+yz*yz))
                face="inner" if (eid-1)%nr<m["nface"] else "outer"
                row[face+"_mises_MPa"]=max(row[face+"_mises_MPa"],vm)
                if vm>row["max_mises_MPa"]:
                    row.update(max_mises_MPa=vm,max_mises_eid=eid,max_mises_ip=ip,max_mises_face=face)
            elif state=="peeq" and len(fields)==3 and fields[0].isdigit():
                pe=float(fields[2])
                if pe>row["max_peeq"]:
                    row.update(max_peeq=pe,max_peeq_eid=int(fields[0]),max_peeq_ip=int(fields[1]))
            elif state=="displacement" and len(fields)==4 and fields[0].isdigit():
                row["pole_uy_mm"]=float(fields[2])
    path=sorted(paths.values(),key=lambda x:x["time"])
    cols=sorted(set().union(*(r.keys() for r in path))) if path else ["time"]
    with (d/"PATH.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(path)
    first=next((i for i,r in enumerate(path) if r["max_peeq"]>1e-10),None)
    bracket=None
    if first is not None:
        bracket=[path[first-1]["p_kPa"] if first else 0.,path[first]["p_kPa"]]
    elastic=path[:first] if first is not None else path
    estimates={}
    for y in [255.,300.,341.5897774303177,345.]:
        cross=next((i for i,r in enumerate(elastic) if r["max_mises_MPa"]>=y),None)
        if cross is not None:
            hi=elastic[cross];lo=elastic[cross-1] if cross else dict(p_kPa=0.,max_mises_MPa=0.)
            val=lo["p_kPa"]+(y-lo["max_mises_MPa"])*(hi["p_kPa"]-lo["p_kPa"])/(hi["max_mises_MPa"]-lo["max_mises_MPa"])
            estimates[str(y)]=dict(p_kPa=val,kind="interpolated_on_elastic_path",
                                  bracket_kPa=[lo["p_kPa"],hi["p_kPa"]])
        elif len(elastic)>=2 and first is not None and y==m.get("yield_stress_MPa"):
            lo,hi=elastic[-2:]
            val=hi["p_kPa"]+(y-hi["max_mises_MPa"])*(hi["p_kPa"]-lo["p_kPa"])/(hi["max_mises_MPa"]-lo["max_mises_MPa"])
            estimates[str(y)]=dict(p_kPa=val,kind="last_two_elastic_points_extrapolation",bracket_kPa=bracket,
                                  inside_native_bracket=bracket[0]<=val<=bracket[1])
    stdout=(d/"ccx.stdout").read_text(errors="replace") if (d/"ccx.stdout").exists() else ""
    run=json.loads((d/"SOLVER.json").read_text()) if (d/"SOLVER.json").exists() else {}
    eigen=[]
    if m["analysis"]=="buckle":
        with opener("rt") as f: dat=f.read()
        for match in re.finditer(r"^\s+\d+\s+([0-9.]+E[+-]\d+)\s*$",dat,re.M):
            eigen.append(float(match.group(1))*pref)
    r=dict(name=name,analysis=m["analysis"],amplitude_mm=m["amplitude_mm"],
        width_mm=m["gaussian_width_mm"],meridian=m["meridian_direction"],
        yield_MPa=m.get("yield_stress_MPa"),nu=m["nu_face"],ntheta=m["ntheta"],
        nface=m["nface"],ncore=m["ncore"],grading=m["args"]["grading"],
        increments=len(path),endpoint_kPa=path[-1]["p_kPa"] if path else None,
        endpoint_kind="load_cap" if path and path[-1]["time"]>=.999999 else "last_converged_static_increment",
        first_yield_bracket_kPa=bracket,first_yield_estimates=estimates,
        endpoint_max_mises_MPa=path[-1]["max_mises_MPa"] if path else None,
        endpoint_max_peeq=path[-1]["max_peeq"] if path else None,
        endpoint_pole_uy_mm=path[-1].get("pole_uy_mm") if path else None,
        solver=run,errors=[l for l in stdout.splitlines() if "*ERROR" in l],
        eigen_kPa=eigen,peeq_detection_threshold=1e-10)
    (d/"SUMMARY.json").write_text(json.dumps(r,indent=2)+"\n")
    if compress and raw.exists() and (d/"SOLVER.json").exists():
        h=hashlib.sha256()
        with raw.open("rb") as f,gzip.open(packed,"wb",compresslevel=1) as g:
            for b in iter(lambda:f.read(1024*1024),b""):h.update(b);g.write(b)
        (d/"NATIVE-DAT.json").write_text(json.dumps(dict(uncompressed_bytes=raw.stat().st_size,
            uncompressed_sha256=h.hexdigest(),archive=packed.name),indent=2)+"\n")
        raw.unlink()
    return r
if __name__=="__main__":
    for name in sys.argv[1:]:print(json.dumps(collect(name)))
