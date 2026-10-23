"""Independent follow-up arithmetic, constitutive and provenance checks."""
from pathlib import Path
import json, math
import numpy as np
from scipy.optimize import minimize_scalar, brentq

ROOT=Path(__file__).resolve().parent


def acoustic_threshold(Ein,G):
    C=np.zeros((2,2,2,2));C[0,0,0,0]=Ein;C[1,1,1,1]=15000*.006894757293168361
    for i,j,k,l in ((0,1,0,1),(0,1,1,0),(1,0,0,1),(1,0,1,0)):C[i,j,k,l]=G
    angles=np.linspace(-np.pi/2,np.pi/2,2049)
    normals=np.column_stack([np.cos(angles),np.sin(angles)])
    def evaluate(shear,details=False):
        F=np.array([[1,shear],[0,1.]])
        strain=.5*([address](2));S=np.einsum("ijkl,kl->ij",C,strain)
        def single(angle):
            n=np.array([np.cos(angle),np.sin(angle)])
            B=np.einsum("ijkl,j,l->ik",C,n,n)
            A=F@[address]+np.eye(2)*(n@S@n)
            return float(np.linalg.eigvalsh(A)[0])
        B=np.einsum("ijkl,aj,al->aik",C,normals,normals)
        A=np.einsum("ij,ajk,lk->ail",F,B,F)+np.einsum("ai,ij,aj->a",normals,S,normals)[:,None,None]*np.eye(2)
        eig=np.linalg.eigvalsh(A)[:,0];i=int(np.argmin(eig))
        result=minimize_scalar(single,bounds=(angles[max(0,i-2)],angles[min(len(angles)-1,i+2)]),method="bounded",options={"xatol":1e-14})
        stress=F@[address]
        return dict(min_acoustic_eigenvalue=result.fun,angle_radians=result.x,
                    engineering_shear=shear,cauchy_shear_MPa=float(stress[0,1])) if details else result.fun
    shear=brentq(evaluate,0,1,xtol=1e-13)
    return evaluate(shear,True)


owner=json.loads((ROOT/"intake/OWNER-RESULTS.json").read_text())
check=json.loads((ROOT/"ARITHMETIC.json").read_text())
source=json.loads((ROOT/"intake/vacuum-mainline040-common-account-1020--RESULTS.json").read_text())
current=next(r for r in source["rows"] if r["id"]=="R30-ISA-actual-heavy70-vented")["least"]["least"]
out={"core_acoustic":[],"R30_040_exact":{}}
for ei in (.01,.024,1.):
    for label,G in (("W",6800*.006894757293168361),("L",15000*.006894757293168361)):
        out["core_acoustic"].append(dict(E_in_plane_MPa=ei,direction=label,**acoustic_threshold(ei,G)))
out["R30_040_exact"]=dict(tf_mm=current["geometry"]["tf_m"]*1000,
                         tc_mm=current["geometry"]["tc_m"]*1000,
                         nu=current["settings"]["nu"],gamma=current["properties"]["gamma"],
                         actual_load_kPa=current["load_pressure_Pa"]/1000,
                         pressure_stress_over_345=current["properties"]["pressure_face_stress_Pa"]/345e6)
ranges={}
for weather in ("ISA","optimistic"):
    vals=[r["least"]["least"]["properties"]["gamma"] for r in source["rows"]
          if r["R_m"]==30 and r["weather"]==weather and isinstance(r["least"].get("least"),dict)]
    if vals:ranges[weather]=[min(vals),max(vals)]
out["R30_gamma_ranges"]=ranges
out["r30_scaled"]={
    "Be_tf_mm":current["geometry"]["tf_m"]*1000/3,
    "Be_tc_mm":current["geometry"]["tc_m"]*1000/3,
    "face_5052_mm":current["geometry"]["tf_m"]*1000/3*290000/70300*math.sqrt((1-.33**2)/(1-current["settings"]["nu"]**2)),
    "cell_over_h":9.525/((current["geometry"]["tf_m"]+current["geometry"]["tc_m"])*1000/3),
    "cells_per_wavelength":owner["scaling"]["designs"]["R30 ISA (040)"]["groups"]["cells_per_wrinkle_wavelength"]/3,
    "full_curvature_cap_m_by_angular_similarity":[15,18],
    "note":"5m R10 Be cap angular similarity suggests 15m at R30; R30-similar 6m cap on R10 corresponds to 18m at R30. Neither establishes a global minimum."}
out["r30_scaled"]["core_5052_mm"]=(current["geometry"]["tf_m"]+current["geometry"]["tc_m"])*1000/3-out["r30_scaled"]["face_5052_mm"]
out["metrology"]=dict(minimum_waviness_mm=.0751,maximum_waviness_mm=.1288,
                      advertised_scan_mm=[.1,.3],scan_to_minimum_tolerance=[.1/.0751,.3/.0751])
out["scope"]={
    "typical_core_crush_is_post_peak":"35 psi is crush strength. Hexcel also lists bare 55/25 psi and stabilized 60/35 psi compressive strengths. C365 and D7336 measure different properties.",
    "full_similarity":False,"smallest_cap_demonstrated":False,
    "reason":"Only selected cap sizes and ideal uniform pressure/edge were compared; no modeled reinforcement, seams, thermal residuals, cell law or nonaxisymmetric modes."}
(ROOT/"PHYSICAL-CHECKS.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
print(json.dumps(out,indent=2))
