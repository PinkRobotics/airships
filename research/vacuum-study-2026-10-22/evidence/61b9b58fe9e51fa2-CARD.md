# MAINLINE-027 — size as a lever

ESTIMATE. **QUESTIONABLE inputs; PROJECTION fabrication, joints and named mechanical optimisms. No certification.** Unit `vacuum-mainline027-size-as-lever-1020`; order `ord-admiral-rr2-mainline027-dispatch-1019`. Radii are 10, 15, 20, 30, 50 m, at the inherited 500 m atmosphere. Times are measurements, not limits.

**Size alone does not make either P2 design pass.** With the corrected seam masses and the inherited design properties, optimistic least SF at R = 50 is 0.58971 aramid /0.50005 aluminium. Under MAINLINE-021's full named mechanical optimisms, aluminium first passes at the sampled **R = 20 m: SF 1.00749, payload 209.84 kg**; R = 30 and 50 carry 3,543.71 and 26,391.28 kg at SF 1. Aramid remains below 1. These payloads include the stated weather/gas/surface budget and joint screen, not a complete vehicle.

**Neither family's optimistic reserve drops below 5% at any radius.** Temperature/pressure, humidity and internal air alone charge **5.7396167%** of reference lift. All other reserve rows are nonnegative. This is an algebraic limit, not an extrapolated fitted crossing. The conservative floor is 13.1183154%. Fixed-area masses help, but full-gauge splice doublers do not remain fixed kg/m² as the faces thicken.

Size and safety-factor curves [source link unavailable in this public projection]

## Basis and interpretation

Aluminium is 021 revision 1's **Hexcel CR-III 5056 3/8-1.0**,16.01846 kg/m³, Ec 103.421 MPa, W shear 46.884 MPa, crush 241.317 kPa, cell 9.525 mm. Aramid is **HRH-10-4.8-32**,32 kg/m³, Ec 76 MPa, W shear 14 MPa, crush 1 MPa, cell 4.8 mm. The old 019 aluminium core was 1/4-1.6; it is deliberately replaced here by the ordered 021 core. Typical core data remain QUESTIONABLE. [Hexcel primary sheet, pp.2,5](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf)

**Design** means E = 290 GPa, compression 283 MPa, wrinkle coefficient 0.33 and the inherited gamma 0.2 below Vc 2 /1 above it. **021 full** means the historical SR-200 lot at E = 293.6 GPa /379.2 MPa, wrinkle coefficient 0.82, and gamma=0.2+0.4min(Vc,2). The second set is a separate structural optimism, not another weather forecast. Both use inherited ν = 0.33. The historical strength is not a current sheet guarantee. [021 revision 1](74176cf445147edf-CARD.md)

Every point is re-optimised on **its own** mass line for global buckling, face compression, core crush, crimp, wrinkling, equibiaxial dimpling and joint net-section compression. Joint efficiencies 0.9/0.6 come from 020's optimistic/conservative screen; they affect only the joint compression mode. Factors use the high-pressure end (+1%/+2%) with no internal-pressure structural relief. Float mass uses the hot, low-pressure, humid end. These are envelope checks, not simultaneous weather states. Reserve excludes payload and retains the original 100 kg systems /5%-of-structure joint allowances as floors.

## Each budget row's law

| Row | Held / scaled quantity | Mass law before allowance credit | Tag |
|---|---|---|---|
| Passive vacuum/power/controls |15+10+5 kg,24 h sealed-service assumption |R⁰;100 kg baseline system floor retained |PROJECTION |
| Active vacuum package, literal fixed-system screen |223 kg pump,20 kg controls,1223.333 kg battery |R⁰; only excess over 100 kg charged |QUESTIONABLE; capacity fails above R = 10 under inherited gas load |
| Active capacity-corrected variant |240 m³/h modules at 320 K gas,24 h at 5500 W each +5 W monitoring |ceil(196.03558(R/10)³/240) modules; power/battery follow count;20 kg controls fixed |PROJECTION |
| Retained water |0.1/1 mm whole-area equivalent,1000 kg/m³ |R² |QUESTIONABLE |
| Contamination |5/25 kg at R = 10 spread over area |R² |QUESTIONABLE |
| Extra coatings |zero independently added in baseline;0.1 kg/m² sensitivity |R² for fixed coating thickness |QUESTIONABLE scope choice |
| Two face/core bond films |020:0.146473/0.292946 kg/m² per interface |R² |QUESTIONABLE material; PROJECTION installed bond |
| Seam length at 020 panel size |a×b=0.6096×1.8288 /0.3048×0.6096 m; length=A(1/a+1/b) |R² |PROJECTION |
| Frozen 020 seams, requested screen |0.477521/2.375979 kg per hull m² at 009c5 gauges |R², only while seam cross-section stays fixed |PROJECTION |
| Resized 020 Be doubler/core gap |two full-gauge straps,60/120 mm wide;1/2 mm paste gap through actual core |A·tf and A·tc, approaching R³ under structural similarity |PROJECTION |
| Seam adhesive/sealant |020 film, width and bead area fixed |R² |PROJECTION |
| Temperature/pressure loss |same T and fractional p envelope |R³ |QUESTIONABLE |
| Humidity loss |same vapour partial pressure |R³ |QUESTIONABLE |
| Internal air |1% of reference lift |R³ |QUESTIONABLE |
| Payload |searched independently until every modelled SF≥1 |solution, not a prescribed% |PROJECTION |

Joining is charged as `max(0, actual joining −0.05×structural mass)` in reserve. It is not added again on top of the entire existing allowance. See [METHOD.md](d483d0e885adb191-METHOD.md) for exact closure and formulas, and [SCALE-ROWS.csv](88df46445810633e-SCALE-ROWS.csv) for every row at every radius. No phantom negative reserve credit is taken when an allowance exceeds actual mass.

## P2 with resized 020 seams

Both material settings are separately re-optimised. Reserve shares therefore differ slightly between them. `none` means even the zero-payload point fails SF 1; it does not assert a zero-payload qualified vehicle.

### Optimistic budget; fixed system package

| R (m) | Family | Design reserve (%) | Design least SF |021-full reserve (%) |021-full least SF | Payload at SF 1,021-full kg |
|---:|---|---:|---:|---:|---:|---:|
|10|aluminium|23.5607|0.416016|23.5061|0.899527|none|
|10|aramid|22.6144|0.516063|22.2417|0.764596|none|
|15|aluminium|20.0194|0.455119|19.9505|0.975090|none|
|15|aramid|19.0172|0.550561|18.6196|0.815709|none|
|20|aluminium|18.2216|0.472131|18.1469|1.007487|209.84|
|20|aramid|17.1954|0.565440|16.7869|0.837753|none|
|30|aluminium|16.4113|0.487964|16.3312|1.037410|3,543.71|
|30|aramid|15.3628|0.579226|14.9444|0.858177|none|
|50|aluminium|14.9568|0.500050|14.8728|1.060113|26,391.28|
|50|aramid|13.8913|0.589711|13.4654|0.873713|none|

### Conservative budget; fixed system package

| R (m) | Family | Design reserve (%) | Design least SF |021-full reserve (%) |021-full least SF | Payload at SF 1,021-full kg |
|---:|---|---:|---:|---:|---:|---:|
|10|aluminium|96.2712|0.000063|96.2711|0.000064|none|
|10|aramid|96.2093|0.000152|96.2139|0.000162|none|
|15|aluminium|72.2871|0.089012|72.4026|0.140968|none|
|15|aramid|69.3407|0.056059|69.6408|0.130797|none|
|20|aluminium|63.3369|0.142976|63.3425|0.246001|none|
|20|aramid|59.8155|0.090442|60.6921|0.241159|none|
|30|aluminium|55.8479|0.192046|55.7515|0.327645|none|
|30|aramid|51.8598|0.120006|53.3009|0.320812|none|
|50|aluminium|50.5830|0.228045|50.4256|0.382888|none|
|50|aramid|46.2653|0.140495|48.0369|0.372663|none|

The optimistic aluminium 021-full points balance global buckling and joint compression. Aramid balances global/crimp and joint compression; its design-property points instead balance crimp and wrinkling. The conservative R = 10 mathematical solutions have extremely thin faces and very low dimpling/global factors; they are not manufacturable configurations established by this study.

**The fixed conservative systems table is a scaling diagnostic, not a qualified operating package above R = 10.** At the inherited one-percent-volume/day gas load, one pump's 240 m³/h catalog speed fails already at R = 15. Keeping its mass fixed would require gas-load limits to tighten with radius. The corrected variant budgets whole parallel modules and batteries:

| R (m) | Modules | Design reserve (%) Al / Ar | Design least SF Al / Ar |021-full least SF Al / Ar |
|---:|---:|---:|---:|---:|
|10|1|96.271 /96.209|0.000063 /0.000152|0.000064 /0.000162|
|15|3|83.691 /81.812|0.032666 /0.020533|0.040154 /0.036274|
|20|7|77.858 /75.254|0.062140 /0.038421|0.088447 /0.079162|
|30|23|71.636 /68.615|0.095465 /0.060255|0.155254 /0.144579|
|50|103|66.401 /63.052|0.125869 /0.079732|0.215068 /0.209492|

All capacity-corrected conservative points fail SF 1 and have no nonnegative payload at SF 1. Modules are only a transparent bound on hardware/power: pressure-dependent installed speed, manifold losses, cooling and the leak law remain open. A sealed-service hull can instead retain the fixed 30 kg optimistic package **only conditional on** the stated leak and thermal acceptance test. The allowed normalized total gas load grows 40.7195→5089.9363 Pa·m³/s from R = 10→50 for a 10 Pa start,320 K gas limit and 0.01p₀ ceiling; this is an acceptance condition, not a prediction of leakage.

### What the literal fixed areal 020 screen would say

This holds 020's seam cross-sections at the old 009c5 gauges even when the new faces become much thicker. It is supplied because the brief asks for the area scaling; the resized-seam tables above are the load-transfer comparison to use.

| R (m) | Optimistic reserve (%) |021-full SF Al / Ar | Conservative reserve (%) |021-full SF Al / Ar |
|---:|---:|---:|---:|---:|
|10|24.7267|0.880958 /0.739500|no mass line|infeasible|
|15|16.7888|1.022608 /0.834197|89.1332|0.014393 /0.010965|
|20|12.8383|1.086906 /0.877629|66.1809|0.215394 /0.175434|
|30|8.8963|1.148198 /0.919254|45.6822|0.430293 /0.394241|
|50|6.2741|1.187919 /0.946335|30.5002|0.581669 /0.514766|

### Aluminium family check

A separate 1110-search sweep checks 37 inherited aluminium rows, of which 25 have same-sheet modulus data. The remaining Plascore rows transfer Hexcel modulus and use bare compression as the crush proxy; they remain QUESTIONABLE sensitivities. The full 021 optimistic winner and its payload stay **5056 3/8-1.0 at every radius**. With design properties, the best core switches back to **5056 1/4-1.6**:

| R (m) | Family-best design least SF, optimistic budget | Selected 021-core least SF | Family-best reserve (%) |
|---:|---:|---:|---:|
|10|0.425315|0.416016|22.4847|
|15|0.471745|0.455119|18.9070|
|20|0.492130|0.472131|17.0937|
|30|0.511201|0.487964|15.2691|
|50|0.525820|0.500050|13.8039|

No design-property aluminium row reaches SF 1 in either budget; no conservative row reaches it even with full 021. [CATALOGUE.json](d68dfa16808feb56-CATALOGUE.json) carries all candidates, scores, best geometries and independently reoptimised payload maxima.

## Optional P3: SiC arc frame

The 011b equilateral continuum is re-optimised, with arc bays 0.4–3 m, outer tube radius≤min(0.25 m, s/3), fixed 80 µm film, film allowable 1.5 GPa, SiC E = 410 GPa /compression 3900 MPa, global k 0.2, Perry imperfection a₀=s/1000,20 g/node, and joints 5% of tube mass. Each new sphere recounts `N=8πR²/(√3s²)+2` nodes and `3N−6` members. Tube area comes from the remaining mass after film, nodes, joints,50 kg baseline systems and the same 019 weather/water/contamination/gas budget. P3 does not receive Be face/core bond films: its frame/film attachment masses are unresolved inside the inherited joint assumption.

| R (m) | Optimistic reserve (%) | Optimistic least SF | Payload at SF 1 kg | Bay (m) | Outer radius (mm) | Conservative SF fixed /scaled pumps |
|---:|---:|---:|---:|---:|---:|---:|
|10|8.4120|1.109903|429.33|2.2427|123.868|0.269047 /0.269047|
|15|7.5212|1.029373|428.08|2.4182|167.847|0.618687 /0.387406|
|20|7.0758|0.968291|none|2.5707|208.231|0.690295 /0.411772|
|30|6.6304|0.782755|none|1.9612|250.000|0.638822 /0.416458|
|50|6.2741|0.472790|none|1.0731|250.000|0.406419 /0.285501|

These P3 passes are **PROJECTION**. The 380 MPa flexural-strength sensitivity gives least SF 0.23692→0.25174 over R = 10→50. It is a separate strength screen, not a replacement compression allowable.20 g/node, the ceramic joints, thin curved tubes and membrane assumptions have not been grounded. The supplier's standard seal-tube example is typically 12 in long and distinguishes 3900 MPa compression from 380 MPa four-point flexure. Its current modulus is 430 GPa; this continuation retains 011b's 410 GPa for comparison. [Saint-Gobain seal tubes](https://www.ceramicsrefractories.saint-gobain.com/products/shapes/tubes/hexoloy-seal-tubes), [SiC primary technical sheet](https://www.saint-gobain.co.jp/jp/documents/zhipintetashito/hexoloy-sa-sic-en-1013-tds-215398.pdf)

For a **separate similarity check**, all 011b member lengths, radii and walls scale with R; member count stays fixed, tubes/joint fraction scale R³, but film thickness stays 80 µm and film mass scales R². Structural factors stay constant while film SF falls as 1/R: nominal least SF at R = 10,15,20,30,50 becomes 1.22553,0.82161,0.61621,0.41080,0.24648. Film reaches SF 1 atR≈12.324 m before weather. Those are shape-scaling diagnostics, not mass-closed payload points. A genuinely similar film would need thickness∝R, losing its area-mass advantage. Similar solid nodes would also need mass per node∝R³; the simple diagnostic holds the inherited 20 g count and identifies that limit.

## Limits on going bigger

- **QUESTIONABLE/PROJECTION: sheet and panel production.** 020's large stock dimensions become less speculative at gauges≥1.4986 mm, but material grade, compound forming, gauge and installed tolerances remain unverified. Both enhanced P2 families are below this threshold at R = 20 and above it at R = 30. Panel count still grows with area: the optimistic lower bound rises 1128→28180 pieces per skin, and coincident seam length 2.749→68.714km. R = 50 aluminium carries about 435.16 tonnes of Be faces, before splice straps. [SR-200 supplier sheet, p.3](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6)
- **PROJECTION: assembly and ground handling.** Diameter 20→100 m requires matching clearance, supports and handling loads. Projected area πR² grows 314.16→7853.98 m². At the same wind speed and drag coefficient, force grows 25-fold and a moment with lever arm R grows 125-fold. This follows dimensional mechanics; no drag coefficient or mooring design is supplied. Local attachment, landing and asymmetric-pressure modes are unscored.
- **QUESTIONABLE: P2 modes.** For tf, tc∝R at fixed material and cell size, global/face/crimp/wrinkle/crush factors are size-invariant; fixed-cell dimpling improves as R². In particular crimp pressure∝h²/(Rtc) is constant, not intrinsically improved or worsened by R. If face/core gauges are held instead, global falls as R⁻² and face/crimp/wrinkle/dimpling as R⁻¹. Any core-depth or gauge cap can therefore reverse the apparent size benefit.
- **PROJECTION: P3 modes and components.** With fixed bay and capped tube radius, global lattice capacity eventually falls roughly as 1/R. The 0.25 m radius cap is active at R = 30 and 50. With similar growing bays and fixed film, film failure worsens as 1/R. The 20 g node law cannot establish load capacity as node/member forces increase.
- **QUESTIONABLE: operational and material limits.** Coatings, hardpoints, thermal gradients, internal heating, icing, leak/outgas and dimensional defects have no radius-independent guarantee. An extra 0.1 kg/m² consumes 125.66→3141.59 kg across this radius range. The R = 20 aluminium 209.84 kg payload is only 41.75 g/m² of extra areal mass; this narrow pass is especially fragile. Full 021 with gamma held at 0.2 fails SF 1 at every sampled radius for both cores.

## Verification and filing

53 input pins verified. Both 020 join totals reproduce 968.197361 and 3721.996275 kg; three revised 021 geometries reproduce all six modes; the 011b SiC point reproduces to 3e-14 absolute SF. 116 main P2 optima plus 30 catalogue winners were compared with 100001 fractions; 15 P3 optima with 801×1001 grids. Independent 45-digit scalar checks cover 159 P2 and 17 P3 geometries including payload points. Maximum pressure-factor discrepancy is below 1e-12 and mass discrepancy below 3e-10 kg. These check arithmetic, not the physical assumptions.

[RESULTS.json](2786b4340427a9c7-RESULTS.json), [FRAME.json](48c07950145981f5-FRAME.json), [INPUTS.json](4a8053170f59db42-INPUTS.json), [NFI.json](fecbe3eb74d15e6e-NFI.json), [VALIDATION.json](98538a93f39aa5f8-VALIDATION.json), [METHOD.md](d483d0e885adb191-METHOD.md) and [row export](88df46445810633e-SCALE-ROWS.csv) provide the trace. Seventeen evidence needs remain open. The brief says **stop and file; robotics sends the next job**. No executable successor is named.
