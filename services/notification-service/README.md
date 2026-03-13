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

## Events published
None for now.

## Events consumed
- `incident.created`
- `task.created`

## How to run locally
1. install dependencies from `requirements.txt`
2. run `uvicorn app.main:app --reload --port 8003`
3. for Kubernetes, build the container image from `Dockerfile`

## Environment variables
- `RABBITMQ_URL`
- `RABBITMQ_EXCHANGE`
- `NOTIFICATION_QUEUE_NAME`

## Container port
- `8003`
