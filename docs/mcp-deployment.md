# MCP servers and deployment

The plugin, hosted MCP services and workspace installation have separate delivery paths. Publishing this repository does not deploy a server or update an installed workspace connection.

## Production and beta endpoints

The request path selects the channel, not the domain alone. There are two service instances with four supported resource URLs:

| Resource URL | Channel | Use |
| --- | --- | --- |
| `https://mcp.ampliflow.com/mcp` | Production | Default for this plugin and new production clients |
| `https://mcp.ampliflow.cc/mcp` | Production | Compatibility URL, not beta |
| `https://mcp.ampliflow.com/mcp-beta` | Beta | Explicit beta configuration for new clients |
| `https://mcp.ampliflow.cc/mcp-beta` | Beta | Existing beta clients |

Plugin `0.8.0` declares only the first URL in [mcp.json](../plugins/ampliflow/mcp.json). Published `0.7.0` declares the existing `.cc/mcp-beta` URL. Neither package silently falls back to another channel.

Each exact URL is a separate OAuth resource, including aliases served by the same instance. A channel or resource change requires fresh resource-bound OAuth; do not copy, reuse or transform another resource's authorization. Discover the authorization server from the selected resource's metadata. Production uses issuer `https://mcp.ampliflow.com`; beta retains issuer `https://mcp.ampliflow.cc`, including for the `.com/mcp-beta` resource. Do not redirect authenticated MCP requests across domains.

## Hosting and deployment ownership

| Surface | Owner and source of truth |
| --- | --- |
| Plugin manifests, marketplace, skills, packaging and client acceptance | This repository: [release](../RELEASE.md), [testing](../plugins/ampliflow/TESTING.md) and [submission](../SUBMIT.md) guides |
| Hosted MCP implementation, image build and qualification | [af-cli-dev](https://github.com/AmpliFlow/af-cli-dev), especially `.github/workflows/mcp-deploy.yml` and `mcp-promote.yml` |
| Routing, certificates, service units, private state, limits, deployment receivers and recovery | [ampliflow-iac deployment runbook](https://github.com/pbjorklund/ampliflow-iac/blob/master/docs/mcp-server-deployment.md) |

The implementation and IaC repositories require their own access. Follow the authoritative IaC runbook for execution rather than copying deployment commands into this package.

Both instances run on the existing MCP guest, not separate machines. Beta service `af-mcp` uses application/listener ports `8080/9000`; production service `af-mcp-stable` uses `8081/9001`. Receiver ports are internal, not public client endpoints. Each instance has separate deployment authority and private OAuth/reference/approval state. Never copy session or approval databases between channels. Shared hosting is not high availability or isolation from guest compromise.

The qualified configuration bounds each instance to one CPU, 640 MiB memory, a 512 MiB Go memory limit and eight concurrent requests. Logs distinguish both container names under the `af-mcp` job. These are configuration facts to verify after deployment, not permanent capacity guarantees.

## Server release flow

1. Approved relevant changes on `af-cli-dev/main`, or an authorized manual dispatch, run `mcp-deploy.yml`. It builds and publishes beta, deploys an immutable digest and qualifies both beta resource URLs, including retained-session continuity and fresh OAuth.
2. Production requires the separate `mcp-promote.yml` workflow with the successful `beta_build_run_id`. It selects matching source/CI/release evidence, copies the tested image manifest without rebuilding, promotes the exact digest and verifies both production aliases and unchanged beta.
3. Ordinary stable-registry notifications do not deploy production. The production receiver requires its separate promotion authority. A workflow/environment name is not itself evidence of human approval.
4. Record source, workflow run/attempt, selected and running digest, qualification and previous-image recovery evidence. Inspect failed or uncertain operations before another dispatch; never assume an unacknowledged promotion did not apply.

Do not deploy by changing this plugin's URL, retagging an unqualified image or running broad infrastructure provisioning. Changes to services, networking, credentials or production promotion retain their applicable execution approval. Recovery restores only the approved affected image/configuration, preserves private state and does not automatically resume a paused receiver. The IaC runbook owns the exact recovery procedure.

## Health and client diagnosis

On either domain, `/health` selects production and `/health-beta` selects beta. These read-only checks use normal certificate verification:

```sh
curl --fail --silent --show-error https://mcp.ampliflow.com/health
curl --fail --silent --show-error https://mcp.ampliflow.com/health-beta
```

A healthy response proves neither OAuth, tool availability nor a working installed plugin. Compare the served version with the intended deployment evidence, then verify exact-resource OAuth, authenticated inventory, live operation schemas and representative reads. Do not bypass TLS errors or substitute beta to make a production check pass.

For ChatGPT, inspect the workspace installation's actual MCP URL as well as its displayed package version. GitHub publication does not automatically synchronize a workspace marketplace or replace an existing connection. Versions `0.7.0` and `0.8.0` reuse plugin name `ampliflow`, marketplace name `ampliflow-pilot` and MCP server key `ampliflow`. The displayed version alone therefore does not establish which resource the workspace uses. A retained binding/cache/override must be investigated, not assumed from the version label.

Preserve working clients and their authentication. Do not rename, uninstall, reset, add a duplicate connection or restart an active client without the applicable owner decision. After the authorized change, verify fresh OAuth and the actual workflows in new Desktop **Work** conversations. SDK checks and a successful beta read are not production-client acceptance.

## Verified checkpoint and remaining work

As checked on 2026-11-06:

- Plugin `0.8.0` is published from `1a122842e631a067c9204e7c0a173caff5f3d64b`. Its ZIP SHA-256 is `36b0157dcd6b1eb55ffb44cf8292ed873d275529fe95c053e584d9a0eeb0f71a`.
- Hosted CLI `14.2.4` was qualified on production and beta at image digest `c9c811aeb8747535986cf5e8725c9a23d9ae3ee4e9b8c6200df09e1889eb0170`, with exact-resource OAuth and 28-tool inventories. All four health URLs returned verified HTTPS 200 during this documentation check. Infrastructure delivery is complete.
- The user demonstrated a working Desktop project read, but a later screenshot showed version `0.8.0` still bound to `.cc/mcp-beta`. No complete normal-resource client acceptance is recorded. The proposed production/beta marketplace split is not an implemented feature or an approval to change the working entry.

Remaining client-case, persisted-field/recovery, recording, country/policy and publisher requirements are tracked in [MCP acceptance status](../submission/MCP-EVIDENCE.md) and [SUBMIT.md](../SUBMIT.md). Keep credentials, raw OAuth state, private traces, screenshots and tenant records outside this public repository. Preserve private delivery evidence separately; do not recreate resolved infrastructure work because an older task log or snapshot described it as pending.
