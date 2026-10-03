"""Local link and anchor failures, with the package check's contract preserved."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_links
import noticecheck
from linkparse import anchors, parse_links


class LinkContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='links-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, text):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def run_check(self, source):
        self.write('README.md', source)
        return check_links.check(self.root, [Path('README.md')])

    def test_broken_link(self):
        errors, _ = self.run_check('[missing](absent.md)')
        self.assertEqual(errors, ['README.md: broken link: absent.md'])

    def test_broken_anchor(self):
        self.write('page.html', '<h1 id="present">Here</h1>')
        errors, _ = self.run_check('[missing](page.html#absent)')
        self.assertEqual(errors, ['README.md: broken anchor: page.html#absent'])

    def test_external_is_listed_without_network(self):
        with patch('socket.socket', side_effect=AssertionError('network forbidden')):
            errors, external = self.run_check('[external](https://example.org/missing#absent)\n<https://example.org/missing#absent>')
        self.assertEqual(errors, [])
        self.assertEqual(external, ['README.md -> https://example.org/missing#absent'])

    def test_removed_tracked_target_fails(self):
        self.write('old.md', '# Former note')
        self.write('README.md', '[old](old.md)')
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), 'add', '.'], check=True)
        (self.root / 'old.md').unlink()
        self.assertEqual(check_links.check(self.root)[0], ['README.md: broken link: old.md'])

    def test_headings_explicit_ids_and_directory_index(self):
        self.write('guide.md', '# A `code` heading!\n# A `code` heading!\nSetext title\n====\n<a name="named"></a>')
        self.write('page/index.html', '<h1 id="part">Page</h1><a name="old-name"></a>')
        errors, _ = self.run_check('\n'.join('[ok](' + p + ')' for p in (
            'guide.md#a-code-heading', 'guide.md#a-code-heading-1', 'guide.md#setext-title',
            'guide.md#named', 'page/#part', '/page/index.html#old-name')))
        self.assertEqual(errors, [])

    def test_images_references_titles_encoding_and_embedded_html(self):
        self.write('an image.svg', '<svg/>')
        self.write('a(b).md', '# Heading')
        source = ('![image](<an image.svg> "title")\n[ref][guide]\n[guide]: a(b).md#heading "title"\n'
                  '[guide][]\n[guide]\n<img src="an%20image.svg">\n[inline](a(b).md#heading)')
        self.assertEqual(self.run_check(source)[0], [])
        self.assertEqual(len(parse_links(source, '.md', repository=True)), 6)
        (self.root / 'an image.svg').unlink()
        self.assertEqual(len(self.run_check(source)[0]), 2)

    def test_linked_image_checks_both_destinations(self):
        self.assertEqual(parse_links('[![plot](plot.svg)](paper.md)', '.md', repository=True),
                         ['paper.md', 'plot.svg'])
        errors, _ = self.run_check('[![plot](plot.svg)](paper.md)')
        self.assertEqual(len(errors), 2)

    def test_code_comments_and_fenced_headings_are_not_links(self):
        source = ('`[example](missing.md)`\n```md\n[bad](bad.md)\n# Not a heading\n```\n'
                  '<!-- [bad](gone.md) -->\n    [code](absent.md)\n')
        self.assertEqual(self.run_check(source)[0], [])
        self.assertNotIn('not-a-heading', anchors(source, '.md'))

    def test_html_href_src_and_poster(self):
        self.write('index.html', '<a href="missing.md#x">X</a><img src="gone.svg"><video poster="gone.png">')
        self.assertEqual(len(check_links.check(self.root, [Path('index.html')])[0]), 3)

    def test_tree_escape_is_refused(self):
        self.assertIn('link escapes tree', self.run_check('[outside](../outside.md)')[0][0])

    def test_notice_package_semantics_unchanged(self):
        self.write('page.html', '<a href="#absent">X</a><a href="/site/">Root</a>'
                   '<a href="../outside.md">Outer site</a><img src="missing.png">')
        self.write('note.md', '![ignored image](missing.svg)\n[external](https://example.org/no)')
        self.assertEqual(noticecheck.link_errors(self.root), ['broken relative link: page.html -> missing.png'])


if __name__ == '__main__':
    unittest.main()
