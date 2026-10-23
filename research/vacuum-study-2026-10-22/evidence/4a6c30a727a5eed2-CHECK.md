# CHECK MAINLINE-060: the carbon-framed P3

- **Unit:** vacuum-mainline060-check-1020.
- **Order:** ord-admiral-rr2-check060-opus-6ea7-1020.
- **Card checked:** rpt-ref-93808d41af02a0580060, by owner ref-4189c1615990eb515921.
- **Checker:** ref-55cff924be25afe6f9dd (claude-opus-5-5, max).

All values are QUESTIONABLE or PROJECTION. I did not read or run the owner's code (carbon60/extra60/src60/card60.py, CARBON.json, EXTRA.json).

Everything was rebuilt in my own script from the pinned inputs:
- 051's ply constants, witnesses, GAPS and hail table;
- 052's bills;
- 054's cavity rows;
- the primary source PDFs, which I re-downloaded and read.

## Verdict

**The card's answer stands.** No carbon frame floats on sourced compression, and carbon is not a better lead than SiC.

**216 of the 237 numbers I checked reproduce.** The other 21 rows are:
- **19 mismatch rows of four kinds:**
  - the member load: 775 kN printed, where the axial force is 701 kN (1 row);
  - the M55J hail stress: 100 MPa printed, where 051's table gives 98.9 (1 row);
  - the Pf normalization, 0.5–0.8% on the unsafe side (1 row);
  - the CV 5.2% interpolation, about 1% on the safe side (16 rows).
- **One conservative modelling note:** m taken from CV.
- **One independent cross-check** that supports the hail margin.

I also raise two objections about how sources are read.

## The five items asked for

**1. The UHM pitch compression is confirmed in the primary documents.**
- **DIALEAD brochure:**
  - K13D2U 340 MPa / 560 GPa and K13C2U 380/560 (350 °F epoxy, Vf 60%).
  - K13C6U 340/550 (250 °F epoxy).
  - K63712 440/330 and K13916 360/430.
- **GRANOC sheet:** YS-80A/90A/95A 380/360/340 MPa (typical, not guaranteed).
- **Montagnier and Hochard:** K63712 at 374 MPa (CV 5.1%, n = 6) against Mitsubishi's 440 MPa, a gap of 15.0%.
- **NCAMP:** 0CLC (combined-loading compression) mean 189.2 ksi, CV 5.198%, modified CV 6.599, 18 specimens. This is an IM PAN fabric, as the card says.
- **CMH-17's floor:** "at least 6%".

**Objection: the 15% is not an independent shortfall.** The authors attribute it to the Celanese fixture. They write that "the failure stresses are underestimated in comparison with the manufacturer's experimental data" and that the Celanese test "leads to premature ruptures in high-modulus carbon fibers". Their pure-bending tests reached about 60% higher failure strain. The card sizes on the 340 MPa sheet value, so no number changes; only the wording should.

**2. First-ply failure at 0.19 GPa is confirmed.**
- **The 0° ply ratio:** my classical lamination theory, using 051's ply constants, gives 1.7875 for 50/20/20/10 and 1.3551 for 70/10/10/10. That matches 051 exactly.
- **The derived values:**
  - laminate mean 0.1902 GPa;
  - Weibull scale 0.200 GPa at m 10 and 0.195 GPa at m 20;
  - 11.4× below 2.16 GPa;
  - mean SF 0.274 at the stiffness wall;
  - a 3.68 GPa ply needed (using 051's 2.161413).
- **Transverse modulus:** the DIALEAD sheet gives 5.0 GPa, where 051 assumes 8 GPa. Using it moves the first-ply value by only 0.15%.

**3. The whole-bill rows are confirmed** at all five radii, within 1 kg.
- **The headline row:** M55J 50/20/20/10 is −469.9 kg at R10 and −4,624 kg at R30.
- **Other line-by-line rows:** K13D2U 50/20/20/10 is +618.6 kg at its stiffness wall and −8,922.8 kg at mean strength. M55J 70/10/10/10 at Pf 1e-3 is −2,043.6 kg.
- **Weather and axis variants:** optimistic weather gives −2,175 kg. Baseline axes, which is 052's mask 1, give −2,405 kg. The combined case gives +258 kg.
- **Margins:** the float limits (1.0074 to 1.0788) and the tube multipliers (1.1197, 1.1368, 0.8595) agree.
- **Cavity:** 054's increments match, including the R20/R30 extrapolation.

**4. The Pf 1e-3 sizing is confirmed at CV 6%, with three method notes.**
- **The CV 6% walls reproduce:** ×6.69, ×4.26, ×1.54, ×1.76, ×1.32, and the size-scaled walls up to ×11.90. So do the Pf values at the witnesses (1, 0.995, 0.216, 2.94e-9).
- **Normalization (fix C060-02).** 051's k(m) is normalized to the fresh-FE peak, which is 0.5–0.8% above the comparison peak the card multiplies it by.
  - **Walls:** used consistently, the walls rise by 0.5–0.8%. M55J 70/10/10/10 goes from ×1.316 to ×1.326.
  - **Pf at the stiffness wall:** 0.247 instead of 0.216.
  - **Payload:** −2,092 kg instead of −2,044 at R10, and −48,427 kg instead of −47,116 at R30.
- **CV 5.2% interpolation (note C060-03).** Every CV 5.2% value is 0.9–1.3% above mine. I interpolate k(23.1) as ln S linear in m between 051's m 20 and 30, which bounds k from above.
  - **Walls:** K13D2U 50/20/20/10 is ×6.15 against the card's ×6.21.
  - **Required UD strength:** 1.78 against 1.80 GPa at R10. So the card errs conservative.
- **m from CV (note C060-04).** m = 1.2/CV understates the exact Weibull m: 20.0 against 20.68 at CV 6%, and 23.1 against 23.96 at 5.2%. Exact m would lower the walls by about 2%, so this is also conservative.

**5. The hail energy is confirmed.**
- **The design strike:** 50.8 mm ice at 32.0 m/s carries 28.47–32.33 J (810–920 kg/m³, Matejak).
- **Kim et al., Table 8:** 254–263 J at 1.59 mm; my own fit through the three thicknesses gives 38.9 + 134.2 J/mm. That is 233.5 J at 1.45 mm, 7.2–7.4 times the strike.
- **An independent cross-check:** Pernas-Sánchez's own scaling, KEc = 85×10⁶ × A_f × t, gives 250 J at 1.45 mm.
- **Strike stresses:** 159 MPa reproduces.

**Mismatch C060-05:** for M55J 50/20/20/10, 051's table gives 98.9 MPa where the card prints 100 MPa. The 5.6× exceedance holds.

## Other findings

**Mismatch C060-01: the member load.** The card says each tube carries up to 775 kN (174 klb), 1.43 times NG-2's 121.7 klb collapse load.
- **Where 775 kN comes from:** peak combined stress × area (0.6951 GPa × 1.1145×10⁻³ m²).
- **The actual axial force:** 051's FE maximum is 701.4 kN (157.7 klb), which is 1.30 times NG-2.
- **The conclusion still holds:** the load is above every sourced strut test.

**Objection C060-07: the joint fitting share.** The card uses Messinger's 44K strut, whose fittings are 16.9% of the strut, or 0.203× the tube.
- **The nearer strut:** his 110K strut, closer to these members' 158 klb, has 27.8% (0.385× the tube).
- **The effect:** with that share the strength-ignored light frame never floats: −730 kg at R10 and −11,661 kg at R30. The card's 44K share gives −76 and +6,005 kg.

**Strut sources:** the Messinger weights (13.31 + 1.20 + 1.50 = 16.01 lb) and NG-2's −121.7 klb are confirmed.

**Not re-opened (C060-08):** T800S, the Toray Europe sheets, the hard-impact and compression-after-impact rows, Jegley and Wu's 70% of DUL, and the CORDIS 70% share. None of them decides the answer.

**Tube data (C060-09):** a search found no tube compression data for M55J, K13C2U or XN-80, consistent with the card's gap row.

## Files

- **RESULTS.json:** 237 rows of card value against my value, with verdicts, plus the objections.
- **RESULTS-CHECK.json:** the full computation.
- **NFI.json:** C060-01 to C060-09.
- **INPUTS.json:** pins for the inputs, the source PDFs and my scripts.

The scripts are in .ship/work/scripts/check060/.
