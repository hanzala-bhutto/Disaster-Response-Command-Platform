# Ingestion Service

## What this service does
Accepts simulated disaster events and prepares them for the system.

## Inputs
- mock incident events

## Outputs
- normalized events

## Main endpoints
- `GET /health`
- `GET /metrics`

## Events published
None for now.

## Events consumed
None for now.

## How to run locally
1. install dependencies from `requirements.txt`
2. run `uvicorn app.main:app --reload --port 8006`
3. for Kubernetes, build the container image from `Dockerfile`

## Environment variables
None for now.

## Container port
- `8006`
