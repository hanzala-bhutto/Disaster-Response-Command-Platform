# Kubernetes Base

This folder contains the Phase 6 deployment assets for the platform.

## Included resources
- Namespace
- ConfigMap and Secret
- Deployments and Services for the frontend and backend services
- RabbitMQ and Qdrant infrastructure
- PersistentVolumeClaims for stateful dependencies
- Ingress for the web entry point

## Images expected by the manifests
- `disaster-response/frontend-web:local`
- `disaster-response/api-gateway:local`
- `disaster-response/incident-service:local`
- `disaster-response/coordination-service:local`
- `disaster-response/notification-service:local`
- `disaster-response/rag-service:local`
- `disaster-response/ai-orchestrator:local`
- `disaster-response/ingestion-service:local`

## Apply order
Use `kubectl apply -k infra/k8s/base` after the images are built and available to the cluster runtime.

The default `secrets.yaml` keeps the AI orchestrator in fallback mode. Add a real `LLM_API_KEY` value when live LLM calls are needed.

## Access pattern
- ingress host: `disaster.local`
- frontend routes are served by `frontend-web`
- `/api/*` requests are proxied from the frontend container to `api-gateway`

## References
- `docs/phase-6-architecture.md`
- `docs/phase-7-architecture.md`
- `infra/k8s/monitoring/README.md`
- `README.md`
