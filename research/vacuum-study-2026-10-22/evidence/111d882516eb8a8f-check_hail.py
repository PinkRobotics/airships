import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from checklib import *
from scipy.special import kv, j1, gamma
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
audit=Audit();mats=materials()
hail=read("HAIL.json");cache={};outputs=[]
rhoice=.00753/(math.pi/6*.025**3)
shi=json.loads((UP/"045/COMPUTE.json").read_text())["p2"]["calibration"]["shi"]["k_over_rho_v2"]

def Iint(a):
    z=np.exp(1j*math.pi/4)
    return -np.imag(z*kv(1,a*z))

def contact(mat,r,t,c):
    Q=mat["Q_Pa"];D=Q*t**3/12
    x,w=leggauss(256);theta=(x+1)*math.pi/4;weights=w/2
    cs=np.cos(theta)**2;sn=np.sin(theta)**2
    Dt=D[0,0]*cs*cs+2*(D[0,1]+2*D[2,2])*cs*sn+D[1,1]*sn*sn
    k=mat["Ehoop_Pa"]*t/r**2;ell=(Dt/k)**.25
    fac=c*ell*Iint(c/ell)/Dt
    Mx=float(weights@(fac*(D[0,0]*cs+D[0,1]*sn)))
    My=float(weights@(fac*(D[0,1]*cs+D[1,1]*sn)))
    strain=t/2*np.linalg.solve(D,np.array([Mx,My,0.]))
    ply=[mat["lamina_Q_Pa"]@strain_transform(a)@strain for a,f in mat["layup"]]
    # Exact extrema of D(theta), a quadratic in cos²(theta).
    d0=D[1,1];d1=2*(D[0,1]+2*D[2,2])-2*D[1,1]
    d2=D[0,0]-2*(D[0,1]+2*D[2,2])+D[1,1]
    cand=[d0,d0+d1+d2]
    if d2 and 0< -d1/(2*d2)<1:cand.append(d0-d1*d1/(4*d2))
    return dict(Mx_per_pressure_m2=Mx,My_per_pressure_m2=My,
        shell_surface_axial_per_pressure=6*Mx/t**2,shell_surface_hoop_per_pressure=6*My/t**2,
        max_homogenized_tensile_stress_per_pressure=6*max(Mx,My)/t**2,
        ell_minmax_m=[(min(cand)/k)**.25,(max(cand)/k)**.25],ply=ply)

# Independent real-axis integration checks the complex-Bessel evaluation.
for a in [.25,.5,1.,2.,4.,8.]:
    num=quad(lambda u:j1(a*u)*u*u/(u**4+1),0,1,epsabs=1e-10)[0]
    tail,error=quad(lambda u:j1(a*u)*u*u/(u**4+1),1,20000,epsabs=2e-8,limit=24000)
    num+=tail
    audit.check(f"integral/{a}","quadrature_error_within_request",True,error<=2e-8)
    audit.check(f"integral/{a}","I",float(Iint(a)),num,rtol=2e-5,atol=2e-8)
index={}
for i,row in enumerate(hail["rows"]):
    mat=mats[row["material"]];r=row["radius_m"];t=row["wall_m"];c=row["patch_radius_m"]
    key=(mat["id"],r,t,c)
    if key not in cache:cache[key]=contact(mat,r,t,c)
    unit=cache[key];pflow=rhoice*row["velocity_m_s"]**2;pshi=shi*pflow
    ss=unit["max_homogenized_tensile_stress_per_pressure"]
    stress={"flow":ss*pflow,"Shi":ss*pshi}
    sx=unit["shell_surface_axial_per_pressure"]*pshi
    sy=unit["shell_surface_hoop_per_pressure"]*pshi
    vm=math.sqrt(sx*sx+sy*sy-sx*sy)
    calc=dict(p_flow_Pa=pflow,p_Shi_Pa=pshi,stress_flow_Pa=stress["flow"],stress_Shi_Pa=stress["Shi"],
      hail_only_von_Mises_Shi_Pa=vm,Al_hail_only_yield_SF=.276e9/vm if mat["id"]=="Al6061T6" else None,
      measured_member_break_probability=None,identified_probability_bounds=[0,1])
    name=f"hail[{i}]/{mat['id']}/{row['reserve']}/{row['section_policy']}/D{row['diameter_m']}"
    audit.fields(name,row,calc,atol=1e-7)
    audit.fields(name,row["unit_contact"],{k:v for k,v in unit.items() if k not in ["ply","ell_minmax_m"]})
    audit.fields(name,row["unit_contact"],{"ell_minmax_m":unit["ell_minmax_m"]},rtol=2e-5,atol=1e-10)
    for j,ply in enumerate(unit["ply"]):
        for k,s in enumerate(ply):
            audit.check(name,f"ply[{j}].stress_per_contact[{k}]",row["unit_contact"]["ply"][j]["stress_per_contact_Pa"][k],float(s),atol=1e-8)
            audit.check(name,f"ply[{j}].Shi_stress[{k}]",row["ply_damage_screen_Shi"][j]["surface_stress_Pa"][k],float(s*pshi),atol=1e-5)
            audit.check(name,f"ply[{j}].Shi_stress_magnitude[{k}]",row["ply_damage_screen_Shi"][j]["surface_stress_Pa"][k],float(abs(s*pshi)),atol=1e-5)
        limits=[mat["ply_Xc_GPa"],mat["ply_transverse_tension_GPa"],mat["ply_shear_GPa"]]
        for k,cap in enumerate(limits):
            util=None if cap is None else abs(float(ply[k]*pshi))/(cap*1e9)
            audit.check(name,f"ply[{j}].utilization[{k}]",row["ply_damage_screen_Shi"][j]["maximum_stress_utilization"][k],util,atol=1e-10)
    for j,pop in enumerate(row["sourced_population_surrogates"]):
        s0=pop["scale_Pa"];m=pop["m"]
        # Source-derived scales for converted published means.
        if pop["population"]=="Hexoloy SA 4-pt bars":s0=380e6/gamma(1+1/10)
        if "Tyranno" in pop["population"]:s0=597e6/gamma(1+1/10.2)
        audit.check(name,f"source_surrogate[{j}].scale",pop["scale_Pa"],float(s0))
        audit.check(name,f"source_surrogate[{j}].Pf",pop["uncalibrated_045_Pbreak_surrogate"],
                    probability([stress[pop["pressure_model"]]],m,s0),atol=1e-15)
    for j,pop in enumerate(row["explicit_common_fit_scenarios"]):
        audit.check(name,f"common_fit[{j}].Pf",pop["conditional_probability_if_contact_fit_applies"],
          probability([stress[pop["pressure_model"]]],pop["m"],pop["assumed_contact_scale_Pa"]),atol=1e-15)
    index[(row["material"],row["reserve"],row["section_policy"],row["diameter_m"])]=stress
    outputs.append(dict(index=i,**calc,unit_contact=unit))
for i,row in enumerate(hail["target_rows"]):
    ss=index[row["material"],row["reserve"],row["section_policy"],row["diameter_m"]][row["pressure_model"]]
    target=ss/(-math.log1p(-row["target_conditional_strike_probability"]))**(1/row["m"])
    audit.check(f"hail-target[{i}]","required_matching_contact_test_scale_Pa",row["required_matching_contact_test_scale_Pa"],target)
dump("INDEPENDENT-HAIL.json",outputs)
audit.save("HAIL-CHECK.json")
