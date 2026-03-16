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
- `GET /metrics`

## Events published
- `task.created`

## Events consumed
- `incident.created`

## Kafka behavior
This service listens for `incident.created` and auto-creates a starter task.

## How to run locally
1. install dependencies from `requirements.txt`
2. run `uvicorn app.main:app --reload --port 8002`
3. for Kubernetes, build the container image from `Dockerfile`

## Environment variables
- `KAFKA_BOOTSTRAP_SERVERS`
- `INCIDENT_CREATED_TOPIC`
- `TASK_CREATED_TOPIC`
- `COORDINATION_CONSUMER_GROUP`

## Container port
- `8002`
