from uuid import UUID

from fastapi import FastAPI, HTTPException, Response, status

from .event_bus import safe_publish
from .metrics import configure_metrics
from .schemas import Incident, IncidentCreate, IncidentUpdate
from .service import IncidentService

app = FastAPI(title="Incident Service")
configure_metrics(app)
service = IncidentService()


@app.get("/health")
def health() -> dict:
    return {"service": "incident-service", "status": "ok", "phase": 7}


@app.get("/incidents", response_model=list[Incident])
def list_incidents() -> list[Incident]:
    return service.list_incidents()


@app.get("/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: UUID) -> Incident:
    incident = service.get_incident(incident_id)
    if incident is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return incident


@app.post("/incidents", response_model=Incident, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate) -> Incident:
    incident = service.create_incident(payload)
    safe_publish(
        "incident.created",
        {
            "event_type": "incident.created",
            "incident": incident.model_dump(mode="json"),
            "occurred_at": incident.created_at.isoformat(),
        },
    )
    return incident


@app.patch("/incidents/{incident_id}", response_model=Incident)
def update_incident(incident_id: UUID, payload: IncidentUpdate) -> Incident:
    incident = service.update_incident(incident_id, payload)
    if incident is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return incident


@app.delete("/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: UUID) -> Response:
    deleted = service.delete_incident(incident_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
