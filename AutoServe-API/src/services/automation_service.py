from __future__ import annotations

import json
from typing import Any

from src.config import MAX_RETRY_COUNT
from src.core.action_registry import ActionRegistry, UnknownAutomationActionError
from src.core.idempotency import DuplicateRequestError, ensure_unique_request_id, normalize_request_id
from src.core.retry_manager import RetryLimitExceededError, build_retry_state
from src.core.state_machine import StateTransitionError, validate_transition
from src.database.repository import AutomationRepository
from src.models.automation import ActionResult, AuditEvent, AutomationJob, AutomationRun, JobStatus, RunStatus, utc_now


class AutomationService:
    def __init__(self, repository: AutomationRepository):
        self.repository = repository

    def create_job(self, *, automation_type: str, payload: dict[str, Any], request_id: str) -> AutomationJob:
        normalized_request_id = normalize_request_id(request_id)
        existing = self.repository.get_job_by_request_id(normalized_request_id)
        if existing:
            raise DuplicateRequestError(f"Request ID '{normalized_request_id}' already exists.")
        if not automation_type or not automation_type.strip():
            raise ValueError("automation_type is required")
        if not isinstance(payload, dict):
            raise ValueError("payload must be a JSON object")
        job = AutomationJob(
            id=f"JOB-{self._generate_seed()}",
            request_id=normalized_request_id,
            automation_type=automation_type.strip(),
            payload=payload,
            status=JobStatus.PENDING,
        )
        return self.repository.create_job(job)

    def get_job(self, job_id: str) -> AutomationJob | None:
        return self.repository.get_job_by_id(job_id)

    def get_job_by_request_id(self, request_id: str) -> AutomationJob | None:
        return self.repository.get_job_by_request_id(normalize_request_id(request_id))

    def list_jobs(self, status: str | None = None, automation_type: str | None = None) -> list[AutomationJob]:
        return self.repository.list_jobs(status=status, automation_type=automation_type)

    def execute_job(self, job_id: str) -> dict[str, Any]:
        job = self.repository.get_job_by_id(job_id)
        if job is None:
            raise KeyError(f"Automation job '{job_id}' was not found.")
        handler = ActionRegistry.get(job.automation_type)
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
            result_payload = handler(job.payload)
            action_result = ActionResult(
                id=f"RES-{run.id}",
                run_id=run.id,
                action_type=job.automation_type,
                success=True,
                result=result_payload,
            )
            self.repository.create_action_result(action_result)
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
                "result": action_result.result,
            }
        except Exception as exc:  # pragma: no cover - handled by route error handler
            run.status = RunStatus.FAILED
            run.completed_at = utc_now()
            run.error_message = str(exc)
            self.repository.update_run(run)
            job.status = JobStatus.FAILED
            job.updated_at = utc_now()
            self.repository.update_job(job)
            raise

    def retry_job(self, job_id: str, *, max_retries: int = MAX_RETRY_COUNT) -> dict[str, Any]:
        job = self.repository.get_job_by_id(job_id)
        if job is None:
            raise KeyError(f"Automation job '{job_id}' was not found.")
        if job.status not in (JobStatus.FAILED, JobStatus.COMPLETED):
            raise ValueError("Only completed or failed jobs can be retried.")
        existing_runs = self.repository.list_runs(job_id=job.id)
        current_attempt = max(len(existing_runs), job.retry_count + 1)
        retry_state = build_retry_state(current_attempt, max_retries=max_retries)
        job.retry_count = retry_state.retry_count
        next_attempt = retry_state.attempt_number
        run = AutomationRun(
            id=f"RUN-{job.id}-{next_attempt}",
            job_id=job.id,
            status=RunStatus.RUNNING,
            attempt_number=next_attempt,
        )
        self.repository.create_run(run)
        job.status = JobStatus.RUNNING
        job.updated_at = utc_now()
        self.repository.update_job(job)
        try:
            handler = ActionRegistry.get(job.automation_type)
            result_payload = handler(job.payload)
            action_result = ActionResult(
                id=f"RES-{run.id}",
                run_id=run.id,
                action_type=job.automation_type,
                success=True,
                result=result_payload,
            )
            self.repository.create_action_result(action_result)
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
                "result": action_result.result,
            }
        except Exception as exc:  # pragma: no cover - handled by route error handler
            run.status = RunStatus.FAILED
            run.completed_at = utc_now()
            run.error_message = str(exc)
            self.repository.update_run(run)
            job.status = JobStatus.FAILED
            job.updated_at = utc_now()
            self.repository.update_job(job)
            raise

    @staticmethod
    def _generate_seed() -> str:
        import uuid

        return uuid.uuid4().hex[:8].upper()
