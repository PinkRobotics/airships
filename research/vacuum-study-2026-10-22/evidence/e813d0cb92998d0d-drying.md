# MAINLINE-059 drying of wet outdoor surfaces (sourcing; values as printed, quotes verified against extracted text)

Latent heat / energy
- Latent heat of vaporization at 20 C: about 2.45 MJ/kg (FAO-56 Ch.1; Ch.3 uses 2.45 for air about 20 C). 1 mm/day = 2.45 MJ m-2 day-1.
- Solar constant: about 0.082 MJ m-2 min-1 (FAO-56 Ch.3). Hourly Rs 2.450 MJ m-2 h-1 at 14-15 h, Senegal (FAO-56 Example 19).

Potential evaporation (FAO-56, Allen et al. 1998, fao.org/3/x0490e)
- Hourly grass ETo: 0.63 mm/h at 14-15 h (T 38 C, RH 52 %, u2 3.3 m/s, Rs 2.450 MJ m-2 h-1); 0.00 mm/h at 02-03 h (T 28 C, RH 90 %, 1.9 m/s). Calculated.
- Daily ETo, arid/semi-arid tropics: 6 - 8 mm/day at >30 C (4 - 6 at 20 C, 2 - 4 at ~10 C); humid tropics 3 - 5 at 20 C. "Not intended for direct application".

Measured drying on pavement (Deckert and Hauf 2003, SIRWEC, Bueckeburg airfield, concrete + tarmac, Mar-Jun 2003, WSW wind)
- Eddy-correlation evaporation, moist paved surface: 0.128 to 0.268 mm/h; dry surface 0.025 to 0.111 mm/h. QUESTIONABLE: source area includes grassland; T/RH/wind/sun per run not printed.
- Water-film sensor dried within five minutes in its final phase, much sooner than the pavement (no pavement drying time printed).
- Permeable concrete, Shenzhen (Zhang et al. 2019): post-rain evaporation boost fades to a lower level in eight hours; daytime rate follows solar radiation. Qualitative.

Dew / wetness after sunrise
- Shrub leaves, Changchun (Xu et al. 2022, Water 14:2428): dew gone about 4 h after sunrise; evaporation periods 282 +/- 21 (Syringa), 255, 242, 229 min; September dew evaporated 0.46-0.72 mm/d.
- Leaf sensor, Santa Maria, Brazil (Jorge et al. 2020): dry-off typically 7-10 AM; wetness duration 9.00-9.54 h warm seasons, 10.58-11.12 h cold.

Correlation
- Carrier/ASHRAE pool: m_evap [kg/s] = 4e-5 * A_pool * F_act * (p_w - p_a) with p in kPa (Smedegard, Stene, Georges, IBPSA 2025). Original tests forced convection only; applied down to 0 m/s; unoccupied factor 0.5; indoor pools, QUESTIONABLE for outdoor spheres.

Files: drying.json (17 rows, all quotes verified).

Gaps
- No measured kg/m2/h film drying on roofs or solar panels with stated sun, wind, T, RH.
- No solar-panel dew/rain drying times; no aircraft/vehicle surface data.
- No hours-after-rain drying time for dense asphalt/concrete.
- Class A pan mm/day and peak mm/h: only unverified snippets; no row.
- ASHRAE original velocity-term pool formula (0.089 + 0.0782 V), Shah correlations: no open text found.
- Lewis-relation mass-transfer correlations with coefficients: not verified; Haseba 1973 (wet leaf plates, h ~ U^0.5) not extracted.
- Ground-level clear-sky irradiance (about 1000 W/m2) and NASA solar constant: fetch gave no usable text.
