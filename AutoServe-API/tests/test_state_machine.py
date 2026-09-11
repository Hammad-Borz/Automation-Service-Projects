import pytest

from src.core.state_machine import StateTransitionError, validate_transition
from src.models.automation import JobStatus


def test_valid_jobs_transitions():
    validate_transition(JobStatus.PENDING, JobStatus.RUNNING)
    validate_transition(JobStatus.RUNNING, JobStatus.COMPLETED)
    validate_transition(JobStatus.RUNNING, JobStatus.FAILED)
    validate_transition(JobStatus.FAILED, JobStatus.RUNNING)


def test_invalid_transition_raises_error():
    with pytest.raises(StateTransitionError):
        validate_transition(JobStatus.COMPLETED, JobStatus.FAILED)


def test_completed_job_protection():
    with pytest.raises(StateTransitionError):
        validate_transition(JobStatus.COMPLETED, JobStatus.RUNNING)
