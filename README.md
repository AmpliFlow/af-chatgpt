# AmpliFlow for ChatGPT

Connect ChatGPT to your AmpliFlow management system. This repository contains the pilot plugin, marketplace catalog, icon, and focused read-only review skills.

AmpliFlow brings processes, goals, risks, projects, and documents into one management system. The bundled skills review project tasks, portfolio status, goals, risks and controls, improvements, and checklists through your connected account.

## Pilot setup

Workspace admins can import this repository from **Admin > Plugins > Add > Import marketplace**:

- **Source:** `https://github.com/AmpliFlow/af-chatgpt`
- **Path:** leave empty
- **Branch, tag, or commit:** leave empty for `main`, or select a reviewed commit

Follow the [setup guide](plugins/ampliflow/README.md) for authentication and testing.

The package connects directly to `https://mcp.ampliflow.cc/mcp`; it does not depend on a workspace-scoped app ID. Each user authenticates with an AmpliFlow account. The bundled skills are read-only, but the connected server may expose write tools under the user's permissions.

OpenAI currently limits GitHub-imported plugins with bundled MCP configuration to ChatGPT desktop. Our public web and mobile distribution route is OpenAI's **With MCP** submission and review. Live installation through this corrected package has not yet been confirmed. See the [discovery guide](plugins/ampliflow/DISCOVERY.md) for package fixes, workspace-pilot alternatives, and the checks needed to isolate missing tools.

## Moving from the old marketplace

This catalog replaces the pilot previously hosted in `AmpliFlow/af-cli`. With no users to migrate, remove the old marketplace in ChatGPT and import this repository as a new source. Deleting the old marketplace also removes its imported plugins. A separately registered personal MCP connection is not required by this package.

## Repository ownership

- **This repository:** plugin manifests, marketplace catalog, skills, assets, and setup instructions.
- **[af-cli](https://github.com/AmpliFlow/af-cli):** public CLI releases and installer.
- **af-cli-dev:** private MCP server implementation and CLI development.

Edit the plugin here and bump its version before publishing updates. Use the [acceptance checks](plugins/ampliflow/TESTING.md) before expanding the pilot. Public directory submission remains a separate step.

## Development and project setup

Start work in this repository. [PROJECT.md](PROJECT.md) records the rollout order, package architecture, connector blocker, test evidence, and the bound standalone AmpliFlow project.

The current package version is `0.3.1`. Run the deterministic validator and the manual [acceptance checks](plugins/ampliflow/TESTING.md) before expanding the pilot. Keep local auth and `.af` runtime files out of commits. MCP server changes belong in `af-cli-dev`; plugin work does not require its old worktree.

## License

Copyright (c) 2026 Cognit Consulting AB, trading as AmpliFlow. All rights reserved. See [LICENSE](LICENSE). Package-use terms need confirmation before broad customer distribution.
