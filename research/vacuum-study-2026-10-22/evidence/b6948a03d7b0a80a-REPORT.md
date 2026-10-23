# I015 targeted correction disposition

**All five original findings are technically CLOSED.** This is targeted closure of the sole original review's three MEDIUM and two LOW findings, not a new canonical round. One inherited units-label cleanup remains editorial. No physical pressure-capacity or all-up vehicle qualification follows; the separate I019 eleven findings remain open and were not re-reviewed.

## Pins and custody

Candidate `736180fd7f8d8e20bb5aa4702ced78311ad0502e`; tree `2ddef4f134e0cefae662f578cb3c352ef21394a2`; direct parent `525649577913441a7cf29fef9e70de18c43dbbb9` (the original I019 candidate, not an I019 correction). Exactly the three I015 files change, +546/−151. Source HEAD was clean at candidate on `i015-correction`; all three working files matched exact commit blobs. Original I015 branch remains `6ddf3bd1576948bd0c952f25c22e48f4f7b04f17`, I019 branch remains `52564957…`, and landing58 package remains `ef22b604e1fa020d06289be95bd8b623c8d0c970`.

Read and preserved original review REPORT `7e07cb77f3db096907a652f06e7afcf94230b428735ed8157c8bd2373dd3c574`, correction brief `f2f95c8bd62bf4c7f230205a469b8d13274777977c4fda8f0944a1937259a2c2`, both incoming reports, corrected worker evidence and raw checks. Exact source paths, bytes, blobs and hashes are in CUSTODY.json. Original input bytes were copied without rewriting.

Actual governance receipt `gov-00915deeecb4` matches candidate, parent and three paths: approve/clean, three low extends findings, zero conflicts, 3/3 proposals applied, no new debt, 718 carried. Builder and Co-Authored-By are `glm-5.3`; governance is not scientific validation.

## Five original findings

| Finding | State | Targeted evidence and limits |
|---|---|---|
| F1 MEDIUM: coordinate mapping | CLOSED | `coupled.py:251–259,601–655`, JSON conventions/reconciliation and README state `y=√D c`, `c=y/√D`; trial maps to `y=(1,−1)`. Stored values `0.9679228632975162` and `0.9852152424534183` reproduce the prior demonstrated values. False impossibility argument withdrawn; old inconsistent values retained as history. Seven stored eigenvalues compare exactly equal with original committed JSON; matrix/eigensolver construction is unchanged. |
| F2 MEDIUM: vector and direct energy | CLOSED under declared model assumptions | Both comparison and completed geometries export all 22 `y` entries and mapped radial entries, with interleaved n=2…12 cos/sin order determined by `idx`. Stored squared norms are `1.0000000000000002` and `1.0`; mapping error is zero. `direct_member_energy` (`275–300`) evaluates both endpoints separately and sums `½(E a_pc/L̄)ΔL²`; it does not call the matrix assembler. `energy_rows` (`516–535`) independently compares with the assembled quadratic. All four stored products match within `8.31e−16`. Uniqueness is withdrawn and the block-diagonal counterexample named. See energy scope below. |
| F3 MEDIUM: extra assembly | CLOSED | `coupled.py:559–564` charges `lugs_t*(1+ASSEMBLY)`. The extra 14.8645 t of lugs incurs 0.743225 t assembly; corrected stacked sea-level figure is +17.3 t in code/output/README. Nominal construction and positive sign remain unchanged. |
| F4 LOW: precision claim | CLOSED | Code/output/README and the amendment explicitly retain `1.000150027465328` versus `1.000150027596421`, difference `1.3109313634629416e−10`. Both print 1.0002 at four decimals, but 1.000150027/1.000150028 at nine. Full-precision equality withdrawn; original evidence/submission bytes remain preserved. |
| F5 LOW: comparison and sag summaries | CLOSED | README now states compliant comparison 0.7809, matching JSON `0.7808988797775454`; both family sags are shown, 0.063/0.0815 m, with worst 0.0815 m. Comparison FAIL remains. |

**Energy scope and units.** Static expansion of the endpoint formula gives, for one family, `U = 2 E a_j A sin²(φ/2)/(N L̄) Σ_a S_a²`, whereas `yᵀK_f y = 2 E a_j sin²(φ/2)/N Σ_a S_a²`; hence `U=(A/L̄)yᵀK_f y`. The direct code represents all identical-angle planes by their aggregate per-start section; distributing that section equally over planes and summing gives the same equal-length expression. This assumes the same angular field at each plane, first-order extension, equal actual per-cord section, rigid endpoint motion for this foundation check and one mean length per family. Actual per-plane `1/L` weighting is explicitly disclosed as ratios **1.2843944535241254** (d60) and **1.2245988424419496** (d180/11). The check validates this selected foundation extension; it does not establish a common physical pressure-work normalization across differing family lengths, ring/crimp energy, geometric/prestress stability or full-vehicle capacity.

For dimensional consistency, `a_j` is the licensed dimensionless section fraction, `A` is the area scale in m², `y,c` have metres of physical amplitude, `K_f` has Pa, `yᵀK_f y` has N, and `A/L̄` has m, yielding J. **Editorial carry:** the inherited `coupled.py:700` / JSON `conventions.units` phrase “K Pa per metre of modal amplitude” should say **K in Pa**. The newly stated per-member dimensions are correct. This stale label does not alter the verified products or reopen the missing-vector/direct-energy MEDIUM finding.

The stored physical-amplitude estimate uses a finite angular grid; no claim of an exact continuous maximum is adopted here. The completed pure-s5 amplitude is `1/√24 = 0.20412414523193154 m` for unit numeric y norm. Prior matrix comparison FAIL, altitude −459.6 t and SF1.2 sea-level −296.3 t remain unchanged. Conditional completed-matrix pass and nominal +32.9 t arithmetic remain model-scoped; full physical status is UNKNOWN. References to I019 do not qualify its uncorrected termination or explicit slack claims.

## Checks and public text

Preserved raw gate receipts record argv/start/wall/exit/output hash: `make readmecheck` 03:59:42−0700 / 0.05 s / exit 0; `make linkcheck` same start / 0.46 s / exit 0; `make buildercheck` same start / 16.89 s / exit 0. Output hashes match. README output says generated figures match; linkcheck reports 845 documents, zero errors, 216 external links unfetched. Builder reports 1051 checked + 51 exempted and 12 tests OK. Nonshallow first-parent history from `602d88df275a6f44c4bf233e94f27e04e1dd1d29` through candidate contains **1102** inclusive commits, consistent with that coverage, including candidate. Gate times follow candidate's recorded 03:58:51 commit timestamp. **Attribution limit:** raw gates.json omits cwd/HEAD; execution on final tip is worker-attributed and consistent with coverage/times, not independently captured in those absent fields. Numerical regeneration/determinism are also worker-reported; no separate raw numerical execution receipt was supplied.

One data-only scalar check was necessary to validate the full exported vectors and dependent stored representations without replay. Exact script and stdout/stderr are retained. Invocation from lead workspace:

```bash
timeout 60s python3 -I -B .ship/artifacts/r3-i015-corrected-1014/scalar-check.py
```

CPU limit 30 s, address space 1 GiB; exit 0, observed wall 0.000265 s, max RSS 12440 KiB. It parses stored JSON only: vector norms/mapping, seven-value exact comparison, four energy products/ratios, historical-value match, rounding and assembly/sag checks. It does not independently rerun endpoint enumeration, a matrix solve or the generator; the independent energy conclusion above comes from source tracing and algebra. No canonical reviewer, new model, full suite/gate, ancestor replay, sweep, renderer or external source lookup was launched. All tool calls completed; no tracked job remains.

Corrected I015 README and new commit text meet the requested public hygiene: no internal review-round labels, internal artifact directory names, queue/order IDs or “Captain”. Existing Builder/governance trailers remain. Source/runtime/primary, outbox and state were not changed; no ship-seat contact occurred.

## Artifact bindings

| Artifact | SHA256 |
|---|---|
| `CUSTODY.json` | `5c255654dad67571988ee8dee7ae08b12828b609da29b642c021f7e552eef8f3` |
| `EVIDENCE.original.json` | `c605a3ccc15cf1adafbc965b1680c326e169663a25047155fd1b5b25deea5c4d` |
| `governance.original.md` | `3fa15fdc6fcef87caec97a48230a221315a7f0372d0aa1cff0ac4ea70276c345` |
| `gates.original.json` | `4264284436d8d79d8361f4ab3dcd7f2f1120d333ba5e8128a3544b6c4252ae6e` |
| `scalar-check.py` | `84b172bf7efc4964eb93506cb174e5d2dae03c1e70909d7cbb524e7e8c50dc21` |
| `scalar-check.stdout` | `0aaf01bcce5dfff72f0bf627e2214506179914af9c65fa634d5a4dfa736d0d42` |

Exact candidate file SHA256:

- `README.md`: `ab53e7e6d6cf9decfeea34888c9919ae10fe4d525818d29f088bf23f004d3336`
- `coupled.json`: `164a394f0ca0ffe8ce9acff09a099a4b0ce46429e0a7045dc0dd944477fd247b`
- `coupled.py`: `24694cdb24991469191f0d31e5dec471bdc4cc2767fde73666f41c2b9224a8b8`
