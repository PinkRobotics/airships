# MAINLINE-025 independent numerical screen

All physical conclusions are QUESTIONABLE; mixed-material CMC cases are PROJECTION. The compression allowable of a finished ceramic arc, and the node tensile model, remain UNKNOWN. The script imports no inherited executable. It uses closed-form identities and its own search implementation.

## Reconstruction and stress meaning

The stipulated 011b point gives SF=1.225527946881; the 380 MPa proxy point gives 0.262245935560. The original 131-spacing by 4000-radius grid independently recovers both. The latter is an assumed compression-proxy case, not a measured compression failure prediction. The continuous ideal-local result is1.227314390995, slightly above the inherited grid maximum; the difference is search discretization.

At full pressure the SiC baseline mean compression is 1428.350070 MPa. The geometric imperfection adds 58.830561 MPa at one face and subtracts it at the other; the two faces remain at 1487.180631 and 1369.519509 MPa compression. There is zero midspan tensile stress in this assumed loading model. Node/contact tension is a separate unverified load path.

For load multiplier λ, σ=λN₀/A, σ_E=π²EI/(As²), η=(s/1000)r_o A/I, σ_b=ση/(1−σ/σ_E), σ_c,max=σ+σ_b and σ_t,max=max(0,σ_b−σ). N≥N_E returns FAIL_EULER with no post-pole stress. The smaller root of σ_c,max=F_c reproduces geometric Perry capacity; it is a conditional elastic extreme-stress limit. Flexural strength is never silently substituted for a measured F_c. Tension and node limits use separately declared F_t.

## Fixed assumptions and equations

R=10 m; p=95,460.8379139 Pa; lift ceiling=4,889.44215019 kg; film=97.515 kg; systems=50 kg; V=8πR²/(√3s²)+2; nodes=0.02V kg; tube length=(3V−6)s; tube budget=(lift−film−systems−nodes)/1.05; joints=0.05 tube. Area is tube budget/(ρ total length); r_i²=r_o²−A/π; I=A(r_o²+r_i²)/4 exactly. The dimensions are constrained to 0.4≤s≤3 m, sqrt(A/π)×1.0001≤r_o≤min(0.25 m,s/3), retaining the inherited s/3 bound. Mass, Euler and imperfection all retain s as member length; exact spherical arc length, discrete node counts, fixture design and fabrication tolerances are unresolved.

The global pressure is k_g 4√(3/2)E√(IA)/(sR²), with k_g=0.2 fixed. Local critical mean stress is γ_local×0.6Et/r_o. Euler is pinned-end π²EI/s². Film pressure is 2×1.5 GPa×80 µm/s. These modes are independent minima, without a combined local/global/column interaction. Joint mass is only the assigned fraction, with no demonstrated bearing/bond/load-path capacity. Every mass-limited optimized row has zero nominal float margin; it does not reserve useful payload or extra defect tolerance.

## Geometry-independent compression ceiling

Because (3V−6)s²=8√3πR², the inherited load gives N/A=4√3πρpR³/M_tube. The radius and spacing cancel except for spacing-dependent node mass. Ignoring all node mass makes M_tube≤(lift−film−systems)/1.05 and sets an optimistic lower bound on mean compression. Perry bending and all other modes can only reduce the resulting F_c/(N/A) ceiling. For SiC the floor is 1426.237492 MPa. This explains why geometry changes cannot rescue a low assumed compression limit within this mass/load model.

## Local-shell knockdown

[NASA SP-8007 Rev.2](https://ntrs.nasa.gov/api/citations/20205011530/downloads/20205011530%20Rev%202FINALa%201-2023.pdf), report pp.23–25, Eqs.9–10, gives γ=1−0.901(1−exp(−√(r/t)/16)), r/t<1500, for isotropic cylinders. The report cautions about L/r>5 and uncaptured shell/column interaction. Here r=(r_o+r_i)/2 enters γ while the inherited 0.6Et/r_o formula is retained. Curvature, ceramic manufacture and the long-strut range make the transfer QUESTIONABLE. The numerical formula is still evaluated outside r/t<1500 and every row carries an explicit range flag; no extrapolated row becomes an established allowable.

At the original point NASA γ=0.529082162, giving least SF=0.648522400. Reoptimizing the conditional 3900 MPa case gives SF=1.075748394, s=2.337089226 m, r_o=108.721372 mm, t=1.149730 mm.

## Conditional SiC reoptimization

| Assumed F_c MPa | Local rule | γ at optimum | Least SF | s m | r_o mm | t mm | Active modes |
|---:|---|---:|---:|---:|---:|---:|---|
| 100 | 0.3 | 0.300000 | 0.069072346 | 1.440033 | 239.076194 | 0.320084 | compression_extreme, local_shell |
| 100 | 0.5 | 0.500000 | 0.069152036 | 1.155652 | 250.000000 | 0.245203 | compression_extreme |
| 100 | 0.7 | 0.700000 | 0.069152036 | 1.155652 | 250.000000 | 0.245203 | compression_extreme |
| 100 | 1.0 | 1.000000 | 0.069152036 | 1.155652 | 250.000000 | 0.245203 | compression_extreme |
| 100 | NASA | 0.274755 | 0.069035480 | 1.414105 | 226.769511 | 0.331362 | compression_extreme, local_shell |
| 200 | 0.3 | 0.300000 | 0.137481064 | 1.251706 | 157.891981 | 0.421155 | compression_extreme, local_shell |
| 200 | 0.5 | 0.500000 | 0.137985253 | 1.385880 | 214.190118 | 0.343802 | compression_extreme, local_shell |
| 200 | 0.7 | 0.700000 | 0.138257012 | 1.351989 | 250.000000 | 0.287241 | compression_extreme, local_shell |
| 200 | 1.0 | 1.000000 | 0.138302742 | 1.154455 | 250.000000 | 0.244946 | compression_extreme |
| 200 | NASA | 0.345295 | 0.137630254 | 1.286140 | 171.634460 | 0.398105 | compression_extreme, local_shell |
| 380 | 0.3 | 0.300000 | 0.259647388 | 1.088805 | 107.083842 | 0.540126 | compression_extreme, local_shell |
| 380 | 0.5 | 0.500000 | 0.260908672 | 1.210718 | 145.497360 | 0.442029 | compression_extreme, local_shell |
| 380 | 0.7 | 0.700000 | 0.261605125 | 1.297004 | 178.003978 | 0.387098 | compression_extreme, local_shell |
| 380 | 1.0 | 1.000000 | 0.262246189 | 1.394308 | 220.394509 | 0.336155 | compression_extreme, local_shell |
| 380 | NASA | 0.418420 | 0.260499014 | 1.165838 | 130.688049 | 0.473860 | compression_extreme, local_shell |
| 1000 | 0.3 | 0.300000 | 0.671624706 | 1.137118 | 68.208732 | 0.889542 | compression_extreme, local_shell, global_lattice |
| 1000 | 0.5 | 0.500000 | 0.678886062 | 0.941377 | 79.414678 | 0.629503 | compression_extreme, local_shell |
| 1000 | 0.7 | 0.700000 | 0.681884481 | 1.022095 | 97.742847 | 0.555277 | compression_extreme, local_shell |
| 1000 | 1.0 | 1.000000 | 0.684574023 | 1.111081 | 121.623526 | 0.485129 | compression_extreme, local_shell |
| 1000 | NASA | 0.535449 | 0.679537708 | 0.956457 | 82.804761 | 0.613376 | compression_extreme, local_shell |
| 3900 | 0.3 | 0.300000 | 0.907738458 | 2.769652 | 92.032373 | 1.615798 | local_shell, film, global_lattice |
| 3900 | 0.5 | 0.500000 | 1.031863297 | 2.436486 | 104.349877 | 1.249834 | local_shell, film, global_lattice |
| 3900 | 0.7 | 0.700000 | 1.122576528 | 2.239598 | 113.393626 | 1.055595 | local_shell, film, global_lattice |
| 3900 | 1.0 | 1.000000 | 1.227314391 | 2.048473 | 123.867713 | 0.882690 | local_shell, film, global_lattice |
| 3900 | NASA | 0.590442 | 1.075748394 | 2.337089 | 108.721372 | 1.149730 | local_shell, film, global_lattice |

No row in this table establishes the assumed F_c. Low values and 380 MPa are scenario inputs. A tensile weakest-link or Weibull extrapolation is not used as a compression law.

## CMC scalar screening

[NASA CMC dataset](https://ntrs.nasa.gov/api/citations/20210021598/downloads/TM-20210021598.pdf): E=272 GPa, ρ=2440 kg/m³, tensile PLS=128 MPa, UTS=357 MPa for the selected CVI balanced 0/90 Sylramic-iBN material supplied by the parent research. The calculation uses F_t=128 MPa as a no-cracking tensile proxy. F_c=128 MPa is a no-cracking proxy, 300 MPa an assumption, and 580 MPa an optimistic mixed-material ceiling from a different Honeywell Hi-Nicalon material. No case is a same-lot orthotropic tube allowable. A single E cannot resolve laminate bending, shear, off-axis and interlaminar failure.

| Assumed F_c MPa | Local rule | γ at optimum | Least SF | s m | r_o mm | t mm | Active modes |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 128 | 1.0 | 1.000000 | 0.112455802 | 1.154336 | 250.000000 | 0.311211 | compression_extreme |
| 128 | NASA | 0.341544 | 0.112119344 | 1.355914 | 201.020818 | 0.455436 | compression_extreme, local_shell |
| 300 | 1.0 | 1.000000 | 0.263141074 | 1.410484 | 229.030323 | 0.415837 | compression_extreme, local_shell |
| 300 | NASA | 0.439334 | 0.261538191 | 1.189935 | 139.765984 | 0.574813 | compression_extreme, local_shell |
| 580 | 1.0 | 1.000000 | 0.506234896 | 1.213800 | 153.078345 | 0.535275 | compression_extreme, local_shell |
| 580 | NASA | 0.519380 | 0.502975528 | 1.046478 | 102.700642 | 0.687974 | compression_extreme, local_shell |

The JSON also contains a strict material swap at the frozen SiC s/r_o/t (mass changes), and a mass-limited same-s/r_o swap (wall thickness is recomputed). This distinguishes a fixed physical component from a fixed pair of search coordinates.

## Contact and tension sensitivities

At each declared point the JSON reports C_t in {0,0.02,0.05,0.1,0.2} with σ_contact,t=C_t N/A. This is an illustrative multiplier, UNKNOWN as a node model. The all-compression midspan result cannot establish that a real node has no tensile stress. F_t in {50,100,200,380} MPa is another declared sensitivity; 380 MPa remains a flexural proxy. The optimized contact cases change both s and r_o, whereas fixed cases preserve the baseline geometry.

An additional reliability sensitivity uses F_t=15.586 MPa and 7.192 MPa supplied by the parallel reliability calculation. Those are explicitly hypothetical whole-array uniform tensile-field screens at Pf=10⁻⁶, with assumed Weibull moduli 10/8, 380 MPa mean bend strength and 40/20 mm bend spans. Applying them to the unknown contact stress through C_t is a PROJECTION, not a calibrated contact reliability calculation and never a compression allowable. Fixed results cover C_t={0.005,0.01,0.02,0.05}; the 15.586 MPa branch is also reoptimized.

## Borrowed wall-thickness screens

Minimum walls of 2 mm and 4 mm are pure geometric sensitivity constraints borrowed from a different SiSiC construction example; they are not stated manufacturing limits for Hexoloy SA. The JSON reports both increased mass at the baseline outer diameter and mass-limited reoptimization to a smaller diameter. E=410 GPa and ρ=3100 kg/m³ are held fixed. A wall constraint restricts r_o≤(A/π+t_min²)/(2t_min), with exact annulus area. The original F_t=None 4 mm optimum is ONLY AN UPPER BOUND WITH TENSION UNSCORED: at its limiting multiplier 0.247764181, the model has 3.192013 GPa midspan tensile stress. This is not a complete stress screen. Its mid-radius/thickness ratio is 6.210955, outside a genuinely thin-shell regime; the local-shell expression is uncalibrated and inactive there. Record-level flags identify every unscored positive tensile stress at the limiting load, and a top-level index lists those rows.

Additional 2 mm and 4 mm cases impose F_t=15.586 MPa (uniform-field illustrative reliability screen) or F_t=380 MPa (typical bend-strength proxy, not an allowable), with the NASA local rule. Neither tensile proxy is calibrated to the nonuniform component stress field. Their results are:

| Minimum wall mm | Assumed F_t MPa | Least SF | s m | r_o mm | Tensile stress at limit MPa | Active modes |
|---:|---:|---:|---:|---:|---:|---|
| 2 | 15.586 | 0.794572089 | 3.000000 | 80.839112 | 0.000000 | global_lattice |
| 2 | 380 | 0.794572089 | 3.000000 | 80.839112 | 0.000000 | global_lattice |
| 4 | 15.586 | 0.213946781 | 3.000000 | 41.919556 | 15.586000 | midspan_tension |
| 4 | 380 | 0.233144783 | 3.000000 | 41.919556 | 380.000000 | midspan_tension |

## Corrected equilateral equilibrium and inherited demand

There is a distinct inherited load-path inconsistency. Each of the three triangular-grid member families has length density 2/(√3s). Because the direction factors sum to Σcos²θ=3/2, membrane force per width is N_x=(√3/s)N_member. Sphere equilibrium N_x=pR/2 therefore gives N_member=pRs/(2√3), while the inherited point uses pRs/2. The inherited Et=2EA/(√3s) is consistent with the former rule. The pinned NOTE-P3-EQUILIBRIUM confirms this correction by membrane, node and tributary-load equilibrium. The corrected branch changes only the member-force factor to 1/√3, leaving global and film expressions unchanged. Uniform triangular topology and the smeared global model remain surrogate assumptions requiring discrete-model review. The inherited calculation is retained. Compression, Euler and local pressure factors improve by √3 at fixed geometry; geometry-dependent reoptimization is reported for every requested compression scenario. At the original SiC geometry the two mean demands are 0.824658297 and 1.428350070 GPa. The film-sag volume/lift charge is owned by 024/022b and is not added to this inherited mass budget.

| Material | Assumed F_c MPa | Reoptimized SF, inherited demand | Reoptimized SF, corrected equilateral demand |
|---|---:|---:|---:|
| SiC | 100 | 0.069035480 | 0.119572959 |
| SiC | 200 | 0.137630254 | 0.238382593 |
| SiC | 380 | 0.260499014 | 0.451197528 |
| SiC | 1000 | 0.679537708 | 1.168659430 |
| SiC | 3900 | 1.075748394 | 1.205708188 |
| CMC | 128 | 0.112119344 | 0.194196401 |
| CMC | 300 | 0.261538191 | 0.452997435 |
| CMC | 580 | 0.502975528 | 0.871161319 |

The next table freezes the original physical s/r_o/t for each material, so the two mean stresses are the same for SiC and CMC, while mass changes with density. F_t is an independent input: unscored for the SiC compression scenarios and 128 MPa for CMC. The JSON separately provides fixed search coordinates with a recalculated mass-limited wall, avoiding confusion between a physical material swap and a refitted member.

| Material | Assumed F_c MPa | Fixed geometry SF, inherited demand | Fixed geometry SF, corrected equilateral demand |
|---|---:|---:|---:|
| SiC | 100 | 0.067730845 | 0.117313265 |
| SiC | 200 | 0.135402425 | 0.234523880 |
| SiC | 380 | 0.257054643 | 0.445231703 |
| SiC | 1000 | 0.648522400 | 1.123273747 |
| SiC | 3900 | 0.648522400 | 1.123273747 |
| CMC | 128 | 0.086660261 | 0.150099974 |
| CMC | 300 | 0.202869216 | 0.351379790 |
| CMC | 580 | 0.391385707 | 0.677899929 |

## Size/stressed-measure interface for 022b

Every row exposes total and single-member tube material volume, outer/inner surface area, the signed full-pressure and limiting-load stress state, and the force branch. Those geometric extents are not Weibull effective volume or area. Effective tensile measures and size-adjusted compression allowance remain null: 022b must integrate the actual positive tensile stress field with calibrated inputs. Compression stays a separately declared conditional F_c. Node/joint material and tube end faces are not included in these tube surface measures.

## Search verification and forward carry

The inherited 0.02 m / 4000-radius search is labeled grid reproduction. Continuous results use a full-domain grid followed by five separated SLSQP epigraph starts and direct recomputation of each score. A doubled spacing grid and 4000-radius grid are reported separately for selected SiC/CMC cases. These establish numerical resolution for this surrogate, not proof of a global structural optimum. A flat optimum in radius is resolved by maximizing the second-lowest capacity at the chosen spacing, within 10⁻¹² relative tolerance on the primary score. Such a radius is not a unique geometry prediction. Self-checks cover original point/grid recovery, float closure, exact annulus inertia, compressive/tensile roots, and refusal to extrapolate through the Euler pole. Repository tests were not run for this outputs-only analytic script.

Verified starting state: original arithmetic reproduced, stress signs separated, and all requested bounded sensitivity families computed independently. Learned: the inherited mean compression is about 1.43 GPa, so tensile coupon size scaling alone does not resolve compression capacity; local knockdown consumes much of the original small structural margin. Deferred: calibrated ceramic/CMC compression data, probabilistic component reliability, actual nodal stresses, orthotropic shell/column interaction and manufacturing. Next: use these conditional tables to choose the necessary component/connection tests and numerical shell analysis; do not certify the vehicle from this surrogate.

