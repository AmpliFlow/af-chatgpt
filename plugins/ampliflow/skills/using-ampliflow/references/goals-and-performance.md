# Goals and performance

Load this reference for goals, goal hierarchies, measurements, KPI targets, progress, or action coverage.

## Route

- `ampliflow_goals`: goals, parent-child relationships, measurements, progress values, task lists, and goal or measurement action plans.
- `ampliflow_kpis`: standalone KPIs, targets, progress, options, and lifecycle.
- `ampliflow_people`: responsible users or teams when current performance results supply their identities.
- `ampliflow_projects` or `ampliflow_tasks`: delivery evidence only when an action or task result explicitly links to those records.

## Relationships and order

1. Determine whether the user means a goal measurement or a standalone KPI; do not treat the terms as interchangeable.
2. Resolve the goal before its measurements, and a measurement before its progress history or task list.
3. Preserve parent and child goal refs when reviewing hierarchy.
4. Resolve a KPI before its targets or progress entries.
5. Read action coverage from the owner returned by AmpliFlow. Keep goal-owned and measurement-owned actions distinct.

## Interpretation

- Empty progress history means no recorded values, not zero performance.
- Do not calculate percentage progress when baseline equals target.
- Do not assume that a larger value is better; direction and target semantics must come from current records.
- Show the date of the newest evidence. Call it stale only when the user supplies a threshold or policy.
- Report returned statuses and tenant option labels without substituting generic labels.
