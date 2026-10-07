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
