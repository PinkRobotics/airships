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

