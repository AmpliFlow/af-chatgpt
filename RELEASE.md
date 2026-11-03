# Coordinated 0.7.0 delivery

This delivery combines the submission/build work with personal-deviation and grading guidance. The preceding public release was `0.6.0`; the starting source manifest was `0.6.1`. Source and ZIP use `0.7.0`. Verify publication and client acceptance through the tagged artifacts and delivery evidence, not this procedure. Before tagging, confirm that the version remains unpublished.

## Release notes

- Read personal deviations through the effective credential principal, live forms, and bounded responsibility, creator, or involvement filters. Separate ownership unions from intersections and preserve partial-result limits.
- Read live tenant impact categories and all five score definitions. Select evidence-supported categories without a fixed category-count cap or a private local-skill dependency.
- Verify persisted improvement impact and category UUID/score values through the native read-only `show_improvement_gradings` operation, with selected-but-ungraded zero and separate non-atomic reads kept explicit. Preserve structured authenticated-identity evidence, unknown tenant binding, and discarded profile JWT/cookie side-effect limits.
- Preserve exact proposal confirmation, immutable approval fields, serial writes, and authoritative uncertain-write recovery. Focused reviews remain read-only.
- Add the complete seven-skill submission kit, deterministic ZIP builder, checksum/report outputs, offline validation, and CI artifact build. Public-store access, policy adoption, reviewer execution, and submission remain separate.

## Included scope

- `.gitignore`, `.github/workflows/check.yml`: exclude runtime/build state and run an offline draft artifact build on pushes/PRs.
- `scripts/check.py`, `scripts/build_submission.py`: validate inputs and build the allowlisted plugin ZIP with source-version parity.
- `plugins/ampliflow/plugin.json`, `skills/using-ampliflow/SKILL.md`, its process/risk/improvement reference, and `skills/reviewing-improvements/SKILL.md`: candidate metadata and routing/grading/ownership instructions.
- `plugins/ampliflow/tests/`: operation contracts, instruction validation, ownership/grading regression checks, and submission-build safety/determinism tests.
- `README.md`, `SUBMIT.md`, `plugins/ampliflow/{README,DISCOVERY,TESTING}.md`, and `submission/`: setup, acceptance cases, reviewer inputs, source notes, and unadopted policy drafts. No private investigation evidence or credentials are included.

## Delivery mechanics

1. Coordinate the backend contracts and deployment with their owner. `get_authenticated_identity` belongs to the users toolset and maps to `ampliflow_people`; ownership filters belong to `ampliflow_improvements`; shared grading definitions map to `ampliflow_projects`; persisted grading read-back uses `show_improvement_gradings` through `ampliflow_improvements`. Identity returns `result.authenticated_identity`; persisted grades return `result.improvement_gradings`. These contracts do not prove an atomic snapshot, human approval, original executor, or write attribution beyond returned evidence. Profile JWT/cookie issuance can occur even when discarded; never automatically retry an uncertain identity read. Validate live schemas before relying on them.
2. Run `python3 -B scripts/build_submission.py`, then `(cd dist && sha256sum -c SHA256SUMS)`. Both build and standalone `scripts/check.py` run deterministic checks. CI only builds/uploads a draft artifact; no release or store workflow is configured here.
3. After explicit delivery authorization, the delivery owner commits the full coordinated source, verifies `0.7.0` is still unpublished, tags `v0.7.0`, and creates the GitHub release with these curated notes and verified artifact bytes/checksums. Do not change versions only in generated ZIPs. Source archives are not the allowlisted submission ZIP.
4. The Desktop route imports/syncs the repository marketplace. The owner must verify the imported source revision and candidate version, fresh beta OAuth, and a new Work conversation after the required Desktop restart. A GitHub tag or built ZIP does not update or prove another Desktop installation.
5. Public-store submission uses [SUBMIT.md](SUBMIT.md). GitHub publication does not authorize portal submission, policy adoption, recording/upload, external contact, production writes, or a Desktop restart.

## Evidence limits

Local tests are instruction and artifact contracts, not model behavior or deployed schema tests. Live identity, UUID filters, form resolution, native ownership fields, grading, OAuth, Desktop acceptance, and the reviewer cases require separate authorized execution. Do not call an unavailable/partial personal read empty or complete, present a service credential as the original human, or report a stored write without authoritative read-back.
