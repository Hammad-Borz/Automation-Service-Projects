from __future__ import annotations

from src.database.repository import AutomationRepository
from src.models.automation import AutomationJob


class JobManager:
    def __init__(self, repository: AutomationRepository):
        self.repository = repository

    def create(self, job: AutomationJob) -> AutomationJob:
        return self.repository.create_job(job)

    def get(self, job_id: str) -> AutomationJob | None:
        return self.repository.get_job_by_id(job_id)

    def list(self, *, status: str | None = None, automation_type: str | None = None) -> list[AutomationJob]:
        return self.repository.list_jobs(status=status, automation_type=automation_type)
