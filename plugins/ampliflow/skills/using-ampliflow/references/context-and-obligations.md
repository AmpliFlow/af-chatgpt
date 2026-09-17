# Context and obligations

Load this reference for customers, customer requirements, stakeholders, legislation, or environmental aspects.

## Route

- `ampliflow_customers`: customer identity, industries, contacts or fields, and lifecycle.
- `ampliflow_customer_requirements`: requirements, customer association, fulfillment, options, and lifecycle.
- `ampliflow_stakeholders`: interested parties, interests, influence, options, and lifecycle.
- `ampliflow_legislation`: legal or regulatory records, classifications, ownership, applicability, and lifecycle.
- `ampliflow_environment`: environmental aspects, impacts, significance inputs, process links, options, and lifecycle.
- `ampliflow_processes` or `ampliflow_controls`: process and control context only through explicit returned links.

## Relationships and order

1. Resolve a customer before customer-scoped requirements when the relationship is in scope.
2. Resolve each requirement, stakeholder, legislation record, or environmental aspect in its owning domain.
3. Read tenant option labels before interpreting classifications, applicability, fulfillment, influence, or significance.
4. Follow process, control, owner, or customer links only from current results and preserve both source and target refs.
5. Keep requirement, obligation, stakeholder expectation, and internal control distinct even when their wording overlaps.

## Obligation gap review

1. Ask the user to choose legislation, customer requirements, environmental aspects, or a combined review when the intended sources are unclear.
2. Review at most 10 selected records per source by default. Use the first bounded page, then ask before reading another batch.
3. Discover the exact list, detail, and option reads from each owning dispatcher's live catalog. Use current tenant option labels before interpreting a field.
4. Keep legislation, customer-requirement, and environmental-aspect findings in separate report sections. Do not merge similar wording into one obligation.
5. Flag missing ownership, applicability, review data, fulfillment evidence, or links only when a successful response returns the relevant field and its value supports that finding. If the field was omitted, redacted, or unreadable, label it "not returned" instead of calling it a gap.
6. Follow a process, control, customer, or owner link only when the source response returns it. Never infer a control or evidence mapping from similar names.

Minimize customer terms and sensitive details in the answer. Prefer a short finding and exact record ref over copied contract text. Omit contacts, internal identifiers, and unrelated fields unless the user needs them for the stated review.

## Interpretation

- Applicability is a recorded assessment, not legal advice or independent proof of compliance.
- A fulfilled customer requirement does not by itself prove customer acceptance.
- Stakeholder interest and influence are context evidence, not automatically risk scores.
- An environmental aspect's process link identifies operational context; significance depends on the current recorded inputs and tenant rules.
- State when source text or supporting evidence is unavailable rather than reconstructing it from titles.
- Never assert legal compliance or noncompliance. Report recorded gaps and unavailable evidence, and recommend qualified legal review when legal interpretation is required.
- Keep ambiguous matches unresolved until the user selects a record. Preserve successful source results when another source is unavailable, partial, or saturated, and state the exact coverage limit.
