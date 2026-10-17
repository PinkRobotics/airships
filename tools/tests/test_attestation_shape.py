"""The lander's attestation table is history by shape only when it is exact."""
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import check_float_ledger as gate
import float_claims

ATT = 'docs/governance/landing-attestations.md'
EXACT = (
    'Landed', 'The object', 'Pre-checks under the lock', 'Gate',
    'Governance records', 'Evidence before landing', 'Tool', 'Order', 'Foreign route',
)


def table(fields):
    rows = ['| field | value |', '|---|---|']
    for name in fields:
        rows.append(f'| {name} | Unit `ci-float-claims-1015` keeps this float marker. |')
    return '\n'.join(rows)


def under(heading, raw):
    return f'{heading}\n\n{raw}\n'


class AttestationShape(unittest.TestCase):
    def test_exact_table_passes_without_hand_record(self):
        path = ROOT / ATT
        page = path.read_text(encoding='utf-8')
        blocks = [block for block in gate.source_blocks(path) if block[0] == 1320]
        self.assertEqual(len(blocks), 1)
        line, text, raw = blocks[0]
        self.assertTrue(gate.attestation_table_by_shape(ATT, line, raw, page))
        self.assertNotIn(float_claims.key_of(text), (ROOT / 'research/analysis/float-claims/docs.json').read_text(encoding='utf-8'))
        synthetic = table(EXACT)
        self.assertTrue(gate.attestation_table_by_shape(
            ATT, 3, synthetic, under('## Landing 997 — Shape rule exact table', synthetic)))
        numbered = under('## Landing 997 — Shape rule 1', synthetic)
        self.assertFalse(gate.attestation_table_by_shape(ATT, 3, synthetic, numbered))

    def test_renamed_row_fails(self):
        raw = table(('Arrived',) + EXACT[1:])
        self.assertFalse(gate.attestation_table_by_shape(
            ATT, 3, raw, under('## Landing 996 — Shape rule renamed row', raw)))

    def test_extra_row_fails(self):
        raw = table(EXACT + ('Note',))
        self.assertFalse(gate.attestation_table_by_shape(
            ATT, 3, raw, under('## Landing 995 — Shape rule extra row', raw)))

    def test_table_elsewhere_fails(self):
        raw = table(EXACT)
        headed = under('## Landing 997 — Shape rule exact table', raw)
        self.assertFalse(gate.attestation_table_by_shape('docs/FLOAT.md', 3, raw, headed))
        prose = 'A note about the record.\n\n' + raw + '\n'
        self.assertFalse(gate.attestation_table_by_shape(ATT, 3, raw, prose))

    def test_optional_lander_rows_stay_in_the_writer_positions(self):
        no_records = (
            'Landed', 'The object', 'Pre-checks under the lock', 'Gate',
            'Evidence before landing', 'Tool', 'Order', 'Foreign route',
        )
        with_rebase = (
            'Landed', 'The object', 'Rebase', 'Pre-checks under the lock', 'Gate',
            'Governance records', 'Evidence before landing', 'Tool', 'Order', 'Foreign route',
        )
        self.assertTrue(gate.exact_lander_row_set(no_records))
        self.assertTrue(gate.exact_lander_row_set(with_rebase))
        self.assertTrue(gate.exact_lander_row_set(EXACT))
        self.assertFalse(gate.exact_lander_row_set(('Landed', 'The object', 'Rebase')))
        self.assertFalse(gate.exact_lander_row_set(EXACT[:4] + ('Rebase',) + EXACT[4:]))


# The lander's own public entries: helm ship/tools/land.py (sha256 3f4d36dd...) _public_attestation_entry,
# rendered from a patch-identical two-commit rebase of d7b704f5 onto 19533a82 in a scratch clone. Neither was
# landed or pushed. The Rebase cell is the provenance sentence, one blank line and the fenced range-diff.
REBASED_ENTRY = (
    '\n'
    '\n'
    '## Landing 993 — Rebase cell shape rule fixture\n'
    '\n'
    '| field | value |\n'
    '|---|---|\n'
    '| Landed | 2026-10-17 09:03:00 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `19533a82d619a4af9c13b99f9fe46944f5249281` → `69acb28abe7a1625f3189d7360eafb74130268dc`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |\n'
    '| The object | SIGNED `69acb28abe7a1625f3189d7360eafb74130268dc`, tree `38a501f41a82060174518573edf796559fd6512b`, from branch `rc-fixture-1017`, parent `c830c2a75946339e7aef1e19fafa4e266902a521`, governance `gov-000000000000` preserved. Unit `ci-float-rebase-cell-1017`. |\n'
    "| Rebase | law I.3c.5, mechanised: the signed object `41dc0953d010d11a9c8caf1210810edd3101c884` was rebased off `d7b704f5647e658e5334930477ee45def715c615` onto the moved main `19533a82d619a4af9c13b99f9fe46944f5249281`, landing as `69acb28abe7a1625f3189d7360eafb74130268dc`. `git range-diff` showed every pair `=`; each new commit was re-governed mechanically with that pair as its reason. The gate below honours the OLD sha's EXISTING record — no fresh signature was asked or given. Range-diff:\n"
    '\n'
    '```\n'
    '1:  06378fbf = 1:  c830c2a7 Fixture: the float rebase cell keeps its full range-diff\n'
    '2:  41dc0953 = 2:  69acb28a Fixture: a second patch-identical pair in the range-diff\n'
    '``` |\n'
    '| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |\n'
    '| Gate | `tools/land_gate.py 41dc0953d…` → rc=0, HONOURED-XO 41dc0953d010d11a9c8caf1210810edd3101c884 — the last record for this sha (store line 1) is XO-SIGNED. (store `fo-verdicts.tsv`) |\n'
    '| Governance records | `c830c2a75` ← `gov-ack-c830c2a75946` (reconcile record; trailer `gov-000000000000` is bound to another sha); `69acb28ab` ← `gov-ack-69acb28abe7a` (reconcile record; trailer `gov-000000000000` is bound to another sha). Each record names the landed sha as the commit it governed. |\n'
    '| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck ledgercheck portcheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |\n'
    '| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |\n'
    '| Order | sha256 `0000000000000000…` (informational) |\n'
    '| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |\n'
)
PLAIN_ENTRY = (
    '\n'
    '\n'
    '## Landing 992 — Plain shape rule fixture\n'
    '\n'
    '| field | value |\n'
    '|---|---|\n'
    '| Landed | 2026-10-17 09:03:00 PDT by the lander using `ship/tools/land.py`, a pure **FAST-FORWARD**: main `19533a82d619a4af9c13b99f9fe46944f5249281` → `69acb28abe7a1625f3189d7360eafb74130268dc`; pushed main-only, non-force, origin verified equal. The signed sha IS main; the landed tree equals the signed tree by identity. |\n'
    '| The object | SIGNED `69acb28abe7a1625f3189d7360eafb74130268dc`, tree `38a501f41a82060174518573edf796559fd6512b`, from branch `rc-fixture-1017`, parent `c830c2a75946339e7aef1e19fafa4e266902a521`, governance `gov-000000000000` preserved. Unit `ci-float-rebase-cell-1017`. |\n'
    '| Pre-checks under the lock | primary on main; HEAD == main == the named base; origin/main == the named base; merge-base(main, candidate) == main and candidate != main; tree == the named tree; Helm-Audit-ID on every commit in base..candidate; tracked tree clean; object imported exact from the source. |\n'
    '| Gate | `tools/land_gate.py 41dc0953d…` → rc=0, HONOURED-XO 41dc0953d010d11a9c8caf1210810edd3101c884 — the last record for this sha (store line 1) is XO-SIGNED. (store `fo-verdicts.tsv`) |\n'
    '| Governance records | `c830c2a75` ← `gov-ack-c830c2a75946` (reconcile record; trailer `gov-000000000000` is bound to another sha); `69acb28ab` ← `gov-ack-69acb28abe7a` (reconcile record; trailer `gov-000000000000` is bound to another sha). Each record names the landed sha as the commit it governed. |\n'
    '| Evidence before landing | `PYTHONDONTWRITEBYTECODE=1 make readmecheck linkcheck buildercheck claimsrestore claimscheck ledgercheck portcheck` rc=0 (environment PATH set to host paths, not shown) (gate timeout 1200 s, named by the order) |\n'
    '| Tool | `ship/tools/land.py` sha256 `3f4d36dddae3efb1…` from helm (informational) |\n'
    '| Order | sha256 `0000000000000000…` (informational) |\n'
    '| Foreign route | order-named preserve_paths `—` pinned — (the attestation post-conditions below refuse any mismatch); record `docs/governance/landing-attestations.md`. |\n'
)
REBASED_HEADING = '## Landing 993 — Rebase cell shape rule fixture'
# The same entry with the Rebase cell on one line: the range-diff pairs inline, no blank line, no fence.
REBASED_ONE_LINE = re.sub(r'Range-diff:\n\n```\n(.*?)\n``` \|', lambda m: 'Range-diff: ' + ' '.join(m[1].split('\n')) + ' |',
                          REBASED_ENTRY, flags=re.S)


def pieces(page, rel=ATT):
    """(line, raw) of every inventoried table block of `page` at `rel`, through the gate's own splitter."""
    with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as tmp:
        root = Path(tmp)
        path = root / rel
        path.parent.mkdir(parents=True)
        path.write_text(page, encoding='utf-8')
        previous, gate.ROOT = gate.ROOT, root
        try:
            blocks = list(gate.source_blocks(path))
        finally:
            gate.ROOT = previous
    return [(line, raw) for line, _text, raw in blocks if raw.lstrip().startswith(('|', '```'))]


def verdicts(page, rel=ATT):
    return [gate.attestation_table_by_shape(rel, line, raw, page) for line, raw in pieces(page, rel)]


class RebasedAttestationShape(unittest.TestCase):
    """The lander's fenced Rebase cell, and nothing that only resembles it."""

    def test_lander_rebased_table_passes_without_hand_record(self):
        found = pieces(REBASED_ENTRY)
        # The blank line inside the Rebase cell splits the one table into two inventoried blocks.
        self.assertEqual(len(found), 2)
        self.assertEqual(verdicts(REBASED_ENTRY), [True, True])
        fence = found[1][1]
        for pair in ('1:  06378fbf = 1:  c830c2a7', '2:  41dc0953 = 2:  69acb28a'):
            self.assertIn(pair, fence)
        docs = (ROOT / 'research/analysis/float-claims/docs.json').read_text(encoding='utf-8')
        for _line, raw in found:
            self.assertNotIn(float_claims.key_of(gate.clean(raw)), docs)
        # A rebased table the lander wrote into the record itself (landing 80) reads the same way.
        page = (ROOT / ATT).read_text(encoding='utf-8')
        real = [block for block in gate.source_blocks(ROOT / ATT) if block[0] == 1203]
        self.assertEqual(len(real), 1)
        self.assertTrue(gate.attestation_table_by_shape(ATT, 1203, real[0][2], page))

    def test_unchanged_table_without_rebase_passes(self):
        self.assertEqual(len(pieces(PLAIN_ENTRY)), 1)
        self.assertEqual(verdicts(PLAIN_ENTRY), [True])

    def test_renamed_first_field_fails(self):
        self.assertEqual(verdicts(REBASED_ENTRY.replace('| Landed |', '| Arrived |')), [False, False])

    def test_extra_field_fails(self):
        page = REBASED_ENTRY + '| Note | Unit `ci-float-claims-1015` keeps this float marker. |\n'
        self.assertEqual(verdicts(page), [False, False])

    def test_same_table_in_another_file_fails(self):
        self.assertEqual(verdicts(REBASED_ENTRY, 'docs/FLOAT.md'), [False, False])

    def test_figure_bearing_heading_fails(self):
        page = REBASED_ENTRY.replace(REBASED_HEADING, '## Landing 993 — Rebase cell shape rule 3')
        self.assertEqual(verdicts(page), [False, False])

    def test_blank_line_inside_another_cell_fails(self):
        page = REBASED_ENTRY.replace(' preserved. Unit', ' preserved.\n\nUnit')
        found = verdicts(page)
        self.assertTrue(found)
        self.assertNotIn(True, found)

    def test_rebase_without_exact_provenance_or_shape_fails(self):
        variants = {
            'altered provenance': REBASED_ENTRY.replace('every pair `=`', 'every pair `!`'),
            'one line': REBASED_ONE_LINE,
            'changed pair': REBASED_ENTRY.replace(' = 2:  69acb28a', ' ! 2:  69acb28a'),
            'no pairs': re.sub(r'\n[12]:  [0-9a-f]+ = [^\n]*', '', REBASED_ENTRY),
            'open fence': REBASED_ENTRY.replace('``` |', '```'),
            'text after the table': REBASED_ENTRY.rstrip('\n') + '\nA line written straight after the table.\n',
        }
        self.assertNotEqual(REBASED_ONE_LINE, REBASED_ENTRY)
        for name, page in variants.items():
            with self.subTest(variant=name):
                found = verdicts(page)
                self.assertTrue(found)
                self.assertNotIn(True, found)

    def test_block_passes_only_as_its_own_text(self):
        # The splitter blanks style markup, so the second block's inventoried text is no longer the
        # table's text in the file; that block is refused while the first, unchanged, still passes.
        page = REBASED_ENTRY.replace('(store `fo-verdicts.tsv`)', '(store `fo-verdicts.tsv`) <style>p{}</style>')
        self.assertEqual(verdicts(page), [True, False])


if __name__ == '__main__':
    unittest.main()
