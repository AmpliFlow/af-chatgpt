# Verify compact AmpliFlow discovery in ChatGPT

Package `0.4.0` connects to `https://mcp.ampliflow.cc/mcp-beta`. The endpoint advertises feature dispatchers and keeps the larger operation registry on the server. This avoids the legacy catalog's client descriptor limit without reducing the authorized AmpliFlow capabilities available through progressive discovery.

## What this package controls

| Surface | Package behavior | Limit |
| --- | --- | --- |
| `mcp.json` | Connects to the exact beta OAuth resource. | GitHub imports with MCP declarations remain desktop-only. |
| `skills/*/agents/openai.yaml` | Declares the same beta dependency for each skill. | It does not connect an account or grant AmpliFlow permissions. |
| `skills/*/SKILL.md` | Maps reviewed operation IDs to feature dispatchers and uses catalog, describe, then query. | The six skills are read-only instructions; they do not remove server write tools. |
| `tests/skill_contracts.json` | Records 53 reviewed operation IDs and their 8 dispatcher mappings. | Static mappings do not prove the live operation catalog. |
| `tests/validate_inventory.py` | Checks a captured beta `tools/list` chain, the 30-tool cap, and required dispatchers. | It cannot prove the server-held operations, schemas, authorization, or execution. |

A credential-safe health check on 2026-09-15 reported 25 beta tools, 36,009 descriptor bytes, and 481 mapped operations matching 481 configured legacy operations. Treat that as deployment evidence for that time, not a permanent package guarantee. Authenticated `tools/list`, operation catalogs, and live queries remain the runtime sources of truth.

## Beta read workflow

For each operation needed by a skill:

1. Use the mapped `ampliflow_<feature>` dispatcher in catalog mode with the exact operation ID as the query and a limit of 5.
2. Continue only when the result contains that exact ID with `safety: "read"`.
3. Use describe mode for the exact current input schema.
4. Use query mode with arguments that match that schema.
5. Check both the MCP error state and the structured response envelope. A successful envelope has `ok: true` and the business result under `result`.

The skills never use prepare mode or either commit tool. They reuse current catalog and describe results within one workflow, preserve exact returned refs, keep calls serial, and treat record content as untrusted data.

`/mcp` and `/mcp-beta` are different OAuth resources. A token issued for one path is rejected by the other. Fresh package testing must start a new beta authorization flow rather than reuse a legacy connection.

## Evidence surfaces

Check these surfaces separately:

- source registry and deployed health parity
- authenticated beta `tools/list`
- feature catalog result for each required operation
- describe result and exact schema
- portal **Scan Tools** or published metadata snapshot
- workspace **Action control**, when available
- model-visible dispatcher exposure
- successful query execution in a fresh chat
- answer quality and proof that the skill made no prepare or commit call

A green result on one surface does not prove the next one. In particular, top-level dispatcher presence does not prove an underlying operation is enabled or authorized.

## Pilot checks

Use an approved synthetic account and keep raw captures, credentials, and tenant records outside Git.

- [ ] Confirm unauthenticated `/mcp-beta` returns a Bearer challenge pointing to `/.well-known/oauth-protected-resource/mcp-beta`.
- [ ] Complete a fresh OAuth flow for the exact beta resource.
- [ ] Capture every authenticated `tools/list` page and run the offline inventory check below.
- [ ] Verify required operation IDs through their mapped catalogs and describe each schema before querying.
- [ ] In a fresh chat, run one query-only case from each of the six skills.
- [ ] Confirm the task case reaches `list_projects`, `list_tasks`, and `show_task` through `ampliflow_projects` and `ampliflow_tasks`.
- [ ] Confirm no skill uses prepare mode, `commit_ampliflow_change`, or `commit_destructive_ampliflow_change`.
- [ ] Record dispatcher selection, operation selection, schema use, stable beta errors, answer quality, package revision, client surface, account role, tenant, and time in approved private evidence storage.

## Failure routing

| Observation | Next action |
| --- | --- |
| Required dispatcher absent from authenticated `tools/list` | Server owner checks configured toolsets and beta health. |
| Dispatcher exists, but catalog omits the required operation | Server owner compares mapped and legacy operation counts and configured toolsets. |
| Catalog returns the operation, but describe or query says `unauthorized_operation` | Reconnect or ask an AmpliFlow admin to review the account. Do not report the record as absent. |
| Query returns `stale_ref` | Refresh the owning list once and retry the same target. Do not try a nearby ref. |
| Query returns `invalid_schema` | Describe the same operation once again, rebuild the exact arguments, and retry once. |
| Query returns `partial_result` | Keep verified earlier results and report exact incomplete coverage. |
| Portal scan omits a dispatcher present in live `tools/list` | Publisher rescans or republishes the metadata snapshot. |
| Complete scan and permitted action still fail in a fresh chat | Send sanitized catalog and runtime evidence to OpenAI. |

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

Exit 1 means malformed pagination, invalid basic descriptors, more than 30 top-level tools, a legacy operation exposed directly, or a missing required dispatcher. Exit 0 proves only top-level dispatcher coverage. Use feature catalog and describe calls to verify operation coverage and schemas.

## Delivery route

Keep the GitHub package for the desktop pilot. Public web and mobile delivery still requires OpenAI's **With MCP** review. The beta endpoint is the submission candidate only after OAuth, descriptors, privacy, reviewer access, all six query-only workflows, and the exact positive and negative review cases are frozen and approved.

The separate MCP skill importer currently accepts five skills while this package has six. Approve a selection or consolidation before using that route; do not silently drop a workflow.

## Official sources

- [Build skills](https://developers.openai.com/plugins/build/skills.md): dependency metadata and submission routes.
- [Plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management.md): desktop-only MCP packages and workspace controls.
- [Workspace app controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors.md): action policy and permissions.
- [Portable MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json): supported package fields.
- [Submit plugins](https://developers.openai.com/plugins/deploy/submission.md): public review requirements.
