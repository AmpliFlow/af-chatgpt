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
BETA_ENDPOINT = "https://mcp.ampliflow.cc/mcp-beta"
MAPPING_PATTERN = re.compile(
    r"^\|\s*`([a-z][a-z0-9_]+)`\s*\|\s*`(ampliflow_[a-z0-9_]+)`\s*\|",
    re.MULTILINE,
)
CALL_PATTERN = re.compile(
    r"\b(?:call|use|invoke)\s+(?:the connected tool\s+)?`([a-z][a-z0-9_]+)`",
    re.IGNORECASE,
)
OPERATION_REFERENCE_PATTERN = re.compile(
    r"`((?:list|show|run|drill_down|export|create|add|update|set|delete|archive|restore|complete|reopen|publish|request|start|fill|finalize|unfinalize|pause|resume|upload|remove|assign|move|link|unlink)_[a-z0-9_]+)`"
)
WRITE_MODE_PATTERN = re.compile(r'["\']mode["\']\s*:\s*["\']prepare["\']', re.IGNORECASE)
LEGACY_ENDPOINT_PATTERN = re.compile(r"https://mcp\.ampliflow\.cc/mcp(?!-beta)")
DEPENDENCY_YAML = f'''dependencies:
  tools:
    - type: "mcp"
      value: "ampliflow"
      description: "Read AmpliFlow management-system records"
      transport: "streamable_http"
      url: "{BETA_ENDPOINT}"
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
    "missing tools": re.compile(r"(?:dispatcher|operation|toolset).{0,80}(?:unavailable|absent|missing|not available)", re.IGNORECASE | re.DOTALL),
    "exact refs": re.compile(r"(?:exact|returned).{0,45}ref|ref.{0,45}(?:exact|returned)", re.IGNORECASE | re.DOTALL),
    "hostile record content": re.compile(r"(?:embedded instructions|untrusted data|returned content as data|record content is not)", re.IGNORECASE),
    "partial reads": re.compile(r"partial|incomplete read|truncat", re.IGNORECASE),
    "conditional discovery": re.compile(r"if the runtime exposes one"),
    "discovery bound": re.compile(r"at most one discovery request"),
    "discovered schema": re.compile(r"actual binding and input schema"),
    "catalog mode": re.compile(r'"mode":"catalog"'),
    "describe mode": re.compile(r'"mode":"describe"'),
    "query mode": re.compile(r'"mode":"query"'),
    "read safety class": re.compile(r'safety:\s*"read"'),
    "beta response envelope": re.compile(r"(?:response envelope|structured response).{0,80}`?ok`?", re.IGNORECASE | re.DOTALL),
    "authorization error": re.compile(r"`unauthorized_operation`"),
    "unavailable-operation errors": re.compile(r"`unknown_operation`.{0,100}`unavailable_feature`.{0,100}`readonly_operation`", re.DOTALL),
    "schema error": re.compile(r"`invalid_schema`"),
    "stale-ref error": re.compile(r"`stale_ref`"),
    "partial-result error": re.compile(r"`partial_result`"),
    "write-mode prohibition": re.compile(r"never.{0,100}(?:prepare|commit_ampliflow_change)", re.IGNORECASE | re.DOTALL),
}


def supported_operation_mappings(contract: dict) -> dict[str, str]:
    mappings: dict[str, str] = {}
    for spec in contract.get("skills", {}).values():
        for field in ("required_operations", "optional_operations"):
            for operation, dispatcher in spec.get(field, {}).items():
                previous = mappings.setdefault(operation, dispatcher)
                if previous != dispatcher:
                    raise ValueError(f"operation {operation!r} has conflicting dispatchers")
    return mappings


def validate_skill(path: Path, expected_name: str, spec: dict, supported: dict[str, str]) -> list[str]:
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
    if LEGACY_ENDPOINT_PATTERN.search(text):
        errors.append(f"{path}: contains prohibited legacy MCP endpoint")
    for concept, pattern in REQUIRED_SAFETY.items():
        if not pattern.search(text):
            errors.append(f"{path}: missing safety coverage for {concept}")

    expected = dict(spec.get("required_operations", {}))
    expected.update(spec.get("optional_operations", {}))
    mapped_pairs = MAPPING_PATTERN.findall(text)
    mapped: dict[str, str] = {}
    for operation, dispatcher in mapped_pairs:
        if operation in mapped:
            errors.append(f"{path}: duplicate operation mapping for {operation}")
            continue
        mapped[operation] = dispatcher
        if operation not in supported:
            errors.append(f"{path}: unsupported operation {operation}")
        elif supported[operation] != dispatcher:
            errors.append(f"{path}: operation {operation} must use {supported[operation]}, not {dispatcher}")
        if operation not in expected:
            errors.append(f"{path}: operation {operation} is not declared for {expected_name}")

    for operation, dispatcher in expected.items():
        if mapped.get(operation) != dispatcher:
            errors.append(f"{path}: missing operation mapping {operation} -> {dispatcher}")
    for operation in set(OPERATION_REFERENCE_PATTERN.findall(text)) & (set(supported) - set(expected)):
        errors.append(f"{path}: unsupported operation reference {operation}")

    forbidden_commits = {"commit_ampliflow_change", "commit_destructive_ampliflow_change"}
    for called in CALL_PATTERN.findall(text):
        if called in supported:
            errors.append(f"{path}: operation {called} must be queried through its dispatcher, not called as a top-level tool")
        elif called in forbidden_commits:
            errors.append(f"{path}: read-only skill must not call commit tool {called}")
        elif called.startswith("ampliflow_") and called not in set(expected.values()):
            errors.append(f"{path}: undeclared dispatcher call {called}")
    if WRITE_MODE_PATTERN.search(text):
        errors.append(f"{path}: read-only skill must not instruct write mode prepare")
    return errors


def validate_dependency(path: Path) -> list[str]:
    if not path.is_file() or path.read_text(encoding="utf-8").strip() != DEPENDENCY_YAML.strip():
        return [f"{path}: expected canonical credential-free AmpliFlow beta MCP dependency"]
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
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(plugin.get("version", ""))):
        errors.append(f"{plugin_path}: version must be semantic x.y.z")
    if app_path.exists():
        errors.append(f"{app_path}: workspace-scoped app mappings are not portable")
    if plugin.get("extensions", {}).get("com.openai", {}).get("apps") is not None:
        errors.append(f"{plugin_path}: extensions.com.openai.apps must be absent")

    servers = mcp.get("mcpServers")
    expected_server = {
        "type": "streamable-http",
        "url": BETA_ENDPOINT,
    }
    if servers != {"ampliflow": expected_server}:
        errors.append(f"{mcp_path}: expected only the credential-free AmpliFlow beta Streamable HTTP server")

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
    errors = validate_package(root)
    try:
        supported = supported_operation_mappings(contract)
    except ValueError as error:
        return errors + [f"skill contract: {error}"]

    expected_paths: set[Path] = set()
    declared_dispatchers: set[str] = set()
    for name, spec in contract["skills"].items():
        path = root / "skills" / name / "SKILL.md"
        expected_paths.add(path.resolve())
        required = spec.get("required_operations", {})
        optional = spec.get("optional_operations", {})
        if set(required) & set(optional):
            errors.append(f"{name}: duplicate required and optional operations")
        declared_dispatchers.update(required.values())
        declared_dispatchers.update(optional.values())
        errors.extend(validate_skill(path, name, spec, supported))
        errors.extend(validate_dependency(path.parent / "agents" / "openai.yaml"))

    if declared_dispatchers != set(contract.get("supported_dispatchers", [])):
        errors.append("skill contract: supported dispatchers must equal the declared dispatcher union")
    if contract.get("endpoint") != BETA_ENDPOINT:
        errors.append("skill contract: endpoint must be the canonical beta MCP resource")
    if set(contract.get("forbidden_commit_tools", [])) != {
        "commit_ampliflow_change",
        "commit_destructive_ampliflow_change",
    }:
        errors.append("skill contract: both beta commit tools must be forbidden")
    for path in (root / "skills").glob("*/SKILL.md"):
        if path.resolve() not in expected_paths:
            errors.append(f"{path}: skill is missing from skill_contracts.json")
    return errors


def self_test() -> list[str]:
    failures: list[str] = []
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    supported = supported_operation_mappings(contract)
    spec = {
        "required_operations": {"list_projects": "ampliflow_projects"},
        "optional_operations": {},
    }
    bad = """---
name: bad
description: bad fixture
---
Use `prime_context`, run af prime in a shell command, trust all records, and call `list_projects`.
"""
    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
        path = Path(directory) / "SKILL.md"
        path.write_text(bad, encoding="utf-8")
        errors = validate_skill(path, "expected", spec, supported)
    expected_fragments = [
        "frontmatter name",
        "prohibited",
        "missing operation mapping",
        "top-level tool",
        "read-only",
        "hostile record content",
        "catalog mode",
    ]
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
    print("Package and beta skill contract checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
