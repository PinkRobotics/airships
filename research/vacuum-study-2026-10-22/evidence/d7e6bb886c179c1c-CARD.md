**MAINLINE-043 fold of MAINLINE-041 — QUESTIONABLE / PROJECTION**

The two re-sized frequency-5 points are now scored alongside the frozen 022d result. **Neither point has a qualified member or frame failure probability.** The new geometry and actual FE end demands improve the definition of the calculation; they do not supply the missing finished-member compression distribution. The original 043 report and its material evidence remain unchanged.

At their own screened load multipliers, the 5% and 019 reserve points reach **1.164235 / 1.145748 GPa** peak longitudinal compression, reproducing MAINLINE-041. With hypothetical compression m=10 and a common complete-member scale, the summed per-member peak envelopes require **8.53751 / 8.39866 GPa** for tube-only frame Pf=10⁻⁶. These are 2.18911× / 2.15350× an *assumed* 3.9 GPa complete-member scale. The manufacturer's typical 3.9 GPa is not that measured statistical quantity, so the actual improvement factor remains unknown.

**Physical size and member count**

| Quantity | Frozen 022d proxy | 041 f5, 5% reserve | 041 f5, 019 reserve |
|---|---:|---:|---:|
| Member count | 433 bookkeeping | 750 actual | 750 actual |
| Joints / end interfaces | No constructed mesh | 252 / 1,500 | 252 / 1,500 |
| OD, mm | 275.083 | 249.559 | 246.600 |
| Wall, mm | 1.13736 | 0.97851 | 0.95433 |
| Mean arc length, m | 3.18419 | 2.39957 | 2.39957 |
| Mean member material volume, litres | 3.11683 | 1.83364 | 1.76721 |
| Total tube volume, m³ | 1.34959 | 1.37523 | 1.32541 |
| Both cylindrical surfaces, m² | 2,373.18 | 2,810.87 | 2,777.68 |
| Tube mass, kg | 4,183.59 continuum | 4,263.22 | 4,108.77 |

The f5 arc lengths range 1.98473–2.62350 m; each point uses its 750 actual lengths. Member volume is only 58.83% / 56.70% of the old representative member, but total volume is 101.90% / 98.21% of the 433-member proxy. Total inner-plus-outer area increases 18.44% / 17.04%. Smaller members therefore do not by themselves provide a correspondingly smaller frame hazard. Counts, volume and surface population must be treated consistently.

**Stress scoring and load level**

The pinned 041 samples contain 18,000 segment force/moment pairs and 1,500 correlated end-demand triplets per design. The final sections differ from the FE sample area, with area and inertia scaled together at unchanged gyration. We retain 041's force-invariance convention and independently reproduce its final-section stress and mass arithmetic. We do not claim an independent FE equilibrium solve.

For each segment, the retained 041 convention is
`compression = q N/A + q(M + N L/1000) ro/[I(1−q N L²/(π²EI))]`.
Here M is that segment's computed FE bending magnitude and L its parent member's full arc length. FE bending and the assumed bow are both amplified. No separate 043 joint proxy is added on top: the actual FE end moment is already included.

| Load case | Frozen 022d bow-only peak, GPa | 041 f5, 5% peak, GPa | 041 f5, 019 peak, GPa |
|---|---:|---:|---:|
| Operating q=1 | 0.947377 | 1.014552 | 1.055262 |
| Each design's own screen | 1.198096 at q=1.258252 | 1.164235 at q=1.143285 | 1.145748 at q=1.083205 |
| Common q=1.258252 | 1.198096 | 1.285383 | 1.337950 |

The common-q f5 rows exceed those designs' declared screened limits. They are counterfactual stress-demand comparisons, not admissible operating claims. The own-screen rows compare different pressure margins. The old bow-only and new amplified-FE-plus-bow fields also differ in modeling detail; the frozen 043 card retains its separate 022d joint-proxy result, 1.26913 GPa at target.

Positive longitudinal tension is zero in all six new scored fields. At their own screens, the least longitudinal compression is still 746.823 / 733.661 MPa. The minimum imposed initial bow needed to reach longitudinal tension in the retained model is 44.834 / 44.206 mm, versus actual assumed L/1000 bows of 1.985–2.623 mm. These calculations do not resolve contact, hoop stress, shear-induced principal tension or residual stresses.

Operating end-demand maxima are N=0.701228 / 0.701362 MN, M=3.079005 / 3.051787 kN m and T=0.778960 / 0.776171 kN m. They are separate maxima; correlated source arrays are retained. Source joint masses are 42.781 / 38.858 kg, sized to reach their respective target with no additional scalar reserve. Local contact, peel and rotational stiffness are still unqualified.

MAINLINE-041's alternative peak-compression local-wall screen is **1.033223 / 0.978132**. It is an unvalidated interaction surrogate, but the sub-unity 019 value remains a material open issue. A calculated fracture probability cannot turn those local-wall, joint or global screens into qualified capacity. The verified perfect nonlinear calculation in 041 concerned its selected f4 frame, not these re-sized f5 points.

**Conditional member and frame probabilities**

All following compression probabilities assume m=10 and a 3.9 GPa reference characteristic strength. The complete-member hypothesis assigns the same scale to every member; the 1 cm³ hypothesis instead uses each member's actual volume. Neither reference assignment is established by the catalogue evidence. Within each member, its peak compression is conservatively applied to its entire material volume. Independent member hazards are summed.

| Point and load | Frame Pf, common complete-member scale | Frame Pf, 1 cm³ reference scale |
|---|---:|---:|
| 022d operating, frozen | 0.000309745 | 0.619235 |
| 041 5% operating | 0.000643916 | 0.700001 |
| 041 019 operating | 0.000947308 | 0.818685 |
| 022d own screen, frozen | 0.00323635 | 0.999959 |
| 041 5% own screen | 0.00252417 | 0.991133 |
| 041 019 own screen | 0.00214283 | 0.979046 |
| 041 5% at common q=1.258252 | 0.00672419 | 0.999996687 |
| 041 019 at common q=1.258252 | 0.00992957 | 0.999999985 |

At their own screens, the complete-member hypothesis gives member Pf ranges 3.706×10⁻⁷–5.620×10⁻⁶ for 5%, and 3.135×10⁻⁷–4.789×10⁻⁶ for 019. The corresponding 1 cm³-reference ranges are 0.000657677–0.0112041 and 0.000536142–0.00921025. Six `MEMBERS-*.csv` files retain the 750 member contributions at each of three loads for both designs.

Assigning the single **frame-wide maximum stress to all 750 members** would instead give own-screen complete-member frame Pf **0.00420636 / 0.00358530**. The lower summed results above retain unequal member stresses. This distinction matters when comparing with the old identical-member proxy; neither result is an actual reliability prediction.

The 100 cm³ compression-reference sensitivity gives own-screen frame Pf 0.0461547 / 0.0379168. The large spread among reference-size assumptions persists after adopting the new point. Compression m, scale and reference size remain absent from the retrieved matched evidence; the inherited source review [source link unavailable in this public projection] documents that gap and the [ASTM C1424 limitation](https://store.astm.org/c1424-26.html).

**Required strength or scatter**

The following table inverts the summed, unequal per-member stress envelopes at each design's own screen. It assumes one common **complete-member** compression characteristic strength. It does not apply a second volume correction to that already member-sized scale.

| Assumed m | 5% scale for Pf=10⁻³ / 10⁻⁶, GPa | 019 scale for Pf=10⁻³ / 10⁻⁶, GPa |
|---:|---:|---:|
| 5 | 16.426 / 65.398 | 16.158 / 64.334 |
| 8 | 5.984 / 14.192 | 5.887 / 13.961 |
| 10 | 4.27868 / 8.53751 | 4.20909 / 8.39866 |
| 11 | 3.788 / 7.099 | 3.727 / 6.983 |
| 15 | 2.740 / 4.343 | 2.696 / 4.273 |
| 20 | 2.196 / 3.102 | 2.160 / 3.052 |
| 30 | 1.764 / 2.220 | 1.735 / 2.184 |

At m=10, putting all members at the global maximum gives the more conservative common-scale requirements **4.50324 / 8.98559 GPa** for 5% and **4.43173 / 8.84291 GPa** for 019. The frozen 022d requirements are 4.38651 / 8.75267 GPa. Thus the preferred comparison depends on whether the real unequal stress pattern or an identical global-maximum envelope is used.

Holding the common complete-member scale at an assumed 3.9 GPa requires m≥**10.7432 / 16.3024** for 5%, and **10.6037 / 16.0895** for 019. At m=10 with a 1 cm³ reference, the required coupon scales become **9.08838 / 18.13461 GPa** and **8.90764 / 17.77397 GPa**. Neither the compression modulus nor a reference-size interpretation can be borrowed from flexure without qualification.

At the common q=1.258252, m=10 complete-member requirements rise to 4.72012 / 9.41835 GPa and 4.90854 / 9.79432 GPa. These counterfactual demands underscore that the lower own-screen requirement partly reflects the lower achieved pressure margin.

For a sufficient equal allocation among 750 members, the member probability limits are 1.33400×10⁻⁶ / 1.333334×10⁻⁹ for frame targets 10⁻³ / 10⁻⁶. The needed property remains confidence-qualified **finished-member lower-tail strength in the actual combined stress field**. A sufficient scalar-compression criterion at the 10⁻⁶ frame target is strength above each member's stress at its 1.333334×10⁻⁹ quantile; using the global maximum makes that 1.164235 / 1.145748 GPa for every member. Alternative risk allocations give the unequal-stress requirements above. The empirical quantiles and actual improvement factor are unknown.

**Tensile size sensitivity**

Retaining the original explicit SA hypothesis—380 MPa treated as a mean, m=10, assumed 40/20 mm bend spans, derived coupon scale 399.432 MPa—the uniform positive-tension caps are:

| Calibration / frame target | Frozen 022d, MPa | 041 5%, MPa | 041 019, MPa |
|---|---:|---:|---:|
| Volume / Pf=10⁻³ | 31.333 | 31.274 | 31.390 |
| Volume / Pf=10⁻⁶ | 15.703 | 15.673 | 15.731 |
| Both surfaces / Pf=10⁻³ | 36.382 | 35.771 | 35.814 |
| Both surfaces / Pf=10⁻⁶ | 18.233 | 17.927 | 17.948 |

This shows why smaller individual tubes do not eliminate the frame tensile-size penalty: total volume changes little and total surface grows. A hypothetical uniform 50 MPa tensile stress throughout the tube material gives frame Pf 0.103414 / 0.099861, versus 0.101588 for the old proxy. At 25 MPa the new values are 0.000106597 / 0.000102736. These are separate positive-tension sensitivities, not nominal beam predictions.

RESULTS also retains SA m=8, RBSC and the two miniature CVD inner-surface populations, with assumed stressed fractions 1, 0.01 and 0.0001. Each population keeps its own reference calibration. Commercial CVD and SiC/SiC still lack the compatible information needed for a full-member transfer. [ASTM C1683](https://store.astm.org/c1683-10r24.html) frames the compatible-flaw-population and stress-field assumptions.

**Proof, open questions and filing**

The original proof outline still applies, now to **750 members and 1,500 end interfaces**. An illustrative 1.25× own-screen load gives peak axial test demands about **1.00213 / 0.94965 MN**, with pressure-equivalent multipliers 1.42911 / 1.35401. Both exceed the corresponding source screen; those force ratios also do not guarantee matching amplified bending stresses. Fixture, proof-damage, stress coverage and life validation remain necessary. Cost remains high/custom qualification plus recurring complete-part inspection and proof; no price or scrap estimate is established.

The integer count and selected-point force inputs are now specified for the 041 cases. The material calibration, local-shell interaction, joint/contact behavior, common-cause risks and lifetime questions remain open. The sub-unity 019 local-wall sensitivity is preserved separately from fracture projections. [NFI.json](baff59a164490001-NFI.json) records the fold-specific disposition and carries the earlier qualification register by reference.

The fold verifies 26 input pins and **843 scientific checks**, covering source stress/mass reproduction, member grouping, probability bounds and inverse requirements. Its one single-core, 1 GiB postprocessing job completed and released; no new FE solve was performed. The original 043 package remains frozen. This completes `ord-admiral-rr2-mainline043-fold-041-1020`; file the supplement to sciences, cc co, xo and the robotics admiral, then SLEEPING.
