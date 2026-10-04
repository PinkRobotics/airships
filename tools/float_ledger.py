#!/usr/bin/env python3
"""The float ledger: every float figure this repository quotes, with its basis.

    python3 tools/float_ledger.py            # regenerate both files
    python3 tools/float_ledger.py --check    # fail if either differs from a fresh generation
    python3 tools/float_ledger.py --names    # list every digit-bearing NAME the prose types

WHY THIS EXISTS. A lift-to-mass ratio means nothing without the hull it belongs to, the
altitude the lift was taken at, the safety factor the structure was sized with, and whether
the knockdown behind it was measured, cited or assumed. This repository has published float
figures stripped of all four — the same hull reads one ratio at sea level and a visibly
lower one at the altitude the fleet works at, and only the first was ever printed.

WHAT IT WRITES, from the model and the tools and from nothing else:

    research/analysis/float-ledger.json     the ledger, for gates and pages
    docs/FLOAT-LEDGER.md                    the same rows, for a reader

NO NUMBER IN EITHER FILE IS TYPED, and that is enforced rather than promised. A number can
reach the output only as a `Q` — a float that carries where it came from — and a `Q` is made
only by importing the model, running a tool, reading a generated file, or doing arithmetic on
other `Q`s. Every formatter wraps what it prints in private-use marks; before a file is
written the text is swept, and a single ASCII digit outside those marks aborts the run. Names
that happen to contain a digit ("Ship 0", "SP-8007") are typed between guillemets in this
source so they can be told from figures; `--names` lists them. The handful of definitions the
arithmetic needs (the sea-level datum, "no safety factor", kilograms per tonne) are declared
in DEFINITIONS below and printed in the ledger itself.

WHERE EACH NUMBER COMES FROM:
    research/analysis/vacuum-cell.py     imported: ship0(), rho_air(), kelvin_faces(), SHIP0
    research/analysis/vacuum-cell.py     run with --json: the model's own published payload
    tools/ship_scoping.py                run with --json (its default hull) and with --band
    tools/subdivision_study.py           run; the PUBLICATION SUMMARY block is parsed
    tools/scale_study.py                 run; the per-span blocks are parsed
    research/analysis/mass-budget.py     run with --json
    research/figures.json                read: the fleet model's atmosphere and class figures
    research/geometry/skin/loaded-skin.json, research/geometry/nodes/{manifest,assembly}.json
    git                                  the history table: every hash is resolved, every
                                         quoted value is read out of that commit's own files

The history table needs the commits themselves. In a shallow clone or an exported tree they
are not there; the table is then carried forward verbatim from the committed ledger and a
note is printed, so `--check` still means what it says everywhere the files can be compared.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True      # importing the model must not leave a __pycache__ behind

import argparse                     # noqa: E402
import ast                          # noqa: E402
import difflib                      # noqa: E402
import importlib.util               # noqa: E402
import inspect                      # noqa: E402
import json                         # noqa: E402
import hashlib                      # noqa: E402
import os                           # noqa: E402
import pathlib                      # noqa: E402
import re                           # noqa: E402
import shutil                       # noqa: E402
import subprocess                   # noqa: E402
import tempfile                     # noqa: E402
from types import SimpleNamespace   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "research" / "analysis" / "float-ledger.json"
OUT_MD = ROOT / "docs" / "FLOAT-LEDGER.md"

MODEL = "research/analysis/vacuum-cell.py"
SCOPING = "tools/ship_scoping.py"
SUBDIV = "tools/subdivision_study.py"
SCALE = "tools/scale_study.py"
BUDGET = "research/analysis/mass-budget.py"
FIGURES = "research/figures.json"
SKIN = "research/geometry/skin/loaded-skin.json"
MANIFEST = "research/geometry/nodes/manifest.json"
ASSEMBLY = "research/geometry/nodes/assembly.json"


# =====================================================================================
# PROVENANCE — the only road a digit can take into the output
# =====================================================================================
VO, VC = "", ""         # around a value computed by, or read out of, the repository
NO, NC = "«", "»"         # around a typed NAME that happens to contain a digit
ASCII_DIGITS = frozenset("0123456789")
NAMES_SEEN: set[str] = set()


class Q(float):
    """A number that knows where it came from. Nothing else may be printed."""

    def __new__(cls, value, src: str):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"float_ledger: not a number: {value!r} (from {src})")
        obj = super().__new__(cls, value)
        obj.src = src
        return obj


class S(str):
    """Text read out of the repository: a label, a citation, a commit subject."""

    def __new__(cls, value, src: str):
        obj = super().__new__(cls, value)
        obj.src = src
        return obj


class N:
    """A sourced number at the precision it is published at — what the outputs hold."""

    def __init__(self, x, dp: int):
        if not isinstance(x, Q):
            raise TypeError(f"float_ledger: a number with no source was about to be "
                            f"published: {x!r}")
        self.v = round(float(x), dp) + 0.0      # + 0.0 turns a negative zero into zero
        self.dp = dp
        self.src = x.src


def _q(*xs):
    for x in xs:
        if not isinstance(x, Q):
            raise TypeError(f"float_ledger: arithmetic on a number with no source: {x!r}")


def div(a, b):
    _q(a, b)
    return Q(float(a) / float(b), "derived")


def sub(a, b):
    _q(a, b)
    return Q(float(a) - float(b), "derived")


def add(a, b):
    _q(a, b)
    return Q(float(a) + float(b), "derived")


def mul(a, b):
    _q(a, b)
    return Q(float(a) * float(b), "derived")


# The definitions the arithmetic needs. These are the ONLY literals that reach a figure,
# and the ledger prints this table so a reader can see exactly what was typed.
DEFINITIONS = {
    "seaLevelM": (Q(0.0, "definition"), "the sea-level datum, in metres"),
    "noFactor": (Q(1.0, "definition"),
                 "a safety factor of one — the crush floor — and the float line, "
                 "lift ÷ mass = one"),
    "kiloPerUnit": (Q(1000.0, "definition"),
                    "kilograms in a tonne, grams in a kilogram, litres in a cubic metre"),
    "percent": (Q(100.0, "definition"), "parts in a hundred"),
}
ZERO_M = DEFINITIONS["seaLevelM"][0]
ONE = DEFINITIONS["noFactor"][0]
KILO = DEFINITIONS["kiloPerUnit"][0]
PERCENT = DEFINITIONS["percent"][0]


def fmt(n, sign: bool = False) -> str:
    """Print a published number: fixed decimals, thousands separators, a true minus."""
    if not isinstance(n, N):
        raise TypeError(f"float_ledger: only a published number (N) can be printed: {n!r}")
    body = f"{abs(n.v):,.{n.dp}f}"
    pre = "−" if n.v < 0 else ("+" if sign and n.v > 0 else "")
    return VO + pre + body + VC


def num(x, dp: int = 0, sign: bool = False) -> str:
    return fmt(N(x, dp), sign)


def bare(x, dp: int) -> str:
    """A number for an identifier: no separators, no sign — 'chord-1050', 'sf-1.2'."""
    n = N(x, dp)
    return VO + f"{n.v:.{dp}f}" + VC


def quote(s) -> str:
    """Text read out of the repository, printed as read."""
    if not isinstance(s, S):
        raise TypeError(f"float_ledger: only sourced text (S) can be quoted: {s!r}")
    return VO + str(s) + VC


def unmark(text: str, where: str) -> str:
    """Strip the marks — and refuse any digit that did not arrive inside them."""
    out, depth, name_from = [], 0, None
    for i, ch in enumerate(text):
        if ch in (VO, NO):
            depth += 1
            if ch == NO:
                name_from = len(out)
            continue
        if ch in (VC, NC):
            depth -= 1
            if depth < 0:
                sys.exit(f"float_ledger: unbalanced mark in {where}: "
                         f"{text[max(0, i - 60):i + 20]!r}")
            if ch == NC and name_from is not None:
                NAMES_SEEN.add("".join(out[name_from:]))
                name_from = None
            continue
        if depth == 0 and ch in ASCII_DIGITS:
            sys.exit(f"float_ledger: a TYPED DIGIT reached {where}: "
                     f"...{text[max(0, i - 70):i + 25]!r}\n"
                     "  every figure must come from the model or a tool (a Q), and every "
                     "digit-bearing name must sit between guillemets.")
        out.append(ch)
    if depth:
        sys.exit(f"float_ledger: unclosed mark in {where}")
    return "".join(out)


def plain(node, where: str = "ledger"):
    """The JSON tree with every number published and every string swept."""
    if isinstance(node, N):
        return int(node.v) if node.dp == 0 else node.v
    if node is None or isinstance(node, bool):
        return node
    if isinstance(node, (int, float)):
        sys.exit(f"float_ledger: a bare number reached the JSON at {where}: {node!r}")
    if isinstance(node, S):
        return str(node)
    if isinstance(node, str):
        return unmark(node, where)
    if isinstance(node, dict):
        return {unmark(k, where): plain(v, f"{where}/{unmark(k, where)}")
                for k, v in node.items()}
    if isinstance(node, (list, tuple)):
        return [plain(v, f"{where}[]") for v in node]
    sys.exit(f"float_ledger: cannot publish {type(node).__name__} at {where}")


# =====================================================================================
# READING THE MODEL, THE TOOLS AND THEIR FILES
# =====================================================================================
def die(msg: str) -> None:
    sys.exit("float_ledger: " + msg)


def load_module(rel: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_tool(rel: str, *args: str) -> str:
    """Run one of the repository's own tools and return what it printed."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    p = subprocess.run([sys.executable, str(ROOT / rel), *args], cwd=ROOT, env=env,
                       capture_output=True, text=True, errors="replace")
    if p.returncode != 0:
        die(f"{rel} {' '.join(args)} exited {p.returncode}:\n"
            + (p.stdout[-1500:] + p.stderr[-1500:]))
    return p.stdout


def run_json(rel: str, out: pathlib.Path) -> dict:
    """Run a tool with --json into scratch and read its payload back."""
    run_tool(rel, "--json", str(out))
    if not out.exists():
        die(f"{rel} --json wrote nothing")
    return json.loads(out.read_text(encoding="utf-8"))


def read_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def dig(doc, pointer: str):
    for part in pointer.split("/"):
        doc = doc[int(part)] if isinstance(doc, list) else doc[part]
    return doc


def qp(doc, pointer: str, src: str) -> Q:
    return Q(dig(doc, pointer), f"{src}: {pointer}")


def sp(doc, pointer: str, src: str) -> S:
    return S(dig(doc, pointer), f"{src}: {pointer}")


def qtext(text: str, src: str) -> Q:
    return Q(float(text.replace(",", "")), src)


def agree(a, b, dp: int) -> bool:
    """Two figures agree at a print precision of dp decimals."""
    return abs(float(a) - float(b)) <= 0.5 * 10.0 ** (-dp) + 1e-9


# ---- tools/ship_scoping.py --band ----------------------------------------------------
_BAND_HEAD = re.compile(
    r"^\s+(house-harsh|frame-practice) (\S+) .*?@ (\d+) MPa(, both moves)?:(.*)$")
_BAND_ROW = re.compile(
    r"^\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+([+-]\d+\.\d+)\s+(\d+\.\d+|-)\s*(\[.*\])?$")
_BAND_MOVE = re.compile(
    r"^\s+(as drawn|chordal spoke net|in-surface shear|both moves)\s+crush\s+(\S+) t\s+"
    r"band\s+(\S+) t\s+@SF(\S+)\s+(\S+) t ratio (\S+) (FLOATS|sinks)$")
_BAND_CLOSED = re.compile(r"band (?:CLOSED at every hull|still closed) "
                          r"\(best (\S+) t at (\d+) m\)")
_BAND_WIDEST = re.compile(r"widest at (\d+) m - design at (\S+) t:")
_BAND_SPLIT = re.compile(r"float reserve (\S+) t AND emergent SF (\S+)\s+"
                         r"\(crush (\S+) / lift (\S+)\)")
_BAND_GOAL = re.compile(r"-> mid-band at (\d+) m: (\S+) t, float\s+reserve (\S+) t, "
                        r"emergent SF (\S+)")


def parse_band(out: str) -> SimpleNamespace:
    """The band study's own tables, as the tool prints them."""
    src = f"{SCOPING} --band (stdout)"
    res = SimpleNamespace(record=None, band={}, moves={}, mid={}, goal={}, goal_result={})
    m = re.search(r"record reproduced first: (\S+) t, ratio (\S+) at (\S+) m", out)
    if not m:
        die("the band study did not print its 'record reproduced first' line")
    res.record = dict(massT=qtext(m[1], src), ratio=qtext(m[2], src),
                      diaM=qtext(m[3], src))
    section, world = None, None
    lines = out.splitlines()
    for i, line in enumerate(lines):
        for head, name in (("THE BAND, BY HULL", "band"), ("THE TWO DESIGN MOVES", "moves"),
                           ("MID-BAND DESIGN POINTS", "mid"),
                           ("THE DESIGN-GOAL SCENARIO", "goal")):
            if line.startswith(head):
                section, world = name, None
        h = _BAND_HEAD.match(line)
        if h and section:
            world = (float(h[2]), float(h[3]))
            label = S(f"{h[1]} {h[2]}", src)
            if section == "band":
                res.band[world] = dict(label=label, rows=[])
            elif section == "goal":
                res.goal[world] = dict(label=label, rows=[])
            elif section == "moves":
                res.moves[world] = dict(label=label, rows={})
            elif section == "mid":
                c = _BAND_CLOSED.search(h[5])
                w = _BAND_WIDEST.search(h[5])
                if c:
                    res.mid[world] = dict(closed=True, bestBandT=qtext(c[1], src),
                                          bestDiaM=qtext(c[2], src))
                elif w and i + 1 < len(lines):
                    s2 = _BAND_SPLIT.search(lines[i + 1])
                    if not s2:
                        die("the band study's mid-band line changed shape")
                    res.mid[world] = dict(
                        closed=False, diaM=qtext(w[1], src), designT=qtext(w[2], src),
                        reserveT=qtext(s2[1], src),
                        emergentSF=None if s2[2] == "-" else qtext(s2[2], src),
                        crushT=qtext(s2[3], src), liftT=qtext(s2[4], src))
                else:
                    die("the band study's mid-band block changed shape")
            continue
        if world is None:
            continue
        r = _BAND_ROW.match(line)
        if r and section in ("band", "goal"):
            row = dict(diaM=qtext(r[1], src), crushT=qtext(r[2], src),
                       liftT=qtext(r[3], src), bandT=qtext(r[4], src),
                       sfFloat=None if r[5] == "-" else qtext(r[5], src),
                       guard=bool(r[6]))
            (res.band if section == "band" else res.goal)[world]["rows"].append(row)
            continue
        mv = _BAND_MOVE.match(line)
        if mv and section == "moves":
            res.moves[world]["rows"][mv[1]] = dict(
                crushT=qtext(mv[2], src), bandT=qtext(mv[3], src), sf=qtext(mv[4], src),
                massT=qtext(mv[5], src), ratio=qtext(mv[6], src), floats=mv[7] == "FLOATS")
            continue
        if section == "goal":
            g = _BAND_GOAL.search(line)
            c = _BAND_CLOSED.search(line)
            if g:
                res.goal_result[world] = dict(
                    closed=False, diaM=qtext(g[1], src), designT=qtext(g[2], src),
                    reserveT=qtext(g[3], src),
                    emergentSF=None if g[4] == "-" else qtext(g[4], src))
            elif c:
                res.goal_result[world] = dict(closed=True, bestBandT=qtext(c[1], src),
                                              bestDiaM=qtext(c[2], src))
    for name in ("band", "moves", "mid", "goal", "goal_result"):
        got = getattr(res, name)
        if len(got) < 2 or any(("rows" in v and not v["rows"]) for v in got.values()):
            die(f"the band study's '{name}' block could not be read — "
                f"{SCOPING} --band changed its output")
    return res


# ---- tools/subdivision_study.py -------------------------------------------------------
def parse_subdivision(out: str) -> SimpleNamespace:
    src = f"{SUBDIV} (stdout, PUBLICATION SUMMARY)"
    i = out.find("PUBLICATION SUMMARY")
    if i < 0:
        die(f"{SUBDIV} printed no PUBLICATION SUMMARY")
    lines = out[i:].splitlines()
    cols = lines[1].split()
    want = ["span", "n", "nodes", "strut_mm", "OD_mm", "wall_mm", "tube_kgm3", "joint_kgm3",
            "film_kgm3", "total_kgm3", "over_wall"]
    if cols[:len(want)] != want:
        die(f"{SUBDIV} changed its publication columns: {cols}")
    rows = []
    for line in lines[2:]:
        if "best documented row" in line or not line.strip():
            break
        t = line.split()
        rows.append(dict(
            spanM=qtext(t[0], src), n=qtext(t[1], src), nodes=qtext(t[2], src),
            strutMm=qtext(t[3], src), odMm=qtext(t[4], src), wallMm=qtext(t[5], src),
            tubeKgM3=qtext(t[6], src), jointKgM3=qtext(t[7], src),
            filmKgM3=qtext(t[8], src), totalKgM3=qtext(t[9], src),
            overWall=qtext(t[10], src), filmMarginAtSF=qtext(t[14], src),
            governor=S(" ".join(t[15:]), src)))
    if not rows:
        die(f"{SUBDIV} printed no publication rows")
    w = re.search(r"the wall is (\S+) kg/m3\. None of the checked rows floats\.", out)
    if not w:
        die(f"{SUBDIV} no longer prints 'None of the checked rows floats'")
    unc = re.search(r"NOT YET COUNTED:\n\s+(.+)", out)
    est = re.search(r"Estimate/source uncertainties[^\n]*\n\s+(.+)", out)
    return SimpleNamespace(
        rows=rows, wall=qtext(w[1], src),
        notCounted=S(unc[1].strip(), src) if unc else None,
        uncertain=S(est[1].strip(), src) if est else None)


# ---- tools/scale_study.py -------------------------------------------------------------
_SCALE_BLOCK = re.compile(
    r"^SPAN (\S+) — (PARITY with today|\+\d+% on every margin): main (\S+), rim (\S+)\n"
    r"\s+tube (\S+) kg \+ joints ~(\S+) kg \(od\^\d estimate\) \+ film (\d+) g = (\S+) kg\n"
    r"\s+(\S+) kg/m3\s+vs the wall (\S+) -> (\S+)x\s+vs sea-level air (\S+)x", re.M)
_SCALE_GEOM = re.compile(
    r"^\s+span (\S+): main \S+, rim \S+\s+\(\S+x\)\n[^\n]*\n"
    r"\s+(\S+) kg -> (\S+) kg/m3 \(unchanged\), film (\d+) g", re.M)
_SCALE_PRINT = re.compile(
    r"^\s+span (\S+):\s+(\d+) joints/m3,\s+(\d+) cuts/m3,\s+(\S+) kg printed/m3,"
    r"\s+(\S+) g per joint", re.M)


def parse_scale(out: str) -> SimpleNamespace:
    src = f"{SCALE} (stdout)"
    blocks = [dict(spanM=qtext(m[1], src), label=S(m[2], src), mainTube=S(m[3], src),
                   rimTube=S(m[4], src), tubeKg=qtext(m[5], src), jointsKg=qtext(m[6], src),
                   filmG=qtext(m[7], src), totalKg=qtext(m[8], src),
                   kgPerM3=qtext(m[9], src), wall=qtext(m[10], src),
                   overWall=qtext(m[11], src), overSeaLevelAir=qtext(m[12], src))
              for m in _SCALE_BLOCK.finditer(out)]
    if not blocks:
        die(f"{SCALE} printed no SPAN blocks this tool can read")
    geom = [dict(spanM=qtext(m[1], src), totalKg=qtext(m[2], src),
                 kgPerM3=qtext(m[3], src)) for m in _SCALE_GEOM.finditer(out)]
    printed = [dict(spanM=qtext(m[1], src), jointsPerM3=qtext(m[2], src),
                    cutsPerM3=qtext(m[3], src), printedKgPerM3=qtext(m[4], src),
                    gPerJoint=qtext(m[5], src)) for m in _SCALE_PRINT.finditer(out)]
    return SimpleNamespace(blocks=blocks, geom=geom, printed=printed)


# =====================================================================================
# THE FACTS — everything the ledger says, gathered once
# =====================================================================================
def gather(scratch: pathlib.Path) -> SimpleNamespace:
    F = SimpleNamespace()
    vc = load_module(MODEL, "vacuum_cell_for_the_float_ledger")
    F.vc = vc
    fig = read_json(FIGURES)
    F.fig = fig

    # The atmosphere. The target altitude is the fleet model's working altitude; the ship
    # model hard-codes the same height, and a self-check holds the two together.
    F.alt_sl = ZERO_M
    F.alt_t = qp(fig, "atmosphere/workAltMslM", FIGURES)
    F.alt_g = qp(fig, "atmosphere/terrainMslM", FIGURES)
    rsrc = f"{MODEL}: rho_air()"
    F.rho_sl = Q(vc.rho_air(float(F.alt_sl)), rsrc)
    F.rho_t = Q(vc.rho_air(float(F.alt_t)), rsrc)
    F.rho_g = Q(vc.rho_air(float(F.alt_g)), rsrc)
    F.fig_rho_sl = qp(fig, "atmosphere/rhoSeaLevel", FIGURES)
    F.fig_rho_t = qp(fig, "atmosphere/rhoAtWorkAlt", FIGURES)
    F.fig_rho_g = qp(fig, "atmosphere/rhoAtGround", FIGURES)

    sh = vc.SHIP0
    c = f"{MODEL}: SHIP0"
    F.sf_decl = Q(sh["sfDeclared"], c)
    F.sf_lat = Q(vc.LATTICE_SF, f"{MODEL}: LATTICE_SF")
    F.gi_harsh = Q(sh["giKnockdown"], c)
    F.gi_frame = Q(sh["giKnockdownFrame"], c)
    F.k_shell = Q(vc.K_SHELL, f"{MODEL}: K_SHELL")
    F.k_local = Q(vc.K_LOCAL, f"{MODEL}: K_LOCAL")
    F.k_classical = Q(vc.K_CLASSICAL, f"{MODEL}: K_CLASSICAL")
    F.ortho = Q(vc.ORTHO_PENALTY, f"{MODEL}: ORTHO_PENALTY")
    F.eta = Q(sh["etaMass"], c)
    F.node_frac = Q(vc.NODE_MASS_FRAC, f"{MODEL}: NODE_MASS_FRAC")
    film_params = inspect.signature(vc.barrier_kg_per_m2).parameters
    F.film_sf = Q(film_params['sf'].default, MODEL + ': barrier_kg_per_m2(), default sf')
    F.film_eff = Q(film_params['eff'].default, MODEL + ': barrier_kg_per_m2(), default eff')
    F.dia = Q(sh["diaM"], c)
    F.depth = Q(sh["depthM"], c)
    F.sigmas = sorted(((S(k, c), Q(v, c)) for k, v in sh["sigmaWorldsMPa"].items()),
                      key=lambda kv: float(kv[1]))
    F.sig_mid = next(kv for kv in F.sigmas if kv[0] == sh["sigmaMid"])
    F.sig_lo, F.sig_hi = F.sigmas[0], F.sigmas[-1]

    F.P = run_json(MODEL, scratch / "vacuum-cell.json")
    F.SS = run_json(SCOPING, scratch / "ship-scoping.json")
    F.band = parse_band(run_tool(SCOPING, "--band"))
    F.sub = parse_subdivision(run_tool(SUBDIV))
    F.scale = parse_scale(run_tool(SCALE))
    F.MB = run_json(BUDGET, scratch / "mass-budget.json")
    F.skin = read_json(SKIN)
    F.manifest = read_json(MANIFEST)
    F.assembly = read_json(ASSEMBLY)
    F.source_artifacts = []
    for rel, fresh in [("research/analysis/vacuum-cell.json", "vacuum-cell.json"),
                       ("research/analysis/ship-scoping.json", "ship-scoping.json"),
                       ("research/analysis/mass-budget.json", "mass-budget.json")]:
        now=(scratch / fresh).read_bytes(); committed=(ROOT / rel).read_bytes()
        changed=[]
        def differences(a, b, pointer=""):
            if isinstance(a,dict) and isinstance(b,dict):
                for key in a.keys() & b.keys():
                    differences(a[key],b[key],pointer+"/"+key)
            elif isinstance(a,list) and isinstance(b,list):
                for i,(x,y) in enumerate(zip(a,b)):
                    differences(x,y,pointer+"/"+str(i))
            elif isinstance(a,(int,float)) and not isinstance(a,bool) and a != b:
                changed.append(dict(pointer=S(pointer.lstrip('/'),rel),
                    old=N(Q(a,rel+" committed"),9),fresh=N(Q(b,rel+" fresh"),9)))
        differences(json.loads(committed),json.loads(now))
        changed.sort(key=lambda r:str(r['pointer']))
        F.source_artifacts.append(dict(path=rel, freshSha=S(hashlib.sha256(now).hexdigest(), "fresh tool bytes"),
            committedSha=S(hashlib.sha256(committed).hexdigest(), "committed tool bytes"),
            committedEqualsFresh=now==committed,changedNumbers=changed))
    F.checks = []           # the generator's own cross-checks, as published
    F.findings = []
    F.all_cases = []
    F.pressure_inputs = []
    F.reg = {}              # every ship row, built once: (hull, basis, chord, SF, moves)
    return F


def check(F, what: str, ok: bool) -> None:
    """A cross-check between two computations of the same thing. A miss stops the run:
    the ledger would otherwise be making a statement its own sources disagree about."""
    F.checks.append({"check": what, "holds": bool(ok)})
    if not ok:
        die("SELF-CHECK FAILED — " + unmark(what, "a self-check"))


def ship(F, key, sf, dia=None, gi=None, chordal: bool = False, membrane: bool = False):
    """One whole-ship ledger from the model, every figure sourced. None when the model's
    section catalogue cannot build that hull."""
    try:
        r = F.vc.ship0(str(key), float(sf), None if dia is None else float(dia),
                       None if gi is None else float(gi), chordal, membrane,
                       basis=F.vc.ship_basis(None, None if gi is None else float(gi)))
    except RuntimeError:
        return None
    src = f"{MODEL}: ship0()"
    o = SimpleNamespace()
    o.mass = Q(r["totalT"], src)
    o.lift_sl = Q(r["liftSLT"], src)
    o.lift_t = Q(r["lift2500T"], src)
    o.ratio_sl = Q(r["ratioSL"], src)
    o.ratio_t = Q(r["ratio2500"], src)
    o.areal = Q(r["arealKgM2"], src)
    g = r["geom"]
    o.dia, o.len, o.vol, o.area, o.depth = (Q(g[k], src) for k in
                                            ("diaM", "lenM", "vM3", "areaM2", "depthM"))
    o.per_m3 = div(mul(o.mass, KILO), o.vol)        # structure, kg per m3 enclosed
    o.checks_pass = bool(r["checksPass"])
    o.lines = [(S(k, src), Q(v, src)) for k, v in r["ledgerT"].items()]
    return o


def at_block(alt, rho, mass, lift, dp: int, inv_dp: int = 3, lift_dp: int = None) -> dict:
    """One altitude's half of a row: the air displaced there against the same mass."""
    return {"altitudeM": N(alt, 0), "rhoAirKgPerCubicM": N(rho, 4),
            "lift": N(lift, dp if lift_dp is None else lift_dp),
            "liftToMass": N(div(lift, mass), 3), "massToLift": N(div(mass, lift), inv_dp),
            "margin": N(sub(lift, mass), dp), "floats": bool(float(lift) > float(mass))}


def ship_at(F, o) -> dict:
    return {"seaLevel": at_block(F.alt_sl, F.rho_sl, o.mass, o.lift_sl, 1),
            "target": at_block(F.alt_t, F.rho_t, o.mass, o.lift_t, 1)}


def density_at(F, kg_per_m3, dp: int = 4, inv_dp: int = 2) -> dict:
    """A density row: the object's mass per m3 enclosed against the air in that m3."""
    return {"seaLevel": at_block(F.alt_sl, F.rho_sl, kg_per_m3, F.rho_sl, dp, inv_dp, 4),
            "target": at_block(F.alt_t, F.rho_t, kg_per_m3, F.rho_t, dp, inv_dp, 4)}


QUANTITY = "lift ÷ mass, mass ÷ lift, and the margin lift − mass"
DECLARED = "declared — applied to every member check"
BESIDE = "the model's lattice factor, shown beside the declared one"
CRUSH = "none — the crush floor: every capacity meets its demand with no margin at all"
AS_DRAWN, BOUND, CLOSED_FORM, STUDY = "as drawn", "a bound, not a design", \
    "closed form, no design", "a sizing study, not drawn"


def make_case(F, cid, label, mass, mass_dp, unit, at, sf, sf_kind, kds, inputs, status,
              evidence, code, moves, why_not=None, extras=None) -> dict:
    c = {"id": cid, "label": label, "quantity": QUANTITY, "massUnit": unit,
         "mass": N(mass, mass_dp),
         "safetyFactor": {"value": None if sf is None else N(sf, 2), "kind": sf_kind},
         "knockdowns": kds, "inputs": inputs, "designStatus": status,
         "evidence": evidence, "sizingPressure": {"valuePa": None if evidence in ("assumed", "literature") else N(Q(F.vc.P_ATM, MODEL + ": P_ATM"), 0),
             "basis": "Full vacuum against sea-level pressure; altitude changes lift only. Assumed allowances and literature rows are not structural sizing results."}, "codePath": code, "whatWouldMoveIt": moves, "at": at}
    reads = any(v["floats"] or v["liftToMass"].v >= float(ONE) for v in at.values())
    c["readsOneOrMore"] = reads
    qualifies = (status == AS_DRAWN and evidence == "reviewed-model" and sf is not None
                 and float(sf) >= float(F.sf_decl) and at["target"]["floats"])
    c["floatsToday"] = qualifies
    if reads and not qualifies:
        if not why_not:
            die("a row reads one or more and gives no reason it is not a floating "
                "design: " + unmark(cid, "a row id"))
        c["notAFloatingDesignBecause"] = why_not
    if extras:
        c["extras"] = extras
    if evidence not in ('assumed', 'literature') and not cid.startswith('vintage-') and cid != 'closed-bare':
        c['filmSizing'] = {'safetyFactor': N(F.film_sf, 1), 'efficiency': N(F.film_eff, 2),
            'efficiencyStatus': 'assumed', 'codePath': MODEL + ': `«barrier_kg_per_m2()»`',
            'basis': 'Separate film sizing defaults; not the structural factor printed in the row.'}
    F.all_cases.append(c)
    return c


def table(head: list, rows: list, align: str = "") -> str:
    """A Markdown table; align is one letter per column, l or r."""
    align = align or "l" * len(head)
    out = ["| " + " | ".join(head) + " |",
           "|" + "|".join(" ---: " if a == "r" else " --- " for a in align) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def refs(K: dict, *ids: str) -> list:
    return [{"id": i, "value": K[i]["value"], "status": K[i]["status"]} for i in ids]


EVIDENCE = {
    "reviewed-model": (
        "reviewed model",
        "Computed by `research/analysis/vacuum-cell.py` on its record path: the path "
        "`make cellparity` holds the browser model to, and the one two recorded adversarial "
        "reviews attacked and changed (see the history). REVIEWED DESCRIBES THE CODE, NOT "
        "THE INPUTS — every knockdown and allowable in such a row still carries its own "
        "status, and most are assumed."),
    "to-verify": (
        "unreviewed or [TO VERIFY]",
        "Computed, but the result turns on an input the code itself marks [TO VERIFY] or "
        "[SCOPING], or comes from a study script or an output file no gate holds, or "
        "describes an object off the record path."),
    "assumed": (
        "assumed basis",
        "An assumed allowance or arithmetic conditional on an assumption; not a structurally validated result."),
    "literature": (
        "literature",
        "A published value, on its author's own basis, cited where it appears."),
    "measured": (
        "measured",
        "A weighed or tested physical object. NO ROW IN THIS LEDGER IS ONE: nothing here "
        "has been built."),
}


def ev(code: str) -> str:
    return EVIDENCE[code][0]


def knockdown_registry(F) -> dict:
    sb = F.P["stockBuild"]
    psrc = f"{MODEL} --json"
    F.joint_share = mul(div(qp(sb, "printed/nodesKg", psrc), qp(sb, "pipe/kg", psrc)),
                        PERCENT)
    K = {}
    K["gi-harsh"] = dict(
        name="general-instability knockdown γ on the ring, web and spoke capacity "
             "(Bryant's form, minimised over the buckling wave number)",
        value=N(F.gi_harsh, 2), status="assumed",
        basis="The model calls it house-harsh and SIZES THE RECORD with it. No test and no "
              "citation in this repository stands behind the value.")
    K["gi-reserve"] = dict(
        name=f"imperfection knockdown priced as a stability reserve ({NO}K_SHELL{NC})",
        value=N(F.k_shell, 2), status="assumed",
        basis="On the harsh basis the ledger also buys the mass that would hold the hull "
              "at this lower knockdown — its stability-reserve line. No source is cited.")
    K["gi-frame"] = dict(
        name="general-instability knockdown γ, the frame-practice world",
        value=N(F.gi_frame, 2), status="assumed",
        basis=f"Marked [TO VERIFY — {NO}SHIP-2{NC} knockdown tests] in the model. A practice "
              "is named (ring-framed pressure hulls with out-of-round control); no source "
              "is cited and no test exists. Reported beside the record, never sized at, and "
              "no reserve is priced on this basis.")
    K["local-wall"] = dict(
        name=f"knockdown on the classical local wall-buckling coefficient ({NO}K_LOCAL{NC})",
        value=N(F.k_local, 2), status="assumed",
        basis=f"The model's comment names NASA {NO}SP-8007{NC} and calls its own value "
              "mildly conservative for an isotropic wall. No page, figure or test establishes "
              "this numerical choice for the model's composite wall; treated here as assumed.")
    K["classical"] = dict(
        name=f"classical thin-cylinder buckling coefficient ({NO}K_CLASSICAL{NC})",
        value=N(F.k_classical, 3), status="literature",
        basis="Textbook theory — part of the formula, not a knockdown. Until the correction "
              "recorded in the history, four closed-form routes left it out.")
    K["ortho"] = dict(
        name=f"orthotropic-wall penalty on the laminate modulus ({NO}ORTHO_PENALTY{NC})",
        value=N(F.ortho, 4), status="assumed",
        basis="Derived in the model for a cross-ply tube wall at its best fibre split. No "
              "source is cited and no tube has been tested.")
    K["joint-mass"] = dict(
        name="joint mass efficiency η: joints billed as member mass × (one ÷ η − one)",
        value=N(F.eta, 2), status="assumed",
        basis="Marked [TO VERIFY] in the scoping tool. No joint of this hull has been "
              "designed.")
    K["node-fraction"] = dict(
        name=f"node allowance as a fraction of lattice mass ({NO}NODE_MASS_FRAC{NC})",
        value=N(F.node_frac, 2), status="assumed",
        basis="The model's working figure, inside a range it calls usual. The one article "
              f"whose joints were drawn carries them at {num(F.joint_share, 1)} % of its "
              "tube mass (the bench cell, below).")
    return K


def chord_input(F, key, mpa) -> dict:
    if key == F.sig_hi[0]:
        status = "literature"
        basis = (f"The scoping tool cites a Toray zero-degree datasheet ceiling (SACMA "
                 f"{NO}SRM 1R-94{NC}, sixty percent fibre volume): a unidirectional coupon "
                 "value, not a test of this chord. [TO VERIFY — coupon campaign].")
    elif key == F.sig_mid[0]:
        status = "assumed"
        basis = (f"The scoping tool calls it the {NO}[0/90]{NC} working estimate. "
                 "[TO VERIFY — coupon campaign].")
    else:
        status = "assumed"
        basis = ("The scoping tool calls it co-critical verified-class; no coupon data is "
                 "in this repository. [TO VERIFY — coupon campaign].")
    return {"name": "chord axial-compressive allowable", "value": N(mpa, 0), "unit": "MPa",
            "status": status, "basis": basis}


SHIP_CODE = f"`{MODEL}`: `{NO}ship0(){NC}`"


def world_words(F, gi) -> str:
    return "harsh" if float(gi) == float(F.gi_harsh) else "frame-practice"


def ship_kds(F, K, gi) -> list:
    if float(gi) == float(F.gi_harsh):
        return refs(K, "gi-harsh", "gi-reserve", "classical", "local-wall", "ortho",
                    "joint-mass")
    return refs(K, "gi-frame", "classical", "local-wall", "ortho", "joint-mass")


# =====================================================================================
# THE SHIP ROWS — every one built by the same function, from the model
# =====================================================================================
VARIANTS = (("as drawn", False, False), ("chordal spoke net", True, False),
            ("in-surface shear", False, True), ("both moves", True, True))
SCALED = "scaled from the record hull by rule, not drawn"
MOVES_SHIP = ("The knockdown tests and the chord coupon campaign, which the model names as "
              "the two things that decide it; the two design moves it prices only as "
              "bounds; wall depth and ring pitch; joint mass, which is an efficiency factor "
              "here and not a design.")


def cap(text: str) -> str:
    return text[:1].upper() + text[1:]


def ship_case(F, K, dia, gi, sig, sf, chordal: bool = False, membrane: bool = False):
    """One ship row and the model result behind it; (None, None) if the model's section
    catalogue cannot build that hull at that factor."""
    key, mpa = sig
    tup = (round(float(dia), 6), float(gi), str(key), round(float(sf), 6), chordal, membrane)
    if tup in F.reg:
        return F.reg[tup]
    o = ship(F, key, sf, dia, gi, chordal, membrane)
    if o is None:
        F.reg[tup] = (None, None)
        return F.reg[tup]
    harsh = float(gi) == float(F.gi_harsh)
    on_record = agree(dia, F.dia, 6)
    as_drawn = not (chordal or membrane)
    crush = float(sf) < float(F.sf_decl)
    vname = next(n for n, c, m in VARIANTS if c == chordal and m == membrane)
    status = AS_DRAWN if (as_drawn and on_record) else (SCALED if as_drawn else BOUND)
    evidence = "reviewed-model" if (harsh and as_drawn and on_record) else "to-verify"
    if agree(sf, F.sf_decl, 6):
        sfk, sfw = DECLARED, f"SF {num(sf, 1)}"
    elif agree(sf, F.sf_lat, 6):
        sfk, sfw = BESIDE, f"SF {num(sf, 1)}"
    elif agree(sf, ONE, 6):
        sfk, sfw = CRUSH, "the crush floor (no safety factor)"
    else:
        sfk, sfw = "as stated", f"SF {num(sf, 2)}"
    at = ship_at(F, o)
    F.law_ok = getattr(F, "law_ok", True) and (
        abs(float(o.lift_t) - float(o.lift_sl) * float(F.rho_t) / float(F.rho_sl)) < 1e-9
        and abs(float(o.ratio_sl) - float(o.lift_sl) / float(o.mass)) < 1e-12
        and abs(float(o.ratio_t) - float(o.lift_t) / float(o.mass)) < 1e-12)
    why = []
    if not harsh:
        why.append("it stands on the frame-practice knockdown, which no test supports and "
                   "the model marks [TO VERIFY]")
    if key == F.sig_hi[0]:
        why.append("it takes the chord allowable at a datasheet ceiling the coupon campaign "
                   "has not confirmed")
    if chordal:
        why.append("the chordal spoke net is a bound — cord mass priced at diametral-cord "
                   "rates, geometry and terminations [SCOPING], nothing drawn")
    if membrane:
        why.append("the in-surface shear system is an outer bound — its stiffness is "
                   "credited and its own mass is not priced")
    if crush:
        why.append("it carries no safety factor: every member sits exactly at its demand")
    if not on_record:
        why.append("the hull is scaled from the record by rule and has not been drawn")
    if at["seaLevel"]["floats"] and not at["target"]["floats"]:
        why.append(f"it clears the float line at sea level only — at "
                   f"{fmt(at['target']['altitudeM'])} m the same row reads "
                   f"{fmt(at['target']['liftToMass'])}")
    label = (f"{num(o.dia, 0)} m hull, {vname}, {world_words(F, gi)} stability basis "
             f"(γ {num(gi, 2)}), chords at {num(mpa, 0)} MPa, {sfw}")
    cid = (f"hull-{bare(o.dia, 0)}m/{vname.replace(' ', '-')}/gamma-{bare(gi, 2)}/"
           f"chord-{bare(mpa, 0)}/sf-{bare(sf, 1)}")
    c = make_case(
        F, cid, label, o.mass, 1, "t", at, sf, sfk, ship_kds(F, K, gi),
        [chord_input(F, key, mpa)], status, evidence, SHIP_CODE, MOVES_SHIP,
        (cap("; ".join(why)) + ".") if why else None,
        extras={"hullDiameterM": N(o.dia, 1), "wallDepthM": N(o.depth, 2),
                "enclosedCubicM": N(o.vol, 0), "hullAreaSqM": N(o.area, 0),
                "arealKgPerSqM": N(o.areal, 2), "structureKgPerCubicMEnclosed": N(o.per_m3, 3),
                "memberChecksPass": o.checks_pass})
    F.pressure_inputs.append((c, o.mass, o.lift_sl))
    F.reg[tup] = (c, o)
    return F.reg[tup]


def kd_table(K: dict, ids: list) -> str:
    return table(["Factor", "Value", "Status", "Basis"],
                 [[K[i]["name"], fmt(K[i]["value"]), K[i]["status"], K[i]["basis"]]
                  for i in ids], "lrll")


def a(c: dict, where: str, field: str, sign: bool = False) -> str:
    return fmt(c["at"][where][field], sign)


def d_record(F, K):
    P0 = F.P["ship0"]
    psrc = f"{MODEL} --json"
    alt0, altT = num(F.alt_sl, 0), num(F.alt_t, 0)
    cases, rows = [], []
    for gi in (F.gi_harsh, F.gi_frame):
        for sf in (F.sf_decl, F.sf_lat):
            for sig in F.sigmas:
                c, o = ship_case(F, K, F.dia, gi, sig, sf)
                if c is None:
                    die("the model could not build the record hull")
                cases.append(c)
                rows.append([num(gi, 2), num(sig[1], 0), num(sf, 1), fmt(c["mass"]),
                             a(c, "seaLevel", "liftToMass"), a(c, "seaLevel", "margin", True),
                             a(c, "target", "liftToMass"), a(c, "target", "margin", True),
                             ev(c["evidence"])])
    F.c_rec, F.o_rec = ship_case(F, K, F.dia, F.gi_harsh, F.sig_mid, F.sf_decl)
    F.c_best, F.o_best = ship_case(F, K, F.dia, F.gi_frame, F.sig_hi, F.sf_decl)
    rec, best, cr, cb = F.o_rec, F.o_best, F.c_rec, F.c_best

    check(F, "the model's published record (its --json payload) is the row this ledger "
             "computes by calling it: mass, sea-level ratio and target-altitude ratio",
          agree(rec.mass, qp(P0, "mid/totalT", psrc), 1)
          and agree(rec.ratio_sl, qp(P0, "mid/ratioSL", psrc), 3)
          and agree(rec.ratio_t, qp(P0, "mid/ratio2500", psrc), 3))
    check(F, "the scoping tool's band study reproduces the same record before it prints "
             "anything (mass, ratio, hull diameter)",
          agree(rec.mass, F.band.record["massT"], 1)
          and agree(rec.ratio_sl, F.band.record["ratio"], 3)
          and agree(rec.dia, F.band.record["diaM"], 0))

    design = {
        "id": f"{NO}ship0{NC}-record", "name": f"{NO}Ship 0{NC} — the hull of record",
        "object": (f"A capsule {num(rec.dia, 0)} m across and {num(rec.len, 0)} m long "
                   f"enclosing {num(rec.vol, 0)} m³ behind {num(rec.area, 0)} m² of hull: "
                   f"film on hoop rings over a two-walled skeleton {num(rec.depth, 1)} m "
                   "deep, with diametral tension spokes, as drawn."),
        "geometry": {"diameterM": N(rec.dia, 1), "lengthM": N(rec.len, 1),
                     "enclosedCubicM": N(rec.vol, 0), "hullAreaSqM": N(rec.area, 0),
                     "wallDepthM": N(rec.depth, 2)},
        "lift": {"seaLevelT": N(rec.lift_sl, 1), "targetT": N(rec.lift_t, 1)},
        "massBreakdownT": {
            "record": {quote(k): N(v, 1) for k, v in rec.lines},
            "bestDefensibleWorld": {quote(k): N(v, 1) for k, v in best.lines}},
        "cases": cases,
    }

    chk = P0["checks"]
    gm_h, gm_f = qp(chk, "giMarginHarsh", psrc), qp(chk, "giMarginFrame", psrc)
    gm_r, wind = qp(chk, "giMarginK02", psrc), qp(chk, "windMargin", psrc)
    miss_sl = mul(sub(ONE, best.ratio_sl), PERCENT)
    miss_t = mul(sub(ONE, best.ratio_t), PERCENT)
    lines = [(f"`{quote(k)}`", num(v, 1), num(v2, 1))
             for (k, v), (_, v2) in zip(rec.lines, best.lines)]
    md = f"""## {NO}Ship 0{NC} — the hull of record

**The object.** {design["object"]} This is the hull the gated model carries
(`{MODEL}`, mirrored in `ship/model.js`) and the viewer draws.

**Lift.** {num(rec.lift_sl, 1)} t at sea level; {num(rec.lift_t, 1)} t at {altT} m. One
hull, two lifts — and every mass below is the same at both, because the structure is
sized for sea-level pressure either way.

**Safety factor.** {num(F.sf_decl, 1)} declared, applied to every member check;
{num(F.sf_lat, 1)} always shown beside it.

**Code path.** {SHIP_CODE}, called once per row.
**Evidence.** The harsh-basis rows are *{ev("reviewed-model")}*; the frame-practice rows
are *{ev("to-verify")}*.

{kd_table(K, ["gi-harsh", "gi-reserve", "gi-frame", "classical", "local-wall", "ortho",
              "joint-mass"])}

{table(["Chord axial-compressive allowable (MPa)", "Status", "Basis"],
       [[num(m, 0), chord_input(F, k, m)["status"], chord_input(F, k, m)["basis"]]
        for k, m in F.sigmas], "rll")}

{table(["Knockdown γ", "Chord allowable (MPa)", "SF", "Mass (t)",
        f"Lift ÷ mass at {alt0} m", f"Margin at {alt0} m (t)",
        f"Lift ÷ mass at {altT} m", f"Margin at {altT} m (t)", "Evidence"],
       rows, "rrrrrrrrl")}

**The two rows the site quotes.** The record — harsh knockdown, mid coupons, declared
factor — weighs {fmt(cr["mass"])} t: lift ÷ mass {a(cr, "seaLevel", "liftToMass")} at sea
level and {a(cr, "target", "liftToMass")} at {altT} m, short by
{num(sub(rec.mass, rec.lift_sl), 1)} t and {num(sub(rec.mass, rec.lift_t), 1)} t. The
best defensible world — the frame-practice knockdown and the chord ceiling together —
weighs {fmt(cb["mass"])} t: {a(cb, "seaLevel", "liftToMass")} and
{a(cb, "target", "liftToMass")}, short by {num(sub(best.mass, best.lift_sl), 1)} t and
{num(sub(best.mass, best.lift_t), 1)} t. That best world misses by {num(miss_sl, 1)} % of
its lift ratio at sea level and by {num(miss_t, 1)} % at {altT} m: "nearly floats" is a
sea-level statement.

**Structure per cubic metre enclosed.** {num(rec.per_m3, 3)} kg/m³ on the record basis
and {num(best.per_m3, 3)} kg/m³ in the best world, against air at
{num(F.rho_sl, 4)} kg/m³ (sea level) and {num(F.rho_t, 4)} kg/m³ ({altT} m). Per square
metre of hull: {num(rec.areal, 2)} and {num(best.areal, 2)} kg/m².

**Where the mass is** (tonnes; the model's own line names):

{table(["Line", "Record", "Best defensible world"],
       lines + [["**total**", f"**{num(rec.mass, 1)}**", f"**{num(best.mass, 1)}**"]],
       "lrr")}

**What the model's own checks say about the record.** The general-instability margin is
{num(gm_h, 2)} at γ {num(F.gi_harsh, 2)} — the structure is sized to it. The same
structure reads {num(gm_f, 2)} at γ {num(F.gi_frame, 2)} and {num(gm_r, 2)} at γ
{num(F.k_shell, 2)}, which is what the stability-reserve line buys back. Standing
unpressurised during erection, the hull does not pass the model's wind check on its
film clamps (margin {num(wind, 2)}); the model reports that and leaves erection as a
separate bill.

**What would move it.** {MOVES_SHIP}
"""
    return design, md


def d_tool_default(F, K):
    SS = F.SS
    src = f"{SCOPING} --json"
    alt0, altT = num(F.alt_sl, 0), num(F.alt_t, 0)
    depth = qp(SS, "chosenConfig/depth", src)
    differs = not agree(depth, F.depth, 6)
    cases, rows, by = [], [], {}
    moves = ("Whatever moves the record, and one thing more: this row exists only because "
             "the tool's sweep and the model's record disagree about the wall depth. "
             "Reconciling them removes one of the two hulls.")
    saved = F.vc.SHIP0["depthM"]
    same = True
    try:
        F.vc.SHIP0["depthM"] = float(depth)
        for block, gi in (("results", F.gi_harsh), ("resultsFramePractice", F.gi_frame)):
            for name, r in SS[block].items():
                sig = next(kv for kv in F.sigmas if kv[0] == r["sigmaKey"])
                sf = Q(r["sf"], src)
                mass, l_sl, l_t = (Q(r[k], src) for k in ("totalT", "liftSLT", "lift2500T"))
                m = ship(F, sig[0], sf, None, gi)
                same = same and m is not None and agree(m.mass, mass, 1) \
                    and agree(m.ratio_sl, Q(r["ratioSL"], src), 3) \
                    and agree(m.ratio_t, Q(r["ratio2500"], src), 3)
                at = {"seaLevel": at_block(F.alt_sl, F.rho_sl, mass, l_sl, 1),
                      "target": at_block(F.alt_t, F.rho_t, mass, l_t, 1)}
                harsh = float(gi) == float(F.gi_harsh)
                why = ["it is the scoping tool's default hull, not the gated record"]
                if not harsh:
                    why.append("it stands on the frame-practice knockdown, which no test "
                               "supports and the model marks [TO VERIFY]")
                cid = (f"hull-{bare(F.dia, 0)}m/tool-default-wall-{bare(depth, 1)}m/"
                       f"gamma-{bare(gi, 2)}/chord-{bare(sig[1], 0)}/sf-{bare(sf, 1)}")
                c = make_case(
                    F, cid,
                    f"{num(F.dia, 0)} m hull with a {num(depth, 1)} m wall (the scoping "
                    f"tool's default run), {world_words(F, gi)} stability basis "
                    f"(γ {num(gi, 2)}), chords at {num(sig[1], 0)} MPa, SF {num(sf, 1)}",
                    mass, 1, "t", at, sf,
                    DECLARED if agree(sf, F.sf_decl, 6) else BESIDE,
                    ship_kds(F, K, gi), [chord_input(F, *sig)],
                    "the scoping tool's sweep pick, off the record", "to-verify",
                    f"`{SCOPING}`: `ship_ledger()` at the configuration `main()` re-derives "
                    "from its own sweep; written to `research/analysis/ship-scoping.json`",
                    moves, cap("; ".join(why)) + ".",
                    extras={"wallDepthM": N(depth, 2), "toolKey": quote(S(name, src)),
                            "arealKgPerSqM": N(Q(r["arealKgM2"], src), 2)})
                F.pressure_inputs.append((c, mass, l_sl))
                cases.append(c)
                by[(harsh, str(sig[0]), agree(sf, F.sf_decl, 6))] = c
                rows.append([num(gi, 2), num(sig[1], 0), num(sf, 1), fmt(c["mass"]),
                             a(c, "seaLevel", "liftToMass"), a(c, "seaLevel", "margin", True),
                             a(c, "target", "liftToMass"), a(c, "target", "margin", True),
                             ev(c["evidence"])])
    finally:
        F.vc.SHIP0["depthM"] = saved
    check(F, "the model, given the scoping tool's wall depth in memory only, reproduces "
             "every row of the tool's default output (two implementations, one answer)",
          same)
    F.c_tool = by[(True, str(F.sig_mid[0]), True)]
    F.c_tool_best = by[(False, str(F.sig_hi[0]), True)]
    F.tool_depth, F.tool_differs = depth, differs
    ct, cb = F.c_tool, F.c_tool_best
    design = {
        "id": f"{NO}ship0{NC}-tool-default",
        "name": f"The same name, a different hull: the scoping tool's default run",
        "object": (f"The same {num(F.dia, 0)} m capsule with its wall {num(depth, 1)} m "
                   f"deep instead of {num(F.depth, 1)} m."),
        "sameHullAsTheRecord": not differs,
        "cases": cases,
    }
    if differs:
        F.findings.append({
            "id": "two-hulls-one-name",
            "finding": (
                f"Two different hulls are both called {NO}ship 0{NC}. The gated model's "
                f"record has a wall {num(F.depth, 1)} m deep ({fmt(F.c_rec['mass'])} t, "
                f"lift ÷ mass {a(F.c_rec, 'seaLevel', 'liftToMass')} at sea level). "
                f"`{SCOPING}` run with no arguments re-derives its configuration from its "
                f"own sweep, picks a wall {num(depth, 1)} m deep ({fmt(ct['mass'])} t, "
                f"{a(ct, 'seaLevel', 'liftToMass')}) and writes that to "
                "`research/analysis/ship-scoping.json`. The tool's guard checks only the "
                "separately committed plan it uses for its band study, so it cannot see "
                "that its own sweep has moved off it.")})
    md = f"""## The same name, a different hull: what `{SCOPING}` prints by default

**The object.** {design["object"]} Run with no arguments, the scoping tool re-derives its
configuration from its own sweep and takes the lightest ruled row; today that row has
the deeper wall. It writes the result to `research/analysis/ship-scoping.json`, a
committed file that no page reads; the full check holds it to a fresh run through
analysisfresh. Its `--band` study uses a separately committed plan that matches the
record above, and guards only that plan.

**This is where two much-quoted figures come from.** On the harsh basis this hull reads
{a(ct, "seaLevel", "liftToMass")} at sea level — and {a(ct, "target", "liftToMass")} at
{altT} m. In the best defensible world it reads {a(cb, "seaLevel", "liftToMass")} at sea
level — and {a(cb, "target", "liftToMass")} at {altT} m. Each pair is one hull. The
second pair needs both unverified inputs at once: the frame-practice knockdown
(γ {num(F.gi_frame, 2)}, assumed) and a chord allowable of {num(F.sig_hi[1], 0)} MPa — a
carbon-laminate compressive ceiling from a datasheet, not an alloy and not a test.

**Lift, safety factor, knockdowns.** As for the record: same envelope, same lift, same
factors.
**Code path.** `{SCOPING}`: `{NO}ship_ledger(){NC}`, the tool's own implementation, at the
configuration `main()` picks.
**Evidence.** *{ev("to-verify")}* — an output for a wall the record does not
have. The deeper wall helps the harsh basis and hurts the best world, which is why
neither hull dominates the other.

{table(["Knockdown γ", "Chord allowable (MPa)", "SF", "Mass (t)",
        f"Lift ÷ mass at {alt0} m", f"Margin at {alt0} m (t)",
        f"Lift ÷ mass at {altT} m", f"Margin at {altT} m (t)", "Evidence"],
       rows, "rrrrrrrrl")}

**What would move it.** {moves}
"""
    return design, md


# Remaining sections share a renderer; the JSON retains the complete basis of every row.
def section(F, ident, name, obj, cases, note="", extra=None):
    d = dict(id=ident, name=name, object=obj, cases=cases)
    if extra:
        d.update(extra)
    rows = [[c['label'], fmt(c['mass']) + ' ' + c['massUnit'],
             '—' if c['safetyFactor']['value'] is None else fmt(c['safetyFactor']['value']),
             a(c, 'seaLevel', 'liftToMass'), a(c, 'seaLevel', 'margin', True),
             a(c, 'target', 'liftToMass'), a(c, 'target', 'margin', True), ev(c['evidence'])]
            for c in cases]
    md = f"## {name}\n\n{obj}\n\n{note}\n\n" + table(
        ['Object and basis', 'Mass (or density)', 'SF', 'Lift ÷ mass at sea level',
         'Margin at sea level (mass unit)', f'Lift ÷ mass at {num(F.alt_t)} m',
         f'Margin at {num(F.alt_t)} m (mass unit)', 'Evidence'], rows)
    md += '\n\nRepository structural-model rows are sized for full vacuum against sea-level pressure '
    md += f'({num(Q(F.vc.P_ATM, MODEL + ": P_ATM"))} Pa); altitude changes lift only. '
    md += 'Literature inputs and fleet allowances are not resized structures.\n'
    for code in dict.fromkeys(c['codePath'] for c in cases):
        md += f'\nCode: {code}.\n'
    for move in dict.fromkeys(c['whatWouldMoveIt'] for c in cases):
        md += f'\nWhat would move it: {move}\n'
    return d, md


def d_moves(F, K):
    cases, ok = [], True
    for (gamma, sigma), world in F.band.moves.items():
        gi = Q(gamma, SCOPING + ' --band')
        sig = next(s for s in F.sigmas if float(s[1]) == sigma)
        for name, ch, mem in VARIANTS:
            r = world['rows'][name]
            for sf in (ONE, F.sf_decl):
                c, o = ship_case(F, K, F.dia, gi, sig, sf, ch, mem)
                if c is None:
                    die('a design-move row could not be computed')
                cases.append(c)
                ok &= agree(o.mass, r['crushT'] if sf == ONE else r['massT'], 1)
                if sf == ONE:
                    ok &= agree(sub(o.lift_sl, o.mass), r['bandT'], 1)
                else:
                    ok &= agree(o.ratio_sl, r['ratio'], 3)
    check(F, 'every design-move mass and sea-level band reproduces the independent scoping tool', ok)
    return section(F, 'moves', 'Design moves — bounds only',
                   'The record envelope with each credited move and each stability/coupon world.', cases,
                   'The chordal net is priced at diametral-cord rates on undrawn geometry. '
                   'The in-surface shear system receives stiffness credit but its own mass is unpriced. '
                   'The crush floor carries no safety margin; it is not a proposed operating point.')


def d_sizes(F, K):
    cases, ok, bands = [], True, []
    for name, data, moves in [('as drawn', F.band.band, False), ('both moves', F.band.goal, True)]:
        for (gamma, sigma), world in data.items():
            gi = Q(gamma, SCOPING + ' --band')
            sig = next(s for s in F.sigmas if float(s[1]) == sigma)
            for r in world['rows']:
                c, o = ship_case(F, K, r['diaM'], gi, sig, ONE, moves, moves)
                if c is None:
                    die('a band row could not be computed')
                cases.append(c)
                ok &= agree(o.mass, r['crushT'], 1) and agree(o.lift_sl, r['liftT'], 1)
                ok &= agree(sub(o.lift_sl, o.mass), r['bandT'], 1)
                bands.append(dict(case=c['id'], seaLevelT=N(sub(o.lift_sl, o.mass), 1),
                                  targetT=N(sub(o.lift_t, o.mass), 1),
                                  toolSolverGuard=r['guard']))
    check(F, 'all hull-size crush masses and sea-level bands reproduce the scoping tool, with and without moves', ok)
    # The model's published size curve includes sizes absent from the band study.
    for world, gamma, sig in [('floatWindow', F.gi_harsh, F.sig_mid),
                              ('floatWindowFrame', F.gi_frame, F.sig_hi)]:
        for r in F.P['ship0'][world]['curve']:
            dia = Q(r['diaM'], MODEL + ': ship0_summary()')
            c, o = ship_case(F, K, dia, gamma, sig, F.sf_decl)
            if o is None:
                die('a published size-curve hull could not be computed')
            cases.append(c)
            ok &= agree(o.ratio_sl, Q(r['ratioSL'], MODEL + ': ship0_summary()'), 3)
    for r in F.band.goal[(float(F.gi_frame), float(F.sig_hi[1]))]['rows']:
        c, o = ship_case(F, K, r['diaM'], F.gi_frame, F.sig_hi, F.sf_decl, True, True)
        if c is None:
            die('a declared-factor goal row could not be computed')
        cases.append(c)
    check(F, 'the published size curves reproduce by calling the model', ok)
    check(F, 'every sampled crush-floor band is closed at the working altitude, including both favourable credits',
          all(b['targetT'].v < 0 for b in bands))
    curve = F.P['ship0']['floatWindow']['curve']
    falling = all(a['ratioSL'] > b['ratioSL'] for a, b in zip(curve, curve[1:]))
    check(F, 'the record-basis ratio decreases at each size in the published size curve', falling)
    F.findings.append(dict(id='size-and-altitude', finding=
        'On the record basis the ratio falls at each sampled diameter in the published curve. '
        'The best-world curve is not monotone, but its largest hull also has a lower ratio '
        'than its smallest. At the working altitude every sampled band is closed, even '
        'at the crush floor with both favourable credits. This is a finite sweep, not '
        'a proof about all possible diameters or architectures.'))
    F.size_cases = cases
    return section(F, 'sizes', 'Size, safety margin and the float band',
                   'Each hull is scaled from the record by the model’s rule; none is a new drawn design.',
                   cases, 'A band is lift minus the crush-floor mass. A positive sea-level band '
                   'does not establish a floating design at the working altitude.', dict(bands=bands))


def d_mission0(F, K):
    r = F.band.goal_result[(float(F.gi_frame), float(F.sig_hi[1]))]
    if r['closed']:
        die('the scoping tool no longer publishes the goal hull used by the mission page')
    dia = r['diaM']; cases = []
    for gi, sig, sf, moves in [(F.gi_harsh, F.sig_mid, F.sf_decl, False),
                               (F.gi_frame, F.sig_hi, F.sf_decl, False),
                               (F.gi_frame, F.sig_hi, F.sf_decl, True),
                               (F.gi_frame, F.sig_hi, ONE, True)]:
        c, o = ship_case(F, K, dia, gi, sig, sf, moves, moves)
        if c is None:
            die('the mission hull could not be computed')
        cases.append(c)
    # The tool prints a mass target and a rounded emergent factor, not a re-solved design.
    mass = r['designT']; ref = o
    at = {'seaLevel': at_block(F.alt_sl, F.rho_sl, mass, ref.lift_sl, 1),
          'target': at_block(F.alt_t, F.rho_t, mass, ref.lift_t, 1)}
    cases.append(make_case(F, 'mission-mid-band', 'Mid-band mass target from the scoping study',
        mass, 1, 't', at, r['emergentSF'], 'rounded emergent factor, below the declared factor',
        ship_kds(F, K, F.gi_frame), [chord_input(F, *F.sig_hi)], BOUND, 'to-verify',
        f'`{SCOPING}`: `band_study()`, goal mid-band target', MOVES_SHIP,
        'Both design moves are bounds, the shear system mass is unpriced, the emergent '
        'factor is below the declared factor, and the sea-level reserve disappears at altitude.'))
    F.pressure_inputs.append((cases[-1], mass, ref.lift_sl))
    F.mission_cases = cases
    return section(F, 'mission', '«Mission 0» — the scoping goal hull',
        f'The {num(dia)} m hull that the scoping tool picks for its widest sea-level goal band.', cases,
        'No propulsion, payload or operational equipment is added here. The page’s mission '
        'scenario is not a certified vehicle or a replay of a fire with a different outcome.')


def d_bench(F, K):
    sb = F.P['stockBuild']; src = MODEL + ': stock_build()'
    span = Q(F.vc.DEMO_PITCH_PINNED_M * 2, MODEL + ': DEMO_PITCH_PINNED_M (doubled)')
    vol = Q(float(span) ** 3 / 2, MODEL + ': stock_build(), span cubed / two')
    mass = qp(sb, 'totalKg', src)
    # stock_build uses the literal sea-level density, whose rounding is immaterial here.
    stock_ast = ast.parse(inspect.getsource(F.vc.stock_build))
    displaced = next(n.value for n in ast.walk(stock_ast) if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 'displaced' for t in n.targets))
    if not isinstance(displaced, ast.BinOp) or not isinstance(displaced.left, ast.Constant):
        die('stock_build displaced-air expression changed; inspect its density basis')
    rho_sb = Q(displaced.left.value, MODEL + ': stock_build(), displaced-air density literal')
    cases = []
    for name, v in [('nominal', vol), ('loaded-shape', mul(vol, div(
            qp(F.skin, 'numbers/dispLoadedM3', SKIN), qp(F.skin, 'numbers/dispNominalM3', SKIN))))]:
        at = {'seaLevel': at_block(F.alt_sl, rho_sb, mass, mul(rho_sb, v), 3, 1),
              'target': at_block(F.alt_t, F.rho_t, mass, mul(F.rho_t, v), 3, 1)}
        c = make_case(F, 'bench-' + name, 'Article A, ' + name + ' displaced volume', mass, 3,
            'kg', at, F.sf_lat, BESIDE, [], [],
            AS_DRAWN, 'to-verify', f'`{MODEL}`: `stock_build()`, `kelvin_faces()`; `{SKIN}`',
            'Weighed tube, joints and skin; boundary-load tests; the loaded volume and '
            'missing adhesive, seams, barrier and hardware. Computed mesh volume is not a physical weighing.',
            extras={'enclosedCubicM': N(v, 6), 'displacedSeaLevelG': N(mul(mul(rho_sb, v), KILO), 1),
                    'displacedTargetG': N(mul(mul(F.rho_t, v), KILO), 1),
                    'structureKgPerCubicMEnclosed': N(div(mass, v), 2),
                    'jointShareOfTubePct': N(F.joint_share, 1)})
        cases.append(c)
    check(F, 'the bench-cell geometry and mass reproduce enclosed litres, displaced air, density and mass-to-lift',
          agree(mul(vol, KILO), qp(sb, 'enclosedL', src), 0)
          and agree(mul(rho_sb, vol), qp(sb, 'displacedAirKg', src), 3)
          and agree(div(mass, vol), qp(sb, 'kgPerM3', src), 2)
          and agree(div(mass, mul(rho_sb, vol)), qp(sb, 'massOverDisplaced', src), 1))
    F.bench_cases = cases
    return section(F, 'bench', 'The bench cell — article A',
        f'A Kelvin article spanning {num(span, 3)} m. Its nominal displaced air is '
        f'{fmt(cases[0]["extras"]["displacedSeaLevelG"])} g at sea level and '
        f'{fmt(cases[0]["extras"]["displacedTargetG"])} g at {num(F.alt_t)} m.', cases,
        f'The drawn joints are {num(qp(sb,"printed/nodesKg",src),3)} kg on '
        f'{num(qp(sb,"pipe/kg",src),3)} kg of tube: {num(F.joint_share,1)} %. '
        f'The committed assembly record passes {num(qp(F.assembly,"verdict/proofsPassed",ASSEMBLY))} '
        f'of {num(qp(F.assembly,"verdict/proofsRun",ASSEMBLY))} proofs; this generator reads that record, '
        'it does not rerun the assembly prover. The payload’s nodesMeasured flag means mesh integration, not a weighed article. '
        'This stock-build path reports pinned Euler, bending and material checks; it does not '
        'apply the closed-form local-wall knockdown or establish the assembled boundary conditions.')


def density_case(F, K, cid, label, density, code, evidence='to-verify', extra=None,
                 sf=None, kds=None, status=CLOSED_FORM):
    return make_case(F, cid, label, density, 4, 'kg/m³', density_at(F, density),
        sf, 'not established for a fabricated object' if sf is None else BESIDE,
        refs(K, 'classical', 'local-wall', 'ortho', 'node-fraction') if kds is None else kds,
        [], status, evidence, code,
        'Material properties, end fixity, joint mass, film convention, and a drawn and tested structure.',
        'This is a formula or an assumed allowance, not a fabricated floating design. '
        'The hierarchy has no drawn higher-level strut, and film and joint assumptions remain open.', extra)


def d_closed(F, K):
    src = MODEL + ' --json'; cases = []
    bu = F.P['designPoint']['buildUp']
    vals = [('closed-total', 'Closed form, pressure-rated film on every interior face', qp(bu,'total',src)),
            ('closed-bare', 'Closed form, lattice and node allowance only',
             add(qp(bu,'lattice',src), qp(bu,'nodes',src))),
            ('closed-envelope', 'Closed form, outer-envelope film only',
             qp(F.P,'designPoint/filmIsAChoiceAndTheModelPickedOneIncoherently/totalIfOuterEnvelopeOnly',src))]
    for cid, label, value in vals:
        cases.append(density_case(F,K,cid,label,value,f'`{MODEL}`: `total_shell()`, JSON `designPoint`', sf=F.sf_lat))
    for key, r in F.P['materials'].items():
        cases.append(density_case(F,K,'material-' + quote(S(key,src)), quote(S(r['name'],src)),
            Q(r['totalKgPerM3'],src), f'`{MODEL}`: `total_shell()`, JSON `materials`', sf=F.sf_lat,
            kds=refs(K, 'classical', 'local-wall', 'node-fraction', *(['ortho'] if r['orthotropic'] else [])),
            extra={'publishedTargetLiftToMass': N(Q(r['marginX'],src),3), 'materialSource': S(r['source'],src)}))
    for key, ladder in F.P['hierarchy']['ladders'].items():
        for r in ladder.values():
            cases.append(density_case(F,K,'hierarchy-' + quote(S(key,src)) + '-' + bare(Q(r['levels'],src),0),
                quote(S(key,src)) + ', hierarchy level ' + num(Q(r['levels'],src)), Q(r['totalKgPerM3'],src),
                f'`{MODEL}`: `hierarchy_ladder()`, JSON `hierarchy/ladders`', sf=F.sf_lat,
                kds=refs(K, 'classical', 'local-wall', 'node-fraction',
                         *(['ortho'] if F.vc.MATERIALS[key]['orthotropic'] else [])),
                extra={'filmConvention': 'outer envelope only', 'exponent':N(Q(r['exponent'],src),4)}))
    for key, r in F.P['weightlessArticle']['rows'].items():
        cases.append(density_case(F,K,'weightless-' + quote(S(key,src)),
            quote(S(r['label'],src)) + ', finite article at unit subdivision', Q(r['densityAtN1'],src),
            f'`{MODEL}`: `weightless_article()`, JSON `weightlessArticle`', sf=F.sf_lat))
    F.closed_cases = cases
    return section(F,'closed','Closed-form cells and hierarchy',
        'These are sizing laws, not bills of parts. Interior pressure-rated film and outer-envelope-only '
        'film are different mass conventions; the bare-lattice row omits both.', cases,
        'A material’s target-altitude margin may share digits with an unrelated ship’s sea-level ratio. '
        'Names and basis, not numeric coincidence, identify a result.')


def d_r1(F, K):
    cases=[]
    for r in F.sub.rows:
        cid='subdivision-' + bare(r['spanM'],1) + '-n-' + bare(r['n'],0)
        c=density_case(F,K,cid, f'Span {num(r["spanM"],1)} m, subdivision {num(r["n"])}',
            r['totalKgM3'], f'`{SUBDIV}`: `main()`, PUBLICATION SUMMARY', sf=F.sf_lat, status=STUDY,
            kds=refs(K, 'classical', 'local-wall', 'ortho'),
            extra={'toolPrintedMassToTargetLift':N(r['overWall'],2),
                   'tubeKgPerCubicM':N(r['tubeKgM3'],2), 'jointKgPerCubicM':N(r['jointKgM3'],2),
                   'filmKgPerCubicM':N(r['filmKgM3'],2), 'filmMarginAtFactor':N(r['filmMarginAtSF'],2),
                   'governor':r['governor']})
        cases.append(c)
    return section(F,'subdivision','«R1» — subdivision with film bending',
        'Rounded stdout values are retained. Dividing rounded density by air density can differ '
        'in the last decimal from the tool’s multiple; the JSON records both.', cases,
        'Not counted: ' + quote(F.sub.notCounted) + '. Uncertainties: ' + quote(F.sub.uncertain) + '.')


def d_one_metre(F, K):
    cases=[]
    for i,r in enumerate(F.scale.blocks):
        c=density_case(F,K,'scale-' + bare(Q(i,SCALE + ': stdout block index'),0),
            f'Span {num(r["spanM"],3)} m, {quote(r["label"])}',r['kgPerM3'],
            f'`{SCALE}`: `main()`, SPAN blocks', sf=F.sf_lat, status=STUDY,
            kds=[],
            extra={'totalKg':N(r['totalKg'],2),'tubeKg':N(r['tubeKg'],2),
                   'jointsKg':N(r['jointsKg'],2),'filmG':N(r['filmG'],0),
                   'mainTube':r['mainTube'],'rimTube':r['rimTube'],
                   'toolPrintedMassToTargetLift':N(r['overWall'],2)})
        cases.append(c)
    return section(F,'scale','One-metre study — catalogue sweep',
        'Margins are held at the bench article’s margins, or improved as labelled; joints are '
        'estimated by an outside-diameter cube law. These catalogue dimensions are not procurement evidence. '
        'This study checks Euler, material and film-bending demands; it does not perform the '
        'closed-form local-wall buckling check.', cases)


def d_fleet(F, K):
    cases=[]; stale=[]; old=read_json('research/analysis/mass-budget.json')
    for key,r in F.fig['classes'].items():
        src=FIGURES + ': classes/' + key
        spec=r['spec']; vol=Q(spec['dispM3'],src); payload=Q(spec['payloadT'],src)
        for label,mass in [('empty structure allowance',payload),('loaded structure plus payload',add(payload,payload))]:
            at={k:at_block(alt,rho,mass,div(mul(vol,rho),KILO),1) for k,alt,rho in
                [('seaLevel',F.alt_sl,F.fig_rho_sl),('target',F.alt_t,F.fig_rho_t),('ground',F.alt_g,F.fig_rho_g)]}
            c=make_case(F,'fleet-' + quote(S(key,src)) + '-' + label.split()[0],quote(S(key,src)) + ', ' + label,
                mass,1,'t',at,None,'not specified by simulator',[],[], 'assumed fleet, not a structural design',
                'assumed','`sim/physics.js`: `ledger()`; `research/figures.json`',
                'An actual structural and equipment mass budget; the simulator assumes structure equals payload.',
                'The simulator assumes the dry structure equals the payload. It has not sized a hull.',
                {'structureAllowanceKgPerCubicM':N(div(mul(payload,KILO),vol),4)})
            cases.append(c)
        fresh=F.MB['classes'][key]
        for field in ['hullAreaM2','requiredKgPerM2']:
            aold=old['classes'][key][field]; anew=fresh[field]
            if aold != anew:
                stale.append(dict(design=S(key,src),field=S(field,BUDGET),old=N(Q(aold,'committed mass-budget.json'),3),
                                  fresh=N(Q(anew,BUDGET + ' fresh run'),3)))
        for world, budget in fresh['cases'].items():
            mass=add(Q(budget['totalT'],BUDGET),payload)
            at={k:at_block(alt,rho,mass,div(mul(vol,rho),KILO),1) for k,alt,rho in
                [('seaLevel',F.alt_sl,F.fig_rho_sl),('target',F.alt_t,F.fig_rho_t)]}
            cases.append(make_case(F,'budget-' + quote(S(key,src)) + '-' + world,
                quote(S(key,src)) + ', equipment budget ' + world + ', loaded', mass,1,'t',at,None,
                'not a common structural safety factor',[],[], 'assumed equipment budget','assumed',
                f'`{BUDGET}`: `budget()`; freshly run JSON `classes/cases`',
                'Measured component masses and structural validation. The budget’s case names are not evidence classes.',
                'The equipment budget contains assumed and literature inputs; it does not define a tested hull.'))
    F.stale=stale
    note='The budget’s case named “demonstrated” cites a numerical shell study; it is not a measured vehicle.'
    # The finding and its table are written only while the committed budget lags a fresh run.
    if stale:
        F.findings.append(dict(id='stale-budget',finding='The committed mass budget differs from a fresh run. '
            'The ledger uses the fresh run and leaves the committed budget for its owner to update with its prose.', changes=stale))
        note+='\n\n' + table(['Class','Committed field','Old','Fresh'],
            [[quote(r['design']),quote(r['field']),fmt(r['old']),fmt(r['fresh'])] for r in stale])
    return section(F,'fleet','Fleet allowances and equipment budgets',
        'The simulator assumes dry structure equals payload. A fleet buoyancy surplus is conditional on '
        'that allowance; it is not evidence of a buildable vacuum hull.',cases,note)


def d_literature(F,K):
    cases=[]
    for world,r in F.MB['evidence']['shell_kg_per_m3'].items():
        c=density_case(F,K,'literature-' + world,'Shell input used in the budget’s ' + world + ' case',
            Q(r['value'],BUDGET + ': evidence/shell_kg_per_m3'),f'`{BUDGET}`: `EVIDENCE`',
            evidence='assumed' if world=='credible' else 'literature',kds=[],
            extra={'source':S(r['source'],BUDGET),
                   'basisCaveat':'Source density only; air-density comparisons are arithmetic on that density. '
                   'Original altitude, safety factor and knockdown are not established by the budget citation.'})
        c['sizingPressure']={'valuePa':None,'basis':'Not established by this secondary citation; not resized by the ledger.'}
        cases.append(c)
    return section(F,'literature','Literature densities — not the drawn hulls',
        'These are the budget tool’s cited inputs. Their original load cases are not imported as '
        'validated ship cases. The altitude columns compare density only.',cases,
        '\n\n'.join(quote(c['extras']['source']) for c in cases))


def d_v2(F,K):
    sc=load_module(SCOPING,'scoping_for_ledger');sc.configure();out=sc.v2_closure_reproduction();cases=[]
    for key,r in out.items():
        sf=Q(sc.SF_DECL if key=='sf12' else sc.SF_15,SCOPING + ': v2_closure_reproduction()')
        mass=Q(r['totalT'],SCOPING);lift=Q(r['liftT'],SCOPING)
        at={'seaLevel':at_block(F.alt_sl,F.rho_sl,mass,lift,1),
            'target':at_block(F.alt_t,F.rho_t,mass,mul(lift,div(F.rho_t,F.rho_sl)),1)}
        cases.append(make_case(F,'vintage-' + quote(S(key,SCOPING)),'Superseded closure ' + quote(S(key,SCOPING)),
            mass,1,'t',at,sf,'historical declared factor',[],[], 'superseded model','to-verify',
            f'`{SCOPING}`: `«v2_closure_reproduction()»`',
            'This closure was replaced by the drawn wall and skeleton model; see history.',
            'The old band-and-chord closure is superseded and omits the present stability and load-path corrections.'))
    return section(F,'vintage','Superseded closure, reproduced',
        'Historical arithmetic retained by the scoping tool, with its old geometry and no sag debit. '
        'These ratios never establish the current hull.',cases)


def d_pressure(F,K):
    p=Q(F.vc.P_ATM,MODEL + ': P_ATM')
    pt=Q(F.vc.isa_pressure(float(F.alt_t)),MODEL + ': isa_pressure()')
    rows=[]
    for c in [F.c_rec,F.c_best,F.c_tool,F.c_tool_best,*F.mission_cases]:
        # Same temperature inside and outside at sea level; density difference is
        # proportional to pressure difference. Use the sag-debited model lift.
        _,m,lift=next(r for r in F.pressure_inputs if r[0]['id']==c['id'])
        dp=mul(p,div(m,lift))
        rows.append(dict(case=c['id'],label=c['label'],evidence='assumed',quantity='pressure difference',unit='Pa',
            neutralSeaLevelPa=N(dp,0),fullVacuumAtTargetPa=N(pt,0),
            governing='sea-level neutral requirement' if dp>pt else 'working-altitude full vacuum',
            feasibleSeaLevelNeutral=bool(dp<=p),
            calculation='deltaP_neutral = sea-level pressure × model mass / sea-level model lift; '
                'equal internal and external air temperature assumed; no payload added',
            basis='arithmetic on model outputs, no structure resized',
            codePath=f'`{MODEL}`: `isa_pressure()`, `«ship0()»`; `tools/float_ledger.py`: `d_pressure()`'))
    obj='Not computed: a hull partly evacuated low down and fully evacuated only at the working altitude.'
    note=(f'Each present structural row is sized for full vacuum against {num(p)} Pa at sea level. '
          'A staged-pressure hull would require an internal-pressure and temperature schedule, '
          'gas and pump/valve masses, load cases including transients and faults, and structural '
          'resizing and stability checks at those loads. None is computed here. The sea-level '
          'neutral differences below retain the current mass and sag-debited volume. A difference '
          'above ambient pressure cannot be achieved by evacuating air. “Governing” compares these '
          'two arithmetic requirements only; it does not select a structural design.\n\n'
          'Prior work: `research/analysis/vacuum-cell.py`, `main()` → `nullResults.partialVacuum` '
          'and `nullResults.altitude` studies a closed-form lattice, including local-pressure sizing. '
          '`docs/FLOAT.md`, “Full vacuum, not partial”, now limits that conclusion to the closed-form route. '
          '`research/analysis/air-ballast.md` retracts admitting air as a control mechanism for '
          'permanently sealed cells; `docs/PHYSICS.md`, “Ballast”, carries that architectural limitation. '
          'Those records do not compute this staged-pressure ship.\n\n'
          '**Evidence: assumed. Arithmetic on model outputs, no structure resized. No conclusion '
          'about whether a resized hull would float.**')
    md='## Pressure schedule — not computed\n\n'+obj+'\n\n'+note+'\n\n'+table(
        ['Hull and current basis','Neutral difference at sea level (Pa)',
         f'Full-vacuum difference at {num(F.alt_t)} m (Pa)','Larger requirement','Neutral achievable at sea level?'],
        [[r['label'],fmt(r['neutralSeaLevelPa']),fmt(r['fullVacuumAtTargetPa']),r['governing'],
          'yes, arithmetically' if r['feasibleSeaLevelNeutral'] else 'no'] for r in rows])
    return dict(id='pressure-question',name='Pressure schedule — not computed',object=obj,
                evidence='assumed',cases=[],rows=rows,note=note),md


# Identities survive hash rewriting. Expected excerpts are checked against commit files.
HISTORY_SPECS = [{'id': 'levels',
  'identity': {'authorDate': '2026-08-12T13:18:36-07:00',
               'subject': 'The seven levels: the ship story gets its shell, and level 1 gets its catalog'},
  'path': 'cell/levels.html',
  'pointers': None,
  'contains': '<h1>No cell floats.',
  'expected': '<h1>No cell floats.<br>The ship does.</h1>',
  'replacedBy': {'authorDate': '2026-08-13T04:25:01-07:00',
                 'subject': "The second panel's verdict: no world floats as drawn — and the model now says "
                            'exactly why and what would change it'},
  'why': 'The drawn shell and then the general-instability corrections replaced the closure claim.'},
 {'id': 'ship-first',
  'identity': {'authorDate': '2026-08-13T02:18:31-07:00',
               'subject': "SHIP-2's bill: the wall's checks, the honest ledger, and the verdict — ship 0 "
                          'floats at the declared SF on the mid coupons'},
  'path': 'research/analysis/ship-scoping.json',
  'pointers': ['results/s1050_sf1.2/totalT', 'results/s1050_sf1.2/ratioSL', 'results/s1050_sf1.2/residualSLT'],
  'contains': None,
  'expected': 'results/s1050_sf1.2/totalT = 219.10303646359674; results/s1050_sf1.2/ratioSL = '
              '1.02906001313099; results/s1050_sf1.2/residualSLT = 6.36713711667187',
  'replacedBy': {'authorDate': '2026-08-13T02:55:32-07:00',
                 'subject': 'The refuters were right: corrected shell mechanics, the licensed spokes, and the '
                            'honest verdict — ship 0 as drawn does not float'},
  'why': 'Corrected shell mechanics, spoke support and stability sizing.'},
 {'id': 'ship-round-one',
  'identity': {'authorDate': '2026-08-13T02:55:32-07:00',
               'subject': 'The refuters were right: corrected shell mechanics, the licensed spokes, and the '
                          'honest verdict — ship 0 as drawn does not float'},
  'path': 'research/analysis/ship-scoping.json',
  'pointers': ['results/s1050_sf1.2/ratioSL',
               'resultsFramePractice/s1450_sf1.2/ratioSL',
               'resultsFramePractice/s1450_sf1.2/residualSLT'],
  'contains': None,
  'expected': 'results/s1050_sf1.2/ratioSL = 0.6979651514142527; resultsFramePractice/s1450_sf1.2/ratioSL = '
              '1.0586358151430362; resultsFramePractice/s1450_sf1.2/residualSLT = 12.452338003787105',
  'replacedBy': {'authorDate': '2026-08-13T04:25:01-07:00',
                 'subject': "The second panel's verdict: no world floats as drawn — and the model now says "
                            'exactly why and what would change it'},
  'why': 'Odd circumferential modes lose diametral-spoke credit; the wall lacks the credited in-surface shear '
         'system.'},
 {'id': 'ship-record',
  'identity': {'authorDate': '2026-08-13T04:25:01-07:00',
               'subject': "The second panel's verdict: no world floats as drawn — and the model now says "
                          'exactly why and what would change it'},
  'path': 'research/analysis/vacuum-cell.json',
  'pointers': ['ship0/mid/totalT', 'ship0/mid/ratioSL', 'ship0/mid/ratio2500'],
  'contains': None,
  'expected': 'ship0/mid/totalT = 403.1; ship0/mid/ratioSL = 0.558; ship0/mid/ratio2500 = 0.436',
  'replacedBy': None,
  'why': 'Current record: the ratios differ with altitude.'},
 {'id': 'tool-default',
  'identity': {'authorDate': '2026-08-13T04:25:01-07:00',
               'subject': "The second panel's verdict: no world floats as drawn — and the model now says "
                          'exactly why and what would change it'},
  'path': 'research/analysis/ship-scoping.json',
  'pointers': ['chosenConfig/depth', 'results/s1050_sf1.2/ratioSL', 'resultsFramePractice/s1450_sf1.2/ratioSL'],
  'contains': None,
  'expected': 'chosenConfig/depth = 4.0; results/s1050_sf1.2/ratioSL = 0.5870241138189819; '
              'resultsFramePractice/s1450_sf1.2/ratioSL = 0.9364235702149636',
  'replacedBy': None,
  'why': 'The default sweep chooses a different wall from the hull of record.'},
 {'id': 'closed-first',
  'identity': {'authorDate': '2026-08-11T12:54:02-07:00',
               'subject': 'The vacuum-cell physics, the research corpus, and the verification plan'},
  'path': 'research/analysis/vacuum-cell.json',
  'pointers': ['designPoint/buildUp/total', 'hierarchy/ladder/2/totalKgPerM3'],
  'contains': None,
  'expected': 'designPoint/buildUp/total = 1.4319; hierarchy/ladder/2/totalKgPerM3 = 0.4499',
  'replacedBy': {'authorDate': '2026-08-12T10:07:51-07:00',
                 'subject': 'The 0.605 lands: the physics is corrected, the built article is pinned, every '
                            'consequence is published'},
  'why': 'The classical cylinder-buckling coefficient was missing from closed-form routes.'},
 {'id': 'closed-corrected',
  'identity': {'authorDate': '2026-08-12T10:07:51-07:00',
               'subject': 'The 0.605 lands: the physics is corrected, the built article is pinned, every '
                          'consequence is published'},
  'path': 'research/analysis/vacuum-cell.json',
  'pointers': ['designPoint/buildUp/total', 'hierarchy/ladder/2/totalKgPerM3'],
  'contains': None,
  'expected': 'designPoint/buildUp/total = 1.6296; hierarchy/ladder/2/totalKgPerM3 = 0.5383',
  'replacedBy': None,
  'why': 'Corrected coefficient; these remain formulas, not drawn hierarchical struts.'},
 {'id': 'bench-first',
  'identity': {'authorDate': '2026-08-11T12:54:02-07:00',
               'subject': 'The vacuum-cell physics, the research corpus, and the verification plan'},
  'path': 'research/analysis/vacuum-cell.json',
  'pointers': ['stockBuild/totalKg'],
  'contains': None,
  'expected': 'stockBuild/totalKg = 2.883',
  'replacedBy': {'authorDate': '2026-08-11T20:16:28-07:00',
                 'subject': 'The frame sinks in earnest: every socket whole, every proof re-measured, the page '
                            'follows'},
  'why': 'Full sockets and land posts increased drawn joint volume.'},
 {'id': 'bench-frame',
  'identity': {'authorDate': '2026-08-11T20:16:28-07:00',
               'subject': 'The frame sinks in earnest: every socket whole, every proof re-measured, the page '
                          'follows'},
  'path': 'research/analysis/vacuum-cell.json',
  'pointers': ['stockBuild/totalKg', 'stockBuild/printed/nodesKg'],
  'contains': None,
  'expected': 'stockBuild/totalKg = 3.133; stockBuild/printed/nodesKg = 0.715',
  'replacedBy': {'authorDate': '2026-08-12T01:29:22-07:00',
                 'subject': "P14 closes: the bill is the saw table's, and 0.44 kg of phantom tube is gone"},
  'why': 'The saw-table cut lengths replaced centre-to-centre span billing.'},
 {'id': 'bench-saw',
  'identity': {'authorDate': '2026-08-12T01:29:22-07:00',
               'subject': "P14 closes: the bill is the saw table's, and 0.44 kg of phantom tube is gone"},
  'path': 'research/analysis/vacuum-cell.json',
  'pointers': ['stockBuild/totalKg', 'stockBuild/displacedAirKg'],
  'contains': None,
  'expected': 'stockBuild/totalKg = 2.691; stockBuild/displacedAirKg = 0.218',
  'replacedBy': None,
  'why': 'Current bench mass; displaced air here is the sea-level figure.'},
 {'id': 'subdivision-first',
  'identity': {'authorDate': '2026-08-11T17:07:52-07:00',
               'subject': 'Where the mass is, and the routes to a cell that floats'},
  'path': 'docs/FLOAT.md',
  'pointers': None,
  'contains': '| **R1** |',
  'expected': '| **R1** | subdivide the lattice so the film needs no separate frame | **~4.1× the wall** | '
              'priced, not designed |',
  'replacedBy': {'authorDate': '2026-08-12T01:02:09-07:00',
                 'subject': 'Land order 865: R1 answers for film bending, and does not survive it'},
  'why': 'Film bending was added to the axial-only subdivision sizing.'},
 {'id': 'subdivision-corrected',
  'identity': {'authorDate': '2026-08-12T01:02:09-07:00',
               'subject': 'Land order 865: R1 answers for film bending, and does not survive it'},
  'path': 'docs/FLOAT.md',
  'pointers': None,
  'contains': '| **R1** |',
  'expected': '| **R1** | subdivide the lattice so the film needs no separate frame | **11.24× the wall** | '
              'film bending priced; not designed |',
  'replacedBy': None,
  'why': 'Current bounded study; missing mass lines and invented catalogue remain.'},
 {'id': 'float-table',
  'identity': {'authorDate': '2026-08-11T17:07:52-07:00',
               'subject': 'Where the mass is, and the routes to a cell that floats'},
  'path': 'docs/FLOAT.md',
  'pointers': None,
  'contains': '| 0.71 m |',
  'expected': '| 0.71 m | 6.55 | 2.61 | 0.16 | 9.31 | 9.7× |',
  'replacedBy': None,
  'why': 'The published table is not reproduced by today’s scale or subdivision tools; retained as a disputed '
         'historical claim.'},
 {'id': 'scale-lever',
  'identity': {'authorDate': '2026-08-13T21:18:00-07:00',
               'subject': 'The engineering page: seven scales, live numbers, and the two walls said plainly'},
  'path': 'engineering/index.html',
  'pointers': None,
  'contains': 'scale is the lever',
  'expected': '<span class="fact">a ship must beat <b>1.0 kg/m³</b> of enclosed volume — scale is the '
              'lever</span>',
  'replacedBy': None,
  'why': 'Still published; the current record-basis size curve falls with hull diameter.'},
 {'id': 'budget-area',
  'identity': {'authorDate': '2026-08-11T12:54:02-07:00',
               'subject': 'The vacuum-cell physics, the research corpus, and the verification plan'},
  'path': 'research/analysis/mass-budget.json',
  'pointers': ['classes/P100/hullAreaM2', 'classes/P100/requiredKgPerM2'],
  'contains': None,
  'expected': 'classes/P100/hullAreaM2 = 22592; classes/P100/requiredKgPerM2 = 4.426',
  'replacedBy': {'authorDate': '2026-08-13T16:54:35-07:00',
                 'subject': 'The dashboard family becomes the capsule — and pays the honest drag bill'},
  'why': 'Fleet geometry changed to a capsule; the committed mass budget was not regenerated.'},
 {'id': 'fleet-sea-level',
  'identity': {'authorDate': '2026-08-09T00:41:01-07:00',
               'subject': 'import: verbatim copy of the deployed airships tree'},
  'path': 'index.html',
  'pointers': None,
  'contains': 'const liftT = cls.dispM3 * CFG.rhoSL / 1000',
  'expected': 'const liftT = cls.dispM3 * CFG.rhoSL / 1000;     // what the evacuated volume displaces',
  'replacedBy': {'authorDate': '2026-08-09T10:59:55-07:00',
                 'subject': 'physics: lift answers to altitude, and float-up and descent are different '
                            'questions'},
  'why': 'The simulator originally used sea-level density at every altitude. The replacement makes altitude an '
         'explicit argument; the fleet remains a simulation.'},
 {'id': 'vintage-closure',
  'identity': {'authorDate': '2026-08-12T13:18:36-07:00',
               'subject': 'The seven levels: the ship story gets its shell, and level 1 gets its catalog'},
  'path': 'cell/catalog.js',
  'pointers': None,
  'contains': 'liftT: 225.5, massT: 221.7',
  'expected': 'liftT: 225.5, massT: 221.7, residualT: 3.8, ratio: 1.017,',
  'replacedBy': {'authorDate': '2026-08-13T03:01:03-07:00',
                 'subject': 'The corrected ship physics lands under the gates: 322 parity values, both '
                            'knockdown worlds, the honest verdict on every surface'},
  'why': 'The scoping closure was replaced on the page by the corrected drawn-hull model and its negative '
         'record-world verdict.'},
 {'id': 'concept-positive',
  'identity': {'authorDate': '2026-08-13T04:25:01-07:00',
               'subject': "The second panel's verdict: no world floats as drawn — and the model now says "
                          'exactly why and what would change it'},
  'path': 'concept/index.html',
  'pointers': None,
  'contains': 'floats only in the best defensible world, with two named test campaigns',
  'expected': 'floats only in the best defensible world, with two named test campaigns',
  'replacedBy': None,
  'why': 'Still published, but contradicted by the same commit’s computed best-world ratio below the float '
         'line; the gate reports this sentence.'}]


def git_output(*args):
    p = subprocess.run(['git', *args],cwd=ROOT,capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    return p.stdout.rstrip('\n')


def history():
    try:
        log = git_output('log','HEAD','--format=%H%x09%aI%x09%s')
        shallow = git_output('rev-parse','--is-shallow-repository') == 'true'
    except RuntimeError:
        if (ROOT / '.git').exists():
            die('history is unreadable; refusing carry-forward for an inaccessible repository')
        log, shallow = '', True
    index={}
    for line in log.splitlines():
        sha,date,subject=line.split('\t',2)
        index.setdefault((date,subject),[]).append(sha)
    def resolve(identity):
        matches=index.get((identity['authorDate'],identity['subject']),[])
        if len(matches)>1:
            die('ambiguous history identity: ' + repr(identity))
        return matches[0] if matches else None
    resolved=[]; missing=False
    for spec in HISTORY_SPECS:
        sha=resolve(spec['identity']); repl=resolve(spec['replacedBy']) if spec['replacedBy'] else None
        missing |= sha is None or (spec['replacedBy'] is not None and repl is None)
        resolved.append((spec,sha,repl))
    if missing:
        if not shallow:
            die('a history row resolves to no commit in complete HEAD history')
        if not OUT_JSON.exists():
            die('shallow/exported tree has no ledger history to carry forward')
        old=json.loads(OUT_JSON.read_text())['history']
        if len(old)!=len(HISTORY_SPECS):
            die('carried history has a different row set')
        for row,(spec,sha,repl) in zip(old,resolved):
            if row['id']!=spec['id'] or row['identity']!=spec['identity'] or row['quotedValue']!=spec['expected']:
                die('carried history does not match the checked identities and excerpts')
            if (sha and row['commit']!=sha) or (repl and row['replacementCommit']!=repl):
                die('carried hashes disagree with available history; regenerate in a complete clone')
        print('float_ledger: history carried forward from the ledger: shallow/exported tree; '
              'missing commit files were NOT independently checked here.',file=sys.stderr)
        def sourced(v):
            if isinstance(v,str):return S(v,'carried history')
            if isinstance(v,list):return [sourced(x) for x in v]
            if isinstance(v,dict):return {k:sourced(x) for k,x in v.items()}
            return v
        return sourced(old)
    out=[]
    for spec,sha,repl in resolved:
        txt=git_output('show',sha+':'+spec['path'])
        if spec['pointers']:
            doc=json.loads(txt)
            value='; '.join(p+' = '+json.dumps(dig(doc,p),ensure_ascii=False) for p in spec['pointers'])
        else:
            lines=[l.strip() for l in txt.splitlines() if spec['contains'] in l]
            if len(lines)!=1:die('history excerpt is missing or ambiguous: '+spec['id'])
            value=lines[0]
        if value!=spec['expected']:die('history excerpt changed: '+spec['id'])
        out.append(dict(id=spec['id'], identity={k:S(v,'git author identity') for k,v in spec['identity'].items()},
                        commit=S(sha,'git resolved identity'),path=spec['path'],quotedValue=S(value,'git show'),
                        replacementIdentity=None if spec['replacedBy'] is None else
                            {k:S(v,'git author identity') for k,v in spec['replacedBy'].items()},
                        replacementCommit=None if repl is None else S(repl,'git resolved replacement'),
                        why=spec['why']))
    return out


def history_md(rows):
    def cell(s):return quote(S(str(s).replace('|','\\|').replace('<','&lt;').replace('>','&gt;'),'checked history'))
    return ('## The history of being wrong\n\n'
            'This is the checked sequence below, not an assertion of exhaustive history. Each identity '
            'uses author date and subject, then resolves to the hash in this repository. The quoted '
            'value is read from that commit’s own file. Rewriting hashes does not change the identity. '
            'Missing or ambiguous identities in complete history fail generation. Shallow clones '
            'carry this table forward with a diagnostic; they do not independently verify missing objects.\n\n'+
            table(['Author date, subject and resolved commit','Published value (quoted from the file)',
                   'Replacement and reason'],[
                [cell(r['identity']['authorDate'])+' — '+cell(r['identity']['subject'])+' (`'+cell(r['commit'])+'`)',
                 '`'+r['path']+'`: '+cell(r['quotedValue']),
                 ('Standing / not replaced in this checked sequence' if not r['replacementCommit'] else
                  cell(r['replacementIdentity']['authorDate'])+' — '+cell(r['replacementIdentity']['subject'])+
                  ' (`'+cell(r['replacementCommit'])+'`)')+'. '+r['why']] for r in rows]))


def generate(scratch):
    F=gather(scratch);K=knockdown_registry(F);designs=[];parts=[]
    for build in [d_record,d_tool_default,d_moves,d_sizes,d_mission0,d_bench,d_closed,d_r1,
                  d_one_metre,d_fleet,d_literature,d_v2,d_pressure]:
        d,md=build(F,K);designs.append(d);parts.append(md)
    check(F,'lift scales with density and every ship ratio is lift divided by mass',F.law_ok)
    check(F,'no computed case is a floating design today',not any(c['floatsToday'] for c in F.all_cases))
    hist=history()
    headlines=[F.c_rec,F.c_best,F.c_tool,F.c_tool_best,F.bench_cases[0],*F.mission_cases]
    headrows=[[c['label'],fmt(c['mass'])+' '+c['massUnit'],a(c,'seaLevel','liftToMass'),
               a(c,'seaLevel','margin',True),a(c,'target','liftToMass'),a(c,'target','margin',True)] for c in headlines]
    top=('# Float ledger\n\n**Nothing floats today as drawn.** These are computed masses and '
         'load cases, not flight or physical test results. Negative margin means a mass deficit '
         'before adding unpriced payload and equipment. A positive formula or allowance is not '
         'a floating vehicle.\n\n'
         f'Headline comparison: sea level ({num(F.rho_sl,4)} kg/m³) and the working altitude '
         f'{num(F.alt_t)} m ({num(F.rho_t,4)} kg/m³). **Every model structure is sized for full '
         f'vacuum against sea-level pressure, {num(Q(F.vc.P_ATM,MODEL))} Pa. Altitude changes lift only.** '
         'The pressure-schedule question below is explicitly not computed.\n\n'+
         table(['Design and basis','Mass','Lift ÷ mass at sea level','Margin at sea level (mass unit)',
                f'Lift ÷ mass at {num(F.alt_t)} m',f'Margin at {num(F.alt_t)} m (mass unit)'],headrows)+
         '\n\nGenerated by `«python3» tools/float_ledger.py`. Do not edit the generated files. '
         'The JSON carries every row’s quantity, units, factors, input status, code path and '
         'what would move it; tables below use the same rows. “Reviewed” describes code, not verified inputs.\n\n'+
         f'The structural SF column is separate from film sizing. Modern film-bearing model rows '
         f'use `«barrier_kg_per_m2()»` defaults: film SF {num(F.film_sf,1)} and assumed '
         f'efficiency {num(F.film_eff,2)}. These remain in force even in a structural crush-floor row. '
         'The JSON records this secondary basis per applicable row.\n\n'+
         '## Evidence and knockdowns\n\n'+table(['Class','Meaning'],[[v[0],v[1]] for v in EVIDENCE.values()])+
         '\n\n'+kd_table(K,list(K))+'\n\n## Definitions, not fitted values\n\n'+
         table(['Definition','Value','Meaning'],[[k,num(v),meaning] for k,(v,meaning) in DEFINITIONS.items()]))
    reads=list({c['id']:c for c in F.all_cases if c['readsOneOrMore']}.values())
    tail='\n\n## Rows that read one or more are not floating designs\n\n'+table(
        ['Row','Why this does not establish a floating design'],[[c['label'],c['notAFloatingDesignBecause']] for c in reads])
    tail+='\n\n## Self-checks\n\n'+'\n'.join('- HOLDS: '+c['check'] for c in F.checks)
    payload=dict(generatedBy='tools/float_ledger.py', verdict='Nothing floats today as drawn.',
                 atmosphere={'seaLevelM':N(F.alt_sl,0),'targetM':N(F.alt_t,0),
                             'rhoSeaLevel':N(F.rho_sl,6),'rhoTarget':N(F.rho_t,6)},
                 evidenceClasses={k:v[1] for k,v in EVIDENCE.items()},knockdowns=K,
                 definitions={k:dict(value=N(v,3),meaning=m) for k,(v,m) in DEFINITIONS.items()},
                 designs=designs,findings=F.findings,selfChecks=F.checks,sourceArtifacts=F.source_artifacts,
                 headlines=[c['id'] for c in headlines],readsOneOrMore=[c['id'] for c in reads],history=hist)
    js=json.dumps(plain(payload),ensure_ascii=False,indent=2)+'\n'
    md=unmark(top+'\n\n'+'\n\n'.join(parts)+'\n\n'+history_md(hist)+tail+'\n','Markdown ledger')
    for name,body in [('JSON',js),('Markdown',md)]:
        if re.search(r'/home/|/Users/|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',body):
            die('private path or email in generated '+name)
    return js,md


def write_pair(outputs):
    # No output is opened until generation, provenance and history checks all succeed.
    # Stage both complete files; roll back if the second replacement fails.
    staged=[]; old={p:p.read_bytes() if p.exists() else None for p,_ in outputs}
    try:
        for path,body in outputs:
            fd,tmp=tempfile.mkstemp(prefix='.'+path.name+'.',dir=path.parent)
            with os.fdopen(fd,'w',encoding='utf-8',newline='\n') as f:f.write(body)
            staged.append((path,pathlib.Path(tmp)))
        for path,tmp in staged:os.replace(tmp,path)
    except BaseException:
        for path,data in old.items():
            if data is None:path.unlink(missing_ok=True)
            else:path.write_bytes(data)
        raise
    finally:
        for _,tmp in staged:tmp.unlink(missing_ok=True)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true')
    ap.add_argument('--names',action='store_true')
    args=ap.parse_args()
    # Local scratch stays in the clone unless the caller supplies the lane's TMPDIR.
    base=pathlib.Path(os.environ.get('TMPDIR',str(ROOT / '.scratch' / 'ledger')))
    base.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='float-ledger-',dir=base) as tmp:
        js,md=generate(pathlib.Path(tmp))
    if args.names:
        print('\n'.join(sorted(NAMES_SEEN)));return 0
    outputs=[(OUT_JSON,js),(OUT_MD,md)]
    if args.check:
        stale=[]
        for path,body in outputs:
            if not path.exists() or path.read_bytes()!=body.encode('utf-8'):
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            print('float_ledger: fresh generation differs: '+', '.join(stale),file=sys.stderr);return 1
        print('float_ledger: both ledger files equal fresh generation');return 0
    write_pair(outputs)
    print('float_ledger: wrote research/analysis/float-ledger.json and docs/FLOAT-LEDGER.md')
    return 0


if __name__=='__main__':
    sys.exit(main())
