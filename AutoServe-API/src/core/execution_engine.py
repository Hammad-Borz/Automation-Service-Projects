from __future__ import annotations

from typing import Any

from src.core.action_registry import ActionRegistry, UnknownAutomationActionError
from src.core.state_machine import validate_transition
from src.database.repository import AutomationRepository
from src.models.automation import ActionResult, AutomationJob, AutomationRun, JobStatus, RunStatus, utc_now


class ExecutionEngine:
    """Coordinate execution of an automation job and persist its lifecycle artifacts."""

    def __init__(self, repository: AutomationRepository):
        self.repository = repository

    def execute(self, job: AutomationJob) -> dict[str, Any]:
        if job is None:
            raise ValueError("job is required")
        validate_transition(job.status, JobStatus.RUNNING)
        run = AutomationRun(
            id=f"RUN-{job.id}-{job.retry_count + 1}",
            job_id=job.id,
            status=RunStatus.RUNNING,
            attempt_number=job.retry_count + 1,
        )
        self.repository.create_run(run)
        job.status = JobStatus.RUNNING
        job.updated_at = utc_now()
        self.repository.update_job(job)
        try:
            action = ActionRegistry.get(job.automation_type)
            payload = action(job.payload)
            result = ActionResult(
                id=f"RES-{run.id}",
                run_id=run.id,
                action_type=job.automation_type,
                success=True,
                result=payload,
            )
            self.repository.create_action_result(result)
            run.status = RunStatus.COMPLETED
            run.completed_at = utc_now()
            self.repository.update_run(run)
            job.status = JobStatus.COMPLETED
            job.updated_at = utc_now()
            self.repository.update_job(job)
            return {
                "job_id": job.id,
                "run_id": run.id,
                "attempt_number": run.attempt_number,
                "status": "completed",
                "result": payload,
            }
        except UnknownAutomationActionError:
            run.status = RunStatus.FAILED
            run.completed_at = utc_now()
            run.error_message = "Unknown automation action."
            self.repository.update_run(run)
            job.status = JobStatus.FAILED
            job.updated_at = utc_now()
            self.repository.update_job(job)
            raise
