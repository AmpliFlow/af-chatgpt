"""Offline regression checks, not evidence of ChatGPT runtime behavior."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import validate_skills as skills
from validate_inventory import check_inventory

CONTRACT = json.loads(skills.CONTRACT_PATH.read_text())


def tool(name):
    return {"name": name, "description": "Synthetic read", "inputSchema": {"type": "object"}}


def page(names, cursor=None, next_cursor=None):
    result = {"tools": [tool(name) for name in names]}
    if next_cursor is not None:
        result["nextCursor"] = next_cursor
    return {"params": {} if cursor is None else {"cursor": cursor}, "result": result}


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.names = sorted(CONTRACT["supported_tools"])
        self.capture = {"pages": [page(self.names[:40], next_cursor="next"), page(self.names[40:], cursor="next")]}

    def test_full_catalog_over_40_includes_late_task_detail(self):
        errors, coverage = check_inventory(self.capture, CONTRACT)
        self.assertEqual(errors, [])
        self.assertEqual(coverage["reviewing-project-tasks"]["missing_required"], [])
        self.assertGreater(len(self.names), 40)
        self.assertNotIn("show_task", self.names[:40])

    def test_prefix_without_final_page_fails(self):
        self.capture["pages"].pop()
        errors, _ = check_inventory(self.capture, CONTRACT)
        self.assertTrue(any("incomplete" in error for error in errors))

    def test_complete_but_filtered_catalog_reports_exact_missing_dependency(self):
        capture = {"pages": [page([n for n in self.names if n != "show_task"])]}
        errors, coverage = check_inventory(capture, CONTRACT)
        self.assertTrue(errors)
        self.assertEqual(coverage["reviewing-project-tasks"]["missing_required"], ["show_task"])

    def test_optional_absence_is_not_core_failure(self):
        required = sorted({n for spec in CONTRACT["skills"].values() for n in spec["required_tools"]})
        errors, coverage = check_inventory({"pages": [page(required)]}, CONTRACT)
        self.assertEqual(errors, [])
        self.assertIn("list_history", coverage["reviewing-checklists"]["missing_optional"])

    def test_bad_cursor_and_duplicate_and_extra_page_fail(self):
        wrong_cursor = copy.deepcopy(self.capture)
        wrong_cursor["pages"][1]["params"]["cursor"] = "wrong"
        duplicate = {"pages": [page(self.names + ["show_task"])]}
        extra = {"pages": [page(self.names), page([])]}
        repeated = {"pages": [page([], next_cursor="same"), page([], cursor="same", next_cursor="same")]}
        for capture in (wrong_cursor, duplicate, extra, repeated):
            with self.subTest(capture=capture):
                errors, _ = check_inventory(capture, CONTRACT)
                self.assertTrue(errors)

    def test_malformed_input_fails_without_traceback(self):
        for capture in (None, [], {}, {"pages": []}, {"pages": [None]}, {"pages": [{"params": {}, "result": {"tools": [None]}}]}, {"pages": [{"params": {}, "error": {"code": 401}}]}):
            with self.subTest(capture=capture):
                errors, _ = check_inventory(capture, CONTRACT)
                self.assertTrue(errors)

    def test_cli_exit_codes_and_scope_warning(self):
        script = Path(__file__).with_name("validate_inventory.py")
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "capture.json"
            for capture, expected in ((self.capture, 0), ({"pages": [page([])]}, 1), (None, 1)):
                path.write_text(json.dumps(capture))
                result = subprocess.run([sys.executable, "-B", str(script), str(path)], capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                if expected == 0:
                    self.assertIn("does not prove ChatGPT discovery", result.stdout)

    def test_null_cursor_is_not_end_of_catalog(self):
        capture = {"pages": [page(self.names)]}
        capture["pages"][0]["result"]["nextCursor"] = None
        self.assertTrue(check_inventory(capture, CONTRACT)[0])

    def test_empty_string_cursor_is_opaque_and_followed(self):
        capture = {"pages": [page(self.names[:40], next_cursor=""), page(self.names[40:], cursor="")]}
        self.assertEqual(check_inventory(capture, CONTRACT)[0], [])

    def test_invalid_descriptor_fails(self):
        for field, value in (("name", ""), ("inputSchema", []), ("description", None)):
            capture = copy.deepcopy(self.capture)
            capture["pages"][0]["result"]["tools"][0][field] = value
            self.assertTrue(check_inventory(capture, CONTRACT)[0])


class SkillDiscoveryTests(unittest.TestCase):
    def test_each_skill_has_dependency_and_discovery_guidance(self):
        self.assertEqual(skills.validate(skills.ROOT), [])
        for name, spec in CONTRACT["skills"].items():
            root = skills.ROOT / "skills" / name
            self.assertEqual(skills.validate_dependency(root / "agents" / "openai.yaml"), [])
            text = (root / "SKILL.md").read_text()
            self.assertIn("## Tool discovery", text)
            self.assertIn("if the runtime exposes one", text)
            self.assertIn("actual binding and input schema", text)
            self.assertIn("at most one discovery request", text)
            self.assertIn("optional_tools", spec)

    def test_unknown_tool_and_checklist_export_rejected(self):
        name = "reviewing-checklists"
        source = (skills.ROOT / "skills" / name / "SKILL.md").read_text()
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "SKILL.md"
            for instruction in ("Call `export_checklist_report`.", "Use the connected tool `get_unknown`."):
                path.write_text(source + "\n" + instruction)
                errors = skills.validate_skill(path, name, CONTRACT["skills"][name]["required_tools"], set(CONTRACT["supported_tools"]))
                self.assertTrue(any("unsupported MCP tool" in error for error in errors))

    def test_removed_discovery_guidance_rejected(self):
        name = "reviewing-project-tasks"
        source = (skills.ROOT / "skills" / name / "SKILL.md").read_text()
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text(source.replace("if the runtime exposes one", "unconditionally"))
            errors = skills.validate_skill(path, name, CONTRACT["skills"][name]["required_tools"], set(CONTRACT["supported_tools"]))
            self.assertTrue(any("conditional discovery" in error for error in errors))

    def test_missing_or_wrong_dependency_rejected(self):
        source = skills.ROOT / "skills" / "reviewing-project-tasks" / "agents" / "openai.yaml"
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "openai.yaml"
            self.assertTrue(skills.validate_dependency(path))
            path.write_text(source.read_text().replace("https://mcp.ampliflow.cc/mcp", "https://wrong.example/mcp"))
            self.assertTrue(skills.validate_dependency(path))


if __name__ == "__main__":
    unittest.main()
