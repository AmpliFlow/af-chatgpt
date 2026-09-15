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
COMMIT_TOOLS = ["commit_ampliflow_change", "commit_destructive_ampliflow_change"]


def tool(name):
    return {
        "name": name,
        "title": name.replace("_", " ").title(),
        "description": "Synthetic compact AmpliFlow tool",
        "inputSchema": {"type": "object"},
    }


def page(names, cursor=None, next_cursor=None):
    result = {"tools": [tool(name) for name in names]}
    if next_cursor is not None:
        result["nextCursor"] = next_cursor
    return {"params": {} if cursor is None else {"cursor": cursor}, "result": result}


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.names = sorted(CONTRACT["supported_dispatchers"] + COMMIT_TOOLS)
        midpoint = max(1, len(self.names) // 2)
        self.capture = {
            "pages": [
                page(self.names[:midpoint], next_cursor="next"),
                page(self.names[midpoint:], cursor="next"),
            ]
        }

    def test_compact_catalog_covers_dispatchers_not_underlying_operations(self):
        errors, coverage = check_inventory(self.capture, CONTRACT)
        self.assertEqual(errors, [])
        self.assertEqual(coverage["reviewing-project-tasks"]["missing_required_dispatchers"], [])
        self.assertIn("list_projects", coverage["reviewing-project-tasks"]["operations_require_runtime_catalog"])
        self.assertNotIn("list_projects", self.names)
        self.assertLessEqual(len(self.names), 30)

    def test_prefix_without_final_page_fails(self):
        self.capture["pages"].pop()
        errors, _ = check_inventory(self.capture, CONTRACT)
        self.assertTrue(any("incomplete" in error for error in errors))

    def test_complete_but_filtered_catalog_reports_exact_missing_dispatcher(self):
        capture = {"pages": [page([name for name in self.names if name != "ampliflow_tasks"])]}
        errors, coverage = check_inventory(capture, CONTRACT)
        self.assertTrue(errors)
        self.assertEqual(coverage["reviewing-project-tasks"]["missing_required_dispatchers"], ["ampliflow_tasks"])

    def test_optional_dispatcher_absence_is_not_core_failure(self):
        names = [name for name in self.names if name != "ampliflow_history"]
        errors, coverage = check_inventory({"pages": [page(names)]}, CONTRACT)
        self.assertEqual(errors, [])
        self.assertEqual(coverage["reviewing-checklists"]["missing_optional_dispatchers"], ["ampliflow_history"])

    def test_direct_legacy_operation_surface_is_rejected(self):
        capture = {"pages": [page(self.names + ["list_projects"])]}
        errors, _ = check_inventory(capture, CONTRACT)
        self.assertTrue(any("legacy operation" in error for error in errors))

    def test_more_than_30_top_level_tools_is_rejected(self):
        names = [f"ampliflow_extra_{index}" for index in range(31)]
        errors, _ = check_inventory({"pages": [page(names)]}, CONTRACT)
        self.assertTrue(any("30-tool" in error for error in errors))

    def test_bad_cursor_and_duplicate_and_extra_page_fail(self):
        wrong_cursor = copy.deepcopy(self.capture)
        wrong_cursor["pages"][1]["params"]["cursor"] = "wrong"
        duplicate = {"pages": [page(self.names + [self.names[0]])]}
        extra = {"pages": [page(self.names), page([])]}
        repeated = {"pages": [page([], next_cursor="same"), page([], cursor="same", next_cursor="same")]}
        for capture in (wrong_cursor, duplicate, extra, repeated):
            with self.subTest(capture=capture):
                errors, _ = check_inventory(capture, CONTRACT)
                self.assertTrue(errors)

    def test_malformed_input_fails_without_traceback(self):
        malformed = (
            None,
            [],
            {},
            {"pages": []},
            {"pages": [None]},
            {"pages": [{"params": {}, "result": {"tools": [None]}}]},
            {"pages": [{"params": {}, "error": {"code": 401}}]},
        )
        for capture in malformed:
            with self.subTest(capture=capture):
                errors, _ = check_inventory(capture, CONTRACT)
                self.assertTrue(errors)

    def test_cli_exit_codes_and_scope_warning(self):
        script = Path(__file__).with_name("validate_inventory.py")
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "capture.json"
            for capture, expected in ((self.capture, 0), ({"pages": [page([])]}, 1), (None, 1)):
                path.write_text(json.dumps(capture))
                result = subprocess.run(
                    [sys.executable, "-B", str(script), str(path)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                if expected == 0:
                    self.assertIn("does not prove operation catalog coverage", result.stdout)

    def test_null_cursor_is_not_end_of_catalog(self):
        capture = {"pages": [page(self.names)]}
        capture["pages"][0]["result"]["nextCursor"] = None
        self.assertTrue(check_inventory(capture, CONTRACT)[0])

    def test_empty_string_cursor_is_opaque_and_followed(self):
        capture = {"pages": [page(self.names[:3], next_cursor=""), page(self.names[3:], cursor="")]}
        self.assertEqual(check_inventory(capture, CONTRACT)[0], [])

    def test_invalid_descriptor_fails(self):
        for field, value in (("name", ""), ("inputSchema", []), ("description", None)):
            capture = copy.deepcopy(self.capture)
            capture["pages"][0]["result"]["tools"][0][field] = value
            self.assertTrue(check_inventory(capture, CONTRACT)[0])


class SkillDiscoveryTests(unittest.TestCase):
    def test_each_skill_has_beta_dependency_and_operation_workflow(self):
        self.assertEqual(skills.validate(skills.ROOT), [])
        for name, spec in CONTRACT["skills"].items():
            root = skills.ROOT / "skills" / name
            self.assertEqual(skills.validate_dependency(root / "agents" / "openai.yaml"), [])
            text = (root / "SKILL.md").read_text()
            self.assertIn("## Tool discovery", text)
            self.assertIn("## Beta operation workflow", text)
            self.assertIn('"mode":"catalog"', text)
            self.assertIn('"mode":"describe"', text)
            self.assertIn('"mode":"query"', text)
            self.assertIn("optional_operations", spec)

    def test_unknown_operation_wrong_mapping_and_direct_call_are_rejected(self):
        name = "reviewing-project-tasks"
        source = (skills.ROOT / "skills" / name / "SKILL.md").read_text()
        spec = CONTRACT["skills"][name]
        supported = skills.supported_operation_mappings(CONTRACT)
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "SKILL.md"
            cases = (
                source + "\n| `get_unknown` | `ampliflow_tasks` | Unsupported |\n",
                source.replace("| `list_projects` | `ampliflow_projects` |", "| `list_projects` | `ampliflow_tasks` |"),
                source + "\nCall `list_projects`.\n",
            )
            for text in cases:
                path.write_text(text)
                errors = skills.validate_skill(path, name, spec, supported)
                self.assertTrue(any("operation" in error for error in errors), errors)

    def test_write_modes_and_commit_calls_are_rejected(self):
        name = "reviewing-checklists"
        source = (skills.ROOT / "skills" / name / "SKILL.md").read_text()
        spec = CONTRACT["skills"][name]
        supported = skills.supported_operation_mappings(CONTRACT)
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "SKILL.md"
            cases = (
                source + '\nCall `ampliflow_checklists` with `{"mode":"prepare","operation":"start_checklist","arguments":{}}`.\n',
                source + "\nCall `commit_ampliflow_change`.\n",
                source + "\nCall `commit_destructive_ampliflow_change`.\n",
            )
            for text in cases:
                path.write_text(text)
                errors = skills.validate_skill(path, name, spec, supported)
                self.assertTrue(any("write" in error or "commit" in error for error in errors), errors)

    def test_removed_beta_guidance_is_rejected(self):
        name = "reviewing-project-tasks"
        source = (skills.ROOT / "skills" / name / "SKILL.md").read_text()
        spec = CONTRACT["skills"][name]
        supported = skills.supported_operation_mappings(CONTRACT)
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text(source.replace('"mode":"describe"', '"mode":"catalog"', 1))
            errors = skills.validate_skill(path, name, spec, supported)
            self.assertTrue(any("describe mode" in error for error in errors))

    def test_missing_or_wrong_dependency_rejected(self):
        source = skills.ROOT / "skills" / "reviewing-project-tasks" / "agents" / "openai.yaml"
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "openai.yaml"
            path.write_text(source.read_text())
            self.assertEqual(skills.validate_dependency(path), [])
            path.write_text(source.read_text().replace("https://mcp.ampliflow.cc/mcp-beta", "https://wrong.example/mcp"))
            self.assertTrue(skills.validate_dependency(path))

    def test_package_version_marks_beta_contract(self):
        plugin = json.loads((skills.ROOT / "plugin.json").read_text())
        self.assertEqual(plugin["version"], "0.4.0")


if __name__ == "__main__":
    unittest.main()
