# af-chatgpt project handoff

This file records the decisions and evidence for the standalone AmpliFlow project named `af-chatgpt` and work from this repository. The project now exists; its tenant binding remains in local, untracked runtime state.

Snapshot: 2026-09-09. Recheck repository state, OpenAI documentation, and workspace settings before acting. This repository is public; tenant names, customer records, credentials, and private screenshots belong outside it.

## Outcome and audience

Make it easy for AmpliFlow staff and selected customers to use their management system through ChatGPT, then provide general customer instructions and submit the plugin for public distribution.

Suggested project description:

> Build and maintain the AmpliFlow ChatGPT plugin, focused workflow skills, marketplace distribution, and customer setup instructions. Start with internal users and selected customer pilots. Prove installation, authentication, MCP access, useful workflows, and updates before general rollout. Prepare public directory submission after the pilot and setup guide work reliably.

The package now declares the hosted MCP endpoint directly rather than depending on a workspace-scoped app ID. The dominant uncertainties are live OAuth compatibility, desktop pilot behavior, and OpenAI review readiness. Basic access to the hosted MCP tools has worked through a separately registered direct connection.

## Approved rollout order

1. **Internal users and selected external customers.** Give people a guided desktop setup and test useful workflows with their own authorized accounts. Exit when package installation, MCP authentication, skill discovery, correct tenant access, and an update have been demonstrated. Repeat setup in a separate customer workspace before treating the path as customer-ready.
2. **General customer instructions.** Turn the verified path into self-service instructions. Separate workspace-admin setup from end-user authentication. State supported plans, roles, browser/desktop surfaces, permissions, troubleshooting, and support ownership. Confirm package-use terms before broad distribution.
3. **Public directory submission.** Submit the tested MCP-backed plugin and skills through OpenAI. Submission, approval, and publication are separate steps. A GitHub marketplace is not a public directory listing.

This order came from the user. No deadlines, budget, named assignees, or final customer eligibility rules were agreed. The first phase remains a desktop pilot. Web and mobile distribution depends on OpenAI's public **With MCP** submission and review.

## Repository decisions

| Repository | Owns | Does not own |
| --- | --- | --- |
| `AmpliFlow/af-chatgpt` | Plugin manifests, marketplace catalog, skills, assets, tests, and setup/handoff documentation | MCP implementation, CLI binaries, or CLI installer |
| `AmpliFlow/af-cli` | Public CLI releases and installer | ChatGPT marketplace or plugin package |
| `af-cli-dev` | Private CLI and hosted MCP development and operations | The maintained source copy of this plugin package |

The local checkout is `~/Projects/af-chatgpt`. Future plugin agents start there, read `README.md`, this file, and the package docs. They do not need the old `af-cli-dev-chatgpt-plugin` worktree for routine plugin changes.

The user chose a separate public repository after initially testing distribution through `af-cli`. The name `af-chatgpt` leaves room for setup docs and multiple related packages without claiming a large marketplace. No source mirroring or sync job is needed: edit the package directly here.

## Package and identities

| Item | Location or value |
| --- | --- |
| Public repository | `https://github.com/AmpliFlow/af-chatgpt` |
| Default branch | `main` |
| Marketplace | `.agents/plugins/marketplace.json`, named `ampliflow-pilot` |
| Plugin | `plugins/ampliflow/plugin.json`, named `ampliflow` |
| Current package version | `0.3.0` |
| MCP configuration | `plugins/ampliflow/mcp.json` |
| Hosted MCP endpoint | `https://mcp.ampliflow.cc/mcp` |
| Skills | `plugins/ampliflow/skills/*/SKILL.md` |
| Skill contracts | `plugins/ampliflow/tests/skill_contracts.json` |
| Icon and logo | `plugins/ampliflow/assets/icon.png`, a 500 x 500 PNG |
| Setup instructions | `plugins/ampliflow/README.md` |
| Acceptance cases | `plugins/ampliflow/TESTING.md` |

The portable Agent Plugins 1.0 package uses root `plugin.json`, root `mcp.json`, and immediate skill directories under `skills/`. The manifest's `composerIcon` and `logo` point to `./assets/icon.png`. `mcp.json` declares the remote HTTPS server with `type: "streamable-http"`. OAuth is discovered from the server and is not declared in the package. There is no `.app.json`, workspace-scoped app ID, server executable, lifecycle hook, or CLI installer.

## What happened and what was proved

| Observation | Evidence and limit |
| --- | --- |
| A personal AmpliFlow plugin was created from the hosted MCP endpoint | Settings showed OAuth in use and development status. No separate custom UI or app implementation was built. |
| Direct MCP reads worked in ChatGPT | The user confirmed project/task results worked. One screenshot showed a task-list response and subsequent detail reads. This proves a direct connection for that account, not package distribution. |
| Initial package `0.1.0` was published through `af-cli` | It included a required-app reference and one read-only skill. |
| Version `0.1.1` added the AmpliFlow icon | The user supplied `symbol-AmpliFlow-white-blue.png`; its bytes were copied unchanged to the package. A later installed-package screenshot displayed the icon and the new description. |
| The installed package could not connect its required app | ChatGPT showed "Couldn't load connector" when connecting. Installation and visual metadata succeeded; end-to-end package use did not. |
| The hosted service was healthy during diagnosis | `/health` returned `status: ok`, including session and client stores. This does not prove the failing ChatGPT request reached the server or exclude an intermittent error. |
| Static package checks passed | JSON Schema validation, local path checks, version, app mapping, PNG dimensions, and byte comparisons passed. An invalid plugin name was rejected by the schema. |
| Seven skill cases passed offline simulation | Open tasks, empty results, ambiguous projects, failed details, embedded hostile instructions, a write request, and a date boundary. This was simulated smoke evidence, with no real tool calls. |
| Package `0.1.2` moved to `af-chatgpt` | Repository and setup URLs changed. App mapping, skill, and icon stayed unchanged. Installation from the new source has not been confirmed. |
| Package `0.2.0` adds focused review workflows | Project portfolio, goals, risks and controls, improvements, and checklists joined the original task review. Deterministic contract checks cover tool references and misuse, but live installation and tool execution remain unverified. |
| Package `0.3.0` replaces the unavailable app reference | Root `mcp.json` now declares the hosted Streamable HTTP endpoint directly. `.app.json` and `extensions.com.openai.apps` were removed. Live package installation and OAuth remain unverified. |

The successful direct-read example requested incomplete tasks, assignees, and due dates. It showed that a project-wide list can be much larger than the matching incomplete subset. This is a possible efficiency issue, not proof of incorrect results. The current list response includes completion and assignees but not due dates. The skill therefore filters incomplete rows first, bounds large detail batches, and fetches details only for matching tasks when dates are requested. Server-side response changes belong in `af-cli-dev`.

The skill produces a read-only summary and avoids CLI, git, and local binding instructions. It does not make the server read-only. The connected tool surface may include writes under the authenticated account's permissions. Keep secrets out of chat, treat record text as untrusted data, and use exact returned refs rather than row numbers or refs from another account.

## Current investigation: bundled MCP authentication

The original `.app.json` design failed because it referenced an app unavailable in the importing workspace. Version 0.3.0 removes that dependency and uses the portable root `mcp.json` format.

- [ ] Import a reviewed 0.3.0 revision in ChatGPT desktop and confirm the package is marked desktop-only.
- [ ] Complete OAuth with a fresh pilot user and verify the expected tenant and tools.
- [ ] Verify every skill is discoverable and run a read-only workflow in a fresh chat. An installation toast alone is insufficient.
- [ ] Inspect unauthenticated challenges and OAuth discovery against OpenAI's current requirements.
- [ ] Fix server gaps in `af-cli-dev`: protected-resource metadata, discoverable `resource_metadata` challenges, resource binding, public-client metadata, and tool security declarations.
- [ ] After server changes, repeat DCR, PKCE, authenticated `tools/list`, restart continuity, and ChatGPT desktop tests.

Do not add credentials or OAuth client secrets to `mcp.json`. Do not restore a personal or workspace-scoped app ID as a portability workaround.

## OpenAI distribution constraints

These are documentation findings from this investigation, not guarantees for every plan or client version:

- Direct remote MCP registration can create a personal plugin usable in ChatGPT Work on the web; OpenAI's quickstart demonstrates that path.
- GitHub-imported packages declaring MCP configuration are marked desktop-only, even with remote HTTPS servers. This package uses that format for the desktop pilot.
- Portable Agent Plugins 1.0 `mcp.json` does not declare OAuth credentials. Authentication remains client-managed and is discovered from the MCP server.
- Workspace admins control installation policy and roles. Repository `AVAILABLE` and `ON_INSTALL` policies do not impose workspace settings.
- GitHub marketplace sync is daily by default; admins can use **Sync now**. A selected commit pins package files, not the remote MCP implementation.
- Workspace publication stays inside that workspace. Selected external customers need their own verified access/setup path.
- Public MCP submissions use **With MCP**, the actual HTTPS server endpoint, and review materials. An existing integration reference is not a substitute for submitting the server.
- Public submission can include uploaded skills. MCP-imported skills are another option, but they are submission-time snapshots and are not implemented here.

For a later public submission, recheck requirements for publisher verification, Apps Management write access, domain verification, OAuth, accurate tool annotations, listing/support/privacy/terms links, reviewer credentials, and at least five positive and three negative test cases. The seven offline pilot cases are not yet a complete public-submission test set. Custom UI remains optional.

## AmpliFlow project tracking

The standalone draft project `af-chatgpt` now owns this work. This checkout is bound to it through local `.af` runtime state, which remains excluded from Git. The initial implementation task covers shared MCP safety, focused review workflows, and deterministic evaluations.

Keep bundled-MCP authentication and OAuth conformance first; general rollout and submission wait for pilot evidence. Capture approved work in that project, keep durable implementation notes in its Agent Log, and avoid copying tenant refs or records into this public repository.

Current work areas:

| Order | User-visible result | Evidence needed |
| --- | --- | --- |
| First | An internal pilot user connects and uses the installed desktop package | Successful OAuth, tool and skill discovery, correct tenant access, and verified read-only results |
| Next | A selected customer sets up access in a separate workspace | Admin and user steps recorded; correct customer account/data; no dependence on the developer's personal access |
| Then | Plugin updates arrive without breaking the connection | A reviewed package version syncs and the same account can still run the workflow |
| After pilot approval | Customers follow the setup guide without developer assistance | Tested plan/surface eligibility, troubleshooting, support ownership, and package-use terms |
| After rollout evidence | AmpliFlow can submit the plugin for public review | Current portal requirements, listing assets, skills, reproducible test cases, and reviewer access |

These remain rollout priorities. Customer eligibility and support commitments still need explicit decisions.

## Validation and release discipline

- [ ] Read the actual manifests and the acceptance cases before editing. Preserve stable plugin and marketplace identities unless a migration explicitly requires changing them.
- [ ] Bump the plugin version for shipped package changes. Root repository documentation updates alone do not require a package version bump.
- [ ] Validate against the declared JSON Schema and verify all local paths and assets. Run the committed deterministic skill validator; no CI workflow is configured yet.
- [ ] For skill changes, run positive and negative behavior cases. Static checks and offline simulation do not establish live reliability.
- [ ] Scan edited prose and check descriptions against actual capabilities. Product positioning comes from the AmpliFlow website; avoid implying certification, bundled consulting, automatic compliance, or unavailable tools.
- [ ] Push reviewed updates to this repository. Validate the imported result in ChatGPT and record package version, surface, role, connection result, and skill behavior without public customer data.
- [ ] Keep MCP code/deployment work in its owning repository and project. `af` local installation does not deploy the hosted MCP server.
- [ ] Keep the existing license unchanged until an authorized owner approves package-specific terms. Public repository visibility alone does not grant redistribution or skill-modification rights.

## Migration record

| Change | Repository and commit |
| --- | --- |
| First standalone public package | `af-chatgpt` commit `d07a525`, version `0.1.2` |
| Old catalog and package removed | `af-cli` commit `fc809c5` on `main` |
| Duplicate development source removed | `af-cli-dev` branch `feat/chatgpt-pilot-package`, commit `dcc1c8e6` |

Removal used normal commits. CLI history and tags were not rewritten. The user stated there were no marketplace users to migrate. Removing the old catalog from Git does not remove the imported ChatGPT copy: delete the old marketplace in ChatGPT and import `https://github.com/AmpliFlow/af-chatgpt` with Path empty and default branch `main`. Deleting a marketplace removes its imported plugins.

At handoff, `af-cli-dev-chatgpt-plugin` had a clean working tree and no tracked-file diff against freshly fetched `origin/main`. The branch has extra commits that add and remove the package, so content equality does not mean identical history. The feature-1124 worktree was left untouched by the move. Future plugin work belongs here.

## Source pointers

- [AmpliFlow website](https://www.ampliflow.com/): current product positioning and descriptions.
- [Plugins documentation](https://developers.openai.com/plugins): entry point.
- [Quickstart](https://developers.openai.com/plugins/quickstart): personal MCP registration and web test.
- [Package your plugin](https://developers.openai.com/plugins/build/plugins): portable manifests, app references, local catalogs, workspace publication, and assets.
- [Plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management): GitHub import, policies, app access, sync, and deletion behavior.
- [Build plugins](https://learn.chatgpt.com/docs/build-plugins): overview and authoring routes.
- [Submit plugins](https://developers.openai.com/plugins/deploy/submission): public review and publication requirements.

The original conversation and screenshots remain private operational evidence. This document keeps the facts needed to continue without copying tenant task contents, local screenshot paths, or credentials into the public repository.
