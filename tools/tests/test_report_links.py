"""Links from the three reports to files of this repository, in the source and in the PDF.

A report's source lives in research/reports/ and its PDF in research/pdf/out/, one folder
deeper. A relative link copied from one to the other names a different file: `../../README.md`
is the repository's README from the source and research/README.md from the PDF. These tests
hold source links to real files, published float links to served pages, other relative
links to the same files, and recorded PDFs to exactly those converted links.
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
from gen_float_pages import published

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
    return [u for u in urls if relative(u) or u.startswith(md2tex.PUBLIC_ORIGIN + '/float/')]


def named_file(folder: str, target: str) -> str:
    """The repository path a relative link names when it is followed from `folder`."""
    return posixpath.normpath(posixpath.join(folder, target.partition('#')[0]))


class ReportLinks(unittest.TestCase):
    def test_rebasing_keeps_addresses_and_moves_paths(self):
        same = ('https://pinkrobotics.ca/airships', 'mailto:someone@example.invalid', '#section', '/rooted')
        for target in same:
            self.assertEqual(md2tex.link_target(target), target)
        self.assertEqual(md2tex.link_target('../../README.md'), '../../../README.md')
        self.assertEqual(md2tex.link_target('../../docs/FLOAT.md#1-where-the-mass-is'),
                         md2tex.PUBLIC_ORIGIN + '/float/#1-where-the-mass-is')
        self.assertEqual(md2tex.link_target('01-brief.md'), '../../reports/01-brief.md')

    def test_every_source_link_names_a_file_and_its_pdf_form_names_the_same_one(self):
        seen = 0
        for stem in REPORTS:
            for target in source_links(stem):
                seen += 1
                wanted = named_file(md2tex.SOURCE_DIR, target)
                self.assertTrue((ROOT / wanted).is_file(), f'{stem}: {target} names no file ({wanted})')
                converted = md2tex.link_target(target)
                if wanted in md2tex.PUBLIC_PAGES:
                    route = md2tex.PUBLIC_PAGES[wanted]
                    served = route + 'index.html' if route.endswith('/') else route
                    self.assertIn(served, published(ROOT), f'{stem}: {converted} is not published')
                    self.assertTrue((ROOT / served).is_file())
                    self.assertEqual(converted, md2tex.PUBLIC_ORIGIN + '/' + route +
                                     ('#' + target.partition('#')[2] if '#' in target else ''))
                else:
                    got = named_file(md2tex.PDF_DIR, converted)
                    self.assertEqual(got, wanted, f'{stem}: {target} re-based for the PDF names {got}')
                # The mistake this guards against, said once: unchanged, the link names another file.
                self.assertNotEqual(named_file(md2tex.PDF_DIR, target), wanted)
        self.assertGreater(seen, 0, 'the reports hold no relative link: this test reads nothing')

    def test_the_recorded_pdfs_carry_exactly_the_rebased_links(self):
        for stem in REPORTS:
            wanted = sorted(md2tex.link_target(t) for t in source_links(stem))
            self.assertEqual(sorted(pdf_links(stem)), wanted, f'{stem}.pdf: relative links')
            for link in wanted:
                if relative(link):
                    self.assertTrue((ROOT / named_file(md2tex.PDF_DIR, link)).is_file(), f'{stem}.pdf: {link}')
                else:
                    route = link.removeprefix(md2tex.PUBLIC_ORIGIN + '/').partition('#')[0]
                    self.assertIn(route + 'index.html' if route.endswith('/') else route, published(ROOT))


if __name__ == '__main__':
    unittest.main()
