# MCP acceptance status

Candidate `0.8.0` has offline package checks only. This file is a public status summary, not private investigation evidence or proof of deployment.

Normal-origin TLS and routing are under construction. The new origin needs fresh resource-bound OAuth; beta authorization cannot be reused or transformed. The published `0.7.0` beta artifact remains usable for internal tests and rollback. This candidate has no beta fallback.

The backend owner owns the compact stable MCP cutover, CI, and IaC. This repository changes only the client package, not the hosted service.

## Earlier preparation

Earlier preparation checked public health, protected-resource metadata, an unauthenticated Bearer challenge, and approved synthetic product fixtures. Those checks do not establish current OAuth, authorization, operation schemas, model behavior, or candidate acceptance. Native product authentication is not resource-bound MCP OAuth.

Keep raw client traces, account details, credential sources, session identifiers, deployment investigations, and customer records outside this repository and all build artifacts.

## Coordinated backend dependency

The server owner must deliver and verify these contracts with this package:

- `get_authenticated_identity` in the users toolset, routed through `ampliflow_people`. Preserve `result.authenticated_identity`, effective principal, tenant UUID and binding, separate identity/original-executor/write-attribution evidence, and server-side effects. Unknown binding is not verified identity binding. Discarded profile JWT/cookie issuance can still occur; never automatically retry an uncertain identity read.
- Improvement list filters for responsibility, creation, and involvement as UUID arrays. Different groups intersect; an ownership union needs separate bounded queries and exact-identity deduplication. Preserve native ownership fields.
- Live active grading options and category detail with all five score definitions, without a private local-skill prerequisite. Category relevance is not a fixed API count cap.
- `show_improvement_gradings` through `ampliflow_improvements`, accepting the exact `improvement_ref` under its live schema. Read `result.improvement_gradings` identity, `impact`, and native UUID-to-score `impact_list` after confirmed creation or grading updates. Score 0 is selected but ungraded; `consistency: "separate_non_atomic_reads"` is not an atomic snapshot or approval evidence. Generic improvement detail omits the map. Missing or mismatched fields remain unverified without automatic write retry.

Package instructions require live catalog and describe discovery before use. Missing contracts are unavailable capabilities, not empty business results. Source agreement alone is not deployed proof.

## Checks still needed with separate authorization

1. Complete fresh OAuth for exactly `https://mcp.ampliflow.com/mcp`; verify reconnect, expiry, denied access, and tenant isolation through the intended client.
2. Capture the authenticated tool inventory privately and run the offline inventory checker. Verify operation mappings, filters, native ownership outputs, and grading definitions through live catalog/describe/query.
3. Run the bounded personal-deviation and grading cases in [TESTING.md](../plugins/ampliflow/TESTING.md), the six focused read workflows, and the router's confirmation and recovery cases. A service principal must not be presented as a human.
4. Verify the exact candidate in a fresh Desktop Work conversation. Desktop import/sync, OAuth, restart, and human UI steps are not performed by the offline build.
5. Before any public-store submission, provision approved reviewer access, run [review.json](review.json), record an approved walkthrough, resolve owner policy/country decisions, and complete authorized portal checks.

No production write, account change, external store action, paid model run, or Desktop restart is authorized by this preparation. Server release, Desktop acceptance, submission, approval, and publication remain separate outcomes.
