#!/usr/bin/env python3
"""Fast loading-URL check over exactly the files selected by dist.manifest.

Non-loading URL positions are explicitly allowed below. Loading positions never inherit
that allowance: e.g. a canonical link's href is fine, a stylesheet's href is not.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from publish import read_manifest, wanted_files

NON_LOADING = {('a', 'href'), ('area', 'href'), ('link:canonical', 'href')}
REMOTE = re.compile(r'^(?:https?:)?//', re.I)
LOADING = re.compile(
    r'''(?:\b(?:fetch|import|importScripts|Worker|SharedWorker|WebSocket|EventSource)\s*\(\s*|'''
    r'''\bfrom\s+|\bimport\s+|\burl\(\s*|@import\s+|'''
    r'''\.(?:src|href|poster)\s*=\s*|\b(?:src|poster)\s*=\s*)'''
    r'''["'`]?(?P<url>(?:https?:)?//[A-Za-z0-9[][^\s"'`<>)]*)''', re.I)


def served_files():
    served, _, partial = read_manifest()
    return list(wanted_files(served, partial))


class Loads(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        role = 'link:canonical' if tag == 'link' and attrs.get('rel', '').lower() == 'canonical' else tag
        for name, value in attrs.items():
            if not value or (role, name) in NON_LOADING:
                continue
            if name in {'src', 'href', 'xlink:href', 'poster', 'data', 'action', 'ping', 'srcset'}:
                for url in re.split(r'[,\s]+', value):
                    if REMOTE.match(url):
                        self.errors.append(f'{tag}[{name}]={url}')
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            if re.search(r'url\s*=\s*["\']?(?:https?:)?//', attrs.get('content', ''), re.I):
                self.errors.append('external meta refresh')


def violations(text, suffix):
    errors = [m.group('url') for m in LOADING.finditer(text)]
    if suffix in {'.html', '.svg'}:
        parser = Loads()
        parser.feed(text)
        errors += parser.errors
    return sorted(set(errors))


def main():
    count, failures = 0, []
    for path, rel in served_files():
        if path.suffix not in {'.html', '.svg', '.js', '.mjs', '.css'}:
            continue
        count += 1
        failures += [f'{rel}: {error}' for error in violations(path.read_text(), path.suffix)]
    for failure in failures:
        print(failure)
    print(f'first-party static: {count} served source files, {len(failures)} external loads')
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
