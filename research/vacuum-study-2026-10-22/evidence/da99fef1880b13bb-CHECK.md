# Independent CHECK MAINLINE-021b

The headline conditional result reproduces. This check uses its own equations and search; it never executes or imports the owner's calculation. The filed CARD, results, inputs and program bytes match their pins. Copies are fixed in snapshots/.

## Mass and mechanical equations

Let S be faces plus core, f its core fraction, A=4πR², w the square-equivalent panel width and F the fixed reserve. Seam length is 2A/w. Two face strips, two local adhesive layers and one through-core splice give J=cS+d+films. The direct solution is S=min[(L−100−F)/1.05, (L−100−F−d−films)/(1+c)]. Reserve is F+max(0,J−.05S). This avoids iterating an already geometry-dependent reserve.

The seven fixed reserve lines independently sum to 411.298944071647 kg. Water is 1000A×.0001; climate is L[1−.99T0/(T0+10)]; humidity is L×.378×1000/p0×T0/(T0+10); internal gas is .01L. Contamination adds 5 kg. Systems excess and payload are zero. The retained 100 kg systems allowance is not spent twice.

CR-1457 mechanics use h=tf+tc, applied stress pR/(4tf), σ0=Eh/[R√(1−ν²)], σcrimp=Gch²/(2tftc), Vc=σ0/σcrimp and Kc=1−Vc/4 below Vc=2, otherwise 1/Vc. Global SF=γKcσ0/applied. Honeycomb wrinkling uses βC√(EEctf/tc), with β³+β=1. Equibiaxial dimpling is E(tf/cell)²/(1−ν²). Core crush uses twice core strength divided by p. No extra knockdown is applied to gamma.

## Filed floating point

| Quantity | Independent value |
|---|---:|
| faces (kg) | 3216.321838286494 |
| core (kg) | 606.261758440977 |
| joint_allowance_0_05S (kg) | 191.129179836374 |
| joint_seams (kg) | 187.433238328369 |
| joint_bond_films (kg) | 368.126371059474 |
| joint_excess_in_reserve (kg) | 364.430429551470 |
| reserve_fixed_items (kg) | 411.298944071647 |
| reserve_total (kg) | 775.729373623117 |
| systems_allowance (kg) | 100.000000000000 |
| total (kg) | 4889.442150186961 |

| Mode | Today at frozen geometry | Needed values | Full grade/coefficients | Full set, gamma .20 |
|---|---:|---:|---:|---:|
| global_buckling | 0.427141815416 | 1.000000000000 | 1.204138097758 | 0.430916473498 |
| face_compression | 1.000004042760 | 1.000004042760 | 1.099134878304 | 1.099134878304 |
| core_shear_crimping | 3.095893356651 | 3.095893356651 | 3.095893356651 | 3.095893356651 |
| core_crush | 5.055822063463 | 5.055822063463 | 5.055822063463 | 5.055822063463 |
| face_wrinkling | 0.541692740664 | 1.000000000000 | 1.354353251534 | 1.354353251534 |
| intracell_dimpling | 4.975309121116 | 4.975309121116 | 5.037071579171 | 5.037071579171 |

These today/full mode columns hold geometry and reserve fixed; they do not claim the geometry fits today's panel/film mass budget. Replacing its seams/films with today's endpoints gives 1229.431530407718 kg reserve, reproducing the card.

## All 32 subsets

Usage is logarithmic, u=max[0,ln(required/today)/ln(full/today)]; film uses the inverse ratio. It is not a linear fraction of improvement. The independent exhaustive grid uses 1999 interior fractions k/2000 and all 25×25 endpoint-spaced panel/film combinations on 47 cores. All outcome classifications agree. The largest score residual is below 2.5e−8; this is below the declared 5e−8 numerical comparison tolerance. Headline scalar mass/modes agree to floating-point precision.

| Set (G gamma, W wrinkle, S strength, P panel, B film) | Filed usage | Own same-grid usage | Within endpoints |
|---|---:|---:|---|
| ∅ | — | — | no |
| G | 1.95603551746 | 1.95603550451 | no |
| W | — | — | no |
| S | — | — | no |
| P | — | — | no |
| B | — | — | no |
| G,W | 1.75834185978 | 1.75834184588 | no |
| G,S | 1.95603551746 | 1.95603550451 | no |
| W,S | 4.21649191932 | 4.2164919045 | no |
| G,P | 1.4921435051 | 1.4921435051 | no |
| W,P | — | — | no |
| S,P | — | — | no |
| G,B | 1.76360305366 | 1.76360304499 | no |
| W,B | — | — | no |
| S,B | — | — | no |
| P,B | — | — | no |
| G,W,S | 1.11017208072 | 1.11017205628 | no |
| G,W,P | 0.834659884358 | 0.834659884358 | yes |
| G,S,P | 1.4921435051 | 1.4921435051 | no |
| W,S,P | 2.44244177762 | 2.44244177762 | no |
| G,W,B | 1.27201652532 | 1.27201651363 | no |
| G,S,B | 1.76360305366 | 1.76360304499 | no |
| W,S,B | 3.43131754151 | 3.43131753116 | no |
| G,P,B | 1.32546682819 | 1.32546682819 | no |
| W,P,B | — | — | no |
| S,P,B | — | — | no |
| G,W,S,P | 0.773437596848 | 0.773437596848 | yes |
| G,W,S,B | 0.919468771067 | 0.919468751809 | yes |
| G,W,P,B | 0.719318272715 | 0.719318272715 | yes |
| G,S,P,B | 1.32546682819 | 1.32546682819 | no |
| W,S,P,B | 1.71195249683 | 1.71195249683 | no |
| G,W,S,P,B | 0.719318272715 | 0.719318272715 | yes |

A second search maximizes the weakest SF at each subset's full endpoints, refines every located maximum and includes both sides of every Vc=2 crossing. Increasing panel width or reducing film increases allowable S and all scored capacities, so full endpoint geometry provides an upper envelope for a subset within its named bounds. All 47 per-core maxima for every subset are in CALCULATIONS.json. The strongest pair is G+W at .900488404807. Of the triples, only G+W+P reaches 1; full-endpoint maximum is 1.045398208390.

Continuous G+W+P refinement yields u=0.833939833782, f=0.158637957849, w=3.130603618568 m. Exact root solving then enforces compression demand=345 MPa and equal gamma/panel usage; residuals are 0 Pa and about 1e−16 in usage. Required gamma=0.468102499569, C=0.609290546965. This is a refinement, not a contradiction of the card's disclosed grid.

## Family and predecessor checks

| Family | Filed full-set SF | Independently refined full-set SF | Refined today SF |
|---|---:|---:|---:|
| aluminium | 1.198548163722 | 1.198557213141 | 0.419234512436 |
| aramid | 0.940696248372 | 0.940818283714 | 0.517417463145 |
| other | 1.038957797615 | 1.039019963465 | 0.314942473911 |

Every full-set family geometry, mass and mode is also evaluated at its reported grid fraction. Aramid remains below 1, constrained by crimp/global and wrinkle. All family winners agree.

At the 019 fixed reserve, the two named cores independently refine to SF 0.556669198388 aluminium and 0.608701337365 aramid. Rebuilt aluminium reserve is 535.945907158891 kg. All eight fixed-reserve subset values reproduce, including G+W usage .665635107091. The 021-rev1 E290/283 MPa, 5%-margin grid check reproduces .958071728400.

## Numerical and source qualifications

There are 218 explicit scalar comparisons: 216 within tolerance and two retained RMS convention differences. The differences are not discarded or silently normalized.

| Field | Filed | Own with mechanical nu=.33 | Own with inherited width nu=.30 |
|---|---:|---:|---:|
| needed-gamma rms_worst_mm | 1.708852033042 | 1.717841920399 | 1.708852033042 |
| full-curve rms_worst_mm | 0.813274204866 | 0.817552658091 | 0.813274204866 |

The amplitude values 45.819441454003 mm and 21.806317396351 mm reproduce. Their lambda_I=1 fit and width-2.625 RMS must not be treated as a coupled tolerance at the same knockdown. SOURCE-AUDIT.md links the actual equation and fit domain. The near-.45 inversion floor also makes inferred amplitude sensitive to small gamma changes.

The current-grade subset table uses E290 even for O3. Coupling selection of O3 to E293.6 on the same grid changes G+W+S+P from .773437596848 to .762656524691, G+W+S+B from .919468771067 to .912124640700 and all five from .719318272715 to .708874022151. This is conservative inconsistency in interpretation, not a lost feasibility margin. Every subset's yes/no outcome and the chosen no-O3 triple remain unchanged.

The critical source transfer is tensile 345 MPa to thin formed-sheet compression. The exact point has only 0.00000404 compression SF above 1. A historical lower-nu scalar screen gives fixed-geometry global SF .961118; retuning the same set reaches 1 within the endpoints at usage .883289. A full orthotropic calculation remains needed. At +1% pressure the printed needed-value point has minimum SF .990099; at uniformly minus .1016 mm face gauge it has wrinkle SF .787988. These are stated sensitivities, not a claim that an unmeasured condition occurs.

All seven NFI rows are open evidence tasks, not vetoes. Original NFI rows are retained in snapshots/NFI.json. The grade, core, adhesive, climate and source tags are explicitly audited in INPUTS.json and SOURCE-AUDIT.md.

## Reproduction and scope

Run `python3 check021b.py`, `python3 supplemental.py`, then `python3 make_check.py` from this output directory. CALCULATIONS.json and SUPPLEMENTAL.json preserve independent searches, exact residuals and sensitivities; RESULTS.json packages them. No owner program is used as an oracle. Material transfer and model validation are distinct from reproducing arithmetic.

Started 2026-10-20T01:01:34-07:00; ended 2026-10-20T01:21:10-07:00. Times are measurements only. The checker submits one report and ends the turn; the robotics seat assigns further work.
