from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


NotificationLevel = Literal["info", "warning", "critical"]


class Notification(BaseModel):
    id: UUID
    incident_id: UUID | None = None
    task_id: UUID | None = None
    title: str
    message: str
    level: NotificationLevel
    source_event: str
    created_at: datetime
