# Unpublished 0.8.0 normal-origin candidate

Source and generated ZIP use `0.8.0`. This is an unpublished candidate, not a release or deployment. Normal-origin TLS and routing are under construction. Source agreement and offline checks do not establish hosted readiness or client acceptance.

## Release notes

- Target the normal resource `https://mcp.ampliflow.com/mcp` under the existing `ampliflow` server name and in all seven skill dependencies.
- Preserve stable dispatcher and operation IDs, six focused read-only workflows, and the router's exact confirmation, privacy, approval-field, and recovery guidance.
- Validate the exact normal resource and reject beta, alternate, credential-bearing, and additional connections. Keep the deterministic allowlisted ZIP, reports, and checksums.
- Require fresh resource-bound OAuth for the new origin. Never reuse or transform beta authorization.

The published `0.7.0` beta artifact remains usable for internal tests and rollback. Do not overwrite its artifacts or retag its release. Use that explicit artifact for beta tests, not a new beta-plugin framework or a fallback in the normal package.

## Offline preparation

1. Run `python3 -B scripts/check.py` and `python3 -B scripts/build_submission.py`.
2. Verify `(cd dist && sha256sum -c SHA256SUMS)`. Source archives are not the allowlisted submission ZIP; never change versions only in generated files.
3. Keep the candidate unpublished until the separately authorized delivery work below is verified. CI builds/uploads a draft artifact only; no release or store workflow is configured here.

## Later delivery, with separate authorization

1. The backend owner delivers the compact stable MCP cutover, CI, and IaC. Verify normal-origin TLS, routing, protected-resource metadata, exact resource-bound OAuth, authenticated tool inventory, catalog/describe schemas, and deployed contract parity. This package does not deploy the service.
2. Preserve the coordinated identity, ownership filters, grading definitions, and persisted grading read-back contracts in [MCP-EVIDENCE.md](submission/MCP-EVIDENCE.md). Missing contracts remain unavailable capabilities, not empty results. Source parity is not runtime proof.
3. After explicit publication authorization, confirm `0.8.0` is still unpublished, commit the complete source, tag `v0.8.0`, and create the GitHub release with these curated notes and verified artifact bytes/checksums. No such action is part of this files-only preparation.
4. For Desktop delivery, import/sync the marketplace and verify the exact source revision and candidate version. Complete fresh OAuth for exactly `https://mcp.ampliflow.com/mcp`, then perform the separately authorized Desktop restart and acceptance checks in new Work conversations. A GitHub release or ZIP does not update another installation or prove acceptance.
5. Follow [SUBMIT.md](SUBMIT.md) for public-store preparation. GitHub publication does not authorize policy adoption, country choices, reviewer provisioning, portal submission, recording/upload, external contact, production writes, or a Desktop restart.

## Evidence limits

Local tests prove instruction and artifact contracts only, not model behavior or deployed schemas. Fresh normal-origin OAuth, tenant isolation, live operations, Desktop acceptance, and reviewer execution remain pending. Legal, country, policy, store approval, and recording boundaries are unchanged.

Tasks 1236 (entity links) and 1238 (training semantics) are capture-only and are not implemented by this candidate.
