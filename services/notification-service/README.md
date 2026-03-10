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
- `notification.created` later

## Events consumed
- `incident.created`
- `task.created`

## How to run locally
1. install dependencies from `requirements.txt`
2. run `uvicorn app.main:app --reload --port 8003`

## Environment variables
- `RABBITMQ_URL`
- `RABBITMQ_EXCHANGE`
