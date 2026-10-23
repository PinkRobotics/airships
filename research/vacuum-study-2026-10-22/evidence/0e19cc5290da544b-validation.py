from check_model import *
from check_thermal import balance,js
import time
results={}
alb=next(k for k in CONS if k.startswith("AlBeMet"))
cb=props(alb)
def alb_at(mult,n=1200):
    c=dict(cb,E_today_Pa=cb["E_today_Pa"]*mult,E1=cb["E1"]*mult)
    return optimize(c,15,finish="reference040",thermal_mode="pinned",n=n)
results["AlBeMet_R15_old_coating_witness"]=dict(multiplier=3.3,point=alb_at(3.3,n=3000))
results["AlBeMet_R15_old_coating_float_interval"]=[
    brentq(lambda k:alb_at(k)["payload_kg"],3.1,3.3,xtol=1e-9),
    brentq(lambda k:alb_at(k)["payload_kg"],3.6,3.9,xtol=1e-9)]
print("AlBeMet",results["AlBeMet_R15_old_coating_float_interval"],
      results["AlBeMet_R15_old_coating_witness"]["point"]["payload_kg"],flush=True)

dense=[]
for old in json.loads((ROOT/"CORRECTED-SEARCHES.json").read_text()):
    if old["weather"]!="ISA" or old["R_m"] not in [15,30]:continue
    key=FOLD["constructions"][-2]["key"];c=props(key,old["properties"]);R=old["R_m"]
    ep=optimize(c,R,n=1500,thermal_mode=old["thermal_basis"])
    l=old["least"];lp=optimize(c,R,mask=l["mask"],u=l["usage"],n=1500,thermal_mode=old["thermal_basis"]) if l else None
    dense.append(dict(variant=old["variant"],R_m=R,basis=old["thermal_basis"],
        endpoint_payload_delta=ep["payload_kg"]-old["endpoint"]["payload_kg"],
        endpoint=ep,least_at_saved_usage=lp))
results["dense_corrected_searches"]=dense

# Fully specified heat-balance closure, refined independently of owner values.
thermals=[]
for R,tc,finish in [(10,.022106790073497733,"reference040"),(30,.12387360186798597,"MLCCAg")]:
    c=props(FOLD["constructions"][-2]["key"])
    for n in [128,256,512]:
        t=balance(R,[tc],c["k"],finish,n=n)
        thermals.append(dict(R_m=R,finish=finish,n=n,**t))
results["thermal_quadrature"]=thermals

# A favorable split E bound guards the Be subset count despite nonmonotone E.
bound=[]
key=next(k for k in CONS if k.startswith("Be |"))
for R in [15,20,30]:
    for climate in ["ISA","optimistic"]:
        for floor in [False,True]:
            c=props(key,dict(thermal_E_override=290e9))
            for mask in [0,1,2,4,8]:
                t=optimize(c,R,mask=mask,climate=climate,floor=floor,n=400,
                           thermal_mode="pinned" if R==15 else "independent")
                bound.append(dict(R_m=R,weather=climate,floor=floor,mask=mask,
                                  payload_kg=t["payload_kg"] if t else None))
results["Be_fewer_than_two_axis_favorable_bound"]=bound
(ROOT/"VALIDATION.json").write_text(json.dumps(results,default=js,indent=2)+"\n")
print("validation complete",flush=True)
