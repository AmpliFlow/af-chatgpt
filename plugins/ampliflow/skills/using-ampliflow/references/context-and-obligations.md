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

## Interpretation

- Applicability is a recorded assessment, not legal advice or independent proof of compliance.
- A fulfilled customer requirement does not by itself prove customer acceptance.
- Stakeholder interest and influence are context evidence, not automatically risk scores.
- An environmental aspect's process link identifies operational context; significance depends on the current recorded inputs and tenant rules.
- State when source text or supporting evidence is unavailable rather than reconstructing it from titles.
