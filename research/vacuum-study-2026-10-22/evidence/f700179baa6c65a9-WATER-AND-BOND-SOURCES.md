# Water retention and the proposed bond

QUESTIONABLE / PROJECTION. No matched outdoor-retention or installed bond qualification is established.

## What the retention sources support

The pinned 016 input explicitly calls its 0.1–1 mm retained surface-film band an owner assumption. The pinned 019 input selects 0.1 mm in its optimistic planning scenario and 1 mm in a separate conservative scenario. It expressly describes planning scenarios rather than measured site or statistical bounds. Its water entry refers to equivalent whole-surface retention, not rainfall depth. See 016 input [source link unavailable in this public projection] and 019 input [source link unavailable in this public projection].

Thus neither thickness is a measured retention value for CCAg, multilayer CCAg, Ag/FEP, AZ-93 or their Be installations. The source supports carrying **both named scenarios**, not asserting 0.1 mm as a safe upper bound. It also does not establish 1 mm as a maximum. Atmospheric `both` weather retains whichever vehicle-water scenario is explicitly selected; it does not automatically import 019's entire conservative account.

The original 048 research separates bulk-material uptake from exterior liquid. FEP's low absorption concerns the film material; it does not measure water on its exterior, in overlaps or at edges. Historical AF163-2U WVR is regained moisture after a specified outgassing/humidity procedure; it is not exterior retention or equilibrium uptake for the chosen cure. TML remains distinct from water inventory. See the filed [048 source audit](fa88eaee87d844a8-SOURCE-AUDIT.md).

| Route | Exterior liquid before processing | Source-supported exterior limit after processing / in wet service | Added material-water accounting |
|---|---|---|---|
| Dry-gas assembly | Unmeasured; evaluate 0.1 and 1 mm wet-service scenarios | No measured limit. Dry gas alone does not establish surface shedding or future wetting. Both service scenarios remain. | No removal credit for pre-existing modeled material water. |
| Preseal 70 °C bake | Unmeasured; accessible existing liquid can evaporate | No measured residual or later wet-service retention. A dry release condition would need measurement; both wet-service scenarios remain. | Assume a 90% reduction of the separately modeled material inventory, subject to demonstrating that endpoint. |
| Internal onboard sorbent | Unmeasured exterior inventory | No direct external-liquid removal mechanism or measured exterior limit. Both service scenarios remain. | Water stays aboard; add bed/cartridge and apply the stated vapor-capture assumption. |

The numeric rows are scenario accounting, not measured before/after moisture results. The actual outside-water values before and after each process are unknown. A verified dry release and an operating restriction excluding later wetting would constitute a separate envelope; neither is proved by the listed process.

For reference, 0.1 / 1 mm charge 125.664 / 1256.637 kg at R10, 180.956 / 1809.557 kg at R12, and 282.743 / 2827.433 kg at R15. The paired rows hold all other loads and the coating's dry optical input fixed. Wet optics, latent heat, drainage and structural water distribution remain unqualified.

CHECK-040's best 1 mm result of −594.989 kg at R30 belongs to its original **0.20 kg/m² coating account**. This addendum reruns the newly coated account only at R10–15, as 048 requires; it does not transplant that R30 result into an uncomputed new-finish case.

## What the 200 °F source actually tests

The November 2009 3M AF163-2 technical sheet, printed page 15, describes its detailed low-temperature metal-joint tests using:

- AF163-2K at .060 lb/ft².
- EC-3924B primer.
- A 200 ± 5 °F cycle, 50 psi pressure and 1 °F/min rise rate, with 2/4/6-hour cases.
- Metal-to-metal shear and peel tests.

Those are different from AF163-2U at .015 lb/ft² per interface bonded to Be faces and the selected 5056 honeycomb. The 048 structural-primer mass allowance also does not specify or qualify the EC-3924B process. General adhesive-family cure guidance does not transfer the detailed test values to that assembly. [3M technical sheet](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf?fn=TDS_AF163-2.pdf); local PDF [source link unavailable in this public projection] and extracted text [source link unavailable in this public projection].

The proposed construction still needs exact-film/primer/adherend cure qualification, shear/peel/flatwise/creep performance, environmental durability, process pressure/tooling and measured residual strains. Oven setpoint does not establish actual stress-free temperature. CHECK-040 also retains CHECK-037b's tooling concern: the cited 50 psi process pressure is above the selected core's 35 psi minimum-average stabilized compression figure unless tooling changes the load path.

No source test in this record qualifies the target 200 °F, 2U .015 Be/honeycomb bond. That finding is carried explicitly in this addendum's NFI.json, along with the earlier process and structural qualifications.
