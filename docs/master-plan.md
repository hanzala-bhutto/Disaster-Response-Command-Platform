# Master Plan

## 1. Project goal
Build a simple disaster response platform that is easy to explain and demonstrates a full modern system.

## 2. Main user story
A disaster operator receives a new incident, reviews AI-supported guidance, creates response tasks, and monitors the situation from one dashboard.

## 3. Main modules
### Frontend
- dashboard
- incident detail page
- task view
- AI assistant
- document upload page

### Backend services
- API Gateway
- Incident Service
- Ingestion Service
- Coordination Service
- Notification Service
- RAG Service
- AI Orchestrator

### Infrastructure
- RabbitMQ
- PostgreSQL
- Redis
- Qdrant
- Kubernetes

## 4. Simple responsibilities
### API Gateway
One entry point for the frontend.

### Incident Service
Stores and manages incidents.

### Ingestion Service
Accepts simulated external events.

### Coordination Service
Turns incidents into actionable tasks.

### Notification Service
Creates alerts for the dashboard.

### RAG Service
Indexes documents and retrieves relevant SOP content.

### AI Orchestrator
Runs simple multi-step AI workflows.

## 5. MVP scope
Keep the first version small.

### Include
- incident CRUD
- task creation
- RabbitMQ event publication and consumption
- document upload and indexing
- Qdrant retrieval
- one AI workflow: triage + response plan
- React dashboard

### Exclude for now
- advanced auth
- multi-tenant design
- real sensor integrations
- advanced maps
- full automation

## 6. Event flow
1. user creates an incident
2. incident service stores it
3. incident service publishes `incident.created`
4. coordination service consumes it
5. coordination service creates tasks
6. notification service creates alert
7. AI orchestrator fetches incident + RAG context
8. AI orchestrator calls LLM API
9. frontend shows the plan

## 7. Agentic workflow pattern
Use the same pattern everywhere:
1. collect input
2. fetch structured context
3. retrieve knowledge from Qdrant
4. call LLM with a strict prompt
5. parse structured response
6. save result
7. require human review before action

## 8. First AI workflows
### Workflow A: Triage
Input: incident
Output: severity summary, risks, first actions

### Workflow B: Response Plan
Input: incident + SOP context
Output: step-by-step plan, teams, resources, cautions

### Workflow C: Public Advisory Draft
Input: incident + plan
Output: short public message

## 9. Data model
### Incident
- id
- title
- type
- severity
- location
- description
- status
- created_at

### Task
- id
- incident_id
- title
- team
- status
- priority
- created_at

### Notification
- id
- incident_id
- message
- level
- read
- created_at

### Document
- id
- title
- category
- source
- uploaded_at

### AI Result
- id
- incident_id
- workflow_type
- prompt_version
- result_json
- created_at

## 10. API groups
### Gateway routes
- `GET /health`
- `GET /incidents`
- `POST /incidents`
- `GET /tasks`
- `POST /documents/upload`
- `POST /ai/respond`

## 11. Event names
- `incident.created`
- `incident.updated`
- `task.created`
- `notification.created`
- `ai.plan.generated`

## 12. Why RabbitMQ
RabbitMQ is easier than Kafka for the first version and is enough for event-driven learning.

## 13. Why Qdrant
Qdrant is lightweight, clear, and good for student RAG projects.

## 14. Why Kubernetes still matters
Even if the LLM is external, the rest of the platform can still run on Kubernetes:
- frontend
- FastAPI services
- RabbitMQ
- PostgreSQL
- Redis
- Qdrant

## 15. Development pattern
Each phase should follow the same loop:
1. define one small goal
2. implement only what is needed
3. test the end-to-end flow
4. document what was learned
5. move to the next phase
