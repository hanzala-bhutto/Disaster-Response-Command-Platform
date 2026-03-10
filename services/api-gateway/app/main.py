from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

from .clients import clients

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"service": "api-gateway", "status": "ok", "phase": 2}


@app.get("/incidents")
async def list_incidents() -> list[dict]:
    return await clients.get_incidents()


@app.post("/incidents", status_code=status.HTTP_201_CREATED)
async def create_incident(payload: dict) -> dict:
    return await clients.create_incident(payload)


@app.patch("/incidents/{incident_id}")
async def update_incident(incident_id: str, payload: dict) -> dict:
    return await clients.update_incident(incident_id, payload)


@app.delete("/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_incident(incident_id: str) -> Response:
    await clients.delete_incident(incident_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/tasks")
async def list_tasks() -> list[dict]:
    return await clients.get_tasks()


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(payload: dict) -> dict:
    return await clients.create_task(payload)


@app.patch("/tasks/{task_id}")
async def update_task(task_id: str, payload: dict) -> dict:
    return await clients.update_task(task_id, payload)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str) -> Response:
    await clients.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.exception_handler(httpx.HTTPStatusError)
async def http_status_error_handler(_, exc: httpx.HTTPStatusError):
    detail = exc.response.text or "Downstream service error"
    return JSONResponse(status_code=exc.response.status_code, content={"detail": detail})


@app.exception_handler(httpx.RequestError)
async def request_error_handler(_, exc: httpx.RequestError):
    return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content={"detail": str(exc)})
