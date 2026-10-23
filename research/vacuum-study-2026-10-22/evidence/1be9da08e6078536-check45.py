"""Independent CHECK-045 arithmetic. No owner or predecessor program imports."""
from pathlib import Path
import json
import math
import numpy as np
from scipy.optimize import brentq, minimize
from scipy.special import j0, j1, jn_zeros, gamma as Gamma, kv

ROOT = Path(__file__).resolve().parent
PI = math.pi
R = 10.
P = 95460.83791390514
B = 4889.442150186961
AREA = 4*PI*R**2
VOLUME = 4*PI*R**3/3
RGAS = 287.05287
G = 9.80665
NU_BE = .0752
E_BE = 290e9
RHO_BE = 1850.
SIGMA_Y = 345e6
CRUSH = 241000.
RHO_CORE = 16.01846337396
EC = 15000*6894.757293168
GC = 6800*6894.757293168
RESERVE = 411.2989440716474
FACE_LIMIT = 10e6*901/30
BEAM_E = 410e9
CHECKS = []
EXTRA = {}


def save(name, data):
    (ROOT/name).write_text(json.dumps(data, indent=2, allow_nan=False)+"\n")


def check(path, got, expected, rtol=2e-7, atol=1e-10, note=""):
    if isinstance(got, np.generic):
        got = got.item()
    if isinstance(expected, (float, int)) and not isinstance(expected, bool) and isinstance(got, (float, int)):
        difference = got-expected
        ok = abs(difference) <= atol+rtol*abs(expected)
    else:
        difference = None
        ok = got == expected
    CHECKS.append(dict(path=path, owner=expected, independent=got,
                       difference=difference, relative_tolerance=rtol,
                       absolute_tolerance=atol, pass_=bool(ok), note=note))
    return got


def compare(prefix, got, expected, rtol=2e-7, atol=1e-10, note=""):
    if isinstance(got, dict):
        for k, v in got.items():
            if k in expected:
                compare(prefix+"/"+str(k), v, expected[k], rtol, atol, note)
    elif isinstance(got, list):
        for i, v in enumerate(got):
            if i < len(expected):
                compare(prefix+"/"+str(i), v, expected[i], rtol, atol, note)
    else:
        check(prefix, got, expected, rtol, atol, note)


def joining(tf, tc):
    length = AREA*(1/(.6096-30*tf)+1/(1.8288-30*tf))
    bond = .015*.45359237/.09290304
    return 2*AREA*bond+length*(2*tf*math.sqrt(901)*.070+.0005*tc*500+.002)


def geometry_p2(tf, k=1., extra=0.):
    def balance(tc):
        structural = AREA*(2*RHO_BE*tf+k*RHO_CORE*tc)
        return structural+max(.05*structural, joining(tf, tc))+100+RESERVE+extra-B
    if balance(0.) >= 0:
        return None
    tc = brentq(balance, 0., .5, xtol=1e-15)
    if tc < 1e-9:
        return None
    structural = AREA*(2*RHO_BE*tf+k*RHO_CORE*tc)
    # Reconstructed density sensitivity: E_c and G_c scale linearly with
    # density. This additional scaling is not stated in the owner's CARD.
    h = tf+tc
    sig = P*R/(4*tf)
    sig0 = E_BE*h/(R*math.sqrt(1-NU_BE**2))
    crimp = h*h*(k*GC)/(2*tf*tc)
    vc = sig0/crimp
    kc = 1-vc/4 if vc <= 2 else 1/vc
    gn = sig/(kc*sig0)
    gf = .2+.4*min(vc, 2)
    wb = brentq(lambda x:x*x*x+x-1, 0, 1)
    wn = sig/(wb*math.sqrt(E_BE*(k*EC)*tf/tc))
    usage = max(0., math.log(gn/.2)/math.log(gf/.2), math.log(wn/.33)/math.log(.82/.33))
    return dict(tf_m=tf, tc_m=tc, sigma_m_Pa=sig, gamma_need=gn,
                gamma_full=gf, Q_need=wn, usage=usage, Vc=vc,
                others=dict(face_345=SIGMA_Y/sig, crimp=crimp/sig,
                            crush=(35*6894.757293168)/(P/2),
                            dimpling=E_BE*(tf/.009525)**2/((1-NU_BE**2)*sig),
                            scarf_screen=FACE_LIMIT/sig),
                S_kg=structural, J_kg=joining(tf, tc))


LAM_C = float(jn_zeros(1, 1)[0])
LAM_S = brentq(lambda x:x*j0(x)-(1-NU_BE)*j1(x), 1., 3.)


def p2_opt(k=1., extra=0., patch_diameter=0., edge="clamped"):
    lc = LAM_C if edge == "clamped" else LAM_S
    minimum_tf = P*R/(4*FACE_LIMIT)
    if patch_diameter:
        minimum_tf = max(minimum_tf, ((P*R/4)*(patch_diameter/2)**2*12*(1-NU_BE**2)/(lc**2*E_BE))**(1/3))
    # Scarf sets the optimum for the requested witnesses. Check the entire
    # remaining feasible thickness interval, then refine any sampled minima.
    upper = (B-100-RESERVE-extra)/(2*RHO_BE*AREA*1.05)
    if minimum_tf >= upper or geometry_p2(minimum_tf,k,extra) is None:
        return None
    grid=np.linspace(minimum_tf,upper,501)
    vals=[geometry_p2(x,k,extra) for x in grid]
    vals=[v for v in vals if v is not None]
    return min(vals, key=lambda v:v["usage"])


P2 = p2_opt()
TF = P2["tf_m"]
TC = P2["tc_m"]
N = P*R/4
DF = E_BE*TF**3/(12*(1-NU_BE**2))
Q0 = P-2*N/R
TEQ = math.sqrt(3)*(TF+TC)
WIDTH = math.sqrt(R*TEQ)/(12*(1-.33**2))**.25
LAMBDA_FREE = ((P2["gamma_need"]-.036)/.964)**(-1/1.23)-1
DEPTH_EQ3 = -math.log((P2["gamma_need"]-.45)/.51)/3.88*TEQ
DEPTH_LEE = (.25/(P2["gamma_need"]-.068)-.28)*TEQ


def growth(b, edge="clamped", strength=CRUSH, fraction=1.):
    lc = LAM_C if edge == "clamped" else LAM_S
    excess = fraction*N-lc*lc*DF/b**2
    if excess <= 0:
        return None
    return (strength-fraction*Q0)*b*b/(4*excess)


def global_depth(b):
    lam=b/WIDTH
    if lam<LAMBDA_FREE:
        return None
    return DEPTH_EQ3 if lam<1 else DEPTH_LEE


def spread(a, tf=TF, sy=SIGMA_Y, crush=CRUSH):
    return a+tf/2*math.sqrt(sy/crush)


def soft_depth(a, pressure=None, energy=None, tf=TF, sy=SIGMA_Y, crush=CRUSH):
    b=spread(a,tf,sy,crush)
    if energy is not None:
        cc=PI*crush*b*b
        aa=PI*sy*tf
        d=2*energy/(cc+math.sqrt(cc*cc+4*aa*energy))
    else:
        d=max(0., (pressure*a*a-crush*b*b)/(2*sy*tf))
    return d,b


def hard_depth(energy, radius=.0127, tf=TF, sy=SIGMA_Y, crush=CRUSH):
    def bb(d):
        a=math.sqrt(max(0.,2*radius*min(d,radius)-min(d,radius)**2))
        return spread(a,tf,sy,crush)
    def crushed_volume(d):
        z=min(d,radius)
        a=math.sqrt(max(0.,2*radius*z-z*z))
        offset=tf/2*math.sqrt(sy/crush)
        # Integrate the growing contact area; charging its final footprint
        # through the full penetration overstates the work.
        int_a=.5*((z-radius)*a+radius**2*math.asin((z-radius)/radius)+PI*radius**2/2)
        integral=radius*z*z-z**3/3+2*offset*int_a+offset**2*z
        return PI*(integral+(d-z)*(radius+offset)**2)
    d=brentq(lambda x:PI*sy*tf*x*x+crush*crushed_volume(x)-energy,0.,1.,xtol=1e-15)
    return d,bb(d)


def score(d,b,cap=False):
    out={"depth_m":min(d,TC) if cap else d,"crushed_diameter_m":2*b if d>0 else 0.}
    if d>0:
        out["face_membrane_strain"]=.5*(d/b)**2
    for edge in ["clamped","ss"]:
        lim=growth(b,edge)
        out[edge]="no crush" if d==0 else ("grows" if lim is not None and d>lim else "stable")
        if d>0:
            out[edge+"_threshold_m"]=lim
    return out


def p3point(s,ro,lam,film_allowable=1.74e9,extra=0.,minwall=0.):
    length=2*R*math.asin(s/(2*R))
    faces=AREA/(math.sqrt(3)*s*s/4)
    members=1.5*faces; nodes=faces/2+2
    force=P*R*s/(2*math.sqrt(3))
    radius=s
    b=s/(2*math.sqrt(3))
    h=radius-math.sqrt(radius*radius-b*b)
    mean=h*h*(radius-h/3)/(b*b)
    sag=3*B*mean/R
    gauge=max(12e-6,lam*P*s/(2*film_allowable))
    mfilm=AREA*1560*gauge
    cj=1550/(2*PI*1470e6*28.9e6)
    mjoint=2*members*cj*(lam*force)**2/ro
    mnodes=.02*nodes
    mtube=B-.05*B-100-sag-extra-mfilm-mjoint-mnodes
    if mtube<=0:return None
    a=mtube/(3100*members*length)
    if a>=PI*ro*ro:return None
    ri=math.sqrt(ro*ro-a/PI);wall=ro-ri
    inertia=PI*(ro**4-ri**4)/4
    glocal=.099+.901*math.exp(-math.sqrt(ro/wall)/16)
    ne=PI*PI*BEAM_E*inertia/length**2
    mode=dict(compression=3.9e9*a/force,euler=ne/force,
              local=glocal*.6*BEAM_E*wall/ro*a/force,
              film=2*film_allowable*gauge/(P*s),
              global_=.2*4*math.sqrt(1.5)*BEAM_E*math.sqrt(inertia*a)/(s*R*R*P))
    mode["global"]=mode.pop("global_")
    def perry(q):
        mom=q*force*length/1000/(1-q*force/ne)
        return q*force/a+mom*ro/inertia-3.9e9
    mode["perry"]=brentq(perry,0,ne/force*(1-1e-12))
    wave=PI*((9/8)*inertia/a*R*R)**.25
    return dict(s=s,L=length,ro=ro,t=wall,A=a,I=inertia,N=force,members=members,nodes=nodes,
                m_tube=mtube,m_film=mfilm,m_joint=mjoint,m_nodes=mnodes,sag=sag,
                lam=lam,half_over_L=wave/length,gamma_local=glocal,modes=mode,
                film_stress_Pa=P*s/(2*gauge),film_line_load_N_per_m=P*s/2,
                ply_fibre_stress_Pa=P*s/gauge,bay_area_m2=math.sqrt(3)*s*s/4,
                stress_axial_Pa=force/a,projected_tube_cover_fraction=members*s*2*ro/AREA,
                tube_length_per_m2=members*s/AREA)


def p3opt(allowable=1.74e9,extra=0.,minwall=0.):
    def con(x):
        s,ro,lam=np.exp(x)
        v=p3point(s,ro,lam,allowable,extra,minwall)
        if v is None:return np.full(9,-1e4)
        return np.array([v["modes"][k]/lam-1 for k in ["compression","euler","local","global","perry"]]+
                        [v["half_over_L"]-1,(v["t"]-minwall)/.001, s/(3*ro)-1, 1.])
    sols=[]
    for start in [[3.17,.1375,1.258],[2.2,.11,.85],[1.7,.05,.4],[.8,.025,.1],[4.,.18,1.]]:
        fit=minimize(lambda x:-x[2],np.log(start),method="SLSQP",
                     bounds=list(zip(np.log([.4,.003,.001]),np.log([8.,.25,5.]))),
                     constraints=[{"type":"ineq","fun":con}],
                     options={"maxiter":1000,"ftol":3e-12})
        if np.min(con(fit.x))>=-1e-7:
            v=p3point(*np.exp(fit.x),allowable,extra,minwall)
            sols.append(v)
    return max(sols,key=lambda v:v["lam"]) if sols else None


def main():
    c=json.loads((ROOT/"inputs/owner/COMPUTE.json").read_text())
    d=json.loads((ROOT/"inputs/owner/DET.json").read_text())
    P2.update(teq_m=TEQ,R_over_teq=R/TEQ,length_scale_m=math.sqrt(R*TEQ),
              width_lambda1_m=WIDTH,classical_wavelength_m=2*PI*WIDTH,
              lambda_free=LAMBDA_FREE,width_free_m=WIDTH*LAMBDA_FREE,
              depth_allow_eq3_lambda1_m=DEPTH_EQ3,depth_allow_lee_envelope_m=DEPTH_LEE,
              lee_x_at_need=DEPTH_LEE/TEQ,eq3_x_at_need=DEPTH_EQ3/TEQ)
    compare("DET/p2",P2,d["p2"])
    base={"N_N_per_m":N,"D_face_Nm":DF,"q0_Pa":Q0,"crush_Pa":CRUSH,
          "bare_Pa":379000.,"crush_scatter":.2,
          "patch":{e:{"D_crit_m":2*l*math.sqrt(DF/N)} for e,l in [("clamped",LAM_C),("ss",LAM_S)]},
          "hole_edge":{"elastic_edge_stress_Pa":2*P2["sigma_m_Pa"],
                       "factor_on_345":345e6/(2*P2["sigma_m_Pa"]),
                       "plastic_ring_over_hole_radius":345e6/(2*(345e6-P2["sigma_m_Pa"]))}}
    compare("COMPUTE/p2",base,c["p2"])
    for i,row in enumerate(c["p2"]["growth"]):
        b=row["b_m"]
        vals={e+"_"+k+"_m":growth(b,e,strength) for e in ["clamped","ss"] for k,strength in [("typ",CRUSH),("min",.8*CRUSH)]}
        compare(f"COMPUTE/p2/growth/{i}",vals,row)
    for i,row in enumerate(d["p2"]["depth_vs_width"]):
        lam=row["r0_m"]/WIDTH
        vals=dict(lambda_=lam,plateau=.964/(1+lam)**1.23+.036,
                  depth_allowed_m=global_depth(row["r0_m"]),unlimited=global_depth(row["r0_m"]) is None)
        vals["lambda"]=vals.pop("lambda_")
        compare(f"DET/p2/depth_vs_width/{i}",vals,row)
    for i,row in enumerate(c["p2"]["undetected"]):
        b=row["diameter_m"]/2
        vals=dict(lambda_if_r0_is_half_width=b/WIDTH,global_allowed_m=global_depth(b),
                  growth_clamped_m=growth(b),growth_ss_m=growth(b,"ss"))
        compare(f"COMPUTE/p2/undetected/{i}",vals,row)
    density=.00753/(PI*.025**3/6)
    check("COMPUTE/threats/rho_ice",density,c["threats"]["rho_ice"])
    hails=[]
    for i,(dia,vel) in enumerate(zip([.025,.035,.045,.055,.065,.075],[23,27.2,30.7,33.9,36.7,39.5])):
        mass={.025:.00753,.045:.0439,.075:.203}.get(dia,PI*dia**3*density/6)
        item=dict(D_m=dia,v_m_s=vel,m_kg=mass,E_J=mass*vel**2/2,rho_v2_Pa=density*vel**2)
        compare(f"COMPUTE/threats/hail_iec/{i}",item,c["threats"]["hail_iec"][i])
        hails.append(item)
    hails.append(dict(D_m=.0508,v_m_s=105*.3048,E_J=32.1193,rho_v2_Pa=density*(105*.3048)**2))
    compare("COMPUTE/threats/design_hail",hails[-1],c["threats"]["design_hail"])
    # Shi's tabulated 3 mm-plate energy fraction applied to its representative
    # 64.84 J / 0.480 mm example: effective force = work / travel.
    qeff=.0655*64.84/(PI*(.0508/2)**2*.000480)
    kshi=qeff/(density*46.88**2)
    compare("COMPUTE/p2/calibration/shi",dict(q_eff_Pa=qeff,k_over_rho_v2=kshi),c["p2"]["calibration"]["shi"])
    for i,hail in enumerate(hails):
        row=c["p2"]["threats"][i]
        a=hail["D_m"]/2
        b=spread(a)
        check(f"COMPUTE/p2/threats/{i}/lambda",b/WIDTH,row["lambda"])
        for key,q,energy in [("fluid rho v2",hail["rho_v2_Pa"],None),
                             ("Shi-calibrated k rho v2",kshi*hail["rho_v2_Pa"],None),
                             ("all energy to the panel",None,hail["E_J"])]:
            dent,bb=soft_depth(a,q,energy)
            vals=score(dent,bb)
            if q is not None: vals["q_Pa"]=q
            else:vals["E_J"]=energy
            compare(f"COMPUTE/p2/threats/{i}/readings/{key}",vals,row["readings"][key])
    for i,energy in enumerate([5.42327,30.,35.,135.582]):
        dent,b=hard_depth(.8*energy)
        row=c["p2"]["threats"][i+7]
        check(f"COMPUTE/p2/threats/{i+7}/lambda",b/WIDTH,row["lambda"])
        for key,factor in [("80 percent absorbed",1.),("depth x2 (Clarke band)",2.)]:
            compare(f"COMPUTE/p2/threats/{i+7}/readings/{key}",score(dent*factor,b),row["readings"][key],
                    rtol=5e-6,note="Exact analytic contact-work integral; owner hard-contact quadrature differs by about one part per million.")
    for i,(mass,vel) in enumerate([(4*.4535925,20.),(4*.4535925,38.00554),(8*.4535925,20.),(8*.4535925,38.00554)]):
        dia=(6*mass/(PI*944))**(1/3);energy=mass*vel*vel/2
        vals=dict(m_kg=mass,v_m_s=vel,E_J=energy,D_m=dia)
        compare(f"COMPUTE/threats/birds/{i}",vals,c["threats"]["birds"][i])
        row=c["p2"]["threats"][i+11]; b=spread(dia/2)
        check(f"COMPUTE/p2/threats/{i+11}/lambda",b/WIDTH,row["lambda"])
        for key,q,en in [("fluid rho v2",944*vel*vel,None),("all energy to the panel",None,energy)]:
            dent,bb=soft_depth(dia/2,q,en)
            out=score(dent,bb,cap=en is not None)
            if en is not None:out.update(E_J=en,bottoms_out=dent>TC)
            compare(f"COMPUTE/p2/threats/{i+11}/readings/{key}",out,row["readings"][key])
    # This mass uses the independent standard-atmosphere value, as the
    # author's threat table did, rather than the slightly different COMMON B.
    pa=101325*(1-.0065*500/288.15)**(G/(RGAS*.0065))
    rho500=pa/(RGAS*(288.15-.0065*500))
    meff=1.5*rho500*VOLUME
    for i,vel in enumerate([.914,3.048]):
        energy=.5*meff*vel**2;dent=energy/(PI*.25**2*CRUSH)
        compare(f"COMPUTE/threats/mooring/{i}",dict(v_m_s=vel,m_eff_kg=meff,E_J=energy),c["threats"]["mooring"][i])
        row=c["p2"]["threats"][i+15]
        vals=score(dent,.25);vals.update(E_J=energy,bottoms_out=dent>TC,global_allowed_m=global_depth(.25))
        compare(f"COMPUTE/p2/threats/{i+15}/readings/core crush only",vals,row["readings"]["core crush only"])
    for i,(mass,vel) in enumerate([(.002,130*.3048),(9*.45359237,50*.3048),(9*.45359237,80*.3048)]):
        compare(f"COMPUTE/threats/debris/{i}",dict(m_kg=mass,v_m_s=vel,E_J=.5*mass*vel**2),c["threats"]["debris"][i])
    for sc in [.4e6,.9e6]:
        dent,b=hard_depth(1.57,tf=.000508,sy=345e6,crush=sc)
        compare(f"COMPUTE/p2/calibration/pach/model_crush_{sc/1e6:.1f}MPa",
                dict(depth_m=dent,diameter_m=2*b),c["p2"]["calibration"]["pach"][f"model_crush_{sc/1e6:.1f}MPa"],
                rtol=5e-6,note="Exact analytic contact-work integral.")
    check("COMPUTE/p2/calibration/pach/test_depth_m",.0011,c["p2"]["calibration"]["pach"]["test_depth_m"])
    dent,b=hard_depth(.8*1.07,tf=.000301,sy=503e6)
    compare("COMPUTE/p2/calibration/clarke",dict(fe_max_displacement_m=.00237,model_depth_m=dent,
                 model_diameter_m=2*b,ratio_fe_over_model=.00237/dent),c["p2"]["calibration"]["clarke"],rtol=5e-6)
    pricing={}
    pricing["patch"]=[]
    for i,row in enumerate(c["p2"]["pricing"]["patch"]):
        val=p2_opt(patch_diameter=row["D_m"],edge=row["edge"])
        out=dict(usage=val["usage"],gamma=val["gamma_need"],tf_m=val["tf_m"],tc_m=val["tc_m"],
                 feasible=val["usage"]<=1)
        pricing["patch"].append(out);compare(f"COMPUTE/p2/pricing/patch/{i}",out,row)
    pricing["extra_mass"]=[]
    for i,row in enumerate(c["p2"]["pricing"]["extra_mass"]):
        val=p2_opt(extra=row["kg"])
        out=dict(usage=val["usage"],gamma=val["gamma_need"],kg_per_m2=row["kg"]/AREA)
        pricing["extra_mass"].append(out);compare(f"COMPUTE/p2/pricing/extra_mass/{i}",out,row)
    pricing["denser_core"]=[]
    for i,row in enumerate(c["p2"]["pricing"]["denser_core"]):
        val=p2_opt(k=row["k"])
        out=dict(usage=val["usage"],gamma=val["gamma_need"],crush_Pa=CRUSH*row["k"]**(5/3),feasible=val["usage"]<=1)
        pricing["denser_core"].append(out);compare(f"COMPUTE/p2/pricing/denser_core/{i}",out,row)
    margin=brentq(lambda ex:p2_opt(extra=ex)["usage"]-1,0.,50.,xtol=1e-10)
    check("COMPUTE/p2/pricing/mass_margin_kg",margin,c["p2"]["pricing"]["mass_margin_kg"])
    for key in ["Shi-calibrated k rho v2","all energy to the panel"]:
        h=hails[-1];a=h["D_m"]/2
        dent,b=soft_depth(a,h["rho_v2_Pa"]*kshi if key.startswith("Shi") else None,h["E_J"] if key.startswith("all") else None)
        ncr=LAM_C**2*DF/b**2
        vent=ncr/N
        vals=dict(b_m=b,depth_m=dent,crush_needed_Pa=Q0+4*(N-ncr)*dent/b**2,
                  vent_fraction_dp=vent,air_admitted_kg=(1-vent)*rho500*VOLUME)
        compare("COMPUTE/p2/pricing/design_hail_needs/"+key,vals,c["p2"]["pricing"]["design_hail_needs"][key])
    p3=p3opt()
    compare("DET/p3",p3,d["p3"],rtol=3e-6)
    triangle=p3["s"]/(2*math.sqrt(3));rhombus=p3["s"]*math.sqrt(3)/4
    merged=dict(inradius_triangle_m=triangle,inradius_rhombus_m=rhombus,
                tension_ratio_same_rise_to_span=rhombus/triangle,film_SF_after=p3["lam"]*triangle/rhombus)
    compare("COMPUTE/p3/film/merged_bay",merged,c["p3"]["film"]["merged_bay"],rtol=3e-6)
    for em in [81,180]:
        toughness={"StratoFilm 420 J_c low":500.,"Mylar EWF 10 mm/min":40200.,
                   "Mylar EWF 1 m/s":63700.,"Kapton HN Elmendorf, 2F/t":2*.07/25e-6}
        tears={k:em*1e9*v/(PI*p3["film_stress_Pa"]**2) for k,v in toughness.items()}
        compare(f"COMPUTE/p3/film/tear/E_{em}GPa",tears,c["p3"]["film"]["tear"][f"E_{em}GPa"],rtol=3e-6)
    stop={}
    for em in [81,180]:
        allow=math.sqrt(em*1e9*40200/(PI*.025))
        v=p3opt(allow)
        out=dict(film_stress_Pa=allow,SF=v["lam"],film_kg=v["m_film"])
        compare(f"COMPUTE/p3/film/stop_25mm_slit/E_{em}GPa",out,c["p3"]["film"]["stop_25mm_slit"][f"E_{em}GPa"],rtol=2e-5)
        stop[str(em)]=v
    # Centre moment of an infinite isotropic plate on a Winkler foundation.
    # Its Hankel integral is independently checked by quadrature and the
    # identity I(x)=-Re[K1(z)/z], z=x exp(i*pi/4).
    from scipy.integrate import quad
    nu=.16
    wall=p3["t"];ro=p3["ro"]
    ds=430e9*wall**3/(12*(1-nu**2))
    foundation=430e9*wall/ro**2
    ell=(ds/foundation)**.25
    contact=.012
    xc=contact/ell
    intg_quad=quad(lambda u:j1(u)*u*u/(u**4+xc**4),0,1000,epsabs=1e-10,limit=1000)[0]
    z=xc*np.exp(1j*PI/4)
    intg=float(-(kv(1,z)/z).real)
    stress_per_pressure=3*(1+nu)*contact**2*intg/wall**2
    laws={"tube C-ring flexure":(299e6,4.6),"tube sectored flexure":(192e6,5.5),
          "Hexoloy SA 4-pt bars":(380e6/Gamma(1.1),10.)}
    for i,h in enumerate(hails):
        vals=dict(D_m=h["D_m"],v_m_s=h["v_m_s"],q_flow_Pa=h["rho_v2_Pa"],
                  sigma_flow_Pa=stress_per_pressure*h["rho_v2_Pa"],
                  c_m=contact,sigma_per_MPa_contact=stress_per_pressure*1e6,
                  sigma_shi_Pa=stress_per_pressure*h["rho_v2_Pa"]*kshi)
        for tag,factor in [("flow",1.),("shi",kshi)]:
            sig=stress_per_pressure*h["rho_v2_Pa"]*factor
            vals["Pf_"+tag]={key:-math.expm1(-(sig/scale)**mod) for key,(scale,mod) in laws.items()}
        vals["strikes_to_half_shi"]={key:math.log(2)/(vals["sigma_shi_Pa"]/scale)**mod for key,(scale,mod) in laws.items()}
        vals["q_to_fracture_Pa"]={key:scale/stress_per_pressure for key,(scale,mod) in laws.items()}
        compare(f"COMPUTE/p3/tube_hail/{i}",vals,c["p3"]["tube_hail"][i],rtol=3e-5,atol=1e-13)
    p3prices={}
    for key in ["film_allowable","wall_min","extra_mass"]:
        outrows=[]
        for i,row in enumerate(c["p3"]["pricing"][key]):
            v=p3opt(allowable=row.get("film_allowable_Pa",1.74e9),extra=row.get("extra_kg",0),minwall=row.get("wall_min_m",0))
            out=dict(SF=v["lam"],s=v["s"],OD=2*v["ro"],wall=v["t"],film_kg=v["m_film"],tube_kg=v["m_tube"]) if v else dict(SF=None,s=None,OD=None)
            compare(f"COMPUTE/p3/pricing/{key}/{i}",out,row,rtol=2e-5)
            outrows.append(out)
        p3prices[key]=outrows
    EXTRA.update(p2=P2,p3=p3,p2_constants=base,p2_pricing=pricing,p2_margin=margin,
                 p3_pricing=p3prices,p3_tear_stop_witnesses=stop,
                 shell_contact=dict(nu=nu,plate_D=ds,foundation=foundation,length=ell,integral=intg,
                                    quadrature_integral=intg_quad,
                                    stress_per_pressure=stress_per_pressure),
                 assumptions=dict(core_density_kg_m3=RHO_CORE,core_E_Pa=EC,core_G_Pa=GC,
                                  rounded_crush_Pa=CRUSH,beam_E_Pa=BEAM_E,
                                  damage_nu=NU_BE,gamma_map_nu=.33,pressure_Pa=P))
    save("ARITHMETIC.json",EXTRA)
    save("ARITHMETIC-CHECKS.json",CHECKS)
    failures=[v for v in CHECKS if not v["pass_"]]
    save("ARITHMETIC-DIFFERENCES.json",failures)
    print(json.dumps(dict(checks=len(CHECKS),differences=len(failures),first=failures[:12]),indent=2))


if __name__=="__main__":
    main()
