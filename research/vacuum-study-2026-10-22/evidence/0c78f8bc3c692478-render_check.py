"""Administrative rendering of completed, saved scientific results."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
s=json.loads((R/'SUMMARY.json').read_text());a=json.loads((R/'ACCOUNT-RESULTS.json').read_text());extra=json.loads((R/'EXTRA-AUDITS.json').read_text());sup=json.loads((R/'SUPPLEMENTAL-RESULTS.json').read_text())
original=next(x for x in s['primary'] if x['R_m']==10 and x['weather']=='ISA' and x['drying']=='bake70' and not x['cure_in_global'])
revised=next(x for x in s['primary'] if x['R_m']==10 and x['weather']=='ISA' and x['drying']=='bake70' and x['cure_in_global'])
def axes(mask):return 'none' if mask is None else '+'.join(name for bit,name in [(1,'G'),(2,'Q'),(4,'E/Fcy'),(8,'film')] if mask&bit)
def least(row):return 'none' if row['least_mask'] is None else f"{axes(row['least_mask'])} {row['least_usage']:.9f}"
lines=['# Complete independent CHECK MAINLINE-048','',
'**The numerical main account and supplied cure/water addendum reproduce. Two source corrections and twelve ambiguous/null sensitivity least-set entries need correction. All installed-hull qualification values remain unknown.**','',
'QUESTIONABLE material transfers; PROJECTION installation, manufacturing, processing and operation. This report completes the resumed check and preserves the previously filed partial package. No owner executable was accessed.','',
'## Result and coverage','',
'| Check | Independent coverage | Result |','|---|---:|---|',
f"| Stored accounts | {a['distinct_points']:,} distinct points; {a['comparison_count']:,} comparisons | All pass, including a tighter 2e-8 relative/absolute audit |",
f"| Subsets and least sets | {s['total_configurations']:,} configurations; {s['subset_optimizations']:,} subset optimizations; {s['search_comparisons']:,} comparisons | All selected masks, counts, ties and common usages agree |",
f"| Favorable E bounds | {s['favorable_E_bounds']:,} bounds; {s['E_usage_cases']} selected E cases | All exclusions reproduce; no sampled/refined E improvement over the common-usage point |",
'| Current thermal tables | 13 finishes × 3 radii; 241 core thicknesses each | Independently reconstructed tables agree |',
f"| Direct thermal convergence | {s['thermal_convergence_points']} endpoint core thicknesses at 256 nodes | Every checked gradient/curvature ratio is covered by the 1.002 guard |",
f"| Water, resource, service and reconciliation audit | {s['supplemental_comparisons']:,} comparisons | All pass |",
f"| Extra audit | {s['extra_comparisons']:,} comparisons, including six optical limits and 43 historical040 targets | 24 null-versus-computed least-field differences in 12 cases; all other comparisons pass |",
f"| Exact E and optical-screen detail | {s['detail_comparisons']} comparisons | All pass |",'',
'Raw account values are in [ACCOUNT-COMPARISONS.csv.gz](ACCOUNT-COMPARISONS.csv.gz); all search deltas are in [SEARCH-COMPARISONS.csv](SEARCH-COMPARISONS.csv). [SUMMARY.json](SUMMARY.json) links the independent results. The largest search payload difference is '+f"{s['largest_search_differences']['payload']['delta']:.12f} kg"+' (a favorable-E bound, below the 0.002 kg comparison tolerance). The largest common-usage difference is '+f"{s['largest_search_differences']['usage']['delta']:.12g}"+'. No discrete selection differs.','',
'## R10 reconciliation and addendum','',
f"The independently reoptimized original040 endpoint is {s['old040_R10']['payload_kg']:.9f} kg, compared with the filed −109.649207820 kg. The new original048 multilayer bake endpoint is {original['payload_kg']:.9f} kg, compared with +124.261910191 kg. The mass recovery is chiefly coating replacement; the exterior-water charge remains aboard.",'',
'| Old-to-new bill contribution | Payload gain, kg |','|---|---:|']
for k,v in s['reconciliation'].items():lines.append(f'| {k} | {v:+.9f} |')
lines+=['',f"Including balanced cure compression in global buckling and crimping yields {revised['payload_kg']:.9f} kg at the R10 ISA/floor/bake named endpoint. The least set changes from {least(original)} to {least(revised)}. This is a structural-model sensitivity, not a measured residual-stress field.",'',
'| R, m | Weather | Route | Original endpoint, kg | Cure-included endpoint, kg | Original least | Cure-included least |','|---:|---|---|---:|---:|---|---|']
for before in s['primary']:
 if before['cure_in_global']:continue
 after=next(x for x in s['primary'] if x['id']==before['id']+'-cure_included')
 lines.append(f"| {before['R_m']} | {before['weather']} | {before['drying']} | {before['payload_kg']:+.6f} | {after['payload_kg']:+.6f} | {least(before)} | {least(after)} |")
lines+=['','All rows above use the multilayer candidate, retained joining floor and 0.1 mm exterior retention. The complete four-finish, actual/floor and dry/wet matrices are retained in the four SEARCH files. G, Q, E/Fcy and film are separately counted axes.','',
'The following original cases lose all floating subsets when cure compression is included:','']
lines += ['- '+x for x in s['lost_float_configurations']]
lines += ['', 'At R15 optimistic weather with multilayer and sorbent, both joining conventions require three axes after the cure change, rather than two.','',
'| R, m | Extra water when changing 0.1 to 1 mm, kg |','|---:|---:|']
for x in s['water_offsets']:lines.append(f"| {x['R_m']} | {x['added_kg']:.9f} |")
lines += ['',f"All {s['one_mm_configurations']} one-millimetre configurations are non-floating in the stated model. The best all-four payload is {s['best_one_mm']['all_four_payload_kg']:.9f} kg; the most favorable relaxed-E bound is {s['best_one_mm_bound']['independent']['payload_kg']:.9f} kg. Both occur in the original-cure R10 ISA/actual/bake multilayer case. The mass scenario is independently reproduced; neither 0.1 mm nor 1 mm is a measured outdoor retention limit.",'',
'## Exact correction list','',
'| Filed field or statement | Filed value | Independent finding | Disposition |','|---|---|---|---|',
'| COATINGS.SolarWhite.areal_mass_kg_m2; CARD mass row | null / unknown; density or mass said absent | Manufacturer sheet: 0.285 kg/m² at150 μm, 1.9 g/cm³ | Correct source coverage; complete installed Be mass remains unqualified |',
'| SolarWhite optical heading interpretation | .15–.18 website heading treated as uncertain absorptance | Linked manufacturer sheet explicitly gives typical α=.18, εH=.89 on Al2024-T3 | Source-label ambiguity resolved for that specimen |',
'| COATINGS.CCAg.optical_source | NASA2015 slide19 cited for model .09/.65 | Cited slide gives .08 / normal .72 on3mil Kapton | Use the patent for its different .09/.65–.70 range and state the unresolved emittance statistic/Be transfer |',
'| SENSITIVITIES least at12 R12/R15 optical rows | null | Independent floating subsets and positive-payload witnesses | Populate entries or explicitly label not searched; null is not no-float evidence |','',
'[SOURCE-AUDIT.md](SOURCE-AUDIT.md) provides primary references and distinguishes matched measurements from transferred/assumed properties. SolarWhite’s source mass does not displace the lightest deposited recipe; its legacy full-cycle screen still fails. No optimistic mass allowance was added to make it lead.','',
'For each row below the exact filed `least` value is null. Common usage is the independent least root. The separate positive witness increases common usage slightly and is reoptimized on1801 core-grid points.','',
'| Source row | Optical case | R, m | Weather | Independent least mask | Common usage | Positive witness payload, kg |','|---:|---|---:|---|---:|---:|---:|']
for x in s['null_field_witnesses']:
 lines.append(f"| {x['source_row_index']} | {x['type']} | {x['R_m']} | {x['weather']} | {x['independent_least_mask']} | {x['independent_common_usage']:.12f} | {x['positive_witness']['signed_payload_kg']:.12f} |")
lines += ['','All twelve full witnesses, modes, geometry, bills and pressure values are in [NULL-SENSITIVITY-WITNESSES.json](NULL-SENSITIVITY-WITNESSES.json). The differences comprise12 mask fields and12 usage fields. A positive current-account payload does not repair a failed legacy finish screen; wet/aged optics remain assumed.','',
'## Source, thermal and process limits','',
'The multilayer recipe independently totals7.5752 g/m² before10%; classical lower/upper recipes total9.3256–11.1786 g/m². Bulk-density transfer, classical ITO cap, the patent’s total-thickness ambiguity and the absence of a matched recipe/Be optical specimen remain open. Catalog bare-film mass is kept separate from adhesive-backed tape.','',
'The initial thermal reconstruction omitted the supplied natural-convection maximum and extra radiative conductance. The independent coupled Newton solver now reproduces the current tables. Legacy night curvature requires mean removal while legacy day retains the raw midpoint projection: all26 diagnostic differences are reconciled explicitly. Numerical boundary closure does not validate the physical convection, core approximation or actual weather/wetting mission.','',
'WVR, TML, material-water inventory and exterior liquid are distinct. The historical AF163-2U WVR bound is not an installed sorption isotherm. The70°C coupon source does not demonstrate90% hull-wide water removal or the inherited nominal volatile conditioning. Onboard adsorption retains mass. The detailed200°F source uses2K .060 film/EC3924B/metal joints/50psi; it does not qualify2U .015 onBe/honeycomb.','',
'All thirteen partial-check NFI identifiers are retained with continuation dispositions, and four new entries record the source correction, exact bond transfer, physical thermal boundary and null sensitivity fields. [NFI.json](NFI.json) distinguishes resolved numerical work from open evidence. Installed-hull SF remains null.','',
'## Execution and closeout','',
'Every scientific job used simjob with1CPU/3GiB, numerical threads1 and a900-second technical watchdog. Exit75 admission refusals were retried only under the explicit resume authority, at least60seconds apart. Missing optional ties and NumPy-boolean serialization caused failed checker invocations; corrected reruns completed and all receipts remain. [EXECUTION.json](EXECUTION.json) records outcomes and released reservations.','',
'Final custody checks cover all pinned non-code inputs, own execution snapshots, the immutable partial package and previous043 artifacts. Recorded live-source drift does not replace the dispatch-pinned brief. No owner code, out-of-band seat contact or successor work is involved. The numerical check is complete; the brief says stop and file.']
(R/'CHECK.md').write_text('\n'.join(lines)+'\n')
(R/'CARD.md').write_text('# CHECK-048 — complete\n\nQUESTIONABLE / PROJECTION. The original432 configurations and648 cure/water additions independently reproduce:17,858 witness points,1,714,368 tight comparisons,17,280 subset optimizations and3,775 favorable-E bounds.\n\nR10 ISA/floor/bake is +124.262kg before cure inclusion and +118.695kg after. All432 one-millimetre water rows remain negative.\n\nCorrections: SolarWhite has a manufacturer285g/m² mass; the classical CCAg optical citation/statistic needs correction;12 null sensitivity least fields have independent floating witnesses. Physical qualification remains open.\n\nSee [CHECK.md](CHECK.md), [SUMMARY.json](SUMMARY.json), [SOURCE-AUDIT.md](SOURCE-AUDIT.md), [NFI.json](NFI.json) and [MANIFEST.json](MANIFEST.json). Original partial and prior043 packages remain frozen. No successor.\n')
old=Path('.ship/work/outputs/mainline048-independent-check-1020/NFI.json')
if not old.exists():old=R.parent/'mainline048-independent-check-1020/NFI.json'
nfi=json.loads(old.read_text());nfi['checker_complete']=True
resolved={
 'NFI-048-C01':('resolved_numerically','Independent current tables and legacy conventions reproduce; physical boundary is separately retained as C16.','THERMAL-RESOLVED-RESULTS.json; EXTRA-AUDITS.json'),
 'NFI-048-C02':('resolved_numerically','All1080 configurations,16 subsets each, all ties/common roots and3775 E bounds independently reproduce.','SEARCH-*.json; SUMMARY.json'),
 'NFI-048-C03':('resolved_numerically','Species normalization and net desorption corrections pass the complete tighter witness audit.','DETAIL-VALIDATION.json'),
 'NFI-048-C12':('resolved_check_coverage','Auxiliary arithmetic, independent sensitivity searches, old040 targets and source review completed. Null least fields are explicitly carried in C17.','SUPPLEMENTAL-RESULTS.json; EXTRA-AUDITS.json; SOURCE-AUDIT.md'),
 'NFI-048-C13':('resolved_authority_and_execution','Explicit resume order authorized>=60s unchanged exit75 retries; all final jobs completed and reservations released.','EXECUTION.json; intake/RESUME-ORDER.json')}
for row in nfi['rows']:
 row['partial_finding']=row.pop('finding');row['status']='open_evidence'
 if row['id'] in resolved:
  status,finding,evidence=resolved[row['id']];row.update(status=status,finding=finding,continuation_evidence=evidence)
 else:row['finding']=row['partial_finding']
 if row['id']=='NFI-048-C13':row['automatic_retry']=True
nfi['rows'] += [
 dict(id='NFI-048-C14',status='source_correction_to_file',topic='SolarWhite linked manufacturer mass and optical label',finding='The source sheet supplies285g/m² at150um and1.9g/cm³ with alpha .18/hemispherical epsilon .89 onAl2024-T3. Correct the claimed absence and ambiguous web-heading interpretation; installed Be qualification is still absent.',evidence='sources/enbio-solarwhite-datasheet.pdf; SOLARWHITE-SOURCE.json; SOURCE-AUDIT.md',qualified_installed_Be_mass_kg_m2=None),
 dict(id='NFI-048-C15',status='open_evidence',topic='Exact200F bond transfer and tooling',finding='The detailed200F tests useAF163-2K .060lb/ft²,EC3924B and metal joints at50psi, not2U .015Be/honeycomb. Require exact construction allowables,process/tooling evidence and measured stress-free temperature.',evidence='intake/addendum048/8-WATER-AND-BOND-SOURCES.md; pinned3M sheet',qualified_bond_strength_Pa=None),
 dict(id='NFI-048-C16',status='open_evidence',topic='Physical thermal and residual-stress boundary',finding='Numerical equivalence is closed. The actual convection,radiative core term,coupled weather/wetting and residual cure field remain unqualified. Cure inclusion is a sensitivity; whole-hull scalar modes remain projections.',evidence='METHOD.md; thermal and addendum checks',installed_hull_SF=None),
 dict(id='NFI-048-C17',status='result_or_status_correction_to_file',topic='Twelve null sensitivity least-set fields',finding='Independent floating subsets exist for12 R12/R15 optical sensitivity rows with null least fields. Populate them or explicitly marknot searched; do not use null as a no-geometry conclusion. Failed legacy finish screens and physical qualification remain separate.',evidence='EXTRA-AUDITS.json; NULL-SENSITIVITY-WITNESSES.json',mismatches=extra['mismatches'])]
(R/'NFI.json').write_text(json.dumps(nfi,indent=2)+'\n')
(R/'MISMATCHES.json').write_text(json.dumps(dict(open_sensitivity_fields=extra['mismatches'],source_corrections=[nfi['rows'][3],nfi['rows'][13]],resolved_legacy_curvature_diagnostics='THERMAL-RESOLVED-RESULTS.json reconciled by EXTRA-AUDITS.json',main_search_mismatches=s['search_mismatches'],tight_witness_mismatches=[]),indent=2)+'\n')
(R/'SCOPE.json').write_text(json.dumps(dict(full_check_complete=True,original_configurations=432,addendum_configurations=648,witness_points=17858,witness_comparisons=1714368,subset_optimizations=17280,favorable_E_bounds=3775,owner_code_accessed=False,physical_qualification=False,installed_hull_SF=None,nonblocking_corrections=['SolarWhite manufacturer mass/optics','classical CCAg optical citation/statistic','12 null optical sensitivity least fields'],next='none',time_budget=None),indent=2)+'\n')
body='''Complete CHECK MAINLINE-048, including the supplied cure/water addendum. QUESTIONABLE/PROJECTION; installed-hull SF remains unknown. Owner executable code was never accessed.

Independent thermal reconstruction,17,858 witness points/1,714,368 tighter comparisons,1,080 configurations/17,280 subset optimizations and3,775 favorable-E bounds reproduce. Every main least-set selection agrees; maximum search payload difference0.000638kg. Supplemental water/resource/service arithmetic and historical040 checks also complete.

R10 ISA/floor/bake reproduces+124.262kg; including cure compression yields+118.695kg. Two formerly floating cases fail with cure. All432 one-millimetre-water cases remain negative; the best relaxed bound is−998.280kg.

Corrections: the linked SolarWhite manufacturer sheet supplies285g/m² and explicit .18/.89 aluminum-substrate optics, contrary to the claimed missing mass/label ambiguity. Classical CCAg’s cited NASA slide supplies different optics and normal emittance. Twelve null R12/R15 sensitivity least fields have independently verified floating witnesses; populate them or labelnot searched. These witnesses do not cure failed finish screens or qualify wet/aged optics.

Exact differences and seventeen NFI dispositions retain material,bond,retention,conditioning and physical-boundary qualifications. Both orders are complete. Mandatory simjob retries and corrected checker failures retain receipts; every admitted reservation released. Custody verifies pinned inputs and frozen partial/prior043 artifacts. No time budget,live own work,successor or out-of-band contact. SLEEPING.'''
# Presentation only: separate punctuation-adjacent prose for the queue body.
for a,b in [('reconstruction,17','reconstruction, 17'),('comparisons,1','comparisons, 1'),('and3','and 3'),('difference0','difference 0'),('reproduces+','reproduces +'),('yields+','yields +'),('All432','All 432'),('is−','is −'),('supplies285','supplies 285'),('labelnot','label not'),('material,bond,retention,conditioning','material, bond, retention, conditioning'),('budget,live','budget, live'),('work,successor','work, successor')]:body=body.replace(a,b)
assert len(body.split())<=250,len(body.split())
(R/'REPORT-BODY.txt').write_text(body+'\n')
print(json.dumps(dict(rendered=True,report_words=len(body.split()),nfi_entries=len(nfi['rows']))))
