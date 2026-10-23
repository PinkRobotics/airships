#!/usr/bin/env python3
"""MAINLINE050 own account, atmospheric envelope and thermal implementation.

Retains the equations and declared material/thermal transfers of 040/048.
No predecessor module is imported or executed.
"""
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss,Legendre

B=Path(__file__).resolve().parent
P=json.loads((B/"inputs/040/INPUTS.json").read_text())
P0=P["case"]["p0_Pa"]; TREF=284.9; RHOREF=1.1672683307461802
LIFT0=4889.442150186961; RD=287.053; RV=461.5; GRAV=9.80665; LAPSE=.0065
SIGMA=5.670374419e-8; NU=.0768; ALPHAF=11.3e-6; ALPHAC=23.6e-6
RHOCORE=P["core"]["rho"]; GC=P["core"]["Gc_Pa"]; EC=P["core"]["Ec_Pa"]
CRUSH=P["core"]["crush_Pa"]; CELL=P["core"]["s_cell_m"]
KBIAX=.5*67e9*RHOCORE/2700; COREMIN=25*6894.757293168361
CURE=(200-32)*5/9+273.15; SCARF=30.34139731914874
FILM0=.030*.45359237/.3048**2; COATING=.0075752*1.10; PRIMER=.010
BETA=float(np.roots([1,0,1,-1])[2].real)
# Select the sole real root, independently of the order returned by NumPy.
BETA=next(float(x.real) for x in np.roots([1,0,1,-1]) if abs(x.imag)<1e-12)
Q70=.5*RHOREF*(70*.514444)**2
QGUST=.5*RHOREF*(35*.514444+35*.3048)**2
PMIN=P0*1.01+max(Q70,QGUST)
AXES=["gamma","Q","face_compression_and_E","film"]

def save(name,obj):
    def convert(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,np.generic):return x.item()
        raise TypeError(type(x).__name__)
    (B/name).write_text(json.dumps(obj,indent=2,default=convert,allow_nan=False)+"\n")

def es_water(t):
    """Buck (1981) saturation pressure, Pa; T in kelvin."""
    c=np.asarray(t)-273.15
    return 611.21*np.exp((18.678-c/234.5)*c/(257.14+c))

def es_ice(t):
    c=np.asarray(t)-273.15
    return 611.15*np.exp((23.036-c/333.7)*c/(279.82+c))

def atmosphere(z,offset,anomaly_hpa,rh):
    """Sea-level pressure anomaly; RH specified locally; constant e/p profile.

    Solve the implicit hydrostatic pressure because the local RH sets e/p.
    Heights are geopotential; local ambient T is ISA(z)+offset.
    """
    z,offset,anomaly_hpa,rh=np.broadcast_arrays(z,offset,anomaly_hpa,rh)
    ts=288.15+offset; t=ts-LAPSE*z; ps=101325+100*anomaly_hpa
    e=rh*es_water(t)
    p=ps*(t/ts)**(GRAV/(RD*LAPSE))
    for _ in range(12):
        p=ps*(t/ts)**(GRAV*(1-.378*e/p)/(RD*LAPSE))
    rho=(p-.378*e)/(RD*t)
    return {"T_K":t,"p_Pa":p,"e_Pa":e,"rho_kg_m3":rho,
            "pressure_load_Pa":np.maximum(1.01*P0,p)+max(Q70,QGUST)}

def inherited_thermal(radius,core,n=128,ta=TREF,day_sky=275,night_sky=260,
                      wind=2,alpha=.09,eps=.80):
    """Solve the inherited coupled skin balance, independently of 048 code."""
    core=np.atleast_1d(core)
    mu,w=leggauss(n)
    reyn=RHOREF*wind*2*radius/1.79e-5
    hf=(2+(.4*np.sqrt(reyn)+.06*reyn**(2/3))*.71**.4)*.0257/(2*radius)
    us=130*RHOCORE/2700/core[:,None]
    def surface(solar,sky):
        inside=np.full((len(core),n),ta)
        env=.5*(1+mu)*sky**4+.5*(1-mu)*ta**4
        sun=alpha*solar*np.maximum(mu,0)
        for iteration in range(500):
            mean=(inside@w/2)[:,None]
            mean4=(inside**4@w/2)[:,None]
            conduct=us+.8*SIGMA*mean**3
            new=inside.copy()
            for __ in range(20):
                qi=.2*SIGMA*(new**4-mean4); dqi=.8*SIGMA*new**3
                outside=new+qi/conduct
                delta=outside-ta
                hn=1.32*np.maximum(abs(delta),.05)**.25
                h=np.maximum(hf,hn)
                derivh=np.where((hn>hf)&(abs(delta)>.05),.25*h,0)
                residual=eps*SIGMA*(outside**4-env)+h*delta+qi-sun
                derivative=(4*eps*SIGMA*outside**3+h+derivh)*(1+dqi/conduct)+dqi
                correction=residual/derivative
                new-=correction
                if np.max(abs(correction))<1e-10:break
            error=float(np.max(abs(new-inside)))
            inside=new
            if error<2e-9:break
        else:raise ArithmeticError("thermal mean-field iteration failed")
        mean=(inside@w/2)[:,None];mean4=(inside**4@w/2)[:,None]
        qi=.2*SIGMA*(inside**4-mean4)
        outside=inside+qi/(us+.8*SIGMA*mean**3)
        residual=eps*SIGMA*(outside**4-env)+np.maximum(hf,1.32*np.maximum(abs(outside-ta),.05)**.25)*(outside-ta)+qi-sun
        temp=(outside+inside)/2
        deviations=temp-(temp@w/2)[:,None]
        coeff=np.stack([(2*j+1)/2*((deviations*Legendre.basis(j)(mu))@w)
                        for j in range(2,7)],axis=1)
        x=np.cos(np.linspace(0,np.pi,1441))
        angular=np.stack([(1-x*x)*Legendre.basis(j).deriv(2)(x)-x*Legendre.basis(j).deriv()(x)
                          for j in range(2,7)])
        curvature=np.max(abs(coeff@angular),axis=1)
        return outside,inside,curvature,{"iterations":iteration+1,
            "temperature_error_K":error,"energy_residual_W_m2":float(np.max(abs(residual)))}
    out,inside,kd,dd=surface(970,day_sky)
    night,ni,kn,dn=surface(0,night_sky)
    return {"tc_m":core,"gradient_K":np.maximum(np.max(abs(out-inside),axis=1),np.max(abs(night-ni),axis=1)),
            "curvature_temperature_K":np.maximum(kd,kn),"max_outer_K":np.max(out,axis=1),
            "min_outer_K":np.min(night,axis=1),"swing_K":np.max(out,axis=1)-np.min(night,axis=1),
            "day_diagnostics":dd,"night_diagnostics":dn}

class Account:
    def __init__(self,radius,table):
        self.r=radius;self.area=4*math.pi*radius**2;self.volume=4*math.pi*radius**3/3
        self.lift=LIFT0*(radius/10)**3
        self.table=table
        self.logcore=np.log(table["tc_m"])
        force=.47*Q70*math.pi*radius**2
        area=force/CRUSH; a=math.sqrt(area/math.pi)
        thickness=math.sqrt(3*1.33*force*math.log(a/.025)/(2*math.pi*276e6))
        self.pad={"force_N":force,"area_m2":area,"radius_m":a,"thickness_m":thickness,
                  "mass_kg":area*thickness*2700}

    def thermal(self,tc):
        logt=np.log(tc)
        return {k:np.interp(logt,self.logcore,self.table[k])
                for k in ("gradient_K","curvature_temperature_K","max_outer_K","min_outer_K")}

    def evaluate(self,tf,tc,pressure,mask=11,usage=1,thermal=None):
        tf,tc,pressure=np.broadcast_arrays(tf,tc,pressure)
        th=self.thermal(tc) if thermal is None else thermal
        eu=usage if mask&4 else 0
        e=290e9*(293.6/290)**eu
        strength=345e6*(379.2/345)**eu
        q=.33*(.82/.33)**(usage if mask&2 else 0)
        film=FILM0*(.5)**(usage if mask&8 else 0)
        h=tf+tc;sp=pressure*self.r/(4*tf)
        s0=e*h/(self.r*math.sqrt(1-NU**2));scr=GC*h*h/(2*tf*tc)
        vc=s0/scr;kc=np.where(vc<=2,1-vc/4,1/vc)
        g0=np.where(vc<2,.2,1);gf=.2+.4*np.minimum(vc,2)
        gamma=g0*(gf/g0)**(usage if mask&1 else 0)
        grad=1.002*e*ALPHAF*th["gradient_K"]/(2*(1-NU))
        bend=1.002*e*h*ALPHAF*th["curvature_temperature_K"]/(2*(1-NU**2)*self.r)
        coldexc=np.maximum(CURE-th["min_outer_K"],0)
        residual=1.002*KBIAX*(ALPHAC-ALPHAF)*coldexc*tc/(2*tf)
        strain=1.002*abs(ALPHAC-ALPHAF)*np.maximum(abs(CURE-th["min_outer_K"]),abs(CURE-th["max_outer_K"]))
        edge=strain*math.sqrt(2*KBIAX*GC)
        st=sp+grad+bend;sd=st+residual
        modes={"global_buckling":gamma*kc*s0/sp,"face_compression":strength/sd,
               "core_shear_crimping":scr/st,"core_crush":np.full(tf.shape,2*CRUSH)/pressure,
               "face_wrinkling":BETA*q*np.sqrt(e*EC*tf/tc)/sd,
               "intracell_dimpling":e*(tf/CELL)**2/(1-NU**2)/sd,
               "scarf_average_shear_screen":10e6*(SCARF+1/SCARF)/sd,
               "core_cell_wall_yield_screen":227.53e6/(1.2*67e9*strain),
               "thermal_core_interface_screen":COREMIN/edge}
        lap=SCARF*tf
        length=self.area*(1/(.6096-lap)+1/(1.8288-lap))
        mface=2*self.area*tf*1850;mcore=self.area*tc*RHOCORE
        mfilm=np.full(tf.shape,2*self.area*film)
        mscarf=2*length*np.hypot(lap,tf)*.07
        msplice=length*tc*.0005*500;mseal=length*.002
        actual=mfilm+mscarf+msplice+mseal
        mprimer=PRIMER*self.area;mcoat=COATING*self.area
        addedwater=.1*(.002*mfilm+.001*mcore+.01*mprimer+.01*mcoat+.01*(mscarf+msplice+mseal))
        bill={"faces":mface,"core":mcore,"charged_joining":np.maximum(actual,.05*(mface+mcore)),
              "coating":np.full(tf.shape,mcoat),"mooring_pad":np.full(tf.shape,self.pad["mass_kg"]),
              "gas":np.full(tf.shape,.01*self.lift),"systems":np.full(tf.shape,100.),
              "water":np.full(tf.shape,.1*self.area),"contamination":np.full(tf.shape,5*(self.r/10)**2),
              "absorbed_water":addedwater,"structural_primer":np.full(tf.shape,mprimer)}
        total=sum(bill.values())
        minimum=np.minimum.reduce(list(modes.values()))
        return {"modes":modes,"minimum_SF":minimum,"mass_kg":total,"bill_kg":bill,
                "tf_m":tf,"tc_m":tc,"pressure_Pa":pressure,
                "E_Pa":e,"strength_Pa":strength,"Q":q,"gamma":gamma,"gamma_full":gf,
                "thermal":th,"edge_Pa":edge,"gradient_Pa":grad,"bending_Pa":bend,"cure_Pa":residual,
                "joining":{"film":mfilm,"scarf":mscarf,"splice":msplice,"seal":mseal,"length_m":length}}

    def thin_face(self,tc,pressure,mask=11,usage=1):
        tc,pressure=np.broadcast_arrays(tc,pressure)
        th=self.thermal(tc)
        lower=np.full(tc.shape,1e-7);upper=np.full(tc.shape,min(.0195,.008*self.r/10))
        for _ in range(47):
            mid=(lower+upper)/2
            valid=self.evaluate(mid,tc,pressure,mask,usage,th)["minimum_SF"]>=1
            upper=np.where(valid,mid,upper);lower=np.where(valid,lower,mid)
        point=self.evaluate(upper,tc,pressure,mask,usage,th)
        point["mass_kg"]=np.where(point["minimum_SF"]>=1-1e-10,point["mass_kg"],np.inf)
        return point

    def optimum(self,pressures,mask=11,usage=1,grid=640):
        """Global log scan; refine the three best separate local minima."""
        pressures=np.atleast_1d(pressures).astype(float)
        logt=np.linspace(math.log(.0012*self.r/10),math.log(1.4*self.r/10),grid)
        trial=self.thin_face(np.exp(logt)[None,:],pressures[:,None],mask,usage)
        m=trial["mass_kg"]
        local=(m[:,1:-1]<=m[:,:-2])&(m[:,1:-1]<=m[:,2:])
        local=np.pad(local,((0,0),(1,1)),constant_values=True)&np.isfinite(m)
        order=np.argsort(np.where(local,m,np.inf),axis=1)[:,:3]
        best=np.argmin(m,axis=1)
        order=np.where(np.take_along_axis(np.where(local,m,np.inf),order,axis=1)<np.inf,order,best[:,None])
        left=logt[np.maximum(order-2,0)];right=logt[np.minimum(order+2,grid-1)]
        ratio=(math.sqrt(5)-1)/2
        a=right-ratio*(right-left);c=left+ratio*(right-left)
        fa=self.thin_face(np.exp(a),pressures[:,None],mask,usage)["mass_kg"]
        fc=self.thin_face(np.exp(c),pressures[:,None],mask,usage)["mass_kg"]
        for _ in range(32):
            choose=fa<=fc
            right=np.where(choose,c,right);left=np.where(choose,left,a)
            a=right-ratio*(right-left);c=left+ratio*(right-left)
            fa=self.thin_face(np.exp(a),pressures[:,None],mask,usage)["mass_kg"]
            fc=self.thin_face(np.exp(c),pressures[:,None],mask,usage)["mass_kg"]
        tc=np.exp((left+right)/2)
        scores=self.thin_face(tc,pressures[:,None],mask,usage)
        which=np.argmin(scores["mass_kg"],axis=1)
        chosen=tc[np.arange(len(pressures)),which]
        result=self.thin_face(chosen,pressures,mask,usage)
        result["grid_minimum_mass_kg"]=m[np.arange(len(pressures)),best]
        result["local_minimum_count"]=np.sum(local,axis=1)
        result["mask"]=mask;result["usage"]=usage
        return result

def scalar_record(account,result,index=0):
    def scalar(x):
        if isinstance(x,dict):return {k:scalar(v) for k,v in x.items()}
        if isinstance(x,np.ndarray):
            v=float(x[index]);return v if math.isfinite(v) else None
        return x
    return {"R_m":account.r,"area_m2":account.area,"volume_m3":account.volume,
            "reference_lift_kg":account.lift,"pad":account.pad,**scalar(result),
            "qualified_installed_hull_SF":None,"tag":"QUESTIONABLE / PROJECTION"}
