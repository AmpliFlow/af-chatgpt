"""Offline instruction contracts, not model or live-service acceptance."""

import json
import tempfile
import unittest
from pathlib import Path

import validate_skills as skills


class ImprovementGuidanceTests(unittest.TestCase):
    def test_package_has_bounded_identity_and_live_grading_guidance(self):
        self.assertEqual(skills.validate_improvement_guidance(skills.ROOT), [])

    def test_native_grading_read_has_reviewed_dispatcher_mapping(self):
        contract = json.loads(skills.CONTRACT_PATH.read_text())
        spec = contract["skills"]["reviewing-improvements"]
        self.assertEqual(spec["operation_policy"], "read_only")
        self.assertEqual(spec["required_operations"].get("show_improvement_gradings"), "ampliflow_improvements")
        self.assertIn("| `show_improvement_gradings` | `ampliflow_improvements` |", skills.IMPROVEMENT_GUIDANCE_PATH.read_text())

    def test_wrong_native_readback_dispatcher_is_rejected(self):
        contract = json.loads(skills.CONTRACT_PATH.read_text())
        source = skills.IMPROVEMENT_GUIDANCE_PATH.read_text()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text(source.replace(
                "| `show_improvement_gradings` | `ampliflow_improvements` |",
                "| `show_improvement_gradings` | `ampliflow_projects` |",
            ))
            errors = skills.validate_skill(path, "reviewing-improvements", contract["skills"]["reviewing-improvements"], skills.supported_operation_mappings(contract))
            self.assertTrue(any("show_improvement_gradings must use ampliflow_improvements" in error for error in errors), errors)

    def test_missing_persisted_grading_or_identity_evidence_is_rejected(self):
        paths = (
            "skills/reviewing-improvements/SKILL.md",
            "skills/using-ampliflow/SKILL.md",
            "skills/using-ampliflow/references/processes-risks-controls-and-improvements.md",
        )
        cases = {
            paths[0]: ("result.authenticated_identity", "original_executor_evidence", "write_attribution_evidence", "tenant_binding", "JWT/cookie", "automatically retry an uncertain identity read", "show_improvement_gradings", "selected but ungraded"),
            paths[1]: ("show_improvement_gradings",),
            paths[2]: ("show_improvement_gradings", "result.improvement_gradings", "impact_list", "separate_non_atomic_reads", "selected but ungraded", "Generic improvement detail", "mismatch", "same-tenant URL"),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in paths:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text((skills.ROOT / relative).read_text())
            self.assertEqual(skills.validate_improvement_guidance(root), [])
            for relative, concepts in cases.items():
                target = root / relative
                source = target.read_text()
                for concept in concepts:
                    with self.subTest(path=relative, concept=concept):
                        self.assertIn(concept, source)
                        target.write_text(source.replace(concept, "omitted"))
                        self.assertTrue(skills.validate_improvement_guidance(root))
                target.write_text(source)

    def test_harmless_heading_changes_do_not_change_contract(self):
        text = skills.IMPROVEMENT_GUIDANCE_PATH.read_text()
        self.assertEqual(skills.improvement_guidance_errors(text.replace("## My deviations and ownership", "## Personal records")), [])

    def test_missing_ownership_or_grading_rule_is_rejected(self):
        for concept in ("credential principal", "responsible_user_ids", "created_by_user_ids", "involved_user_ids", "AND", "deduplicate", "two pages", "five", "active", "distinct consequence", "not an API limit"):
            with self.subTest(concept=concept):
                text = skills.IMPROVEMENT_GUIDANCE_PATH.read_text()
                self.assertIn(concept, text)
                errors = skills.improvement_guidance_errors(text.replace(concept, "omitted"))
                self.assertTrue(errors, concept)


if __name__ == "__main__":
    unittest.main()
