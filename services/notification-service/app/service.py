from datetime import datetime, timezone
from threading import Lock
from uuid import UUID, uuid4

from .schemas import Notification


class NotificationService:
    def __init__(self) -> None:
        self._lock = Lock()
        self._notifications: list[Notification] = []

    def list_notifications(self) -> list[Notification]:
        with self._lock:
            return list(self._notifications)

    def add_notification(
        self,
        *,
        title: str,
        message: str,
        level: str,
        source_event: str,
        incident_id: UUID | None = None,
        task_id: UUID | None = None,
    ) -> Notification:
        notification = Notification(
            id=uuid4(),
            incident_id=incident_id,
            task_id=task_id,
            title=title,
            message=message,
            level=level,
            source_event=source_event,
            created_at=datetime.now(timezone.utc),
        )
        with self._lock:
            self._notifications.insert(0, notification)
        return notification
