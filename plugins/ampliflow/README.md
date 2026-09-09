# AmpliFlow for ChatGPT: pilot

Bring your management system into ChatGPT. AmpliFlow connects processes, goals, risks, projects, and documents with the people responsible for them. This package adds focused review skills to the registered AmpliFlow connection.

The skills review project tasks, portfolio status, goals, risks and controls, improvements, and checklists without changing records. They do not restrict the connected server's permissions: other tools may allow writes. Review tool approvals and use an account with suitable access.

## Install and test

This pilot package references a registered app. It contains no credentials or server executable, does not install the CLI, and leaves local agent configuration unchanged.

For a workspace admin:

1. Make the registered AmpliFlow app available to the intended workspace roles. Confirm that a pilot user can connect and read the expected tenant's projects.
2. Open **Admin > Plugins > Add > Import marketplace**.
3. Set Source to `https://github.com/AmpliFlow/af-chatgpt`. Leave Path empty. Select a reviewed commit in **Branch, tag, or commit** for a fixed pilot revision, or `main` to receive updates.
4. Import, inspect the report, and configure the plugin's workspace installation policy and required app access. Repository policy values do not set workspace permissions.
5. Have the pilot user install the package, complete authentication if prompted, and start a new chat on a supported surface. Verify that the bundled skills are available.
6. Start with: "Show incomplete tasks in [project name], including assignees and due dates. Do not change anything." Then test the other workflows listed in [TESTING.md](TESTING.md) against approved AmpliFlow data.

For local desktop testing, run `codex plugin marketplace add AmpliFlow/af-chatgpt`, restart the ChatGPT desktop app, and select **AmpliFlow pilot** in the Plugins Directory. The required app still needs to be accessible to that account.

The initial pilot installed the package and displayed its icon, but connecting the required app failed with "Couldn't load connector". The direct MCP connection had worked separately. Verify required-app access and skill discovery before inviting other users. OpenAI says local and repo marketplace availability varies by surface.

## External customer pilots

The `.app.json` file references the app registered for this pilot. Importing the catalog does not grant access to that app, connect an AmpliFlow account, or share the publisher's tenant data.

If a customer workspace cannot access the referenced app, its admin must register `https://mcp.ampliflow.cc/mcp` and verify OAuth first. Prepare a customer-specific copy of the package in a separate controlled marketplace with that connection's **App Id**. Use the `asdk_app_...` value, rather than its Version Id or a `plugin_`-prefixed ID. Keep the shared pilot mapping unchanged. Never put credentials in these files.

OpenAI currently marks GitHub-imported plugins with bundled MCP configuration desktop-only, including remote HTTPS servers. This package uses `.app.json` instead; that choice alone is not proof of browser compatibility.

Pilot access is by arrangement with AmpliFlow. This package does not change the repository's license or grant additional redistribution rights. Confirm package-use terms before broad customer distribution.

## Description for the registered connection

The package manifest does not edit the personal connection you already created. Use **Edit description** on that connection to set:

> AmpliFlow brings processes, goals, risks, projects, and documents into one management system, connecting ownership, ways of working, and follow-up. Connect ChatGPT to your AmpliFlow account to find records, review what needs attention, and work with your management system through the tools available to your account. An AmpliFlow account is required. Available actions depend on your permissions and the connection settings; some tools can change live records.

This connection description covers the MCP server independently of the bundled skill.

## Maintenance

This repository is the source of truth for the plugin package and marketplace. Edit the files here, bump `plugins/ampliflow/plugin.json`'s version, and run the checks in [TESTING.md](TESTING.md). Publish the manifest and skill files together. MCP server implementation stays in `af-cli-dev`; CLI releases and the installer stay in `af-cli`.

Workspace marketplaces sync daily by default. Review changes before publishing; new entries can be imported automatically. A pinned catalog revision does not pin the hosted MCP implementation. Public directory submission is a separate later step through OpenAI's **With MCP** submission flow.

## Sources

- [AmpliFlow](https://www.ampliflow.com/): product positioning.
- [Package your plugin](https://developers.openai.com/plugins/build/plugins): manifests and local marketplaces.
- [Plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management): GitHub import, app references, permissions, and desktop limits.
- [Submit plugins](https://developers.openai.com/plugins/deploy/submission): public submission.
