# CHECK-054 independent method

All results remain QUESTIONABLE or PROJECTION. The boundary of this check is the new 054 account: the fourteen filed 052 ground-service geometries, structural bills, free volumes and conditioned material inventories are inherited inputs. No frame optimization, nonlinear solve, installed-life qualification or new structural credit is claimed. No owner or predecessor executable was opened, hashed, imported or run.

The implementation is `check54.py`; `audit54.py` performs separate balance, decimal, table, export, precision and moisture audits. Only our scripts run. Scientific invocations use simjob with one core and 1 GiB; the execution records preserve admission and release. There is no work-time limit.

## Inputs and provenance

`INPUTS.json` records every frozen file's origin, digest and byte count. The canonical order and owner report, sixteen report artifacts, instruction files, selected owner-manifest data, upstream 052/046/034 data and primary-source documents are frozen. `OWNER-INPUT-PIN-CHECK.json` independently verifies 87 non-code entries in the owner's 88-entry input ledger. The remaining entry is `baseline052/model52.py`, which was deliberately not opened or hashed. Reading execution metadata containing executable filenames does not mean those executables were accessed.

The source audit distinguishes coupon measurements, upper reporting limits, missing properties and invented design allowances. Numerical density conversions are stated in the independent script; densities of unweighed coatings, hardware, and the working bed are projections. The 052 full bill is retained, including its separate 50 kg ground-vacuum allocation and 1% ISA-lift gas reserve.

## Water, dry gas and crossings

Area is \(4\pi R^2\). The unique seam length is \(1799.6766239090878(R/10)\) m, with 252 nodes and the fixed port leak. The declared mbar L/s leakage is converted at the reference 284.9 K: 1 mbar L/s = 0.1 Pa m³/s. Weather pressure determines water fraction and dry-species partial pressures. Normalized 034 dry fractions, molecular weights, oxygen permeability and relative species permeances yield total dry moles and mass.

For a coupon rate \(w\), 054 uses \(w\max[1,p_{w,\mathrm{ext}}/(\mathrm{RH}_{test}p_{sat}(T_{test}))]\). This is an unvalidated correction. The 052 baseline had no such correction; comparing it with the 054 both-weather result without accounting for that change would create a false mismatch.

Water rate is corrected WVTR × area / 1000 plus seam/node/port water. Release inventory is the 052 conditioned remainder plus 0.001 times any positive barrier mass increment. Its finite release is \(S(1-e^{-d})\). We solve humidity and hot total-pressure crossings by 100-step bracketed bisection. The schedule is 90% of the earlier crossing. Route selection uses the colder humidity target.

The modified Buck over-water saturation expression is
\(611.21\exp[(18.678-C/234.5)C/(257.14+C)]\) Pa.
The inherited main limit is 32.51651646315005 Pa. Independently inverting 052's cold crossing gives 21.87136725311824 Pa, consistent with 046's 268.6301428187726 K temperature. The owner 054 results use 21.87136709931465 Pa. The difference is 0.00000015380359 Pa. We preserve the upstream value in our primary results and list all 2,816 strict numerical differences. A diagnostic substitution of the declared 054 design limit resolves all of them; it is not used to generate the primary independent results. No displayed number, route or payload changes.

Coating-loss scenarios mix the intact barrier's humidity-corrected rate with the stated 40 g/m²/day bare-PET envelope. This does not describe a through-hole. Multilayer carrier sensitivities replace only the carrier gauge.

## Capture, transport, energy and mass

Let \(F=1-e^{-d}\), \(E=\dot Wd\), capacity \(c=0.06\), housing \(H=\max(1,0.25M)\), and fixed hardware 5 kg. The independent solution is piecewise:

\[
M_{\mathrm{low}}={1.1[E+SF+0.006F]\over c},\quad M_{\mathrm{low}}\le4;
\qquad
M_{\mathrm{high}}={1.1[E+SF+0.005F]\over c-0.000275F}.
\]

This solves \(cM=1.1[E+(S+0.001(H+5))F]\) directly from the stated sizing equation. Battery mass is power × 24 × days / 108 Wh/kg. Capture mass is dry beads + housing + 5 kg hardware + battery. Headspace capacity is not credited.

Initial dry fill, dry ingress, all external water and 1% bead initial moisture consume the existing gas reserve before an excess debit is added. Existing material release redistributes carried mass. Payload is 052 payload minus barrier increment, capture system and reserve excess.

Capture free volume reproduces with \(V_0-M/600-(H+5)/1000\). The hardware effective density of 1000 kg/m³ and inclusion of all 5 kg hardware were reconstructed from the non-code outputs; the source method does not fully document this convention. That documentation gap is an NFI. Wet-fibre free volume replaces old film solid volume with new film solid volume and recomputes initial dry fill.

The GSTA equation is transcribed from Lin et al., Eq. 1–2 and Table 2:
\[
q={0.21\over4}{\sum_{n=1}^4nK_n(p/100000)^n\over1+\sum_{n=1}^4K_n(p/100000)^n},
\quad \ln K_n=-H_n/(R_gT)+S_n/R_g.
\]

We use \(H=[-46600,-125000,-193600,-272200]\) J/mol and \(S=[-53.7,-221.1,-356.7,-567.5]\) J/mol/K. The separate 60-digit Decimal evaluation checks all fifteen published equilibrium points. The usable-capacity convention is \(0.8(q-0.01)\). It supplies a conditional screen, not actual batch kinetics.

Peak release rate adds the full one-day inventory derivative at time zero. Required effective water conductance is \((\dot W_{\mathrm{peak}}/M_w)R_g320/[24(p_{\mathrm{design}}-p_{\mathrm{bed,end}})]\) m³/h. Using peak source and final loading together is conservative within this lumped model. It is an effective species conductance, not a qualified fan flow or pump rating. Heat is water rate × 4.4 MJ/kg / 86400. Ideal radiation area is heat divided by \(0.8\sigma(333^4-321.940239586^4)\). It excludes real view factors, interfaces, added thermal hardware and electrical heat.

Ground regeneration energy is \([(M+H+5)1000(325)+W_{\mathrm{captured}}4.4\times10^6]/3.6\times10^6\) kWh, then doubled. Pumping, cooldown and cycling data remain absent.

## Fibre and supplemental moisture screens

The two-direction film equation is \(t=p\,r_c/(F_y\eta R_{ret}\phi_T-\sigma_T)\), using the inherited 052 curvature, \(\phi_T=0.964012200518\) and thermal stress 90.501688129 MPa. Area × thickness × density gives mass. The unchanged-gauge SF divides new allowable by old mechanical-plus-thermal stress. Resizing restores only SF=1 in that screen.

SK99 and DM20 minimum creep rates are \(7\times10^{-6}\) and \(1.3\times10^{-6}\) percent/s at 900 MPa and 30°C. Multiplication by mission seconds gives the stated linear screen. Those rates are not valid for the higher stresses in the strength-sized films, and are not a rupture-life model.

The card's 1% carried-film-water allowance is reproduced. A separate 3.5% Kevlar-49 moisture sensitivity uses the manufacturer's 24°C/55% RH equilibrium datum, the same finite-release proxy and the same retained-mass reserve. It does not assert 3.5% is the installed hull's equilibrium moisture or a universal worst case.

## Comparison rules

Primary machine comparisons use absolute tolerance \(10^{-8}\) plus relative tolerance \(10^{-9}\). Every failure is listed by table, row, field, owner value, independent value and delta. The explicitly isolated cold-input precision offset is reconciled separately.

CSV comparisons use absolute \(2\times10^{-7}\) plus relative \(2\times10^{-8}\), covering that diagnosed offset; this tolerance is never used to erase a payload error. All ten CSV exports and 378 complete bills are covered. Card table entries and principal prose figures are checked against half a unit in the last printed digit. The one remaining displayed discrepancy is the owner report's 47.35 kg foil payload; 47.34455788658644 rounds to 47.34 kg, as its card already states.

Exploratory files preserve one failed label lookup and the initial convention-alignment pass. Their failures are not attributed to the owner. The final numerical and presentation ledgers are separate from source and installed-service qualifications.
