# Kubernetes Base

This folder contains the Phase 6 deployment assets for the platform.

## Included resources
- Namespace
- ConfigMap and Secret
- Deployments and Services for the frontend and backend services
- Kafka and Qdrant infrastructure
- Kafka topic bootstrap Job
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

## Local cluster workflow
This stack is intended for local Kubernetes deployment.

Recommended setup:
1. create a `kind` cluster with `infra/k8s/kind/cluster.yaml`
2. build the local Docker images listed below
3. load those images into the `kind` cluster
4. apply `kubectl apply -k infra/k8s/base`
5. optionally apply `kubectl apply -k infra/k8s/monitoring`

Convenience script:
- `scripts/local_k8s/deploy-kind.ps1`

## Access pattern
- ingress host: `disaster.local`
- frontend routes are served by `frontend-web`
- `/api/*` requests are proxied from the frontend container to `api-gateway`

## References
- `docs/phase-6-architecture.md`
- `docs/phase-7-architecture.md`
- `docs/kafka-messaging.md`
- `infra/k8s/monitoring/README.md`
- `README.md`
