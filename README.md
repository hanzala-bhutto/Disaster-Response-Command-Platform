# Disaster Response Command Platform

A disaster operations platform built to demonstrate:
- React frontend
- FastAPI backend
- microservices
- Kafka event streaming
- PostgreSQL storage
- Qdrant RAG
- agentic AI workflows
- Kubernetes deployment
- observability with Prometheus and Grafana

## Simple idea
This platform receives disaster incidents like floods or fires and turns them into:
- incident records
- coordination tasks
- alerts
- AI-generated response plans

## Stack
- Frontend: React
- Backend: FastAPI
- Message Broker: Kafka
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
3. Phase 3 - Kafka event flow and notifications
4. Phase 4 - RAG with Qdrant
5. Phase 5 - AI orchestration
6. Phase 6 - Kubernetes deployment
7. Phase 7 - observability and monitoring
8. Phase 8 - automated testing

## Current status
Phase 8 automated frontend testing assets are implemented.

## What to read first
- `docs/master-plan.md`
- `docs/phases.md`
- `docs/learning-map.md`
- `docs/kafka-messaging.md`
- `docs/phase-6-architecture.md`
- `docs/phase-7-architecture.md`
- `docs/phase-8-testing.md`
- `infra/k8s/base/README.md`
- `infra/k8s/monitoring/README.md`

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
- Kubernetes manifests for the application stack, Kafka, and Qdrant
- ConfigMaps, Secrets, persistent volumes, and ingress
- a local cluster runbook in `infra/k8s/base/README.md`

## Local Kubernetes
The intended deployment target is a local Kubernetes cluster.

Recommended workflow:
- create a local `kind` cluster with `infra/k8s/kind/cluster.yaml`
- build and load the Docker images into that cluster
- apply `infra/k8s/base`
- apply `infra/k8s/monitoring`

Convenience script:
- `scripts/local_k8s/deploy-kind.ps1`

## Observability
Phase 7 adds:
- `/metrics` endpoints on all FastAPI services
- Prometheus scrape configuration for application and infrastructure metrics
- Grafana provisioning with a platform overview dashboard
- Kafka exporter metrics for broker visibility
- a monitoring runbook in `infra/k8s/monitoring/README.md`

## Automated testing
Phase 8 adds:
- Playwright browser-based end-to-end tests for the React dashboard
- route-level API mocking so frontend flows can be tested without all backend services running
- repeatable test commands in `frontend/web/package.json`
- a testing architecture guide in `docs/phase-8-testing.md`

## Architecture references
- `docs/phase-3-architecture.md`
- `docs/phase-4-architecture.md`
- `docs/phase-5-architecture.md`
- `docs/phase-6-architecture.md`
- `docs/phase-7-architecture.md`
- `docs/phase-8-testing.md`
