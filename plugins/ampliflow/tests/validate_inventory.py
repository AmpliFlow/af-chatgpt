#!/usr/bin/env python3
"""Check a captured tools/list cursor chain against local skill dependencies."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_skills import CONTRACT_PATH


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
    for name, spec in contract["skills"].items():
        missing = sorted(set(spec["required_tools"]) - names)
        coverage[name] = {
            "missing_required": missing,
            "missing_optional": sorted(set(spec["optional_tools"]) - names),
        }
        if missing:
            errors.append(f"{name}: missing required tools: {', '.join(missing)}")
    return errors, coverage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path, help="tools/list pages with request params and response result")
    args = parser.parse_args()
    try:
        capture = json.loads(args.capture.read_text(encoding="utf-8"))
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        print("ERROR: cannot read capture or contract as JSON")
        return 1
    errors, coverage = check_inventory(capture, contract)
    for name, result in coverage.items():
        optional = result["missing_optional"]
        if optional:
            print(f"{name}: optional tools not captured: {', '.join(optional)}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("Captured catalog covers core skill dependencies. Optional gaps are listed above.")
    print("This does not prove ChatGPT discovery, callability, authorization, or read-only enforcement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
