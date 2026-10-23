# MAINLINE-007 core density with thickness — ESTIMATE

Unit vacuum-mainline007-core-trade-1019. Status ESTIMATE. Tag QUESTIONABLE. Certification none. Started 2026-10-19T22:45:53-07:00. Ended 2026-10-19T22:52:16.272157-07:00. Those times are measurements.

Case: evacuated sphere, external radius 10 m, 500 m ISA air. Pressure 95460.8379139 Pa. Air density 1.16726833075 kg/m3. Lift mass 4889.44215019 kg. Internal pressure 0. Aluminum 6061-T6 uses E 68.9 GPa, nu 0.33, density 2700 kg/m3, and 276 MPa as a QUESTIONABLE typical tensile yield transferred to compression. Modeled strength safety factors are QUESTIONABLE.

P2 is held on the float-mass ceiling with margin 0. Joints are 5 percent of the sandwich. Systems are 100 kg. Structural mass is (lift - 100) / 1.05. Both faces and the core use the external area 4*pi*R^2. Face separation is core thickness plus face thickness, the definition that reproduces the sealed baseline. The inner mould line is ignored.

Knockdown kd stays 0.2. Buckling pressure and the buckling safety factor scale in direct proportion to kd. The required-modulus factor scales as 1/kd, so a larger knockdown lowers the required modulus. Yield, membrane stress, the crimp modulus, the wrinkling product, and the crush target do not depend on kd. MAINLINE-004's curve is one multiplication of the buckling numbers here.

The stated safety factor is the lesser of knocked-down buckling and QUESTIONABLE yield. Core shear, face wrinkling, and core crush stay beside the row. The buckling split maximises tf times separation on the mass line: tf = M_struct / (2*area*(2*2700 - rho_core)). The two factors are equal at separation 0.189070201186 m, independent of density and of face thickness. When the buckling-peak separation is below that line, both rules pick the buckling peak. When it is above, the least-factor split sits on the equal line and yield would govern the thinner-face peak.

Checks against the sealed cards, recomputed here: baseline buckling pressure 11701.5583953 Pa, PASS against 11701.5583953 Pa. P2-A buckling safety factor 0.23078902511, PASS. P2-E buckling safety factor 0.233885578993, PASS. A uniform face-thickness sample cannot land on the equal-factor crossing. The closed form is the reported row. It dominates that sample, and the safety-factor gap stays under 1e-4.

## Where buckling safety factor reaches 1

On the buckling-optimal split, buckling safety factor reaches 1 at core density 3.73369568197 kg/m3. Face 0.00033632751569 m, core 0.485753861595 m, separation 0.486090189111 m. Buckling safety factor 1. QUESTIONABLE yield safety factor 0.38896115458. Governing aluminum yield. Least stated safety factor 0.38896115458. Membrane stress 709582426.806 Pa. Modulus factor 1. Strength factor 2.57095082176.

## Where the least stated safety factor peaks

On the named densities the maximised lesser safety factor is highest at 1 kg/m3, value 0.737028554512. A geometric sample from 0.25 to 64 kg/m3, ratio 1.05, 114 points, has no point where the next density is higher. There is no interior peak. The sample high end is the low-density end, 0.25 kg/m3, least factor 0.767296865535, still below 1.

## The 6061 gap

Yield cannot reach safety factor 1 on this ceiling. Spending the whole ceiling on faces, thickness 0.000672189940789 m, gives membrane stress 355036694.695 Pa and QUESTIONABLE yield safety factor 0.777384434128. The 276 MPa transfer must close by a factor 1.28636483585 even with no core. Every split that still carries a core needs a larger factor. At the named least-factor peak the two factors are equal at 0.737028554512, so both the knockdown model and the transfer must close by 1.35679953494. Where buckling safety factor first reaches 1, the strength factor is 2.57095082176.

## Density 32 kg/m3

The split that maximises buckling safety factor and the split that maximises the lesser of buckling and yield are the same point. Buckling governs, because the separation is below the equal-factor line.

Face 0.000338098517163 m, core 0.0563779277369 m, separation 0.0567160262541 m.

Masses in kilograms: faces 2294.28248625, core 2267.09099012, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.117292381934. QUESTIONABLE yield safety factor 0.391009309267. Governing knocked-down buckling. Least stated safety factor 0.117292381934.

Membrane stress 705865547.082 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 8.52570289312. Strength factor 2.55748386624.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 8415684.61498 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 4.08353910899e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

## Density 16 kg/m3

The split that maximises buckling safety factor and the split that maximises the lesser of buckling and yield are the same point. Buckling governs, because the separation is below the equal-factor line.

Face 0.00033709376674 m, core 0.113094958741 m, separation 0.113432052508 m.

Masses in kilograms: faces 2287.46441051, core 2273.90906586, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.233887632327. QUESTIONABLE yield safety factor 0.389847320235. Governing knocked-down buckling. Least stated safety factor 0.233887632327.

Membrane stress 707969468.235 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 4.27555741212. Strength factor 2.56510676897.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 4207842.30749 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 4.12016256089e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

## Density 8 kg/m3

The two splits diverge. The buckling peak is past the equal-factor line, so yield is the lesser factor there. The least-factor split moves onto the equal-factor line.

### Split that maximises buckling safety factor

Face 0.000336593627621 m, core 0.226527511389 m, separation 0.226864105016 m.

Masses in kilograms: faces 2284.0705464, core 2277.30292997, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.467081236071. QUESTIONABLE yield safety factor 0.389268911748. Governing QUESTIONABLE aluminum yield. Least stated safety factor 0.389268911748.

Membrane stress 709021428.812 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 2.14095519745. Strength factor 2.56891822033.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 2103921.15375 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 4.13855611666e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

### Split that maximises the lesser safety factor

Face 0.000392667668911 m, core 0.188677533518 m, separation 0.189070201186 m.

Masses in kilograms: faces 2664.58002614, core 1896.79345023, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.454118270855. QUESTIONABLE yield safety factor 0.454118270855. The two factors are equal, so both govern. Least stated safety factor 0.454118270855.

Membrane stress 607771185.864 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 2.202069514. Strength factor 2.202069514.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 2524481.3121 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 2.60670019668e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

## Density 6 kg/m3

The two splits diverge. The buckling peak is past the equal-factor line, so yield is the lesser factor there. The least-factor split moves onto the equal-factor line.

### Split that maximises buckling safety factor

Face 0.000336468824644 m, core 0.30214900453 m, separation 0.302485473355 m.

Masses in kilograms: faces 2283.22365335, core 2278.14982301, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.622544067457. QUESTIONABLE yield safety factor 0.389124577706. Governing QUESTIONABLE aluminum yield. Least stated safety factor 0.389124577706.

Membrane stress 709284418.957 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 1.60631199023. Strength factor 2.56987108318.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 1577940.86531 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 4.14316304327e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

### Split that maximises the lesser safety factor

Face 0.000462625968325 m, core 0.188607575218 m, separation 0.189070201186 m.

Masses in kilograms: faces 3139.30586185, core 1422.06761452, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.535024707714. QUESTIONABLE yield safety factor 0.535024707714. The two factors are equal, so both govern. Least stated safety factor 0.535024707714.

Membrane stress 515864026.503 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 1.86907255979. Strength factor 1.86907255979.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 2524481.3121 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 1.59395661353e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

## Density 4 kg/m3

The two splits diverge. The buckling peak is past the equal-factor line, so yield is the lesser factor there. The least-factor split moves onto the equal-factor line.

### Split that maximises buckling safety factor

Face 0.000336344114183 m, core 0.453391865919 m, separation 0.453728210033 m.

Masses in kilograms: faces 2282.3773881, core 2278.99608827, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.933469986989. QUESTIONABLE yield safety factor 0.388980350657. Governing QUESTIONABLE aluminum yield. Least stated safety factor 0.388980350657.

Membrane stress 709547409.101 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 1.07127172157. Strength factor 2.57082394602.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 1051960.57687 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 4.14777338748e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

### Split that maximises the lesser safety factor

Face 0.000532532408361 m, core 0.188537668778 m, separation 0.189070201186 m.

Masses in kilograms: faces 3613.67978812, core 947.693688253, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.615871169453. QUESTIONABLE yield safety factor 0.615871169453. The two factors are equal, so both govern. Least stated safety factor 0.615871169453.

Membrane stress 448145673.461 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 1.62371620819. Strength factor 1.62371620819.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 2524481.3121 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 1.0450291119e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

## Density 3 kg/m3

The two splits diverge. The buckling peak is past the equal-factor line, so yield is the lesser factor there. The least-factor split moves onto the equal-factor line.

### Split that maximises buckling safety factor

Face 0.000336281793613 m, core 0.604634664917 m, separation 0.60497094671 m.

Masses in kilograms: faces 2281.95449068, core 2279.41898569, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 1.24439603478. QUESTIONABLE yield safety factor 0.388908277218. Governing QUESTIONABLE aluminum yield. Least stated safety factor 0.388908277218.

Membrane stress 709678904.173 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 0.803602689215. Strength factor 2.57130037744.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 788970.432655 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 4.15007984158e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

### Split that maximises the lesser safety factor

Face 0.00056746619913 m, core 0.188502734987 m, separation 0.189070201186 m.

Masses in kilograms: faces 3850.73490747, core 710.638568901, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.656271930489. QUESTIONABLE yield safety factor 0.656271930489. The two factors are equal, so both govern. Least stated safety factor 0.656271930489.

Membrane stress 420557374.432 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 1.52375860301. Strength factor 1.52375860301.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 2524481.3121 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 8.63667392302e+15 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

## Density 2 kg/m3

The two splits diverge. The buckling peak is past the equal-factor line, so yield is the lesser factor there. The least-factor split moves onto the equal-factor line.

### Split that maximises buckling safety factor

Face 0.000336219496134 m, core 0.907120200569 m, separation 0.907456420065 m.

Masses in kilograms: faces 2281.53174994, core 2279.84172643, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 1.86624825854. QUESTIONABLE yield safety factor 0.388836230483. Governing QUESTIONABLE aluminum yield. Least stated safety factor 0.388836230483.

Membrane stress 709810399.245 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 0.535834391499. Strength factor 2.57177680886.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 525980.288436 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 4.15238715056e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

### Split that maximises the lesser safety factor

Face 0.000602387046663 m, core 0.18846781414 m, separation 0.189070201186 m.

Masses in kilograms: faces 4087.7021961, core 473.671280272, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.696657722737. QUESTIONABLE yield safety factor 0.696657722737. The two factors are equal, so both govern. Least stated safety factor 0.696657722737.

Membrane stress 396177334.999 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 1.43542512681. Strength factor 1.43542512681.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 2524481.3121 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 7.2200406689e+15 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

## Density 1 kg/m3

The two splits diverge. The buckling peak is past the equal-factor line, so yield is the lesser factor there. The least-factor split moves onto the equal-factor line.

### Split that maximises buckling safety factor

Face 0.000336157221732 m, core 1.81457668291 m, separation 1.81491284013 m.

Masses in kilograms: faces 2281.10916581, core 2280.26431056, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 3.73180518599. QUESTIONABLE yield safety factor 0.388764210437. Governing QUESTIONABLE aluminum yield. Least stated safety factor 0.388764210437.

Membrane stress 709941894.317 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 0.267966828428. Strength factor 2.57225324028.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 262990.144218 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 4.15469531457e+16 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

### Split that maximises the lesser safety factor

Face 0.000637294958154 m, core 0.188432906228 m, separation 0.189070201186 m.

Masses in kilograms: faces 4324.58170281, core 236.791773561, joints 228.068673818, systems 100, residual gas 0. Total 4889.44215019. Float margin 0.

Buckling safety factor 0.737028554512. QUESTIONABLE yield safety factor 0.737028554512. The two factors are equal, so both govern. Least stated safety factor 0.737028554512.

Membrane stress 374476671.643 Pa. That is the required compressive strength. It does not depend on the 276 MPa transfer. Modulus factor 1.35679953494. Strength factor 1.35679953494.

QUESTIONABLE targets beside the row, outside the stated factor: crimp shear modulus 2524481.3121 Pa from p = 2*Gc*d/R; wrinkling product Ec times Gc 6.0974053774e+15 Pa^2 from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to the membrane stress; crush 47730.418957 Pa, about p/2.

## Real cores beside the rows

Each sourced value is QUESTIONABLE. A missing modulus was left empty. No value below is a PROJECTION of a core that can carry this shell. Honeycomb shear is orthotropic plate shear. The smaller W modulus is the one compared with the crimp target. A stabilised honeycomb compressive modulus is not the continuum Ec of the wrinkling formula. Comparisons use the buckling-optimal row at the nearest named density. Hexcel HRH-10 at 24 kg/m3 is equally far from 16 and from 32. The script attaches it to 32 because 32 is first. Its crimp margin against the 16 kg/m3 row would be about twice the margin printed below, because that row's separation is about twice as large. The wrinkling product barely moves across the buckling peaks, so the wrinkling miss does not.

ROHACELL 31 IG-F, 32 kg/m3, offset 0 kg/m3 from the named 32 kg/m3 buckling row. QUESTIONABLE compressive strength 400000 Pa, crush margin 8.38039993658 against p/2. QUESTIONABLE shear modulus used 13000000 Pa, crimp margin 1.54473469418. QUESTIONABLE Ec times Gc 2.21e+14 Pa^2, wrinkling margin 0.00541197216683. Evonik ROHACELL IG-F product information, April 2022, https://cdn.sanity.io/files/dorbplvp/production/ed045b3e26f3de6b4faf1533d03ca5c1b66f8ae0.pdf.

Divinycell H35, 38 kg/m3, offset 6 kg/m3 from the named 32 kg/m3 buckling row. QUESTIONABLE compressive strength 500000 Pa, crush margin 10.4754999207 against p/2. QUESTIONABLE shear modulus used 12000000 Pa, crimp margin 1.42590894847. QUESTIONABLE Ec times Gc 4.8e+14 Pa^2, wrinkling margin 0.0117545096836. DIAB Divinycell H, H Oct 2012 rev9 SI, nominal column, via https://www.castrocompositesshop.com/en/index.php?controller=attachment&id_attachment=1020.

Plascore PAMG-XR1 5052 3/16-2.0, 32 kg/m3, offset 0 kg/m3 from the named 32 kg/m3 buckling row. QUESTIONABLE compressive strength 1289319.61382 Pa, crush margin 27.0125350248 against p/2. QUESTIONABLE shear modulus used 137895145.863 Pa, crimp margin 16.3854935364. No Ec times Gc product, so no wrinkling margin. Plascore PAMG-XR1 5052 datasheet rev 4.6.2021, http://plascore.com/wp-content/uploads/dlm_uploads/2025/08/PLA_PAMG-XR1-5052_2023-06-02.pdf.

Hexcel HRH-10-4.8-32, 32 kg/m3, offset 0 kg/m3 from the named 32 kg/m3 buckling row. QUESTIONABLE compressive strength 1000000 Pa, crush margin 20.9509998415 against p/2. QUESTIONABLE shear modulus used 14000000 Pa, crimp margin 1.66356043988. QUESTIONABLE Ec times Gc 1.064e+15 Pa^2, wrinkling margin 0.0260558297987. Hexcel HexWeb HRH-10 datasheet, https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_HRH10_DataSheet_eu1.pdf.

Plascore PAMG-XR1 5052 3/8-1.0, 16 kg/m3, offset 0 kg/m3 from the named 16 kg/m3 buckling row. QUESTIONABLE compressive strength 358527.379245 Pa, crush margin 7.51150706572 against p/2. QUESTIONABLE shear modulus used 48263301.0522 Pa, crimp margin 11.4698454755. No Ec times Gc product, so no wrinkling margin. Plascore PAMG-XR1 5052 datasheet rev 4.6.2021, http://plascore.com/wp-content/uploads/dlm_uploads/2025/08/PLA_PAMG-XR1-5052_2023-06-02.pdf.

Hexcel HRH-10-6.4-24, 24 kg/m3, offset -8 kg/m3 from the named 32 kg/m3 buckling row. QUESTIONABLE compressive strength 550000 Pa, crush margin 11.5230499128 against p/2. QUESTIONABLE shear modulus used 9000000 Pa, crimp margin 1.06943171135. QUESTIONABLE Ec times Gc 3.69e+14 Pa^2, wrinkling margin 0.00903627931927. Hexcel HexWeb HRH-10 datasheet, https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_HRH10_DataSheet_eu1.pdf.

Schaedler nickel microlattice, 0.9 kg/m3, offset -0.1 kg/m3 from the named 1 kg/m3 buckling row. No compressive strength was retrieved, so no crush margin. No shear modulus was retrieved, so no crimp margin. No Ec times Gc product, so no wrinkling margin. T. A. Schaedler et al., Science 334, 962-965 (2011), doi:10.1126/science.1211649.

At 8, 6, 4, 3, 2, and 1 kg/m3 no catalog structural core with a sourced shear modulus, compressive modulus, and compressive strength was retrieved. The Plascore 5052 sheet's lightest listed row is 16 kg/m3. The Rohacell IG-F sheet used here starts at 31 kg/m3. The lightest HexWeb HRH-10 row retrieved is 24 kg/m3. Schaedler et al., Science 334, 962-965 (2011), doi:10.1126/science.1211649, report a nickel microlattice at or above 0.9 kg/m3. The open abstract gives no modulus coefficient and no strength. Those numbers are not invented. A usable core at that density is not claimed.

On the advisory targets, the catalog cores at 16 to 38 kg/m3 clear crush and crimp. Their wrinkling products fall short by about 40 to 180 times, and the aluminium honeycomb sheets have no Ec, so that product stays open. The faces still set the stated safety factor. MAINLINE-007b can change that reading once shear and wrinkling use a sourced sandwich-shell formula. Needs-further-investigation rows are in NFI.json. Nothing here is a certification.
