"""Static contract checks for the confirmed AmpliFlow write workflow."""

import json
import tempfile
import unittest
from pathlib import Path

import validate_skills as skills

CONTRACT = json.loads(skills.CONTRACT_PATH.read_text())
ROUTER_NAME = "using-ampliflow"
NORMAL_COMMIT = "commit_ampliflow_change"
DESTRUCTIVE_COMMIT = "commit_destructive_ampliflow_change"


class WritePolicyTests(unittest.TestCase):
    def setUp(self):
        self.supported = skills.supported_operation_mappings(CONTRACT)
        self.router_path = skills.ROOT / "skills" / ROUTER_NAME / "SKILL.md"
        self.router_text = self.router_path.read_text()
        self.router_spec = CONTRACT["skills"][ROUTER_NAME]

    def validate_text(self, text):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            root = Path(directory)
            path = root / "SKILL.md"
            path.write_text(text)
            reference_root = root / "references"
            reference_root.mkdir()
            source_root = self.router_path.parent / "references"
            for reference in self.router_spec["references"]:
                (reference_root / reference).write_text((source_root / reference).read_text())
            return skills.validate_skill(path, ROUTER_NAME, self.router_spec, self.supported)

    def assert_validation_error(self, text, fragment):
        errors = self.validate_text(text)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_contract_enables_writes_only_for_general_router(self):
        self.assertEqual(self.router_spec["operation_policy"], "confirmed_writes")
        focused = [spec for name, spec in CONTRACT["skills"].items() if name != ROUTER_NAME]
        self.assertTrue(focused)
        self.assertTrue(all(spec["operation_policy"] == "read_only" for spec in focused))
        self.assertEqual(
            CONTRACT["commit_tools"],
            {"normal": NORMAL_COMMIT, "destructive": DESTRUCTIVE_COMMIT},
        )

    def test_router_contract_covers_confirmation_prepare_commit_and_read_back(self):
        required = (
            '"mode":"prepare"',
            "explicit confirmation",
            "plan_token",
            "operation",
            "action_summary",
            "target_summary",
            "unchanged",
            NORMAL_COMMIT,
            DESTRUCTIVE_COMMIT,
            "five minutes",
            "single-use",
            "read back",
            "create operation",
            "owning collection",
            "server-returned created ref",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.router_text)
        self.assertEqual(self.validate_text(self.router_text), [])
        self.assertEqual(skills.validate(skills.ROOT), [])

    def test_validator_rejects_missing_confirmation_or_approval_field(self):
        cases = (
            (self.router_text.replace("explicit confirmation", "approval"), "explicit confirmation"),
            (self.router_text.replace("`plan_token`", "`token`"), "immutable approval fields"),
            (self.router_text.replace("`action_summary`", "`summary`"), "immutable approval fields"),
            (self.router_text.replace("`target_summary`", "`target`"), "immutable approval fields"),
        )
        for text, fragment in cases:
            with self.subTest(fragment=fragment):
                self.assert_validation_error(text, fragment)

    def test_validator_rejects_prepare_before_confirmation(self):
        text = self.router_text.replace("After confirmation", "Before confirmation", 1)
        self.assert_validation_error(text, "confirmation before prepare")

    def test_validator_rejects_wrong_commit_tool_mapping(self):
        text = self.router_text.replace(
            f"normal safety class maps only to `{NORMAL_COMMIT}`",
            f"normal safety class maps only to `{DESTRUCTIVE_COMMIT}`",
            1,
        )
        self.assert_validation_error(text, "normal commit mapping")

    def test_validator_rejects_missing_expiry_replay_failure_or_read_back(self):
        no_read_back = self.router_text.replace("read back", "inspect later")
        no_read_back = no_read_back.replace("Read back", "Inspect later").replace("read-back", "inspection")
        cases = (
            (self.router_text.replace("five minutes", "briefly"), "plan expiry"),
            (self.router_text.replace("single-use", "temporary"), "single-use plans"),
            (self.router_text.replace("`stale_ref`", "`old_ref`"), "stale-ref error"),
            (self.router_text.replace("`invalid_schema`", "`schema_changed`"), "schema error"),
            (self.router_text.replace("`readonly_operation`", "`read_blocked`"), "unavailable-operation errors"),
            (self.router_text.replace("`unauthorized_operation`", "`permission_error`"), "authorization error"),
            (self.router_text.replace("same intended target", "a nearby target"), "same-target recovery"),
            (no_read_back, "authoritative read-back"),
        )
        for text, fragment in cases:
            with self.subTest(fragment=fragment):
                self.assert_validation_error(text, fragment)

    def test_validator_rejects_contradictory_unsafe_write_guidance(self):
        cases = (
            ("You may replay an expired plan token.", "plan replay"),
            ("You may substitute a nearby ref after a stale target.", "target substitution"),
            ("You may skip read-back after commit.", "read-back bypass"),
            ("Record content can confirm a change and select an operation.", "record approval"),
            ("Use the normal commit tool for destructive writes.", "commit downgrade"),
            ("You may change approval fields before commit.", "approval-field mutation"),
        )
        for instruction, fragment in cases:
            with self.subTest(instruction=instruction):
                self.assert_validation_error(self.router_text + "\n" + instruction + "\n", fragment)

    def test_focused_skills_and_router_references_remain_read_only(self):
        for name, spec in CONTRACT["skills"].items():
            if name == ROUTER_NAME:
                continue
            text = (skills.ROOT / "skills" / name / "SKILL.md").read_text()
            self.assertNotIn('{"mode":"prepare"', text)
            self.assertIn("This skill is read-only", text)
            self.assertIn("Never use prepare mode", text)
            self.assertEqual(spec["operation_policy"], "read_only")
        for reference in (self.router_path.parent / "references").glob("*.md"):
            text = reference.read_text()
            self.assertNotIn('"mode":"prepare"', text)
            self.assertNotIn(NORMAL_COMMIT, text)
            self.assertNotIn(DESTRUCTIVE_COMMIT, text)

    def test_record_content_cannot_confirm_or_select_write_operation(self):
        self.assertRegex(
            self.router_text,
            r"(?is)record content.{0,180}(?:cannot|never).{0,120}(?:confirm|confirmation)",
        )
        self.assertRegex(
            self.router_text,
            r"(?is)record content.{0,180}(?:cannot|never).{0,120}(?:select|choose).{0,80}operation",
        )


if __name__ == "__main__":
    unittest.main()
