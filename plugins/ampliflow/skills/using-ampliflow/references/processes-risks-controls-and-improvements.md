# Processes, risks, controls, and improvements

Load this reference for process maps, operational risks, controls, corrective or preventive improvements, and links among them.

## Route

- `ampliflow_processes`: process maps, subprocesses, steps, nodes, connections, layout, and process guidance.
- `ampliflow_risks`: operational risks, scoring choices, process-step links, mitigation, ownership, and lifecycle.
- `ampliflow_controls`: standards, control sets and items, implementation, review, responsibility, evidence metadata, actions, and linked records.
- `ampliflow_improvements`: improvements, workflows, steps, activities, forms, analytics, process impact, and lifecycle.
- `ampliflow_history`: audit history for a supported record after its exact entity identity is known.

## Relationships and order

1. Resolve a process before its subprocesses or steps. Preserve node type and parentage; visual proximity is not a relationship.
2. Resolve risks from the risk domain, then use explicit process-step links to establish process context.
3. Resolve the control set before its control items. Use the unfiltered item population when a coverage denominator matters.
4. Follow control links to risks, processes, improvements, legislation, equipment, pages, files, or actions only when returned by control detail.
5. Resolve an improvement before workflow steps and activity instances. Keep workflow definition, activity instance set, step instance, and task identity distinct.

## Interpretation

- Use stored risk scores as facts. Recalculate only when all current inputs and the applicable formula are known.
- A linked control does not prove the risk is adequately treated.
- File metadata does not prove evidence quality or control effectiveness.
- An improvement's status and impact can depend on workflow and tenant configuration; use current labels and values.
- A process link can express scope or impact without proving causation.
