"""Counterexamples for editorial record bindings; no feeds or physical tests."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import gen_assembly_prose as assembly

class AssemblyProse(unittest.TestCase):
    def test_current_counts_and_all_failures(self):
        text=assembly.outputs()[assembly.FILE]
        self.assertIn('12 of the 16 proofs pass',text)
        self.assertIn('P12 passes',text)
        for name in ('P8','P11','P13','P16'):self.assertIn('| '+name+' —',text)
        self.assertIn('18 frozen defects',text)
    def test_changed_report_status_cannot_hide_in_summary(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as folder:
            root=Path(folder)
            for file in (assembly.FILE,'research/geometry/nodes/assembly.json','research/geometry/nodes/contract.json'):
                p=root/file;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((assembly.ROOT/file).read_bytes())
            p=root/'research/geometry/nodes/assembly.json';j=json.loads(p.read_text());j['proofs'][0]['passed']=False;p.write_text(json.dumps(j))
            with self.assertRaises(AssertionError):assembly.outputs(root)
    def test_typed_counts_are_rejected(self):
        result=assembly.outputs()[assembly.FILE]
        self.assertNotIn('The five proofs still failing',result)

from check_cell_evidence import evidence_errors
class EvidenceWords(unittest.TestCase):
    def setUp(self):self.ledger=json.loads((assembly.ROOT/'research/analysis/float-ledger.json').read_text())
    def test_old_cell_and_catalogue_claims_are_red(self):
        for text in ('one cell, as built & billed','billed from the measured saw table and the weighed joints','kg, measured','proven on the article'):
            self.assertTrue(evidence_errors([text],self.ledger),text)
    def test_denial_and_proposed_tests_are_not_evidence_claims(self):
        for text in ('No cell has been built and no joint has been physically weighed or tested.','equipment lines: named, not yet weighed','A future programme would test joints.','Closing the gap needs knockdown tests.'):
            self.assertEqual(evidence_errors([text],self.ledger),[],text)
    def test_computation_cannot_launder_physical_word(self):
        self.assertTrue(evidence_errors(['Computed mass; the joints have been weighed.'],self.ledger))
        self.assertTrue(evidence_errors(['No cell has been built, but its joints have been weighed.'],self.ledger))
        self.assertTrue(evidence_errors(['The programme needs tests and the joints are tested.'],self.ledger))
        self.assertTrue(evidence_errors(['No uncertainty remains: the joints have been weighed.'],self.ledger))
        self.assertTrue(evidence_errors(['The model is not final because the joints were weighed.'],self.ledger))
