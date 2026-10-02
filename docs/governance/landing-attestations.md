# Landing attestations

## Landing 1 — ord-boyce-land-airships-goals-1001

| field | value |
|---|---|
| Landed | 2026-10-01 20:17:22 PDT by the landing tool (`ship/tools/land.py`) on `ord-boyce-land-airships-goals-1001` from `boyce`, a pure **FAST-FORWARD**: main `09b9c0e2901f624f063a00043da75480cd63129e` → `23bf131deaec6262c226fa31e3637cd48a91d074`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `23bf131deaec6262c226fa31e3637cd48a91d074`, tree `d2633f68e3c47412fbbe20ab6bc2c49b36700552`, from `pr/goals` in `/home/tyler/data/t/pr-integration`, parent `3a2351b3d3e573a72968e235cb211dc8b2104164`, governance `gov-70f70e75988e` preserved. Unit `not named by the order`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 23bf131de…` → rc=0, HONOURED-XO 23bf131deaec6262c226fa31e3637cd48a91d074 — the last record for this sha (store line 636) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Evidence before landing | `/home/tyler/.local/node/bin/node --test --test-skip-pattern=^every layout item sits inside the hull$ tests/node/run.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/state.test.mjs` rc=0: # duration_ms 2125.863446 |
| Tool | `ship/tools/land.py` sha256 `9a465ba5134e6406…` from `/home/tyler/dev/helm` (informational) |
| Order | `ord-boyce-land-airships-goals-1001` sha256 `9b8e4c5f5f41d239…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md` (created by this landing). |

## Landing 2 — The front door made true: clean-clone checks, a first-party page, the viewer bound to the model, six labelled checks

| field | value |
|---|---|
| Landed | 2026-10-02 00:21:14 PDT by the landing tool (`ship/tools/land.py`) from `boyce`, a pure **FAST-FORWARD**: main `3650c06e45a4ba7c15a682e00bdfea066d754cab` → `e014537f461a90c749d11bb9abcc8d3e193088e6`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `e014537f461a90c749d11bb9abcc8d3e193088e6`, tree `521c0ad671fd7d9184c12b86eb6392b11e0bc66f`, from `pr/batch-a` (source checkout redacted), parent `f610da2f20e4cef5c0add139dc4cfa156e17fe01`, governance `gov-17eaf34e19f2` preserved. Unit `not named by the order`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py e014537f4…` → rc=0, HONOURED-XO e014537f461a90c749d11bb9abcc8d3e193088e6 — the last record for this sha (store line 650) is XO-SIGNED. (store redacted) |
| Evidence before landing | `redacted --test tests/node/run.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/state.test.mjs` rc=0: # duration_ms 4184.134964 |
| Tool | `ship/tools/land.py` sha256 `5aa40860c75cf358…` (informational) |
| Order | sha256 `0099e6e808ac9123…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

