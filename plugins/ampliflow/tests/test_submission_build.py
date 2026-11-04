import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SubmissionBuildTests(unittest.TestCase):
    def setUp(self):
        self.build = load_script("build_submission")
        self.check = load_script("check")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "plugins", self.root / "plugins")
        shutil.copytree(ROOT / ".agents", self.root / ".agents")
        for name in ("README.md", "SUBMIT.md", "RELEASE.md", "LICENSE"):
            shutil.copyfile(ROOT / name, self.root / name)
        review = {"test_cases": {
            "positive": [{"description": "Synthetic read", "prompt": "Read records", "tools_triggered": "ampliflow_projects", "expected_behavior": "Read only"}] * 5,
            "negative": [{"description": "Synthetic boundary", "prompt": "Do not read"}] * 3,
        }}
        shutil.copytree(ROOT / "submission", self.root / "submission")
        (self.root / "submission/review.json").write_text(json.dumps(review))

    def build_bundle(self, answers=None):
        with mock.patch.object(self.build, "run_checks") as checks:
            report = self.build.build(self.root, self.root / "dist", answers)
            checks.assert_called_once_with(self.root)
        return report

    def test_deterministic_full_plugin_root_paths_and_unchanged_skills(self):
        (self.root / ".af").mkdir()
        (self.root / ".af/credentials").write_text("not for distribution")
        self.build_bundle()
        output = self.root / "dist"
        first = {p.name: p.read_bytes() for p in output.iterdir()}
        for path in (self.root / "plugins/ampliflow/skills").rglob("*.md"):
            path.touch()
        self.build_bundle()
        self.assertEqual(first, {p.name: p.read_bytes() for p in output.iterdir()})
        with zipfile.ZipFile(output / "ampliflow-plugin.zip") as archive:
            names = archive.namelist()
            self.assertEqual(names, sorted(names))
            expected_skills = {"using-ampliflow", "reviewing-project-tasks", "reviewing-project-portfolio", "reviewing-risks-and-controls", "reviewing-checklists", "reviewing-goals", "reviewing-improvements"}
            self.assertEqual({name.split("/")[1] for name in names if name.startswith("skills/")}, expected_skills)
            self.assertTrue({"plugin.json", "mcp.json", "assets/icon.png", "LICENSE"} <= set(names))
            self.assertFalse(any(name.startswith(("plugins/", "tests/", "submission/", ".")) for name in names))
            for name in names:
                if name != "plugin.json":
                    source = self.root / ("LICENSE" if name == "LICENSE" else f"plugins/ampliflow/{name}")
                    self.assertEqual(archive.read(name), source.read_bytes())
            plugin = json.loads(archive.read("plugin.json"))
            self.assertEqual(plugin["version"], "0.8.0")
            extension = plugin["extensions"]["com.openai"]
            self.assertEqual(extension["interface"]["shortDescription"], "Manage work in AmpliFlow")
            self.assertEqual(extension["interface"]["supportURL"], "https://www.ampliflow.com/support/")
            self.assertNotIn("countries", extension["publication"])
            self.assertNotIn("demo_recording_url", extension["review"])
            self.assertEqual(len(extension["review"]["test_cases"]["positive"]), 5)
            self.assertTrue(extension["publication"]["release_notes"])
        fields = first["PORTAL-FIELDS.txt"].decode()
        self.assertIn("Manage work in AmpliFlow", fields)
        self.assertIn("https://mcp.ampliflow.com/mcp", fields)
        self.assertIn("NOT READY FOR SUBMISSION", fields)
        self.assertIn("demo_recording_url, countries", fields)
        self.assertIn("Reviewer credentials: enter only in secure Review details", fields)
        report = json.loads(first["build-report.json"])
        source_version = json.loads((self.root / "plugins/ampliflow/plugin.json").read_text())["version"]
        self.assertEqual(report["source_package_version"], source_version)
        self.assertEqual(report["package_version"], "0.8.0")
        self.assertEqual(report["validation"], "local validation only; not portal or runtime acceptance")
        self.assertFalse(report["ready_for_submission"])
        self.assertEqual(report["missing_fields"], ["demo_recording_url", "countries"])
        for name in ("ampliflow-plugin.zip", "build-report.json", "PORTAL-FIELDS.txt"):
            digest = hashlib.sha256(first[name]).hexdigest()
            self.assertIn(f"{digest}  {name}\n", first["SHA256SUMS"].decode())
        self.assertEqual(report["archive"]["sha256"], hashlib.sha256(first["ampliflow-plugin.zip"]).hexdigest())

    def test_archive_and_portal_use_only_normal_resource(self):
        self.build_bundle()
        with zipfile.ZipFile(self.root / "dist/ampliflow-plugin.zip") as archive:
            mcp = json.loads(archive.read("mcp.json"))
            self.assertEqual(mcp["mcpServers"], {
                "ampliflow": {"type": "streamable-http", "url": "https://mcp.ampliflow.com/mcp"},
            })
            for name in archive.namelist():
                with self.subTest(member=name):
                    data = archive.read(name)
                    self.assertNotIn(b"mcp.ampliflow.cc", data)
                    self.assertNotIn(b"/mcp-beta", data)
        fields = (self.root / "dist/PORTAL-FIELDS.txt").read_text()
        self.assertIn("MCP server URL: https://mcp.ampliflow.com/mcp\n", fields)
        self.assertNotIn("mcp.ampliflow.cc", fields)

    def test_bundle_uses_source_release_version_without_an_independent_override(self):
        manifest = self.root / "plugins/ampliflow/plugin.json"
        data = json.loads(manifest.read_text())
        data["version"] = "9.8.7"
        manifest.write_text(json.dumps(data))
        report = self.build_bundle()
        self.assertEqual(report["package_version"], "9.8.7")
        with zipfile.ZipFile(self.root / "dist/ampliflow-plugin.zip") as archive:
            self.assertEqual(json.loads(archive.read("plugin.json"))["version"], "9.8.7")

    def test_private_answers_overlay_only_approved_fields_without_packaging_input(self):
        with tempfile.TemporaryDirectory() as private:
            answers = Path(private) / "answers.json"
            data = {"support_url": "https://example.com/support", "privacy_policy_url": "https://example.com/privacy", "terms_of_service_url": "https://example.com/terms", "demo_recording_url": "https://example.com/demo", "countries": ["SE"]}
            answers.write_text(json.dumps(data))
            report = self.build_bundle(answers)
            self.assertEqual(report["missing_fields"], [])
            self.assertFalse(report["ready_for_submission"])
            self.assertNotIn(private, json.dumps(report))
            fields = (self.root / "dist/PORTAL-FIELDS.txt").read_text()
            self.assertNotIn(private, fields)
            self.assertIn("Countries: SE", fields)
            self.assertIn("https://example.com/demo", fields)
            self.assertIn("NOT READY FOR SUBMISSION", fields)
            with zipfile.ZipFile(self.root / "dist/ampliflow-plugin.zip") as archive:
                plugin = json.loads(archive.read("plugin.json"))
                extension = plugin["extensions"]["com.openai"]
                self.assertEqual(extension["interface"]["websiteURL"], "https://www.ampliflow.com")
                self.assertEqual(extension["interface"]["supportURL"], data["support_url"])
                self.assertEqual(extension["review"]["demo_recording_url"], data["demo_recording_url"])
                self.assertEqual(extension["publication"]["countries"], ["SE"])
                self.assertFalse(any("answers" in name for name in archive.namelist()))

    def test_invalid_answers_are_rejected_without_echoing_values(self):
        path = self.root / "answers.json"
        for data in ({"support_url": "https://user:secret@example.com"}, {"demo_recording_url": "http://example.com"}, {"countries": ["se"]}, {"credentials": "private"}):
            path.write_text(json.dumps(data))
            with self.subTest(data=data), self.assertRaises(ValueError) as caught:
                self.build_bundle(path)
            self.assertNotIn("secret", str(caught.exception))
            self.assertNotIn("private", str(caught.exception))
            self.assertEqual(list((self.root / "dist").iterdir()), [])

    def test_supplied_answers_must_be_complete(self):
        path = self.root / "answers.json"
        path.write_text(json.dumps({"countries": []}))
        with self.assertRaisesRegex(ValueError, "missing"):
            self.build_bundle(path)
        self.assertEqual(list((self.root / "dist").iterdir()), [])

    def test_rejects_symlinks_sensitive_files_and_nested_output(self):
        skill = self.root / "plugins/ampliflow/skills/using-ampliflow"
        for relative in ("extra.md", "references"):
            path = skill / relative
            if path.exists():
                shutil.rmtree(path)
            path.symlink_to(self.root / "README.md")
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                self.build_bundle()
            path.unlink()
        for filename in (".env", "__pycache__", "credential.md"):
            path = skill / filename
            path.write_text("-----BEGIN RSA PRIVATE KEY-----")
            with self.subTest(filename=filename), self.assertRaises(ValueError):
                self.build_bundle()
            path.unlink()
        with mock.patch.object(self.build, "run_checks"), self.assertRaises(ValueError):
            self.build.build(self.root, skill / "dist")

    def test_failed_checks_remove_stale_outputs_and_do_not_build(self):
        output = self.root / "dist"
        output.mkdir()
        for name in ("ampliflow-plugin.zip", "build-report.json", "SHA256SUMS"):
            (output / name).write_text("stale")
        with mock.patch.object(self.build, "run_checks", side_effect=ValueError("failed check")), self.assertRaises(ValueError):
            self.build.build(self.root, output)
        self.assertEqual(list(output.iterdir()), [])

    def test_output_symlink_and_unexpected_artifacts_are_rejected(self):
        output = self.root / "dist"
        output.symlink_to(self.root / "plugins", target_is_directory=True)
        with self.assertRaises(ValueError):
            self.build.build(self.root, output)
        output.unlink()
        output.mkdir()
        (output / "tenant-records.json").write_text("{}")
        with self.assertRaises(ValueError):
            self.build.build(self.root, output)

    def test_check_detects_bad_json_missing_links_and_escaping_assets(self):
        self.assertEqual(self.check.validate_files(self.root), [])
        (self.root / "README.md").write_text("[missing](missing.md)\n")
        (self.root / "plugins/ampliflow/mcp.json").write_text("{")
        manifest = self.root / "plugins/ampliflow/plugin.json"
        data = json.loads(manifest.read_text())
        data["extensions"]["com.openai"]["interface"]["logo"] = "../../README.md"
        manifest.write_text(json.dumps(data))
        errors = self.check.validate_files(self.root)
        self.assertTrue(any("JSON" in error for error in errors), errors)
        self.assertTrue(any("link" in error for error in errors), errors)
        self.assertTrue(any("asset" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
