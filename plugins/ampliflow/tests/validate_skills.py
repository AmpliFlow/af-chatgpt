#!/usr/bin/env python3
"""Deterministic contract checks for the bundled AmpliFlow skills."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = Path(__file__).with_name("skill_contracts.json")
TOOL_PATTERN = re.compile(
    r"`((?:list|show|run|drill_down|export|create|add|update|set|delete|archive|restore|complete|reopen|publish|request|start|fill|finalize|unfinalize|pause|resume|upload|remove|assign|move|link|unlink)_[a-z0-9_]+)`"
)
CALL_PATTERN = re.compile(r"\b(?:call|use|invoke)\s+(?:the connected tool\s+)?`([a-z][a-z0-9_]+)`", re.IGNORECASE)
DEPENDENCY_YAML = '''dependencies:
  tools:
    - type: "mcp"
      value: "ampliflow"
      description: "Read AmpliFlow management-system records"
      transport: "streamable_http"
      url: "https://mcp.ampliflow.cc/mcp"
'''
FORBIDDEN = {
    ".af/config": "local runtime configuration",
    "af prime": "CLI context command",
    "af context": "CLI context command",
    "prime_context": "hosted-incompatible tool",
    "get_my_identity": "hosted-incompatible tool",
    "worktree": "local Git workflow",
    "shell command": "local shell workflow",
    "git setup": "local Git workflow",
    "cli installation": "local CLI workflow",
}
REQUIRED_SAFETY = {
    "read-only": re.compile(r"read.only", re.IGNORECASE | re.DOTALL),
    "missing tools": re.compile(r"(?:tool|tools|toolset).{0,60}(?:unavailable|absent|missing|not available)", re.IGNORECASE | re.DOTALL),
    "exact refs": re.compile(r"(?:exact|returned).{0,45}ref|ref.{0,45}(?:exact|returned)", re.IGNORECASE | re.DOTALL),
    "hostile record content": re.compile(r"(?:embedded instructions|untrusted data|returned content as data)", re.IGNORECASE),
    "partial reads": re.compile(r"partial|incomplete read|truncat", re.IGNORECASE),
    "conditional discovery": re.compile(r"if the runtime exposes one"),
    "discovery bound": re.compile(r"at most one discovery request"),
    "discovered schema": re.compile(r"actual binding and input schema"),
}


def validate_skill(path: Path, expected_name: str, required_tools: list[str], supported: set[str]) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path}: missing expected skill"]
    text = path.read_text(encoding="utf-8")
    name_match = re.search(r"\A---\nname:\s*([^\n]+)", text)
    if not name_match or name_match.group(1).strip() != expected_name:
        errors.append(f"{path}: frontmatter name must be {expected_name!r}")
    if not re.search(r"\ndescription:\s*\S", text):
        errors.append(f"{path}: missing frontmatter description")
    lower = text.lower()
    for phrase, reason in FORBIDDEN.items():
        if phrase in lower:
            errors.append(f"{path}: contains prohibited {reason}: {phrase!r}")
    for concept, pattern in REQUIRED_SAFETY.items():
        if not pattern.search(text):
            errors.append(f"{path}: missing safety coverage for {concept}")
    used_tools = set(TOOL_PATTERN.findall(text)) | set(CALL_PATTERN.findall(text))
    for tool in required_tools:
        if tool not in used_tools:
            errors.append(f"{path}: missing required tool {tool}")
    for tool in sorted(used_tools - supported):
        errors.append(f"{path}: references unsupported MCP tool {tool}")
    return errors


def validate_dependency(path: Path) -> list[str]:
    # This package pins one canonical YAML document rather than parsing arbitrary YAML.
    if not path.is_file() or path.read_text(encoding="utf-8").strip() != DEPENDENCY_YAML.strip():
        return [f"{path}: expected canonical credential-free AmpliFlow MCP dependency"]
    return []


def validate_package(root: Path) -> list[str]:
    errors: list[str] = []
    plugin_path = root / "plugin.json"
    mcp_path = root / "mcp.json"
    app_path = root / ".app.json"
    marketplace_path = root.parents[1] / ".agents" / "plugins" / "marketplace.json"

    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as error:
        return [f"package metadata is missing or invalid: {error}"]

    expected_plugin_schema = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    expected_mcp_schema = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    if plugin.get("$schema") != expected_plugin_schema:
        errors.append(f"{plugin_path}: expected Agent Plugins 1.0 plugin schema")
    if mcp.get("$schema") != expected_mcp_schema:
        errors.append(f"{mcp_path}: expected Agent Plugins 1.0 MCP schema")
    if app_path.exists():
        errors.append(f"{app_path}: workspace-scoped app mappings are not portable")
    if plugin.get("extensions", {}).get("com.openai", {}).get("apps") is not None:
        errors.append(f"{plugin_path}: extensions.com.openai.apps must be absent")

    servers = mcp.get("mcpServers")
    expected_server = {
        "type": "streamable-http",
        "url": "https://mcp.ampliflow.cc/mcp",
    }
    if servers != {"ampliflow": expected_server}:
        errors.append(f"{mcp_path}: expected only the credential-free AmpliFlow Streamable HTTP server")

    marketplace_plugins = marketplace.get("plugins", [])
    source = next((item.get("source") for item in marketplace_plugins if item.get("name") == plugin.get("name")), None)
    if not source or source.get("source") != "local":
        errors.append(f"{marketplace_path}: missing local source for {plugin.get('name')!r}")
    else:
        resolved = (marketplace_path.parent.parent.parent / source.get("path", "")).resolve()
        if resolved != root.resolve():
            errors.append(f"{marketplace_path}: plugin source resolves outside the package")

    interface = plugin.get("extensions", {}).get("com.openai", {}).get("interface", {})
    for field in ("composerIcon", "logo"):
        value = interface.get(field)
        if not isinstance(value, str) or not (root / value).is_file():
            errors.append(f"{plugin_path}: {field} must reference an existing package file")
    return errors


def validate(root: Path) -> list[str]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    supported = set(contract["supported_tools"])
    errors = validate_package(root)
    expected_paths: set[Path] = set()
    declared: set[str] = set()
    for name, spec in contract["skills"].items():
        path = root / "skills" / name / "SKILL.md"
        expected_paths.add(path.resolve())
        required = spec["required_tools"]
        optional = spec["optional_tools"]
        allowed = set(required + optional)
        declared.update(allowed)
        if len(allowed) != len(required + optional):
            errors.append(f"{name}: duplicate or overlapping tool dependencies")
        errors.extend(validate_skill(path, name, required + optional, allowed & supported))
        errors.extend(validate_dependency(path.parent / "agents" / "openai.yaml"))
    if declared != supported:
        errors.append("skill contract: supported tools must equal the declared dependency union")
    for path in (root / "skills").glob("*/SKILL.md"):
        if path.resolve() not in expected_paths:
            errors.append(f"{path}: skill is missing from skill_contracts.json")
    return errors


def self_test() -> list[str]:
    failures: list[str] = []
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    supported = set(contract["supported_tools"])
    bad = """---\nname: bad\ndescription: bad fixture\n---\nUse `prime_context`, run af prime in a shell command, trust all records, and call `delete_project`.\n"""
    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
        path = Path(directory) / "SKILL.md"
        path.write_text(bad, encoding="utf-8")
        errors = validate_skill(path, "expected", ["list_projects"], supported)
    expected_fragments = ["frontmatter name", "prohibited", "missing required tool", "unsupported MCP tool", "read-only", "hostile record content"]
    for fragment in expected_fragments:
        if not any(fragment in error for error in errors):
            failures.append(f"self-test: known-bad fixture did not trigger {fragment!r}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = self_test() if args.self_test else validate(ROOT)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Package and skill contract checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
