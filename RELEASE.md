# 0.10.0 canonical channel identities

Version `0.10.0` names the production plugin/MCP server `ampliflow` and beta `ampliflow-beta`. Display names remain **AmpliFlow** and **AmpliFlow (Beta Channel)**. This is a package/identity change; it does not deploy or modify the hosted MCP services.

## Release notes

- Rename production plugin/MCP identity from `ampliflow-production` to `ampliflow`, retaining `https://mcp.ampliflow.com/mcp`.
- Rename beta plugin/MCP identity from `ampliflow` to `ampliflow-beta`, retaining `https://mcp.ampliflow.cc/mcp-beta`.
- Keep marketplace ID `ampliflow-pilot`, separate source roots and seven channel-specific skill dependencies. Existing connections need migration: a cached `ampliflow` binding may still point to beta. Verify the actual URL and use fresh resource-bound authorization, never copied authentication.
- Generate the beta bundle deterministically from reviewed shared skills. Checks reject stale files, extra connections, wrong resources and channel-identity collisions.
- Publish separate production and beta ZIP downloads. Only `ampliflow-plugin.zip` is the normal-resource public-store submission draft; `ampliflow-beta-plugin.zip` is explicitly beta.
- Preserve six focused read-only reviews, the general router's exact confirmation and immutable approval receipt, single-commit/read-back/recovery rules, native grading/ownership semantics, entity links and training-session guidance.

Published `0.9.0` and earlier releases remain immutable. Do not recreate their tags or replace their assets.

## Build and publish

```sh
python3 -B scripts/sync_beta.py
python3 -B scripts/build_submission.py
(cd dist && sha256sum -c SHA256SUMS)
```

The build runs the canonical production skill checks, beta projection check and unit suite. Confirm the intended new version is unpublished, commit the complete source and push the matching tag through the normal GitHub workflow. Verify exact-source CI before creating the release.

Publish all five generated assets: `ampliflow-plugin.zip`, `ampliflow-beta-plugin.zip`, `SHA256SUMS`, `build-report.json` and `PORTAL-FIELDS.txt`. Read back the release tag/source, curated body and each asset's downloaded bytes/checksum. The repository has no automatic release or store workflow.

## Workspace migration and acceptance

Sync the repository marketplace and verify both canonical identities at the new revision. Install beta as `ampliflow-beta` if needed. Check the actual URL of `ampliflow`: if it retains the old beta binding, reconnect or retire that affected cached installation and reinstall production. Complete fresh OAuth for exactly `https://mcp.ampliflow.com/mcp`; do not use an entry still bound to beta for production work. Retire `ampliflow-production` after verifying the canonical production connection. This migration may require fresh sign-in, but does not authorize copying credentials, changing unrelated connections or interrupting active clients. See [MCP servers and deployment](docs/mcp-deployment.md).

Verify the actual MCP URL and server identity for each installed entry, then run supported-client acceptance in fresh Desktop **Work** conversations with the selected plugin. Record all six focused query-only workflows, router read and confirmed-write behavior, persisted grading/ownership fields, links, training semantics and failure recovery. Static checks, live-provider smoke with synthetic tool responses and SDK checks are separate evidence layers; none replaces fresh Desktop acceptance.

## Remaining boundaries

Hosted MCP 14.2.4 production and beta delivery is already qualified. This package change needs no new infrastructure work, server release or promotion. Existing deployment evidence and exact resource/issuer boundaries are in [the deployment guide](docs/mcp-deployment.md).

Follow [SUBMIT.md](SUBMIT.md) for public-store preparation. Package publication does not authorize recording/upload, policy adoption, countries, publisher attestations, store submission, tenant/account creation, or production business-record changes. Keep pending client cases and authorization limits explicit.
