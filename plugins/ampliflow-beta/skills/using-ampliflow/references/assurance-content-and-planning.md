# Assurance, content, and planning

Load this reference for checklists, pages, documents, custom lists, news, announcements, or year wheels.

## Route

- `ampliflow_checklists`: checklist templates, reusable steps, actual runs, schedules, reports, and lifecycle.
- `ampliflow_content`: pages, folders, documents, rendering, and editor assets.
- `ampliflow_custom_lists`: list definitions, fields, items, files, imports, and lifecycle.
- `ampliflow_communications`: news, comments, reactions, acknowledgements, and announcements.
- `ampliflow_year_wheels`: year wheels, templates, categories, scheduled items, recurrence, and lifecycle.
- `ampliflow_history`: audit history after the exact supported record identity is known.

## Relationships and order

1. Keep a checklist template, template revision, schedule, recurrence, and actual checklist run distinct.
2. Resolve folders or lists before child pages, documents, fields, or items when the described operation is parent-scoped.
3. Resolve a custom-list definition and its fields before interpreting item values.
4. Resolve a year wheel before categories and items; preserve template identity separately from a tenant wheel.
5. Resolve a communication before engagement, acknowledgement, comment, or reaction details.

## Annual management-plan review

1. Resolve one exact year wheel before reading categories or items. If names are ambiguous, show the candidates and wait for the user to select one.
2. Default to at most 20 categories, 50 items, and 10 focused item-detail reads. Stop at the first reached ceiling, state coverage, and ask before another bounded batch.
3. Discover the exact wheel, category, item, and option reads from the live year-wheel catalog. Build arguments from current schemas and preserve wheel, template, category, item, owner, and recurrence identities separately.
4. Report returned dates, recurrence definitions, categories, and owners. Flag missing ownership only when an owner field was returned empty; label an omitted or failed field "not verified."
5. Treat same-date or overlapping returned ranges as possible collisions, not scheduling errors. Identify a coverage gap only against an explicit expected activity supplied by the user or a returned template/category requirement.
6. Separate recorded facts, possible collisions or supported gaps, and recommendations. Preserve successful sections when another category or item read is partial or unavailable.

A scheduled item is not completed work. A recurrence rule is not an expanded occurrence list, and a date is not reminder evidence. State that task linkage, completion state, reminders, or occurrence expansion are unsupported when the returned contract omits them. This workflow is read-only: do not create, update, delete, or apply year-wheel templates.

## Interpretation

- A current checklist template may differ from the revision used by a historical run.
- Checklist completion, skipped steps, and finalization are separate evidence; prefer normalized values returned by AmpliFlow.
- A rendered or listed document is not proof that its content was reviewed.
- Custom-list field meaning comes from the current definition, not from a similar field name elsewhere.
- Publication does not prove readership; use returned acknowledgement or engagement evidence.
- A recurring year-wheel item is a plan, not proof that the planned activity occurred.
