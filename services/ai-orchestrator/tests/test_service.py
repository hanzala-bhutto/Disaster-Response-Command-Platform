import asyncio
from uuid import uuid4

from app.schemas import WorkflowRequest
from app.service import OrchestratorService
import app.service as service_module


def test_run_workflow_uses_fallback_mode(monkeypatch):
    orchestrator = OrchestratorService()
    incident_id = uuid4()

    async def fake_get_incident(incident_id_str):
        return {
            "id": incident_id_str,
            "title": "River overflow near bridge",
            "description": "Water levels are rising quickly.",
            "severity": "high",
            "location": "Zone A",
            "type": "flood",
        }

    async def fake_get_tasks():
        return [{"incident_id": str(incident_id), "title": "Dispatch field team"}]

    async def fake_get_notifications():
        return [{"incident_id": str(incident_id), "message": "Flood warning issued"}]

    async def fake_search_knowledge(payload):
        return {
            "matches": [
                {
                    "document_title": "Flood SOP",
                    "source": "Manual",
                    "incident_type": "flood",
                    "chunk_index": 0,
                    "text": "Evacuate low-lying areas first.",
                    "score": 0.94,
                }
            ]
        }

    async def fake_generate(prompt):
        return None

    monkeypatch.setattr(service_module.clients, "get_incident", fake_get_incident)
    monkeypatch.setattr(service_module.clients, "get_tasks", fake_get_tasks)
    monkeypatch.setattr(service_module.clients, "get_notifications", fake_get_notifications)
    monkeypatch.setattr(service_module.clients, "search_knowledge", fake_search_knowledge)
    monkeypatch.setattr(service_module.llm_client, "generate", fake_generate)

    result = asyncio.run(
        orchestrator.run_workflow(
            WorkflowRequest(
                incident_id=incident_id,
                workflow_type="response_plan",
            )
        )
    )

    assert result.mode == "fallback"
    assert result.workflow_type == "response_plan"
    assert len(result.evidence) == 1
    assert orchestrator.list_runs().runs[0].run_id == result.run_id
