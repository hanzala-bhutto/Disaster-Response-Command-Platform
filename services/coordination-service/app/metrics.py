from time import perf_counter

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

SERVICE_NAME = "coordination-service"

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
task_mutations_total = Counter(
    "platform_task_mutations_total",
    "Total task create, update, and delete operations.",
    ("service", "action", "team", "priority"),
)
tasks_in_store = Gauge(
    "platform_tasks_in_store",
    "Current number of tasks in memory.",
    ("service",),
)
events_published_total = Counter(
    "platform_events_published_total",
    "Total domain events published by a service.",
    ("service", "routing_key", "status"),
)
events_consumed_total = Counter(
    "platform_events_consumed_total",
    "Total domain events consumed by a service.",
    ("service", "routing_key", "status"),
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



def set_task_store_size(size: int) -> None:
    tasks_in_store.labels(SERVICE_NAME).set(size)



def record_task_mutation(action: str, team: str, priority: str) -> None:
    task_mutations_total.labels(SERVICE_NAME, action, team, priority).inc()



def record_event_publish(routing_key: str, status: str) -> None:
    events_published_total.labels(SERVICE_NAME, routing_key, status).inc()



def record_event_consumed(routing_key: str, status: str) -> None:
    events_consumed_total.labels(SERVICE_NAME, routing_key, status).inc()
