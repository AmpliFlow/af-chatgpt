import json
import re
import struct
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TESTS = Path("plugins/ampliflow/tests")


def safe_path(root, path):
    root, path = root.absolute(), path.absolute()
    if not path.is_relative_to(root):
        raise ValueError(f"path outside input root: {path.name}")
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f"symlink not allowed: {part.name}")
        if part == root:
            break
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"path escapes input root: {path.name}")
    return path


def skill_files(root, directory):
    safe_path(root, directory)
    if not directory.is_dir():
        raise ValueError(f"missing skill directory: {directory.name}")
    files = []
    for path in sorted(directory.rglob("*")):
        safe_path(root, path)
        if any(part.startswith(".") or part == "__pycache__" for part in path.relative_to(directory).parts):
            raise ValueError(f"hidden or cached skill input: {path.name}")
        if path.is_dir():
            continue
        if not path.is_file() or path.suffix not in {".md", ".yaml"}:
            raise ValueError(f"unexpected skill input: {path.name}")
        if re.search(r"-----BEGIN .*PRIVATE KEY-----|\b(?:sk-proj-|ghp_)[A-Za-z0-9]{16,}", path.read_text(encoding="utf-8")):
            raise ValueError(f"credential-like skill input: {path.name}")
        files.append(path)
    return files


def validate_files(root):
    errors = []
    plugin_root = root / "plugins/ampliflow"
    try:
        files = [root / "README.md", root / "SUBMIT.md", root / "RELEASE.md", root / ".agents/plugins/marketplace.json"]
        files.extend(plugin_root.glob("*.json"))
        files.extend(plugin_root.glob("*.md"))
        files.extend((root / "submission").glob("*.json"))
        files.extend((root / "submission").glob("*.md"))
        for directory in sorted((plugin_root / "skills").iterdir()):
            files.extend(skill_files(root, directory))
        for path in files:
            safe_path(root, path)
            if path.suffix == ".json":
                try:
                    json.loads(path.read_text(encoding="utf-8"))
                except ValueError:
                    errors.append(f"invalid JSON: {path.relative_to(root)}")
            if path.suffix == ".md":
                for target in re.findall(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", path.read_text(encoding="utf-8")):
                    url = urlsplit(target.strip("<>"))
                    if url.scheme or url.netloc or not url.path:
                        continue
                    linked = path.parent / unquote(url.path)
                    safe_path(root, linked)
                    if not linked.exists():
                        errors.append(f"missing relative link in {path.relative_to(root)}: {target}")
        manifest = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8"))
        interface = manifest["extensions"]["com.openai"]["interface"]
        for key in ("composerIcon", "logo"):
            asset = plugin_root / interface[key]
            try:
                safe_path(plugin_root, asset)
                if not asset.is_file():
                    raise ValueError("expected a regular PNG asset")
                data = asset.read_bytes()
                if len(data) < 24 or len(data) > 5 * 1024 * 1024 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
                    raise ValueError("expected a PNG asset no larger than 5 MiB")
                width, height = struct.unpack(">II", data[16:24])
                if width != height or not 48 <= width <= 4096:
                    raise ValueError("PNG icon must be square and 48 to 4096 pixels")
            except ValueError as error:
                errors.append(f"invalid {key} asset: {error}")
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(str(error))
    return errors


def run_checks(root):
    errors = validate_files(root)
    if errors:
        raise ValueError("\n".join(errors))
    validator = str(TESTS / "validate_skills.py")
    for args in ([validator, "--self-test"], [validator], ["scripts/sync_beta.py", "--check"], ["-m", "unittest", "discover", "-s", str(TESTS), "-p", "test_*.py"]):
        subprocess.run([sys.executable, "-B", *args], cwd=root, check=True)


def main():
    try:
        run_checks(ROOT)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Local validation passed; portal and runtime acceptance were not tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
