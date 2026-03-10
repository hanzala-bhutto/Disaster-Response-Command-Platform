from fastapi import FastAPI

app = FastAPI(title="AI Orchestrator")


@app.get("/health")
def health() -> dict:
    return {"service": "ai-orchestrator", "status": "ok", "phase": 1}
