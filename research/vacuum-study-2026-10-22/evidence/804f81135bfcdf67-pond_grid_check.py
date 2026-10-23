"""Resolve published quadrature conventions without executable access."""
from pond_check import *
def main():
    n=301
    ll=np.array([(i/n,j/n,1-(i+j)/n) for i in range(n+1) for j in range(n+1-i)])
    t=3*ll.min(axis=1);xy=ll@V
    k=P['mean_per_crown']/np.mean(t*(2-t));d=k*C*t*(2-t)
    beta=np.deg2rad(P['beta_deg']);target=np.array(P['pond_volume_per_s3'])
    probes=[0,4,20,32,40,44,48,52]
    def calculate(indices,aznum,phase,vertical=False):
        results=np.zeros(len(indices))
        for phi in (np.arange(aznum)+phase)*2*np.pi/aznum:
            x=[address]([np.cos(phi),np.sin(phi)])
            low=([address]([np.cos(phi),np.sin(phi)])).min()
            for j,i in enumerate(indices):
                dep=np.maximum(d-np.tan(min(beta[i],np.pi/2-1e-9))*(x-low),0)
                results[j]+=dep.mean()*AREA*(np.cos(beta[i]) if vertical else 1)/aznum
        return results
    fits=[]
    for az in [6,8,12,18,24,36,48,60]:
        for phase in [0.,.5]:
            for vertical in [False,True]:
                val=calculate(probes,az,phase,vertical)
                err=float(np.max(abs(val-target[probes])))
                fits.append(dict(azimuths=az,phase=phase,vertical=vertical,max_error_s3=err))
    fits.sort(key=lambda x:x['max_error_s3'])
    best=fits[0]
    full=calculate(list(range(len(beta))),best['azimuths'],best['phase'],best['vertical'])
    rows=[dict(beta_deg=b,own=v,owner=o,delta_s3=v-o,
               passed=abs(v-o)<1e-11) for b,v,o in zip(P['beta_deg'],full,target)]
    dump('POND-GRID-INDEPENDENT.json',dict(barycentric_divisions=n,k=k,
         fits=fits,profile=rows,matches=sum(x['passed'] for x in rows)))
    print(json.dumps(dict(k=float(k),best=fits[:5],matches=int(sum(x['passed'] for x in rows))),indent=2))
if __name__=='__main__':main()
