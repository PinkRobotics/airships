"""Fidelity of the three float pages to their documents, with red-then-restored proofs.

The document side is read by a small stripper written here, not by the generator's parser:
two readers that agree are the evidence that no word and no figure changed on a page.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import gen_float_pages as pages
import publish

DOCS = {'docs/FLOAT.md': 'float/index.html',
        'docs/FLOAT-LEDGER.md': 'float/ledger.html',
        'docs/MEMBER-CENSUS.md': 'float/census.html'}
LINK = re.compile(r'\[([^\]]*)\]\(([^)\s]*)\)')
TOOL = str(ROOT / 'tools/gen_float_pages.py')


def collapse(text: str) -> str:
    return ' '.join(text.split())


class MainText(HTMLParser):
    """The text inside <main>, every tag replaced by nothing."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth, self.parts = 0, []

    def handle_starttag(self, tag, attrs):
        self.depth += tag == 'main'

    def handle_endtag(self, tag):
        self.depth -= tag == 'main'

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)


def page_text(page: str) -> str:
    parser = MainText()
    parser.feed(page)
    parser.close()
    return collapse(''.join(parser.parts))


def published(root: Path) -> set[str]:
    """The served files, read by the publishing tool rather than by the generator."""
    with patch.object(publish, 'ROOT', root):
        served, _, partial = publish.read_manifest()
        return {rel.as_posix() for _, rel in publish.wanted_files(served, partial)}


def target_of(doc: str, dest: str) -> str:
    return posixpath.normpath(posixpath.join(posixpath.dirname(doc), dest.split('#')[0]))


def inline_text(doc: str, text: str, live: set[str]) -> str:
    out = []
    for index, piece in enumerate(re.split(r'`([^`]*)`', text)):
        if index % 2:                       # a code span is literal
            out.append(piece)
            continue

        def link(match):
            target = target_of(doc, match.group(2))
            words = match.group(1)
            return words if target in DOCS or target in live else f'{words} ({target})'

        piece = LINK.sub(link, piece)
        piece = re.sub(r'</?(?:details|summary)>', '', piece)
        # An emphasis marker touches a word. A star with a space on both sides is text.
        piece = re.sub(r'\*+(?=\S)|(?<=\S)\*+', '', piece)
        out.append(piece.replace('&lt;', '<').replace('&gt;', '>'))
    return ''.join(out)


def markdown_text(doc: str, text: str, live: set[str]) -> str:
    """The document's text with its Markdown markup removed and white space collapsed."""
    parts, prose, fenced = [], [], False

    def flush():
        if prose:
            parts.append(inline_text(doc, '\n'.join(prose), live))
            prose.clear()

    for line in text.split('\n'):
        if line.startswith('```'):
            flush()
            fenced = not fenced
        elif fenced or line.startswith('    '):
            flush()
            parts.append(line)
        elif re.fullmatch(r'-{3,}', line) or re.fullmatch(r'\|(?: *:?-+:? *\|)+', line):
            flush()
        else:
            line = re.sub(r'^(?:#{1,6} |> |- |\d+\. )', '', line)
            if line.startswith('|'):
                cells = re.split(r'(?<!\\)\|', line.strip()[1:-1])
                line = ' '.join(cell.replace('\\|', '|') for cell in cells)
            prose.append(line)
    flush()
    return collapse('\n'.join(parts))


def first_difference(a: str, b: str) -> str:
    at = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    near = slice(max(0, at - 60), at + 60)
    return f'first difference at character {at}: {a[near]!r} != {b[near]!r}'


class Structure(HTMLParser):
    """Tags, attributes and the style text of one page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags, self.attrs, self.stack, self.css, self.hrefs = [], [], [], [], []
        self.bare_tables, self.header_cells = 0, []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        self.attrs += [(tag, name) for name in attrs]
        if tag == 'a':
            self.hrefs.append(attrs.get('href', ''))
        if tag == 'table' and (not self.stack or self.stack[-1] != ('div', 'tablewrap')):
            self.bare_tables += 1
        if tag == 'th':
            self.header_cells.append(attrs.get('scope'))
        if tag not in ('meta', 'hr', 'br'):
            self.stack.append((tag, attrs.get('class')))

    def handle_endtag(self, tag):
        while self.stack and self.stack.pop()[0] != tag:
            pass

    def handle_data(self, data):
        if self.stack and self.stack[-1][0] == 'style':
            self.css.append(data)


def structure(page: str) -> Structure:
    parser = Structure()
    parser.feed(page)
    parser.close()
    return parser


class ScratchTrees(unittest.TestCase):
    def tree(self, **documents: str) -> Path:
        """A small repository holding three documents; keywords replace their text."""
        temp = tempfile.TemporaryDirectory(prefix='float-pages-')
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        texts = {'docs/FLOAT.md': '# Float case\n', 'docs/FLOAT-LEDGER.md': '# Float ledger\n',
                 'docs/MEMBER-CENSUS.md': '# Member census\n'}
        texts.update({'docs/' + name: text for name, text in documents.items()})
        texts['dist.manifest'] = ('served float\nserved cell\nexcluded docs\n'
                                  'excluded dist.manifest\n')
        texts['cell/ship.html'] = '<title>fixture</title>\n'
        for name, text in texts.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_text(text, encoding='utf-8')
        return root

    def copy(self) -> Path:
        """The three documents, their pages, the manifest and every file they link."""
        temp = tempfile.TemporaryDirectory(prefix='float-pages-')
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        names = [*DOCS, *DOCS.values(), 'dist.manifest']
        for doc in DOCS:
            for _, dest in LINK.findall((ROOT / doc).read_text(encoding='utf-8')):
                names.append(target_of(doc, dest))
        for name in dict.fromkeys(names):
            if (ROOT / name).is_file():
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, root / name)
        return root

    def run_check(self, root: Path) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, TOOL, '--check', '--root', str(root)],
                              capture_output=True, text=True)

    def body(self, markdown: str) -> str:
        page = pages.render(self.tree(**{'FLOAT.md': markdown}))['float/index.html'].html
        return page[page.index('<main>'):page.index('</main>')]


class Fidelity(ScratchTrees):
    def test_each_page_says_exactly_what_its_document_says(self):
        live = published(ROOT)
        for doc, page in DOCS.items():
            with self.subTest(page=page):
                want = markdown_text(doc, (ROOT / doc).read_text(encoding='utf-8'), live)
                have = page_text((ROOT / page).read_text(encoding='utf-8'))
                self.assertTrue(want == have, first_difference(want, have))
                self.assertGreater(len(want.split()), 1000)

    def test_committed_pages_equal_a_fresh_render_and_nothing_else_is_there(self):
        self.assertEqual(pages.check(ROOT), [])
        self.assertEqual(sorted(p.name for p in (ROOT / 'float').iterdir()),
                         ['census.html', 'index.html', 'ledger.html'])

    def test_one_digit_changed_in_a_document_is_red_then_restored(self):
        root = self.copy()
        self.assertEqual(self.run_check(root).returncode, 0)
        for doc, page in DOCS.items():
            with self.subTest(doc=doc):
                path = root / doc
                before = path.read_text(encoding='utf-8')
                digit = re.search(r'\d', before)
                other = str((int(digit.group()) + 1) % 10)
                path.write_text(before[:digit.start()] + other + before[digit.end():],
                                encoding='utf-8')
                result = self.run_check(root)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(f'{page} differs from a fresh render of {doc}', result.stdout)
                self.assertEqual([p.split(' ')[0] for p in pages.check(root)], [page])
                print(f'one digit changed in {doc}: RED exit=1; {result.stdout.splitlines()[0]}')
                path.write_text(before, encoding='utf-8')
                self.assertEqual(self.run_check(root).returncode, 0)
                print(f'one digit changed in {doc}: restored PASS')

    def test_one_word_changed_in_a_page_is_red_then_restored(self):
        root = self.copy()
        live = published(root)
        for doc, page in DOCS.items():
            with self.subTest(page=page):
                path = root / page
                before = path.read_text(encoding='utf-8')
                word = re.search(r'(?s)<main>.*?<p>(\w+)', before)
                changed = word.group(1)[::-1] + 'x'
                path.write_text(before[:word.start(1)] + changed + before[word.end(1):],
                                encoding='utf-8')
                result = self.run_check(root)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(f'{page} differs from a fresh render of {doc}', result.stdout)
                want = markdown_text(doc, (root / doc).read_text(encoding='utf-8'), live)
                self.assertNotEqual(want, page_text(path.read_text(encoding='utf-8')))
                print(f'one word changed in {page}: RED exit=1; {result.stdout.splitlines()[0]}')
                path.write_text(before, encoding='utf-8')
                self.assertEqual(self.run_check(root).returncode, 0)
                self.assertEqual(want, page_text(path.read_text(encoding='utf-8')))
                print(f'one word changed in {page}: restored PASS')

    def test_a_stray_file_beside_the_pages_is_red(self):
        root = self.copy()
        (root / 'float/extra.html').write_text('<p>not generated</p>\n')
        result = self.run_check(root)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('float/extra.html is not written by the generator', result.stdout)


class Links(ScratchTrees):
    def test_unpublished_link_renders_as_text_and_is_counted(self):
        root = self.copy()
        before = pages.render(root)['float/census.html']
        note = root / 'docs/working/example-note.md'
        note.parent.mkdir(parents=True, exist_ok=True)
        note.write_text('# Example\n')
        doc = root / 'docs/MEMBER-CENSUS.md'
        doc.write_text(doc.read_text(encoding='utf-8')
                       + '\nSee the [example note](working/example-note.md).\n', encoding='utf-8')
        after = pages.render(root)['float/census.html']
        self.assertIn('<p>See the example note (<code>docs/working/example-note.md</code>).</p>',
                      after.html)
        self.assertNotIn('example-note.md"', after.html)
        self.assertEqual((after.as_text, after.kept), (before.as_text + 1, before.kept))
        result = self.run_check(root)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        print('unpublished link added to a document: rendered as text, counted '
              f'{before.as_text} -> {after.as_text}; RED exit=1 until the page is written')
        self.assertEqual(pages.write(root), ['float/census.html'])
        self.assertEqual(self.run_check(root).returncode, 0)
        live = published(root)
        want = markdown_text('docs/MEMBER-CENSUS.md', doc.read_text(encoding='utf-8'), live)
        self.assertEqual(want, page_text((root / 'float/census.html').read_text(encoding='utf-8')))

    def test_counts_match_an_independent_reading_of_the_documents(self):
        live = published(ROOT)
        rendered = pages.render(ROOT)
        for doc, page in DOCS.items():
            with self.subTest(doc=doc):
                text = re.sub(r'`[^`]*`', '', (ROOT / doc).read_text(encoding='utf-8'))
                targets = [target_of(doc, dest) for _, dest in LINK.findall(text)]
                kept = sum(t in DOCS or t in live for t in targets)
                self.assertEqual((rendered[page].kept, rendered[page].as_text),
                                 (kept, len(targets) - kept))
                # The frame holds seven links: one back, three in the row, three in the footer.
                self.assertEqual(rendered[page].html.count('<a href='), kept + 7)

    def test_document_links_become_page_links_and_every_link_resolves(self):
        live = published(ROOT)
        ids = {page: set(re.findall(r' id="([^"]+)"', (ROOT / page).read_text(encoding='utf-8')))
               for page in DOCS.values()}
        self.assertIn('href="ledger.html#the-history-of-being-wrong"',
                      (ROOT / 'float/index.html').read_text(encoding='utf-8'))
        for page in DOCS.values():
            for href in structure((ROOT / page).read_text(encoding='utf-8')).hrefs:
                with self.subTest(page=page, href=href):
                    self.assertNotRegex(href, r'^(?:[a-z][a-z0-9+.-]*:|//)|\.md(?:#|$)')
                    path, _, fragment = href.partition('#')
                    target = posixpath.normpath(posixpath.join('float', path))
                    if target == '.':
                        continue                    # the monitor, one level up
                    self.assertIn(target, live)
                    if fragment:
                        self.assertIn(fragment, ids[target])

    def test_link_rules_one_by_one(self):
        root = self.tree(**{
            'FLOAT.md': '# Float case\n\nSee the [ledger](FLOAT-LEDGER.md#rows-and-bases), the '
                        '[census](MEMBER-CENSUS.md), the [checks](../cell/ship.html) and the\n'
                        '[questions](OPEN-QUESTIONS.md).\n',
            'FLOAT-LEDGER.md': '# Float ledger\n\n## Rows and bases\n\n'
                               'Back to the [case](FLOAT.md).\n',
            'OPEN-QUESTIONS.md': '# Open questions\n'})
        rendered = pages.render(root)
        page = rendered['float/index.html']
        self.assertIn('See the <a href="ledger.html#rows-and-bases">ledger</a>, the '
                      '<a href="census.html">census</a>, the '
                      '<a href="../cell/ship.html">checks</a> and the\n'
                      'questions (<code>docs/OPEN-QUESTIONS.md</code>).', page.html)
        self.assertEqual((page.kept, page.as_text), (3, 1))
        self.assertIn('Back to the <a href="index.html">case</a>.',
                      rendered['float/ledger.html'].html)


class Rendering(ScratchTrees):
    def test_heading_ids_follow_the_github_scheme(self):
        body = self.body('# Float case\n\n## Pressure schedule — not computed\n\n'
                         '## A1. What "one metre" means, and the one decision to make first\n\n'
                         '### The same name: what `tools/ship_scoping.py` prints by default\n\n'
                         '## Twice\n\n## Twice\n\n### Twice\n')
        for wanted in ('float-case', 'pressure-schedule--not-computed',
                       'a1-what-one-metre-means-and-the-one-decision-to-make-first',
                       'the-same-name-what-toolsship_scopingpy-prints-by-default',
                       'twice', 'twice-1', 'twice-2'):
            with self.subTest(id=wanted):
                self.assertEqual(body.count(f' id="{wanted}"'), 1)

    def test_measured_constructs_render_as_written(self):
        body = self.body(
            '# Float case\n\n> **Hull of record.** As drawn,\n> the hull does *not* float.\n\n'
            'Mass is `K_SHELL` times stock_build; a * b stays, [TO VERIFY] stays, ~15.1 stays.\n\n'
            '- **First** item\n  continues here\n- second\n\n'
            '1. one\n   more\n2. two\n\n---\n\n```json\n{"a": "<b>"}\n```\n\n'
            '    --res 112 -> ~160\n\n<details><summary>Old table</summary>\n\n'
            '| Case | Mass | |\n| --- | ---: | --- |\n| a \\| b | 0.558 | &lt;h1&gt; |\n\n'
            '</details>\n\n| Class | Old |\n| --- | --- |\n')
        for wanted in (
                '<blockquote>\n<p><strong>Hull of record.</strong> As drawn,\n'
                'the hull does <em>not</em> float.</p>',
                '<code>K_SHELL</code> times stock_build; a * b stays, [TO VERIFY] stays, '
                '~15.1 stays.',
                '<ul>\n<li><strong>First</strong> item\ncontinues here</li>\n<li>second</li>\n'
                '</ul>',
                '<ol>\n<li>one\nmore</li>\n<li>two</li>\n</ol>', '<hr>',
                '<pre><code>{"a": "&lt;b&gt;"}\n</code></pre>',
                '<pre><code>--res 112 -&gt; ~160\n</code></pre>',
                '<details>\n<summary>Old table</summary>', '</details>',
                '<th scope="col">Case</th>\n<th scope="col" class="r">Mass</th>\n<td></td>',
                '<td>a | b</td>\n<td class="r">0.558</td>\n<td>&lt;h1&gt;</td>',
                '<th scope="col">Class</th>\n<th scope="col">Old</th>\n</tr>\n</thead>\n</table>'):
            with self.subTest(wanted=wanted):
                self.assertIn(wanted, body)

    def test_unknown_construct_stops_with_file_and_line(self):
        cases = {
            'image': ('![alt](x.png)\n', 3),
            'reference definition': ('[x]: FLOAT-LEDGER.md\n', 3),
            'deep heading': ('#### Deep\n', 3),
            'raw block': ('<div>hello</div>\n', 3),
            'raw inline': ('text <b>bold</b>\n', 3),
            'comment': ('<!-- hidden -->\n', 3),
            'setext heading': ('Title\n=====\n', 4),
            'external link': ('[a](https://example.org/)\n', 3),
            'bare address': ('see https://example.org/ now\n', 3),
            'strikethrough': ('~~gone~~\n', 3),
            'nested list': ('- a\n  - b\n', 4),
            'star bullet': ('* a\n', 3),
            'loose list': ('- a\n\n- b\n', 5),
            'list from two': ('2. a\n', 3),
            'underscore emphasis': ('_em_\n', 3),
            'backslash escape': ('\\*not\\*\n', 3),
            'hard break': ('one  \ntwo\n', 3),
            'entity': ('caf&eacute;\n', 3),
            'unclosed code': ('a `b\n', 3),
            'double backtick': ('a ``b`` c\n', 3),
            'unclosed fence': ('```\ncode\n', 3),
            'tilde fence': ('~~~\ncode\n~~~\n', 3),
            'unmatched emphasis': ('a **b\nc\n', 3),
            'table without rule': ('| a | b |\n| 1 | 2 |\n', 3),
            'short row': ('| a | b |\n| --- | --- |\n| 1 |\n', 5),
            'centred column': ('| a |\n| :---: |\n', 4),
            'link to a missing file': ('[x](missing.md)\n', 3),
            'missing fragment': ('[x](FLOAT-LEDGER.md#nowhere)\n', 3),
            'second line of a paragraph': ('one\ntwo [x](missing.md)\n', 4),
            'unclosed details': ('<details><summary>More</summary>\n\ntext\n', 3),
            'text after a list': ('- a\nlazy\n', 4),
            'indented text': ('  odd\n', 3),
            'link in the words of a link': ('[a [b](FLOAT-LEDGER.md) c](MEMBER-CENSUS.md)\n', 3),
            'definition in a list item': ('- [x]: FLOAT-LEDGER.md\n', 3),
            'definition in a quotation': ('> [x]: FLOAT-LEDGER.md\n', 3),
            'list item that opens a block': ('- > quoted\n', 3),
            'empty list item': ('-\n', 3),
            'table without its pipes': ('a | b\n--- | ---\n', 4),
            'rule line one cell too long': ('| a | b |\n|---|---|---|\n| 1 | 2 |\n', 4),
            'rule line two cells too long': ('| a |\n| --- | --- | --- |\n', 4),
            'longer rule line with an alignment': ('| a |\n| --- | ---: |\n', 4),
            'rule line one cell too short': ('| a | b |\n| --- |\n', 4),
            'second title': ('# Again\n', 3),
        }
        for label, (markdown, line) in cases.items():
            with self.subTest(construct=label):
                root = self.tree(**{'FLOAT.md': '# Float case\n\n' + markdown})
                with self.assertRaises(pages.Unknown) as caught:
                    pages.render(root)
                self.assertRegex(str(caught.exception), rf'^docs/FLOAT\.md:{line}: \S')
        with self.assertRaises(pages.Unknown) as caught:
            pages.render(self.tree(**{'FLOAT.md': 'Words first.\n\n# Float case\n'}))
        self.assertRegex(str(caught.exception), r'^docs/FLOAT\.md:1: \S')
        root = self.tree(**{'FLOAT.md': '# Float case\n\n![alt](x.png)\n'})
        result = self.run_check(root)
        self.assertEqual(result.returncode, 2)
        self.assertRegex(result.stderr, r'^docs/FLOAT\.md:3: ')
        self.assertFalse((root / 'float').exists())

    def test_code_span_outranks_a_bracket_and_brackets_nest_in_the_words_of_a_link(self):
        body = self.body('# Float case\n\nA [b `c](FLOAT-LEDGER.md) d` e and '
                         '[the [0/90] rows](FLOAT-LEDGER.md) and **[bold](MEMBER-CENSUS.md)**.\n')
        self.assertIn('<p>A [b <code>c](FLOAT-LEDGER.md) d</code> e and '
                      '<a href="ledger.html">the [0/90] rows</a> and '
                      '<strong><a href="census.html">bold</a></strong>.</p>', body)

    def test_a_short_cell_stays_on_one_line_and_a_long_cell_wraps(self):
        short, long = 'x' * pages.WRAP, 'x' * (pages.WRAP + 1)
        body = self.body('# Float case\n\n| Tube | Note |\n| ---: | --- |\n'
                         f'| 9.5 × 0.50 mm | `{short}` |\n| {long} | **{long}** |\n')
        self.assertIn(f'<td class="r">9.5 × 0.50 mm</td>\n<td><code>{short}</code></td>', body)
        self.assertIn(f'<td class="r w">{long}</td>\n<td class="w"><strong>{long}</strong></td>',
                      body)
        for page in DOCS.values():
            with self.subTest(page=page):
                text = (ROOT / page).read_text(encoding='utf-8')
                self.assertIn('td{white-space:nowrap}', text)
                self.assertRegex(text, r'td\.w\{white-space:normal;min-width:\d+ch\}')

    def test_render_is_deterministic_and_carries_no_date_of_its_own(self):
        root = self.tree(**{'FLOAT.md': '# Float case\n\nPlain words only.\n'})
        first = {name: page.html for name, page in pages.render(root).items()}
        self.assertEqual(first, {name: page.html for name, page in pages.render(root).items()})
        for name, page in first.items():
            with self.subTest(page=name):
                self.assertNotRegex(page, r'\b(?:19|20)\d\d\b')
                self.assertTrue(page.endswith('</html>\n'))
                self.assertNotRegex(page, r'[ \t]\n')


class Pages(unittest.TestCase):
    def test_no_script_no_other_host_no_web_font(self):
        for page in DOCS.values():
            with self.subTest(page=page):
                found = structure((ROOT / page).read_text(encoding='utf-8'))
                banned = {'script', 'link', 'img', 'iframe', 'object', 'embed', 'video', 'audio',
                          'source', 'form', 'input', 'button', 'base'}
                self.assertEqual(banned & set(found.tags), set())
                loading = {'src', 'srcset', 'poster', 'data', 'action', 'style', 'onclick',
                           'onload'}
                self.assertEqual([pair for pair in found.attrs if pair[1] in loading], [])
                self.assertNotRegex(''.join(found.css), r'url\(|@import|@font-face|//')

    def test_frame_follows_the_notices_page(self):
        notices = (ROOT / 'notices.html').read_text(encoding='utf-8')
        tokens = re.search(r':root\{[^}]*\}', notices).group()
        for page in DOCS.values():
            with self.subTest(page=page):
                text = (ROOT / page).read_text(encoding='utf-8')
                self.assertIn(tokens, text)
                self.assertIn('font:16px/1.55 system-ui,sans-serif', text)
                self.assertIn('<footer><a href="../">Fleet monitor</a> · '
                              '<a href="../notices.html">Data, licences and notices</a> · '
                              '<a href="../LICENSE">Code licence</a></footer>', text)
                self.assertEqual(text.count('<h1'), 1)
                self.assertLess(text.index('</header>'), text.index('<main>'))
                head = text[:text.index('<main>')]
                self.assertEqual(sorted(re.findall(r'<a href="([a-z]+\.html)"', head)),
                                 ['census.html', 'index.html', 'ledger.html'])
                self.assertEqual(head.count('aria-current="page"'), 1)
                doc = next(d for d, p in DOCS.items() if p == page)
                self.assertIn(f'rendered from <code>{doc}</code>', head)
                self.assertNotRegex(head, r'(?i)public')

    def test_tables_scroll_in_their_own_container_and_header_cells_carry_scope(self):
        for page in DOCS.values():
            with self.subTest(page=page):
                text = (ROOT / page).read_text(encoding='utf-8')
                found = structure(text)
                self.assertGreater(found.tags.count('table'), 0)
                self.assertEqual(found.bare_tables, 0)
                self.assertEqual(set(found.header_cells), {'col'})
                self.assertNotIn('<th scope="col"></th>', text)
                self.assertRegex(text, r'\.tablewrap\{[^}]*overflow-x:auto')
                # Each container takes keyboard focus and is named by a heading of its page.
                ids = set(re.findall(r'<h[123] id="([^"]+)"', text))
                names = re.findall(r'<div class="tablewrap" role="group" aria-labelledby="([^"]+)" '
                                   r'tabindex="0">\n<table>', text)
                self.assertEqual(len(names), found.tags.count('table'))
                self.assertLessEqual(set(names), ids)

    def test_float_gate_does_not_inventory_the_pages(self):
        import check_float_ledger
        listed = {path.relative_to(ROOT).as_posix() for path in check_float_ledger.paths()}
        self.assertEqual([name for name in listed if name.startswith('float/')], [])
        self.assertNotIn('docs/FLOAT-LEDGER.md', listed)
        self.assertLessEqual({'docs/FLOAT.md', 'docs/MEMBER-CENSUS.md'}, listed)
        for tool in ('tools/check_float_ledger.py', 'tools/float_claims.py'):
            self.assertIn('The three pages under float/ are not inventoried',
                          (ROOT / tool).read_text(encoding='utf-8'))

    def test_manifest_serves_the_pages_once_and_the_generator_reads_it_as_publishing_does(self):
        lines = [line.split() for line in (ROOT / 'dist.manifest').read_text().splitlines()]
        self.assertEqual([line[0] for line in lines if line[1:2] == ['float']], ['served'])
        self.assertEqual(pages.published(ROOT), published(ROOT))
        self.assertLessEqual(set(DOCS.values()), published(ROOT))


if __name__ == '__main__':
    unittest.main()
