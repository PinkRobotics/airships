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

## Landing 22 — Settle fifteen weather, rotor and plant objections; size-gate the records

| field | value |
|---|---|
| Landed | 2026-10-07 22:45:47 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `49d0533267c550bfd6c5d223b7551cc188d5d194` → `9ce0a4a64608c28d841d835b546c226bec2a02e8`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `9ce0a4a64608c28d841d835b546c226bec2a02e8`, tree `8260a53ff0b37219026f8962dc62c226c9449e72`, from `pr/c23-fix` in `/home/tyler/data/t/pr-c23-fix`, parent `ea1c070c17539151c262bafbeb894b5bc5815339`, governance `gov-9af317e022b7` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 9ce0a4a64…` → rc=0, HONOURED-XO 9ce0a4a64608c28d841d835b546c226bec2a02e8 — the last record for this sha (store line 966) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Governance records | `b29a097ea` ← `gov-332a4dad1080` (its trailer); `2577d9090` ← `gov-fb3a91422a40` (its trailer); `aa4d435b3` ← `gov-b490caf42a81` (its trailer); `18ed76e76` ← `gov-8c3c88435a69` (its trailer); `a3117b787` ← `gov-a5be0cb37f85` (its trailer); `38644dca7` ← `gov-73686b1480d1` (its trailer); `43b67a28d` ← `gov-53f4fb2918a5` (its trailer); `e6d5c9512` ← `gov-dff2fb580239` (its trailer); `c96922230` ← `gov-139df751545d` (its trailer); `2552b30f0` ← `gov-e70a700ef701` (its trailer); `d33618966` ← `gov-6367ae8df262` (its trailer); `3df74368b` ← `gov-52c88b5f543c` (its trailer); `297e4ede1` ← `gov-91fd0aa32c14` (its trailer); `05a7f1b87` ← `gov-e2f91e5b02ee` (its trailer); `f50f1889e` ← `gov-58c7af82dbf1` (its trailer); `fa55b6e94` ← `gov-890a8f782e3d` (its trailer); `e80a54f15` ← `gov-05a407dff2d2` (its trailer); `d3f2b971a` ← `gov-052df487806c` (its trailer); `e1ebaf747` ← `gov-1fbce84d24f2` (its trailer); `aa4c27f6e` ← `gov-1eeac691eabb` (its trailer); `1a54d0ad4` ← `gov-e6fcba1a0407` (its trailer); `3caa03e53` ← `gov-6f1c560ebc5b` (its trailer); `a116b1e42` ← `gov-709ac1571cf9` (its trailer); `27271c07a` ← `gov-8ad9d54ffaf7` (its trailer); `4f73091f1` ← `gov-db8d81071f9a` (its trailer); `945c57871` ← `gov-5b056587db88` (its trailer); `3628fec5b` ← `gov-7f5c9614e91c` (its trailer); `2747636f6` ← `gov-8f84aa5e955e` (its trailer); `17926686e` ← `gov-a00e9fd6ee1b` (its trailer); `94d544048` ← `gov-a8ecc24219b1` (its trailer); `268feaf32` ← `gov-6d2d8507d8c3` (its trailer); `ea1c070c1` ← `gov-af908465422a` (its trailer); `9ce0a4a64` ← `gov-9af317e022b7` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/home/tyler/data/pinkrobotics/tmp/boyce-land-c23-1007 FLOAT_PLANT_WORKERS=8 make ciparity energycheck energydoccheck servedenergycheck figfresh ledgercheck floatplantcheck floatpagecheck floatverdictcheck noticecheck linkcheck cellparity explorercheck levelscheck shipcheck bandcheck` rc=0 (gate timeout 1800 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `7ad33759f7af8e0b…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `2cc053b1a32b2461…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 23 — Wait for page readiness before sampling generated regions

| field | value |
|---|---|
| Landed | 2026-10-08 02:24:10 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `097d5a608346182f2a7b87ed5880d28af6ce8b0d` → `8c65db4b52dd4e8f9e944ad3bb4d9212ad968be1`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `8c65db4b52dd4e8f9e944ad3bb4d9212ad968be1`, tree `6f7d7d183740d7df27836278add975bcf2d9b8c3`, from `pr/c24-small` in `/home/tyler/data/t/pr-c24-small`, parent `097d5a608346182f2a7b87ed5880d28af6ce8b0d`, governance `gov-713d04764c7b` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 8c65db4b5…` → rc=0, HONOURED-XO 8c65db4b52dd4e8f9e944ad3bb4d9212ad968be1 — the last record for this sha (store line 971) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Governance records | `8c65db4b5` ← `gov-713d04764c7b` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/home/tyler/data/pinkrobotics/tmp/boyce-land-c24small-1008 FLOAT_PLANT_WORKERS=8 make ciparity energycheck energydoccheck servedenergycheck figfresh ledgercheck floatplantcheck floatpagecheck floatverdictcheck noticecheck linkcheck cellparity explorercheck levelscheck shipcheck bandcheck` rc=0 (gate timeout 1800 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `7ad33759f7af8e0b…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `586504b472ccbb91…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 24 — Wait for settled fleet planning before reading wind readiness

| field | value |
|---|---|
| Landed | 2026-10-08 08:48:16 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `1e14170cb3c495adf4ae052e35d72535b440ae63` → `ce805de46653924764112051c87e871064729be2`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `ce805de46653924764112051c87e871064729be2`, tree `9662f3b8beb16431557385c048576bc373e76dc2`, from `pr/c25-waits` in `/home/tyler/data/t/pr-c25-waits`, parent `f970bb389a61c20693630861796ce7e9976b877e`, governance `gov-5e847ce86004` preserved. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py ce805de46…` → rc=0, HONOURED-XO ce805de46653924764112051c87e871064729be2 — the last record for this sha (store line 981) is XO-SIGNED. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Governance records | `f970bb389` ← `gov-9e8ef4440a3c` (its trailer); `ce805de46` ← `gov-5e847ce86004` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/home/tyler/data/pinkrobotics/tmp/boyce-land-c25-1008 FLOAT_PLANT_WORKERS=8 make ciparity energycheck energydoccheck servedenergycheck figfresh ledgercheck floatplantcheck floatpagecheck floatverdictcheck noticecheck linkcheck cellparity explorercheck levelscheck shipcheck bandcheck` rc=0 (gate timeout 1800 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `7ad33759f7af8e0b…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `86d776ffaf29dda4…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 25 — Restore claims records on demand from pinned history

| field | value |
|---|---|
| Landed | 2026-10-09 22:11:58 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `6278355e27f47865fbdb615c94c3638096eee6a7` → `33979de2982edba6cc06d76f56ebcb5948670a64`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `33979de2982edba6cc06d76f56ebcb5948670a64`, tree `07449bce9145093731e940976fc2334756a16ca4`, from `worker/claims-cleanup-1009` in `/home/tyler/data/helm/ship-workspaces/worker-robotics-recovery-pilots-1009/.ship/code/airships-cleanup-1009`, parent `6278355e27f47865fbdb615c94c3638096eee6a7`, governance `gov-7bc3e353b6a3` preserved. Unit `robotics-charter-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 33979de29…` → rc=0, HONOURED 33979de2982edba6cc06d76f56ebcb5948670a64 — the last record for this sha (store line 1054) is PASS. (store `/home/tyler/data/helm/tmp/fo-verdicts.tsv`) |
| Governance records | `33979de29` ← `gov-7bc3e353b6a3` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `/usr/bin/env PATH=/home/tyler/.local/node/bin:/snap/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/mnt/scratch PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck` rc=0 (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `7ad33759f7af8e0b…` from `/home/tyler/dev/helm` (informational) |
| Order | sha256 `fe81a21026e39896…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 26 — Newcomer documentation and a neutral programme plan on the public owner

| field | value |
|---|---|
| Landed | 2026-10-09 22:53:49 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `363740b90700f288313c96090b6287f740a25dca` → `a0e5ad639b9b3d67befcbe8a74f20ef9e1a23c8c`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `a0e5ad639b9b3d67befcbe8a74f20ef9e1a23c8c`, tree `ee6875b6a8bdb88bde50adda5489a2b67a222f09`, from branch `worker/neutral-public-owner-fixed-1009`, parent `363740b90700f288313c96090b6287f740a25dca`, governance `gov-7c3bc49bbcd6` preserved. Unit `robotics-public-face-science-docs-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py a0e5ad639…` → rc=0, HONOURED-XO a0e5ad639b9b3d67befcbe8a74f20ef9e1a23c8c — the last record for this sha (store line 1061) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `a0e5ad639` ← `gov-7c3bc49bbcd6` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `make readmecheck linkcheck buildercheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 180 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `d74e14c13dcf0e27…` from helm (informational) |
| Order | sha256 `959e358e921f002c…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 27 — Exclude citation metadata from the site build and bind the README claims records to their lines

| field | value |
|---|---|
| Landed | 2026-10-10 00:01:10 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `ae244c455512ffe8d7383315e49ea66597dd7b39` → `2e8bb831195afcda0a0a8268bb9a25f9e2b041b8`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `2e8bb831195afcda0a0a8268bb9a25f9e2b041b8`, tree `67ae57b2c426c8c2a26673a3f6c8a0cc07d7b24a`, from branch `worker/citation-rootclaims-neutral-first-1009`, parent `2275403acfc586c0c367c47cd5f2fff9c695d480`, governance `gov-658200c5c140` preserved. Unit `robotics-citation-manifest-first-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 2e8bb8311…` → rc=0, HONOURED-XO 2e8bb831195afcda0a0a8268bb9a25f9e2b041b8 — the last record for this sha (store line 1073) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `2275403ac` ← `gov-e6f1dd18d082` (its trailer); `2e8bb8311` ← `gov-658200c5c140` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `d74e14c13dcf0e27…` from helm (informational) |
| Order | sha256 `dd37b8d65f98e7ae…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 28 — Record exact programme and navigation dispositions for public float plants

| field | value |
|---|---|
| Landed | 2026-10-10 01:07:32 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `7f31c959126d90e5a8f965b897f9f8ee9fc30ed7` → `a628457a14709e5a0a1c8fe33f5c69487c3e33cc`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `a628457a14709e5a0a1c8fe33f5c69487c3e33cc`, tree `5ee5c13ee29aca5f7e9f53975f64366a1cf1ae3f`, from branch `worker/public-floatplants-four-dispositions-1010`, parent `7f31c959126d90e5a8f965b897f9f8ee9fc30ed7`, governance `gov-8f8a80d109c9` preserved. Unit `robotics-public-ci-floatplants-1010`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py a628457a1…` → rc=0, HONOURED-XO a628457a14709e5a0a1c8fe33f5c69487c3e33cc — the last record for this sha (store line 1085) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `a628457a1` ← `gov-8f8a80d109c9` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `d74e14c13dcf0e27…` from helm (informational) |
| Order | sha256 `e06942b85c867ef3…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 29 — Record accepted site cleanup and truthful research preparation

| field | value |
|---|---|
| Landed | 2026-10-10 04:48:33 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `637edff72908ff85d79b357870d7cc9cbb4eb1be` → `91173d0e303dc84583ef9a516995c071ded21c33`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `91173d0e303dc84583ef9a516995c071ded21c33`, tree `772af5e3e1f46a7da69ed9c1fa3dce2fee1c97c6`, from branch `worker/cleanup-cf335-actual637-final-1010`, parent `637edff72908ff85d79b357870d7cc9cbb4eb1be`, governance `gov-eee9138e2490` preserved. Unit `robotics-cleanup-site-readme-seed-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 91173d0e3…` → rc=0, HONOURED-XO 91173d0e303dc84583ef9a516995c071ded21c33 — the last record for this sha (store line 1091) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `91173d0e3` ← `gov-eee9138e2490` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `66eb26098b618a97…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 30 — Link the numbered question register to existing physics issues

| field | value |
|---|---|
| Landed | 2026-10-10 05:10:37 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `c289878f515243e977a065c773e466aa04346ed0` → `deca118736d068b845321ab03f6c55e61be82f8b`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `deca118736d068b845321ab03f6c55e61be82f8b`, tree `f276cfead13c6375247346fd442948ddfc9b4e0d`, from branch `worker/questions-links-actualc289-final-1010`, parent `c289878f515243e977a065c773e466aa04346ed0`, governance `gov-6c212cf33b0c` preserved. Unit `robotics-public-face-science-docs-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py deca11873…` → rc=0, HONOURED-XO deca118736d068b845321ab03f6c55e61be82f8b — the last record for this sha (store line 1092) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `deca11873` ← `gov-6c212cf33b0c` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `7e273245e2afc65c…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 31 — Record monitor binding repair with its bounded synthetic scope

| field | value |
|---|---|
| Landed | 2026-10-10 05:27:15 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `a61b246dacbcb3165384f317667ed889cede5cdd` → `239f8568e55e419fe448ecfccb66149b972f0e92`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `239f8568e55e419fe448ecfccb66149b972f0e92`, tree `4d740fed39af169692b2931a6db6ab6e23370269`, from branch `worker/monitor5cff-actuala61-final-1010`, parent `a61b246dacbcb3165384f317667ed889cede5cdd`, governance `gov-e3d464532c46` preserved. Unit `robotics-p2-monitor-wiring-repair-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 239f8568e…` → rc=0, HONOURED-XO 239f8568e55e419fe448ecfccb66149b972f0e92 — the last record for this sha (store line 1093) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `239f8568e` ← `gov-e3d464532c46` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `d29e0cbc11c7dedd…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 32 — Record neutral NACA0012 preparation on current main

| field | value |
|---|---|
| Landed | 2026-10-10 05:44:27 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `c0430d2805dacb80db5343c0e5b67c4943b9868e` → `9ae3d22d01a629f6c7aa85eaf17867f0be58bdde`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `9ae3d22d01a629f6c7aa85eaf17867f0be58bdde`, tree `625f002bfdf83257f7d822c4d86762f8e9320e03`, from branch `worker/naca0012-neutral-slot4-1010`, parent `c0430d2805dacb80db5343c0e5b67c4943b9868e`, governance `gov-00a1514d8972` preserved. Unit `robotics-charter-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 9ae3d22d0…` → rc=0, HONOURED-XO 9ae3d22d01a629f6c7aa85eaf17867f0be58bdde — the last record for this sha (store line 1094) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `9ae3d22d0` ← `gov-00a1514d8972` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `f32b61f7f6dfb2d3…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 33 — Record conditional P4.5 stipulated stiffness assumptions

| field | value |
|---|---|
| Landed | 2026-10-10 06:00:49 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `37e9104748ddab630f66ba8f87ea78e0567278cd` → `25e5bee382555c068f927525b56e0b74352cf95e`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `25e5bee382555c068f927525b56e0b74352cf95e`, tree `063685741204c5eecf9c85cc5d6688854d36d702`, from branch `worker/p45-cut-content-slot5-1010`, parent `37e9104748ddab630f66ba8f87ea78e0567278cd`, governance `gov-96453759481f` preserved. Unit `robotics-charter-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 25e5bee38…` → rc=0, HONOURED-XO 25e5bee382555c068f927525b56e0b74352cf95e — the last record for this sha (store line 1095) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `25e5bee38` ← `gov-96453759481f` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `0c5a204662ea4375…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 34 — Add reviewed public-face record with dated mirror history

| field | value |
|---|---|
| Landed | 2026-10-10 06:19:05 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `df13ab897260bf22afa5b1df374866321d8b1858` → `493066da962b7ec9e59d03b02dd27179ce43d61b`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `493066da962b7ec9e59d03b02dd27179ce43d61b`, tree `eef407b864141e2567dded3aa58247c296b51bb4`, from branch `public-face-science-actual33-minimal-1010`, parent `df13ab897260bf22afa5b1df374866321d8b1858`, governance `gov-f5bd2d849529` preserved. Unit `robotics-charter-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 493066da9…` → rc=0, HONOURED-XO 493066da962b7ec9e59d03b02dd27179ce43d61b — the last record for this sha (store line 1096) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `493066da9` ← `gov-f5bd2d849529` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `a28949a7e4f9019a…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 35 — Record the assumed port paper with unavailable source outcomes withheld

| field | value |
|---|---|
| Landed | 2026-10-10 06:40:16 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `0afdc897925f4806b34c0e1fb788ada2eaa30001` → `4828400ba341516b513037121992047b81944a68`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `4828400ba341516b513037121992047b81944a68`, tree `586d8ab5a3fc1e7823516e4927464ef4db80c92f`, from branch `worker/p16-public-cut-actual0afdc897-final-1010`, parent `0afdc897925f4806b34c0e1fb788ada2eaa30001`, governance `gov-268500a6e32c` preserved. Unit `robotics-charter-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 4828400ba…` → rc=0, HONOURED-XO 4828400ba341516b513037121992047b81944a68 — the last record for this sha (store line 1097) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `4828400ba` ← `gov-268500a6e32c` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `c4dbfd8eaa86aff9…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 36 — Repair float disposition locations and landing-series metadata

| field | value |
|---|---|
| Landed | 2026-10-10 08:03:08 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `5f752f5398bb2fa37cae4e196b8d2552e8d94623` → `98ebe919f93153fabe8f780047fb4b6d7f75fcfc`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `98ebe919f93153fabe8f780047fb4b6d7f75fcfc`, tree `46c60d9fcadfdbaf5d9931a198c135f8c70dc687`, from branch `worker/ledgercheck-nine-records-1010`, parent `5f752f5398bb2fa37cae4e196b8d2552e8d94623`, governance `gov-c198452db366` preserved. Unit `robotics-charter-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 98ebe919f…` → rc=0, HONOURED-XO 98ebe919f93153fabe8f780047fb4b6d7f75fcfc — the last record for this sha (store line 1098) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `98ebe919f` ← `gov-c198452db366` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `6c1d1a26f36b8ba9…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 37 — Map assumed port inputs to prospective measurement evidence

| field | value |
|---|---|
| Landed | 2026-10-10 08:57:47 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `2628bdddcd69f5e0b5e9d0e0eac7e2c22b33b797` → `01ccfe284d43232bdb6c1b65668ec326f2e3ae00`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `01ccfe284d43232bdb6c1b65668ec326f2e3ae00`, tree `eac87f222e61fd9a12b66708b159c2e7efa5203b`, from branch `worker/p16-measurement-crosswalk-1010`, parent `2628bdddcd69f5e0b5e9d0e0eac7e2c22b33b797`, governance `gov-250f43d2b83f` preserved. Unit `robotics-p16-measurement-crosswalk-1010`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 01ccfe284…` → rc=0, HONOURED-XO 01ccfe284d43232bdb6c1b65668ec326f2e3ae00 — the last record for this sha (store line 1100) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `01ccfe284` ← `gov-250f43d2b83f` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `dd148ab32dc7651d…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 38 — Twelve research papers, with the confidence key renamed so evaccheck passes

| field | value |
|---|---|
| Landed | 2026-10-10 13:31:56 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `94db332d3dc437708d3ed0dfeb6b619c70d9da25` → `faa02d718cc69f5c70b1807f3357db8ca71a6f4f`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `faa02d718cc69f5c70b1807f3357db8ca71a6f4f`, tree `d92075577f613599920fac4b43e27cd370d5892b`, from branch `worker/ci-evac-fix-1010`, parent `2ca19e37af261dd84063a650a7aebc6530f4a238`, governance `gov-58c220b7a83d` preserved. Unit `robotics-airships-ci-red-evac-1010`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py faa02d718…` → rc=0, HONOURED-XO faa02d718cc69f5c70b1807f3357db8ca71a6f4f — the last record for this sha (store line 1159) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `1f2a2f0c6` ← `gov-a919aea5842e` (its trailer); `e5618cf8a` ← `gov-4a0fe1c575e3` (its trailer); `b6a4c60b6` ← `gov-a79b4f32638e` (its trailer); `55dce5ffa` ← `gov-ba01a5af87d1` (its trailer); `191bd2da2` ← `gov-64a7703f4566` (its trailer); `7bf95ee75` ← `gov-6c18cf1b05d5` (its trailer); `d392a778b` ← `gov-b1ebc9bcbc26` (its trailer); `ca3fa99a2` ← `gov-c4f20766d6f0` (its trailer); `6c19a96d8` ← `gov-388276e71c98` (its trailer); `c84f9134b` ← `gov-e05e5f416036` (its trailer); `707a7c9ad` ← `gov-4b2d2505547c` (its trailer); `73ef64a13` ← `gov-5847caa4498d` (its trailer); `2d4309c71` ← `gov-d725f088d22b` (its trailer); `e905fef9a` ← `gov-2c9e0cadd6ba` (its trailer); `7ab8a26b7` ← `gov-600a7c97126e` (its trailer); `2ca19e37a` ← `gov-67a74de27dc8` (its trailer); `faa02d718` ← `gov-58c220b7a83d` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `275d42ae3f736387…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 39 — Six evidence pieces: Q15, Q4, Q10, Q13, Q18 and Q3

| field | value |
|---|---|
| Landed | 2026-10-10 16:36:29 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `682c4b375f7d67484891df7a551d0da03cedcf11` → `24336c4673df10957b110ee822bdda7e8acb00d5`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `24336c4673df10957b110ee822bdda7e8acb00d5`, tree `956c4e53098f544e479e0cf45403e9366a049c77`, from branch `worker/nextstack-accepted38-1010`, parent `258b7442840d17213500d36993cb439dc6379ee6`, governance `gov-e8c179b6eb1c` preserved. Unit `robotics-airships-next-stack-six-1010`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 24336c467…` → rc=0, HONOURED-XO 24336c4673df10957b110ee822bdda7e8acb00d5 — the last record for this sha (store line 1193) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `111e55095` ← `gov-3df558384f65` (its trailer); `861d39d7f` ← `gov-2dc7cf864b8e` (its trailer); `cfab410ac` ← `gov-0f47cd813f7b` (its trailer); `66147f62e` ← `gov-5b2efca57fdf` (its trailer); `ebe82e879` ← `gov-9e109eafe89e` (its trailer); `258b74428` ← `gov-6d17c7fac23f` (its trailer); `24336c467` ← `gov-e8c179b6eb1c` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `c65ce5feaac6888f…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 40 — Singles stack: 72 XO-SIGNED pieces in 94 patch-identical commits

| field | value |
|---|---|
| Landed | 2026-10-10 20:00:49 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `9482358277442f85adb764d73cb83cc48a3642d9` → `3804861ec9a731ad7849afa185d58a6624fef1ec`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `3804861ec9a731ad7849afa185d58a6624fef1ec`, tree `34fc13ae793725dd434ac45973a5b22cd4d751cb`, from branch `worker/singles-stack-1010`, parent `e0813f54b985920c17fc444d84706353169f6402`, governance `gov-41479e55c505` preserved. Unit `robotics-airships-singles-stack-1010`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 3804861ec…` → rc=0, HONOURED-XO 3804861ec9a731ad7849afa185d58a6624fef1ec — the last record for this sha (store line 1249) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `15cae8bb6` ← `gov-9ad2aefcae44` (its trailer); `af1921c38` ← `gov-fa1eb8f35044` (its trailer); `6741d40ff` ← `gov-e07861c2f28f` (its trailer); `57499ff95` ← `gov-d5bc54fe1159` (its trailer); `7ca6f7c3b` ← `gov-50afe3f3d765` (its trailer); `825091fa4` ← `gov-2764fb39ee78` (its trailer); `73c508392` ← `gov-5b53e58d8246` (its trailer); `1594a412a` ← `gov-c2e652502ae3` (its trailer); `2df183542` ← `gov-e66df1a64915` (its trailer); `77b908842` ← `gov-cd1205acd9ad` (its trailer); `600ad8403` ← `gov-d4078b39298a` (its trailer); `dad3a9574` ← `gov-d57d4df46524` (its trailer); `9a80c4056` ← `gov-f957e247b00d` (its trailer); `83907cc44` ← `gov-a13383825112` (its trailer); `224d81db7` ← `gov-7aeba4fff54c` (its trailer); `e1480bdb7` ← `gov-38db8d0e6f63` (its trailer); `c158728f7` ← `gov-7d5b89600392` (its trailer); `a696030d7` ← `gov-0ce061e93aa8` (its trailer); `da50cec39` ← `gov-67464ebe9d98` (its trailer); `24f38d9ec` ← `gov-e2860dda9b90` (its trailer); `82fcceb87` ← `gov-c17adb498877` (its trailer); `7d552adad` ← `gov-2a5d5a8a0a36` (its trailer); `59c9467c6` ← `gov-6b3b46433ead` (its trailer); `50b8071a0` ← `gov-99c2ae74f0be` (its trailer); `f268c3c2d` ← `gov-da7579817355` (its trailer); `f2d86ac11` ← `gov-f5c18c310afb` (its trailer); `15607f52b` ← `gov-6b655a0fdc5b` (its trailer); `432104c74` ← `gov-3a0448c527bd` (its trailer); `cd62deef2` ← `gov-6326fb3a42d8` (its trailer); `e2772d6e5` ← `gov-16e6da83ed14` (its trailer); `69e9fb7e0` ← `gov-8e28b314c6bb` (its trailer); `77ebc86fc` ← `gov-48dd29edcff1` (its trailer); `d2e5b6143` ← `gov-7b3e220ce3a4` (its trailer); `df372e700` ← `gov-f64aa4cf4252` (its trailer); `d16a092d9` ← `gov-6d327da36852` (its trailer); `8f2feeb71` ← `gov-1cf41b26cab9` (its trailer); `86ac4a0d9` ← `gov-44d96d1dbce4` (its trailer); `d34822984` ← `gov-f2f801402a3f` (its trailer); `542f2ba31` ← `gov-c6190e1bfc53` (its trailer); `ed1e8c248` ← `gov-c673bab57fce` (its trailer); `0cda03e39` ← `gov-1f4f36a2b478` (its trailer); `e0394731e` ← `gov-32be5943416c` (its trailer); `0235b8349` ← `gov-dcbae49d5a83` (its trailer); `22bcded75` ← `gov-737f3e5f334b` (its trailer); `11ca06af6` ← `gov-7fe056725724` (its trailer); `71f77ac2d` ← `gov-9b96ac795086` (its trailer); `83b4acffb` ← `gov-fcc68a7124b4` (its trailer); `4dbf71f37` ← `gov-e68ea9fbcfa4` (its trailer); `3030bac80` ← `gov-31c63ef55a03` (its trailer); `a344c2906` ← `gov-91730dd46ab2` (its trailer); `ba3bbb560` ← `gov-c7a2f6196527` (its trailer); `a6abbd356` ← `gov-5af5c8a47031` (its trailer); `b86a9bdff` ← `gov-91a847303d3f` (its trailer); `39d82bdce` ← `gov-e5918e047878` (its trailer); `8782fdb9e` ← `gov-45924da4e1bf` (its trailer); `b88bf33a8` ← `gov-bd4df987d690` (its trailer); `61874155d` ← `gov-930aa2def39d` (its trailer); `c156bdceb` ← `gov-35dd88d7bfb5` (its trailer); `3f4bfb88d` ← `gov-a56e0c7d8877` (its trailer); `f6835582c` ← `gov-125727e5e0f5` (its trailer); `8e7eb936f` ← `gov-3742bb8c027f` (its trailer); `f02cfc529` ← `gov-0a953b3b0a3e` (its trailer); `7277f9391` ← `gov-ca1d183dc87a` (its trailer); `c34d84d6d` ← `gov-087fe83ba1a5` (its trailer); `3eb32cdf2` ← `gov-7ac974c0d492` (its trailer); `7cb0f5e34` ← `gov-356be9708a0e` (its trailer); `0f00320d5` ← `gov-3171b67ce898` (its trailer); `47d0f0622` ← `gov-ae8a4aa4aa26` (its trailer); `b3fe23d37` ← `gov-a2793c5c0cf3` (its trailer); `1e74c41cc` ← `gov-3b9dfb0a5a50` (its trailer); `d718a8b6b` ← `gov-f0a28b6c151c` (its trailer); `c6259c2c6` ← `gov-5a0e716ee0bf` (its trailer); `863d5aa54` ← `gov-b1cd37533db4` (its trailer); `3f5b793eb` ← `gov-8f6576f893c0` (its trailer); `fbe9b0d63` ← `gov-a826b64787ac` (its trailer); `ceab24eba` ← `gov-f13bc54a903a` (its trailer); `8b0643e29` ← `gov-d5e634af6347` (its trailer); `5859b9f5b` ← `gov-72da18e2fe8b` (its trailer); `7534cac85` ← `gov-6933c5e24f45` (its trailer); `3b62e6719` ← `gov-2c0e1aace68e` (its trailer); `0db5d67ad` ← `gov-49a1091a8760` (its trailer); `0be6b3686` ← `gov-0e3f865a27cb` (its trailer); `5ccc7ad13` ← `gov-6aa1236923c6` (its trailer); `2afd987a7` ← `gov-afc683afee77` (its trailer); `08eaeb0cc` ← `gov-f38827d32cd2` (its trailer); `c6cfd6f52` ← `gov-3cd3290d7218` (its trailer); `d426f91ec` ← `gov-1a879f4ea141` (its trailer); `d73797290` ← `gov-b6299ee89e62` (its trailer); `44efa7fe7` ← `gov-041dd942c735` (its trailer); `761239740` ← `gov-e8020f77d600` (its trailer); `95014aa93` ← `gov-9a86b04f75c4` (its trailer); `ad14919cf` ← `gov-1856f94d0c07` (its trailer); `e0813f54b` ← `gov-d6fc84dd2088` (its trailer); `3804861ec` ← `gov-41479e55c505` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `ac1f87866ab3a24c…` from helm (informational) |
| Order | sha256 `9635711afff087b0…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 41 — Next stack: 41 evidence pieces on landing 40

| field | value |
|---|---|
| Landed | 2026-10-10 23:28:43 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `6da378c94d8188c329dcc8eae4e5ca0aef3e9f89` → `9af9160220981d7da600999c2d44771f86696dc1`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `9af9160220981d7da600999c2d44771f86696dc1`, tree `25cf5ab5a7c82450182ac524d60b71c460085c29`, from branch `worker/nextstack6da-1010`, parent `561846ce811c7848aaf59c28267af0d25fc3cd7f`, governance `gov-b98774535c6c` preserved. Unit `robotics-airships-nextstack6da-1010`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 9af916022…` → rc=0, HONOURED-XO 9af9160220981d7da600999c2d44771f86696dc1 — the last record for this sha (store line 1313) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `798e4989a` ← `gov-35cea2c12fcc` (its trailer); `f692c6245` ← `gov-79d37a23a659` (its trailer); `053572d7b` ← `gov-098baed2a3a0` (its trailer); `87f27edb5` ← `gov-bb2a929eac1e` (its trailer); `02e3c84ac` ← `gov-cc493969a37e` (its trailer); `0c185a154` ← `gov-bbff59f04188` (its trailer); `3eb37e4fa` ← `gov-ca724821b07d` (its trailer); `648f5db3e` ← `gov-71a390405397` (its trailer); `3f351748b` ← `gov-554a63d6ed6d` (its trailer); `230bb3007` ← `gov-1d07ada14e20` (its trailer); `e9308fa95` ← `gov-66a5b2e064e9` (its trailer); `80736796b` ← `gov-2663898509ec` (its trailer); `226e31d59` ← `gov-86e4caab6dd4` (its trailer); `712c4494c` ← `gov-6527b4680d10` (its trailer); `ae6251ce6` ← `gov-37be963942d1` (its trailer); `eb6045b7a` ← `gov-27e24442eadf` (its trailer); `55cf5614b` ← `gov-9023338a672f` (its trailer); `c553390dd` ← `gov-464d9cfeff00` (its trailer); `7914d5906` ← `gov-208c378336ed` (its trailer); `e3f055db5` ← `gov-fa4e12df8f69` (its trailer); `9cbcf0836` ← `gov-9b62f2852324` (its trailer); `dbb55b346` ← `gov-b840ec998e87` (its trailer); `a17da6307` ← `gov-05fa79a33f6c` (its trailer); `6f64dfaa3` ← `gov-1a3cf46cd204` (its trailer); `611894bd0` ← `gov-241558d4a49c` (its trailer); `e7b96200b` ← `gov-a2a7ce315e66` (its trailer); `1827239d7` ← `gov-a49d6db4f8d6` (its trailer); `b0746f985` ← `gov-d8ede1d343c6` (its trailer); `d21a6fea0` ← `gov-647a438c76bf` (its trailer); `30ad1068d` ← `gov-0c895cde3a12` (its trailer); `257a1891d` ← `gov-1c255175a1ae` (its trailer); `b74bdbc99` ← `gov-4990153d1e26` (its trailer); `01d0862b1` ← `gov-bdb0007d51c9` (its trailer); `b46fbdb28` ← `gov-977fc34592be` (its trailer); `285489371` ← `gov-9d6cc94b5e40` (its trailer); `1d0bbaa20` ← `gov-21937f1a1e14` (its trailer); `a133dbbbc` ← `gov-6b6f62182cb9` (its trailer); `12aac901b` ← `gov-6be407942dc3` (its trailer); `338c34912` ← `gov-0132ccd2532f` (its trailer); `4ebccb156` ← `gov-d8126f3f86e9` (its trailer); `561846ce8` ← `gov-95cc838b4e2c` (its trailer); `9af916022` ← `gov-b98774535c6c` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `bac3fde0dd502002…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 42 — Next stack: 36 evidence pieces on landing 41

| field | value |
|---|---|
| Landed | 2026-10-11 04:51:56 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `d7b0b6d3d2ff986d4194f879af945351b29605e1` → `2e524e7ae67ea5010981171702ff71254c62e383`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `2e524e7ae67ea5010981171702ff71254c62e383`, tree `ca97a18c62621f4edc206fa5602e69a895e2bf29`, from branch `worker/nextstackd7-1010`, parent `5a7c51bf21f5b99bc3330ad3672b341a34255995`, governance `gov-7859a8278ff6` preserved. Unit `robotics-airships-nextstackd7-1010`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 2e524e7ae…` → rc=0, HONOURED-XO 2e524e7ae67ea5010981171702ff71254c62e383 — the last record for this sha (store line 1362) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `436ee3805` ← `gov-bb8820291f5b` (its trailer); `83933156b` ← `gov-87bf056a1a96` (its trailer); `6f12bb035` ← `gov-5a9c8fbdd7af` (its trailer); `0514afea1` ← `gov-0d18cb778c77` (its trailer); `c3fb27f5b` ← `gov-7391f14e8f15` (its trailer); `7bb0a4666` ← `gov-712ee6a0b540` (its trailer); `c3e9770bf` ← `gov-f9eabd16c9b9` (its trailer); `474733b31` ← `gov-9db676766650` (its trailer); `fdda9ff0f` ← `gov-ebf4d39f462d` (its trailer); `64179767f` ← `gov-e5f7f2b1fbed` (its trailer); `f5ddb31c4` ← `gov-183c3c30f9cd` (its trailer); `5ef561e58` ← `gov-d58df91e1bf2` (its trailer); `dc5606d75` ← `gov-9e37101cf919` (its trailer); `6c8cbc4da` ← `gov-bbbba4d0380d` (its trailer); `9b18cf011` ← `gov-dc5331104038` (its trailer); `569190087` ← `gov-c16e5ea8eb04` (its trailer); `c417e5a10` ← `gov-aaacf4db9b5c` (its trailer); `9c4069087` ← `gov-82fd0e03723e` (its trailer); `c1a9e9b54` ← `gov-e8f0632745df` (its trailer); `6b17b30c7` ← `gov-5362febe5c33` (its trailer); `2481550ad` ← `gov-d8c931b73ef0` (its trailer); `955422a88` ← `gov-178ad3bdc0b7` (its trailer); `3a4cb1eca` ← `gov-40584083cbf2` (its trailer); `9b1fa722a` ← `gov-54151c2c7ec1` (its trailer); `1a6a95404` ← `gov-17327b71c8ff` (its trailer); `c75a17d0c` ← `gov-8522e56b0ce7` (its trailer); `e414089ae` ← `gov-5abbb4ef944d` (its trailer); `92b720048` ← `gov-7fb6a2030092` (its trailer); `db5dc3ece` ← `gov-a0d845df81da` (its trailer); `794976e26` ← `gov-315e2c6202ed` (its trailer); `750fd390d` ← `gov-824997f0055d` (its trailer); `7d83875cb` ← `gov-57188d7a734a` (its trailer); `704ac4df7` ← `gov-bb8feb758630` (its trailer); `4dbc7ee73` ← `gov-8b1fa2c392af` (its trailer); `5a7c51bf2` ← `gov-def3ec1f8e23` (its trailer); `2e524e7ae` ← `gov-7859a8278ff6` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `9696d56ccd0e3429…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 43 — Next stack: 196 evidence pieces on landing 42

| field | value |
|---|---|
| Landed | 2026-10-11 09:24:50 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `96a4a2a230304356c278b420595d7671af91d185` → `2ee264035e9d6143fa0d2e8bc46a77b7226d1e4f`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `2ee264035e9d6143fa0d2e8bc46a77b7226d1e4f`, tree `b0d9b81f07728bf401c166d42145b8b304b99576`, from branch `worker/nextstack96a-1011`, parent `d26644ec8504ec792cd4c46f85621696490dc2eb`, governance `gov-67e90d85e0e4` preserved. Unit `robotics-airships-nextstack96a-1011`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 2ee264035…` → rc=0, HONOURED-XO 2ee264035e9d6143fa0d2e8bc46a77b7226d1e4f — the last record for this sha (store line 1561) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `354998d30` ← `gov-6d9ccf55de14` (its trailer); `26aabfe06` ← `gov-518e65edb291` (its trailer); `c14a901f1` ← `gov-53b4b662d1a5` (its trailer); `89788ced2` ← `gov-da8636dfd205` (its trailer); `8a4da4efc` ← `gov-6935a214f64a` (its trailer); `86ed53d82` ← `gov-62d645022473` (its trailer); `312f29561` ← `gov-10c525ddd4a1` (its trailer); `80a9008c8` ← `gov-e7cace1c0bed` (its trailer); `2d63aa5bf` ← `gov-5ad8c9608b4c` (its trailer); `c7c8f5f66` ← `gov-6969686e3dd4` (its trailer); `71da72272` ← `gov-60aeb9e7cb7d` (its trailer); `e3f4bc2cc` ← `gov-9b3808472b98` (its trailer); `aac96e1b6` ← `gov-cee2db1e5258` (its trailer); `db913b8f4` ← `gov-708012e2d5b5` (its trailer); `92708ef15` ← `gov-3eb6e69298ff` (its trailer); `3eaa8d837` ← `gov-a9a72f24e0e1` (its trailer); `de9658c64` ← `gov-e6462d1c8fde` (its trailer); `5f5d97939` ← `gov-01bc698a5a54` (its trailer); `469d51e9a` ← `gov-0b628f2d0232` (its trailer); `d5b47e152` ← `gov-57399f6e7f2b` (its trailer); `ccdbe4680` ← `gov-340c92f78283` (its trailer); `198ff592b` ← `gov-bd8ff6ddf01f` (its trailer); `ca002549a` ← `gov-4d7033087bc2` (its trailer); `ae6cbcbfb` ← `gov-73151d2ef654` (its trailer); `f3459f685` ← `gov-15bcb947ac68` (its trailer); `1f3019b3f` ← `gov-f6ba5ef531cd` (its trailer); `26daac371` ← `gov-021832a76a67` (its trailer); `138c95296` ← `gov-154f64c34004` (its trailer); `9d5467344` ← `gov-7bfcadc2f34a` (its trailer); `ce6be40a2` ← `gov-7f9e4c453478` (its trailer); `fdb6d0031` ← `gov-23e7b354dc90` (its trailer); `1cf3315df` ← `gov-f9b448c0d65b` (its trailer); `5dd238a38` ← `gov-7ef507b53ae2` (its trailer); `698220883` ← `gov-968875fd67d0` (its trailer); `e0e24a3e3` ← `gov-23332cb0de82` (its trailer); `1b25dd663` ← `gov-f93444405d8c` (its trailer); `19ad983ec` ← `gov-56deb6a3bbd5` (its trailer); `e2facf514` ← `gov-8a882608773b` (its trailer); `3b502240e` ← `gov-44bb54318fd2` (its trailer); `87df73e3c` ← `gov-cc1bcde1e3e2` (its trailer); `6e46f7f4d` ← `gov-0062a0f817ff` (its trailer); `18aecb5ae` ← `gov-ef583ca7f6cf` (its trailer); `079a91166` ← `gov-26ffa5b83c81` (its trailer); `95813f0b2` ← `gov-6571550ac60b` (its trailer); `d6784171c` ← `gov-f6adf47efd5e` (its trailer); `cf059df09` ← `gov-26ae6c4e9727` (its trailer); `868943ab3` ← `gov-856c96892859` (its trailer); `e194559b5` ← `gov-c8efced23491` (its trailer); `bd37a3b16` ← `gov-b99bb6f55660` (its trailer); `95a7f57e3` ← `gov-f08ea9835b1d` (its trailer); `8dc128165` ← `gov-028cf927a62a` (its trailer); `9253c551e` ← `gov-963e03bc2dd6` (its trailer); `662d25fb7` ← `gov-235628367b29` (its trailer); `0d184222b` ← `gov-f63804324919` (its trailer); `51ac51a20` ← `gov-cdf2f4534b55` (its trailer); `97ecf9fa8` ← `gov-069d9c86eaea` (its trailer); `dcc3f7b90` ← `gov-dfbca507e33e` (its trailer); `6a2931e08` ← `gov-6aa5a92156df` (its trailer); `bf48ce3bf` ← `gov-a8010cabc895` (its trailer); `8225ae58b` ← `gov-7d2042283a70` (its trailer); `8d8854d27` ← `gov-70d27a0fd60f` (its trailer); `c1ada5b0b` ← `gov-1641e6ff9783` (its trailer); `5b654b4d7` ← `gov-0178dbaf262e` (its trailer); `a2c513bba` ← `gov-5a00e269b416` (its trailer); `407644e4c` ← `gov-39ee9812a79d` (its trailer); `8d3d58b9e` ← `gov-17adcf5dc582` (its trailer); `20756aa2c` ← `gov-745b9e360eea` (its trailer); `5c8c2f71b` ← `gov-13b8cce2e116` (its trailer); `e07359b1c` ← `gov-cb9ce5ec6b98` (its trailer); `2c9191eb6` ← `gov-5e378a241d23` (its trailer); `1bea20c3a` ← `gov-4cbb8c313d39` (its trailer); `3e5b934b8` ← `gov-46378977f4c0` (its trailer); `39e05a23e` ← `gov-49d705d9b04f` (its trailer); `e388e8063` ← `gov-d919d2cc7f2e` (its trailer); `44149afa1` ← `gov-e9c1995adb8c` (its trailer); `9d01ee2e6` ← `gov-b96b539a79c5` (its trailer); `cff59a87b` ← `gov-cd67e4aee096` (its trailer); `17834e173` ← `gov-8e56db49b77c` (its trailer); `8b3382cb9` ← `gov-4f7bfb56b119` (its trailer); `c89c01e7a` ← `gov-f712c17e6a28` (its trailer); `f1f7767d1` ← `gov-2588101e1b4a` (its trailer); `b13e8fc3b` ← `gov-8bdaa059f55d` (its trailer); `a07cfc584` ← `gov-0d2acc0de8be` (its trailer); `b532363ea` ← `gov-fba9b57d30ae` (its trailer); `c85e7af3b` ← `gov-d99b55db5ace` (its trailer); `7122db459` ← `gov-26322eb81a04` (its trailer); `cc19620c6` ← `gov-2117923de06e` (its trailer); `3f609248d` ← `gov-e3ff544fe6af` (its trailer); `6304fc818` ← `gov-7535e1964edc` (its trailer); `822f15501` ← `gov-027193eb8e6b` (its trailer); `cb1810fdb` ← `gov-f9391a5f71d5` (its trailer); `32d842e39` ← `gov-6c404817dbe7` (its trailer); `1e7400474` ← `gov-14325f5dd2fb` (its trailer); `c394fdbf7` ← `gov-8b19e17091a1` (its trailer); `c16b25082` ← `gov-c75a8cb28406` (its trailer); `075ea3e03` ← `gov-92e55f1e01e6` (its trailer); `67a9d1d60` ← `gov-6ee857b56ee9` (its trailer); `c4545c883` ← `gov-42ebaf19caba` (its trailer); `059e16f45` ← `gov-7a5454d58608` (its trailer); `e2ba9285d` ← `gov-2930cf3071db` (its trailer); `679cf318e` ← `gov-58c35c9399f9` (its trailer); `dd053acea` ← `gov-77804c581bf5` (its trailer); `fe5bb677a` ← `gov-e5127ae3fc47` (its trailer); `2daa30c8e` ← `gov-630eedb19ae8` (its trailer); `aed487af4` ← `gov-0c60e73b510b` (its trailer); `cf8ed4539` ← `gov-c9bc4ec6d754` (its trailer); `ef6bb28fe` ← `gov-5ab9c3a66f7f` (its trailer); `5ccef7ff8` ← `gov-09b193a2c4a1` (its trailer); `4044f8644` ← `gov-37d2ba662957` (its trailer); `35ee53a51` ← `gov-7532e098d38c` (its trailer); `c9e3af57f` ← `gov-aed34fa39e8f` (its trailer); `020562335` ← `gov-39e8543cc270` (its trailer); `6e935dfef` ← `gov-cd38f1d6b731` (its trailer); `a39ffc2c8` ← `gov-7b5231f750d3` (its trailer); `16a87b73f` ← `gov-fc14a147cfd6` (its trailer); `c7dd35703` ← `gov-f5f16c07d8fb` (its trailer); `fe7ddcd32` ← `gov-a2d63bcf5d96` (its trailer); `b0aa672cf` ← `gov-58f2c9e2a40d` (its trailer); `b21cc039d` ← `gov-20d807422d83` (its trailer); `6f552fbdc` ← `gov-285c996ae743` (its trailer); `9486156d1` ← `gov-c8828065ed46` (its trailer); `5844d3cb7` ← `gov-b5744d01a536` (its trailer); `7ae2e5487` ← `gov-e65ba2beec68` (its trailer); `9bed2b9d5` ← `gov-f98e437e2a1f` (its trailer); `9d49b90e0` ← `gov-22f2fe4e6e42` (its trailer); `140e43d7b` ← `gov-b3e6e0039364` (its trailer); `1b8657989` ← `gov-45ee4ec1127b` (its trailer); `442c25f73` ← `gov-6534a4a628be` (its trailer); `efc67f1f4` ← `gov-6500eecfab36` (its trailer); `a97a5f2e6` ← `gov-f2e0b918e0c2` (its trailer); `83e4e09a4` ← `gov-f1aececb95ad` (its trailer); `0219bd5bd` ← `gov-5003b9a2e593` (its trailer); `6977bfbcb` ← `gov-e5a806ca631e` (its trailer); `985b2dd72` ← `gov-ef2e0eefba06` (its trailer); `282d93f57` ← `gov-9dc94657b864` (its trailer); `e1ce7e2bf` ← `gov-ef4e0e81e965` (its trailer); `00b437719` ← `gov-b2796357f4bf` (its trailer); `cedae48ec` ← `gov-2fdbee05c269` (its trailer); `dd23403d6` ← `gov-d9d6a37ac53f` (its trailer); `52d839ceb` ← `gov-e6ef838527c4` (its trailer); `2aa734fad` ← `gov-d4b313c4084b` (its trailer); `e5971e43e` ← `gov-378bd14ea1ac` (its trailer); `a76b9b312` ← `gov-f9920ea30a4e` (its trailer); `997c40833` ← `gov-6b98d58c2b79` (its trailer); `4430a22fd` ← `gov-231f669c5716` (its trailer); `d78fb0a18` ← `gov-0a09310c18e7` (its trailer); `47532e55b` ← `gov-b6a251acd49d` (its trailer); `6829a6f75` ← `gov-f9084281abfe` (its trailer); `c72933a92` ← `gov-9675abb282d6` (its trailer); `06eb610f5` ← `gov-e467a1a95057` (its trailer); `bd79fc0af` ← `gov-44b058970d06` (its trailer); `a1c39a652` ← `gov-c5e815ff767b` (its trailer); `558ce5763` ← `gov-756d3ad95d50` (its trailer); `afad4b383` ← `gov-bd306781f0bd` (its trailer); `4fa5c627f` ← `gov-dc2ef6fcc2cb` (its trailer); `fcc0d0db9` ← `gov-3c750523b937` (its trailer); `a5128adaa` ← `gov-f40085db8f9e` (its trailer); `2bf0a2384` ← `gov-73c4c73c74ab` (its trailer); `374ef75d3` ← `gov-c6ea594cf34a` (its trailer); `3f0d48d46` ← `gov-7bde0e9d3497` (its trailer); `ef5e738e4` ← `gov-2a15d96bd934` (its trailer); `9501e425a` ← `gov-1beef369555a` (its trailer); `f94ca7384` ← `gov-1ee0fa7a9e6b` (its trailer); `cd491be65` ← `gov-aa91186917f3` (its trailer); `5fa4edf61` ← `gov-86fc403fa82c` (its trailer); `86f81fc3e` ← `gov-2cb4429407af` (its trailer); `680abf005` ← `gov-cb8aed615d03` (its trailer); `5dd9569f7` ← `gov-1e7502ddfa90` (its trailer); `4dbf42581` ← `gov-d820eb0c30f8` (its trailer); `8be4939bc` ← `gov-907fb3498301` (its trailer); `6f54bd3e5` ← `gov-2464dc826a57` (its trailer); `16ad27aa6` ← `gov-43491f9d598e` (its trailer); `2741b90ee` ← `gov-d221806aedd5` (its trailer); `65936a22d` ← `gov-0a71c31569ea` (its trailer); `a300ce3a2` ← `gov-619af69bed09` (its trailer); `09668bd44` ← `gov-77f2b5169467` (its trailer); `b2314f06d` ← `gov-7b7c9e2027c5` (its trailer); `10c343901` ← `gov-25a26f8b26b5` (its trailer); `244eb679d` ← `gov-02b01a1895c5` (its trailer); `2f4fbf669` ← `gov-18eec9185e98` (its trailer); `29591f8cb` ← `gov-babcb90f63e1` (its trailer); `dbe5a4bd0` ← `gov-902392bc0451` (its trailer); `53df305a8` ← `gov-b5b66c325ef6` (its trailer); `021197dde` ← `gov-b6a5f3d53fc0` (its trailer); `4b7cfaf22` ← `gov-fc52289445b2` (its trailer); `c282fb5e6` ← `gov-6419ce89ecd7` (its trailer); `8cb16f2e0` ← `gov-5ce24088f09b` (its trailer); `ea8f6c0bb` ← `gov-0ecb32801569` (its trailer); `30764ed5a` ← `gov-f3d2881a24fe` (its trailer); `27448da2d` ← `gov-cd3876bc9d90` (its trailer); `70ddb4bbc` ← `gov-5f3423d7ffcc` (its trailer); `52aa1098c` ← `gov-a35cf364509d` (its trailer); `2515cf355` ← `gov-f4b5322114c9` (its trailer); `c0c57773a` ← `gov-7bebe5f308ad` (its trailer); `30a3d71ea` ← `gov-dfd44eea3dbc` (its trailer); `d26644ec8` ← `gov-783e83ec0c2e` (its trailer); `2ee264035` ← `gov-67e90d85e0e4` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `c26eddacf56e535b…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 44 — Next stack: 56 evidence pieces on landing 43

| field | value |
|---|---|
| Landed | 2026-10-11 13:44:57 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `62066b11351dc4a1ffe99a4b4f4e27b4462c003a` → `d3ecfa33ea05b35f3422fa0a8b0a5959d5f8a3fb`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `d3ecfa33ea05b35f3422fa0a8b0a5959d5f8a3fb`, tree `a9b05f282eb42ca24abc53e6ad26433ff47f4cf7`, from branch `worker/nextstack620-1011`, parent `bd9f0520c7f6d21ce5f0212f56a2fd2576dd56a7`, governance `gov-fe5c37ab6fdc` preserved. Unit `robotics-airships-nextstack620-1011`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py d3ecfa33e…` → rc=0, HONOURED-XO d3ecfa33ea05b35f3422fa0a8b0a5959d5f8a3fb — the last record for this sha (store line 1618) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `09b6e1eb2` ← `gov-b883c3882e94` (its trailer); `082e13432` ← `gov-6bd574dd27c8` (its trailer); `e958c9dd2` ← `gov-3bea127f9a3b` (its trailer); `7ad7b9786` ← `gov-fd43b33b8d26` (its trailer); `897334961` ← `gov-8694c5d5e5b4` (its trailer); `ec8517f1a` ← `gov-eef1e6217adb` (its trailer); `b558235d8` ← `gov-2c3746166c80` (its trailer); `ae1d78c14` ← `gov-a38a470cca9b` (its trailer); `d27246ffe` ← `gov-993fe8625768` (its trailer); `97b54c1a8` ← `gov-c51a2b4692bc` (its trailer); `828e63e9a` ← `gov-214ff19d7ac2` (its trailer); `d3d77165d` ← `gov-343535c62236` (its trailer); `921894120` ← `gov-f586e6bb02ff` (its trailer); `26df1d90f` ← `gov-e1c90680d80c` (its trailer); `31e705d20` ← `gov-9bb790fe72cd` (its trailer); `a9676621e` ← `gov-7f296ebe0952` (its trailer); `466673e21` ← `gov-38efe341600d` (its trailer); `1755c6bae` ← `gov-87f12bd662b5` (its trailer); `f506ddf69` ← `gov-337a329df38a` (its trailer); `eddc97c49` ← `gov-5003e51a0c38` (its trailer); `cb2751d0e` ← `gov-108dbf1c5153` (its trailer); `fbf44023b` ← `gov-35b61d635b18` (its trailer); `0d22394bc` ← `gov-cdf40a5212a7` (its trailer); `60065ca19` ← `gov-578a230d9085` (its trailer); `293377bd7` ← `gov-d7e184357848` (its trailer); `4f4fd65a3` ← `gov-9ee4bda26238` (its trailer); `8bf78c8b6` ← `gov-5b21b4b218bb` (its trailer); `de87f5710` ← `gov-256f1928d024` (its trailer); `0167ddb15` ← `gov-1d2981516925` (its trailer); `2aac06813` ← `gov-f2cda5d64dd8` (its trailer); `0f15db774` ← `gov-df65341584f9` (its trailer); `fa4b5866a` ← `gov-d3b624c837e4` (its trailer); `138007bae` ← `gov-aa46116e6b77` (its trailer); `d64d81d51` ← `gov-7e441851cdf4` (its trailer); `de9b56bd8` ← `gov-0e9983253bd1` (its trailer); `306a89ee4` ← `gov-31af23eb51e4` (its trailer); `b696e61c9` ← `gov-2f3456300c70` (its trailer); `8d9d9fd7c` ← `gov-9d2888e20a8c` (its trailer); `349b31625` ← `gov-f5d951f4b659` (its trailer); `16c44d3c7` ← `gov-13f3ba6cb94a` (its trailer); `836d1dba1` ← `gov-0126c45d6916` (its trailer); `630372e1f` ← `gov-5264295f4e3a` (its trailer); `a3b6a2f32` ← `gov-ace3e6a19137` (its trailer); `e378417a2` ← `gov-adb541a253ca` (its trailer); `357f5de3d` ← `gov-a35eb97c42de` (its trailer); `7d4524f07` ← `gov-f22f329bea5c` (its trailer); `871c1949a` ← `gov-72a67a2322ad` (its trailer); `d2f74f1ab` ← `gov-02d1a09bee86` (its trailer); `d9fb3d346` ← `gov-04d6ccb2444f` (its trailer); `790c8bd9d` ← `gov-4d0163475642` (its trailer); `b8c70b989` ← `gov-91a550283d72` (its trailer); `9f0a4a204` ← `gov-ac905f57844f` (its trailer); `e2412aeed` ← `gov-5f7855c5f25a` (its trailer); `69928f8ed` ← `gov-bc3bcacec618` (its trailer); `bd9f0520c` ← `gov-d784bb1b0b02` (its trailer); `d3ecfa33e` ← `gov-fe5c37ab6fdc` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `389c0362922459dc…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 45 — Next stack: 89 evidence pieces on landing 44

| field | value |
|---|---|
| Landed | 2026-10-11 18:50:42 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `1a4ec99e8a8338245419a8ab9821e9dfa193f531` → `4d272f0e7b90736652c382c42f51137007d5de8d`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `4d272f0e7b90736652c382c42f51137007d5de8d`, tree `3b4fee0d69dffd5e9180fb147c6a831bfb91778d`, from branch `worker/nextstack1a4-1011`, parent `aaeb5d8ae89f6a6edeb1a9b4792265cfbad4e8c2`, governance `gov-7c7689e24cf5` preserved. Unit `robotics-airships-nextstack1a4-1011`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 4d272f0e7…` → rc=0, HONOURED-XO 4d272f0e7b90736652c382c42f51137007d5de8d — the last record for this sha (store line 1710) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `fc26276b8` ← `gov-245e008aac9d` (its trailer); `0f06e11e7` ← `gov-8e00914685b3` (its trailer); `e8166c3c4` ← `gov-4b87b81dba24` (its trailer); `b76720d0d` ← `gov-e3bd772c25c5` (its trailer); `17e17f958` ← `gov-5ccfacbc32db` (its trailer); `070a21180` ← `gov-7e0a9ff08842` (its trailer); `471147d2e` ← `gov-97e3907b0738` (its trailer); `18fb7577c` ← `gov-a5ba2148b3a8` (its trailer); `588fad090` ← `gov-2865ca6c6132` (its trailer); `cb017b137` ← `gov-78df981ac930` (its trailer); `9f49d2944` ← `gov-3bb5a9ad8800` (its trailer); `67b0971f9` ← `gov-223cf7753ec0` (its trailer); `d8e3d1041` ← `gov-124afeca70e9` (its trailer); `f3c5a81a3` ← `gov-bcab76a7a588` (its trailer); `3047c87e5` ← `gov-eb5459100a4b` (its trailer); `b11603aba` ← `gov-580a3e03b1af` (its trailer); `c57d42947` ← `gov-15c635dbaa9e` (its trailer); `1b6b13a0a` ← `gov-c15f7044c4e1` (its trailer); `34126d34d` ← `gov-fab6c68ecc1a` (its trailer); `9754712a5` ← `gov-e70bbe471ad6` (its trailer); `1233f11b1` ← `gov-c1507af41adc` (its trailer); `0de7b92aa` ← `gov-d4c48dde8c6c` (its trailer); `6e188981b` ← `gov-4bcbe87b5e77` (its trailer); `dc575d949` ← `gov-4c781e53741e` (its trailer); `54b7817af` ← `gov-435cc37d3759` (its trailer); `1066a2043` ← `gov-578b158d9776` (its trailer); `3d91f9da6` ← `gov-15d4c6cee971` (its trailer); `fd5af85f5` ← `gov-b63b6dbf4411` (its trailer); `02dc066a7` ← `gov-2c107e8c7d03` (its trailer); `ee0e496aa` ← `gov-9a6a0e90d486` (its trailer); `1191d58f4` ← `gov-fec8205756d2` (its trailer); `5c7665ea6` ← `gov-6007a95a2c11` (its trailer); `3ed35aedd` ← `gov-c8ff34a0510f` (its trailer); `a696ed859` ← `gov-bae80582d226` (its trailer); `0f31b54b9` ← `gov-c7d696430cd4` (its trailer); `4153f2609` ← `gov-e2aaaa278c79` (its trailer); `b156b9f6b` ← `gov-b51cf76f00af` (its trailer); `4a80795f5` ← `gov-b80f730ba75d` (its trailer); `ffd8d119e` ← `gov-d62a340d8302` (its trailer); `9549d4032` ← `gov-def96a161105` (its trailer); `7edf7588d` ← `gov-c7d71445160d` (its trailer); `92b8c1786` ← `gov-ed32f7ee7ca3` (its trailer); `d0093007f` ← `gov-636e96bcc9ce` (its trailer); `4e048794d` ← `gov-c9ac37d116b6` (its trailer); `c3fcd24cb` ← `gov-0e0fdd0d64a3` (its trailer); `cb0a42dc0` ← `gov-1d0935ca51ff` (its trailer); `f37a1f662` ← `gov-65f1a7c1d093` (its trailer); `74232cfc6` ← `gov-88f5279500b1` (its trailer); `82cf05608` ← `gov-f333279e5b1b` (its trailer); `ef3c57864` ← `gov-8778a5c5c647` (its trailer); `b52df343a` ← `gov-f34aab34fe57` (its trailer); `837801489` ← `gov-c2238fde0ce0` (its trailer); `888dfb130` ← `gov-fe4853bf8ce9` (its trailer); `b1d04dfe7` ← `gov-995ca5260371` (its trailer); `6de2dc259` ← `gov-438dc9afd5ac` (its trailer); `9b5c95f10` ← `gov-d42ab49b9e09` (its trailer); `61b63e779` ← `gov-91c8ec42d938` (its trailer); `6b7fbbdce` ← `gov-dcff77a3b682` (its trailer); `4594b1fb1` ← `gov-fa80de431d90` (its trailer); `520a06b9b` ← `gov-b514ba28cbf1` (its trailer); `1a4f8f63f` ← `gov-132841b9a570` (its trailer); `64ccba7f4` ← `gov-71688e4d9164` (its trailer); `05d416e2a` ← `gov-13ab5102b866` (its trailer); `c947ccf02` ← `gov-97145b96e7ad` (its trailer); `171b4a6e4` ← `gov-25a504f312cc` (its trailer); `2b6009c15` ← `gov-37ac60c7324c` (its trailer); `0417b50d5` ← `gov-b066d6b0f30d` (its trailer); `411571217` ← `gov-344763c3b910` (its trailer); `51e5d5b1b` ← `gov-7466024d747c` (its trailer); `c3549d320` ← `gov-93d091c04b23` (its trailer); `9ea8973af` ← `gov-7fbe46a613e3` (its trailer); `9458d9c8d` ← `gov-a1b692f36671` (its trailer); `3d08a25ab` ← `gov-2efeb41e21e0` (its trailer); `f4ca6326f` ← `gov-81096c16a57f` (its trailer); `0c195cb95` ← `gov-885026a5fa5a` (its trailer); `72c2cf768` ← `gov-dbde716f2cae` (its trailer); `982a4b810` ← `gov-a5d2a678d085` (its trailer); `5acbb2fd8` ← `gov-699f309a0ccc` (its trailer); `058644386` ← `gov-c2a352eb0062` (its trailer); `266c6991e` ← `gov-353fbe656564` (its trailer); `23c93b516` ← `gov-1896abf8e534` (its trailer); `5223faaed` ← `gov-62fdc885d483` (its trailer); `623a1c0f8` ← `gov-d07634a6cbf9` (its trailer); `8f3664611` ← `gov-6d2dd10ab6d3` (its trailer); `7ed149054` ← `gov-883f32baa944` (its trailer); `ff8dd4ce7` ← `gov-58165d37b452` (its trailer); `423c5e0c9` ← `gov-96cdd0c1e072` (its trailer); `aaeb5d8ae` ← `gov-0dfdcb74f190` (its trailer); `4d272f0e7` ← `gov-7c7689e24cf5` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `f72f68741dfaa431…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 46 — CI producer-timeout fix

| field | value |
|---|---|
| Landed | 2026-10-11 22:41:13 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `f10a7d519811f9b67cc381fa349d51f123d7fee2` → `444e6f6bba349e7d135aa56629cdd9b75e59a84a`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `444e6f6bba349e7d135aa56629cdd9b75e59a84a`, tree `7a9c46f1ec66ccc33d2ef23ffe6cc5ffb95aadc6`, from branch `worker/ci-producer-timeout-fix-1011`, parent `83ebdbc3625025079a63170575e971e06bf139a2`, governance `gov-fe08da2f0ef3` preserved. Unit `robotics-ci-producer-timeout-fix-1011`. |
| Rebase | law I.3c.5, mechanised: the signed object `4f903503059acca0a0bb67741a57f2d93e06ed44` was rebased off `1a4ec99e8a8338245419a8ab9821e9dfa193f531` onto the moved main `f10a7d519811f9b67cc381fa349d51f123d7fee2`, landing as `444e6f6bba349e7d135aa56629cdd9b75e59a84a`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  6e24577e = 1:  83ebdbc3 Cache failed generated producers and bound claim plant concurrency
2:  4f903503 = 2:  444e6f6b Update plant runner test for two-worker default
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 4f9035030…` → rc=0, HONOURED-XO 4f903503059acca0a0bb67741a57f2d93e06ed44 — the last record for this sha (store line 1751) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `83ebdbc36` ← `gov-ack-83ebdbc36250` (reconcile record; trailer `gov-e3d1e0808cae` is bound to another sha); `444e6f6bb` ← `gov-ack-444e6f6bba34` (reconcile record; trailer `gov-fe08da2f0ef3` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `a10435c2a7c77ae7…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 47 — CI46 earned full-plants receipt on landing 46

| field | value |
|---|---|
| Landed | 2026-10-12 07:41:32 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `62c4881246679937b3671f67c9a5cc078076fc6c` → `c4d67c1a1910f0f871e0256796ee006aa47d96b9`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `c4d67c1a1910f0f871e0256796ee006aa47d96b9`, tree `b12eb725f88a9834837346181f4553120b5f56c8`, from branch `worker/ci46-earned-receipt-1012`, parent `62c4881246679937b3671f67c9a5cc078076fc6c`, governance `gov-e9855a83d88b` preserved. Unit `robotics-charter-1009`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py c4d67c1a1…` → rc=0, HONOURED-XO c4d67c1a1910f0f871e0256796ee006aa47d96b9 — the last record for this sha (store line 1831) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `c4d67c1a1` ← `gov-e9855a83d88b` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck floatplantcheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `120fa3449d1415d6…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 48 — Next stack: 52 evidence pieces rebased on landing 47

| field | value |
|---|---|
| Landed | 2026-10-12 11:30:00 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `46512b3fb49751cb935d6e0229e609c7c9096afd` → `a5e038e3f0374d1af3e15bdbbb28bbe555f875d1`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `a5e038e3f0374d1af3e15bdbbb28bbe555f875d1`, tree `8554dbaa27772b241af754ed6e7c387afdfef1aa`, from branch `worker/nextstack465-rebase52-1012`, parent `a0d786076201ed7bf2aba8608dd9e471e22b0c63`, governance `gov-94b60aa2f660` preserved. Unit `robotics-airships-nextstack465-rebase52-1012`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py a5e038e3f…` → rc=0, HONOURED-XO a5e038e3f0374d1af3e15bdbbb28bbe555f875d1 — the last record for this sha (store line 1859) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `bf2e4a8fb` ← `gov-12099abd078c` (its trailer); `1f7e0b3b0` ← `gov-a73cf10473ce` (its trailer); `2bd753d0d` ← `gov-7b166accee41` (its trailer); `84882ce77` ← `gov-0ad6f8aaf57d` (its trailer); `60cd2b9b4` ← `gov-d9000aa10bdd` (its trailer); `b44b39249` ← `gov-e0407e828080` (its trailer); `519aac714` ← `gov-27c6ef764178` (its trailer); `5c87ee498` ← `gov-ab77bfb2716a` (its trailer); `30d50b317` ← `gov-9126e2cf42f5` (its trailer); `bb7423c66` ← `gov-5c2dc70b1c29` (its trailer); `3d39a0139` ← `gov-4e0856159310` (its trailer); `6e1094bff` ← `gov-88eff34b09a5` (its trailer); `0fe10e3af` ← `gov-1dbf2059f02f` (its trailer); `c1937c6d1` ← `gov-b56499867a96` (its trailer); `2b5c7442f` ← `gov-60441b211d5c` (its trailer); `b85497072` ← `gov-27f9036e4fb5` (its trailer); `057b3e012` ← `gov-627fa62455ce` (its trailer); `e7eca80cc` ← `gov-ddf57829846a` (its trailer); `0bdd4f690` ← `gov-cfad30a03351` (its trailer); `4664b514b` ← `gov-f36e90123a02` (its trailer); `30b8666b9` ← `gov-601464710079` (its trailer); `41c66aa88` ← `gov-78f0e38e63a9` (its trailer); `97b3d460f` ← `gov-a78574eca34a` (its trailer); `f2edae81b` ← `gov-553daca89988` (its trailer); `7eeaff0f0` ← `gov-79358b7abef1` (its trailer); `95ab8c8a9` ← `gov-c391a4bb8e90` (its trailer); `cfcd72026` ← `gov-6232d998b2a6` (its trailer); `8e84d1ee9` ← `gov-895e2a97d4b2` (its trailer); `7d00f18e4` ← `gov-fdce697473ae` (its trailer); `a2dd3022f` ← `gov-e8d452213a59` (its trailer); `175abbff3` ← `gov-995e614b5f14` (its trailer); `2a5809902` ← `gov-7135e22482ce` (its trailer); `3bbe6ef56` ← `gov-ff9ae7eb6c63` (its trailer); `b5068073f` ← `gov-ce149caab94f` (its trailer); `b24e2da62` ← `gov-9b14eeadcb9e` (its trailer); `71e8e9ec1` ← `gov-c303479bdf7e` (its trailer); `1e1bb79a3` ← `gov-e791fd388405` (its trailer); `7855ccd53` ← `gov-af1fe15f3785` (its trailer); `c2ceb1f72` ← `gov-5a48ebe9c76a` (its trailer); `ce39275d8` ← `gov-04cd1bd93bd5` (its trailer); `a617ca0b7` ← `gov-545c8e32fc76` (its trailer); `467e8d238` ← `gov-9d4cee6b1475` (its trailer); `db9733b0d` ← `gov-3ab54ddcc917` (its trailer); `3972fe70c` ← `gov-d6333ea18905` (its trailer); `63d4e788f` ← `gov-04f2aa53b20c` (its trailer); `0f8ea48d9` ← `gov-a95d43378ebc` (its trailer); `a4355cf27` ← `gov-91143b859677` (its trailer); `3518ee916` ← `gov-826296bbaef8` (its trailer); `949aabdc5` ← `gov-84630d6f37df` (its trailer); `682ddb43e` ← `gov-d9e3611337d7` (its trailer); `a0d786076` ← `gov-f4fb11670fcf` (its trailer); `a5e038e3f` ← `gov-94b60aa2f660` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck floatplantcheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `999d5a6c058bea17…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 49 — Next stack: 90 evidence pieces on landing 48

| field | value |
|---|---|
| Landed | 2026-10-12 13:55:48 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `1a9d694e6302ba7fba1dd436c93e306b2789d32d` → `63d8e8ff2edde8504dbdebd33c9f9ee10b29f065`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `63d8e8ff2edde8504dbdebd33c9f9ee10b29f065`, tree `af1a629f2148e53dc4c4cea4d62164e2d7f3ac5e`, from branch `worker/nextstack1a9-1012`, parent `09a2c7dae207aec9adfd0fd2eb6f511cdf9bae64`, governance `gov-f9e942cc3cce` preserved. Unit `robotics-airships-nextstack1a9-1012`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 63d8e8ff2…` → rc=0, HONOURED-XO 63d8e8ff2edde8504dbdebd33c9f9ee10b29f065 — the last record for this sha (store line 1866) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `66d68d1c1` ← `gov-4230aaeda42c` (its trailer); `ce82f87c6` ← `gov-bb6fcd958708` (its trailer); `72b92d3a5` ← `gov-e756ae7b4484` (its trailer); `7d87a189b` ← `gov-0452c97a8f6f` (its trailer); `278d62449` ← `gov-7cf769287ef7` (its trailer); `c98cfe463` ← `gov-c0b69047ef71` (its trailer); `753a8e37c` ← `gov-e8808a2e0f9e` (its trailer); `a6201a9c6` ← `gov-cd4195ef7b99` (its trailer); `cfc511169` ← `gov-487b477605f4` (its trailer); `8736373ff` ← `gov-d17a431e075a` (its trailer); `17e0d6910` ← `gov-877e62e6b829` (its trailer); `a9107bd4a` ← `gov-45c16cec85de` (its trailer); `36314534d` ← `gov-7a26b48a7d25` (its trailer); `8cee62a6b` ← `gov-e50d6ee2150c` (its trailer); `231b4e763` ← `gov-bb3ddb9c9410` (its trailer); `4c150a8db` ← `gov-6b936ec8900a` (its trailer); `d537c407c` ← `gov-f78324d25c5d` (its trailer); `fda051e26` ← `gov-40adc1ba40c9` (its trailer); `69273e9f9` ← `gov-03ead1e0784d` (its trailer); `d57d750eb` ← `gov-3dd2514cf1c1` (its trailer); `cdf8101b6` ← `gov-7dba4d9e02af` (its trailer); `4ca7b45b4` ← `gov-e1cd904133dc` (its trailer); `6b1b7d4de` ← `gov-db5610b825dd` (its trailer); `36b962cc2` ← `gov-e0e5d7370518` (its trailer); `aadc4c0a0` ← `gov-641ada5ac8cd` (its trailer); `64b30816b` ← `gov-6b4c487b4931` (its trailer); `f4749a000` ← `gov-131e28d6c9a8` (its trailer); `707af2b64` ← `gov-6186028e0603` (its trailer); `b3b61cb7f` ← `gov-3ae3d049d5d4` (its trailer); `225641a03` ← `gov-c656c3d5026c` (its trailer); `c0933c539` ← `gov-0169e9bb9ada` (its trailer); `357b8c053` ← `gov-67b8c5252ae4` (its trailer); `aeaca440b` ← `gov-4125cf480855` (its trailer); `2abe876e2` ← `gov-26a4cb57d279` (its trailer); `9e4818116` ← `gov-febce275c70e` (its trailer); `34e395b0c` ← `gov-98932ddc017b` (its trailer); `ce77029c6` ← `gov-2b8d63a1b65e` (its trailer); `7b31535f3` ← `gov-1b9be308891f` (its trailer); `fda3a9ad7` ← `gov-fdb6f9fbca80` (its trailer); `daca4376d` ← `gov-db64c5faeaf3` (its trailer); `a391c9978` ← `gov-204a7a3e6ff3` (its trailer); `2d319ddf0` ← `gov-4cd5089927fd` (its trailer); `bdeed328d` ← `gov-6d373ee2c60b` (its trailer); `e4646cd65` ← `gov-eb8e06643950` (its trailer); `53d86274e` ← `gov-481897476fc3` (its trailer); `338ed2325` ← `gov-5734e5621f6a` (its trailer); `d109a238f` ← `gov-2f1d1a64d6ad` (its trailer); `dc9cc3eec` ← `gov-01888b57caab` (its trailer); `2f09ec486` ← `gov-6e530a2a0bd0` (its trailer); `8aecda823` ← `gov-2bf645b56275` (its trailer); `0d02bf7a0` ← `gov-59adc222b8b8` (its trailer); `9ab7d71d3` ← `gov-20c10e6287ce` (its trailer); `c75fe13f8` ← `gov-bceab2a3a8ca` (its trailer); `7df8751da` ← `gov-efb884343275` (its trailer); `9b0b3fcac` ← `gov-8c724d992066` (its trailer); `f5ca412ee` ← `gov-ebd3b89b23f1` (its trailer); `532176904` ← `gov-b3b20f80701c` (its trailer); `1bc8b606b` ← `gov-871ca401e3b7` (its trailer); `b2bdbf65b` ← `gov-af86548993b1` (its trailer); `55b171e5d` ← `gov-0f4854fa5202` (its trailer); `bd8df911e` ← `gov-6b94874459ee` (its trailer); `c6bc2331b` ← `gov-57f41331427f` (its trailer); `bdeb6e721` ← `gov-119c1f5b155f` (its trailer); `8f07c7662` ← `gov-5edcaa0a7801` (its trailer); `632bbd378` ← `gov-4f0281af52ff` (its trailer); `94ac677eb` ← `gov-a39d4e0ca131` (its trailer); `e6ef6d1a8` ← `gov-eea94c680dd2` (its trailer); `3359a3f36` ← `gov-28feaad38942` (its trailer); `e76a8959c` ← `gov-82a1240b5485` (its trailer); `e563e8f4e` ← `gov-f8cd460506ba` (its trailer); `2a4fb3363` ← `gov-3346d0ca43c9` (its trailer); `03db09e16` ← `gov-8dde40e1e5d6` (its trailer); `71e3c6da4` ← `gov-47f59648ecd7` (its trailer); `2c5a2c07c` ← `gov-338516e8f51d` (its trailer); `03e7cc1b7` ← `gov-1cd8fa617cb3` (its trailer); `0b0660e75` ← `gov-ed04b882536c` (its trailer); `783eef40d` ← `gov-0838e7db01ac` (its trailer); `7539e5334` ← `gov-c3dcd14f955b` (its trailer); `d0acc943a` ← `gov-a9d050f436d7` (its trailer); `344032006` ← `gov-64d574a6c606` (its trailer); `6ea0ab508` ← `gov-dec0c9eae717` (its trailer); `dc061bb83` ← `gov-bb6aee4bb3ff` (its trailer); `0bc019e73` ← `gov-2d522bf29562` (its trailer); `d059dd1ce` ← `gov-86477a52c950` (its trailer); `d4c9f5583` ← `gov-8961d5249e58` (its trailer); `183613428` ← `gov-72a402a9fd0b` (its trailer); `ae6d9c0cc` ← `gov-6e305dfbcafe` (its trailer); `f205bfa3d` ← `gov-5fbd2b010b27` (its trailer); `09a2c7dae` ← `gov-d87a89969e23` (its trailer); `63d8e8ff2` ← `gov-f9e942cc3cce` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck floatplantcheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `2d453c6eaeb3e33d…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 50 — Next stack: 26 evidence pieces on landing 49

| field | value |
|---|---|
| Landed | 2026-10-12 17:44:39 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `cbfc8fe37a2cca94837b3a4ed9dddd0c641c9aed` → `d075d273dc764114caccd313b013108b0b4d3db7`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `d075d273dc764114caccd313b013108b0b4d3db7`, tree `6bc6f2facf311124d44afb37f4fb4dd24491eaae`, from branch `worker/nextstackcbf-1012`, parent `4787a84dd2bbb00b76a950a9013ae9718734af49`, governance `gov-22ef7de84415` preserved. Unit `robotics-airships-nextstackcbf-1012`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py d075d273d…` → rc=0, HONOURED-XO d075d273dc764114caccd313b013108b0b4d3db7 — the last record for this sha (store line 1884) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `6ac456a85` ← `gov-debe7806b518` (its trailer); `514dcdc4e` ← `gov-e4b6335401b5` (its trailer); `7075e9694` ← `gov-17215e4fd32e` (its trailer); `3c44a93bd` ← `gov-40a71e42ed04` (its trailer); `93f5c026c` ← `gov-03977f87593a` (its trailer); `9ba314e04` ← `gov-933fdd0c0095` (its trailer); `8725edead` ← `gov-8543f2f848ec` (its trailer); `6a8ddd442` ← `gov-e2c4695d6b8a` (its trailer); `6092cff4c` ← `gov-b8fa60472538` (its trailer); `4b903df89` ← `gov-b57ee20629e9` (its trailer); `e92387e1f` ← `gov-39d0f1416667` (its trailer); `15ca72331` ← `gov-8b43ecf5ff75` (its trailer); `48819b4ac` ← `gov-4b3c07c96a81` (its trailer); `58aaec610` ← `gov-98d978351415` (its trailer); `8db573e2b` ← `gov-980af15c01f4` (its trailer); `30f639426` ← `gov-1e084fad0ad7` (its trailer); `8faf95b82` ← `gov-1d5a96766079` (its trailer); `7ec15e6ea` ← `gov-ee4184d71d30` (its trailer); `2c2920318` ← `gov-88c1ee9b68d3` (its trailer); `aef1762e8` ← `gov-94d6b08c9908` (its trailer); `290ab8664` ← `gov-6fb4c2c89e05` (its trailer); `82bd1af31` ← `gov-8f09a0c0047d` (its trailer); `83a21f9f0` ← `gov-60b8522f2409` (its trailer); `d1f7515a4` ← `gov-bba18e630284` (its trailer); `4787a84dd` ← `gov-39cc8a4b2b54` (its trailer); `d075d273d` ← `gov-22ef7de84415` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck floatplantcheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `7611da2d89c0fcde…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 51 — Next stack: 28 evidence pieces on landing 50

| field | value |
|---|---|
| Landed | 2026-10-12 23:03:50 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `142b573085a6fc761450fef9be06cd12f14cedfd` → `0255492b326ba1a16b09ee575968892438621041`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `0255492b326ba1a16b09ee575968892438621041`, tree `fa46bf6616d53895b54ffae880b673ed37f1f9d6`, from branch `worker/nextstack142-1012`, parent `db31bfcb7aa7c79c5bc4f3de7e540e6e88bf4658`, governance `gov-1e19a64088eb` preserved. Unit `robotics-airships-nextstack142-1012`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 0255492b3…` → rc=0, HONOURED-XO 0255492b326ba1a16b09ee575968892438621041 — the last record for this sha (store line 1946) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `b39fe46ed` ← `gov-1f5ce57eb70e` (its trailer); `4cb0c564b` ← `gov-ef5c77c80a63` (its trailer); `c43d11b44` ← `gov-e898699c0c39` (its trailer); `ac67cd883` ← `gov-49a21267a343` (its trailer); `937a2792e` ← `gov-c0e2a54012a3` (its trailer); `8a010037a` ← `gov-8ea0276c748c` (its trailer); `ebfd0ec8b` ← `gov-adb169ff9954` (its trailer); `a7fbba64a` ← `gov-da1856caa844` (its trailer); `ca08c8285` ← `gov-8a55264d4a8b` (its trailer); `8b089bc78` ← `gov-f50ba0c47944` (its trailer); `0a1fc5a87` ← `gov-f25250b28537` (its trailer); `21dc970b8` ← `gov-06edc1e89c70` (its trailer); `c7cdcae93` ← `gov-96cca26f0947` (its trailer); `9e4039165` ← `gov-4f5ae1dbdb51` (its trailer); `d95585bee` ← `gov-636fb57791ec` (its trailer); `7bd29bd92` ← `gov-5696a812858b` (its trailer); `572114a41` ← `gov-4de87664fa26` (its trailer); `4c4c3efdd` ← `gov-8c56152532e5` (its trailer); `de4aa2a68` ← `gov-b6a92e47edd7` (its trailer); `f04aea216` ← `gov-5e8068c8adb5` (its trailer); `da91114f5` ← `gov-387685160766` (its trailer); `0f0b46cc3` ← `gov-2fd4ce83bc5c` (its trailer); `c3d21f162` ← `gov-3d7b704710ac` (its trailer); `5ccd8afae` ← `gov-4beba6b941fb` (its trailer); `78b86d92e` ← `gov-d77f69bb1172` (its trailer); `9153cf77c` ← `gov-e639c5d78f5f` (its trailer); `db31bfcb7` ← `gov-d6d3ef70864f` (its trailer); `0255492b3` ← `gov-1e19a64088eb` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make ciparity reposizecheck claimscheck ledgercheck linkcheck buildercheck readmecheck evaccheck floatplantcheck` rc=0 (environment PATH, TMPDIR set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `61bade1707728213…` (informational) |
| Foreign route | order-named preserve_paths `research/claims/register.json, research/claims/carry-history.json, research/claims/rule-changes.json, research/claims/accepted-defects.json` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 52 — Record controlled pressure and geometry design comparisons

| field | value |
|---|---|
| Landed | 2026-10-14 00:35:01 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `afb2c2d1726b9d9a805f9781085c3dd6a52913e5` → `2da1ca08e9013c4c65cd26984b2b66492da28c46`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `2da1ca08e9013c4c65cd26984b2b66492da28c46`, tree `cb33d4acd708f8d406c30aec27a39470a85f39cb`, from branch `r3-i002-pressure-geometry`, parent `afb2c2d1726b9d9a805f9781085c3dd6a52913e5`, governance `gov-96850bb0d04b` preserved. Unit `r3-i002`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 2da1ca08e…` → rc=0, HONOURED-XO 2da1ca08e9013c4c65cd26984b2b66492da28c46 — the last record for this sha (store line 1960) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `2da1ca08e` ← `gov-96850bb0d04b` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--test-reporter=tap make readmecheck linkcheck buildercheck` rc=0 (environment PATH set to host paths, not shown) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `1e0e62b9a8519011…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 53 — Record corrected gas-envelope and partial-vacuum budgets

| field | value |
|---|---|
| Landed | 2026-10-14 00:44:03 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `985fe3cea7a5b7cf389ad23e6540f8d7e1c5032e` → `b71738ba6a7980aa59ed5484c86d83cbd30d9b1a`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `b71738ba6a7980aa59ed5484c86d83cbd30d9b1a`, tree `28f1805e395aff9730440458af4c3fdffbf39dbc`, from branch `main`, parent `2dc07d658e506f43dfd79e570013a273ba33667b`, governance `gov-2be9d0122d03` preserved. Unit `r3-i003`. |
| Rebase | law I.3c.5, mechanised: the signed object `f9bd1a3181b2a255a25ef922db3ab432e4cf53b8` was rebased off `afb2c2d1726b9d9a805f9781085c3dd6a52913e5` onto the moved main `985fe3cea7a5b7cf389ad23e6540f8d7e1c5032e`, landing as `b71738ba6a7980aa59ed5484c86d83cbd30d9b1a`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  515238ba = 1:  2dc07d65 R3-I003 design iteration: gas-supported vs evacuated hull at P-100 scale
2:  f9bd1a31 = 2:  b71738ba R3-I003 corrections: payload in every mission case, full-mixture hybrid, membrane equilibrium, connected gas schedule
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py f9bd1a318…` → rc=0, HONOURED-XO f9bd1a3181b2a255a25ef922db3ab432e4cf53b8 — the last record for this sha (store line 1961) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `2dc07d658` ← `gov-ack-2dc07d658e50` (reconcile record; trailer `gov-29889ad1cc9a` is bound to another sha); `b71738ba6` ← `gov-ack-b71738ba6a79` (reconcile record; trailer `gov-2be9d0122d03` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck` rc=0 (environment PATH set to host paths, not shown) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `2cc503031326b89d…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 54 — Reorient the programme toward airship design iterations

| field | value |
|---|---|
| Landed | 2026-10-14 00:57:35 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `857245e2805dab3217b8f30425ecb3131971a24d` → `20c94a85006e2df5432b6129e2df63c0fc1a6083`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `20c94a85006e2df5432b6129e2df63c0fc1a6083`, tree `e90f7dc7ee5c3e1937f8983eb77e09e0956594cd`, from branch `worker-r3-programme-claims-repair-1014`, parent `a00020baf3c36101e84498077a3fb8dd322607d4`, governance `gov-a25f54973066` preserved. Unit `r3-programme-claims-repair-1014`. |
| Rebase | law I.3c.5, mechanised: the signed object `8a7986868133914e38d69267758cba25e2212102` was rebased off `afb2c2d1726b9d9a805f9781085c3dd6a52913e5` onto the moved main `857245e2805dab3217b8f30425ecb3131971a24d`, landing as `20c94a85006e2df5432b6129e2df63c0fc1a6083`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  9a197434 = 1:  a00020ba Redirect the programme around design iterations
2:  8a798686 = 2:  20c94a85 Repair programme README claim locations
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 8a7986868…` → rc=0, HONOURED-XO 8a7986868133914e38d69267758cba25e2212102 — the last record for this sha (store line 1962) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `a00020baf` ← `gov-ack-a00020baf3c3` (reconcile record; trailer `gov-e2958037c0d0` is bound to another sha); `20c94a850` ← `gov-ack-20c94a85006e` (reconcile record; trailer `gov-a25f54973066` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `86901fbb9c5a2d85…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 55 — Record near-ambient helium support and pressure-control design

| field | value |
|---|---|
| Landed | 2026-10-14 01:25:54 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `29230ac279e8b8408d130e71974d6284410e6ec6` → `d8b7f13fd4d64b21eb55c5a7e0b006d87231328c`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `d8b7f13fd4d64b21eb55c5a7e0b006d87231328c`, tree `f2b91116bca269add0892924aca24f0f29afba93`, from branch `r3-i006-gas-support`, parent `7bc200648eb087b6cd545da7933ebba7e0a8068b`, governance `gov-2e5551fda150` preserved. Unit `r3-i006-gas-support-1014`. |
| Rebase | law I.3c.5, mechanised: the signed object `300ceae0cfda20c126abc88d8d1f50728ef88c1f` was rebased off `afb2c2d1726b9d9a805f9781085c3dd6a52913e5` onto the moved main `29230ac279e8b8408d130e71974d6284410e6ec6`, landing as `d8b7f13fd4d64b21eb55c5a7e0b006d87231328c`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  4aefd672 = 1:  7bc20064 Price helium envelope support and gas inventory for R3-I006
2:  300ceae0 = 2:  d8b7f13f Carry reported I002 landing into I006 source context
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 300ceae0c…` → rc=0, HONOURED-XO 300ceae0cfda20c126abc88d8d1f50728ef88c1f — the last record for this sha (store line 1963) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `7bc200648` ← `gov-ack-7bc200648eb0` (reconcile record; trailer `gov-f990c50175f4` is bound to another sha); `d8b7f13fd` ← `gov-ack-d8b7f13fd4d6` (reconcile record; trailer `gov-2e5551fda150` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `36deb922aac0d86c…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 56 — Record baseline vacuum hull mass and lift assessment

| field | value |
|---|---|
| Landed | 2026-10-14 01:37:37 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `34a3697f289fe093c014c49ca32e0092455e02f7` → `b354ce4a1fe99aa0ceaef60a96d8904eb794421d`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `b354ce4a1fe99aa0ceaef60a96d8904eb794421d`, tree `2c5db1c5eda29b73b8811828e4e07ddc6fe27122`, from branch `worker-r3-i001-landing54-1014`, parent `34a3697f289fe093c014c49ca32e0092455e02f7`, governance `gov-2523e832c4a9` preserved. Unit `r3-i001`. |
| Rebase | law I.3c.5, mechanised: the signed object `b5ee0d9c14cdccbb14117e09bb3c7f4f7b0e3cdf` was rebased off `29230ac279e8b8408d130e71974d6284410e6ec6` onto the moved main `34a3697f289fe093c014c49ca32e0092455e02f7`, landing as `b354ce4a1fe99aa0ceaef60a96d8904eb794421d`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  b5ee0d9c = 1:  b354ce4a docs: append unchanged R3-I001 to landed programme
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py b5ee0d9c1…` → rc=0, HONOURED-XO b5ee0d9c14cdccbb14117e09bb3c7f4f7b0e3cdf — the last record for this sha (store line 1964) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `b354ce4a1` ← `gov-ack-b354ce4a1fe9` (reconcile record; trailer `gov-2523e832c4a9` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `8a6c415d506c7022…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 57 — Record no-net capsule assessment and clarify I006 source reference

| field | value |
|---|---|
| Landed | 2026-10-14 02:08:08 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `486ec5165517101f3e743fbc35226077823142df` → `bf75d1a383dd3720d330df14f5303ee47b722a94`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `bf75d1a383dd3720d330df14f5303ee47b722a94`, tree `c97070293ce6ecb494bec8cc191214b4647f7aed`, from branch `worker-r3-i008-landing56-1014`, parent `486ec5165517101f3e743fbc35226077823142df`, governance `gov-51844c8d4108` preserved. Unit `r3-i008`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py bf75d1a38…` → rc=0, HONOURED-XO bf75d1a383dd3720d330df14f5303ee47b722a94 — the last record for this sha (store line 1965) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `bf75d1a38` ← `gov-51844c8d4108` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `3b0a2b25f91db8cb…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 58 — Record X-web capsule geometry and failed hardware budget

| field | value |
|---|---|
| Landed | 2026-10-14 02:46:00 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `afb9c053d39baa6ab3b9bee00462487f5998a1bf` → `11a534f82360daed5e167188273c3d9776045c2e`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `11a534f82360daed5e167188273c3d9776045c2e`, tree `dc93125215f6f63691128075b09e957972bcded4`, from branch `worker-r3-i011-landing57-1014`, parent `afb9c053d39baa6ab3b9bee00462487f5998a1bf`, governance `gov-2d26b312a9c5` preserved. Unit `r3-i011`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 11a534f82…` → rc=0, HONOURED-XO 11a534f82360daed5e167188273c3d9776045c2e — the last record for this sha (store line 1966) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `11a534f82` ← `gov-2d26b312a9c5` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `df86f31b318acf1e…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 59 — Record 76 m helium suspension and corrected bag pressure bounds

| field | value |
|---|---|
| Landed | 2026-10-14 03:05:00 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `96ffc35fefc5db10ae0c47ed992e6ace9b2bdac6` → `5c9b20e1b655ed3a7c459e75b784fc13efa4fffb`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `5c9b20e1b655ed3a7c459e75b784fc13efa4fffb`, tree `541f15df78ebd19f0f46b82c284b18b9d0d7d080`, from branch `r3-i010-landing57-package`, parent `96ffc35fefc5db10ae0c47ed992e6ace9b2bdac6`, governance `gov-3a46132e652b` preserved. Unit `r3-i010`. |
| Rebase | law I.3c.5, mechanised: the signed object `20e8883475cb244d0c16413668a18a70e2d05f8e` was rebased off `afb9c053d39baa6ab3b9bee00462487f5998a1bf` onto the moved main `96ffc35fefc5db10ae0c47ed992e6ace9b2bdac6`, landing as `5c9b20e1b655ed3a7c459e75b784fc13efa4fffb`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  20e88834 = 1:  5c9b20e1 research: package corrected 76m envelope design on named base
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 20e888347…` → rc=0, HONOURED-XO 20e8883475cb244d0c16413668a18a70e2d05f8e — the last record for this sha (store line 1967) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `5c9b20e1b` ← `gov-ack-5c9b20e1b655` (reconcile record; trailer `gov-3a46132e652b` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `8a8c2c8d0f69ec1e…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 60 — Record one-vent water delivery and corrected fuel-limited trim ledger

| field | value |
|---|---|
| Landed | 2026-10-14 03:27:13 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `daeaf1d09c018c4b8136f819dd0697292c32fbbf` → `76e7d3b899a949dd8605fdb37c3f6de65ece6931`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `76e7d3b899a949dd8605fdb37c3f6de65ece6931`, tree `af66713217b0500d5a83b0cd2c3d7e7a13546e50`, from branch `landing57-i007`, parent `daeaf1d09c018c4b8136f819dd0697292c32fbbf`, governance `gov-9be7e72b1806` preserved. Unit `r3-i007`. |
| Rebase | law I.3c.5, mechanised: the signed object `428cad41e1bdf28757dafde93374fdf765fc4ba1` was rebased off `afb9c053d39baa6ab3b9bee00462487f5998a1bf` onto the moved main `daeaf1d09c018c4b8136f819dd0697292c32fbbf`, landing as `76e7d3b899a949dd8605fdb37c3f6de65ece6931`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  428cad41 = 1:  76e7d3b8 R3-I007 landing57 package: byte-identical two-file candidate on the Captain's named base
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 428cad41e…` → rc=0, HONOURED-XO 428cad41e1bdf28757dafde93374fdf765fc4ba1 — the last record for this sha (store line 1968) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `76e7d3b89` ← `gov-ack-76e7d3b899a9` (reconcile record; trailer `gov-9be7e72b1806` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `ff1df6e601cc4205…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 61 — Record failed finite-endpoint net designs and corrected mechanical accounting

| field | value |
|---|---|
| Landed | 2026-10-14 03:38:01 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `84658ea416209d442f7643c9f8860161331867a8` → `8d4618d0ae333390add72d99878e2f05291c805a`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `8d4618d0ae333390add72d99878e2f05291c805a`, tree `a023968f1451feb1d3c51552e3caedaf1ea4b243`, from branch `landing58-package`, parent `84658ea416209d442f7643c9f8860161331867a8`, governance `gov-a41532a17502` preserved. Unit `r3-i004-i005-i009`. |
| Rebase | law I.3c.5, mechanised: the signed object `ef22b604e1fa020d06289be95bd8b623c8d0c970` was rebased off `96ffc35fefc5db10ae0c47ed992e6ace9b2bdac6` onto the moved main `84658ea416209d442f7643c9f8860161331867a8`, landing as `8d4618d0ae333390add72d99878e2f05291c805a`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  ef22b604 = 1:  8d4618d0 Land the corrected spoke-network record as one nine-file package
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py ef22b604e…` → rc=0, HONOURED-XO ef22b604e1fa020d06289be95bd8b623c8d0c970 — the last record for this sha (store line 1969) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `8d4618d0a` ← `gov-ack-8d4618d0ae33` (reconcile record; trailer `gov-a41532a17502` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `4b65087ba82ac914…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 62 — Record continuous ring joint geometry and failed pressure screens

| field | value |
|---|---|
| Landed | 2026-10-14 04:46:24 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `4b70658b28de619b9815b8ab28f29529d8402862` → `886787c112146190d827a11c85e5b5980d97d25b`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `886787c112146190d827a11c85e5b5980d97d25b`, tree `74feebc4a8c902f1ec0d0ccf287d9dcba7fb9db1`, from branch `worker-r3-i014-landing61-1014`, parent `4b70658b28de619b9815b8ab28f29529d8402862`, governance `gov-03e73e55219e` preserved. Unit `r3-i014`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 886787c11…` → rc=0, HONOURED-XO 886787c112146190d827a11c85e5b5980d97d25b — the last record for this sha (store line 1970) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `886787c11` ← `gov-03e73e55219e` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `00160483f1134845…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 63 — Record helium suspension routing and construction mass bounds

| field | value |
|---|---|
| Landed | 2026-10-14 04:49:13 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `510acd50fb84405952ba2f3b16185746fa1a41cb` → `e914782948438a7141c1f37e1dc5bf82450589b1`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `e914782948438a7141c1f37e1dc5bf82450589b1`, tree `a9ef3271e6f23318dd04492f69e4203b1a4a283b`, from branch `r3-i013-landing59-package`, parent `510acd50fb84405952ba2f3b16185746fa1a41cb`, governance `gov-861881d01677` preserved. Unit `r3-i013`. |
| Rebase | law I.3c.5, mechanised: the signed object `087fdfd827df235500e9bda0a9c8860075f47356` was rebased off `daeaf1d09c018c4b8136f819dd0697292c32fbbf` onto the moved main `510acd50fb84405952ba2f3b16185746fa1a41cb`, landing as `e914782948438a7141c1f37e1dc5bf82450589b1`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  087fdfd8 = 1:  e9147829 research: package finite-support routing on accepted pressure base
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 087fdfd82…` → rc=0, HONOURED-XO 087fdfd827df235500e9bda0a9c8860075f47356 — the last record for this sha (store line 1971) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `e91478294` ← `gov-ack-e91478294843` (reconcile record; trailer `gov-861881d01677` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `ee40692f17e9255d…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 64 — Record isolated ballonet control and failure protection limits

| field | value |
|---|---|
| Landed | 2026-10-14 06:12:12 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `8b439af9d4a164c3c7ad6814919d072fa810cc28` → `024b8b4b0fc7198fae5e7326e294a562169ad71f`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `024b8b4b0fc7198fae5e7326e294a562169ad71f`, tree `1f30b12eb720ee8bc2642d6bc5c68071baf740f0`, from branch `r3-i018-landing63-package`, parent `8b439af9d4a164c3c7ad6814919d072fa810cc28`, governance `gov-6ff48b8193e4` preserved. Unit `r3-i018`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 024b8b4b0…` → rc=0, HONOURED-XO 024b8b4b0fc7198fae5e7326e294a562169ad71f — the last record for this sha (store line 1972) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `024b8b4b0` ← `gov-6ff48b8193e4` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `411b1aa44b7ee902…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 65 — Add continuous cap and barrel construction with shared clip loads

| field | value |
|---|---|
| Landed | 2026-10-14 06:18:38 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `e3e9c1e236a6483b224b503fd327358011d60699` → `a035783f8ba24658ec7f022c21d92ddd937b8a3b`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `a035783f8ba24658ec7f022c21d92ddd937b8a3b`, tree `db7f08629a8d9cdd17d93ea2c043cd8ab8ab74a8`, from branch `worker-r3-i016-landing63-1014`, parent `e3e9c1e236a6483b224b503fd327358011d60699`, governance `gov-23e01f64986f` preserved. Unit `r3-i016`. |
| Rebase | law I.3c.5, mechanised: the signed object `a627d00d1181b34c757b1ca3bfdc64039da99867` was rebased off `8b439af9d4a164c3c7ad6814919d072fa810cc28` onto the moved main `e3e9c1e236a6483b224b503fd327358011d60699`, landing as `a035783f8ba24658ec7f022c21d92ddd937b8a3b`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  a627d00d = 1:  a035783f Add continuous cap and barrel construction with shared clip loads
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py a627d00d1…` → rc=0, HONOURED-XO a627d00d1181b34c757b1ca3bfdc64039da99867 — the last record for this sha (store line 1973) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `a035783f8` ← `gov-ack-a035783f8ba2` (reconcile record; trailer `gov-23e01f64986f` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `89474d1d0c72f427…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 66 — Record guide-rack construction and portable reproduction paths

| field | value |
|---|---|
| Landed | 2026-10-14 07:12:57 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `ba085772a5a15d15ccede0040de00c7e8c9b155c` → `6387c13ee32085b9f3a9d9ed309abeba4eee261a`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `6387c13ee32085b9f3a9d9ed309abeba4eee261a`, tree `67acf55fd0ef05e730ded2477b51c1c228bb3889`, from branch `r3-i022-landing64-package`, parent `c96fd431f74c95940987c93d442ee616d2124230`, governance `gov-1854574746f8` preserved. Unit `r3-i022`. |
| Rebase | law I.3c.5, mechanised: the signed object `b0396d128d7bc2d8e63b5470ae7a1b486d350e27` was rebased off `e3e9c1e236a6483b224b503fd327358011d60699` onto the moved main `ba085772a5a15d15ccede0040de00c7e8c9b155c`, landing as `6387c13ee32085b9f3a9d9ed309abeba4eee261a`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  fab3b0c5 = 1:  c96fd431 Record finite guide racks and corrected rope travel
2:  b0396d12 = 2:  6387c13e Use relative paths in pressure and guide-rack examples
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py b0396d128…` → rc=0, HONOURED-XO b0396d128d7bc2d8e63b5470ae7a1b486d350e27 — the last record for this sha (store line 1975) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `c96fd431f` ← `gov-ack-c96fd431f74c` (reconcile record; trailer `gov-061c18a3c86b` is bound to another sha); `6387c13ee` ← `gov-ack-6387c13ee320` (reconcile record; trailer `gov-1854574746f8` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `e507d968e8eed95d…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 67 — Record coupled endpoint and taut-cord termination limits

| field | value |
|---|---|
| Landed | 2026-10-14 07:28:29 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `cbb64c2544185c3eee9d8aa27de52ec20fcdba25` → `8566efc878df9749fc8ce831de384758d905b0a4`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `8566efc878df9749fc8ce831de384758d905b0a4`, tree `828a9f7a0e2dca350ac3b5e78f27dcba1d594f92`, from branch `i015-i019-landing65-package`, parent `cbb64c2544185c3eee9d8aa27de52ec20fcdba25`, governance `gov-90ac398be110` preserved. Unit `r3-i015-i019`. |
| Rebase | law I.3c.5, mechanised: the signed object `7bdc8b7865f3c9fd9185146ad320776a89e1190e` was rebased off `ba085772a5a15d15ccede0040de00c7e8c9b155c` onto the moved main `cbb64c2544185c3eee9d8aa27de52ec20fcdba25`, landing as `8566efc878df9749fc8ce831de384758d905b0a4`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  7bdc8b78 = 1:  8566efc8 Add coupled cord cell and termination fitting design iterations
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 7bdc8b786…` → rc=0, HONOURED-XO 7bdc8b7865f3c9fd9185146ad320776a89e1190e — the last record for this sha (store line 1976) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `8566efc87` ← `gov-ack-8566efc878df` (reconcile record; trailer `gov-90ac398be110` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `2df24a388ae6a0a6…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 68 — Record polar transition construction and local connection limits

| field | value |
|---|---|
| Landed | 2026-10-14 07:35:56 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `6b303343dfb8ba6f8b6432560bda3dc5a266b338` → `84864c083961fad534419cd7145a99b696f84834`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `84864c083961fad534419cd7145a99b696f84834`, tree `5fd7c075dc95a3292002d7d26c537bb7949b78ec`, from branch `worker-r3-i020-landing65-1014`, parent `6b303343dfb8ba6f8b6432560bda3dc5a266b338`, governance `gov-d9e5ba8b2c3a` preserved. Unit `r3-i020`. |
| Rebase | law I.3c.5, mechanised: the signed object `eefd5fbc345b6ceed760327f28b2482ad9a56e99` was rebased off `ba085772a5a15d15ccede0040de00c7e8c9b155c` onto the moved main `6b303343dfb8ba6f8b6432560bda3dc5a266b338`, landing as `84864c083961fad534419cd7145a99b696f84834`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  eefd5fbc = 1:  84864c08 Record finite polar transition and complete support demands
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py eefd5fbc3…` → rc=0, HONOURED-XO eefd5fbc345b6ceed760327f28b2482ad9a56e99 — the last record for this sha (store line 1977) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `84864c083` ← `gov-ack-84864c083961` (reconcile record; trailer `gov-d9e5ba8b2c3a` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `985fbd863d09f297…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 69 — Record radial escape yokes and upper-anchor demand limits

| field | value |
|---|---|
| Landed | 2026-10-14 08:50:46 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `3005ed8272a91245449d16c1601d4b172ea6690c` → `3386390b3dbc3b3d17c96a49acf99a3c01249a07`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `3386390b3dbc3b3d17c96a49acf99a3c01249a07`, tree `eb15aaba807331599d4d0db68b4a648597c9b9e9`, from branch `r3-i026-landing68-package`, parent `3005ed8272a91245449d16c1601d4b172ea6690c`, governance `gov-796955b34f57` preserved. Unit `r3-i026`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 3386390b3…` → rc=0, HONOURED-XO 3386390b3dbc3b3d17c96a49acf99a3c01249a07 — the last record for this sha (store line 1978) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `3386390b3` ← `gov-796955b34f57` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `06eef0df392a49b2…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 70 — Record the vacuum-cell load path and its public provenance links

| field | value |
|---|---|
| Landed | 2026-10-14 10:13:51 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `8f57d0d6b1059a62189f6226d84b784c3bc0290e` → `8af7a475f7e3bfc3d888c7bbba242c00ba28cc45`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `8af7a475f7e3bfc3d888c7bbba242c00ba28cc45`, tree `8684975432b6cf65fb93bef7bf69fc21746c7d09`, from branch `i023-package68`, parent `53f4b00e533e8669b62fc21f9de49fdab326b118`, governance `gov-729967f7663b` preserved. Unit `r3-i023`. |
| Rebase | law I.3c.5, mechanised: the signed object `4156dd1463c12a724c36ad51bdec7ca105b2aef4` was rebased off `3005ed8272a91245449d16c1601d4b172ea6690c` onto the moved main `8f57d0d6b1059a62189f6226d84b784c3bc0290e`, landing as `8af7a475f7e3bfc3d888c7bbba242c00ba28cc45`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  0f07a833 = 1:  53f4b00e Add vacuum-cell load path design iteration R3-I023
2:  4156dd14 = 2:  8af7a475 Remove unpublished branch references from public provenance text
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 4156dd146…` → rc=0, HONOURED-XO 4156dd1463c12a724c36ad51bdec7ca105b2aef4 — the last record for this sha (store line 1982) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `53f4b00e5` ← `gov-ack-53f4b00e533e` (reconcile record; trailer `gov-d5e9edea0f8b` is bound to another sha); `8af7a475f` ← `gov-ack-8af7a475f7e3` (reconcile record; trailer `gov-729967f7663b` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `c286e93f8a5a38cc…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 71 — Record spaced polar node geometry, its installed metadata and local provenance prose

| field | value |
|---|---|
| Landed | 2026-10-14 11:07:52 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `20dee8ccd6fbf3e0e1ccfd87b2b60f2fb2287e3e` → `4b508bab60841aafef379e650a13937df620b569`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `4b508bab60841aafef379e650a13937df620b569`, tree `08eafc920a26830154831766e9715278d0d45c35`, from branch `worker-r3-i024-landing70-1014`, parent `9fdd39467db4ae790aaacfc4e1c22f820007ba9e`, governance `gov-a9dc0bf650f8` preserved. Unit `r3-i024`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 4b508bab6…` → rc=0, HONOURED-XO 4b508bab60841aafef379e650a13937df620b569 — the last record for this sha (store line 1984) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `0e9c0cd5b` ← `gov-7267adbdd92b` (its trailer); `9fdd39467` ← `gov-547f468fc583` (its trailer); `4b508bab6` ← `gov-a9dc0bf650f8` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `d5c29603641a01af…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 72 — Record the corrected I012 and I017 units, the I007 README scrub and the I024 public provenance chain

| field | value |
|---|---|
| Landed | 2026-10-14 12:13:30 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `a02d2d4b1e6687815b243821577f9f861e62707f` → `f3f60ee4f4de706e5eaf060d9451207e7f2b99da`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `f3f60ee4f4de706e5eaf060d9451207e7f2b99da`, tree `0f9e79e4a2e0da9914e26bbd86e194f8e320cd38`, from branch `package71-i012-i017-i007`, parent `9aad39ed23771e8a3612914d13d1b46cc502ae4a`, governance `gov-c6bcab7097c8` preserved. Unit `r3-i012-i017`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py f3f60ee4f…` → rc=0, HONOURED-XO f3f60ee4f4de706e5eaf060d9451207e7f2b99da — the last record for this sha (store line 1986) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `9aad39ed2` ← `gov-d067b751cc29` (its trailer); `f3f60ee4f` ← `gov-c6bcab7097c8` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `dd657762d81b6559…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 73 — Historic-day views open fitted and running, standby rows say the day's truth, and the monitor page keeps to public content

| field | value |
|---|---|
| Landed | 2026-10-14 14:09:36 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `e3a6f7b854ef0683fbcdacd6db330a7c3b94044b` → `0e1c1544482ddcbb03f18f59c171505d1d116fb3`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `0e1c1544482ddcbb03f18f59c171505d1d116fb3`, tree `160cf473be6803a3de9bfc3d155a58c629a94751`, from branch `public-msg-1014`, parent `5f58901d172043a26934bf9a1b01a2d4671d547a`, governance `gov-0bd918ef0d6f` preserved. Unit `robotics-site-airships-1013`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 0e1c15444…` → rc=0, HONOURED-XO 0e1c1544482ddcbb03f18f59c171505d1d116fb3 — the last record for this sha (store line 1997) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `860837b12` ← `gov-bfe0884f1cef` (its trailer); `a6a956205` ← `gov-9d14996fe169` (its trailer); `05343e1f6` ← `gov-f07f7c1ad5a2` (its trailer); `5f58901d1` ← `gov-7dfb815ed047` (its trailer); `0e1c15444` ← `gov-0bd918ef0d6f` (its trailer). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `5a5782915d143134…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 74 — Record R3-I028: aluminium socket bodies at fixed drawn dimensions, with its full run count

| field | value |
|---|---|
| Landed | 2026-10-14 16:40:43 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `69f8eeac41b9a08f3391b7ad16516bdd2fdc7de3` → `c9c88bda99d47434edba8523c6d78138e631473f`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `c9c88bda99d47434edba8523c6d78138e631473f`, tree `44fdb529dca89cae2b3b5671d9b70be15084b3f9`, from branch `i028-socket-body`, parent `6153a24ea9633f5f1dc168961734d20c613ab6ed`, governance `gov-e8f2bb1faf76` preserved. Unit `float-programme-r3`. |
| Rebase | law I.3c.5, mechanised: the signed object `c0d861099bbe9312d56bfdb65103788a27fa7065` was rebased off `e3a6f7b854ef0683fbcdacd6db330a7c3b94044b` onto the moved main `69f8eeac41b9a08f3391b7ad16516bdd2fdc7de3`, landing as `c9c88bda99d47434edba8523c6d78138e631473f`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  20de8d76 = 1:  821c17a3 Add R3-I028: machined aluminium socket bodies at frozen drawn dimensions
2:  12048b2a = 2:  6153a24e R3-I028: consolidated review correction of the candidate claim set
3:  c0d86109 = 3:  c9c88bda R3-I028: provenance record correction — four scientific invocations
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py c0d861099…` → rc=0, HONOURED-XO c0d861099bbe9312d56bfdb65103788a27fa7065 — the last record for this sha (store line 1999) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `821c17a33` ← `gov-ack-821c17a334b8` (reconcile record; trailer `gov-edb2ab2f1eb4` is bound to another sha); `6153a24ea` ← `gov-ack-6153a24ea963` (reconcile record; trailer `gov-369e1dff7e55` is bound to another sha); `c9c88bda9` ← `gov-ack-c9c88bda99d4` (reconcile record; trailer `gov-e8f2bb1faf76` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `8619306767e8b052…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 75 — Record R3-I027: one curved water tank in place of four flat panels, with its control stop and withdrawn claims

| field | value |
|---|---|
| Landed | 2026-10-14 16:43:53 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `342e02f76f44218b7e5abcace14c5b607e44fa08` → `d40a2bb787511f454f3d51ad49624f5cc6e2723c`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `d40a2bb787511f454f3d51ad49624f5cc6e2723c`, tree `04cf3d0b0379696e8345a9255b52bc9c7e38c9d5`, from branch `i027`, parent `7a891f119038b038aef146780fdae84e1c48b6fe`, governance `gov-f90e40042c0e` preserved. Unit `float-programme-r3`. |
| Rebase | law I.3c.5, mechanised: the signed object `0e991985dc64adaa9b2c954abb1cac8309d33dfb` was rebased off `e3a6f7b854ef0683fbcdacd6db330a7c3b94044b` onto the moved main `342e02f76f44218b7e5abcace14c5b607e44fa08`, landing as `d40a2bb787511f454f3d51ad49624f5cc6e2723c`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  29df1dbc = 1:  e068fb67 Add R3-I027 curved-tank candidate with control-stop record
2:  b13f1c02 = 2:  7a891f11 Correct I027 record: withdraw unsupported claims after sole canonical review
3:  0e991985 = 3:  d40a2bb7 Bind the final baseline 5ac2d4fe to run 3 only in R3-I027 provenance
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 0e991985d…` → rc=0, HONOURED-XO 0e991985dc64adaa9b2c954abb1cac8309d33dfb — the last record for this sha (store line 2000) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `e068fb67b` ← `gov-ack-e068fb67b13d` (reconcile record; trailer `gov-19286d12a7ce` is bound to another sha); `7a891f119` ← `gov-ack-7a891f119038` (reconcile record; trailer `gov-c2ea2394b1e8` is bound to another sha); `d40a2bb78` ← `gov-ack-d40a2bb78751` (reconcile record; trailer `gov-f90e40042c0e` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `047892769f1ef0bc…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 76 — Record R3-I029: the failed receiver-integrated split cassette, with unsupported claims withdrawn

| field | value |
|---|---|
| Landed | 2026-10-14 17:29:20 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `3e4ba19d705c992700caba9c03316ca2c4b7af4f` → `ea9830bfe03050ae40c1a19c2345df8a0c14e161`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `ea9830bfe03050ae40c1a19c2345df8a0c14e161`, tree `f98fc99b469186f4d7c25f12b006d0df5b237f50`, from branch `worker-r3-i029-restart-1014`, parent `5933b618c50f657da5b188768b15d6c414adcce8`, governance `gov-45e46a1fa783` preserved. Unit `float-programme-r3`. |
| Rebase | law I.3c.5, mechanised: the signed object `3965d8155ad48197ea141c8135f3d04cecfe7640` was rebased off `e3a6f7b854ef0683fbcdacd6db330a7c3b94044b` onto the moved main `3e4ba19d705c992700caba9c03316ca2c4b7af4f`, landing as `ea9830bfe03050ae40c1a19c2345df8a0c14e161`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  077a754d = 1:  5933b618 Record the failed receiver-integrated split cassette alternative
2:  3965d815 = 2:  ea9830bf Withdraw unsupported R3-I029 connection and section claims
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 3965d8155…` → rc=0, HONOURED-XO 3965d8155ad48197ea141c8135f3d04cecfe7640 — the last record for this sha (store line 2001) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `5933b618c` ← `gov-ack-5933b618c50f` (reconcile record; trailer `gov-eb03e0dd0e09` is bound to another sha); `ea9830bfe` ← `gov-ack-ea9830bfe030` (reconcile record; trailer `gov-45e46a1fa783` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `3fa61c6f8ca21180…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 77 — Record R3-I032: a four-tank continuous-transfer design stopped before calculation, with hand estimates withdrawn

| field | value |
|---|---|
| Landed | 2026-10-14 18:01:40 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `bef6780cc2a7e6a245cc975a4139d14edf283712` → `e11d78872107b5a5e277e79e50a3b63d0d2cab4f`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `e11d78872107b5a5e277e79e50a3b63d0d2cab4f`, tree `8906dc3eca7af6eb187cc881c798d7516239a9b8`, from branch `i032-successor-1014`, parent `45a425e390de1b847e56bc850fac63ee1654d4e4`, governance `gov-df234bce49f0` preserved. Unit `float-programme-r3`. |
| Rebase | law I.3c.5, mechanised: the signed object `725790d9031ffee2fc3abfc758b5486994051a0b` was rebased off `3e4ba19d705c992700caba9c03316ca2c4b7af4f` onto the moved main `bef6780cc2a7e6a245cc975a4139d14edf283712`, landing as `e11d78872107b5a5e277e79e50a3b63d0d2cab4f`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  a1a60eed = 1:  45a425e3 R3-I032 control stop: frozen successor design, guard-stopped before calculation
2:  725790d9 = 2:  e11d7887 I032 consolidated archival correction: withdraw hand-estimate claims and qualify attribution
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 725790d90…` → rc=0, HONOURED-XO 725790d9031ffee2fc3abfc758b5486994051a0b — the last record for this sha (store line 2002) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `45a425e39` ← `gov-ack-45a425e390de` (reconcile record; trailer `gov-424e913409f4` is bound to another sha); `e11d78872` ← `gov-ack-e11d78872107` (reconcile record; trailer `gov-df234bce49f0` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `9054c62680fa7884…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 78 — Record R3-I030: a circumferential transfer hoop that fails its screens, with unsupported strength claims withdrawn

| field | value |
|---|---|
| Landed | 2026-10-14 18:38:53 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `54114a7744e6769e7732476057c181cab545061f` → `7251787ed9aeac91ba8291627a69034e24552643`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `7251787ed9aeac91ba8291627a69034e24552643`, tree `e85eefe39e660226f22d8e4804d920c36c540211`, from branch `lead-i030-on-land76-1014`, parent `2ac2f156475629357963f89ee2b065bfc8cd56ef`, governance `gov-9aadcff57a2c` preserved. Unit `float-programme-r3`. |
| Rebase | law I.3c.5, mechanised: the signed object `f622e641c8697b6e1f116d7ac34990425b87e764` was rebased off `bef6780cc2a7e6a245cc975a4139d14edf283712` onto the moved main `54114a7744e6769e7732476057c181cab545061f`, landing as `7251787ed9aeac91ba8291627a69034e24552643`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  6a48239d = 1:  2ac2f156 research: measure circumferential transfer hoop
2:  f622e641 = 2:  7251787e research: withdraw unsupported local strength claims
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py f622e641c…` → rc=0, HONOURED-XO f622e641c8697b6e1f116d7ac34990425b87e764 — the last record for this sha (store line 2004) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `2ac2f1564` ← `gov-ack-2ac2f1564756` (reconcile record; trailer `gov-579fb0cf1e3e` is bound to another sha); `7251787ed` ← `gov-ack-7251787ed9ae` (reconcile record; trailer `gov-9aadcff57a2c` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `e798076ac43dc971…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 79 — Record R3-I031: a tapered-pot socket cartridge that fails, with construction claims withdrawn

| field | value |
|---|---|
| Landed | 2026-10-14 19:04:47 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `99379c8b480a5ac1689177c455fd3f0b0bf89618` → `dbbabb80727678117c16c70c28ddd85a0a84080a`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `dbbabb80727678117c16c70c28ddd85a0a84080a`, tree `f6a49fc04a303e839603d3703203d3fbcb440642`, from branch `lead-i031-on-land78-1014`, parent `dbe594c7f18832dc57ae60930c5a8313c4ed2303`, governance `gov-db12e90a269d` preserved. Unit `float-programme-r3`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py dbbabb807…` → rc=0, HONOURED-XO dbbabb80727678117c16c70c28ddd85a0a84080a — the last record for this sha (store line 2007) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `dbe594c7f` ← `gov-ack-dbe594c7f188` (reconcile record; trailer `gov-4c59ff59f0e8` is bound to another sha); `dbbabb807` ← `gov-ack-dbbabb807276` (reconcile record; trailer `gov-db12e90a269d` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `20ef92f711c10b67…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 80 — Record R3-I033: a triangulated frame that fails, with its full stock bill

| field | value |
|---|---|
| Landed | 2026-10-14 19:08:15 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `5d5a1ee219e65974db38845a5149d4962bec2c44` → `3a78caaf672b1af0e681aa12300cccfb0530c260`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `3a78caaf672b1af0e681aa12300cccfb0530c260`, tree `ad650ea876b86d337b1f38c53f488353b91f3e36`, from branch `lead-i033-on-i031-land78-1014`, parent `5d5a1ee219e65974db38845a5149d4962bec2c44`, governance `gov-65ae2b9b182b` preserved. Unit `float-programme-r3`. |
| Rebase | law I.3c.5, mechanised: the signed object `564d49d30dbcb6825c934e098ebbc0a6dbb174e3` was rebased off `dbbabb80727678117c16c70c28ddd85a0a84080a` onto the moved main `5d5a1ee219e65974db38845a5149d4962bec2c44`, landing as `3a78caaf672b1af0e681aa12300cccfb0530c260`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:

```
1:  564d49d3 = 1:  3a78caaf Record R3-I033 triangulated frame failure and full stock bill
``` |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 564d49d30…` → rc=0, HONOURED-XO 564d49d30dbcb6825c934e098ebbc0a6dbb174e3 — the last record for this sha (store line 2008) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `3a78caaf6` ← `gov-ack-3a78caaf672b` (reconcile record; trailer `gov-65ae2b9b182b` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `8f5d3871007dd85f…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 81 — Record R3-I035: segregated upper-tank exchange chambers, with capacity, mass and moment claims withdrawn

| field | value |
|---|---|
| Landed | 2026-10-14 19:32:41 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `0dd250ba6fc43bb69745287d9e82de207c7fc1e2` → `2694cba1a8887d0548c9e6aa816d271590b34276`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `2694cba1a8887d0548c9e6aa816d271590b34276`, tree `472860948c8cd7596cf67ac4faf54d74000c3a3e`, from branch `lead-i035-on-land80-1014`, parent `229935f7c9b2132b52efb31d0beb098eefe173d3`, governance `gov-5f5db3987f04` preserved. Unit `float-programme-r3`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 2694cba1a…` → rc=0, HONOURED-XO 2694cba1a8887d0548c9e6aa816d271590b34276 — the last record for this sha (store line 2009) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `229935f7c` ← `gov-ack-229935f7c9b2` (reconcile record; trailer `gov-dd2455ebdaac` is bound to another sha); `2694cba1a` ← `gov-ack-2694cba1a888` (reconcile record; trailer `gov-5f5db3987f04` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `e630928e91ba5912…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 82 — Record R3-I037: circular spacer fillets counted, with bookkeeping-centre and physical qualifications

| field | value |
|---|---|
| Landed | 2026-10-14 21:00:24 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `dc31909d854a7f5264e43b0fd31a4a8654646aed` → `c9b432654415f7d3d86db7817672ba6a8513dbeb`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `c9b432654415f7d3d86db7817672ba6a8513dbeb`, tree `b84b8c42cb3c99a53b398b5c64bd57203ef5696a`, from branch `lead-i037-on-land81-1014`, parent `c72b8987d74bb6fe43ce51e8d4572e5478cf18a7`, governance `gov-680797ca279c` preserved. Unit `float-programme-r3`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py c9b432654…` → rc=0, HONOURED-XO c9b432654415f7d3d86db7817672ba6a8513dbeb — the last record for this sha (store line 2013) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `c72b8987d` ← `gov-ack-c72b8987d74b` (reconcile record; trailer `gov-746e09b2f8f2` is bound to another sha); `c9b432654` ← `gov-ack-c9b432654415` (reconcile record; trailer `gov-680797ca279c` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `274f71bf3eeee743…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

## Landing 83 — Record R3-I036 as a qualified archive: six-segment wedge cord grip, corrected text, findings open

| field | value |
|---|---|
| Landed | 2026-10-14 21:36:40 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `bb3abface2cbcaa92adb2b39063ef3ac09b60b0d` → `0b9187bb24e142d39f9727f33a9fa4e2a331f372`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |
| The object | SIGNED `0b9187bb24e142d39f9727f33a9fa4e2a331f372`, tree `bfb2791d54d880ed65f6ec1e632f793511761286`, from branch `lead-i036-on-land82-1014`, parent `aca6dd0b9ba767c72861601162effb156c4920eb`, governance `gov-5604a9ae1ad0` preserved. Unit `float-programme-r3`. |
| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |
| Gate | `tools/land_gate.py 0b9187bb2…` → rc=0, HONOURED-XO 0b9187bb24e142d39f9727f33a9fa4e2a331f372 — the last record for this sha (store line 2015) is XO-SIGNED. (store `fo-verdicts.tsv`) |
| Governance records | `aca6dd0b9` ← `gov-ack-aca6dd0b9ba7` (reconcile record; trailer `gov-982d792678b7` is bound to another sha); `0b9187bb2` ← `gov-ack-0b9187bb24e1` (reconcile record; trailer `gov-5604a9ae1ad0` is bound to another sha). Each record names the landed sha as the commit it governed. |
| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |
| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |
| Order | sha256 `088cb01910eba173…` (informational) |
| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |

