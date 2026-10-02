"""Real scratch histories for the builder gate; no commits in the working repository."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/check_builder_line.py"
ATTESTATION = "docs/governance/landing-attestations.md"


class BuilderLine(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "source"
        self.root.mkdir()
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME="Example Builder", GIT_COMMITTER_NAME="Example Builder",
                        GIT_AUTHOR_EMAIL="", GIT_COMMITTER_EMAIL="")
        self.git("init", "-q", "--initial-branch=main")
        self.commit("Earlier work")
        self.start = self.commit("Start record\n\nBuilder: example-model")

    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", "-C", str(cwd or self.root), *args],
                                       env=self.env, stderr=subprocess.STDOUT).decode().strip()

    def commit(self, message, paths=("example.txt",)):
        for name in paths:
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text((p.read_text() if p.exists() else "") + "change\n")
        self.git("add", "-A")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def run_gate(self, root=None):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(root or self.root)],
                              env=self.env, capture_output=True, text=True)

    def test_a_missing_builder_fails_and_names_commit(self):
        missing = self.commit("Change without a builder")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn(missing, result.stdout)
        self.assertIn("missing Builder:", result.stdout)
        print("(a)", result.stdout.strip())

    def test_b_builder_before_separate_audit_paragraph_passes(self):
        self.commit("Change without a builder")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "--amend", "-q", "-m",
                 "Change without a builder\n\nBuilder: example-model\n\nHelm-Audit-ID: x")
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("checked 2 commits; 0 attestations exempted", result.stdout)
        self.assertIn(self.start, result.stdout)
        print("(b)", result.stdout.strip())

    def test_c_attestation_only_passes_regardless_of_subject(self):
        self.commit("An ordinary subject", (ATTESTATION,))
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("1 attestations exempted", result.stdout)
        print("(c)", result.stdout.strip())

    def test_d_mixed_attestation_fails_regardless_of_subject(self):
        missing = self.commit("Record-only landing attestation", (ATTESTATION, "other.txt"))
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn(missing, result.stdout)
        print("(d)", result.stdout.strip())

    def test_e_export_has_no_history_and_node_reports_skip(self):
        export = self.root / "export"
        for relative in ("tools/check_builder_line.py", "3d/tests/builder-line.test.mjs"):
            dest = export / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, dest)
        result = self.run_gate(export)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no history; nothing checked", result.stdout)
        print("(e)", result.stdout.strip())
        node = subprocess.run(["node", "--test", "3d/tests/builder-line.test.mjs"],
                              cwd=export, env=self.env, capture_output=True, text=True)
        self.assertEqual(node.returncode, 0, node.stdout + node.stderr)
        self.assertIn("# SKIP buildercheck: no history;", node.stdout)
        self.assertIn("# pass 0", node.stdout)
        print("(e) node: pass 0; skipped 1 (no history)")

    def test_full_history_without_record_fails(self):
        self.git("-c", "core.hooksPath=/dev/null", "commit", "--amend", "-q", "-m", "No record")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("no Builder record found", result.stdout)

    def test_shallow_history_without_record_is_honest(self):
        self.commit("Outside the visible record")
        shallow = Path(self.tmp.name) / "shallow"
        self.git("clone", "-q", "--depth=1", self.root.as_uri(), str(shallow))
        result = self.run_gate(shallow)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("shallow; checked 0 commits", result.stdout)
        print("shallow:", result.stdout.strip())

    def test_shallow_history_still_checks_visible_record(self):
        missing = self.commit("Missing builder")
        shallow = Path(self.tmp.name) / "shallow"
        self.git("clone", "-q", "--depth=2", self.root.as_uri(), str(shallow))
        result = self.run_gate(shallow)
        self.assertEqual(result.returncode, 1)
        self.assertIn("shallow;", result.stdout)
        self.assertIn(missing, result.stdout)

    def test_linked_worktree_and_case_insensitive_line(self):
        self.commit("Another change\n\nbUiLdEr:\t example-model")
        linked = Path(self.tmp.name) / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        self.assertTrue((linked / ".git").is_file())
        result = self.run_gate(linked)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("checked 2 commits", result.stdout)

    def test_blank_builder_is_missing(self):
        missing = self.commit("Unnamed change\n\nBuilder:   \n\nHelm-Audit-ID: x")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn(missing, result.stdout)

    def test_only_first_parent_commits_are_checked(self):
        self.git("checkout", "-q", "-b", "side")
        self.commit("Side work", ("side.txt",))
        self.git("checkout", "-q", "main")
        self.commit("Main work\n\nBuilder: example-model", ("main.txt",))
        self.git("-c", "core.hooksPath=/dev/null", "merge", "--no-ff", "-q", "side", "-m",
                 "Integrate side work\n\nBuilder: example-model")
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("checked 3 commits", result.stdout)

    def test_broken_git_file_is_an_error_not_no_history(self):
        broken = Path(self.tmp.name) / "broken"
        broken.mkdir()
        (broken / ".git").write_text("gitdir: missing\n")
        result = self.run_gate(broken)
        self.assertEqual(result.returncode, 1)
        self.assertIn("could not check history", result.stderr)


if __name__ == "__main__":
    unittest.main()
