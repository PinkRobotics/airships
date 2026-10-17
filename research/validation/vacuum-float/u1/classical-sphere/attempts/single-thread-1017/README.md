# Classical sphere: single-thread attempt

Builder outcome: **PASS**. Una verification and landing are pending; no points are awarded here. This is another attempt of the original benchmark, whose [eight-thread FAIL record](../../result.json) remains unchanged.

The [case](case.json) was committed before all solves. It preserves the original geometry, material, supports, S8R formulation, pressure normalization, eight-mode minimum rule and acceptance thresholds. [Deck preparation](prepare_decks.py) regenerated every deck using the unchanged original runner and matched the original middle-mesh hash before any solve. Each deck was then solved exactly once with all seven supported thread controls measured as one in its solver process. No retry or tuning occurred.

| Mesh divisions | Elements | Minimum pressure (MPa) | Source error | Adjacent change |
|---:|---:|---:|---:|---:|
| 16 | 1536 | 25.786410 | 1.443194% | — |
| 24 | 3456 | 25.683610 | 1.038781% | 0.400255% |
| 36 | 7776 | 25.652920 | 0.918048% | 0.119636% |

The original comparator is 25419556.372089703 Pa. Both adjacent changes must be at most 1%, and the finest discrepancy at most 5%; neither rule was relaxed.

One thread refers to the seven measured solver controls. Peak process thread counts were 3, 3, 3; measured average CPU-core use was 0.929825, 0.949093, 0.957608. Process thread counts and configured solver parallelism are reported separately.

The [result record](result.json) retains all eight factors, cluster spans, measured thread counts/CPU use, limits, exit records and absolute raw paths with hashes. Cluster values alone do not establish mode-shape correspondence; the minimum is used at every mesh. This finite series does not establish universal solver determinism or a physical hull result.

For replay, use the pinned original runner from the source freeze, regenerate decks with the supplied preparer under the recorded scope/environment, and pass each deck through the original fixed-deck solve path with one thread. Use fresh run directories under /home. The result record pins the exact frozen sources and complete executed commands.
