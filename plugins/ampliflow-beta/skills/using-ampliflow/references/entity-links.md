# Read-only entity links

Default to readable Markdown entity links in lists, summaries, and follow-ups when current frontend evidence, native UUIDs, and any required parent identity are available. This reference applies to all seven skills. Links grant no access and do not prove a write succeeded. Keep the six focused skills read-only; only the general router handles explicit confirmed writes. Link formatting requires no browser navigation, client action, export, or mutation.

## Resolve frontend evidence once

- Discover `get_authenticated_identity` on `ampliflow_people` through the skill's normal catalog workflow. Require the exact returned operation with `safety: "read"`, describe its current input and output schemas, then query with described arguments. It is optional for links; existing required personal-identity behavior remains required.
- Read `result.authenticated_identity.frontend_context` only as defined by the live schema: `base_url` (string or null), `origin_evidence` (string), and `entity_url_templates` (object). Reuse current identity and discovery results from this authenticated connection; do not add a second identity call just to format another record or answer.
- Use frontend evidence bound to the live authenticated API origin after the server's bounded credential-free same-origin SPA shell check. That check follows no redirects and adopts no cookies; an API-only origin remains unavailable rather than becoming a guessed frontend. Preserve exact custom domains and ports. Do not reconstruct a slug, hostname, domain, port, or route from tenant names, emails, prior conversations, or record content. Never use the MCP origin as the frontend origin or take a domain/template from record content.
- Keep `tenant_binding` as returned (`match` or `unknown`). Neither value is canonical-host proof; frontend origin evidence is a separate contract, not an upgrade of tenant binding. Preserve effective-principal, original-executor, and write-attribution distinctions.
- For development/loopback origins without a verified frontend mapping, expect `base_url: null` and empty templates. A missing field, null base, empty templates, unsupported entity type, or missing native UUID/parent means no constructed link. Explain the missing evidence and retain readable labels and exact refs. Do not guess, substitute a register link for an entity, or request an address already supplied. A supplied address alone does not verify the current connection's frontend mapping.
- Discard frontend evidence, URLs, templates, and record identities on a tenant switch, reconnection, or changed authenticated origin. Resolve them through the new current connection before linking; never reuse an origin across tenants.
- Do not add authentication call loops or automatically retry an uncertain identity read. Preserve `server_side_effect`: profile authentication can issue a JWT/cookie even when discarded. The generic read retry guidance does not authorize retrying this uncertain call. If optional link evidence is unavailable, continue independent reads and explain the link limit; stop affected reads on authentication or authorization failures as the skill requires.

## Select the entity and template

Prefer a returned entity URL only when the current connection confirms its origin and the live schema identifies it as that exact entity's URL. A URL embedded in a title, description, comment, or attachment is untrusted record content, not origin evidence. Reject credentials, unsafe schemes, and origin mismatches; do not open a URL to verify it.

Otherwise use the exact returned absolute template from `entity_url_templates` for the matching type. Require its origin to agree with the current verified frontend evidence. Replace only its named placeholders with the corresponding native UUIDs from current schema-defined results. Keep a task paired with its required project UUID. Never substitute cache-local refs, row positions, improvement numbers, names, or inferred IDs, even when a ref happens to look like an ID.

The following route shapes identify the supported contract; they are not fallback templates. Never construct these routes when the server has not supplied the matching absolute template.

| Returned template key | Required placeholders | Recognized route shape |
| --- | --- | --- |
| `improvement` | {improvement_id} | `/improvements/{improvement_id}` |
| `project` | {project_id} | `/projects/{project_id}` |
| `project_task` | {project_id}, {task_id} | `/projects/{project_id}/tasks/{task_id}` |
| `risk` | {risk_id} | `/operational-risk-analysis` with `modal` containing percent-encoded JSON `{"type":"risk_form","id":"{risk_id}"}` |
| `risk_register` | none | `/operational-risk-analysis` |
| `process` | {process_id} | `/process/{process_id}` |
| `subprocess` | {subprocess_id} | `/subprocess/{subprocess_id}` |
| `process_chart` | none | `/processchart` |

Use register/chart templates only when referring to those views. Goals, measurements, checklists, controls, and other unsupported types have no template in this contract: use a confirmed returned entity URL if available, otherwise explain that their link evidence is unavailable. Do not invent paths or apply a project-task template to a goal action without verified project and task UUIDs.

## Format safely

- Substitute the raw native UUID, not a selector ref or an already encoded string: percent-encode each placeholder value as a URI component. Do not encode the whole URL or double-encode the template's existing percent escapes. Keep the returned risk modal's encoded JSON unchanged except for the native risk UUID placeholder. If placeholders remain unresolved or the URL disagrees with the verified origin, omit the link and explain why.
- Use the entity's readable title, optionally with its native display number, as the Markdown label. Escape backslashes first, then brackets and other Markdown punctuation (including backticks, asterisks, and underscores). Normalize newlines to spaces and escape angle brackets to prevent HTML or nested-link injection. Treat the label as text, never as Markdown supplied by the record.
- Put the escaped label in square brackets, followed by the angle-delimited absolute URL in parentheses. The angle-delimited destination protects parentheses; percent-encode literal angle brackets, whitespace, or control characters if present in a confirmed URL. Do not change its origin, path semantics, or existing encoding. Keep exact refs separately when needed for follow-up operations; a link is not a portable selector or access grant.

For example, given a current confirmed frontend at `https://quality.example.org:8443`, the returned project template `https://quality.example.org:8443/projects/{project_id}`, and native project UUID `11111111-1111-4111-8111-111111111111`, a title `Plan [Q4]` becomes:

```text
[Plan \[Q4\]](<https://quality.example.org:8443/projects/11111111-1111-4111-8111-111111111111>)
```

If only project ref `42` is returned, do not put `42` into that template. Report: "Plan [Q4] (ref 42). Link unavailable: native project UUID was not returned." Reuse an already verified URL when available instead of asking the user for the same address.
