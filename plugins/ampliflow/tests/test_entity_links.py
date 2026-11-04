"""Static instruction/package contracts, not model or Desktop execution proof."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import validate_skills as skills


REFERENCE = "entity-links.md"
REFERENCE_PATH = skills.ROOT / "skills/using-ampliflow/references" / REFERENCE


class EntityLinkGuidanceTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads(skills.CONTRACT_PATH.read_text())

    def test_all_seven_skills_default_to_links_and_load_shared_read_only_rules(self):
        self.assertEqual(len(self.contract["skills"]), 7)
        for name, spec in self.contract["skills"].items():
            with self.subTest(skill=name):
                text = (skills.ROOT / "skills" / name / "SKILL.md").read_text()
                self.assertRegex(text, r"(?i)default to readable Markdown entity links in lists, summaries, and follow-ups")
                self.assertIn("native UUIDs and required parent", text)
                target = "references/" if name == "using-ampliflow" else "../using-ampliflow/references/"
                self.assertIn(f"`{target}{REFERENCE}`", text)
                field = "required_operations" if name == "reviewing-improvements" else "optional_operations"
                self.assertEqual(spec[field].get("get_authenticated_identity"), "ampliflow_people")
                self.assertIn("| `get_authenticated_identity` | `ampliflow_people` |", text)
                self.assertEqual(spec["operation_policy"], "confirmed_writes" if name == "using-ampliflow" else "read_only")

    def test_frontend_evidence_discovery_and_fallback_boundaries(self):
        text = REFERENCE_PATH.read_text()
        for concept in (
            "get_authenticated_identity", "ampliflow_people", "catalog", "describe", 'safety: "read"',
            "result.authenticated_identity.frontend_context", "base_url", "origin_evidence", "entity_url_templates",
            "tenant_binding", "match", "unknown", "canonical-host proof", "same-origin SPA",
            "development/loopback", "base_url: null", "empty templates", "custom domains and ports",
            "Do not reconstruct", "MCP origin", "record content", "tenant switch", "Discard",
            "Reuse current", "Do not add authentication call loops", "JWT/cookie", "uncertain identity read",
            "missing evidence", "address already supplied", "unsupported", "Links grant no access",
            "read-only", "router", "no browser",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_template_ids_encoding_and_markdown_safety_are_explicit(self):
        text = REFERENCE_PATH.read_text()
        for key, placeholders in {
            "improvement": "{improvement_id}",
            "project": "{project_id}",
            "project_task": "{project_id}, {task_id}",
            "risk": "{risk_id}",
            "risk_register": "none",
            "process": "{process_id}",
            "subprocess": "{subprocess_id}",
            "process_chart": "none",
        }.items():
            with self.subTest(template=key):
                self.assertIn(f"| `{key}` | {placeholders} |", text)
        for concept in (
            "returned entity URL", "current connection confirms its origin", "exact returned absolute template",
            "native UUID", "cache-local refs", "improvement numbers", "required project UUID",
            "percent-encode each placeholder value", "Do not encode the whole URL", "double-encode",
            "backslashes", "brackets", "newlines", "angle brackets", "parentheses",
            "/improvements/{improvement_id}", "/projects/{project_id}/tasks/{task_id}",
            "/operational-risk-analysis", "risk_form", "/process/{process_id}",
            "/subprocess/{subprocess_id}", "/processchart", "not fallback templates",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_validator_enforces_exact_shared_reference_allowlist_and_read_only_boundary(self):
        spec = self.contract["skills"]["using-ampliflow"]
        self.assertIn(REFERENCE, spec["references"])
        supported = skills.supported_operation_mappings(self.contract)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "using-ampliflow"
            shutil.copytree(skills.ROOT / "skills/using-ampliflow", target)
            path = target / "SKILL.md"
            validate = lambda: skills.validate_skill(path, "using-ampliflow", spec, supported)
            self.assertEqual(validate(), [])
            reference = target / "references" / REFERENCE
            source = reference.read_text()
            reference.unlink()
            self.assertTrue(any("missing declared reference" in error for error in validate()))
            reference.write_text(source + '\n{"mode":"prepare"}\n')
            self.assertTrue(any("read-only reference must not instruct writes" in error for error in validate()))
            reference.write_text(source)
            (target / "references/unreviewed.md").write_text("Unexpected reference")
            self.assertTrue(any("exactly match" in error for error in validate()))
            (target / "references/unreviewed.md").unlink()
            path.write_text(path.read_text().replace("## Entity links", "## Links to records"))
            self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
