# Kubernetes Monitoring Stack

This folder contains the Phase 7 observability stack for the platform.

## Included components
- Prometheus for metric scraping, storage, and query execution
- Grafana for dashboards and visual analysis
- Kafka exporter for broker and topic metrics
- ingress routes for the monitoring tools

## Apply order
1. apply the platform stack from `infra/k8s/base`
2. apply the monitoring stack with `kubectl apply -k infra/k8s/monitoring`

This monitoring stack is intended to run on the same local Kubernetes cluster as the application stack.

## Access hosts
- `grafana.disaster.local`
- `prometheus.disaster.local`

## Default Grafana credentials
- username: `admin`
- password: `admin`

## What Prometheus scrapes
- all FastAPI services at `/metrics`
- Qdrant at `/metrics`
- Kafka exporter at `/metrics`
- Prometheus itself for self-observation

## What Grafana shows
- request rate and latency across services
- incident, task, notification, and document counts
- event publication and consumption rates
- AI workflow throughput and duration
- service health through the `up` metric

## References
- `docs/phase-7-architecture.md`
- `README.md`
