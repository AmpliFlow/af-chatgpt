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

## Timesheet completion review

1. Require a clear start date, end date, and user, project, or explicitly approved organization scope before reading a report. Ask one targeted question when any boundary is missing.
2. Default to a maximum 31-day range and at most 10 selected users or projects. Ask before widening either bound.
3. Resolve only the minimum project or user identities needed for exact IDs. Discover the report and outstanding-week reads from the live timesheet catalog, then use their current schemas.
4. Keep recorded entries and outstanding weeks separate. A recorded entry is submitted time data; an outstanding week is the server's tenant-specific completion signal. Neither proves work quality, productivity, attendance, or misconduct.
5. Return only the requested period, scope, completion state, and necessary totals or refs. Do not echo free-text notes, contact data, employment details, or unrelated entry fields by default.
6. If grouping is unavailable, pagination is missing, or a result exceeds the approved bound, stop rather than fetching or reproducing the raw set. State the exact limit and ask the user to narrow the scope.
7. Preserve successful bounded results when another read is partial or unavailable. Report tenant-specific completion rules as unknown unless the server returns them.

Never rank people, compare productivity, infer performance, or characterize missing time as misconduct. This workflow is read-only: do not create, update, approve, export, or otherwise change timesheets.

## Interpretation

- A project can be draft, launched, completed, archived, or deleted through distinct lifecycle concepts. Report the returned state rather than collapsing them.
- Missing status updates do not mean the project has no work.
- Unassigned tasks and tasks without dates are explicit gaps, not lookup failures.
- Time entries do not by themselves prove delivery progress or task completion.
