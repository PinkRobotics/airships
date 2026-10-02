"""Exercise the real Make target in disposable copies; never mutate protected model files."""
from __future__ import annotations

import contextlib
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from schema import validate


class SourceSchema(unittest.TestCase):
    def test_source_schema_rejects_invalid_records_and_private_text(self):
        original = json.loads((HERE / "sources.json").read_text())
        validate(original)
        mutations = [
            ("missing field", lambda d: d["records"][0].pop("locator")),
            ("bad class", lambda d: d["records"][0].update({"class": "simulation"})),
            ("long quote", lambda d: d["records"][0].update({"quote": "word " * 25})),
            ("home path", lambda d: d["records"][0].update({"limits": "/" + "home/example/private"})),
            ("email", lambda d: d["records"][0].update({"limits": "example" + "@" + "example.invalid"})),
            ("repr value", lambda d: d["records"][0].update({"value": "{'H_m': '0'}"})),
            ("repr document", lambda d: d["records"][0].update({"document": "{'title': 'x'}"})),
            ("lost digits", lambda d: d["records"][0]["value"].update({"H_m": 0})),
            ("removed record", lambda d: d["records"].pop(6)),
        ]
        for name, mutate in mutations:
            with self.subTest(name=name):
                data = copy.deepcopy(original)
                mutate(data)
                with self.assertRaises(ValueError):
                    validate(data)


class Gate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scratch = os.environ.get("TMPDIR")
        if not scratch:
            raise RuntimeError("set TMPDIR to an explicit scratch directory")
        cls.tmp = tempfile.TemporaryDirectory(prefix="labelled-gate-", dir=scratch)
        cls.root = Path(cls.tmp.name)
        shutil.copy(ROOT / "Makefile", cls.root / "Makefile")
        shutil.copytree(ROOT / "sim", cls.root / "sim")
        shutil.copytree(HERE, cls.root / "research/validation",
                        ignore=shutil.ignore_patterns("__pycache__"))
        analysis = cls.root / "research/analysis"
        analysis.mkdir()
        for name in ("helium.py", "vacuum-cell.py", "vacuum-cell.json", "reproductions.py"):
            shutil.copy(ROOT / "research/analysis" / name, analysis / name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_gate(self, expected):
        result = subprocess.run(["make", "--no-print-directory", "labelledcheck"],
                                cwd=self.root, text=True, capture_output=True, timeout=60,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    @contextlib.contextmanager
    def mutated(self, path, transform):
        file = self.root / path
        old = file.read_bytes()
        try:
            file.write_text(transform(old.decode()))
            yield
        finally:
            file.write_bytes(old)

    def test_01_baseline_keeps_misses_and_does_not_write(self):
        paths = [self.root / "research/validation" / name for name in ("report.json", "report.md")]
        before = [p.read_bytes() for p in paths]
        result = self.run_gate(0)
        report = json.loads(before[0])
        self.assertTrue(any(r["verdict"] == "MISS" for c in report["checks"] for r in c["rows"]))
        self.assertEqual(before, [p.read_bytes() for p in paths])
        print("baseline: make labelledcheck exit 0; existing MISS rows retained; report bytes unchanged")

    def test_02_six_reference_mutations(self):
        mutations = [
            ("1-atmosphere", 1, "rho", "1.2000 × 10^0 kg/m^3"),
            ("2-hindenburg", 11, "total_lift_lb", "480000"),
            ("3-cl415-cycle", 18, "3_miles", "5 minutes"),
            ("4-helicopter-hover", 23, "takeoff_power", "MRP = 4300 hp"),
            ("5-vacuum-shells", 27, "example_shell_mass_kg", "76.0"),
            ("6-helium", 30, None, "0.170000"),
            ("6-helium", 31, None, "1.1"),
            ("6-helium", 32, "helium_gross_lift_lb", "2500"),
            ("6-helium", 34, "max_takeoff_weight_kg", "9500"),
            ("4-helicopter-hover", 35, "engine_power_hp", "1500"),
            ("5-vacuum-shells", 27, "example_payload_at_zero_buoyancy_kg", "9.7"),
            ("3-cl415-cycle", 18, "1_mile", "1 minute"),
            ("3-cl415-cycle", 18, "6_miles", "1 minute"),
            ("3-cl415-cycle", 18, "10_miles", "1 minute"),
            ("3-cl415-cycle", 18, "15_miles", "1 minute"),
            ("3-cl415-cycle", 19, "time_on_water", "approximately 20 to 22 seconds"),
        ]
        for name, index, field, value in mutations:
            with self.subTest(check=name):
                def transform(text):
                    data = json.loads(text)
                    if field is None:
                        data["records"][index]["value"] = value
                    else:
                        data["records"][index]["value"][field] = value
                    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
                with self.mutated("research/validation/sources.json", transform):
                    result = self.run_gate(2)
                    self.assertIn("report.json is stale", result.stderr)
                    # The report's actual reference row must change, not just a data hash.
                    self.assertIn("reference", self.render_changed_fields(name))
                    excerpt = next(line for line in result.stderr.splitlines() if "is stale" in line)
                    print(f"reference {name} record {index} {field or 'value'} -> {value}: "
                          f"exit 2; {excerpt}")
                self.run_gate(0)
                print(f"reference {name}: restored; make labelledcheck exit 0")

    def render_changed_fields(self, check_id):
        # Run the same generator without writing; make's stale check has already run above.
        command = [sys.executable, "-B", "-c",
                   "import sys,json; sys.path.insert(0,'research/validation'); "
                   "import check; print(json.dumps(check.generate()))"]
        p = subprocess.run(command, cwd=self.root, capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        fresh = next(c for c in json.loads(p.stdout)["checks"] if c["id"] == check_id)
        old = next(c for c in json.loads((self.root / "research/validation/report.json").read_text())["checks"]
                   if c["id"] == check_id)
        changed = set()
        for index, (previous, current) in enumerate(zip(old["rows"], fresh["rows"])):
            changed.update(key for key in current if previous.get(key) != current[key])
            if previous["model_value"] != current["model_value"]:
                changed.add(f"model_row_{index}")
        if old.get("model_diagnostics") != fresh.get("model_diagnostics"):
            changed.add("model_diagnostics")
        return changed

    def test_03_six_model_mutations_in_disposable_copy(self):
        mutations = [
            ("1-atmosphere", "sim/atmosphere.js",
             "return densityRatio(hM) * rho0;", "return densityRatio(hM) * rho0 * 1.01;", "model_value"),
            ("2-hindenburg", "sim/physics.js",
             "return volumeM3 * (purity * (rho - gasDensity));",
             "return 1.01 * volumeM3 * (purity * (rho - gasDensity));", "model_value"),
            ("3-cl415-cycle", "sim/plan.js",
             "gsOut, gsRet, tailOut, windUsed:", "gsOut: gsOut * 0.5, gsRet, tailOut, windUsed:", "model_value"),
            ("4-helicopter-hover", "sim/physics.js",
             "return Math.pow(thrustN, 1.5)", "return 1.01 * Math.pow(thrustN, 1.5)", "model_value"),
            ("5-vacuum-shells", "research/analysis/reproductions.py",
             "thin_mass = 4 * math.pi", "thin_mass = 4.1 * math.pi", "model_value"),
            ("5-vacuum-shells", "research/analysis/vacuum-cell.py",
             'MATERIALS["T700_LAM"]["E"] * s["I"]',
             '1.01 * MATERIALS["T700_LAM"]["E"] * s["I"]', "model_diagnostics"),
            ("6-helium", "research/analysis/helium.py",
             "return pressure_Pa / (constants[gas] * temperature_K)",
             "return 1.01 * pressure_Pa / (constants[gas] * temperature_K)", "model_value"),
            ("6-helium", "research/analysis/helium.py",
             'return gas_density(temperature_K, pressure_Pa, "air") - gas_kg_m3 - structure_kg_m3',
             'return gas_density(temperature_K, pressure_Pa, "air") - gas_kg_m3 - structure_kg_m3 + 0.01', "model_value"),
            ("3-cl415-cycle", "sim/plan.js",
             'dur.WATER_FILL = deliveredT / fill / 60;',
             'dur.WATER_FILL = deliveredT / fill / 30;', "model_value"),
        ]
        for name, path, old, new, changed_field in mutations:
            with self.subTest(check=name):
                def transform(text):
                    self.assertEqual(text.count(old), 1)
                    return text.replace(old, new)
                with self.mutated(path, transform):
                    result = self.run_gate(2)
                    self.assertIn("report.json is stale", result.stderr)
                    changed = self.render_changed_fields(name)
                    self.assertIn(changed_field, changed)
                    expected_rows = []
                    if name == "2-hindenburg": expected_rows = [0]
                    if name == "3-cl415-cycle": expected_rows = list(range(6 if "WATER_FILL" in old else 5))
                    if name == "4-helicopter-hover": expected_rows = [0, 1, 2]
                    if name == "5-vacuum-shells" and "thin_mass" in old: expected_rows = [0, 1]
                    if name == "6-helium": expected_rows = [1, 2, 3] if "return gas_density" in old else [0, 1, 2, 3]
                    for index in expected_rows:
                        self.assertIn(f"model_row_{index}", changed)
                    print(f"model {name} {path}: exit 2; report.json is stale; "
                          f"computed {changed_field} changed")
                self.run_gate(0)
                print(f"model {name}: restored; make labelledcheck exit 0")

    def test_04_bad_schema_and_failed_model_go_red(self):
        def bad_schema(text):
            data = json.loads(text)
            data["records"][0].pop("quote")
            return json.dumps(data)
        with self.mutated("research/validation/sources.json", bad_schema):
            self.assertIn("missing required fields", self.run_gate(2).stderr)
        with self.mutated("sim/atmosphere.js", lambda text: "throw new Error('fixture model failure');\n" + text):
            self.assertIn("JavaScript model could not run", self.run_gate(2).stderr)
        with self.mutated("research/analysis/helium.py",
                          lambda text: text.replace('if __name__ == "__main__":',
                                                    'raise ValueError("fixture gas failure")\nif __name__ == "__main__":')):
            self.assertIn("cannot run", self.run_gate(2).stderr)
        self.run_gate(0)
        print("bad schema, JavaScript failure and Python failure: exit 2 each; restored exit 0")

    def test_05_either_report_drift_goes_red(self):
        for filename in ("report.json", "report.md"):
            with self.mutated(f"research/validation/{filename}", lambda text: text + "\n"):
                self.assertIn(f"{filename} is stale", self.run_gate(2).stderr)
            self.run_gate(0)
        print("JSON and Markdown drift: exit 2 each; restored exit 0")

    def test_06_update_publishes_a_new_miss_then_gate_passes(self):
        files = ["sources.json", "report.json", "report.md"]
        before = {f: (self.root / "research/validation" / f).read_bytes() for f in files}
        try:
            data = json.loads(before["sources.json"])
            data["records"][0]["value"]["T_K"] = "280.000"
            (self.root / "research/validation/sources.json").write_text(json.dumps(data))
            self.run_gate(2)
            p = subprocess.run([sys.executable, "-B", "research/validation/check.py", "--update"],
                               cwd=self.root, capture_output=True, text=True, timeout=60)
            self.assertEqual(p.returncode, 0, p.stderr)
            report = json.loads((self.root / "research/validation/report.json").read_text())
            self.assertEqual(report["checks"][0]["rows"][0]["verdict"], "MISS")
            self.run_gate(0)
            print("new reference miss: exit 2 before --update; MISS published by --update; exit 0 after")
        finally:
            for name, content in before.items():
                (self.root / "research/validation" / name).write_bytes(content)
        self.run_gate(0)

    def test_07_target_without_tmpdir_needs_no_runtime_scratch(self):
        env = {k: v for k, v in os.environ.items() if k != "TMPDIR"}
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        p = subprocess.run(["make", "--no-print-directory", "labelledcheck"],
                           cwd=self.root, capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(list((self.root / "research/validation").glob("labelled-helium-*")), [])
        print("no TMPDIR: checker needs no runtime scratch; exit 0; no temporary directory created")


if __name__ == "__main__":
    unittest.main()
