from importlib import import_module
from types import SimpleNamespace

from app.schemas import KnowledgeDocumentCreate, SearchRequest


def test_add_document_and_search(monkeypatch):
    service_module = import_module("app.service")
    monkeypatch.setattr(service_module.RagService, "_seed", lambda self: None)

    upserted_points = []

    monkeypatch.setattr(service_module.repository, "ensure_collection", lambda: None)
    monkeypatch.setattr(service_module.repository, "upsert_points", lambda points: upserted_points.extend(points))
    monkeypatch.setattr(service_module, "chunk_text", lambda text, size, overlap: ["chunk one", "chunk two"])
    monkeypatch.setattr(service_module.embedding_service, "embed_text", lambda text: [0.1, 0.2, 0.3])
    monkeypatch.setattr(
        service_module.repository,
        "search",
        lambda vector, limit, incident_type=None: [
            SimpleNamespace(
                id="chunk-1",
                payload={
                    "document_id": str("123e4567-e89b-12d3-a456-426614174000"),
                    "document_title": "Flood SOP",
                    "incident_type": "flood",
                    "source": "Manual",
                    "chunk_index": 0,
                    "text": "Evacuate low-lying zones first.",
                },
                score=0.91,
            )
        ],
    )

    service = service_module.RagService()
    document = service.add_document(
        KnowledgeDocumentCreate(
            title="Flood SOP",
            category="SOP",
            incident_type="flood",
            source="Manual",
            content="This document explains evacuation priorities, shelter setup, and flood route management in detail.",
        )
    )

    assert document.chunk_count == 2
    assert len(upserted_points) == 2

    result = service.search(SearchRequest(query="evacuate", incident_type="flood", limit=5))
    assert len(result.matches) == 1
    assert result.matches[0].document_title == "Flood SOP"
