# AmpliFlow submission handoff

**The `0.9.0` production submission draft is not ready for public submission.** Its GitHub marketplace has separate production and beta plugins; this guide applies only to the production ZIP. The normal MCP service is deployed and qualified. Supported-client acceptance, approved media, owner decisions and portal checks remain separate gates.

## Prepared package

- One complete plugin ZIP: all seven skills and references, exact normal MCP connection, icon, listing, release notes, and five positive plus three negative reviewer cases.
- `PORTAL-FIELDS.txt`: generated portal values, missing fields, and ZIP checksum.
- [Reviewer setup and cases](submission/REVIEWER.md) and [machine-readable cases](submission/review.json).
- [Proposed license and policy changes](submission/POLICY-APPROVAL.md), still awaiting owner adoption.
- [Source notes](submission/SOURCES.md) and [acceptance limits](submission/MCP-EVIDENCE.md).

The draft lacks a walkthrough URL and country choice. Support, privacy, terms, website, listing copy, and assets are filled in; their presence is not approval of the proposed policies. Missing values are explicit. Credentials and private evidence never belong in the ZIP or public repository.

## Remaining access and decisions

1. Reuse the existing approved demo access saved privately; no new account or password reset is needed. Confirm the intended ChatGPT test surface and bounded test turns. The agent must verify fresh resource-bound OAuth for the normal endpoint and execute the cases; native browser access is not hosted MCP OAuth. Keep credentials out of chat and attachments.
2. Approve the walkthrough concept and, separately, its destination/visibility before recording or uploading. Use only approved synthetic data and avoid restricted standards text.
3. Verify the new production entry's `ampliflow-production` identity, exact normal-resource binding and live operation contracts described in [MCP-EVIDENCE.md](submission/MCP-EVIDENCE.md). Preserve the existing `ampliflow` beta connection; the two-entry package does not migrate its authorization or prove a production-client pass. No new infrastructure work is required.
4. Choose countries, adopt or revise the proposed rights/policy text, and provide authorized publisher/portal access for scans, domain verification, and attestations. No country scope, legal approval, account access, or store action is inferred.

## Owner portal steps after verified preparation

1. Obtain the exact final `ampliflow-plugin.zip` and verify its checksum against `SHA256SUMS`. Upload only that ZIP at [OpenAI Plugins](https://platform.openai.com/plugins), with the intended organization and verified publisher. Do not upload build reports, checksums, policy drafts, credentials, or a repository source archive.
2. Complete owner-only organization, domain, and authentication steps using the actual draft's values. Enter reviewer credentials only in secure **Review details**. Authorized agents can inspect and fix technical findings; do not bypass challenges.
3. Compare imported values with `PORTAL-FIELDS.txt`, review actual test evidence and the approved walkthrough, complete the required attestations, and explicitly authorize submission. Save the submitted version and confirmation. Approval and publication are later outcomes.

Do not submit the current draft as a tested release. A valid upload, green local checks, or an earlier task completion is not live acceptance.

## Offline build

```sh
python3 -B scripts/check.py
python3 -B scripts/build_submission.py
python3 -B scripts/build_submission.py --answers /absolute/private/path/answers.json
(cd dist && sha256sum -c SHA256SUMS)
```

Inputs are [answers.example.json](submission/answers.example.json) and [review.json](submission/review.json). Outputs are `dist/ampliflow-plugin.zip`, `PORTAL-FIELDS.txt`, `SHA256SUMS`, and `build-report.json`. A separate `dist/ampliflow-beta-plugin.zip` is a beta download and must not be uploaded to the public-store draft. The build preserves source version `0.9.0`, adapts only public listing/review/publication metadata, and copies skills and references byte-for-byte. Rebuild after approved answers or content changes; compare exact bytes before handoff. No upload or attachment is performed by these commands.

Keep all seven skills. Do not restore the obsolete separate JSON-import workflow, assumed five-skill cap, legacy endpoint, or invented approval committees. See [release mechanics](RELEASE.md) for the separate GitHub/Desktop route.
