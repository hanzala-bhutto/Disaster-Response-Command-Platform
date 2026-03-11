# API Gateway

## What this service does
Acts as the main backend entry point for the frontend.

## Inputs
- frontend HTTP requests

## Outputs
- routes requests to backend services

## Main endpoints
- `GET /health`
- `GET /incidents`
- `POST /incidents`
- `PATCH /incidents/{incident_id}`
- `DELETE /incidents/{incident_id}`
- `GET /tasks`
- `POST /tasks`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
- `GET /notifications`
- `GET /knowledge/documents`
- `POST /knowledge/documents`
- `POST /knowledge/search`

## Events published
None for now.

## Events consumed
None for now.

## How to run locally
1. install dependencies from `requirements.txt`
2. run `uvicorn app.main:app --reload --port 8000`

## Environment variables
- `INCIDENT_SERVICE_URL`
- `COORDINATION_SERVICE_URL`
- `NOTIFICATION_SERVICE_URL`
- `RAG_SERVICE_URL`
