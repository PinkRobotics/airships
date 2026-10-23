import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from checklib import *
import datetime, collections, re
names=["SCALAR-CHECK.json","FE-CHECK-all.json","FE-RECONCILIATION.json",
       "HAIL-CHECK.json","GAPS-WITNESSES-DAMAGE-CHECK.json","SECTIONS-TABLES-CHECK.json"]
audits={name:json.loads((ROOT/name).read_text()) for name in names}
discrepancies=[]
for name,audit in audits.items():
    for row in audit["rows"]:
        if row["passed"]:continue
        item=dict(artifact=name,**row)
        if row["field"].startswith("failed_ids/"):
            item.update(category="checker_unknown_vs_empty",status="resolved",
              disposition="Initial checker encoded an unknown compression-failure member set as empty. Corrected to null; all 364 member-set comparisons pass in FE-RECONCILIATION.")
        elif row["field"].startswith("linear_multipliers"):
            item.update(category="eigen_order_and_multiplicity",status="resolved",
              disposition="Every owner-returned eigenvalue is present in the independent 12-mode solution. Lowest factors and residuals pass. Scalar Lanczos returned different multiplicities/order.")
        elif ".Shi_stress[" in row["field"]:
            item.update(category="signed_tensor_vs_magnitude_label",status="open labeling fix",
              disposition="Owner field is a magnitude. Independent signed tensor component is negative. All magnitude, utilization and probability comparisons agree; label as absolute surface stress or retain sign.")
        elif row["field"]=="hypothetical_m_needed_if_typical_is_whole_member_scale":
            item.update(category="ill_conditioned_shape_inversion",status="open numerical presentation fix",
              disposition="Peak stress lies within 3.2e-11 of assumed scale. A 1e-8 relative wall reduction makes finite-m target impossible. Do not present a trillion-scale exponent as a stable material-processing target.")
        else:
            raise RuntimeError("Unclassified discrepancy: "+str(item))
        discrepancies.append(item)
dump("DISCREPANCIES.json",dict(rows=discrepancies,
    category_counts=dict(collections.Counter(x["category"] for x in discrepancies)),
    exact_row_field_owner_independent_values=True))

# Publish a clean audit with resolved set/mode comparisons, retaining raw records above.
final=[]
for name,audit in audits.items():
    if name=="FE-RECONCILIATION.json":continue
    for raw in audit["rows"]:
        row=dict(raw,artifact=name)
        if name=="FE-CHECK-all.json" and row["field"].startswith("failed_ids/"):continue
        if not row["passed"] and row["field"].startswith("linear_multipliers"):
            label=row["row"]
            if name=="GAPS-WITNESSES-DAMAGE-CHECK.json":label=label.split("/",1)[1]
            expanded=json.loads((ROOT/"eigen-expanded"/(label+".json")).read_text())
            row["raw_independent_same_index"]=row["independent"]
            row["independent"]=min(expanded["linear_multipliers"],key=lambda v:abs(v-row["owner"]))
            row["comparison"]="owner-returned eigenvalue exists in expanded independent spectrum"
            row["passed"]=bool(np.isclose(row["owner"],row["independent"],rtol=row["rtol"],atol=row["atol"]))
        final.append(row)
final.extend(dict(x,artifact="FE-RECONCILIATION.json") for x in audits["FE-RECONCILIATION.json"]["rows"])
dump("FINAL-AUDIT.json",dict(comparisons=len(final),passed=sum(x["passed"] for x in final),
    flagged=sum(not x["passed"] for x in final),rows=final))

anchors={}
for res in ["5","019"]:
    for mat in ["Hexoloy-SA","K13D2U-50-20-20-10"]:
        label=f"{mat}-{res}-same_tube_mass-m6-intact"
        calc=json.loads((ROOT/"fe"/(label+".json")).read_text())
        anchors[mat+"/"+res]=dict(SF_or_ceiling=calc["conditional_SF_or_ceiling"],
            required_scale_GPa=calc["q1_whole_member_scale_needed_m10_Pf1e3_Pa"]/1e9)
witnesses=[]
for row in read("WITNESSES.json")["rows"]:
    calc=json.loads((ROOT/"fe"/(row["FE"]["label"]+".json")).read_text())
    base=BASE[row["reserve"]]
    witnesses.append(dict(material=row["material"],reserve=row["reserve"],
       frame_kg=calc["frame_tubes_kg"]+base["mass_kg"]["joint"]+base["mass_kg"]["nodes"],
       total_including_reserve_sag_kg=calc["total_mass_including_reserve_sag_kg"],
       SF_or_ceiling=calc["conditional_SF_or_ceiling"]))
gaprows=json.loads((ROOT/"INDEPENDENT-GAPS.json").read_text())
hexg=next((g,o) for g,o in zip(gaprows,read("GAPS.json")["rows"])
           if o["material"]=="Hexoloy-SA" and o["reserve"]=="5" and o["section_policy"]=="same_tube_mass" and o["load_case"]=="operating")
anchors["Hexoloy_5_hypothetical_Pf"]=hexg[0]["hypothetical_Pf_m10_if_typical_is_member_scale"]
anchors["Hexoloy_5_combined_hypothetical_load"]=hexg[0]["joint_mechanical_and_hypothetical_reliability_q"]
hail=json.loads((ROOT/"INDEPENDENT-HAIL.json").read_text())
designindex=next(i for i,x in enumerate(read("HAIL.json")["rows"]) if
    x["material"]=="Hexoloy-SA" and x["reserve"]=="5" and x["section_policy"]=="same_tube_mass" and x["diameter_m"]==.0508)
stress=hail[designindex]["stress_Shi_Pa"]
anchors["Hexoloy_5_hail"]={"Shi_stress_MPa":stress/1e6,
    "conditional_299_m4p6":probability([stress],4.6,299e6),
    "conditional_192_m5p5":probability([stress],5.5,192e6)}
damage=read("DAMAGE.json")["rows"]
anchors["all_72_secondary_overload_triggers_reproduced"]=all(
    json.loads((ROOT/"fe"/(f"{v['material']}-{v['reserve']}-same_tube_mass-m6-lost{v['removed_member']}.json")).read_text())["conditional_SF_or_ceiling"]<1
    for v in damage)
nfi=read("NFI.json")
for row in nfi:row["origin"]="MAINLINE-051 owner; retained by checker"
nfi.extend([
 dict(id="CHECK051-signed-stress-label",status="Open labeling fix",tag="QUESTIONABLE",
      issue="336 HAIL surface_stress_Pa shear values discard the tensor sign. Rename as magnitude or retain signed values. Utilization and probability are unaffected.",
      evidence="DISCREPANCIES.json"),
 dict(id="CHECK051-ill-conditioned-shape",status="Open numerical presentation fix",tag="QUESTIONABLE / PROJECTION",
      issue="FRAME-COMPARE rows32/86 report m about 6.8e12/2.25e11 at an active compression limit. Independent values differ; 1e-8 thinner wall makes finite m impossible. Use a resolution-aware infeasible/unbounded flag and retain required scale targets.",
      evidence="SENSITIVITIES.json"),
 dict(id="CHECK051-joint-reference",status="Open physical/source qualification",tag="QUESTIONABLE / PROJECTION",
      issue="Legacy sleeves retain1470MPa while current cited T700S composite compression is1450MPa. Matching sleeve construction remains unqualified. A 1450 sensitivity reduces K13D2U ceilings to1.120291/1.061343; both still exceed1.",
      evidence="SENSITIVITIES.json; SOURCE-CHECK.md"),
 dict(id="CHECK051-eigen-order",status="Resolved numerical; label guidance",tag="QUESTIONABLE",
      issue="49 higher-mode index differences across25 solves, repeated16 times in witness records, reflect returned multiplicity/order. Expanded independent12-mode solves contain every owner value; lowest factors match. Do not identify modes by array index across solves.",
      evidence="FE-RECONCILIATION.json; eigen-expanded/"),
 dict(id="CHECK051-member-ids",status="Resolved data mapping",tag="QUESTIONABLE",
      issue="Original041/043-fold and CHECK041 use different member numbering. Coordinate/edge maps reconcile all3000 member stress comparisons; the target surface is unchanged.",
      evidence="MEMBER-ID-MAP-5.json; MEMBER-ID-MAP-019.json")
])
dump("NFI.json",nfi)
start=json.loads((ROOT/"START.json").read_text())["started_at"]
result=dict(task="CHECK-051",status="COMPLETE — conditional arithmetic checked; qualification remains open",
   started_at=start,scientific_completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
   time_budget=None,owner_code_accessed=False,own_prior_solver_reused="041 beam.py, frame_tools.py, score.py",
   coverage=dict(target_rows=288,material_models=18,fixed_frame_rows=108,gap_rows=280,witnesses=36,
      hail_rows=980,hail_target_rows=15680,member_loss_rows=72,fresh_FE_cases=182,
      additional_expanded_eigen_solves=25,minimum_wall_inversions=36),
   final_comparisons=len(final),flagged_fields=sum(not x["passed"] for x in final),
   unresolved_categories=["signed tensor versus magnitude labeling","ill-conditioned shape inversion"],
   outcome_changing_numerical_discrepancy_found=False,anchors=anchors,witnesses=witnesses,
   qualified_structural_SF=None,qualified_frame_probability=None,actual_hail_break_probability=None,
   dynamic_cascade_probability=None,NFI_count=len(nfi),next="none")
dump("RESULTS.json",result)
lines=[
 "**CHECK-051 COMPLETE — the requested conditional results reproduce.**",
 "",
 "QUESTIONABLE / PROJECTION. No outcome-changing arithmetic discrepancy was found. Physical qualification remains open. The original partial and completed owner packages were checked from pinned non-code inputs; no owner or upstream-owner program was read, copied, hashed, imported or run.",
 "",
 f"Coverage: 288 target rows over m=5–40; 18 constitutive models; 108 fixed-force comparisons; 36 independent minimum-wall inversions and 36 fresh-FE passing witnesses; 280 strength-gap rows; 980 hail scenarios with 15,680 target scales; and 72 member-loss cases. All 182 published FE cases were re-solved, with 25 additional 12-mode solves to resolve eigenvalue ordering. The final audit has {len(final):,} comparisons and {sum(not x['passed'] for x in final):,} flagged fields in the two categories below.",
 "",
 "| Result | 5% reserve | 019 reserve |",
 "|---|---:|---:|",
 f"| Hexoloy same-mass mechanical SF | {anchors['Hexoloy-SA/5']['SF_or_ceiling']:.9f} | {anchors['Hexoloy-SA/019']['SF_or_ceiling']:.9f} |",
 f"| Hexoloy required whole-member m10 scale, GPa | {anchors['Hexoloy-SA/5']['required_scale_GPa']:.9f} | {anchors['Hexoloy-SA/019']['required_scale_GPa']:.9f} |",
 f"| K13D2U 50/20/20/10 mechanical ceiling | {anchors['K13D2U-50-20-20-10/5']['SF_or_ceiling']:.9f} | {anchors['K13D2U-50-20-20-10/019']['SF_or_ceiling']:.9f} |",
 f"| K13D2U required whole-member m10 scale, GPa | {anchors['K13D2U-50-20-20-10/5']['required_scale_GPa']:.9f} | {anchors['K13D2U-50-20-20-10/019']['required_scale_GPa']:.9f} |",
 "",
 "The strength targets above are at operating q=1 and frame Pf=1e-3. The older own-screen targets 4.278678/4.209090 GPa refer to different loads. The whole-member and coupon size conventions reproduce independently and remain alternative hypotheses.",
 "",
 "| 5% reserve witness | Frame kg | Total including reserve/sag kg | Mechanical SF or ceiling |",
 "|---|---:|---:|---:|"]
for mat in ["K13D2U-50-20-20-10","M55J-50-20-20-10","Al6061T6"]:
    w=next(x for x in witnesses if x["material"]==mat and x["reserve"]=="5")
    lines.append(f"| {mat} | {w['frame_kg']:.6f} | {w['total_including_reserve_sag_kg']:.6f} | {w['SF_or_ceiling']:.9f} |")
lines.extend([
 "",
 f"Hexoloy's invented whole-member 3.9 GPa/m10 distribution gives operating Pf={anchors['Hexoloy_5_hypothetical_Pf']:.10g} and a combined load multiplier {anchors['Hexoloy_5_combined_hypothetical_load']:.9f}. The 50.8 mm design-hail Shi stress is {stress/1e6:.6f} MPa; transferred probabilities reproduce {anchors['Hexoloy_5_hail']['conditional_299_m4p6']*100:.6f}% and {anchors['Hexoloy_5_hail']['conditional_192_m5p5']*100:.6f}%. Actual impact fracture probabilities remain unidentified.",
 "",
 "All 72 sampled losses reproduce a secondary-overload trigger. Joint and film failures remain independent obstacles; this does not simulate a dynamic rupture chain or establish lifetime failure probability.",
 "",
 "**Exact discrepancies and dispositions**",
 "",
 "- 336 shear fields in HAIL.json use positive magnitudes under a tensor-like surface_stress_Pa name. Independent signed values are negative. Every corresponding magnitude, utilization and probability matches. DISCREPANCIES.json lists each row, field, owner value and independent value; rename the field or preserve its sign.",
 "- FRAME-COMPARE rows32 and86, M55J-50-20-20-10 minimum-wall cases, report enormous required Weibull exponents. Owner versus independent values are 6,806,150,609,724.931 versus 6,812,112,419,084.157 and 224,890,447,498.35278 versus 224,903,840,631.78098. These inversions are ill-conditioned: a relative wall reduction of1e-8 changes both to no finite m. Report an unresolved/infeasible limit at practical precision, while retaining stable required-scale targets.",
 "- 49 higher-mode array-index differences (plus16 duplicate witness fields) resolve through 25 expanded independent eigensolves. Every owner-returned value appears in the independent low spectrum; lowest factors are unchanged. The complete raw differences and reconciliation are retained.",
 "- Initial checker diagnostics from member numbering and unknown-versus-empty failure sets were corrected. Both coordinate maps and all corrected member-set comparisons are retained; these are not owner arithmetic defects.",
 "",
 "The 16 owner qualification NFIs remain, with three additional open fixes/sensitivities and two resolved mapping/spectrum entries. A sensitivity replacing the legacy1470MPa joint-sleeve input with the current cited1450MPa T700S compression average gives K13D2U ceilings1.120291/1.061343. It does not qualify that sleeve construction.",
 "",
 "SOURCE-CHECK.md records the primary material audit. The published figures were visually inspected, and all four CSV exports match their JSON detail records. Numerical tolerances are2e-8 for scalar/hail arithmetic and3e-6 for independent FE and dependent gap comparisons, with documented absolute floors. See METHOD.md, FINAL-AUDIT.json, DISCREPANCIES.json and the per-attempt execution receipts.",
 "",
 "No time budget was applied. All launched jobs are accounted for in EXECUTION.json. Stop and file; next job none."
])
(ROOT/"CHECK.md").write_text("\n".join(lines)+"\n")
print(json.dumps(dict(final_comparisons=len(final),flagged_fields=result["flagged_fields"],
                     categories=collections.Counter(x["category"] for x in discrepancies),anchors=anchors),indent=1))
