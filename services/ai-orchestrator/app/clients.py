import httpx

from .settings_data import settings


class DownstreamClients:
    async def get_incident(self, incident_id: str) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.incident_service_url}/incidents/{incident_id}")
            response.raise_for_status()
            return response.json()

    async def get_tasks(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.coordination_service_url}/tasks")
            response.raise_for_status()
            return response.json()

    async def get_notifications(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.notification_service_url}/notifications")
            response.raise_for_status()
            return response.json()

    async def search_knowledge(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(f"{settings.rag_service_url}/search", json=payload)
            response.raise_for_status()
            return response.json()


clients = DownstreamClients()
