from fastapi import FastAPI

from .metrics import configure_metrics
from .schemas import KnowledgeDocument, KnowledgeDocumentCreate, SearchRequest, SearchResponse
from .service import RagService

app = FastAPI(title="RAG Service")
configure_metrics(app)
service = RagService()


@app.get("/health")
def health() -> dict:
    return {"service": "rag-service", "status": "ok", "phase": 7}


@app.get("/documents", response_model=list[KnowledgeDocument])
def list_documents() -> list[KnowledgeDocument]:
    return service.list_documents()


@app.post("/documents", response_model=KnowledgeDocument)
def create_document(payload: KnowledgeDocumentCreate) -> KnowledgeDocument:
    return service.add_document(payload)


@app.post("/search", response_model=SearchResponse)
def search(payload: SearchRequest) -> SearchResponse:
    return service.search(payload)
