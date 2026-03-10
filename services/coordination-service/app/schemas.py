from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


TaskPriority = Literal["low", "medium", "high", "critical"]
TaskStatus = Literal["todo", "in_progress", "done"]


class TaskCreate(BaseModel):
    incident_id: UUID
    title: str = Field(min_length=3, max_length=120)
    team: str = Field(min_length=2, max_length=120)
    priority: TaskPriority


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=120)
    team: str | None = Field(default=None, min_length=2, max_length=120)
    priority: TaskPriority | None = None
    status: TaskStatus | None = None


class Task(BaseModel):
    id: UUID
    incident_id: UUID
    title: str
    team: str
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
