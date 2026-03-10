# Coordination Service

## What this service does
Creates and manages response tasks for incidents.

## Inputs
- incidents and events

## Outputs
- coordination tasks

## Main endpoints
- `GET /health`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

## Events published
- `task.created` later

## Events consumed
- `incident.created` later

## How to run locally
1. install dependencies from `requirements.txt`
2. run `uvicorn app.main:app --reload --port 8002`

## Environment variables
This will be added later.
