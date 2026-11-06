# MCP acceptance status

Candidate `0.10.1` retains canonical production `ampliflow` and beta `ampliflow-beta` plugin/MCP identities. Package/model checks, workspace synchronization and full supported-client acceptance remain separate evidence layers.

Historical release checkpoint: [`0.8.0`](https://github.com/AmpliFlow/af-chatgpt/releases/tag/v0.8.0) was published from source `1a122842e631a067c9204e7c0a173caff5f3d64b`. Its four release assets and 69-test CI are verified. This file summarizes the acceptance limits; private traces and account details remain outside the repository.

As checked on 2026-11-06, the normal MCP service is deployed at CLI `14.2.4`; strict HTTPS, fresh resource-bound OAuth and its 28-tool inventory are qualified. The previous certificate/deployment blocker is resolved. Beta and normal remain separate; beta authorization cannot be reused or transformed.

A user-supplied Desktop screenshot shows version `0.8.0` but the beta URL `https://mcp.ampliflow.cc/mcp-beta`. The verified release ZIP declares only `https://mcp.ampliflow.com/mcp`. Both versions reuse plugin name `ampliflow` and MCP server key `ampliflow`; the displayed workspace binding differs from the artifact. The precise cache/override layer is unproven. A working beta-bound project read is not a normal-client pass. Version `0.9.0` kept legacy `ampliflow` on beta and added production identity `ampliflow-production`. Version `0.10.0` corrects the names to production `ampliflow` and beta `ampliflow-beta`; this may disrupt existing connections. That historical migration does not apply anew to guidance-only `0.10.1`. Never reuse a retained beta binding as production. The user now confirms af-chatgpt and all four resources work (`.com/mcp`, `.com/mcp-beta`, `.cc/mcp`, `.cc/mcp-beta`). Accept this as user-attested client/connectivity evidence; exact `0.10.1` installation and detailed workflow cases remain unclaimed. Preserve the working client and authentication without another login/sync request or interruption. See [the migration plan](../docs/mcp-deployment.md).

Infrastructure delivery is complete. Remaining client binding, reviewer cases, persisted-field/recovery evidence and submission preparation belong to the client/server owners; no new infrastructure work is requested here.

## Earlier preparation

Earlier preparation checked public health, protected-resource metadata, an unauthenticated Bearer challenge, and approved synthetic product fixtures. Those checks do not establish current OAuth, authorization, operation schemas, model behavior, or candidate acceptance. Native product authentication is not resource-bound MCP OAuth.

Keep raw client traces, account details, credential sources, session identifiers, deployment investigations, and customer records outside this repository and all build artifacts.

## Operation contracts to verify in client acceptance

Service qualification does not prove every workflow below. Verify these live contracts through the intended normal connection:

- `get_authenticated_identity` in the users toolset, routed through `ampliflow_people`. Preserve `result.authenticated_identity`, effective principal, tenant UUID and binding, separate identity/original-executor/write-attribution evidence, and server-side effects. Unknown binding is not verified identity binding. Discarded profile JWT/cookie issuance can still occur; never automatically retry an uncertain identity read.
- Improvement list filters for responsibility, creation, and involvement as UUID arrays. Different groups intersect; an ownership union needs separate bounded queries and exact-identity deduplication. Preserve native ownership fields.
- Live active grading options and category detail with all five score definitions, without a private local-skill prerequisite. Category relevance is not a fixed API count cap.
- `show_improvement_gradings` through `ampliflow_improvements`, accepting the exact `improvement_ref` under its live schema. Read `result.improvement_gradings` identity, `impact`, and native UUID-to-score `impact_list` after confirmed creation or grading updates. Score 0 is selected but ungraded; `consistency: "separate_non_atomic_reads"` is not an atomic snapshot or approval evidence. Generic improvement detail omits the map. Missing or mismatched fields remain unverified without automatic write retry.

Package instructions require live catalog and describe discovery before use. Missing contracts are unavailable capabilities, not empty business results. Source agreement alone is not deployed proof.

## Remaining candidate and submission checks

1. Reuse valid authorization for exactly `https://mcp.ampliflow.com/mcp`; verify reconnect, expiry, denied access, and tenant isolation as separate detailed cases without resetting the working client.
2. Capture the authenticated tool inventory privately and run the offline inventory checker. Verify operation mappings, filters, native ownership outputs, and grading definitions through live catalog/describe/query.
3. Run the bounded personal-deviation and grading cases in [TESTING.md](../plugins/ampliflow/TESTING.md), the six focused read workflows, and the router's confirmation and recovery cases. A service principal must not be presented as a human.
4. Verify the installed package and exact normal-resource connection in fresh Desktop Work conversations. The displayed version alone is insufficient. Do not restart, replace authentication or interrupt the working active client to force acceptance; the offline build performs none of these steps.
5. Before any public-store submission, verify the existing approved demo access using valid exact-normal-resource OAuth, run [review.json](review.json), record an approved walkthrough, resolve owner policy/country decisions, and complete authorized portal checks. Reuse the saved access; no new account or password reset is needed.

Before publication, run deterministic checks and a bounded synthetic model comparison with an approved credential source and spending limit. Retain source revisions, results and limits; a failed run is not acceptance evidence. No production write, account change, external store action or Desktop restart is authorized by this preparation. Server release, Desktop acceptance, submission, approval, and publication remain separate outcomes.
