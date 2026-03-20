from datetime import datetime, timezone
from importlib import import_module
from uuid import uuid4

from fastapi.testclient import TestClient


def load_main(monkeypatch):
    service_module = import_module("app.service")
    monkeypatch.setattr(service_module.RagService, "_seed", lambda self: None)
    main = import_module("app.main")
    monkeypatch.setattr(main, "service", service_module.RagService())
    return main


def test_health_endpoint(monkeypatch):
    main = load_main(monkeypatch)
    client = TestClient(main.app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "rag-service"


def test_document_and_search_routes(monkeypatch):
    main = load_main(monkeypatch)
    client = TestClient(main.app)

    document_id = uuid4()
    created_at = datetime.now(timezone.utc)
    document = {
        "id": str(document_id),
        "title": "Flood SOP",
        "category": "SOP",
        "incident_type": "flood",
        "source": "Manual",
        "content_preview": "Prioritize evacuation in low-lying zones.",
        "chunk_count": 2,
        "created_at": created_at.isoformat(),
    }

    monkeypatch.setattr(main.service, "list_documents", lambda: [document])
    monkeypatch.setattr(main.service, "add_document", lambda payload: document)
    monkeypatch.setattr(
        main.service,
        "search",
        lambda payload: {
            "query": payload.query,
            "matches": [
                {
                    "id": "chunk-1",
                    "document_id": str(document_id),
                    "document_title": "Flood SOP",
                    "incident_type": "flood",
                    "source": "Manual",
                    "chunk_index": 0,
                    "text": "Prioritize evacuation in low-lying zones.",
                    "score": 0.98,
                }
            ],
        },
    )

    list_response = client.get("/documents")
    assert list_response.status_code == 200
    assert list_response.json()[0]["title"] == "Flood SOP"

    create_response = client.post(
        "/documents",
        json={
            "title": "Flood SOP",
            "category": "SOP",
            "incident_type": "flood",
            "source": "Manual",
            "content": "This document explains evacuation, shelter management, and route closure handling for flood events.",
        },
    )
    assert create_response.status_code == 200

    search_response = client.post("/search", json={"query": "evacuation", "incident_type": "flood", "limit": 5})
    assert search_response.status_code == 200
    assert search_response.json()["matches"][0]["document_title"] == "Flood SOP"
