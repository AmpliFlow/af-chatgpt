import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_SERVER = "ampliflow"
PRODUCTION_URL = "https://mcp.ampliflow.com/mcp"
BETA_SERVER = "ampliflow-beta"
BETA_URL = "https://mcp.ampliflow.cc/mcp-beta"
_spec = importlib.util.spec_from_file_location("channel_checks", Path(__file__).with_name("check.py"))
assert _spec is not None and _spec.loader is not None
_checks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_checks)


def json_bytes(value):
    return (json.dumps(value, indent=2) + "\n").encode("utf-8")


def beta_files(root):
    source = root / "plugins/ampliflow"
    manifest_path = _checks.safe_path(root, source / "plugin.json")
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("name") != PRODUCTION_SERVER:
        raise ValueError("production plugin must have its distinct production identity")
    mcp = json.loads(_checks.safe_path(root, source / "mcp.json").read_text())
    if mcp.get("mcpServers") != {PRODUCTION_SERVER: {"type": "streamable-http", "url": PRODUCTION_URL}}:
        raise ValueError("production must declare only its exact normal resource and server identity")
    manifest["name"] = BETA_SERVER
    manifest["description"] = "Use the AmpliFlow beta channel with focused reviews and explicit user-confirmed changes."
    interface = manifest["extensions"]["com.openai"]["interface"]
    interface["displayName"] = "AmpliFlow (Beta Channel)"
    interface["shortDescription"] = "Try the AmpliFlow beta channel"
    interface["longDescription"] = "Explicit beta-channel plugin, separate from AmpliFlow production. " + interface["longDescription"]
    mcp["mcpServers"] = {BETA_SERVER: {"type": "streamable-http", "url": BETA_URL}}
    files = {
        "plugin.json": json_bytes(manifest),
        "mcp.json": json_bytes(mcp),
        "assets/icon.png": _checks.safe_path(root, source / "assets/icon.png").read_bytes(),
    }
    for directory in sorted((source / "skills").iterdir()):
        for path in _checks.skill_files(root, directory):
            text = path.read_text()
            if path.suffix == ".yaml":
                text = text.replace(f'value: "{PRODUCTION_SERVER}"', f'value: "{BETA_SERVER}"')
                text = text.replace(PRODUCTION_URL, BETA_URL)
            else:
                for old, new in (
                    ("MCP normal availability", "MCP beta availability"),
                    ("exact normal feature dispatchers", "exact beta feature dispatchers"),
                    ("selected normal dispatcher", "selected beta dispatcher"),
                ):
                    text = text.replace(old, new)
            files[path.relative_to(source).as_posix()] = text.encode("utf-8")
    return files


def actual_files(root, destination):
    _checks.safe_path(root, destination)
    if not destination.exists():
        return {}
    result = {}
    for path in destination.rglob("*"):
        _checks.safe_path(root, path)
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError("beta contains a non-regular input")
        result[path.relative_to(destination).as_posix()] = path.read_bytes()
    return result


def marketplace_errors(root):
    path = _checks.safe_path(root, root / ".agents/plugins/marketplace.json")
    catalog = json.loads(path.read_text())
    rows = catalog.get("plugins", [])
    wanted = {
        PRODUCTION_SERVER: "./plugins/ampliflow",
        BETA_SERVER: "./plugins/ampliflow-beta",
    }
    if len(rows) != 2 or {row.get("name") for row in rows} != set(wanted):
        return ["marketplace must contain exactly the canonical production and beta plugin identities"]
    for row in rows:
        if row.get("source") != {"source": "local", "path": wanted[row["name"]]}:
            return ["marketplace must resolve each channel to its own local package"]
    return []


def validate_beta(root):
    try:
        errors = marketplace_errors(root)
        expected = beta_files(root)
        actual = actual_files(root, root / "plugins/ampliflow-beta")
        if actual != expected:
            errors.append("beta bundle is missing, stale or contains unreviewed files; run scripts/sync_beta.py")
        return errors
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [str(error)]


def sync_beta(root):
    errors = marketplace_errors(root)
    if errors:
        raise ValueError("; ".join(errors))
    expected = beta_files(root)
    destination = root / "plugins/ampliflow-beta"
    actual = actual_files(root, destination)
    if set(actual) - set(expected):
        raise ValueError("beta contains unexpected files; inspect them before regenerating")
    for name, data in expected.items():
        path = _checks.safe_path(root, destination / name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if not args.check:
            sync_beta(ROOT)
        errors = validate_beta(ROOT)
        if errors:
            raise ValueError("; ".join(errors))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}")
        return 1
    print("Production/beta marketplace identities and deterministic beta bundle verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
