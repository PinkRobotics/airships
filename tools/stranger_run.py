#!/usr/bin/env python3
"""Run every check gate in a fresh local clone with an empty environment and HOME.

  TMPDIR=<scratch> python3 tools/stranger_run.py --commit HEAD
  TMPDIR=<scratch> python3 tools/stranger_run.py --commit HEAD --working-tree \
      --include tools/stranger_run.py --include tools/check_ci_parity.py

Default input is exactly a commit. --working-tree applies the tracked diff against that
commit plus explicitly named untracked files, without making a commit. The report labels
that overlay and hashes the complete input tree. Ignored files and build outputs are not
copied. Run under the project's shared make-check lock on a shared workstation.

This is not a container or a dependency installer. Python packages, system tools, kernel,
and network remain host-provided. An actual headless Chromium probe decides whether
bubblewrap can hide the real home. Failed isolation is reported, never called isolated.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import time

from check_ci_parity import make_gates

ROOT = Path(__file__).resolve().parent.parent
SYSTEM_PATH = "/usr/local/bin:/usr/bin:/bin:/snap/bin"
# Current fixed-port browser drivers. Refuse an occupied port instead of borrowing a
# server that may serve another checkout. The remaining drivers allocate ephemeral ports.
FIXED_PORTS = (8791, 8871, 8898, 8907, 8909, 8911, 8913)


def process(command, cwd, timeout=60, input_bytes=None):
    """Bound the command and clean up only the process group this invocation started."""
    proc = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            start_new_session=True)
    timed_out = False
    try:
        try:
            output, _ = proc.communicate(input_bytes, timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGKILL)
            output, _ = proc.communicate()
    finally:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    return (124 if timed_out else proc.returncode), output


def env_command(env, command, prefix=()):
    return ["/usr/bin/env", "-i", *(f"{k}={v}" for k, v in sorted(env.items())),
            *prefix, *command]


def clean_environment(run):
    home, scratch, bin_dir = run / "home", run / "tmp", run / "bin"
    for path in (home, scratch, bin_dir):
        path.mkdir()
    # Legacy gates create TemporaryDirectory(dir=Path.home() / 'tmp'). No user state
    # is seeded: HOME contains only this empty scratch directory before tools start.
    (home / "tmp").mkdir()
    return {
        "PATH": f"{bin_dir}:{SYSTEM_PATH}", "HOME": str(home), "TMPDIR": str(scratch),
        "AIRSHIPS_TMPDIR": str(scratch), "A3D_CHROME_PROFILE": str(scratch / "3d-profile"),
        "A3D_TEST_TIMEOUT": "1800", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1",
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
    }


def scrubber(source, run):
    account = pwd.getpwuid(os.getuid())
    substitutions = [(str(source), "<source>"), (str(run), "<scratch>"),
                     (str(Path.home()), "<real-home>"), (account.pw_dir, "<real-home>")]
    identities = {account.pw_name, socket.gethostname(), socket.getfqdn()}

    def scrub(text):
        text = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)
        for value, label in sorted(substitutions, key=lambda p: -len(p[0])):
            text = text.replace(value, label)
        for identity in identities:
            if identity:
                text = re.sub(r"(?<![\w-])" + re.escape(identity) + r"(?![\w-])",
                              "<identity>", text)
        # Also redact home paths and addresses emitted by a tool about another account.
        text = re.sub(r"/(?:home|Users)/[^\s\"'<>:]+", "<home-path>", text)
        return re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "<email>", text)
    return scrub


def git(source, env, *args):
    rc, out = process(env_command(env, ["git", "-C", str(source), *args]), source)
    if rc:
        raise RuntimeError(f"git {args[0]} failed: " + out.decode(errors="replace"))
    return out


def clone_input(source, clone, commit, overlay, includes, env):
    sha = git(source, env, "rev-parse", "--verify", f"{commit}^{{commit}}").decode().strip()
    git(source, env, "clone", "--quiet", "--no-hardlinks", "--no-checkout", str(source), str(clone))
    git(clone, env, "checkout", "--quiet", "--detach", sha)
    git(clone, env, "remote", "remove", "origin")
    patch = b""
    if includes and not overlay:
        raise ValueError("--include requires --working-tree")
    if overlay:
        patch = git(source, env, "diff", "--binary", "--no-ext-diff", "--no-textconv", sha, "--")
        if patch:
            rc, out = process(env_command(env, ["git", "apply", "--binary", "-"]), clone,
                              input_bytes=patch)
            if rc:
                raise RuntimeError("overlay did not apply: " + out.decode(errors="replace"))
    untracked = set(git(source, env, "ls-files", "--others", "--exclude-standard", "-z")
                    .decode().rstrip("\0").split("\0"))
    for name in includes:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or name not in untracked:
            raise ValueError("--include must name an untracked, non-ignored repository file")
        src = source / relative
        if not src.is_file() or src.is_symlink() or not src.resolve().is_relative_to(source):
            raise ValueError("--include must name an ordinary file inside the repository")
        dest = clone / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    return sha, {"mode": "working-tree-overlay" if overlay else "commit",
                 "patch_sha256": hashlib.sha256(patch).hexdigest(),
                 "included_files": sorted(includes), "tree_sha256": tree_digest(clone, env)}


def tree_digest(clone, env):
    names = git(clone, env, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    digest = hashlib.sha256()
    for name in sorted(set(names.split(b"\0")) - {b""}):
        path = clone / os.fsdecode(name)
        if not path.exists() and not path.is_symlink():
            continue  # tracked deletion in an overlay
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            content, kind = os.fsencode(os.readlink(path)), b"120000"
        elif stat.S_ISREG(mode):
            content = path.read_bytes()
            kind = b"100755" if mode & 0o111 else b"100644"
        else:
            raise ValueError("tree contains an unsupported entry")
        digest.update(name + b"\0" + kind + b"\0" + hashlib.sha256(content).digest())
    return digest.hexdigest()


def isolation_probe(run, env):
    real_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    prefix = ["/usr/bin/bwrap", "--die-with-parent", "--ro-bind", "/", "/",
              "--tmpfs", str(real_home), "--bind", str(run), str(run),
              "--dev-bind", "/dev", "/dev", "--proc", "/proc", "--"]
    chrome = ["chromium", "--headless=new", "--no-sandbox", "--disable-gpu",
              "--disable-background-networking", "--no-first-run", "--dump-dom",
              "data:text/html,<title>stranger-probe</title>"]
    attempts = []
    for hidden in (True, False):
        if hidden and not Path("/usr/bin/bwrap").is_file():
            attempts.append({"mode": "bwrap", "exit_code": None, "rendered": False,
                             "reason": "bwrap unavailable"})
            continue
        profile = run / "tmp" / ("probe-hidden" if hidden else "probe-env")
        rc, out = process(env_command(env, [*chrome, f"--user-data-dir={profile}"],
                                     prefix if hidden else ()), run, timeout=30)
        rendered = rc == 0 and b"<title>stranger-probe</title>" in out
        reason = "headless page rendered" if rendered else (
            "snap-confine refused the mount namespace" if b"snap-confine" in out else
            "headless probe timed out" if rc == 124 else "headless probe failed")
        attempts.append({"mode": "bwrap" if hidden else "env-only", "exit_code": rc,
                         "rendered": rendered, "reason": reason})
        if rendered:
            return (prefix if hidden else []), attempts
    raise RuntimeError("Chromium cannot render even with env-only isolation")


def tool_versions(env, prefix, run):
    commands = {
        "python": ["python3", "--version"], "node": ["node", "--version"],
        "chromium": ["chromium", "--version"], "make": ["make", "--version"],
        "git": ["git", "--version"], "latexmk": ["latexmk", "-v"],
        "pdflatex": ["pdflatex", "--version"], "pdfinfo": ["pdfinfo", "-v"],
        "python_packages": ["python3", "-c", "import importlib.metadata as m; "
                            "print('; '.join(n+'='+m.version(n) for n in "
                            "['websockets','numpy','Pillow','PyYAML']))"],
    }
    result = {}
    for name, cmd in commands.items():
        rc, out = process(env_command(env, cmd, prefix), run, timeout=30)
        lines = out.decode(errors="replace").strip().splitlines()
        # latexmk's first line contains the tool author's address; use only its version.
        if name == "latexmk":
            match = re.search(r"\bVersion\s+([0-9][\w.-]*)", out.decode(errors="replace"))
            lines = ["Latexmk " + match.group(1)] if match else []
        result[name] = {"exit_code": rc, "version": lines[0] if lines and rc == 0 else None}
    return result


def run_gates(clone, gates, env, prefix, timeout, scrub):
    results = []
    for gate in gates:
        start = time.monotonic()
        rc, raw = process(env_command(env, ["make", "--no-print-directory", gate], prefix),
                          clone, timeout=timeout)
        output = scrub(raw.decode(errors="replace"))
        result = {"gate": gate, "status": "pass" if rc == 0 else "fail", "exit_code": rc,
                  "seconds": round(time.monotonic() - start, 3),
                  "output_tail": output.splitlines()[-30:]}
        results.append(result)
        print(f"{gate}: {result['status']} ({rc}), {result['seconds']:.3f}s", flush=True)
    return results


def report_exit(report):
    return 0 if (not report["errors"] and report["gates"] and
                 all(g["exit_code"] == 0 for g in report["gates"])) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--commit", default="HEAD")
    ap.add_argument("--source", type=Path, default=ROOT)
    ap.add_argument("--working-tree", action="store_true")
    ap.add_argument("--include", action="append", default=[])
    ap.add_argument("--output", type=Path, default=Path("stranger-run.json"))
    ap.add_argument("--gate-timeout", type=int, default=3600)
    args = ap.parse_args()
    report = {"schema_version": 1, "commit": None,
              "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "source": None, "tools": {}, "isolation": {}, "gates": [], "errors": [],
              "status": "fail"}
    # TMPDIR is mandatory. There is no implicit platform temporary-directory fallback.
    scratch = os.environ.get("TMPDIR")
    if not scratch or not Path(scratch).is_dir():
        report["errors"].append("TMPDIR must name an existing scratch directory")
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        return 1
    source = args.source.resolve()
    with tempfile.TemporaryDirectory(prefix="stranger-", dir=scratch,
                                     ignore_cleanup_errors=True) as td:
        run = Path(td).resolve()
        scrub = scrubber(source, run)
        try:
            env = clean_environment(run)
            # A user-installed Node executable is copied into the disposable tool directory;
            # no private bin directory is placed on PATH or exposed through the home mask.
            node = shutil.which("node")
            if not node:
                raise RuntimeError("Node must be installed; stranger runs do not accept the browser shim")
            shutil.copy2(node, run / "bin/node")
            clone = run / "repo"
            report["commit"], report["source"] = clone_input(
                source, clone, args.commit, args.working_tree, args.include, env)
            gates = make_gates((clone / "Makefile").read_text())
            prefix, probes = isolation_probe(run, env)
            report["isolation"] = {
                "environment": "env -i with an explicit allowlist",
                "environment_keys": sorted(env), "fresh_home": True,
                "home_seed": "one empty tmp directory; no user configuration copied",
                "real_home_hidden": bool(prefix), "bwrap_probes": probes, "container": False,
                "tool_path": "disposable Node copy plus system executable directories",
                "scratch": "new directory under caller TMPDIR; removed after report",
                "not_isolated": ["host kernel and installed system tools and Python packages",
                                 "host network; fixed test ports checked for availability",
                                 "host identity and system configuration"] + (
                                     [] if prefix else ["host filesystem, including real home"]),
            }
            report["tools"] = tool_versions(env, prefix, run)
            for port in FIXED_PORTS:
                with socket.socket() as sock:
                    try:
                        sock.bind(("127.0.0.1", port))
                    except OSError as exc:
                        raise RuntimeError(f"test port {port} is occupied; refusing another checkout's server") from exc
            report["gates"] = run_gates(clone, gates, env, prefix, args.gate_timeout, scrub)
        except (OSError, RuntimeError, ValueError) as exc:
            report["errors"].append(scrub(str(exc)))
        rc = report_exit(report)
        report["status"] = "pass" if rc == 0 else "fail"
        # Scrub the entire record, including version strings and preflight errors.
        args.output.write_text(scrub(json.dumps(report, indent=2, sort_keys=True)) + "\n")
    print(f"stranger run: {report['status']}; {len(report['gates'])} gates recorded", flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
