import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def load_channels():
    spec = importlib.util.spec_from_file_location("sync_beta", ROOT / "scripts/sync_beta.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MarketplaceChannelTests(unittest.TestCase):
    def test_marketplace_has_production_and_legacy_beta_as_distinct_plugins(self):
        catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        entries = catalog["plugins"]
        self.assertEqual({entry["name"] for entry in entries}, {"ampliflow-production", "ampliflow"})
        self.assertEqual(len(entries), 2)
        actual = {}
        for entry in entries:
            package = ROOT / entry["source"]["path"]
            manifest = json.loads((package / "plugin.json").read_text())
            self.assertEqual(manifest["name"], entry["name"])
            self.assertEqual(entry["source"]["source"], "local")
            actual[entry["name"]] = (
                manifest["extensions"]["com.openai"]["interface"]["displayName"],
                json.loads((package / "mcp.json").read_text())["mcpServers"],
            )
        self.assertEqual(actual, {
            "ampliflow-production": ("AmpliFlow", {
                "ampliflow-production": {"type": "streamable-http", "url": "https://mcp.ampliflow.com/mcp"},
            }),
            "ampliflow": ("AmpliFlow (Beta Channel)", {
                "ampliflow": {"type": "streamable-http", "url": "https://mcp.ampliflow.cc/mcp-beta"},
            }),
        })

    def test_both_packages_bind_all_seven_skills_to_only_their_own_server(self):
        for directory, server, endpoint in (
            ("ampliflow", "ampliflow-production", "https://mcp.ampliflow.com/mcp"),
            ("ampliflow-beta", "ampliflow", "https://mcp.ampliflow.cc/mcp-beta"),
        ):
            package = ROOT / "plugins" / directory
            dependencies = list((package / "skills").glob("*/agents/openai.yaml"))
            self.assertEqual(len(dependencies), 7)
            for dependency in dependencies:
                with self.subTest(channel=directory, skill=dependency.parent.parent.name):
                    self.assertEqual(dependency.read_text(), f'''dependencies:
  tools:
    - type: "mcp"
      value: "{server}"
      description: "Read AmpliFlow management-system records"
      transport: "streamable_http"
      url: "{endpoint}"
''')

    def test_beta_projection_is_current_and_preserves_shared_workflow_text(self):
        self.assertEqual(load_channels().validate_beta(ROOT), [])
        source = ROOT / "plugins/ampliflow/skills"
        beta = ROOT / "plugins/ampliflow-beta/skills"
        replacements = (
            ("MCP normal availability", "MCP beta availability"),
            ("exact normal feature dispatchers", "exact beta feature dispatchers"),
            ("selected normal dispatcher", "selected beta dispatcher"),
        )
        for path in source.rglob("*.md"):
            expected = path.read_text()
            for old, new in replacements:
                expected = expected.replace(old, new)
            self.assertEqual((beta / path.relative_to(source)).read_text(), expected)

    def test_drift_wrong_resource_extra_files_and_symlinks_fail_without_rewriting(self):
        channels = load_channels()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "plugins", root / "plugins", ignore=shutil.ignore_patterns("tests"))
            shutil.copytree(ROOT / ".agents", root / ".agents")
            self.assertEqual(channels.validate_beta(root), [])
            beta = root / "plugins/ampliflow-beta"
            dependency = beta / "skills/using-ampliflow/agents/openai.yaml"
            original = dependency.read_bytes()
            dependency.write_text(dependency.read_text().replace("https://mcp.ampliflow.cc/mcp-beta", "https://mcp.ampliflow.com/mcp"))
            wrong = dependency.read_bytes()
            self.assertTrue(channels.validate_beta(root))
            self.assertEqual(dependency.read_bytes(), wrong)
            dependency.write_bytes(original)
            extra = beta / "unreviewed.md"
            extra.write_text("unexpected")
            self.assertTrue(channels.validate_beta(root))
            with self.assertRaises(ValueError):
                channels.sync_beta(root)
            extra.unlink()
            dependency.unlink()
            dependency.symlink_to(root / "plugins/ampliflow/skills/using-ampliflow/agents/openai.yaml")
            self.assertTrue(channels.validate_beta(root))


if __name__ == "__main__":
    unittest.main()
