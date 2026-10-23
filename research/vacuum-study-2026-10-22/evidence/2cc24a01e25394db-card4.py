"""U3 repair-preparation job card (ord-sciences-g1-ops-u3-repair-and-a3-admission-1018, under the CO's
rpt-co27-sci-u3-group-a-ledger-disposition-fix-a3-1018): ONE bounded regeneration plus ONE equality check, run in the
retained A/src under the qualified v3 service profile (card3: real short canonical TMP, caps, guards, collection).
Rendered from card3.render, then four exact substitutions, each asserted to occur once:
  1. pre-run source guard: the worktree differs from the index in EXACTLY the reviewed shard, at its pinned bytes;
  2. payload: /bin/sh -c '<regenerate> && <regenerate --check>' (the two enumerated commands, nothing else);
  3. PASS requires the post-run worktree delta to be EXACTLY the shard plus the two generated ledger files;
  4. PASS keeps SRC (governance and A3 use it); only tmp, home, bin and the short TMP are removed.
  python3 card4.py        writes group-v4-RP.sh and prints its sha256"""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import card3
D = card3.D
SHARD = 'research/analysis/float-claims/vacuum-float-machinery-1017.json'
SHARD_SHA = 'eeffae43aa46c12d9efed29766ca2b6b277f3e47d1f7976aeb5c1379d075bc77'
POST = ['docs/FLOAT-LEDGER.md', SHARD, 'research/analysis/float-ledger.json']          # sorted
CHAIN = "/bin/sh -c 'ref-81e2f24e4e80426e80f0 -B tools/float_ledger.py && ref-81e2f24e4e80426e80f0 -B tools/float_ledger.py --check'"


def render4(p, shard=SHARD, shard_sha=SHARD_SHA, post=POST, chain=CHAIN):
    s = card3.render(dict(p, targets='REPAIRCHAIN'))
    def rep(old, new):
        nonlocal s
        assert s.count(old) == 1, (old[:70], s.count(old))
        s = s.replace(old, new)
    rep('timeout 60 git -C "$SRC" diff --quiet || refuse 12 "worktree differs from index"',
        f'dl=$(timeout 60 git -C "$SRC" diff --name-only) && [ "$dl" = {card3.q(shard)} ] || refuse 12 "worktree delta [$dl] is not exactly the reviewed shard"\n'
        f'echo "{shard_sha}  $SRC/{shard}" | sha256sum -c || refuse 12 "reviewed shard bytes differ"')
    rep('echo "source HEAD $h tree $t entries $n clean"', 'echo "source HEAD $h index-tree $t entries $n; worktree delta exactly the reviewed shard"')
    rep('ref-994275a3cda2dd1ca6ee --no-print-directory REPAIRCHAIN', chain)
    rep('''  timeout 120 git -C "$CLONE" worktree remove --force "$SRC"; echo "worktree remove rc=$?"
  [ ! -e "$SRC" ] || finish INCOMPLETE_CLEANUP 31 "manager_rc=0 success collected, but src removal failed"
  echo "removed src"; finish PASS 0 "manager_rc=0 success collected; tmp, home, bin, short TMP and src removed"''',
        f'''  d2=$(timeout 60 git -C "$SRC" diff --name-only | LC_ALL=C sort | tr '\\n' ' ') || finish FAIL 22 "post-run delta unreadable"
  echo "post-run worktree delta: $d2"
  [ "$d2" = {card3.q(' '.join(post) + ' ')} ] || finish FAIL 22 "post-run delta [$d2] is not exactly the three allowed paths"
  finish PASS 0 "manager_rc=0 regenerate and check passed; delta exactly the three allowed paths; tmp, home, bin and short TMP removed; src kept"''')
    rep('# U3 gate group', '# U3 REPAIR-PREPARATION job (regenerate once, check once) as group')
    return s


if __name__ == '__main__':
    p = dict(card3.COMMON, group='RP', src_group='A', cache='u3rp', unit='u3gate-rp-1018.service',
             cores=4, mem=16, tasks=4096, runtime=1200, targets='REPAIRCHAIN')
    f = os.path.join(D, 'group-v4-RP.sh'); open(f, 'w').write(render4(p))
    print(os.path.basename(f), hashlib.sha256(open(f, 'rb').read()).hexdigest(), os.path.getsize(f))
