from datetime import datetime, timezone
from uuid import UUID, uuid4

from .schemas import Task, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}

    def list_tasks(self) -> list[Task]:
        return sorted(self._tasks.values(), key=lambda task: task.created_at, reverse=True)

    def get_task(self, task_id: UUID) -> Task | None:
        return self._tasks.get(task_id)

    def create_task(self, payload: TaskCreate) -> Task:
        task = Task(
            id=uuid4(),
            incident_id=payload.incident_id,
            title=payload.title,
            team=payload.team,
            priority=payload.priority,
            status="todo",
            created_at=datetime.now(timezone.utc),
        )
        self._tasks[task.id] = task
        return task

    def update_task(self, task_id: UUID, payload: TaskUpdate) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None

        updated = task.model_copy(update=payload.model_dump(exclude_none=True))
        self._tasks[task_id] = updated
        return updated

    def delete_task(self, task_id: UUID) -> bool:
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True
