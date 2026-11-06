# Submission requirements checked 2026-11-02

The current submission is a complete plugin ZIP, not the older separate portal-JSON workflow. These are preparation notes; the authenticated portal was not accessed.

| Official source | Requirement used here |
| --- | --- |
| [Upload and submit](https://developers.openai.com/plugins/deploy/submission) | Upload a ZIP with root plugin.json, mcp.json, assets, and skills. Verify publisher access, connect the single remote MCP server, complete domain verification and OAuth, resolve required scans, provide reviewer access and a video, attest and submit. Publication follows approval. |
| [Submission field reference](https://developers.openai.com/plugins/deploy/submission#automatically-provide-submission-and-review-information) | Display name and subtitle: 30 characters each; long description: 4000; developer name: 80. Four public HTTPS URLs: website, support, privacy, terms. Up to three unique starter prompts of 128 characters. Square icon: at least 48 pixels, at most 4096 for raster, at most 5 MiB. |
| [Review fields](https://developers.openai.com/plugins/deploy/submission#configure-onboarding-review-and-publication) | Exactly five positive and three negative cases for initial MCP review. Package uses review.test_cases.positive/negative with prompt and expected_behavior, plus demo_recording_url; country codes and release notes belong under publication. Credentials and reviewer instructions are prohibited in ZIP metadata. |
| [Build skills](https://developers.openai.com/plugins/build/skills) | Package skills with their supporting references and MCP dependencies. No universal five-skill limit was established in this current guide; retain all seven existing skills instead of inventing a new consolidation. |
| [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines) | Truthful capabilities, protected data, accurate tool behavior and security, accessible policies and reviewer flow. Server-side safety and permissions remain required; skill instructions alone do not establish them. |
| [Portable plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json) | Existing Agent Plugins 1.0 package format. OpenAI-specific review/publication metadata goes under extensions.com.openai; not all public-submission requirements are expressed by the portable schema. |

## Removed assumptions

- The normal resource is `https://mcp.ampliflow.com/mcp`. The path selects the channel: both domains' `/mcp` URLs serve production and `/mcp-beta` URLs serve beta. Version `0.10.0` uses production identity `ampliflow` and beta identity `ampliflow-beta`; beta keeps `.cc/mcp-beta`. Migrating older identities may require fresh connections and sign-in. Published earlier artifacts remain unchanged. Configuration and version labels do not prove an installed workspace's resource binding or client acceptance.
- A separate `chatgpt-app-submission.json` import is unnecessary for the documented ZIP route. Its [published schema](https://developers.openai.com/plugins/schemas/chatgpt-app-submission.v1.json) still exists, but uses different fields and does not establish current portal import support. Do not generate an empty tools object just to pass that schema.
- No current source reviewed establishes mandatory internal committees, separate departmental signatures, a customer pilot, global-versus-EU project residency, or a universal five-skill cap. They are not added as submission gates here. Actual account eligibility and portal findings still control the real submission.
- Task completion labels and local contract tests are not runtime acceptance evidence. The agent must execute the reviewer cases with the intended account and client before reporting a passing candidate; the submitter is not asked to perform the technical test run.

## Evidence limits

The 2026-11-06 delivery qualified normal-service HTTPS, fresh resource-bound OAuth and the 28-tool inventory, and published plugin `0.8.0` with verified release bytes. A human demonstrated a working Desktop project read, but a later screenshot shows the installed version label with a beta resource binding. Neither fact proves normal-client acceptance or all reviewer cases. Existing approved demo access is saved privately; a new reviewer account is not required. Authenticated publisher access, domain verification, complete client-case evidence and approved media remain unverified. Local contract tests validate package instructions and build behavior, not model behavior or the deployed server's full security contract. See [MCP-EVIDENCE.md](MCP-EVIDENCE.md) for the precise limits.

Existing license restrictions and live terms' automation prohibitions are concrete unresolved rights questions, described in [SUBMIT.md](../SUBMIT.md). No policy or license was changed or approved by this preparation.
