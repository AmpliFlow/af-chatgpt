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

## Interpretation

- A current checklist template may differ from the revision used by a historical run.
- Checklist completion, skipped steps, and finalization are separate evidence; prefer normalized values returned by AmpliFlow.
- A rendered or listed document is not proof that its content was reviewed.
- Custom-list field meaning comes from the current definition, not from a similar field name elsewhere.
- Publication does not prove readership; use returned acknowledgement or engagement evidence.
- A recurring year-wheel item is a plan, not proof that the planned activity occurred.
