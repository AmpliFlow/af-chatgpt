# 0.10.1 improvement preflight guidance

Version `0.10.1` is a guidance patch. It retains the canonical production `ampliflow` and beta `ampliflow-beta` identities introduced in `0.10.0`, their display names, marketplace ID `ampliflow-pilot`, seven skills and exact MCP resources. No server/IaC deployment or migration is required by this patch.

## Release notes

- Read live grading options and required category detail before proposing improvement creation or grading changes. Look up the selected score's definition; a category label or guessed severity is not a scoring rule.
- Resolve required customer and user choices through authorized bounded reads before asking for IDs. Ask only for a genuinely unresolved choice or missing fact after those reads; do not invent placeholders or present an incomplete draft as confirmed.
- Do not require another confirmation for a bounded empty-catalog fallback. Existing discovery, authorization and capability-stop rules still apply.
- Preserve fresh explicit confirmation of each exact write proposal before prepare. Forward `plan_token`, `operation`, `action_summary` and `target_summary` unchanged, choose the commit tool by the returned safety class, commit once and read back authoritative state. Changed or expired plans need a new exact proposal and fresh confirmation; uncertain writes are never automatically retried. The six focused reviews remain read-only.

Published `0.10.0` and earlier releases remain immutable. Do not recreate their tags or replace their assets.

## Pre-release checks

Run deterministic checks and a bounded synthetic model comparison before publication, using an approved credential source and spending limit. Record source revisions, model, budgets, case coverage and failures. Synthetic model results do not prove Desktop workflows.

Existing client connectivity is verified across both aliases and channels; see [the acceptance status](submission/MCP-EVIDENCE.md). This patch changes no connection identity or resource. Preserve working authentication and active clients; verify candidate-specific workflows separately.

## Build and publish

After shared-source editing is complete:

```sh
python3 -B scripts/sync_beta.py
python3 -B scripts/build_submission.py
(cd dist && sha256sum -c SHA256SUMS)
```

The build runs the canonical production skill checks, beta projection check and unit suite. Confirm the intended new version is unpublished, commit the complete source and push the matching tag through the normal GitHub workflow. Verify exact-source CI before creating the release.

Publish all five generated assets: `ampliflow-plugin.zip`, `ampliflow-beta-plugin.zip`, `SHA256SUMS`, `build-report.json` and `PORTAL-FIELDS.txt`. Read back the release tag/source, curated body and each asset's downloaded bytes/checksum. The repository has no automatic release or store workflow. Only `ampliflow-plugin.zip` is the normal-resource public-store submission draft; the beta ZIP is a separate download.

## Candidate acceptance and remaining boundaries

Record exact candidate installation and supported-client cases separately: all six focused query-only workflows, router reads and confirmed writes, persisted grading/ownership fields, links, training semantics and failure recovery. Deterministic checks and synthetic model comparisons do not establish these Desktop results. Historical identity migration guidance is in [MCP servers and deployment](docs/mcp-deployment.md); it is not a new migration requirement for this patch.

Hosted MCP 14.2.4 production and beta delivery is already qualified. Follow [SUBMIT.md](SUBMIT.md) for public-store preparation. Package publication does not authorize recording/upload, policy adoption, countries, publisher attestations, store submission, tenant/account creation or production business-record changes. Keep pending client cases and authorization limits explicit.
