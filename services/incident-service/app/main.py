from fastapi import FastAPI

app = FastAPI(title="Incident Service")


@app.get("/health")
def health() -> dict:
    return {"service": "incident-service", "status": "ok", "phase": 1}
