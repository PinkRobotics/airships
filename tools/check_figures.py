#!/usr/bin/env python3
"""Every model figure quoted in a report must be the figure the model produces.

WHY THIS EXISTS. This project has moved almost every published number more than once, several of
them by half in a single day: hulls resized, the descent balance moved to a different altitude,
three drop passes collapsed into one. Code that goes stale fails a test. Prose that goes stale
just sits there being wrong, in the document most likely to be forwarded to someone who will not
check it — and a report full of confidently-stated obsolete numbers is worse for this project than
no report at all, because the entire pitch is "our arithmetic is checkable".

So a report does not get to type a model number. It cites one:

    the P-10000 delivers 13,183 t/h<!--f:P10000.cycle.tph--> on a 15 km leg

The marker is an HTML comment, so it is invisible wherever the Markdown is rendered, and this
tool reads the number immediately before it and compares it with `research/figures.json`, which
`make factsheet` regenerates from the live model. Numbers from CITED SOURCES are written plainly
and are not markable — they are not ours to regenerate, and `research/sources.json` is where they
are accounted for.

    python3 tools/check_figures.py            # check every report
    python3 tools/check_figures.py --list     # print every key figures.json offers
    python3 tools/check_figures.py --fix      # rewrite every cited number to match the model

`--fix` exists because the alternative is retyping forty numbers by hand every time the model
moves, which is how numbers get typed wrong. It rewrites ONLY the digits in front of a marker,
at the precision the author chose, and it deliberately does not touch a word of prose — so after
running it you still have to read the diff and fix the sentences that discuss the OLD value.
It reports how many it changed so you know how much prose to go and check.
"""
import decimal
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / "research" / "figures.json"
REPORTS = sorted((ROOT / "research" / "reports").glob("*.md"))

# `1,234.5 unit<!--f:key.path-->` — the number may carry thousand separators and a sign, and may
# be followed by a unit or closing punctuation before the marker.
CITE = re.compile(r"([-−]?[\d][\d,]*(?:\.\d+)?)\s*(?:[^\d<]{0,24}?)<!--\s*f:([A-Za-z0-9_.]+)\s*-->")
BARE = re.compile(r"<!--\s*f:([A-Za-z0-9_.]+)\s*-->")


def flatten(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}{k}."))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, f"{prefix}{i}."))
    else:
        out[prefix[:-1]] = obj
    return out


def fmt_like(value, raw, dp):
    """Render `value` the way the author rendered `raw`: same decimals, same separators."""
    q = decimal.Decimal(str(float(value))).quantize(
        decimal.Decimal(1).scaleb(-dp), rounding=decimal.ROUND_HALF_UP)
    out = f"{q:,.{dp}f}" if "," in raw else f"{q:.{dp}f}"
    # A minus sign written as U+2212 stays U+2212; the author picked the typography.
    if "−" in raw:
        out = out.replace("-", "−")
    return out


def fix(flat):
    """Rewrite every cited number to the model's value, in place. Returns the count changed."""
    total = 0
    for rp in REPORTS:
        src = rp.read_text()
        out, last, n = [], 0, 0
        for m in CITE.finditer(src):
            raw, key = m.group(1), m.group(2)
            full = key if key in flat else f"classes.{key}"
            want = flat.get(full)
            if not isinstance(want, (int, float)) or isinstance(want, bool):
                continue
            dp = len(raw.split(".")[1]) if "." in raw else 0
            new = fmt_like(want, raw, dp)
            if new == raw:
                continue
            # m.start(1)/end(1) is the number itself — the unit and the marker are untouched.
            out.append(src[last:m.start(1)])
            out.append(new)
            last = m.end(1)
            n += 1
        if n:
            out.append(src[last:])
            rp.write_text("".join(out))
            print(f"check_figures: {rp.name}: rewrote {n} figure(s)")
            total += n
    return total


def main():
    if not FIGURES.exists():
        print("check_figures: research/figures.json is missing — run `make factsheet`", file=sys.stderr)
        return 1
    flat = flatten(json.loads(FIGURES.read_text()))

    if "--list" in sys.argv:
        for k in sorted(flat):
            print(f"{k} = {flat[k]}")
        return 0

    if not REPORTS:
        print("check_figures: no reports yet — nothing to check")
        return 0

    if "--fix" in sys.argv:
        n = fix(flat)
        if n:
            print(f"\ncheck_figures: {n} figure(s) rewritten. READ THE DIFF — only the numbers "
                  "moved.\nAny sentence that discusses the old value is now wrong and this tool "
                  "cannot tell.")
        else:
            print("check_figures: nothing to fix")
        return 0

    bad, checked = [], 0
    for rp in REPORTS:
        src = rp.read_text()
        # Every marker must be preceded by a number. A marker on its own is a citation the author
        # meant to make and did not finish, which is exactly the state this tool exists to catch.
        cited_spans = {m.end() for m in CITE.finditer(src)}
        for m in BARE.finditer(src):
            if m.end() not in cited_spans:
                line = src[:m.start()].count("\n") + 1
                bad.append(f"{rp.name}:{line}: marker f:{m.group(1)} has no number before it")

        for m in CITE.finditer(src):
            raw, key = m.group(1), m.group(2)
            checked += 1
            line = src[:m.start()].count("\n") + 1
            # `f:P10000.cycle.tph` resolves to `classes.P10000.cycle.tph`. The prefix carries no
            # information a reader of the prose needs, and a marker nobody can read at a glance
            # is a marker nobody checks.
            full = key if key in flat else f"classes.{key}"
            if full not in flat:
                bad.append(f"{rp.name}:{line}: no such figure — f:{key}")
                continue
            want = flat[full]
            if not isinstance(want, (int, float)) or isinstance(want, bool):
                bad.append(f"{rp.name}:{line}: f:{key} is {want!r}, not a number")
                continue
            got = float(raw.replace(",", "").replace("−", "-"))
            # Compare at the precision the author WROTE. Quoting 13,183 against 13,183.4 is
            # correct rounding; quoting 13,200 is not, and neither is quoting last week's 12,052.
            dp = len(raw.split(".")[1]) if "." in raw else 0
            # ROUND HALF UP, not Python's round(), which is banker's: round(13722.5) is 13722,
            # so a report writing the correct 13,723 was being failed by the gate meant to
            # protect it. Authors round the way everyone was taught; the checker must agree.
            q = decimal.Decimal(str(float(want))).quantize(
                decimal.Decimal(1).scaleb(-dp), rounding=decimal.ROUND_HALF_UP)
            if abs(float(q) - got) > 10 ** (-dp) / 2 + 1e-9:
                bad.append(f"{rp.name}:{line}: f:{key} — report says {raw}, "
                           f"the model says {want}")

    for b in bad:
        print("check_figures: " + b, file=sys.stderr)
    if bad:
        print(f"\ncheck_figures: {len(bad)} of {checked} cited figures do not match the model.\n"
              "Regenerate with `make factsheet`, then correct the reports — the model is the "
              "authority, not the prose.", file=sys.stderr)
        return 1
    print(f"check_figures: {checked} cited figures across {len(REPORTS)} report(s) match the model")
    return 0


if __name__ == "__main__":
    sys.exit(main())
