# Counterfactual dry-air constant study

Scratch copies only. All gas-specific constants and density dials stay unchanged.
Old: JS 287.0528; Python 287.05. New: 8314.32 J/(kmol K) / 28.9644 kg/kmol = 287.05307204706463 J/(kg K).

JS constant relative change: 9.47724824983e-07 (9.47724824983e-05%).
Python constant relative change: 1.07021322579e-05 (0.00107021322579%).

10414 changed leaves: 10378 numeric; 36 text or flag; 0 added; 0 removed.
Baseline regeneration drift: 187 leaves.

Old means a fresh original-constant run. Published old is the committed cache; any difference between these columns predates the constant change.

Relative effect = constant effect / absolute fresh old value. It is signed; rankings, medians and decade bands use its magnitude. Text and flags have no relative effect; fresh old zero is undefined. JSON null is treated as an absent side.

A large relative effect on a small residual does not imply a large physical change. These are model comparisons, not current drawn-hull float evidence.

## Effects by output

| Published/generated file | Changed leaves | Largest relative magnitude | Field | Median relative magnitude |
| --- | ---: | ---: | --- | ---: |
| research/figures.json | 39 | 7.98782140486e-06 | /classes/P100/bases/favourable/worst/unheldT | 3.1715713307e-07 |
| research/analysis/mass-budget.json | 151 | 0.000308071472582 | /classes/P1000/airBallast/idealWorkMWh | 2.80946738916e-06 |
| research/analysis/delivery.json | 78 | 0.0416666666667 | /classes/P1000/coverageLevelBySwath/80 m | 0.000312341283098 |
| research/analysis/vacuum-cell.json | 6 | 0.00109529025192 | /ship0/worldsFramePractice/s1050_sf12/ratioSL | 7.21759672315e-06 |
| research/analysis/helium.json | 2 | 1.33901073887e-05 | /atmosphere/pPa | 8.32444322608e-06 |
| research/analysis/water-availability.json | 9619 | 0.0665661880026 | /classes/P1000/acceptedPlans/byFire/737/releasedT | 1.12998364312e-06 |
| research/analysis/descent.json | 401 | 1 | /favourableClasses/P100/profile/3/unheldT | 2.52773673535e-07 |
| research/geometry/skin/loaded-skin.json | 2 | 2.67801072004e-06 | /numbers/p2500Pa | 2.67801072004e-06 |
| ship/skin.generated.js | 1 | 2.67801072004e-06 | /numbers/p2500Pa | 2.67801072004e-06 |
| research/validation/report.json | 115 | 22.7254892282 | /checks/0/rows/22/difference | 8.10531599538e-06 |

## Relative magnitudes by decade

10375 defined numeric relative effects; 39 undefined or categorical. Rounding-scale band: magnitude below 1e-12 (6 nonzero effects). This names a floating-point rounding scale, not a proof that every effect in it is rounding.

| Relative magnitude band | Leaves |
| --- | ---: |
| [1e-15, 1e-14) | 2 |
| [1e-14, 1e-13) | 4 |
| [1e-9, 1e-8) | 1 |
| [1e-8, 1e-7) | 82 |
| [1e-7, 1e-6) | 3300 |
| [1e-6, 1e-5) | 6804 |
| [1e-5, 1e-4) | 47 |
| [1e-4, 1e-3) | 49 |
| [1e-3, 1e-2) | 39 |
| [1e-2, 1e-1) | 15 |
| [1e-1, 1e0) | 13 |
| [1e0, 1e1) | 17 |
| [1e1, 1e2) | 2 |

## Selected full rows

86 numeric leaves have magnitude at least 1e-3. List the largest 40; when more than 40 meet that threshold, select all of them up to 200. Ties sort by file and field. Special rows sort by file and field.

Complete rows remain in constant-study.json, changed_fields. The Markdown byte budget can omit special rows; exact counts follow.

Selected numeric rows: 86; listed: 86; omitted by row cap: 10289; omitted by byte budget: 0.

| Published/generated file | Field | Published old | Fresh old | Standard R | Constant effect | Relative effect |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| research/validation/report.json | /checks/0/rows/22/difference | 0.00908350243116729 | 0.00908350243116729 | 0.21551053908478934 | 0.20642703665362205 | 22.7254892282 |
| research/validation/report.json | /checks/0/rows/25/difference | 0.00908350243116729 | 0.00908350243116729 | 0.21551053908478934 | 0.20642703665362205 | 22.7254892282 |
| research/validation/report.json | /checks/0/rows/2/difference | 3.1684982304547304e-07 | 3.1684982304547304e-07 | -8.441122876234886e-07 | -1.1609621106689616e-06 | -3.66407687879 |
| research/validation/report.json | /checks/0/rows/23/difference | -2.2810980562226746e-06 | -2.2810980562226746e-06 | -1.0439080116553257e-05 | -8.157982060330582e-06 | -3.57633992895 |
| research/validation/report.json | /checks/0/rows/26/difference | -2.2810980562226746e-06 | -2.2810980562226746e-06 | -1.0439080116331212e-05 | -8.157982060108537e-06 | -3.57633992886 |
| research/validation/report.json | /checks/0/rows/32/difference | 5.434383921421038e-06 | 5.434383921421038e-06 | -1.6817924387568794e-06 | -7.116176360177917e-06 | -1.30947251116 |
| research/validation/report.json | /checks/0/rows/35/difference | 5.434383921421038e-06 | 5.434383921421038e-06 | -1.6817924387568794e-06 | -7.116176360177917e-06 | -1.30947251116 |
| research/validation/report.json | /checks/0/rows/5/difference | 1.2265990694482198e-05 | 1.2265990694482198e-05 | -8.441122876234886e-07 | -1.3110102982105687e-05 | -1.06881729398 |
| research/validation/report.json | /checks/0/rows/8/difference | 1.2265990694482198e-05 | 1.2265990694482198e-05 | -8.441122876234886e-07 | -1.3110102982105687e-05 | -1.06881729398 |
| research/validation/report.json | /checks/0/rows/40/difference | 0.2683396931242896 | 0.2683396931242896 | 0.5446700258762576 | 0.27633033275196794 | 1.02977807545 |
| research/validation/report.json | /checks/0/rows/43/difference | 0.2683396931242896 | 0.2683396931242896 | 0.5446700258762576 | 0.27633033275196794 | 1.02977807545 |
| research/analysis/descent.json | /favourableClasses/P100/profile/3/unheldT | 1.4210854715202004e-14 | 1.4210854715202004e-14 | 0 | -1.4210854715202004e-14 | -1 |
| research/validation/report.json | /checks/0/implementation_comparison/0/max_minus_min/density_kg_m3 | 1.1949140871436725e-05 | 1.1949140871436725e-05 | 0.0 | -1.1949140871436725e-05 | -1 |
| research/validation/report.json | /checks/0/implementation_comparison/1/max_minus_min/density_kg_m3 | 9.543071744388953e-06 | 9.543071744388953e-06 | 0.0 | -9.543071744388953e-06 | -1 |
| research/validation/report.json | /checks/0/implementation_comparison/1/max_minus_min/pressure_Pa | 0.10512893942359369 | 0.10512893942359369 | 0.0 | -0.10512893942359369 | -1 |
| research/validation/report.json | /checks/0/implementation_comparison/2/max_minus_min/pressure_Pa | 0.18814691694569774 | 0.18814691694569774 | 0.0 | -0.18814691694569774 | -1 |
| research/validation/report.json | /checks/0/implementation_comparison/3/max_minus_min/density_kg_m3 | 6.486002736005858e-06 | 6.486002736005858e-06 | 0.0 | -6.486002736005858e-06 | -1 |
| research/validation/report.json | /checks/0/implementation_comparison/3/max_minus_min/pressure_Pa | 0.2222505080717383 | 0.2222505080717383 | 0.0 | -0.2222505080717383 | -1 |
| research/validation/report.json | /checks/0/implementation_comparison/4/max_minus_min/pressure_Pa | 0.2518599206523504 | 0.2518599206523504 | 0.0 | -0.2518599206523504 | -1 |
| research/validation/report.json | /checks/0/implementation_comparison/4/max_minus_min/density_kg_m3 | 5.601949390143801e-06 | 5.601949390143801e-06 | 1.1102230246251565e-16 | -5.601949390032779e-06 | -0.99999999998 |
| research/validation/report.json | /checks/0/implementation_comparison/2/max_minus_min/density_kg_m3 | 7.435551878431923e-06 | 7.435551878431923e-06 | 2.220446049250313e-16 | -7.435551878209878e-06 | -0.99999999997 |
| research/validation/report.json | /checks/0/rows/31/difference | 0.28981736006971914 | 0.28981736006971914 | 0.5336614574043779 | 0.24384409733465873 | 0.841371604779 |
| research/validation/report.json | /checks/0/rows/34/difference | 0.28981736006971914 | 0.28981736006971914 | 0.5336614574043779 | 0.24384409733465873 | 0.841371604779 |
| research/validation/report.json | /checks/0/rows/44/difference | 7.603213680318355e-06 | 7.603213680318355e-06 | 1.4569838131528456e-06 | -6.146229867165509e-06 | -0.808372633677 |
| research/validation/report.json | /checks/0/rows/41/difference | 7.603213680540399e-06 | 7.603213680540399e-06 | 1.456983813263868e-06 | -6.146229867276531e-06 | -0.808372633668 |
| research/validation/report.json | /checks/0/rows/29/difference | -1.0516188145848204e-06 | -1.0516188145848204e-06 | -1.6817924387568794e-06 | -6.30173624172059e-07 | -0.599241488867 |
| research/validation/report.json | /checks/0/rows/38/difference | 2.0012642903965983e-06 | 2.0012642903965983e-06 | 1.456983813263868e-06 | -5.442804771327303e-07 | -0.271968315102 |
| research/validation/report.json | /checks/0/rows/13/difference | 0.45515908136439975 | 0.45515908136439975 | 0.5705022106558317 | 0.11534312929143198 | 0.253412782506 |
| research/validation/report.json | /checks/0/rows/16/difference | 0.45515908136439975 | 0.45515908136439975 | 0.5705022106558317 | 0.11534312929143198 | 0.253412782506 |
| research/validation/report.json | /checks/0/rows/14/difference | 5.2281952490851324e-05 | 5.2281952490851324e-05 | 4.181168773564892e-05 | -1.0470264755202408e-05 | -0.200265373736 |
| research/validation/report.json | /checks/0/rows/17/difference | 5.2281952490851324e-05 | 5.2281952490851324e-05 | 4.181168773564892e-05 | -1.0470264755202408e-05 | -0.200265373736 |
| research/validation/report.json | /checks/5/rows/1/difference | -8.635056730899038e-05 | -8.635056730899038e-05 | -9.946067029109606e-05 | -1.3110102982105687e-05 | -0.151824167353 |
| research/validation/report.json | /checks/0/rows/19/difference | 0.19723041937686503 | 0.19723041937686503 | 0.21551053908478934 | 0.018280119707924314 | 0.0926840786816 |
| research/validation/report.json | /checks/0/rows/20/difference | -9.716649934654598e-06 | -9.716649934654598e-06 | -1.0439080116553257e-05 | -7.224301818986589e-07 | -0.0743497179333 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/byFire/737/releasedT | 179.80600000000004 | 179.80600000000004 | 191.77499999999998 | 11.968999999999937 | 0.0665661880026 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/byFire/737/tph | 713.7721352595107 | 713.7721352595107 | 757.9507271446012 | 44.17859188509044 | 0.0618945314656 |
| research/validation/report.json | /checks/0/rows/37/difference | 0.52019961377664 | 0.52019961377664 | 0.5446700258762576 | 0.024470412099617533 | 0.0470404272736 |
| research/validation/report.json | /checks/0/rows/28/difference | 0.5120678681414574 | 0.5120678681414574 | 0.5336614574043779 | 0.021593589262920432 | 0.0421693892673 |
| research/analysis/delivery.json | /classes/P1000/coverageLevelBySwath/80 m | 2.4 | 2.4 | 2.3 | -0.10000000000000009 | -0.0416666666667 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/byFire/737/suppliedMWh | 15.07218587759914 | 15.07218587759914 | 15.552862793893297 | 0.48067691629415776 | 0.0318916526241 |
| research/analysis/delivery.json | /classes/P1000/coverageLevelBySwath/50 m | 3.8 | 3.8 | 3.7 | -0.09999999999999964 | -0.0263157894737 |
| research/validation/report.json | /checks/0/rows/11/difference | 4.273888074646237e-05 | 4.273888074646237e-05 | 4.181168773564892e-05 | -9.271930108134541e-07 | -0.0216943680934 |
| research/validation/report.json | /checks/0/rows/10/difference | 0.5602880207879934 | 0.5602880207879934 | 0.5705022106558317 | 0.010214189867838286 | 0.0182302485309 |
| research/analysis/delivery.json | /classes/P1000/coverageLevelBySwath/30 m | 6.3 | 6.3 | 6.2 | -0.09999999999999964 | -0.015873015873 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/byFire/737/options/ballastT | 820.194 | 820.194 | 808.225 | -11.968999999999937 | -0.0145928889994 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/byFire/737/retainedT | 820.194 | 820.194 | 808.225 | -11.968999999999937 | -0.0145928889994 |
| research/validation/report.json | /checks/5/rows/2/difference | -0.0009009264200823264 | -0.0009009264200823264 | -0.0009140359743202708 | -1.3109554237944465e-05 | -0.0145511930228 |
| research/analysis/delivery.json | /classes/P1000/_lineKmAtCL4/80 m swath | 1.47 | 1.47 | 1.46 | -0.010000000000000009 | -0.00680272108844 |
| research/analysis/delivery.json | /classes/P1000/equivalentLoads/LAT (BAe-146) | 16.9 | 16.9 | 16.8 | -0.09999999999999787 | -0.00591715976331 |
| research/analysis/delivery.json | /classes/P1000/ownUpwash/acceptedPlan/releasedT | 191.77499999999998 | 191.77499999999998 | 190.75400000000002 | -1.0209999999999582 | -0.00532394733412 |
| research/analysis/delivery.json | /classes/P1000/payloadT | 191.77499999999998 | 191.77499999999998 | 190.75400000000002 | -1.0209999999999582 | -0.00532394733412 |
| research/analysis/delivery.json | /classes/P1000/workedExamplePlan/releasedT | 191.77499999999998 | 191.77499999999998 | 190.75400000000002 | -1.0209999999999582 | -0.00532394733412 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/workedExample/releasedT | 191.77499999999998 | 191.77499999999998 | 190.75400000000002 | -1.0209999999999582 | -0.00532394733412 |
| research/analysis/delivery.json | /classes/P1000/ownUpwash/acceptedMeanWaterReleaseKgS | 1265.7149999999997 | 1265.7149999999997 | 1258.9764 | -6.738599999999678 | -0.00532394733412 |
| research/analysis/delivery.json | /classes/P1000/releaseRateM3s | 1.2657149999999997 | 1.2657149999999997 | 1.2589764 | -0.006738599999999595 | -0.00532394733412 |
| research/analysis/delivery.json | /classes/P1000/ownUpwash/acceptedPlan/tph | 451.52834591975494 | 451.52834591975494 | 449.2244232020365 | -2.3039227177184216 | -0.00510249852205 |
| research/analysis/delivery.json | /classes/P1000/workedExamplePlan/tph | 451.52834591975494 | 451.52834591975494 | 449.2244232020365 | -2.3039227177184216 | -0.00510249852205 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/workedExample/tph | 451.52834591975494 | 451.52834591975494 | 449.2244232020365 | -2.3039227177184216 | -0.00510249852205 |
| research/analysis/delivery.json | /classes/P1000/_lineKmAtCL4/20 m swath | 5.88 | 5.88 | 5.85 | -0.03000000000000025 | -0.00510204081633 |
| research/analysis/delivery.json | /classes/P1000/_lineKmAtCL4/30 m swath | 3.92 | 3.92 | 3.9 | -0.020000000000000018 | -0.00510204081633 |
| research/analysis/delivery.json | /classes/P1000/lineKmAtCL/CL2, 30 m swath | 7.84 | 7.84 | 7.8 | -0.040000000000000036 | -0.00510204081633 |
| research/analysis/delivery.json | /classes/P1000/lineKmAtCL/CL4, 30 m swath | 3.92 | 3.92 | 3.9 | -0.020000000000000018 | -0.00510204081633 |
| research/analysis/delivery.json | /classes/P1000/lineKmAtCL/CL8, 30 m swath | 1.96 | 1.96 | 1.95 | -0.010000000000000009 | -0.00510204081633 |
| research/analysis/water-availability.json | /classes/P1000/throughputTph/atWorkedExample15km | 451.5 | 451.5 | 449.2 | -2.3000000000000114 | -0.00509413067553 |
| research/analysis/water-availability.json | /geometry/P1000/drawTonnesPer12h | 5418 | 5418 | 5391 | -27 | -0.00498338870432 |
| research/analysis/delivery.json | /classes/P1000/equivalentLoads/SEAT | 63.3 | 63.3 | 63.0 | -0.29999999999999716 | -0.00473933649289 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/byFire/737/cycleMin | 15.114571537704549 | 15.114571537704549 | 15.181065982148993 | 0.06649444444444441 | 0.00439936019877 |
| research/analysis/delivery.json | /classes/P1000/_lineKmAtCL4/50 m swath | 2.35 | 2.35 | 2.34 | -0.010000000000000231 | -0.00425531914894 |
| research/analysis/water-availability.json | /classes/P10000/acceptedPlans/byFire/1384/releasedT | 2944.576 | 2944.576 | 2934.7250000000004 | -9.850999999999658 | -0.00334547316829 |
| research/analysis/water-availability.json | /classes/P10000/acceptedPlans/byFire/1384/tph | 7558.660602903904 | 7558.660602903904 | 7536.902712068217 | -21.75789083568725 | -0.00287853787579 |
| research/analysis/water-availability.json | /classes/P10000/acceptedPlans/byFire/1384/suppliedMWh | 197.78338818511432 | 197.78338818511432 | 197.32477363764795 | -0.4586145474663681 | -0.00231877182242 |
| research/analysis/delivery.json | /classes/P1000/ownUpwash/end of release/heldT | 501.1 | 501.1 | 500.0 | -1.1000000000000227 | -0.00219517062463 |
| research/analysis/delivery.json | /classes/P1000/ownUpwash/acceptedPlan/suppliedMWh | 24.472360372481326 | 24.472360372481326 | 24.419280065020427 | -0.05308030746089898 | -0.00216899010365 |
| research/analysis/delivery.json | /classes/P1000/workedExamplePlan/suppliedMWh | 24.472360372481326 | 24.472360372481326 | 24.419280065020427 | -0.05308030746089898 | -0.00216899010365 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/workedExample/suppliedMWh | 24.472360372481326 | 24.472360372481326 | 24.419280065020427 | -0.05308030746089898 | -0.00216899010365 |
| research/analysis/water-availability.json | /classes/P10000/acceptedPlans/byFire/1384/options/ballastT | 7055.424 | 7055.424 | 7065.275 | 9.850999999999658 | 0.00139623075807 |
| research/analysis/water-availability.json | /classes/P10000/acceptedPlans/byFire/1384/retainedT | 7055.424 | 7055.424 | 7065.275 | 9.850999999999658 | 0.00139623075807 |
| research/analysis/delivery.json | /classes/P1000/ownUpwash/acceptedPlan/options/ballastT | 808.225 | 808.225 | 809.246 | 1.0209999999999582 | 0.00126326208667 |
| research/analysis/delivery.json | /classes/P1000/ownUpwash/acceptedPlan/retainedT | 808.225 | 808.225 | 809.246 | 1.0209999999999582 | 0.00126326208667 |
| research/analysis/delivery.json | /classes/P1000/ownUpwash/end of release/waterAboardT | 808.225 | 808.225 | 809.246 | 1.0209999999999582 | 0.00126326208667 |
| research/analysis/delivery.json | /classes/P1000/workedExamplePlan/options/ballastT | 808.225 | 808.225 | 809.246 | 1.0209999999999582 | 0.00126326208667 |
| research/analysis/delivery.json | /classes/P1000/workedExamplePlan/retainedT | 808.225 | 808.225 | 809.246 | 1.0209999999999582 | 0.00126326208667 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/workedExample/options/ballastT | 808.225 | 808.225 | 809.246 | 1.0209999999999582 | 0.00126326208667 |
| research/analysis/water-availability.json | /classes/P1000/acceptedPlans/workedExample/retainedT | 808.225 | 808.225 | 809.246 | 1.0209999999999582 | 0.00126326208667 |
| research/analysis/vacuum-cell.json | /ship0/worldsFramePractice/s1050_sf12/ratioSL | 0.913 | 0.913 | 0.912 | -0.0010000000000000009 | -0.00109529025192 |
| research/analysis/delivery.json | /classes/P1000/ownUpwash/end of release/airMassFlowKgS | 175949 | 175949 | 175770 | -179 | -0.001017340252 |

### Text, flags, absent sides and fresh old zero

All special rows listed: 39; omitted: 0.

| Published/generated file | Text or flag | Added | Removed | Fresh old zero | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| research/analysis/descent.json | 0 | 0 | 0 | 3 | 3 |
| research/analysis/mass-budget.json | 27 | 0 | 0 | 0 | 27 |
| research/validation/report.json | 9 | 0 | 0 | 0 | 9 |
| Total | 36 | 0 | 0 | 3 | 39 |

Replace each all-digit path segment with {n}; groups of more than 10 leaves collapse. P10000 stays literal. Id tuples follow placeholder order; .. denotes an inclusive range. Identical id sets share one reference. Changes compare fresh old with Standard R; a shared change is printed only when every leaf agrees.

Collapsed groups: 0; represented leaves: 0; full special rows: 39.

| Published/generated file | Field | Published old | Fresh old | Standard R | Constant effect | Relative effect |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| research/analysis/descent.json | /classes/P100/profile/20/unheldT | 0 | 0 | -2.842170943040401e-14 | -2.842170943040401e-14 | undefined (fresh old zero) |
| research/analysis/descent.json | /favourableClasses/P100/profile/20/unheldT | 0 | 0 | -2.842170943040401e-14 | -2.842170943040401e-14 | undefined (fresh old zero) |
| research/analysis/descent.json | /favourableClasses/P100/profile/4/unheldT | 0 | 0 | 1.4210854715202004e-14 | 1.4210854715202004e-14 | undefined (fresh old zero) |
| research/analysis/mass-budget.json | /classes/P100/rightSized/credible/cellular/phi=0.74/0.750/why | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.708075 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P100/rightSized/credible/cellular/phi=0.85/0.750/why | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.813329 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P100/rightSized/credible/hullThatCloses/0.900/why | effective shell density 1.035000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.035000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.035000 kg/m3 (including sundries) >= air density 0.956858 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.750/why | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.708075 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.750/why | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.813329 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P100/rightSized/demonstrated/hullThatCloses/0.900/why | effective shell density 1.080000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.080000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.080000 kg/m3 (including sundries) >= air density 0.956858 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P100/rightSized/floor/cellular/phi=0.74/0.750/why | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.708075 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P100/rightSized/floor/cellular/phi=0.85/0.750/why | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.813329 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P100/rightSized/floor/hullThatCloses/0.900/why | effective shell density 0.990000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 0.990000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 0.990000 kg/m3 (including sundries) >= air density 0.956858 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P1000/rightSized/credible/cellular/phi=0.74/0.750/why | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.708075 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P1000/rightSized/credible/cellular/phi=0.85/0.750/why | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.813329 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P1000/rightSized/credible/hullThatCloses/0.900/why | effective shell density 1.035000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.035000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.035000 kg/m3 (including sundries) >= air density 0.956858 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.750/why | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.708075 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.750/why | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.813329 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P1000/rightSized/demonstrated/hullThatCloses/0.900/why | effective shell density 1.080000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.080000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.080000 kg/m3 (including sundries) >= air density 0.956858 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P1000/rightSized/floor/cellular/phi=0.74/0.750/why | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.708075 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P1000/rightSized/floor/cellular/phi=0.85/0.750/why | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.813329 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P1000/rightSized/floor/hullThatCloses/0.900/why | effective shell density 0.990000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 0.990000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 0.990000 kg/m3 (including sundries) >= air density 0.956858 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P10000/rightSized/credible/cellular/phi=0.74/0.750/why | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.708075 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P10000/rightSized/credible/cellular/phi=0.85/0.750/why | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.862500 kg/m3 (including sundries) >= air density 0.813329 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P10000/rightSized/credible/hullThatCloses/0.900/why | effective shell density 1.035000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.035000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.035000 kg/m3 (including sundries) >= air density 0.956858 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.750/why | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.708075 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.750/why | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.900000 kg/m3 (including sundries) >= air density 0.813329 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P10000/rightSized/demonstrated/hullThatCloses/0.900/why | effective shell density 1.080000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.080000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 1.080000 kg/m3 (including sundries) >= air density 0.956858 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P10000/rightSized/floor/cellular/phi=0.74/0.750/why | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.708076 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.708075 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P10000/rightSized/floor/cellular/phi=0.85/0.750/why | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.813330 kg/m3 | effective shell density 0.825000 kg/m3 (including sundries) >= air density 0.813329 kg/m3 | None | n/a |
| research/analysis/mass-budget.json | /classes/P10000/rightSized/floor/hullThatCloses/0.900/why | effective shell density 0.990000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 0.990000 kg/m3 (including sundries) >= air density 0.956859 kg/m3 | effective shell density 0.990000 kg/m3 (including sundries) >= air density 0.956858 kg/m3 | None | n/a |
| research/validation/report.json | /checks/0/implementation_comparison/0/agree_to_roundoff | False | False | True | 1 | n/a |
| research/validation/report.json | /checks/0/implementation_comparison/1/agree_to_roundoff | False | False | True | 1 | n/a |
| research/validation/report.json | /checks/0/implementation_comparison/2/agree_to_roundoff | False | False | True | 1 | n/a |
| research/validation/report.json | /checks/0/implementation_comparison/3/agree_to_roundoff | False | False | True | 1 | n/a |
| research/validation/report.json | /checks/0/implementation_comparison/4/agree_to_roundoff | False | False | True | 1 | n/a |
| research/validation/report.json | /checks/0/rows/14/verdict | MISS | MISS | agrees | None | n/a |
| research/validation/report.json | /checks/0/rows/17/verdict | MISS | MISS | agrees | None | n/a |
| research/validation/report.json | /checks/0/verdict | MISS | MISS | agrees | None | n/a |
| research/validation/report.json | /checks/1/limits/1 | At that state, matching the printed lift would require purity 0.990602538 at full normal volume with dry-air contamination; equivalently this is the full-purity fill fraction. This limit is reported, never passed back into the comparison. | At that state, matching the printed lift would require purity 0.990602538 at full normal volume with dry-air contamination; equivalently this is the full-purity fill fraction. This limit is reported, never passed back into the comparison. | At that state, matching the printed lift would require purity 0.990603547 at full normal volume with dry-air contamination; equivalently this is the full-purity fill fraction. This limit is reported, never passed back into the comparison. | None | n/a |

## Complete list

Every changed leaf is in [constant-study.json](constant-study.json), `changed_fields`:

```python
import json; print(json.dumps(json.load(open("research/validation/constant-study.json"))["changed_fields"], indent=2))
```
