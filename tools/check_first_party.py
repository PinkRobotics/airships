#!/usr/bin/env python3
"""Inspect returned HTML with browser request headers; no page scripts run.

Reports automatic HTML/CSS load addresses, including nested srcdoc, and literal
inline addresses as references. Does not interpret scripts or reconstruct computed
addresses, follow subresources, or cover interaction-only form actions and link
pings. Hostname scoping deliberately ignores ports. Redirecting documents fail closed.
"""
import argparse
from html.parser import HTMLParser
import re
import shutil
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

LOAD_LINK_RELS = {'stylesheet', 'icon', 'preload', 'modulepreload', 'prefetch',
                  'preconnect', 'dns-prefetch', 'manifest', 'apple-touch-icon',
                  'apple-touch-icon-precomposed'}
CSS_URL = re.compile(r'url\(\s*["\']?([^"\')\s]+)', re.I)
# Textual references, not proof of a request. Include non-loading strings and
# comments deliberately; the report must not vouch for what a script will do.
INLINE_ADDRESS = re.compile(r'''(?<![\w:/])(?:[a-z][a-z0-9+.-]*:)?//[^\s"'`<>()[\]{};,]+''', re.I)


def browser_user_agent():
    browser = shutil.which('chromium') or shutil.which('google-chrome')
    if browser:
        try:
            version = subprocess.check_output([browser, '--version'], text=True, timeout=3)
            match = re.search(r'\b(\d+)\.\d+\.\d+\.\d+\b', version)
            if match:
                return ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                        f'(KHTML, like Gecko) Chrome/{match.group(1)}.0.0.0 Safari/537.36')
        except (OSError, subprocess.SubprocessError):
            pass
    raise RuntimeError('Chromium or Chrome is required to supply the current browser User-Agent')


class Loads(HTMLParser):
    def __init__(self, address, inherited_base=None, depth=0):
        super().__init__(convert_charrefs=True)
        self.address, self.base, self.loads = address, inherited_base or address, []
        self.fallback_base = inherited_base or address
        self.srcdocs = []
        self.depth = depth
        self.in_style = False
        self.in_script = False

    def inline_addresses(self, source, text):
        for match in INLINE_ADDRESS.finditer(text):
            self.add(source, match.group())

    def add(self, source, value):
        if value and not value.lstrip().startswith(('#', 'data:', 'blob:', 'javascript:')):
            self.loads.append((source, value.strip()))

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == 'base' and attrs.get('href'):
            self.base = urljoin(self.fallback_base, attrs['href'])
        if tag == 'style':
            self.in_style = True
        if tag == 'script':
            self.in_script = True
        if tag == 'link':
            if set(attrs.get('rel', '').lower().split()) & LOAD_LINK_RELS:
                self.add('link[href]', attrs.get('href'))
        elif tag == 'object':
            self.add('object[data]', attrs.get('data'))
        elif tag in {'script', 'img', 'iframe', 'frame', 'audio', 'video', 'source',
                     'embed', 'track', 'input', 'image', 'use'}:
            self.add(f'{tag}[src]', attrs.get('src'))
            if tag in {'image', 'use'}:
                self.add(f'{tag}[href]', attrs.get('href') or attrs.get('xlink:href'))
        if tag in {'img', 'source'} and attrs.get('srcset'):
            for candidate in attrs['srcset'].split(','):
                self.add(f'{tag}[srcset]', candidate.strip().split()[0] if candidate.strip() else '')
        if tag == 'iframe' and attrs.get('srcdoc') is not None:
            self.srcdocs.append(attrs['srcdoc'])
        if tag == 'video':
            self.add('video[poster]', attrs.get('poster'))
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            match = re.search(r'url\s*=\s*["\']?([^"\';]+)', attrs.get('content', ''), re.I)
            if match:
                self.add('meta[refresh]', match.group(1))
        for value in [attrs.get('style', '')]:
            self.inline_addresses('named in an inline style', value)
            for match in CSS_URL.finditer(value):
                self.add(f'{tag}[style]', match.group(1))

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False
        if tag == 'script':
            self.in_script = False

    def handle_data(self, data):
        if self.in_script:
            self.inline_addresses('named in an inline script', data)
        if self.in_style:
            self.inline_addresses('named in an inline style', data)
            for match in CSS_URL.finditer(data):
                self.add('style[url]', match.group(1))
            for match in re.finditer(r'@import\s+["\']([^"\']+)', data, re.I):
                self.add('style[@import]', match.group(1))

    def foreign(self):
        own = urlsplit(self.address).hostname
        found = set()
        for source, raw in self.loads:
            absolute = urljoin(self.base, raw)
            parts = urlsplit(absolute)
            if parts.hostname and parts.hostname != own:
                found.add((parts.hostname, source, absolute))
        for source in self.srcdocs:
            if self.depth >= 32:
                raise RuntimeError('iframe[srcdoc] nesting exceeds the inspector limit')
            child = Loads(self.address, inherited_base=self.base, depth=self.depth + 1)
            child.feed(source)
            found.update((host, 'iframe[srcdoc] ' + kind, url)
                         for host, kind, url in child.foreign())
        return sorted(found)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        return None


def inspect(address, opener=None, user_agent=None):
    opener = opener or build_opener(NoRedirect())
    request = Request(address, headers={
        'User-Agent': user_agent or browser_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    })
    with opener.open(request, timeout=15) as response:
        body = response.read().decode(response.headers.get_content_charset() or 'utf-8', errors='replace')
        headers = {name: response.headers.get_all(name, []) for name in ('report-to', 'nel')}
        parser = Loads(response.url)
        parser.feed(body)
        return parser.foreign(), headers


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('addresses', nargs='+', help='absolute HTML addresses; one GET per address')
    args = parser.parse_args(argv)
    failed = False
    for address in args.addresses:
        try:
            foreign, headers = inspect(address)
        except (HTTPError, URLError, OSError, RuntimeError, ValueError) as exc:
            print(f'{address}: check failed: {exc}')
            failed = True
            continue
        print(address)
        for name, values in headers.items():
            print(f'  {name}: {", ".join(values) if values else "(absent)"}')
        if foreign:
            for host, source, url in foreign:
                print(f'  FOREIGN {host} {source} {url}')
            failed = True
        else:
            print('  foreign HTML loads or inline addresses: none')
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
