# Reference scene audit

The old reference was the 2026-10-01 fleet day at seed 7: 86 recorded fires, one eligible out-of-control fire of 21 ha, all 16 ships assigned to that fire, zero qualifying fires without a ship. The new reference is the seed-7 exercise: 117 invented fires, 43 out of control, 16 distinct fires served, 27 qualifying fires without a ship. The live failure fallback remains the same real day.

All changed mission values below result from changing the scene, not the vehicle or energy model. Rates and legs are rounded here for readability; the golden files retain their prior precision.

| Hull | New exercise fire | Fire size ha, old → new | Water source, old → new | One-way km, old → new | Cycle min, old → new | Release kL/h, old → new |
|---|---|---:|---|---:|---:|---:|
| Condor | EX034 | 21.000 → 42239.867 | Tuchodi Lakes → Redfern Lake | 61.949 → 22.774 | 96.657 → 58.385 | 6207.509 → 10276.624 |
| Osprey | EX090 | 21.000 → 146863.532 | Kluachesi Lake → Maxhamish Lake | 19.628 → 38.957 | 41.488 → 76.892 | 1446.199 → 780.312 |
| Pelican | EX094 | 21.000 → 1743.974 | Kluachesi Lake → None | 19.628 → 12.702 | 41.488 → 34.073 | 1446.199 → 1760.915 |
| Heron | EX044 | 21.000 → 2402.348 | Kluachesi Lake → Klowee Lake | 19.628 → 27.576 | 41.488 → 53.294 | 1446.199 → 1125.823 |
| Albatross | EX057 | 21.000 → 2782.251 | Kluachesi Lake → Pelly Lake | 19.628 → 30.829 | 41.488 → 56.885 | 1446.199 → 1054.764 |
| Skimmer | EX039 | 21.000 → 2006.715 | Kluachesi Lake → Klowee Lake | 19.628 → 25.732 | 41.488 → 51.253 | 1446.199 → 1170.660 |
| Kingfisher | EX074 | 21.000 → 1675.472 | Kluachesi Lake → None | 19.628 → 18.118 | 41.685 → 40.945 | 143.937 → 146.538 |
| Tern | EX116 | 21.000 → 794.055 | Kluachesi Lake → Kluachesi Lake | 19.628 → 18.728 | 41.685 → 40.696 | 143.937 → 147.435 |
| Merganser | EX106 | 21.000 → 608.305 | Kluachesi Lake → None | 19.628 → 16.998 | 41.685 → 37.818 | 143.937 → 158.655 |
| Dipper | EX049 | 21.000 → 258.671 | Kluachesi Lake → None | 19.628 → 5.089 | 41.685 → 19.642 | 143.937 → 305.474 |
| Grebe | EX045 | 21.000 → 202.816 | Kluachesi Lake → None | 19.628 → 6.710 | 41.685 → 21.626 | 143.937 → 277.437 |
| Loon | EX097 | 21.000 → 274.218 | Kluachesi Lake → None | 19.628 → 13.370 | 41.685 → 32.598 | 143.937 → 184.061 |
| Swift | EX058 | 21.000 → 193.485 | Kluachesi Lake → None | 19.628 → 9.269 | 41.685 → 25.865 | 143.937 → 231.970 |
| Petrel | EX022 | 21.000 → 6747.898 | Kluachesi Lake → Aline Lake | 19.628 → 15.900 | 41.685 → 38.702 | 143.937 → 155.032 |
| Kestrel | EX013 | 21.000 → 72.601 | Kluachesi Lake → None | 19.628 → 5.529 | 41.685 → 19.376 | 143.937 → 309.661 |
| Auklet | EX078 | 21.000 → 49.780 | Kluachesi Lake → None | 19.628 → 5.265 | 41.685 → 18.825 | 143.937 → 318.729 |

## Golden audit

| Model key | Result |
|---|---|
| `version` | SAME |
| `note` | MOVED |
| `classes` | SAME |
| `defaults` | SAME |
| `hullNames` | SAME |
| `ledger` | SAME |
| `plans` | SAME |
| `fleet` | MOVED |
| `idle` | SAME |
| `uncovered` | MOVED |
| `states` | MOVED |
| `narrative` | MOVED |
| `selftest` | SAME |

| UI key | Result |
|---|---|
| `title` | MOVED |
| `roster` | MOVED |
| `fires` | MOVED |
| `focus` | MOVED |
| `forces` | MOVED |
| `ops` | SAME |
| `status` | SAME |
| `stats` | SAME |
| `dialCount` | SAME |
| `bars` | MOVED |
| `map` | SAME |
| `m3dMounted` | SAME |
| `avatar` | SAME |
| `selected` | SAME |
| `ships` | SAME |
| `errors` | SAME |

`fleet`, `states` and `narrative` now use invented fire identities, geometry, real lake selections and resulting routes. UI focus, roster, fire rows, forces and bars follow the selected exercise mission. Class constants, defaults, mass/lift ledger, plan grid and self-test output are byte-equivalent as parsed JSON.

The old no-script worked example was Kingfisher, P-100, on the 21 ha eligible fire: 19.8 km model leg, 42 minute cycle, 100 t released, 144 kL/h. The new example is Petrel, P-100, on Exercise 022: 6,748 ha, 17.9 km model leg, 39 minute cycle, 100 t released, 155 kL/h.

The poster remains 924 × 467 pixels. Its former 2026-10-01 record scene is replaced by the invented exercise and a large burned-in EXERCISE label.

The four generated no-script regions formerly described the 2026-10-01 record, real fire sizes and the guard note. They now describe the fixed exercise and contain both exact exercise sentences.

## Published research figures

`tools/figures_dump.js` uses simulation constants and explicitly chosen example distances. It does not read the application scene. Executed against `?view=exercise`, its complete output compared with `research/figures.json` at tolerance 0:

```text
IDENTICAL — every simulation output matches the baseline
```
