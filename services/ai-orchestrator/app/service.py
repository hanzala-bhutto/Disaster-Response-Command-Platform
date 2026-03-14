import asyncio
from datetime import datetime, timezone
from threading import Lock
from time import perf_counter

from .clients import clients
from .llm_client import llm_client
from .metrics import record_workflow_run, set_workflow_history_size
from .prompts import build_prompt
from .schemas import EvidenceItem, WorkflowHistory, WorkflowRequest, WorkflowResult


class OrchestratorService:
    def __init__(self) -> None:
        self._lock = Lock()
        self._runs: list[WorkflowResult] = []
        set_workflow_history_size(0)

    def list_runs(self) -> WorkflowHistory:
        with self._lock:
            return WorkflowHistory(runs=list(self._runs))

    async def run_workflow(self, payload: WorkflowRequest) -> WorkflowResult:
        start_time = perf_counter()
        incident, tasks, notifications = await asyncio.gather(
            clients.get_incident(str(payload.incident_id)),
            clients.get_tasks(),
            clients.get_notifications(),
        )
        related_tasks = [task for task in tasks if task.get("incident_id") == str(payload.incident_id)]
        related_notifications = [note for note in notifications if note.get("incident_id") == str(payload.incident_id)]

        retrieval_query = payload.question or f"{incident['title']} {incident['description']}"
        search_response = await clients.search_knowledge(
            {
                "query": retrieval_query,
                "incident_type": incident.get("type"),
                "limit": 5,
            }
        )
        evidence = [EvidenceItem(**match) for match in search_response.get("matches", [])]

        prompt = build_prompt(
            workflow_type=payload.workflow_type,
            incident=incident,
            tasks=related_tasks,
            notifications=related_notifications,
            evidence=[item.model_dump() for item in evidence],
            question=payload.question,
        )
        llm_response = await llm_client.generate(prompt)
        if llm_response:
            result = self._build_result(payload, evidence, llm_response, mode="llm")
        else:
            result = self._build_fallback(payload, incident, evidence)

        with self._lock:
            self._runs.insert(0, result)
            set_workflow_history_size(len(self._runs))
        record_workflow_run(payload.workflow_type, result.mode, perf_counter() - start_time)
        return result

    def _build_result(self, payload: WorkflowRequest, evidence: list[EvidenceItem], response: dict, mode: str) -> WorkflowResult:
        return WorkflowResult(
            incident_id=payload.incident_id,
            workflow_type=payload.workflow_type,
            mode=mode,
            summary=response.get("summary", "No summary returned."),
            response_plan=self._ensure_list(response.get("response_plan")),
            resource_needs=self._ensure_list(response.get("resource_needs")),
            caution_notes=self._ensure_list(response.get("caution_notes")),
            public_message=response.get("public_message", "No advisory message returned."),
            evidence=evidence,
            created_at=datetime.now(timezone.utc),
        )

    def _build_fallback(self, payload: WorkflowRequest, incident: dict, evidence: list[EvidenceItem]) -> WorkflowResult:
        severity = incident.get("severity", "medium")
        location = incident.get("location", "the affected area")
        incident_type = incident.get("type", "incident")
        top_evidence = evidence[:2]
        evidence_line = (
            " Use the retrieved guidance in the evidence panel for details."
            if top_evidence
            else " Add knowledge documents to improve this plan."
        )

        response = {
            "summary": f"{incident['title']} is a {severity} severity {incident_type} event affecting {location}.{evidence_line}",
            "response_plan": [
                f"Confirm the situation and establish an operations lead for {location}.",
                f"Dispatch the first response team and verify evacuation or shelter needs for this {incident_type}.",
                "Review the highest-scoring SOP chunks and align actions with them.",
                "Track field updates, blocked routes, and medical needs every 15 minutes.",
            ],
            "resource_needs": [
                "Operations lead",
                "Field response team",
                "Public communication support",
            ],
            "caution_notes": [
                "Do not send public messages without human review.",
                "Validate road, weather, and medical status before dispatch decisions.",
            ],
            "public_message": f"Emergency teams are responding to a {incident_type} incident near {location}. Please follow official guidance and avoid the affected area until more information is shared.",
        }
        return self._build_result(payload, evidence, response, mode="fallback")

    def _ensure_list(self, value: object) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        if value is None:
            return []
        return [str(value)]


service = OrchestratorService()
