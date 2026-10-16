"""The lander's attestation table is history by shape only when it is exact."""
from pathlib import Path
import sys
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


if __name__ == '__main__':
    unittest.main()
