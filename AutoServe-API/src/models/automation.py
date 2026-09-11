from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class RunStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AuditEvent(str, Enum):
    JOB_CREATED = "JOB_CREATED"
    JOB_STARTED = "JOB_STARTED"
    JOB_COMPLETED = "JOB_COMPLETED"
    JOB_FAILED = "JOB_FAILED"
    JOB_RETRIED = "JOB_RETRIED"
    ACTION_EXECUTED = "ACTION_EXECUTED"
    ACTION_FAILED = "ACTION_FAILED"
    ACTION_RESULT_SAVED = "ACTION_RESULT_SAVED"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).isoformat()


@dataclass(slots=True)
class AutomationJob:
    id: str
    request_id: str
    automation_type: str
    payload: dict[str, Any]
    status: JobStatus
    retry_count: int = 0
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "AutomationJob":
        return cls(
            id=row["id"],
            request_id=row["request_id"],
            automation_type=row["automation_type"],
            payload=json.loads(row["payload"] if isinstance(row["payload"], str) else json.dumps(row["payload"])),
            status=JobStatus(row["status"]),
            retry_count=int(row.get("retry_count", 0)),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def to_record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "request_id": self.request_id,
            "automation_type": self.automation_type,
            "payload": json.dumps(self.payload),
            "status": self.status.value,
            "retry_count": self.retry_count,
            "created_at": to_iso(self.created_at),
            "updated_at": to_iso(self.updated_at),
        }


@dataclass(slots=True)
class AutomationRun:
    id: str
    job_id: str
    status: RunStatus
    attempt_number: int
    started_at: datetime = field(default_factory=utc_now)
    completed_at: datetime | None = None
    error_message: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "AutomationRun":
        completed_at = row.get("completed_at")
        return cls(
            id=row["id"],
            job_id=row["job_id"],
            status=RunStatus(row["status"]),
            attempt_number=int(row.get("attempt_number", 1)),
            started_at=datetime.fromisoformat(row["started_at"]),
            completed_at=datetime.fromisoformat(completed_at) if completed_at else None,
            error_message=row.get("error_message"),
        )

    def to_record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "job_id": self.job_id,
            "status": self.status.value,
            "attempt_number": self.attempt_number,
            "started_at": to_iso(self.started_at),
            "completed_at": to_iso(self.completed_at),
            "error_message": self.error_message,
        }


@dataclass(slots=True)
class ActionResult:
    id: str
    run_id: str
    action_type: str
    success: bool
    result: dict[str, Any]
    error_message: str | None = None
    created_at: datetime = field(default_factory=utc_now)

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "ActionResult":
        return cls(
            id=row["id"],
            run_id=row["run_id"],
            action_type=row["action_type"],
            success=bool(row.get("success", False)),
            result=json.loads(row["result"] if isinstance(row["result"], str) else json.dumps(row["result"])),
            error_message=row.get("error_message"),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def to_record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "run_id": self.run_id,
            "action_type": self.action_type,
            "success": self.success,
            "result": json.dumps(self.result),
            "error_message": self.error_message,
            "created_at": to_iso(self.created_at),
        }


@dataclass(slots=True)
class AuditLog:
    id: str
    job_id: str | None
    run_id: str | None
    event_type: str
    message: str
    metadata: dict[str, Any]
    created_at: datetime = field(default_factory=utc_now)

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "AuditLog":
        return cls(
            id=row["id"],
            job_id=row.get("job_id"),
            run_id=row.get("run_id"),
            event_type=row["event_type"],
            message=row["message"],
            metadata=json.loads(row["metadata"] if isinstance(row["metadata"], str) else json.dumps(row["metadata"])),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def to_record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "job_id": self.job_id,
            "run_id": self.run_id,
            "event_type": self.event_type,
            "message": self.message,
            "metadata": json.dumps(self.metadata),
            "created_at": to_iso(self.created_at),
        }
