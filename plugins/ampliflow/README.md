# AmpliFlow for ChatGPT: desktop pilot

The AmpliFlow plugin works in ChatGPT Desktop **Work** mode. It connects to the hosted AmpliFlow MCP server and adds one general router for reads and explicit user-confirmed changes plus six read-only focused review skills.

> [!IMPORTANT]
> **Use Work mode for this pilot**
> Chat mode runs the conversation in ChatGPT cloud and does not receive the MCP tools loaded by the GitHub-imported desktop plugin. The `@AmpliFlow` mention can still appear there, which makes this failure easy to misread as an authentication or server problem.

## What the package contains

Package `0.8.0` declares only `https://mcp.ampliflow.com/mcp` in `mcp.json`. It contains:

- one remote MCP connection
- one lightweight router that loads focused domain references only when needed and handles explicit confirmed changes
- six read-only focused review skills
- the AmpliFlow icon and plugin metadata
- no credentials, server executable, CLI installer, app ID, or custom UI

OAuth is discovered from and handled for that exact MCP resource. Each user signs in with an AmpliFlow account and receives only the access allowed by that account. The new normal origin requires fresh resource-bound OAuth; never reuse or transform beta authorization.

Candidate `0.8.0` is unpublished. Normal-origin TLS and routing are under construction; source agreement is not deployment or client acceptance. The published `0.7.0` beta artifact remains usable for internal tests and rollback, without changing this candidate's connection or adding a fallback.

## Admin installation

Use these steps only after a separately authorized release and verified hosted readiness.

1. Open **Admin > Plugins > Add > Import marketplace**.
2. Set **Source** to `https://github.com/AmpliFlow/af-chatgpt`.
3. Leave **Path** empty and import the marketplace.
4. Make **AmpliFlow pilot** available to the pilot users.

See OpenAI's [marketplace import guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github) for current ChatGPT workspace administration steps.

## User setup and first test

1. Install **AmpliFlow** from the Plugins Directory.
2. Complete AmpliFlow authentication when prompted.
3. Fully quit and reopen ChatGPT Desktop.
4. On the new-conversation screen, select **Work** at the top.
5. Add `@AmpliFlow` in the composer.
6. Ask: `What projects do I have?`

Then try:

```text
Show incomplete tasks in [project name], including assignees and due dates. Do not change anything.
```

For a domain outside the focused reviews, try:

```text
Show purchase orders due this month and the suppliers and items linked to them. Do not change anything.
```

A successful request routes to the smallest relevant feature set. For example, a task read uses `ampliflow_projects` and, when needed, `ampliflow_tasks`. Read workflows call each feature dispatcher in this order:

```text
catalog -> describe -> query
```

They require `safety: "read"` and a successful structured response with `ok: true`. For an explicit mutation request, only the general router uses:

```text
read current state -> propose exact change -> wait for explicit confirmation -> prepare -> commit once -> read back
```

The router forwards `plan_token`, `operation`, `action_summary`, and `target_summary` unchanged. It selects `commit_ampliflow_change` or `commit_destructive_ampliflow_change` from the server's safety class. Follow-up calls use exact identities from the described structured operation result, never from prose. Missing receipt identities stop the chain as unverified. Calls stay serial; plans are neither transactions nor proof of human approval. Client cancellation does not prove a remote write was cancelled, and uncertain writes are never automatically retried. Hosted server paths are not client files or exports. The six focused review skills never prepare or commit changes.

For improvement creation or grading updates, the router reads `show_improvement_gradings` through `ampliflow_improvements` after the confirmed write and compares the exact persisted `impact` and UUID-to-score `impact_list` with the proposal. Generic `show_improvement` omits the map. Score 0 means selected but ungraded. The result discloses `separate_non_atomic_reads`, not an atomic snapshot or approval evidence. Missing or mismatched fields remain unverified without automatic write retry.

Personal reads use `get_authenticated_identity` through `ampliflow_people` and preserve `result.authenticated_identity` evidence. Unknown tenant binding stays unknown; the effective principal is not proof of an original human or per-write attribution. Profile authentication can issue a JWT/cookie even when discarded; do not automatically retry an uncertain identity read.

## Supported surfaces

| Surface | Status |
| --- | --- |
| Desktop **Work** mode | Package `0.5.0` pilot path verified; package `0.8.0` acceptance pending |
| Desktop **Chat** mode | Unsupported for the imported package; no plugin MCP tools reach the cloud turn |
| Web and mobile | Not delivered by this GitHub package; use the future **With MCP** review route |

Earlier beta-client evidence, not normal-origin acceptance: this distinction was verified on ChatGPT Desktop `26.901.20858`: the same installed package, OAuth credential, and 25-tool inventory worked in a local Work turn, while a Chat turn produced no local `thread/start`, `turn/start`, or MCP call.

## Troubleshooting

### The plugin is visible, but no AmpliFlow tools are available

Confirm that the conversation was created in **Work** mode. Switching to or retrying in Chat mode will not mount the imported plugin's MCP tools. Start a new Work conversation after selecting `@AmpliFlow`.

### Authentication does not complete

Confirm the connection targets exactly `https://mcp.ampliflow.com/mcp`. Do not reuse credentials for another resource. Complete the prompted OAuth flow, restart Desktop, and retry in a new Work conversation.

### The plugin shows no tools after an update

Fully quit and reopen Desktop. If an obsolete AmpliFlow marketplace is still configured, remove it so only one installed plugin owns the `ampliflow` MCP server name. Do not add a duplicate personal MCP connection.

### A dispatcher or operation is unavailable

Report the affected workflow and preserve any independent verified results. Do not search for another endpoint, derive an operation ID from tenant content, or use a runtime namespace fallback. For a write, also stop on readonly mode or an authorization failure; never try another operation or target.

### A prepared change expires or the target changes

Discard the plan. Refresh the same target and operation, show a new exact proposal, and obtain fresh confirmation before preparing again. Plans expire after five minutes and are single-use.

See [DISCOVERY.md](DISCOVERY.md) for inventory and operation checks, and [TESTING.md](TESTING.md) for the full pilot cases.

## Customer pilots

Each customer workspace imports the same reviewed repository revision. Each user authenticates with their own account; importing the package does not grant AmpliFlow access or share the publisher's tenant data.

Keep the pilot guided until a separate customer workspace has verified installation, Work-mode execution, correct tenant isolation, and package updates. Confirm package-use terms before broad distribution.

## Public distribution

The GitHub-imported package is Desktop pilot infrastructure. Public browser and mobile access requires OpenAI's **With MCP** submission and review. Submit the frozen production MCP endpoint only after OAuth, metadata, privacy, support, reviewer access, and exactly five positive plus three negative review tests are ready.

## Maintenance

This repository is the source of truth for the package. For each shipped package update:

1. edit the package here
2. bump `plugins/ampliflow/plugin.json`
3. run [TESTING.md](TESTING.md)
4. publish the manifest, MCP declaration, and complete skill directories together
5. verify the imported revision in a fresh Desktop Work conversation

Hosted MCP changes are maintained separately; CLI releases belong in `af-cli`.
