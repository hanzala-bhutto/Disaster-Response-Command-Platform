from datetime import datetime, timezone
from threading import Lock
from uuid import UUID, uuid4

from .metrics import record_task_mutation, set_task_store_size
from .schemas import Task, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self) -> None:
        self._lock = Lock()
        self._tasks: dict[UUID, Task] = {}

    def list_tasks(self) -> list[Task]:
        with self._lock:
            tasks = list(self._tasks.values())
        return sorted(tasks, key=lambda task: task.created_at, reverse=True)

    def get_task(self, task_id: UUID) -> Task | None:
        with self._lock:
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
        with self._lock:
            self._tasks[task.id] = task
            set_task_store_size(len(self._tasks))
        record_task_mutation("create", task.team, task.priority)
        return task

    def update_task(self, task_id: UUID, payload: TaskUpdate) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
        if task is None:
            return None

        updated = task.model_copy(update=payload.model_dump(exclude_none=True))
        with self._lock:
            self._tasks[task_id] = updated
        record_task_mutation("update", updated.team, updated.priority)
        return updated

    def delete_task(self, task_id: UUID) -> bool:
        with self._lock:
            if task_id not in self._tasks:
                return False

            task = self._tasks[task_id]
            del self._tasks[task_id]
            set_task_store_size(len(self._tasks))
        record_task_mutation("delete", task.team, task.priority)
        return True
