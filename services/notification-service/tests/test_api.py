from uuid import uuid4

from fastapi.testclient import TestClient

import app.main as main
from app.main import app
from app.service import NotificationService


def create_client(monkeypatch):
    monkeypatch.setattr(main, "service", NotificationService())
    monkeypatch.setattr(main, "start_notification_consumer", lambda handler: None)
    return TestClient(app)


def test_health_endpoint(monkeypatch):
    client = create_client(monkeypatch)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "notification-service"


def test_notifications_are_exposed_via_api(monkeypatch):
    client = create_client(monkeypatch)
    incident_id = str(uuid4())

    main.handle_event(
        "incident.created",
        {"incident": {"id": incident_id, "title": "Flood warning", "location": "Zone A", "severity": "critical"}},
    )

    response = client.get("/notifications")

    assert response.status_code == 200
    notifications = response.json()
    assert len(notifications) == 1
    assert notifications[0]["source_event"] == "incident.created"


def test_handle_task_created_event_creates_notification(monkeypatch):
    service = NotificationService()
    monkeypatch.setattr(main, "service", service)
    incident_id = str(uuid4())
    task_id = str(uuid4())

    main.handle_event(
        "task.created",
        {"task": {"id": task_id, "incident_id": incident_id, "title": "Review route closures", "team": "Logistics"}},
    )

    notifications = service.list_notifications()
    assert len(notifications) == 1
    assert notifications[0].title == "Task created"
    assert notifications[0].source_event == "task.created"
