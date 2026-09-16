# Projects, work, and time

Load this reference for projects, project groups, milestones, tasks, collaboration, project pages or files, and project-related time.

## Route

- `ampliflow_projects`: project identity, portfolio and lifecycle, groups, milestones, membership, tags, status updates, discussions, and project-linked pages or files.
- `ampliflow_tasks`: task identity, assignment, comments, subtasks, attachments, movement, and completion state.
- `ampliflow_timesheets`: time entries, timers, reports, calendar sources, and matching rules.
- `ampliflow_content`: page or document detail after a project result supplies an explicit content link.
- `ampliflow_people`: user or team detail after a current project or task result identifies them.

## Relationships and order

1. Resolve the project before project-scoped tasks, milestones, files, discussions, or time.
2. Resolve a task through its owning project unless the current result already supplies an exact task ref accepted by the described operation.
3. Keep project status, latest narrative update, task completion, and archive or deletion state separate.
4. For time analysis, preserve the project/task association returned by the time entry. A project billing default and a task override are different facts.
5. Follow linked pages, files, users, or teams only when the source result supplies the relationship.

## Interpretation

- A project can be draft, launched, completed, archived, or deleted through distinct lifecycle concepts. Report the returned state rather than collapsing them.
- Missing status updates do not mean the project has no work.
- Unassigned tasks and tasks without dates are explicit gaps, not lookup failures.
- Time entries do not by themselves prove delivery progress or task completion.
