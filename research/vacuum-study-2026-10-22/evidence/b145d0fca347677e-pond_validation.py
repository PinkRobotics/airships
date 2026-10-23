from pond_check import *
from liquid_check import flux

def cartesian(beta,phi,n=600):
    u,w=leggauss(n);u=(u+1)/2;w=w/2
    l=np.array(np.broadcast_arrays(u[:,None],(1-u[:,None])*u[None,:],
                                 (1-u[:,None])*(1-u[None,:])))
    t=3*l.min(axis=0)
    point=np.einsum('ic,ijk->cjk',V,l)
    x=point[0]*np.cos(phi)+point[1]*np.sin(phi)
    xmin=(V[:,0]*np.cos(phi)+V[:,1]*np.sin(phi)).min()
    depth=K*C*t*(2-t)-np.tan(beta)*(x-xmin)
    weight=2*(1-u[:,None])*w[:,None]*w[None,:]*AREA
    return float(np.sum(np.maximum(depth,0)*weight))

def main():
    tests=[]
    for bd,phid in [(0,0),(5,0),(7.64,30),(7.64,210),(12,0),(14,30),(16,30),(14,210),(16,210)]:
        b,p=np.deg2rad([bd,phid])
        strip=float(dish(b,p,n=768)[0]);direct=cartesian(b,p)
        tests.append(dict(beta_deg=bd,azimuth_deg=phid,strip_s3=strip,
                          cartesian_s3=direct,delta_kg=(strip-direct)*S**3*1000,
                          passed=abs(strip-direct)<1e-7))
    # Bay-level tilt threshold depends on direction; derive from positive maximum.
    ph=np.linspace(0,2*np.pi,721)
    xmin=(V[:,0,None]*np.cos(ph)+V[:,1,None]*np.sin(ph)).min(axis=0)
    thresholds=np.rad2deg(np.arctan(2*K*C/(-xmin)))
    own=json.loads((ROOT/'PONDS-INDEPENDENT.json').read_text())
    average_curve=np.array([r['own'] for r in own['profile']])
    average=interp1d(np.deg2rad(P['beta_deg']),average_curve,bounds_error=False,fill_value=0)
    positions={}
    for name,top in [('node',[0,0]),('bay',[.5,np.sqrt(3)/6])]:
        centers,angles=lattice();d=centers-top
        b=np.arctan(np.linalg.norm(d,axis=1)*S/10)
        phi=np.arctan2(d[:,1],d[:,0])+np.pi-angles
        vv,aa=dish(b,phi,n=768)
        xlo=(V[:,0,None]*np.cos(phi)+V[:,1,None]*np.sin(phi)).min(axis=0)
        max_normal=np.maximum(2*K*C+np.tan(b)*xlo,0)**2/(4*K*C)
        max_vertical=float(np.max(max_normal*np.cos(b))*S)
        rates={mode:float(flux(10,'paint_040','midday_fair',0.,0.,mode)[0]) for mode in ['sphere040','flatplate']}
        positions[name]=dict(volume_kg=float(vv.sum()*S**3*1000),
            averaged_azimuth_volume_kg=float(average(b).sum()*S**3*1000),
            max_depth_m=max_vertical,constant_top_flux_kg_m2_h=rates,
            constant_flux_complete_evaporation_h={m:max_vertical*1000/r for m,r in rates.items()},
            owner_volume_kg=P['radii']['10']['pond_vertex_up_kg' if name=='node' else 'pond_face_up_kg'],
            owner_wetted_area_m2=P['radii']['10']['pond_vertex_up_surface_m2' if name=='node' else 'pond_face_up_surface_m2'])
        positions[name]['owner_bulk_time_h']={m:positions[name]['owner_volume_kg']/positions[name]['owner_wetted_area_m2']/r for m,r in rates.items()}
    # Numerical shape calibration error: same shape with reported k.
    bet=np.deg2rad(np.array(P['beta_deg']));az=np.arange(144)*2*np.pi/144
    curve=[]
    for b in bet:
        x,_=dish(np.full_like(az,min(b,np.pi/2-1e-9)),az,n=384,k=P['k_shape'])
        curve.append(float(x.mean()))
    ownercurve=np.array(P['pond_volume_per_s3'])
    comp=[dict(beta_deg=b,declared_k_exact=v,owner=o,delta_s3=v-o)
          for b,v,o in zip(P['beta_deg'],curve,ownercurve)]
    # Identify common triangular quadratures as numerical convention diagnostics.
    norms=[]
    for n in [50,60,80,100,120,150,200,240,300,301]:
        ll=np.array([(i/n,j/n,1-(i+j)/n) for i in range(n+1) for j in range(n+1-i)])
        tt=3*ll.min(axis=1);mean=np.mean(tt*(2-tt))
        norms.append(dict(n=n,k=P['mean_per_crown']/mean))
    dump('POND-VALIDATION.json',dict(cartesian_checks=tests,positions=positions,
        continuous_spill_angle_min_deg=float(thresholds.min()),continuous_spill_angle_max_deg=float(thresholds.max()),
        owner_k_exact_mean_depth_per_s=float(P['k_shape']*C*.5),
        charged_mean_depth_per_s=float(P['mean_per_crown']*C),
        declared_k_profile_comparison=comp,normalization_diagnostics=norms))
    print(json.dumps(dict(checks=tests,positions=positions,angles=[float(thresholds.min()),float(thresholds.max())],norms=norms),indent=2))
if __name__=='__main__':main()
