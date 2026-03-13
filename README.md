# Disaster Response Command Platform

A disaster operations platform built to demonstrate:
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
3. Phase 3 - RabbitMQ event flow and notifications
4. Phase 4 - RAG with Qdrant
5. Phase 5 - AI orchestration
6. Phase 6 - Kubernetes deployment

## Current status
Phase 6 deployment assets are implemented.

## What to read first
- `docs/master-plan.md`
- `docs/phases.md`
- `docs/learning-map.md`
- `docs/phase-6-architecture.md`
- `infra/k8s/base/README.md`

## Goal
Build one flow end to end:
1. create incident
2. publish event
3. create task
4. retrieve SOP context
5. generate AI response plan
6. show it on the dashboard

## Deployment
Phase 6 adds:
- container images for the frontend and each service
- Kubernetes manifests for the application stack, RabbitMQ, and Qdrant
- ConfigMaps, Secrets, persistent volumes, and ingress
- a local cluster runbook in `infra/k8s/base/README.md`

## Architecture references
- `docs/phase-3-architecture.md`
- `docs/phase-4-architecture.md`
- `docs/phase-5-architecture.md`
- `docs/phase-6-architecture.md`
