#!/usr/bin/env python3
"""Independently bound 24h gas over every filed finite geometry, using no owner code."""
from check_model import *

def run():
    gas=read("inputs/034/INPUTS.json")
    ru=gas["constants"]["R_universal_J_mol_K"]
    species=gas["species"]
    mm=sum(s["M_kg_mol"]*s["dry_x"] for s in species.values())/sum(s["dry_x"] for s in species.values())
    old=read("owner-data/SUPPLEMENTAL-RESULTS.json")["gas_24h_bounds"]
    records=[]
    for R in (10,12,15,20,30):
        table=np.load(B/f"owner-data/COUPLED-R{R}.npz")
        valid=np.isfinite(table["mass_kg"])
        tf=table["tf_m"][valid];tc=table["tc_m"][valid]
        indexes=np.argwhere(valid);mask=indexes[:,1]
        A=4*np.pi*R**2;V=4/3*np.pi*R**3
        seam=A*(1/(.6096-SCARF*tf)+1/(1.8288-SCARF*tf))
        film=2*A*.1464728290914915*np.where(mask&8,.5,1)
        core=A*RHO_CORE*tc;scarf=seam*2*tf*np.sqrt(1+SCARF**2)*.07
        splice=seam*.0005*tc*500;seal=seam*.002
        coating=A*.00833272;primer=A*.01
        uptake=.1*(.002*film+.001*core+.01*(scarf+splice+seal+coating+primer))
        inventory=.1*(.0485*film+.001*core+.01*(scarf+splice+seal+coating+primer))+uptake
        # Thin-layer whole-sphere account, with an exact inner cavity and
        # the inherited outer-area pore approximation.
        connected=4/3*np.pi*(R-2*tf-tc)**3+A*tc*(1-RHO_CORE/2700)
        # A second strictly smaller gas volume gives a conservative check:
        # discard ALL pores from available storage.
        inner=4/3*np.pi*(R-2*tf-tc)**3
        initial_moles=10*connected/(ru*258)
        leak_moles=(.001*seam+.01)*.1*86400/(ru*258)
        permeation_moles=10*3.34645e-16*(seam*.07/1250)/(tf*np.sqrt(1+SCARF**2))*106500*86400
        ingress=leak_moles+permeation_moles
        total_mass=(initial_moles+ingress)*mm+inventory
        total_moles=initial_moles+ingress+inventory/species["H2O"]["M_kg_mol"]
        pressure=total_moles*ru*326/connected
        pressure_no_pore_credit=total_moles*ru*326/inner
        j=int(np.argmax(total_mass));k=int(np.argmax(pressure))
        original=next(x for x in old if x["R_m"]==R)
        records.append(dict(R_m=R,finite_geometries=len(tf),owner=original,
            maximum_gas_mass_kg=float(total_mass[j]),maximum_pressure_Pa=float(pressure[k]),
            pressure_no_core_pore_credit_Pa=float(np.max(pressure_no_pore_credit)),
            allowance_kg=.01*LIFT_REF*(R/10)**3,pressure_limit_Pa=800,
            all_geometry_mass_pass=bool(np.max(total_mass)<.01*LIFT_REF*(R/10)**3),
            all_geometry_pressure_pass_even_without_pores=bool(np.max(pressure_no_pore_credit)<800),
            mass_maximizer=dict(index=indexes[j],mask=int(mask[j]),tf_m=tf[j],tc_m=tc[j],
                inventory_kg=inventory[j],connected_volume_m3=connected[j]),
            pressure_maximizer=dict(index=indexes[k],mask=int(mask[k]),tf_m=tf[k],tc_m=tc[k]),
            differences=dict(mass_kg=float(total_mass[j])-original["mass_kg_upper"],
                pressure_Pa=float(pressure[k])-original["pressure_Pa_upper"])))
    save("GAS-CHECK.json",dict(records=records,scope="Every filed finite coupled-table geometry; independent conservative all-inventory release and no-backpressure ingress at 258 K, pressure at 326 K.",
        owner_specific_sampling_not_assumed=True,qualified_sealed_life=None,
        approximations=["dry incoming mixture","10 Barrer scarf polymer path","all finite inventory water",
            "90% conditioning","pores connected in primary bound; omitted as extra conservative check"],
        owner_code_access=False))
    print([(r["R_m"],r["maximum_gas_mass_kg"],r["maximum_pressure_Pa"],r["pressure_no_core_pore_credit_Pa"],r["differences"]) for r in records],flush=True)

if __name__=="__main__":run()
