# Event Contracts

## `incident.created`
Published by the incident service when a new incident is created.

Example fields:
- `event_type`
- `incident.id`
- `incident.title`
- `incident.type`
- `incident.severity`
- `incident.location`
- `incident.status`
- `occurred_at`

## `task.created`
Published by the coordination service when a task is created.

Example fields:
- `event_type`
- `task.id`
- `task.incident_id`
- `task.title`
- `task.team`
- `task.priority`
- `task.status`
- `occurred_at`
