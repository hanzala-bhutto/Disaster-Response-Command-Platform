from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


IncidentType = Literal["flood", "fire", "earthquake", "storm", "heatwave", "other"]
IncidentSeverity = Literal["low", "medium", "high", "critical"]
IncidentStatus = Literal["new", "in_progress", "resolved"]


class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    type: IncidentType
    severity: IncidentSeverity
    location: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=5, max_length=1000)


class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=120)
    type: IncidentType | None = None
    severity: IncidentSeverity | None = None
    location: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, min_length=5, max_length=1000)
    status: IncidentStatus | None = None


class Incident(BaseModel):
    id: UUID
    title: str
    type: IncidentType
    severity: IncidentSeverity
    location: str
    description: str
    status: IncidentStatus
    created_at: datetime
