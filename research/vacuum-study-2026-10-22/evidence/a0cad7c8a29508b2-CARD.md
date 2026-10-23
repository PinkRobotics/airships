# MAINLINE-053 — completed CHECK-048 fold

**Confirmed: the completed independent CHECK-048 reproduces the owner's tables once the previously unwritten convection and conductance terms are supplied.**

**The owner's boundary is not established as the physically best-supported one.**
CHECK-040's forced/conduction reading is also not established as the installed
boundary. The better-supported model form must address local mixed convection,
cell radiation and bonded-interface resistance. The available evidence does
not select the required coefficient set for this hull. All inherited properties
remain QUESTIONABLE; installed performance remains PROJECTION.

| Term | Owner reading | CHECK-040 reading | Physical judgment |
| --- | --- | --- | --- |
| External convection | Max of forced h and 1.32 max(abs(To−Ta),.05)^.25 | Forced h only | Buoyancy can matter, but neither this max rule nor its omission is qualified |
| Core transport | Solid-core conduction plus 4(.20)σ average(Ti)³ | Solid-core conduction alone | Gap radiation is a separate physical path from enclosure radiation; neither .20 nor its omission is measured here |
| Bond/contact resistance | Zero | Zero | Both lack the bonded-panel resistance needed to select installed conductance |
| Inner enclosure | Uniform .20 diffuse empty sphere | Same | The enclosure identity is valid under those assumptions; actual finish and obstruction remain open |
| Weather and optics | Fixed dry optical pair and prescribed sky/ground/wind | Same | Neither is a measured coupled weather/wetting mission |

Both forced branches extrapolate Whitaker's sphere range Re 3.5–76,000.
The hull uses Re 2.61–7.83 million, and treats an average coefficient as local
on a non-isothermal surface. This is a shared limitation, not evidence that
CHECK-040 supplies a uniquely correct replacement.
[Whitaker, Table 1 and Eq.33](https://www.researchgate.net/profile/Stephen-Whitaker-3/publication/229709417_Forced_convection_heat_transfer_correlations_for_flow_in_pipes_past_flat_plates_single_cylinders_single_spheres_and_for_flow_in_packed_beds_and_tube_bundles/links/59d73bda0f7e9b42a6b0694a/Forced-convection-heat-transfer-correlations-for-flow-in-pipes-past-flat-plates-single-cylinders-single-spheres-and-for-flow-in-packed-beds-and-tube-bundles.pdf).

Later isothermal-sphere experiments found a heat-transfer transition near
Re 290,000, within measurements up to 330,000. They support taking flow
regime seriously; they do not validate either inherited branch at the hull
Reynolds numbers. [Will et al., 2017](https://research.utwente.nl/files/20163165/experimental.pdf).
A large-sphere natural-convection study simulated diameters 1–40 m and
Ra approximately 4e8–2e14, finding substantial variation among correlations.
Its still-air averages do not validate a local max rule for the current
nonuniform, 2 m/s case.
[Rodríguez Maestre et al., 2021](https://www.sciencedirect.com/science/article/pii/S1290072921002258).

As an explicitly approximate regime diagnostic, take beta=1/(284.9 K),
nu=1.79e−5/1.1672683307461802 m²/s and standard gravity 9.80665 m/s².
[NIST conventional value](https://physics.nist.gov/cgi-bin/cuu/Value?gn%7Csearch_for=acceleration+of+gravity).
Then Re=vD/nu, Ra=g beta |ΔT| D³ Pr/nu² and
Ri=Gr/Re²=g beta |ΔT| D/v². Using the already solved multilayer
forced/conduction extrema gives:

| R m | Re | Extremal abs(ΔT) K | Ra | Ri |
| --- | --- | --- | --- | --- |
| 10 | 2.6084e+06 | 14.485623 | 1.2043e+13 | 2.493075 |
| 12 | 3.1301e+06 | 14.836086 | 2.1314e+13 | 3.064071 |
| 15 | 3.9126e+06 | 15.254827 | 4.2805e+13 | 3.938191 |
| 20 | 5.2168e+06 | 15.777866 | 1.0494e+14 | 5.430958 |
| 30 | 7.8253e+06 | 16.483515 | 3.7002e+14 | 8.510779 |

These Ri values make an assertion of negligible buoyancy unsupported.
They do not validate the owner's coefficient or combine opposed, cross and
aiding convection into one law. The surface is nonuniform, so the diagnostic
is not a new mixed-flow solution.

NASA's honeycomb analysis distinguishes solid conduction and cell radiation,
and states that adhesive-interface resistance must be considered for bonded
aluminum panels. This supports treating both transport and interface terms,
but supplies no measured parameter for the selected CR-III/AF163/Be assembly.
[NASA, section 3.1, pp.65–66](https://ntrs.nasa.gov/api/citations/19680009019/downloads/19680009019.pdf).
The gap and enclosure terms describe different paths. Accepting that
distinction does not establish the effective gap emissivity .20.

**The consequence remains the already computed four-way comparison.**
No new coefficient set is sufficiently supported to replace it, and no
payload improvement follows from merely declaring the owner numerically
reproduced. Below are the existing cure-inclusive, retained-floor/bake
multilayer endpoints at the 028b gamma/Q/film assumptions, 200°F cure and
30.341397319:1 scarf. Every mass debit is retained.

| R / weather | Owner filed kg | Forced/conduction kg | Mixed/conduction kg | Forced/gap kg | Mixed/gap kg |
| --- | --- | --- | --- | --- | --- |
| R10 / ISA | 118.694825 | 118.088578 | 118.594926 | 118.188125 | 118.692997 |
| R10 / optimistic | -29.257217 | -29.863021 | -29.358656 | -29.761952 | -29.259078 |
| R12 / ISA | 327.176036 | 325.606508 | 326.919327 | 325.868218 | 327.172431 |
| R12 / optimistic | 63.720186 | 62.148681 | 63.459553 | 62.414379 | 63.716507 |
| R15 / ISA | 813.155245 | 808.781562 | 812.392615 | 809.578126 | 813.147416 |
| R15 / optimistic | 298.508108 | 294.119183 | 297.733541 | 294.928213 | 298.499990 |

The forced/conduction alternative costs 0.605804–4.388925 kg in these six
cases. Across the complete previously filed matrix, thermal-boundary changes
cause no endpoint float-sign or minimum/tied optimism-set change. All four
selected-finish day/cycle screens pass. Frozen scarf checks newly cross one
in 288 comparisons and global checks in 85; resizing restores the stated
limits. Free-edge and cell-wall screens remain passing. These alternatives
are not certified physical bounds; installed hull SF remains unknown.
The original [full card](8b817facdc012a8d-CARD.md)
retains the R10–30 temperature family, both cure branches, all joining/drying
routes and complete witnesses.

**The completed check's qualifications and corrections are incorporated.**
Its thermal ledger contains 103,714 comparisons; 26 legacy
curvature entries are reconciled in its follow-on audit by distinguishing raw
day from mean-removed night projection. The cited 1,714,368 count is its
full account audit at 2e−8. This coverage precision does not change the
numerical closure. Our 36 equivalent completed-check/053 primary
accounts agree within 0.000061672 kg,
with matching least sets and usages.

CHECK-048's two lost-float cases and multilayer sorbent axis-count changes
come from **including cure compression**, not from choosing a different
thermal boundary. MAINLINE-053's zero-flip statement compares thermal choices
while holding that cure treatment fixed. Both findings stand.

The following source/status corrections apply to interpretation of the
inherited 048 material, without changing the selected multilayer inputs:

- SolarWhite has a manufacturer nominal mass of .285 kg/m² at 150 μm,
  with typical alpha .18 and hemispherical epsilon .89 on Al2024-T3.
  The previous missing-mass/ambiguous-label interpretation is superseded
  locally; installed Be performance is still unknown.
  [ENBIO sheet](https://enbio.eu/wp-content/uploads/2024/07/SolarWhite.pdf).
- NASA 2015 gives classical CCAg/ITO alpha .08 and **normal** epsilon .72
  on 3 mil Kapton. It does not support a hemispherical .09/.65 attribution.
  The classical assumed pair requires its patent citation and transfer
  caveat; the multilayer .09/.80 class is a different source.
  [NASA, slide19](https://ntrs.nasa.gov/api/citations/20150018109/downloads/20150018109.pdf).
- The twelve null sensitivity least fields have independently supplied
  floating witnesses. Their nulls cannot establish no-float conclusions;
  the witnesses do not repair failed finish screens or qualify wet/aged optics.
  The complete witnesses and corrected dispositions are pinned in this fold.

The completed checker resolves C01/C02/C03 arithmetic, C12 coverage and
C13 execution. Its ten open-evidence entries and two source/result corrections
are retained with dispositions. MAINLINE-053's nine physical NFI groups remain.
[PHYSICAL-EVIDENCE.json](dcfcb62b54de4a18-PHYSICAL-EVIDENCE.json),
[CORRECTIONS.json](4f7fa4633a4e3a4f-CORRECTIONS.json) and [NFI.json](8498ed7b74061012-NFI.json) record the basis.
No repeated optimizer or thermal solve was needed: the existing complete
four-boundary matrix already covers the requested readings. The short
dimensionless arithmetic and output comparisons ran on one process.
All previous filing bytes are verified unchanged. No successor is named.
