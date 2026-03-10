# Phase Plan

## Phase 1 - Project skeleton
### Goal
Create the folder structure, planning documents, and basic service placeholders.

### Deliverables
- monorepo structure
- simple READMEs
- FastAPI placeholder apps
- implementation roadmap

### What you learn
- project organization
- service boundaries
- how to reduce complexity early

## Phase 2 - Core backend and frontend
### Goal
Implement incident and task CRUD with a simple React dashboard.

### Deliverables
- incident service endpoints
- coordination task endpoints
- React pages for incidents and tasks
- PostgreSQL models

### What you learn
- REST APIs
- React data flow
- database basics

## Phase 3 - Messaging
### Goal
Connect services using RabbitMQ.

### Deliverables
- publish `incident.created`
- consume event in coordination service
- create notifications
- show notifications in the dashboard

### What you learn
- async systems
- event design
- loose coupling

## Phase 4 - RAG
### Goal
Index documents in Qdrant and retrieve useful context.

### Deliverables
- document upload endpoint
- chunking and embeddings
- Qdrant search
- evidence display in UI

### What you learn
- embeddings
- vector search
- grounded AI answers

## Phase 5 - AI orchestration
### Goal
Build controlled agentic workflows.

### Deliverables
- triage workflow
- response plan workflow
- advisory draft workflow
- structured LLM prompts and outputs

### What you learn
- AI workflow design
- context building
- safe orchestration

## Phase 6 - Kubernetes
### Goal
Deploy the system locally on Kubernetes.

### Deliverables
- Docker images
- Kubernetes manifests
- Secrets and ConfigMaps
- local cluster runbook

### What you learn
- containerization
- deployments and services
- infrastructure basics

## Recommended order
Always finish one small end-to-end slice before adding new complexity.
