# Member census

The drawing and the bill disagree. This generated record preserves those disagreements; it does not approve a cap design.
The checks use smeared areas at full radius and do not resolve station lengths, sections or connections.

gpt-6-astra executed the census and regeneration. muse-spark-1.3 and a second gpt-6 run examined the float case. claude-opus-5-5 ruled the publication basis. A person directs the project; no person checked the arithmetic.

There are **20 recorded comparisons with disagreements** for the hull of record.
A passing `make censuscheck` means fresh measurements match this record, including unknown counterparts.
It does not mean the drawing agrees with the bill.

Generated with `python3 research/analysis/member-census.py`. JSON: [complete measurements](../research/analysis/member-census.json).

## Both directions

Quantities use analytic arcs for rings and meridians, and actual endpoints for straight members.
Rendering segments are not physical member counts. Signed differences are drawn minus billed.
Tonnes price unchanged model sections, including existing allowances; they do not resize or check those sections.
All mass pairs below are record / favourable. Unknown mass is never zero.

| Bill line | Drawing counterpart | Region | Billed quantity | Drawn quantity | Signed difference | Unit | Billed t | Drawn t | Signed t |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| rings | hoops/barrel | barrel | 16,989.733 | 16,989.733 | -0.000 | m | 58.221 / 58.221 | 58.221 / 58.221 | -0.000 / -0.000 |
| capGrid | no explicit grid topology | caps | 8,494.867 | unknown | unknown | m2 | 45.107 / 33.220 | unknown / unknown | unknown / unknown |
| bars | bars/barrel | barrel | 16,989.733 | 17,004.000 | 14.267 | m | 4.185 / 3.587 | 4.188 / 3.590 | 0.004 / 0.003 |
| film | ShipFilm mesh | whole hull | 16,989.733 | 17,723.094 | 733.361 | m2 | 1.968 / 1.968 | 2.053 / 2.053 | 0.085 / 0.085 |
| clamps | GridClamps patch only | whole hull | 16,989.733 | unknown | unknown | count | 2.243 / 2.243 | unknown / unknown | unknown / unknown |
| pads | not drawn | whole hull | 50,969.199 | unknown | unknown | count | 2.039 / 2.039 | unknown / unknown | unknown / unknown |
| longerons | longs | barrel and shoulder overlap | 5,015.774 | 4,869.030 | -146.743 | m | 29.464 / 29.464 | 28.602 / 28.602 | -0.862 / -0.862 |
| innerRings | hoopsInner | barrel and caps | 9,826.902 | 7,508.594 | -2,318.308 | m | 66.785 / 27.163 | 51.029 / 20.755 | -15.756 / -6.408 |
| fanWebs | webs | barrel and caps | 30,437.117 | 29,063.804 | -1,373.313 | m | 13.655 / 13.655 | 13.039 / 13.039 | -0.616 / -0.616 |
| thetaWebs | thetas | barrel and caps | 36,831.504 | 32,292.676 | -4,538.828 | m | 38.011 / 15.735 | 33.327 / 13.796 | -4.684 / -1.939 |
| junctionShear | junctions; section inferred from smeared bill | shoulders | 610.940 | 1,307.772 | 696.832 | m | 7.791 / 5.641 | 16.676 / 12.076 | 8.886 / 6.435 |
| spokes | spokes; diameter inferred from smeared bill | barrel and caps above cutoff | 84,780.045 | 84,780.045 | 0.000 | m | 4.568 / 2.005 | 4.568 / 2.005 | 0.000 / 0.000 |
| flangeDoubler | not independently drawn | barrel | 8,494.867 | unknown | unknown | m2 | 0.000 / 0.000 | unknown / unknown | unknown / unknown |
| torsionStraps | helical straps not drawn; outfit circumferential straps are different | whole hull | 16,989.733 | unknown | unknown | m2 | 0.256 / 0.256 | unknown / unknown | unknown / unknown |
| skins | void skin retired; jacket no separate mesh | whole hull | 16,989.733 | unknown | unknown | m2 | 1.019 / 1.019 | unknown / unknown | unknown / unknown |
| tiJoints | GridJoints patch only | whole hull, unallocated | 263.218 | unknown | unknown | t members | 46.450 / 32.945 | unknown / unknown | unknown / unknown |
| stabilityReserve | additional solved areas; no separate drawing | whole hull, unallocated | 81.340 | unknown | unknown | t allowance | 81.340 / 0.000 | unknown / unknown | unknown / unknown |

| Drawn family | Bill lines or allowance | Barrel m | Caps m | Total m | Physical count or runs | Render segments |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| hoops | rings, capGrid | 16,989.733 | 16,905.361 | 33,895.094 | 260 | 16640 |
| hoopsInner | innerRings | 3,757.345 | 3,751.249 | 7,508.594 | 64 | 4096 |
| longs | longerons | 3,744.000 | 1,125.030 | 4,869.030 | 72 | 2880 |
| webs | fanWebs | 11,946.647 | 17,117.156 | 29,063.804 | 9,216 | 9216 |
| thetas | thetaWebs | 13,803.448 | 18,489.228 | 32,292.676 | 9,216 | 9216 |
| junctions | junctionShear | 664.742 | 643.030 | 1,307.772 | 144 | 144 |
| spokes | spokes | 43,056.000 | 41,724.045 | 84,780.045 | 2,160 | 2160 |
| bars | bars, capGrid | 17,004.000 | 24,888.412 | 41,892.412 | 327 | 15042 |

The outer cap hoops have no hoop bill line. The cap bars have only an area allowance without station identities.
The cap grid has no explicit drawing topology. Partial fitting symbols do not establish whole-hull populations.
Film is billed on projected capsule area; the executed mesh has a different area and volume.

## Recorded disagreements

| Comparison | Region | Kind | Billed | Drawn | Signed difference | Sign |
| --- | --- | --- | ---: | ---: | ---: | --- |
| innerRings | barrel and caps | quantity | 9,826.902 | 7,508.594 | -2,318.308 | negative |
| longerons | barrel and shoulder overlap | quantity | 5,015.774 | 4,869.030 | -146.743 | negative |
| fanWebs | barrel and caps | quantity | 30,437.117 | 29,063.804 | -1,373.313 | negative |
| thetaWebs | barrel and caps | quantity | 36,831.504 | 32,292.676 | -4,538.828 | negative |
| junctionShear | shoulders | quantity | 610.940 | 1,307.772 | 696.832 | positive |
| bars | barrel | quantity | 16,989.733 | 17,004.000 | 14.267 | positive |
| film | whole hull | quantity | 16,989.733 | 17,723.094 | 733.361 | positive |
| capGrid-allocation | caps | no complete drawn allocation | unknown | unknown | unknown | unknown |
| pads-allocation | whole hull | no complete drawn allocation | unknown | unknown | unknown | unknown |
| torsionStraps-allocation | whole hull | no complete drawn allocation | unknown | unknown | unknown | unknown |
| skins-allocation | whole hull | no complete drawn allocation | unknown | unknown | unknown | unknown |
| tiJoints-allocation | whole hull, unallocated | no complete drawn allocation | unknown | unknown | unknown | unknown |
| stabilityReserve-allocation | whole hull, unallocated | no complete drawn allocation | unknown | unknown | unknown | unknown |
| cap-hoops | caps | drawn family has no station-mapped bill line | unknown | 16,905.361 | unknown | unknown |
| cap-bars | caps | drawn family has no station-mapped bill line | unknown | 24,888.412 | unknown | unknown |
| fittings | whole hull | clamp and joint symbols are a close-up, not a whole-hull count | unknown | unknown | unknown | unknown |
| sections | whole hull | inner-ring, fan, theta and junction display sections are schematic | unknown | unknown | unknown | unknown |
| outer-stations | whole hull stations | count | 268.000 | 260.000 | -8.000 | negative |
| inner-stations | barrel and caps | count | 68.000 | 64.000 | -4.000 | negative |
| theta-count | barrel and caps | count | 9,792.000 | 9,216.000 | -576.000 | negative |

## Film, close-up fittings and outfit

These are separate representations, not additional copies of the hull. The film mesh is a schematic drape, not a measured membrane.
The outfit is outside the bare-hull mass comparison; its mass is unknown. The person and wrap are context, not added members.

### film

| Quantity or object | Value or count | Chord length m |
| --- | ---: | ---: |
| vertices | 172,983.000 | — |
| triangles | 345,312.000 | — |
| areaM2 | 17,723.094 | — |
| barrelM2 | 8,716.014 | — |
| capM2 | 9,007.079 | — |
| volumeM3 | 183,201.692 | — |
| billAreaM2 | 16,989.733 | — |

### grid

| Quantity or object | Value or count | Chord length m |
| --- | ---: | ---: |
| GridGhostFrame | 4214 | 8,081.445 |
| GridHoops | 442 | 102.000 |
| GridCross | 11 | 88.000 |
| GridClamps | 47 | unknown |
| GridInner | 130 | 26.538 |
| GridWebs | 56 | 177.088 |
| GridTheta | 60 | 186.385 |
| GridJointsOuter | 63 | unknown |
| GridJointsInner | 35 | unknown |
| GridJointsX | 30 | unknown |
| GridSpokes | 10 | 180.024 |

### outfit

| Quantity or object | Value or count | Chord length m |
| --- | ---: | ---: |
| VesselWrap | 1 | unknown |
| VesselSolar | 622 | unknown |
| VesselStraps | 336 | 784.125 |
| VesselPylons | 6 | 45.000 |
| VesselRotors | 234 | 306.082 |
| VesselPods | 6 | unknown |
| VesselModule | 12 | 119.600 |
| VesselTankWater | 1 | unknown |
| VesselTanksN2 | 2 | unknown |
| VesselLines | 10 | 197.421 |
| VesselLinesWater | 1 | 7.050 |
| VesselRecvBay | 1 | unknown |
| VesselBatteryBox | 1 | unknown |
| VesselCryoBox | 1 | unknown |
| VesselShipMind | 1 | unknown |
| VesselPulleys | 3 | unknown |
| VesselBucket | 1 | unknown |
| VesselSprayer | 1 | unknown |
| VesselPump | 1 | unknown |
| VesselPumpPipe | 1 | 12.700 |
| VesselPerson | 1 | 1.800 |

## Nominal fleet sizes: scaled models

These execute the existing hull model at configured nominal fleet diameters. They are scaled models, not the fleet renderer’s member design.
The fleet simulation uses a dry-structure allowance. This census does not replace that allowance or establish payload capacity.

### Nominal diameter 55 m

| Drawn family | Bill lines or allowance | Barrel m | Caps m | Total m | Physical count or runs | Render segments |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| hoops | rings, capGrid | 19,006.636 | 18,971.914 | 37,978.550 | 274 | 17536 |
| hoopsInner | innerRings | 4,279.816 | 4,139.033 | 8,418.849 | 68 | 4352 |
| longs | longerons | 4,180.000 | 1,256.044 | 5,436.044 | 76 | 3040 |
| webs | fanWebs | 14,035.397 | 20,262.202 | 34,297.599 | 10,336 | 10336 |
| thetas | thetaWebs | 16,306.271 | 21,465.842 | 37,772.113 | 10,336 | 10336 |
| junctions | junctionShear | 740.247 | 745.307 | 1,485.554 | 152 | 152 |
| spokes | spokes | 51,767.692 | 48,734.120 | 100,501.812 | 2,432 | 2432 |
| bars | bars, capGrid | 19,030.000 | 27,853.827 | 46,883.827 | 346 | 15916 |

record: current model bill 487.447 t.

| Bill line | Billed | Drawn | Signed quantity | Unit | Billed t | Drawn t | Signed t |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| rings | 19,006.636 | 19,006.636 | -0.000 | m | 66.853 | 66.853 | -0.000 |
| capGrid | 9,503.318 | unknown | unknown | m2 | 53.103 | unknown | unknown |
| bars | 19,006.636 | 19,030.000 | 23.364 | m | 4.681 | 4.687 | 0.006 |
| film | 19,006.636 | unknown | unknown | m2 | 2.201 | unknown | unknown |
| clamps | 19,006.636 | unknown | unknown | count | 2.573 | unknown | unknown |
| pads | 57,019.907 | unknown | unknown | count | 2.281 | unknown | unknown |
| longerons | 5,599.875 | 5,436.044 | -163.832 | m | 34.137 | 33.138 | -0.999 |
| innerRings | 11,005.241 | 8,418.849 | -2,586.391 | m | 82.363 | 63.006 | -19.356 |
| fanWebs | 35,750.878 | 34,297.599 | -1,453.279 | m | 17.171 | 16.473 | -0.698 |
| thetaWebs | 42,719.908 | 37,772.113 | -4,947.795 | m | 46.959 | 41.520 | -5.439 |
| junctionShear | 682.086 | 1,485.554 | 803.468 | m | 9.218 | 20.077 | 10.859 |
| spokes | 100,501.812 | 100,501.812 | -0.000 | m | 5.405 | 5.405 | -0.000 |
| flangeDoubler | 9,503.318 | unknown | unknown | m2 | 0.000 | unknown | unknown |
| torsionStraps | 19,006.636 | unknown | unknown | m2 | 0.303 | unknown | unknown |
| skins | 19,006.636 | unknown | unknown | m2 | 1.140 | unknown | unknown |
| tiJoints | 314.484 | unknown | unknown | t members | 55.497 | unknown | unknown |
| stabilityReserve | 103.562 | unknown | unknown | t allowance | 103.562 | unknown | unknown |

favourable: current model bill 273.490 t.

| Bill line | Billed | Drawn | Signed quantity | Unit | Billed t | Drawn t | Signed t |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| rings | 19,006.636 | 19,006.636 | -0.000 | m | 66.853 | 66.853 | -0.000 |
| capGrid | 9,503.318 | unknown | unknown | m2 | 39.076 | unknown | unknown |
| bars | 19,006.636 | 19,030.000 | 23.364 | m | 4.013 | 4.018 | 0.005 |
| film | 19,006.636 | unknown | unknown | m2 | 2.201 | unknown | unknown |
| clamps | 19,006.636 | unknown | unknown | count | 2.573 | unknown | unknown |
| pads | 57,019.907 | unknown | unknown | count | 2.281 | unknown | unknown |
| longerons | 5,599.875 | 5,436.044 | -163.832 | m | 33.309 | 32.334 | -0.974 |
| innerRings | 11,005.241 | 8,418.849 | -2,586.391 | m | 37.990 | 29.062 | -8.928 |
| fanWebs | 35,750.878 | 34,297.599 | -1,453.279 | m | 17.171 | 16.473 | -0.698 |
| thetaWebs | 42,719.908 | 37,772.113 | -4,947.795 | m | 18.251 | 16.137 | -2.114 |
| junctionShear | 682.086 | 1,485.554 | 803.468 | m | 6.675 | 14.538 | 7.863 |
| spokes | 100,501.812 | 100,501.812 | -0.000 | m | 2.241 | 2.241 | -0.000 |
| flangeDoubler | 9,503.318 | unknown | unknown | m2 | 0.000 | unknown | unknown |
| torsionStraps | 19,006.636 | unknown | unknown | m2 | 0.303 | unknown | unknown |
| skins | 19,006.636 | unknown | unknown | m2 | 1.140 | unknown | unknown |
| tiJoints | 223.337 | unknown | unknown | t members | 39.412 | unknown | unknown |
| stabilityReserve | 0.000 | unknown | unknown | t allowance | 0.000 | unknown | unknown |

Spoke counts: Python bill 2432; JavaScript formula 2432; drawn 2432.
The odd-column anchor and formula-length questions remain open.

### Nominal diameter 119 m

| Drawn family | Bill lines or allowance | Barrel m | Caps m | Total m | Physical count or runs | Render segments |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| hoops | rings, capGrid | 89,350.037 | 88,582.769 | 177,932.806 | 603 | 38592 |
| hoopsInner | innerRings | 19,842.783 | 19,497.667 | 39,340.449 | 150 | 9600 |
| longs | longerons | 19,635.000 | 5,900.100 | 25,535.100 | 165 | 6600 |
| webs | fanWebs | 136,256.801 | 206,916.411 | 343,173.213 | 49,500 | 49500 |
| thetas | thetaWebs | 142,331.922 | 208,862.356 | 351,194.278 | 49,500 | 49500 |
| junctions | junctionShear | 3,482.506 | 3,424.117 | 6,906.623 | 330 | 330 |
| spokes | spokes | 524,240.769 | 512,190.577 | 1,036,431.346 | 12,118 | 12118 |
| bars | bars, capGrid | 89,012.000 | 130,285.068 | 219,297.068 | 748 | 34408 |

record: current model bill 8,798.679 t.

| Bill line | Billed | Drawn | Signed quantity | Unit | Billed t | Drawn t | Signed t |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| rings | 88,976.187 | 89,350.037 | 373.850 | m | 541.611 | 543.887 | 2.276 |
| capGrid | 44,488.094 | unknown | unknown | m2 | 512.359 | unknown | unknown |
| bars | 88,976.187 | 89,012.000 | 35.813 | m | 21.915 | 21.924 | 0.009 |
| film | 88,976.187 | unknown | unknown | m2 | 10.306 | unknown | unknown |
| clamps | 88,976.187 | unknown | unknown | count | 13.552 | unknown | unknown |
| pads | 266,928.561 | unknown | unknown | count | 10.677 | unknown | unknown |
| longerons | 26,304.678 | 25,535.100 | -769.578 | m | 346.527 | 336.389 | -10.138 |
| innerRings | 50,929.808 | 39,340.449 | -11,589.359 | m | 1,301.646 | 1,005.449 | -296.197 |
| fanWebs | 350,204.985 | 343,173.213 | -7,031.773 | m | 349.336 | 342.322 | -7.014 |
| thetaWebs | 367,408.392 | 351,194.278 | -16,214.114 | m | 1,885.257 | 1,802.058 | -83.198 |
| junctionShear | 3,204.010 | 6,906.623 | 3,702.613 | m | 93.368 | 201.266 | 107.898 |
| spokes | 1,030,187.784 | 1,036,431.346 | 6,243.562 | m | 44.061 | 44.328 | 0.267 |
| flangeDoubler | 44,488.094 | unknown | unknown | m2 | 284.012 | unknown | unknown |
| torsionStraps | 88,976.187 | unknown | unknown | m2 | 3.072 | unknown | unknown |
| skins | 88,976.187 | unknown | unknown | m2 | 5.339 | unknown | unknown |
| tiJoints | 5,336.031 | unknown | unknown | t members | 941.653 | unknown | unknown |
| stabilityReserve | 2,433.990 | unknown | unknown | t allowance | 2,433.990 | unknown | unknown |

favourable: current model bill 3,600.018 t.

| Bill line | Billed | Drawn | Signed quantity | Unit | Billed t | Drawn t | Signed t |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| rings | 88,976.187 | 89,350.037 | 373.850 | m | 541.611 | 543.887 | 2.276 |
| capGrid | 44,488.094 | unknown | unknown | m2 | 373.933 | unknown | unknown |
| bars | 88,976.187 | 89,012.000 | 35.813 | m | 18.784 | 18.792 | 0.008 |
| film | 88,976.187 | unknown | unknown | m2 | 10.306 | unknown | unknown |
| clamps | 88,976.187 | unknown | unknown | count | 13.552 | unknown | unknown |
| pads | 266,928.561 | unknown | unknown | count | 10.677 | unknown | unknown |
| longerons | 26,304.678 | 25,535.100 | -769.578 | m | 258.229 | 250.674 | -7.555 |
| innerRings | 50,929.808 | 39,340.449 | -11,589.359 | m | 548.700 | 423.840 | -124.860 |
| fanWebs | 350,204.985 | 343,173.213 | -7,031.773 | m | 349.336 | 342.322 | -7.014 |
| thetaWebs | 367,408.392 | 351,194.278 | -16,214.114 | m | 848.283 | 810.848 | -37.436 |
| junctionShear | 3,204.010 | 6,906.623 | 3,702.613 | m | 67.611 | 145.745 | 78.133 |
| spokes | 1,030,187.784 | 1,036,431.346 | 6,243.562 | m | 20.028 | 20.149 | 0.121 |
| flangeDoubler | 44,488.094 | unknown | unknown | m2 | 0.000 | unknown | unknown |
| torsionStraps | 88,976.187 | unknown | unknown | m2 | 3.072 | unknown | unknown |
| skins | 88,976.187 | unknown | unknown | m2 | 5.339 | unknown | unknown |
| tiJoints | 3,006.488 | unknown | unknown | t members | 530.557 | unknown | unknown |
| stabilityReserve | 0.000 | unknown | unknown | t allowance | 0.000 | unknown | unknown |

Spoke counts: Python bill 11972; JavaScript formula 12118; drawn 12118.
The odd-column anchor and formula-length questions remain open.

### Nominal diameter 256 m

| Drawn family | Bill lines or allowance | Barrel m | Caps m | Total m | Physical count or runs | Render segments |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| hoops | rings, capGrid | 410,970.585 | 412,385.858 | 823,356.442 | 1,309 | 83776 |
| hoopsInner | innerRings | 91,065.588 | 91,007.221 | 182,072.809 | 326 | 20864 |
| longs | longerons | 90,624.000 | 27,231.507 | 117,855.507 | 354 | 14160 |
| webs | fanWebs | 1,341,259.938 | 2,074,857.847 | 3,416,117.785 | 230,808 | 230808 |
| thetas | thetaWebs | 1,352,382.079 | 2,081,364.044 | 3,433,746.123 | 230,808 | 230808 |
| junctions | junctionShear | 16,070.776 | 15,839.447 | 31,910.224 | 708 | 708 |
| spokes | spokes | 5,130,712.615 | 5,121,161.718 | 10,251,874.333 | 56,994 | 56994 |
| bars | bars, capGrid | 411,648.000 | 602,520.868 | 1,014,168.868 | 1,608 | 73968 |

record: sizing refused: `ship_size_compression: no section`.

favourable: sizing refused: `ship_size_compression: no section`.

Spoke counts: Python bill sizing refused; JavaScript formula 56994; drawn 56994.
The odd-column anchor and formula-length questions remain open.

Section allocation, fittings, polar omissions, torsion straps and the retired skin remain [open questions](OPEN-QUESTIONS.md).
