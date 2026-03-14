from datetime import datetime, timezone
from threading import Lock
from uuid import UUID, uuid4

from .metrics import record_incident_mutation, set_incident_store_size
from .schemas import Incident, IncidentCreate, IncidentUpdate


class IncidentService:
    def __init__(self) -> None:
        self._lock = Lock()
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
        with self._lock:
            self._incidents[sample.id] = sample
            set_incident_store_size(len(self._incidents))

    def list_incidents(self) -> list[Incident]:
        with self._lock:
            incidents = list(self._incidents.values())
        return sorted(incidents, key=lambda incident: incident.created_at, reverse=True)

    def get_incident(self, incident_id: UUID) -> Incident | None:
        with self._lock:
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
        with self._lock:
            self._incidents[incident.id] = incident
            set_incident_store_size(len(self._incidents))
        record_incident_mutation("create", incident.severity)
        return incident

    def update_incident(self, incident_id: UUID, payload: IncidentUpdate) -> Incident | None:
        with self._lock:
            incident = self._incidents.get(incident_id)
        if incident is None:
            return None

        updated = incident.model_copy(update=payload.model_dump(exclude_none=True))
        with self._lock:
            self._incidents[incident_id] = updated
        record_incident_mutation("update", updated.severity)
        return updated

    def delete_incident(self, incident_id: UUID) -> bool:
        with self._lock:
            if incident_id not in self._incidents:
                return False

            incident = self._incidents[incident_id]
            del self._incidents[incident_id]
            set_incident_store_size(len(self._incidents))
        record_incident_mutation("delete", incident.severity)
        return True
