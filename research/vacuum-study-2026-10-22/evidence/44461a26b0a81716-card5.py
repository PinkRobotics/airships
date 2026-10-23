"""U3 repair-preparation job card v5 (ord-sciences-g1-ops-u3-rp-allowed-delta-card-fix-1018): corrects v4-RP.
Same qualified v3 service, payload (regenerate && --check), controls, collection, cleanup and SRC retention; governance is
B's in-seat Helm door, outside this card. Rendered from card3.render, then exact substitutions (each asserted once):
  1. pre-run guard: every Git call's exit status is checked BEFORE its output is parsed; the worktree delta is exactly
     the reviewed shard at its pinned bytes;
  2. payload: /bin/sh -c '<regenerate> && <regenerate --check>';
  3. post-run guard (before PASS), each Git call status-checked first: HEAD unchanged; index write-tree unchanged;
     nothing untracked; the shard still at its pinned bytes; the worktree delta CONTAINS the shard and is otherwise a
     subset of the two generated ledger files (either, both or neither may change; no changed bytes demanded);
  4. PASS keeps SRC.
  python3 card5.py        writes group-v5-RP.sh, prints its sha256 and the whole-command worst-case bound"""
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import card3
D = card3.D
SHARD = 'research/analysis/float-claims/vacuum-float-machinery-1017.json'
SHARD_SHA = 'eeffae43aa46c12d9efed29766ca2b6b277f3e47d1f7976aeb5c1379d075bc77'
GENERATED = ['docs/FLOAT-LEDGER.md', 'research/analysis/float-ledger.json']
CHAIN = "/bin/sh -c 'ref-81e2f24e4e80426e80f0 -B tools/float_ledger.py && ref-81e2f24e4e80426e80f0 -B tools/float_ledger.py --check'"


def render5(p, shard=SHARD, shard_sha=SHARD_SHA, generated=GENERATED, chain=CHAIN):
    s = card3.render(dict(p, targets='REPAIRCHAIN'))
    q = card3.q
    def rep(old, new):
        nonlocal s
        assert s.count(old) == 1, (old[:70], s.count(old))
        s = s.replace(old, new)
    # 1. pre-run source guards: status first, then parse
    rep('h=$(timeout 60 git -C "$SRC" rev-parse HEAD) && [ "$h" = "$HEAD" ] || refuse 12 "HEAD [$h]"',
        'h=$(timeout 60 git -C "$SRC" rev-parse HEAD) || refuse 12 "git rev-parse failed"; [ "$h" = "$HEAD" ] || refuse 12 "HEAD [$h]"')
    rep('top=$(timeout 60 git -C "$SRC" rev-parse --show-toplevel) && [ "$top" = "$SRC" ] || refuse 12 "toplevel [$top]"',
        'top=$(timeout 60 git -C "$SRC" rev-parse --show-toplevel) || refuse 12 "git toplevel failed"; [ "$top" = "$SRC" ] || refuse 12 "toplevel [$top]"')
    rep('t=$(timeout 60 git -C "$SRC" write-tree) && [ "$t" = "$TREE" ] || refuse 12 "write-tree [$t]"',
        't=$(timeout 60 git -C "$SRC" write-tree) || refuse 12 "git write-tree failed"; [ "$t" = "$TREE" ] || refuse 12 "write-tree [$t]"')
    rep('timeout 60 git -C "$SRC" diff --quiet || refuse 12 "worktree differs from index"',
        f'dl=$(timeout 60 git -C "$SRC" diff --name-only) || refuse 12 "git diff failed"\n'
        f'[ "$dl" = {q(shard)} ] || refuse 12 "worktree delta [$dl] is not exactly the reviewed shard"\n'
        f'echo "{shard_sha}  $SRC/{shard}" | sha256sum -c || refuse 12 "reviewed shard bytes differ"')
    rep('u=$(timeout 60 git -C "$SRC" ls-files --others --exclude-standard) && [ -z "$u" ] || refuse 12 "untracked [$u]"',
        'u=$(timeout 60 git -C "$SRC" ls-files --others --exclude-standard) || refuse 12 "git ls-files failed"; [ -z "$u" ] || refuse 12 "untracked [$u]"')
    rep('n=$(timeout 60 git -C "$SRC" ls-files | wc -l) && [ "$n" = "$ENTRIES" ] || refuse 12 "entries [$n]"',
        'lf=$(timeout 60 git -C "$SRC" ls-files) || refuse 12 "git ls-files failed"; n=$(printf "%s\\n" "$lf" | grep -c . | head -1); [ "$n" = "$ENTRIES" ] || refuse 12 "entries [$n]"')
    rep('echo "source HEAD $h tree $t entries $n clean"', 'echo "source HEAD $h index-tree $t entries $n; worktree delta exactly the reviewed shard"')
    # 2. payload
    rep('ref-994275a3cda2dd1ca6ee --no-print-directory REPAIRCHAIN', chain)
    # 3. post-run guard, then PASS keeping SRC
    allowed = ' '.join([shard] + generated)
    rep('''  timeout 120 git -C "$CLONE" worktree remove --force "$SRC"; echo "worktree remove rc=$?"
  [ ! -e "$SRC" ] || finish INCOMPLETE_CLEANUP 31 "manager_rc=0 success collected, but src removal failed"
  echo "removed src"; finish PASS 0 "manager_rc=0 success collected; tmp, home, bin, short TMP and src removed"''',
        f'''  stamp postguard
  h2=$(timeout 60 git -C "$SRC" rev-parse HEAD) || finish FAIL 22 "post-run git rev-parse failed"
  [ "$h2" = "$HEAD" ] || finish FAIL 22 "post-run HEAD drift [$h2]"
  t2=$(timeout 60 git -C "$SRC" write-tree) || finish FAIL 22 "post-run git write-tree failed"
  [ "$t2" = "$TREE" ] || finish FAIL 22 "post-run index drift [$t2]"
  u2=$(timeout 60 git -C "$SRC" ls-files --others --exclude-standard) || finish FAIL 22 "post-run git ls-files failed"
  [ -z "$u2" ] || finish FAIL 22 "post-run untracked [$u2]"
  echo "{shard_sha}  $SRC/{shard}" | sha256sum -c || finish FAIL 22 "post-run shard drift"
  d2=$(timeout 60 git -C "$SRC" diff --name-only) || finish FAIL 22 "post-run git diff failed"
  echo "post-run worktree delta: $(printf '%s ' $d2)"
  python3 -I -c "import sys; d=set(sys.argv[1].split()); a=set(sys.argv[2].split()); sys.exit(0 if sys.argv[3] in d and d <= a else 1)" "$d2" {q(allowed)} {q(shard)} \\
    || finish FAIL 22 "post-run delta [$(printf '%s ' $d2)] must contain the shard and otherwise only the generated ledger files"
  finish PASS 0 "manager_rc=0 regenerate and check passed; HEAD, index, untracked and shard unchanged; delta within the allowed set; tmp, home, bin and short TMP removed; src kept"''')
    rep('# U3 gate group', '# U3 REPAIR-PREPARATION job v5 (regenerate once, check once) as group')
    return s


def worst_case_seconds(script):
    """Sum every bounded step: each `timeout [--kill-after=Ks] Ns` outside the unit (N + K), the outer manager bound with
    its kill-after, and nothing for the payload's own inner timeout (inside the outer bound)."""
    total = 0; lines = script.split('\n'); in_unit = False; mult = 1
    for ln in lines:
        if 'systemd-run --user --wait' in ln:
            m = re.search(r'timeout --kill-after=(\d+)s (\d+)s systemd-run', ln); total += int(m[1]) + int(m[2]); in_unit = True; continue
        if in_unit:
            if ln.strip().startswith('> "$R/systemd-run.log"'): in_unit = False
            continue
        if ln.lstrip().startswith('for d in '):
            mult = len(re.findall(r'"[^"]+"|\S+', ln.split(' in ', 1)[1].rsplit('; do', 1)[0])); continue
        if ln.strip() == 'done':
            mult = 1; continue
        for m in re.finditer(r'timeout (?:--kill-after=(\d+)s )?(\d+)s? ', ln):
            total += mult * (int(m[2]) + (int(m[1]) if m[1] else 0))
    return total


if __name__ == '__main__':
    p = dict(card3.COMMON, group='RP', src_group='A', cache='u3rp', unit='u3gate-rp-1018.service',
             cores=4, mem=16, tasks=4096, runtime=1200, targets='REPAIRCHAIN')
    text = render5(p)
    f = os.path.join(D, 'group-v5-RP.sh'); open(f, 'w').write(text)
    print(os.path.basename(f), hashlib.sha256(text.encode()).hexdigest(), len(text.encode()),
          'worst-case bounded seconds', worst_case_seconds(text), 'socket', len('unpublished-local-ref:20a620f831079f49') + card3.SOCKET_TAIL)
