# AmpliFlow for ChatGPT

> [!NOTE]
> **MCP endpoint**
> Version `0.8.0` targets `https://mcp.ampliflow.com/mcp`. Hosted MCP 14.2.4 is deployed and qualified on the normal resource. Fresh Desktop acceptance remains pending; hosted checks do not prove client installation or behavior. Standalone MCP clients do not receive the bundled skills.

Use AmpliFlow from ChatGPT Desktop in **Work** mode. The imported plugin connects to AmpliFlow's hosted MCP server and adds one general router for reads and explicit user-confirmed changes plus six read-only review skills for project tasks, project portfolios, goals, risks and controls, improvements, and checklists.

> [!IMPORTANT]
> **Desktop mode matters**
> Select **Work** before starting the conversation. The GitHub-imported plugin does not expose its MCP tools in **Chat** mode. Chat may still show `@AmpliFlow`, but the cloud conversation cannot call the locally loaded tools.

The published `0.7.0` beta artifact remains available for internal tests and rollback. It targets the separate `.cc` beta origin; do not rewrite that artifact or silently fall back to it. Moving to the normal origin requires fresh resource-bound OAuth; beta authorization cannot be reused or transformed.

## Install the desktop pilot

Use the published `0.8.0` package. GitHub publication does not automatically sync a workspace marketplace or update an existing installation.

A workspace admin imports this repository:

1. Open **Admin > Plugins > Add > Import marketplace**.
2. Set **Source** to `https://github.com/AmpliFlow/af-chatgpt`.
3. Leave **Path** empty and import the marketplace.
4. Make **AmpliFlow pilot** available to the intended users.

See OpenAI's [marketplace import guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github) for current ChatGPT workspace administration steps.

Each pilot user then:

1. Installs **AmpliFlow** from the Plugins Directory in ChatGPT Desktop.
2. Completes AmpliFlow authentication when prompted.
3. Restarts ChatGPT Desktop after the first installation or an update.
4. Selects **Work** at the top of the new-conversation screen.
5. Adds `@AmpliFlow` and asks, for example: `What projects do I have?`

A successful request calls a compact feature tool such as `ampliflow_projects`. Reads use `catalog`, `describe`, then `query`. For an explicit change request, the general router reads the current state, shows the exact proposal, waits for confirmation, calls `prepare`, commits the unchanged approval receipt with the tool matching the server's safety class, then reads the target back.

See the package [setup guide](plugins/ampliflow/README.md), [acceptance checks](plugins/ampliflow/TESTING.md), and [discovery guide](plugins/ampliflow/DISCOVERY.md).

## Supported surface

| Surface | Pilot status |
| --- | --- |
| ChatGPT Desktop, **Work** mode | Supported pilot path; marketplace import verified for package `0.5.0`; `0.8.0` changes the MCP resource; fresh normal-origin acceptance remains pending |
| ChatGPT Desktop, **Chat** mode | Not supported by the GitHub-imported package; the cloud conversation does not receive its local MCP tools |
| ChatGPT web and mobile | Requires OpenAI's **With MCP** submission and review |

The package connects only to `https://mcp.ampliflow.com/mcp`. It does not add another MCP connection, use an alternate endpoint, depend on a workspace app ID, or install the AmpliFlow CLI.

The general skill supports only explicit user-confirmed writes discovered through the live catalog. Its six focused review skills remain read-only. Improvement creation and grading changes require the native persisted-score read-back, not generic improvement detail. Identity reads preserve unknown tenant binding and distinguish the effective credential principal from original-executor and write-attribution evidence. These separate reads prove neither an atomic snapshot nor human approval. The server remains authoritative for availability, authorization, target preconditions, safety class, plan expiry, and read-back behavior.

## Troubleshooting

- **`@AmpliFlow` is visible, but the answer says no tools are available:** start a new conversation in **Work**, not Chat.
- **Authentication is requested:** complete OAuth for the exact normal resource. Coordinate any required restart with the owner; do not interrupt an active client.
- **A required dispatcher or operation is missing:** report the unavailable workflow. Do not add another MCP server or fall back to another endpoint.
- **The version is current but the MCP URL is still beta, or two sources own the same server name:** inspect the workspace's actual connection, preserve the working client and obtain approval for the selected migration. Do not uninstall or reset it solely from the version label. See [MCP deployment and channel diagnosis](docs/mcp-deployment.md).

## Repository ownership

- **This repository:** plugin manifests, marketplace catalog, skills, icon, tests, and pilot documentation.
- **[af-cli](https://github.com/AmpliFlow/af-cli):** public CLI releases and installer.
- Hosted MCP implementation and deployment are maintained separately from this public package. See [MCP servers and deployment](docs/mcp-deployment.md) for production/beta URLs, OAuth boundaries, deployment ownership, promotion/recovery and current acceptance limits.

Package changes require a version bump and the checks in [plugins/ampliflow/TESTING.md](plugins/ampliflow/TESTING.md). Keep credentials, tenant records, screenshots, `.af/`, and other local runtime state out of Git.

## Public distribution

Use [SUBMIT.md](SUBMIT.md) to prepare the complete plugin ZIP and track remaining reviewer access, video, country, policy, and portal decisions. The kit keeps all seven skills and five positive plus three negative reviewer cases. It does not claim live acceptance or policy approval. [RELEASE.md](RELEASE.md) covers the coordinated GitHub/Desktop delivery; a release does not authorize public-store submission.

The GitHub marketplace remains a Desktop pilot route, not a public ChatGPT listing. Public distribution uses OpenAI's **With MCP** review.

## License

Copyright (c) 2026 Cognit Consulting AB, trading as AmpliFlow. All rights reserved. See [LICENSE](LICENSE). Confirm package-use terms before broad customer distribution.
