"""Independent grids, endpoint optima, least-axis selection and scarf roots."""
from account_check import *
from collections import defaultdict

rows = []
for model in ("owner_table","forced_conduction","mixed_conduction","forced_gap","mixed_gap"):
    rows.extend(json.loads((ROOT/f"owner/ACCOUNT-{model}.json").read_text()))
groups=defaultdict(list)
for row in rows:
    groups[tuple(row[k] for k in ("model","R_m","weather","cure_in_global"))].append(row)

checks=[]
def check(label, passed, **details):
    checks.append({"check":label,"passed":bool(passed),**details})

grid_results=[]
for group,cases in groups.items():
    template=cases[0]
    R=template["R_m"]
    tc=np.geomspace(.0012*R/10,1.4*R/10,1001)
    for mask in range(16):
        tf=minimum_faces(template,tc,mask,float(mask!=0))
        for case in cases:
            ans=evaluate(case,tf,tc,mask,float(mask!=0))
            feasible=(np.minimum.reduce(np.broadcast_arrays(*ans["modes"].values()))>=1-2e-9)&(ans["service_pressure_SF"]>=1)
            scores=np.where(feasible,ans["payload_kg"],-1e90)
            i=int(np.argmax(scores))
            expected=case["result"]["endpoints"][mask]
            difference=float(scores[i]-expected["payload_kg"])
            key=[*group,case["floor"],case["drying"],mask]
            check("endpoint not beaten by independent dense grid",difference<=.001,
                  case=key,grid_minus_filed_kg=difference)
            grid_results.append({"case":key,"grid_payload_kg":float(scores[i]),
                "filed_payload_kg":expected["payload_kg"],"difference_kg":difference,
                "grid_tc_m":float(tc[i]),"grid_tf_m":float(tf[i])})
    # Minimum axis count and ties derived from all independently rechecked endpoints.
    for case in cases:
        eps=case["result"]["endpoints"]
        floating=[w for w in eps if w["payload_kg"]>=-1e-5]
        minimum=min((int(w["mask"]).bit_count() for w in floating),default=None)
        expected=case["result"]["minimum_axis_count"]
        check("minimum axis count from endpoints",minimum==expected,case=[*group,case["floor"],case["drying"]],
              own=minimum,filed=expected)
        ties={w["mask"] for w in floating if int(w["mask"]).bit_count()==minimum}
        reported={w["mask"] for w in case["result"]["ties"]}
        check("complete tied minimum set",ties==reported,case=[*group,case["floor"],case["drying"]],
              own=sorted(ties),filed=sorted(reported))
    print("grid",group,flush=True)
dump("ENDPOINT-GRID-INDEPENDENT.json",grid_results)

# Reoptimize every named mask-11 endpoint, including all floor/drying variants.
optimized=[]
for j,case in enumerate(rows):
    ans=optimize(case,11,1.,n=801)
    expected=case["result"]["endpoints"][11]
    difference=float(ans["payload_kg"]-expected["payload_kg"])
    check("independent mask11 optimum",abs(difference)<.001,
        case=[case[k] for k in ("model","R_m","weather","cure_in_global","floor","drying")],
        difference_kg=difference)
    optimized.append({k:case[k] for k in ("model","R_m","weather","cure_in_global","floor","drying")}|{
        "own":ans,"filed_payload_kg":expected["payload_kg"],"difference_kg":difference})
    if (j+1)%36==0:
        dump("OPTIMA-INDEPENDENT.json",optimized)
        print("optimized endpoints",j+1,flush=True)
dump("OPTIMA-INDEPENDENT.json",optimized)

# Independently root the common-axis usage for every primary table row/tie.
least=[]
for case in rows:
    if not case["floor"] or case["drying"]!="bake":
        continue
    own_ties=[]
    for target in case["result"]["ties"]:
        mask=target["mask"]
        def value(u):
            point=optimize(case,mask,u,n=501)
            return -1e80 if point is None else float(point["payload_kg"])
        root=brentq(value,0.,1.,xtol=2e-9,rtol=1e-11)
        point=optimize(case,mask,root,n=801)
        check("primary common-axis usage",abs(root-target["usage"])<2e-6,
            case=[case[k] for k in ("model","R_m","weather","cure_in_global")],
            mask=mask,own=root,filed=target["usage"],difference=root-target["usage"])
        own_ties.append({"mask":mask,"usage":root,"point":point})
    chosen=min(own_ties,key=lambda x:(x["usage"],x["mask"])) if own_ties else None
    expected=case["result"]["chosen"]
    check("primary chosen least mask",(chosen["mask"] if chosen else None)==(expected["mask"] if expected else None),
          case=[case[k] for k in ("model","R_m","weather","cure_in_global")])
    least.append({k:case[k] for k in ("model","R_m","weather","cure_in_global")}|{"ties":own_ties,"chosen":chosen})
    print("least",case["model"],case["R_m"],case["weather"],case["cure_in_global"],flush=True)
dump("LEAST-INDEPENDENT.json",least)

# Closed-form low scarf root, independently of the bisection.
scarf=[]
for row in optimized:
    ans=row["own"];R=row["R_m"];tc=float(ans["tc_m"])
    tv=thermal(row["model"],R,tc)
    b=E0*ALPHA*1.002*tv["curvature_temperature_K"]/(2*(1-NU**2)*R)
    g=E0*ALPHA*1.002*tv["gradient_K"]/(2*(1-NU))
    constant=ans["pressure_Pa"]*R/4+KB*DA*1.002*(CURE-tv["min_outer_K"])*tc/2
    cap=10e6*(1+SCARF**2)/SCARF
    z=cap-g-b*tc
    closed=2*constant/(z+np.sqrt(z*z-4*b*constant))
    check("closed scarf face root",abs(float(ans["tf_m"])-closed)<1e-10,
          case=[row[k] for k in ("model","R_m","weather","cure_in_global","floor","drying")],
          difference_m=float(ans["tf_m"])-closed)
    scarf.append({"model":row["model"],"R_m":R,"weather":row["weather"],
                  "tf_m":float(ans["tf_m"]),"closed_tf_m":float(closed)})
dump("SCARF-ROOTS-INDEPENDENT.json",scarf)
dump("SEARCH-CHECKS.json",checks)
dump("SEARCH-SUMMARY.json",{"checks":len(checks),"passed":sum(r["passed"] for r in checks),
    "failures":[r for r in checks if not r["passed"]],
    "endpoint_grid_witnesses":len(grid_results),"reoptimized_endpoints":len(optimized),
    "primary_least_rows":len(least),
    "max_reoptimization_abs_difference_kg":max(abs(x["difference_kg"]) for x in optimized)})
print("search complete",len(checks),"failures",sum(not r["passed"] for r in checks),flush=True)
