from uuid import UUID

from fastapi import FastAPI, HTTPException, Response, status

from .schemas import Task, TaskCreate, TaskUpdate
from .service import TaskService

app = FastAPI(title="Coordination Service")
service = TaskService()


@app.get("/health")
def health() -> dict:
    return {"service": "coordination-service", "status": "ok", "phase": 2}


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
    return service.create_task(payload)


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
