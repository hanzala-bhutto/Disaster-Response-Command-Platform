from time import perf_counter

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

SERVICE_NAME = "ai-orchestrator"

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
downstream_requests_total = Counter(
    "platform_downstream_requests_total",
    "Total downstream HTTP requests issued by a service.",
    ("service", "target_service", "method", "status_code"),
)
downstream_request_duration_seconds = Histogram(
    "platform_downstream_request_duration_seconds",
    "Downstream HTTP request latency in seconds.",
    ("service", "target_service", "method"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)
ai_workflow_runs_total = Counter(
    "platform_ai_workflow_runs_total",
    "Total AI workflow runs executed by mode and type.",
    ("service", "workflow_type", "mode"),
)
ai_workflow_duration_seconds = Histogram(
    "platform_ai_workflow_duration_seconds",
    "AI workflow duration in seconds.",
    ("service", "workflow_type", "mode"),
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0),
)
ai_workflow_history_size = Gauge(
    "platform_ai_workflow_history_size",
    "Current number of workflow results retained in memory.",
    ("service",),
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



def record_downstream_request(target_service: str, method: str, status_code: str, duration_seconds: float) -> None:
    downstream_requests_total.labels(SERVICE_NAME, target_service, method, status_code).inc()
    downstream_request_duration_seconds.labels(SERVICE_NAME, target_service, method).observe(duration_seconds)



def record_workflow_run(workflow_type: str, mode: str, duration_seconds: float) -> None:
    ai_workflow_runs_total.labels(SERVICE_NAME, workflow_type, mode).inc()
    ai_workflow_duration_seconds.labels(SERVICE_NAME, workflow_type, mode).observe(duration_seconds)



def set_workflow_history_size(size: int) -> None:
    ai_workflow_history_size.labels(SERVICE_NAME).set(size)
