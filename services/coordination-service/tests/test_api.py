from uuid import uuid4

from fastapi.testclient import TestClient

import app.main as main
from app.main import app
from app.service import TaskService


def create_client(monkeypatch):
    published_messages: list[tuple[str, dict]] = []
    monkeypatch.setattr(main, "service", TaskService())
    monkeypatch.setattr(main, "safe_publish", lambda topic, payload: published_messages.append((topic, payload)))
    monkeypatch.setattr(main, "start_incident_consumer", lambda handler: None)
    return TestClient(app), published_messages


def test_health_endpoint(monkeypatch):
    client, _ = create_client(monkeypatch)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "coordination-service"


def test_task_crud_flow(monkeypatch):
    client, published_messages = create_client(monkeypatch)
    incident_id = str(uuid4())

    create_response = client.post(
        "/tasks",
        json={
            "incident_id": incident_id,
            "title": "Dispatch field team",
            "team": "Operations",
            "priority": "high",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["status"] == "todo"
    assert len(published_messages) == 1
    assert published_messages[0][0] == main.settings.task_created_topic

    task_id = created["id"]

    update_response = client.patch(f"/tasks/{task_id}", json={"status": "done"})
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "done"

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    assert any(task["id"] == task_id for task in list_response.json())

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204


def test_handle_incident_created_generates_follow_up_task(monkeypatch):
    service = TaskService()
    published_messages: list[tuple[str, dict]] = []
    monkeypatch.setattr(main, "service", service)
    monkeypatch.setattr(main, "safe_publish", lambda topic, payload: published_messages.append((topic, payload)))

    incident_id = str(uuid4())
    main.handle_incident_created(
        {
            "incident": {
                "id": incident_id,
                "type": "flood",
                "location": "Zone A",
                "severity": "high",
            }
        }
    )

    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].incident_id == uuid4().__class__(incident_id)
    assert tasks[0].team == "Operations"
    assert len(published_messages) == 1
