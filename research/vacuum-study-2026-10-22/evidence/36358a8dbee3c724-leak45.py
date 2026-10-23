"""Independent compressible inflow and rigid-sphere descent calculation."""
from pathlib import Path
import math
import json
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from check45 import ROOT, save, compare, check, CHECKS, R, VOLUME, RGAS, G, B, P2

PI=math.pi
GAMMA=1.4
CD_HOLE=.6
T0=288.15
LAPSE=.0065
P0=101325.
AREA=PI*R*R


def atmosphere(z):
    temperature=T0-LAPSE*z
    pressure=P0*(temperature/T0)**(G/(RGAS*LAPSE))
    return temperature,pressure,pressure/(RGAS*temperature)


TEMP500,PA500,RHO500=atmosphere(500.)
MASS=RHO500*VOLUME
CRITICAL=(2/(GAMMA+1))**(GAMMA/(GAMMA-1))
P2_GAS_VOLUME=4*PI/3*(R-P2["tf_m"]-P2["tc_m"])**3


def flux(pressure,temperature,ratio=0.):
    if ratio>=1:return 0.
    if ratio<=CRITICAL:
        factor=math.sqrt(GAMMA)*(2/(GAMMA+1))**((GAMMA+1)/(2*(GAMMA-1)))
    else:
        factor=math.sqrt(2*GAMMA/(GAMMA-1)*(ratio**(2/GAMMA)-ratio**((GAMMA+1)/GAMMA)))
    return CD_HOLE*pressure/math.sqrt(RGAS*temperature)*factor


def simulate(area,drag,volume=VOLUME,capture=False,rtol=2e-9,ground_altitude=0.):
    def rhs(t,y):
        z,v,m=y
        temp,pa,rho=atmosphere(z)
        pi=max(0,m)*RGAS*temp/volume
        mdot=area*flux(pa,temp,pi/pa)
        inertia=MASS+m+.5*rho*VOLUME
        force=(rho*VOLUME-MASS-m)*G-.5*rho*drag*AREA*v*abs(v)
        if capture:
            force-=mdot*v
        return [v,force/inertia,mdot]
    def ground(t,y):return y[0]-ground_altitude
    ground.terminal=True;ground.direction=-1
    def half(t,y):return y[2]-.5
    half.direction=1
    estimated=300/(area*flux(PA500,TEMP500))
    result=solve_ivp(rhs,[0,max(200.,estimated*2)],[500.,0.,0.],
                     method="DOP853",rtol=rtol,atol=[1e-7,1e-9,1e-9],
                     events=[ground,half],dense_output=True,max_step=30. if area<1e-4 else 5.)
    tt=result.t
    zz,vv,mm=result.y
    temp=T0-LAPSE*zz;pa=P0*(temp/T0)**(G/(RGAS*LAPSE))
    dp=pa-mm*RGAS*temp/volume
    idx=int(np.argmax(dp))
    out=dict(dp0_Pa=PA500,dp_max_ratio=float(dp[idx]/PA500),z_at_dp_max_m=float(zz[idx]),
             t_end_s=float(tt[-1]),z_end_m=float(zz[-1]),v_end_m_s=float(vv[-1]),
             m_in_end_kg=float(mm[-1]),reached_ground=bool(len(result.t_events[0])),
             M_not_air_kg=MASS,t_first_half_kg_s=float(result.t_events[1][0]) if len(result.t_events[1]) else None,
             integration_steps=len(tt),rhs_evaluations=result.nfev,capture_momentum=capture,
             ground_centre_altitude_m=ground_altitude,
             net_heaviness_kg=MASS+float(mm[-1])-atmosphere(float(zz[-1]))[2]*VOLUME)
    return out


def main():
    owner=json.loads((ROOT/"inputs/owner/COMPUTE.json").read_text())["leak"]
    output=dict(constants=dict(R_gas=RGAS,g=G,V=VOLUME,V_p2=P2_GAS_VOLUME,critical_ratio=CRITICAL,
                               m_nonair=MASS,initial_pressure=PA500,initial_temperature=TEMP500,
                               sharp_orifice_Cd=CD_HOLE),holes=[],big=[],thresholds={},valves=[],detection=[],momentum_sensitivity=[])
    for i,diameter in enumerate([.001,.003,.01,.03,.1]):
        area=PI*diameter**2/4;rate=area*flux(PA500,TEMP500)
        row=dict(hole_m=diameter,mdot_kg_s=rate,t_48p9_h=48.894/rate/3600,
                 t_411_h=411.2989440716474/rate/3600,t_244_h=.05*B/rate/3600)
        compare(f"leak/holes/{i}",row,owner["holes"][i])
        for drag in [.47,.2]:
            tr=simulate(area,drag)
            # During all five small-hole descents the flow is choked, so the
            # trajectory is identical for P2 and P3; only gas-pressure scoring
            # uses the smaller P2 internal volume.
            p2=dict(tr)
            if tr["z_at_dp_max_m"]<1e-5:
                z=tr["z_end_m"];temp,pa,rho=atmosphere(z)
                p2["dp_max_ratio"]=(pa-tr["m_in_end_kg"]*RGAS*temp/P2_GAS_VOLUME)/PA500
            else:
                p2=simulate(area,drag,P2_GAS_VOLUME)
            for label,val in [(f"p2_cd{drag}",p2),(f"p3_cd{drag}",tr)]:
                row[label]=val
                compare(f"leak/holes/{i}/{label}",val,owner["holes"][i][label],
                        rtol=1e-3,atol=2e-5,note="Independent DOP853 integration; event times are rooted rather than sampled.")
            print("hole",diameter,"drag",drag,"time",tr["t_end_s"],"speed",tr["v_end_m_s"],flush=True)
        output["holes"].append(row)
    for i,row in enumerate(owner["big"]):
        val=simulate(row["area_m2"],row["cd_drag"])
        compare(f"leak/big/{i}",val,row,rtol=1e-3,atol=2e-5)
        output["big"].append({**val,"case":row["case"],"area_m2":row["area_m2"],"cd_drag":row["cd_drag"]})
        print("big",row["case"],row["cd_drag"],val["t_end_s"],val["v_end_m_s"],flush=True)
    for drag in [.47,.2]:
        for speed in [.914,4.2]:
            def target(diameter):
                return -simulate(PI*diameter**2/4,drag)["v_end_m_s"]-speed
            dia=brentq(target,.04 if speed==.914 else .09,.09 if speed==.914 else .2,xtol=2e-8)
            label=f"v{speed}_cd{drag}";output["thresholds"][label]=dia
            check("leak/touchdown_thresholds_hole_m/"+label,dia,owner["touchdown_thresholds_hole_m"][label],rtol=2e-4)
    temp,pa,rho=atmosphere(0)
    gradient=VOLUME*rho*G/(RGAS*temp)
    neutral_gradient=VOLUME*rho*(G/RGAS-LAPSE)/temp
    for i,speed in enumerate([.914,2.,7.5]):
        rate=gradient*speed;area=rate/flux(pa,temp)
        row=dict(descent_m_s=speed,mdot_kg_s=rate,area_m2=area,diameter_m=math.sqrt(4*area/PI))
        compare(f"leak/landing_valve/{i}",row,owner["landing_valve"][i])
        row["neutral_descent_mass_rate_kg_s"]=neutral_gradient*speed
        row["neutral_descent_valve_diameter_m"]=math.sqrt(4*neutral_gradient*speed/(flux(pa,temp)*PI))
        output["valves"].append(row)
    neutral=dict(dp_500_Pa=PA500,dp_ground_isa_Pa=MASS*RGAS*T0/VOLUME,ratio=T0/TEMP500)
    compare("leak/neutral_dp",neutral,owner["neutral_dp"])
    output["neutral"]=neutral
    check("leak/drop_test_speed_m_s",math.sqrt(2*G*36*.0254),owner["drop_test_speed_m_s"])
    for i,resolution in enumerate([1.,.1]):
        rate=VOLUME*resolution/(RGAS*TEMP500*3600)
        row=dict(resolution_Pa_per_h=resolution,mdot_kg_s=rate,hole_m=math.sqrt(4*rate/(PI*flux(PA500,TEMP500))))
        compare(f"leak/pressure_detection/{i}",row,owner["pressure_detection"][i])
        output["detection"].append(row)
    for dia in [.0631,.1,.3,1.]:
        area=PI*dia*dia/4
        for drag in [.47,.2]:
            no=simulate(area,drag);yes=simulate(area,drag,capture=True)
            output["momentum_sensitivity"].append(dict(hole_m=dia,drag=drag,
                no_capture_speed_m_s=-no["v_end_m_s"],capture_speed_m_s=-yes["v_end_m_s"],
                no_capture_time_s=no["t_end_s"],capture_time_s=yes["t_end_s"]))
    # Stationary vent: retain subsonic transition instead of assuming choking
    # all the way to 54.1% internal/ambient pressure.
    fraction=json.loads((ROOT/"ARITHMETIC.json").read_text())["p2_constants"]["patch"]["clamped"]["D_crit_m"]**2/(.08086510609617895**2)
    target_mass=(1-fraction)*MASS
    vent_time=quad(lambda mass:1/(PI*.2**2/4*flux(PA500,TEMP500,mass/MASS)),0,target_mass,epsabs=1e-8)[0]
    output["stationary_vent"]=dict(pressure_fraction=fraction,target_mass_kg=target_mass,
                                 valve_diameter_m=.2,time_s=vent_time,
                                 choked_only_time_s=target_mass/(PI*.2**2/4*flux(PA500,TEMP500)))
    save("LEAK-RESULTS.json",output);save("LEAK-CHECKS.json",CHECKS)
    failures=[v for v in CHECKS if not v["pass_"]];save("LEAK-DIFFERENCES.json",failures)
    print(json.dumps(dict(checks=len(CHECKS),differences=len(failures),first=failures[:8]),indent=2))


if __name__=="__main__":
    main()
