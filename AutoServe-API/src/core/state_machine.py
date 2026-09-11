from __future__ import annotations

from typing import Final

from src.models.automation import JobStatus


class StateTransitionError(ValueError):
    """Raised when a job transition violates the state machine."""


VALID_JOB_TRANSITIONS: Final[dict[JobStatus, tuple[JobStatus, ...]]] = {
    JobStatus.PENDING: (JobStatus.RUNNING,),
    JobStatus.RUNNING: (JobStatus.COMPLETED, JobStatus.FAILED),
    JobStatus.FAILED: (JobStatus.RUNNING,),
    JobStatus.COMPLETED: (),
}


def validate_transition(current: JobStatus, next_status: JobStatus) -> None:
    """Validate a single state transition for an automation job."""
    if current == next_status:
        raise StateTransitionError(f"Invalid transition: job already in {current.value} state.")
    allowed = VALID_JOB_TRANSITIONS.get(current, ())
    if next_status not in allowed:
        raise StateTransitionError(
            f"Invalid job transition from {current.value} to {next_status.value}."
        )


def can_retry(status: JobStatus) -> bool:
    return status == JobStatus.FAILED


def is_terminal(status: JobStatus) -> bool:
    return status == JobStatus.COMPLETED
