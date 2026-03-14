from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx

from .metrics import configure_metrics
from .schemas import WorkflowHistory, WorkflowRequest, WorkflowResult
from .service import service

app = FastAPI(title="AI Orchestrator")
configure_metrics(app)


@app.get("/health")
def health() -> dict:
    return {"service": "ai-orchestrator", "status": "ok", "phase": 7}


@app.get("/workflow-runs", response_model=WorkflowHistory)
def list_runs() -> WorkflowHistory:
    return service.list_runs()


@app.post("/workflows/run", response_model=WorkflowResult)
async def run_workflow(payload: WorkflowRequest) -> WorkflowResult:
    return await service.run_workflow(payload)


@app.exception_handler(httpx.HTTPStatusError)
async def http_status_error_handler(_, exc: httpx.HTTPStatusError):
    detail = exc.response.text or "Downstream service error"
    return JSONResponse(status_code=exc.response.status_code, content={"detail": detail})


@app.exception_handler(httpx.RequestError)
async def request_error_handler(_, exc: httpx.RequestError):
    return JSONResponse(status_code=502, content={"detail": str(exc)})
