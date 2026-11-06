# 0.9.0 production and beta plugins

Version `0.9.0` splits the GitHub marketplace into **AmpliFlow** for production and **AmpliFlow (Beta Channel)** for beta. This is a package/identity change; it does not deploy or modify the hosted MCP services.

## Release notes

- Add production plugin and MCP identity `ampliflow-production` at `https://mcp.ampliflow.com/mcp`.
- Retain legacy plugin and MCP identity `ampliflow` at its exact existing `https://mcp.ampliflow.cc/mcp-beta` resource, now explicitly labelled **AmpliFlow (Beta Channel)**. Preserve its working connection; production starts with fresh resource-bound OAuth.
- Keep the marketplace ID `ampliflow-pilot`. Each entry has its own local source root, MCP identity and seven skill dependencies, so installing production does not replace beta's server binding.
- Generate the beta bundle deterministically from reviewed shared skills. Checks reject stale files, extra connections, wrong resources and channel-identity collisions.
- Publish separate production and beta ZIP downloads. Only `ampliflow-plugin.zip` is the normal-resource public-store submission draft; `ampliflow-beta-plugin.zip` is explicitly beta.
- Preserve six focused read-only reviews, the general router's exact confirmation and immutable approval receipt, single-commit/read-back/recovery rules, native grading/ownership semantics, entity links and training-session guidance.

Published `0.8.0` and earlier releases remain immutable. Do not recreate their tags or replace their assets.

## Build and publish

```sh
python3 -B scripts/sync_beta.py
python3 -B scripts/build_submission.py
(cd dist && sha256sum -c SHA256SUMS)
```

The build runs the canonical production skill checks, beta projection check and unit suite. Confirm the intended new version is unpublished, commit the complete source and push the matching tag through the normal GitHub workflow. Verify exact-source CI before creating the release.

Publish all five generated assets: `ampliflow-plugin.zip`, `ampliflow-beta-plugin.zip`, `SHA256SUMS`, `build-report.json` and `PORTAL-FIELDS.txt`. Read back the release tag/source, curated body and each asset's downloaded bytes/checksum. The repository has no automatic release or store workflow.

## Workspace migration and acceptance

Sync the existing repository marketplace and verify both entries at the new revision. The legacy entry becomes explicitly beta without changing its identity or resource. Install the fresh production entry separately and complete OAuth for exactly `https://mcp.ampliflow.com/mcp`. Preserve active-client boundaries; no uninstall, reset, authentication copying or forced restart is part of this migration. See [MCP servers and deployment](docs/mcp-deployment.md).

Verify the actual MCP URL and server identity for each installed entry, then run supported-client acceptance in fresh Desktop **Work** conversations with the selected plugin. Record all six focused query-only workflows, router read and confirmed-write behavior, persisted grading/ownership fields, links, training semantics and failure recovery. Static checks, live-provider smoke with synthetic tool responses and SDK checks are separate evidence layers; none replaces fresh Desktop acceptance.

## Remaining boundaries

Hosted MCP 14.2.4 production and beta delivery is already qualified. This package change needs no new infrastructure work, server release or promotion. Existing deployment evidence and exact resource/issuer boundaries are in [the deployment guide](docs/mcp-deployment.md).

Follow [SUBMIT.md](SUBMIT.md) for public-store preparation. Package publication does not authorize recording/upload, policy adoption, countries, publisher attestations, store submission, tenant/account creation, or production business-record changes. Keep pending client cases and authorization limits explicit.
