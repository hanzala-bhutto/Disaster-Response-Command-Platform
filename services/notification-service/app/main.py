from fastapi import FastAPI

app = FastAPI(title="Notification Service")


@app.get("/health")
def health() -> dict:
    return {"service": "notification-service", "status": "ok", "phase": 1}
