from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


WorkflowType = Literal["triage", "response_plan", "public_advisory"]
RunMode = Literal["llm", "fallback"]


class WorkflowRequest(BaseModel):
    incident_id: UUID
    workflow_type: WorkflowType = "response_plan"
    question: str | None = Field(default=None, max_length=500)


class EvidenceItem(BaseModel):
    document_title: str
    source: str
    incident_type: str
    chunk_index: int
    text: str
    score: float


class WorkflowResult(BaseModel):
    run_id: UUID = Field(default_factory=uuid4)
    incident_id: UUID
    workflow_type: WorkflowType
    mode: RunMode
    summary: str
    response_plan: list[str]
    resource_needs: list[str]
    caution_notes: list[str]
    public_message: str
    evidence: list[EvidenceItem]
    created_at: datetime


class WorkflowHistory(BaseModel):
    runs: list[WorkflowResult]
