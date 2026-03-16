# Incident Service

## What this service does
Stores and manages disaster incidents.

## Inputs
- incident create and read requests

## Outputs
- incident records
- incident events

## Main endpoints
- `GET /health`
- `GET /incidents`
- `GET /incidents/{incident_id}`
- `POST /incidents`
- `PATCH /incidents/{incident_id}`
- `DELETE /incidents/{incident_id}`
- `GET /metrics`

## Events published
- `incident.created`

## Kafka behavior
When a new incident is created, this service publishes `incident.created`.

## Events consumed
None for now.

## How to run locally
1. install dependencies from `requirements.txt`
2. run `uvicorn app.main:app --reload --port 8001`
3. for Kubernetes, build the container image from `Dockerfile`

## Environment variables
- `KAFKA_BOOTSTRAP_SERVERS`
- `INCIDENT_CREATED_TOPIC`

## Container port
- `8001`
