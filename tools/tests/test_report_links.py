"""Links from the three reports to files of this repository, in the source and in the PDF.

A report's source lives in research/reports/ and its PDF in research/pdf/out/, one folder
deeper. A relative link copied from one to the other names a different file: `../../README.md`
is the repository's README from the source and research/README.md from the PDF. These tests
hold the source links to real files, the re-based links to the same files, and the recorded
PDFs to exactly the re-based links.
"""
from __future__ import annotations

from pathlib import Path
import posixpath
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import md2tex

REPORTS = ('01-brief', '02-paper', '03-diligence')
LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
SCHEME = re.compile(r'[A-Za-z][A-Za-z0-9+.-]*:')


def relative(target: str) -> bool:
    return not SCHEME.match(target) and not target.startswith(('#', '/'))


def source_links(stem: str) -> list[str]:
    text = (ROOT / md2tex.SOURCE_DIR / f'{stem}.md').read_text(encoding='utf-8')
    return [m.group(2) for m in LINK.finditer(text) if relative(m.group(2))]


def pdf_links(stem: str) -> list[str]:
    out = subprocess.run(['pdfinfo', '-url', str(ROOT / md2tex.PDF_DIR / f'{stem}.pdf')],
                         check=True, capture_output=True, text=True).stdout
    urls = [line.split(None, 2)[2].strip() for line in out.splitlines()[1:] if len(line.split(None, 2)) == 3]
    return [u for u in urls if relative(u)]


def named_file(folder: str, target: str) -> str:
    """The repository path a relative link names when it is followed from `folder`."""
    return posixpath.normpath(posixpath.join(folder, target.partition('#')[0]))


class ReportLinks(unittest.TestCase):
    def test_rebasing_keeps_addresses_and_moves_paths(self):
        same = ('https://pinkrobotics.ca/airships', 'mailto:someone@example.invalid', '#section', '/rooted')
        for target in same:
            self.assertEqual(md2tex.link_target(target), target)
        self.assertEqual(md2tex.link_target('../../README.md'), '../../../README.md')
        self.assertEqual(md2tex.link_target('../../docs/FLOAT.md#the-verdict'), '../../../docs/FLOAT.md#the-verdict')
        self.assertEqual(md2tex.link_target('01-brief.md'), '../../reports/01-brief.md')

    def test_every_source_link_names_a_file_and_its_pdf_form_names_the_same_one(self):
        seen = 0
        for stem in REPORTS:
            for target in source_links(stem):
                seen += 1
                wanted = named_file(md2tex.SOURCE_DIR, target)
                self.assertTrue((ROOT / wanted).is_file(), f'{stem}: {target} names no file ({wanted})')
                got = named_file(md2tex.PDF_DIR, md2tex.link_target(target))
                self.assertEqual(got, wanted, f'{stem}: {target} re-based for the PDF names {got}')
                # The mistake this guards against, said once: unchanged, the link names another file.
                self.assertNotEqual(named_file(md2tex.PDF_DIR, target), wanted)
        self.assertGreater(seen, 0, 'the reports hold no relative link: this test reads nothing')

    def test_the_recorded_pdfs_carry_exactly_the_rebased_links(self):
        for stem in REPORTS:
            wanted = sorted(md2tex.link_target(t) for t in source_links(stem))
            self.assertEqual(sorted(pdf_links(stem)), wanted, f'{stem}.pdf: relative links')
            for link in wanted:
                self.assertTrue((ROOT / named_file(md2tex.PDF_DIR, link)).is_file(), f'{stem}.pdf: {link}')


if __name__ == '__main__':
    unittest.main()
