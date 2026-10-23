from check_model import *
result=[]
for E1,E2,G,name in [(59.5*6894.757293168361e6,.806*6894.757293168361e6,.595*6894.757293168361e6,"unrounded Msi conversion"),
 (410.2e9,5.557e9,4.102e9,"rounded source-extraction values"),
 (410.2e9,5.56e9,4.10e9,"mixed rounded"),
 (410.2e9,5.56e9,4.102e9,"rounded transverse values"),
 (410e9,5.56e9,4.10e9,"literal rounded CARD prose"),
 (935e9*338/540,5.557e9,4.102e9,"projected E1 and rounded transverse values")]:
    E,nu=qi(E1,E2,G)
    result.append(dict(name=name,E1=E1,E2=E2,G=G,E_QI=E,nu=nu))
press=[]
for row in ROWS:
    if not row.get("endpoint_all_geometry"):continue
    c=props(row["construction"]);R=row["R_m"];g=row["endpoint_all_geometry"]
    a=bill(c,R,g["tf_m"],g["tc_m"],finish=row["finish"],variant=row["variant"],climate=row["weather"],floor=row["floor"])
    diffperm=(c["seam_film"]-.07)/1250*10*3.34645e-16*a["joining"]["length_m"]/(g["tf_m"]*np.sqrt(1+SCARF**2))*P0*86400
    delta_p=diffperm*RGAS*320/(4*np.pi*R**3/3)
    oldP=.01*P0/a["vacuum"]["pressure_SF"]
    revisedSF=.01*P0/(oldP-delta_p)
    press.append(dict(construction=row["construction"],R_m=R,weather=row["weather"],variant=row["variant"],
        owner_SF=row["endpoint_all_vacuum"]["pressure_SF"],checker_face_specific=a["vacuum"]["pressure_SF"],
        checker_fixed_70gsm=revisedSF,delta_fixed=revisedSF-row["endpoint_all_vacuum"]["pressure_SF"]))
(ROOT/"PROPERTY-PRECISION.json").write_text(json.dumps(result,indent=2)+"\n")
(ROOT/"PERMEATION-GAP-AUDIT.json").write_text(json.dumps(press,indent=2)+"\n")
print(json.dumps(result,indent=2))
print("fixed scarf pressure maximum difference",max(abs(x["delta_fixed"]) for x in press))
