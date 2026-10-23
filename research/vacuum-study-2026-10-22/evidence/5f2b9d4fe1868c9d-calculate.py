"""Independent 036 calculation. Reads data, never imports predecessor executables."""
from pathlib import Path
import datetime
import json
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT / "INPUTS.json").read_text())
BX = brentq(lambda b: b**3+b-1, 0, 1, xtol=1e-15)
RHO = 1850.
MODE_NAMES = ["global", "face", "crimp", "crush", "wrinkle", "dimple", "joint"]
CHECKS = []

def check(name, ok, **details):
    CHECKS.append(dict(name=name, pass_=bool(ok), **details))
    if not ok:
        raise AssertionError((name, details))

class Model:
    def __init__(self, radius, route, mechanics, E, nu, wrinkle=.82, gamma=None, cores=None):
        self.R, self.route, self.mechanics = radius, route, mechanics
        self.E, self.nu, self.wrinkle, self.gamma = E, nu, wrinkle, gamma
        self.A = 4*math.pi*radius**2
        self.lift = I["R10"]["case"]["lift0_kg"]*(radius/10)**3
        self.cores = cores or I[f"R{radius}"]["cores"]
        if radius == 10:
            self.p = I["R10"]["case"]["p0_Pa"]
            self.reserve = I["R10"]["case"]["reserve_fixed_items_kg"]
            self.rt = next(x for x in I["R10"]["routes"] if x["id"] == route)
            self.eta = 1.
        else:
            sc, c = I["R20"]["scenario"], I["R20"]["case"]
            self.sc = sc
            self.p = c["p0_Pa"]*(1+sc["pressure_swing_fraction"])
            dry = self.lift*(1-sc["pressure_swing_fraction"])*c["T0_K"]/(c["T0_K"]+sc["temperature_rise_K"])
            moist = self.lift*((1-sc["pressure_swing_fraction"])-.378*sc["water_vapour_Pa"]/c["p0_Pa"])*c["T0_K"]/(c["T0_K"]+sc["temperature_rise_K"])
            self.reserve = self.lift-moist+.01*self.lift+self.A*(1000*sc["water_film_m"]+sc["contamination_kg_m2"])
            self.eta = sc["joint_efficiency"]
        self.available = self.lift-100-self.reserve

    def joint_mass(self, S, f, core):
        tf, tc = (1-f)*S/(2*self.A*RHO), f*S/(self.A*core["rho"])
        if self.R == 10:
            a, b = I["R10"]["panel"]["a_m"], I["R10"]["panel"]["b_m"]
            scarf = self.rt["seam"] == "scarf"
            overlap = 30*tf if scarf else 0.
            length = self.A*(1/(a-overlap)+1/(b-overlap))
            q = 2*self.A*(self.rt["bond_kg_m2"]+self.rt.get("primer_kg_m2",0))
            q += length*(.25*tc+.002+(2*tf*math.sqrt(901)*.070 if scarf else 0.))
        else:
            sc = self.sc
            length = self.A*(1/sc["panel_a_m"]+1/sc["panel_b_m"])
            q = 2*self.A*sc["film_kg_m2_per_interface"]
            q += length*(2*RHO*tf*sc["splice_width_m"]+
                         2*sc["film_kg_m2_per_interface"]*sc["splice_width_m"]+
                         1100*sc["core_gap_m"]*tc+1100*sc["sealant_area_m2"])
        return q

    def geometry(self, f, core):
        f = np.asarray(f)
        if self.R == 10:
            lo, hi = np.zeros_like(f), np.full_like(f,self.available/1.05,dtype=float)
            # Monotone mass closure; both skins, every physical joint, allowance retained.
            for _ in range(48):
                s=(lo+hi)/2
                q=self.joint_mass(s,f,core)
                too_heavy=s+np.maximum(.05*s,q)>self.available
                hi=np.where(too_heavy,s,hi);lo=np.where(too_heavy,lo,s)
            S=(lo+hi)/2
        else:
            q0=self.joint_mass(np.zeros_like(f),f,core)
            q1=self.joint_mass(np.ones_like(f),f,core)-q0
            sfloor=self.available/1.05
            S=np.where(q1*sfloor+q0<=.05*sfloor,sfloor,(self.available-q0)/(1+q1))
        tf=(1-f)*S/(2*self.A*RHO)
        tc=f*S/(self.A*core["rho"])
        return S,tf,tc

    def evaluate(self, f, core, Fcy, geom=None):
        S,tf,tc=self.geometry(f,core) if geom is None else geom
        h=tf+tc
        stress=self.p*self.R/(4*tf)
        s0=self.E*h/(self.R*math.sqrt(1-self.nu**2))
        crimp=h*h*core["Gc_Pa"]/(2*tf*tc)
        vc=s0/crimp
        kc=np.where(vc<=2,1-vc/4,1/vc)
        if self.mechanics=="full":
            gamma=.2+.4*np.minimum(vc,2)
        elif self.mechanics=="today":
            gamma=np.where(vc<2,.2,1.)
        else:
            gamma=np.zeros_like(vc)+self.gamma
        joint=(10e6*901/30/stress if self.R==10 and self.rt["seam"]=="scarf"
               else self.eta*Fcy/stress)
        values=np.stack([
            gamma*kc*s0/stress,Fcy/stress,crimp/stress,
            np.zeros_like(stress)+core["crush_Pa"]/(self.p/2),
            BX*self.wrinkle*np.sqrt(self.E*core["Ec_Pa"]*tf/tc)/stress,
            self.E/(1-self.nu**2)*(tf/core["s_cell_m"])**2/stress,joint])
        return dict(S=S,tf=tf,tc=tc,stress=stress,Vc=vc,Kc=kc,gamma=gamma,
                    values=values,least=values.min(axis=0))

    def point(self,f,core,Fcy):
        e=self.evaluate(f,core,Fcy)
        q=float(self.joint_mass(e["S"],f,core))
        vals=dict(zip(MODE_NAMES,map(float,e["values"])))
        S=float(e["S"])
        return dict(radius_m=self.R,route=self.route,mechanics=self.mechanics,E_Pa=self.E,
                    nu=self.nu,wrinkle=self.wrinkle,Fcy_Pa=Fcy,core=core["name"],fraction=float(f),
                    tf_m=float(e["tf"]),tc_m=float(e["tc"]),demand_Pa=float(e["stress"]),
                    required_Fcy_Pa=float(e["stress"])/self.eta,
                    gamma=float(e["gamma"]),Vc=float(e["Vc"]),Kc=float(e["Kc"]),
                    least_SF=min(vals.values()),modes=vals,
                    masses_kg=dict(structural=S,faces=(1-f)*S,core=f*S,physical_joining=q,
                                   charged_joining=max(q,.05*S),fixed_reserve=self.reserve,systems=100.,
                                   lift=self.lift,residual=S+max(q,.05*S)+self.reserve+100-self.lift),
                    tag="PROJECTION",overall_installed_SF=None)

    def optimum(self,Fcy,n=1601):
        grid=np.linspace(1e-7,1-1e-7,n)
        best=None
        for core in self.cores:
            q=self.evaluate(grid,core,Fcy)
            y=q["least"]
            candidates=[grid[0],grid[-1],grid[int(np.argmax(y))]]
            peaks=np.where((y[1:-1]>=y[:-2])&(y[1:-1]>=y[2:])&
                           ((y[1:-1]>y[:-2])|(y[1:-1]>y[2:])))[0]+1
            for j in peaks:
                opt=minimize_scalar(lambda f:-float(self.evaluate(f,core,Fcy)["least"]),
                    bounds=(grid[j-1],grid[j+1]),method="bounded",options={"xatol":1e-13})
                candidates.append(opt.x)
            if self.mechanics=="today":
                for j in np.where((q["Vc"][:-1]-2)*(q["Vc"][1:]-2)<0)[0]:
                    root=brentq(lambda f:float(self.evaluate(f,core,Fcy)["Vc"])-2,grid[j],grid[j+1])
                    candidates.extend([root-1e-10,root,root+1e-10])
            f=max(candidates,key=lambda f:float(self.evaluate(f,core,Fcy)["least"]))
            p=self.point(f,core,Fcy)
            if best is None or p["least_SF"]>best["least_SF"]:best=p
        return best

    def threshold(self,n=4001):
        """Minimize required strength on the feasible set of all strength-independent modes."""
        grid=np.linspace(1e-7,1-1e-7,n)
        independent=[0,2,3,4,5]
        if self.R==10 and self.rt["seam"]=="scarf":independent.append(6)
        best=None
        for core in self.cores:
            def constraint(f):
                return np.min(self.evaluate(f,core,1e15)["values"][independent],axis=0)-1
            values=self.evaluate(grid,core,1e15)["values"]
            roots=[grid[0],grid[-1]]
            # Individual crossings also recover zero-width feasible sets at held coefficients.
            for mode in independent:
                y=values[mode]-1
                for j in np.where(y[:-1]*y[1:]<0)[0]:
                    roots.append(brentq(lambda f:float(self.evaluate(f,core,1e15)["values"][mode])-1,
                                        grid[j],grid[j+1],xtol=2e-15))
            roots=sorted(roots)
            def need(f):return float(self.evaluate(f,core,1e15)["stress"])/self.eta
            candidates=[f for f in roots if constraint(f)>=-2e-9]
            for left,right in zip(roots[:-1],roots[1:]):
                if constraint((left+right)/2)<0:continue
                opt=minimize_scalar(need,bounds=(left,right),method="bounded",options={"xatol":1e-14})
                candidates.extend([left,right,opt.x])
            for f in candidates:
                Fcy=need(f)
                p=self.point(f,core,Fcy)
                if best is None or Fcy<best["Fcy_Pa"]:best=p
        return best

def main():
    models=[]
    for h in I["R10"]["held"]:
        models.append(("R10_"+h["route"]+"_held",Model(10,h["route"],"held",h["E_Pa"],h["nu"],
                     h["wrinkle"],h["gamma_constant"])))
        models.append(("R10_"+h["route"]+"_full",Model(10,h["route"],"full",293.6e9,.0752)))
        models.append(("R10_"+h["route"]+"_catalog_E_full",Model(10,h["route"],"full",290e9,.0752)))
    models += [
        ("R20_027_full",Model(20,"027_coupled_eta09","full",293.6e9,.33)),
        ("R20_SR200_nu0752",Model(20,"027_coupled_eta09","full",293.6e9,.0752)),
        ("R20_handbook_elastic",Model(20,"027_coupled_eta09","full",42.5e6*6894.757293168361,.10))]
    results={"tag":"PROJECTION","overall_installed_SF":None,"models":[],"held_geometry":[],"thickness":[]}
    for name,m in models:
        threshold=m.threshold()
        strengths=[m.optimum(x*1e6) for x in I["Fcy_sensitivities_MPa"]]
        results["models"].append(dict(id=name,cores_searched=len(m.cores),threshold=threshold,points=strengths))
        if threshold:
            below=m.optimum(threshold["Fcy_Pa"]*.9999)
            above=m.optimum(threshold["Fcy_Pa"]*1.0001)
            check(name+"_threshold_bracket",below["least_SF"]<1 and above["least_SF"]>=1-2e-7,
                  below_SF=below["least_SF"],above_SF=above["least_SF"])
        for p in strengths+([threshold] if threshold else []):
            check(name+"_mass",abs(p["masses_kg"]["residual"])<1e-5,
                  residual_kg=p["masses_kg"]["residual"])
        print(name,"threshold_MPa",None if threshold is None else threshold["Fcy_Pa"]/1e6,
              "SF345",strengths[6]["least_SF"],flush=True)
    # Reproduce the held predecessor geometries independently.
    for h in I["R10"]["held"]:
        p=h["point"];core=p["core"]
        m=Model(10,h["route"],"held",290e9,.0752,h["wrinkle"],h["gamma_constant"],[core])
        q=m.point(p["fraction"],core,345e6)
        check(h["route"]+"_028b_reproduction",abs(q["tf_m"]-p["tf_m"])<1e-11 and
              abs(q["tc_m"]-p["tc_m"])<1e-10 and abs(q["least_SF"]-1)<2e-7,
              sf=q["least_SF"],demand_Pa=q["demand_Pa"])
        results["held_geometry"].append(dict(id="R10_"+h["route"],point=q))
    p=I["R20"]["reference"];core=I["R20"]["selected_core"]
    m=Model(20,"027_coupled_eta09","full",293.6e9,.33,cores=[core])
    q=m.point(p["core_mass_fraction"],core,379.2e6)
    check("R20_027_reproduction",abs(q["least_SF"]-p["least_SF"])<2e-8 and
          abs(q["tf_m"]-p["tf_m"])<1e-11 and abs(q["tc_m"]-p["tc_m"])<1e-10,
          sf=q["least_SF"],demand_Pa=q["demand_Pa"])
    results["held_geometry"].append(dict(id="R20_027",point=q))
    payload=p["payload_at_SF1"]["point"]
    results["R20_payload_held"]=dict(payload_kg=payload["payload_kg"],tf_m=payload["tf_m"],
                                   face_demand_Pa=m.p*20/(4*payload["tf_m"]),
                                   required_Fcy_Pa=m.p*20/(4*payload["tf_m"]*.9))
    # Extra loss is separate from stock that has already been supplied etched.
    for entry in results["held_geometry"]:
        p=entry["point"]; t=p["tf_m"]
        for loss in [.1016e-3,.0254e-3]:
            results["thickness"].append(dict(id=entry["id"],additional_total_loss_m=loss,
                finished_m=t-loss,membrane_demand_Pa=p["demand_Pa"]*t/(t-loss),
                effective_Fcy_need_Pa=p["required_Fcy_Pa"]*t/(t-loss),
                face_SF_multiplier=(t-loss)/t,tag="PROJECTION"))
        tol=.1016e-3 if p["radius_m"]==10 else .1524e-3
        results["thickness"].append(dict(id=entry["id"],case="SR200 lower stock tolerance, if model gauge is nominal",
            nominal_m=t,minus_tolerance_m=tol,finished_m=t-tol,
            membrane_demand_Pa=p["demand_Pa"]*t/(t-tol),
            effective_Fcy_need_Pa=p["required_Fcy_Pa"]*t/(t-tol),
            face_SF_multiplier=(t-tol)/t,tag="PROJECTION",
            qualification="No extra etch deducted; final-gauge guarantee would replace this scenario."))
    # A bound requiring no core or physical joint mass.
    cap=(I["R10"]["case"]["lift0_kg"]-100-I["R10"]["case"]["reserve_fixed_items_kg"])/1.05
    tcap=cap/(2*4*math.pi*10**2*RHO)
    results["R10_zero_core_face_bound"]=dict(max_tf_m=tcap,Fcy_at_SF1_Pa=I["R10"]["case"]["p0_Pa"]*10/(4*tcap),
                                           SF255=255e6*4*tcap/(I["R10"]["case"]["p0_Pa"]*10))
    check("255_face_bound_reproduction",abs(results["R10_zero_core_face_bound"]["SF255"]-.958217295537760)<1e-9)
    # Strength cannot repair today's buckling/wrinkling envelope.
    today=[]
    for rad,route in [(10,"af015_scarf"),(20,"027_coupled_eta09")]:
        m=Model(rad,route,"today",290e9,.0752 if rad==10 else .33,.33)
        q=m.optimum(1e15)
        today.append(q)
        check(f"R{rad}_today_strength_alone_insufficient",q["least_SF"]<1,sf=q["least_SF"])
    results["today_infinite_strength_screens"]=today
    # The published Tsai-Wu polynomial uses F12*s1*s2, not 2*F12.
    A=3.521e-4+2.889e-4-2.726e-4
    B=2.394e-3+7.800e-4
    biax=(-B+math.sqrt(B*B+4*A))/(2*A)
    results["NASA4397_unqualified_polynomial_extrapolation"]=dict(compression_ksi=biax,
        compression_MPa=biax*6.894757293168361,
        qualification="Not an allowable: historical thick-sheet fit substitutes tensile/bending failure for missing biaxial yield.")
    results["validation"]=dict(checks=len(CHECKS),all_pass=all(x["pass_"] for x in CHECKS))
    (ROOT/"RESULTS.json").write_text(json.dumps(results,indent=2)+"\n")
    (ROOT/"VALIDATION.json").write_text(json.dumps(CHECKS,indent=2)+"\n")
    print(results["validation"],flush=True)

if __name__=="__main__":main()
