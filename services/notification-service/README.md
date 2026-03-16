# Notification Service

## What this service does
Creates alerts and notification records for the dashboard.

## Inputs
- incident and task events

## Outputs
- notifications

## Main endpoints
- `GET /health`
- `GET /notifications`
- `GET /metrics`

## Events published
None for now.

## Events consumed
- `incident.created`
- `task.created`

## Kafka behavior
This service consumes both event topics in its own consumer group and turns them into dashboard notifications.

## How to run locally
1. install dependencies from `requirements.txt`
2. run `uvicorn app.main:app --reload --port 8003`
3. for Kubernetes, build the container image from `Dockerfile`

## Environment variables
- `KAFKA_BOOTSTRAP_SERVERS`
- `INCIDENT_CREATED_TOPIC`
- `TASK_CREATED_TOPIC`
- `NOTIFICATION_CONSUMER_GROUP`

## Container port
- `8003`
