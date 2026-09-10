# Diagnose missing AmpliFlow tools in ChatGPT

The package now declares each skill's MCP dependency and checks for host-provided discovery before reporting a tool as unavailable. This fixes package omissions, not a proven cause of the observed 40-tool prefix. Browser delivery and live tool discovery still need verification outside this repository.

## What this package controls

| Surface | Package behavior | Limit |
| --- | --- | --- |
| `mcp.json` | Connects to the universal HTTPS endpoint. | GitHub imports with MCP declarations are desktop-only, even with a remote URL. |
| `skills/*/agents/openai.yaml` | Declares the documented AmpliFlow MCP server dependency. | Does not select actions, grant permissions, or enable deferred loading. Client handling needs a live test. |
| `skills/*/SKILL.md` | Uses available host discovery once per missing capability, then uses the returned binding and schema or reports reduced scope. | Cannot call tools the host neither exposes nor discovers. |
| `tests/skill_contracts.json` | Lists 25 unique core tools and 28 additional tools used by conditional branches. | Package expectations, not a deployed catalog or enforced read-only profile. |
| `tests/validate_inventory.py` | Checks captured catalog pagination and dependency coverage. | Does not connect, authenticate, call tools, or prove runtime behavior. |

The portable MCP schema has no `allowed_tools` or `defer_loading` field. OpenAI's Responses API supports those controls and `tool_search`, but the API request format is not ChatGPT plugin configuration. A skill must not assume the runtime exposes that facility.

## Delivery route

The customer goal remains public **With MCP** review and publication of `https://mcp.ampliflow.cc/mcp`, with the reviewed skills. Keep the bundled-MCP GitHub package for desktop testing; it is not proof of browser delivery.

A workspace browser pilot can instead reference an existing, available registered app through `.app.json`. That reference does not create the app or grant access. This repository deliberately retains the universal endpoint rather than restoring the workspace-scoped dependency that failed cross-workspace installation.

OpenAI also supports uploading packaged skills during submission. Its separate MCP skill importer accepts at most five uniquely named skills across ten catalog pages. This package has six. Before using that importer, approve a five-skill selection or a consolidation; do not silently drop a workflow. Do not infer the upload route's limits from the MCP importer limit.

## Isolate the tool-discovery failure

Use an approved synthetic account. These are operator checks, not changes performed by the package.

- [ ] Capture authenticated `tools/list` from the exact endpoint and follow every `nextCursor`. Record the server release and time separately. Health output and source registration are not substitutes.
- [ ] Check the capture with the offline command below. Investigate any missing core dependency before testing answers. Optional gaps block their corresponding branches, not every review.
- [ ] Compare those names with the portal's **Scan Tools** result and published metadata. OpenAI publishes a metadata snapshot; deploying a changed server does not itself refresh the published tool list.
- [ ] Inspect workspace **Action control**, when supported, for filtering. An approved custom set or read-only action policy can restrict actions. Prompt instructions and metadata hints do not enforce access.
- [ ] In a fresh chat, request incomplete tasks with due dates for one synthetic project. Verify `list_projects`, `list_tasks`, and the late-alphabet `show_task` actually execute, directly or after host discovery. A model saying a tool exists is not execution evidence.
- [ ] Run the deferred, missing, optional, and authorization cases in [TESTING.md](TESTING.md). Record both calls and answer correctness in approved private evidence storage.

| Observation | Next owner/action |
| --- | --- |
| Required tool absent from complete authenticated inventory | Server owner checks deployment and registration. Existing af-cli task #986 covers constrained client-safe surfaces. |
| Inventory contains the tool but scanned/published metadata does not | Publisher checks scan failures and metadata publication. |
| Scanned tool blocked by workspace action policy | Workspace admin reviews the intended access policy. |
| Tool available after host discovery and successfully called | Deferred visibility explains that case; verify the other workflows. |
| Complete scan, permitted action, but fresh chat cannot discover or call it | Report the catalog comparison and sanitized runtime trace to OpenAI. |
| Authentication or descriptor failure | Reverify deployed behavior against existing af-cli tasks #1127 and #1128. |

The observed first 40 alphabetical tools do not establish a platform limit. The inspected Go SDK v1.4.1 defaults to 1,000 tools per page, and the inspected server does not override that setting. Neither fact proves the production response. Avoid renaming tools, adding a fake search tool, or changing page size without evidence.

If a smaller surface is needed, start from the approved workflow dependencies, not an assumed cap of 40. The 25 core tools omit conditional branches that can matter to users. Any narrower server profile needs explicit coverage decisions and live verification by its owner.

## Offline inventory check

The checker reads a capture from an operator-managed path. Keep raw captures, headers, credentials, and private evidence out of Git. It prints dependency names from this repository, not captured descriptions or record data.

Capture format: a nonempty `pages` array, each entry containing the exact request `params` and response `result`. For the first page, `params` is `{}`. For each later page it is `{"cursor":"<previous nextCursor>"}`. Preserve descriptors, especially `name`, `description`, and `inputSchema`; the final result must omit `nextCursor`. A present cursor must be a string, including an empty string if that is what the server returned; null is invalid.

Synthetic format example, intentionally missing most dependencies:

```json
{
  "pages": [
    {
      "params": {},
      "result": {
        "tools": [
          {
            "name": "list_projects",
            "description": "Synthetic project list",
            "inputSchema": {"type": "object"}
          }
        ]
      }
    }
  ]
}
```

```text
python3 -B plugins/ampliflow/tests/validate_inventory.py /path/to/approved-tools-list-capture.json
```

Exit 1 means malformed/incomplete pagination, invalid basic descriptors, duplicate names, or missing core dependencies. Exit 0 means the captured catalog covers the core dependencies; optional gaps are printed. This is not full JSON Schema validation, an authenticity check, or a release approval.

## Official sources

- [Build skills](https://developers.openai.com/plugins/build/skills.md): dependency metadata and submission upload/import routes.
- [Plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management.md): desktop-only MCP packages and existing-app references.
- [Workspace app controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors.md): action policy and permissions.
- [Portable MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json): supported package fields.
- [Tool search](https://developers.openai.com/api/docs/guides/tools-tool-search): Responses API deferred loading.
- [App review](https://developers.openai.com/plugins/deploy/app-review.md): published metadata snapshots.
- [MCP skill import](https://developers.openai.com/plugins/build/mcp-server.md#import-skills-from-the-mcp-server): importer limits.
