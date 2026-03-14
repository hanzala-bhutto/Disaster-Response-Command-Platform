import httpx
from time import perf_counter
from typing import Any

from .metrics import record_downstream_request
from .settings_data import settings


class DownstreamClients:
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
                return response.json()
        finally:
            status_code = str(response.status_code) if response is not None else "error"
            record_downstream_request(target_service, method, status_code, perf_counter() - start_time)

    async def get_incident(self, incident_id: str) -> dict:
        return await self._request_json(
            target_service="incident-service",
            method="GET",
            url=f"{settings.incident_service_url}/incidents/{incident_id}",
        )

    async def get_tasks(self) -> list[dict]:
        return await self._request_json(
            target_service="coordination-service",
            method="GET",
            url=f"{settings.coordination_service_url}/tasks",
        )

    async def get_notifications(self) -> list[dict]:
        return await self._request_json(
            target_service="notification-service",
            method="GET",
            url=f"{settings.notification_service_url}/notifications",
        )

    async def search_knowledge(self, payload: dict) -> dict:
        return await self._request_json(
            target_service="rag-service",
            method="POST",
            url=f"{settings.rag_service_url}/search",
            payload=payload,
            timeout=20.0,
        )


clients = DownstreamClients()
