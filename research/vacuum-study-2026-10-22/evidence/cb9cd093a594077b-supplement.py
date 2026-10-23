from check_model import *
from check_thermal import balance,js
from dataclasses import dataclass
import csv
RES=read("owner/RESULTS.json")
out={};comparisons=[]
def cmp(row,field,old,new,basis):
    comparisons.append(dict(row=row,field=field,owner=old,checker=float(new),
                            delta=float(new)-old,basis=basis))

point=read("upstream/028b_properties.json")["full_named_maxima"][0]["point"]
tf=point["tf_m"];tc=point["tc_m"]
tfactors=[]
for row in RES["thermal_factors"]:
    c=props(row["construction"]);g=c["coredata"]["Gc_Pa"]
    stress_per_K=abs(c["alpha_c"]-c["alpha_f"])*np.sqrt(c["E_today_Pa"]*tf*g/tc)
    K=.5*c["wall_E"]*c["coredata"]["rho"]/c["wall_rho"]
    eps=abs(c["alpha_c"]-c["alpha_f"])*GUARD*max(abs(c["cure_K"]-row["min_outer_K"]),
                                                               abs(c["cure_K"]-row["max_outer_K"]))
    new=dict(legacy_037_day_SF=c["coredata"]["shear_strength_W_Pa"]/(row["rise_K"]*stress_per_K),
             legacy_037_full_cycle_SF=c["coredata"]["shear_strength_W_Pa"]/(row["swing_K"]*stress_per_K),
             current_edge_SF=c["edge_allow"]/(eps*np.sqrt(2*K*g)))
    for k,v in new.items():cmp(row["construction"]+"|"+row["finish"],k,row[k],v,"provided thermal extrema; independent stress arithmetic")
    klegacy=c["k"]*2700/2640 if c["core"].startswith("CR-III") else c["k"]
    independent=balance(10,[tc],klegacy,row["finish"],n=37,legacy=True)
    tfactors.append(dict(row=row,conditional=new,independent_temperature={k:float(v[0]) for k,v in independent.items() if isinstance(v,np.ndarray)}))
out["source_geometry_thermal_factors"]=tfactors

edges=[]
for finish,rows in RES["edge_vs_cure"].items():
    for row in rows:
        if finish=="folded":
            c=props(row["construction"],dict(cure_K=row["cure_K"]))
            own=next(x for x in RES["thermal_factors_own_geometry"] if x["construction"]==row["construction"] and x["R_m"]==20)
            mint=T0+own["rise_K"]-own["swing_K"];maxt=T0+own["rise_K"]
            therm=dict(min_outer_K=mint,max_outer_K=maxt,gradient_K=0.,curvature_temperature_K=0.)
            tf1=row["tf_m"];tc1=row["tc_m"]
        else:
            key=next(k for k in CONS if k.startswith("M55J") and "room-temperature" in k)
            c=props(key,dict(cure_K=row["cure_K"]))
            rr=next(x for x in RES["rows_040_coating"] if x["case"]==c["label"] and x["R_m"]==20 and x["weather"]=="ISA" and not x["floor"])
            tf1=rr["endpoint_all_geometry"]["tf_m"];tc1=rr["endpoint_all_geometry"]["tc_m"]
            therm=temperatures(c,20,tc1,"reference040","pinned")
        mech=mechanics(c,20,tf1,tc1,thermal=therm)
        new=dict(edge_SF=mech["modes"]["thermal_core_interface_screen"],tau_Pa=mech["edge_shear_Pa"],
                 cure_compression_Pa=mech["cure_compression_Pa"],wall_SF=mech["modes"]["core_cell_wall_yield_screen"])
        for k,v in new.items():cmp(f'{finish}|{c["key"]}|Tcure{row["cure_K"]}',k,row[k],v,"provided thermal extrema/table")
        edges.append(dict(finish=finish,cure_K=row["cure_K"],construction=c["key"],checker=new))
out["edge_vs_cure"]=edges

dry=[]
for row in RES["dry_gas_pressure_at_primary_geometry"]:
    rr=next(x for x in ROWS if x["construction"]==row["construction"] and x["R_m"]==row["R_m"]
            and x["weather"]=="ISA" and not x["floor"] and x["finish"]=="MLCCAg" and x["variant"]=="primary")
    c=props(row["construction"]);g=rr["endpoint_all_geometry"]
    baked=bill(c,row["R_m"],g["tf_m"],g["tc_m"])
    wet=bill(c,row["R_m"],g["tf_m"],g["tc_m"],variant="dry_gas")
    new=dict(bake_pressure_SF=baked["vacuum"]["pressure_SF"],
             dry_gas_pressure_SF_same_geometry=wet["vacuum"]["pressure_SF"],
             dry_gas_material_water_kg=wet["vacuum"]["added_material_water_kg"])
    for k,v in new.items():cmp(f'{row["construction"]}|R{row["R_m"]}',k,row[k],v,"independent service ledger")
    dry.append(dict(construction=row["construction"],R_m=row["R_m"],**new))
out["dry_gas"]=dry

own=[]
for row in RES["thermal_factors_own_geometry"]:
    c=props(row["construction"])
    per=abs(c["alpha_c"]-c["alpha_f"])*np.sqrt(c["E1"]*row["tf_m"]*c["coredata"]["Gc_Pa"]/row["tc_m"])
    new=dict(day_SF=c["coredata"]["shear_strength_W_Pa"]/(per*row["rise_K"]),
             full_cycle_SF=c["coredata"]["shear_strength_W_Pa"]/(per*row["swing_K"]))
    for k,v in new.items():cmp(f'{row["construction"]}|R{row["R_m"]}',k,row[k],v,"provided thermal extrema; full-endpoint E")
    own.append(dict(row=row,checker=new))
out["own_geometry_thermal_factors"]=own
out["coatings"]=dict(MLCCAg=50e-9*8400+120e-9*10500+80*15e-9*3970+80*5e-9*2648+10e-9*7200,
    CCAg_min=(80e-9+1600e-9)*3970+120e-9*10500+500e-9*2648+10e-9*7200,
    CCAg_max=(80e-9+1900e-9)*3970+120e-9*10500+750e-9*2648+10e-9*7200)
out["supply"]=dict(be_share=RES["answer"]["supply_R30"]["beryllium_faces_t"]/433,
    pitch_original_share=RES["answer"]["supply_R30"]["projection_faces_t"]*.67/1400,
    albemet_Be=next(x for x in ROWS if x["construction"].startswith("AlBeMet") and x["R_m"]==30 and x["weather"]=="ISA" and not x["floor"] and x["variant"]=="primary" and x["finish"]=="MLCCAg")["faces_at_all_endpoint_kg"]*.62)
(ROOT/"SUPPLEMENT.json").write_text(json.dumps(out,default=js,indent=2)+"\n")
with (ROOT/"SUPPLEMENT-COMPARISONS.csv").open("w") as f:
    w=csv.DictWriter(f,fieldnames=list(comparisons[0]));w.writeheader();w.writerows(comparisons)
print("supplement comparisons",len(comparisons),flush=True)

# Modulus targets: scan the whole [1,8] range before refining the first crossing.
targets=[]
for finish,rows in RES["E_multiplier_to_float"].items():
    for row in rows:
        key=row.get("construction")
        if key is None:
            key=next(k for k,c in CONS.items() if c["face"]==row["face"] and c["core"]==row["core"] and c["cure_K"]==row["cure_K"])
        c=props(key);R=row["R_m"];f="MLCCAg" if finish=="folded" else "reference040"
        thermal_mode="pinned" if c["core"].startswith("CR-III") and (f=="reference040" or R==15) else "independent"
        def ev(k):
            cc=dict(c,E_today_Pa=c["E_today_Pa"]*k,E1=c["E1"]*k)
            result=optimize(cc,R,finish=f,thermal_mode=thermal_mode)
            return result["payload_kg"] if result else -np.inf
        samples=[(float(k),ev(k)) for k in np.geomspace(1,8,29)]
        found=None
        for i,(k,value) in enumerate(samples):
            if value>=0:
                if i==0:found=k
                else:
                    lo=samples[i-1][0];hi=k
                    for _ in range(25):
                        mid=(lo+hi)/2
                        if ev(mid)>=0:hi=mid
                        else:lo=mid
                    found=hi
                break
        targets.append(dict(finish=f,row=row,thermal_basis=thermal_mode,checker_k_E=found,
                            checker_E_Pa=c["E_today_Pa"]*found if found else None,samples=samples))
        print("modulus",finish,key,R,row["k_E"],found,flush=True)
        (ROOT/"MODULUS-TARGETS.json").write_text(json.dumps(targets,indent=2)+"\n")
