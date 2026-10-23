"""U4 published-basis map: test + render cards (ord-sciences-g1-ops-u4-published-basis-map-block-1018), adapted from the
qualified u4c2 cards (u4card5.render5 lineage: u4card3.render, guard u4guard3.sh 84a24f19) with ONLY the brief's allowed
adaptations, each asserted once:
  identities: root = C's u4-published-basis-map-1018, src = root/src, dirs tests-001 (test) and map-001 (render),
    hold simjob-u4pb-blk-1018-hold.service, scopes simjob-<grant>-<n>.scope;
  pins: python3.14, the guard and the complete nine-file source inventory from SOURCE-FREEZE.json (d314c7b9); the old
    tests-001/receipt.json pin of the u4c2 lineage is removed;
  inventory: after hashing src, the hash list must equal the frozen nine-line inventory exactly (refuse 12);
  sequence: n1 = global 4 = test; n2 = global 5 = render, only after tests-001 shows closure_complete and rc 0, and only if
    its source hashes equal tests-001's byte for byte (refuse 16);
  argv: exactly SOURCE-FREEZE.json test_argv and render_argv; render refuses if its --output-dir already exists;
  receipt: global_n 4 / 5, kind test / render.
Everything else is u4c2: caps 2 CPU / 4 GiB / swap 0 / threads 2, env -i, stdin /dev/null, autoload off, pinned pytest
9.0.2, owned 0700 HOME/TMP, the precheck, collection, cleanup and the typed receipt.
  python3 u4card6.py template            write hold-u4pb.sh, u4pb-blk-n1-test.template.sh, u4pb-blk-n2-render.template.sh
  python3 u4card6.py scripts <grant>     write the final scripts and assert they equal the templates with @GRANT@ replaced"""
import hashlib, json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, 'unpublished-local-ref:20b04395a2a7b036')
import u4card3 as c3
ROOT = 'unpublished-local-ref:f56d0a128c360347'
FREEZE = ROOT + '/SOURCE-FREEZE.json'; FREEZE_SHA = 'd314c7b9a2461dd47267ca5f57a9358e6fadd1d4d77428504c4a48f7ac703f30'
F = json.load(open(FREEZE)); assert hashlib.sha256(open(FREEZE, 'rb').read()).hexdigest() == FREEZE_SHA
INV = sorted((x['name'], x['sha256']) for x in F['exact_inventory']); assert len(INV) == 9
EXPECT_LIST = ''.join(f'{s}  ./{n}\n' for n, s in INV)
HOLD = 'simjob-u4pb-blk-1018-hold.service'; PLACEHOLDER = '@GRANT@'
OUT = F['render_argv'][F['render_argv'].index('--output-dir') + 1]
STEPS = [('n1-test', 1, 4, 'test', 'tests-001', None, None, F['test_argv']),
         ('n2-render', 2, 5, 'render', 'map-001', 'tests-001', '0', F['render_argv'])]

def render6(grant, tag, n, g, kind, inv, needs, needs_rc, argv):
    p = dict(root=ROOT, inv=inv, n=n, kind=kind, unit=f'simjob-{grant}-{n}.scope', hold=HOLD, grant=grant, argv=argv,
             x_out=OUT if kind == 'render' else None, plugin=1, pytest='9.0.2', guard=c3.GUARD2, uid=1000, needs=needs,
             needs_rc=needs_rc, scope_prefix=f'simjob-{grant}')
    s = c3.render(p)
    def rep(old, new):
        nonlocal s
        assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new)
    gsha = hashlib.sha256(open(c3.GUARD2, 'rb').read()).hexdigest()
    rep(f'{gsha}  {c3.GUARD2}\nPINS', f'{gsha}  {c3.GUARD2}\n' + ''.join(f'{s_}  {ROOT}/src/{n_}\n' for n_, s_ in INV) + 'PINS')
    rep(f'n={n}, kind=', f'n={n}, global_n={g}, kind=')
    rep(f'# U4 block invocation n={n} ({kind})', f'# U4 block invocation n={n} = global {g} ({kind}, published-basis map card u4pb)')
    hl = "| xargs -0 -r sha256sum ) > \"$I/source-sha256.txt\" || refuse 12 \"source hashing failed\""
    extra = ('\n[ "$(LC_ALL=C sort "$I/source-sha256.txt")" = "$(printf \'%s\' ' + c3.v1.q(EXPECT_LIST) + ' | LC_ALL=C sort)" ] || refuse 12 "source inventory is not exactly the frozen nine files"')
    if kind == 'render':
        extra += f'\ncmp -s "$I/source-sha256.txt" {c3.v1.q(ROOT + "/tests-001/source-sha256.txt")} || refuse 16 "render source differs from the passing test tests-001 source"'
    rep(hl, hl + extra)
    return s

def bounds(s):
    t = 0; mult = 1
    for ln in s.split('\n'):
        if ln.strip().startswith('for d in tmp home; do'): mult = 2; continue
        if ln.strip() == 'done': mult = 1; continue
        for m in re.finditer(r'timeout (?:--kill-after=(\d+)s )?(\d+)s? ', ln): t += mult * (int(m[2]) + int(m[1] or 0))
    return t

def write(name, text):
    f = os.path.join(D, name); assert not os.path.exists(f), f; open(f, 'w').write(text); return f

if __name__ == '__main__':
    if sys.argv[1] == 'template':
        text, unit = c3.hold_line('pb'); assert unit == HOLD
        write('hold-u4pb.sh', text); print('hold-u4pb.sh', hashlib.sha256(text.encode()).hexdigest())
        for tag, n, g, kind, inv, needs, nrc, argv in STEPS:
            t = render6(PLACEHOLDER, tag, n, g, kind, inv, needs, nrc, argv); write(f'u4pb-blk-{tag}.template.sh', t)
            print(f'u4pb-blk-{tag}.template.sh', hashlib.sha256(t.encode()).hexdigest(), len(t.encode()), 'placeholders', t.count(PLACEHOLDER), 'bounded', bounds(t))
    else:
        grant = sys.argv[2]; assert re.fullmatch(r'[0-9a-f]{12}-u4pb-blk-\d{10}', grant), grant
        for tag, n, g, kind, inv, needs, nrc, argv in STEPS:
            t = render6(grant, tag, n, g, kind, inv, needs, nrc, argv)
            tpl = open(os.path.join(D, f'u4pb-blk-{tag}.template.sh')).read()
            assert t == tpl.replace(PLACEHOLDER, grant) and PLACEHOLDER not in t
            write(f'u4pb-blk-{tag}.sh', t); print(f'u4pb-blk-{tag}.sh', hashlib.sha256(t.encode()).hexdigest(), len(t.encode()))
