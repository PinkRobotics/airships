#!/usr/bin/env python3
"""A search-and-fetch helper, for when the assistant's own web tooling is unavailable.

    python3 tools/websearch.py search "query"        # ranked results
    python3 tools/websearch.py get URL [OUT]         # fetch, follow, save
    python3 tools/websearch.py text URL              # fetch and strip to readable text

Uses DuckDuckGo's HTML endpoint, which needs no key. It exists because a session can run
out of hosted search budget in the middle of a research task, and the research should not
stop for that. Nothing here is used by the site or by any gate — it is a tool for a person
(or an assistant) doing the reading.

Be polite: one request at a time, a real User-Agent, and a short pause between calls.
"""
from __future__ import annotations

import html
import re
import subprocess
import sys
import time
import urllib.parse

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def curl(url: str, out: str | None = None, timeout: int = 60) -> bytes:
    cmd = ["curl", "-sSL", "--max-time", str(timeout), "-A", UA, url]
    if out:
        cmd += ["-o", out]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"curl failed ({r.returncode}): {r.stderr.decode()[:300]}")
    return r.stdout


ENDPOINTS = ("https://lite.duckduckgo.com/lite/?q=", "https://html.duckduckgo.com/html/?q=")


def search(q: str, n: int = 12) -> list[tuple[str, str]]:
    """Try both endpoints with backoff. The service rate-limits, and a blocked reply is a
    200 with no results in it rather than an error code, so detect it by emptiness."""
    body = ""
    for attempt in range(5):
        for base in ENDPOINTS:
            try:
                body = curl(base + urllib.parse.quote(q)).decode("utf-8", "replace")
            except SystemExit:
                continue
            if "result__a" in body or "result-link" in body:
                break
        if "result__a" in body or "result-link" in body:
            break
        time.sleep(3 * (attempt + 1))
    out = []
    for href, txt in re.findall(r'result-link"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S):
        m = re.search(r"uddg=([^&]+)", href)
        url = urllib.parse.unquote(m.group(1)) if m else href
        out.append((re.sub("<[^>]+>", "", html.unescape(txt)).strip(), url))
        if len(out) >= n:
            return out
    for href, txt in re.findall(r'result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S):
        m = re.search(r"uddg=([^&]+)", href)
        url = urllib.parse.unquote(m.group(1)) if m else href
        title = re.sub("<[^>]+>", "", html.unescape(txt)).strip()
        out.append((title, url))
        if len(out) >= n:
            break
    return out


def to_text(raw: bytes) -> str:
    s = raw.decode("utf-8", "replace")
    s = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"[ \t\xa0]+", " ", re.sub(r"\n\s*\n+", "\n", s)).strip()


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    mode, arg = sys.argv[1], sys.argv[2]
    if mode == "search":
        for i, (t, u) in enumerate(search(arg), 1):
            print(f"{i:>2}. {t[:88]}\n    {u}")
    elif mode == "get":
        out = sys.argv[3] if len(sys.argv) > 3 else None
        data = curl(arg, out)
        print(f"saved {out}" if out else to_text(data)[:4000])
    elif mode == "text":
        print(to_text(curl(arg))[:12000])
    else:
        sys.exit(__doc__)
    time.sleep(0.5)


if __name__ == "__main__":
    main()
