from __future__ import annotations

from typing import Any

from src.database.repository import AutomationRepository
from src.models.automation import AutomationRun, RunStatus


class RunService:
    def __init__(self, repository: AutomationRepository):
        self.repository = repository

    def create_run(self, *, job_id: str, attempt_number: int, status: RunStatus = RunStatus.RUNNING) -> AutomationRun:
        run = AutomationRun(
            id=f"RUN-{job_id}-{attempt_number}",
            job_id=job_id,
            status=status,
            attempt_number=attempt_number,
        )
        return self.repository.create_run(run)

    def get_run(self, run_id: str) -> AutomationRun | None:
        return self.repository.get_run_by_id(run_id)

    def list_runs(self, *, job_id: str | None = None, status: str | None = None) -> list[AutomationRun]:
        return self.repository.list_runs(job_id=job_id, status=status)

    def update_run_state(self, run: AutomationRun, *, status: RunStatus, error_message: str | None = None) -> AutomationRun:
        run.status = status
        run.error_message = error_message
        run.completed_at = run.started_at if status in (RunStatus.COMPLETED, RunStatus.FAILED) else None
        return self.repository.update_run(run)
