# AmpliFlow for ChatGPT: pilot

Bring your management system into ChatGPT. AmpliFlow connects processes, goals, risks, projects, and documents with the people responsible for them. This package connects to AmpliFlow's hosted MCP server and adds focused review skills.

The skills review project tasks, portfolio status, goals, risks and controls, improvements, and checklists without changing records. They do not restrict the connected server's permissions: other tools may allow writes. Review tool approvals and use an account with suitable access.

## Install and test

The package declares the compact remote HTTPS endpoint in `mcp.json`. It contains no credentials or server executable, does not install the CLI, and leaves local agent configuration unchanged. OAuth is discovered from and handled by the AmpliFlow MCP server. `/mcp-beta` is a separate OAuth resource, so users moving from `/mcp` must authenticate again.

OpenAI currently marks GitHub-imported plugins with bundled MCP configuration desktop-only, including remote HTTPS servers. Use this route for the desktop pilot. Public ChatGPT web and mobile distribution requires OpenAI's **With MCP** submission and review.

For a workspace admin:

1. Open **Admin > Plugins > Add > Import marketplace**.
2. Set Source to `https://github.com/AmpliFlow/af-chatgpt`. Leave Path empty. Select a reviewed commit in **Branch, tag, or commit** for a fixed pilot revision, or `main` to receive updates.
3. Import, inspect the report, and configure the plugin's workspace installation policy. Repository policy values do not set workspace permissions.
4. Have the pilot user install the package in ChatGPT desktop, complete AmpliFlow authentication when prompted, and start a new chat. Verify that the bundled skills and AmpliFlow tools are available.
5. Start with: "Show incomplete tasks in [project name], including assignees and due dates. Do not change anything." Then test the other workflows listed in [TESTING.md](TESTING.md) against approved AmpliFlow data.

For local desktop testing, run `codex plugin marketplace add AmpliFlow/af-chatgpt`, restart the ChatGPT desktop app, and select **AmpliFlow pilot** in the Plugins Directory.

The earlier package installed and displayed its icon, but its `.app.json` dependency referred to an app unavailable in another workspace. Version 0.3.0 removed that dependency. Version 0.4.0 switches the direct connection to the compact beta resource. Verify fresh installation, beta OAuth, dispatcher discovery, operation discovery, and skill discovery before inviting other users.

## Progressive operation discovery

The beta endpoint advertises feature tools such as `ampliflow_projects` and `ampliflow_tasks`, not hundreds of operation tools. Each bundled skill uses the matching dispatcher to catalog a stable operation ID, describe its current schema, then query it. The skills verify `safety: "read"`, consume successful results from the structured `ok` envelope, and never prepare or commit changes.

Follow the [discovery guide](DISCOVERY.md) to compare authenticated beta inventory, operation catalogs, scanned metadata, action policy, and fresh ChatGPT execution. It also covers the five-skill MCP-import limit and the separate workspace browser-pilot option.

## External customer pilots

A customer can import the same package in ChatGPT desktop. Each user authenticates against `https://mcp.ampliflow.cc/mcp-beta` with their own AmpliFlow account. Importing the catalog does not connect an account, grant AmpliFlow permissions, or share the publisher's tenant data. Never put credentials in package files.

Pilot access is by arrangement with AmpliFlow. This package does not change the repository's license or grant additional redistribution rights. Confirm package-use terms before broad customer distribution.

## Public distribution

For browser and mobile access, submit the reviewed production endpoint through OpenAI's **With MCP** flow. The candidate used by this package is `https://mcp.ampliflow.cc/mcp-beta`; do not submit a personal or workspace-scoped app ID. Complete the beta pilot and OpenAI's current OAuth, metadata, reviewer-access, privacy, support, and test requirements before submission.

## Maintenance

This repository is the source of truth for the plugin package and marketplace. Edit the files here, bump `plugins/ampliflow/plugin.json`'s version, and run the checks in [TESTING.md](TESTING.md). Publish `plugin.json`, `mcp.json`, and the complete skill directories, including `agents/openai.yaml`, together. MCP server implementation stays in `server repository`; CLI releases and the installer stay in `af-cli`.

Workspace marketplaces sync daily by default. Review changes before publishing; new entries can be imported automatically. A pinned catalog revision pins package files, not the hosted MCP implementation.

## Sources

- [AmpliFlow](https://www.ampliflow.com/): product positioning.
- [Package your plugin](https://developers.openai.com/plugins/build/plugins): portable manifests, MCP configuration, and local marketplaces.
- [Authentication](https://developers.openai.com/plugins/build/auth): MCP OAuth requirements.
- [Plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management): GitHub import, permissions, and desktop limits.
- [Submit plugins](https://developers.openai.com/plugins/deploy/submission): public submission.
