# AmpliFlow for ChatGPT: pilot

Bring your management system into ChatGPT. AmpliFlow connects processes, goals, risks, projects, and documents with the people responsible for them. This package connects to AmpliFlow's hosted MCP server and adds focused review skills.

The skills review project tasks, portfolio status, goals, risks and controls, improvements, and checklists without changing records. They do not restrict the connected server's permissions: other tools may allow writes. Review tool approvals and use an account with suitable access.

## Install and test

The package declares the remote HTTPS endpoint in `mcp.json`. It contains no credentials or server executable, does not install the CLI, and leaves local agent configuration unchanged. OAuth is discovered from and handled by the AmpliFlow MCP server.

OpenAI currently marks GitHub-imported plugins with bundled MCP configuration desktop-only, including remote HTTPS servers. Use this route for the desktop pilot. Public ChatGPT web and mobile distribution requires OpenAI's **With MCP** submission and review.

For a workspace admin:

1. Open **Admin > Plugins > Add > Import marketplace**.
2. Set Source to `https://github.com/AmpliFlow/af-chatgpt`. Leave Path empty. Select a reviewed commit in **Branch, tag, or commit** for a fixed pilot revision, or `main` to receive updates.
3. Import, inspect the report, and configure the plugin's workspace installation policy. Repository policy values do not set workspace permissions.
4. Have the pilot user install the package in ChatGPT desktop, complete AmpliFlow authentication when prompted, and start a new chat. Verify that the bundled skills and AmpliFlow tools are available.
5. Start with: "Show incomplete tasks in [project name], including assignees and due dates. Do not change anything." Then test the other workflows listed in [TESTING.md](TESTING.md) against approved AmpliFlow data.

For local desktop testing, run `codex plugin marketplace add AmpliFlow/af-chatgpt`, restart the ChatGPT desktop app, and select **AmpliFlow pilot** in the Plugins Directory.

The earlier package installed and displayed its icon, but its `.app.json` dependency referred to an app unavailable in another workspace. Version 0.3.0 removes that dependency and declares the MCP endpoint directly. Verify fresh installation, OAuth, tool discovery, and skill discovery before inviting other users.

## Tool discovery

Version 0.3.1 adds each skill's documented MCP dependency and bounded, conditional host-discovery guidance. These changes do not enable a hidden runtime setting or prove that missing actions are callable. Follow the [discovery guide](DISCOVERY.md) to compare authenticated server inventory, scanned metadata, action policy, and a fresh ChatGPT session. It also covers the five-skill MCP-import limit and the separate workspace browser-pilot option.

## External customer pilots

A customer can import the same package in ChatGPT desktop. Each user authenticates against `https://mcp.ampliflow.cc/mcp` with their own AmpliFlow account. Importing the catalog does not connect an account, grant AmpliFlow permissions, or share the publisher's tenant data. Never put credentials in package files.

Pilot access is by arrangement with AmpliFlow. This package does not change the repository's license or grant additional redistribution rights. Confirm package-use terms before broad customer distribution.

## Public distribution

For browser and mobile access, submit the production endpoint through OpenAI's **With MCP** flow. Submit `https://mcp.ampliflow.cc/mcp` directly and include the reviewed skills; do not submit a personal or workspace-scoped app ID. Complete OpenAI's current OAuth, metadata, reviewer-access, privacy, support, and test requirements before submission.

## Maintenance

This repository is the source of truth for the plugin package and marketplace. Edit the files here, bump `plugins/ampliflow/plugin.json`'s version, and run the checks in [TESTING.md](TESTING.md). Publish `plugin.json`, `mcp.json`, and the complete skill directories, including `agents/openai.yaml`, together. MCP server implementation stays in `af-cli-dev`; CLI releases and the installer stay in `af-cli`.

Workspace marketplaces sync daily by default. Review changes before publishing; new entries can be imported automatically. A pinned catalog revision pins package files, not the hosted MCP implementation.

## Sources

- [AmpliFlow](https://www.ampliflow.com/): product positioning.
- [Package your plugin](https://developers.openai.com/plugins/build/plugins): portable manifests, MCP configuration, and local marketplaces.
- [Authentication](https://developers.openai.com/plugins/build/auth): MCP OAuth requirements.
- [Plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management): GitHub import, permissions, and desktop limits.
- [Submit plugins](https://developers.openai.com/plugins/deploy/submission): public submission.
