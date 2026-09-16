#!/usr/bin/env python3
"""Check a captured beta tools/list cursor chain against local skill dispatchers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_skills import CONTRACT_PATH, supported_operation_mappings

BETA_TOOL_LIMIT = 30
COMMIT_TOOLS = {"commit_ampliflow_change", "commit_destructive_ampliflow_change"}


def check_inventory(capture: object, contract: dict) -> tuple[list[str], dict]:
    errors: list[str] = []
    coverage: dict = {}
    if not isinstance(capture, dict) or not isinstance(capture.get("pages"), list) or not capture["pages"]:
        return ["capture must contain a nonempty pages array"], coverage

    names: set[str] = set()
    expected_cursor = None
    seen_cursors: set[str] = set()
    for index, page in enumerate(capture["pages"]):
        label = f"page {index + 1}"
        if index and expected_cursor is None:
            return [f"{label}: unexpected page after end of catalog"], coverage
        if not isinstance(page, dict):
            return [f"{label}: expected params and result objects"], coverage
        expected_params = {} if expected_cursor is None else {"cursor": expected_cursor}
        if page.get("params") != expected_params:
            return [f"{label}: cursor does not match preceding nextCursor"], coverage
        result = page.get("result")
        if "error" in page or not isinstance(result, dict) or not isinstance(result.get("tools"), list):
            return [f"{label}: missing tools/list result or request failed"], coverage
        for descriptor in result["tools"]:
            if not isinstance(descriptor, dict):
                return [f"{label}: invalid tool descriptor"], coverage
            name = descriptor.get("name")
            if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9_.-]{1,128}", name):
                return [f"{label}: invalid tool name"], coverage
            if name in names:
                return [f"{label}: duplicate tool name; recapture a stable catalog"], coverage
            if not isinstance(descriptor.get("description"), str) or not descriptor["description"].strip():
                return [f"{label}: missing tool description"], coverage
            schema = descriptor.get("inputSchema")
            if not isinstance(schema, dict) or schema.get("type") != "object":
                return [f"{label}: missing object inputSchema"], coverage
            names.add(name)
        expected_cursor = result.get("nextCursor")
        if "nextCursor" in result:
            if not isinstance(expected_cursor, str) or expected_cursor in seen_cursors:
                return [f"{label}: invalid or repeated nextCursor"], coverage
            seen_cursors.add(expected_cursor)

    if expected_cursor is not None:
        errors.append("incomplete catalog: nextCursor requires another page")
    if len(names) > BETA_TOOL_LIMIT:
        errors.append(f"beta catalog exceeds the {BETA_TOOL_LIMIT}-tool limit: {len(names)} tools")

    operation_ids = set(supported_operation_mappings(contract))
    exposed_operations = sorted(names & operation_ids)
    if exposed_operations:
        errors.append(f"beta catalog exposes operation IDs as top-level tools: {', '.join(exposed_operations)}")
    unexpected = sorted(name for name in names if not name.startswith("ampliflow_") and name not in COMMIT_TOOLS)
    if unexpected:
        errors.append(f"beta catalog contains unexpected top-level tools: {', '.join(unexpected)}")

    for name, spec in contract["skills"].items():
        required_operations = spec.get("required_operations", {})
        optional_operations = spec.get("optional_operations", {})
        required_dispatchers = set(required_operations.values()) | set(spec.get("required_dispatchers", []))
        optional_dispatchers = (
            set(optional_operations.values()) | set(spec.get("optional_dispatchers", []))
        ) - required_dispatchers
        missing_required = sorted(required_dispatchers - names)
        coverage[name] = {
            "missing_required_dispatchers": missing_required,
            "missing_optional_dispatchers": sorted(optional_dispatchers - names),
            "operations_require_runtime_catalog": sorted(set(required_operations) | set(optional_operations)),
        }
        if missing_required:
            errors.append(f"{name}: missing required dispatchers: {', '.join(missing_required)}")
    return errors, coverage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path, help="beta tools/list pages with request params and response result")
    args = parser.parse_args()
    try:
        capture = json.loads(args.capture.read_text(encoding="utf-8"))
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        print("ERROR: cannot read capture or contract as JSON")
        return 1
    errors, coverage = check_inventory(capture, contract)
    for name, result in coverage.items():
        optional = result["missing_optional_dispatchers"]
        if optional:
            print(f"{name}: optional dispatchers not captured: {', '.join(optional)}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("Captured beta catalog covers the skills' top-level dispatchers. Optional gaps are listed above.")
    print("This does not prove operation catalog coverage, schemas, callability, authorization, or read-only behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
