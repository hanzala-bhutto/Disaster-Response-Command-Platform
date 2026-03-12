# Phase 5 Architecture

This document explains the Phase 5 AI orchestration flow in a simple way.

## What changed in Phase 5
Phase 4 gave the system retrieval with Qdrant.
Phase 5 adds an AI orchestrator that combines:
- incident context
- related tasks
- notifications
- retrieved evidence
- an LLM or fallback logic

## Main idea
When a workflow runs:
1. the frontend sends a workflow request
2. the gateway forwards it to the AI orchestrator
3. the AI orchestrator fetches incident data
4. the AI orchestrator fetches related tasks and notifications
5. the AI orchestrator searches the RAG service for evidence
6. the AI orchestrator builds a structured prompt
7. the LLM is called if credentials are present
8. otherwise fallback logic is used
9. the frontend shows the structured result

## Diagram: orchestration overview
```mermaid
flowchart LR
	U[User] --> FE[React Frontend]
	FE --> GW[API Gateway]
	GW --> AO[AI Orchestrator]
	AO --> IS[Incident Service]
	AO --> CS[Coordination Service]
	AO --> NS[Notification Service]
	AO --> RS[RAG Service]
	RS --> Q[(Qdrant)]
	AO --> LLM[External LLM API or Fallback]
	LLM --> AO
	AO --> FE
```

## Diagram: workflow sequence
```mermaid
sequenceDiagram
	participant User
	participant Frontend as React Frontend
	participant Gateway as API Gateway
	participant Orchestrator as AI Orchestrator
	participant Incident as Incident Service
	participant Coordination as Coordination Service
	participant Notification as Notification Service
	participant RAG as RAG Service
	participant LLM

	User->>Frontend: Run workflow
	Frontend->>Gateway: POST /ai/workflows/run
	Gateway->>Orchestrator: Forward request
	Orchestrator->>Incident: Get incident
	Orchestrator->>Coordination: Get tasks
	Orchestrator->>Notification: Get notifications
	Orchestrator->>RAG: Search evidence
	RAG-->>Orchestrator: Relevant chunks
	Orchestrator->>LLM: Prompt with context and evidence
	LLM-->>Orchestrator: Structured JSON or no response
	Orchestrator-->>Gateway: Workflow result
	Gateway-->>Frontend: Structured AI output
```

## Diagram: fallback decision
```mermaid
flowchart TD
	A[Workflow Request] --> B[Collect incident context]
	B --> C[Retrieve evidence from RAG]
	C --> D{LLM configured?}
	D -- Yes --> E[Call external LLM API]
	D -- No --> F[Use fallback planner]
	E --> G[Structured workflow result]
	F --> G
```

## Diagram: orchestration inputs and outputs
```mermaid
flowchart TD
	A[Incident Details] --> E[AI Orchestrator]
	B[Related Tasks] --> E
	C[Notifications] --> E
	D[Retrieved Evidence] --> E
	E --> F[Summary]
	E --> G[Response Plan]
	E --> H[Resource Needs]
	E --> I[Caution Notes]
	E --> J[Public Message]
```

## Why this matters
This phase introduces the difference between:
- a direct prompt
- a real workflow

A workflow is better because it has clear steps and known inputs.

## Workflow types in this phase
- triage
- response_plan
- public_advisory

## Why fallback mode exists
The project should still work without paid API usage.
Fallback mode makes the architecture testable even when no LLM key is configured.

## Simple architecture roles
### Frontend
- lets the user run workflows
- displays summaries, plans, cautions, and evidence

### API Gateway
- forwards AI workflow requests

### AI Orchestrator
- central workflow engine
- gathers context
- reuses RAG
- calls LLM or fallback
- stores workflow run history in memory

### RAG Service
- provides evidence chunks

### Incident / Coordination / Notification Services
- provide structured operational context

## What this prepares for later
Phase 5 makes it easy to add:
- tool calling
- approval flows
- automatic task suggestions
- richer agents
- audit logs and AI analytics
