from uuid import UUID

from fastapi import FastAPI, HTTPException, Response, status

from .event_bus import safe_publish, start_incident_consumer
from .metrics import configure_metrics
from .schemas import Task, TaskCreate, TaskUpdate
from .service import TaskService

app = FastAPI(title="Coordination Service")
configure_metrics(app)
service = TaskService()


def handle_incident_created(message: dict) -> None:
    incident = message.get("incident", {})
    incident_id = incident.get("id")
    if not incident_id:
        return

    task = service.create_task(
        TaskCreate(
            incident_id=incident_id,
            title=f"Review {incident.get('type', 'incident')} response for {incident.get('location', 'unknown area')}",
            team="Operations",
            priority=incident.get("severity", "medium"),
        )
    )
    safe_publish(
        "task.created",
        {
            "event_type": "task.created",
            "task": task.model_dump(mode="json"),
            "occurred_at": task.created_at.isoformat(),
        },
    )


@app.on_event("startup")
def startup_consumer() -> None:
    start_incident_consumer(handle_incident_created)


@app.get("/health")
def health() -> dict:
    return {"service": "coordination-service", "status": "ok", "phase": 7}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return service.list_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID) -> Task:
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    task = service.create_task(payload)
    safe_publish(
        "task.created",
        {
            "event_type": "task.created",
            "task": task.model_dump(mode="json"),
            "occurred_at": task.created_at.isoformat(),
        },
    )
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, payload: TaskUpdate) -> Task:
    task = service.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID) -> Response:
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
