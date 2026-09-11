from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.schemas import (
    AutomationListResponse,
    CreateJobRequest,
    CreateJobResponse,
    ErrorResponse,
    ExecuteJobResponse,
    JobResponse,
    MetricsSummaryResponse,
    RetryJobResponse,
    RunResponse,
)
from src.core.action_registry import ActionRegistry, UnknownAutomationActionError
from src.core.idempotency import DuplicateRequestError
from src.core.retry_manager import RetryLimitExceededError
from src.database.repository import AutomationRepository
from src.services.automation_service import AutomationService
from src.services.metrics_service import MetricsService
from src.services.run_service import RunService

router = APIRouter()


def get_repository() -> AutomationRepository:
    repository = AutomationRepository()
    repository.initialize()
    return repository


def get_automation_service() -> AutomationService:
    return AutomationService(get_repository())


def get_run_service() -> RunService:
    return RunService(get_repository())


def get_metrics_service() -> MetricsService:
    return MetricsService(get_repository())


@router.get("/health", tags=["Health"], response_model=dict[str, str])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "AutoServe API"}


@router.post(
    "/jobs",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateJobResponse,
    tags=["Jobs"],
    responses={409: {"model": ErrorResponse, "description": "Duplicate request ID"}},
)
def create_job(request: CreateJobRequest, service: AutomationService = Depends(get_automation_service)) -> CreateJobResponse:
    existing = service.get_job_by_request_id(request.request_id)
    if existing is not None:
        return CreateJobResponse(
            job_id=existing.id,
            request_id=existing.request_id,
            automation_type=existing.automation_type,
            status=existing.status.value,
            created_at=existing.created_at.isoformat(),
        )
    try:
        job = service.create_job(
            automation_type=request.automation_type,
            payload=request.payload,
            request_id=request.request_id,
        )
    except DuplicateRequestError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"error": "duplicate_request", "message": str(exc)}) from exc
    return CreateJobResponse(
        job_id=job.id,
        request_id=job.request_id,
        automation_type=job.automation_type,
        status=job.status.value,
        created_at=job.created_at.isoformat(),
    )


@router.get("/jobs", response_model=list[JobResponse], tags=["Jobs"])
def list_jobs(
    status: str | None = Query(default=None),
    automation_type: str | None = Query(default=None),
    service: AutomationService = Depends(get_automation_service),
) -> list[JobResponse]:
    jobs = service.list_jobs(status=status, automation_type=automation_type)
    return [
        JobResponse(
            id=job.id,
            request_id=job.request_id,
            automation_type=job.automation_type,
            payload=job.payload,
            status=job.status.value,
            retry_count=job.retry_count,
            created_at=job.created_at.isoformat(),
            updated_at=job.updated_at.isoformat(),
        )
        for job in jobs
    ]


@router.get("/jobs/{job_id}", response_model=JobResponse, tags=["Jobs"])
def get_job(job_id: str, service: AutomationService = Depends(get_automation_service)) -> JobResponse:
    job = service.get_job(job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "job_not_found", "message": f"Automation job '{job_id}' was not found."},
        )
    return JobResponse(
        id=job.id,
        request_id=job.request_id,
        automation_type=job.automation_type,
        payload=job.payload,
        status=job.status.value,
        retry_count=job.retry_count,
        created_at=job.created_at.isoformat(),
        updated_at=job.updated_at.isoformat(),
    )


@router.post("/jobs/{job_id}/execute", response_model=ExecuteJobResponse, tags=["Jobs"])
def execute_job(job_id: str, service: AutomationService = Depends(get_automation_service)) -> ExecuteJobResponse:
    try:
        result = service.execute_job(job_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "job_not_found", "message": str(exc)}) from exc
    except UnknownAutomationActionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "unknown_automation", "message": str(exc)}) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "invalid_state", "message": str(exc)}) from exc
    return ExecuteJobResponse(
        job_id=result["job_id"],
        run_id=result["run_id"],
        attempt_number=result["attempt_number"],
        status=result["status"],
        result=result["result"],
    )


@router.post("/jobs/{job_id}/retry", response_model=RetryJobResponse, tags=["Jobs"])
def retry_job(job_id: str, service: AutomationService = Depends(get_automation_service)) -> RetryJobResponse:
    try:
        result = service.retry_job(job_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "job_not_found", "message": str(exc)}) from exc
    except (RetryLimitExceededError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "retry_failed", "message": str(exc)}) from exc
    except UnknownAutomationActionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "unknown_automation", "message": str(exc)}) from exc
    return RetryJobResponse(
        job_id=result["job_id"],
        run_id=result["run_id"],
        attempt_number=result["attempt_number"],
        status=result["status"],
        result=result["result"],
    )


@router.get("/automations", response_model=AutomationListResponse, tags=["Automation"])
def list_automations() -> AutomationListResponse:
    return AutomationListResponse(automations=ActionRegistry.list_available())


@router.get("/runs", response_model=list[RunResponse], tags=["Runs"])
def list_runs(
    job_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    service: RunService = Depends(get_run_service),
) -> list[RunResponse]:
    runs = service.list_runs(job_id=job_id, status=status)
    return [
        RunResponse(
            id=run.id,
            job_id=run.job_id,
            status=run.status.value,
            attempt_number=run.attempt_number,
            started_at=run.started_at.isoformat(),
            completed_at=run.completed_at.isoformat() if run.completed_at else None,
            error_message=run.error_message,
        )
        for run in runs
    ]


@router.get("/runs/{run_id}", response_model=RunResponse, tags=["Runs"])
def get_run(run_id: str, service: RunService = Depends(get_run_service)) -> RunResponse:
    run = service.get_run(run_id)
    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "run_not_found", "message": f"Run '{run_id}' was not found."},
        )
    return RunResponse(
        id=run.id,
        job_id=run.job_id,
        status=run.status.value,
        attempt_number=run.attempt_number,
        started_at=run.started_at.isoformat(),
        completed_at=run.completed_at.isoformat() if run.completed_at else None,
        error_message=run.error_message,
    )


@router.get("/metrics/summary", response_model=MetricsSummaryResponse, tags=["Metrics"])
def metrics_summary(service: MetricsService = Depends(get_metrics_service)) -> MetricsSummaryResponse:
    data = service.get_summary()
    return MetricsSummaryResponse(**data)
