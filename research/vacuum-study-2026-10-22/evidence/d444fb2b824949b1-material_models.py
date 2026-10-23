"""Explicit virtual tube constructions; no unknown compression statistics imputed."""
import math
import numpy as np
from scipy.optimize import minimize_scalar

def lamina(E1,E2,G,nu):
    den=1-nu*nu*E2/E1
    return np.array([[E1/den,nu*E2/den,0],[nu*E2/den,E2/den,0],[0,0,G]])

def transform(Q,angle):
    c=math.cos(math.radians(angle));s=math.sin(math.radians(angle))
    # Engineering shear convention: local strains from global strains.
    T=np.array([[c*c,s*s,c*s],[s*s,c*c,-c*s],[-2*c*s,2*c*s,c*c-s*s]])
    return T.T@Q@T,T

def model(key,E1,E2,G,nu,rho,Xc=None,Xt2=None,S=None,layup=None,kind="composite",note=""):
    Q=lamina(E1*1e9,E2*1e9,G*1e9,nu)
    layup=layup or [(0,1.)]
    assert abs(sum(w for a,w in layup)-1)<1e-10
    Qb=sum(w*transform(Q,a)[0] for a,w in layup)
    compliance=np.linalg.inv(Qb)
    Ex=1/compliance[0,0];Ey=1/compliance[1,1];Gxy=Qb[2,2]
    # Global uniaxial compression of unit magnitude.
    strain=[address]([-1.,0,0])
    limits=[]
    ply_ratios=[]
    for angle,w in layup:
        stress=Q@transform(Q,angle)[1]@strain
        ply_ratios.append(dict(angle=angle,fraction=w,stress_per_unit_global_compression=stress.tolist()))
        if Xc is not None and stress[0]<0:limits.append(Xc*1e9/-stress[0])
        if Xt2 is not None and stress[1]>1e-12:limits.append(Xt2*1e9/stress[1])
        if S is not None and abs(stress[2])>1e-12:limits.append(S*1e9/abs(stress[2]))
    allowable=min(limits) if limits else None
    a=compliance
    def ratio(z):
        z2=z*z
        num=Qb[0,0]+2*(Qb[0,1]+2*Qb[2,2])*z2+Qb[1,1]*z2*z2
        den=a[1,1]+(2*a[0,1]+a[2,2])*z2+a[0,0]*z2*z2
        return math.sqrt(num/den)/math.sqrt(3)
    zlist=np.linspace(-10,10,401)
    vals=[ratio(math.exp(z)) for z in zlist]
    j=int(np.argmin(vals))
    lo=zlist[max(0,j-1)];hi=zlist[min(len(zlist)-1,j+1)]
    opt=minimize_scalar(lambda z:ratio(math.exp(z)),bounds=(lo,hi),method="bounded")
    shell=min(ratio(0),math.sqrt(Qb[1,1]/a[0,0])/math.sqrt(3),float(opt.fun))
    return dict(id=key,kind=kind,tag="QUESTIONABLE / PROJECTION",
        Eax_Pa=Ex,Ehoop_Pa=Ey,Gaxhoop_Pa=Gxy,nu_axhoop=-a[0,1]/a[0,0],
        density_kgm3=rho,ply_Xc_GPa=Xc,screen_compression_Pa=allowable,
        compression_weibull_m=None,complete_tube_characteristic_compression_Pa=None,
        qualified_allowable_Pa=None,qualified_structural_SF=None,
        Q_Pa=Qb.tolist(),layup=layup,ply_ratios=ply_ratios,
        lamina_Q_Pa=Q.tolist(),ply_transverse_tension_GPa=Xt2,ply_shear_GPa=S,
        local_classical_coefficient_Pa=shell,
        omits_transverse_compression_and_interlaminar_failure=kind=="composite",note=note)

def models():
    items=[]
    def iso(key,E,nu,rho,Xc=None,note=""):
        items.append(model(key,E,E,E/(2*(1+nu)),nu,rho,Xc,kind="isotropic",note=note))
    iso("041-reference",410,.14,3100,3.9,"041 assumed property set, calibration row only.")
    iso("Hexoloy-SA",430,.14,3100,3.9,"Saint-Gobain typical compression is neither a Weibull scale nor an allowable; E430 is current pinned sheet, unlike 041 E410.")
    iso("CVD-PureSiC-HR",462,.21,3210,None,"CoorsTek gives E/rho/nu; compression and m are blank. No CVD compression strength borrowed from sintered SiC.")
    iso("UltraSiC-sintered",410,.21,3150,3.5,"CoorsTek typical compression, not statistical allowable.")
    # These matrix and transverse constants are stated hypotheses, not products.
    for key,Ef,rhof in [("SCS6-epoxy",380,3080),("SCSUltra-epoxy",415,2890)]:
        items.append(model(key,.6*Ef+.4*3,6,4.2,.30,.6*rhof+.4*1200,
            note="Virtual 60 vol% axial fibre/epoxy tube. E follows Voigt mixing with assumed matrix E3GPa/rho1200; E2=6/G=4.2/nu=.30 are assumptions. Fibre tensile strengths excluded from compression."))
    # CMC property ranges are not a vendor-qualified P3 tube.
    items.append(model("HNS-MI-CMC-scenario",230,230,70,.20,2700,1.0,
        note="Virtual MI CMC: E230/rho2700/G70/nu.20 are design assumptions; 1GPa compression is a screening translation of GE's >1GPa hot-component averages (815–1316C), not RT tube data. m/size/allowable unknown."))
    items.append(model("Tyranno-SA-CVI-scenario",230,230,70,.20,2750,None,
        note="Virtual CVI tube: density2750 from Yang2003 bars; E230/G70/nu.20 assumed. Measured 597MPa and m10.2 are flexure, explicitly excluded from compression."))
    for key,E1,rho,Xc,Xt2,S in [
        ("M55J",338,1626,.890,.037,.068),
        ("K13D2U",.6*935+.4*3,1800,None,None,None),
        ("T700S",134,1560,1.450,.081,.136)]:
        for name,layup in [("UD",[(0,1.)]),
                          ("70-10-10-10",[(0,.7),(45,.1),(-45,.1),(90,.1)]),
                          ("50-20-20-10",[(0,.5),(45,.2),(-45,.2),(90,.1)])]:
            E2,G,nu=(6,4.2,.35) if key=="M55J" else (8,4.5,.3)
            note="Virtual homogenized balanced laminate (B=0,D=Qt^3/12); not a measured pultruded tube. "
            if key=="M55J":
                note+="Toray2025 composite E1/Xc/Xt90/S at Vf60%; E2/G/nu transferred from Steeves2015 model, different resin/fraction. Density mixes fibre1910 and assumed epoxy1200."
            elif key=="K13D2U":
                note+="Mitsubishi fibre E935/rho2200; E1/rho mix with Vf60% epoxy E3/rho1200. E2/G/nu assumed. No compression allowable or m found; fibre tension3.7GPa is not used."
            else:
                note+="Toray2025 composite E1/Xc/Xt90/S at Vf60%; E2/G/nu assumed; density mixes fibre1800 and assumed epoxy1200. Current Xc1450MPa, not older1470."
            items.append(model(key+"-"+name,E1,E2,G,nu,rho,Xc,Xt2,S,layup,note=note))
    iso("Al6061T6",68.3,.33,2700,.276,
        "Kaiser tube typical tensile yield276MPa used as symmetric J2 compression-yield projection. rho2700/nu.33 assumed standard nominal; not brittle Weibull rupture and not a compression allowable.")
    return items
