"""Task business logic and durable JSON persistence."""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path

from .logger import get_logger
from .models import Priority, Status, Task, TaskCreate, TaskSummary, TaskUpdate, utc_now


class TaskNotFoundError(LookupError):
    """Raised when a requested task does not exist."""


class TaskStorageError(RuntimeError):
    """Raised when the on-disk task store is unreadable."""


class TaskManager:
    def __init__(self, storage_path: str | Path | None = None) -> None:
        self.storage_path = Path(storage_path) if storage_path else Path(__file__).resolve().parents[1] / "data" / "tasks.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self.logger = get_logger(self.storage_path.parent.parent / "logs")
        if not self.storage_path.exists():
            self._write([])

    def _read(self) -> list[Task]:
        try:
            with self.storage_path.open("r", encoding="utf-8") as source:
                raw = json.load(source)
            if not isinstance(raw, list):
                raise ValueError("task storage must contain a JSON array")
            return [Task.model_validate(item) for item in raw]
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            raise TaskStorageError(f"Unable to read task storage: {exc}") from exc

    def _write(self, tasks: list[Task]) -> None:
        temporary = self.storage_path.with_suffix(".tmp")
        try:
            with temporary.open("w", encoding="utf-8") as target:
                json.dump([task.model_dump(mode="json") for task in tasks], target, indent=2)
                target.flush()
                os.fsync(target.fileno())
            temporary.replace(self.storage_path)
        except OSError as exc:
            if temporary.exists():
                temporary.unlink(missing_ok=True)
            raise TaskStorageError(f"Unable to write task storage: {exc}") from exc

    def create_task(self, request: TaskCreate) -> Task:
        with self._lock:
            tasks = self._read()
            task = Task(**request.model_dump())
            tasks.append(task)
            self._write(tasks)
        self.logger.info("task created: %s", task.id)
        return task

    def list_tasks(self, status: Status | None = None) -> list[Task]:
        with self._lock:
            tasks = self._read()
        return [task for task in tasks if task.status == status] if status else tasks

    @staticmethod
    def _task_index(tasks: list[Task], task_id: str) -> int:
        for index, task in enumerate(tasks):
            if task.id == task_id:
                return index
        raise TaskNotFoundError(f"Task '{task_id}' was not found")

    def update_task(self, task_id: str, request: TaskUpdate) -> Task:
        with self._lock:
            tasks = self._read()
            index = self._task_index(tasks, task_id)
            updated = tasks[index].model_copy(update=request.model_dump(exclude_none=True) | {"updated_at": utc_now()})
            tasks[index] = updated
            self._write(tasks)
        self.logger.info("task updated: %s", task_id)
        return updated

    def complete_task(self, task_id: str) -> Task:
        with self._lock:
            tasks = self._read()
            index = self._task_index(tasks, task_id)
            completed = tasks[index].model_copy(update={"status": Status.COMPLETED, "updated_at": utc_now()})
            tasks[index] = completed
            self._write(tasks)
        self.logger.info("task completed: %s", task_id)
        return completed

    def delete_task(self, task_id: str) -> Task:
        with self._lock:
            tasks = self._read()
            index = self._task_index(tasks, task_id)
            deleted = tasks.pop(index)
            self._write(tasks)
        self.logger.info("task deleted: %s", task_id)
        return deleted

    def get_task_summary(self) -> TaskSummary:
        tasks = self.list_tasks()
        return TaskSummary(total_tasks=len(tasks), pending_tasks=sum(task.status == Status.PENDING for task in tasks), completed_tasks=sum(task.status == Status.COMPLETED for task in tasks), priority_breakdown={priority.value: sum(task.priority == priority for task in tasks) for priority in Priority})
