from app.schemas import IncidentCreate, IncidentUpdate
from app.service import IncidentService


def test_service_create_update_delete_incident():
    service = IncidentService()
    initial_count = len(service.list_incidents())

    incident = service.create_incident(
        IncidentCreate(
            title="Bridge collapse risk",
            type="storm",
            severity="high",
            location="Zone B",
            description="Structural cracking has been reported after heavy wind.",
        )
    )

    assert len(service.list_incidents()) == initial_count + 1
    assert service.get_incident(incident.id) is not None

    updated = service.update_incident(incident.id, IncidentUpdate(status="in_progress", severity="critical"))
    assert updated is not None
    assert updated.status == "in_progress"
    assert updated.severity == "critical"

    assert service.delete_incident(incident.id) is True
    assert service.get_incident(incident.id) is None
