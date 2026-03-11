from datetime import datetime, timezone
from threading import Lock
from uuid import UUID, uuid4

from qdrant_client import models

from .chunking import chunk_text
from .embedding import embedding_service
from .repository import repository
from .schemas import KnowledgeChunkResult, KnowledgeDocument, KnowledgeDocumentCreate, SearchRequest, SearchResponse
from .settings_data import settings


class RagService:
    def __init__(self) -> None:
        self._lock = Lock()
        self._documents: dict[UUID, KnowledgeDocument] = {}
        self._seed()

    def _seed(self) -> None:
        if self._documents:
            return

        self.add_document(
            KnowledgeDocumentCreate(
                title="Flood Response Quick Guide",
                category="SOP",
                incident_type="flood",
                source="Sample Manual",
                content=(
                    "When flooding is reported, first confirm affected zones and blocked roads. "
                    "Prioritize evacuation for low-lying areas and communicate shelter locations. "
                    "Coordinate with medical and transport teams, and monitor river levels every 15 minutes."
                ),
            )
        )

    def list_documents(self) -> list[KnowledgeDocument]:
        with self._lock:
            documents = list(self._documents.values())
        return sorted(documents, key=lambda document: document.created_at, reverse=True)

    def add_document(self, payload: KnowledgeDocumentCreate) -> KnowledgeDocument:
        repository.ensure_collection()
        document_id = uuid4()
        chunks = chunk_text(payload.content, settings.chunk_size_words, settings.chunk_overlap_words)
        created_at = datetime.now(timezone.utc)
        points: list[models.PointStruct] = []

        for index, chunk in enumerate(chunks):
            chunk_id = str(uuid4())
            vector = embedding_service.embed_text(chunk)
            points.append(
                models.PointStruct(
                    id=chunk_id,
                    vector=vector,
                    payload={
                        "document_id": str(document_id),
                        "document_title": payload.title,
                        "incident_type": payload.incident_type,
                        "category": payload.category,
                        "source": payload.source,
                        "chunk_index": index,
                        "text": chunk,
                        "created_at": created_at.isoformat(),
                    },
                )
            )

        repository.upsert_points(points)

        document = KnowledgeDocument(
            id=document_id,
            title=payload.title,
            category=payload.category,
            incident_type=payload.incident_type,
            source=payload.source,
            content_preview=payload.content[:160],
            chunk_count=len(chunks),
            created_at=created_at,
        )
        with self._lock:
            self._documents[document_id] = document
        return document

    def search(self, payload: SearchRequest) -> SearchResponse:
        repository.ensure_collection()
        vector = embedding_service.embed_text(payload.query)
        results = repository.search(vector, limit=payload.limit, incident_type=payload.incident_type)
        matches = [
            KnowledgeChunkResult(
                id=str(result.id),
                document_id=result.payload["document_id"],
                document_title=result.payload["document_title"],
                incident_type=result.payload["incident_type"],
                source=result.payload["source"],
                chunk_index=result.payload["chunk_index"],
                text=result.payload["text"],
                score=float(result.score),
            )
            for result in results
        ]
        return SearchResponse(query=payload.query, matches=matches)
