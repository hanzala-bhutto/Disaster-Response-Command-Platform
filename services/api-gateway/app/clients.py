import httpx
from time import perf_counter
from typing import Any

from .metrics import record_downstream_request
from .settings_data import settings


class ServiceClients:
    async def _request_json(
        self,
        *,
        target_service: str,
        method: str,
        url: str,
        payload: dict | None = None,
        timeout: float = 10.0,
    ) -> Any:
        response: httpx.Response | None = None
        start_time = perf_counter()
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.request(method, url, json=payload)
                response.raise_for_status()
                if response.status_code == 204:
                    return None
                return response.json()
        finally:
            status_code = str(response.status_code) if response is not None else "error"
            record_downstream_request(target_service, method, status_code, perf_counter() - start_time)

    async def get_incidents(self) -> list[dict]:
        return await self._request_json(
            target_service="incident-service",
            method="GET",
            url=f"{settings.incident_service_url}/incidents",
        )

    async def create_incident(self, payload: dict) -> dict:
        return await self._request_json(
            target_service="incident-service",
            method="POST",
            url=f"{settings.incident_service_url}/incidents",
            payload=payload,
        )

    async def update_incident(self, incident_id: str, payload: dict) -> dict:
        return await self._request_json(
            target_service="incident-service",
            method="PATCH",
            url=f"{settings.incident_service_url}/incidents/{incident_id}",
            payload=payload,
        )

    async def delete_incident(self, incident_id: str) -> None:
        await self._request_json(
            target_service="incident-service",
            method="DELETE",
            url=f"{settings.incident_service_url}/incidents/{incident_id}",
        )

    async def get_tasks(self) -> list[dict]:
        return await self._request_json(
            target_service="coordination-service",
            method="GET",
            url=f"{settings.coordination_service_url}/tasks",
        )

    async def create_task(self, payload: dict) -> dict:
        return await self._request_json(
            target_service="coordination-service",
            method="POST",
            url=f"{settings.coordination_service_url}/tasks",
            payload=payload,
        )

    async def update_task(self, task_id: str, payload: dict) -> dict:
        return await self._request_json(
            target_service="coordination-service",
            method="PATCH",
            url=f"{settings.coordination_service_url}/tasks/{task_id}",
            payload=payload,
        )

    async def delete_task(self, task_id: str) -> None:
        await self._request_json(
            target_service="coordination-service",
            method="DELETE",
            url=f"{settings.coordination_service_url}/tasks/{task_id}",
        )

    async def get_notifications(self) -> list[dict]:
        return await self._request_json(
            target_service="notification-service",
            method="GET",
            url=f"{settings.notification_service_url}/notifications",
        )

    async def get_documents(self) -> list[dict]:
        return await self._request_json(
            target_service="rag-service",
            method="GET",
            url=f"{settings.rag_service_url}/documents",
        )

    async def create_document(self, payload: dict) -> dict:
        return await self._request_json(
            target_service="rag-service",
            method="POST",
            url=f"{settings.rag_service_url}/documents",
            payload=payload,
            timeout=20.0,
        )

    async def search_knowledge(self, payload: dict) -> dict:
        return await self._request_json(
            target_service="rag-service",
            method="POST",
            url=f"{settings.rag_service_url}/search",
            payload=payload,
            timeout=20.0,
        )

    async def run_ai_workflow(self, payload: dict) -> dict:
        return await self._request_json(
            target_service="ai-orchestrator",
            method="POST",
            url=f"{settings.ai_orchestrator_url}/workflows/run",
            payload=payload,
            timeout=30.0,
        )

    async def get_ai_workflow_runs(self) -> dict:
        return await self._request_json(
            target_service="ai-orchestrator",
            method="GET",
            url=f"{settings.ai_orchestrator_url}/workflow-runs",
            timeout=20.0,
        )


clients = ServiceClients()
