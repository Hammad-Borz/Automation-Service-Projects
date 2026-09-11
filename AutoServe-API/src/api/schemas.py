from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateJobRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    automation_type: str = Field(..., min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)
    request_id: str = Field(..., min_length=1)

    @field_validator("automation_type")
    @classmethod
    def validate_automation_type(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("automation_type cannot be empty")
        return value

    @field_validator("request_id")
    @classmethod
    def validate_request_id(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("request_id cannot be empty")
        if len(value) < 3:
            raise ValueError("request_id must be at least 3 characters")
        return value

    @field_validator("payload")
    @classmethod
    def validate_payload(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError("payload must be a JSON object")
        if not value:
            raise ValueError("payload cannot be empty")
        return value


class CreateJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_id: str
    request_id: str
    automation_type: str
    status: str
    created_at: str


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    request_id: str
    automation_type: str
    payload: dict[str, Any]
    status: str
    retry_count: int
    created_at: str
    updated_at: str


class RunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    job_id: str
    status: str
    attempt_number: int
    started_at: str
    completed_at: str | None = None
    error_message: str | None = None


class ActionResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    run_id: str
    action_type: str
    success: bool
    result: dict[str, Any]
    error_message: str | None = None
    created_at: str


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    job_id: str | None = None
    run_id: str | None = None
    event_type: str
    message: str
    metadata: dict[str, Any]
    created_at: str


class MetricsSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_jobs: int
    pending_jobs: int
    running_jobs: int
    completed_jobs: int
    failed_jobs: int
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate: float


class ErrorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    error: str
    message: str


class ExecuteJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_id: str
    run_id: str
    attempt_number: int
    status: str
    result: dict[str, Any]


class RetryJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_id: str
    run_id: str
    attempt_number: int
    status: str
    result: dict[str, Any]
    error_message: str | None = None


class AutomationListResponse(BaseModel):
    automations: list[str]
