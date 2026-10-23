"""Transient local inventories under held weather; no redistribution assumed."""
from liquid_check import *
from scipy.optimize import brentq
def one(R,finish,cond,mode,initial,step):
    beta=np.deg2rad(np.arange(step/2,180,step))[:,None]
    phi=np.deg2rad(np.arange(step/2,360,step))[None,:]
    ev,t,err,h=flux(R,finish,cond,beta,phi,mode)
    mass=retained(finish,R,beta,night=None if initial=='rain' else 'night_050_saturated')
    if isinstance(mass,tuple):mass=mass[0]
    weights=np.broadcast_to(np.sin(beta)*np.deg2rad(step)/2/len(phi[0]),ev.shape)
    area=4*np.pi*R*R
    start=float(np.sum(mass*weights)*area)
    potential=float(np.sum(ev*weights)*area)
    bulk=start/potential if potential>0 else None
    def inventory(hours):
        return float(np.sum(np.maximum(mass-ev*hours,0)*weights)*area)
    times=[0,.2,1,2,4,8,12,24]
    condmass=float(np.sum(np.where(ev<0,mass,0)*weights)*area)
    full=float(np.max(np.where(ev>0,mass/np.maximum(ev,1e-30),0))) if np.all(ev>=0) else None
    fraction=float(np.sum(np.where(ev<0,weights,0)))
    ninety_nine=None
    if full is not None:
        ninety_nine=brentq(lambda x:inventory(x)-.01*start,0,full)
    return dict(R=R,finish=finish,condition=cond,mode=mode,initial=initial,step_deg=step,
        initial_kg=start,potential_fullwet_kg_h=potential,bulk_hours=bulk,
        residual_at_bulk_hours_kg=inventory(bulk) if bulk else None,
        local_full_dry_hours=full,local_99pct_removal_hours=ninety_nine,
        condensing_area_fraction=fraction,initial_water_on_condensing_area_kg=condmass,
        inventory_kg={str(x):inventory(x) for x in times},
        min_K=float(t.min()),max_energy_residual_W_m2=float(abs(err).max()))
def main():
    rows=[]
    for R in [10,30]:
        for finish in ['MLCCAg','paint_040']:
            for cond in ['morning_fair','midday_fair','overcast_day']:
                for mode in ['sphere040','flatplate']:
                    for initial in ['rain','dew']:
                        rows.append(one(R,finish,cond,mode,initial,1.))
    finer=[one(10,'MLCCAg','midday_fair',mode,'rain',.5) for mode in ['sphere040','flatplate']]
    dump('LOCAL-DRYING.json',dict(assumptions='fixed weather, uniform optics, full-area initial film within retention model; dry elements cease evaporating; no runoff or redistribution; molecular droplets not resolved',rows=rows,convergence=finer))
    print(json.dumps([r for r in rows if r['R']==10 and r['finish']=='MLCCAg' and r['initial']=='rain'],indent=2))
    # Recalculate the droplet occupancy calibration and measured uncertainty.
    dump('CALIBRATION-INDEPENDENT.json',dict(acrylic_54g_m2=KAPPA,
         acrylic_critical_base_radius_mm=float(AC*1000),measured_g_m2=.35/.08**2,
         measurement_sd_g_m2=.08/.08**2,calibration_kappa_measured=(.35/1000/.08**2)/(RHO*HEFF),
         rain_upper_factor=.08/.054))
if __name__=='__main__':main()
