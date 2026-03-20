import httpx
from fastapi.testclient import TestClient

import app.main as main
from app.main import app


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "api-gateway"


def test_gateway_forwards_incident_requests(monkeypatch):
    async def fake_get_incidents():
        return [{"id": "incident-1", "title": "Flood warning"}]

    async def fake_create_incident(payload):
        return {"id": "incident-2", **payload}

    monkeypatch.setattr(main.clients, "get_incidents", fake_get_incidents)
    monkeypatch.setattr(main.clients, "create_incident", fake_create_incident)

    client = TestClient(app)

    list_response = client.get("/incidents")
    assert list_response.status_code == 200
    assert list_response.json()[0]["id"] == "incident-1"

    create_response = client.post("/incidents", json={"title": "Wildfire", "severity": "high"})
    assert create_response.status_code == 201
    assert create_response.json()["id"] == "incident-2"


def test_gateway_maps_downstream_request_error(monkeypatch):
    async def fake_get_notifications():
        request = httpx.Request("GET", "http://notification-service/notifications")
        raise httpx.RequestError("notification service unavailable", request=request)

    monkeypatch.setattr(main.clients, "get_notifications", fake_get_notifications)

    client = TestClient(app)
    response = client.get("/notifications")

    assert response.status_code == 502
    assert response.json()["detail"] == "notification service unavailable"
