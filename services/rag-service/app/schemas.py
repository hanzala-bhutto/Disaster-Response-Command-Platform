from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


IncidentType = Literal["flood", "fire", "earthquake", "storm", "heatwave", "other"]


class KnowledgeDocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    category: str = Field(min_length=2, max_length=80)
    incident_type: IncidentType
    source: str = Field(min_length=2, max_length=160)
    content: str = Field(min_length=20, max_length=20000)


class KnowledgeDocument(BaseModel):
    id: UUID
    title: str
    category: str
    incident_type: IncidentType
    source: str
    content_preview: str
    chunk_count: int
    created_at: datetime


class KnowledgeChunkResult(BaseModel):
    id: str
    document_id: UUID
    document_title: str
    incident_type: IncidentType
    source: str
    chunk_index: int
    text: str
    score: float


class SearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)
    incident_type: IncidentType | None = None
    limit: int = Field(default=5, ge=1, le=10)


class SearchResponse(BaseModel):
    query: str
    matches: list[KnowledgeChunkResult]
