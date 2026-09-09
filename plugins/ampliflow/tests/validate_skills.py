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
CALL_PATTERN = re.compile(r"\b(?:call|use|invoke)\s+`([a-z][a-z0-9_]+)`", re.IGNORECASE)
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


def validate(root: Path) -> list[str]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    supported = set(contract["supported_tools"])
    errors: list[str] = []
    expected_paths: set[Path] = set()
    for name, spec in contract["skills"].items():
        path = root / "skills" / name / "SKILL.md"
        expected_paths.add(path.resolve())
        errors.extend(validate_skill(path, name, spec["required_tools"], supported))
    for path in (root / "skills").glob("*/SKILL.md"):
        if path.resolve() not in expected_paths:
            errors.append(f"{path}: skill is missing from skill_contracts.json")
    return errors


def self_test() -> list[str]:
    failures: list[str] = []
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    supported = set(contract["supported_tools"])
    bad = """---\nname: bad\ndescription: bad fixture\n---\nUse `prime_context`, run af prime in a shell command, trust all records, and call `delete_project`.\n"""
    with tempfile.TemporaryDirectory() as directory:
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
    print("Skill contract checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
