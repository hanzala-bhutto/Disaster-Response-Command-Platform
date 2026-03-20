from fastapi.testclient import TestClient

import app.main as main
from app.main import app
from app.service import IncidentService


def create_client(monkeypatch):
    published_messages: list[tuple[str, dict]] = []
    monkeypatch.setattr(main, "service", IncidentService())
    monkeypatch.setattr(main, "safe_publish", lambda topic, payload: published_messages.append((topic, payload)))
    return TestClient(app), published_messages


def test_health_endpoint(monkeypatch):
    client, _ = create_client(monkeypatch)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "incident-service"


def test_incident_crud_flow(monkeypatch):
    client, published_messages = create_client(monkeypatch)

    create_response = client.post(
        "/incidents",
        json={
            "title": "Wildfire near ridge road",
            "type": "fire",
            "severity": "critical",
            "location": "Zone C",
            "description": "Smoke is moving toward nearby homes.",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["status"] == "new"
    assert len(published_messages) == 1
    assert published_messages[0][0] == main.settings.incident_created_topic

    incident_id = created["id"]

    list_response = client.get("/incidents")
    assert list_response.status_code == 200
    assert any(item["id"] == incident_id for item in list_response.json())

    update_response = client.patch(f"/incidents/{incident_id}", json={"status": "resolved"})
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "resolved"

    delete_response = client.delete(f"/incidents/{incident_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/incidents/{incident_id}")
    assert get_response.status_code == 404
