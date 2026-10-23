import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from checklib import *
import csv
import beam
audit=Audit(); mats=materials()
ownpoints,owncells,ownedges=beam.geodesic(5)
for ref in read("MATERIAL-MODELS.json"):
    cur=mats[ref["id"]];audit.fields("material/"+ref["id"],ref,cur,atol=1e-5)
    for field in ["Q_Pa","lamina_Q_Pa"]:
        for i in range(3):
            for j in range(3):
                audit.check("material/"+ref["id"],f"{field}[{i}][{j}]",ref[field][i][j],cur[field][i,j],atol=1e-4)
    for i,rr in enumerate(ref["ply_ratios"]):
        for j in range(3):audit.check("material/"+ref["id"],f"ply_ratios[{i}][{j}]",rr["stress_per_unit_global_compression"][j],cur["ply_ratios"][i][j],atol=1e-12)
dump("INDEPENDENT-MATERIALS.json",mats)
cache={}
for row in read("TARGETS.json")["rows"]:
    res,case=row["reserve"],row["load"];key=(res,case)
    if key not in cache:
        base,arr,rr=base_data(res);ro=base["section"]["r_o_m"];t=base["section"]["wall_m"]
        q=1. if case=="operating" else base["least_screened_SF"]
        ss,_=peak(arr,mats["041-reference"],ro,t,q)
        cache[key]=(ss,arr["L"],base["section"]["area_m2"])
        lookup={tuple(np.round(p,8)):i for i,p in enumerate(arr["points"][:252])}
        nodemap=[lookup[tuple(np.round(p,8))] for p in ownpoints]
        edgeindex={tuple(sorted(edge)):i for i,edge in enumerate(arr["edges"])}
        membermap=[edgeindex[tuple(sorted((nodemap[u],nodemap[v])))] for u,v in ownedges]
        with (UP/f"043-fold/MEMBERS-f5-{res}-{case}.csv").open() as f:
            for v in csv.DictReader(f):
                audit.check(f"member/{res}/{case}/{v['member']}","peak_compression_Pa",float(v["peak_compression_Pa"]),ss[membermap[int(v["member"])]])
        dump("MEMBER-ID-MAP-"+res+".json",dict(own041_to_check041=membermap))
    ss,L,A=cache[key]
    calc=target_row(ss,L,A,row["m"],row["frame_Pf_target"])
    audit.fields(f"target/{res}/{case}/m{row['m']}/p{row['frame_Pf_target']}",row,calc)
for row in read("TARGETS.json")["summary"]:
    res,case=row["reserve"],row["load"];ss,L,A=cache[res,case]
    cur=dict(peak_compression_GPa=float(ss.max()/1e9),area_m2=A,
        actual_length_m=[float(L.min()),float(L.mean()),float(L.max())],
        hypothetical_whole_3p9_m10_Pf=probability(ss,10,3.9e9),
        hypothetical_coupon1cm3_3p9_m10_Pf=probability(ss,10,3.9e9,A*L/1e-6))
    audit.fields(f"target-summary/{res}/{case}",row,cur)
    for size,targets in row["m_required_at_hypothetical_3p9_GPa"].items():
        for pf,owner in targets.items():
            audit.check(f"target-summary/{res}/{case}","m_needed/"+size+"/"+pf,owner,
                        shape_needed(ss,3.9e9,float(pf),1 if size=="equal_complete_member" else A*L/1e-6))
frames=[]
for i,row in enumerate(read("FRAME-COMPARE.json")["rows"]):
    res=row["reserve"];mat=mats[row["material"]];ro=row["ro_m"];t=row["wall_m"]
    cur=fixed_score(res,mat,ro,t)
    audit.fields(f"frame[{i}]/{row['material']}/{res}/{row['section_policy']}",row,cur)
    # Independent inversion of equal mass or deterministic minimum wall.
    base=BASE[res]
    if row["section_policy"]=="same_tube_mass":
        A=base["mass_kg"]["tube"]/(mat["density_kgm3"]*sum(base["geometry"]["member_arc_lengths_m"]))
        needed=ro-math.sqrt(ro*ro-A/math.pi)
        audit.check(f"frame[{i}]","same_mass_wall",t,needed)
    frames.append(dict(index=i,**cur))
dump("INDEPENDENT-FRAME-FIXED.json",frames)
audit.save("SCALAR-CHECK.json")
