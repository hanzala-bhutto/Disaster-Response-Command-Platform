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

## Events published
- `incident.created` later
- `incident.updated` later

## Events consumed
None for now.

## How to run locally
1. install dependencies from `requirements.txt`
2. run `uvicorn app.main:app --reload --port 8001`

## Environment variables
This will be added later.
