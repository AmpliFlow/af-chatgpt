# People and training

Load this reference for users, members, teams, roles, positions, competencies, competency matrices, or training plans.

## Route

- `ampliflow_people`: users, tenant members, teams, roles, positions, competencies, competency matrices, and organization records.
- `ampliflow_training_plans`: training plans, assigned positions and people, deadlines, execution, evaluation, status, and performance options.
- The owning business dispatcher: responsibilities or assignments on projects, goals, risks, controls, improvements, or checklists.

## Relationships and order

1. Resolve the person, team, role, or position in the organization domain before comparing assignments across records.
2. Keep account user, tenant member, team, role, and position identities distinct.
3. Resolve competencies and matrices before interpreting position expectations or individual coverage.
4. Resolve a training plan before its assigned positions, people, execution, or evaluation evidence.
5. Read responsibility from the domain that owns it. Organization membership alone does not prove responsibility for a record.

## Interpretation

- A required competency, completed activity, and evaluated competency level are different evidence.
- Training assignment does not prove attendance, completion, effectiveness, or competence.
- An archived or inactive user can still appear in historical ownership evidence.
- Access to a record and responsibility for it are different relationships.
- Report missing organization links as unknown unless a current operation explicitly returns an empty complete set.
