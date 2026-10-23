# MAINLINE-050 — the weather in which each size floats

**None of R=10, 12, 15, 20 or 30 m floats on the declared MIL 10% hot profile, even with all four optimistic endpoints.** Bigger sizes improve ordinary-weather margin, but the answer depends strongly on whether the hull is designed for one day or built to withstand the entire pressure range. These are QUESTIONABLE/PROJECTION budget and stress screens; installed-hull capability remains unqualified.

The requested four-dimensional map is complete: 2,027,245 weather points across five radii, plus continuous interpolated zero-payload surfaces and all sixteen optimism-subset boundaries. It retains the 048 multilayer CCAg/ITO finish, bake70, joining floor and 037b fix. The frozen-048 comparison and the extension with weather-dependent skin temperatures are both supplied.

The following upper offsets include **any RH from 0 to 100% and any sea-pressure anomaly from −30 to +30 hPa**. Each column has a different physical meaning. The design family can change thickness for its selected design day. The fixed hull is one build sized for the full pressure range, with its extra mass retained in every weather state.

| Radius m | Design-family upper offset at 100 m, K | Design-family upper offset at 500 m, K | Fixed full-range hull upper offset at 100 m, K | Original ISA payload, kg |
|---:|---:|---:|---:|---:|
| 10 | +5.8 | -2.7 | -6.5 | 124.3 |
| 12 | +9.5 | +1.5 | -3.0 | 337.0 |
| 15 | +12.2 | +4.5 | -0.3 | 832.3 |
| 20 | +14.3 | +6.9 | +1.8 | 2290.0 |
| 30 | +15.8 | +8.6 | +3.3 | 8525.5 |

The cold interface screen supplies the other end of the window: approximately **ISA −10.5 K at 100 m, −7.9 K at 500 m**, corresponding to about 277 K air under the declared clear-sky model. Colder air adds buoyancy but fails that screen. Thus, for example, the R10 full-range hull has a projected common 100 m band of roughly −10.5 to −6.5 K; R30 has −10.5 to +3.3 K. At 500 m only R30 retains a common fixed-hull band across the entire pressure/RH rectangle, approximately −7.9 to −6.8 K. Favorable pressure and humidity permit wider bands; the complete surfaces give them.

The fixed builds use 103.953 kPa design load and masses 5024, 8568, 16560, 38937 and 130621 kg. Original ISA geometries are separately checked and cannot inherit that pressure capacity. The family upper offsets at 100 m change by only about 0.1–0.3 K when the dry thermal field follows ambient; the major new effect is the cold exclusion.

Weather envelopes [source link unavailable in this public projection]

At the original dry ISA reference, the least sets are gamma/Q/film for R10 (common log usage .8331), and gamma/Q for R12/15/20/30 (usage .8847/.7208/.5984/.5666). The higher-radius film floor already dominates much of the bill. All minimum-cardinality ties are retained in the maps. For a concrete transition, R10 at 500 m, standard sea pressure and RH100 uses gamma/Q up to about −4.87 K; gamma/Q/film then carries it to +5.71 K, with a gamma/Q/E tie over the initial part of that interval; all four endpoints extend the boundary to +6.19 K. `LEAST-SET-TRANSITIONS.json` and the sixteen surfaces show the other sizes and ties without assigning a false unique winner.

The sourced design cases are markers, not annual flight probabilities. [MIL-HDBK-310](https://chet-aero.com/wp-content/uploads/2016/11/mil-hdbk-310.pdf) supplies surface hot values 49/46/45°C, the joint 43.3°C hot-humid dewpoints 27.8/24.4/20°C, absolute-humidity dewpoints 31/30/29°C, and 1-km low pressures 847/856/861 hPa for 1/5/10%. Assumed coincident quantities and altitude mappings are explicit in `DESIGN-DAYS.json`.

| Design-marker interpretation | Smallest sampled radius, 1% / 5% / 10% |
|---|---|
| Hot profile: standard sea pressure, peak RH3%, projected lapse | none / none / none |
| Joint hot-humid profile: 1000 hPa sea pressure, projected lapse | none / none / none |
| Low pressure at 1 km, ISA temperature, RH0–100 bracket | none / none / none |
| Absolute humidity at 100 m, assumed saturated Ta=Td | 30 m on gamma/Q/E / 30 m on gamma/Q / 20 m on gamma/Q |
| Same absolute-humidity marginals, assumed Ta=41°C | none / none / none |

The absolute-humidity comparison demonstrates why a dewpoint percentile alone cannot select a unique hull. On the 10% hot case at 100 m, the primary-endpoint deficits are about 295/397/602/1114/2993 kg. Even R30 with all four endpoints is short by 2771 kg. No sampled size closes; this is not an unbounded-radius impossibility proof.

The 12-hour night estimates below retain all deposited water. Clear reference air is 284.9 K with a 280 K dewpoint, 260 K effective sky and 0.2 m/s wind. The overcast case uses RH95%, sky only 2 K colder than air and 0.5 m/s wind. Saturated clear air is a separate sensitivity. The cold case has 268.15 K air and a sky 24.9 K colder; its cold mechanical screen fails.

| Radius m | Clear reference dew kg/m² | Overcast dew kg/m² | Saturated-clear dew kg/m² | Cold frost kg/m² | Total original ISA water allowance kg/m² |
|---:|---:|---:|---:|---:|---:|
| 10 | 0.090 | 0.004 | 0.243 | 0.084 | 0.199 |
| 12 | 0.090 | 0.004 | 0.242 | 0.084 | 0.286 |
| 15 | 0.089 | 0.004 | 0.241 | 0.083 | 0.394 |
| 20 | 0.088 | 0.004 | 0.239 | 0.082 | 0.556 |
| 30 | 0.085 | 0.003 | 0.236 | 0.081 | 0.854 |

Condensation heat matters. The reference clear-night R10 minimum rises from the dry-model 271.54 K to about 273.66 K; that case deposits liquid, not frost. These are whole-sphere averages, not the upward-facing peak. A fresh dry hull uses the reserved 0.1 kg/m² film allowance; a physically preexisting film consumes additional capacity.

Actual humid-night density further lowers the allowance. R10 has about 0.184 kg/m² available in the reference night and 0.178 in saturated air. It retains about 117 kg payload after the dry-start reference night, but loses about 82 kg on the saturated-clear night. R12 retains only about 33 kg in the saturated-clear case. Adding a preexisting 0.1 kg/m² film to those dry-start deposition estimates is an explicitly conservative arithmetic comparison, not a wet-start transient. `DEW-ACCOUNT.csv` gives each size.

Water account [source link unavailable in this public projection]

Drainage can remove liquid if wetting and droplet pinning permit; no shedding fraction or hardware mass is credited. Frost requires melting, sublimation or removal. Night heating of the R10 reference clear case costs about 21.1 W/m², 26.6 kW total and 319 kWh over 12 hours: roughly 2952 kg of battery at the inherited 108 usable Wh/kg, before heaters/cables. The chosen overcast case needs about 1.16 W/m² and 162 kg of battery. Ground power while moored changes the flying-mass account but leaves installation and support costs open.

A projected low-emittance night state (epsilon .05) suppresses the reference and overcast cases in this model, but still collects about .027 kg/m² under saturated clear air. A switching mechanism and wet optical properties are unqualified. A ground-supported cover can block sky cooling; a carried 10–50 g/m² cover alone would weigh 12.6–62.8 kg at R10 or 113–565 kg at R30, before supports and retained water. A morning wait has no assumed hardware mass but costs availability. At the low solar absorptance, the reference deposit needs about 2.8 hours of ideal solar-only evaporation energy; saturated-clear water needs about 7.6 hours. Those are energy-equivalent times, not dry-out forecasts, and warmer air simultaneously reduces lift.

Fifteen numerical checks pass: inherited regression, independent grid refinement, direct decision-case solves, interpolation, fixed-build stress and pressure checks, night energy closure, time/zone convergence and the conditional gas reserve. Interpolation checks on the reported cases are within 0.05 kg; the dew refinement changes mean deposition by less than 0.0001 kg/m². Numerical convergence does not close the physical NFIs.

One simjob admission refusal was preserved; queue authority explicitly permitted unchanged retries, and the retry and all subsequent jobs completed under simjob. Times were measured, not task caps. No other seat was contacted out of band. The brief names no successor: file this card and stop.
