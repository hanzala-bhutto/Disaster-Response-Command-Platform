import httpx

from .settings_data import settings


class ServiceClients:
    async def get_incidents(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.incident_service_url}/incidents")
            response.raise_for_status()
            return response.json()

    async def create_incident(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{settings.incident_service_url}/incidents", json=payload)
            response.raise_for_status()
            return response.json()

    async def update_incident(self, incident_id: str, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.patch(f"{settings.incident_service_url}/incidents/{incident_id}", json=payload)
            response.raise_for_status()
            return response.json()

    async def delete_incident(self, incident_id: str) -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(f"{settings.incident_service_url}/incidents/{incident_id}")
            response.raise_for_status()

    async def get_tasks(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.coordination_service_url}/tasks")
            response.raise_for_status()
            return response.json()

    async def create_task(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{settings.coordination_service_url}/tasks", json=payload)
            response.raise_for_status()
            return response.json()

    async def update_task(self, task_id: str, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.patch(f"{settings.coordination_service_url}/tasks/{task_id}", json=payload)
            response.raise_for_status()
            return response.json()

    async def delete_task(self, task_id: str) -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(f"{settings.coordination_service_url}/tasks/{task_id}")
            response.raise_for_status()

    async def get_notifications(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.notification_service_url}/notifications")
            response.raise_for_status()
            return response.json()

    async def get_documents(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.rag_service_url}/documents")
            response.raise_for_status()
            return response.json()

    async def create_document(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(f"{settings.rag_service_url}/documents", json=payload)
            response.raise_for_status()
            return response.json()

    async def search_knowledge(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(f"{settings.rag_service_url}/search", json=payload)
            response.raise_for_status()
            return response.json()


clients = ServiceClients()
