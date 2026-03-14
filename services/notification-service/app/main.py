from uuid import UUID

from fastapi import FastAPI

from .event_bus import start_notification_consumer
from .metrics import configure_metrics
from .schemas import Notification
from .service import NotificationService

app = FastAPI(title="Notification Service")
configure_metrics(app)
service = NotificationService()


def handle_event(routing_key: str, payload: dict) -> None:
    if routing_key == "incident.created":
        incident = payload.get("incident", {})
        incident_id = incident.get("id")
        service.add_notification(
            title="New incident received",
            message=f"{incident.get('title', 'Incident')} reported at {incident.get('location', 'unknown location')}",
            level="critical" if incident.get("severity") == "critical" else "warning",
            source_event=routing_key,
            incident_id=UUID(incident_id) if incident_id else None,
        )
    elif routing_key == "task.created":
        task = payload.get("task", {})
        incident_id = task.get("incident_id")
        task_id = task.get("id")
        service.add_notification(
            title="Task created",
            message=f"{task.get('team', 'Team')} assigned: {task.get('title', 'New task')}",
            level="info",
            source_event=routing_key,
            incident_id=UUID(incident_id) if incident_id else None,
            task_id=UUID(task_id) if task_id else None,
        )


@app.on_event("startup")
def startup_consumer() -> None:
    start_notification_consumer(handle_event)


@app.get("/health")
def health() -> dict:
    return {"service": "notification-service", "status": "ok", "phase": 7}


@app.get("/notifications", response_model=list[Notification])
def list_notifications() -> list[Notification]:
    return service.list_notifications()
