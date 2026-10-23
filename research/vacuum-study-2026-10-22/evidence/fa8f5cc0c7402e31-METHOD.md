# REVIEW-A2 method

This is one independent review of MAINLINE058 and MAINLINE061 under
`ord-admiral-rr2-review-a2-dispatch-1020`. `LOAD-BEARING.json` listed the 17
claims before the independent calculations. MAINLINE056 and MAINLINE062
are outside this review. No predecessor implementation was read, imported
or executed, and no new finite-element solution was run.

The review uses pinned numerical inputs, source documents and a small
selection of consequential rows. A reproduction is agreement within the
stated mathematical account, not qualification of a complete hull.
Everything retains QUESTIONABLE / PROJECTION status. There is no known
qualified installed-hull safety factor.

## Pressure, thermal boundaries and weather counts

The atmosphere calculation independently solves the implicit 050
constant-vapour-fraction column using Rd=287.053 J/(kg K), g=9.80665 m/s²,
a 0.0065 K/m lapse and the Buck saturation-pressure expression. Pressure
load is `max(1.01*p500ISA,p_local)+q70`, with the original reference-density
wind allowance. The rectangular-grid maximum occurs at 100 m, ISA+20 K,
100% RH and the named sea-pressure anomaly. Temperature edges are scalar
roots of displaced air mass minus the saved hull mass. P3 uses the saved
sag volume as a separate displacement loss.

The thermal calculation was written from the balance equations. It solves
the two skins with outer sky/ground radiation and internal cavity
radiation, using 128 Gauss-Legendre zones. Through-core conductance is
`130*(16.018463373960138/2700)/tc`; inner emissivity is 0.2.
The outer coefficient is the greater of the Whitaker forced coefficient
and `1.32*max(abs(To-Ta),0.05)^0.25`, following the inherited equation-only
CONVECTION.md. The fixed reference density is 1.1672683307461802 kg/m³.
Four independently converged clear-night roots agree with the saved
boundaries within 0.00345 K, sufficient for the displayed 0.1 K claims.
The initial forced-convection-only diagnostic is retained but is
superseded by `058-THERMAL-MIXED-CONVECTION.json`.

For weather counts, Heathrow station elevation is 25.29 m and the
thermometer is 2 m above that surface. Thus sea-level temperature is
`Tobs + 0.0065*27.29`, and floor temperature is sea-level temperature minus
0.65 K. Station pressure is solved hydrostatically and the vapour fraction
is `es(Tdew)/p_station`. This uses the documented site elevation, 2 m
observation height and 050 column convention; the selected saved counts
then reproduce exactly, in both hours and days.

For each hour the independent calculation evaluates the floor, air
admission and climb branches. Admitted air caps the net lift; climbing
also changes temperature. P2's best branch is the union of climb and trim,
subject to the supplied day/no-sun and clear-night thermal boundaries.
P3 has no cold rejection in the inherited account. Every one of the 24
UTC hours must pass, and days with an incomplete T/Tdew/SLP hour are
excluded. There are 87,354 complete hours and 3,559 complete days.
Twenty-four raw NOAA FM-12 observations, covering 2014-01-01, match the
processed arrays exactly. This is a raw-data spot check, not a complete
independent audit of the ten-year record-selection/QC converter.

Eight selected weather configurations were checked, not all endpoint
tables or all optimism subsets. The authoritative count file is
`checks/058-COVERAGE-height27.29-humidityTrue.json`. Other height/humidity
files retain diagnostic interpretations and are not the final convention.

To expose the hardware accounting difference, the P2 recount adds the
exact valve/bladder masses already declared for the matching R10, R12 and
R20 whole-band configurations: `5 + .02*ballast_capacity`.
For P3's standard-pressure configuration, only the common 5 kg valve is
added. That is an optimistic upper bound on coverage, not a complete
replacement bill; a matched standard-pressure bladder capacity is missing.
All these recounts keep the original thermal roots and operation model
fixed so the effect being tested is the mass omission.

## 061 mass closures and limits

The density factor is independently derived at each supplied witness
geometry, using face volume `2*4*pi*R²*tf` and nominal face density
1850 kg/m³:

`factor = 1.15*nominal_face_mass / (lift - other_mass_with_growth)`.

Other component growth is recomputed from the named bill, not read from
the owner's growth total. Concept rates are 15% for faces/core/pad,
30% for actual joining/primer and 20% for absorbed water. Coating already
contains 10%, so only the increment to 20% is added on its unburdened
mass. Primary joining is actual joining; the retained-floor sensitivity
is a different account. All six favorable factors and both R30 handbook
factors agree within 2.72e-8.

The supplied density witness is independently mass-closing. This does
not independently repeat the constrained multistart search over all eight
factors and two thicknesses. Its claim to be the best feasible product
found is therefore left as an unresolved ranking, not promoted to a
global optimum.

P3's bound deletes every reducible film, joint, node and cavity item, and
retains the fixed-family SiC tube lower bound, systems, service, gas,
water, contamination, pad, sag and weather debit. Adding 15% only to the
retained tube/pad components reproduces all six negative upper bounds.
Even granting the entire 058 tube-relief fraction free leaves all six
negative. This argument is restricted to the inherited constant-g/R
family and named levers; the tube law and load envelope remain inputs.

NASA Table VI-1 was visually inspected: TRL7 hardware is 5%, while the
adjacent battery column is 6%. The R12 ISA P2 mass is independently
re-summed with those rates. No additional project/system-level growth
allowance is silently added or removed. The mixed concept rates are the
declared scenario, not a claim that all components have one maturity.

For R30 beryllium, face volume times 1850 kg/m³ is divided by 430,000 kg,
the USGS estimated 2025 world mine output expressed as Be content. This
does not estimate available finished sheet or fabrication yield.

The frozen CHECK057 account and the new 061 account are re-summed
separately. The latter's cure-compression global demand and resized
geometry are an explicitly different scenario. Their numerical
comparison is not an independent validation of residual-stress
superposition in a buckling analysis.

## Authority and execution

061's original dispatched PROCESS-v2 bytes were independently hash-checked
at SHA256 `be858ac11e1e4adc8e164157752df002a8edce54b62f077eb6b95f89d3e7c11a`.
The later in-place v2.1 update is not treated as an owner fault.
This review follows its own current pinned brief.

Substantive calculations ran through simjob at 1 CPU / 1 GiB; each
reservation exited successfully and was released. No other seat was
contacted, restored or woken. Proposed fixes remain unreviewed in this
register. This unit performs no owner fix and no second review round.
