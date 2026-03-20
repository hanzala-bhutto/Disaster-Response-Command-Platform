from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

import app.main as main
from app.main import app


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "ai-orchestrator"


def test_workflow_routes(monkeypatch):
    run_id = uuid4()
    incident_id = uuid4()
    workflow_result = {
        "run_id": str(run_id),
        "incident_id": str(incident_id),
        "workflow_type": "response_plan",
        "mode": "fallback",
        "summary": "Fallback workflow generated.",
        "response_plan": ["Confirm scope"],
        "resource_needs": ["Field team"],
        "caution_notes": ["Validate routes"],
        "public_message": "Emergency teams are responding.",
        "evidence": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    async def fake_run_workflow(payload):
        return workflow_result

    monkeypatch.setattr(main.service, "list_runs", lambda: {"runs": [workflow_result]})
    monkeypatch.setattr(main.service, "run_workflow", fake_run_workflow)

    client = TestClient(app)

    list_response = client.get("/workflow-runs")
    assert list_response.status_code == 200
    assert list_response.json()["runs"][0]["run_id"] == str(run_id)

    run_response = client.post("/workflows/run", json={"incident_id": str(incident_id), "workflow_type": "response_plan"})
    assert run_response.status_code == 200
    assert run_response.json()["summary"] == "Fallback workflow generated."
