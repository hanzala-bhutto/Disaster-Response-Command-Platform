from fastapi import FastAPI

app = FastAPI(title="Coordination Service")


@app.get("/health")
def health() -> dict:
    return {"service": "coordination-service", "status": "ok", "phase": 1}
