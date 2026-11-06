# AmpliFlow for ChatGPT

Version `0.10.0` provides two separate plugins in this GitHub marketplace:

| Plugin | Plugin / MCP server identity | MCP resource |
| --- | --- | --- |
| **AmpliFlow** | `ampliflow` | `https://mcp.ampliflow.com/mcp` |
| **AmpliFlow (Beta Channel)** | `ampliflow-beta` | `https://mcp.ampliflow.cc/mcp-beta` |

These are the canonical channel names. Version `0.9.0` used `ampliflow-production` for production and `ampliflow` for beta; upgrading requires checking existing connections and may require fresh sign-in. Production must not inherit beta authorization. Each plugin contains the same seven reviewed skills and connects to only its own resource. Neither falls back to the other channel.

Hosted MCP 14.2.4 is deployed and qualified separately from this package. Marketplace synchronization, installation, exact-resource OAuth and supported-client acceptance are separate steps. A displayed version or successful beta read is not production-client proof.

## Import or update the marketplace

A workspace admin imports this repository:

1. Open **Admin > Plugins > Add > Import marketplace**.
2. Set **Source** to `https://github.com/AmpliFlow/af-chatgpt`.
3. Leave **Path** empty and import the marketplace, or select **Sync now** on the existing repository source.
4. Verify that the synchronized revision contains both **AmpliFlow** and **AmpliFlow (Beta Channel)**, then make the intended entries available to users.

See OpenAI's [marketplace import guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github) for current administration steps. GitHub publication alone does not prove a workspace has synchronized.

### Migrate existing connections

The marketplace ID `ampliflow-pilot` stays unchanged. Plugin/MCP identity `ampliflow` now means production, and `ampliflow-beta` means beta. Older installations may retain a beta binding under `ampliflow` even after synchronization. Inspect the actual MCP URL; do not run production workflows through an entry still bound to `.cc/mcp-beta`.

Install **AmpliFlow (Beta Channel)** under its new identity if beta is needed. Reconnect the affected production entry with fresh OAuth for exactly `https://mcp.ampliflow.com/mcp`. If its cached beta URL persists, retire that specific cached installation and reinstall the current production entry. Retire the old `ampliflow-production` entry after verifying the canonical production connection. Do not copy tokens, registrations, refs or prepared plans between the entries. Verify that the actual MCP URL matches the selected channel; the package version alone is insufficient. Coordinate any installation/update restart with the owner and use an idle client; do not interrupt active work. See [MCP servers and deployment](docs/mcp-deployment.md) for the channel and migration details.

## Use the desktop pilot

Select **Work** before starting a new ChatGPT Desktop conversation. Choose `@AmpliFlow` for production or **AmpliFlow (Beta Channel)** for beta, then ask, for example: `What projects do I have?`

The GitHub-imported plugin does not expose its MCP tools in **Chat** mode. A visible mention does not prove tools are mounted. Web and mobile require OpenAI's separate **With MCP** submission and review.

Both plugins provide one general router for reads and explicit user-confirmed changes, plus six read-only review skills for project tasks, portfolios, goals, risks and controls, improvements, and checklists. Standalone MCP clients do not receive these bundled skills.

Reads use `catalog`, `describe`, then `query`. For a change, the router reads current state, shows one exact proposal, waits for fresh confirmation, prepares it, commits the unchanged approval receipt through the safety-matched tool once, then reads the target back. Focused review skills never prepare or commit. Live server permissions, schemas, safety classes and preconditions remain authoritative.

See the [package setup guide](plugins/ampliflow/README.md), [acceptance checks](plugins/ampliflow/TESTING.md) and [discovery guide](plugins/ampliflow/DISCOVERY.md). Static tests and live-provider smoke tests do not establish fresh Desktop acceptance.

## Build and maintain the channels

`plugins/ampliflow` is the reviewed production source. `plugins/ampliflow-beta` is its deterministic beta projection, with the `ampliflow-beta` identity, beta resource and beta availability wording. Do not hand-edit the generated beta tree.

```sh
python3 -B scripts/sync_beta.py
python3 -B scripts/check.py
python3 -B scripts/build_submission.py
(cd dist && sha256sum -c SHA256SUMS)
```

Checks reject missing/extra marketplace entries, shared channel identities, stale beta files, wrong resources/dependencies and unsafe skill changes. Both ZIP downloads contain all seven skills. `ampliflow-plugin.zip` is the production submission draft; `ampliflow-beta-plugin.zip` is the explicit beta download, not a public-store upload.

Package changes require a version bump and the checks in [TESTING.md](plugins/ampliflow/TESTING.md). Keep credentials, tenant records, screenshots, `.af/` and local runtime state out of Git. Published `0.9.0` and earlier artifacts remain immutable; do not replace them with this build.

## Ownership and public distribution

- This repository owns the marketplace, plugin manifests, skills, icon, packaging, tests and client guidance.
- Hosted implementation and deployment have separate owners and approval boundaries; see [MCP servers and deployment](docs/mcp-deployment.md). This package change deploys no server.
- [RELEASE.md](RELEASE.md) covers GitHub publication. [SUBMIT.md](SUBMIT.md) covers the normal-only public-store draft and remaining reviewer, video, country, policy and portal requirements. GitHub publication does not authorize store submission or policy adoption.

## License

Copyright (c) 2026 Cognit Consulting AB, trading as AmpliFlow. All rights reserved. See [LICENSE](LICENSE). Confirm package-use terms before broad customer distribution.
