"""Independent 3-D beam and truss reconstruction of the filed frame screen."""
from pathlib import Path
import json
import math
import numpy as np
from scipy.spatial import ConvexHull
from scipy.sparse import coo_matrix, csc_matrix, bmat
from scipy.sparse.linalg import splu
from scipy.linalg import null_space, eigvalsh
from check45 import ROOT, save, P, R, PI, compare, CHECKS


def mesh(f):
    phi=(1+math.sqrt(5))/2
    original=[]
    for a in [-1,1]:
        for b in [-phi,phi]:
            original.extend([(0,a,b),(a,b,0),(b,0,a)])
    original=np.array(original,float)
    original/=np.linalg.norm(original,axis=1)[:,None]
    hull=ConvexHull(original)
    points=[];index={};triangles=[]
    def add(x):
        x=x/np.linalg.norm(x)*R
        key=tuple(np.round(x,11))
        if key not in index:
            index[key]=len(points);points.append(x)
        return index[key]
    for face in hull.simplices:
        a,b,c=original[face]
        ids={}
        for i in range(f+1):
            for j in range(f+1-i):
                ids[i,j]=add((1-(i+j)/f)*a+i/f*b+j/f*c)
        for i in range(f):
            for j in range(f-i):
                triangles.append((ids[i,j],ids[i+1,j],ids[i,j+1]))
                if j<f-i-1:
                    triangles.append((ids[i+1,j],ids[i+1,j+1],ids[i,j+1]))
    points=np.array(points)
    tris=np.array(triangles)
    for k,t in enumerate(tris):
        a,b,c=points[t]
        if np.dot(np.cross(b-a,c-a),a)<0:
            tris[k]=t[[0,2,1]]
    edges=sorted(set(tuple(sorted((t[i],t[(i+1)%3]))) for t in tris for i in range(3)))
    return points,tris,np.array(edges)


def local_beam(length,E,A,I,nu):
    k=np.zeros((12,12))
    def put(ids,block):
        k[np.ix_(ids,ids)]+=block
    put([0,6],E*A/length*np.array([[1,-1],[-1,1]]))
    put([3,9],E/(2*(1+nu))*2*I/length*np.array([[1,-1],[-1,1]]))
    L=length
    basic=E*I/L**3*np.array([[12,6*L,-12,6*L],
                            [6*L,4*L*L,-6*L,2*L*L],
                            [-12,-6*L,12,-6*L],
                            [6*L,2*L*L,-6*L,4*L*L]])
    put([1,5,7,11],basic)
    signs=np.diag([1,-1,1,-1])
    put([2,4,8,10],signs@basic@signs)
    return k


def assemble(points,tris,edges,E,A,I,nu,load):
    size=6*len(points)
    vals=[];rr=[];cc=[];members=[]
    for n,(i,j) in enumerate(edges):
        delta=points[j]-points[i];length=np.linalg.norm(delta)
        ex=delta/length
        reference=np.eye(3)[np.argmin(abs(ex))]
        ey=np.cross(reference,ex);ey/=np.linalg.norm(ey)
        ez=np.cross(ex,ey)
        rotation=np.array([ex,ey,ez])
        trans=np.zeros((12,12))
        for q in range(4):trans[q*3:q*3+3,q*3:q*3+3]=rotation
        local=local_beam(length,E,A,I,nu)
        global_k=trans.T@local@trans
        ids=np.r_[np.arange(6*i,6*i+6),np.arange(6*j,6*j+6)]
        rr.extend(np.repeat(ids,12));cc.extend(np.tile(ids,12));vals.extend(global_k.ravel())
        members.append(dict(nodes=[int(i),int(j)],length=float(length),ids=ids,k=global_k,t=trans,local=local))
    K=coo_matrix((vals,(rr,cc)),shape=(size,size)).tocsc()
    force=np.zeros(size);areas=np.zeros(len(points));spherical=np.zeros(len(points))
    for triangle in tris:
        a,b,c=points[triangle]
        cross=np.cross(b-a,c-a)/2;area=np.linalg.norm(cross)
        angle=2*math.atan2(abs(np.dot(a,np.cross(b,c))),
                           R**3+R*(np.dot(a,b)+np.dot(b,c)+np.dot(c,a)))
        for i in triangle:
            areas[i]+=area/3
            spherical[i]+=angle*R*R/3
            if load=="normal_planar":
                force[6*i:6*i+3]-=P*cross/3
    if load!="normal_planar":
        weights=areas if load=="radial_planar" else spherical if load=="radial_spherical" else np.ones(len(points))*4*PI*R*R/len(points)
        for i,x in enumerate(points):force[6*i:6*i+3]=-P*weights[i]*x/R
    # Six orthonormal rigid modes constrain only rigid translation/rotation;
    # they introduce no physically anchored node or artificial reaction.
    rigid=np.zeros((size,6))
    for i,x in enumerate(points):
        rigid[6*i:6*i+3,:3]=np.eye(3)
        for q in range(3):
            rigid[6*i:6*i+3,3+q]=np.cross(np.eye(3)[q],x)
            rigid[6*i+3:6*i+6,3+q]=np.eye(3)[q]
    rigid=np.linalg.qr(rigid)[0]
    return K,force,members,rigid,areas,spherical


def solve(K,force,rigid):
    # Symmetric Lagrange multipliers eliminate the free-body nullspace.
    scale=1e7
    C=csc_matrix(rigid*scale)
    augmented=bmat([[K,C],[C.T,None]],format="csc")
    sol=splu(augmented).solve(np.r_[force,np.zeros(6)])
    return sol[:-6],float(np.linalg.norm(sol[-6:]*scale))


def stresses(u,members,A,I,ro,removed=None):
    axial=[];moments=[];peak=[];tension=[]
    for j,m in enumerate(members):
        if j==removed:
            axial.append(np.nan);moments.append(np.nan);peak.append(np.nan);tension.append(np.nan);continue
        q=m["local"]@(m["t"]@u[m["ids"]])
        n=(q[6]-q[0])/2
        moment=max(np.linalg.norm(q[[4,5]]),np.linalg.norm(q[[10,11]]))
        axial.append(n);moments.append(moment)
        peak.append(abs(n)/A+moment*ro/I)
        tension.append(max(0.,n/A+moment*ro/I))
    return dict(axial=np.array(axial),moments=np.array(moments),peak=np.array(peak),tension=np.array(tension))


def truss_nullity(points,edges,A,E,removed):
    size=3*len(points)
    compatibility=np.zeros((len(edges),size))
    for k,(i,j) in enumerate(edges):
        axis=(points[j]-points[i]);length=np.linalg.norm(axis);axis/=length
        compatibility[k,3*i:3*i+3]=-axis*math.sqrt(E*A/length)
        compatibility[k,3*j:3*j+3]=axis*math.sqrt(E*A/length)
    values=np.linalg.svd(compatibility,compute_uv=False)
    altered=np.delete(compatibility,removed,axis=0)
    damaged_values=np.linalg.svd(altered,compute_uv=False)
    # Count rank from compatibility rather than the squared-condition K.
    rank=int(np.sum(values>values[0]*1e-10))
    rank2=int(np.sum(damaged_values>damaged_values[0]*1e-10))
    return dict(intact_rank=rank,damaged_rank=rank2,
                intact_nonrigid_nullity=size-rank-6,damaged_nonrigid_nullity=size-rank2-6,
                intact_smallest_nonzero_singular=float(values[-1]),
                damaged_smallest_nonzero_singular=float(damaged_values[-1]))


def run_frequency(f,p3,load):
    points,tris,edges=mesh(f)
    E=410e9;nu=.16;A=p3["A"];I=p3["I"];ro=p3["ro"]
    K,F,members,rigid,areas,sph=assemble(points,tris,edges,E,A,I,nu,load)
    u,reaction=solve(K,F,rigid)
    intact=stresses(u,members,A,I,ro)
    lengths=np.array([x["length"] for x in members])
    out=dict(nodes=len(points),members=len(edges),edge_min_m=float(min(lengths)),
             edge_max_m=float(max(lengths)),edge_mean_m=float(np.mean(lengths)),
             N_intact_min_kN=float(min(intact["axial"]))/1000,
             N_intact_max_kN=float(max(intact["axial"]))/1000,
             N_theory_kN=-P*R*float(np.mean(lengths))/(2*math.sqrt(3))/1000,
             M_max_intact_Nm=float(max(intact["moments"])),
             sigma_max_intact_Pa=float(max(intact["peak"])),rigid_reaction_norm_N=reaction,
             area_sum_planar_m2=float(sum(areas)),area_sum_spherical_m2=float(sum(sph)),cases=[])
    # Independently identify every edge orbit by edge length, its endpoint
    # valences and the unordered neighbour-length signature. No filed stress
    # or removed-member force is used to pick an edge.
    groups={}
    for k,(a,b) in enumerate(edges):
        signature=[]
        for i in [a,b]:
            signature.append(tuple(sorted(round(lengths[j],7) for j,e in enumerate(edges) if i in e)))
        key=(round(lengths[k],7),tuple(sorted(signature)))
        groups.setdefault(key,k)
    for key,k in groups.items():
        m=members[k]
        correction=coo_matrix((m["k"].ravel(),(np.repeat(m["ids"],12),np.tile(m["ids"],12))),shape=K.shape).tocsc()
        uu,react=solve(K-correction,F,rigid)
        result=stresses(uu,members,A,I,ro,k)
        neighbour=[j for j,e in enumerate(edges) if j!=k and any(i in e for i in edges[k])]
        ratio=np.abs(result["axial"]/intact["axial"])
        out["cases"].append(dict(edge_id=k,edge_nodes=edges[k].tolist(),edge_signature=repr(key),
          removed_N_kN=float(intact["axial"][k])/1000,neighbours=len(neighbour),
          neighbour_N_ratio_max=float(np.nanmax(ratio[neighbour])),
          N_ratio_max_anywhere=float(np.nanmax(ratio)),M_max_Nm=float(np.nanmax(result["moments"])),
          M_max_intact_Nm=out["M_max_intact_Nm"],sigma_max_Pa=float(np.nanmax(result["peak"])),
          sigma_max_intact_Pa=out["sigma_max_intact_Pa"],
          sigma_ratio=float(np.nanmax(result["peak"])/out["sigma_max_intact_Pa"]),
          tension_max_Pa=float(np.nanmax(result["tension"])),rigid_reaction_norm_N=react))
    if load=="radial_spherical":
        out["truss"]=truss_nullity(points,edges,A,E,next(iter(groups.values())))
    if load=="radial_spherical":
        save(f"FRAME-MESH-f{f}.json",dict(points_m=points.tolist(),triangles=tris.tolist(),edges=edges.tolist(),
             pressure_Pa=P,E_Pa=E,nu=nu,section_A_m2=A,section_I_m4=I,ro_m=ro,
             load="radial, one third of each spherical triangle area",
             rigid_mode_constraints="orthogonal free-body modes"))
    return out


def main():
    p3=json.loads((ROOT/"ARITHMETIC.json").read_text())["p3"]
    expected=json.loads((ROOT/"inputs/owner/DET.json").read_text())["frame"]
    output={}
    for load in ["normal_planar","radial_planar","radial_spherical","radial_equal"]:
        output[load]={}
        for f in [4,5]:
            value=run_frequency(f,p3,load);output[load][f"f{f}"]=value
            print(load,f,"N",value["N_intact_min_kN"],value["N_intact_max_kN"],
                  "stress ratios",min(x["sigma_ratio"] for x in value["cases"]),max(x["sigma_ratio"] for x in value["cases"]),flush=True)
    save("FRAME-RESULTS.json",output)
    # The pressure quadrature is under-specified in the filed card.
    # Keep all variants, and state the chosen reconstruction explicitly.
    for load,data in output.items():
        for key,value in data.items():
            compare(f"frame/{load}/{key}",{k:v for k,v in value.items() if k not in ["cases","truss"]},expected[key],rtol=3e-6,atol=1e-6)
            for i,row in enumerate(expected[key]["rigid_joint_cases"]):
                # Match a reported removed-force orbit only after all independent
                # orbit calculations. The geometry ambiguity remains recorded.
                chosen=min(value["cases"],key=lambda x:abs(x["removed_N_kN"]-row["removed_N_kN"]))
                compare(f"frame/{load}/{key}/case{i}",chosen,row,rtol=3e-5,atol=1e-5,
                        note="All independent edge orbits calculated first; comparison paired by removed-force class.")
    save("FRAME-CHECKS.json",CHECKS)
    save("FRAME-DIFFERENCES.json",[x for x in CHECKS if not x["pass_"]])


if __name__=="__main__":
    main()
