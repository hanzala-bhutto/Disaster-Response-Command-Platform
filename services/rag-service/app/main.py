from fastapi import FastAPI

app = FastAPI(title="RAG Service")


@app.get("/health")
def health() -> dict:
    return {"service": "rag-service", "status": "ok", "phase": 1}
