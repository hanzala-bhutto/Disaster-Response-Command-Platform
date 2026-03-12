# AI Orchestrator

## What this service does
Runs simple AI workflows for triage, planning, and drafting.

## Inputs
- incident data
- retrieved knowledge
- workflow requests

## Outputs
- structured AI results

## Main endpoints
- `GET /health`
- `GET /workflow-runs`
- `POST /workflows/run`

## Events published
- `ai.plan.generated` later

## Events consumed
This will be added later.

## How to run locally
1. install dependencies from `requirements.txt`
2. set `LLM_API_KEY` and `LLM_MODEL` if you want real LLM output
3. run `uvicorn app.main:app --reload --port 8005`

## Environment variables
- `INCIDENT_SERVICE_URL`
- `COORDINATION_SERVICE_URL`
- `NOTIFICATION_SERVICE_URL`
- `RAG_SERVICE_URL`
- `LLM_BASE_URL`
- `LLM_API_KEY`
- `LLM_MODEL`

## Phase 5 note
This service supports two modes:
- `llm` when API credentials are configured
- `fallback` when they are not
