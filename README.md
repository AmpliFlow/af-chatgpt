# AmpliFlow for ChatGPT

Connect ChatGPT to your AmpliFlow management system. This repository contains the pilot plugin, marketplace catalog, icon, and focused read-only review skills.

AmpliFlow brings processes, goals, risks, projects, and documents into one management system. The bundled skills review project tasks, portfolio status, goals, risks and controls, improvements, and checklists through your connected account.

## Pilot setup

Workspace admins can import this repository from **Admin > Plugins > Add > Import marketplace**:

- **Source:** `https://github.com/AmpliFlow/af-chatgpt`
- **Path:** leave empty
- **Branch, tag, or commit:** leave empty for `main`, or select a reviewed commit

Follow the [setup guide](plugins/ampliflow/README.md) for required-app access, authentication, and testing.

The pilot's direct MCP connection worked, and the package installed with its icon while hosted in `af-cli`. Connecting the package's required app failed with "Couldn't load connector" and still needs investigation. Installation from this new repository has not yet been confirmed. See [PROJECT.md](PROJECT.md) for the evidence and next checks.

The package references an existing registered AmpliFlow app. Importing it does not grant app access or connect a user's account. The bundled skills are read-only; the connected server may expose write tools under the user's permissions.

## Moving from the old marketplace

This catalog replaces the pilot previously hosted in `AmpliFlow/af-cli`. With no users to migrate, remove the old marketplace in ChatGPT and import this repository as a new source. Deleting the old marketplace also removes its imported plugins. Keep the original MCP connection so required-app access can be tested separately.

## Repository ownership

- **This repository:** plugin manifests, marketplace catalog, skills, assets, and setup instructions.
- **[af-cli](https://github.com/AmpliFlow/af-cli):** public CLI releases and installer.
- **af-cli-dev:** private MCP server implementation and CLI development.

Edit the plugin here and bump its version before publishing updates. Use the [acceptance checks](plugins/ampliflow/TESTING.md) before expanding the pilot. Public directory submission remains a separate step.

## Development and project setup

Start work in this repository. [PROJECT.md](PROJECT.md) records the rollout order, package architecture, connector blocker, test evidence, and the bound standalone AmpliFlow project.

The current package version is `0.2.0`. Run the deterministic validator and the manual [acceptance checks](plugins/ampliflow/TESTING.md) before expanding the pilot. Keep local auth and `.af` runtime files out of commits. MCP server changes belong in `af-cli-dev`; plugin work does not require its old worktree.

## License

Copyright (c) 2026 Cognit Consulting AB, trading as AmpliFlow. All rights reserved. See [LICENSE](LICENSE). Package-use terms need confirmation before broad customer distribution.
