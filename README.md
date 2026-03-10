# Disaster Response Command Platform

A simple student project to learn:
- React frontend
- FastAPI backend
- microservices
- RabbitMQ messaging
- PostgreSQL storage
- Qdrant RAG
- agentic AI workflows
- Kubernetes deployment

## Simple idea
This platform receives disaster incidents like floods or fires and turns them into:
- incident records
- coordination tasks
- alerts
- AI-generated response plans

## Stack
- Frontend: React
- Backend: FastAPI
- Message Broker: RabbitMQ
- Database: PostgreSQL
- Cache: Redis
- Vector DB: Qdrant
- AI: external LLM API
- Deployment: Docker + Kubernetes

## Project structure
- `frontend/web` - React app
- `services` - FastAPI microservices
- `shared` - shared schemas and helpers
- `infra` - deployment files
- `docs` - architecture and phase plans
- `scripts` - seed and simulator scripts
- `data` - sample documents and sample incidents

## Phases
1. Phase 1 - plan and project skeleton
2. Phase 2 - incident and task CRUD
3. Phase 3 - RabbitMQ event flow
4. Phase 4 - RAG with Qdrant
5. Phase 5 - AI orchestration
6. Phase 6 - Kubernetes deployment

## Current status
Phase 1 is being implemented.

## What to read first
- `docs/master-plan.md`
- `docs/phases.md`
- `docs/learning-map.md`

## Goal of MVP
Build one flow end to end:
1. create incident
2. publish event
3. create task
4. retrieve SOP context
5. generate AI response plan
6. show it on the dashboard
