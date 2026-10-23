"""Discrete response and realized geometry for the 041 estimate card."""
import beam as b
import numpy as np
import math
from scipy.sparse import coo_matrix

LIFT=4889.44215019
SURFACE=4*math.pi*b.R*b.R


def configure(area=None,gyration=None,ro=None,wall=None):
    if area is not None:
        inertia=area*gyration*gyration
        ro=math.sqrt(2*gyration*gyration+area/(2*math.pi))
        ri2=2*gyration*gyration-area/(2*math.pi)
        if ri2<=0:raise ValueError("section has no hollow core")
        wall=ro-math.sqrt(ri2)
    elif ro is None:
        ro,wall=b.SELECTED["r_o_m"],b.SELECTED["wall_m"]
    b.RO,b.TW=ro,wall
    b.AREA=math.pi*(2*ro*wall-wall*wall)
    b.INERTIA=b.AREA*(ro*ro+(ro-wall)**2)/4
    b.EA=b.E*b.AREA;b.EI=b.E*b.INERTIA;b.GJ=b.E*b.INERTIA/(1+b.NU)
    b.PARAMS=np.array([b.EA,b.EI,b.GJ])
    b.CASE.update(r_o_m=ro,wall_m=wall)
    return {"r_o_m":ro,"wall_m":wall,"area_m2":b.AREA,"inertia_m4":b.INERTIA,
            "gyration_m":math.sqrt(b.INERTIA/b.AREA)}


def geometry(f):
    pts=f.x[:f.nmain]
    chords=np.linalg.norm(pts[f.edges[:,1]]-pts[f.edges[:,0]],axis=1)
    arcs=np.asarray(f.true_member_lengths)
    tri=pts[f.faces]
    sides=np.stack([np.linalg.norm(tri[:,j]-tri[:,(j+1)%3],axis=1) for j in range(3)],axis=1)
    planar_area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
    unit=tri/b.R
    determinant=np.einsum("ni,ni->n",unit[:,0],np.cross(unit[:,1],unit[:,2]))
    denominator=1+np.einsum("ni,ni->n",unit[:,0],unit[:,1])+np.einsum("ni,ni->n",unit[:,1],unit[:,2])+np.einsum("ni,ni->n",unit[:,2],unit[:,0])
    spherical_area=2*b.R*b.R*np.arctan2(abs(determinant),denominator)
    # Realized-cell extension of 022d's chosen cap: actual triangle inradius,
    # with curvature radius equal to the largest chord of that cell.
    inradius=2*planar_area/sides.sum(axis=1)
    rho=sides.max(axis=1)
    h=inradius**2/(rho+np.sqrt(rho**2-inradius**2))
    means=h*h*(rho-h/3)/(inradius*inradius)
    mean_sag=float(np.sum(spherical_area*means)/SURFACE)
    return {"frequency":f.frequency,"segments":f.segments,"nodes":f.nmain,
            "members":len(f.edges),"faces":len(f.faces),"DOF":f.ndof,
            "chord_min_m":float(chords.min()),"chord_mean_m":float(chords.mean()),"chord_max_m":float(chords.max()),
            "arc_min_m":float(arcs.min()),"arc_mean_m":float(arcs.mean()),"arc_max_m":float(arcs.max()),
            "total_arc_m":float(arcs.sum()),"spherical_cell_area_sum_m2":float(spherical_area.sum()),
            "planar_cell_area_sum_m2":float(planar_area.sum()),"cap_mean_sag_m":mean_sag,
            "sag_lift_debit_kg":3*LIFT*mean_sag/b.R,
            "sag_status":"PROJECTION: actual inradius/max-chord extension of circular-cap surrogate",
            "film_curvature_radius_max_m":float(rho.max()),
            "node_mass_kg":.02*f.nmain,"member_arc_lengths_m":arcs.tolist(),
            "cell_max_chords_m":rho.tolist(),"cell_spherical_areas_m2":spherical_area.tolist()}


def geometric_stiffness(f,N):
    L=f.length
    # Vectorized standard cubic-Hermite initial-compression stiffness.
    v=np.empty((len(L),4,4))
    v[:,0,:]=np.stack([36+0*L,3*L,-36+0*L,3*L],axis=1)
    v[:,1,:]=np.stack([3*L,4*L*L,-3*L,-L*L],axis=1)
    v[:,2,:]=np.stack([-36+0*L,-3*L,36+0*L,-3*L],axis=1)
    v[:,3,:]=np.stack([3*L,-L*L,-3*L,4*L*L],axis=1)
    v*=N[:,None,None]/(30*L[:,None,None])
    kg=np.zeros((len(L),12,12))
    for indices,sign in [([1,5,7,11],1),([2,4,8,10],-1)]:
        signs=np.array([1,sign,1,sign])
        for j,ii in enumerate(indices):
            for k,jj in enumerate(indices):kg[:,ii,jj]=v[:,j,k]*signs[j]*signs[k]
    return f.assemble(np.einsum("eji,ejk,ekl->eil",f.transforms,kg,f.transforms))


def force_arrays(f,u):
    forces,N=f.strains_forces(u)
    nm=len(f.edges);m=f.segments
    bending=np.maximum(np.linalg.norm(forces[:,[4,5]],axis=1),np.linalg.norm(forces[:,[10,11]],axis=1))
    endN=np.stack([N[:nm],N[-nm:]],axis=1)
    endM=np.stack([np.linalg.norm(forces[:nm,4:6],axis=1),np.linalg.norm(forces[-nm:,10:12],axis=1)],axis=1)
    endT=np.stack([abs(forces[:nm,3]),abs(forces[-nm:,9])],axis=1)
    result={"subelement_N":N,"subelement_M":bending,
            "subelement_member":f.member_of_beam.copy(),
            "member_max_N":N.reshape(m,nm).max(axis=0),
            "member_mean_N":(N.reshape(m,nm)*f.length.reshape(m,nm)).sum(axis=0)/f.length.reshape(m,nm).sum(axis=0),
            "member_max_M":bending.reshape(m,nm).max(axis=0),
            "joint_N":endN,"joint_M":endM,"joint_T":endT}
    return result


def response(f,number=6,film_K=None):
    Kbeam=f.linear_stiffness()
    K=Kbeam if film_K is None else Kbeam+film_K
    Q=f.rigid_basis()
    volume,g,Hp=f.pressure()
    inverse=b.GaugeInverse(K,Q)
    u=inverse.projected(-b.P*g)
    arrays=force_arrays(f,u)
    G=geometric_stiffness(f,arrays["subelement_N"])
    eigen,modes,residuals=b.eigen_buckling(K,G-b.P*Hp,Q,number=number)
    result={"section":{"area_m2":b.AREA,"inertia_m4":b.INERTIA,"r_o_m":b.RO,"wall_m":b.TW,
                       "gyration_m":math.sqrt(b.INERTIA/b.AREA),"E_Pa":b.E,"nu":b.NU},
            "geometry":geometry(f),"linear_lambda":eigen.tolist(),
            "relative_eigen_residuals":residuals,"pressure_fan_volume_m3":float(volume),
            "static_relative_residual":float(np.linalg.norm(K@u+b.P*g)/np.linalg.norm(b.P*g)),
            "max_translation_m":float(np.max(np.linalg.norm(u[:3*f.nn].reshape(-1,3),axis=1))),
            "film_material_stiffness_included":film_K is not None,
            "initial_moment_coupling_in_linear_buckling":False,
            "status":"QUESTIONABLE"}
    return result,arrays,u,modes
