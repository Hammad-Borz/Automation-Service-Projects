from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class DuplicateRequestError(ValueError):
    """Raised when a request ID already exists for a processed job."""


@dataclass(frozen=True)
class IdempotencyResult:
    existing_job_id: str | None
    created: bool
    response_status: int


def normalize_request_id(request_id: str) -> str:
    value = request_id.strip()
    if not value:
        raise ValueError("request_id cannot be empty")
    return value


def ensure_unique_request_id(existing_job: Any | None) -> None:
    if existing_job is not None:
        raise DuplicateRequestError(f"Request ID already exists for job {existing_job.id}.")
