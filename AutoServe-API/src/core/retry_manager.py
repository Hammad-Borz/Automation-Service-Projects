from __future__ import annotations

from dataclasses import dataclass

from src.config import MAX_RETRY_COUNT
from src.models.automation import JobStatus


class RetryLimitExceededError(RuntimeError):
    """Raised when a failed job exceeds the configured retry limit."""


@dataclass(slots=True)
class RetryDecision:
    can_retry: bool
    retry_count: int
    attempt_number: int
    next_status: JobStatus


def can_process_retry(current_retry_count: int, max_retries: int = MAX_RETRY_COUNT) -> bool:
    return current_retry_count < max_retries


def build_retry_state(current_retry_count: int, max_retries: int = MAX_RETRY_COUNT) -> RetryDecision:
    if current_retry_count >= max_retries:
        raise RetryLimitExceededError(
            f"Retry limit reached: {current_retry_count}/{max_retries}."
        )
    return RetryDecision(
        can_retry=True,
        retry_count=current_retry_count + 1,
        attempt_number=current_retry_count + 1,
        next_status=JobStatus.RUNNING,
    )
