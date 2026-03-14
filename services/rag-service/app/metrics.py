from time import perf_counter

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

SERVICE_NAME = "rag-service"

http_requests_total = Counter(
    "platform_http_requests_total",
    "Total HTTP requests handled by a service.",
    ("service", "method", "path", "status_code"),
)
http_request_duration_seconds = Histogram(
    "platform_http_request_duration_seconds",
    "HTTP request latency in seconds.",
    ("service", "method", "path"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)
rag_documents_ingested_total = Counter(
    "platform_rag_documents_ingested_total",
    "Total documents ingested into the RAG store.",
    ("service", "category", "incident_type"),
)
rag_chunks_indexed_total = Counter(
    "platform_rag_chunks_indexed_total",
    "Total knowledge chunks indexed in Qdrant.",
    ("service", "incident_type"),
)
rag_documents_in_store = Gauge(
    "platform_rag_documents_in_store",
    "Current number of document metadata records in memory.",
    ("service",),
)
rag_search_requests_total = Counter(
    "platform_rag_search_requests_total",
    "Total retrieval queries sent to the RAG service.",
    ("service", "incident_type"),
)
rag_search_match_count = Histogram(
    "platform_rag_search_match_count",
    "Number of retrieval results returned per search.",
    ("service", "incident_type"),
    buckets=(0, 1, 2, 3, 5, 10, 20),
)


def _route_path(request: Request) -> str:
    route = request.scope.get("route")
    if route is not None and getattr(route, "path", None):
        return str(route.path)
    return request.url.path



def configure_metrics(app: FastAPI) -> None:
    if getattr(app.state, "metrics_enabled", False):
        return

    app.state.metrics_enabled = True

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)

        start_time = perf_counter()
        status_code = "500"
        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            return response
        finally:
            path = _route_path(request)
            duration = perf_counter() - start_time
            http_requests_total.labels(SERVICE_NAME, request.method, path, status_code).inc()
            http_request_duration_seconds.labels(SERVICE_NAME, request.method, path).observe(duration)

    @app.get("/metrics", include_in_schema=False)
    def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)



def set_document_store_size(size: int) -> None:
    rag_documents_in_store.labels(SERVICE_NAME).set(size)



def record_document_ingested(category: str, incident_type: str, chunk_count: int) -> None:
    normalized_incident_type = incident_type or "all"
    rag_documents_ingested_total.labels(SERVICE_NAME, category, normalized_incident_type).inc()
    rag_chunks_indexed_total.labels(SERVICE_NAME, normalized_incident_type).inc(chunk_count)



def record_search(incident_type: str | None, match_count: int) -> None:
    normalized_incident_type = incident_type or "all"
    rag_search_requests_total.labels(SERVICE_NAME, normalized_incident_type).inc()
    rag_search_match_count.labels(SERVICE_NAME, normalized_incident_type).observe(match_count)
