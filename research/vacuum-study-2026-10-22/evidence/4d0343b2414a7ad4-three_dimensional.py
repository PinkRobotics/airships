#!/usr/bin/env python3
"""Full 360-degree hemisphere, C3D20 bricks and C3D15 polar wedges.

Own mesh generator for an independent check of the axisymmetric restriction.
The shared numerical input constructor supplies geometry/material constants only.
"""
import argparse
import hashlib
import json
import math
from axisymmetric import ROOT, case_parameters

def main():
    a=argparse.ArgumentParser()
    a.add_argument("name")
    a.add_argument("--case",choices=["flat","dimple","transfer40"],default="flat")
    a.add_argument("--ntheta",type=int,default=24)
    a.add_argument("--nphi",type=int,default=64)
    a.add_argument("--ncore",type=int,default=2)
    a.add_argument("--nface",type=int,default=1)
    a.add_argument("--amplitude",type=float,default=0.)
    a.add_argument("--pressure",type=float,default=0.1)
    a.add_argument("--analysis",choices=["buckle","static"],default="buckle")
    a.add_argument("--grading",type=float,default=1.)
    a.add_argument("--count-only",action="store_true")
    args=a.parse_args()
    p=case_parameters(args.case)
    ro,ti,to,tc=(p[k] for k in ["radius_outer_mm","face_inner_mm","face_outer_mm","core_mm"])
    ri=ro-ti-to-tc
    radial=[ri]; mats=[]
    for x,y,n,mat in [(ri,ri+ti,args.nface,"INNER"),(ri+ti,ro-to,args.ncore,"CORE"),(ro-to,ro,args.nface,"OUTER")]:
        radial.extend(x+(y-x)*k/(2*n) for k in range(1,2*n+1));mats.extend([mat]*n)
    nr=len(mats);nt=args.ntheta;np=args.nphi
    nodes=[]; ids={}
    def node(j,i,k):
        i=i%(2*np)
        if j==0:i=0
        key=(j,i,k)
        if key not in ids:
            th=math.pi/2*(j/(2*nt))**args.grading;ph=math.pi*i/np
            delta=args.amplitude*math.exp(-(ro*th/(0.1*ro))**2)
            r=radial[k]-delta
            xyz=(r*math.sin(th)*math.cos(ph),r*math.sin(th)*math.sin(ph),r*math.cos(th))
            if j==0:xyz=(0.,0.,xyz[2])
            if j==2*nt:xyz=(xyz[0],xyz[1],0.)
            ids[key]=len(nodes)+1;nodes.append((ids[key],*xyz))
        return ids[key]
    elems=[];groups={};surface=[]
    for j in range(nt):
        for i in range(np):
            for k in range(nr):
                t,f,r=2*j,2*i,2*k
                if j==0:
                    coords=[(0,0,r),(2,f,r),(2,f+2,r),
                            (0,0,r+2),(2,f,r+2),(2,f+2,r+2),
                            (1,f,r),(2,f+1,r),(1,f+2,r),
                            (1,f,r+2),(2,f+1,r+2),(1,f+2,r+2),
                            (0,0,r+1),(2,f,r+1),(2,f+2,r+1)]
                    typ="C3D15"
                else:
                    coords=[(t,f,r),(t+2,f,r),(t+2,f+2,r),(t,f+2,r),
                            (t,f,r+2),(t+2,f,r+2),(t+2,f+2,r+2),(t,f+2,r+2),
                            (t+1,f,r),(t+2,f+1,r),(t+1,f+2,r),(t,f+1,r),
                            (t+1,f,r+2),(t+2,f+1,r+2),(t+1,f+2,r+2),(t,f+1,r+2),
                            (t,f,r+1),(t+2,f,r+1),(t+2,f+2,r+1),(t,f+2,r+1)]
                    typ="C3D20"
                eid=len(elems)+1
                elems.append((eid,typ,*[node(*c) for c in coords]))
                groups.setdefault(mats[k],[]).append(eid)
                if k==nr-1:surface.append(eid)
    meta=p|dict(name=args.name,dimension=3,analysis=args.analysis,amplitude_mm=args.amplitude,
               gaussian_width_mm=.1*ro,meridian_direction="isotropic",
               pressure_reference_MPa=args.pressure,element_type="C3D20+C3D15",
               defined_nodes=len(nodes),defined_elements=len(elems),nominal_dofs=3*len(nodes),
               max_equator_edge_mm=math.pi*ro/np*2,
               max_meridian_edge_mm=math.pi*ro/2*(1-((nt-1)/nt)**args.grading),
               minimum_meridian_edge_mm=math.pi*ro/2/nt**args.grading,
               meridional_grading=args.grading,
               ntheta=nt,nphi=np,ncore=args.ncore,nface=args.nface,args=vars(args),
               material_law="linear elastic; NLGEOM for static",bond="shared conforming nodes")
    if args.count_only:
        print(json.dumps(meta,indent=2));return
    d=ROOT/"runs"/args.name;d.mkdir(exist_ok=False)
    lines=["*HEADING",f"MAINLINE-029 {args.name}; full hemisphere; N mm MPa; QUESTIONABLE","*NODE"]
    lines.extend(",".join([str(n[0])]+[f"{x:.14g}" for x in n[1:]]) for n in nodes)
    for typ in ["C3D15","C3D20"]:
        lines.append(f"*ELEMENT,TYPE={typ},ELSET=ALL")
        for e in elems:
            if e[1]!=typ:continue
            fields=[e[0],*e[2:]]
            if len(fields)>16:
                lines.append(",".join(map(str,fields[:16]))+",")
                lines.append(",".join(map(str,fields[16:])))
            else:lines.append(",".join(map(str,fields)))
    def setout(kind,name,values):
        lines.append(f"*{kind},{kind}={name}")
        for i in range(0,len(values),16):lines.append(",".join(map(str,values[i:i+16])))
    for mat,values in groups.items():setout("ELSET",mat,values)
    setout("NSET","RIM",[n for (j,i,k),n in ids.items() if j==2*nt])
    setout("NSET","POLES",[ids[(0,0,0)],ids[(0,0,2*nr)]])
    lines.extend(["*MATERIAL,NAME=FACE","*ELASTIC",f"{p['E_face_MPa']},{p['nu_face']}",
                  "*MATERIAL,NAME=COREMAT","*ELASTIC",f"{p['E_core_MPa']},{p['nu_core']}"])
    for group,mat in [("INNER","FACE"),("OUTER","FACE"),("CORE","COREMAT")]:
        lines.append(f"*SOLID SECTION,ELSET={group},MATERIAL={mat}")
    lines.extend(["*BOUNDARY","RIM,1,3"])
    if args.analysis=="buckle":
        lines.extend(["*STEP","*BUCKLE","8,0.00001,40,2000"])
    else:
        lines.extend(["*STEP,NLGEOM,INC=2000","*STATIC","0.01,1,0.000001,0.02"])
    lines.append("*DLOAD")
    lines.extend(f"{e},P2,{args.pressure}" for e in surface)
    lines.extend(["*NODE FILE,FREQUENCY=1","U","*NODE PRINT,NSET=POLES,FREQUENCY=1","U,RF","*END STEP"])
    deck=d/"model.inp";deck.write_text("\n".join(lines)+"\n")
    meta["deck_sha256"]=hashlib.sha256(deck.read_bytes()).hexdigest()
    (d/"MODEL.json").write_text(json.dumps(meta,indent=2)+"\n")
    print(json.dumps({k:meta[k] for k in ["name","defined_nodes","defined_elements","nominal_dofs"]}))

if __name__=="__main__":main()
