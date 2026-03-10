from fastapi import FastAPI

app = FastAPI(title="Ingestion Service")


@app.get("/health")
def health() -> dict:
    return {"service": "ingestion-service", "status": "ok", "phase": 1}
