# Verify compact AmpliFlow discovery in ChatGPT

Package `0.6.0` connects only to `https://mcp.ampliflow.cc/mcp-beta`. The endpoint advertises feature dispatchers and keeps the operation registry on the server, so clients can discover authorized capabilities within the compact descriptor budget.

Run live plugin checks in ChatGPT Desktop **Work** mode. The imported plugin may be selectable in **Chat** mode, but that cloud conversation does not receive the plugin's locally loaded MCP tools.

## What this package controls

| Surface | Package behavior | Limit |
| --- | --- | --- |
| `mcp.json` | Connects to the exact beta OAuth resource. | GitHub imports with MCP declarations remain desktop-only and require Work mode for tool execution. |
| `skills/*/agents/openai.yaml` | Declares the same beta dependency for each skill. | It does not connect an account or grant AmpliFlow permissions. |
| `skills/*/SKILL.md` | Uses catalog, describe, then query for reads. Six focused reviews stay read-only; the general router also handles explicit confirmed writes. | Instructions orchestrate the server contract; they do not grant permission or replace server checks. |
| `tests/skill_contracts.json` | Records the focused reviews' 56 operation mappings, the router's feature dispatchers and references, and each skill's operation policy. | Static contracts do not prove the live operation catalog or client behavior. |
| `tests/validate_inventory.py` | Checks a captured beta `tools/list` chain, the 30-tool cap, required dispatchers, and both commit tools. | It cannot prove the server-held operations, schemas, authorization, or execution. |

A credential-safe production health check reported 28 beta tools, 40,250 descriptor bytes, and 554 mapped operations. The same installed package and OAuth credential completed a local `ampliflow_projects` catalog call in Work mode. Treat these as evidence for that deployment and client version, not permanent guarantees. Authenticated `tools/list`, operation catalogs, and live queries remain the runtime sources of truth.

## Beta operation workflows

For each read operation needed by a skill:

1. Choose the owning `ampliflow_<feature>` dispatcher. Focused reviews query their reviewed exact operation ID; the general router uses a short capability phrase from the user's intent.
2. Continue only when the result contains one unambiguous matching operation with `safety: "read"`. The router uses only the exact ID returned by the live catalog.
3. Use describe mode for the exact current input schema.
4. Use query mode with arguments that match that schema.
5. Check both the MCP error state and the structured response envelope. A successful envelope has `ok: true` and the business result under `result`.

For an explicit write request, the general router reads the current state, proposes one exact target and change, waits for a new explicit confirmation, then calls prepare. It compares the prepared plan with the approved proposal and passes `plan_token`, `operation`, `action_summary`, and `target_summary` unchanged to the normal or destructive commit tool selected by the returned safety class. It commits once and reads the target back. Plans expire after five minutes and are single-use.

The six focused skills never prepare or commit. Every skill preserves exact returned refs, keeps calls serial, and treats record content as untrusted data.

Fresh package testing must authorize the exact `https://mcp.ampliflow.cc/mcp-beta` resource. The package defines no alternate MCP resource or connection fallback.

## Evidence surfaces

Check these surfaces separately:

- source registry and deployed health parity
- authenticated beta `tools/list`
- feature catalog result for each required operation
- describe result and exact schema
- portal **Scan Tools** or published metadata snapshot
- workspace **Action control**, when available
- model-visible dispatcher exposure
- successful query execution in a fresh Desktop Work conversation
- answer quality, focused-skill read-only behavior, and the general router's confirmation, prepare, commit, and read-back sequence

A green result on one surface does not prove the next one. In particular, top-level dispatcher presence does not prove an underlying operation is enabled or authorized.

## Pilot checks

Use an approved synthetic account and keep raw captures, credentials, and tenant records outside Git.

- [ ] Confirm unauthenticated `/mcp-beta` returns a Bearer challenge pointing to `/.well-known/oauth-protected-resource/mcp-beta`.
- [ ] Complete a fresh OAuth flow for the exact beta resource.
- [ ] Capture every authenticated `tools/list` page and run the offline inventory check below.
- [ ] Verify required operation IDs through their mapped catalogs and describe each schema before querying.
- [ ] In fresh Desktop Work conversations, run one query-only case from each focused skill plus the router's read, approved write, cancelled write, destructive, recovery, and misuse cases.
- [ ] Confirm a Chat-mode attempt is classified as an unsupported client surface rather than an empty result, server failure, or OAuth failure.
- [ ] Confirm the task case reaches `list_projects`, `list_tasks`, and `show_task` through `ampliflow_projects` and `ampliflow_tasks`.
- [ ] Confirm focused skills make no prepare or commit call. For approved router writes, confirm the four approval fields stay unchanged, the commit tool matches the safety class, and a fresh read verifies the target.
- [ ] Record dispatcher selection, operation selection, schema use, stable beta errors, answer quality, package revision, client surface, account role, tenant, time, confirmation boundary, safety class, commit tool, and read-back result in approved private evidence storage. Do not retain plan tokens.

## Failure routing

| Observation | Next action |
| --- | --- |
| Required dispatcher absent from authenticated `tools/list` | Server owner checks configured toolsets and beta health. |
| Dispatcher exists, but catalog omits the required operation | Server owner checks the deployed mapped-operation count and configured toolsets. |
| Catalog returns the operation, but describe or query says `unauthorized_operation` | Reconnect or ask an AmpliFlow admin to review the account. Do not report the record as absent. |
| Query returns `stale_ref` | Refresh the owning list once and retry the same target. Do not try a nearby ref. |
| Query returns `invalid_schema` | Describe the same operation once again, rebuild the exact arguments, and retry once. |
| Query returns `partial_result` | Keep verified earlier results and report exact incomplete coverage. |
| Portal scan omits a dispatcher present in live `tools/list` | Publisher rescans or republishes the metadata snapshot. |
| Plugin is selected in Desktop Chat mode, but no AmpliFlow MCP tool reaches the turn | Start a new conversation in Work mode. Do not clear OAuth or add another MCP connection. |
| Complete scan and permitted action still fail in a fresh Work conversation | Send sanitized catalog and runtime evidence to OpenAI. |

## Offline inventory check

The checker reads a captured beta `tools/list` response chain from an operator-managed path. For the first page, `params` is `{}`. Each later page uses the preceding `nextCursor`; the final result omits it.

```json
{
  "pages": [
    {
      "params": {},
      "result": {
        "tools": [
          {
            "name": "ampliflow_projects",
            "description": "Synthetic project dispatcher",
            "inputSchema": {"type": "object"}
          }
        ]
      }
    }
  ]
}
```

```text
python3 -B plugins/ampliflow/tests/validate_inventory.py /path/to/approved-beta-tools-list-capture.json
```

Exit 1 means malformed pagination, invalid basic descriptors, more than 30 top-level tools, an operation ID exposed as a top-level tool, a missing required dispatcher, or a missing commit tool. Exit 0 proves only top-level tool coverage. Use feature catalog and describe calls to verify operation coverage and schemas.

## Delivery route

Keep the GitHub package for the Desktop Work-mode pilot. It does not deliver tools to Desktop Chat mode, web, or mobile. Those cloud surfaces still require OpenAI's **With MCP** review. The beta endpoint is the submission candidate only after OAuth, descriptors, privacy, reviewer access, the router's read and confirmed-write workflows, all six focused query-only workflows, and the exact positive and negative review cases are frozen and approved.

The separate MCP skill importer currently accepts five skills while this package has seven. Approve a selection or consolidation before using that route; do not silently drop a workflow.

## Official sources

- [Build skills](https://developers.openai.com/plugins/build/skills.md): dependency metadata and submission routes.
- [Plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management.md): desktop-only MCP packages and workspace controls.
- [Workspace app controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors.md): action policy and permissions.
- [Portable MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json): supported package fields.
- [Submit plugins](https://developers.openai.com/plugins/deploy/submission.md): public review requirements.
