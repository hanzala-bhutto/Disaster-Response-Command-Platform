from datetime import datetime, timezone
from uuid import UUID, uuid4

from .schemas import Incident, IncidentCreate, IncidentUpdate


class IncidentService:
    def __init__(self) -> None:
        self._incidents: dict[UUID, Incident] = {}
        self._seed()

    def _seed(self) -> None:
        sample = Incident(
            id=uuid4(),
            title="River overflow near central bridge",
            type="flood",
            severity="high",
            location="Zone A",
            description="Water level is rising and nearby streets are partially blocked.",
            status="new",
            created_at=datetime.now(timezone.utc),
        )
        self._incidents[sample.id] = sample

    def list_incidents(self) -> list[Incident]:
        return sorted(self._incidents.values(), key=lambda incident: incident.created_at, reverse=True)

    def get_incident(self, incident_id: UUID) -> Incident | None:
        return self._incidents.get(incident_id)

    def create_incident(self, payload: IncidentCreate) -> Incident:
        incident = Incident(
            id=uuid4(),
            title=payload.title,
            type=payload.type,
            severity=payload.severity,
            location=payload.location,
            description=payload.description,
            status="new",
            created_at=datetime.now(timezone.utc),
        )
        self._incidents[incident.id] = incident
        return incident

    def update_incident(self, incident_id: UUID, payload: IncidentUpdate) -> Incident | None:
        incident = self._incidents.get(incident_id)
        if incident is None:
            return None

        updated = incident.model_copy(update=payload.model_dump(exclude_none=True))
        self._incidents[incident_id] = updated
        return updated

    def delete_incident(self, incident_id: UUID) -> bool:
        if incident_id not in self._incidents:
            return False

        del self._incidents[incident_id]
        return True
