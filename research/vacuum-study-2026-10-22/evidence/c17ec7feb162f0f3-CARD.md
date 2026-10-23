# MAINLINE-052 — P3 whole account

**Conditional mass closure exists, beginning at tested radius 10 m in ISA and 12 m in the optimistic weather case, with ground vacuum service. No tested radius through 30 m closes in the combined adverse-weather case. No tested radius carries the 24-hour onboard dry-cavity pump-and-battery package. These are QUESTIONABLE / PROJECTION screens; qualified installed SF, ten-year life and frame failure probability remain unknown.**

Unit `vacuum-mainline052-p3-common-account-1020`. Order `ord-admiral-rr2-mainline052-dispatch-1019`. Primary: the checked f5-019 section resized with the conservative local-peak screen enforced, all SiC tube mass corrected, and every named debit charged once. Full endpoint at R=10 ISA leaves **30.863 kg**. The least root leaves zero payload by construction. Stop and file; no successor.

The complete scenario data are in [RESULTS.json](3078814df8e27774-RESULTS.json), [ROWS.csv](d469fc3a06e1bd8d-ROWS.csv), [MASS-ACCOUNT.csv](6c7d6fdd9a070ffd-MASS-ACCOUNT.csv) and [VACUUM-SERVICE.csv](1f48ae887b968268-VACUUM-SERVICE.csv). Equations, bounds and exclusions are in [METHOD.md](9307f895ceba1166-METHOD.md); source pins and unresolved qualifications accompany this card.

## Payload with every favorable endpoint granted

The columns use the same 100 kg general systems, .1 kg/m² exterior water, gas reserve, complete barrier/protection, tube/sleeve/bond/node bills, weather headroom and explicit load-introduction allowance. Ground hardware50 is additional. Negative values are shortfalls. Pressure-only onboard rows do not sustain the dry-cavity life assumption.

| R, m | Weather | Ground, kg | Onboard pressure only, kg | Onboard dry cavity, kg |
| --- | --- | --- | --- | --- |
| 10 | ISA | 30.863 | -231.471 | -3,958.582 |
| 10 | optimistic | -76.414 | -338.748 | -4,065.859 |
| 10 | both | -429.988 | -692.322 | -4,419.433 |
| 12 | ISA | 231.557 | -30.776 | -5,621.443 |
| 12 | optimistic | 46.259 | -216.074 | -5,806.741 |
| 12 | both | -564.756 | -827.090 | -6,417.756 |
| 15 | ISA | 727.200 | 198.644 | -8,586.689 |
| 15 | optimistic | 365.436 | -163.119 | -8,948.452 |
| 15 | both | -828.029 | -1,356.584 | -10,141.918 |
| 20 | ISA | 2,234.491 | 1,439.714 | -14,533.620 |
| 20 | optimistic | 1,377.330 | 582.553 | -15,390.781 |
| 20 | both | -1,451.805 | -2,246.583 | -18,219.916 |
| 30 | ISA | 8,895.646 | 7,568.424 | -30,235.132 |
| 30 | optimistic | 6,003.914 | 4,676.692 | -33,393.086 |
| 30 | both | -3,545.029 | -4,872.251 | -42,942.029 |

## Least moving-axis set and the required values

S=SiC member compression target, F=effective PBO ply strength, L=ten-year retention, J=sleeve allowance. The declared lower/favorable endpoints are S 1→3.9 GPa, F 3.48→5.8 GPa, L .861568874→.951110130, J max(actual,5% of tubes)→actual. They are engineering targets, not qualified material bounds. Enumerate every subset; minimize moving-axis count, then common log usage u. The actual required SiC strength shown below can be smaller than the search ceiling; excess ceiling strength is unnecessary. None of these axis counts measures confidence.

| R | Weather | Set; u | Required SiC, GPa | Ply strength, GPa | 10-y retention | Sleeve allowance, kg | Payload, kg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | ISA | SFJ; 0.839340 | 1.055318 | 5.343008 | 0.861569 | 45.874 | 0.000 |
| 10 | optimistic | no closure | 1.070940 | 5.800000 | 0.951110 | 36.125 | -76.414 |
| 10 | both | no closure | 1.062923 | 5.800000 | 0.951110 | 35.187 | -429.988 |
| 12 | ISA | SJ; 0.493789 | 1.055318 | 3.480000 | 0.861569 | 148.027 | 0.000 |
| 12 | optimistic | SFJ; 0.873568 | 1.070940 | 5.437248 | 0.861569 | 78.054 | -0.000 |
| 12 | both | no closure | 1.062923 | 5.800000 | 0.951110 | 60.803 | -564.756 |
| 15 | ISA | SJ; 0.124004 | 1.055318 | 3.480000 | 0.861569 | 564.054 | -0.000 |
| 15 | optimistic | SJ; 0.716772 | 1.070940 | 3.480000 | 0.861569 | 201.129 | 0.000 |
| 15 | both | no closure | 1.062923 | 5.800000 | 0.951110 | 118.756 | -828.029 |
| 20 | ISA | S; 0.035814 | 1.049950 | 3.480000 | 0.861569 | 1,681.225 | 0.000 |
| 20 | optimistic | SJ; 0.304542 | 1.070940 | 3.480000 | 0.861569 | 987.860 | 0.000 |
| 20 | both | no closure | 1.062923 | 5.800000 | 0.951110 | 281.496 | -1,451.805 |
| 30 | ISA | S; 0.027289 | 1.037838 | 3.480000 | 0.861569 | 5,738.621 | 0.000 |
| 30 | optimistic | SJ; 0.111521 | 1.070940 | 3.480000 | 0.861569 | 4,689.453 | -0.000 |
| 30 | both | no closure | 1.062923 | 5.800000 | 0.951110 | 950.049 | -3,545.029 |

For a failed row the displayed values are the all-endpoint attempt. All 15 onboard dry-cavity cases fail, so they have no least floating set. Pressure-only onboard roots are separately listed below; they are arithmetic alternatives with the lifetime condition unresolved.

| R | Weather | Pressure-only least set; u | Required SiC, GPa | Ply strength, GPa | Retention | Sleeves, kg |
| --- | --- | --- | --- | --- | --- | --- |
| 15 | ISA | SFJ; 0.664536 | 1.055318 | 4.886589 | 0.861569 | 212.348 |
| 20 | ISA | SJ; 0.256132 | 1.055318 | 3.480000 | 0.861569 | 1,052.998 |
| 20 | optimistic | SFJ; 0.598856 | 1.070940 | 4.725358 | 0.861569 | 587.214 |
| 30 | ISA | S; 0.037331 | 1.052119 | 3.480000 | 0.861569 | 5,662.742 |
| 30 | optimistic | SJ; 0.346452 | 1.070940 | 3.480000 | 0.861569 | 3,096.008 |

At R=10 ISA, S/F/J must move. The actual minimum member target is 1.055318 GPa, the effective ply requirement 5.343008 GPa (92.12% of the raw yarn value), retention 0.861569, and sleeve allowance 45.874 kg. Keeping the inherited 60% ply efficiency prevents 10 m closure within the other stated bounds. R=12 ISA can close at that lower film strength. The primary optimistic continuous crossing within the requested 10–30 m interval is 11.3584 m; the requested discrete first pass is 12 m. ISA already passes at the lower tested boundary, so no smaller-radius optimum is claimed.

## First floating account: R=10 ISA least root

| Debit | kg |
| --- | --- |
| SiC tubes | 4,182.243 |
| joint sleeves and allowance | 45.874 |
| joint bond and installation | 10.107 |
| nodes | 5.040 |
| PBO two plies | 114.631 |
| barrier and protection | 95.751 |
| systems | 100.000 |
| vacuum service | 50.000 |
| gas | 48.894 |
| exterior water | 125.664 |
| contamination | 5.000 |
| mooring load introduction | 33.138 |
| sag lift debit | 73.101 |
| weather headroom | 0.000 |
| Total bill | 4,889.442 |
| ISA lift | 4,889.442 |
| Payload | 0.000 |

The 046 package is 95.751051 kg, including the barrier; the older 034 barrier is not charged again. The inherited 019 bulk reserve is replaced by the explicit gas/water/weather/contamination account. The reference section's local-peak shortfall is repaired: global screen 1.083359, local peak 1, film at ten years 1, and sized joint screens 1. These equality screens provide no unallocated load factor.

## Vacuum and ten-year service

The R=10 least root admits an upper-envelope 1.258056 kg/day external water. Its dry-cavity first crossing is 17.280 h, versus 450.2 h for the total-pressure limit. The scheduled ground interval is 15.552 h. The colder h=2 case shortens the first crossing to 11.475 h. Dry initial fill and demonstrated 90% conditioning removal are assumptions. Initial evacuation to 10 Pa in 24 h requires about 1575 m³/h effective ground speed.

| R | Weather | Dry pumps | Dry equipment+battery, kg | Electrical energy/24 h, kWh | Ground first humidity limit, h |
| --- | --- | --- | --- | --- | --- |
| 10 | ISA | 15 | 4,039.444 | 360.12 | 17.385 |
| 10 | optimistic | 15 | 4,039.444 | 360.12 | 17.356 |
| 10 | both | 15 | 4,039.444 | 360.12 | 17.283 |
| 12 | ISA | 22 | 5,903.000 | 528.12 | 20.869 |
| 12 | optimistic | 22 | 5,903.000 | 528.12 | 20.831 |
| 12 | both | 22 | 5,903.000 | 528.12 | 20.764 |
| 15 | ISA | 35 | 9,363.889 | 840.12 | 26.095 |
| 15 | optimistic | 35 | 9,363.889 | 840.12 | 26.042 |
| 15 | both | 35 | 9,363.889 | 840.12 | 25.984 |
| 20 | ISA | 63 | 16,818.111 | 1512.12 | 34.821 |
| 20 | optimistic | 63 | 16,818.111 | 1512.12 | 34.742 |
| 20 | both | 63 | 16,818.111 | 1512.12 | 34.698 |
| 30 | ISA | 147 | 39,180.778 | 3528.12 | 52.380 |
| 30 | optimistic | 148 | 39,447.000 | 3552.12 | 52.245 |
| 30 | both | 148 | 39,447.000 | 3552.12 | 52.230 |

The dry target is 32.5165 Pa water partial pressure, based on the 046 5%-of-cold-saturation screen. A small pump meeting 954.608 Pa total pressure cannot be credited with this job. E2M28 counts use an assumed 75% nominal inlet speed, 3 Pa ultimate and 1000 W electric input, with a 24-hour battery mission. This rules out this carried package in this envelope; it does not prove that every onboard vacuum architecture fails. Improved WVTR, different power, shorter duty or regenerable capture requires a fresh complete account.

## Frame probability under the two requested readings

Use each resized member's maximum amplified compression over its 24 segments, with m=10. The whole-member hypothesis assigns the same 3.9 GPa scale to each complete member at every size. The coupon hypothesis assigns that scale to 1 cm³ of SiC and includes actual member volume. Both are hypothetical; the catalog does not provide either calibration. Values below use each ground least root, or the favorable attempt if it fails. They are intact-member compression only, not ten-year hull reliability.

| R | Weather | Whole-member Pf | 1 cm³-calibrated Pf |
| --- | --- | --- | --- |
| 10 | ISA | 0.000947798 | 0.824296 |
| 10 | optimistic | 0.00109666 | 0.869382 |
| 10 | both | 0.00101783 | 0.847108 |
| 12 | ISA | 0.000947798 | 0.950457 |
| 12 | optimistic | 0.00109666 | 0.970321 |
| 12 | both | 0.00101783 | 0.96104 |
| 15 | ISA | 0.000947798 | 0.997174 |
| 15 | optimistic | 0.00109666 | 0.998961 |
| 15 | both | 0.00101783 | 0.998233 |
| 20 | ISA | 0.000900995 | 0.999998 |
| 20 | optimistic | 0.00109666 | 1 |
| 20 | both | 0.00101783 | 1 |
| 30 | ISA | 0.00080293 | 1−2.8e-18 |
| 30 | optimistic | 0.00109666 | 1−1.4e-24 |
| 30 | both | 0.00101783 | 1−9.5e-23 |

The disparity worsens with size because the coupon hypothesis charges more SiC volume. Reporting a nearly constant whole-member Pf across radii is a consequence of that hypothesis, not evidence that larger real frames preserve reliability. H values and required scale for Pf=10^-3 are retained in the machine data. Joint, film, instability, damage and common-cause failure are not included.

## P2 at the same weather and service allocation

These are the best filed subset endpoints, heavy70 and vented with retained joint floor, minus the same additional 50 kg ground equipment. P2-048 uses MLCCAg, bake70 and .1 kg/m² exterior water. P2 is not reoptimized here; 048 contains no R=20/30 result. Equal payload does not equate material confidence or life.

| R | Weather | P3-052, kg | P2-040, kg | P2-048, kg |
| --- | --- | --- | --- | --- |
| 10 | ISA | 30.863 | -151.270 | 82.641 |
| 10 | optimistic | -76.414 | -299.686 | -65.635 |
| 10 | both | -429.988 | -638.195 | -404.216 |
| 12 | ISA | 231.557 | -38.779 | 301.687 |
| 12 | optimistic | 46.259 | -303.092 | 37.662 |
| 12 | both | -564.756 | -883.995 | -543.388 |
| 15 | ISA | 727.200 | 270.277 | 811.041 |
| 15 | optimistic | 365.436 | -246.151 | 295.282 |
| 15 | both | -828.029 | -1,380.628 | -839.539 |
| 20 | ISA | 2,234.491 | 1,314.615 | not calculated |
| 20 | optimistic | 1,377.330 | 89.758 | not calculated |
| 20 | both | -1,451.805 | -2,598.996 | not calculated |
| 30 | ISA | 8,895.646 | 6,279.292 | not calculated |
| 30 | optimistic | 6,003.914 | 2,140.737 | not calculated |
| 30 | both | -3,545.029 | -6,931.397 | not calculated |

P2-048 also closes at 10 m ISA and 12 m optimistic under these endpoint assumptions. Both leads fail the combined adverse-weather rows. The P3 least-axis labels S/F/L/J and P2 gamma/Q/material/film labels describe different assumptions and must not be ranked by counting alone.

## Limits and audit

The alternative checked f5-5 family gives −21.563 kg at R=10 ISA, versus +30.863 kg for the selected f5-019 family. Using a 30 kg instead of 50 kg ground band adds 20 kg. Explicitly nesting all 50 kg inside systems100 adds 50 kg, but changes the allocation contract. A further .9 kg/m² water layer costs 1,130.973 kg at R=10. The smallest endpoint margin is therefore easily spent. No qualified damage-tolerance fix from 045 is smuggled into a zero mass entry.

The combined-weather cubic subtotal alone exceeds lift by 10.201 kg per (R/10)^3 even before the positive surface/equipment terms. Hence simple enlargement cannot rescue this chosen family at the stated endpoints; this is not a theorem about all possible P3 geometries.

Final validation: **1,440 assertions, zero failures**, including six 750-member comparisons, the checked mechanics, bill identities, roots and all subset monotonic grids. A member-ID mismatch was found and fixed before filing; its superseded run is preserved. All scientific jobs were admitted through simjob at one core/1 GiB and released. [NFI.json](13b38defbfc1755a-NFI.json) carries 15 new open qualifications and points to inherited registers. This card establishes conditional accounts only; no installed-hull pass is filed.

Conditional payload, probability and onboard vacuum costs [source link unavailable in this public projection]
