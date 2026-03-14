from fastapi import FastAPI

from .metrics import configure_metrics

app = FastAPI(title="Ingestion Service")
configure_metrics(app)


@app.get("/health")
def health() -> dict:
    return {"service": "ingestion-service", "status": "ok", "phase": 7}
