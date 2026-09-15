# AmpliFlow for ChatGPT

Use AmpliFlow from ChatGPT Desktop in **Work** mode. The imported plugin connects to AmpliFlow's hosted MCP server and adds six focused, read-only review skills for project tasks, project portfolios, goals, risks and controls, improvements, and checklists.

> **Desktop mode matters:** select **Work** before starting the conversation. The GitHub-imported plugin does not expose its MCP tools in **Chat** mode. Chat may still show `@AmpliFlow`, but the cloud conversation cannot call the locally loaded tools.

## Install the desktop pilot

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

A successful request calls a compact feature tool such as `ampliflow_projects`. The skill discovers the required read operation with `catalog`, reads its schema with `describe`, and executes it with `query`.

See the package [setup guide](plugins/ampliflow/README.md), [acceptance checks](plugins/ampliflow/TESTING.md), and [discovery guide](plugins/ampliflow/DISCOVERY.md).

## Supported surface

| Surface | Pilot status |
| --- | --- |
| ChatGPT Desktop, **Work** mode | Supported and verified with package `0.4.2` |
| ChatGPT Desktop, **Chat** mode | Not supported by the GitHub-imported package; the cloud conversation does not receive its local MCP tools |
| ChatGPT web and mobile | Requires OpenAI's **With MCP** submission and review |

The package connects only to `https://mcp.ampliflow.cc/mcp-beta`. It does not add another MCP connection, use an alternate endpoint, depend on a workspace app ID, or install the AmpliFlow CLI.

The six bundled skills use read operations only. This is an instruction-level limit, not a server permission boundary: the connected server may expose other approved tools under the user's AmpliFlow permissions.

## Troubleshooting

- **`@AmpliFlow` is visible, but the answer says no tools are available:** start a new conversation in **Work**, not Chat.
- **Authentication is requested:** complete OAuth for the exact beta resource, then restart Desktop and open a new Work conversation.
- **A required dispatcher or operation is missing:** report the unavailable workflow. Do not add another MCP server or fall back to another endpoint.
- **An old AmpliFlow pilot source is also installed:** remove the obsolete source so only the current workspace installation owns the `ampliflow` MCP server name.

## Repository ownership

- **This repository:** plugin manifests, marketplace catalog, skills, icon, tests, and pilot documentation.
- **[af-cli](https://github.com/AmpliFlow/af-cli):** public CLI releases and installer.
- Hosted MCP implementation and deployment are maintained separately from this public package.

Package changes require a version bump and the checks in [plugins/ampliflow/TESTING.md](plugins/ampliflow/TESTING.md). Keep credentials, tenant records, screenshots, `.af/`, and other local runtime state out of Git.

## Public distribution

The GitHub marketplace is a Desktop pilot route, not a public ChatGPT listing. Browser and mobile distribution requires OpenAI review through **With MCP**, using a frozen production endpoint, privacy and support information, reviewer access, and the required positive and negative tests.

## License

Copyright (c) 2026 Cognit Consulting AB, trading as AmpliFlow. All rights reserved. See [LICENSE](LICENSE). Confirm package-use terms before broad customer distribution.
