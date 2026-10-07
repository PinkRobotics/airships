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

## Landing 3 — Credit to the crew that does the work, and a first-party note that audits its own page

| field | value |
|---|---|
| Landed | 2026-10-02 01:21:10 PDT by the landing tool (`ship/tools/land.py`) from `boyce`, a pure **FAST-FORWARD**: main `1b7f4a025da2710dc973048cc061c1dbc5d46831` → `d1f917d1bbd716ee9d7e4962ce36c62f070e4aec`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `d1f917d1bbd716ee9d7e4962ce36c62f070e4aec`, tree `75525b545bcad4f96b32e2b078f767edb9cfd42c`, from `pr/batch-a2` (source checkout redacted), parent `d2ac4eebd153814376b424d7d6001e04724d2fe4`, governance `gov-ee99c660dae6` preserved. Unit `not named by the order`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py d1f917d1b…` → rc=0, HONOURED-XO d1f917d1bbd716ee9d7e4962ce36c62f070e4aec — the last record for this sha (store line 653) is XO-SIGNED. (store redacted) |
| Evidence before landing | `redacted --test tests/node/run.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/parity-consumers.test.mjs 3d/tests/spec-required.test.mjs 3d/tests/state.test.mjs` rc=0: # duration_ms 3082.495108 |
| Tool | `ship/tools/land.py` sha256 `5aa40860c75cf358…` (informational) |
| Order | sha256 `f5662f2199f864ba…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 4 — A front door a stranger can check: a generated README, a notice for every file, and a named builder on every change

| field | value |
|---|---|
| Landed | 2026-10-02 04:21:32 PDT by the landing tool (`ship/tools/land.py`) from `boyce`, a pure **FAST-FORWARD**: main `ced40d7b2ad7d9e457783529eb92989500cd5eb8` → `af92cd0f8189fca329a4e96944672b0384959d5f`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `af92cd0f8189fca329a4e96944672b0384959d5f`, tree `0e1c8408cf927faf8d553048391ae4484e617818`, from `pr/batch-r` (source checkout redacted), parent `5f89b3bf1a05decd3c51c80f368c0fa0253e3e8c`, governance `gov-d3e909ae05f6` preserved. Unit `not named by the order`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py af92cd0f8…` → rc=0, HONOURED-XO af92cd0f8189fca329a4e96944672b0384959d5f — the last record for this sha (store line 661) is XO-SIGNED. (store redacted) |
| Evidence before landing | `redacted --test tests/node/run.mjs 3d/tests/builder-line.test.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/parity-consumers.test.mjs 3d/tests/spec-required.test.mjs 3d/tests/state.test.mjs` rc=0: # duration_ms 2217.585471 |
| Tool | `ship/tools/land.py` sha256 `5aa40860c75cf358…` (informational) |
| Order | sha256 `fed617364ba1b56c…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 5 — The 2026 fire season as a record, a guard on where the fleet is simulated, and an invented exercise for the reference scene

| field | value |
|---|---|
| Landed | 2026-10-02 08:33:31 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `d64dedcd75dd9692bde74b14d941f4bf224a3e6f` → `a7d047426d852beaab012184568ea33ea60b438a`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `a7d047426d852beaab012184568ea33ea60b438a`, tree `1370bdb32599a3897e02df56c770c916f2b5e982`, from `pr/batch-b` (source checkout redacted), parent `bad81c650831d56cca8187436fc6b73c8a580e83`, governance `gov-01de49d092fc` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py a7d047426…` → rc=0, HONOURED-XO a7d047426d852beaab012184568ea33ea60b438a — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `node --test tests/node/run.mjs 3d/tests/builder-line.test.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/parity-consumers.test.mjs 3d/tests/spec-required.test.mjs 3d/tests/state.test.mjs` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `c28dd95a406ba105…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 6 — Every statement about floating held to one ledger by a gate, and every view of the monitor named for what it shows

| field | value |
|---|---|
| Landed | 2026-10-02 15:36:34 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `5a03514eecb5c49e48707a4b6271b0d6c8ad79ee` → `bad5dfe0dd56ac149984a836256a53a7ad27e426`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `bad5dfe0dd56ac149984a836256a53a7ad27e426`, tree `ca761ea81ff9df07bb7abe6ece8a21b007bc7ab8`, from `pr/batch-c` (source checkout redacted), parent `9fe8e27e12bc1bfc2073405d5f4f4b8931711d05`, governance `gov-f7d3a60ee98d` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py bad5dfe0d…` → rc=0, HONOURED-XO bad5dfe0dd56ac149984a836256a53a7ad27e426 — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `node --test tests/node/run.mjs 3d/tests/builder-line.test.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/parity-consumers.test.mjs 3d/tests/spec-required.test.mjs 3d/tests/state.test.mjs` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `f5e4b317896f10ae…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 7 — The concept page describes the monitor's views and the limits of its worked example

| field | value |
|---|---|
| Landed | 2026-10-02 17:33:07 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `18f01d6af2179a36c5bb90fe8b87b20a8470d7d1` → `7a97e9b46e61946a8545ac42221825373f63a672`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `7a97e9b46e61946a8545ac42221825373f63a672`, tree `0f834a7129d5aff15562924c08bb79a85befcd1c`, from `pr/concept1` (source checkout redacted), parent `06906b317706438a8c4d261d07f5f75a5a75998f`, governance `gov-eb2867020c93` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 7a97e9b46…` → rc=0, HONOURED-XO 7a97e9b46e61946a8545ac42221825373f63a672 — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `node --test tests/node/run.mjs 3d/tests/builder-line.test.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/parity-consumers.test.mjs 3d/tests/spec-required.test.mjs 3d/tests/state.test.mjs` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `9581690a6da7ab82…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 8 — Every gate serves its own tree on a port the system chose

| field | value |
|---|---|
| Landed | 2026-10-02 19:28:09 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `129bfd7dfcfc35412afcd7faf44caea044bab9a3` → `5e48f2a6c4b7eaf480054518a69f9ee3dd8ff13d`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `5e48f2a6c4b7eaf480054518a69f9ee3dd8ff13d`, tree `2878d979864c88e8a3d1a942c684d2e0c569088c`, from `pr/ports` (source checkout redacted), parent `92b9db5701102a4497a70b32023096c750e1ef51`, governance `gov-f5c2841f1b1c` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 5e48f2a6c…` → rc=0, HONOURED-XO 5e48f2a6c4b7eaf480054518a69f9ee3dd8ff13d — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `node --test tests/node/run.mjs 3d/tests/builder-line.test.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/parity-consumers.test.mjs 3d/tests/spec-required.test.mjs 3d/tests/state.test.mjs` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `f30f1c3111797281…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 9 — Make the README the way in and retire superseded documents

| field | value |
|---|---|
| Landed | 2026-10-02 20:28:31 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `ae7345e421c3b99f9173bb32492d0adbf12618a9` → `1498c4baa7163ec1e30ac0e2365cd42755f45108`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `1498c4baa7163ec1e30ac0e2365cd42755f45108`, tree `22fd47d425980374fae4a4be569dd8509df7b116`, from `pr/present` (source checkout redacted), parent `e2060c33e6edc286e75047097e64845bde06595c`, governance `gov-1d60e855daf8` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 1498c4baa…` → rc=0, HONOURED-XO 1498c4baa7163ec1e30ac0e2365cd42755f45108 — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `node --test tests/node/run.mjs 3d/tests/builder-line.test.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/parity-consumers.test.mjs 3d/tests/spec-required.test.mjs 3d/tests/state.test.mjs` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `d208dde24a75cd4a…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 10 — Read an http.server command as its own parser reads it

| field | value |
|---|---|
| Landed | 2026-10-02 21:54:04 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `2e3264a30ab74deb9d863a4f4f8908b64406ecf7` → `12332d78d890d707435e454b2a8c53e340609540`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `12332d78d890d707435e454b2a8c53e340609540`, tree `d69a4b85ec1093fd44b59d8a70e5b0c466ad05f1`, from `pr/ports3` (source checkout redacted), parent `2e3264a30ab74deb9d863a4f4f8908b64406ecf7`, governance `gov-78f418cb7b45` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 12332d78d…` → rc=0, HONOURED-XO 12332d78d890d707435e454b2a8c53e340609540 — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `node --test tests/node/run.mjs 3d/tests/builder-line.test.mjs 3d/tests/control.test.mjs 3d/tests/model.test.mjs 3d/tests/parity-consumers.test.mjs 3d/tests/spec-required.test.mjs 3d/tests/state.test.mjs` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `8049777bdd40eb85…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 11 — Price every vertical force in the energy model

| field | value |
|---|---|
| Landed | 2026-10-03 08:13:28 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `d9eeb8524e620689250fd5abd36d84db498570cb` → `bd06b800b745ea2ffeeb77ca12807bee10db5128`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `bd06b800b745ea2ffeeb77ca12807bee10db5128`, tree `82a844b19ae3f4684b6cea54a436abfd443a313e`, from `pr/energy1` (source checkout redacted), parent `a9be53929076196e46f2fcb55c59ec98d8af6b82`, governance `gov-c45010e3dcc4` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py bd06b800b…` → rc=0, HONOURED-XO bd06b800b745ea2ffeeb77ca12807bee10db5128 — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `env redacted redacted redacted redacted` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `8cceec42e77bf38d…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 12 — Harden the claim gate against uncued statements

| field | value |
|---|---|
| Landed | 2026-10-03 12:43:38 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `2c5f09fb400bed5223b3aa7fd5c5f6d4ac8bcac1` → `64a6b43b2a53db0634ab5039491ee17b12b56d10`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `64a6b43b2a53db0634ab5039491ee17b12b56d10`, tree `86bd10e647936bf64c98dc6cccfc6ab0bf004b1e`, from `pr/gate` (source checkout redacted), parent `f922c20e3a19892dc8d02175608100f6433c94ea`, governance `gov-2f6ad1d1a282` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 64a6b43b2…` → rc=0, HONOURED-XO 64a6b43b2a53db0634ab5039491ee17b12b56d10 — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `env redacted redacted redacted redacted redacted redacted` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `4b77aae6bc2739cc…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 13 — Print the energy figures on the pages and give the claim plants their own job

| field | value |
|---|---|
| Landed | 2026-10-03 22:37:50 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `e1e70de543eb395306c619296760dab8976c1238` → `95a1d6579a150da35cd93f7c5c64708f43e94b11`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `95a1d6579a150da35cd93f7c5c64708f43e94b11`, tree `70015dbe68b37cc3a5609f6a28fc4c6e290196e5`, from `pr/d2a-g2` (source checkout redacted), parent `61ac88b88d080f1c0c2982834dcb1afcc9b0883b`, governance `gov-51cd931a25e8` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 95a1d6579…` → rc=0, HONOURED-XO 95a1d6579a150da35cd93f7c5c64708f43e94b11 — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `env redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `eb7057e7b91745ec…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 14 — Finish the energy pages and record a full plant pass for every gate change

| field | value |
|---|---|
| Landed | 2026-10-04 03:58:02 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `791bcf42c7bda4cc79db5aea84e61788e950a9fc` → `62d4c3e7c9bb7ba652461917378927b35223f9bb`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `62d4c3e7c9bb7ba652461917378927b35223f9bb`, tree `98a71355b1e259dd98e35bbf208ab2f8a96bd179`, from `pr/d2r` (source checkout redacted), parent `1cb085d24ec5afd17ba6974e5bfe9d59341ac6b1`, governance `gov-d3ced4aef395` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 62d4c3e7c…` → rc=0, HONOURED-XO 62d4c3e7c9bb7ba652461917378927b35223f9bb — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `env redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted` rc=0 |
| Tool | `ship/tools/land.py` sha256 `d4ad25b6e0d27bd0…` (informational) |
| Order | sha256 `9ea81062a1aeaabe…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 15 — Correct the served force figures and show the scope of feasibility

| field | value |
|---|---|
| Landed | 2026-10-04 07:43:58 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `efdb8a65c42c3b7e4f52a13ee7571e7e983f359a` → `9ae3542450571b35ba9b41a331c30835a12f5712`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `9ae3542450571b35ba9b41a331c30835a12f5712`, tree `67c6145050f3f1bb9afee58b62ec6e8a7fafde07`, from `pr/c15` (source checkout redacted), parent `c8a4e6d9778332eb37b09105e2f49350944bd430`, governance `gov-37769eb94c60` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 9ae354245…` → rc=0, HONOURED-XO 9ae3542450571b35ba9b41a331c30835a12f5712 — the last record for this sha is XO-SIGNED. (store redacted) |
| Evidence before landing | `env redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted redacted` rc=0 (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `c0d17fe009ac84c3…` (informational) |
| Order | sha256 `35c721ad5dbd1f70…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 16 — License the content, drop the link-only papers, extend the claims register

| field | value |
|---|---|
| Landed | 2026-10-04 21:02:00 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `c10d2c3194ae01a7943f9caec49e1633bb8917d2` → `30c6f4497073cea16c9f088bff093e02e0fe889d`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `30c6f4497073cea16c9f088bff093e02e0fe889d`, tree `7301a47fc312711112ead2659e86e47eb50e898f`, from `pr/c16` in `/home/tyler/data/t/pr-c16`, parent `7083ed68a5dd7f046da9bc69e9b27b32b909f699`, governance `gov-58411c1d7d58` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 30c6f4497…` → rc=0, HONOURED-XO 30c6f4497073cea16c9f088bff093e02e0fe889d — the last record for this sha (store line 820) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/home/tyler/data/pinkrobotics/tmp/boyce-land-c16-1004 FLOAT_PLANT_WORKERS=8 make ciparity energycheck energydoccheck servedenergycheck figfresh ledgercheck floatplantcheck floatpagecheck floatverdictcheck noticecheck linkcheck` rc=0 (gate timeout 1800 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `89ccda35b01beef0…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `a531bd08424374ba…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 17 — Make CI reproducible on a clean runner, plants in four shares

| field | value |
|---|---|
| Landed | 2026-10-05 10:12:18 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `5cbc5ffc1f30db9729e1a15d1400e2ee0d9bb178` → `2f80e10e1499c0977898ebba6bed9c074159fa8b`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `2f80e10e1499c0977898ebba6bed9c074159fa8b`, tree `d807148dea1839e8cfeeb0dbe4ff449b1fb94a8f`, from `pr/c17` in `/home/tyler/data/t/pr-c17`, parent `c1ab101ae74e97df94aa406127d8d0546170a2fa`, governance `gov-02ac5ac690ec` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 2f80e10e1…` → rc=0, HONOURED-XO 2f80e10e1499c0977898ebba6bed9c074159fa8b — the last record for this sha (store line 871) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Governance records | `b7745f232` ← `gov-ee021b1c85d5` (its trailer); `70798cbaf` ← `gov-64f585dadd65` (its trailer); `5b77d1ffc` ← `gov-1cd5b15972b2` (its trailer); `f41dc9009` ← `gov-d30a1cd4b36f` (its trailer); `ad36c9529` ← `gov-11d5f2821341` (its trailer); `acad2e248` ← `gov-ef47142b81d2` (its trailer); `c1ab101ae` ← `gov-fee274833272` (its trailer); `2f80e10e1` ← `gov-02ac5ac690ec` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/home/tyler/data/pinkrobotics/tmp/boyce-land-c17-1005 FLOAT_PLANT_WORKERS=8 make ciparity energycheck energydoccheck servedenergycheck figfresh ledgercheck floatplantcheck floatpagecheck floatverdictcheck noticecheck linkcheck` rc=0 (gate timeout 1800 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `7ad33759f7af8e0b…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `6cff4644559464ee…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 18 — Sign rotor authority, state stored-energy limits, fix the CI browser probe

| field | value |
|---|---|
| Landed | 2026-10-05 14:06:08 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `0ab9b54b70693f71d556ad66a26e9e30ae9fc89e` → `74651d8ac085ebc4fb343f5eac8acc18649674d9`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `74651d8ac085ebc4fb343f5eac8acc18649674d9`, tree `f3c0c3ded1fa82d2a2f012a97010f86cedcfed55`, from `pr/c18` in `/home/tyler/data/t/pr-c18`, parent `ba0685d0886ce4c005351b31c3ea2e5576f6091b`, governance `gov-ba06d2a84a35` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 74651d8ac…` → rc=0, HONOURED-XO 74651d8ac085ebc4fb343f5eac8acc18649674d9 — the last record for this sha (store line 879) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Governance records | `b73c37775` ← `gov-452836efdc08` (its trailer); `5680cb029` ← `gov-8243541d5d37` (its trailer); `4a26876eb` ← `gov-91ef1cca5c45` (its trailer); `3551fe3eb` ← `gov-74921fb96725` (its trailer); `ba0685d08` ← `gov-eeed694a4b23` (its trailer); `74651d8ac` ← `gov-ba06d2a84a35` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/home/tyler/data/pinkrobotics/tmp/boyce-land-c18-1005 FLOAT_PLANT_WORKERS=8 make ciparity energycheck energydoccheck servedenergycheck figfresh ledgercheck floatplantcheck floatpagecheck floatverdictcheck noticecheck linkcheck cellparity explorercheck levelscheck shipcheck bandcheck` rc=0 (gate timeout 1800 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `7ad33759f7af8e0b…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `002024645bfd3a30…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 19 — Complete the hull closure and answer objections 038 to 043

| field | value |
|---|---|
| Landed | 2026-10-06 02:48:42 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `a3eb3cbad74d75cdf62e2136e05ce4ec2a2a29bf` → `462a6747d73fcede0528ef6a6897f35eb13099ca`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `462a6747d73fcede0528ef6a6897f35eb13099ca`, tree `460eb8f57cdc28860069744a0b58f028cd5b5639`, from `pr/c19c` in `/home/tyler/data/t/pr-c19c`, parent `fad53e21024bf8f1366f132a4a86163037bc0bca`, governance `gov-870f5de02833` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 462a6747d…` → rc=0, HONOURED-XO 462a6747d73fcede0528ef6a6897f35eb13099ca — the last record for this sha (store line 904) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Governance records | `c81d2059b` ← `gov-0dfe5396333b` (its trailer); `93439d593` ← `gov-40bf6155916d` (its trailer); `7d80c814b` ← `gov-027f1e7b47fd` (its trailer); `4400b1b05` ← `gov-bb84dba5153d` (its trailer); `0ca6489ee` ← `gov-40e5d362cb70` (its trailer); `02f1142ae` ← `gov-7c908f3955f2` (its trailer); `c88e6071e` ← `gov-a3322be50598` (its trailer); `2d2a41240` ← `gov-205299bac3ce` (its trailer); `f532d05cf` ← `gov-bf7d2ad73bbf` (its trailer); `d226762c3` ← `gov-c0b89ef7b9cd` (its trailer); `60749fee9` ← `gov-d3c9600f49c2` (its trailer); `46e0dcdb3` ← `gov-c77001810265` (its trailer); `9bc6ee87a` ← `gov-e2b5fde0bb90` (its trailer); `15044fa13` ← `gov-68d3bc521344` (its trailer); `b7d423724` ← `gov-8ab2df3dd07d` (its trailer); `fad53e210` ← `gov-7aecd600837d` (its trailer); `462a6747d` ← `gov-870f5de02833` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/home/tyler/data/pinkrobotics/tmp/boyce-land-c19c-1006 FLOAT_PLANT_WORKERS=8 make ciparity energycheck energydoccheck servedenergycheck figfresh ledgercheck floatplantcheck floatpagecheck floatverdictcheck noticecheck linkcheck cellparity explorercheck levelscheck shipcheck bandcheck` rc=0 (gate timeout 1800 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `7ad33759f7af8e0b…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `a97f0760c85cc1e7…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 20 — Settle nineteen objections by runs

| field | value |
|---|---|
| Landed | 2026-10-06 09:30:15 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `6b1f60e4f0296936764983829bf4de02c544aaa6` → `e5346d166a7f5b9dbe9a7454d76234041e0a70d6`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `e5346d166a7f5b9dbe9a7454d76234041e0a70d6`, tree `aebe429053a4770423a3094998b0f58e22cfb74b`, from `pr/c21` in `/home/tyler/data/t/pr-c21`, parent `f1340f87196864667c14a3ae81c4f50be0cface5`, governance `gov-5b0805eb8844` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py e5346d166…` → rc=0, HONOURED-XO e5346d166a7f5b9dbe9a7454d76234041e0a70d6 — the last record for this sha (store line 916) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Governance records | `f2cec7286` ← `gov-55c914c8801b` (its trailer); `2f9e852a9` ← `gov-d1abfb338a3e` (its trailer); `86838b108` ← `gov-1f3385a949fc` (its trailer); `53b6abfa5` ← `gov-25c0302f02b7` (its trailer); `247926b5e` ← `gov-dcc7f2c113e6` (its trailer); `67cc26c4c` ← `gov-2b6f202c19fd` (its trailer); `7ed4c2a9a` ← `gov-5b27890dbc23` (its trailer); `0a10d4f5c` ← `gov-21429201ca7c` (its trailer); `1303d7a38` ← `gov-81654f8f5f93` (its trailer); `e543e13b5` ← `gov-dc5dc20f3f48` (its trailer); `ad587aa54` ← `gov-636734ba50eb` (its trailer); `4d6bc6985` ← `gov-294345b15e91` (its trailer); `fe6750203` ← `gov-45c26e56561f` (its trailer); `ffca1be95` ← `gov-07b05453a18e` (its trailer); `9bc913c40` ← `gov-6c68dce1c7e7` (its trailer); `347403e8e` ← `gov-638c68ce2d56` (its trailer); `eb38d9a11` ← `gov-4148f7f63e12` (its trailer); `42f260658` ← `gov-f1709eaa123b` (its trailer); `e3a90ae88` ← `gov-ff2d7a7992df` (its trailer); `b946c8fd3` ← `gov-f4f81dfbe990` (its trailer); `3fc7e01c0` ← `gov-ae7abc63a78b` (its trailer); `f1340f871` ← `gov-c5b55bb53bf6` (its trailer); `e5346d166` ← `gov-5b0805eb8844` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/home/tyler/data/pinkrobotics/tmp/boyce-land-c21-1006 FLOAT_PLANT_WORKERS=8 make ciparity energycheck energydoccheck servedenergycheck figfresh ledgercheck floatplantcheck floatpagecheck floatverdictcheck noticecheck linkcheck cellparity explorercheck levelscheck shipcheck bandcheck` rc=0 (gate timeout 1800 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `7ad33759f7af8e0b…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `9be9c9ca91788fd8…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 21 — Settle nineteen more objections by runs; print fleet distances

| field | value |
|---|---|
| Landed | 2026-10-07 02:09:56 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `0a81bb37821bb1d3badc66440affbbe9ac2d87ae` → `531d677d422744fffd860a770114e8d248e6a4aa`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `531d677d422744fffd860a770114e8d248e6a4aa`, tree `fbbcde8afa4c55e369b60c1ba4934660ef0f5f23`, from `pr/c22` in `/home/tyler/data/t/pr-c22`, parent `daf5a654dcf3b919e71da6021dce93017aae42b6`, governance `gov-62a59d89b22a` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 531d677d4…` → rc=0, HONOURED-XO 531d677d422744fffd860a770114e8d248e6a4aa — the last record for this sha (store line 936) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Governance records | `5dbe4d67f` ← `gov-a27efcc48486` (its trailer); `a42d76431` ← `gov-1c0342e1ab02` (its trailer); `17c3b7ac2` ← `gov-c8830189664d` (its trailer); `fc6295e33` ← `gov-68dc19b25cbf` (its trailer); `308dd1618` ← `gov-5b68122697e2` (its trailer); `603eb3f28` ← `gov-c68a211fc366` (its trailer); `25cd87a47` ← `gov-29de2207e9ac` (its trailer); `71db2f2aa` ← `gov-6cd9800a41be` (its trailer); `fcddf884f` ← `gov-4c71cb991bf5` (its trailer); `24b1d9e04` ← `gov-2f1b7a4c9348` (its trailer); `b999c3882` ← `gov-994c55720d5e` (its trailer); `5f34f9111` ← `gov-5d28f287f2ae` (its trailer); `247fe4b0e` ← `gov-3b2d80e228e8` (its trailer); `fde55e619` ← `gov-3b327e0470c4` (its trailer); `71637a17e` ← `gov-24a14f2516ac` (its trailer); `8e9327d6b` ← `gov-4991d70c2c6a` (its trailer); `a1cf61b78` ← `gov-51ba286dd68c` (its trailer); `01330a63c` ← `gov-5f750997d049` (its trailer); `017d72a17` ← `gov-4ec7353a0be5` (its trailer); `34c1e61e2` ← `gov-abdf6144fb55` (its trailer); `907429b52` ← `gov-974d774cebad` (its trailer); `3bfb90fd3` ← `gov-29a65e590e1c` (its trailer); `19a025003` ← `gov-a6305917ae92` (its trailer); `c5e8e34e9` ← `gov-471ab3ee2299` (its trailer); `bd74b4edd` ← `gov-155afd2b7bf8` (its trailer); `d20c1eab4` ← `gov-13d5a6cc67f9` (its trailer); `d089bbf7f` ← `gov-a369e730fade` (its trailer); `daf5a654d` ← `gov-413b351be257` (its trailer); `531d677d4` ← `gov-62a59d89b22a` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/home/tyler/data/pinkrobotics/tmp/boyce-land-c22-1007 FLOAT_PLANT_WORKERS=8 make ciparity energycheck energydoccheck servedenergycheck figfresh ledgercheck floatplantcheck floatpagecheck floatverdictcheck noticecheck linkcheck cellparity explorercheck levelscheck shipcheck bandcheck` rc=0 (gate timeout 1800 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `7ad33759f7af8e0b…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `ab8046114da1ad29…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

