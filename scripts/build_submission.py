import argparse
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("submission_checks", Path(__file__).with_name("check.py"))
assert _spec is not None and _spec.loader is not None
_checks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_checks)

SKILLS = (
    "using-ampliflow", "reviewing-project-tasks", "reviewing-project-portfolio",
    "reviewing-risks-and-controls", "reviewing-checklists", "reviewing-goals", "reviewing-improvements",
)
OUTPUTS = {"ampliflow-plugin.zip", "SHA256SUMS", "build-report.json", "PORTAL-FIELDS.txt"}
URL_FIELDS = {
    "support_url": "supportURL", "privacy_policy_url": "privacyPolicyURL",
    "terms_of_service_url": "termsOfServiceURL",
}


def run_checks(root):
    subprocess.run([sys.executable, "-B", str(root / "scripts/check.py")], cwd=root, check=True)


def read_json(path):
    _checks.safe_path(Path(path.anchor), path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise ValueError("cannot read metadata JSON") from None
    if not isinstance(data, dict):
        raise TypeError("metadata JSON must contain an object")
    return data


def valid_url(value, field):
    if not isinstance(value, str):
        raise TypeError(f"{field} must be an HTTPS URL without credentials")
    try:
        url = urlsplit(value)
        valid = url.scheme == "https" and url.hostname and not url.username and not url.password
        valid = valid and len(value) <= 1024 and not any(c.isspace() or ord(c) < 32 for c in value)
        _ = url.port
    except ValueError:
        valid = False
    if not valid:
        raise ValueError(f"{field} must be an HTTPS URL without credentials")


def submission_manifest(root, answers_path):
    source = read_json(root / "plugins/ampliflow/plugin.json")
    source_version = source["version"]
    extension = source["extensions"]["com.openai"]
    interface = extension["interface"]
    interface["shortDescription"] = "Manage work in AmpliFlow"
    interface["websiteURL"] = "https://www.ampliflow.com"
    answers = read_json(answers_path.absolute() if answers_path else root / "submission/answers.example.json")
    if set(answers) - (set(URL_FIELDS) | {"demo_recording_url", "countries"}):
        raise ValueError("answers contain unsupported fields")
    missing = []
    for field, key in URL_FIELDS.items():
        interface.pop(key, None)
        value = answers.get(field)
        if value in (None, ""):
            missing.append(field)
        else:
            valid_url(value, field)
            interface[key] = value
    review_path = root / "submission/review.json"
    review = read_json(review_path) if review_path.exists() or review_path.is_symlink() else {}
    if set(review) - {"test_cases", "commerce", "commerce_description"}:
        raise ValueError("review contains unsupported fields; keep access credentials out of the package")
    cases = review.get("test_cases")
    if cases is None:
        missing.append("review.test_cases")
    else:
        if not isinstance(cases, dict) or set(cases) != {"positive", "negative"}:
            raise ValueError("review.test_cases must contain positive and negative lists")
        for kind, count in (("positive", 5), ("negative", 3)):
            rows = cases[kind]
            if not isinstance(rows, list) or len(rows) != count:
                raise ValueError(f"review requires exactly {count} {kind} cases")
            required = {"description", "prompt"} | ({"tools_triggered", "expected_behavior"} if kind == "positive" else set())
            allowed = required | {"tools_triggered", "expected_behavior", "file_attachment_urls", "expected_output_url"}
            for row in rows:
                if not isinstance(row, dict) or set(row) - allowed or any(not isinstance(row.get(key), str) or not row[key].strip() for key in required):
                    raise ValueError(f"invalid {kind} review case")
                if "expected_output_url" in row:
                    valid_url(row["expected_output_url"], "expected_output_url")
                attachments = row.get("file_attachment_urls", [])
                if not isinstance(attachments, list):
                    raise TypeError("review attachments must be a list")
                for url in attachments:
                    valid_url(url, "file_attachment_urls")
    demo = answers.get("demo_recording_url")
    if demo in (None, ""):
        missing.append("demo_recording_url")
    else:
        valid_url(demo, "demo_recording_url")
        review["demo_recording_url"] = demo
    publication = {"release_notes": "Target the normal AmpliFlow MCP resource; reconnect with fresh resource-bound OAuth. Preserve seven skills and existing operation and safety contracts. Desktop pilot package; fresh client acceptance and public-store approval remain separate."}
    countries = answers.get("countries")
    if countries in (None, [], ""):
        missing.append("countries")
    elif not isinstance(countries, list) or any(not isinstance(code, str) or not re.fullmatch(r"[A-Z]{2}", code) for code in countries):
        raise ValueError("countries must be a list of uppercase two-letter country codes")
    else:
        publication["countries"] = sorted(set(countries))
    if answers_path and missing:
        raise ValueError("answers are missing required fields: " + ", ".join(missing))
    extension["review"] = review
    extension["publication"] = publication
    return source, source_version, missing


def digest(data):
    return hashlib.sha256(data).hexdigest()


def portal_fields(manifest, archive_hash, missing):
    extension = manifest["extensions"]["com.openai"]
    interface = extension["interface"]
    publication = extension["publication"]
    review = extension["review"]
    lines = [
        "AmpliFlow OpenAI submission handoff",
        "NOT READY FOR SUBMISSION: owner approvals, live tests and portal checks remain.",
        "",
        "Upload ONLY ampliflow-plugin.zip at https://platform.openai.com/plugins",
        f"Package version: {manifest['version']}",
        f"ZIP SHA-256: {archive_hash}",
        "MCP server URL: https://mcp.ampliflow.com/mcp",
        "Authentication: OAuth, discovered from that exact MCP resource",
        "Missing package values: " + (", ".join(missing) if missing else "none"),
        "",
        "These listing values import from the ZIP. Compare them in Metadata & Skills.",
        "Change ZIP-managed fields in the source and rebuild, not in the portal.",
    ]
    for key in ("displayName", "shortDescription", "developerName", "category", "websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL", "longDescription"):
        lines.append(f"{key}: {interface.get(key, 'NOT SET')}")
    lines.extend([
        "Countries: " + (", ".join(publication.get("countries", [])) or "NOT CHOSEN"),
        "Video URL: " + review.get("demo_recording_url", "NOT PROVIDED"),
        "Release notes: " + publication["release_notes"],
        "Skills: all seven existing AmpliFlow skills and their supporting references",
        "Custom UI: none; no UI screenshots or CSP are declared by this package",
        "",
        "Reviewer credentials: enter only in secure Review details, never in this file or ZIP.",
        "Supply login URL, existing approved demo account, tenant and sign-in steps there.",
        "Do not reuse a customer account or disable production security.",
        "Domain verification: use ONLY the exact challenge token and URL from your draft.",
        "Policy text awaiting owner decision: submission/POLICY-APPROVAL.md in the repository.",
        "Test setup and expected results: submission/REVIEWER.md and submission/review.json in the repository.",
        "Local validation and prepared expected results are not live test passes.",
        "Run the five positive and three negative cases before attesting or submitting.",
        "OpenAI approval and Publish plugin are later actions, not part of this handoff.",
    ])
    return ("\n".join(lines) + "\n").encode("utf-8")


def build(root, output, answers_path=None):
    root, output = root.absolute(), output.absolute()
    _checks.safe_path(root, output)
    if output.resolve() != root.resolve() / "dist":
        raise ValueError("output must be the repository's dist directory, outside all inputs")
    removable = OUTPUTS | {"ampliflow-skills.zip"}
    if output.exists() and (not output.is_dir() or any(
        path.name not in removable or path.is_symlink() or not path.is_file() for path in output.iterdir()
    )):
        raise ValueError("dist contains unexpected files, directories, or symlinks")
    output.mkdir(exist_ok=True)
    for name in removable:
        (output / name).unlink(missing_ok=True)
    run_checks(root)
    manifest, source_version, missing = submission_manifest(root, answers_path)
    plugin_root = root / "plugins/ampliflow"
    inputs = [plugin_root / "mcp.json", plugin_root / "assets/icon.png"]
    for name in SKILLS:
        inputs.extend(_checks.skill_files(root, plugin_root / "skills" / name))
    members = {"plugin.json": (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")}
    for path in inputs:
        _checks.safe_path(root, path)
        members[path.relative_to(plugin_root).as_posix()] = path.read_bytes()
    members["LICENSE"] = _checks.safe_path(root, root / "LICENSE").read_bytes()
    members = dict(sorted(members.items()))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in members.items():
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    archive_data = buffer.getvalue()
    report = {
        "source_package_version": source_version,
        "package_version": source_version,
        "validation": "local validation only; not portal or runtime acceptance",
        "ready_for_submission": False,
        "status": "draft; human review, runtime evidence, and portal acceptance remain required",
        "missing_fields": missing,
        "checks": ["JSON, path, relative-link and PNG asset safety", "validate_skills self-test", "validate_skills", "unittest discovery", "submission metadata structure"],
        "skills": list(SKILLS),
        "adaptation": "Generated manifest only: public subtitle, website, review and publication metadata, and supplied answer URLs. Version comes from the source manifest. All seven skills and references remain byte-for-byte unchanged; Desktop sources are unchanged.",
        "allowlist": ["plugin.json (generated)", "mcp.json", "assets/icon.png", "skills/ (seven explicit skill directories)", "LICENSE"],
        "archive": {"name": "ampliflow-plugin.zip", "sha256": digest(archive_data)},
        "files": [{"path": name, "sha256": digest(data), "size": len(data)} for name, data in members.items()],
    }
    fields_data = portal_fields(manifest, digest(archive_data), missing)
    report["portal_fields_sha256"] = digest(fields_data)
    report_data = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    sums = f"{digest(archive_data)}  ampliflow-plugin.zip\n{digest(report_data)}  build-report.json\n{digest(fields_data)}  PORTAL-FIELDS.txt\n"
    for name, data in (("ampliflow-plugin.zip", archive_data), ("build-report.json", report_data), ("PORTAL-FIELDS.txt", fields_data), ("SHA256SUMS", sums.encode("ascii"))):
        (output / name).write_bytes(data)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--answers", type=Path)
    args = parser.parse_args()
    try:
        report = build(ROOT, ROOT / "dist", args.answers)
    except (OSError, TypeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Built draft dist/ampliflow-plugin.zip ({report['archive']['sha256']}); local validation only, not publication.")
    if report["missing_fields"]:
        print("Missing fields: " + ", ".join(report["missing_fields"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
