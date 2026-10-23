# CHECK050 source audit

The source inputs are QUESTIONABLE; the hull, profile, transfer and operating calculations are PROJECTION. A numerical reproduction does not qualify an installed hull. No MAINLINE050 executable source was read, copied, imported or executed.

The independently downloaded handbook and Dong paper exactly match the owner's byte counts and SHA-256 hashes. Download receipts are in `sources/FETCH-PINS.json`. The official catalogue was checked through the browser; its separate raw HTTP response was only 244 bytes and is not treated as a retrieved catalogue document.

| Source | Independently checked values and interpretation | Disposition |
|---|---|---|
| [MIL-HDBK-310](https://chet-aero.com/wp-content/uploads/2016/11/mil-hdbk-310.pdf), pp 7, 9, 10, 44, 72, 95; [DLA catalogue](https://quicksearch.dla.mil/qsDocDetails.aspx?ident_number=202658) | Hot 1/5/10%: 49/46/45°C. Table I peak RH: 3%. Joint 43.3°C dewpoints: 27.8/24.4/20°C. Absolute-humidity dewpoints: 31/30/29°C. Low pressures at 1 km: 847/856/861 hPa. | MATCH. The 5/10% hot cycles are discussed as temperature adjustments to Table I. These are handbook design markers, not local annual operating probabilities. Surface-to-altitude profiles, pressure coincidences and saturation brackets remain explicit assumptions. |
| [NCAR EOL saturation formulations](https://www.eol.ucar.edu/data-software/conventions-and-standards/water-vapor-pressure-formulations) | Buck 1996 water coefficients 611.21 Pa, 18.678, 234.5, 257.14; ice coefficients 611.15 Pa, 23.036, 333.7, 279.82. | MATCH. The owner's recorded correction from a 1981 annotation to the 1996 coefficients is supported. Enhancement corrections are omitted by the model. |
| [Dong et al.](https://arxiv.org/pdf/1909.05757), equations 1–6 and Table 2 | Coupled energy/mass balance, Le=.87 and external forced-convection exponent −2/3. Table 2 separately gives −3/4 for natural plate convection. | MATCH to the stated adopted analogy. Extending one exponent, a large-sphere convection law and a grey sky to this hull is a PROJECTION, not an experimentally validated deposition rate. |
| [NIST-JANAF Be](https://janaf.nist.gov/tables/Be-002.html) | Molar heat capacity 16.380 J/(mol K) at 298.15 K and 16.472 at 300 K. | Supports the scale of the rounded 1825 J/(kg K) planning value. It does not support constant capacity at every night temperature. |
| [NIST aluminum](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7429905&Mask=42) | Solid Shomate coefficients A=28.08920, B=−5.414849, C=8.560423, D=3.427370, E=−.277375, with T/1000 and molar units. | Supports the scale of 900 J/(kg K) near room temperature. The model uses a constant value and omits polymer storage. |

The five local handbook page images were visually inspected. The 1% pressure value was also checked in section 5.3.1.13.2, printed p44. The source gives geometric altitude; the calculation's geopotential-altitude convention is retained as a declared approximation.

Inherited material provenance is retained in the pinned 040/048/034 data and the owner's source/NFI registers. Be, honeycomb, scarf, interface strength, conditioning, coating optics, leakage and permeability remain transferred or assumed properties. This check does not convert those proxies into measured installed-system allowables.

`clarifications/CONVENTIONS.md` is the owner's pinned equation-only clarification. Its local copies and original report are hashed in `clarifications/PINS.json`. It supplies no executable code. The independently reconstructed transient matched the principal deposits before clarification; correcting its forced-convection density to the documented humid-night value resolves the small remaining differences.
