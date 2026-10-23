# Audit and release: grok block 4f943bf0fef5-u4g-blk-1018142234 (re rpt-u4-grok-block-receipts-1018)

Both receipts verify: tests-001 cce6eb83 (442 B) and x-001 2258a433 (439 B). The sealed rows.jsonl (32d0057a, 406182 B)
was hash-verified only; it was not read.

| Invocation | Script used | Status | Unit | Guard | memory.peak | homeunpublished-local-ref:e9671acd244849c5 | Precheck |
|---|---|---|---|---|---|---|---|
| n1 test (tests-001) | v2 u4g-blk-n1-test.sh 088b844d | DONE rc 0 | simjob-4f943bf0fef5-u4g-blk-1018142234-1.scope, collected (not-found) | OK: cpu.max 200000 100000, memory.max 4294967296, swap 0, stdin /dev/null | 15003648 | absent | MemAvailable 63360573440, PSI 0.00 |
| n2 X (x-001) | v2 u4g-blk-n2-x.sh 19d33b43 | DONE rc 0 | simjob-4f943bf0fef5-u4g-blk-1018142234-2.scope, collected | OK, same controls | 14352384 | absent | MemAvailable 63517241344, PSI 0.05 |

- **Sequence legal:** test pass, then X as invocation 2. No tests-002 and no third invocation. No scope was left.
- **Version:** both ran the v2 scripts, the card current at 14:28–14:29. v3 was delivered at 14:30:29. By v3's closure
  criteria both are complete: collected, GUARD OK, memory.peak present, and home and tmp verified absent on disk.
- **Ops defect (receipt UTC strings):** this host's `date` is uutils 0.8.0. It ignores the `%6N` width and prints the
  full nanosecond count, unpadded. So tests-001 start `21:28:21.69239373Z` means 21:28:21.069239373, which is before its
  end at 21:28:21.273789947. Decode the fraction as nanoseconds left-padded to 9 digits. The monotonic fields are correct.
  The same applies to launch.log stamps in the U3 v2 scripts.
- **Release:** at 14:32:17 Ops stopped simjob-u4g-blk-1018-hold.service (it had been active since 14:22:41; stop rc 0;
  it is now not-found). The ledger then counted only muse's block: 2 cores, 4 GiB.
