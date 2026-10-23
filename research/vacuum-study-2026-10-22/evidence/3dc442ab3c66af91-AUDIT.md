# U4c block audit (a5473681a744-u4c-blk-1018152626), Ops, 2026-10-18 15:42

- One invocation: n1 test, unit simjob-a5473681a744-u4c-blk-1018152626-1.scope. Its launch.sh re-hashes to be8ab88f, the
  carded u4c-blk3-n1-test.sh. No n2, no X; x-001 does not exist.
- receipt.json 9995ee99 (489 B) matches the successor's validation 56920df0. rc 4, guard ok, collected, cleanup yes,
  closure_complete true, memory.peak 24477696 (digit-only), precheck MemAvailable 59.1 GB and PSI 0.00.
- guard.txt: cpu.max 200000 100000, memory.max 4 GiB, swap 0, stdin /dev/null, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, threads 2.
- Cause of rc 4 (stderr.txt): pytest walked up from src/ and took the seat checkout's pyproject.toml as inifile
  (rootdir = the seat workspace). Its addopts `-n --dist=loadgroup` need xdist, which autoload-off does not load. The
  card's argv (inherited from the muse brief) does not isolate pytest from an ancestor config. A rerun would need an
  explicit config isolation in the argv (e.g. `-c <empty ini in src>` or `--rootdir` plus `-o addopts=`) and a new card;
  no rerun is authorized.
- After: no invocation scope left; tests-001/home and tmp absent; no [private path]
- Hold simjob-u4c-blk-1018-hold.service (active since 15:26:33) stopped 15:42:18, rc 0, now not-found; the ledger no
  longer lists the grant (release-u4c.txt).
