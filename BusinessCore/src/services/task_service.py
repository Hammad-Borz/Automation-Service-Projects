from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from src.database.repository import TaskRepository
from src.models.task import Task


class TaskService:
    def __init__(self):
        self.repository = TaskRepository()

    def create_task(self, session: Session, task_data: dict[str, Any]) -> Task:
        return self.repository.create(session, task_data)

    def list_tasks(self, session: Session) -> list[Task]:
        return self.repository.list(session)

    def mark_task_completed(self, session: Session, task: Task) -> Task:
        task.status = "completed"
        task.completed_at = datetime.now(timezone.utc)
        session.commit()
        session.refresh(task)
        return task
